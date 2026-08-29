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
        # Forgeable signature hash: SHA-1 is collision-broken (SHAttered) and MD5
        # trivially so — a signature over such a hash gives no integrity guarantee.
        sig = str(cert.get("sig_algorithm") or "").lower()
        if sig in ("sha1", "md5", "md2", "md4"):
            yield Finding(
                "TLS-CERT-WEAK-SIGNATURE", f"Certificate signed with weak hash ({sig.upper()})",
                SEV_MEDIUM, CONF_HIGH, CAT_WEAK_CRYPTO, target, port, "tcp",
                f"The certificate's signature uses {sig.upper()} — a collision-broken "
                "hash (SHA-1/MD5); the certificate can be forged and browsers/CAs reject it.",
                "Re-issue the certificate with a SHA-256 (or stronger) signature.",
                {"sig_algorithm": sig}, "tls_scan")
        # Under-strength public key: RSA/DSA below 2048 bits is factorable at or near
        # practical reach and no longer CA/B-compliant. (EC keys are excluded — 256-bit
        # EC ≈ 3072-bit RSA, so the bit count isn't comparable.)
        kbits = cert.get("public_key_bits")
        ktype = str(cert.get("public_key_type") or "").upper()
        if isinstance(kbits, int) and kbits < 2048 and ("RSA" in ktype or "DSA" in ktype):
            yield Finding(
                "TLS-CERT-WEAK-KEY", f"Under-strength {ktype or 'RSA'} public key ({kbits}-bit)",
                SEV_MEDIUM, CONF_HIGH, CAT_WEAK_CRYPTO, target, port, "tcp",
                f"The certificate carries a {kbits}-bit {ktype or 'RSA'} public key — "
                "below the 2048-bit minimum; factorable/deprecated and CA/B-noncompliant.",
                "Re-issue with a >=2048-bit RSA key (or a 256-bit+ ECDSA key).",
                {"public_key_type": ktype, "public_key_bits": kbits}, "tls_scan")


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


def _rule_unauth_access(facts: list[dict]) -> Iterable[Finding]:
    """Proven UNAUTHENTICATED access to a datastore (from the collected banner) —
    a real foothold, not just an open port. Redis unauth is RCE-capable."""
    from main_scripts.unauth_access import classify_unauth_access, is_rce_capable
    for f in facts:
        if _scanner(f) != "service_banner" or f.get("status") != "open":
            continue
        d = _data(f)
        svc = (d.get("service") or "").lower()
        if classify_unauth_access(svc, d.get("banner")) is not True:
            continue
        rce = is_rce_capable(svc)
        impact = ("full read/write of the datastore AND remote code execution "
                  "(e.g. Redis CONFIG SET dir + SAVE to drop a webshell / cron / SSH key)"
                  if rce else "full read/write access to the datastore's data")
        yield Finding(
            "SVC-UNAUTH-DATASTORE-ACCESS",
            f"Unauthenticated {svc} access confirmed",
            SEV_CRITICAL if rce else SEV_HIGH, CONF_HIGH, CAT_DEFAULT_CRED,
            f.get("target"), f.get("port"), "tcp",
            f"{svc} answered a read-only query WITHOUT authentication on port "
            f"{f.get('port')} — a proven unauthenticated foothold enabling {impact}.",
            f"Enable authentication on {svc}; bind it to localhost/management network only.",
            {"service": svc, "unauthenticated": True, "rce_capable": rce}, "service_banner")


def _rule_tls_server_fingerprint(facts: list[dict]) -> Iterable[Finding]:
    """JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only
    on a curated known-suspicious profile; the JA4S is attached to the TLS fact
    (tls_fingerprint) for downstream correlation regardless."""
    from main_scripts.ja4s import match_suspicious
    for f in facts:
        if _scanner(f) not in ("tls_scan", "tls_fingerprint") or f.get("status") != "open":
            continue
        ja4s = _data(f).get("ja4s")
        label = match_suspicious(ja4s)
        if label:
            yield Finding(
                "TLS-SUSPICIOUS-SERVER-FINGERPRINT",
                "TLS server fingerprint matches known-suspicious profile",
                SEV_HIGH, CONF_MEDIUM, CAT_MISCONFIG, f.get("target"), f.get("port"), "tcp",
                f"Server JA4S {ja4s} matches a known-suspicious profile: {label}.",
                "Investigate the host — this TLS server behaviour is associated with the named tooling/actor.",
                {"ja4s": ja4s, "match": label}, "tls_fingerprint")


