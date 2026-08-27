"""
nfs_scanner.py — NFS export exposure over ONC RPC (VA checklist: anonymous
network file-share exposure).

METHOD (collection, read-only): speak ONC/Sun RPC (RFC 1057) to the target's
portmapper (111) to (a) DUMP the registered RPC programs — the `rpcinfo -p`
view — and (b) locate mountd, then call the MOUNT protocol's EXPORT procedure
(RFC 1813 §5.2.3) to read the list of exported directories and the client groups
each is shared to. An export shared to `*` / `(everyone)` / an empty group is
world-readable — a classic enterprise data-exposure misconfiguration.

No files are read, nothing is mounted, no credentials are sent — this is exactly
what `showmount -e <host>` returns, reimplemented natively (impacket speaks MSRPC,
not ONC/Sun RPC, so there is no library path; the wire format is small and
fully specified, so we craft it directly like the SNMP/DNS probes already do).

SAFETY: raw sockets via BaseScanner timeouts; every RPC call independently
guarded; XDR parsing is bounded (export/program/client caps + per-string length
cap) so a malicious portmapper cannot make us read unbounded data.
"""

from __future__ import annotations

import asyncio
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_NFS_PORTS = [2049]
PORTMAP_PORT = 111
MOUNTD_FALLBACK_PORT = 20048   # common fixed mountd port when portmap is filtered

# ONC RPC / program numbers
PMAP_PROG, PMAP_VERS = 100000, 2
PMAP_GETPORT, PMAP_DUMP = 3, 4
MOUNT_PROG, MOUNT_VERS = 100005, 3
MOUNTPROC_EXPORT = 5
IPPROTO_TCP, IPPROTO_UDP = 6, 17
_XID = 0x76656468   # "vedh" — fixed; we do one request/response per socket

# Bounds
MAX_EXPORTS = 1000
MAX_PROGRAMS = 2000
MAX_CLIENTS = 200
MAX_STR = 4096

# A client group that means "anyone" — an export shared to it is world-readable.
_WORLD_GROUPS = {"*", "everyone", "(everyone)", "", "0.0.0.0/0", "::/0", "anon"}


# ── XDR / ONC-RPC wire helpers (pure) ─────────────────────────────────────────
class _XDR:
    """Minimal, BOUNDED big-endian XDR reader (RFC 4506)."""

    def __init__(self, buf: bytes):
        self.b = buf
        self.o = 0

    def u32(self) -> int:
        if self.o + 4 > len(self.b):
            raise ValueError("xdr: truncated u32")
        (v,) = struct.unpack_from(">I", self.b, self.o)
        self.o += 4
        return v

    def opaque(self, maxlen: int = MAX_STR) -> bytes:
        n = self.u32()
        if n > maxlen or self.o + n > len(self.b):
            raise ValueError("xdr: bad/oversized opaque")
        s = self.b[self.o:self.o + n]
        self.o += n + ((-n) % 4)   # skip 4-byte padding
        return s

    def string(self, maxlen: int = MAX_STR) -> str:
        return self.opaque(maxlen).decode("utf-8", "replace")


def parse_portmap_dump(data: bytes) -> list[dict]:
    """Parse a PMAPPROC_DUMP reply — the list of registered RPC programs."""
    x = _XDR(data)
    out: list[dict] = []
    while len(out) < MAX_PROGRAMS:
        if x.u32() == 0:          # list continuation marker: 0 = end
            break
        prog, vers, prot, port = x.u32(), x.u32(), x.u32(), x.u32()
        out.append({"program": prog, "version": vers,
                    "protocol": {IPPROTO_TCP: "tcp", IPPROTO_UDP: "udp"}.get(prot, str(prot)),
                    "port": port})
    return out


def parse_mount_export(data: bytes) -> list[dict]:
    """Parse a MOUNTPROC_EXPORT reply — exports + their allowed client groups."""
    x = _XDR(data)
    exports: list[dict] = []
    while len(exports) < MAX_EXPORTS:
        if x.u32() == 0:          # exportnode list: 0 = end
            break
        path = x.string()
        clients: list[str] = []
        while True:               # groups sub-list
            if x.u32() == 0:
                break
            g = x.string()
            if len(clients) < MAX_CLIENTS:
                clients.append(g)
        exports.append({"path": path, "clients": clients,
                        "world_readable": is_world_readable(clients)})
    return exports


def is_world_readable(clients: list[str]) -> bool:
    """An export with no client restriction, or one shared to a wildcard group,
    is readable by anyone who can reach the server."""
    if not clients:
        return True
    return any((c or "").strip().lower() in _WORLD_GROUPS for c in clients)


