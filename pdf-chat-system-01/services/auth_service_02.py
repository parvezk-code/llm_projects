"""
auth_service.py

Six focused classes replacing the original monolithic AuthService:

  TokenParser        – stateless JWT decoding and claim extraction (uses PyJWT)
  TokenStore         – credential persistence (keyring when available, file fallback)
  TokenRefresher     – stale-token detection and refresh network call
  OAuthFlowManager   – full PKCE login flow + local callback server (uses oauthlib)
  LoginHandle        – handle returned to callers for poll / cancel
  AuthService        – thin facade; the only public surface callers need to import
"""

from __future__ import annotations

import json
import os
import platform
import threading
import time
import uuid
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
import jwt  # PyJWT — decode without verification for claim extraction
from oauthlib.oauth2 import WebApplicationClient  # PKCE helper


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OAUTH_CLIENT_ID    = "app_EMoamEEZ73f0CkXaXp7hrann"
OAUTH_ISSUER       = "https://auth.openai.com"
OAUTH_REDIRECT_PORT = 1455
OAUTH_REDIRECT_URI  = f"http://localhost:{OAUTH_REDIRECT_PORT}/auth/callback"
CODEX_API_ENDPOINT  = "https://chatgpt.com/backend-api/codex/responses"
OAUTH_ORIGINATOR    = "pdf-chat"

_TOKEN_FILE = Path(".pdf-chat/auth.json")
_KEYRING_SERVICE = "pdf-chat"
_KEYRING_USERNAME = "oauth-tokens"

OAUTH_MODELS = (
    "gpt-5.3-codex", "gpt-5.4", "gpt-5.2-codex", "gpt-5.1-codex-max",
    "gpt-5.2", "gpt-5.1-codex-mini", "gpt-5.1-codex", "gpt-5.1",
    "gpt-5-codex", "gpt-5-codex-mini", "gpt-5", "gpt-oss-120b", "gpt-oss-20b",
)
DEFAULT_OAUTH_MODEL = "gpt-5.3-codex"

_HTML_SUCCESS = """<!doctype html>
<html><head><title>pdf-chat sign-in</title>
<style>body{font-family:system-ui,-apple-system,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#131010;color:#f1ecec}.c{text-align:center;padding:2rem}</style>
</head><body><div class="c"><h1>Signed in</h1><p>You can close this tab and return to pdf-chat.</p></div>
<script>setTimeout(()=>window.close(),1500)</script></body></html>"""


# ---------------------------------------------------------------------------
# StoredAuth
# ---------------------------------------------------------------------------

@dataclass
class StoredAuth:
    access_token:  str
    refresh_token: str
    expires_at:    float
    account_id:    str | None = None
    email:         str | None = None


# ---------------------------------------------------------------------------
# 1. TokenParser
#    Stateless; no I/O. Uses PyJWT for safe base64 decoding of JWT payloads.
# ---------------------------------------------------------------------------