def _rule_rdp(facts: list[dict]) -> Iterable[Finding]:
    """Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint
    exposure rule so a CONFIRMED RDP wins the (rule_id,target,port) dedup."""
    for f in facts:
        if _scanner(f) != "rdp_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        if not d.get("rdp_confirmed"):
            continue
        target, port = f.get("target"), f.get("port") or 3389
        # NLA required (proven by the RDP-only probe being refused) means the RDP
        # stack is NOT reachable pre-auth: low risk. NLA merely *supported* (or the
        # requirement unknown) stays medium. This is the confirmed-handshake fact,
        # not a port-based guess — so no "BlueKeep class" language here.
        nla_required = d.get("nla_required")
        if nla_required is True:
            sev = SEV_LOW
            desc = ("RDP confirmed via X.224 handshake; NLA (CredSSP) is REQUIRED "
                    + ("with TLS" if d.get("tls") else "") +
                    " — the RDP stack is not reachable pre-authentication.")
        else:
            sev = SEV_MEDIUM
            desc = "RDP confirmed via X.224 handshake — reachable from the scan vantage."
        yield Finding(
            "SVC-RDP-EXPOSED", "RDP exposed (confirmed by handshake)",
            sev, CONF_HIGH, CAT_EXPOSURE, target, port, "tcp",
            desc,
            "Restrict RDP to VPN/jump hosts; enforce NLA + MFA.",
            {"port": port, "confirmed": True,
             "nla": d.get("nla"), "nla_required": nla_required, "tls": d.get("tls"),
             "selected_protocol": d.get("selected_protocol")}, "rdp_scan")
        # The BlueKeep-class finding fires ONLY when NLA is genuinely not in force:
        # nla False AND the server did not refuse (so it accepted a weaker session)
        # AND NLA is not required. A CONFIRMED-NLA host never reaches this.
        if (d.get("nla") is False and d.get("negotiation") != "failure"
                and nla_required is not True):
            yield Finding(
                "SVC-RDP-NO-NLA", "RDP without Network Level Authentication",
                SEV_HIGH, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                "RDP negotiated without NLA (CredSSP): the RDP stack is reachable "
                "pre-authentication — brute-forceable and in the BlueKeep "
                "(CVE-2019-0708) class.",
                "Require NLA (CredSSP) on RDP; patch legacy hosts; restrict to VPN/jump hosts.",
                {"port": port, "selected_protocol": d.get("selected_protocol"),
                 "standard_rdp_security": d.get("standard_rdp_security", False)}, "rdp_scan")


def _rule_ssh(facts: list[dict]) -> Iterable[Finding]:
    for f in facts:
        if _scanner(f) != "ssh_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port")

        failures = [x for x in (d.get("failures") or []) if isinstance(x, dict)]
        if failures:
            names = ", ".join(sorted({x.get("algorithm") for x in failures}))
            reasons = sorted({r for x in failures for r in (x.get("reasons") or [])})
            yield Finding(
                "SSH-WEAK-ALGO", f"Weak SSH algorithm(s) offered ({names})",
                SEV_HIGH, CONF_HIGH, CAT_WEAK_CRYPTO, target, port, "tcp",
                f"SSH server offers broken/deprecated algorithms: {names} "
                f"({'; '.join(reasons) or 'weak'}).",
                "Disable weak KEX/ciphers/MACs and legacy host keys; keep only "
                "curve25519/ECDH-strong KEX, AES-GCM/ChaCha20 ciphers, ETM SHA-2 "
                "MACs, and ed25519/rsa-sha2 host keys.",
                {"weak_algorithms": names, "reasons": reasons}, "ssh_scan")

        if d.get("terrapin_vulnerable"):
            yield Finding(
                "SSH-TERRAPIN", "SSH vulnerable to Terrapin (CVE-2023-48795)",
                SEV_MEDIUM, CONF_MEDIUM, CAT_WEAK_CRYPTO, target, port, "tcp",
                "SSH offers a Terrapin-affected mode (ChaCha20-Poly1305 or CBC+ETM) "
                "without strict key exchange — a MitM can truncate handshake "
                "messages and downgrade connection security.",
                "Enable strict key exchange (upgrade OpenSSH >= 9.6 / current "
                "server); prefer AES-GCM ciphers.",
                {"terrapin": True}, "ssh_scan")


_DEFAULT_SMB_SHARES = {"IPC$", "ADMIN$", "PRINT$", "NETLOGON", "SYSVOL"}


def _rule_smb_enum(facts: list[dict]) -> Iterable[Finding]:
    """Anonymous SMB (null-session) information disclosure. The null session is a
    misconfiguration; a disclosed USER list is the higher-value finding because it
    directly seeds password-spraying against other services."""
    for f in facts:
        if _scanner(f) != "smb_enum_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        if not d.get("null_session"):
            continue
        target, port = f.get("target"), f.get("port") or 445
        shares = [s for s in (d.get("shares") or []) if isinstance(s, dict)]
        nondefault = sorted({s.get("name") for s in shares
                             if str(s.get("name") or "").upper().rstrip("$") + "$"
                             not in _DEFAULT_SMB_SHARES
                             and str(s.get("name") or "") not in _DEFAULT_SMB_SHARES})
        kind = "guest" if d.get("guest_session") else "null"
        yield Finding(
            "SMB-NULL-SESSION",
            f"SMB {kind} session permitted (anonymous enumeration)",
            SEV_MEDIUM, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
            f"Server accepted an anonymous SMB {kind} session (empty credentials) and "
            f"disclosed identity/shares to an unauthenticated peer"
            + (f"; server_os='{d.get('server_os')}'" if d.get("server_os") else "")
            + (f", domain='{d.get('server_domain')}'" if d.get("server_domain") else "")
            + (f", non-default shares: {', '.join(nondefault)}" if nondefault else "")
            + ".",
            "Disable anonymous/null SMB sessions (RestrictAnonymous / "
            "RestrictNullSessAccess); restrict share and pipe access to authenticated users.",
            {"null_session": True, "guest_session": d.get("guest_session"),
             "server_os": d.get("server_os"), "server_domain": d.get("server_domain"),
             "share_count": d.get("share_count"), "nondefault_shares": nondefault},
            "smb_enum_scan")

        users = [u for u in (d.get("users") or []) if isinstance(u, dict)]
        if users:
            sample = ", ".join(sorted({str(u.get("name")) for u in users})[:10])
            yield Finding(
                "SMB-NULL-SESSION-USERS",
                f"Domain/local users disclosed via SMB null session ({len(users)})",
                SEV_HIGH, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
                f"{len(users)} user account(s) were enumerated anonymously over SMB "
                f"(SAMR / RID cycling): {sample}"
                + (" ..." if len(users) > 10 else "")
                + ". A valid username list directly enables targeted password spraying.",
                "Disable anonymous SAMR/LSA enumeration (RestrictAnonymous=2, "
                "RestrictAnonymousSAM=1); require authentication for account enumeration.",
                {"user_count": len(users), "sample_users": sample,
                 "method": d.get("user_enum_method")}, "smb_enum_scan")


