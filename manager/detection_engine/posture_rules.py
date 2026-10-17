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
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from default_creds_catalog import has_known_defaults
from eol_catalog import lookup_eol
from models import Asset, Fact, FindingState
from os_release_intel import release_from_ssh_fact

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
    "snmp_scan",                             # SNMP default-community rig-verified (lab, 9 Oct)
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


class Undetermined:
    """What a detector returns when its scanner ran but could not settle the
    question: an OS guess with no release, or a build two releases share. That is
    a coverage gap (NO_EVIDENCE, with the reason), not agent drift and not clean.
    Falsy, so it can never pass for a finding."""
    __slots__ = ("reason",)

    def __init__(self, reason: str):
        self.reason = reason

    def __bool__(self) -> bool:
        return False


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
    # True for a rule that only means something when NOTHING else explained the port: it is
    # skipped when another scanner already produced an open-port fact for the same port (the
    # unidentified-service rule must not fire on a port the MQTT or ADB scanner identified).
    unless_explained: bool = False
    # What the detector's evidence IS (see BASIS_*). Dedicated-scanner rules read a
    # protocol-level answer, hence the default; a rule that keys off an open port or a
    # banner heuristic must say so and is then capped at SUSPECTED.
    evidence_basis: str = "protocol_observed"
    # One finding per host, whichever fact proved it (port None, so the finding id
    # is stable when the evidence moves between scanners). For host properties
    # such as the OS release, which several scanners can each reveal.
    host_level: bool = False


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


# US-CERT/CISA TA14-017A bandwidth-amplification factors (lower bound of the published
# range). A measured response/request ratio at or above a protocol's factor makes the
# service a usable reflective-DDoS source; below it the service is merely exposed.
_AMP_FACTOR_THRESHOLDS = {
    "dns": 28.0, "ntp": 556.0, "snmp": 6.3, "ssdp": 30.8,
    "chargen": 358.0, "memcached": 10000.0, "ldap": 46.0,
}


def _num(v: Any) -> Optional[float]:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _udp_amplifier(f: Fact) -> Optional[dict]:
    """A UDP service that is demonstrably usable as a reflective-DDoS amplifier.

    Fires only on a protocol-level proof or a measured factor — NEVER on "the service
    answered a normal query" (a closed-recursion DNS server or a stock NTP daemon
    answers one too, and is not an amplifier):
      * NTP    — monlist actually enabled;
      * DNS    — open recursion (RA set, NOERROR, answers present);
      * memcached — stats served to an unauthenticated UDP client;
      * chargen — any reply (the service IS the amplifier, TA14-017A ~358x);
      * any of the above protocols — a measured `amplification_factor` at or above the
        TA14-017A threshold.
    Below that it is exposure (handled by the exposure rules), not amplification."""
    d = _d(f)
    if d.get("monlist_enabled") is True:
        return {"service": "ntp", "monlist_enabled": True, "basis": "protocol_observed"}
    if d.get("open_recursion") is True:
        return {"service": "dns", "open_resolver": True, "basis": "protocol_observed"}
    svc = str(d.get("service") or "").lower()
    if d.get("responded") is not True or f.status != "open" or svc not in _AMPLIFIERS:
        return None
    if svc == "memcached" and d.get("exposed_unauthenticated") is True:
        return {"service": svc, "exposed_unauthenticated": True, "basis": "protocol_observed"}
    if svc == "chargen":
        return {"service": svc, "basis": "protocol_observed",
                "factor_reference": _AMP_FACTOR_THRESHOLDS["chargen"]}
    factor = _num(d.get("amplification_factor"))
    threshold = _AMP_FACTOR_THRESHOLDS.get(svc)
    if factor is not None and threshold is not None and factor >= threshold:
        return {"service": svc, "amplification_factor": round(factor, 2),
                "threshold": threshold, "basis": "measured_factor"}
    return None


# Ports where an open socket that returns no identifiable banner is the NORMAL case: these
# protocols are client-first or binary, and have dedicated scanners / rules of their own.
_SILENT_BY_DESIGN_PORTS = frozenset({
    53, 88, 111, 135, 139, 389, 445, 464, 593, 636, 873, 2049, 3268, 3269, 3389, 5985, 5986,
})
_EPHEMERAL_FLOOR = 49152          # dynamic RPC / ephemeral range: unidentified by nature


def _unidentified_service(f: Fact) -> Optional[dict]:
    """An open TCP port that the banner stage tried to identify and could not.

    Fires only when service_banner SAYS it found nothing (`identified is False`) — a fact
    from a probe build that predates the flag is never read as "unidentified". Ports the
    exposed-service catalog already names, silent-by-design protocols and the ephemeral range
    are excluded, so this is the long tail: Smart Install 4786, SLP 427, Radmin 4899, AFP 548,
    EPMD 4369, BGP 179 and whatever else answers on a non-standard port."""
    d = _d(f)
    port = f.port
    if d.get("identified") is not False or f.status != "open" or (f.proto or "tcp") == "udp":
        return None
    if not isinstance(port, int) or port <= 0 or port >= _EPHEMERAL_FLOOR \
            or port in _SILENT_BY_DESIGN_PORTS:
        return None
    try:
        from port_intel import catalog_categories     # standalone module, no cycle
        if port in catalog_categories():
            return None
    except ImportError:                                # pragma: no cover
        pass
    ev: dict = {"port": port, "identified": False}
    if d.get("raw_hex"):
        ev["raw_hex"] = str(d["raw_hex"])[:128]
    return ev


def _snmpv3_noauth(f: Fact) -> Optional[dict]:
    """An SNMPv3 user that answered a read at security level noAuthNoPriv: no authentication
    and no encryption, the v3 equivalent of a default community. The probe tries only a few
    documented default user names and records the first that got a GetResponse."""
    user = _d(f).get("snmpv3_noauth_user")
    return {"user": user} if isinstance(user, str) and user else None


def _ftp_anonymous_write(f: Fact) -> Optional[dict]:
    """Anonymous FTP accepted an upload (the probe stored a tiny file and tried to delete it).
    Only present when the operator explicitly enabled the opt-in write test; `anon_write` is
    None when it was not tested, and that is never read as a clean result."""
    d = _d(f)
    if d.get("ftp") is True and d.get("anonymous_login") is True and d.get("anon_write") is True:
        return {"software": d.get("software"),
                "leftover_file": d.get("anon_write_leftover") or None}
    return None


def _udp_service_answered(f: Fact, service: str) -> Optional[dict]:
    d = _d(f)
    if d.get("responded") is True and f.status == "open" \
            and str(d.get("service") or "").lower() == service:
        return d
    return None


def _sip_exposed(f: Fact) -> Optional[dict]:
    """A SIP service that answered an OPTIONS probe with a real SIP status line. The status
    line is the protocol observation; a bare UDP reply on 5060 that is not SIP is not this."""
    d = _udp_service_answered(f, "sip")
    line = str((d or {}).get("sip_response") or "")
    if d is not None and line.upper().startswith("SIP/2.0"):
        return {"sip_response": line[:120], "server": d.get("server") or None}
    return None


def _netbios_exposed(f: Fact) -> Optional[dict]:
    """A NetBIOS name service that answered a node-status query: it discloses host, domain
    and MAC details to whoever can reach UDP/137."""
    return {"service": "netbios-ns"} if _udp_service_answered(f, "netbios-ns") else None


def _mdns_exposed(f: Fact) -> Optional[dict]:
    """An mDNS responder that answered a unicast query with a response (QR bit set), i.e.
    reachable beyond the local link where multicast DNS is meant to stay."""
    d = _udp_service_answered(f, "mdns")
    if d is not None and d.get("mdns_response") is True:
        return {"answer_count": d.get("answer_count")}
    return None


def _reply_text(value: Any, limit: int = 128) -> str:
    """A string the scanned host chose (via the agent): printable only, and short."""
    return "".join(ch if ch.isprintable() else "?" for ch in str(value or "")[:limit])


def _xdmcp_reply(f: Fact):
    """The display manager's answer to the agent's XDMCP Query (UDP/177), as fact data;
    Undetermined when the Query met silence; None when the fact is not about XDMCP, the
    port is closed, or what answered was not XDMCP."""
    d = _d(f)
    if str(d.get("service") or d.get("service_guess") or "").lower() != "xdmcp":
        return None
    if f.status == "open|filtered":
        # Silence on UDP: a display manager that ignored us, or a firewall that dropped the
        # Query. It proves nothing, so it must never be the re-check that clears a finding.
        return Undetermined("no reply to the XDMCP Query (open|filtered)")
    if f.status != "open" or d.get("responded") is not True:
        return None
    return d


