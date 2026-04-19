from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import threading
import time
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, parse_qs, urlparse

import httpx


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OAUTH_CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
OAUTH_ISSUER = "https://auth.openai.com"
OAUTH_REDIRECT_PORT = 1455
OAUTH_REDIRECT_URI = f"http://localhost:{OAUTH_REDIRECT_PORT}/auth/callback"
CODEX_API_ENDPOINT = "https://chatgpt.com/backend-api/codex/responses"
OAUTH_ORIGINATOR = "pdf-chat"

_TOKEN_FILE = Path(".pdf-chat/auth.json")

OAUTH_MODELS = (
    "gpt-5.3-codex",
    "gpt-5.4",
    "gpt-5.2-codex",
    "gpt-5.1-codex-max",
    "gpt-5.2",
    "gpt-5.1-codex-mini",
    "gpt-5.1-codex",
    "gpt-5.1",
    "gpt-5-codex",
    "gpt-5-codex-mini",
    "gpt-5",
    "gpt-oss-120b",
    "gpt-oss-20b",
)
DEFAULT_OAUTH_MODEL = "gpt-5.3-codex"

_HTML_SUCCESS = """<!doctype html>
<html><head><title>pdf-chat sign-in</title>
<style>body{font-family:system-ui,-apple-system,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#131010;color:#f1ecec}.c{text-align:center;padding:2rem}</style>
</head><body><div class="c"><h1>Signed in</h1><p>You can close this tab and return to pdf-chat.</p></div>
<script>setTimeout(()=>window.close(),1500)</script></body></html>"""


# ---------------------------------------------------------------------------
# StoredAuth dataclass
# ---------------------------------------------------------------------------

@dataclass
class StoredAuth:
    access_token: str
    refresh_token: str
    expires_at: float
    account_id: str | None = None
    email: str | None = None



# ---------------------------------------------------------------------------
# AuthService — thin facade, preserves the original public API exactly
# ---------------------------------------------------------------------------

class AuthService:
    """
    Thin facade that composes TokenStore, TokenParser, TokenRefresher, and
    OAuthFlowManager. Exposes the exact same public API as the original
    monolithic AuthService — callers require zero changes.
    """

    def __init__(self) -> None:
        self._store = TokenStore()
        self._parser = TokenParser()
        self._refresher = TokenRefresher(self._parser, self._store)
        self._flow = OAuthFlowManager(self._parser, self._store)

    # ------------------------------------------------------------------
    # Public API (identical signatures to the original)
    # ------------------------------------------------------------------

    def load_stored_auth(self) -> StoredAuth | None:
        return self._store.load()

    def logout(self) -> None:
        self._store.delete()

    def start_login(self) -> LoginHandle:
        return self._flow.start_login()

    def cancel_login(self, handle: LoginHandle) -> None:
        handle.cancel()

    def poll_login(self, handle: LoginHandle) -> StoredAuth | None:
        return handle.poll()

    def refresh_if_needed(self, stored: StoredAuth) -> StoredAuth:
        return self._refresher.refresh_if_needed(stored)

    # ------------------------------------------------------------------
    # Properties (identical to the original)
    # ------------------------------------------------------------------

    @property
    def redirect_port(self) -> int:
        return OAUTH_REDIRECT_PORT

    @property
    def default_model(self) -> str:
        return DEFAULT_OAUTH_MODEL

    @property
    def oauth_models(self) -> list[str]:
        return list(OAUTH_MODELS)


# ---------------------------------------------------------------------------
# TokenStore — filesystem persistence only
# ---------------------------------------------------------------------------

class TokenStore:
    """Reads and writes StoredAuth to disk. The only class that touches the filesystem."""

    def __init__(self, token_file: Path = _TOKEN_FILE) -> None:
        self._token_file = token_file

    def load(self) -> StoredAuth | None:
        """Return persisted credentials or None if not signed in."""
        if not self._token_file.exists():
            return None
        try:
            data = json.loads(self._token_file.read_text())
            return StoredAuth(**data)
        except (json.JSONDecodeError, TypeError, ValueError):
            return None

    def save(self, stored: StoredAuth) -> None:
        """Write credentials to disk atomically with restricted permissions."""
        self._token_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._token_file.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(asdict(stored), indent=2))
        os.chmod(tmp, 0o600)
        tmp.replace(self._token_file)

    def delete(self) -> None:
        """Delete stored credentials from disk."""
        self._token_file.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# TokenParser — stateless JWT decoding and claim extraction
