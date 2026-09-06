"""finding_content.py — the deterministic per-finding explanation knowledge base.

Pure and offline (no DB, no network, no AI on this path): given a finding it
returns structured, human-readable content instantly — the ALWAYS-AVAILABLE spine
so a finding is never presented as a bare title + CVSS number. This is the sibling
of ``remediation_kb.py`` (which owns *how to fix*); this module owns *what it is,
why it matters, and whether it can be exploited*.

Three ideas drive the design:

1. **One category taxonomy.** We reuse ``remediation_kb.classify_finding`` rather
   than inventing a second one, so a finding's explanation and its fix can never
   describe two different problems.

2. **Epistemic honesty about exploitation.** The platform detects exposure; it does
   not (on this path) prove exploitation. So an unvalidated finding says exactly
   that — "Not validated. Absence of proof is not proof of absence." — instead of
   pretending certainty in either direction. Where third-party signals exist (CISA
   KEV, FIRST EPSS, a public PoC) they are reported as what they are.

3. **Impact scaled to the asset.** The same weakness on a throwaway host and on a
   business-critical system are not the same business risk, so ``business_impact``
   is led by the asset's criticality and amplified when the weakness is under
   active exploitation.

An optional ``overrides`` dict (AI-generated prose or an analyst's edit, persisted
in ``findings.content_overrides``) wins field-by-field over the KB — the KB remains
the floor, never a ceiling.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from app.services.finding_priority import severity_rank
from app.services.remediation_kb import classify_finding

# The exact, agreed line for a finding we have observed but not actively exploited.
# Kept as a named constant so the wording is pinned by test and reused verbatim.
NOT_VALIDATED_NOTE = (
    "Not validated. Absence of proof is not proof of absence."
)

# EPSS (FIRST exploit-prediction) bands. 0.5 ≈ top ~2% of CVEs by predicted
# exploitation; 0.1 ≈ a meaningful, non-trivial probability. These mirror the
# thresholds the industry uses to separate "act now" from "watch".
_EPSS_WEAPONIZED = 0.5
_EPSS_POC = 0.1


# ── curated content, keyed by remediation_kb category ─────────────────────────
# Each entry: technical (the mechanism/why), impact (technical consequence on the
# box), business (base business consequence — later scaled by asset criticality).
_CONTENT: dict[str, dict[str, str]] = {
    "weak_tls": {
        "technical": (
            "The service negotiates deprecated SSL/TLS versions (SSLv2/SSLv3/TLS 1.0/1.1) "
            "or weak cipher suites (RC4, 3DES, CBC-mode, export-grade). These primitives "
            "have known cryptographic flaws — padding-oracle attacks (POODLE, BEAST), RC4 "
            "keystream bias, and Sweet32 birthday collisions — that a network-positioned "
            "attacker can use to recover plaintext or force a downgrade."
        ),
        "impact": (
            "An attacker able to intercept traffic (ARP spoofing, rogue Wi-Fi, an upstream "
            "tap) can decrypt or tamper with the session, capturing credentials, session "
            "tokens, or sensitive payloads in transit."
        ),
        "business": (
            "confidential data in transit — customer records, credentials, payment data — "
            "can be exposed, and the weak channel typically fails PCI DSS and modern TLS "
            "baselines at audit."
        ),
    },
    "smb_signing": {
        "technical": (
            "SMB message signing is not required, so the server accepts unsigned sessions. "
            "Without signing, an attacker who can relay or man-in-the-middle NTLM "
            "authentication injects commands into an authenticated session (SMB/NTLM relay)."
        ),
        "impact": (
            "An attacker on the local segment can relay captured NTLM authentication to this "
            "host and act as the victim — frequently reaching code execution or privilege "
            "escalation on the target."
        ),
        "business": (
            "a single unprivileged foothold on the network can be pivoted into administrative "
            "access on this system, accelerating lateral movement and ransomware deployment."
        ),
    },
    "exposed_rdp": {
        "technical": (
            "Remote Desktop (TCP/3389) is reachable and may lack Network Level Authentication. "
            "RDP is a leading ransomware entry vector: exposed endpoints are continuously "
            "brute-forced and targeted by pre-auth vulnerabilities such as BlueKeep "
            "(CVE-2019-0708)."
        ),
        "impact": (
            "Attackers brute-force credentials or exploit an RDP pre-auth flaw to gain an "
            "interactive session, then use the host as a beachhead into the internal network."
        ),
        "business": (
            "exposed RDP is one of the most common ransomware and data-breach entry points; a "
            "successful login yields full interactive control of the system."
        ),
    },
    "default_credentials": {
        "technical": (
            "The service authenticates with a vendor-default, shared, or weak credential. "
            "Default credentials are publicly documented per product and are the first thing "
            "automated attackers try."
        ),
        "impact": (
            "Anyone who reaches the service can authenticate with a known password and obtain "
            "the account's privileges — frequently administrative."
        ),
        "business": (
            "trivial, no-skill takeover of the system and any data or downstream systems it "
            "can reach — often full administrative control."
        ),
    },
    "missing_patch": {
        "technical": (
            "The affected component runs a version with published security vulnerabilities for "
            "which the vendor has shipped a fix. The window between disclosure and patching is "
            "exactly what attackers use, especially once exploit code is public."
        ),
        "impact": (
            "Depending on the specific CVE, exploitation can yield remote code execution, "
            "denial of service, information disclosure, or privilege escalation on the host."
        ),
        "business": (
            "known, fixable vulnerabilities are the leading root cause of breaches; leaving "
            "them open invites both targeted and opportunistic (worm/ransomware) compromise."
        ),
    },
    "open_mgmt_port": {
        "technical": (
            "A management or administrative service is exposed — potentially to untrusted "
            "networks — and may use a cleartext protocol (Telnet, FTP, plain HTTP). Cleartext "
            "admin protocols carry credentials and commands with no encryption."
        ),
        "impact": (
            "An attacker who reaches the port can capture credentials off the wire or interact "
            "directly with the management plane of the device."
        ),
        "business": (
            "administrative exposure widens the attack surface of critical infrastructure; "
            "captured admin credentials can compromise the device and everything it controls."
        ),
    },
    "anon_ftp": {
        "technical": (
            "The FTP service permits anonymous login, granting unauthenticated access to its "
            "file store, and transmits data in cleartext."
        ),
        "impact": (
            "Anyone can connect without credentials to read — and sometimes write — files, "
            "exposing sensitive data or enabling malware staging."
        ),
        "business": (
            "unintended public exposure of files can leak confidential data, and writable "
            "anonymous FTP can be abused to host malicious content under your brand."
        ),
    },
    "outdated_ssh": {
        "technical": (
            "The SSH server offers weak key-exchange algorithms, CBC-mode ciphers, or weak "
            "MACs, runs an outdated OpenSSH with known CVEs, or permits legacy SSH protocol 1 "
            "— each undermining the confidentiality/integrity guarantees of the tunnel."
        ),
        "impact": (
            "Depending on the weakness, an attacker may attack or downgrade the session "
            "cryptography, or exploit a version-specific SSH CVE to gain access."
        ),
        "business": (
            "the primary secure-administration channel is weakened, risking interception of "
            "privileged sessions or direct compromise of the host."
        ),
    },
    "generic": {
        "technical": (
            "The service exhibits a security weakness in its exposure or configuration. Review "
            "the specific evidence below and the vendor's hardening guidance for the affected "
            "component."
        ),
        "impact": (
            "The weakness may let an attacker access, disrupt, or extract information from the "
            "service beyond its intended use."
        ),
        "business": (
            "unaddressed exposure raises both the likelihood and the impact of a compromise of "
            "this asset."
        ),
    },
}

# Asset-criticality lead-in for business impact. Empty for medium/low/unknown so
# ordinary systems read plainly; critical/high get an explicit blast-radius framing.
_CRITICALITY_LEAD: dict[str, str] = {
    "critical": "This system is business-critical, so the blast radius is high — ",
    "high": "This is a high-value system, so ",
}


@dataclass
class ExploitationView:
    """The honest exploitation posture of a finding.

    ``status`` is 'validated' only when the platform actively proved exploitation
    (or a trusted feed marks it exploited-in-the-wild); otherwise 'not_validated'
    and ``note`` carries the epistemic-honesty line plus any third-party signal.
    """

    status: str
    maturity: str
    actively_exploited: bool
    summary: str
    note: str
    signals: dict[str, Any] = field(default_factory=dict)


@dataclass
class FindingContent:
    category: str
    impact: str
    business_impact: str
    technical_details: str
    exploit_maturity: str
    actively_exploited: bool
    exploitation: ExploitationView

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "impact": self.impact,
            "business_impact": self.business_impact,
            "technical_details": self.technical_details,
            "exploit_maturity": self.exploit_maturity,
            "actively_exploited": self.actively_exploited,
            "exploitation": asdict(self.exploitation),
        }


def _evidence(finding: Any) -> dict[str, Any]:
    ev = getattr(finding, "evidence", None)
    return ev if isinstance(ev, dict) else {}


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def exploitation_signals(finding: Any) -> dict[str, Any]:
    """Extract the raw exploitation signals from a finding + its evidence.

    Never guesses: KEV/PoC default False and EPSS defaults None when unrecorded,
    so downstream logic distinguishes 'known-safe-ish' from 'simply unknown'.
    """
    ev = _evidence(finding)
    enr = ev.get("enrichment") if isinstance(ev.get("enrichment"), dict) else {}
    kev = bool(ev.get("kev") or enr.get("kev"))
    validated = bool(getattr(finding, "exploit_validated", False))
    epss = _float_or_none(
        getattr(finding, "epss_score", None)
        if getattr(finding, "epss_score", None) is not None
        else enr.get("epss")
    )
    poc = bool(ev.get("poc_available") or ev.get("poc") or enr.get("poc") or enr.get("poc_available"))
    return {"kev": kev, "validated": validated, "epss": epss, "poc": poc}


def exploit_maturity(signals: dict[str, Any]) -> str:
    """Map exploitation signals to the frontend maturity enum.

    WEAPONIZED — proven/near-certain exploitation (validated, on CISA KEV, or a
    very high EPSS). POC — a public proof-of-concept or a non-trivial EPSS.
    THEORETICAL — no public exploit signal today (which can change).
    """
    epss = signals.get("epss")
    if signals.get("kev") or signals.get("validated") or (epss is not None and epss >= _EPSS_WEAPONIZED):
        return "WEAPONIZED"
    if signals.get("poc") or (epss is not None and epss >= _EPSS_POC):
        return "POC"
    return "THEORETICAL"


def detection_method(finding: Any) -> str | None:
    """How the finding was ESTABLISHED, as the frontend confidence enum
    (exploit | behavioural | configuration | credentialed | version | banner |
    inference). Derived only from genuine validation signals; detection COVERAGE
    (a blue-team signal) is deliberately NOT consulted, since it says nothing
    about how the weakness was proven. ``None`` ⇒ the UI shows "Unverified".
    """
    if bool(getattr(finding, "exploit_validated", False)):
        return "exploit"
    state = str(getattr(finding, "verification_state", "") or "").lower()
    if state == "confirmed":
        return "behavioural"
    if state == "corroborated":
        return "inference"
    return None


def _build_exploitation(signals: dict[str, Any], maturity: str) -> ExploitationView:
    actively_exploited = bool(signals.get("kev") or signals.get("validated"))
    if signals.get("validated"):
        return ExploitationView(
            status="validated",
            maturity=maturity,
            actively_exploited=True,
            summary="The platform actively validated this weakness on the target.",
            note="Confirmed exploitable — treat as an active, demonstrated risk.",
            signals=signals,
        )

    # Not validated by us — say so, then add whatever trustworthy external signal exists.
    if signals.get("kev"):
        context = (
            " However, this vulnerability is on the CISA Known Exploited Vulnerabilities "
            "list — it is being exploited in the wild right now — so treat it as exploitable."
        )
    elif maturity == "WEAPONIZED":
        context = (
            " However, exploit-prediction scoring places it in the highest exploitation band, "
            "so weaponization is likely — treat it as exploitable."
        )
    elif maturity == "POC":
        context = (
            " Public proof-of-concept code or a meaningful exploit-prediction score exists, so "
            "the barrier to exploitation is low."
        )
    else:
        context = (
            " No public exploit is currently known for this weakness, but that can change at "
            "any time and does not make the exposure safe."
        )
    return ExploitationView(
        status="not_validated",
        maturity=maturity,
        actively_exploited=actively_exploited,
        summary="This finding reflects observed exposure, not a demonstrated exploit.",
        note=NOT_VALIDATED_NOTE + context,
        signals=signals,
    )


def _scale_business_impact(base: str, *, asset_criticality: str | None, severity: Any,
                           actively_exploited: bool) -> str:
    lead = _CRITICALITY_LEAD.get((asset_criticality or "").lower(), "")
    # Capitalize the base sentence only when there is no lead-in prefix.
    body = base if lead else (base[:1].upper() + base[1:] if base else base)
    text = f"{lead}{body}".rstrip()
    if not text.endswith("."):
        text += "."
    if actively_exploited and severity_rank(severity) >= severity_rank("high"):
        text += (
            " Because this weakness is under active exploitation, prioritise remediation ahead "
            "of the normal SLA."
        )
    return text


def _technical_with_cves(base: str, finding: Any) -> str:
    cves = [str(c).upper() for c in (getattr(finding, "cve_ids", None) or [])]
    if not cves:
        return base
    shown = ", ".join(cves[:6])
    more = f" (+{len(cves) - 6} more)" if len(cves) > 6 else ""
    return f"{base} Associated CVEs: {shown}{more}."


def finding_content(finding: Any, *, asset_criticality: str | None = None,
                    overrides: dict[str, Any] | None = None) -> FindingContent:
    """Build the deterministic explanation + exploitation content for a finding.

    ``asset_criticality`` scales the business impact; ``overrides`` (persisted AI
    or analyst prose) wins field-by-field. Always returns fully-populated content
    — the ``generic`` category guarantees no empty states.
    """
    overrides = overrides or {}
    category = classify_finding(finding)
    base = _CONTENT.get(category, _CONTENT["generic"])

    signals = exploitation_signals(finding)
    maturity = exploit_maturity(signals)
    exploitation = _build_exploitation(signals, maturity)

    severity = getattr(finding, "severity", "info")
    technical = _technical_with_cves(base["technical"], finding)
    business = _scale_business_impact(
        base["business"], asset_criticality=asset_criticality, severity=severity,
        actively_exploited=exploitation.actively_exploited,
    )

    return FindingContent(
        category=category,
        impact=overrides.get("impact") or base["impact"],
        business_impact=overrides.get("business_impact") or business,
        technical_details=overrides.get("technical_details") or technical,
        exploit_maturity=maturity,
        actively_exploited=exploitation.actively_exploited,
        exploitation=exploitation,
    )