def _xdmcp_willing(f: Fact):
    """XDMCP answered Willing: this display manager offers a remote X login to the host that
    asked, and XDMCP and the X session it starts are unencrypted."""
    d = _xdmcp_reply(f)
    if not isinstance(d, dict):
        return d
    if d.get("xdmcp_opcode") != "willing":
        return None
    return {"hostname": _reply_text(d.get("xdmcp_hostname")),
            "status": _reply_text(d.get("xdmcp_status")),
            "authentication": _reply_text(d.get("xdmcp_auth")) or None}


def _xdmcp_exposed(f: Fact):
    """XDMCP answered Unwilling: the display manager is running and reachable but declined
    this host. Its access list decides who else it would offer a login to."""
    d = _xdmcp_reply(f)
    if not isinstance(d, dict):
        return d
    if d.get("xdmcp_opcode") != "unwilling":
        return None
    return {"hostname": _reply_text(d.get("xdmcp_hostname")),
            "status": _reply_text(d.get("xdmcp_status"))}


# UPnP Internet Gateway Device markers: the device / service types a gateway announces.
_UPNP_IGD = re.compile(r"InternetGatewayDevice|WAN(?:IP|PPP)Connection|WANCommonInterfaceConfig",
                       re.IGNORECASE)


def _ssdp_answer(f: Fact) -> Optional[dict]:
    """iot_scan's unicast M-SEARCH reply (UDP 1900): None unless the device really
    answered SSDP (a ST / USN / LOCATION header came back)."""
    if f.port != 1900:
        return None
    d = _d(f)
    if not any(str(d.get(k) or "").strip() for k in ("st", "usn", "location")):
        return None
    return d


def _upnp_summary(d: dict) -> dict:
    dev = d.get("upnp_device") if isinstance(d.get("upnp_device"), dict) else {}
    return {"server": str(d.get("server") or "")[:120] or None,
            "st": str(d.get("st") or "")[:160] or None,
            "device_type": str(dev.get("device_type") or "")[:160] or None,
            "manufacturer": str(dev.get("manufacturer") or "")[:80] or None,
            "model_name": str(dev.get("model_name") or "")[:80] or None}


def _is_igd(d: dict) -> bool:
    dev = d.get("upnp_device") if isinstance(d.get("upnp_device"), dict) else {}
    blob = " ".join(str(x or "") for x in (d.get("st"), d.get("usn"), dev.get("device_type")))
    return bool(_UPNP_IGD.search(blob))


def _upnp_igd_exposed(f: Fact) -> Optional[dict]:
    """A UPnP Internet Gateway Device answering discovery: any host that can reach it can
    ask the gateway, without authentication, to open inbound port mappings."""
    d = _ssdp_answer(f)
    return _upnp_summary(d) if d is not None and _is_igd(d) else None


def _upnp_exposed(f: Fact) -> Optional[dict]:
    """Any other UPnP device answering unicast M-SEARCH (the IGD case is its own rule)."""
    d = _ssdp_answer(f)
    return _upnp_summary(d) if d is not None and not _is_igd(d) else None


def _ike_aggressive(f: Fact) -> Optional[dict]:
    """An IKEv1 responder whose reply used the AGGRESSIVE exchange (type 4). With a pre-shared
    key, aggressive mode sends the identity and an authentication hash in the clear, which can be
    cracked offline. Fires only on that observed exchange type — the presence of IKE is not it."""
    d = _d(f)
    if str(d.get("service") or "").lower() not in {"ike", "ike-nat"} or f.status != "open":
        return None
    version = str(d.get("version") or "")
    exchange = d.get("exchange_type")
    if version.startswith("IKEv1") and isinstance(exchange, int) \
            and not isinstance(exchange, bool) and exchange == 4:
        return {"version": version, "exchange_type": exchange}
    return None


# Community names that conventionally carry WRITE access on devices that ship them.
_RW_CONVENTION_COMMUNITIES = frozenset({"private", "write", "admin", "secret", "manager"})


def _snmp_default(f: Fact) -> Optional[dict]:
    """A default community answered. The scanner never sends a SET, so this proves READ
    access only; a community conventionally used for write ("private") is named as
    such, never claimed as proven write access (testing-round gap 12)."""
    c = _d(f).get("community")
    if c not in _DEFAULT_COMMUNITIES:
        return None
    out = {"community": c, "access_proven": "read",
           "write_access": "not tested (the scanner never sends an SNMP SET)"}
    if str(c).lower() in _RW_CONVENTION_COMMUNITIES:
        out["note"] = (f"community '{c}' is conventionally the read-write community; "
                       "write access was not tested")
    return out


# ── canonical condition key (cross-producer identity) ─────────────────────────
# Identity of "the same issue on the same service", independent of which producer raised
# it or how it is titled: (service/port, weakness-class). Findings with equal keys on one
# asset are ONE issue; the manager merges them (DefectDojo-style hash over a fixed field
# set, with the service/port always part of it). Rules that describe different weaknesses
# of one service (weak-TLS vs web-method on 443; default-community vs amplifier on 161)
# get different classes, so the "two genuinely different issues on one port stay
# separate" guard holds — the report rolls those up under the service instead.
DEDUP_KEY = "dedup_key"
CLASS_EXPOSED = "exposed"
# Rules that say "this service is reachable / usable from where it should not be", however
# they got there. Everything in categories exposure/amplification, plus the dedicated
# scanners whose finding is the same condition a port-intel row reports for that port.
_EXPOSED_CLASS_RULES = frozenset({"POSTURE-NFS-WORLD-READABLE-EXPORT"})
_EXPOSED_CLASS_CATEGORIES = frozenset({"exposure", "amplification"})


def condition_key(weakness_class: str, port: Optional[int], proto: Optional[str] = None) -> str:
    """`<class>:<port>` (`/udp` suffix for UDP). The exposed class keeps the historical
    `exposed:<port>` spelling so rows stored before this existed still merge."""
    suffix = "/udp" if str(proto or "").lower() == "udp" else ""
    return f"{weakness_class}:{port}{suffix}" if isinstance(port, int) else weakness_class


def weakness_class_for(rule_id: str, category: Optional[str] = None) -> str:
    if (rule_id.startswith("POSTURE-EXPOSED-") or rule_id in _EXPOSED_CLASS_RULES
            or category in _EXPOSED_CLASS_CATEGORIES):
        return CLASS_EXPOSED
    return rule_id.removeprefix("POSTURE-").lower()      # one class per rule


def condition_key_for(rule_id: str, category: Optional[str], port: Optional[int],
                      proto: Optional[str] = None) -> str:
    return condition_key(weakness_class_for(rule_id, category), port, proto)


def group_key_for(rule_id: str, evidence: dict | None) -> str:
    """A stable handle for collapsing identical findings across a fleet.

    Twelve identical cameras produce twelve identical findings. Listed one per
    row they bury the three findings that actually matter, and rows 2-12 tell the
    reader nothing row 1 didn't. This key lets the presentation layer fold them
    into a single row with an asset count.

    PRESENTATION ONLY. Every per-asset finding is still stored with its own
    evidence — merging the underlying records would destroy the ability to say
    "eleven of these are fixed, that one isn't", which is exactly what an
    operator needs during remediation.

    The signature is the strongest device identity in the evidence (product, then
    service). Cosmetic differences in banner strings — casing, padding — must not
    split a group, so it is normalised. With no signature at all the key degrades
    to rule-only: coarser, but deterministic and never a crash.
    """
    ev = evidence or {}
    sig = ev.get("product") or ev.get("service") or ""
    raw = f"{rule_id}|{str(sig).strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _default_cred_candidate(f: Fact) -> Optional[dict]:
    """A device from a known-defaults vendor that is exposing a login.

    CANDIDATE, never confirmation. Vedha does not attempt the credential — a
    login attempt can lock accounts, trip IDS, and wedge embedded management
    interfaces, and it changes the tool from one that observes to one that
    authenticates. So this reports what is provable from evidence already held:
    the vendor publishes defaults, and a login surface is reachable.

    Both halves are required. A known-defaults vendor with no observed login
    surface (web UI firewalled off) is not this risk, and a login surface from an
    uncatalogued vendor is not evidence a default password exists.
    """
    d = _d(f)
    surface = d.get("auth_surface")
    if not isinstance(surface, dict):
        return None
    scheme = surface.get("scheme")
    if not scheme or scheme == "none":
        return None                       # no reachable login -> not this finding

    vendor = surface.get("vendor") or d.get("vendor")
    hit = has_known_defaults(vendor)
    if hit is None:
        return None                       # uncatalogued vendor -> never guess

    vendor = str(vendor).strip().lower()
    return {
        "vendor": vendor,
        "auth_scheme": scheme,
        "realm": surface.get("realm"),
        "default_login": hit["default_login"],
        "reference": hit["reference"],
        "product": d.get("model") or d.get("product") or vendor,
        "detail": (f"{vendor} devices ship a documented default login "
                   f"({hit['default_login']}) and this host exposes a {scheme} "
                   f"login surface. Confirm the default was changed — Vedha does "
                   f"not attempt credentials, so this is unverified."),
    }


