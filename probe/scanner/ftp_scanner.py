"""
ftp_scanner.py — FTP anonymous-access check (VA checklist: anonymous file
exposure / cleartext file transfer).

METHOD (collection, read-only): connect to the FTP control channel, read the
greeting, and attempt the *documented* anonymous login (`USER anonymous` /
`PASS anonymous@…`). If it succeeds, confirm read access with a bounded passive
directory listing (`PASV` + `LIST`). No files are downloaded in full, and NO
write is attempted — we never create/modify/delete anything on the server, so the
check is strictly non-destructive.

POLICY BOUNDARY: the anonymous account is a *documented, well-known* account, not
a guessed credential — logging into it stays inside the "no guessed credentials"
invariant (same class as an SMB null session). Write access is NOT tested by default
(that modifies the target): `anon_write` is then None ("not tested"), and the finding
recommends verifying it manually.

OPT-IN EXCEPTION (`write_test=True`, CLI `--allow-write-test`): upload one tiny,
uniquely-named file and delete it straight away, recording `anon_write` True/False and
whether the cleanup worked. It is never enabled by the workflow or any default; an
operator must switch it on for an engagement whose rules of engagement permit writes.
If the delete fails the file name is reported (`anon_write_leftover`) so it can be
removed by hand. This upgrades the existing port-based FTP finding from a hint to a
confirmed observation.

SAFETY: line-based control protocol over BaseScanner timeouts; the passive data
listing is read with a hard byte cap; every phase guarded.
"""

from __future__ import annotations

import asyncio
import re
import secrets
import socket

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_FTP_PORTS = [21]
ANON_USER = "anonymous"
ANON_PASS = "anonymous@example.com"   # conventional, non-attributing
MAX_LISTING_BYTES = 8192
MAX_SAMPLE_LINES = 20

_PASV_RE = re.compile(r"\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)")
_FINAL_LINE_RE = re.compile(rb"^\d\d\d ", re.MULTILINE)


def parse_pasv(text: str) -> int | None:
    """Extract the passive data PORT from a 227 reply. We connect to the TARGET
    on this port (not the possibly-internal IP the server advertises)."""
    m = _PASV_RE.search(text or "")
    if not m:
        return None
    p1, p2 = int(m.group(5)), int(m.group(6))
    port = p1 * 256 + p2
    return port if 0 < port < 65536 else None


def banner_software(banner: str) -> str:
    """Best-effort software token from the 220 greeting (e.g. 'vsFTPd 3.0.3')."""
    b = (banner or "").strip()
    b = re.sub(r"^\d\d\d[- ]", "", b)          # strip the 220 code
    return b[:120]


