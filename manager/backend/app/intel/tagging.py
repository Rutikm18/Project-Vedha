"""
tagging.py — evidence-based asset tags.

Everything the manager already knows about a host (classifier role, OS, open
services, banners, exposure verdicts, FQDN) is turned into namespaced tags such
as ``role:database`` or ``sector_fn:swift`` that filters, compliance scoping and
the AI assistant can reason over.

Pure logic — no DB, no I/O — so every rule is unit-testable in isolation.

Honesty rules:
  * A tag is only emitted with evidence; a host we know nothing about gets no
    tags rather than guesses (the ``server`` asset_type default is not a claim).
  * Heuristics carry their real confidence. BFSI sector tags from a port or a
    hostname word stay ≤ 0.6; only a banner/product naming the system goes higher.
  * Auto tags are recomputed wholesale; manual tags are never touched.

Storage shape on ``Asset.tags``: ``{"v": 1, "auto": [Tag...], "manual": [Tag...]}``.
"""
from __future__ import annotations

import ipaddress
import re
from dataclasses import asdict, dataclass, field
from typing import Callable, Iterable

TAGS_VERSION = 1


@dataclass(frozen=True)
class ServiceFact:
    port: int
    protocol: str = "tcp"
    service_name: str | None = None
    product: str | None = None
    banner: str | None = None
    exposure: str | None = None

    @property
    def text(self) -> str:
        """Lower-cased product + banner + service name, for keyword signatures."""
        return " ".join(p for p in (self.product, self.banner, self.service_name) if p).lower()

    def describe(self) -> str:
        label = self.service_name or self.product or "open"
        return f"{self.protocol}/{self.port} {label}"