def _os_eol(f: Fact) -> Optional[dict]:
    """An OS past its vendor end-of-SECURITY-support date.

    Reads the release string os_fingerprint already emits; the catalog decides.
    An OS absent from the catalog is treated as SUPPORTED (returns None) rather
    than guessed at — telling a customer their supported fleet is dead destroys
    trust in every other finding, so the asymmetry favours silence.
    """
    d = _d(f)
    if f.scanner == "ssh_scan":
        # A distribution's packaged OpenSSH names the release it was built for.
        derived = release_from_ssh_fact(d)
        if derived is None:
            return Undetermined("the SSH banner does not name a known distribution release")
        release, version = derived["os_release"], None
        how = f"identified from the SSH banner {derived['os_release_evidence']!r}"
    else:
        release, version = d.get("os_release"), d.get("os_version")
        if not release:
            return Undetermined(
                "OS release not identified: an exact release needs SMB on 445 "
                "(Windows build) or a distribution SSH banner (Linux)")
        how = "identified by os_fingerprint"
    hit = lookup_eol(release, version)
    if hit is None:
        return None
    alt = d.get("os_release_alt")
    if alt and lookup_eol(alt) is None:
        # e.g. build 17763 is Windows 10 1809 (EOL) AND Server 2019 (supported);
        # the network cannot tell the SKU, so neither verdict is honest.
        return Undetermined(
            f"build is shared by {release} (end-of-life) and {alt} (supported); "
            f"the edition cannot be told apart from the network")
    return {
        "product": hit["product"],
        "eol_date": hit["eol_date"],
        "days_past_eol": hit["days_past_eol"],
        "source": hit["source"],
        "os_release_source": "ssh_banner" if f.scanner == "ssh_scan" else "os_fingerprint",
        "detail": (f"{hit['product']} reached end-of-support on {hit['eol_date']} "
                   f"({hit['days_past_eol']} days ago), {how}. No security patches "
                   f"are issued, so its vulnerability count can only grow."),
    }


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


# Reasons (ssh-audit's wording, vendored in the probe) that mean an algorithm is BROKEN —
# a practical attack, not just deprecation. Anything else ssh-audit fails (SHA-1 MACs and
# signatures, RIPEMD, SEED, a 1024-bit group on its own, ...) is LEGACY: worth retiring, not
# an emergency. A stock current OpenSSH still offers hmac-sha1, so it must not read as High.
# The NIST curves (ecdh-sha2-nistp*, ecdsa-sha2-nistp*) fail in ssh-audit as "suspected as
# being backdoored": a trust concern with no practical attack, and every default OpenSSH
# offers them, so "backdoored" is deliberately NOT here (it put almost every Linux host on
# the High rule). Those entries fall through to the LEGACY rule.
_SSH_BROKEN_REASON = re.compile(
    r"rc4|3des|blowfish|cast|broken des|\bdes cipher|md5|no encryption|logjam|small ecc|"
    r"untrusted", re.IGNORECASE)
_SSH_BROKEN_ALGO = re.compile(
    r"^(arcfour|3des|des-|blowfish|cast128|none$|diffie-hellman-group1-sha1|hmac-md5)",
    re.IGNORECASE)


def _ssh_entry_is_broken(entry: Any) -> bool:
    if not isinstance(entry, dict):
        return False
    reasons = entry.get("reasons")
    if isinstance(reasons, list) and reasons:
        return any(_SSH_BROKEN_REASON.search(str(r)) for r in reasons)
    return bool(_SSH_BROKEN_ALGO.search(str(entry.get("algorithm") or "")))     # old facts


def _ssh_failures(f: Fact) -> list:
    d = _d(f)
    if d.get("ssh_confirmed") is not True:
        return []
    failures = d.get("failures")
    return failures if isinstance(failures, list) else []


def _ssh_weak_algos(f: Fact) -> Optional[dict]:
    """SSH offering an algorithm with a practical attack (RC4, 3DES, DES, Blowfish, MD5,
    Logjam-class groups, no encryption). Merely deprecated algorithms are the LEGACY rule."""
    broken = [e for e in _ssh_failures(f) if _ssh_entry_is_broken(e)]
    if not broken:
        return None
    d = _d(f)
    return {"software": d.get("software"), "weak_count": len(broken), "weak": broken[:8]}


def _ssh_legacy_algos(f: Fact) -> Optional[dict]:
    """SSH offering only deprecated-but-not-broken algorithms (SHA-1 MACs, CBC, ...)."""
    failures = _ssh_failures(f)
    if not failures or any(_ssh_entry_is_broken(e) for e in failures):
        return None
    d = _d(f)
    return {"software": d.get("software"), "legacy_count": len(failures),
            "legacy": failures[:8], "buckets": d.get("buckets")}


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


# ── additional service-layer detectors (previously-unconsumed facts) ──────────
# Each reads a field the probe already collects and ships but no rule assessed, so
# every one of these weaknesses was a guaranteed silent false-negative. Every path
# is read off the emitting scanner directly (probe/scanner/<x>_scanner.py). None of
# these scanners is rig-validated, so findings land `suspected` (_state_for).

# Minimum acceptable key sizes. RSA/DSA below 2048 bits is below every current
# baseline (NIST SP 800-57, CA/Browser Forum); EC below 256 bits likewise.
_MIN_RSA_DSA_BITS = 2048
_MIN_EC_BITS = 256
# Certificate signature algorithms that are collision-broken for TLS trust.
_WEAK_SIG_ALGOS = {"md2", "md5", "sha1"}


def _tls_weak_key(f: Fact) -> Optional[dict]:
    """A server certificate whose public key is below the modern floor.

    Reads the key type + bit size tls_scanner already parses from the DER. Only
    fires when the probe POSITIVELY parsed both (the `cryptography` path); a
    byte-count-only degraded parse emits neither field and this stays silent —
    absent evidence must never become a weak-key accusation.
    """
    c = _cert(f)
    ktype = str(c.get("public_key_type") or "").lower()
    bits = c.get("public_key_bits")
    if not isinstance(bits, int) or isinstance(bits, bool) or bits <= 0:
        return None
    if ktype in ("rsa", "dsa", "dh") and bits < _MIN_RSA_DSA_BITS:
        floor = _MIN_RSA_DSA_BITS
    elif ktype in ("ec", "ecdsa", "ellipticcurve") and bits < _MIN_EC_BITS:
        floor = _MIN_EC_BITS
    else:
        return None
    return {"public_key_type": ktype, "public_key_bits": bits, "minimum_bits": floor,
            "subject": c.get("subject")}


def _tls_weak_sig(f: Fact) -> Optional[dict]:
    """A certificate signed with a collision-broken hash (MD5/SHA-1). Read from
    the parsed `sig_algorithm`; a forged-chain / downgrade risk, not merely
    cosmetic. Silent when the field was never parsed."""
    c = _cert(f)
    raw = str(c.get("sig_algorithm") or "").lower()
    if not raw:
        return None
    hit = next((a for a in _WEAK_SIG_ALGOS if a in raw), None)
    if not hit:
        return None
    return {"sig_algorithm": c.get("sig_algorithm"), "weak_hash": hit,
            "self_signed": c.get("self_signed"), "subject": c.get("subject")}


def _web_dangerous_methods(f: Fact) -> Optional[dict]:
    """HTTP methods that write or probe state are enabled (PUT/DELETE/TRACE/
    CONNECT/PATCH), read straight from the OPTIONS Allow header the web scanner
    parsed. PUT can plant a webshell; TRACE enables Cross-Site Tracing; CONNECT
    turns the server into an open proxy."""
    d = _d(f)
    methods = d.get("dangerous_methods")
    if isinstance(methods, list) and methods:
        return {"dangerous_methods": methods[:8],
                "allowed_methods": (d.get("allowed_methods") or [])[:12],
                "url": d.get("url") or d.get("final_url")}
    return None


