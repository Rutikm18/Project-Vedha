"""
security_headers.py — baseline response headers for the API.

The API only returns JSON / files, never pages, so the policy is strict: nothing
may be framed, sniffed, or loaded by a document. HSTS is added only on requests
that arrived over HTTPS (uvicorn derives the scheme from the trusted proxy's
X-Forwarded-Proto), so a plain-HTTP lab deployment is not poisoned. The
interactive docs (served outside production only) load their own scripts, so the
restrictive CSP and no-store are skipped for those paths.
"""
from __future__ import annotations

from starlette.datastructures import MutableHeaders

_DOC_PATHS = ("/docs", "/redoc", "/openapi.json")

_STATIC = (
    (b"x-content-type-options", b"nosniff"),
    (b"x-frame-options", b"DENY"),
    (b"referrer-policy", b"no-referrer"),
    (b"permissions-policy", b"camera=(), microphone=(), geolocation=()"),
    (b"cross-origin-resource-policy", b"same-site"),
)
_API_ONLY = (
    (b"content-security-policy", b"default-src 'none'; frame-ancestors 'none'; base-uri 'none'"),
    (b"cache-control", b"no-store"),
)
_HSTS = b"max-age=31536000; includeSubDomains"


class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        path = scope.get("path", "")
        is_doc = path.startswith(_DOC_PATHS)
        https = scope.get("scheme") == "https"

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                for name, value in _STATIC:
                    headers.setdefault(name.decode(), value.decode())
                if not is_doc:
                    for name, value in _API_ONLY:
                        headers.setdefault(name.decode(), value.decode())
                if https:
                    headers.setdefault("strict-transport-security", _HSTS.decode())
            await send(message)

        await self.app(scope, receive, send_with_headers)