def _rule_ldap(facts: list[dict]) -> Iterable[Finding]:
    """Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an
    anonymously READABLE directory tree is a real unauthorized-access disclosure."""
    for f in facts:
        if _scanner(f) != "ldap_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        if not d.get("anonymous_bind"):
            continue
        target, port = f.get("target"), f.get("port") or 389
        contexts = [c for c in (d.get("naming_contexts") or []) if isinstance(c, str)]
        yield Finding(
            "LDAP-ANON-BIND", "LDAP anonymous bind permitted",
            SEV_LOW, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
            "LDAP accepted an anonymous bind (empty credentials) and disclosed the "
            "RootDSE"
            + (f"; naming contexts: {', '.join(contexts[:4])}" if contexts else "")
            + (f", dnsHostName='{d.get('dns_host_name')}'" if d.get("dns_host_name") else "")
            + ".",
            "Require authentication for LDAP binds; disable anonymous bind where the "
            "directory service supports it (dsHeuristics / equivalent).",
            {"naming_contexts": contexts, "dns_host_name": d.get("dns_host_name"),
             "ssl": d.get("ssl")}, "ldap_scan")

        if d.get("anonymous_search_allowed"):
            n = d.get("sample_entry_count") or 0
            yield Finding(
                "LDAP-ANON-SEARCH",
                "LDAP directory readable without authentication",
                SEV_HIGH, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
                f"The directory tree returned {n}+ entries to an ANONYMOUS search "
                "(bounded sample) — directory contents (accounts, groups, attributes) "
                "are exposed to any unauthenticated client.",
                "Restrict anonymous read access to the directory tree; scope anonymous "
                "access to the RootDSE only, or require authentication entirely.",
                {"sample_entry_count": n, "ssl": d.get("ssl")}, "ldap_scan")


def _rule_dns(facts: list[dict]) -> Iterable[Finding]:
    """DNS server hygiene: a full AXFR zone transfer is the high-value finding
    (entire internal inventory disclosed); version.bind is info disclosure; an
    AXFR-confirmed zone with no DNSKEY is an unsigned-zone note (low, no noise
    since it only fires on a zone we PROVED is authoritative)."""
    for f in facts:
        if _scanner(f) != "dns_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 53
        axfr = d.get("axfr") if isinstance(d.get("axfr"), dict) else {}
        transferred = sorted(z for z, r in axfr.items()
                             if isinstance(r, dict) and r.get("transferred"))
        if transferred:
            total = sum(int(axfr[z].get("record_count") or 0) for z in transferred)
            yield Finding(
                "DNS-ZONE-TRANSFER",
                f"DNS zone transfer (AXFR) allowed ({', '.join(transferred)})",
                SEV_HIGH, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
                f"The server allowed a full AXFR zone transfer of {', '.join(transferred)} "
                f"(~{total} records) to an unauthorized client — exposing the complete "
                "zone inventory (host names, addresses, internal services).",
                "Restrict zone transfers to authorized secondary name servers only "
                "(allow-transfer + TSIG); deny AXFR from arbitrary clients.",
                {"zones": transferred, "record_count": total}, "dns_scan")

        vb = d.get("version_bind")
        if vb:
            yield Finding(
                "DNS-VERSION-DISCLOSURE", "DNS server version disclosed (version.bind)",
                SEV_INFO, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "udp",
                f"The server answered a CHAOS version.bind query, disclosing its "
                f"software/version: '{vb}'.",
                "Suppress the version response (e.g. BIND options 'version \"\";') or "
                "restrict CHAOS-class queries.",
                {"version_bind": vb, "hostname_bind": d.get("hostname_bind")}, "dns_scan")

        dnssec = d.get("dnssec") if isinstance(d.get("dnssec"), dict) else {}
        unsigned = sorted(z for z in transferred if dnssec.get(z) is False)
        if unsigned:
            yield Finding(
                "DNS-DNSSEC-ABSENT", f"Zone not DNSSEC-signed ({', '.join(unsigned)})",
                SEV_LOW, CONF_MEDIUM, CAT_MISCONFIG, target, port, "udp",
                f"Confirmed authoritative zone(s) {', '.join(unsigned)} publish no DNSKEY "
                "(not DNSSEC-signed) — responses cannot be cryptographically validated, "
                "leaving resolvers exposed to cache poisoning / spoofing.",
                "Sign the zone with DNSSEC and publish a DS record at the parent.",
                {"unsigned_zones": unsigned}, "dns_scan")


