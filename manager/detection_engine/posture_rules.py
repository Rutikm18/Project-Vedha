"""
posture_rules.py — the manager's POSTURE/CONFIG detection engine (detection-as-code).

The CVE track (normalize→match→enrich) answers "does this host run a version with a
known CVE?". It cannot answer the OTHER half of a real VA: "is this service
MISCONFIGURED or EXPOSED in a way that is exploitable regardless of version?" —
SMBv1 enabled, SMB signing off (NTLM relay), RDP without NLA (pre-auth attack
surface), deprecated TLS, an open UDP amplifier, an anonymous RPC endpoint map.
Those are *direct protocol observations*, not version inferences, so a validated
scanner that completed the real handshake is AUTHORITATIVE for them — the finding is
CONFIRMED, not "suspected".

DESIGN (mirrors the CVE engine's discipline):
  * Every rule is data, not code sprinkled through the pipeline: id, title,
    severity, CWE, MITRE ATT&CK technique, category, the scanners whose facts it
    reads, a pure `detect(fact)->evidence|None`, remediation, and known-FP notes.
  * TRUST TIER: VALIDATED_SCANNERS (proven accurate against ground truth) produce
    CONFIRMED posture findings; anything else stays SUSPECTED. This is the posture
    analogue of matcher.py's `source_confidence == authoritative` gate — and it is
    what makes "run the trusted scanners on priority, trust their output" real.
  * Risk is severity shaped by EXPOSURE (auth in front sharply lowers it; unauth +
    reachable raises it) and by finding STATE, then mapped to the same
    critical/high/medium/low priority the CVE enrichment uses — so a unified,
    explainable ordering spans both tracks.
  * Structural anti-FP: no evidence, no finding (Finding-model invariant, reused).
"""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from models import Asset, Fact, FindingState

# ── trust tier ────────────────────────────────────────────────────────────────
# Scanners validated against ground truth (DESKTOP-34M18MB / 192.168.1.77) whose
# DIRECT protocol observations are authoritative for posture. A finding these raise
# is CONFIRMED; the same shape from an unvalidated scanner is only SUSPECTED. Keep
# this list curated and reviewed — it is governed data, like an allowlist.
VALIDATED_SCANNERS: frozenset = frozenset({
    "port_scan", "syn_scan", "mass_scan",   # port_scanner (open-port set)
    "smb_scan",                              # SMB posture + NTLM build + dialect
    "rdp_scan",                              # NLA / TLS / nla_required
    "tls_scan",                              # cert + JA4X
    "msrpc_scan",                            # endpoint-map enumeration
    "host_discovery",                        # liveness
    "rpc_reconcile",                         # advertised-vs-reachable
    "udp_scan",                              # honest UDP labeling
    "os_fingerprint",                        # os_fusion (build-backed)
    "service_banner",                        # banner grab (honest 'no banner')
    "printer_scan",                          # real PJL handshake confirm
})


def is_validated(scanner: str) -> bool:
    return scanner in VALIDATED_SCANNERS


# ── risk model ────────────────────────────────────────────────────────────────
_SEV_BASE = {"critical": 90, "high": 70, "medium": 45, "low": 20, "info": 5}
_STATE_FACTOR = {"confirmed": 1.0, "suspected": 0.8, "potential": 0.6}
_STATE_CONF = {"confirmed": 90, "suspected": 65, "potential": 45}


def compute_risk(severity: str, state: str,
                 internet_facing: Optional[bool],
                 auth_enforced: Optional[bool]) -> tuple[int, str]:
    """severity × exposure × state → (risk_score 0-100, priority).

    Authentication ENFORCED in front of the service (e.g. RDP NLA required) is the
    single biggest de-escalator — the weakness is not reachable pre-auth. An
    internet-facing service with NO auth is the biggest escalator. Priority uses the
    same buckets as the CVE enrichment so both tracks sort together.
    """
    base = _SEV_BASE.get(severity, 20)
    if auth_enforced is True:
        base = max(5, base - 25)                      # not reachable pre-auth
    elif internet_facing is True:
        base = min(100, base + 10)                    # unauth + internet-facing
    score = round(base * _STATE_FACTOR.get(state, 0.8))
    score = max(1, min(100, score))
    if score >= 80:
        pri = "critical"
    elif score >= 60:
        pri = "high"
    elif score >= 35:
        pri = "medium"
    else:
        pri = "low"
    return score, pri


