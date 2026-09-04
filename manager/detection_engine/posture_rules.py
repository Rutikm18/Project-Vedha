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


# ── fact-path resolution: absent key ≠ collected null ─────────────────────────
# The single most important distinction in this file. `d.get("smbv1_enabled")`
# returns None whether the probe collected `false` (genuinely clean) OR never
# emitted the key at all (agent-side drift → a SILENT false-negative). Conflating
# those is how "the scripts catch it but the manager doesn't" happens with no trace.
# `_MISSING` is returned ONLY for an absent key; a collected `None`/`False` is real
# data and returns itself.
_MISSING = object()


def get_path(data: Any, dotted: str) -> Any:
    """Resolve `a.b.c` inside a Fact.data dict. Returns `_MISSING` (never None)
    when any segment is absent, so callers can tell 'not collected' from 'collected
    as null/false'."""
    cur = data
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return _MISSING
    return cur


# ── detection trace: every rule evaluation records an OUTCOME, not just matches ─
# A non-finding must explain itself. These are the six mutually-exclusive outcomes
# of evaluating one rule against one fact (or, for NO_EVIDENCE, against an asset the
# rule's scanner never covered).
OUTCOME_MATCH = "match"                  # fired → finding
OUTCOME_NO_MATCH = "no_match"            # evaluated, predicate false → genuinely clean
OUTCOME_NO_EVIDENCE = "no_evidence"      # the rule's scanner never ran for this asset
OUTCOME_MISSING_INPUT = "missing_input"  # facts present, a declared `requires` path absent → DRIFT
OUTCOME_UNPARSEABLE = "unparseable"      # a declared path is present but the wrong shape
OUTCOME_ERROR = "error"                  # the detector raised

# Scanner ran but the rule still couldn't be assessed. These are DEFECTS and must
# degrade a campaign's verdict — they are exactly the silent false-clean class.
BLIND_OUTCOMES = frozenset({OUTCOME_MISSING_INPUT, OUTCOME_UNPARSEABLE, OUTCOME_ERROR})
# Scanner was never run. A coverage fact, reported but not a defect.
UNASSESSED_OUTCOMES = frozenset({OUTCOME_NO_EVIDENCE})
_ALL_OUTCOMES = (BLIND_OUTCOMES | UNASSESSED_OUTCOMES
                 | {OUTCOME_MATCH, OUTCOME_NO_MATCH})

# Per-rule verdicts — the roll-up an operator reads to answer "why no finding?"
VERDICT_FINDING = "finding_exists"
VERDICT_CLEAN = "evaluated_clean"
VERDICT_SCHEMA_DRIFT = "schema_drift"
VERDICT_NO_EVIDENCE = "no_evidence_collected"
VERDICT_RULE_ERROR = "rule_error"


@dataclass
class TraceRow:
    """One rule evaluation's outcome. Purely diagnostic — never gates a finding."""
    rule_id: str
    scanner: str
    outcome: str
    asset_ip: str
    port: Optional[int] = None
    reason: Optional[str] = None
    evidence: Optional[dict] = None      # set only on OUTCOME_MATCH

    def to_dict(self) -> dict[str, Any]:
        return {"rule_id": self.rule_id, "scanner": self.scanner,
                "outcome": self.outcome, "asset_ip": self.asset_ip,
                "port": self.port, "reason": self.reason}


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
    # Real-world exploitation evidence (exploitability.py). `kev_refs` names the
    # CVEs this weakness is a documented precondition for and HOW it relates —
    # never a claim that the CVE is present on the host.
    kev_refs: list = field(default_factory=list)
    epss_max: Optional[float] = None
    exploitability: str = "unknown"
    notes: list = field(default_factory=list)
    # Auditable confidence calibration (set by posture_confidence.calibrate_host_findings
    # in a second pass): base tier, cross-signal chain corroboration, downgrades. The
    # `confidence` field above is the calibrated result; this explains how it got there.
    precision_factors: dict = field(default_factory=dict)

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
    # The fact.data paths this detector reads. This is a MACHINE-CHECKABLE CONTRACT
    # between the probe's emitters and this rule: if the probe collected facts for
    # this rule's scanner but a `requires` path is absent, the rule reports
    # MISSING_INPUT (drift) instead of silently looking clean. Declare the minimal
    # set of paths that gate assessability — for rules with OR-alternative inputs,
    # leave it empty rather than declare a path that isn't always required.
    requires: tuple[str, ...] = ()


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
    """Fires on EITHER of the rdp_scanner's two independent probes.

    The scanner probes twice: (A) request SSL|HYBRID|HYBRID_EX and read the
    selected protocol, and (B) request bare PROTOCOL_RDP to learn whether the
    server will accept a session with no NLA at all. Probe B sets
    `nla_required=False` only when the server ANSWERED a standard-RDP request —
    direct proof that NLA is not enforced, and stronger evidence than A's
    selected-protocol bitmask.

    Reading only A was a real false negative, found on a live Windows 11 host:
    A came back RDP_NEG_FAILURE (SSL_NOT_ALLOWED_BY_SERVER), so no `nla` key was
    emitted at all and the rule went silent — while B had already proved the host
    accepts a bare, unauthenticated-at-network-level RDP session.
    """
    d = _d(f)
    if d.get("rdp_confirmed") is not True or d.get("nla_required") is True:
        return None
    # Probe B: the server accepted a bare standard-RDP session.
    if d.get("nla_required") is False:
        return {"proof": "server accepted a standard-RDP (no-NLA) connection request",
                "nla_required": False,
                "standard_rdp_security": d.get("standard_rdp_security"),
                "selected_protocol": d.get("selected_protocol")}
    # Probe A: negotiation completed and selected a protocol without CredSSP.
    if d.get("nla") is False and d.get("negotiation") != "failure":
        return {"proof": "negotiated protocol does not include CredSSP/NLA",
                "selected_protocol": d.get("selected_protocol")}
    return None