def _rule_nfs(facts: list[dict]) -> Iterable[Finding]:
    """NFS anonymous export exposure. A world-readable export is the high-value
    finding (any reachable host can mount and read it); an answering portmapper is
    a low recon-disclosure note."""
    for f in facts:
        if _scanner(f) != "nfs_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 2049
        wr = [p for p in (d.get("world_readable_exports") or []) if isinstance(p, str)]
        if wr:
            yield Finding(
                "NFS-EXPORT-WORLD-READABLE",
                f"NFS export(s) world-readable ({len(wr)})",
                SEV_HIGH, CONF_HIGH, CAT_EXPOSURE, target, port, "tcp",
                "NFS exports are shared with no client restriction / a wildcard group: "
                + ", ".join(wr[:8]) + (" ..." if len(wr) > 8 else "")
                + ". Any host able to reach the server can mount and read these paths.",
                "Restrict every export to specific hosts/subnets (no '*'); enable "
                "root_squash and require Kerberos (sec=krb5); remove exports that do "
                "not need network sharing.",
                {"world_readable_exports": wr, "mountd_port": d.get("mountd_port"),
                 "export_count": d.get("export_count")}, "nfs_scan")

        if d.get("portmap_open"):
            progs = [p for p in (d.get("rpc_programs") or []) if isinstance(p, dict)]
            yield Finding(
                "RPC-PORTMAPPER-EXPOSED", "RPC portmapper (rpcbind) enumerable",
                SEV_LOW, CONF_HIGH, CAT_INFO_DISCLOSURE, target, 111, "tcp",
                f"The portmapper answered a DUMP, disclosing {len(progs)} registered RPC "
                "service(s) (the rpcinfo view) — a map of NFS/NIS/lockd services and "
                "their ports for an attacker.",
                "Firewall port 111 and the dynamic RPC ports from untrusted networks; "
                "disable rpcbind on NFSv4-only hosts.",
                {"program_count": len(progs)}, "nfs_scan")


def _rule_ftp(facts: list[dict]) -> Iterable[Finding]:
    """Confirmed FTP anonymous access (upgrades the port-based cleartext hint).
    Higher severity when a directory listing proved anonymous READ over cleartext;
    write access is deliberately not tested (non-destructive scan)."""
    for f in facts:
        if _scanner(f) != "ftp_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        if not d.get("anonymous_login"):
            continue
        target, port = f.get("target"), f.get("port") or 21
        read = bool(d.get("anon_read"))
        sample = [s for s in (d.get("file_sample") or []) if isinstance(s, str)][:6]
        yield Finding(
            "FTP-ANON-ACCESS",
            "FTP anonymous access permitted" + (" (directory readable)" if read else ""),
            SEV_HIGH if read else SEV_MEDIUM, CONF_HIGH, CAT_EXPOSURE, target, port, "tcp",
            "The FTP server accepted an anonymous login (USER anonymous)"
            + (f" and served a directory listing over cleartext: {', '.join(sample)}"
               if sample else "")
            + ". Data and any credentials traverse the network in cleartext; write "
            "access was NOT tested and should be verified manually.",
            "Disable anonymous FTP unless it is an intentional public read-only mirror; "
            "replace FTP with SFTP/FTPS; if kept, confine anonymous users to a read-only "
            "chroot and confirm uploads are denied.",
            {"anonymous_login": True, "anon_read": read, "software": d.get("software"),
             "file_sample": sample}, "ftp_scan")


def _rule_rsync(facts: list[dict]) -> Iterable[Finding]:
    """rsync daemon exposure. Anonymously-selectable modules are the high finding
    (their contents are pullable unauthenticated); a listable-but-auth'd module
    set is a low disclosure of what the host shares."""
    for f in facts:
        if _scanner(f) != "rsync_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 873
        anon = [m for m in (d.get("anon_modules") or []) if isinstance(m, str)]
        modules = [m for m in (d.get("modules") or []) if isinstance(m, dict)]
        if anon:
            yield Finding(
                "RSYNC-ANON-MODULES",
                f"rsync anonymous module(s) accessible ({len(anon)})",
                SEV_HIGH, CONF_HIGH, CAT_EXPOSURE, target, port, "tcp",
                "The rsync daemon exposes module(s) selectable without authentication: "
                + ", ".join(anon[:8]) + (" ..." if len(anon) > 8 else "")
                + ". Their contents can be listed and pulled by any host able to reach "
                "the daemon, in cleartext.",
                "Require authentication (auth users + a secrets file) on every module, "
                "restrict 'hosts allow' to management hosts, or disable rsync daemon mode.",
                {"anon_modules": anon}, "rsync_scan")
        elif modules:
            names = sorted({str(m.get("name")) for m in modules})
            yield Finding(
                "RSYNC-DAEMON-EXPOSED",
                f"rsync daemon module list disclosed ({len(names)})",
                SEV_LOW, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
                "The rsync daemon enumerated its module list to an unauthenticated "
                "client: " + ", ".join(names[:8]) + (" ..." if len(names) > 8 else "")
                + ". The modules require auth, but their names/comments reveal what the "
                "host shares.",
                "Firewall port 873 to management hosts; set 'list = no' to hide module "
                "names.",
                {"modules": names}, "rsync_scan")