def make_posture_id(asset_ip: str, rule_id: str, port: Optional[int]) -> str:
    """Deterministic id — same (asset, rule, port) always hashes the same, so
    re-scan delta can track a posture finding across runs (like make_finding_id)."""
    raw = f"{asset_ip}|{rule_id}|{port}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class PostureFinding:
    finding_id: str
    asset_ip: str
    rule_id: str
    title: str
    category: str
    severity: str
    state: str                 # confirmed | suspected | potential
    confidence: int            # 0-100
    cwe: str
    mitre: str                 # ATT&CK technique id
    port: Optional[int]
    proto: Optional[str]
    evidence_refs: list[str]
    evidence: dict
    remediation: str
    fp_notes: str
    internet_facing: Optional[bool]
    auth_enforced: Optional[bool]
    risk_score: int
    priority: str
    created_at: str
    scanner: str

    def __post_init__(self) -> None:
        if not self.evidence_refs:                    # no evidence, no finding
            raise ValueError(f"posture finding {self.rule_id} on {self.asset_ip} "
                             f"has zero evidence_refs")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PostureRule:
    rule_id: str
    title: str
    severity: str
    cwe: str
    mitre: str
    category: str
    scanners: tuple
    detect: Callable[[Fact], Optional[dict]]
    remediation: str
    fp_notes: str = ""
    # auth_enforced(fact) -> True/False/None; overrides the exposure map per-fact.
    auth_enforced: Optional[Callable[[Fact], Optional[bool]]] = None


# ── detectors (pure: Fact -> evidence dict | None) ────────────────────────────
_WEAK_TLS = {"SSLV3", "SSL3", "TLSV1", "TLSV1.0", "TLSV1.1"}
_AMPLIFIERS = {"ntp", "dns", "ssdp", "memcached", "chargen", "snmp", "ldap", "netbios"}
_DEFAULT_COMMUNITIES = {"public", "private"}


def _d(f: Fact) -> dict:
    return f.data if isinstance(f.data, dict) else {}


def _smbv1(f: Fact) -> Optional[dict]:
    return {"negotiated": "SMBv1"} if _d(f).get("smbv1_enabled") is True else None


