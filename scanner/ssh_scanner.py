"""
ssh_scanner.py — SSH configuration / algorithm audit (VA checklist §6).

METHOD (collection + local verdict): open the SSH transport, read the server
identification string, exchange KEXINIT, and record which algorithms the server
offers. Each offered algorithm is looked up in the vendored weakness table and
tagged as a failure / warning / info. No authentication, no key-exchange
completion, no exploitation — we read only what the server volunteers in its
KEXINIT (RFC 4253 §7.1), exactly like a client would before deciding whether to
continue.

ENGINE / CONTENT SPLIT: this module is the *engine* (socket + KEXINIT wire parse
+ evaluator + Terrapin heuristic). The *content* — the algorithm weakness table —
lives in ``ssh_kexdb.py``, a byte-faithful vendor of ssh-audit's MASTER_DB
(MIT-licensed; see that module for the full attribution). Grading a check therefore
means updating data, not this code.

COLLECTION / INTERPRETATION SPLIT: like every scanner here, this emits pure facts
(the offered algorithms + which are weak, per the vendored table) and never a
vulnerability verdict. ``findings.py`` (_rule_ssh) turns those facts into the
SSH-WEAK-ALGO / SSH-TERRAPIN findings.
"""

from __future__ import annotations

import asyncio
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)
from .ssh_kexdb import lookup

# Neutral client identification — blends in as a common OpenSSH client rather than
# signing the scan with a brand string a blue team can grep/attribute.
CLIENT_ID = b"SSH-2.0-OpenSSH_9.6"

DEFAULT_SSH_PORTS = [22]

SSH_MSG_KEXINIT = 20


# ── banner parsing ────────────────────────────────────────────────────────────
def parse_ssh_banner(data) -> dict | None:
    """Parse an SSH identification string 'SSH-<proto>-<software>[ comments]'.

    Returns {protocol, software, comments, raw} or None if it is not an SSH
    identification string.
    """
    if isinstance(data, (bytes, bytearray)):
        data = bytes(data).decode("latin-1", "replace")
    line = data.strip().splitlines()[0].strip() if data.strip() else ""
    if not line.startswith("SSH-"):
        return None
    parts = line.split("-", 2)
    if len(parts) < 3:
        return None
    proto = parts[1]
    rest = parts[2]
    if " " in rest:
        software, comments = rest.split(" ", 1)
        comments = comments.strip() or None
    else:
        software, comments = rest, None
    return {"protocol": proto, "software": software,
            "comments": comments, "raw": line}


# ── KEXINIT parsing (RFC 4253 §7.1) ───────────────────────────────────────────
class _Cursor:
    def __init__(self, buf: bytes):
        self.buf = buf
        self.pos = 0

    def read(self, n: int) -> bytes:
        chunk = self.buf[self.pos:self.pos + n]
        if len(chunk) != n:
            raise ValueError("truncated SSH KEXINIT payload")
        self.pos += n
        return chunk

    def read_name_list(self) -> list[str]:
        (length,) = struct.unpack(">I", self.read(4))
        if length == 0:
            return []
        body = self.read(length).decode("latin-1", "replace")
        return body.split(",")


_KEXINIT_FIELDS = (
    "kex_algorithms",
    "server_host_key_algorithms",
    "encryption_c2s",
    "encryption_s2c",
    "mac_c2s",
    "mac_s2c",
    "compression_c2s",
    "compression_s2c",
    "languages_c2s",
    "languages_s2c",
)


def parse_kexinit(payload: bytes) -> dict:
    """Parse a SSH_MSG_KEXINIT body into its name-lists.

    Accepts the payload with or without the leading SSH_MSG_KEXINIT (20) type
    byte. Returns a dict of the ten name-lists plus first_kex_packet_follows.
    Field order mirrors ssh-audit's SSH2_Kex.parse exactly (cookie, kex, hostkey,
    enc c2s/s2c, mac c2s/s2c, comp c2s/s2c, lang c2s/s2c, follows, reserved).
    """
    if payload and payload[0] == SSH_MSG_KEXINIT:
        payload = payload[1:]
    cur = _Cursor(payload)
    cur.read(16)  # cookie
    out: dict = {name: cur.read_name_list() for name in _KEXINIT_FIELDS}
    out["first_kex_packet_follows"] = bool(cur.read(1)[0])
    return out


