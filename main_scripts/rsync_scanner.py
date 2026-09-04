"""
rsync_scanner.py — rsync daemon anonymous-module exposure (VA checklist:
anonymous network file-share exposure; common on enterprise backup hosts).

METHOD (collection, read-only): speak the rsync daemon protocol (port 873). After
the `@RSYNCD:` version handshake, request the module list (empty module name), then
for each advertised module test whether it can be selected WITHOUT authentication
(the daemon answers `@RSYNCD: OK` for anonymous, or `@RSYNCD: AUTHREQD` when a
secret is required). No files are listed or transferred — only the module-selection
handshake is performed, so nothing is read from the shares themselves.

POLICY BOUNDARY: selecting a module with no secret is anonymous access, not a
guessed credential — inside the "no guessed credentials" invariant. We never send
a password/secret and never answer an AUTHREQD challenge.

SAFETY: text protocol over BaseScanner timeouts; module list + per-module anon
probe both bounded (module cap, byte caps); every phase guarded.
"""

from __future__ import annotations

import asyncio
import re
import socket

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_RSYNC_PORTS = [873]
MAX_MODULES = 100
MAX_LIST_BYTES = 65536
_GREETING_RE = re.compile(r"@RSYNCD:\s*([\d.]+)")


def parse_modules(data: str) -> list[dict]:
    """Parse the daemon's module listing into [{name, comment}]. Lines are
    'name<whitespace>comment'; @RSYNCD:/@ERROR lines are protocol, not modules."""
    out: list[dict] = []
    for line in (data or "").splitlines():
        line = line.rstrip("\r")
        if not line.strip():
            continue
        if line.startswith("@RSYNCD:") or line.startswith("@ERROR"):
            continue
        parts = re.split(r"\s{2,}|\t", line.strip(), maxsplit=1)
        name = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ""
        if name:
            out.append({"name": name, "comment": comment})
        if len(out) >= MAX_MODULES:
            break
    return out


def _recv_until(sock: socket.socket, markers: list[bytes],
                max_bytes: int = MAX_LIST_BYTES) -> bytes:
    buf = b""
    while len(buf) < max_bytes:
        try:
            chunk = sock.recv(min(4096, max_bytes - len(buf)))
        except OSError:
            break
        if not chunk:
            break
        buf += chunk
        if any(m in buf for m in markers):
            break
    return buf


def _handshake(sock: socket.socket) -> str | None:
    """Read the @RSYNCD greeting and echo it back VERBATIM. Returns the negotiated
    protocol version string, or None if this isn't an rsync daemon.

    The greeting must be echoed whole, not reduced to its version number: since
    protocol 32 the daemon appends its digest-name list ("@RSYNCD: 32.0 sha512
    sha256 sha1 md5 md4") and answers a version-only reply with "@ERROR: your
    client omitted the digest name list", tearing the session down before any
    module listing is sent. That made module enumeration return empty against
    every rsync 3.2+ daemon.
    """
    raw = _recv_until(sock, [b"\n"], 256).decode("latin-1", "replace")
    greet = raw.split("\n", 1)[0].rstrip("\r")
    m = _GREETING_RE.search(greet)
    if not m:
        return None
    sock.sendall(f"{greet}\n".encode("latin-1", "replace"))
    return m.group(1)


class RsyncScanner(BaseScanner):
    name = "rsync_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_RSYNC_PORTS

    def _list_modules(self, target: str, port: int) -> tuple[str | None, list[dict]]:
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                ver = _handshake(s)
                if ver is None:
                    return None, []
                s.sendall(b"\n")   # empty module name => list all modules
                data = _recv_until(s, [b"@RSYNCD: EXIT", b"@ERROR"])
                return ver, parse_modules(data.decode("latin-1", "replace"))
        except OSError:
            return None, []

    def _test_anon(self, target: str, port: int, module: str) -> bool | None:
        """Select a module without a secret: OK => anonymous, AUTHREQD => auth."""
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                if _handshake(s) is None:
                    return None
                s.sendall(module.encode("latin-1", "replace") + b"\n")
                resp = _recv_until(s, [b"\n"], 512).decode("latin-1", "replace")
                if "@RSYNCD: OK" in resp:
                    return True
                if "AUTHREQD" in resp:
                    return False
                return None
        except OSError:
            return None

    def _probe(self, target: str, port: int) -> dict:
        """Blocking: list modules, then anon-test each. Monkeypatchable for tests."""
        ver, modules = self._list_modules(target, port)
        if ver is None:
            return {"rsync": None, "reason": "no_rsync"}
        anon: list[str] = []
        for mod in modules[:MAX_MODULES]:
            a = self._test_anon(target, port, mod["name"])
            mod["anonymous"] = a
            if a:
                anon.append(mod["name"])
        return {"rsync": True, "version": ver, "modules": modules,
                "module_count": len(modules), "anon_modules": anon}

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not data.get("rsync"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_rsync"),
                              data=data)
        evidence = (f"modules={data.get('module_count', 0)} "
                    f"anon={len(data.get('anon_modules') or [])}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("rsync daemon anonymous-module enumeration")
    parser.add_argument("-p", "--ports", default=None, help="rsync ports (default: 873)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_RSYNC_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = RsyncScanner(scope, rate=args.rate, concurrency=args.concurrency,
                               timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