def _rule_vnc(facts: list[dict]) -> Iterable[Finding]:
    """VNC/RFB authentication exposure. 'None' security type = unauthenticated
    remote desktop (critical); 'VNC Authentication' only = the weak DES scheme."""
    for f in facts:
        if _scanner(f) != "vnc_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 5900
        offered = [t.get("name") for t in (d.get("security_types") or []) if isinstance(t, dict)]
        if d.get("no_auth"):
            yield Finding(
                "VNC-NO-AUTH", "VNC exposed with NO authentication",
                SEV_CRITICAL, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
                "The VNC/RFB server offers the 'None' security type — the remote "
                "desktop is reachable with no password at all. Anyone able to reach "
                "this port gets full interactive control of the console.",
                "Never allow the 'None' security type; require authentication and place "
                "VNC behind a VPN/SSH tunnel with restricted source IPs.",
                {"security_types": offered}, "vnc_scan")
        elif d.get("weak_auth") and not d.get("has_strong_auth"):
            yield Finding(
                "VNC-WEAK-AUTH", "VNC using weak legacy authentication (DES)",
                SEV_MEDIUM, CONF_HIGH, CAT_WEAK_CRYPTO, target, port, "tcp",
                "The VNC/RFB server only offers 'VNC Authentication' — the legacy DES "
                "challenge/response that silently truncates passwords to 8 characters "
                "and is offline-brute-forceable.",
                "Use a VNC variant with strong auth (VeNCrypt/TLS/RA2) or tunnel VNC "
                "over SSH/VPN; enforce a strong password.",
                {"security_types": offered}, "vnc_scan")


def _rule_ipmi(facts: list[dict]) -> Iterable[Finding]:
    """IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable
    BMC is a lower exposure note (management planes should be isolated)."""
    for f in facts:
        if _scanner(f) != "ipmi_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 623
        if d.get("cipher_zero"):
            yield Finding(
                "IPMI-CIPHER-ZERO", "IPMI 2.0 cipher-zero authentication bypass",
                SEV_CRITICAL, CONF_HIGH, CAT_DEFAULT_CRED, target, port, "udp",
                "The BMC accepted an IPMI 2.0 session offering cipher suite 0 (no "
                "authentication) — an attacker can open an administrative session with "
                "NO credentials, then reset passwords and power-cycle or reimage the "
                "host (CVE-2013-4786 class).",
                "Disable cipher suite 0 (set the cipher-suite privilege for ID 0 to "
                "'no access'); isolate all IPMI/BMC interfaces on a dedicated management "
                "network; update BMC firmware.",
                {"cipher_zero": True}, "ipmi_scan")
        else:
            yield Finding(
                "IPMI-EXPOSED", "IPMI/BMC management interface reachable",
                SEV_LOW, CONF_HIGH, CAT_EXPOSURE, target, port, "udp",
                "An IPMI 2.0 BMC (lights-out management) answered from the scan vantage. "
                "BMCs run independent firmware with full hardware control and are a "
                "high-value target; they should not be reachable from general networks.",
                "Confine IPMI/BMC interfaces to an isolated, tightly-firewalled "
                "management network and keep BMC firmware patched.",
                {"rmcp_status": d.get("rmcp_status")}, "ipmi_scan")


def _rule_smtp(facts: list[dict]) -> Iterable[Finding]:
    """SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)."""
    for f in facts:
        if _scanner(f) != "smtp_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        target, port = f.get("target"), f.get("port") or 25
        vectors = []
        if d.get("vrfy_enabled"):
            vectors.append("VRFY")
        if d.get("expn_enabled"):
            vectors.append("EXPN")
        if vectors:
            yield Finding(
                "SMTP-USER-ENUM", f"SMTP user enumeration possible ({'/'.join(vectors)})",
                SEV_MEDIUM, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
                f"The SMTP server answers {' and '.join(vectors)} in a way that reveals "
                "whether a mailbox exists (VRFY returned different codes for postmaster "
                "vs a random user). An attacker can enumerate valid usernames to seed "
                "phishing and password attacks.",
                "Disable VRFY and EXPN (e.g. Postfix 'disable_vrfy_command = yes') and "
                "return a uniform response for all recipients.",
                {"vectors": vectors, "vrfy_postmaster_code": d.get("vrfy_postmaster_code"),
                 "vrfy_random_code": d.get("vrfy_random_code")}, "smtp_scan")
        if d.get("starttls") is False:
            yield Finding(
                "SMTP-NO-STARTTLS", "SMTP without STARTTLS (cleartext mail)",
                SEV_LOW, CONF_HIGH, CAT_CLEARTEXT, target, port, "tcp",
                "The SMTP server does not advertise STARTTLS — mail, and any SMTP AUTH "
                "credentials, traverse the network in cleartext and can be sniffed.",
                "Enable STARTTLS (or implicit TLS on 465) and require TLS before AUTH.",
                {"ehlo_capabilities": d.get("ehlo_capabilities")}, "smtp_scan")


def _rule_msrpc(facts: list[dict]) -> Iterable[Finding]:
    """Windows RPC endpoint-mapper disclosure — the internal RPC service map."""
    for f in facts:
        if _scanner(f) != "msrpc_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        n = int(d.get("endpoint_count") or 0)
        if n <= 0:
            continue
        target, port = f.get("target"), f.get("port") or 135
        ifaces = int(d.get("interface_count") or 0)
        named = [x for x in (d.get("named_services") or []) if isinstance(x, str)][:8]
        yield Finding(
            "MSRPC-ENDPOINTS-EXPOSED",
            f"Windows RPC endpoint mapper enumerable ({ifaces} interfaces)",
            SEV_LOW, CONF_HIGH, CAT_INFO_DISCLOSURE, target, port, "tcp",
            f"The endpoint mapper answered an ept_lookup, disclosing {n} RPC endpoint(s) "
            f"across {ifaces} interface(s)"
            + (f" (e.g. {', '.join(named)})" if named else "")
            + " — the internal RPC service map (services and their dynamic ports) an "
            "attacker uses to plan lateral movement.",
            "Firewall port 135 and the dynamic RPC port range from untrusted networks; "
            "restrict RPC to management VLANs.",
            {"endpoint_count": n, "interface_count": ifaces, "named_services": named},
            "msrpc_scan")


