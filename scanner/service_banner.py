"""
service_banner.py — grab service banners and light version strings.

METHOD (collection only): connect to a port and read whatever the service
voluntarily announces. For services that speak first (SSH, SMTP, FTP) we just
read. For services that wait (HTTP) we send a minimal, benign request and read
the response head. We RECORD the banner verbatim as evidence — we do NOT map it
to a CVE or decide a version is vulnerable. That is the (separate) detection
layer's job.

This keeps the module's output purely factual so its accuracy is measurable:
"port 22 returned banner X".
"""

from __future__ import annotations

import argparse
import asyncio
import re

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, bracket_host, setup_logging, base_argparser, main_entrypoint,
    user_agent,
)

# Probe sent to a port if the service does not greet us first.
# Keep these minimal and non-intrusive — a bare request, nothing exploit-like.
# UA comes from scanner_base (generic by default) so the probe carries no signature.
_HTTP_PROBE = (b"GET / HTTP/1.0\r\nHost: %b\r\nUser-Agent: "
               + user_agent().encode() + b"\r\n\r\n")
_GENERIC_PROBE = b"\r\n"

# Ports where the client must speak first.
_CLIENT_FIRST = {80, 8080, 8000, 8888, 443, 8443}

# --------------------------------------------------------------------------- #
# Service soft-matching (Tier 2.5) — banner -> {service, product, version}.
#
# Ordered most-specific first. Each entry: (compiled regex, service, product).
# `product=None` means "use the regex's (?P<product>...) group as the product".
# An optional (?P<version>...) group supplies the version. Matching is on bytes
# so it works on binary handshakes (MySQL) as well as text banners. Port-number
# independent: a service on a non-standard port still identifies by behaviour.
# --------------------------------------------------------------------------- #
_PATTERNS: list[tuple[re.Pattern, str, str | None]] = [
    # SSH — OpenSSH and dropbear are specific; a generic SSH catch-all follows.
    (re.compile(rb"SSH-\d+\.\d+-OpenSSH[_-](?P<version>[\w.]+)"), "ssh", "OpenSSH"),
    (re.compile(rb"SSH-\d+\.\d+-dropbear[_-](?P<version>[\w.]+)"), "ssh", "dropbear"),
    (re.compile(rb"SSH-\d+\.\d+-(?P<product>[\w.+\-]+)"), "ssh", None),
    # Datastores exposed over HTTP — must win over the generic Server: match
    # below (CouchDB sets `Server: CouchDB/x`, which would otherwise read as http).
    (re.compile(rb'"tagline"\s*:\s*"You Know, for Search"'), "elasticsearch", "Elasticsearch"),
    (re.compile(rb'"cluster_name"\s*:\s*"'), "elasticsearch", "Elasticsearch"),
    (re.compile(rb'"couchdb"\s*:\s*"Welcome"'), "couchdb", "CouchDB"),
    # HTTP Server header
    (re.compile(rb"[Ss]erver:\s*nginx(?:/(?P<version>[\d.]+))?"), "http", "nginx"),
    (re.compile(rb"[Ss]erver:\s*Apache(?:/(?P<version>[\d.]+))?"), "http", "Apache"),
    (re.compile(rb"[Ss]erver:\s*Microsoft-IIS/(?P<version>[\d.]+)"), "http",
     "Microsoft-IIS"),
    (re.compile(rb"[Ss]erver:\s*(?P<product>[\w\-]+)/(?P<version>[\d.]+)"), "http",
     None),
    # FTP
    (re.compile(rb"vsFTPd (?P<version>[\d.]+)"), "ftp", "vsftpd"),
    (re.compile(rb"ProFTPD (?P<version>[\d.]+)"), "ftp", "ProFTPD"),
    (re.compile(rb"220[- ].*FTP", re.I), "ftp", None),
    # SMTP
    (re.compile(rb"ESMTP (?P<product>Postfix|Exim|Sendmail)"), "smtp", None),
    (re.compile(rb"220[- ].*SMTP", re.I), "smtp", None),
    # Databases / caches
    (re.compile(rb"(?P<version>\d+\.\d+\.\d+)-MariaDB"), "mysql", "MariaDB"),
    (re.compile(rb"(?P<version>[45]\.\d+\.\d+)\W.*mysql_native_password"), "mysql",
     "MySQL"),
    (re.compile(rb"mysql_native_password"), "mysql", "MySQL"),
    (re.compile(rb"redis_version:(?P<version>[\d.]+)"), "redis", "Redis"),
    (re.compile(rb"-NOAUTH|-ERR .*auth", re.I), "redis", "Redis"),
    (re.compile(rb"^VERSION (?P<version>[\d.]+)\r?$", re.M), "memcached", "memcached"),
    (re.compile(rb"STAT pid \d+"), "memcached", "memcached"),
    # Mail retrieval
    (re.compile(rb"^\+OK.*POP3", re.I), "pop3", None),
    (re.compile(rb"^\* OK.*IMAP", re.I), "imap", None),
]


def _dec(b) -> str | None:
    if b is None:
        return None
    return b.decode("latin-1", "replace").strip() or None