def _web_missing_hsts(f: Fact) -> Optional[dict]:
    """An HTTPS service that does not send HSTS — the response is downgradeable to
    cleartext on the first request (sslstrip class). Scoped to TLS services and to
    the single header that actually changes the threat model, so it stays a
    low-noise finding rather than a blanket 'headers missing' lint."""
    d = _d(f)
    if d.get("tls") is not True:
        return None
    missing = d.get("security_headers_missing")
    if not isinstance(missing, list) or "strict-transport-security" not in missing:
        return None
    return {"missing_header": "strict-transport-security",
            "security_headers_missing": [m for m in missing if isinstance(m, str)][:8],
            "url": d.get("url") or d.get("final_url")}


def _dns_version_disclosure(f: Fact) -> Optional[dict]:
    """The resolver answered a CHAOS TXT version.bind query, disclosing its exact
    software/version to any client — recon that narrows the attacker's next move
    to version-specific DNS CVEs. Read from the value dns_scanner already stores."""
    d = _d(f)
    if d.get("dns") is not True:
        return None
    ver = d.get("version_bind")
    if isinstance(ver, str) and ver.strip() and ver.strip().lower() not in (
            "unknown", "none", "refused"):
        return {"version_bind": ver.strip()[:120], "hostname_bind": d.get("hostname_bind")}
    return None


def _ldap_anonymous_search(f: Fact) -> Optional[dict]:
    """Anonymous LDAP SEARCH returned directory CONTENT (not merely a successful
    bind to the RootDSE) — usernames, group membership and host objects readable
    with no credentials. Higher severity than anon-bind-only, which discloses only
    the RootDSE. Read from the scanner's own `anonymous_search_allowed`."""
    d = _d(f)
    if d.get("ldap") is True and d.get("anonymous_search_allowed") is True:
        return {"sample_entry_count": d.get("sample_entry_count"),
                "default_naming_context": d.get("default_naming_context"),
                "naming_contexts": (d.get("naming_contexts") or [])[:8]}
    return None


# An amplification ratio at or above this is a usable reflective-DDoS source: a
# small query yields a response this many times larger (US-CERT TA14-017A lists
# SNMPv2 at 6.3x; we require a measured multiple at that published factor to avoid
# flagging a near-1x responder).
_SNMP_AMP_FACTOR = _AMP_FACTOR_THRESHOLDS["snmp"]


def _snmp_amplification(f: Fact) -> Optional[dict]:
    """A readable SNMP agent whose MEASURED response/request size ratio makes it a
    reflective-amplification DDoS source. Reads snmp_scanner's own GETBULK
    amplification_factor — a measured multiple, stronger than a port-presence
    guess. Silent when the walk did not measure it (field absent)."""
    d = _d(f)
    factor = d.get("amplification_factor")
    if isinstance(factor, (int, float)) and not isinstance(factor, bool) \
            and float(factor) >= _SNMP_AMP_FACTOR:
        return {"amplification_factor": round(float(factor), 2),
                "threshold": _SNMP_AMP_FACTOR, "community": d.get("community")}
    return None


def _iot_mqtt_unauth(f: Fact) -> Optional[dict]:
    """An MQTT broker that accepted a CONNECT with no credentials (CONNACK rc=0),
    read from iot_scanner's own flags. An unauthenticated broker lets any client
    subscribe to '#' and read/inject every message — telemetry, commands, secrets."""
    d = _d(f)
    if d.get("mqtt_connack") is True and d.get("unauthenticated_access") is True:
        return {"return_code_meaning": d.get("return_code_meaning"),
                "subscribe_all_granted": d.get("subscribe_all_granted")}
    return None


def _iot_cwmp_exposed(f: Fact) -> Optional[dict]:
    """A TR-069/CWMP (CPE WAN management) interface is reachable. CWMP on 7547 is
    the documented Mirai/TR-064 worm vector; exposing it to untrusted networks is
    a remote-management surface on the device's WAN side."""
    d = _d(f)
    if d.get("cwmp_indicators") is True:
        return {"server": d.get("server"), "http_response": d.get("http_response")}
    return None


def _iot_rtsp_exposed(f: Fact) -> Optional[dict]:
    """An RTSP streaming endpoint (IP camera / NVR) answered an OPTIONS with its
    method list — a reachable camera control/stream surface, frequently shipped
    with default or no credentials."""
    d = _d(f)
    methods = d.get("public_methods")
    if d.get("rtsp_version") and isinstance(methods, str) and methods.strip():
        return {"rtsp_version": d.get("rtsp_version"), "public_methods": methods[:120],
                "server": d.get("server")}
    return None


def _adb_unauth_shell(f: Fact) -> Optional[dict]:
    """Android Debug Bridge in TCP mode accepted a connection with NO auth
    challenge — a full remote shell (adb shell / push / install) to anyone who can
    reach the port. Read from mobile_scanner's own `unauthenticated_shell`."""
    d = _d(f)
    if d.get("unauthenticated_shell") is True:
        return {"adb_version": d.get("adb_version"), "note": d.get("note")}
    return None


def _mcp_ai_unauth(f: Fact) -> Optional[dict]:
    """An AI inference / MCP endpoint (Ollama, vLLM, LM Studio, an MCP server)
    answered discovery with no authentication. Exposed inference is model/prompt
    data exposure and, for MCP tool servers, reachable tool execution. Reads the
    scanner's own `unauthenticated_access` plus its calibrated confidence."""
    d = _d(f)
    if d.get("unauthenticated_access") is True and d.get("auth_enforced") is False:
        return {"kind": d.get("kind"), "path": d.get("path"),
                "model_count": d.get("model_count"),
                "evidence_reason": d.get("evidence_reason")}
    return None


# ── the rule pack ─────────────────────────────────────────────────────────────
def _db_unauthenticated(f: Fact) -> Optional[dict]:
    """A database that served data to an UNAUTHENTICATED probe.

    The strongest statement db_scan can make, and it rests on a command the
    server actually executed for an anonymous client — Redis INFO returning
    server data, or MongoDB serverStatus succeeding. It is never inferred from a
    banner, a port number, or a handshake that would have succeeded anyway:
    MongoDB's isMaster answers without credentials even on a fully hardened
    server, which is precisely why it is not the signal used here.
    """
    d = _d(f)
    if d.get("db") is True and d.get("unauthenticated_read") is True:
        return {"engine": d.get("engine"),
                "server_version": d.get("server_version"),
                "auth_required": d.get("auth_required")}
    return None


def _db_cleartext_transport(f: Fact) -> Optional[dict]:
    """A database listener that cannot negotiate TLS at all.

    `ssl_supported is False` is a POSITIVE negative — the server stated its own
    capability (MySQL omitting CLIENT_SSL from its flags, a TDS PRELOGIN reply of
    ENCRYPT_NOT_SUP). A MISSING key means the probe never learned it, and the
    rule stays silent: absent evidence must not become a cleartext finding
    against a server that may well be hardened.
    """
    d = _d(f)
    if d.get("db") is True and d.get("ssl_supported") is False:
        return {"engine": d.get("engine"),
                "server_version": d.get("server_version"),
                "encryption_mode": d.get("encryption_mode")}
    return None