def _rule_printer(facts: list[dict]) -> Iterable[Finding]:
    """Exposed network printer — an information leak and an attack surface."""
    for f in facts:
        if _scanner(f) != "printer_scan" or f.get("status") != "open":
            continue
        d = _data(f)
        if not d.get("printer"):
            continue
        target, port = f.get("target"), f.get("port")
        proto = d.get("protocol") or "print"
        model = d.get("model") or ""
        yield Finding(
            "PRINTER-EXPOSED",
            "Network printer exposed" + (f" ({proto})") + (f" — {model}" if model else ""),
            SEV_LOW, CONF_HIGH, CAT_EXPOSURE, target, port, "tcp",
            f"A network printer print/management interface ({proto}) is reachable from "
            "the scan vantage"
            + (f"; the device identifies as '{model}'" if model else "")
            + ". Exposed printers allow print-job interception, stored-document / "
            "credential theft, and PJL/PostScript abuse.",
            "Restrict printer ports (9100/631/515) to print servers and management "
            "VLANs; disable unused print protocols; keep printer firmware updated.",
            {"protocol": proto, "model": model}, "printer_scan")


def _rule_os_identification(facts: list[dict]) -> Iterable[Finding]:
    """Fuse OS signals across scanners into ONE identification with calibrated
    confidence (FIX 3a). An exact NTLM build (MS-NLMP 2.2.2.10 VERSION) corroborated
    by an SMB2 Windows handshake and a known hostname is strong, multi-signal proof
    that must outrank a lone TTL guess (which stays ~0.5). Provenance in `data`."""
    agg: dict[str, dict] = {}
    for f in facts:
        t = f.get("target")
        if not t:
            continue
        d = _data(f)
        a = agg.setdefault(t, {})
        sc = _scanner(f)
        if sc == "smb_scan":
            if d.get("smb2_supported"):
                a["smb2"] = True
            if d.get("os_build"):
                a["build"] = d.get("os_build")
                a["release"] = d.get("os_release")
            if d.get("target_name"):
                a.setdefault("hostname", d["target_name"])
        elif sc == "os_fingerprint":
            if d.get("os_guess") and d.get("os_guess") != "unknown":
                a.setdefault("family", d["os_guess"])
                a.setdefault("ttl_conf", d.get("confidence") or 0.5)
            if d.get("stack_guess"):
                a.setdefault("stack", d["stack_guess"])
        elif sc == "msrpc_scan" and d.get("interface_count"):
            a["rpc_windows"] = True

    for t, a in agg.items():
        # Confidence is driven by how many INDEPENDENT signals corroborate: build +
        # SMB2 + hostname is near-certain; build alone strong; stack (p0f) medium;
        # a bare TTL family stays a hint. Never fabricate above the evidence.
        if a.get("build") and a.get("smb2") and a.get("hostname"):
            conf, release, method = 0.97, a.get("release") or "Windows", "smb2_ntlm_version+smb2+hostname"
        elif a.get("build"):
            conf, release, method = 0.90, a.get("release") or "Windows", "smb2_ntlm_version"
        elif a.get("smb2") and a.get("stack"):
            conf, release, method = 0.80, a.get("stack"), "smb2+p0f_stack"
        elif a.get("family"):
            conf, release, method = float(a.get("ttl_conf") or 0.5), a["family"], "ttl_only"
        else:
            continue
        present = [k for k in ("build", "smb2", "hostname", "stack", "family") if a.get(k)]
        yield Finding(
            "ASSET-OS-IDENTIFIED", f"OS identified: {release}",
            SEV_INFO,
            CONF_HIGH if conf >= 0.95 else CONF_MEDIUM if conf >= 0.8 else CONF_LOW,
            CAT_INFO_DISCLOSURE, t, None, None,
            (f"OS identified as {release} (confidence {conf:.2f}) by fusing "
             f"{len(present)} signal(s): {', '.join(present)} [method: {method}]."),
            "Informational — asset inventory and patch-level tracking.",
            {"os_release": release, "os_build": a.get("build"),
             "hostname": a.get("hostname"), "confidence": conf, "method": method,
             "stack": a.get("stack")}, "os_fusion")


_RULES: list[Callable[[list[dict]], Iterable[Finding]]] = [
    _rule_tls, _rule_smb, _rule_snmp, _rule_udp_amplification, _rule_rdp,
    _rule_cleartext_and_exposure, _rule_web, _rule_tls_fingerprint, _rule_unauth_access,
    _rule_tls_server_fingerprint, _rule_ssh, _rule_smb_enum, _rule_ldap, _rule_dns,
    _rule_nfs, _rule_ftp, _rule_rsync, _rule_vnc, _rule_ipmi, _rule_smtp, _rule_msrpc,
    _rule_printer, _rule_os_identification,
]


# ── correlation layer ───────────────────────────────────────────────────────
# Composite findings derived from the BASE findings on the same host. Correlation
# is what separates a good scanner from a great one: an attacker chains weaknesses,
# so the scanner should surface the *path*, not just the parts. Pure over base
# findings; every composite cites the findings it was built from.
def _by_target(findings: list[Finding]) -> dict:
    out: dict = {}
    for f in findings:
        out.setdefault(f.target, []).append(f)
    return out