# MS-RDPBCGR 2.2.1.2.2 failureCode. Only codes that carry POSTURE meaning are
# interpreted; the rest are transport/configuration noise and stay unreported.
_RDP_NEG_FAILURE = {
    2: ("SSL_NOT_ALLOWED_BY_SERVER",
        "the server is configured not to use TLS for RDP"),
    3: ("SSL_CERT_NOT_ON_SERVER",
        "the server has no valid certificate, so TLS cannot be used"),
}


def _rdp_no_tls(f: Fact) -> Optional[dict]:
    """The server REFUSED a TLS-capable negotiation, so the session falls back to
    legacy standard-RDP security (RC4-family, no server authentication → MITM).
    Read straight off the negotiation failure code, which the manager previously
    ignored entirely even though the probe records it."""
    d = _d(f)
    if d.get("rdp_confirmed") is not True or d.get("negotiation") != "failure":
        return None
    code = d.get("failure_code")
    named = _RDP_NEG_FAILURE.get(code)
    if named is None:
        return None
    return {"failure_code": code, "failure": named[0], "meaning": named[1]}


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
    # Protocol labels reach us in two spellings: the dotted "TLSv1.0" that
    # ssl.version() and the probe's cipher_by_version use, and the underscored
    # "TLSv1_0" that tls_scanner's own probe list emits into accepted_versions
    # (they are ssl.TLSVersion member names). Normalising the separator is what
    # makes this rule fire on real scanner output — matching only the dotted form
    # silently missed every legacy-TLS server, and would keep missing the facts
    # already stored in that spelling.
    acc = [str(v).upper().replace(" ", "").replace("_", ".")
           for v in (_d(f).get("accepted_versions") or [])]
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


# ── service-layer detectors ───────────────────────────────────────────────────
# These read the deep-branch scanners that had NO rule at all: their facts were
# collected, shipped and stored, then never assessed. Every path below was read
# off the emitting scanner directly (probe/scanner/<x>_scanner.py), never guessed.
# All of these scanners are EXPERIMENTAL in the trust registry, so their findings
# land as `suspected` rather than `confirmed` — that gating is automatic
# (_state_for) and is the correct treatment until each earns rig validation.

