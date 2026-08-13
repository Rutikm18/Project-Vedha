#!/usr/bin/env python3
"""
findings.py — the interpretation layer that turns collected facts into
vulnerability *findings*.

This is deliberately a SEPARATE module from the collection scanners. Per the
`main_scripts` invariant "no vulnerability conclusions in collection modules",
every scanner emits pure, evidence-backed `ScanResult` facts and never a verdict.
`findings.py` consumes those facts and derives findings — so the collection layer
stays measurable/false-positive-auditable in isolation, and the judgement lives
in one reviewable place.

Boundary (important): these are **configuration / hygiene / exposure** findings a
scanner can conclude from what it directly observed — SMBv1 enabled, weak TLS,
a readable SNMP community, an exposed datastore, a cleartext protocol, a DDoS
amplifier. They are NOT CVE claims. CVE detection needs the pinned vulnerability
database and stays on the manager (the probe never emits a CVE). So a Finding
here has no `cve_id`; it has a `rule_id`, a severity, a confidence, and — always —
the exact observed fact that justifies it.

Design rules:
  * Evidence-backed: every finding cites the fact (scanner, field, value) it came
    from. No finding without an observation.
  * Deterministic + explainable: pure functions over facts; a reviewer can
    reconstruct every verdict. No network, no state, no AI.
  * Ambiguity honoured: a fact whose status is `open|filtered` (never proven open)
    does not raise an exposure finding — consistent with the collection layer's
    refusal to over-claim. Low false-positive by construction.
  * Confidence separates "observed" from "exploitable": an exposed datastore port
    is a real observation (the port answered) but unauth access is unproven, so it
    is `medium` confidence, not `high`.
  * Safe: interpretation only. Nothing here touches the wire.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

# ── taxonomy ────────────────────────────────────────────────────────────────
SEV_CRITICAL = "critical"
SEV_HIGH = "high"
SEV_MEDIUM = "medium"
SEV_LOW = "low"
SEV_INFO = "info"

_SEV_ORDER = {SEV_CRITICAL: 4, SEV_HIGH: 3, SEV_MEDIUM: 2, SEV_LOW: 1, SEV_INFO: 0}

CAT_WEAK_CRYPTO = "weak_crypto"
CAT_MISCONFIG = "misconfiguration"
CAT_EXPOSURE = "exposure"
CAT_CLEARTEXT = "cleartext_protocol"
CAT_AMPLIFICATION = "amplification"
CAT_INFO_DISCLOSURE = "information_disclosure"
CAT_DEFAULT_CRED = "default_credentials"

# Conf: how sure we are the finding is real AND matters as stated.
CONF_HIGH = "high"      # directly observed + unambiguous (SMBv1 on, weak cipher)
CONF_MEDIUM = "medium"  # observed, but the risk depends on unverified context
CONF_LOW = "low"        # weak/heuristic signal


@dataclass
class Finding:
    """One vulnerability finding, always backed by an observed fact."""
    rule_id: str
    title: str
    severity: str
    confidence: str
    category: str
    target: str
    port: int | None
    proto: str | None
    evidence: str                 # human-readable justification citing the fact
    recommendation: str
    data: dict[str, Any] = field(default_factory=dict)   # structured trigger fields
    source_scanner: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "finding",
            "rule_id": self.rule_id,
            "title": self.title,
            "severity": self.severity,
            "confidence": self.confidence,
            "category": self.category,
            "target": self.target,
            "port": self.port,
            "proto": self.proto,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "data": self.data,
            "source_scanner": self.source_scanner,
        }


# ── fact access helpers ─────────────────────────────────────────────────────
def _as_dict(fact: Any) -> dict[str, Any]:
    """Accept a raw JSONL dict or a ScanResult; return a plain dict view."""
    if isinstance(fact, dict):
        return fact
    to_json = getattr(fact, "to_json", None)
    if callable(to_json):
        import json
        return json.loads(fact.to_json())
    # dataclass-ish fallback
    return {k: getattr(fact, k, None)
            for k in ("scanner", "target", "port", "proto", "status", "data", "evidence")}


def _scanner(f: dict) -> str:
    return str(f.get("scanner") or "")


def _data(f: dict) -> dict:
    d = f.get("data")
    return d if isinstance(d, dict) else {}


def _is_open(f: dict) -> bool:
    """A definitively open TCP port. `open|filtered` is NOT open — we never
    raise an exposure finding on an unproven port."""
    return f.get("status") == "open"


# ── rule helpers ────────────────────────────────────────────────────────────
_DATASTORE_PORTS = {
    6379: ("Redis", SEV_HIGH, "Redis commonly ships with no authentication; a reachable instance often allows full data read/write."),
    27017: ("MongoDB", SEV_HIGH, "Historically bound to all interfaces with no auth; exposure has caused mass data breaches."),
    9200: ("Elasticsearch", SEV_HIGH, "Elasticsearch has no auth by default; an exposed node exposes all indexed data."),
    5984: ("CouchDB", SEV_HIGH, "CouchDB admin party / unauth REST exposes the database."),
    11211: ("Memcached", SEV_MEDIUM, "Unauthenticated cache; also a potent UDP amplification reflector."),
    9042: ("Cassandra", SEV_MEDIUM, "Exposed CQL port; verify authentication is enforced."),
    3306: ("MySQL/MariaDB", SEV_MEDIUM, "Database service reachable from the scan vantage; should be network-restricted."),
    5432: ("PostgreSQL", SEV_MEDIUM, "Database service reachable from the scan vantage; should be network-restricted."),
    1433: ("Microsoft SQL Server", SEV_MEDIUM, "Database service reachable from the scan vantage; should be network-restricted."),
    1521: ("Oracle DB", SEV_MEDIUM, "Database listener reachable from the scan vantage; should be network-restricted."),
}

# UDP services that are DDoS amplification reflectors when they answer spoofable queries.
_AMPLIFIER_SERVICES = {"ntp", "dns", "ssdp", "memcached", "chargen", "snmp", "ldap", "netbios"}

# Confirmed datastore service name -> (display name, severity). Keyed on the
# service the banner CONFIRMED (behaviour), not the port number — so an instance
# on a non-standard port is still caught.
_DATASTORE_SERVICES = {
    "redis": ("Redis", SEV_HIGH), "mongodb": ("MongoDB", SEV_HIGH),
    "elasticsearch": ("Elasticsearch", SEV_HIGH), "couchdb": ("CouchDB", SEV_HIGH),
    "memcached": ("Memcached", SEV_MEDIUM), "mysql": ("MySQL/MariaDB", SEV_MEDIUM),
    "postgresql": ("PostgreSQL", SEV_MEDIUM), "mssql": ("Microsoft SQL Server", SEV_MEDIUM),
}


def build_service_index(facts) -> dict:
    """Map (target, port) -> confirmed-service info from service_banner facts.

    Only behaviour-confirmed services (``data.service`` present on an open port)
    are indexed — this is the 'port is only a hint, behaviour confirms' contract."""
    idx: dict = {}
    for raw in facts:
        f = _as_dict(raw)
        if _scanner(f) != "service_banner" or f.get("status") != "open":
            continue
        svc = (_data(f).get("service") or "").lower()
        if not svc:
            continue
        idx[(f.get("target"), f.get("port"))] = {
            "service": svc,
            "product": _data(f).get("product"),
            "version": _data(f).get("version"),
        }
    return idx


# ── rules: each takes the full fact list, yields Finding(s) ─────────────────
def _rule_tls(facts: list[dict]) -> Iterable[Finding]:
    for f in facts:
        if _scanner(f) != "tls_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port")
        accepted = [v.upper().replace(" ", "") for v in (d.get("accepted_versions") or [])]

        obsolete = [v for v in accepted if v in ("SSLV2", "SSLV3")]
        legacy = [v for v in accepted if v in ("TLSV1", "TLSV1.0", "TLSV1.1")]
        if obsolete:
            yield Finding(
                "TLS-OBSOLETE-PROTO", f"Obsolete SSL/TLS protocol offered ({', '.join(obsolete)})",
                SEV_HIGH, CONF_HIGH, CAT_WEAK_CRYPTO, target, port, "tcp",
                f"TLS endpoint negotiated {', '.join(obsolete)} — cryptographically broken (POODLE/DROWN).",
                "Disable SSLv2/SSLv3 entirely; offer TLS 1.2+ only.",
                {"accepted_versions": accepted}, "tls_scan")
        elif legacy:
            yield Finding(
                "TLS-LEGACY-PROTO", f"Deprecated TLS protocol offered ({', '.join(legacy)})",
                SEV_MEDIUM, CONF_HIGH, CAT_WEAK_CRYPTO, target, port, "tcp",
                f"TLS endpoint negotiated {', '.join(legacy)} — deprecated (PCI-DSS forbids TLS < 1.2).",
                "Disable TLS 1.0/1.1; require TLS 1.2 or 1.3.",
                {"accepted_versions": accepted}, "tls_scan")

        weak = [c for c in (d.get("cipher_analysis") or []) if isinstance(c, dict) and c.get("weak")]
        if weak:
            names = ", ".join(str(c.get("name")) for c in weak)
            reasons = sorted({r for c in weak for r in (c.get("weak_reasons") or [])})
            yield Finding(
                "TLS-WEAK-CIPHER", f"Weak TLS cipher(s) accepted ({names})",
                SEV_HIGH, CONF_HIGH, CAT_WEAK_CRYPTO, target, port, "tcp",
                f"Weak cipher accepted: {names} ({', '.join(reasons) or 'weak'}).",
                "Restrict to strong AEAD ciphers (e.g. ECDHE + AES-GCM / ChaCha20); drop RC4/3DES/EXPORT/NULL.",
                {"weak_ciphers": names, "reasons": reasons}, "tls_scan")

        cert = d.get("certificate") if isinstance(d.get("certificate"), dict) else {}
        if cert.get("expired"):
            yield Finding(
                "TLS-CERT-EXPIRED", "Expired TLS certificate",
                SEV_MEDIUM, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                f"Certificate expired (not_after={cert.get('not_after')}).",
                "Renew the certificate and automate renewal (e.g. ACME).",
                {"not_after": cert.get("not_after")}, "tls_scan")
        if cert.get("self_signed"):
            yield Finding(
                "TLS-CERT-SELF-SIGNED", "Self-signed TLS certificate",
                SEV_LOW, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                "Certificate is self-signed (subject == issuer) — no trusted chain."
                + (f" JA4X={cert['ja4x']} (for infrastructure correlation)."
                   if cert.get("ja4x") else ""),
                "Use a CA-issued certificate for anything outside a closed lab.",
                {"self_signed": True, "ja4x": cert.get("ja4x")}, "tls_scan")


def _rule_smb(facts: list[dict]) -> Iterable[Finding]:
    for f in facts:
        if _scanner(f) != "smb_scan":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 445
        if d.get("smbv1_enabled") is True:
            yield Finding(
                "SMB-V1-ENABLED", "SMBv1 protocol enabled",
                SEV_HIGH, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                "Server negotiated SMBv1 — deprecated and the vector for wormable exploits (EternalBlue/WannaCry).",
                "Disable SMBv1 (Windows: Remove-WindowsFeature FS-SMB1). Use SMB 3.x only.",
                {"smbv1_enabled": True, "negotiated_dialect": d.get("negotiated_dialect")}, "smb_scan")
        # signing_required False is only meaningful when we actually negotiated.
        if d.get("signing_required") is False and d.get("signing_supported") is not None:
            yield Finding(
                "SMB-SIGNING-NOT-REQUIRED", "SMB signing not required",
                SEV_MEDIUM, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                "SMB message signing is not required — enables SMB relay / MITM attacks.",
                "Require SMB signing (RequireSecuritySignature = True) on servers and DCs.",
                {"signing_required": False, "signing_supported": d.get("signing_supported")}, "smb_scan")


def _rule_snmp(facts: list[dict]) -> Iterable[Finding]:
    _WEAK_COMMUNITIES = {"public", "private", "community", "manager", "snmp", "cisco", "admin"}
    for f in facts:
        if _scanner(f) != "snmp_scan":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 161
        community = d.get("community")
        if community:
            weak = str(community).lower() in _WEAK_COMMUNITIES
            yield Finding(
                "SNMP-COMMUNITY-READABLE",
                f"SNMP community string readable ('{community}')",
                SEV_HIGH if weak else SEV_MEDIUM, CONF_HIGH, CAT_DEFAULT_CRED,
                target, port, "udp",
                f"SNMP agent answered community '{community}'"
                + (" — a default/guessable string." if weak else ".")
                + " Discloses system/network inventory; write access can reconfigure the device.",
                "Remove default communities; move to SNMPv3 (authPriv). If SNMP is unneeded, disable it.",
                {"community": community, "weak_default": weak,
                 "snmpv3_present": d.get("snmpv3_present")}, "snmp_scan")
        amp = d.get("amplification_factor")
        if isinstance(amp, (int, float)) and amp >= 5:
            yield Finding(
                "SNMP-AMPLIFICATION", f"SNMP DDoS amplification (~{amp}x)",
                SEV_MEDIUM, CONF_HIGH, CAT_AMPLIFICATION, target, port, "udp",
                f"GETBULK reply is ~{amp}x the request — usable as a spoofed-source DDoS reflector.",
                "Restrict SNMP to management networks; disable GETBULK to untrusted sources.",
                {"amplification_factor": amp}, "snmp_scan")


def _rule_udp_amplification(facts: list[dict]) -> Iterable[Finding]:
    for f in facts:
        if _scanner(f) != "udp_scan":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port")
        svc = str(d.get("service") or "").lower()
        if d.get("monlist_enabled") is True:
            yield Finding(
                "UDP-NTP-MONLIST", "NTP monlist enabled (DDoS amplifier)",
                SEV_MEDIUM, CONF_HIGH, CAT_AMPLIFICATION, target, port or 123, "udp",
                "NTP server answered the monlist query — a very high-factor spoofed-source DDoS reflector (CVE-2013-5211 class).",
                "Disable monlist (noquery / restrict default), or upgrade ntpd; consider chrony.",
                {"service": "ntp", "monlist_enabled": True}, "udp_scan")
        if d.get("open_recursion") is True:
            yield Finding(
                "UDP-DNS-OPEN-RESOLVER", "Open DNS resolver (recursion available)",
                SEV_MEDIUM, CONF_HIGH, CAT_AMPLIFICATION, target, port or 53, "udp",
                "DNS server offers recursion to arbitrary clients — usable as a DNS amplification reflector and for cache poisoning.",
                "Disable open recursion; restrict recursion to trusted clients.",
                {"service": "dns", "open_recursion": True}, "udp_scan")
        # generic amplifier that positively answered a spoofable query
        if svc in _AMPLIFIER_SERVICES and d.get("responded") is True and f.get("status") == "open" \
                and svc not in ("ntp", "dns"):
            yield Finding(
                "UDP-AMPLIFIER-EXPOSED", f"UDP amplification service exposed ({svc})",
                SEV_LOW, CONF_MEDIUM, CAT_AMPLIFICATION, target, port, "udp",
                f"{svc.upper()} answered an unauthenticated UDP query — a potential spoofed-source DDoS reflector.",
                "Restrict the service to trusted networks or disable if unneeded.",
                {"service": svc}, "udp_scan")


def _rule_cleartext_and_exposure(facts: list[dict]) -> Iterable[Finding]:
    # Behaviour confirms the service; the port number is only a hint (spec Phase 16).
    index = build_service_index(facts)
    for f in facts:
        # Only reason about definitively OPEN tcp ports from a port scanner or the
        # service banner. `open|filtered` never triggers an exposure finding.
        if _scanner(f) not in ("port_scan", "syn_scan", "mass_scan", "service_banner"):
            continue
        if f.get("proto") not in ("tcp", None) or not _is_open(f):
            continue
        port = f.get("port")
        target = f.get("target")
        confirmed = index.get((target, port), {})
        svc = confirmed.get("service")

        # ── 1) CONFIRMED service (behaviour) — high confidence, any port ──
        if svc in _DATASTORE_SERVICES:
            name, sev = _DATASTORE_SERVICES[svc]
            yield Finding(
                "SVC-DATASTORE-EXPOSED", f"{name} reachable from the scan vantage",
                sev, CONF_HIGH, CAT_EXPOSURE, target, port, "tcp",
                f"{name} confirmed by banner on port {port}; reachable from the scan "
                "position. Bind to localhost/management network and require auth.",
                f"Bind {name} to localhost/management network and require authentication.",
                {"service": name, "port": port, "confirmed": True,
                 "version": confirmed.get("version")}, "service_banner")
            continue
        if svc == "ftp":
            yield Finding(
                "SVC-FTP-CLEARTEXT", "FTP exposed (cleartext control channel)",
                SEV_MEDIUM, CONF_HIGH, CAT_CLEARTEXT, target, port, "tcp",
                f"FTP confirmed by banner on port {port}; credentials travel in cleartext. "
                "Verify anonymous access is disabled.",
                "Use FTPS/SFTP; disable anonymous FTP.",
                {"port": port, "confirmed": True}, "service_banner")
            continue
        if svc == "telnet":
            yield Finding(
                "SVC-TELNET-CLEARTEXT", "Telnet exposed (cleartext credentials)",
                SEV_HIGH, CONF_HIGH, CAT_CLEARTEXT, target, port, "tcp",
                f"Telnet confirmed on port {port} — credentials and session in cleartext.",
                "Disable Telnet; use SSH.",
                {"port": port, "confirmed": True}, "service_banner")
            continue

        # ── 2) No behavioural confirmation — port-number HINT only (lower conf) ──
        if port == 23:
            yield Finding(
                "SVC-TELNET-CLEARTEXT", "Telnet exposed (cleartext credentials)",
                SEV_HIGH, CONF_MEDIUM, CAT_CLEARTEXT, target, port, "tcp",
                "Port 23 open — Telnet by convention (port-based, service not confirmed); "
                "Telnet transmits credentials in cleartext.",
                "Disable Telnet; use SSH.", {"port": 23, "confirmed": False}, _scanner(f))
        elif port == 21:
            yield Finding(
                "SVC-FTP-CLEARTEXT", "FTP exposed (cleartext control channel)",
                SEV_MEDIUM, CONF_MEDIUM, CAT_CLEARTEXT, target, port, "tcp",
                "Port 21 open — FTP by convention (port-based, service not confirmed); "
                "FTP transmits credentials in cleartext.",
                "Use FTPS/SFTP; disable anonymous FTP.", {"port": 21, "confirmed": False}, _scanner(f))
        elif port == 3389:
            yield Finding(
                "SVC-RDP-EXPOSED", "RDP exposed to the scan vantage",
                SEV_MEDIUM, CONF_MEDIUM, CAT_EXPOSURE, target, port, "tcp",
                "Port 3389 open — RDP by convention (port-based, service not confirmed); "
                "a common brute-force / exploit target (e.g. BlueKeep class).",
                "Restrict RDP to VPN/jump hosts; enforce NLA + MFA.",
                {"port": 3389, "confirmed": False}, _scanner(f))
        elif port in _DATASTORE_PORTS:
            name, sev, why = _DATASTORE_PORTS[port]
            yield Finding(
                "SVC-DATASTORE-EXPOSED", f"{name} reachable from the scan vantage",
                sev, CONF_MEDIUM, CAT_EXPOSURE, target, port, "tcp",
                f"Port {port} open — {name} by convention (port-based, service not "
                f"confirmed). {why}",
                f"Bind {name} to localhost/management network and require authentication.",
                {"service": name, "port": port, "confirmed": False}, _scanner(f))


def _rule_web(facts: list[dict]) -> Iterable[Finding]:
    for f in facts:
        if _scanner(f) not in ("web_scan", "http_scan"):
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port")
        methods = d.get("dangerous_methods") or []
        risky = [m for m in methods if str(m).upper() in ("PUT", "DELETE", "TRACE", "CONNECT")]
        if risky:
            yield Finding(
                "WEB-DANGEROUS-METHODS", f"Dangerous HTTP methods enabled ({', '.join(risky)})",
                SEV_MEDIUM, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                f"Server allows {', '.join(risky)} — can enable content tampering (PUT/DELETE) or XST (TRACE).",
                "Disable unused HTTP methods; allow only GET/HEAD/POST as required.",
                {"dangerous_methods": risky}, "web_scan")
        server = d.get("server")
        if server and any(ch.isdigit() for ch in str(server)):
            yield Finding(
                "WEB-SERVER-VERSION-DISCLOSURE", "Web server version disclosed",
                SEV_INFO, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
                f"Server header discloses software + version: '{server}'.",
                "Suppress version tokens (e.g. server_tokens off / ServerTokens Prod).",
                {"server": server}, "web_scan")

        # High-value hardening headers only — ignore the optional ones to avoid noise.
        missing = [h for h in (d.get("security_headers_missing") or []) if isinstance(h, str)]
        key_missing = [h for h in missing if h in (
            "content-security-policy", "strict-transport-security",
            "x-frame-options", "x-content-type-options")]
        if key_missing:
            yield Finding(
                "WEB-MISSING-SECURITY-HEADERS",
                f"Missing HTTP security headers ({len(key_missing)})",
                SEV_LOW, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                "Response omits hardening headers: " + ", ".join(key_missing) + ".",
                "Add HSTS, Content-Security-Policy, X-Frame-Options, and X-Content-Type-Options.",
                {"missing": key_missing}, "web_scan")

        xpb = d.get("x_powered_by")
        if xpb:
            yield Finding(
                "WEB-XPOWEREDBY-DISCLOSURE", "Framework disclosed via X-Powered-By",
                SEV_INFO, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
                f"X-Powered-By header discloses the tech stack: '{xpb}'.",
                "Remove the X-Powered-By header.",
                {"x_powered_by": xpb}, "web_scan")


def _rule_tls_fingerprint(facts: list[dict]) -> Iterable[Finding]:
    """JA4X-based threat-intel match. Fires only when a certificate's structural
    fingerprint matches a curated known-suspicious profile — the JA4X itself is
    always attached to the TLS fact (see tls_scanner) for downstream correlation."""
    from main_scripts.ja4x import match_suspicious
    for f in facts:
        if _scanner(f) != "tls_scan" or f.get("status") != "open":
            continue
        cert = _data(f).get("certificate")
        cert = cert if isinstance(cert, dict) else {}
        ja4x = cert.get("ja4x")
        label = match_suspicious(ja4x)
        if label:
            yield Finding(
                "TLS-SUSPICIOUS-CERT-FINGERPRINT",
                "TLS certificate fingerprint matches known-suspicious tooling",
                SEV_HIGH, CONF_MEDIUM, CAT_MISCONFIG, f.get("target"), f.get("port"), "tcp",
                f"Certificate JA4X {ja4x} matches a known-suspicious profile: {label}.",
                "Investigate the host — this certificate structure is associated with the named tooling/actor.",
                {"ja4x": ja4x, "match": label}, "tls_scan")


_RULES: list[Callable[[list[dict]], Iterable[Finding]]] = [
    _rule_tls, _rule_smb, _rule_snmp, _rule_udp_amplification,
    _rule_cleartext_and_exposure, _rule_web, _rule_tls_fingerprint,
]


# ── public API ──────────────────────────────────────────────────────────────
def run_findings(facts: Iterable[Any]) -> list[Finding]:
    """Derive findings from collected facts. Pure; deterministic; safe.

    Accepts ScanResult objects or raw JSONL dicts. Findings are de-duplicated by
    (rule_id, target, port) and returned most-severe first."""
    norm = [_as_dict(f) for f in facts]
    seen: dict[tuple, Finding] = {}
    for rule in _RULES:
        for finding in rule(norm):
            key = (finding.rule_id, finding.target, finding.port)
            if key not in seen:
                seen[key] = finding
    return sorted(
        seen.values(),
        key=lambda x: (_SEV_ORDER.get(x.severity, 0), x.target or "", x.port or 0),
        reverse=True,
    )


def summarize(findings: list[Finding]) -> dict[str, Any]:
    counts = {s: 0 for s in (SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW, SEV_INFO)}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    return {
        "total": len(findings),
        "by_severity": counts,
        "by_category": _tally(findings, lambda x: x.category),
        "actionable": sum(1 for f in findings if f.severity in (SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM)),
    }


def _tally(findings: list[Finding], key) -> dict[str, int]:
    out: dict[str, int] = {}
    for f in findings:
        k = key(f)
        out[k] = out.get(k, 0) + 1
    return out


def load_facts_jsonl(path: str) -> list[dict]:
    """Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)."""
    import json
    out: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def _main(argv: list[str] | None = None) -> int:
    """CLI: derive findings from one or more scanner JSONL files.

        python -m main_scripts.findings scan1.jsonl scan2.jsonl [--json]
    """
    import argparse
    import json
    ap = argparse.ArgumentParser(description="Derive findings from scanner JSONL facts")
    ap.add_argument("files", nargs="+", help="scanner output JSONL file(s)")
    ap.add_argument("--json", action="store_true", help="emit findings as JSONL")
    ap.add_argument("--min-severity", default="info",
                    choices=[SEV_INFO, SEV_LOW, SEV_MEDIUM, SEV_HIGH, SEV_CRITICAL])
    args = ap.parse_args(argv)

    facts: list[dict] = []
    for p in args.files:
        facts.extend(load_facts_jsonl(p))
    findings = [f for f in run_findings(facts)
                if _SEV_ORDER[f.severity] >= _SEV_ORDER[args.min_severity]]

    if args.json:
        for f in findings:
            print(json.dumps(f.to_dict(), default=str))
    else:
        print(json.dumps(summarize(findings), indent=2))
        for f in findings:
            loc = f"{f.target}:{f.port}" if f.port else f.target
            print(f"  [{f.severity.upper():8}] {f.rule_id:28} {loc:22} {f.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