def _corr_ntlm_relay(facts: list[dict], base: list[Finding]) -> Iterable[Finding]:
    """SMB signing not required => a viable NTLM relay target. If SMBv1 is also on,
    the host is both coercible and relayable — a concrete takeover path."""
    for target, fs in _by_target(base).items():
        by_id = {f.rule_id: f for f in fs}
        if "SMB-SIGNING-NOT-REQUIRED" not in by_id:
            continue
        smbv1 = "SMB-V1-ENABLED" in by_id
        used = sorted(set(by_id) & {"SMB-SIGNING-NOT-REQUIRED", "SMB-V1-ENABLED"})
        port = by_id["SMB-SIGNING-NOT-REQUIRED"].port or 445
        reason = ("SMB signing is not required AND SMBv1 is enabled — the host is both "
                  "coercible and relayable: an attacker can coerce authentication and relay "
                  "it to take over the host."
                  if smbv1 else
                  "SMB signing is not required — the host is a viable NTLM relay target.")
        yield Finding(
            "CORR-NTLM-RELAY-PATH", "NTLM relay attack path (SMB signing not required)",
            SEV_HIGH if smbv1 else SEV_MEDIUM, CONF_HIGH, CAT_MISCONFIG, target, port, "tcp",
            f"{reason} [correlated: {', '.join(used)}]",
            "Require SMB signing on all hosts (especially DCs); disable SMBv1; enforce LDAP/EPA signing.",
            {"correlated_findings": used, "smbv1": smbv1}, "correlation")


def _corr_legacy_windows(facts: list[dict], base: list[Finding]) -> Iterable[Finding]:
    """SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the
    classic ransomware entry combination."""
    for target, fs in _by_target(base).items():
        ids = {f.rule_id for f in fs}
        if "SMB-V1-ENABLED" in ids and "SVC-RDP-EXPOSED" in ids:
            yield Finding(
                "CORR-LEGACY-WINDOWS-SURFACE",
                "Legacy Windows attack surface (SMBv1 + exposed RDP)",
                SEV_HIGH, CONF_MEDIUM, CAT_EXPOSURE, target, None, None,
                "SMBv1 is enabled (wormable, EternalBlue class) AND RDP is exposed "
                "(brute-force / BlueKeep) on the same host — a classic ransomware entry path. "
                "[correlated: SMB-V1-ENABLED, SVC-RDP-EXPOSED]",
                "Disable SMBv1; restrict RDP to VPN/jump hosts with NLA + MFA.",
                {"correlated_findings": ["SMB-V1-ENABLED", "SVC-RDP-EXPOSED"]}, "correlation")


def _corr_cleartext_cluster(facts: list[dict], base: list[Finding]) -> Iterable[Finding]:
    """Two or more cleartext services on one host — any sniffing position harvests
    credentials across all of them."""
    for target, fs in _by_target(base).items():
        ct_ids = sorted({f.rule_id for f in fs if f.category == CAT_CLEARTEXT})
        if len(ct_ids) >= 2:
            yield Finding(
                "CORR-CLEARTEXT-CLUSTER",
                "Multiple cleartext services (credential-capture risk)",
                SEV_MEDIUM, CONF_HIGH, CAT_CLEARTEXT, target, None, None,
                f"Multiple cleartext protocols exposed on one host ({', '.join(ct_ids)}) — "
                "a single sniffing position captures credentials across services. "
                f"[correlated: {', '.join(ct_ids)}]",
                "Replace cleartext services with encrypted equivalents (SSH / FTPS / HTTPS).",
                {"correlated_findings": ct_ids}, "correlation")


# Enterprise Tier-1 attack-path correlations built from the anonymous-access,
# console-exposure and user-disclosure capabilities.
_ANON_EXPOSURE_IDS = {
    "NFS-EXPORT-WORLD-READABLE", "FTP-ANON-ACCESS", "RSYNC-ANON-MODULES",
    "SMB-NULL-SESSION", "LDAP-ANON-SEARCH", "SVC-UNAUTH-DATASTORE-ACCESS",
}
_WEAK_AUTH_SURFACE_IDS = {"SVC-RDP-EXPOSED", "SVC-RDP-NO-NLA", "VNC-WEAK-AUTH", "VNC-NO-AUTH"}
_MGMT_PLANE_IDS = {"IPMI-CIPHER-ZERO", "IPMI-EXPOSED", "VNC-NO-AUTH", "VNC-WEAK-AUTH", "SVC-RDP-EXPOSED"}


def _corr_anon_data_exposure(facts: list[dict], base: list[Finding]) -> Iterable[Finding]:
    """Two or more INDEPENDENT anonymous data-exposure channels on one host — the
    host leaks data by several paths; closing one does not remediate the rest."""
    for target, fs in _by_target(base).items():
        hits = sorted({f.rule_id for f in fs if f.rule_id in _ANON_EXPOSURE_IDS})
        if len(hits) >= 2:
            yield Finding(
                "CORR-ANON-DATA-EXPOSURE",
                "Multiple anonymous data-exposure channels on one host",
                SEV_HIGH, CONF_HIGH, CAT_EXPOSURE, target, None, None,
                f"This host exposes data through {len(hits)} independent anonymous "
                f"channels ({', '.join(hits)}) — an unauthenticated attacker can read "
                "data by several paths, and remediating one leaves the others open. "
                f"[correlated: {', '.join(hits)}]",
                "Treat this host as leaking data: require authentication on every listed "
                "service and re-scan to confirm.",
                {"correlated_findings": hits}, "correlation")


