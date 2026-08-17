"""
service_enum.py — enrichment / enumeration layer that runs AFTER host_discovery.

SCOPE (same contract as the rest of the toolkit — read before use):
  * COLLECTION / OBSERVATION only. It connects, reads what a service voluntarily
    advertises about itself, and records it. It performs NO authentication,
    NO brute force, NO credential spraying, NO exploitation, and sends NO
    payload designed to alter a target's state.
  * Every probe is a normal client handshake (an HTTP GET, a TLS ClientHello, an
    SMB negotiate, reading a banner the server sends first). These are the same
    read-only interactions `nmap -sV`, `curl -I`, and `openssl s_client` perform.
  * Findings such as "SMBv1 offered" or "TLS 1.0 accepted" are DEFENSIVE
    identification of weak configuration — the thing a defender most wants an
    inventory to surface. Nothing here acts on those findings.

What this adds to the plain liveness scan:
  * Hostnames         — reverse DNS + mDNS (5353) + NetBIOS node status (137).
  * Service/version   — banner grab + HTTP Server/title + TLS cert/version.
  * OS hint           — synthesized from banners, HTTP, SMB and Windows-port
                        presence (honest, best-effort; true TTL/stack
                        fingerprinting needs the privileged raw-socket engine).
  * Role tags         — DC / DNS / web / database / mail / file-share / printer /
                        camera / hypervisor / gateway, from the open-port
                        signature (purely descriptive labelling).
  * Weak/legacy flags — Telnet, FTP, TFTP, r-services, SMBv1, SSLv3/TLS1.0/1.1,
                        plaintext mail, rpcbind, X11.
  * Mgmt / auth tags  — SSH, RDP, WinRM, SNMP, IPMI, web-admin, LDAP, Kerberos,
                        global-catalog, RADIUS, IKE/VPN.
  * Local topology    — directly-connected subnets and default gateway, read
                        from THIS host's own routing table (no traffic sent).

Deliberately NOT included (and why): trust-relationship graphs, lateral-movement
path-finding, "initial-access / easiest-target" ranking. Those are offensive
operations *planning*, not observation — a different kind of artifact from an
asset inventory, and they need data this collector doesn't hold (credentials, AD
replication, session/ACL data). This module stays on the inventory side of that
line, consistent with scanner_base's "collection layer only; no correlation, no
risk scoring" contract. Feed its JSONL into whatever separate analysis layer you
run for authorized red-team work.
"""

from __future__ import annotations

import asyncio
import re
import shutil
import socket
import ssl
import struct
import subprocess
from dataclasses import dataclass, field

from .scanner_base import (
    BaseScanner, ScanResult, TOP_TCP_PORTS, base_argparser, run_cli,
    setup_logging, main_entrypoint, bracket_host, LOG,
)

# --------------------------------------------------------------------------- #
# Port knowledge tables. Pure data — a port being open is descriptive, never a
# claim that the service is vulnerable.
# --------------------------------------------------------------------------- #
SERVICE_NAMES = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns", 69: "tftp",
    80: "http", 88: "kerberos", 110: "pop3", 111: "rpcbind", 135: "msrpc",
    137: "netbios-ns", 139: "netbios-ssn", 143: "imap", 161: "snmp",
    389: "ldap", 443: "https", 445: "smb", 465: "smtps", 500: "ike",
    514: "syslog", 515: "printer-lpd", 587: "submission", 623: "ipmi",
    631: "ipp", 636: "ldaps", 993: "imaps", 995: "pop3s", 1194: "openvpn",
    1433: "mssql", 1521: "oracle", 1723: "pptp", 2049: "nfs", 3268: "gc-ldap",
    3269: "gc-ldaps", 3306: "mysql", 3389: "rdp", 5432: "postgres",
    5900: "vnc", 5984: "couchdb", 5985: "winrm-http", 5986: "winrm-https",
    6000: "x11", 6379: "redis", 8006: "proxmox", 8080: "http-alt",
    8443: "https-alt", 8888: "http-alt", 9100: "jetdirect", 9200: "elastic",
    11211: "memcached", 11434: "ollama", 27017: "mongodb", 902: "vmware-esxi",
    554: "rtsp", 1812: "radius", 4500: "ipsec-nat",
}