# ---------------------------------------------------------------------------

class TokenParser:
    """Stateless utility for decoding JWTs and building StoredAuth from raw token dicts."""

    def build_stored_auth(
        self, tokens: dict[str, Any], fallback: StoredAuth | None = None
    ) -> StoredAuth:
        """Construct a StoredAuth from a raw token response dict."""
        expires_in = tokens.get("expires_in", 3600)
        return StoredAuth(
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token")
            or (fallback.refresh_token if fallback else ""),
            expires_at=time.time() + float(expires_in),
            account_id=self._account_id_from_tokens(tokens)
            or (fallback.account_id if fallback else None),
            email=self._email_from_tokens(tokens)
            or (fallback.email if fallback else None),
        )

    def _account_id_from_tokens(self, tokens: dict[str, Any]) -> str | None:
        """Extract the ChatGPT account ID from id_token or access_token claims."""
        for key in ("id_token", "access_token"):
            tok = tokens.get(key)
            if not tok:
                continue
            claims = self._parse_jwt_claims(tok)
            if not claims:
                continue

            account_id = claims.get("chatgpt_account_id")
            if account_id:
                return account_id

            nested = claims.get("https://api.openai.com/auth") or {}
            if isinstance(nested, dict) and nested.get("chatgpt_account_id"):
                return nested["chatgpt_account_id"]

            orgs = claims.get("organizations") or []
            if isinstance(orgs, list) and orgs and isinstance(orgs[0], dict):
                org_id = orgs[0].get("id")
                if org_id:
                    return org_id

        return None

    def _email_from_tokens(self, tokens: dict[str, Any]) -> str | None:
        """Extract the email address from id_token or access_token claims."""
        tok = tokens.get("id_token") or tokens.get("access_token")
        if not tok:
            return None
        claims = self._parse_jwt_claims(tok) or {}
        return claims.get("email")

    def _parse_jwt_claims(self, token: str) -> dict[str, Any] | None:
        """Decode and return the payload claims of a JWT without verification."""
        parts = token.split(".")
        if len(parts) != 3:
            return None
        try:
            payload = parts[1] + "=" * (-len(parts[1]) % 4)
            return json.loads(base64.urlsafe_b64decode(payload))
        except (ValueError, json.JSONDecodeError):
            return None


# ---------------------------------------------------------------------------
# TokenRefresher — token expiry checks and refresh network calls
# ---------------------------------------------------------------------------