@dataclass(frozen=True)
class AssetFacts:
    ip: str | None = None
    hostname: str | None = None
    fqdn: str | None = None
    os: str | None = None
    asset_type: str | None = None
    device_role: str | None = None
    role_detail: str | None = None
    role_confidence: float | None = None
    services: tuple[ServiceFact, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Tag:
    key: str
    value: str
    rule: str
    confidence: float
    evidence: str
    source: str = "auto"

    def to_dict(self) -> dict:
        return asdict(self)


Rule = Callable[[AssetFacts], Iterable[Tag]]
_RULES: list[Rule] = []


def rule(fn: Rule) -> Rule:
    """Register a tagging rule. Order does not matter; dedupe keeps the best tag."""
    _RULES.append(fn)
    return fn


# ── host_type ────────────────────────────────────────────────────────────────

_ROLE_TO_HOST_TYPE = {
    "workstation": "workstation", "server": "server", "network_device": "network",
    "network": "network", "printer": "printer", "hypervisor": "hypervisor",
    "iot": "iot", "cloud": "cloud", "container": "container",
}


@rule
def _host_type(f: AssetFacts) -> Iterable[Tag]:
    if f.device_role and f.device_role in _ROLE_TO_HOST_TYPE:
        conf = f.role_confidence if f.role_confidence else 0.6
        yield Tag("host_type", _ROLE_TO_HOST_TYPE[f.device_role], "host.classifier",
                  _clamp(conf), f"device classifier: {f.device_role}")
    elif f.asset_type and f.asset_type != "server" and f.asset_type in _ROLE_TO_HOST_TYPE:
        # `server` is the promote default when nothing classified the host, so it
        # is not evidence; any other asset_type was set deliberately.
        yield Tag("host_type", _ROLE_TO_HOST_TYPE[f.asset_type], "host.asset_type",
                  0.6, f"asset type: {f.asset_type}")


# ── os_family ────────────────────────────────────────────────────────────────

_OS_PATTERNS: tuple[tuple[str, re.Pattern], ...] = (
    ("windows", re.compile(r"windows|microsoft")),
    # Word-bounded: a bare "os x" matched inside "Cisco IOS XE" and tagged routers macOS.
    ("macos", re.compile(r"\bmac ?os\b|\bos x\b|\bdarwin\b")),
    ("network_os", re.compile(r"cisco|ios[- ]xe|nx-os|junos|fortios|pan-os|routeros|mikrotik|arista|eos\b")),
    ("linux", re.compile(r"linux|ubuntu|debian|centos|red ?hat|rhel|fedora|suse|alpine|rocky|alma")),
    ("bsd", re.compile(r"freebsd|openbsd|netbsd|pfsense|opnsense")),
)
# Banners only name the distro/vendor reliably for these.
_BANNER_OS_PATTERNS: tuple[tuple[str, re.Pattern], ...] = (
    ("linux", re.compile(r"ubuntu|debian|centos|red ?hat|rhel|fedora|raspbian")),
    ("windows", re.compile(r"microsoft-iis|microsoft-httpapi|windows")),
    ("bsd", re.compile(r"freebsd|openbsd")),
)


@rule
def _os_family(f: AssetFacts) -> Iterable[Tag]:
    if f.os:
        low = f.os.lower()
        for family, pat in _OS_PATTERNS:
            if pat.search(low):
                yield Tag("os_family", family, "os.string", 0.85, f"os: {f.os}")
                return
    for svc in f.services:
        for family, pat in _BANNER_OS_PATTERNS:
            if svc.text and pat.search(svc.text):
                yield Tag("os_family", family, "os.banner", 0.6,
                          f"{svc.describe()} banner names {family}")
                return


def os_family_tag(facts: AssetFacts) -> Tag | None:
    """The single os_family tag the evidence supports, or None. Public so the
    remediation planner resolves a platform with the SAME rule the tags use."""
    return next(iter(_os_family(facts)), None)


# ── role (from services) ─────────────────────────────────────────────────────

_PORT_ROLES: dict[int, str] = {
    **dict.fromkeys((80, 443, 8000, 8008, 8080, 8443, 8888), "web"),
    **dict.fromkeys((1433, 1521, 3306, 5432, 6379, 9042, 9200, 27017, 50000, 5984), "database"),
    **dict.fromkeys((25, 110, 143, 465, 587, 993, 995), "mail"),
    53: "dns",
    **dict.fromkeys((389, 636, 3268, 3269), "directory"),
    **dict.fromkeys((139, 445, 2049, 21), "file_share"),
    **dict.fromkeys((22, 23, 3389, 5900, 5985, 5986), "remote_access"),
    **dict.fromkeys((161, 5666, 10050, 10051), "monitoring"),
    **dict.fromkeys((2375, 2376, 6443, 10250), "container_platform"),
    **dict.fromkeys((9392, 9401, 10000), "backup"),
    **dict.fromkeys((5060, 5061), "voip"),
    **dict.fromkeys((102, 502, 20000, 44818, 47808), "ics"),
    **dict.fromkeys((500, 1194, 1723, 4500), "vpn"),
    **dict.fromkeys((515, 631, 9100), "print"),
}
# Service-name tokens → role. Exact token match, so "domain" never hits "domainx".
_NAME_ROLES: dict[str, str] = {
    **dict.fromkeys(("http", "https", "http-alt", "http-proxy", "https-alt"), "web"),
    **dict.fromkeys(("ms-sql-s", "mssql", "oracle", "oracle-tns", "mysql", "mariadb",
                     "postgresql", "postgres", "redis", "mongodb", "mongod", "elasticsearch",
                     "cassandra", "couchdb", "db2", "ibm-db2"), "database"),
    **dict.fromkeys(("smtp", "smtps", "submission", "imap", "imaps", "pop3", "pop3s"), "mail"),
    "domain": "dns",
    **dict.fromkeys(("ldap", "ldaps", "globalcatldap", "globalcatldapssl"), "directory"),
    **dict.fromkeys(("microsoft-ds", "netbios-ssn", "smb", "nfs", "ftp", "ftps"), "file_share"),
    **dict.fromkeys(("ssh", "telnet", "ms-wbt-server", "rdp", "vnc", "winrm", "wsman"), "remote_access"),
    **dict.fromkeys(("snmp", "zabbix-agent", "nrpe"), "monitoring"),
    **dict.fromkeys(("docker", "kubernetes", "kubelet"), "container_platform"),
    **dict.fromkeys(("sip", "sip-tls"), "voip"),
    **dict.fromkeys(("modbus", "s7comm", "iso-tsap", "dnp3", "bacnet", "enip"), "ics"),
    **dict.fromkeys(("isakmp", "openvpn", "pptp", "ipsec-nat-t"), "vpn"),
    **dict.fromkeys(("ipp", "printer", "jetdirect"), "print"),
}
_DC_DETAILS = {"domain_controller", "dc", "active_directory"}


def _service_role(svc: ServiceFact) -> tuple[str, str] | None:
    """(role, rule) for one service, name first (it survives non-standard ports)."""
    if svc.service_name:
        name = svc.service_name.lower().removeprefix("ssl/")
        if name in _NAME_ROLES:
            return _NAME_ROLES[name], "role.service_name"
    if svc.port in _PORT_ROLES:
        return _PORT_ROLES[svc.port], "role.port"
    return None


@rule
def _roles(f: AssetFacts) -> Iterable[Tag]:
    ports = {s.port for s in f.services}
    for svc in f.services:
        hit = _service_role(svc)
        if hit:
            role_name, rule_id = hit
            conf = 0.85 if rule_id == "role.service_name" else 0.6
            yield Tag("role", role_name, rule_id, conf, svc.describe())
    if f.role_detail and f.role_detail.lower() in _DC_DETAILS:
        yield Tag("role", "domain_controller", "role.classifier",
                  _clamp(f.role_confidence or 0.8), f"device classifier: {f.role_detail}")
    elif 88 in ports and 445 in ports and ports & {389, 636, 3268}:
        yield Tag("role", "domain_controller", "role.dc_triad", 0.8,
                  "kerberos/88 + ldap + smb/445 together")
    if f.device_role == "hypervisor":
        yield Tag("role", "hypervisor", "role.classifier",
                  _clamp(f.role_confidence or 0.6), "device classifier: hypervisor")


# ── exposure / zone / domain ─────────────────────────────────────────────────

def _parse_ip(ip: str | None):
    try:
        return ipaddress.ip_address(ip) if ip else None
    except ValueError:
        return None


@rule
def _exposure(f: AssetFacts) -> Iterable[Tag]:
    external = [s for s in f.services if s.exposure == "external"]
    if external:
        yield Tag("exposure", "internet_facing", "exposure.matrix", 0.9,
                  f"{external[0].describe()} reachable externally")
        return
    addr = _parse_ip(f.ip)
    if addr is not None and addr.is_global:
        yield Tag("exposure", "internet_facing", "exposure.public_ip", 0.7,
                  f"globally routable address {f.ip}")
        return
    verdicts = [s.exposure for s in f.services if s.exposure]
    if verdicts and all(v in ("internal_only", "not_exposed") for v in verdicts):
        yield Tag("exposure", "internal_only", "exposure.matrix", 0.8,
                  f"{len(verdicts)} service(s) verified not externally reachable")


@rule
def _zone(f: AssetFacts) -> Iterable[Tag]:
    addr = _parse_ip(f.ip)
    if addr is None:
        return
    prefix = 24 if addr.version == 4 else 64
    net = ipaddress.ip_network(f"{addr}/{prefix}", strict=False)
    yield Tag("zone", str(net), "zone.subnet", 1.0, f"address {f.ip}")


_HOST_LABEL = re.compile(r"^[a-z0-9-]{1,63}$")


@rule
def _domain(f: AssetFacts) -> Iterable[Tag]:
    name = (f.fqdn or f.hostname or "").strip().lower().rstrip(".")
    labels = name.split(".")
    # Need host + at least two domain labels, and every label must look like DNS.
    if len(labels) < 3 or not all(_HOST_LABEL.match(lbl) for lbl in labels):
        return
    yield Tag("domain", ".".join(labels[1:]), "domain.fqdn", 0.9, f"name {name}")


# ── BFSI sector functions ────────────────────────────────────────────────────

# (sector_fn, product/banner signature) — naming the system is strong evidence.
_SECTOR_BANNERS: tuple[tuple[str, re.Pattern], ...] = (
    ("core_banking", re.compile(r"finacle|temenos|\bt24\b|\btransact\b|flexcube|\bbancs\b|fiserv|jack henry|mambu")),
    ("swift", re.compile(r"swift|alliance (access|gateway|lite)")),
    ("hsm", re.compile(r"payshield|safenet|luna ?sa|nshield|thales|utimaco|futurex")),
    ("card_processing", re.compile(r"postilion|base24|\bjpos\b|iso ?8583|mastercard|visanet|way4|cardpro")),
    ("atm", re.compile(r"aptra|\bncr\b|diebold|wincor|\bxfs\b")),
    ("trading", re.compile(r"8=fix\.|\bfix(t)?[0-9.]*\b engine|quickfix|bloomberg")),
    ("payments", re.compile(r"\bnpci\b|\bupi\b|\bimps\b|\brtgs\b|\bneft\b|\bsepa\b|\bach\b gateway")),
)
# Well-known default ports — heuristic only; many products reuse ports.
_SECTOR_PORTS: dict[int, str] = {48002: "swift", 48003: "swift", 1500: "hsm", 1792: "hsm"}
# Hostname tokens (split on non-alphanumerics). Deliberately specific: "core",
# "pay", "bank" are too common to mean anything on their own.
_SECTOR_HOST_TOKENS: dict[str, str] = {
    "swift": "swift", "sag": "swift", "hsm": "hsm", "cbs": "core_banking",
    "finacle": "core_banking", "t24": "core_banking", "flexcube": "core_banking",
    "atm": "atm", "upi": "payments", "imps": "payments", "neft": "payments",
    "rtgs": "payments", "npci": "payments", "switch24": "card_processing",
    "base24": "card_processing", "postilion": "card_processing",
}


def _sector_tags(f: AssetFacts) -> list[Tag]:
    out: list[Tag] = []
    for svc in f.services:
        text = svc.text
        for fn, pat in _SECTOR_BANNERS:
            if text and pat.search(text):
                out.append(Tag("sector_fn", fn, "sector.banner", 0.85,
                               f"{svc.describe()}: {(svc.product or svc.banner or '')[:80]}"))
        if svc.port in _SECTOR_PORTS:
            out.append(Tag("sector_fn", _SECTOR_PORTS[svc.port], "sector.port", 0.45,
                           f"{svc.describe()} is a default {_SECTOR_PORTS[svc.port]} port"))
    name = (f.hostname or f.fqdn or "").lower().split(".")[0]
    for token in re.split(r"[^a-z0-9]+", name):
        if token in _SECTOR_HOST_TOKENS:
            fn = _SECTOR_HOST_TOKENS[token]
            out.append(Tag("sector_fn", fn, "sector.hostname", 0.4,
                           f"hostname token '{token}'"))
    return out


_SECTOR_SCOPE = {
    "swift": "swift_cscf_scope",
    "hsm": "pci_cde_candidate",
    "card_processing": "pci_cde_candidate",
    "payments": "pci_cde_candidate",
    "atm": "pci_cde_candidate",
    "core_banking": "critical_financial_system",
    "trading": "critical_financial_system",
}
_CONFIDENTIAL_ROLES = {"database", "directory", "domain_controller", "file_share", "mail", "backup"}


def _derived(tags: list[Tag]) -> list[Tag]:
    """compliance_scope + data_sensitivity from the evidenced tags.
    A derived tag inherits the confidence of the tag it came from."""
    out: list[Tag] = []
    sectors = [t for t in tags if t.key == "sector_fn"]
    for t in sectors:
        out.append(Tag("compliance_scope", _SECTOR_SCOPE[t.value], "scope.sector",
                       t.confidence, f"sector_fn:{t.value} ({t.evidence})"))
        out.append(Tag("data_sensitivity", "restricted", "sensitivity.sector",
                       t.confidence, f"sector_fn:{t.value}"))
    if not sectors:
        for t in tags:
            if t.key == "role" and t.value in _CONFIDENTIAL_ROLES:
                out.append(Tag("data_sensitivity", "confidential", "sensitivity.role",
                               t.confidence, f"role:{t.value}"))
    return out


# ── entry points ─────────────────────────────────────────────────────────────

def derive_tags(facts: AssetFacts) -> list[Tag]:
    """Every evidenced tag for one asset, deduped by (key, value) keeping the
    highest-confidence instance, in a stable order."""
    raw: list[Tag] = []
    for fn in _RULES:
        raw.extend(fn(facts))
    raw.extend(_sector_tags(facts))
    raw.extend(_derived(raw))
    best: dict[tuple[str, str], Tag] = {}
    for t in raw:
        cur = best.get((t.key, t.value))
        if cur is None or t.confidence > cur.confidence:
            best[(t.key, t.value)] = t
    return sorted(best.values(), key=lambda t: (t.key, -t.confidence, t.value))


def merge_tags(existing: dict | None, auto: Iterable[Tag]) -> dict:
    """New ``Asset.tags`` value: auto tags replaced, manual tags preserved.
    A legacy/free-form dict (no ``manual`` list) contributes no manual tags."""
    manual = []
    if isinstance(existing, dict) and isinstance(existing.get("manual"), list):
        manual = [m for m in existing["manual"] if isinstance(m, dict)]
    return {"v": TAGS_VERSION, "auto": [t.to_dict() for t in auto], "manual": manual}


def tag_strings(tags: dict | None) -> list[str]:
    """Flat ``key:value`` strings (auto + manual) for filters and AI context."""
    if not isinstance(tags, dict):
        return []
    out: list[str] = []
    for bucket in ("auto", "manual"):
        for t in tags.get(bucket) or []:
            if isinstance(t, dict) and t.get("key") and t.get("value"):
                s = f"{t['key']}:{t['value']}"
                if s not in out:
                    out.append(s)
    return out


def _clamp(x: float) -> float:
    return max(0.05, min(1.0, float(x)))


def facts_from_records(asset, services: Iterable) -> AssetFacts:
    """AssetFacts from ORM-shaped objects (Asset + its Service rows). Duck-typed
    so this module never imports the ORM."""
    asset_type = getattr(asset, "asset_type", None)
    return AssetFacts(
        ip=getattr(asset, "ip_address", None),
        hostname=getattr(asset, "hostname", None),
        fqdn=getattr(asset, "fqdn", None),
        os=getattr(asset, "os", None),
        asset_type=getattr(asset_type, "value", asset_type),
        device_role=getattr(asset, "device_role", None),
        role_detail=getattr(asset, "role_detail", None),
        role_confidence=getattr(asset, "role_confidence", None),
        services=tuple(
            ServiceFact(port=int(s.port), protocol=s.protocol or "tcp",
                        service_name=s.service_name, product=s.product,
                        banner=s.banner, exposure=s.exposure)
            for s in services if getattr(s, "port", None) is not None
        ),
    )


def retag(asset, services: Iterable) -> dict:
    """Recompute ``asset.tags`` in place (manual tags preserved); returns it."""
    asset.tags = merge_tags(getattr(asset, "tags", None),
                            derive_tags(facts_from_records(asset, services)))
    return asset.tags