def match_service(data: bytes) -> dict | None:
    """Soft-match collected bytes to {service, product, version}; None if unknown."""
    if not data:
        return None
    for regex, service, product in _PATTERNS:
        m = regex.search(data)
        if not m:
            continue
        groups = m.groupdict()
        prod = product or _dec(groups.get("product"))
        return {"service": service, "product": prod,
                "version": _dec(groups.get("version"))}
    return None


# Probe ladder (Tier 2.5): try a read-only NULL probe first (speak-first services
# greet us), then escalate to protocol probes until something identifies. Ordered
# cheap/common -> specific.
PROBE_LADDER: list[tuple[str, bytes | None]] = [
    ("null", None),
    ("http", _HTTP_PROBE),
    ("generic", _GENERIC_PROBE),
    # Safe, read-only datastore probes — protocol commands, NOT authentication and
    # NOT writes. Only reached for ports the cheaper rungs couldn't identify, so
    # they surface Redis/Memcached (which don't greet) and make the
    # unauthenticated-access proof fire in the field. Redis INFO -> `redis_version`
    # (unauth) or `-NOAUTH` (protected); Memcached version -> `VERSION x.y.z`.
    ("redis", b"INFO\r\n"),
    ("memcached", b"version\r\n"),
]


class ServiceBannerScanner(BaseScanner):
    name = "service_banner"

    def __init__(self, *args, ports: list[int], read_bytes: int = 512, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports
        self.read_bytes = read_bytes

    async def _rung(self, target: str, port: int,
                    payload: bytes | None) -> bytes | None:
        """
        One probe-ladder rung on its own connection. Returns banner bytes, b""
        (open, silent) or None (port not open). `payload` None = read-only (for
        speak-first services); otherwise send the probe then read the reply.
        """
        await self.limiter.wait()
        async with self.sem:
            try:
                fut = asyncio.open_connection(target, port)
                reader, writer = await asyncio.wait_for(fut, timeout=self.timeout)
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return None
            banner = b""
            try:
                if payload is None:
                    try:
                        banner = await asyncio.wait_for(
                            reader.read(self.read_bytes), timeout=1.5)
                    except asyncio.TimeoutError:
                        banner = b""
                else:
                    if b"%b" in payload:
                        payload = payload % bracket_host(target).encode()
                    writer.write(payload)
                    await writer.drain()
                    try:
                        banner = await asyncio.wait_for(
                            reader.read(self.read_bytes), timeout=self.timeout)
                    except asyncio.TimeoutError:
                        banner = b""
            except OSError:
                banner = b""
            finally:
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
            return banner

    async def _grab(self, target: str, port: int) -> ScanResult | None:
        best_banner = b""
        matched = None
        used_probe = None
        port_open = False

        for rung_name, payload in PROBE_LADDER:
            banner = await self._rung(target, port, payload)
            if banner is None:
                # Couldn't connect on this rung. If the very first rung can't
                # connect, the port is closed; otherwise keep the earlier result.
                if not port_open:
                    return None
                continue
            port_open = True
            if len(banner) > len(best_banner):
                best_banner, used_probe = banner, rung_name
            matched = match_service(banner)
            if matched:
                used_probe = rung_name
                break

        if not port_open:
            return None
        if not best_banner:
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="open", data={"banner": None},
                              evidence="open, no banner returned")

        text = best_banner.decode("latin-1", errors="replace").strip()
        first_line = text.splitlines()[0] if text.splitlines() else ""
        data = {"banner": text[:1000], "first_line": first_line[:300],
                "byte_len": len(best_banner), "probe": used_probe}
        if matched:
            data.update(matched)                         # service/product/version
            # DB-free CPE enrichment so the manager-side CVE correlator can match
            # this against NVD — the probe still emits no CVE claim, only identity.
            from .cpe import to_cpe
            cpe = to_cpe(matched.get("service"), matched.get("product"),
                         matched.get("version"))
            if cpe:
                data["cpe"] = cpe["cpe23"]
                data["cpe_vendor"] = cpe["vendor"]
                data["cpe_product"] = cpe["product"]
                data["cpe_version"] = cpe["version"]
            elif matched.get("product"):
                # We named a product but produced no CPE — a coverage gap, not a
                # clean host. Mark it so the map's blind spots are measurable
                # (unmapped product, or a mapped product with no parseable
                # version) instead of silently invisible.
                data["cpe_unmapped"] = " ".join(
                    x for x in (matched.get("product"),
                                matched.get("version")) if x)
            prod = " ".join(x for x in (matched.get("product"),
                                        matched.get("version")) if x)
            evidence = f"{matched['service']}: {prod}".strip().rstrip(":")
        else:
            evidence = first_line[:300] or text[:300]
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._grab(target, p) for p in self.ports]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]


def main() -> None:
    parser = base_argparser("Service banner / version-string grabber")
    parser.add_argument("-p", "--ports", required=True,
                        help="ports to grab, e.g. '22,80,443,3306'")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports)
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = ServiceBannerScanner(scope, rate=args.rate,
                                       concurrency=args.concurrency,
                                       timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