def _db_auth(f: Fact) -> Optional[bool]:
    """Auth posture for risk shaping — only when the server stated it."""
    v = _d(f).get("auth_required")
    return v if isinstance(v, bool) else None


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
        fp_notes="Fires only on a protocol-level proof (NTP monlist, DNS open recursion, "
                 "unauthenticated memcached stats, chargen reply) or a measured factor at "
                 "the TA14-017A threshold. A service that merely answered a normal query "
                 "(e.g. DNS with recursion off) is exposure, not an amplifier.",
        requires=()),   # OR-alternative signals (monlist/open_recursion/service) — no single required path
    PostureRule(
        "POSTURE-SIP-EXPOSED", "SIP service exposed", "low", "CWE-200", "T1595.002",
        "exposure", ("udp_scan",), _sip_exposed,
        "Restrict UDP/TCP 5060 (and 5061) to the SIP trunks and phones that need it, disable "
        "unauthenticated OPTIONS/REGISTER responses to unknown sources, and rate-limit "
        "registration attempts. Exposed SIP is a routine target for extension enumeration, "
        "credential brute force and toll fraud.",
        fp_notes="Fires only when the service returned a real SIP status line. An expected "
                 "PBX/SBC is normal; the finding is about who can reach it.",
        requires=()),
    PostureRule(
        "POSTURE-UPNP-IGD-EXPOSED", "UPnP Internet Gateway Device exposed", "medium",
        "CWE-306", "T1599", "exposure", ("iot_scan",), _upnp_igd_exposed,
        "Turn off UPnP IGD on the router or firewall (or restrict it to a trusted consumer "
        "VLAN), and never answer UPnP on the WAN side. Review the current port-mapping table "
        "and remove mappings nobody owns: malware uses IGD to open inbound ports without any "
        "authentication (and, WAN-facing, to proxy traffic: \"UPnProxy\").",
        fp_notes="Fires only when the device announced an Internet Gateway Device / WAN "
                 "connection service in its SSDP reply or description. A consumer router on "
                 "a home or guest segment is expected; the finding is about who can reach it.",
        requires=()),
    PostureRule(
        "POSTURE-UPNP-EXPOSED", "UPnP / SSDP responder exposed", "low", "CWE-200", "T1046",
        "exposure", ("iot_scan",), _upnp_exposed,
        "Disable UPnP/SSDP on devices that do not need discovery, and block UDP/1900 between "
        "segments and at the perimeter. SSDP answers reveal device make, model and firmware, "
        "and exposed responders are used for reflection and CallStranger-style "
        "(CVE-2020-12695) callback abuse.",
        fp_notes="Fires on a real SSDP reply (ST/USN/LOCATION present) to a unicast "
                 "M-SEARCH. Printers, TVs and media devices commonly answer on a LAN; an "
                 "Internet Gateway Device is the separate, higher rule.",
        requires=()),
    PostureRule(
        "POSTURE-NETBIOS-EXPOSED", "NetBIOS name service exposed", "low", "CWE-200", "T1046",
        "exposure", ("udp_scan",), _netbios_exposed,
        "Block UDP/137 (and 138/139) from untrusted networks and disable NetBIOS over TCP/IP on "
        "hosts that do not need it. The name service discloses host, domain and MAC details and "
        "is a poisoning (NBT-NS/LLMNR) target.",
        fp_notes="Fires only when the node-status query was answered. Common on internal "
                 "Windows networks; a finding at trust boundaries.",
        requires=()),
    PostureRule(
        "POSTURE-MDNS-EXPOSED", "mDNS responder exposed beyond the local link", "low", "CWE-200",
        "T1046", "exposure", ("udp_scan",), _mdns_exposed,
        "Keep multicast DNS on the local link: block UDP/5353 from routed networks and disable "
        "the responder (Avahi/Bonjour) on servers that do not need service discovery. It "
        "discloses hostnames and services and can be used as a reflection source.",
        fp_notes="Fires only when a unicast query got an mDNS response (QR bit set).",
        requires=()),
    PostureRule(
        "POSTURE-XDMCP-WILLING", "XDMCP display manager offers a remote X login", "high",
        "CWE-319", "T1021", "exposure", ("udp_scan",), _xdmcp_willing,
        "Disable XDMCP in the display manager (GDM: Enable=false under [xdmcp] in "
        "/etc/gdm3/custom.conf; LightDM: enabled=false under [XDMCPServer]; xdm: "
        "DisplayManager.requestPort: 0) and block UDP/177 at the network boundary. For remote "
        "desktops use SSH with X11 forwarding, or VNC/RDP behind a VPN.",
        fp_notes="Fires only on an XDMCP Willing reply to the agent's Query: the display "
                 "manager itself offered this host a login. Silence neither raises nor clears it.",
        requires=()),
    PostureRule(
        "POSTURE-XDMCP-EXPOSED", "XDMCP display manager reachable", "low", "CWE-200",
        "T1046", "exposure", ("udp_scan",), _xdmcp_exposed,
        "Disable XDMCP if remote X logins are not needed; otherwise restrict it with the "
        "display manager's access list (Xaccess) and block UDP/177 from untrusted networks.",
        fp_notes="Fires on an XDMCP Unwilling reply: the service runs and answers but refused "
                 "this host. Its access list may still offer other hosts a login.",
        requires=()),
    PostureRule(
        "POSTURE-IKE-AGGRESSIVE-MODE", "IKE aggressive mode offered", "medium", "CWE-522",
        "T1110.002", "weak_crypto", ("udp_scan",), _ike_aggressive,
        "Disable IKEv1 aggressive mode and use main mode or IKEv2 with certificates or a "
        "long random pre-shared key. In aggressive mode the identity and a PSK-derived hash "
        "cross the wire unprotected and can be attacked offline.",
        fp_notes="Fires only when the responder's reply used exchange type 4 (aggressive). "
                 "The current probe sends an IKEv2 request, so this stays silent until a "
                 "responder is shown answering in aggressive mode.",
        requires=()),
    PostureRule(
        "POSTURE-UNIDENTIFIED-SERVICE", "Unidentified service listening", "low", "CWE-1188",
        "T1046", "exposure", ("service_banner",), _unidentified_service,
        "Find out what is listening: identify the owning process (ss -ltnp / netstat -ano), "
        "confirm it is approved, and close or firewall it if it is not. Management and discovery "
        "protocols (Smart Install, SLP, Radmin, AFP, EPMD, BGP) are common on non-standard ports "
        "and should not be reachable from untrusted networks.",
        fp_notes="The banner stage opened the port and nothing identified the service. This is a "
                 "prompt to look, not a verdict: legitimate custom or binary protocols look the "
                 "same. Ports in the exposure catalog, silent-by-design protocols and the "
                 "ephemeral range are excluded.",
        requires=(), evidence_basis="port_inference", unless_explained=True),
    PostureRule(
        "POSTURE-SNMPV3-NOAUTH-USER", "SNMPv3 user accepted without authentication", "high",
        "CWE-306", "T1078", "misconfiguration", ("snmp_scan",), _snmpv3_noauth,
        "Set every SNMPv3 user to authPriv (SHA-2 authentication and AES privacy) and delete "
        "users configured at noAuthNoPriv; restrict SNMP to the management network.",
        fp_notes="Fires only when a read at noAuthNoPriv got a GetResponse for a documented "
                 "default user name. An agent that answers with a Report (unknown user) is the "
                 "secure outcome and never fires this.",
        requires=()),
    PostureRule(
        "POSTURE-FTP-ANONYMOUS-WRITE", "FTP allows anonymous upload", "critical",
        "CWE-732", "T1105", "misconfiguration", ("ftp_scan",), _ftp_anonymous_write,
        "Remove write permission from the anonymous account on every directory (vsftpd "
        "anon_upload_enable=NO, anon_mkdir_write_enable=NO) or disable anonymous access.",
        fp_notes="Proven by a completed upload, only when the operator opted in to the write "
                 "test. Not tested (anon_write is None) is never treated as read-only.",
        requires=()),
    PostureRule(
        "POSTURE-SNMP-DEFAULT-COMMUNITY", "SNMP default community string",
        "high", "CWE-1392", "T1078", "default_credentials", ("snmp_scan",), _snmp_default,
        "Change the community string; move to SNMPv3 with auth+priv; restrict by ACL.",
        fp_notes="snmp_scan is in the validated trust tier (default community verified "
                 "on the lab rig), so a community that answered is CONFIRMED.",
        requires=("community",)),

    PostureRule(
        "POSTURE-OS-END-OF-LIFE", "Operating system is end-of-life / unsupported",
        "high", "CWE-1104", "T1190", "eol_software", ("os_fingerprint", "ssh_scan"), _os_eol,
        "Upgrade to a vendor-supported OS release. An unsupported OS receives no "
        "security patches, so known vulnerabilities accumulate permanently and no "
        "amount of hardening closes them.",
        fp_notes="Fires only on a release string present in the curated EOL "
                 "catalog (eol_catalog.py), matched longest-key-first so a "
                 "supported successor never inherits its ancestor's date. An OS "
                 "absent from the catalog stays silent rather than guessing — the "
                 "cost is catalog freshness, never a false accusation. The release "
                 "comes from os_fingerprint (SMB build) or a distribution SSH "
                 "banner; a host where neither names it is reported unassessed, "
                 "and a build two editions share (17763: Windows 10 1809 / "
                 "Server 2019) is never called end-of-life.",
        # OR-alternative inputs (os_release on os_fingerprint, banner on ssh_scan),
        # so no single required path; an unidentified release is reported by the
        # detector as Undetermined (unassessed), not as drift.
        requires=(),
        host_level=True),

    PostureRule(
        "POSTURE-DEFAULT-CRED-CANDIDATE", "Device may still use vendor default credentials",
        "high", "CWE-1392", "T1078.001", "default_credentials",
        ("web_scan",), _default_cred_candidate,
        "Change the device's default administrator password; where the platform "
        "supports it, disable or rename the default account and require a "
        "password change on first login.",
        fp_notes="A CANDIDATE, not a confirmation: Vedha never attempts the "
                 "credential, so this says 'this vendor ships defaults and a "
                 "login is reachable', not 'the default works'. Confirmation is a "
                 "separate RoE-gated active-validation step. Requires BOTH a "
                 "catalogued vendor and an observed login surface; neither alone "
                 "fires. Scoped to web_scan because that is the only scanner that "
                 "emits auth_surface today — extend BOTH the emitter and this "
                 "tuple together, or the fact-contract gate will (correctly) fail. "
                 "web_scan is not in the validated trust tier, so findings land "
                 "SUSPECTED.",
        requires=("auth_surface",)),

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
        fp_notes="Fires only on algorithms with a practical attack (RC4, 3DES, DES, "
                 "Blowfish, MD5, Logjam-class groups, no encryption). Merely deprecated ones "
                 "(SHA-1 MACs, CBC) are POSTURE-SSH-LEGACY-ALGORITHMS. Offering a weak "
                 "algorithm is not proof it is negotiated — but it is reachable by any client "
                 "that asks for it.",
        requires=("ssh_confirmed", "failures")),
    PostureRule(
        "POSTURE-SSH-LEGACY-ALGORITHMS", "SSH offers legacy algorithms",
        "low", "CWE-327", "T1040", "weak_crypto", ("ssh_scan",), _ssh_legacy_algos,
        "Retire the deprecated algorithms (SHA-1 MACs, CBC ciphers, 1024-bit DH groups) from "
        "KexAlgorithms, Ciphers and MACs in sshd_config when clients allow; prefer curve25519 / "
        "ed25519 over the NIST curves where your policy requires it. Nothing here has a "
        "practical attack today; this is hygiene, not an emergency.",
        fp_notes="Every algorithm ssh-audit fails is deprecated or weak-by-policy but none is on "
                 "the broken list (RC4, 3DES, DES, Blowfish, MD5, Logjam-class groups). A stock "
                 "current OpenSSH offers hmac-sha1 and the NIST curves (failed by ssh-audit as "
                 "\"suspected backdoored\", a trust concern, not an attack) and lands here, "
                 "not under the High rule.",
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
    # ── database (db_scan) ────────────────────────────────────────────────────
    # db_scan ran on every network_va, shipped facts, and had ZERO rules: its
    # evidence was collected and never assessed, so an open Redis looked exactly
    # like a hardened one. These two read only what the server itself stated.
    PostureRule(
        "POSTURE-DB-UNAUTHENTICATED-ACCESS",
        "Database served data without authentication",
        "critical", "CWE-306", "T1213", "misconfiguration", ("db_scan",),
        _db_unauthenticated,
        "Require authentication and restrict the listener to the application "
        "tier. Redis: set requirepass or enable ACLs and bind to the app network "
        "only. MongoDB: enable authorization and create an admin user. Treat "
        "data held here as disclosed until the exposure window is established.",
        fp_notes="Raised only when an anonymous command actually RETURNED server "
                 "data (Redis INFO, MongoDB serverStatus). MongoDB isMaster is "
                 "deliberately not used: it answers without credentials even when "
                 "authorization is enforced, so it would flag hardened servers.",
        auth_enforced=_db_auth,
        # ONLY the universal marker. `unauthenticated_read` is emitted by the
        # engines whose protocol offers a public INFO ping (Redis, MongoDB) and
        # not by MySQL/Postgres/MSSQL — declaring it would make every MySQL host
        # report schema_drift, turning the drift signal that exists to catch real
        # probe regressions into noise nobody reads.
        requires=("db",)),
    PostureRule(
        "POSTURE-DB-CLEARTEXT-TRANSPORT",
        "Database listener cannot negotiate TLS",
        "medium", "CWE-319", "T1040", "weak_crypto", ("db_scan",),
        _db_cleartext_transport,
        "Enable TLS on the listener and require encrypted connections "
        "(MySQL require_secure_transport=ON, PostgreSQL ssl=on with hostssl-only "
        "rules, SQL Server ForceEncryption). Until then every credential and "
        "every row crosses the network in plaintext.",
        fp_notes="Fires only on the server's OWN statement that it cannot "
                 "encrypt. A probe that never reached the capability flags emits "
                 "no ssl_supported key at all, and this rule stays silent rather "
                 "than reading silence as cleartext. auth_enforced is NOT set: "
                 "authentication in front does not protect a cleartext channel, "
                 "it just means credentials are what crosses it.",
        # Same reasoning as above, mirrored: `ssl_supported` comes from MySQL,
        # Postgres and MSSQL, never from Redis or MongoDB.
        requires=("db",)),

    # ── additional service-layer rules (previously-unconsumed facts) ──────────
    # Collected by the probe, shipped, stored, and never assessed until now. None
    # of these scanners is rig-validated, so findings land SUSPECTED (_state_for).
    PostureRule(
        "POSTURE-TLS-WEAK-KEY", "TLS certificate uses a weak public key",
        "high", "CWE-326", "T1040", "weak_crypto", ("tls_scan",), _tls_weak_key,
        "Reissue the certificate with a >=2048-bit RSA key (or a >=256-bit "
        "elliptic-curve key). Keys below this are below every current CA/Browser "
        "Forum and NIST baseline and are brute-forceable over the cert's lifetime.",
        fp_notes="Fires only when the probe POSITIVELY parsed the key type and bit "
                 "size (the full-cert-parse path). A degraded byte-count-only parse "
                 "emits neither and this stays silent.",
        requires=("certificate",)),
    PostureRule(
        "POSTURE-TLS-WEAK-SIGNATURE", "TLS certificate signed with a broken hash (MD5/SHA-1)",
        "high", "CWE-327", "T1557", "weak_crypto", ("tls_scan",), _tls_weak_sig,
        "Reissue the certificate with a SHA-256 (or stronger) signature. MD5 and "
        "SHA-1 are collision-broken, so a signature over them no longer binds the "
        "certificate to its CA — a forged chain becomes feasible.",
        fp_notes="An internally-rooted self-signed cert may use a legacy hash by "
                 "oversight; evidence.self_signed distinguishes that case.",
        requires=("certificate",)),
    PostureRule(
        "POSTURE-WEB-DANGEROUS-METHODS", "Dangerous HTTP methods enabled",
        "medium", "CWE-650", "T1505", "misconfiguration", ("web_scan",),
        _web_dangerous_methods,
        "Disable PUT/DELETE/TRACE/CONNECT/PATCH unless a documented API needs them; "
        "PUT can upload a webshell, TRACE enables Cross-Site Tracing, and CONNECT "
        "turns the server into an open forward proxy.",
        fp_notes="Read from the OPTIONS Allow header the server itself returned. A "
                 "REST API that legitimately uses PUT/PATCH/DELETE should be scoped "
                 "to its authenticated routes — confirm before treating as a defect.",
        requires=("dangerous_methods",)),
    PostureRule(
        "POSTURE-WEB-NO-HSTS", "HTTPS service does not set HSTS",
        "low", "CWE-319", "T1040", "weak_crypto", ("web_scan",), _web_missing_hsts,
        "Send Strict-Transport-Security with a long max-age (and preload where "
        "appropriate) so the browser refuses to downgrade to cleartext after the "
        "first visit.",
        fp_notes="Scoped to TLS services and to the HSTS header specifically, so it "
                 "does not fire as a blanket 'security headers missing' lint.",
        requires=("security_headers_missing",)),
    PostureRule(
        "POSTURE-DNS-VERSION-DISCLOSURE", "DNS server discloses its version (version.bind)",
        "low", "CWE-200", "T1590.002", "information_disclosure", ("dns_scan",),
        _dns_version_disclosure,
        "Override or suppress the CHAOS TXT version.bind response (BIND: "
        "`version \"\";`) so the exact resolver software/version is not disclosed "
        "to anonymous clients.",
        fp_notes="Fires only when a non-empty, non-refused version string was "
                 "returned — a server that answers 'refused'/empty never fires it.",
        requires=("dns", "version_bind")),
    PostureRule(
        "POSTURE-LDAP-ANONYMOUS-SEARCH", "LDAP anonymous search returns directory content",
        "medium", "CWE-200", "T1087.002", "information_disclosure", ("ldap_scan",),
        _ldap_anonymous_search,
        "Disable anonymous SEARCH (set dsHeuristics / require authentication) so "
        "usernames, groups and host objects cannot be enumerated without "
        "credentials — anonymous callers should at most read the RootDSE.",
        fp_notes="Distinct from, and more serious than, POSTURE-LDAP-ANONYMOUS-BIND: "
                 "this fires only when a search actually returned directory entries "
                 "(anonymous_search_allowed), not merely a successful bind.",
        requires=("ldap", "anonymous_search_allowed")),
    PostureRule(
        "POSTURE-SNMP-AMPLIFIER", "SNMP agent usable as a DDoS amplifier",
        "medium", "CWE-406", "T1498.002", "amplification", ("snmp_scan",),
        _snmp_amplification,
        "Restrict SNMP to trusted managers by ACL, move to SNMPv3, and disable "
        "GETBULK on large tables for untrusted sources — a readable agent with a "
        "high response/request ratio is a reflective-DDoS source.",
        fp_notes="Keyed off the MEASURED GETBULK amplification_factor, not a port "
                 "guess; only fires at or above the TA14-017A SNMPv2 factor (6.3x).",
        requires=()),   # amplification_factor only present when the walk measured it
    PostureRule(
        "POSTURE-MQTT-UNAUTHENTICATED", "MQTT broker accepts unauthenticated clients",
        "high", "CWE-306", "T1133", "misconfiguration", ("iot_scan",), _iot_mqtt_unauth,
        "Require username/password (or mutual TLS) on the broker and deny anonymous "
        "CONNECT. An open broker lets any client subscribe to '#' and read or inject "
        "every message — telemetry, commands and often credentials.",
        fp_notes="Fires on a CONNACK return code 0 (accepted) to an anonymous "
                 "CONNECT; a broker that refuses (rc 4/5) never fires it.",
        requires=()),   # iot_scan multiplexes protocols — no single required path
    PostureRule(
        "POSTURE-CWMP-EXPOSED", "TR-069/CWMP management interface exposed",
        "medium", "CWE-284", "T1190", "exposure", ("iot_scan",), _iot_cwmp_exposed,
        "Firewall TCP/7547 from untrusted networks and restrict CWMP to the ACS "
        "management path. CWMP/TR-064 on the WAN side is the documented Mirai worm "
        "vector and a remote device-management surface.",
        fp_notes="Derived from CWMP/ACS indicators in the HTTP response; a plain web "
                 "server on the port without those markers does not fire it.",
        requires=()),
    PostureRule(
        "POSTURE-RTSP-EXPOSED", "RTSP camera/streaming endpoint exposed",
        "medium", "CWE-284", "T1021", "exposure", ("iot_scan",), _iot_rtsp_exposed,
        "Restrict RTSP (554/8554) to trusted networks or a VPN and enforce "
        "authentication — IP cameras and NVRs frequently ship with default or no "
        "credentials, making an exposed stream directly viewable.",
        fp_notes="Fires on an RTSP OPTIONS method list returned by the device; the "
                 "scanner never attempts to open a stream.",
        requires=()),
    PostureRule(
        "POSTURE-ADB-UNAUTHENTICATED", "Android Debug Bridge exposes an unauthenticated shell",
        "critical", "CWE-306", "T1021", "misconfiguration", ("mobile_scan",),
        _adb_unauth_shell,
        "Disable ADB over TCP (`adb tcpip` / setprop service.adb.tcp.port -1) or "
        "firewall 5555. An open ADB daemon grants a full remote shell — app install, "
        "file push/pull and command execution — to anyone who can reach the port.",
        fp_notes="Fires only on a CNXN reply with no AUTH challenge "
                 "(unauthenticated_shell). A device that answers AUTH never fires it.",
        requires=()),
    PostureRule(
        "POSTURE-AI-ENDPOINT-UNAUTHENTICATED", "AI/MCP inference endpoint exposed without auth",
        "high", "CWE-306", "T1133", "misconfiguration", ("mcp_ai_scan",), _mcp_ai_unauth,
        "Put the inference/MCP endpoint behind authentication (API key / OAuth / a "
        "reverse proxy) and bind it to the application network. An open endpoint is "
        "model and prompt-data exposure, resource abuse, and — for MCP tool servers "
        "— reachable tool execution.",
        fp_notes="Fires only when the scanner confirmed an unauthenticated response "
                 "(auth_enforced is False); an endpoint that returns a real auth "
                 "challenge is reported auth_enforced and never fires this.",
        requires=()),
]