# Ports whose plaintext handshake we can read directly (server speaks first, or a
# trivial newline nudge is enough).
BANNER_PORTS = {21, 22, 23, 25, 110, 143, 587, 465, 993, 995, 3306, 6379, 11211}
HTTP_PORTS = {80, 8080, 8888, 8006, 9200, 11434, 631}
TLS_PORTS = {443, 8443, 465, 993, 995, 636, 3269, 5986, 990}

# Management / remote-admin surfaces (identification only).
MGMT_PORTS = {
    22: "ssh", 23: "telnet-mgmt", 3389: "rdp", 5985: "winrm", 5986: "winrm-tls",
    161: "snmp", 623: "ipmi", 902: "vmware", 8006: "proxmox", 5900: "vnc",
}
# Authentication / directory surfaces.
AUTH_PORTS = {
    88: "kerberos", 389: "ldap", 636: "ldaps", 3268: "gc-ldap",
    3269: "gc-ldaps", 445: "smb-auth", 1812: "radius", 500: "ike/vpn",
    4500: "ipsec", 1194: "openvpn", 1723: "pptp",
}
# Weak / legacy protocols worth flagging on sight (before any probe).
LEGACY_PORTS = {
    21: "ftp-cleartext", 23: "telnet-cleartext", 69: "tftp", 111: "rpcbind",
    512: "rexec", 513: "rlogin", 514: "rsh", 110: "pop3-cleartext",
    143: "imap-cleartext", 6000: "x11-open",
}


@dataclass
class Enrichment:
    """Everything learned about one target beyond 'it is alive'."""
    hostnames: dict = field(default_factory=dict)   # {source: name}
    services: dict = field(default_factory=dict)    # {port: {...}}
    os_guess: str | None = None
    os_confidence: float = 0.0
    roles: list = field(default_factory=list)
    mgmt: list = field(default_factory=list)
    auth: list = field(default_factory=list)
    weak: list = field(default_factory=list)


# --------------------------------------------------------------------------- #
# Hostname resolution — reverse DNS, mDNS, NetBIOS. All best-effort, none raise.
# --------------------------------------------------------------------------- #
def reverse_dns(ip: str) -> str | None:
    try:
        return socket.gethostbyaddr(ip)[0]
    except (OSError, socket.herror):
        return None


def _dns_read_name(buf: bytes, off: int) -> tuple[str, int]:
    """Decode a DNS name (with 0xC0 compression) -> (name, next_offset)."""
    labels, jumped, orig = [], False, off
    for _ in range(128):  # guard against pointer loops
        if off >= len(buf):
            break
        ln = buf[off]
        if ln & 0xC0 == 0xC0:                       # compression pointer
            ptr = ((ln & 0x3F) << 8) | buf[off + 1]
            if not jumped:
                orig = off + 2
            off, jumped = ptr, True
            continue
        off += 1
        if ln == 0:
            break
        labels.append(buf[off:off + ln].decode("ascii", "replace"))
        off += ln
    return ".".join(labels), (orig if jumped else off)


def mdns_hostname(ip: str, timeout: float = 1.0) -> str | None:
    """Ask the host over multicast DNS (5353) for the PTR of its own address."""
    rev = ".".join(reversed(ip.split("."))) + ".in-addr.arpa"
    q = bytearray(struct.pack("!HHHHHH", 0, 0, 1, 0, 0, 0))
    for part in rev.split("."):
        q += bytes([len(part)]) + part.encode()
    q += b"\x00" + struct.pack("!HH", 12, 0x8001)   # PTR, IN + unicast-response
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(timeout)
        s.sendto(bytes(q), ("224.0.0.251", 5353))
        data, _ = s.recvfrom(4096)
        # skip header + question, walk to first PTR answer's rdata name
        off = 12
        _, off = _dns_read_name(data, off)
        off += 4                                     # qtype+qclass
        name, off = _dns_read_name(data, off)        # answer owner
        off += 10                                    # type,class,ttl,rdlen
        target, _ = _dns_read_name(data, off)
        return target or None
    except (OSError, IndexError, struct.error):
        return None
    finally:
        s.close()


def _nb_encode(name: str) -> bytes:
    """NetBIOS first-level name encoding (16-byte name -> 32 nibble bytes)."""
    padded = (name.upper() + " " * 16)[:15] + "\x00"
    out = bytearray()
    for ch in padded.encode("ascii", "replace"):
        out.append((ch >> 4) + 0x41)
        out.append((ch & 0x0F) + 0x41)
    return bytes(out)


