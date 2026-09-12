"""
db_scanner.py — fingerprint database services.

WHY: databases are everywhere on internal networks and frequently exposed. A
plain banner grab does NOT identify most of them, because they speak BINARY
protocols, not text banners. This module sends each DB's minimal, valid,
READ-ONLY handshake/ping and identifies the service (and version where the
protocol volunteers it).

Covered: MySQL/MariaDB, PostgreSQL, Microsoft SQL Server, Redis, MongoDB,
and a light Oracle TNS probe.

COLLECTION ONLY: we perform protocol negotiation / server-greeting reads and, at
most, an unauthenticated INFO/version ping that the protocol offers publicly
(e.g. Redis INFO, MySQL server greeting). We do NOT authenticate with guessed
credentials, run queries, enumerate data, or modify anything. The output is
"a PostgreSQL server (v14.x) is listening here" — a fact, not an intrusion.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

# Default port -> probe kind. Multiple ports can map to the same engine.
DEFAULT_DB_PORTS = {
    3306: "mysql",
    33060: "mysqlx",
    5432: "postgres",
    1433: "mssql",
    6379: "redis",
    27017: "mongodb",
    1521: "oracle",
}


# --------------------------------------------------------------------------- #
# Per-engine probes. Each returns a dict of facts or None.
# --------------------------------------------------------------------------- #
# MySQL Protocol::CapabilityFlags. CLIENT_SSL is bit 11, which lives in the
# LOWER 16 bits — the half the initial handshake always carries, before any
# authentication happens.
_MYSQL_CLIENT_SSL = 0x0800


def parse_mysql_greeting(data: bytes) -> dict | None:
    """Parse a MySQL/MariaDB initial handshake packet.

    Returns None when this is not a v9/v10 handshake: identification is by
    protocol structure, never by port number.

    `ssl_supported` comes from the server's OWN advertised capability flags, so
    it is a statement the server made rather than an inference. It is reported
    only when the packet actually reached the flags — treating a short read as
    "TLS not offered" would invert the finding and manufacture a cleartext
    report against a correctly configured server.
    """
    if len(data) < 6:
        return None
    proto = data[4]
    if proto not in (10, 9):
        return None
    rest = data[5:]
    end = rest.find(b"\x00")
    version = rest[:end].decode("latin-1", "replace") if end > 0 else None
    out: dict = {"engine": "mysql/mariadb", "protocol_version": proto,
                 "server_version": version}
    if end < 0:
        return out
    # Layout after version\0: connection id (4) + auth-plugin-data-part-1 (8) +
    # filler (1) = 13 bytes, then capability_flags_1 (2, little-endian).
    # Protocol 9 predates the flags entirely, so it is never parsed for them.
    tail = rest[end + 1:]
    if proto == 10 and len(tail) >= 15:
        caps_low = int.from_bytes(tail[13:15], "little")
        out["capability_flags"] = caps_low
        out["ssl_supported"] = bool(caps_low & _MYSQL_CLIENT_SSL)
    return out


async def _probe_mysql(reader, writer, timeout) -> dict | None:
    # MySQL/MariaDB server speaks first: the initial handshake packet carries the
    # server version and the server's advertised capability flags.
    try:
        data = await asyncio.wait_for(reader.read(256), timeout=timeout)
    except asyncio.TimeoutError:
        return None
    return parse_mysql_greeting(data)


async def _probe_postgres(reader, writer, timeout) -> dict | None:
    # Send an SSLRequest (8 bytes). Postgres replies 'S' (ssl ok) or 'N' (no ssl)
    # — either single-byte reply confirms a PostgreSQL server.
    try:
        writer.write(struct.pack("!ii", 8, 80877103))  # length=8, SSLRequest code
        await writer.drain()
        data = await asyncio.wait_for(reader.read(1), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        return None
    if data in (b"S", b"N"):
        return {"engine": "postgresql",
                "ssl_supported": data == b"S"}
    return None


# TDS PRELOGIN option tokens (MS-TDS 2.2.6.5).
_TDS_VERSION_TOKEN = 0x00
_TDS_ENCRYPTION_TOKEN = 0x01
_TDS_TERMINATOR = 0xFF

# PL_OPTION ENCRYPTION values. The distinction matters for posture: under
# ENCRYPT_OFF the LOGIN packet itself is STILL encrypted by TDS, so credentials
# are not exposed — only session data is. ENCRYPT_NOT_SUP is the one value that
# means the server cannot protect anything, credentials included.
_TDS_ENCRYPTION_MODES = {
    0x00: "off",             # available, not requested (login packet still encrypted)
    0x01: "on",              # available and negotiated
    0x02: "not_supported",   # server cannot encrypt AT ALL
    0x03: "required",        # server refuses cleartext
}


def _build_tds_prelogin() -> bytes:
    """A well-formed PRELOGIN request (MS-TDS 2.2.6.5).

    The previous request's option table was malformed — it decoded to a repeated
    VERSION token with a 256-byte offset and a 512-byte length. Servers answer it
    anyway, which is why identification worked, but a server only returns its own
    ENCRYPTION option when the CLIENT offers one. Encryption posture was therefore
    unobtainable, not merely unparsed.

    Offsets are computed from the table size rather than hardcoded, so adding an
    option cannot silently corrupt the ones after it.
    """
    opts = [
        (0x00, b"\x00" * 6),   # VERSION   — client version; zeros are accepted
        (0x01, b"\x00"),       # ENCRYPTION = ENCRYPT_OFF: we support it, don't demand it
        (0x02, b"\x00"),       # INSTOPT   — empty instance name
        (0x03, b"\x00" * 4),   # THREADID
        (0x04, b"\x00"),       # MARS off
    ]
    table_len = len(opts) * 5 + 1              # 5 bytes per option + terminator
    table, blob, off = b"", b"", table_len
    for token, payload in opts:
        table += struct.pack(">BHH", token, off, len(payload))
        blob += payload
        off += len(payload)
    table += bytes([_TDS_TERMINATOR])
    body = table + blob
    header = struct.pack(">BBHHBB", 0x12, 0x01, 8 + len(body), 0, 0, 0)
    return header + body


_TDS_PRELOGIN_REQUEST = _build_tds_prelogin()


def parse_tds_prelogin(data: bytes) -> dict:
    """Read server version and encryption posture out of a TDS PRELOGIN reply.

    Positive evidence only: fields appear ONLY when the server actually stated
    them. A truncated or unparseable option table yields the identification facts
    alone — never a guessed encryption stance, which would be a false negative
    dressed up as a clean result.
    """
    out: dict = {"engine": "microsoft sql server", "tds_response": True}
    if len(data) < 9 or data[0] != 0x04:
        return out
    payload = data[8:]                          # strip the 8-byte TDS header

    options: dict[int, tuple[int, int]] = {}
    i = 0
    while i < len(payload):
        token = payload[i]
        if token == _TDS_TERMINATOR:
            break
        if i + 5 > len(payload):
            return out                          # truncated table — claim nothing
        options[token] = (
            int.from_bytes(payload[i + 1:i + 3], "big"),
            int.from_bytes(payload[i + 3:i + 5], "big"),
        )
        i += 5

    def _blob(token: int) -> bytes | None:
        if token not in options:
            return None
        off, length = options[token]
        if length <= 0 or off + length > len(payload):
            return None
        return payload[off:off + length]

    ver = _blob(_TDS_VERSION_TOKEN)
    if ver and len(ver) >= 4:
        out["server_version"] = (
            f"{ver[0]}.{ver[1]}.{int.from_bytes(ver[2:4], 'big')}")

    enc = _blob(_TDS_ENCRYPTION_TOKEN)
    if enc:
        mode = _TDS_ENCRYPTION_MODES.get(enc[0])
        if mode is not None:
            out["encryption_mode"] = mode
            out["ssl_supported"] = mode != "not_supported"
            out["encryption_required"] = mode == "required"
    return out


async def _probe_mssql(reader, writer, timeout) -> dict | None:
    # TDS pre-login. A TDS response (type 0x04) confirms SQL Server; the reply's
    # option table also carries the server version and its encryption stance.
    try:
        writer.write(_TDS_PRELOGIN_REQUEST)
        await writer.drain()
        data = await asyncio.wait_for(reader.read(512), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        return None
    if data and data[0] == 0x04:
        return parse_tds_prelogin(data)
    return None


def interpret_redis_info(text: str) -> dict:
    """Classify a Redis INFO reply. `unauthenticated_read` is True only when we
    actually read server data with no credentials (the honest exposure signal)."""
    auth_required = "NOAUTH" in text
    m = re.search(r"redis_version:([0-9.]+)", text)
    return {
        "engine": "redis",
        "auth_required": auth_required,
        "unauthenticated_read": (not auth_required) and ("redis_version" in text),
        "server_version": m.group(1) if m else None,
    }


async def _probe_redis(reader, writer, timeout) -> dict | None:
    # Redis: send INFO server (RESP). Unauthenticated servers reply with a bulk
    # string of server info incl. version; auth-required servers reply -NOAUTH.
    try:
        writer.write(b"*2\r\n$4\r\nINFO\r\n$6\r\nserver\r\n")
        await writer.drain()
        data = await asyncio.wait_for(reader.read(2048), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        return None
    if not data:
        return None
    text = data.decode("latin-1", "replace")
    if "NOAUTH" in text or "redis_version" in text or text.startswith("$"):
        return interpret_redis_info(text)
    return None


def build_op_msg_command(command: str, db: str = "admin") -> bytes:
    """Frame a single-field admin command as OP_MSG (opcode 2013).

    MongoDB 5.1 REMOVED OP_QUERY for everything except the hello/isMaster
    handshake. Sending an OP_QUERY command to a modern server fails at the wire
    level, and reading that failure as "authentication is enforced" would be a
    false negative on precisely the exposed instances that matter most. So the
    identification probe keeps OP_QUERY isMaster (universally supported) and the
    auth probe uses OP_MSG.
    """
    cmd = (b"\x10" + command.encode() + b"\x00" + struct.pack("<i", 1))
    dbf = (b"\x02" + b"$db\x00"
           + struct.pack("<i", len(db) + 1) + db.encode() + b"\x00")
    doc_len = 4 + len(cmd) + len(dbf) + 1
    doc = struct.pack("<i", doc_len) + cmd + dbf + b"\x00"
    body = struct.pack("<I", 0) + b"\x00" + doc      # flagBits + section kind 0
    return struct.pack("<iiii", 16 + len(body), 2, 0, 2013) + body


# Markers in a serverStatus reply. BSON is not fully decoded — the existing
# version extraction already reads raw bytes — but every claim below rests on
# something the server actually said.
_MONGO_AUTH_MARKERS = (b"Unauthorized", b"not authorized", b"requires authentication")
_MONGO_OK_MARKERS = (b"uptime", b"localTime", b"connections")

# BSON string field: name\0 + int32 length + value. Tolerant of the length bytes
# so the same pattern reads a version out of either reply.
_MONGO_VERSION_RE = re.compile(rb"version\x00.{0,4}([0-9]+\.[0-9]+\.[0-9]+)")


def extract_mongo_version(blob: bytes) -> str | None:
    """Pull a MongoDB server version out of a wire reply, or None.

    The isMaster handshake does NOT carry a version on modern servers, which left
    every MongoDB in the estate with server_version=None — and a null version
    means the CVE track has nothing to match on, so a years-out-of-date MongoDB
    correlated to no CVEs at all. serverStatus does carry it.
    """
    m = _MONGO_VERSION_RE.search(blob or b"")
    return m.group(1).decode("latin-1", "replace") if m else None


def interpret_mongodb_auth(reply: bytes) -> dict:
    """Classify a serverStatus reply into auth posture.

    Returns {} when the reply says neither thing. Silence is NOT evidence of
    exposure, and it is not evidence of hardening either — an empty dict keeps
    the fact honest and leaves the manager's rule correctly unable to fire.
    """
    if not reply:
        return {}
    if any(m in reply for m in _MONGO_AUTH_MARKERS):
        return {"auth_required": True, "unauthenticated_read": False}
    if any(m in reply for m in _MONGO_OK_MARKERS):
        return {"auth_required": False, "unauthenticated_read": True}
    return {}


async def _probe_mongodb(reader, writer, timeout) -> dict | None:
    # Step 1 — identification. OP_QUERY {isMaster:1} on admin.$cmd is the one
    # command every server version still answers over OP_QUERY.
    try:
        bson = (b"\x10ismaster\x00\x01\x00\x00\x00\x00")
        bson = struct.pack("<i", len(bson) + 5) + bson + b"\x00"
        full_collection = b"admin.$cmd\x00"
        query = (struct.pack("<i", 0) + full_collection +
                 struct.pack("<i", 0) + struct.pack("<i", -1) + bson)
        body = struct.pack("<i", 0) + query
        header = struct.pack("<iiii", 16 + len(body), 1, 0, 2004)
        writer.write(header + body)
        await writer.drain()
        data = await asyncio.wait_for(reader.read(512), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        return None
    if len(data) < 16:
        return None
    opcode = struct.unpack("<i", data[12:16])[0]
    if opcode not in (1, 2004, 2013):
        return None
    facts: dict = {"engine": "mongodb", "wire_reply_opcode": opcode,
                   "server_version": extract_mongo_version(data)}

    # Step 2 — auth posture. isMaster is answered WITHOUT credentials even on a
    # fully hardened server, so it proves nothing about access control. Only a
    # command the server actually gates can. serverStatus is server metadata,
    # not user data — the same class of public INFO ping this module already
    # sends to Redis, so it stays inside the read-only contract.
    try:
        writer.write(build_op_msg_command("serverStatus"))
        await writer.drain()
        reply = await asyncio.wait_for(reader.read(2048), timeout=timeout)
        facts.update(interpret_mongodb_auth(reply))
        # The handshake rarely volunteers a version; serverStatus does. Without
        # this the CVE track has nothing to match a MongoDB against.
        if facts.get("server_version") is None:
            facts["server_version"] = extract_mongo_version(reply)
    except (asyncio.TimeoutError, OSError):
        pass                 # identification stands; auth posture stays unstated
    return facts


# Mysqlx.ServerMessages.Type values (0..13) — used to validate an X-protocol reply.
_XPROTO_SERVER_TYPES = frozenset(range(0, 14))


async def _probe_mysqlx(reader, writer, timeout) -> dict | None:
    # MySQL X Protocol (mysqlx, default port 33060). Unlike classic MySQL the
    # server sends NO greeting — the client speaks first. We send a
    # Connection.CapabilitiesGet (client message type 1, empty payload) framed as
    # X protocol: [uint32 LE length][1-byte msg type][payload]. A genuine reply is
    # itself an X-protocol frame: [uint32 LE length][1-byte ServerMessages type].
    #
    # The discriminator that separates this from Oracle TNS (whose loose matcher
    # used to claim 33060) is the LITTLE-endian length prefix exactly bounding the
    # frame AND a valid server message type at offset 4 — TNS uses a big-endian
    # length at offset 0, so it cannot satisfy both.
    try:
        frame = struct.pack("<I", 1) + bytes([1])  # len=1 (type byte only), type=CAP_GET
        writer.write(frame)
        await writer.drain()
        data = await asyncio.wait_for(reader.read(512), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        return None
    if len(data) < 5:
        return None
    msg_len = struct.unpack("<I", data[:4])[0]
    msg_type = data[4]
    # First frame must be well-formed (its LE length fits what we read) and carry a
    # known server message type (CONN_CAPABILITIES=2, ERROR=1, NOTICE=11, ...).
    if 1 <= msg_len <= len(data) - 4 and msg_type in _XPROTO_SERVER_TYPES:
        return {"engine": "mysql x protocol", "xproto_msg_type": msg_type}
    return None


async def _probe_oracle(reader, writer, timeout) -> dict | None:
    # Oracle TNS: a connect packet elicits a TNS response (type 2=accept,
    # 4=refuse, 5=redirect, 11=resend). A genuine TNS packet has a structured
    # header — 2-byte BIG-endian total length, 2-byte packet checksum (0 on modern
    # servers), then the type byte. We validate that structure instead of matching
    # a single byte at offset 4, which previously false-positived on any binary
    # protocol (notably MySQL X on 33060) whose 5th byte happened to be 2/4/11.
    try:
        # Minimal TNS connect packet.
        data_payload = (b"(CONNECT_DATA=(COMMAND=ping))")
        # TNS header: length(2), checksum(2), type(1=connect? use 1), reserved...
        tns = struct.pack(">HHBBH", 0, 0, 1, 0, 0) + data_payload
        tns = struct.pack(">H", len(tns)) + tns[2:]
        writer.write(tns)
        await writer.drain()
        data = await asyncio.wait_for(reader.read(256), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        return None
    if len(data) >= 8:
        declared_len = struct.unpack(">H", data[:2])[0]
        checksum = struct.unpack(">H", data[2:4])[0]
        tns_type = data[4]
        if (tns_type in (2, 4, 5, 11)
                and 8 <= declared_len <= len(data)
                and checksum == 0):
            return {"engine": "oracle tns", "tns_packet_type": tns_type}
    return None


_PROBES = {
    "mysql": _probe_mysql,
    "postgres": _probe_postgres,
    "mssql": _probe_mssql,
    "redis": _probe_redis,
    "mongodb": _probe_mongodb,
    # mysqlx MUST precede oracle: the X-protocol reply is structurally specific,
    # whereas the (now tightened) oracle probe must only match true TNS.
    "mysqlx": _probe_mysqlx,
    "oracle": _probe_oracle,
}


def stamp_db_fact(facts: dict) -> dict:
    """Stamp the `db: True` discriminator onto every db_scan fact.

    Every sibling deep-branch scanner emits a boolean marker (`ftp`, `dns`,
    `nfs`, `ldap`, `vnc`) and the manager's detectors all gate on it — the house
    pattern is `d.get("ftp") is True`. db_scanner emitted no such marker, so a
    posture rule could not follow the pattern and none was ever written.

    Stamped CENTRALLY here rather than inside each of the seven probes: a
    per-probe copy is exactly the drift that leaves one engine unassessable
    while the other six work.

    The marker is written LAST so probe payload cannot override it. It is an
    assertion by the scanner ("this fact came from db_scan"), not a field a
    protocol reply is allowed to contradict.
    """
    return {**facts, "db": True}


class DBScanner(BaseScanner):
    name = "db_scan"

    def __init__(self, *args, port_map: dict[int, str] | None = None,
                 try_all_on_port: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.port_map = port_map or DEFAULT_DB_PORTS
        # If True, try every probe on each port (useful for non-standard ports).
        self.try_all = try_all_on_port

    async def _probe_one(self, target: str, port: int, kind: str) -> dict | None:
        await self.limiter.wait()
        async with self.sem:
            try:
                fut = asyncio.open_connection(target, port)
                reader, writer = await asyncio.wait_for(fut, timeout=self.timeout)
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return None
            try:
                return await _PROBES[kind](reader, writer, self.timeout)
            except Exception:
                return None
            finally:
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass

    async def _scan_port(self, target: str, port: int) -> ScanResult | None:
        kinds = list(_PROBES.keys()) if self.try_all else \
            [self.port_map.get(port, "")]
        for kind in kinds:
            if not kind:
                continue
            facts = await self._probe_one(target, port, kind)
            if facts:
                facts = stamp_db_fact(facts)
                return ScanResult(
                    self.name, target, port=port, proto="tcp", status="open",
                    data=facts,
                    evidence=(f"{facts.get('engine')} "
                              f"{facts.get('server_version') or ''}".strip()))
        return None

    async def scan_target(self, target: str) -> list[ScanResult]:
        ports = list(self.port_map.keys())
        tasks = [self._scan_port(target, p) for p in ports]
        return [r for r in await asyncio.gather(*tasks) if r is not None]


def main() -> None:
    parser = base_argparser("Database service fingerprint scanner")
    parser.add_argument("-p", "--ports", default=None,
                        help="ports to probe (default: standard DB ports)")
    parser.add_argument("--try-all", action="store_true",
                        help="try every DB probe on each port (non-standard ports)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        if args.ports:
            # Unknown custom ports: enable try-all so we still identify them.
            port_map = {p: "" for p in parse_ports(args.ports)}
            try_all = True
        else:
            port_map = DEFAULT_DB_PORTS
            try_all = args.try_all

        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = DBScanner(scope, rate=args.rate, concurrency=args.concurrency,
                            timeout=args.timeout, port_map=port_map,
                            try_all_on_port=try_all)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