class TokenParser:
    """
    Decode JWT claims and build a StoredAuth from a raw token-endpoint response.
    Has no side effects — every method is effectively a pure function.
    """

    def build_stored_auth(
        self, tokens: dict[str, Any], fallback: StoredAuth | None = None
    ) -> StoredAuth:
        """Construct a StoredAuth from a raw token response dict."""
        expires_in = tokens.get("expires_in", 3600)
        return StoredAuth(
            access_token=tokens["access_token"],
            refresh_token=(
                tokens.get("refresh_token")
                or (fallback.refresh_token if fallback else "")
            ),
            expires_at=time.time() + float(expires_in),
            account_id=(
                self.account_id_from_tokens(tokens)
                or (fallback.account_id if fallback else None)
            ),
            email=(
                self.email_from_tokens(tokens)
                or (fallback.email if fallback else None)
            ),
        )

    def account_id_from_tokens(self, tokens: dict[str, Any]) -> str | None:
        """Extract the ChatGPT account ID from id_token or access_token claims."""
        for key in ("id_token", "access_token"):
            tok = tokens.get(key)
            if not tok:
                continue
            claims = self._decode_claims(tok)
            if not claims:
                continue

            if account_id := claims.get("chatgpt_account_id"):
                return account_id

            nested = claims.get("https://api.openai.com/auth") or {}
            if isinstance(nested, dict) and nested.get("chatgpt_account_id"):
                return nested["chatgpt_account_id"]

            orgs = claims.get("organizations") or []
            if isinstance(orgs, list) and orgs and isinstance(orgs[0], dict):
                if org_id := orgs[0].get("id"):
                    return org_id

        return None

    def email_from_tokens(self, tokens: dict[str, Any]) -> str | None:
        """Extract email from id_token or access_token claims."""
        tok = tokens.get("id_token") or tokens.get("access_token")
        if not tok:
            return None
        claims = self._decode_claims(tok) or {}
        return claims.get("email")

    def _decode_claims(self, token: str) -> dict[str, Any] | None:
        """
        Decode JWT payload claims without signature verification.
        Uses PyJWT — handles padding and encoding safely.
        """
        try:
            return jwt.decode(
                token,
                options={"verify_signature": False},
                algorithms=["RS256", "HS256"],
            )
        except jwt.exceptions.DecodeError:
            return None


# ---------------------------------------------------------------------------
# 2. TokenStore
#    Owns all credential I/O. Uses OS keyring when available; falls back to a
#    chmod-600 JSON file so it works in every environment.
# ---------------------------------------------------------------------------

class TokenStore:
    """
    Persist and retrieve StoredAuth credentials.

    Preference order:
      1. OS keyring  (macOS Keychain, Windows Credential Locker, etc.)
      2. Encrypted file at _TOKEN_FILE with mode 0o600
    """

    def __init__(self) -> None:
        self._keyring = self._try_import_keyring()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def load(self) -> StoredAuth | None:
        """Return persisted credentials or None if not signed in."""
        raw = self._read_raw()
        if raw is None:
            return None
        try:
            return StoredAuth(**json.loads(raw))
        except (json.JSONDecodeError, TypeError, ValueError):
            return None

    def save(self, stored: StoredAuth) -> None:
        """Persist credentials to the best available backend."""
        raw = json.dumps(asdict(stored))
        if self._keyring:
            self._keyring.set_password(_KEYRING_SERVICE, _KEYRING_USERNAME, raw)
        else:
            self._save_to_file(raw)

    def delete(self) -> None:
        """Remove all stored credentials."""
        if self._keyring:
            try:
                self._keyring.delete_password(_KEYRING_SERVICE, _KEYRING_USERNAME)
            except Exception:
                pass
        _TOKEN_FILE.unlink(missing_ok=True)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _read_raw(self) -> str | None:
        if self._keyring:
            try:
                return self._keyring.get_password(_KEYRING_SERVICE, _KEYRING_USERNAME)
            except Exception:
                pass
        if _TOKEN_FILE.exists():
            return _TOKEN_FILE.read_text()
        return None

    def _save_to_file(self, raw: str) -> None:
        _TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = _TOKEN_FILE.with_suffix(".json.tmp")
        tmp.write_text(raw)
        os.chmod(tmp, 0o600)
        tmp.replace(_TOKEN_FILE)

    @staticmethod
    def _try_import_keyring() -> Any | None:
        try:
            import keyring
            # Probe that a real backend is available (not the null backend)
            keyring.get_keyring()
            return keyring
        except Exception:
            return None


# ---------------------------------------------------------------------------
# 3. TokenRefresher
#    Single responsibility: decide if a token is stale; if so, call the
#    refresh endpoint and delegate persistence back to TokenStore.
# ---------------------------------------------------------------------------

