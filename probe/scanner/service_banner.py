"""
service_banner.py — grab service banners and identify the service behind a port.

METHOD (collection only): connect to a port and read whatever the service
voluntarily announces. For services that speak first (SSH, SMTP, FTP, VNC,
telnet) we just read. For services that wait (HTTP) we send a minimal, benign
request and read the response head. If the plaintext rungs identify nothing we
attempt ONE TLS handshake (certificate deliberately NOT verified — this is a
fingerprint, not a trust decision) and repeat the greet-read / HTTP probe inside
the tunnel, so HTTPS / IMAPS / SMTPS on ANY port yields a real banner and a
POSITIVE "this port speaks TLS" fact instead of an absence inference.

We RECORD the banner verbatim as evidence — we do NOT map it to a CVE or decide
a version is vulnerable. That is the (separate) detection layer's job. This
keeps the module's output purely factual so its accuracy is measurable:
"port 22 returned banner X".

Structured HTTP facts (status, Server, X-Powered-By, WWW-Authenticate, title)
are extracted alongside the soft-match so a consumer never has to re-parse the
raw banner to learn e.g. that a port challenges for Basic auth over cleartext.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import ssl
import warnings

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

# Ports where the client must speak first. The read-only NULL rung is skipped
# here (it can only ever time out) so these ports identify a full greet-wait
# sooner.
_CLIENT_FIRST = {80, 8080, 8000, 8888, 443, 8443}


def _tls_context() -> ssl.SSLContext:
    """A permissive client context for FINGERPRINTING only: no verification, any
    version/cipher the local OpenSSL can still negotiate. The point is to get a
    banner out of a legacy or self-signed listener, not to trust it — tls_scanner
    is where posture (versions, ciphers, certificate validity) is assessed."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            ctx.minimum_version = ssl.TLSVersion.TLSv1
    except (ValueError, AttributeError):
        pass
    try:
        ctx.set_ciphers("ALL:@SECLEVEL=0")
    except ssl.SSLError:
        pass
    return ctx


_TLS_CTX = _tls_context()