def _corr_user_enum_plus_weak_auth(facts: list[dict], base: list[Finding]) -> Iterable[Finding]:
    """A disclosed user list (SMB null session) plus a weak/exposed login surface on
    the same host — the two combine into a ready-made credential-attack path."""
    for target, fs in _by_target(base).items():
        ids = {f.rule_id for f in fs}
        if "SMB-NULL-SESSION-USERS" not in ids:
            continue
        weak = sorted(ids & _WEAK_AUTH_SURFACE_IDS)
        if weak:
            used = ["SMB-NULL-SESSION-USERS"] + weak
            yield Finding(
                "CORR-USER-ENUM-PLUS-WEAK-AUTH",
                "Enumerated users + a weak/exposed authentication surface",
                SEV_HIGH, CONF_MEDIUM, CAT_MISCONFIG, target, None, None,
                "The host discloses a valid user list (SMB null session) AND exposes a "
                f"weak or unauthenticated login surface ({', '.join(weak)}) — together a "
                "ready-made credential-attack path (known usernames against a "
                f"brute-forceable service). [correlated: {', '.join(used)}]",
                "Disable anonymous SAMR/LSA enumeration and remediate the login surface; "
                "enforce MFA and account lockout.",
                {"correlated_findings": used}, "correlation")


def _corr_mgmt_plane_exposed(facts: list[dict], base: list[Finding]) -> Iterable[Finding]:
    """Out-of-band / console management surfaces reachable on one host — these grant
    hardware- or session-level control and belong on an isolated network."""
    for target, fs in _by_target(base).items():
        ids = {f.rule_id for f in fs}
        hits = sorted(ids & _MGMT_PLANE_IDS)
        critical = "IPMI-CIPHER-ZERO" in ids or "VNC-NO-AUTH" in ids
        if "IPMI-CIPHER-ZERO" in ids or len(hits) >= 2:
            yield Finding(
                "CORR-MGMT-PLANE-EXPOSED", "Console/management plane exposed",
                SEV_HIGH if critical else SEV_MEDIUM, CONF_MEDIUM, CAT_EXPOSURE,
                target, None, None,
                f"Out-of-band / console management surfaces are reachable on this host "
                f"({', '.join(hits)}) — they grant hardware- or session-level control and "
                f"belong on an isolated management network. [correlated: {', '.join(hits)}]",
                "Move IPMI/BMC, VNC and RDP management onto an isolated, firewalled "
                "management VLAN; require strong authentication and MFA.",
                {"correlated_findings": hits}, "correlation")


_CORRELATION_RULES: list[Callable[[list[dict], list[Finding]], Iterable[Finding]]] = [
    _corr_ntlm_relay, _corr_legacy_windows, _corr_cleartext_cluster,
    _corr_anon_data_exposure, _corr_user_enum_plus_weak_auth, _corr_mgmt_plane_exposed,
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
    # Correlation pass: composite findings derived from the base findings.
    base = list(seen.values())
    for corr in _CORRELATION_RULES:
        for finding in corr(norm, base):
            key = (finding.rule_id, finding.target, finding.port)
            if key not in seen:
                seen[key] = finding
    return sorted(
        seen.values(),
        key=lambda x: (_SEV_ORDER.get(x.severity, 0), x.target or "", x.port or 0),
        reverse=True,
    )


# Severity ordering for ranking the finding section (worst first).
_SEV_RANK = {SEV_CRITICAL: 4, SEV_HIGH: 3, SEV_MEDIUM: 2, SEV_LOW: 1, SEV_INFO: 0}
# Confidence tie-break so a confirmed finding outranks a same-severity hint.
_CONF_RANK = {CONF_HIGH: 2, CONF_MEDIUM: 1, CONF_LOW: 0}


def _finding_row(f: Finding) -> dict[str, Any]:
    """One finding as the finding-section shows it — the ACTUAL vulnerability, with
    where it came from and whether that source is verified (trusted)."""
    from .scanner_registry import is_verified
    src = f.source_scanner
    return {
        "rule_id": f.rule_id,
        "title": f.title,
        "severity": f.severity,
        "confidence": f.confidence,
        "category": f.category,
        "target": f.target,
        "port": f.port,
        "evidence": f.evidence,
        "recommendation": f.recommendation,
        "source_scanner": src,
        # Trust provenance: a finding from a verified scanner is authoritative; one
        # from an experimental scanner is shown but flagged provisional.
        "verified": is_verified(src),
    }


def summarize(findings: list[Finding], *, top: int = 50) -> dict[str, Any]:
    """Roll up findings for the finding section.

    Beyond counts, this returns the ACTUAL ranked vulnerabilities (`findings`) —
    worst-first, each tagged with its source scanner and whether that source is
    verified — so the report SHOWS what was found, not just how many. Honest by
    construction: if nothing was detected the list is empty; nothing is invented.
    """
    counts = {s: 0 for s in (SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW, SEV_INFO)}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    ranked = sorted(
        findings,
        key=lambda f: (_SEV_RANK.get(f.severity, 0), _CONF_RANK.get(f.confidence, 0)),
        reverse=True)
    rows = [_finding_row(f) for f in ranked]
    verified_rows = [r for r in rows if r["verified"]]

    return {
        "total": len(findings),
        "by_severity": counts,
        "by_category": _tally(findings, lambda x: x.category),
        "actionable": sum(1 for f in findings if f.severity in (SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM)),
        # The finding section itself — the real vulnerabilities, worst first.
        "findings": rows[:top],
        "verified_count": len(verified_rows),
        "experimental_count": len(rows) - len(verified_rows),
        "has_findings": bool(rows),
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