# Credentialed inventory collectors read the host's OWN authoritative state
# (installed packages, the real service table, Defender status, the process list)
# over an authenticated session — the strongest evidence tier there is, stronger
# than any network protocol observation. ingest.py already tags their facts
# SourceConfidence.authoritative; a posture finding derived from them is therefore
# CONFIRMED, exactly like a validated-scanner direct observation. Mirrors
# ingest._AUTHORITATIVE_SCANNERS.
CREDENTIALED_SCANNERS: frozenset = frozenset({"ssh_inventory", "windows_inventory"})


def is_credentialed(scanner: str) -> bool:
    return scanner in CREDENTIALED_SCANNERS


# ── runner ────────────────────────────────────────────────────────────────────
# How the evidence behind a finding was obtained. Separate from WHICH scanner saw it: a
# validated port scanner proves the port is open, not that the service on it is what the
# port number suggests.
BASIS_PROTOCOL_OBSERVED = "protocol_observed"   # a protocol-level answer (flag, status byte, handshake)
BASIS_BANNER_INFERENCE = "banner_inference"     # a banner/port heuristic, no protocol proof
BASIS_PORT_INFERENCE = "port_inference"         # only "this port is open"
EVIDENCE_BASES = frozenset({BASIS_PROTOCOL_OBSERVED, BASIS_BANNER_INFERENCE, BASIS_PORT_INFERENCE})