def netbios_name(ip: str, timeout: float = 1.0) -> str | None:
    """NBNS node-status (NBSTAT) query to UDP/137; return the workstation name."""
    pkt = struct.pack("!HHHHHH", 0x4b3d, 0x0000, 1, 0, 0, 0)
    pkt += b"\x20" + _nb_encode("*") + b"\x00"
    pkt += struct.pack("!HH", 0x0021, 0x0001)        # NBSTAT, IN
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(timeout)
        s.sendto(pkt, (ip, 137))
        data, _ = s.recvfrom(4096)
        # header(12) + echoed question(name+4) then RR: name+type+class+ttl+rdlen
        off = 12
        while off < len(data) and data[off] != 0:
            off += data[off] + 1
        off += 1 + 4                                  # null + qtype/qclass
        off += 2 + 2 + 2 + 4                           # name-ptr,type,class,ttl
        rdlen = struct.unpack_from("!H", data, off)[0]; off += 2  # noqa: E702
        count = data[off]; off += 1
        for _ in range(count):
            nm = data[off:off + 15].decode("ascii", "replace").strip()
            flags = struct.unpack_from("!H", data, off + 16)[0]
            off += 18
            if not (flags & 0x8000) and nm and not nm.startswith("\x01"):
                return nm                             # first unique (non-group)
        return None
    except (OSError, IndexError, struct.error):
        return None
    finally:
        s.close()


async def resolve_hostnames(ip: str, timeout: float) -> dict:
    """Run the three name sources concurrently off the event loop."""
    rdns, mdns, nbns = await asyncio.gather(
        asyncio.to_thread(reverse_dns, ip),
        asyncio.to_thread(mdns_hostname, ip, timeout),
        asyncio.to_thread(netbios_name, ip, timeout),
    )
    out = {}
    if rdns:
        out["reverse_dns"] = rdns
    if mdns:
        out["mdns"] = mdns.rstrip(".")
    if nbns:
        out["netbios"] = nbns
    return out