class TokenRefresher:
    """Decides if a token is stale and performs the refresh network call."""

    def __init__(self, parser: TokenParser, store: TokenStore) -> None:
        self._parser = parser
        self._store = store

    def refresh_if_needed(self, stored: StoredAuth) -> StoredAuth:
        """Return stored as-is if still valid; otherwise refresh and persist."""
        if stored.expires_at - 60 > time.time():
            return stored

        resp = httpx.post(
            f"{OAUTH_ISSUER}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": stored.refresh_token,
                "client_id": OAUTH_CLIENT_ID,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        tokens = resp.json()

        refreshed = self._parser.build_stored_auth(tokens, fallback=stored)
        self._store.save(refreshed)
        return refreshed


# ---------------------------------------------------------------------------
# LoginHandle
# ---------------------------------------------------------------------------

class LoginHandle:
    """Returned by OAuthFlowManager.start_login(). Used to poll or cancel the flow."""

    def __init__(
        self,
        authorize_url: str,
        server: HTTPServer,
        thread: threading.Thread,
        result: dict,
    ) -> None:
        self.authorize_url = authorize_url
        self._server = server
        self._thread = thread
        self._result = result

    def poll(self) -> StoredAuth | None:
        """Return StoredAuth when complete, None if still pending, raise on error."""
        if self._result.get("error"):
            raise RuntimeError(self._result["error"])
        stored = self._result.get("auth")
        if stored is not None:
            self._shutdown()
        return stored

    def cancel(self) -> None:
        self._result.setdefault("error", "Sign-in cancelled")
        self._shutdown()

    def _shutdown(self) -> None:
        if self._result.get("closed"):
            return
        self._result["closed"] = True
        try:
            self._server.shutdown()
            self._server.server_close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# OAuthFlowManager — PKCE login flow and local callback server
# ---------------------------------------------------------------------------

class OAuthFlowManager:
    """
    Manages the full PKCE login flow: generates verifier/challenge, builds
    the authorize URL, spins up the local HTTP callback server, and handles
    the authorization code exchange.
    """

    def __init__(self, parser: TokenParser, store: TokenStore) -> None:
        self._parser = parser
        self._store = store

    def start_login(self) -> LoginHandle:
        """
        Start the OAuth PKCE flow. Opens a local callback server and
        returns a LoginHandle the caller uses to poll or cancel.
        Raises OSError if the callback server port is unavailable.
        """
        verifier, challenge = self._generate_pkce_pair()
        state = self._generate_state()
        authorize_url = self._build_authorize_url(challenge, state)

        result: dict[str, Any] = {}
        handler_class = self._make_handler_class(state, verifier, result)

        server = HTTPServer(("127.0.0.1", OAUTH_REDIRECT_PORT), handler_class)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return LoginHandle(authorize_url, server, thread, result)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _generate_pkce_pair(self) -> tuple[str, str]:
        """Generate a PKCE verifier and its S256 challenge."""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
        verifier = "".join(secrets.choice(alphabet) for _ in range(43))
        challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(verifier.encode("ascii")).digest()
            )
            .rstrip(b"=")
            .decode("ascii")
        )
        return verifier, challenge

    def _generate_state(self) -> str:
        """Generate a random CSRF state token."""
        return (
            base64.urlsafe_b64encode(secrets.token_bytes(32))
            .rstrip(b"=")
            .decode("ascii")
        )

    def _build_authorize_url(self, challenge: str, state: str) -> str:
        """Construct the full OAuth authorize URL with PKCE params."""
        params = {
            "response_type": "code",
            "client_id": OAUTH_CLIENT_ID,
            "redirect_uri": OAUTH_REDIRECT_URI,
            "scope": "openid profile email offline_access",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "id_token_add_organizations": "true",
            "codex_cli_simplified_flow": "true",
            "state": state,
            "originator": OAUTH_ORIGINATOR,
        }
        return f"{OAUTH_ISSUER}/oauth/authorize?{urlencode(params)}"

    def _make_handler_class(self, state: str, verifier: str, result: dict):
        """Build and return the HTTP callback handler class, closing over flow state."""
        parser = self._parser
        store = self._store

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args, **kwargs) -> None:
                pass

            def do_GET(self) -> None:
                if not self.path.startswith("/auth/callback"):
                    self.send_response(404)
                    self.end_headers()
                    return

                query = parse_qs(urlparse(self.path).query)

                err = query.get("error", [None])[0]
                if err:
                    desc = query.get("error_description", [err])[0]
                    result["error"] = desc
                    self._respond(200, _html_error(desc))
                    return

                code = query.get("code", [None])[0]
                recv_state = query.get("state", [None])[0]
                if not code:
                    result["error"] = "Missing authorization code"
                    self._respond(400, _html_error(result["error"]))
                    return
                if recv_state != state:
                    result["error"] = "Invalid state (possible CSRF)"
                    self._respond(400, _html_error(result["error"]))
                    return

                try:
                    resp = httpx.post(
                        f"{OAUTH_ISSUER}/oauth/token",
                        data={
                            "grant_type": "authorization_code",
                            "code": code,
                            "redirect_uri": OAUTH_REDIRECT_URI,
                            "client_id": OAUTH_CLIENT_ID,
                            "code_verifier": verifier,
                        },
                        timeout=30.0,
                    )
                    resp.raise_for_status()
                    tokens = resp.json()

                    stored = parser.build_stored_auth(tokens)
                    store.save(stored)
                    result["auth"] = stored
                    self._respond(200, _HTML_SUCCESS)
                except Exception as e:
                    result["error"] = f"Token exchange failed: {e}"
                    self._respond(500, _html_error(result["error"]))

            def _respond(self, code: int, body: str) -> None:
                self.send_response(code)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))

        return Handler


def _html_error(msg: str) -> str:
    """Module-level helper: returns an HTML error page for the OAuth callback server."""
    safe = msg.replace("<", "&lt;").replace(">", "&gt;")
    return (
        "<!doctype html><html><head><title>pdf-chat sign-in failed</title></head>"
        f"<body><h1>Sign-in failed</h1><pre>{safe}</pre></body></html>"
    )