# --------------------------------------------------------------------------- #
# Service soft-matching — banner -> {service, product, version}.
#
# Ordered most-specific first. Each entry: (compiled regex, service, product).
# `product=None` means "use the regex's (?P<product>...) group as the product".
# An optional (?P<version>...) group supplies the version. Matching is on bytes
# so it works on binary handshakes (MySQL, telnet IAC, RFB) as well as text
# banners. Port-number independent: a service on a non-standard port still
# identifies by behaviour.
#
# Ordering rules that matter:
#   * protocols with unambiguous LEADING bytes (telnet IAC, RFB, AMQP, TLS
#     records) go first — they can't be confused with anything else;
#   * datastores / APIs that ride on HTTP (Elasticsearch, CouchDB, Docker,
#     Kubernetes, Jenkins) precede the generic `Server:` match, which would
#     otherwise label them plain "http";
#   * named HTTP products with non-standard header shapes (Jetty's parens,
#     Coyote, GlassFish) precede the generic `product/version` catch-all;
#   * weak signals (shell prompts, login prompts, bare HTTP status line) go last.
# --------------------------------------------------------------------------- #
_PATTERNS: list[tuple[re.Pattern, str, str | None]] = [
    # ── speak-first protocols with unambiguous leading bytes ──────────────────
    (re.compile(rb"^\xff[\xfb-\xfe]"), "telnet", None),             # IAC WILL/WONT/DO/DONT
    (re.compile(rb"^RFB (?P<version>\d{3}\.\d{3})"), "vnc", None),   # RFB ProtocolVersion
    (re.compile(rb"^AMQP\x00[\x00\x01]\x09\x01"), "amqp", None),     # AMQP 0-9-1 header echo
    # A TLS-only listener answering our plaintext probe with an alert record
    # (or, rarely, a ServerHello) — a POSITIVE "this is TLS" signal even when
    # the tunnelled rung below could not complete a handshake.
    (re.compile(rb"^\x15\x03[\x00-\x04]\x00\x02"), "tls", None),
    (re.compile(rb"^\x16\x03[\x00-\x04]"), "tls", None),
    # ── SSH ───────────────────────────────────────────────────────────────────
    (re.compile(rb"SSH-\d+\.\d+-OpenSSH[_-](?P<version>[\w.]+)"), "ssh", "OpenSSH"),
    (re.compile(rb"SSH-\d+\.\d+-dropbear[_-](?P<version>[\w.]+)"), "ssh", "dropbear"),
    (re.compile(rb"SSH-\d+\.\d+-(?P<product>[\w.+\-]+)"), "ssh", None),
    # ── datastores (must win over the generic Server: match below) ────────────
    (re.compile(rb'"number"\s*:\s*"(?P<version>\d+\.\d+\.\d+)"[^}]*"lucene_version"'),
     "elasticsearch", "Elasticsearch"),
    (re.compile(rb'"tagline"\s*:\s*"You Know, for Search"'), "elasticsearch", "Elasticsearch"),
    (re.compile(rb'"cluster_name"\s*:\s*"'), "elasticsearch", "Elasticsearch"),
    (re.compile(rb'"couchdb"\s*:\s*"Welcome"'), "couchdb", "CouchDB"),
    (re.compile(rb"trying to access MongoDB over HTTP"), "mongodb", "MongoDB"),
    # PostgreSQL answers any non-startup bytes with a FATAL ErrorResponse.
    (re.compile(rb"unsupported frontend protocol|invalid length of startup packet"),
     "postgresql", "PostgreSQL"),
    (re.compile(rb"(?P<version>\d+\.\d+\.\d+)-MariaDB"), "mysql", "MariaDB"),
    # The salt in a MySQL greeting is random binary and may contain \n, so these
    # need DOTALL to reach the auth-plugin name after the version string.
    (re.compile(rb"(?P<version>[458]\.\d+\.\d+)\W.*mysql_native_password", re.S),
     "mysql", "MySQL"),
    (re.compile(rb"(?P<version>[58]\.\d+\.\d+)\W.*caching_sha2_password", re.S),
     "mysql", "MySQL"),
    (re.compile(rb"mysql_native_password|caching_sha2_password"), "mysql", "MySQL"),
    (re.compile(rb"is not allowed to connect to this (?P<product>MySQL|MariaDB) server"),
     "mysql", None),
    (re.compile(rb"redis_version:(?P<version>[\d.]+)"), "redis", "Redis"),
    (re.compile(rb"-NOAUTH|-ERR .*auth|-DENIED Redis|"
                rb"-ERR (?:unknown command|wrong number of arguments|Protocol error)", re.I),
     "redis", "Redis"),
    (re.compile(rb"^VERSION (?P<version>[\d.]+)\r?$", re.M), "memcached", "memcached"),
    (re.compile(rb"STAT pid \d+"), "memcached", "memcached"),
    # ── container / orchestration / CI / observability APIs over HTTP ─────────
    (re.compile(rb"[Ss]erver:\s*Docker/(?P<version>[\d.]+)"), "docker", "Docker"),
    (re.compile(rb"Docker-Experimental:"), "docker", "Docker"),
    (re.compile(rb'"kind"\s*:\s*"Status"\s*,\s*"apiVersion"\s*:\s*"v1"'),
     "kubernetes-api", "Kubernetes"),
    (re.compile(rb"X-Jenkins:\s*(?P<version>[\d.]+)"), "http", "Jenkins"),
    (re.compile(rb"grafana_session|<title>Grafana</title>"), "http", "Grafana"),
    (re.compile(rb"<title>Prometheus Time Series"), "http", "Prometheus"),
    (re.compile(rb"<title>Node Exporter</title>"), "http", "Node Exporter"),
    (re.compile(rb"<title>RabbitMQ Management</title>"), "http", "RabbitMQ"),
    # Services on the risk-catalog ports VA_RISK_PORTS added to the sweep. Each
    # answers the ladder's ordinary HTTP rung (plaintext or inside the TLS rung),
    # so identifying them costs no extra probe — it only upgrades an
    # exposed-service finding from "this port number is risky" to "this product
    # is listening", which is the difference between a lead and a fact.
    (re.compile(rb"X-Etcd-Cluster-Id:|X-Etcd-Index:"), "etcd", "etcd"),
    (re.compile(rb'"etcdserver"\s*:\s*"(?P<version>[\d.]+)"'), "etcd", "etcd"),
    (re.compile(rb'\{"health"\s*:\s*"?true"?\}'), "etcd", "etcd"),
    (re.compile(rb"X-Influxdb-Version:\s*(?P<version>[\w.\-]+)"), "influxdb", "InfluxDB"),
    (re.compile(rb"X-Consul-(?:Index|Knownleader):", re.I), "consul", "Consul"),
    (re.compile(rb"kbn-name:|<title>Kibana</title>", re.I), "http", "Kibana"),
    (re.compile(rb"<title>\s*Cockpit\b|[Ss]erver:\s*Cockpit"), "http", "Cockpit"),
    (re.compile(rb"[Ss]erver:\s*MiniServ/(?P<version>[\d.]+)"), "http", "Webmin"),
    (re.compile(rb"<title>Proxmox Virtual Environment|pve-api-daemon"), "http", "Proxmox VE"),
    (re.compile(rb"<title>Namenode information|Hadoop:\s"), "http", "Apache Hadoop"),
    (re.compile(rb"<title>HBase\b"), "http", "Apache HBase"),
    (re.compile(rb"<title>Portainer\b|portainer"), "http", "Portainer"),
    # Zookeeper's four-letter admin words are the one non-HTTP case worth a
    # signature: `ruok` -> `imok` is a read-only liveness word, and some builds
    # leak it to any connect. We never SEND it (see the probe ladder) — this only
    # recognises it if the server volunteers it.
    (re.compile(rb"^imok$", re.M), "zookeeper", "Apache ZooKeeper"),
    # ── HTTP servers whose header shape the generic catch-all would misread ───
    (re.compile(rb"Apache Tomcat/(?P<version>[\d.]+)"), "http", "Apache Tomcat"),
    (re.compile(rb"[Ss]erver:\s*Apache-Coyote/"), "http", "Apache Tomcat"),
    (re.compile(rb"[Ss]erver:\s*Jetty\((?P<version>\d+(?:\.\d+)*)"), "http", "Jetty"),
    (re.compile(rb"[Ss]erver:\s*WildFly/(?P<version>[\d.]+)"), "http", "WildFly"),
    (re.compile(rb"[Ss]erver:\s*GlassFish Server(?: Open Source Edition)?\s*(?P<version>[\d.]+)"),
     "http", "GlassFish"),
    (re.compile(rb"[Ss]erver:\s*Microsoft-HTTPAPI/(?P<version>[\d.]+)"), "http", "Microsoft-HTTPAPI"),
    (re.compile(rb"[Ss]erver:\s*CUPS/(?P<version>[\d.]+)"), "ipp", "CUPS"),
    (re.compile(rb"[Ss]erver:\s*squid/(?P<version>[\d.]+)"), "http-proxy", "Squid"),
    # UPnP device descriptions put the OS first ("Server: Linux/3.10 UPnP/1.0
    # ...") — the generic match would report product "Linux".
    (re.compile(rb"[Ss]erver:[^\r\n]*UPnP/1\.[01]"), "upnp", None),
    (re.compile(rb"[Ss]erver:\s*nginx(?:/(?P<version>[\d.]+))?"), "http", "nginx"),
    (re.compile(rb"[Ss]erver:\s*Apache(?:/(?P<version>[\d.]+))?"), "http", "Apache"),
    (re.compile(rb"[Ss]erver:\s*Microsoft-IIS/(?P<version>[\d.]+)"), "http", "Microsoft-IIS"),
    (re.compile(rb"[Ss]erver:\s*(?P<product>[\w\-]+)/(?P<version>[\d.]+)"), "http", None),
    # Versionless Server: header ("Kestrel", "cloudflare", "GoAhead-Webs").
    (re.compile(rb"[Ss]erver:\s*(?P<product>[A-Za-z][\w\-. ]{1,40}?)\s*\r?\n"), "http", None),
    # ── FTP ───────────────────────────────────────────────────────────────────
    (re.compile(rb"vsFTPd (?P<version>[\d.]+)"), "ftp", "vsftpd"),
    (re.compile(rb"ProFTPD (?P<version>[\d.]+)"), "ftp", "ProFTPD"),
    (re.compile(rb"Pure-FTPd"), "ftp", "Pure-FTPd"),
    (re.compile(rb"FileZilla Server(?:\s+(?:version\s+)?(?P<version>\d[\w.]*))?"),
     "ftp", "FileZilla Server"),
    (re.compile(rb"Microsoft FTP Service"), "ftp", "Microsoft FTP Service"),
    (re.compile(rb"Version wu-(?P<version>[\d.]+)"), "ftp", "WU-FTPD"),
    (re.compile(rb"220[- ].*FTP", re.I), "ftp", None),
    # ── SMTP ──────────────────────────────────────────────────────────────────
    (re.compile(rb"Microsoft ESMTP MAIL Service(?:, Version:\s*(?P<version>[\d.]+))?"),
     "smtp", "Microsoft ESMTP"),
    (re.compile(rb"ESMTP Exim (?P<version>[\d.]+)"), "smtp", "Exim"),
    (re.compile(rb"ESMTP Sendmail (?P<version>[\d./]+)"), "smtp", "Sendmail"),
    (re.compile(rb"ESMTP hMailServer"), "smtp", "hMailServer"),
    (re.compile(rb"ESMTP (?P<product>Postfix|Exim|Sendmail)"), "smtp", None),
    (re.compile(rb"220[- ].*SMTP", re.I), "smtp", None),
    # ── mail retrieval ────────────────────────────────────────────────────────
    (re.compile(rb"^\+OK.*Dovecot", re.I), "pop3", "Dovecot"),
    (re.compile(rb"^\* OK.*Dovecot", re.I), "imap", "Dovecot"),
    (re.compile(rb"^\* OK.*Cyrus IMAP v?(?P<version>[\d.]+)", re.I), "imap", "Cyrus IMAP"),
    (re.compile(rb"^\* OK.*Courier-IMAP", re.I), "imap", "Courier-IMAP"),
    (re.compile(rb"^\* OK.*Microsoft Exchange", re.I), "imap", "Microsoft Exchange"),
    (re.compile(rb"^\+OK.*Microsoft Exchange", re.I), "pop3", "Microsoft Exchange"),
    (re.compile(rb"^\+OK.*POP3", re.I), "pop3", None),
    (re.compile(rb"^\* OK.*IMAP", re.I), "imap", None),
    # ── real-time / media signalling (HTTP-shaped status lines) ───────────────
    (re.compile(rb"^RTSP/1\.0 \d{3}"), "rtsp", None),
    (re.compile(rb"^SIP/2\.0 \d{3}"), "sip", None),
    # IRC: RFC 1459 registration burst. On a risk-catalog port (6666-6669) this
    # CORROBORATES the botnet-C2 classification instead of leaving it a
    # port-number guess — the server named its own protocol.
    (re.compile(rb"^:[^\s]+ (?:NOTICE AUTH|001|020) "), "irc", None),
    (re.compile(rb"^(?:PING :|ERROR :Closing Link)"), "irc", None),
    # ── an interactive shell on a socket: the bind-shell / backdoor tell ──────
    (re.compile(rb"(?m)^(?:bash|sh|zsh)-[\d.]+[#$] ?$"), "shell", None),
    (re.compile(rb"(?m)^[A-Za-z]:\\[^\r\n]*>\s*$"), "shell", None),
    (re.compile(rb"(?m)^[#$] $"), "shell", None),
    # A bare login/password prompt with no protocol framing: cleartext auth.
    (re.compile(rb"(?im)^(?:login|username|user name|password)\s*:\s*$"), "telnet", None),
    # ── HTTP fallback: a status line but no recognisable Server header ────────
    (re.compile(rb"^HTTP/(?:1\.[01]|2) \d{3}"), "http", None),
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


# --------------------------------------------------------------------------- #
# Structured HTTP(-shaped) head extraction — independent of the soft-match so a
# consumer never re-parses the raw banner for status / Server / auth challenge.
# --------------------------------------------------------------------------- #
_STATUS_RE = re.compile(rb"^(HTTP/\d(?:\.\d)?|RTSP/1\.\d|SIP/2\.0) (\d{3})")
_HEAD_SPLIT_RE = re.compile(rb"\r?\n\r?\n")
_TITLE_RE = re.compile(rb"<title[^>]*>(.*?)</title>", re.I | re.S)
_HEAD_FIELDS = {
    "server": "http_server",
    "x-powered-by": "http_powered_by",
    "x-aspnet-version": "http_aspnet_version",
    "www-authenticate": "http_auth",
    "location": "http_location",
    "content-type": "http_content_type",
}


def parse_http_head(raw: bytes) -> dict:
    """Pull status code, the identifying headers and the <title> out of an
    HTTP/RTSP/SIP response. Returns {} for anything that isn't one — never raises.
    Values are truncated so a hostile server can't bloat the fact."""
    if not raw:
        return {}
    m = _STATUS_RE.match(raw)
    if not m:
        return {}
    out: dict = {"http_status": int(m.group(2))}
    split = _HEAD_SPLIT_RE.search(raw)
    head, body = (raw[:split.start()], raw[split.end():]) if split else (raw, b"")
    for line in re.split(rb"\r?\n", head)[1:]:
        key, sep, value = line.partition(b":")
        if not sep:
            continue
        field = _HEAD_FIELDS.get(key.strip().lower().decode("latin-1", "replace"))
        if field and field not in out:
            out[field] = value.strip().decode("latin-1", "replace")[:200]
    t = _TITLE_RE.search(body)
    if t:
        title = " ".join(t.group(1).decode("latin-1", "replace").split())
        if title:
            out["http_title"] = title[:200]
    auth = out.get("http_auth")
    if auth:
        out["http_auth_scheme"] = auth.split(None, 1)[0].lower()
    return out


# Probe ladder: try a read-only NULL probe first (speak-first services greet
# us), then escalate to protocol probes until something identifies. Ordered
# cheap/common -> specific. The "tls" rung is the same HTTP probe carried inside
# a TLS tunnel after a greet-read (so IMAPS/SMTPS identify too).
PROBE_LADDER: list[tuple[str, bytes | None]] = [
    ("null", None),
    ("http", _HTTP_PROBE),
    ("tls", _HTTP_PROBE),
    ("generic", _GENERIC_PROBE),
    # Safe, read-only datastore probes — protocol commands, NOT authentication and
    # NOT writes. Only reached for ports the cheaper rungs couldn't identify, so
    # they surface Redis/Memcached (which don't greet) and make the
    # unauthenticated-access proof fire in the field. Redis INFO -> `redis_version`
    # (unauth) or `-NOAUTH` (protected); Memcached version -> `VERSION x.y.z`.
    ("redis", b"INFO\r\n"),
    ("memcached", b"version\r\n"),
]

# How much of a multi-segment reply to keep waiting for once the first bytes
# have arrived: the rest of an HTTP head / greeting lands within this or not at
# all, so this bounds the cost of collecting a complete first response.
_CONTINUATION_WAIT = 0.3


class ServiceBannerScanner(BaseScanner):
    name = "service_banner"

    def __init__(self, *args, ports: list[int], read_bytes: int = 2048,
                 greet_timeout: float | None = None, try_tls: bool = True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports
        self.read_bytes = read_bytes
        # How long the read-only rung waits for a speak-first service to greet.
        # SMTP/FTP daemons routinely delay their 220 for a reverse-DNS lookup, so
        # a fixed 1.5s manufactured "no banner" on real services (nmap's NULL
        # probe waits 6s). Bounded by the operator's --timeout, floor 1.5s.
        self.greet_timeout = (greet_timeout if greet_timeout is not None
                              else max(1.5, min(self.timeout, 5.0)))
        # Attempt a TLS handshake when the plaintext rungs identify nothing.
        self.try_tls = try_tls

    async def _connect(self, target: str, port: int, *, tls: bool):
        if tls:
            fut = asyncio.open_connection(
                target, port, ssl=_TLS_CTX, ssl_handshake_timeout=self.timeout)
            # TCP connect + handshake share one deadline.
            return await asyncio.wait_for(fut, timeout=self.timeout * 2)
        return await asyncio.wait_for(asyncio.open_connection(target, port),
                                      timeout=self.timeout)

    async def _read_some(self, reader: asyncio.StreamReader, first_wait: float) -> bytes:
        """Read up to read_bytes: wait `first_wait` for the first segment, then
        only briefly for continuations, so a chunked HTTP head or a greeting
        split across segments is collected whole without stalling on silence."""
        buf = b""
        wait = first_wait
        while len(buf) < self.read_bytes:
            try:
                chunk = await asyncio.wait_for(
                    reader.read(self.read_bytes - len(buf)), timeout=wait)
            except asyncio.TimeoutError:
                break
            if not chunk:
                break
            buf += chunk
            wait = _CONTINUATION_WAIT
        return buf

    async def _rung(self, target: str, port: int, rung_name: str,
                    payload: bytes | None) -> tuple[bytes | None, dict | None]:
        """
        One probe-ladder rung on its own connection. Returns (banner, extra):
        banner is the bytes read, b"" (open, silent) or None (couldn't connect /
        couldn't handshake on this rung); extra carries TLS facts when the rung
        completed a TLS handshake. `payload` None = read-only (for speak-first
        services); otherwise send the probe then read the reply. The "tls" rung
        does a greet-read inside the tunnel first, then the probe.
        """
        tls = rung_name == "tls"
        await self.limiter.wait()
        async with self.sem:
            try:
                reader, writer = await self._connect(target, port, tls=tls)
            except (asyncio.TimeoutError, OSError):   # SSLError/refused are OSErrors
                return None, None
            extra: dict | None = None
            if tls:
                extra = {"tls": True}
                sslobj = writer.get_extra_info("ssl_object")
                if sslobj is not None:
                    try:
                        extra["tls_version"] = sslobj.version()
                        cipher = sslobj.cipher()
                        if cipher:
                            extra["tls_cipher"] = cipher[0]
                    except Exception:
                        pass
            banner = b""
            try:
                if payload is None or tls:
                    greet_wait = min(self.greet_timeout, 2.0) if tls else self.greet_timeout
                    banner = await self._read_some(reader, greet_wait)
                if not banner and payload is not None:
                    if b"%b" in payload:
                        payload = payload % bracket_host(target).encode()
                    writer.write(payload)
                    await writer.drain()
                    banner = await self._read_some(reader, self.timeout)
            except (OSError, asyncio.IncompleteReadError):
                pass
            finally:
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
            return banner, extra

    def _ladder_for(self, port: int) -> list[tuple[str, bytes | None]]:
        rungs = []
        for name, payload in PROBE_LADDER:
            if name == "null" and port in _CLIENT_FIRST:
                continue            # can only time out here — skip straight to the probe
            if name == "tls" and not self.try_tls:
                continue
            rungs.append((name, payload))
        return rungs

    async def _grab(self, target: str, port: int) -> ScanResult | None:
        banners: dict[str, bytes] = {}
        matched = None
        matched_rung = None
        tls_meta: dict | None = None
        tls_attempted = False
        port_open = False

        for rung_name, payload in self._ladder_for(port):
            if rung_name == "tls":
                tls_attempted = True
            banner, extra = await self._rung(target, port, rung_name, payload)
            if banner is None:
                # Couldn't connect (or handshake) on this rung. If the very
                # first plaintext rung can't connect, the port is closed;
                # otherwise keep what earlier rungs collected.
                if not port_open and rung_name != "tls":
                    return None
                continue
            port_open = True
            if extra:
                tls_meta = {**(tls_meta or {}), **extra}
            banners[rung_name] = banner
            m = match_service(banner)
            if m:
                matched, matched_rung = m, rung_name
                break

        if not port_open:
            return None

        # Pick the banner to report: the identified one; else a decrypted TLS
        # reply over plaintext noise (a TLS alert record is not a useful
        # banner); else simply the longest thing any rung collected.
        if matched_rung is not None:
            best, used_probe = banners[matched_rung], matched_rung
        elif banners.get("tls"):
            best, used_probe = banners["tls"], "tls"
        else:
            used_probe = max(banners, key=lambda k: len(banners[k]), default=None)
            best = banners.get(used_probe, b"") if used_probe else b""

        data: dict = dict(tls_meta or {})
        if tls_attempted:
            # Record that a TLS handshake was TRIED on this port, whatever the
            # outcome. Absent `tls` alongside this flag is direct evidence the
            # port does not speak TLS — which is what lets router.py stop
            # inferring "silent, so maybe TLS" about binary protocols like SMB,
            # MSRPC and RDP and speculatively re-probing them.
            data["tls_probed"] = True
        if not best:
            data["banner"] = None
            evidence = "open, no banner returned"
            if tls_meta:
                evidence += f" (TLS {tls_meta.get('tls_version') or 'handshake'} ok)"
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="open", data=data, evidence=evidence)

        text = best.decode("latin-1", errors="replace").strip()
        lines = text.splitlines()
        first_line = lines[0] if lines else ""
        data.update({"banner": text[:1000], "first_line": first_line[:300],
                     "byte_len": len(best), "probe": used_probe})
        data.update(parse_http_head(best))
        if data.get("http_auth_scheme") == "basic" and not data.get("tls"):
            # Fact, not verdict: the port challenges for Basic credentials on a
            # connection that never negotiated TLS.
            data["http_basic_auth_cleartext"] = True
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
            if data.get("tls"):
                evidence += " (over TLS)"
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
    parser.add_argument("--greet-timeout", type=float, default=None,
                        help="seconds to wait for a speak-first service to greet "
                             "(default: --timeout, clamped to 1.5-5s)")
    parser.add_argument("--no-tls", action="store_true",
                        help="skip the TLS-tunnelled rung (plaintext probes only)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports)
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = ServiceBannerScanner(scope, rate=args.rate,
                                       concurrency=args.concurrency,
                                       timeout=args.timeout, ports=ports,
                                       greet_timeout=args.greet_timeout,
                                       try_tls=not args.no_tls)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