# --------------------------------------------------------------------------- #
# TLS + SMB probes (read-only handshakes) run in threads.
# --------------------------------------------------------------------------- #
def tls_info(ip: str, port: int, timeout: float) -> dict | None:
    """One permissive TLS handshake: negotiated version + cert subject/issuer."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((ip, port), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=None) as s:
                cert = s.getpeercert(binary_form=False) or {}
                info = {"tls_version": s.version()}
                der = s.getpeercert(binary_form=True)
                if der:
                    info["cert_present"] = True
                subj = cert.get("subject") or ()
                cn = next((v for t in subj for (k, v) in t if k == "commonName"),
                          None)
                if cn:
                    info["cert_cn"] = cn
                return info
    except (OSError, ssl.SSLError, ValueError):
        return None


def tls_accepts_old(ip: str, port: int, timeout: float) -> list:
    """Which deprecated TLS/SSL versions the server still accepts (weak-config)."""
    weak = []
    attempts = [("TLSv1", ssl.TLSVersion.TLSv1), ("TLSv1.1", ssl.TLSVersion.TLSv1_1)]
    for label, ver in attempts:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            ctx.minimum_version = ver
            ctx.maximum_version = ver
        except (ValueError, OSError):
            continue
        try:
            with socket.create_connection((ip, port), timeout=timeout) as raw:
                with ctx.wrap_socket(raw, server_hostname=None) as s:
                    if s.version() in (label, "TLSv1", "TLSv1.1"):
                        weak.append(label)
        except (OSError, ssl.SSLError, ValueError):
            pass
    return weak


# Minimal SMBv1 NEGOTIATE PROTOCOL request (read-only). If the server answers
# with an SMB1 header (0xFF 'SMB'), it still speaks SMBv1.
_SMB1_NEG = bytes.fromhex(
    "000000a4"                                      # NetBIOS session, len 0xA4
    "ff534d4272000000001801280000000000000000000000000000"
    "0000fffe00004000"
    "00620002"
) + b"\x02PC NETWORK PROGRAM 1.0\x00\x02LANMAN1.0\x00" \
  b"\x02Windows for Workgroups 3.1a\x00\x02LM1.2X002\x00" \
  b"\x02LANMAN2.1\x00\x02NT LM 0.12\x00"


def smb_dialects(ip: str, timeout: float) -> dict | None:
    """Negotiate against 445; report whether SMBv1 is offered (defensive flag)."""
    try:
        with socket.create_connection((ip, 445), timeout=timeout) as s:
            s.sendall(_SMB1_NEG)
            resp = s.recv(1024)
        if len(resp) >= 8 and resp[4:8] == b"\xffSMB":
            return {"smbv1_offered": True}
        if len(resp) >= 8 and resp[4:8] == b"\xfeSMB":
            return {"smbv1_offered": False, "smb2plus": True}
        return {"smbv1_offered": False}
    except (OSError, struct.error):
        return None


# --------------------------------------------------------------------------- #
# OS + role synthesis — pure functions over collected evidence.
# --------------------------------------------------------------------------- #
def guess_os(open_ports: set, services: dict, hostnames: dict,
             ttl: int | None = None) -> tuple:
    """Best-effort OS guess from voluntary evidence. Returns (label, confidence).

    When a TTL is supplied (privileged/root run via ICMP), it is used as a
    strong OS-*family* signal (nmap -O style) and corroborated by the banner and
    port-shape evidence. Unprivileged, `ttl` is None and the guess falls back to
    banners + port shape only.
    """
    windows_ports = {135, 139, 445, 3389, 5985}
    hay = " ".join(
        str(v.get("banner", "")) + " " + str(v.get("server", "")) +
        " " + str(v.get("os", "")) for v in services.values()
    ).lower()

    # Banner text is the most specific evidence — trust it first.
    if "windows" in hay or "microsoft" in hay or "-iis" in hay:
        return "Windows", 0.85 if ttl and 64 < ttl <= 128 else 0.8

    # TTL family signal — only ever set by a privileged ICMP probe. This scanner
    # is now unprivileged (matching scanner_base / host_discovery), so ttl is
    # always None here and this branch stays dormant. TTL/OS fingerprinting now
    # lives in nmap_wrapper (privileged); we fall back to banners + port shape.
    ttl_fam = None
    if ttl_fam:
        # Combine TTL family with port-shape corroboration for a firmer call.
        if ttl_fam == "Windows" or len(open_ports & windows_ports) >= 2:
            conf = 0.75 if ttl_fam == "Windows" else 0.6
            return f"Windows (TTL {ttl}, SMB/RPC surface)" \
                   if len(open_ports & windows_ports) >= 2 \
                   else f"Windows (TTL {ttl})", conf
        if ttl_fam.startswith("Linux"):
            return f"Linux/Unix/macOS (TTL {ttl})", 0.65
        if ttl_fam.startswith("network"):
            return f"network device / BSD / Solaris (TTL {ttl})", 0.6

    if len(open_ports & windows_ports) >= 2:
        return "Windows (likely — SMB/RPC/RDP surface)", 0.55
    for tok, label in (("ubuntu", "Linux (Ubuntu)"), ("debian", "Linux (Debian)"),
                       ("centos", "Linux (CentOS)"), ("raspbian", "Linux (Raspberry Pi OS)"),
                       ("freebsd", "FreeBSD"), ("mikrotik", "MikroTik RouterOS"),
                       ("cisco", "Cisco IOS"), ("openwrt", "OpenWrt")):
        if tok in hay:
            return label, 0.75
    if "openssh" in hay:
        return "Unix-like (OpenSSH present)", 0.45
    return None, 0.0


def classify_roles(open_ports: set) -> list:
    """Descriptive role tags from the open-port signature."""
    p, roles = open_ports, []
    if {88, 389} <= p and (445 in p or 135 in p):
        roles.append("domain_controller?")
    elif 389 in p or 636 in p:
        roles.append("ldap/directory")
    if 53 in p:
        roles.append("dns")
    if p & {80, 443, 8080, 8443, 8888}:
        roles.append("web")
    if p & {1433, 3306, 5432, 1521, 6379, 27017, 9200, 5984, 11211}:
        roles.append("database")
    if p & {25, 465, 587, 110, 143, 993, 995}:
        roles.append("mail")
    if p & {445, 139, 2049}:
        roles.append("file-share")
    if p & {515, 631, 9100}:
        roles.append("printer")
    if 554 in p:
        roles.append("camera/rtsp")
    if p & {902, 8006}:
        roles.append("hypervisor")
    if p & {500, 4500, 1194, 1723}:
        roles.append("vpn")
    return roles


def tags_for(open_ports: set, table: dict) -> list:
    return sorted({f"{table[pt]}:{pt}" for pt in open_ports if pt in table})


# --------------------------------------------------------------------------- #
# Local topology — read THIS host's routing table; no packets sent to targets.
# --------------------------------------------------------------------------- #
def local_topology() -> dict:
    """Directly-connected subnets and default gateway(s) from the OS route table."""
    subnets: set = set()
    gateways: set = set()
    # Linux
    if shutil.which("ip"):
        try:
            out = subprocess.run(["ip", "route"], capture_output=True,
                                 text=True, timeout=4).stdout
            for line in out.splitlines():
                if line.startswith("default"):
                    m = re.search(r"via (\d+\.\d+\.\d+\.\d+)", line)
                    if m:
                        gateways.add(m.group(1))
                m = re.match(r"(\d+\.\d+\.\d+\.\d+/\d+) .*proto kernel", line)
                if m:
                    subnets.add(m.group(1))
        except (OSError, subprocess.SubprocessError):
            pass
    # macOS / BSD
    if not subnets and shutil.which("netstat"):
        try:
            out = subprocess.run(["netstat", "-rn", "-f", "inet"],
                                 capture_output=True, text=True, timeout=4).stdout
            for line in out.splitlines():
                cols = line.split()
                if len(cols) >= 2 and cols[0] == "default":
                    if re.match(r"\d+\.\d+\.\d+\.\d+", cols[1]):
                        gateways.add(cols[1])
        except (OSError, subprocess.SubprocessError):
            pass
    if shutil.which("ifconfig"):
        try:
            out = subprocess.run(["ifconfig"], capture_output=True,
                                 text=True, timeout=4).stdout
            for m in re.finditer(
                r"inet (\d+\.\d+\.\d+\.\d+) netmask (0x[0-9a-f]+)", out):
                ip = m.group(1)
                mask = int(m.group(2), 16)
                if ip.startswith("127."):
                    continue
                prefix = bin(mask).count("1")
                octets = [(mask >> (24 - 8 * i)) & 0xFF for i in range(4)]
                ipo = [int(x) for x in ip.split(".")]
                net = ".".join(str(ipo[i] & octets[i]) for i in range(4))
                subnets.add(f"{net}/{prefix}")
        except (OSError, subprocess.SubprocessError):
            pass
    return {"connected_subnets": sorted(subnets), "gateways": sorted(gateways)}


# --------------------------------------------------------------------------- #
# The scanner.
# --------------------------------------------------------------------------- #
class ServiceEnumScanner(BaseScanner):
    name = "service_enum"

    def __init__(self, *args, ports: list | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = list(ports if ports is not None else TOP_TCP_PORTS)

    async def _open(self, target: str, port: int):
        await self.limiter.wait()
        async with self.sem:
            try:
                fut = asyncio.open_connection(target, port)
                return await asyncio.wait_for(fut, timeout=self.timeout)
            except (asyncio.TimeoutError, OSError):
                return None

    async def _probe_port(self, target: str, port: int) -> dict | None:
        """Connect to one port and read whatever it voluntarily advertises."""
        conn = await self._open(target, port)
        if conn is None:
            return None
        reader, writer = conn
        info: dict = {"service": SERVICE_NAMES.get(port, "unknown")}
        try:
            if port in HTTP_PORTS:
                host = bracket_host(target)
                writer.write(
                    f"GET / HTTP/1.0\r\nHost: {host}\r\n"
                    f"User-Agent: service_enum\r\n\r\n".encode())
                await writer.drain()
                raw = await asyncio.wait_for(reader.read(4096), timeout=self.timeout)
                text = raw.decode("latin-1", "replace")
                m = re.search(r"^Server:\s*(.+)$", text, re.I | re.M)
                if m:
                    info["server"] = m.group(1).strip()
                m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
                if m:
                    info["title"] = m.group(1).strip()[:120]
                m = re.match(r"HTTP/[\d.]+ (\d{3})", text)
                if m:
                    info["http_status"] = int(m.group(1))
            elif port in BANNER_PORTS:
                try:
                    raw = await asyncio.wait_for(reader.read(512), timeout=1.5)
                except asyncio.TimeoutError:
                    raw = b""
                if not raw:                       # nudge protocols that stay quiet
                    writer.write(b"\r\n")
                    await writer.drain()
                    try:
                        raw = await asyncio.wait_for(reader.read(512), timeout=1.5)
                    except asyncio.TimeoutError:
                        raw = b""
                banner = raw.decode("latin-1", "replace").strip()
                if banner:
                    info["banner"] = banner[:200]
        except (asyncio.TimeoutError, OSError):
            pass
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

        # TLS / SMB handshakes off the loop.
        if port in TLS_PORTS:
            t = await asyncio.to_thread(tls_info, target, port, self.timeout)
            if t:
                info.update(t)
                old = await asyncio.to_thread(
                    tls_accepts_old, target, port, self.timeout)
                if old:
                    info["weak_tls"] = old
        if port == 445:
            smb = await asyncio.to_thread(smb_dialects, target, self.timeout)
            if smb:
                info.update(smb)
        return info

    async def scan_target(self, target: str) -> list[ScanResult]:
        # 1) which ports answer
        results = await asyncio.gather(
            *(self._probe_port(target, p) for p in self.ports))
        services = {p: r for p, r in zip(self.ports, results) if r is not None}
        open_ports = set(services)

        if not open_ports:
            # Nothing answered — still try names (silent host may resolve).
            hostnames = await resolve_hostnames(target, min(self.timeout, 1.5))
            data = {"open_ports": [], "hostnames": hostnames}
            return [ScanResult(scanner=self.name, target=target,
                               status="filtered", data=data, vantage=self.name,
                               evidence="no service responded")]

        # 2) names, in parallel with nothing else needed now
        hostnames = await resolve_hostnames(target, min(self.timeout, 1.5))

        # 2b) TTL fingerprint was a privileged (root) ICMP probe. This scanner is
        # now unprivileged (matching scanner_base / host_discovery), so we no
        # longer send raw ICMP: ttl stays None and guess_os uses banners + port
        # shape. For TTL/OS fingerprinting use nmap_wrapper (privileged).
        ttl = None

        # 3) synthesize
        os_label, os_conf = guess_os(open_ports, services, hostnames, ttl)
        enr = Enrichment(
            hostnames=hostnames,
            services={str(p): v for p, v in services.items()},
            os_guess=os_label, os_confidence=os_conf,
            roles=classify_roles(open_ports),
            mgmt=tags_for(open_ports, MGMT_PORTS),
            auth=tags_for(open_ports, AUTH_PORTS),
            weak=tags_for(open_ports, LEGACY_PORTS),
        )
        # weak-protocol findings discovered by probe (not just by port number)
        for p, v in services.items():
            if v.get("smbv1_offered"):
                enr.weak.append("smbv1-offered:445")
            if v.get("weak_tls"):
                enr.weak.append(f"weak-tls:{p}:{','.join(v['weak_tls'])}")
        enr.weak = sorted(set(enr.weak))

        data = {
            "open_ports": sorted(open_ports),
            "hostnames": enr.hostnames,
            "services": enr.services,
            "os_guess": enr.os_guess,
            "os_confidence": round(enr.os_confidence, 2),
            "ttl": ttl,
            "roles": enr.roles,
            "management_surfaces": enr.mgmt,
            "auth_surfaces": enr.auth,
            "weak_legacy": enr.weak,
            "vantage": self.name,
        }
        primary = next(iter(hostnames.values()), None)
        bits = [f"{len(open_ports)} svc"]
        if primary:
            bits.append(f"name={primary}")
        if enr.os_guess:
            bits.append(f"os={enr.os_guess}")
        if enr.roles:
            bits.append("roles=" + "/".join(enr.roles))
        if enr.weak:
            bits.append("weak=" + ",".join(enr.weak))

        return [ScanResult(scanner=self.name, target=target, status="open",
                           data=data, vantage=self.name,
                           evidence="; ".join(bits))]


def main() -> None:
    parser = base_argparser("Service / OS / role enumeration scanner")
    parser.add_argument("-p", "--ports",
                        help="comma/range port spec (default: TOP_TCP_PORTS)")
    parser.add_argument("--topology", action="store_true",
                        help="also print this host's connected subnets + gateway")
    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.topology:
        import json
        print(json.dumps({"local_topology": local_topology()}))

    from .scanner_base import parse_ports
    ports = parse_ports(args.ports) if args.ports else None

    def build(scope, **kw):
        return ServiceEnumScanner(scope, ports=ports, **kw)

    main_entrypoint(lambda: run_cli(build, args))


if __name__ == "__main__":
    main()