def _rpc_call(sock: socket.socket, prog: int, vers: int, proc: int,
              args: bytes = b"") -> bytes | None:
    """Send one ONC-RPC CALL (AUTH_NULL) over a TCP record-marked stream and
    return the procedure result bytes, or None on any RPC-level failure."""
    body = struct.pack(">IIIIII", _XID, 0, 2, prog, vers, proc)  # xid, CALL, rpcvers=2
    body += struct.pack(">IIII", 0, 0, 0, 0)                     # cred AUTH_NULL, verf AUTH_NULL
    body += args
    sock.sendall(struct.pack(">I", 0x80000000 | len(body)) + body)
    reply = _recv_record(sock)
    return _parse_rpc_reply(reply)


def _recv_record(sock: socket.socket, max_bytes: int = 1 << 20) -> bytes:
    """Read RPC record-marking fragments (RFC 1057 §10) until the last fragment."""
    out = b""
    while len(out) < max_bytes:
        hdr = _recv_exact(sock, 4)
        if hdr is None:
            break
        (marker,) = struct.unpack(">I", hdr)
        last = marker & 0x80000000
        frag = marker & 0x7FFFFFFF
        if frag:
            chunk = _recv_exact(sock, min(frag, max_bytes - len(out)))
            if chunk is None:
                break
            out += chunk
        if last:
            break
    return out


def _recv_exact(sock: socket.socket, n: int) -> bytes | None:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def _parse_rpc_reply(data: bytes) -> bytes | None:
    """Strip the ONC-RPC reply header; return the accepted-SUCCESS result bytes."""
    if not data or len(data) < 12:
        return None
    _xid, mtype, reply_stat = struct.unpack_from(">III", data, 0)
    if mtype != 1 or reply_stat != 0:      # not REPLY, or MSG_DENIED
        return None
    off = 12
    if len(data) < off + 8:
        return None
    _vflav, vlen = struct.unpack_from(">II", data, off)
    off += 8 + ((vlen + 3) & ~3)
    if len(data) < off + 4:
        return None
    (accept_stat,) = struct.unpack_from(">I", data, off)
    off += 4
    if accept_stat != 0:                    # not SUCCESS (PROG_UNAVAIL, etc.)
        return None
    return data[off:]


class NFSScanner(BaseScanner):
    name = "nfs_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_NFS_PORTS

    def _rpc(self, target: str, port: int, prog: int, vers: int, proc: int,
             args: bytes = b"") -> bytes | None:
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                return _rpc_call(s, prog, vers, proc, args)
        except OSError:
            return None

    def _portmap_dump(self, target: str) -> list[dict] | None:
        data = self._rpc(target, PORTMAP_PORT, PMAP_PROG, PMAP_VERS, PMAP_DUMP)
        if data is None:
            return None
        try:
            return parse_portmap_dump(data)
        except Exception:
            return []

    def _portmap_getport(self, target: str, prog: int, vers: int,
                         prot: int = IPPROTO_TCP) -> int | None:
        args = struct.pack(">IIII", prog, vers, prot, 0)
        data = self._rpc(target, PORTMAP_PORT, PMAP_PROG, PMAP_VERS, PMAP_GETPORT, args)
        if data is None or len(data) < 4:
            return None
        (p,) = struct.unpack(">I", data[:4])
        return p or None

    def _mount_export(self, target: str, port: int) -> list[dict] | None:
        if not port:
            return None
        data = self._rpc(target, port, MOUNT_PROG, MOUNT_VERS, MOUNTPROC_EXPORT)
        if data is None:
            return None
        try:
            return parse_mount_export(data)
        except Exception:
            return []

    def _probe(self, target: str, port: int) -> dict:
        """Blocking: portmap DUMP + mountd EXPORT. Monkeypatchable for tests."""
        result: dict = {"nfs": None, "portmap_open": False, "rpc_programs": [],
                        "mountd_port": None, "exports": []}

        progs = self._portmap_dump(target)
        if progs is not None:
            result["portmap_open"] = True
            result["nfs"] = True
            result["rpc_programs"] = progs
            result["mountd_port"] = next(
                (p["port"] for p in progs
                 if p["program"] == MOUNT_PROG and p["port"]), None)

        mountd_port = (result["mountd_port"]
                       or self._portmap_getport(target, MOUNT_PROG, MOUNT_VERS)
                       or MOUNTD_FALLBACK_PORT)
        exports = self._mount_export(target, mountd_port)
        if exports is not None:
            result["nfs"] = True
            result["mountd_port"] = mountd_port
            result["exports"] = exports
            result["export_count"] = len(exports)
            result["world_readable_exports"] = [e["path"] for e in exports
                                                if e.get("world_readable")]
        return result

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not data.get("nfs"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason="no_nfs_rpc", data=data)
        wr = data.get("world_readable_exports") or []
        evidence = (f"portmap={data.get('portmap_open')} "
                    f"exports={data.get('export_count', 0)} world_readable={len(wr)}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("NFS export enumeration over ONC RPC (showmount -e)")
    parser.add_argument("-p", "--ports", default=None, help="trigger ports (default: 2049)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_NFS_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = NFSScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