def _ssh_terrapin(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("ssh_confirmed") is True and d.get("terrapin_vulnerable") is True:
        return {"software": d.get("software"),
                "supports_strict_kex": d.get("supports_strict_kex")}
    return None


def _ssh_weak_algos(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("ssh_confirmed") is not True:
        return None
    failures = d.get("failures")
    if not isinstance(failures, list) or not failures:
        return None
    return {"software": d.get("software"), "weak_count": len(failures),
            "weak": failures[:8]}


def _ftp_anonymous(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("ftp") is True and d.get("anonymous_login") is True:
        return {"software": d.get("software"),
                "anon_read": d.get("anon_read"),
                "file_sample": (d.get("file_sample") or [])[:5]}
    return None


def _dns_zone_transfer(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("dns") is not True or d.get("zone_transfer") is not True:
        return None
    axfr = d.get("axfr") if isinstance(d.get("axfr"), dict) else {}
    zones = sorted(z for z, r in axfr.items()
                   if isinstance(r, dict) and r.get("transferred"))
    return {"zones": zones,
            "records": sum(r.get("record_count") or 0 for r in axfr.values()
                           if isinstance(r, dict) and r.get("transferred"))}


def _nfs_world_readable(f: Fact) -> Optional[dict]:
    d = _d(f)
    wr = d.get("world_readable_exports")
    if d.get("nfs") is True and isinstance(wr, list) and wr:
        return {"world_readable_exports": wr[:10], "export_count": len(wr)}
    return None


def _ldap_anonymous_bind(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("ldap") is True and d.get("anonymous_bind") is True:
        return {"default_naming_context": d.get("default_naming_context"),
                "dns_host_name": d.get("dns_host_name"),
                "domain_functional_level": d.get("domain_functional_level")}
    return None


def _vnc_no_auth(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("vnc") is True and d.get("no_auth") is True:
        return {"protocol_version": d.get("protocol_version"),
                "security_types": d.get("security_types")}
    return None


def _vnc_weak_auth(f: Fact) -> Optional[dict]:
    """VNC type 2 is the legacy DES-based challenge with an 8-character password
    ceiling — offline-crackable. Reported separately from no-auth, and NOT when
    no-auth is already the headline (that rule is strictly worse)."""
    d = _d(f)
    if (d.get("vnc") is True and d.get("weak_auth") is True
            and d.get("no_auth") is not True
            and not d.get("has_strong_auth")):
        return {"protocol_version": d.get("protocol_version"),
                "has_strong_auth": d.get("has_strong_auth")}
    return None


def _smtp_user_enum(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("smtp") is not True:
        return None
    verbs = [v for v, on in (("VRFY", d.get("vrfy_enabled")),
                             ("EXPN", d.get("expn_enabled"))) if on is True]
    if not verbs:
        return None
    return {"verbs": verbs, "vrfy_postmaster_code": d.get("vrfy_postmaster_code"),
            "vrfy_random_code": d.get("vrfy_random_code")}


def _smtp_no_starttls(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("smtp") is True and d.get("starttls") is False:
        return {"banner": d.get("banner"),
                "ehlo_capabilities": (d.get("ehlo_capabilities") or [])[:12]}
    return None


def _rsync_anonymous(f: Fact) -> Optional[dict]:
    d = _d(f)
    anon = d.get("anon_modules")
    if d.get("rsync") is True and isinstance(anon, list) and anon:
        return {"anon_modules": anon[:10], "module_count": d.get("module_count")}
    return None


def _smb_null_session(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("smb") is not True or d.get("null_session") is not True:
        return None
    return {"guest_session": d.get("guest_session"),
            "share_count": d.get("share_count"),
            "user_count": d.get("user_count"),
            "shares": [s.get("name") for s in (d.get("shares") or [])
                       if isinstance(s, dict)][:10]}


def _ipmi_cipher_zero(f: Fact) -> Optional[dict]:
    d = _d(f)
    if d.get("ipmi") is True and d.get("cipher_zero") is True:
        return {"rmcp_status": d.get("rmcp_status")}
    return None


# ── the rule pack ─────────────────────────────────────────────────────────────
RULES: list[PostureRule] = [
    PostureRule(
        "POSTURE-SMB-V1-ENABLED", "SMBv1 enabled (wormable, deprecated)",
        "critical", "CWE-477", "T1210", "misconfiguration", ("smb_scan",), _smbv1,
        "Disable SMBv1 (Windows: Remove-WindowsFeature FS-SMB1). SMBv1 is the "
        "EternalBlue/WannaCry transport and has no safe use in 2020+.",
        fp_notes="Requires a SUCCESSFUL SMBv1 negotiate — a filtered/negative "
                 "negotiate does not fire this.",
        requires=("smbv1_enabled",)),
    PostureRule(
        "POSTURE-SMB-SIGNING-OFF", "SMB signing not required (NTLM-relay exposure)",
        "high", "CWE-306", "T1557.001", "misconfiguration", ("smb_scan",), _smb_signing,
        "Require SMB signing (GPO: 'Microsoft network server: Digitally sign "
        "communications (always)') to defeat SMB/NTLM relay.",
        fp_notes="signing_required is read from a successful SMB2 negotiate; only "
                 "fires when SMB2 is up and required=False.",
        requires=("smb2_supported", "signing_required")),
    PostureRule(
        "POSTURE-RDP-NO-NLA", "RDP without Network Level Authentication",
        "high", "CWE-287", "T1210", "misconfiguration", ("rdp_scan",), _rdp_no_nla,
        "Require NLA (CredSSP) on RDP so the RDP stack is not reachable pre-auth; "
        "patch legacy hosts; restrict RDP to VPN/jump hosts.",
        fp_notes="Suppressed when the RDP-only probe was refused (nla_required=True) "
                 "— a CONFIRMED-NLA host never reaches this rule. Fires on EITHER "
                 "probe: a negotiated protocol without CredSSP, or a server that "
                 "accepted a bare standard-RDP request.",
        # `nla` is deliberately NOT required: it is absent whenever the TLS-capable
        # negotiation returned RDP_NEG_FAILURE, which is a legitimate server
        # response, not probe drift. Declaring it made every such host report
        # schema_drift while the second probe's `nla_required` sat unread.
        auth_enforced=_rdp_auth, requires=("rdp_confirmed",)),
    PostureRule(
        "POSTURE-RDP-NO-TLS", "RDP refuses TLS (legacy standard-RDP security)",
        "high", "CWE-326", "T1040", "weak_crypto", ("rdp_scan",), _rdp_no_tls,
        "Set the RDP security layer to TLS (or better, require NLA) and install a "
        "valid certificate. Standard RDP security uses legacy RC4-family crypto with "
        "no server authentication, so the session is interceptable on the path.",
        fp_notes="Derived from the MS-RDPBCGR negotiation failure code, not a "
                 "completed TLS handshake. Only codes 2 (SSL_NOT_ALLOWED_BY_SERVER) "
                 "and 3 (SSL_CERT_NOT_ON_SERVER) are interpreted; other failure "
                 "codes are transport noise and never fire this rule.",
        auth_enforced=_rdp_auth, requires=("rdp_confirmed",)),
    PostureRule(
        "POSTURE-RDP-EXPOSED", "RDP reachable from the scan vantage (confirmed)",
        "low", "CWE-284", "T1021.001", "exposure", ("rdp_scan",), _rdp_exposed,
        "Restrict RDP to VPN/jump hosts and enforce NLA + MFA.",
        fp_notes="Informational when NLA is required; risk escalates automatically "
                 "when auth is not enforced.",
        auth_enforced=_rdp_auth, requires=("rdp_confirmed",)),
    PostureRule(
        "POSTURE-TLS-DEPRECATED-VERSION", "Deprecated TLS/SSL version accepted",
        "high", "CWE-326", "T1040", "weak_crypto", ("tls_scan",), _tls_version,
        "Disable SSLv3/TLS1.0/TLS1.1; require TLS 1.2+ (ideally 1.3).",
        fp_notes="Fires only on versions the server ACCEPTED in a real handshake.",
        requires=("accepted_versions",)),
    PostureRule(
        "POSTURE-TLS-WEAK-CIPHER", "Weak TLS cipher suite offered",
        "medium", "CWE-327", "T1040", "weak_crypto", ("tls_scan",), _tls_cipher,
        "Remove NULL/EXPORT/RC4/DES/3DES/anon cipher suites; prefer AEAD (GCM/"
        "ChaCha20).",
        fp_notes="Keyed off the scanner's own cipher_analysis 'weak' flag.",
        requires=("cipher_analysis",)),
    PostureRule(
        "POSTURE-TLS-SELF-SIGNED", "Self-signed TLS certificate",
        "medium", "CWE-295", "T1557", "weak_crypto", ("tls_scan",), _tls_self_signed,
        "Replace with a certificate from a trusted CA; enable strict validation on "
        "clients.",
        fp_notes="Internal PKI roots also present as self-signed — verify against "
                 "the org's trusted roots before treating as a defect.",
        requires=("certificate",)),
    PostureRule(
        "POSTURE-TLS-EXPIRED-CERT", "Expired TLS certificate",
        "medium", "CWE-298", "T1557", "weak_crypto", ("tls_scan",), _tls_expired,
        "Renew the certificate and automate renewal (ACME) to prevent recurrence.",
        requires=("certificate",)),
    PostureRule(
        "POSTURE-MSRPC-EPMAP-EXPOSED", "MSRPC endpoint mapper enumerable (anonymous)",
        "medium", "CWE-200", "T1135", "information_disclosure", ("msrpc_scan",),
        _msrpc_exposed,
        "Firewall TCP/135 and the dynamic RPC range from untrusted zones; the "
        "endpoint map discloses running services and their dynamic ports.",
        fp_notes="Expected inside a Windows domain LAN; treat as a finding at trust "
                 "boundaries / perimeter.",
        requires=("msrpc",)),
    PostureRule(
        "POSTURE-UDP-AMPLIFIER", "UDP amplification service exposed",
        "medium", "CWE-406", "T1498.002", "amplification", ("udp_scan",), _udp_amplifier,
        "Restrict the service to trusted networks; disable monlist / open recursion; "
        "enable response-rate limiting.",
        fp_notes="Only fires when the service actually ANSWERED (responded=True) — "
                 "no-reply / open|filtered never triggers it.",
        requires=()),   # OR-alternative signals (monlist/open_recursion/service) — no single required path
    PostureRule(
        "POSTURE-SNMP-DEFAULT-COMMUNITY", "SNMP default community string",
        "high", "CWE-1392", "T1078", "default_credentials", ("snmp_scan",), _snmp_default,
        "Change the community string; move to SNMPv3 with auth+priv; restrict by ACL.",
        fp_notes="snmp_scan is not in the validated trust tier yet, so this is "
                 "reported SUSPECTED pending validation.",
        requires=("community",)),

    # ── service-layer rules ───────────────────────────────────────────────────
    # The deep-branch scanners below had NO rule at all: the probe collected,
    # shipped and stored their facts and nothing ever assessed them, so every one
    # of these weaknesses was a guaranteed silent false-negative regardless of the
    # scanner's accuracy. None of these scanners is rig-validated yet, so their
    # findings are SUSPECTED (see _state_for) until they earn the trust tier.
    PostureRule(
        "POSTURE-SSH-TERRAPIN", "SSH vulnerable to Terrapin prefix truncation (CVE-2023-48795)",
        "medium", "CWE-354", "T1557", "weak_crypto", ("ssh_scan",), _ssh_terrapin,
        "Upgrade OpenSSH to 9.6+ (or the vendor backport) so strict key exchange "
        "(kex-strict-s-v00@openssh.com) is offered, or disable ChaCha20-Poly1305 and "
        "all CBC-with-EtM cipher suites.",
        fp_notes="Fires only when a vulnerable algorithm combination is OFFERED and "
                 "strict-kex is absent — the same test ssh-audit applies. A server "
                 "advertising strict-kex never reaches this rule.",
        requires=("ssh_confirmed", "terrapin_vulnerable")),
    PostureRule(
        "POSTURE-SSH-WEAK-ALGORITHMS", "SSH offers deprecated or weak algorithms",
        "high", "CWE-327", "T1040", "weak_crypto", ("ssh_scan",), _ssh_weak_algos,
        "Restrict KexAlgorithms, Ciphers, MACs and HostKeyAlgorithms in sshd_config "
        "to the current recommended set; remove CBC ciphers, SHA-1 MACs and "
        "1024-bit Diffie-Hellman groups.",
        fp_notes="Graded against the scanner's vendored weakness table. Offering a "
                 "weak algorithm is not proof it is negotiated — but it is reachable "
                 "by any client that asks for it.",
        requires=("ssh_confirmed", "failures")),
    PostureRule(
        "POSTURE-FTP-ANONYMOUS-LOGIN", "FTP allows anonymous login",
        "high", "CWE-287", "T1078.001", "misconfiguration", ("ftp_scan",), _ftp_anonymous,
        "Disable the anonymous account, or restrict it to a dedicated read-only "
        "directory that contains nothing sensitive and no writable path.",
        fp_notes="Confirmed by an actual 230 login response, not by the banner. "
                 "`anon_read` records whether a directory listing was returned.",
        requires=("ftp", "anonymous_login")),
    PostureRule(
        "POSTURE-DNS-ZONE-TRANSFER", "DNS zone transfer (AXFR) allowed to any client",
        "high", "CWE-200", "T1590.002", "information_disclosure", ("dns_scan",),
        _dns_zone_transfer,
        "Restrict AXFR to authorized secondaries with `allow-transfer` (BIND) or the "
        "equivalent zone-transfer ACL, and prefer TSIG-authenticated transfers.",
        fp_notes="Fires only when records were actually transferred, not when the "
                 "query merely succeeded — a refused AXFR returns transferred=false.",
        requires=("dns", "zone_transfer")),
    PostureRule(
        "POSTURE-NFS-WORLD-READABLE-EXPORT", "NFS export readable by any host",
        "high", "CWE-732", "T1039", "misconfiguration", ("nfs_scan",), _nfs_world_readable,
        "Replace the wildcard client spec with explicit hosts or subnets, mount "
        "read-only where possible, and enable root_squash.",
        fp_notes="World-readable is decided from the export's client list containing "
                 "a wildcard entry, as reported by the mount daemon itself.",
        requires=("nfs", "world_readable_exports")),
    PostureRule(
        "POSTURE-LDAP-ANONYMOUS-BIND", "LDAP allows anonymous bind (directory disclosure)",
        "low", "CWE-306", "T1087.002", "information_disclosure", ("ldap_scan",),
        _ldap_anonymous_bind,
        "Disable anonymous bind, or restrict the anonymous ACL so the RootDSE alone "
        "is readable and no naming context can be enumerated.",
        fp_notes="An anonymous bind that returns only the RootDSE still confirms the "
                 "bind succeeded; the naming contexts show what was readable. Severity "
                 "matches probe findings.py LDAP-ANON-BIND — a bind that also returned "
                 "directory CONTENT is the higher-severity case.",
        requires=("ldap", "anonymous_bind")),
    PostureRule(
        "POSTURE-VNC-NO-AUTH", "VNC accepts connections with no authentication",
        "critical", "CWE-306", "T1021.005", "misconfiguration", ("vnc_scan",), _vnc_no_auth,
        "Enable VNC authentication, or front the service with SSH/VPN. An unauthenticated "
        "VNC endpoint is a full interactive desktop session for anyone who can reach it.",
        fp_notes="Read from the offered security types in the RFB handshake "
                 "(type 1 = None). The scanner never attempts to complete a session.",
        requires=("vnc", "no_auth")),
    PostureRule(
        "POSTURE-VNC-WEAK-AUTH", "VNC uses legacy DES challenge authentication",
        "medium", "CWE-327", "T1021.005", "weak_crypto", ("vnc_scan",), _vnc_weak_auth,
        "Move to a VNC build offering a modern security type, or tunnel VNC over "
        "SSH/VPN. The legacy type-2 scheme caps passwords at 8 characters and is "
        "offline-crackable from a captured challenge.",
        fp_notes="Suppressed when no-auth is also offered (that finding is strictly "
                 "worse) and when the server ALSO offers a strong security type, since "
                 "a client can then choose it. Mirrors probe findings.py VNC-WEAK-AUTH.",
        requires=("vnc", "weak_auth")),
    PostureRule(
        "POSTURE-SMTP-USER-ENUMERATION", "SMTP VRFY/EXPN allows account enumeration",
        "medium", "CWE-200", "T1087.003", "information_disclosure", ("smtp_scan",),
        _smtp_user_enum,
        "Disable VRFY and EXPN (Postfix: `disable_vrfy_command = yes`) so the server "
        "cannot be used to confirm which mailboxes exist.",
        fp_notes="Decided by comparing the response to a known address against a "
                 "random one, so a server that answers everything identically does "
                 "not fire this rule.",
        requires=("smtp",)),
    PostureRule(
        "POSTURE-SMTP-NO-STARTTLS", "SMTP does not offer STARTTLS (mail in cleartext)",
        "low", "CWE-319", "T1040", "weak_crypto", ("smtp_scan",), _smtp_no_starttls,
        "Advertise and enable STARTTLS with a valid certificate so mail and any "
        "AUTH credentials are not carried in cleartext.",
        fp_notes="Read from the EHLO capability list. A submission port that requires "
                 "implicit TLS is never reached by this plaintext probe.",
        requires=("smtp", "starttls")),
    PostureRule(
        "POSTURE-RSYNC-ANONYMOUS-MODULE", "Rsync module accessible without authentication",
        "high", "CWE-306", "T1039", "misconfiguration", ("rsync_scan",), _rsync_anonymous,
        "Set `auth users` and `secrets file` on every rsync module, and bind the "
        "daemon to a management interface rather than a general-purpose one.",
        fp_notes="A module is counted as anonymous only when the daemon accepted the "
                 "module without a credential challenge.",
        requires=("rsync", "anon_modules")),
    PostureRule(
        "POSTURE-SMB-NULL-SESSION", "SMB null session permits anonymous enumeration",
        "medium", "CWE-306", "T1087.002", "misconfiguration", ("smb_enum_scan",),
        _smb_null_session,
        "Set RestrictAnonymous / RestrictAnonymousSAM (or `restrict anonymous = 2` on "
        "Samba) so shares, users and the domain SID cannot be listed without credentials.",
        fp_notes="Requires a SUCCESSFUL anonymous session — a STATUS_ACCESS_DENIED on "
                 "the null bind reports null_session=false and never fires this. Base "
                 "severity matches probe findings.py SMB-NULL-SESSION; a session that "
                 "also enumerated USERS is the more serious case and is visible in "
                 "evidence.user_count.",
        requires=("smb", "null_session")),
    PostureRule(
        "POSTURE-IPMI-CIPHER-ZERO", "IPMI 2.0 cipher suite 0 (authentication bypass)",
        "critical", "CWE-287", "T1078", "misconfiguration", ("ipmi_scan",), _ipmi_cipher_zero,
        "Disable cipher suite 0 on the BMC and restrict IPMI to an isolated management "
        "VLAN. Cipher 0 accepts any password, granting full out-of-band control of the "
        "host including power and console.",
        fp_notes="Read from the RMCP+ Open Session Response, which states the accepted "
                 "cipher suite; no authentication is attempted.",
        requires=("ipmi", "cipher_zero")),
]


# ── runner ────────────────────────────────────────────────────────────────────
def _state_for(scanner: str) -> str:
    return (FindingState.confirmed.value if is_validated(scanner)
            else FindingState.suspected.value)


def _evidence_ref(f: Fact) -> str:
    if f.source_file:
        return f"{f.source_file}:{f.source_line}"
    return f"{f.scanner}:{f.target}:{f.port}"


def _fact_indicates_no_service(f: Fact, data: dict) -> bool:
    """True when the scanner ran but the service did NOT answer — so a rule's
    declared field is legitimately absent (there was nothing to report), NOT agent
    drift. SNMP/UDP/IPMI probes that get no reply carry responded=False and/or a
    filtered status; treating those as 'blind' cries wolf on every host that simply
    isn't running that service (the false 'N checks couldn't run' the operator saw).
    """
    if data.get("responded") is False:
        return True
    status = (str(f.status) if f.status is not None else "").lower()
    return status in {"filtered", "open|filtered", "closed", "no_response", "unknown", ""}


def evaluate_rule(rule: PostureRule, f: Fact) -> TraceRow:
    """Evaluate ONE rule against ONE fact and record the outcome. NEVER raises —
    a single malformed rule or fact cannot blind the whole submission (fault F9).

    The `requires` contract is checked BEFORE the detector so an absent declared
    path is DRIFT (MISSING_INPUT), not a silent clean no-match — EXCEPT when the
    scanner clearly got no service response, where an absent field is 'not
    applicable' (NO_MATCH), not drift.
    """
    data = f.data if isinstance(f.data, dict) else {}
    no_service = _fact_indicates_no_service(f, data)
    for path in rule.requires:
        if get_path(data, path) is _MISSING:
            if no_service:
                # scanner ran, service didn't answer → nothing to assess → clean/
                # not-applicable, NOT agent drift. Don't count this as a blind rule.
                return TraceRow(rule.rule_id, f.scanner, OUTCOME_NO_MATCH,
                                f.target, f.port)
            return TraceRow(rule.rule_id, f.scanner, OUTCOME_MISSING_INPUT,
                            f.target, f.port,
                            reason=f"required fact path absent: data.{path}")
    try:
        ev = rule.detect(f)
    except (TypeError, ValueError, KeyError) as exc:
        return TraceRow(rule.rule_id, f.scanner, OUTCOME_UNPARSEABLE,
                        f.target, f.port, reason=f"{type(exc).__name__}: {exc}")
    except Exception as exc:                     # a rule bug must not kill the batch
        return TraceRow(rule.rule_id, f.scanner, OUTCOME_ERROR,
                        f.target, f.port, reason=f"{type(exc).__name__}: {exc}")
    if ev:
        return TraceRow(rule.rule_id, f.scanner, OUTCOME_MATCH,
                        f.target, f.port, evidence=ev)
    return TraceRow(rule.rule_id, f.scanner, OUTCOME_NO_MATCH, f.target, f.port)


def _calibrate_host_findings(findings: list, *, reachable_by_id: dict) -> None:
    """Best-effort confidence calibration (lazy import breaks the module cycle;
    calibration is enrichment and must never sink detection)."""
    if not findings:
        return
    try:
        from posture_confidence import calibrate_host_findings
        calibrate_host_findings(findings, reachable_by_id=reachable_by_id)
    except Exception:  # noqa: BLE001 — enrichment only
        pass


def detect_posture_traced(
    asset: Asset, exposure: dict[str, dict] | None = None,
) -> tuple[list[PostureFinding], list[TraceRow]]:
    """Like `detect_posture`, but ALSO returns a per-evaluation trace. The findings
    are byte-for-byte what `detect_posture` produces (that function delegates here),
    so this adds observability with zero behaviour change. The trace is what lets a
    non-finding explain itself: MISSING_INPUT (drift) / NO_MATCH (clean) /
    NO_EVIDENCE (scanner never ran) / ERROR — instead of one undifferentiated 'None'.
    """
    exposure = exposure or {}
    exp = exposure.get(asset.ip, {})
    internet_facing = exp.get("internet_facing")
    default_auth = exp.get("auth_enforced")

    out: list[PostureFinding] = []
    traces: list[TraceRow] = []
    seen: set[tuple] = set()
    reachable_by_id: dict[int, bool] = {}   # finding id() → port confirmed reachable
    now = datetime.now(timezone.utc).isoformat()

    # 1) Evaluate every rule whose scanner produced a fact for this asset.
    scanners_seen = {f.scanner for f in asset.facts}
    for f in asset.facts:
        for rule in RULES:
            if f.scanner not in rule.scanners:
                continue
            row = evaluate_rule(rule, f)
            traces.append(row)
            if row.outcome != OUTCOME_MATCH:
                continue
            key = (rule.rule_id, f.port)
            if key in seen:                       # same weakness, same port → one finding
                continue
            seen.add(key)

            state = _state_for(f.scanner)
            auth = (rule.auth_enforced(f) if rule.auth_enforced else None)
            if auth is None:
                auth = default_auth
            risk, priority = compute_risk(rule.severity, state, internet_facing, auth)
            pf = PostureFinding(
                finding_id=make_posture_id(asset.ip, rule.rule_id, f.port),
                asset_ip=asset.ip, rule_id=rule.rule_id, title=rule.title,
                category=rule.category, severity=rule.severity, state=state,
                confidence=_STATE_CONF.get(state, 65), cwe=rule.cwe, mitre=rule.mitre,
                port=f.port, proto=f.proto, evidence_refs=[_evidence_ref(f)],
                evidence=row.evidence, remediation=rule.remediation,
                fp_notes=rule.fp_notes, internet_facing=internet_facing,
                auth_enforced=auth, risk_score=risk, priority=priority,
                created_at=now, scanner=f.scanner)
            reachable_by_id[id(pf)] = (f.status == "open")   # was the port confirmed up?
            out.append(pf)

    # 1a) Exposed-service / suspicious-port layer: the long tail of risky OPEN
    #     ports — backdoor/C2 listeners, unauthenticated-prone data stores,
    #     container/orchestration APIs, cleartext protocols, exposed admin/dev UIs —
    #     that have no dedicated scanner but ARE findable from the open port + banner
    #     + exposure the validated scanners already collected. Best-effort.
    try:
        out.extend(detect_exposed_services(asset, exposure))
    except Exception:  # noqa: BLE001 — must never sink core detection
        pass

    # 1b) Confidence calibration (second pass, cross-signal aware): now that every rule
    # that fired on this host is known, calibrate each finding's confidence with
    # attack-chain corroboration and stamp the auditable precision_factors. Separate
    # from impact — never changes severity/risk/state.
    _calibrate_host_findings(out, reachable_by_id=reachable_by_id)

    # 2) NO_EVIDENCE (asset-scoped): a rule whose scanner never ran on this asset
    #    was not assessed — a coverage fact, not a defect, but it must be visible so
    #    "no finding" can't masquerade as "checked and clean".
    for rule in RULES:
        if not (scanners_seen & set(rule.scanners)):
            traces.append(TraceRow(
                rule.rule_id, rule.scanners[0] if rule.scanners else "?",
                OUTCOME_NO_EVIDENCE, asset.ip,
                reason=f"no {'/'.join(rule.scanners)} evidence collected for this asset"))
    return out, traces


def detect_posture(asset: Asset,
                   exposure: dict[str, dict] | None = None) -> list[PostureFinding]:
    """Apply every posture rule to one asset's facts. Deduplicates by
    (rule_id, port) — the same weakness seen twice is one finding.

    Thin wrapper over `detect_posture_traced` so existing callers are unchanged."""
    findings, _traces = detect_posture_traced(asset, exposure)
    return findings


# ── exposed-service / suspicious-port layer ───────────────────────────────────
# Ports already covered by a dedicated deep rule — skip so we don't double-report.
_EXPOSED_SVC_DEDICATED_PORTS = {135, 139, 445, 3389}
_PORTSCAN_SCANNERS = {"port_scan", "syn_scan", "mass_scan"}

_EXPOSED_TITLES = {
    "backdoor":      "Suspicious/backdoor port {port} open ({svc})",
    "container":     "Container/orchestration API exposed on {port} ({svc})",
    "datastore":     "Unauthenticated-prone data store exposed on {port} ({svc})",
    "database":      "Database reachable on {port} ({svc})",
    "cleartext":     "Cleartext protocol exposed on {port} ({svc})",
    "remote_access": "Remote-access service exposed on {port} ({svc})",
    "admin_ui":      "Admin/dev interface exposed on {port} ({svc})",
}


def _exposed_title(category: str, service: str, port: int, internet: bool) -> str:
    base = _EXPOSED_TITLES.get(category, "Service exposed on {port}").format(
        port=port, svc=service)
    return base + (" — internet-facing" if internet else "")


def detect_exposed_services(asset: Asset,
                            exposure: dict[str, dict] | None = None) -> list[PostureFinding]:
    """Findings for risky OPEN ports that have no dedicated scanner: backdoor/C2
    listeners, unauthenticated-prone data stores, container APIs, cleartext
    protocols, exposed admin UIs. Reads only what the validated scanners already
    emit — open TCP ports (port/syn/mass scan), banners (service_banner), and the
    exposure classification (exposure_matrix). Severity escalates one level when the
    port is internet-facing (the asset-exposure risk variable)."""
    from port_intel import classify_port, escalate   # standalone module, no cycle

    exposure = exposure or {}
    exp = exposure.get(asset.ip, {})
    default_auth = exp.get("auth_enforced")
    exp_internet = exp.get("internet_facing")

    open_tcp: dict[int, Fact] = {}      # port -> the observing port-scan fact
    banners: dict[int, str] = {}
    # service_banner's soft-matched protocol label + its Basic-over-plaintext
    # flag: OBSERVED protocol evidence that outranks the port number.
    svc_labels: dict[int, str] = {}
    products: dict[int, str] = {}
    basic_cleartext: set[int] = set()
    externally: set[int] = set()

    for f in asset.facts:
        d = f.data if isinstance(f.data, dict) else {}
        if (f.scanner in _PORTSCAN_SCANNERS and f.port and f.status == "open"
                and (f.proto or "tcp") != "udp"):
            open_tcp.setdefault(f.port, f)
        elif f.scanner == "service_banner" and f.port:
            b = d.get("banner")
            if isinstance(b, str) and b.strip():
                banners[f.port] = b.strip()[:200]
            svc = d.get("service")
            if isinstance(svc, str) and svc:
                svc_labels[f.port] = svc
            prod = d.get("product")
            if isinstance(prod, str) and prod:
                products[f.port] = prod
            if d.get("http_basic_auth_cleartext") is True:
                basic_cleartext.add(f.port)
        elif f.scanner == "exposure_matrix":
            for p in (d.get("externally_exposed") or []):
                if isinstance(p, int):
                    externally.add(p)

    now = datetime.now(timezone.utc).isoformat()
    out: list[PostureFinding] = []
    for port in sorted(open_tcp):
        if port in _EXPOSED_SVC_DEDICATED_PORTS:
            continue
        risk = classify_port(port, banners.get(port), service=svc_labels.get(port),
                             basic_auth_cleartext=port in basic_cleartext,
                             product=products.get(port))
        if risk is None:
            continue
        f = open_tcp[port]
        internet = (port in externally) or bool(exp_internet)
        severity = escalate(risk.severity) if internet else risk.severity
        state = _state_for(f.scanner)                 # validated port scan → confirmed
        risk_score, priority = compute_risk(severity, state, internet, default_auth)
        rule_id = f"POSTURE-EXPOSED-{risk.category.upper()}"
        ev: dict[str, Any] = {"port": port, "category": risk.category,
                              "service": risk.service, "internet_facing": internet}
        if banners.get(port):
            ev["banner"] = banners[port]
        if svc_labels.get(port):
            ev["observed_service"] = svc_labels[port]
        if products.get(port):
            # The identified product, so an operator can see at a glance whether it
            # agrees with the service the port catalog named.
            ev["observed_product"] = products[port]
        out.append(PostureFinding(
            finding_id=make_posture_id(asset.ip, rule_id, port),
            asset_ip=asset.ip, rule_id=rule_id,
            title=_exposed_title(risk.category, risk.service, port, internet),
            category="exposure", severity=severity, state=state,
            confidence=_STATE_CONF.get(state, 65), cwe=risk.cwe, mitre=risk.mitre,
            port=port, proto="tcp", evidence_refs=[_evidence_ref(f)],
            evidence=ev, remediation=risk.note,
            fp_notes="Signal derived from the open port (+ banner). A benign internal "
                     "service can share these ports — confirm the owning process/scope.",
            internet_facing=internet, auth_enforced=default_auth,
            risk_score=risk_score, priority=priority, created_at=now, scanner=f.scanner))
    return out


# ── verdict roll-up: the machine-readable answer to "why no finding?" ──────────
def verdict_for_rule(traces: list[TraceRow], rule_id: str) -> tuple[str, list[str]]:
    """Collapse every trace for one rule into a single verdict + reason strings.
    Precedence: a real finding wins; then a rule error; then drift (the dangerous
    silent-clean case); then a genuine clean; then 'scanner never ran'."""
    rows = [t for t in traces if t.rule_id == rule_id]
    outcomes = {t.outcome for t in rows}
    reasons = sorted({t.reason for t in rows if t.reason})
    if OUTCOME_MATCH in outcomes:
        return VERDICT_FINDING, []
    if OUTCOME_ERROR in outcomes:
        return VERDICT_RULE_ERROR, reasons
    if outcomes & {OUTCOME_MISSING_INPUT, OUTCOME_UNPARSEABLE}:
        return VERDICT_SCHEMA_DRIFT, reasons
    if OUTCOME_NO_MATCH in outcomes:
        return VERDICT_CLEAN, []
    return VERDICT_NO_EVIDENCE, reasons


def summarize_traces(traces: list[TraceRow]) -> dict[str, Any]:
    """Engagement-level coverage roll-up over a set of traces. `rules_blind > 0`
    is the single number that tells you detection was incomplete — the thing today's
    empty findings list cannot express."""
    by_outcome: dict[str, int] = {o: 0 for o in _ALL_OUTCOMES}
    rules_by_bucket: dict[str, set] = {"blind": set(), "unassessed": set(),
                                       "matched": set(), "clean": set()}
    for t in traces:
        by_outcome[t.outcome] = by_outcome.get(t.outcome, 0) + 1
        if t.outcome in BLIND_OUTCOMES:
            rules_by_bucket["blind"].add(t.rule_id)
        elif t.outcome in UNASSESSED_OUTCOMES:
            rules_by_bucket["unassessed"].add(t.rule_id)
        elif t.outcome == OUTCOME_MATCH:
            rules_by_bucket["matched"].add(t.rule_id)
        elif t.outcome == OUTCOME_NO_MATCH:
            rules_by_bucket["clean"].add(t.rule_id)
    assessed = rules_by_bucket["matched"] | rules_by_bucket["clean"]
    return {
        "by_outcome": by_outcome,
        "rules_total": len(RULES),
        "rules_matched": len(rules_by_bucket["matched"]),
        "rules_assessed": len(assessed),
        "rules_blind": len(rules_by_bucket["blind"] - assessed),
        "rules_unassessed": len(rules_by_bucket["unassessed"] - assessed
                                - rules_by_bucket["blind"]),
        "blind_rule_ids": sorted(rules_by_bucket["blind"] - assessed),
    }


def detect_all_traced(
    assets: dict[str, Asset] | Any, exposure: dict[str, dict] | None = None,
) -> tuple[list[PostureFinding], list[TraceRow]]:
    """Traced counterpart of `detect_all` — findings identical, plus the full trace."""
    mapping = getattr(assets, "assets", assets)
    findings: list[PostureFinding] = []
    traces: list[TraceRow] = []
    for asset in mapping.values():
        fs, ts = detect_posture_traced(asset, exposure)
        findings.extend(fs)
        traces.extend(ts)
    findings.sort(key=lambda x: (-x.risk_score, x.asset_ip, x.rule_id))
    return findings, traces


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
