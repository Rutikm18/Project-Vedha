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
                 "— a CONFIRMED-NLA host never reaches this rule.",
        auth_enforced=_rdp_auth, requires=("rdp_confirmed", "nla")),
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
        elif f.scanner == "exposure_matrix":
            for p in (d.get("externally_exposed") or []):
                if isinstance(p, int):
                    externally.add(p)

    now = datetime.now(timezone.utc).isoformat()
    out: list[PostureFinding] = []
    for port in sorted(open_tcp):
        if port in _EXPOSED_SVC_DEDICATED_PORTS:
            continue
        risk = classify_port(port, banners.get(port))
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
