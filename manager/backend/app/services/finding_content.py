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
    "vnc_no_auth": {
        "technical": (
            "The VNC server accepts connections without authentication (security type None) "
            "or with a trivially weak scheme. Anyone who can reach the port gets the "
            "graphical console of the machine."
        ),
        "impact": (
            "An attacker with network access gets full interactive control of the desktop as "
            "the logged-in user: they can read data on screen, run commands and install "
            "persistence, with no credential to steal or guess."
        ),
        "business": (
            "unauthenticated remote control of a workstation or server exposes every system "
            "and dataset that machine can reach."
        ),
    },
    "unauth_datastore": {
        "technical": (
            "A database or cache service accepts clients without authentication, or is "
            "reachable from networks that should never talk to it. Such stores (Redis, "
            "MongoDB, Elasticsearch, memcached and similar) typically ship with open access "
            "unless it is explicitly closed."
        ),
        "impact": (
            "A network-adjacent attacker can read, modify or delete the stored data, and on "
            "several engines can turn write access into code execution on the host."
        ),
        "business": (
            "customer, session or application data held in the store can be exfiltrated, "
            "tampered with or destroyed, with direct data-protection and availability "
            "consequences."
        ),
    },
    "nfs_export": {
        "technical": (
            "The NFS server exports a filesystem that is readable by any client (a wildcard "
            "or overly broad client list), and NFS authenticates the client host, not the "
            "user. Any machine that can reach the portmapper/NFS ports can mount it."
        ),
        "impact": (
            "Anyone on the network can mount the share and read its files; if it is also "
            "writable they can plant files or, with root squashing off, take over ownership."
        ),
        "business": (
            "documents, backups, source code or credentials stored on the export are "
            "exposed to every host on the network."
        ),
    },
    "rsync_module": {
        "technical": (
            "The rsync daemon serves one or more modules without a password, so any client "
            "can list and download (and, if the module is writable, upload) files."
        ),
        "impact": (
            "An unauthenticated client can copy the module's contents, and a writable module "
            "lets an attacker replace files that the host or other systems later trust."
        ),
        "business": (
            "backup and deployment data shared through rsync leaves the organisation, or is "
            "silently altered, without any credential being involved."
        ),
    },
    "snmp_exposure": {
        "technical": (
            "The SNMP agent answers to a default community string (public/private). SNMP v1/v2c "
            "uses that string as its only credential and sends it in clear text, so a default "
            "value is equivalent to no authentication."
        ),
        "impact": (
            "An attacker can read the device's configuration, interface, routing and "
            "connection tables, and with a writable (private) community can change settings."
        ),
        "business": (
            "network topology and device configuration are disclosed, which accelerates "
            "targeted attacks, and write access can disrupt connectivity."
        ),
    },
    "amplification": {
        "technical": (
            "The service answers small spoofable UDP requests with much larger responses "
            "(for example DNS open recursion, NTP monlist, SNMP GETBULK, memcached), so it "
            "can be used as a reflector in distributed denial-of-service attacks."
        ),
        "impact": (
            "An attacker spoofing a victim's address can make this host send amplified "
            "traffic to the victim, consuming your bandwidth and getting your address "
            "blocklisted."
        ),
        "business": (
            "the organisation's address space is abused to attack third parties, with "
            "bandwidth cost, reputational damage and possible upstream throttling."
        ),
    },
    "ipmi_cipher_zero": {
        "technical": (
            "The BMC's IPMI 2.0 (RMCP+) interface accepts cipher suite 0, which performs no "
            "authentication or encryption of the session (CVE-2013-4782 class)."
        ),
        "impact": (
            "An attacker who can reach UDP/623 can authenticate with any password and issue "
            "management commands: power control, console access and credential disclosure."
        ),
        "business": (
            "out-of-band management of the server is open to anyone on the network, "
            "bypassing the operating system's access controls entirely."
        ),
    },
    "mqtt_unauth": {
        "technical": (
            "The MQTT broker accepts anonymous CONNECT requests (CONNACK return code 0), so "
            "any client can subscribe to topics, including the wildcard '#', and publish."
        ),
        "impact": (
            "An attacker can read all telemetry and commands flowing through the broker and "
            "inject messages that devices will act on."
        ),
        "business": (
            "operational data is exposed and connected devices or processes can be "
            "manipulated by an unauthenticated party."
        ),
    },
    "ai_endpoint": {
        "technical": (
            "An AI/LLM or MCP endpoint answers requests without authentication, exposing the "
            "model, its tools and any data or actions those tools can reach."
        ),
        "impact": (
            "An attacker can run the model at your cost, invoke its tools, and use prompt "
            "injection to read data or trigger actions the endpoint is connected to."
        ),
        "business": (
            "compute spend, proprietary data and any systems the agent can act on are "
            "available to anyone who finds the endpoint."
        ),
    },
    "cleartext_protocol": {
        "technical": (
            "The service carries credentials or data over an unencrypted protocol (FTP, "
            "Telnet, POP3/IMAP, plain HTTP login, SMTP without STARTTLS, and similar)."
        ),
        "impact": (
            "Anyone able to observe the traffic on the path (shared network, compromised "
            "switch, rogue access point) can read passwords and content directly."
        ),
        "business": (
            "credentials and business data in transit can be harvested passively, and "
            "cleartext transport fails common audit baselines (PCI DSS, ISO 27001)."
        ),
    },
    "suspicious_listener": {
        "technical": (
            "A listener is open on a port commonly associated with backdoors, remote-access "
            "tools or command-and-control, with no legitimate service identified on it."
        ),
        "impact": (
            "If it is not an approved service it may indicate a compromise or an unapproved "
            "tool giving someone remote access to the host."
        ),
        "business": (
            "an unexplained remote-access listener is either a sign of intrusion or an "
            "unmanaged risk; both need an owner to confirm what it is."
        ),
    },
    "sip_exposure": {
        "technical": (
            "A SIP service answers on the network and can be probed for extensions, "
            "registrations and supported methods; SIP is also a common target for "
            "credential brute force and toll fraud."
        ),
        "impact": (
            "An attacker can enumerate extensions, attempt to register, and abuse the PBX "
            "for premium-rate calls if credentials are weak."
        ),
        "business": (
            "telephony fraud generates direct costs, and call systems can be disrupted or "
            "eavesdropped."
        ),
    },
    "netbios_exposure": {
        "technical": (
            "The NetBIOS name service (UDP/137) answered a node-status query, disclosing the "
            "host's NetBIOS names, workgroup or domain and hardware address to any client that "
            "can reach it."
        ),
        "impact": (
            "An attacker learns host and domain names for targeting, and NetBIOS/LLMNR name "
            "resolution can be poisoned to capture credentials."
        ),
        "business": (
            "internal naming and domain details leak beyond the network that needs them, "
            "easing reconnaissance and credential-relay attacks."
        ),
    },
    "mdns_exposure": {
        "technical": (
            "The multicast-DNS responder answered a unicast query from outside its local link, "
            "disclosing hostnames and advertised services."
        ),
        "impact": (
            "An attacker can enumerate hosts and services from a distance, and an open mDNS "
            "responder can be used as a reflection source in denial-of-service attacks."
        ),
        "business": (
            "service and device inventory is exposed, and the host can be abused against third "
            "parties."
        ),
    },
    "ike_aggressive": {
        "technical": (
            "The VPN gateway answered in IKEv1 aggressive mode. With a pre-shared key, "
            "aggressive mode sends the peer identity and a key-derived hash before the channel "
            "is protected."
        ),
        "impact": (
            "An attacker can capture the hash and crack the pre-shared key offline, then "
            "authenticate to the VPN."
        ),
        "business": (
            "a cracked VPN key gives a remote attacker a foothold inside the network perimeter."
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


# Exact rule -> content category. A posture rule id is a precise identity, so it beats
# the keyword guess in remediation_kb.classify_finding; rules not listed here (and every
# non-posture finding) still go through that classifier. The fix plan is rule-keyed too
# (app/remediation/recipes.py), so the explanation and the fix describe the same problem.
_RULE_CATEGORY: dict[str, str] = {
    "POSTURE-VNC-NO-AUTH": "vnc_no_auth", "POSTURE-VNC-WEAK-AUTH": "vnc_no_auth",
    "POSTURE-DB-UNAUTHENTICATED-ACCESS": "unauth_datastore",
    "POSTURE-EXPOSED-DATASTORE": "unauth_datastore", "POSTURE-EXPOSED-DATABASE": "unauth_datastore",
    "POSTURE-NFS-WORLD-READABLE-EXPORT": "nfs_export",
    "POSTURE-RSYNC-ANONYMOUS-MODULE": "rsync_module",
    "POSTURE-SNMP-DEFAULT-COMMUNITY": "snmp_exposure",
    "POSTURE-SNMP-AMPLIFIER": "amplification", "POSTURE-UDP-AMPLIFIER": "amplification",
    "POSTURE-IPMI-CIPHER-ZERO": "ipmi_cipher_zero",
    "POSTURE-MQTT-UNAUTHENTICATED": "mqtt_unauth",
    "POSTURE-AI-ENDPOINT-UNAUTHENTICATED": "ai_endpoint",
    "POSTURE-EXPOSED-CLEARTEXT": "cleartext_protocol", "POSTURE-SMTP-NO-STARTTLS": "cleartext_protocol",
    "POSTURE-DB-CLEARTEXT-TRANSPORT": "cleartext_protocol",
    "POSTURE-EXPOSED-BACKDOOR": "suspicious_listener",
    "POSTURE-SIP-EXPOSED": "sip_exposure",
    "POSTURE-NETBIOS-EXPOSED": "netbios_exposure",
    "POSTURE-MDNS-EXPOSED": "mdns_exposure",
    "POSTURE-IKE-AGGRESSIVE-MODE": "ike_aggressive",
}


def content_category(finding: Any) -> str:
    """The content category for a finding: its exact rule id when known, else the
    shared keyword classifier."""
    rule_id = _evidence(finding).get("rule_id")
    if isinstance(rule_id, str) and rule_id in _RULE_CATEGORY:
        return _RULE_CATEGORY[rule_id]
    return classify_finding(finding)


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
    if state == "inferred":
        # Assessed but weak: say WHICH weak signal, so the report reads
        # "Likely — version match" instead of "detection method not recorded".
        ev = getattr(finding, "evidence", None)
        ev = ev if isinstance(ev, dict) else {}
        if ev.get("matched_version") or ev.get("match_basis"):
            return "version"
        if ev.get("banner_first_line") or ev.get("banner"):
            return "banner"
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
    category = content_category(finding)
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