def _smb_signing(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("smb2_supported") is True and d.get("signing_required") is False:
        return {"dialect": d.get("negotiated_dialect")}
    return None


def _rdp_no_nla(f: Fact) -> Optional[dict]:
    d = _d(f)
    if (d.get("rdp_confirmed") is True and d.get("nla") is False
            and d.get("negotiation") != "failure" and d.get("nla_required") is not True):
        return {"selected_protocol": d.get("selected_protocol")}
    return None


def _rdp_exposed(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("rdp_confirmed") is True:
        return {"security": "NLA" if d.get("nla") else "TLS" if d.get("tls") else "standard-rdp",
                "nla_required": d.get("nla_required")}
    return None


def _rdp_auth(f: Fact) -> Optional[bool]:
    d = _d(f)
    if d.get("nla_required") is True:
        return True
    if d.get("nla") is False:
        return False
    return None


def _cert(f: Fact) -> dict:
    c = _d(f).get("certificate")
    return c if isinstance(c, dict) else {}


def _tls_version(f: Fact) -> Optional[dict]:
    acc = [str(v).upper().replace(" ", "") for v in (_d(f).get("accepted_versions") or [])]
    bad = sorted(set(acc) & _WEAK_TLS)
    return {"deprecated_versions": bad} if bad else None


def _tls_cipher(f: Fact) -> Optional[dict]:
    weak = [c for c in (_d(f).get("cipher_analysis") or [])
            if isinstance(c, dict) and c.get("weak")]
    if weak:
        return {"weak_ciphers": [c.get("cipher") for c in weak][:8]}
    return None


def _tls_self_signed(f: Fact) -> Optional[dict]:
    c = _cert(f)
    return {"subject": c.get("subject")} if c.get("self_signed") else None


def _tls_expired(f: Fact) -> Optional[dict]:
    c = _cert(f)
    return {"issuer": c.get("issuer")} if c.get("expired") else None


def _msrpc_exposed(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("msrpc") is True and (d.get("endpoint_count") or 0) > 0:
        return {"endpoint_count": d.get("endpoint_count"),
                "dynamic_tcp_ports": d.get("dynamic_tcp_ports")}
    return None


def _udp_amplifier(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("monlist_enabled") is True:
        return {"service": "ntp", "monlist_enabled": True}
    if d.get("open_recursion") is True:
        return {"service": "dns", "open_resolver": True}
    svc = str(d.get("service") or "").lower()
    if d.get("responded") is True and svc in _AMPLIFIERS and f.status == "open":
        return {"service": svc}
    return None


def _snmp_default(f: Fact) -> Optional[dict]:
    c = _d(f).get("community")
    return {"community": c} if c in _DEFAULT_COMMUNITIES else None


# ── the rule pack ─────────────────────────────────────────────────────────────
RULES: list[PostureRule] = [
    PostureRule(
        "POSTURE-SMB-V1-ENABLED", "SMBv1 enabled (wormable, deprecated)",
        "critical", "CWE-477", "T1210", "misconfiguration", ("smb_scan",), _smbv1,
        "Disable SMBv1 (Windows: Remove-WindowsFeature FS-SMB1). SMBv1 is the "
        "EternalBlue/WannaCry transport and has no safe use in 2020+.",
        fp_notes="Requires a SUCCESSFUL SMBv1 negotiate — a filtered/negative "
                 "negotiate does not fire this."),
    PostureRule(
        "POSTURE-SMB-SIGNING-OFF", "SMB signing not required (NTLM-relay exposure)",
        "high", "CWE-306", "T1557.001", "misconfiguration", ("smb_scan",), _smb_signing,
        "Require SMB signing (GPO: 'Microsoft network server: Digitally sign "
        "communications (always)') to defeat SMB/NTLM relay.",
        fp_notes="signing_required is read from a successful SMB2 negotiate; only "
                 "fires when SMB2 is up and required=False."),
    PostureRule(
        "POSTURE-RDP-NO-NLA", "RDP without Network Level Authentication",
        "high", "CWE-287", "T1210", "misconfiguration", ("rdp_scan",), _rdp_no_nla,
        "Require NLA (CredSSP) on RDP so the RDP stack is not reachable pre-auth; "
        "patch legacy hosts; restrict RDP to VPN/jump hosts.",
        fp_notes="Suppressed when the RDP-only probe was refused (nla_required=True) "
                 "— a CONFIRMED-NLA host never reaches this rule.",
        auth_enforced=_rdp_auth),
    PostureRule(
        "POSTURE-RDP-EXPOSED", "RDP reachable from the scan vantage (confirmed)",
        "low", "CWE-284", "T1021.001", "exposure", ("rdp_scan",), _rdp_exposed,
        "Restrict RDP to VPN/jump hosts and enforce NLA + MFA.",
        fp_notes="Informational when NLA is required; risk escalates automatically "
                 "when auth is not enforced.",
        auth_enforced=_rdp_auth),
    PostureRule(
        "POSTURE-TLS-DEPRECATED-VERSION", "Deprecated TLS/SSL version accepted",
        "high", "CWE-326", "T1040", "weak_crypto", ("tls_scan",), _tls_version,
        "Disable SSLv3/TLS1.0/TLS1.1; require TLS 1.2+ (ideally 1.3).",
        fp_notes="Fires only on versions the server ACCEPTED in a real handshake."),
    PostureRule(
        "POSTURE-TLS-WEAK-CIPHER", "Weak TLS cipher suite offered",
        "medium", "CWE-327", "T1040", "weak_crypto", ("tls_scan",), _tls_cipher,
        "Remove NULL/EXPORT/RC4/DES/3DES/anon cipher suites; prefer AEAD (GCM/"
        "ChaCha20).",
        fp_notes="Keyed off the scanner's own cipher_analysis 'weak' flag."),
    PostureRule(
        "POSTURE-TLS-SELF-SIGNED", "Self-signed TLS certificate",
        "medium", "CWE-295", "T1557", "weak_crypto", ("tls_scan",), _tls_self_signed,
        "Replace with a certificate from a trusted CA; enable strict validation on "
        "clients.",
        fp_notes="Internal PKI roots also present as self-signed — verify against "
                 "the org's trusted roots before treating as a defect."),
    PostureRule(
        "POSTURE-TLS-EXPIRED-CERT", "Expired TLS certificate",
        "medium", "CWE-298", "T1557", "weak_crypto", ("tls_scan",), _tls_expired,
        "Renew the certificate and automate renewal (ACME) to prevent recurrence."),
    PostureRule(
        "POSTURE-MSRPC-EPMAP-EXPOSED", "MSRPC endpoint mapper enumerable (anonymous)",
        "medium", "CWE-200", "T1135", "information_disclosure", ("msrpc_scan",),
        _msrpc_exposed,
        "Firewall TCP/135 and the dynamic RPC range from untrusted zones; the "
        "endpoint map discloses running services and their dynamic ports.",
        fp_notes="Expected inside a Windows domain LAN; treat as a finding at trust "
                 "boundaries / perimeter."),
    PostureRule(
        "POSTURE-UDP-AMPLIFIER", "UDP amplification service exposed",
        "medium", "CWE-406", "T1498.002", "amplification", ("udp_scan",), _udp_amplifier,
        "Restrict the service to trusted networks; disable monlist / open recursion; "
        "enable response-rate limiting.",
        fp_notes="Only fires when the service actually ANSWERED (responded=True) — "
                 "no-reply / open|filtered never triggers it."),
    PostureRule(
        "POSTURE-SNMP-DEFAULT-COMMUNITY", "SNMP default community string",
        "high", "CWE-1392", "T1078", "default_credentials", ("snmp_scan",), _snmp_default,
        "Change the community string; move to SNMPv3 with auth+priv; restrict by ACL.",
        fp_notes="snmp_scan is not in the validated trust tier yet, so this is "
                 "reported SUSPECTED pending validation."),
]


# ── runner ────────────────────────────────────────────────────────────────────
def _state_for(scanner: str) -> str:
    return (FindingState.confirmed.value if is_validated(scanner)
            else FindingState.suspected.value)


def _evidence_ref(f: Fact) -> str:
    if f.source_file:
        return f"{f.source_file}:{f.source_line}"
    return f"{f.scanner}:{f.target}:{f.port}"


def detect_posture(asset: Asset,
                   exposure: dict[str, dict] | None = None) -> list[PostureFinding]:
    """Apply every posture rule to one asset's facts. Deduplicates by
    (rule_id, port) — the same weakness seen twice is one finding."""
    exposure = exposure or {}
    exp = exposure.get(asset.ip, {})
    internet_facing = exp.get("internet_facing")
    default_auth = exp.get("auth_enforced")

    out: list[PostureFinding] = []
    seen: set[tuple] = set()
    now = datetime.now(timezone.utc).isoformat()

    for f in asset.facts:
        for rule in RULES:
            if f.scanner not in rule.scanners:
                continue
            ev = rule.detect(f)
            if not ev:
                continue
            key = (rule.rule_id, f.port)
            if key in seen:
                continue
            seen.add(key)

            state = _state_for(f.scanner)
            auth = (rule.auth_enforced(f) if rule.auth_enforced else None)
            if auth is None:
                auth = default_auth
            risk, priority = compute_risk(rule.severity, state, internet_facing, auth)
            out.append(PostureFinding(
                finding_id=make_posture_id(asset.ip, rule.rule_id, f.port),
                asset_ip=asset.ip, rule_id=rule.rule_id, title=rule.title,
                category=rule.category, severity=rule.severity, state=state,
                confidence=_STATE_CONF.get(state, 65), cwe=rule.cwe, mitre=rule.mitre,
                port=f.port, proto=f.proto, evidence_refs=[_evidence_ref(f)],
                evidence=ev, remediation=rule.remediation, fp_notes=rule.fp_notes,
                internet_facing=internet_facing, auth_enforced=auth,
                risk_score=risk, priority=priority, created_at=now, scanner=f.scanner))
    return out


def detect_all(assets: dict[str, Asset] | Any,
               exposure: dict[str, dict] | None = None) -> list[PostureFinding]:
    """Run posture detection across every asset. Accepts an IngestResult (uses its
    .assets) or a plain {ip: Asset} mapping."""
    mapping = getattr(assets, "assets", assets)
    findings: list[PostureFinding] = []
    for asset in mapping.values():
        findings.extend(detect_posture(asset, exposure))
    findings.sort(key=lambda x: (-x.risk_score, x.asset_ip, x.rule_id))
    return findings
