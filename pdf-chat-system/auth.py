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
from urllib.parse import urlencode

import httpx


OAUTH_CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
OAUTH_ISSUER = "https://auth.openai.com"
OAUTH_REDIRECT_PORT = 1455
OAUTH_REDIRECT_URI = f"http://localhost:{OAUTH_REDIRECT_PORT}/auth/callback"
CODEX_API_ENDPOINT = "https://chatgpt.com/backend-api/codex/responses"
OAUTH_ORIGINATOR = "pdf-chat"

TOKEN_FILE = Path(".pdf-chat/auth.json")

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


@dataclass
class StoredAuth:
    access_token: str
    refresh_token: str
    expires_at: float
    account_id: str | None = None
    email: str | None = None


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce() -> tuple[str, str]:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    verifier = "".join(secrets.choice(alphabet) for _ in range(43))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def generate_state() -> str:
    return _b64url(secrets.token_bytes(32))


def build_authorize_url(redirect_uri: str, pkce_challenge: str, state: str) -> str:
    params = {
        "response_type": "code",
        "client_id": OAUTH_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email offline_access",
        "code_challenge": pkce_challenge,
        "code_challenge_method": "S256",
        "id_token_add_organizations": "true",
        "codex_cli_simplified_flow": "true",
        "state": state,
        "originator": OAUTH_ORIGINATOR,
    }
    return f"{OAUTH_ISSUER}/oauth/authorize?{urlencode(params)}"


def parse_jwt_claims(token: str) -> dict[str, Any] | None:
    parts = token.split(".")
    if len(parts) != 3:
        return None
    try:
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))
    except (ValueError, json.JSONDecodeError):
        return None


def extract_account_id(claims: dict[str, Any]) -> str | None:
    direct = claims.get("chatgpt_account_id")
    if direct:
        return direct
    nested = claims.get("https://api.openai.com/auth") or {}
    if isinstance(nested, dict) and nested.get("chatgpt_account_id"):
        return nested["chatgpt_account_id"]
    orgs = claims.get("organizations") or []
    if isinstance(orgs, list) and orgs and isinstance(orgs[0], dict):
        return orgs[0].get("id")
    return None


def _account_id_from_tokens(tokens: dict[str, Any]) -> str | None:
    for key in ("id_token", "access_token"):
        tok = tokens.get(key)
        if not tok:
            continue
        claims = parse_jwt_claims(tok)
        if claims:
            account_id = extract_account_id(claims)
            if account_id:
                return account_id
    return None


def _email_from_tokens(tokens: dict[str, Any]) -> str | None:
    tok = tokens.get("id_token") or tokens.get("access_token")
    if not tok:
        return None
    claims = parse_jwt_claims(tok) or {}
    return claims.get("email")


def _persist(auth: StoredAuth) -> None:
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = TOKEN_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(asdict(auth), indent=2))
    os.chmod(tmp, 0o600)
    tmp.replace(TOKEN_FILE)


def load_auth() -> StoredAuth | None:
    if not TOKEN_FILE.exists():
        return None
    try:
        data = json.loads(TOKEN_FILE.read_text())
        return StoredAuth(**data)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def logout() -> None:
    TOKEN_FILE.unlink(missing_ok=True)


def _exchange_code(code: str, verifier: str) -> dict[str, Any]:
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
    return resp.json()


def _refresh(refresh_token: str) -> dict[str, Any]:
    resp = httpx.post(
        f"{OAUTH_ISSUER}/oauth/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": OAUTH_CLIENT_ID,
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()


def _stored_from_tokens(tokens: dict[str, Any], fallback: StoredAuth | None = None) -> StoredAuth:
    expires_in = tokens.get("expires_in", 3600)
    return StoredAuth(
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token") or (fallback.refresh_token if fallback else ""),
        expires_at=time.time() + float(expires_in),
        account_id=_account_id_from_tokens(tokens) or (fallback.account_id if fallback else None),
        email=_email_from_tokens(tokens) or (fallback.email if fallback else None),
    )


def refresh_if_needed(auth: StoredAuth) -> StoredAuth:
    if auth.expires_at - 60 > time.time():
        return auth
    tokens = _refresh(auth.refresh_token)
    refreshed = _stored_from_tokens(tokens, fallback=auth)
    _persist(refreshed)
    return refreshed


_HTML_SUCCESS = """<!doctype html>
<html><head><title>pdf-chat sign-in</title>
<style>body{font-family:system-ui,-apple-system,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#131010;color:#f1ecec}.c{text-align:center;padding:2rem}</style>
</head><body><div class="c"><h1>Signed in</h1><p>You can close this tab and return to pdf-chat.</p></div>
<script>setTimeout(()=>window.close(),1500)</script></body></html>"""


def _html_error(msg: str) -> str:
    safe = msg.replace("<", "&lt;").replace(">", "&gt;")
    return (
        "<!doctype html><html><head><title>pdf-chat sign-in failed</title></head>"
        f"<body><h1>Sign-in failed</h1><pre>{safe}</pre></body></html>"
    )


class LoginHandle:
    def __init__(self, authorize_url: str, server: HTTPServer, thread: threading.Thread, result: dict):
        self.authorize_url = authorize_url
        self._server = server
        self._thread = thread
        self._result = result  # shared dict mutated by the handler

    def poll(self) -> StoredAuth | None:
        if self._result.get("error"):
            raise RuntimeError(self._result["error"])
        auth = self._result.get("auth")
        if auth is not None:
            self._shutdown()
        return auth

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


def start_login() -> LoginHandle:
    verifier, challenge = generate_pkce()
    state = generate_state()
    authorize_url = build_authorize_url(OAUTH_REDIRECT_URI, challenge, state)
    result: dict[str, Any] = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            pass

        def do_GET(self):
            if not self.path.startswith("/auth/callback"):
                self.send_response(404)
                self.end_headers()
                return

            from urllib.parse import parse_qs, urlparse

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
                tokens = _exchange_code(code, verifier)
                auth = _stored_from_tokens(tokens)
                _persist(auth)
                result["auth"] = auth
                self._respond(200, _HTML_SUCCESS)
            except Exception as e:
                result["error"] = f"Token exchange failed: {e}"
                self._respond(500, _html_error(result["error"]))

        def _respond(self, code: int, body: str):
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))

    server = HTTPServer(("127.0.0.1", OAUTH_REDIRECT_PORT), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return LoginHandle(authorize_url, server, thread, result)