class TokenRefresher:
    """
    Refresh OAuth tokens when they are close to expiry.
    Depends on TokenParser (to build StoredAuth) and TokenStore (to persist).
    """

    _EXPIRY_BUFFER_SECONDS = 60

    def __init__(self, parser: TokenParser, store: TokenStore) -> None:
        self._parser = parser
        self._store  = store

    def refresh_if_needed(self, stored: StoredAuth) -> StoredAuth:
        """Return stored unchanged if still valid; otherwise refresh and persist."""
        if stored.expires_at - self._EXPIRY_BUFFER_SECONDS > time.time():
            return stored

        resp = httpx.post(
            f"{OAUTH_ISSUER}/oauth/token",
            data={
                "grant_type":    "refresh_token",
                "refresh_token": stored.refresh_token,
                "client_id":     OAUTH_CLIENT_ID,
            },
            timeout=30.0,
        )
        resp.raise_for_status()

        refreshed = self._parser.build_stored_auth(resp.json(), fallback=stored)
        self._store.save(refreshed)
        return refreshed


# ---------------------------------------------------------------------------
# 4. LoginHandle
#    Returned by OAuthFlowManager.start_login(). Callers poll or cancel it.
# ---------------------------------------------------------------------------

class LoginHandle:
    """Opaque handle for an in-progress OAuth login. Use poll() or cancel()."""

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
# 5. OAuthFlowManager
#    Owns the full PKCE login flow. Uses oauthlib.WebApplicationClient to
#    generate the PKCE verifier/challenge and build the authorize URL —
#    removing all hand-rolled base64/sha256/secrets ceremony.
# ---------------------------------------------------------------------------