# ── evaluation ────────────────────────────────────────────────────────────────
def _dedup(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def evaluate_algorithms(kexinit: dict) -> dict:
    """Grade a server's offered algorithms against the vendored weakness table.

    Returns failures / warnings / unknown (each a list of
    {category, algorithm, reasons}) plus Terrapin (CVE-2023-48795) flags. Mirrors
    ssh-audit: a host-key/cipher/mac appears under 'fail' only if the vendored DB
    marks it a failure — so e.g. ssh-rsa (SHA-1 signature) fails while the modern
    rsa-sha2-256 does not.
    """
    categories = {
        "kex": kexinit.get("kex_algorithms", []),
        "key": kexinit.get("server_host_key_algorithms", []),
        "enc": _dedup(list(kexinit.get("encryption_s2c", []))
                      + list(kexinit.get("encryption_c2s", []))),
        "mac": _dedup(list(kexinit.get("mac_s2c", []))
                      + list(kexinit.get("mac_c2s", []))),
    }

    failures: list[dict] = []
    warnings: list[dict] = []
    unknown: list[dict] = []

    for category, algos in categories.items():
        for algo in algos:
            found = lookup(category, algo)
            if found is None:
                unknown.append({"category": category, "algorithm": algo})
                continue
            fails, warns, _infos = found
            if fails:
                failures.append({"category": category, "algorithm": algo,
                                 "reasons": list(fails)})
            if warns:
                warnings.append({"category": category, "algorithm": algo,
                                 "reasons": list(warns)})

    # Terrapin (CVE-2023-48795): prefix-truncation applies to chacha20-poly1305
    # ciphers (always), and to any CBC cipher paired with an Encrypt-then-MAC MAC.
    # Strict key exchange (the server marker kex-strict-s-v00@openssh.com) is the
    # counter-measure. Matches ssh-audit's server-audit logic (ssh_audit.py L448+):
    # chacha matched by prefix; CBC+ETM requires ≥1 of each.
    kex = kexinit.get("kex_algorithms", [])
    supports_strict_kex = "kex-strict-s-v00@openssh.com" in kex
    enc = categories["enc"]
    mac = categories["mac"]
    chacha = any(c.startswith("chacha20-poly1305") for c in enc)
    cbc_etm = any("-cbc" in c for c in enc) and any(
        m.endswith("-etm@openssh.com") for m in mac)
    terrapin_applicable = chacha or cbc_etm
    terrapin_vulnerable = terrapin_applicable and not supports_strict_kex

    return {
        "failures": failures,
        "warnings": warnings,
        "unknown": unknown,
        "supports_strict_kex": supports_strict_kex,
        "terrapin_vulnerable": terrapin_vulnerable,
    }


# ── scanner ───────────────────────────────────────────────────────────────────
def _read_ident(sock: socket.socket, *, max_lines: int = 20,
                max_bytes: int = 4096) -> str | None:
    """Read the server SSH identification line, skipping any pre-banner text
    lines a server may legally send before its 'SSH-...' string (RFC 4253 §4.2).
    Bounded (max_lines / max_bytes) so a banner flood or tarpit can't hang us."""
    buf = b""
    lines = 0
    while lines < max_lines and len(buf) < max_bytes:
        chunk = sock.recv(1)
        if not chunk:
            break
        buf += chunk
        if chunk == b"\n":
            line = buf.strip()
            if line.startswith(b"SSH-"):
                return line.decode("latin-1", "replace")
            buf = b""
            lines += 1
    return None


def _recv_exact(sock: socket.socket, n: int) -> bytes | None:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def _read_packet(sock: socket.socket, *, max_len: int = 65536) -> bytes | None:
    """Read one unencrypted SSH binary packet and return its payload (RFC 4253
    §6). Pre-key-exchange packets have no MAC, so this framing is unambiguous."""
    header = _recv_exact(sock, 4)
    if header is None:
        return None
    (packet_length,) = struct.unpack(">I", header)
    if not (1 <= packet_length <= max_len):
        return None
    body = _recv_exact(sock, packet_length)
    if body is None or not body:
        return None
    padding_length = body[0]
    payload = body[1:packet_length - padding_length]
    return payload


class SSHScanner(BaseScanner):
    name = "ssh_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_SSH_PORTS

    def _probe(self, target: str, port: int):
        """Blocking: connect, exchange identification, read the server KEXINIT.
        Returns (server_ident_str_or_None, kexinit_payload_bytes_or_None).

        We send our identification string FIRST, then read the server's — some
        servers wait for the client banner before sending anything (a common
        failure mode noted in the risks analysis), and sending first avoids that
        deadlock while remaining fully RFC 4253 §4.2 compliant."""
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                s.sendall(CLIENT_ID + b"\r\n")
                ident = _read_ident(s)
                payload = _read_packet(s)
                if not payload or payload[0] != SSH_MSG_KEXINIT:
                    return ident, None
                return ident, payload
        except OSError:
            return None, None

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                ident, kex_raw = await loop.run_in_executor(
                    None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not kex_raw:
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason="no_ssh_kexinit",
                              data={"ssh": False, "banner": ident})

        kexinit = parse_kexinit(kex_raw)
        ev = evaluate_algorithms(kexinit)
        banner = parse_ssh_banner(ident) if ident else None
        data = {
            "ssh": True,
            "banner": banner,
            "kex_algorithms": kexinit["kex_algorithms"],
            "server_host_key_algorithms": kexinit["server_host_key_algorithms"],
            "encryption": _dedup(list(kexinit["encryption_s2c"])
                                 + list(kexinit["encryption_c2s"])),
            "mac": _dedup(list(kexinit["mac_s2c"]) + list(kexinit["mac_c2s"])),
            **ev,
        }
        sw = banner["software"] if banner else "?"
        evidence = (f"{sw}; {len(ev['failures'])} weak / {len(ev['warnings'])} warn"
                    + ("; Terrapin-vulnerable" if ev["terrapin_vulnerable"] else ""))
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("SSH configuration / algorithm audit")
    parser.add_argument("-p", "--ports", default=None,
                        help="SSH ports (default: 22)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_SSH_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = SSHScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