def _state_for(scanner: str, basis: str = BASIS_PROTOCOL_OBSERVED) -> str:
    """CONFIRMED needs both a trusted scanner AND a protocol-level observation. An
    inference (open port, banner heuristic) is at most SUSPECTED whoever saw the port —
    the same discipline as matcher.py's `source_confidence == authoritative` gate."""
    if basis != BASIS_PROTOCOL_OBSERVED:
        return FindingState.suspected.value
    if is_validated(scanner) or is_credentialed(scanner):
        return FindingState.confirmed.value
    return FindingState.suspected.value


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
    if isinstance(ev, Undetermined):
        return TraceRow(rule.rule_id, f.scanner, OUTCOME_NO_EVIDENCE,
                        f.target, f.port, reason=ev.reason)
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
    # Ports a dedicated scanner reported open: those are explained, whatever the banner said.
    _generic = {"port_scan", "syn_scan", "mass_scan", "service_banner", "udp_scan",
                "host_discovery", "os_fingerprint", "exposure_matrix"}
    explained_ports = {(x.port, x.proto or "tcp") for x in asset.facts
                       if x.scanner not in _generic and x.port and x.status == "open"}
    for f in asset.facts:
        for rule in RULES:
            if f.scanner not in rule.scanners:
                continue
            if rule.unless_explained and (f.port, f.proto or "tcp") in explained_ports:
                continue
            row = evaluate_rule(rule, f)
            traces.append(row)
            if row.outcome != OUTCOME_MATCH:
                continue
            port = None if rule.host_level else f.port
            key = (rule.rule_id, port)
            if key in seen:                       # same weakness, same port → one finding
                continue
            seen.add(key)

            state = _state_for(f.scanner, rule.evidence_basis)
            auth = (rule.auth_enforced(f) if rule.auth_enforced else None)
            if auth is None:
                auth = default_auth
            risk, priority = compute_risk(rule.severity, state, internet_facing, auth)
            pf = PostureFinding(
                finding_id=make_posture_id(asset.ip, rule.rule_id, port),
                asset_ip=asset.ip, rule_id=rule.rule_id, title=rule.title,
                category=rule.category, severity=rule.severity, state=state,
                confidence=_STATE_CONF.get(state, 65), cwe=rule.cwe, mitre=rule.mitre,
                port=port, proto=f.proto, evidence_refs=[_evidence_ref(f)],
                evidence={**(row.evidence or {}), "evidence_basis": rule.evidence_basis,
                          DEDUP_KEY: condition_key_for(rule.rule_id, rule.category,
                                                       port, f.proto)},
                remediation=rule.remediation,
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
        ex_findings, ex_traces = detect_exposed_services_traced(asset, exposure)
        out.extend(ex_findings)
        traces.extend(ex_traces)
    except Exception:  # noqa: BLE001 — must never sink core detection
        pass

    # 1a-ii) Credentialed host-posture / IOA layer: the authoritative Windows/Linux
    #     inventory the probe collects over an authenticated session (Defender state,
    #     the real service table, local admins, the process/listener list) that no
    #     network scanner can see and no rule read until now. CONFIRMED tier. Returns
    #     its findings already keyed and risk-scored; best-effort, never sinks core.
    try:
        from host_posture import detect_host_posture_traced   # local, no import cycle
        hp_findings, hp_traces = detect_host_posture_traced(asset, exposure)
        for pf in hp_findings:
            reachable_by_id[id(pf)] = True   # credentialed = host confirmed reachable
        out.extend(hp_findings)
        traces.extend(hp_traces)
    except Exception:  # noqa: BLE001 — must never sink core detection
        pass

    # 1a-iii) TLS fingerprint threat-intel (IOC) layer: match the JARM/JA4S/JA4X
    #     fingerprints the probe computed against a curated registry of known C2 /
    #     tooling TLS profiles. The manager computed and stored these fingerprints
    #     and matched none of them until now. SUSPECTED by design. Best-effort.
    try:
        from fingerprint_intel import detect_fingerprint_intel_traced
        fi_findings, fi_traces = detect_fingerprint_intel_traced(asset, exposure)
        out.extend(fi_findings)
        traces.extend(fi_traces)
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
    "printer":       "Printer raw-print port open on {port} ({svc})",
}