class FTPScanner(BaseScanner):
    name = "ftp_scan"

    def __init__(self, *args, ports: list[int] | None = None, write_test: bool = False,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_FTP_PORTS
        self.write_test = bool(write_test)      # opt-in only; see the module docstring

    def _read_response(self, sock: socket.socket) -> tuple[int, str]:
        """Read one (possibly multi-line) FTP reply; return (code, full_text)."""
        buf = b""
        while len(buf) < 16384:
            try:
                chunk = sock.recv(4096)
            except OSError:
                break
            if not chunk:
                break
            buf += chunk
            # a complete reply ends with a line 'NNN ' (code + space)
            lines = buf.split(b"\r\n")
            if any(_FINAL_LINE_RE.match(ln) for ln in lines if ln):
                break
        text = buf.decode("latin-1", "replace")
        code = 0
        m = re.search(r"(?m)^(\d\d\d) ", text)
        if m:
            code = int(m.group(1))
        return code, text

    def _cmd(self, sock: socket.socket, line: str) -> tuple[int, str]:
        sock.sendall(line.encode("latin-1") + b"\r\n")
        return self._read_response(sock)

    def _probe(self, target: str, port: int) -> dict:
        """Blocking: greeting → anonymous login → bounded read confirmation.
        Monkeypatchable for tests."""
        data: dict = {"ftp": None}
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                code, greet = self._read_response(s)
                if code == 0:
                    return {"ftp": None, "reason": "no_ftp_greeting"}
                data["ftp"] = True
                data["banner"] = greet.strip().splitlines()[0] if greet.strip() else ""
                data["software"] = banner_software(data["banner"])

                code, _ = self._cmd(s, f"USER {ANON_USER}")
                if code == 230:
                    data["anonymous_login"] = True
                elif code in (331, 332):
                    code, _ = self._cmd(s, f"PASS {ANON_PASS}")
                    data["anonymous_login"] = (code == 230)
                else:
                    data["anonymous_login"] = False

                if data.get("anonymous_login"):
                    data["anon_read"], data["file_sample"] = self._list_bounded(s, target)
                    # None = not tested (the default). Only an explicit opt-in writes anything.
                    data["anon_write"] = None
                    if self.write_test:
                        data.update(self._write_test(s, target))
                try:
                    self._cmd(s, "QUIT")
                except OSError:
                    pass
        except OSError as exc:
            return {"ftp": None, "reason": "no_ftp", "detail": str(exc)[:120]}
        return data

    def _list_bounded(self, ctrl: socket.socket, target: str) -> tuple[bool, list[str]]:
        """Confirm anonymous READ via PASV + LIST, reading a bounded amount."""
        try:
            code, text = self._cmd(ctrl, "PASV")
            if code != 227:
                return False, []
            dport = parse_pasv(text)
            if not dport:
                return False, []
            with socket.create_connection((target, dport), timeout=self.timeout) as d:
                d.settimeout(self.timeout)
                ctrl.sendall(b"LIST\r\n")
                self._read_response(ctrl)          # 150 / 125 then later 226
                blob = b""
                while len(blob) < MAX_LISTING_BYTES:
                    chunk = d.recv(min(4096, MAX_LISTING_BYTES - len(blob)))
                    if not chunk:
                        break
                    blob += chunk
            # Consume the transfer-complete reply (226) the server sends after the listing, so
            # it cannot be mistaken for the answer to the NEXT command.
            self._read_response(ctrl)
            lines = [ln for ln in blob.decode("latin-1", "replace").splitlines() if ln.strip()]
            return True, lines[:MAX_SAMPLE_LINES]
        except OSError:
            return False, []

    def _write_test(self, ctrl: socket.socket, target: str) -> dict:
        """Upload one tiny uniquely-named file over PASV, then delete it. Returns
        {anon_write, anon_write_leftover?}. Only ever called when write_test is on."""
        name = f"vedha-write-test-{secrets.token_hex(4)}.txt"
        out: dict = {"anon_write": False}
        try:
            code, text = self._cmd(ctrl, "PASV")
            dport = parse_pasv(text) if code == 227 else None
            if not dport:
                return out
            with socket.create_connection((target, dport), timeout=self.timeout) as d:
                d.settimeout(self.timeout)
                code, _ = self._cmd(ctrl, f"STOR {name}")
                if code not in (125, 150):
                    return out                       # 550/553: the write was refused
                d.sendall(b"vedha write test - safe to delete\r\n")
            code, _ = self._read_response(ctrl)      # 226 once the transfer completes
            if code not in (226, 250):
                return out
            out["anon_write"] = True
            dele, _ = self._cmd(ctrl, f"DELE {name}")
            if dele not in (250, 200):
                out["anon_write_leftover"] = name    # tell the operator what to remove
        except OSError:
            pass
        return out

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not data.get("ftp"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_ftp"),
                              data=data)
        evidence = (f"anon_login={data.get('anonymous_login')} "
                    f"anon_read={data.get('anon_read')} "
                    f"anon_write={data.get('anon_write')} "
                    f"software={data.get('software')!r}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("FTP anonymous-access check")
    parser.add_argument("-p", "--ports", default=None, help="FTP ports (default: 21)")
    parser.add_argument("--allow-write-test", action="store_true",
                        help="ALSO upload and delete one tiny file to test anonymous WRITE. "
                             "Modifies the target; use only where the rules of engagement allow.")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_FTP_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = FTPScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports,
                             write_test=args.allow_write_test)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
