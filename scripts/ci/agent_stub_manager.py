#!/usr/bin/env python3
"""
agent_stub_manager.py — the manager's /agent/* download endpoints, served from a release
directory, for exercising the installers end to end without a database or Redis.

CI starts this on a Windows runner and runs the real, stamped `install.ps1` (the file the
release produced) against it in Windows PowerShell 5.1, then again with each tamper mode to
prove the installer REFUSES a bad release. Developers can do the same by hand.

It mirrors manager/backend/app/routers/agent_distribution.py for the Windows path:

    GET /agent/install.ps1               windows installer          (public)
    GET /agent/install.cmd               windows launcher           (public)
    GET /agent/manifest.json             signed manifest            (public)
    GET /agent/manifest.json.sig         Ed25519 signature          (public)
    GET /agent/manifest.json.p256.sig    ECDSA P-256 signature      (public)
    GET /agent/package/windows           the Windows zip            (Bearer vet_… required)

Tamper modes (what a hostile mirror or network could do), each of which the installer must
reject without installing anything:

    manifest    flip a byte of the manifest            -> signature does not verify
    signature   corrupt the P-256 signature            -> signature does not verify
    package     flip a byte of the package             -> SHA-256 mismatch
    truncated   cut the package short                  -> size mismatch
    oversize    append bytes to the package            -> larger than the signed size
    redirect    answer the package request with a 302  -> redirects are refused

Plain http on 127.0.0.1 by default; --tls-cert/--tls-key serve https (the Windows installer refuses an
http:// manager for a real install). This is a test fixture, not a server to deploy.

Usage:
    python scripts/ci/agent_stub_manager.py --release dist/agent-release/1.0.371 \
        --token vet_ci_test --port 8765 [--tamper package]
"""
from __future__ import annotations

import argparse
import base64
import json
import ssl
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TAMPER_MODES = ("none", "manifest", "signature", "package", "truncated", "oversize", "redirect")
TOKEN_PREFIX = "vet_"


def _flip(data: bytes, index: int = 10) -> bytes:
    out = bytearray(data)
    out[index % len(out)] ^= 0x01
    return bytes(out)


def _corrupt_signature(text: bytes) -> bytes:
    raw = bytearray(base64.b64decode(text.strip()))
    raw[0] ^= 0x01
    return base64.b64encode(bytes(raw)) + b"\n"


class _Handler(BaseHTTPRequestHandler):
    server_version = "agent-stub-manager"
    release: Path
    token: str
    tamper: str
    allow_tokenless: bool
    package_name: str
    requests: list  # (method, path, status), for assertions

    def log_message(self, fmt, *args):      # keep CI logs quiet; requests are recorded instead
        return

    def _send(self, status: int, body: bytes, content_type: str = "text/plain", headers: dict | None = None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        self.server.requests.append((self.command, self.path, status))

    def _detail(self, status: int, detail: str):
        self._send(status, json.dumps({"detail": detail}).encode(), "application/json")

    def _file(self, name: str, content_type: str, tamper=None):
        body = (self.release / name).read_bytes()
        self._send(200, tamper(body) if tamper else body, content_type)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        t = self.tamper
        if path == "/agent/install.ps1":
            return self._file("install.ps1", "text/plain; charset=utf-8")
        if path == "/agent/install.cmd":
            return self._file("install.cmd", "text/plain; charset=utf-8")
        if path == "/agent/manifest.json":
            return self._file("manifest.json", "application/json", _flip if t == "manifest" else None)
        if path == "/agent/manifest.json.sig":
            return self._file("manifest.json.sig", "text/plain")
        if path == "/agent/manifest.json.p256.sig":
            return self._file("manifest.json.p256.sig", "text/plain",
                              _corrupt_signature if t == "signature" else None)
        if path == "/agent/package/windows":
            auth = self.headers.get("Authorization", "")
            raw = auth[len("Bearer "):].strip() if auth.startswith("Bearer ") else ""
            tokenless_ok = self.allow_tokenless and not auth.strip()      # AGENT_ALLOW_TOKENLESS_INSTALL
            if not tokenless_ok and not raw.startswith(TOKEN_PREFIX):
                return self._detail(401, "An enrolment token is required to download the agent")
            if not tokenless_ok and raw != self.token:
                return self._detail(401, "This enrolment token is invalid, expired, revoked or already used"
                                         " - create a new one in Fleet")
            if t == "redirect":
                return self._send(302, b"", headers={"Location": "https://example.invalid/elsewhere.zip"})
            body = (self.release / self.package_name).read_bytes()
            if t == "package":
                body = _flip(body, len(body) // 2)
            elif t == "truncated":
                body = body[: len(body) - 1]
            elif t == "oversize":
                body = body + b"\0"
            return self._send(200, body, "application/zip", {"X-Vedha-Release": self.release.name})
        return self._detail(404, "not found")

    def do_HEAD(self):  # noqa: F811 — same routing, no body (see _send)
        return self.do_GET()


def serve(release: Path, token: str, *, port: int = 0, tamper: str = "none",
          tls: tuple[Path, Path] | None = None, allow_tokenless: bool = False) -> ThreadingHTTPServer:
    """Start the stub on 127.0.0.1 (port 0 = any free port) in a daemon thread.
    `tls` = (certificate, key) PEM files to serve https."""
    if tamper not in TAMPER_MODES:
        raise ValueError(f"tamper must be one of {TAMPER_MODES}")
    manifest = json.loads((release / "manifest.json").read_text(encoding="utf-8"))
    packages = [p for p in manifest.get("packages", []) if p.get("os") == "windows"]
    if len(packages) != 1:
        raise ValueError(f"{release} does not hold exactly one Windows package")

    class Handler(_Handler):
        pass

    Handler.release = release
    Handler.token = token
    Handler.tamper = tamper
    Handler.allow_tokenless = allow_tokenless
    Handler.package_name = packages[0]["file"]
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    if tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(str(tls[0]), str(tls[1]))
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.requests = []
    Handler.requests = httpd.requests
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--release", required=True, type=Path, help="a built release version directory")
    ap.add_argument("--token", default="vet_ci_test")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--tamper", choices=TAMPER_MODES, default="none")
    ap.add_argument("--tls-cert", type=Path)
    ap.add_argument("--tls-key", type=Path)
    args = ap.parse_args(argv)
    tls = (args.tls_cert, args.tls_key) if args.tls_cert and args.tls_key else None
    httpd = serve(args.release, args.token, port=args.port, tamper=args.tamper, tls=tls)
    scheme = "https" if tls else "http"
    print(f"stub manager on {scheme}://127.0.0.1:{httpd.server_address[1]} (tamper={args.tamper})", flush=True)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
