"""
printer_scanner.py — network printer exposure (VA checklist: exposed print
services / device-information disclosure).

METHOD (collection, read-only): confirm an exposed network printer and read the
device identity it volunteers:
  * 9100 (raw / JetDirect / PDL): send a PJL `INFO ID` query and read the model /
    firmware string the device returns.
  * 631 (IPP): send a Get-Printer-Attributes request (RFC 8010) and read
    printer-make-and-model / printer-name.

Only informational queries are sent — no print job, no PJL filesystem access, no
PRET-style memory/file operations. An exposed printer is an attack surface (job
interception, stored-document/credential theft, PJL/PostScript abuse) and, on the
perimeter, an information leak.

SAFETY: raw sockets over BaseScanner timeouts; bounded reads; every probe guarded.
"""

from __future__ import annotations

import asyncio
import re
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_PRINTER_PORTS = [9100, 631]
IPP_PORT = 631
_UEL = b"\x1b%-12345X"                 # PJL Universal Exit Language wrapper
MAX_READ = 8192


def parse_pjl_id(resp: bytes) -> str:
    """Extract the model string from a PJL INFO ID response."""
    text = resp.decode("latin-1", "replace")
    # Typical: @PJL INFO ID\r\n"HP LaserJet 4250"\r\n  (quoted) or bare token
    m = re.search(r'@PJL\s+INFO\s+ID[^\r\n]*[\r\n]+"?([^"\r\n]+?)"?[\r\n]', text)
    if m:
        return m.group(1).strip()
    m = re.search(r'"([^"\r\n]{2,80})"', text)     # any quoted token fallback
    return m.group(1).strip() if m else ""


def _ipp_attr(tag: int, name: str, value: str) -> bytes:
    n, v = name.encode(), value.encode()
    return bytes([tag]) + struct.pack(">H", len(n)) + n + struct.pack(">H", len(v)) + v


def build_ipp_get_printer_attributes(uri: str) -> bytes:
    """A minimal IPP/1.1 Get-Printer-Attributes request body (RFC 8010)."""
    body = struct.pack(">HHI", 0x0101, 0x000B, 1)   # version 1.1, op-id, request-id
    body += bytes([0x01])                           # operation-attributes-tag
    body += _ipp_attr(0x47, "attributes-charset", "utf-8")
    body += _ipp_attr(0x48, "attributes-natural-language", "en")
    body += _ipp_attr(0x45, "printer-uri", uri)
    body += bytes([0x03])                           # end-of-attributes-tag
    return body


def parse_ipp_make_model(body: bytes) -> str:
    """Best-effort extraction of printer-make-and-model / printer-name from an IPP
    response body (the value follows its attribute name as a length-prefixed str)."""
    for attr in (b"printer-make-and-model", b"printer-name"):
        i = body.find(attr)
        if i < 0:
            continue
        j = i + len(attr)
        if j + 2 > len(body):
            continue
        (vlen,) = struct.unpack_from(">H", body, j)
        if 0 < vlen <= 200 and j + 2 + vlen <= len(body):
            val = body[j + 2:j + 2 + vlen].decode("latin-1", "replace").strip()
            if val:
                return val
    return ""


def _recv_bounded(sock: socket.socket, limit: int = MAX_READ) -> bytes:
    buf = b""
    while len(buf) < limit:
        try:
            chunk = sock.recv(min(4096, limit - len(buf)))
        except OSError:
            break
        if not chunk:
            break
        buf += chunk
    return buf


class PrinterScanner(BaseScanner):
    name = "printer_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_PRINTER_PORTS

    def _probe_pjl(self, target: str, port: int) -> dict:
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                s.sendall(_UEL + b"@PJL INFO ID\r\n" + _UEL)
                resp = _recv_bounded(s)
        except OSError:
            return {"printer": None, "reason": "no_printer"}
        # Reaching an open 9100 is itself a raw-print exposure; PJL model is a bonus.
        return {"printer": True, "protocol": "raw-9100",
                "pjl_responded": bool(resp), "model": parse_pjl_id(resp)}

    def _probe_ipp(self, target: str, port: int) -> dict:
        uri = f"ipp://{target}:{port}/ipp/print"
        ipp = build_ipp_get_printer_attributes(uri)
        req = (f"POST / HTTP/1.1\r\nHost: {target}:{port}\r\n"
               f"Content-Type: application/ipp\r\nContent-Length: {len(ipp)}\r\n"
               f"Connection: close\r\n\r\n").encode() + ipp
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                s.sendall(req)
                resp = _recv_bounded(s)
        except OSError:
            return {"printer": None, "reason": "no_printer"}
        body = resp.split(b"\r\n\r\n", 1)[1] if b"\r\n\r\n" in resp else b""
        is_ipp = b"application/ipp" in resp.lower() or (len(body) >= 8 and body[0] in (0x01, 0x02))
        if not is_ipp and b" 200 " not in resp[:64]:
            return {"printer": None, "reason": "not_ipp"}
        return {"printer": True, "protocol": "ipp-631",
                "model": parse_ipp_make_model(body)}

    def _probe(self, target: str, port: int) -> dict:
        return self._probe_ipp(target, port) if port == IPP_PORT else self._probe_pjl(target, port)

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not data.get("printer"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_printer"),
                              data=data)
        evidence = f"{data.get('protocol')} model={data.get('model')!r}"
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("Network printer exposure (9100 PJL / 631 IPP)")
    parser.add_argument("-p", "--ports", default=None, help="printer ports (default: 9100,631)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_PRINTER_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = PrinterScanner(scope, rate=args.rate, concurrency=args.concurrency,
                                 timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