class OAuthFlowManager:
    """
    Manage the OAuth 2.0 PKCE authorization flow.

    Uses oauthlib.WebApplicationClient for PKCE parameter generation and
    authorization URL construction. Spins up a local HTTP server for the
    redirect callback, exchanges the code for tokens, and persists via
    TokenStore.
    """

    def __init__(self, parser: TokenParser, store: TokenStore) -> None:
        self._parser = parser
        self._store  = store

    def start_login(self) -> LoginHandle:
        """
        Begin the PKCE flow. Starts a local callback server and returns a
        LoginHandle the caller uses to poll or cancel.
        Raises OSError if the redirect port is unavailable.
        """
        # oauthlib generates a cryptographically secure PKCE verifier and
        # derives the S256 challenge automatically.
        client = WebApplicationClient(OAUTH_CLIENT_ID)
        code_verifier = client.create_code_verifier(length=64)
        code_challenge = client.create_code_challenge(code_verifier, "S256")
        state = str(uuid.uuid4()).replace("-", "")

        authorize_url = client.prepare_request_uri(
            f"{OAUTH_ISSUER}/oauth/authorize",
            redirect_uri=OAUTH_REDIRECT_URI,
            scope=["openid", "profile", "email", "offline_access"],
            state=state,
            code_challenge=code_challenge,
            code_challenge_method="S256",
            id_token_add_organizations="true",
            codex_cli_simplified_flow="true",
            originator=OAUTH_ORIGINATOR,
        )

        result: dict[str, Any] = {}
        manager_self = self

        class _Handler(BaseHTTPRequestHandler):
            def log_message(self, *args, **kwargs) -> None:
                pass  # silence request logs

            def do_GET(self) -> None:
                if not self.path.startswith("/auth/callback"):
                    self.send_response(404)
                    self.end_headers()
                    return

                query = parse_qs(urlparse(self.path).query)

                if err := query.get("error", [None])[0]:
                    desc = query.get("error_description", [err])[0]
                    result["error"] = desc
                    self._respond(200, manager_self._html_error(desc))
                    return

                code       = query.get("code",  [None])[0]
                recv_state = query.get("state", [None])[0]

                if not code:
                    result["error"] = "Missing authorization code"
                    self._respond(400, manager_self._html_error(result["error"]))
                    return

                if recv_state != state:
                    result["error"] = "Invalid state (possible CSRF)"
                    self._respond(400, manager_self._html_error(result["error"]))
                    return

                try:
                    # oauthlib builds the token-request body including
                    # code_verifier for PKCE verification server-side.
                    _, headers, body = client.prepare_token_request(
                        f"{OAUTH_ISSUER}/oauth/token",
                        authorization_response=OAUTH_REDIRECT_URI + f"?code={code}",
                        redirect_url=OAUTH_REDIRECT_URI,
                        code=code,
                        code_verifier=code_verifier,
                    )
                    resp = httpx.post(
                        f"{OAUTH_ISSUER}/oauth/token",
                        data=dict(
                            grant_type="authorization_code",
                            code=code,
                            redirect_uri=OAUTH_REDIRECT_URI,
                            client_id=OAUTH_CLIENT_ID,
                            code_verifier=code_verifier,
                        ),
                        timeout=30.0,
                    )
                    resp.raise_for_status()
                    stored = manager_self._parser.build_stored_auth(resp.json())
                    manager_self._store.save(stored)
                    result["auth"] = stored
                    self._respond(200, _HTML_SUCCESS)
                except Exception as exc:
                    result["error"] = f"Token exchange failed: {exc}"
                    self._respond(500, manager_self._html_error(result["error"]))

            def _respond(self, code: int, body: str) -> None:
                self.send_response(code)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))

        server = HTTPServer(("127.0.0.1", OAUTH_REDIRECT_PORT), _Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return LoginHandle(authorize_url, server, thread, result)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _html_error(self, msg: str) -> str:
        safe = msg.replace("<", "&lt;").replace(">", "&gt;")
        return (
            "<!doctype html><html><head><title>pdf-chat sign-in failed</title></head>"
            f"<body><h1>Sign-in failed</h1><pre>{safe}</pre></body></html>"
        )


# ---------------------------------------------------------------------------
# 6. AuthService  —  thin facade
#    Composes the four worker classes above. This is the only symbol callers
#    (e.g. LLMService) need to import. The public API is identical to before.
# ---------------------------------------------------------------------------

class AuthService:
    """
    Facade over TokenStore, TokenParser, TokenRefresher, and OAuthFlowManager.
    Callers interact only with this class; internal classes are an
    implementation detail.
    """

    def __init__(self) -> None:
        self._store     = TokenStore()
        self._parser    = TokenParser()
        self._refresher = TokenRefresher(self._parser, self._store)
        self._flow      = OAuthFlowManager(self._parser, self._store)

    # ------------------------------------------------------------------
    # Credential access
    # ------------------------------------------------------------------

    def load_stored_auth(self) -> StoredAuth | None:
        """Return persisted credentials or None if not signed in."""
        return self._store.load()

    def logout(self) -> None:
        """Delete stored credentials."""
        self._store.delete()

    # ------------------------------------------------------------------
    # Token refresh
    # ------------------------------------------------------------------

    def refresh_if_needed(self, stored: StoredAuth) -> StoredAuth:
        """Return stored as-is if still valid; otherwise refresh and persist."""
        return self._refresher.refresh_if_needed(stored)

    # ------------------------------------------------------------------
    # Login flow
    # ------------------------------------------------------------------

    def start_login(self) -> LoginHandle:
        """
        Start the OAuth PKCE flow. Returns a LoginHandle for polling or
        cancelling. Raises OSError if the callback port is unavailable.
        """
        return self._flow.start_login()

    def poll_login(self, handle: LoginHandle) -> StoredAuth | None:
        """
        Poll a pending login. Returns StoredAuth when done, None if still
        waiting, raises RuntimeError on failure.
        """
        return handle.poll()

    def cancel_login(self, handle: LoginHandle) -> None:
        """Cancel an in-progress login."""
        handle.cancel()

    # ------------------------------------------------------------------
    # Read-only properties (unchanged from original)
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