def _exposed_title(category: str, service: str, port: int, internet: bool) -> str:
    base = _EXPOSED_TITLES.get(category, "Service exposed on {port}").format(
        port=port, svc=service)
    return base + (" — internet-facing" if internet else "")


def _scan_summary_spans(asset: Asset):
    """Yield (state, lo, hi) from every scan_summary fact's run-length-encoded
    port_states. This is the only place a definitively CLOSED port survives —
    the port scanners emit open ports as facts but fold closed ones into the
    summary, so proving a formerly-exposed port is gone means reading it here."""
    for f in asset.facts:
        if f.status != "scan_summary":
            continue
        d = f.data if isinstance(f.data, dict) else {}
        ps = d.get("port_states")
        if not isinstance(ps, dict):
            continue
        for state, spans in ps.items():
            if not isinstance(spans, (list, tuple)):
                continue
            for span in spans:
                if (isinstance(span, (list, tuple)) and len(span) == 2
                        and isinstance(span[0], int) and isinstance(span[1], int)
                        and not isinstance(span[0], bool)
                        and not isinstance(span[1], bool) and span[1] >= span[0]):
                    yield state, span[0], span[1]


def _scan_summary_scanner(asset: Asset) -> str:
    for f in asset.facts:
        if f.status == "scan_summary" and f.scanner:
            return f.scanner
    return "port_scan"


def _summary_closed_ports(asset: Asset, ports: set[int]) -> set[int]:
    """Of `ports`, those a scan_summary marks CLOSED with none marking open —
    definitively re-checked this run and not a live exposed service."""
    closed: set[int] = set()
    openish: set[int] = set()
    for state, lo, hi in _scan_summary_spans(asset):
        bucket = closed if state == "closed" else (openish if state == "open" else None)
        if bucket is None:
            continue
        for p in ports:
            if lo <= p <= hi:
                bucket.add(p)
    return closed - openish


def detect_exposed_services_traced(
    asset: Asset, exposure: dict[str, dict] | None = None,
) -> tuple[list[PostureFinding], list[TraceRow]]:
    """Findings for risky OPEN ports that have no dedicated scanner (backdoor/C2
    listeners, unauthenticated-prone data stores, container APIs, cleartext
    protocols, exposed admin UIs), PLUS a per-(asset, catalog port) evaluation
    trace. Reads only what the validated scanners already emit — open TCP ports
    (port/syn/mass scan), banners (service_banner), the exposure classification
    (exposure_matrix), and the port-state summary. Severity escalates one level
    when the port is internet-facing.

    The trace is what lets an exposed-service finding auto-resolve: MATCH when a
    catalog port is a live exposed service, NO_MATCH when a re-scan proves it
    clean (closed, or an open port re-identified as a benign occupant). A catalog
    port that was NOT re-scanned gets no trace, so its finding stays open —
    absence of evidence is never a clean miss."""
    from port_intel import (catalog_categories, classify_port,  # standalone, no cycle
                            exposure_severity)

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

    catalog = catalog_categories()          # port -> category (port-number hypothesis)
    now = datetime.now(timezone.utc).isoformat()
    out: list[PostureFinding] = []
    traces: list[TraceRow] = []
    evaluated: set[int] = set()             # catalog ports we reached a verdict on
    for port in sorted(open_tcp):
        if port in _EXPOSED_SVC_DEDICATED_PORTS:
            continue
        f = open_tcp[port]
        risk = classify_port(port, banners.get(port), service=svc_labels.get(port),
                             basic_auth_cleartext=port in basic_cleartext,
                             product=products.get(port))
        if risk is None:
            # The port was probed but is not (or no longer) an exposed service —
            # a benign occupant on a catalog port re-checks clean.
            cat = catalog.get(port)
            if cat is not None:
                evaluated.add(port)
                traces.append(TraceRow(
                    f"POSTURE-EXPOSED-{cat.upper()}", f.scanner, OUTCOME_NO_MATCH,
                    asset.ip, port=port,
                    reason="open port re-identified as a benign occupant"))
            continue
        internet = (port in externally) or bool(exp_internet)
        severity, bod_23_02 = exposure_severity(risk.category, risk.severity, internet)
        # A port scan proves the port is open, not what runs on it. Only a protocol-level
        # observation (service_banner's identified protocol / Basic-over-cleartext flag)
        # supports CONFIRMED; a bare port or a banner string is an inference → SUSPECTED.
        if svc_labels.get(port) or port in basic_cleartext:
            basis = BASIS_PROTOCOL_OBSERVED
        elif banners.get(port):
            basis = BASIS_BANNER_INFERENCE
        else:
            basis = BASIS_PORT_INFERENCE
        state = _state_for(f.scanner, basis)
        risk_score, priority = compute_risk(severity, state, internet, default_auth)
        rule_id = f"POSTURE-EXPOSED-{risk.category.upper()}"
        ev: dict[str, Any] = {"port": port, "category": risk.category,
                              "service": risk.service, "internet_facing": internet,
                              "evidence_basis": basis,
                              DEDUP_KEY: condition_key(CLASS_EXPOSED, port, "tcp")}
        if bod_23_02:
            # Internet-facing management interface: why it is at least High.
            ev["bod_23_02"] = True
            ev["severity_basis"] = ("internet-facing management interface "
                                    "(CISA BOD 23-02: remove from the internet or put "
                                    "behind an access-control point within 14 days)")
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
        evaluated.add(port)
        traces.append(TraceRow(rule_id, f.scanner, OUTCOME_MATCH, asset.ip, port=port,
                               reason="exposed service confirmed on this port"))

    # Catalog ports the summary shows CLOSED (and never open) were re-checked and
    # are definitively gone — the clean re-scan that resolves a stale finding.
    candidates = (set(catalog) - _EXPOSED_SVC_DEDICATED_PORTS) - evaluated
    if candidates:
        scanner_name = _scan_summary_scanner(asset)
        for port in sorted(_summary_closed_ports(asset, candidates)):
            traces.append(TraceRow(
                f"POSTURE-EXPOSED-{catalog[port].upper()}", scanner_name,
                OUTCOME_NO_MATCH, asset.ip, port=port, reason="port closed on re-scan"))
    return out, traces


def detect_exposed_services(asset: Asset,
                            exposure: dict[str, dict] | None = None) -> list[PostureFinding]:
    """Findings-only wrapper over detect_exposed_services_traced, for callers that
    do not consume the evaluation trace."""
    findings, _traces = detect_exposed_services_traced(asset, exposure)
    return findings


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
