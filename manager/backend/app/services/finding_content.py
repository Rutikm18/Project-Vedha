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
    "upnp_igd": {
        "technical": (
            "The device answered SSDP discovery as a UPnP Internet Gateway Device. IGD "
            "lets any client that can reach it add, list and remove port mappings on the "
            "gateway, with no authentication."
        ),
        "impact": (
            "Malware on any internal host can open inbound ports through the gateway to "
            "itself or to other internal hosts; a WAN-facing IGD can be abused from the "
            "internet to proxy traffic (\"UPnProxy\")."
        ),
        "business": (
            "the perimeter can be opened from inside without a change request, bypassing "
            "the firewall policy the business relies on."
        ),
    },
    "upnp_exposure": {
        "technical": (
            "A UPnP/SSDP responder answered a unicast M-SEARCH and points to a device "
            "description that discloses make, model and firmware."
        ),
        "impact": (
            "The responder helps an attacker inventory devices and firmware, can be used "
            "for SSDP reflection, and some implementations accept CallStranger-style "
            "(CVE-2020-12695) subscription callbacks to arbitrary URLs."
        ),
        "business": (
            "unmanaged consumer-grade discovery on business segments widens the attack "
            "surface and leaks inventory detail."
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
    "xdmcp_login": {
        "technical": (
            "The X display manager answered an XDMCP query with Willing: it offers a graphical "
            "login session to the host that asked. XDMCP and the X11 session it starts are not "
            "encrypted."
        ),
        "impact": (
            "Anyone who can reach UDP/177 gets a login screen to guess passwords against, and "
            "anyone on the network path can read the session, including the password typed at "
            "the login screen and every keystroke after it."
        ),
        "business": (
            "a remote graphical login reachable outside the VPN and any multi-factor control, "
            "with credentials crossing the network in cleartext."
        ),
    },
    "xdmcp_exposure": {
        "technical": (
            "The X display manager answered an XDMCP query with Unwilling: XDMCP is running and "
            "reachable, although it declined to offer this host a login."
        ),
        "impact": (
            "The display manager discloses its host name and status, and its access list alone "
            "decides which other hosts it will offer an unencrypted remote login."
        ),
        "business": (
            "a legacy remote-login service runs where it is probably not needed, one access-list "
            "change away from exposing logins."
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
    "unidentified_service": {
        "technical": (
            "A TCP port accepted a connection but no probe identified the protocol behind it: "
            "no recognizable banner, no HTTP-shaped reply and no completed TLS handshake."
        ),
        "impact": (
            "Unknown listeners are where unmanaged management interfaces, forgotten test "
            "services and implants live; without knowing what it is, its exposure cannot be judged."
        ),
        "business": (
            "an unowned listening service is an unmanaged risk until someone confirms what it is "
            "and whether it should be reachable."
        ),
    },
    "snmpv3_noauth": {
        "technical": (
            "An SNMPv3 user is configured at security level noAuthNoPriv: the agent answers reads "
            "for that user with no authentication and no encryption, which makes it the SNMPv3 "
            "equivalent of a default community string."
        ),
        "impact": (
            "Anyone who can reach UDP/161 can read the device's configuration, interface, routing "
            "and connection tables, and learn the topology around it."
        ),
        "business": (
            "network and device details leak to any host on the path, easing targeted attacks, "
            "while the deployment looks secure because it runs SNMPv3."
        ),
    },
    "ftp_anonymous_write": {
        "technical": (
            "The FTP server lets the anonymous account upload files. Anonymous read access is a "
            "disclosure risk; anonymous write turns the server into a place anyone can store and "
            "serve content from."
        ),
        "impact": (
            "An attacker can upload tools, malware or web shells (especially when the FTP root is "
            "also served by a web server), host stolen data, or overwrite files other systems trust."
        ),
        "business": (
            "the server can be used to stage attacks and distribute illegal or malicious content "
            "under the organisation's address, with legal and reputational consequences."
        ),
    },
    "smbv1": {
        "technical": ("The server still negotiates the SMBv1 dialect, a 1980s-era protocol with no "
                      "pre-authentication integrity and a long record of remote-code-execution flaws."),
        "impact": ("An attacker with network access can attack the SMBv1 stack directly (the "
                   "EternalBlue/WannaCry class) and downgrade other SMB sessions to it."),
        "business": ("a single unpatched SMBv1 host has repeatedly been the entry point for "
                     "ransomware that then spreads across the whole Windows estate."),
    },
    "smb_null_session": {
        "technical": ("The SMB server accepted a null (anonymous) session and answered enumeration "
                      "requests for shares, users or groups without credentials."),
        "impact": ("An unauthenticated attacker can map accounts and shares, which feeds password "
                   "guessing and targeted attacks."),
        "business": "directory and file-share structure is disclosed to anyone on the network.",
    },
    "tls_certificate": {
        "technical": ("The certificate presented by the service is expired, self-signed, or uses a "
                      "weak key or signature algorithm, so clients cannot rely on it to authenticate "
                      "the server."),
        "impact": ("Clients either reject the service or learn to click through warnings, which "
                   "makes an active man-in-the-middle attack indistinguishable from normal use."),
        "business": ("trust in the service erodes, and expired or weak certificates fail audits and "
                     "can cause outages when strict clients refuse them."),
    },
    "msrpc_exposed": {
        "technical": ("The Windows RPC endpoint mapper answers anonymous queries and lists the "
                      "services running on the host and the dynamic ports they use."),
        "impact": ("An attacker can enumerate the host's RPC services and plan attacks against any "
                   "that are exposed or vulnerable."),
        "business": "internal service layout is disclosed beyond the segment that needs it.",
    },
    "eol_os": {
        "technical": ("The operating system release is past its vendor end-of-support date, so it no "
                      "longer receives security updates."),
        "impact": ("Every vulnerability disclosed after end of support stays exploitable "
                   "permanently; the host cannot be brought to a safe state by patching alone."),
        "business": ("an unsupported platform is a standing, growing risk and typically fails "
                     "compliance baselines that require supported software."),
    },
    "dns_zone_transfer": {
        "technical": ("The DNS server answered a full zone transfer (AXFR) to an arbitrary client, "
                      "returning every record in the zone."),
        "impact": ("An attacker obtains a complete map of internal and external hostnames, "
                   "including systems that were never meant to be public."),
        "business": "the organisation's network inventory is handed to anyone who asks.",
    },
    "ldap_anonymous": {
        "technical": ("The directory service accepts anonymous binds or searches and returns "
                      "directory entries without credentials."),
        "impact": ("An unauthenticated attacker can enumerate users, groups and computers, which "
                   "supports password spraying and targeted phishing."),
        "business": "staff and system details from the directory are exposed to the network.",
    },
    "smtp_enumeration": {
        "technical": ("The mail server answers VRFY/EXPN or RCPT probes in a way that confirms which "
                      "mailbox names exist."),
        "impact": "An attacker can build a valid user list for phishing and password attacks.",
        "business": "the staff address list leaks without authentication.",
    },
    "web_methods": {
        "technical": ("The web server allows HTTP methods that change or expose content (PUT, DELETE, "
                      "TRACE, CONNECT) where only read methods are expected."),
        "impact": ("Depending on configuration an attacker may upload or remove content, or abuse "
                   "TRACE/CONNECT to steal credentials or pivot."),
        "business": "the integrity of a public website can be altered without exploiting a bug.",
    },
    "web_hsts": {
        "technical": ("The HTTPS site does not send the Strict-Transport-Security header, so "
                      "browsers are not told to refuse plain-HTTP connections to it."),
        "impact": ("A network attacker can strip HTTPS on a user's first or later visit and capture "
                   "the session."),
        "business": "customer sessions on untrusted networks are easier to hijack.",
    },
    "dns_disclosure": {
        "technical": "The DNS server reveals its software and version in response to a version query.",
        "impact": "Attackers can match the version to known flaws and choose an exploit.",
        "business": "a small disclosure that shortens an attacker's reconnaissance.",
    },
    "rtsp_exposed": {
        "technical": ("An RTSP streaming endpoint (cameras and media servers) answers requests from "
                      "the network, often with weak or no authentication."),
        "impact": "Anyone who can reach it may view live video or probe the device for known flaws.",
        "business": "physical-security footage and privacy exposure, plus a foothold on an embedded device.",
    },
    "adb_unauth": {
        "technical": ("The Android Debug Bridge is listening over the network and accepted a shell "
                      "without authentication."),
        "impact": ("An attacker gets a command shell on the device: install apps, read data, and "
                   "use it as a pivot."),
        "business": "a device with full remote control by anyone on the network, typically a managed endpoint or kiosk.",
    },
    "mgmt_plane": {
        "technical": ("An out-of-band or remote-administration interface (IPMI/BMC, WinRM, RDP) is "
                      "reachable from the network, in a state that skips or weakens authentication."),
        "impact": ("Control of the management plane is control of the machine beneath its operating "
                   "system: power, console, firmware and credentials."),
        "business": "one reachable management interface can undo every control on the host it manages.",
    },
    "container_api": {
        "technical": ("A container or orchestration API (Docker, registry, Kubernetes, etcd) is "
                      "reachable and may accept commands without authentication."),
        "impact": ("Control of the API usually means running arbitrary containers, which equals "
                   "root on the host and access to every workload secret."),
        "business": "compromise of the container platform exposes every application and credential it runs.",
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
    "POSTURE-SMB-V1-ENABLED": "smbv1", "POSTURE-SMB-NULL-SESSION": "smb_null_session",
    "POSTURE-SMB-SIGNING-OFF": "smb_signing",
    "POSTURE-TLS-DEPRECATED-VERSION": "weak_tls", "POSTURE-TLS-WEAK-CIPHER": "weak_tls",
    "POSTURE-TLS-EXPIRED-CERT": "tls_certificate", "POSTURE-TLS-SELF-SIGNED": "tls_certificate",
    "POSTURE-TLS-WEAK-KEY": "tls_certificate", "POSTURE-TLS-WEAK-SIGNATURE": "tls_certificate",
    "POSTURE-RDP-NO-NLA": "exposed_rdp", "POSTURE-RDP-NO-TLS": "exposed_rdp", "POSTURE-RDP-EXPOSED": "exposed_rdp",
    "POSTURE-MSRPC-EPMAP-EXPOSED": "msrpc_exposed", "POSTURE-OS-END-OF-LIFE": "eol_os",
    "POSTURE-SSH-TERRAPIN": "outdated_ssh", "POSTURE-SSH-WEAK-ALGORITHMS": "outdated_ssh",
    "POSTURE-SSH-LEGACY-ALGORITHMS": "outdated_ssh",
    "POSTURE-DNS-ZONE-TRANSFER": "dns_zone_transfer", "POSTURE-DNS-VERSION-DISCLOSURE": "dns_disclosure",
    "POSTURE-LDAP-ANONYMOUS-BIND": "ldap_anonymous", "POSTURE-LDAP-ANONYMOUS-SEARCH": "ldap_anonymous",
    "POSTURE-SMTP-USER-ENUMERATION": "smtp_enumeration",
    "POSTURE-WEB-DANGEROUS-METHODS": "web_methods", "POSTURE-WEB-NO-HSTS": "web_hsts",
    "POSTURE-RTSP-EXPOSED": "rtsp_exposed", "POSTURE-ADB-UNAUTHENTICATED": "adb_unauth",
    "POSTURE-CWMP-EXPOSED": "open_mgmt_port", "POSTURE-DEFAULT-CRED-CANDIDATE": "default_credentials",
    "POSTURE-FTP-ANONYMOUS-LOGIN": "anon_ftp",
    "POSTURE-EXPOSED-CONTAINER": "container_api", "POSTURE-EXPOSED-REMOTE_ACCESS": "open_mgmt_port",
    "POSTURE-EXPOSED-ADMIN_UI": "open_mgmt_port", "POSTURE-EXPOSED-PRINTER": "open_mgmt_port",
    "CORR-NTLM-RELAY-PATH": "smb_signing", "CORR-LEGACY-WINDOWS-SURFACE": "smbv1",
    "CORR-CLEARTEXT-CLUSTER": "cleartext_protocol", "CORR-DB-UNAUTH-EXPOSED": "unauth_datastore",
    "CORR-SNMP-PUBLIC-LATERAL": "snmp_exposure", "CORR-AD-EXPOSURE": "ldap_anonymous",
    "CORR-MGMT-PLANE-EXPOSED": "mgmt_plane",
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
    "POSTURE-UPNP-IGD-EXPOSED": "upnp_igd", "POSTURE-UPNP-EXPOSED": "upnp_exposure",
    "POSTURE-SNMPV3-NOAUTH-USER": "snmpv3_noauth",
    "POSTURE-FTP-ANONYMOUS-WRITE": "ftp_anonymous_write",
    "POSTURE-UNIDENTIFIED-SERVICE": "unidentified_service",
    "POSTURE-NETBIOS-EXPOSED": "netbios_exposure",
    "POSTURE-MDNS-EXPOSED": "mdns_exposure",
    "POSTURE-XDMCP-WILLING": "xdmcp_login",
    "POSTURE-XDMCP-EXPOSED": "xdmcp_exposure",
    "POSTURE-IKE-AGGRESSIVE-MODE": "ike_aggressive",
}


def content_category(finding: Any) -> str:
    """The content category for a finding: its exact rule id when known, else the
    shared keyword classifier."""
    rule_id = _evidence(finding).get("rule_id")
    if isinstance(rule_id, str) and rule_id in _RULE_CATEGORY:
        return _RULE_CATEGORY[rule_id]
    return classify_finding(finding)


# Root cause and preconditions per category: what normally leads to this weakness, and what an
# attacker needs for it to matter. Standard text about the CLASS of weakness (never a claim about
# this specific host); the report labels it as knowledge-base content.
_CAUSE: dict[str, dict[str, Any]] = {
    "weak_tls": {"root_cause": "The TLS configuration still permits legacy protocol versions or weak ciphers, usually inherited defaults or a compatibility setting nobody revisited.",
                 "preconditions": ["Network position that can observe or modify traffic to the service", "A client that can be made to negotiate the weak option"]},
    "smb_signing": {"root_cause": "SMB message signing is not required by the server policy; on non-domain-controller Windows hosts this is the default.",
                    "preconditions": ["Network access to the SMB port", "A way to coerce or capture an NTLM authentication from a victim"]},
    "exposed_rdp": {"root_cause": "Remote Desktop is reachable from networks that do not need it, often without network-level authentication.",
                    "preconditions": ["Network access to the RDP port", "Valid or guessable credentials, or an unpatched RDP flaw"]},
    "default_credentials": {"root_cause": "A vendor-default or well-known credential was never changed at deployment.",
                            "preconditions": ["Network access to the login surface", "The vendor's published default credential"]},
    "missing_patch": {"root_cause": "The software version in use is older than the release that fixes the issue.",
                      "preconditions": ["Network access to the vulnerable component", "A public or reproducible exploit for the version"]},
    "open_mgmt_port": {"root_cause": "A management or legacy service is exposed beyond the administrative network.",
                       "preconditions": ["Network access to the service port"]},
    "anon_ftp": {"root_cause": "The FTP server keeps its built-in anonymous account enabled.",
                 "preconditions": ["Network access to the FTP port"]},
    "outdated_ssh": {"root_cause": "The SSH server offers older algorithms or runs an old release because the configuration was never hardened.",
                     "preconditions": ["Network access to the SSH port", "A client able to negotiate the weak algorithm"]},
    "vnc_no_auth": {"root_cause": "The VNC server was configured without a password, or with the None security type.",
                    "preconditions": ["Network access to the VNC port"]},
    "unauth_datastore": {"root_cause": "The data store ships with open access and was not given authentication or network restrictions.",
                         "preconditions": ["Network access to the data store port"]},
    "nfs_export": {"root_cause": "The export lists a wildcard or very broad client set, and NFS trusts the client host rather than a user.",
                   "preconditions": ["Network access to the NFS and portmapper ports", "A client that can mount the export"]},
    "rsync_module": {"root_cause": "The rsync daemon module has no authentication configured.",
                     "preconditions": ["Network access to the rsync port"]},
    "snmp_exposure": {"root_cause": "The SNMP agent still uses a default community string, which is its only credential in v1/v2c.",
                      "preconditions": ["Network access to UDP/161", "Knowledge of the default community name"]},
    "amplification": {"root_cause": "The UDP service answers small unauthenticated requests with large responses and is reachable from networks that can spoof source addresses.",
                      "preconditions": ["Ability to send spoofed UDP packets to the service", "A victim address to reflect to"]},
    "ipmi_cipher_zero": {"root_cause": "The BMC firmware enables IPMI 2.0 cipher suite 0, which skips authentication.",
                         "preconditions": ["Network access to UDP/623"]},
    "mqtt_unauth": {"root_cause": "The MQTT broker allows anonymous connections.",
                    "preconditions": ["Network access to the broker port"]},
    "ai_endpoint": {"root_cause": "The AI or MCP endpoint was published without an authentication layer.",
                    "preconditions": ["Network access to the endpoint"]},
    "cleartext_protocol": {"root_cause": "A legacy protocol without transport encryption is in use where an encrypted alternative exists.",
                           "preconditions": ["A network position that can observe the traffic"]},
    "suspicious_listener": {"root_cause": "A listener is bound on a port used by remote-access tooling or malware, with no recorded owner.",
                            "preconditions": ["Network access to the port"]},
    "sip_exposure": {"root_cause": "The SIP service is reachable from networks other than the trunks and phones that need it.",
                     "preconditions": ["Network access to the SIP port"]},
    "upnp_igd": {"root_cause": "UPnP IGD is enabled on the gateway (often a factory default) and answers on this segment.",
                 "preconditions": ["Network access to UDP/1900 and the device's HTTP control port"]},
    "upnp_exposure": {"root_cause": "UPnP/SSDP discovery is enabled on a device where nothing needs it.",
                      "preconditions": ["Network access to UDP/1900"]},
    "netbios_exposure": {"root_cause": "NetBIOS over TCP/IP is enabled and reachable beyond the segment that needs Windows name resolution.",
                         "preconditions": ["Network access to UDP/137"]},
    "mdns_exposure": {"root_cause": "The multicast-DNS responder answers queries that did not originate on its local link.",
                      "preconditions": ["Network access to UDP/5353"]},
    "xdmcp_login": {"root_cause": "XDMCP is enabled in the display manager and its access list (Xaccess) lets this host request a session.",
                    "preconditions": ["Network access to UDP/177", "A password to guess, or a network position that can read the session"]},
    "xdmcp_exposure": {"root_cause": "XDMCP is enabled in the display manager and UDP/177 is reachable from networks that should not reach it.",
                       "preconditions": ["Network access to UDP/177"]},
    "ike_aggressive": {"root_cause": "The VPN gateway accepts IKEv1 aggressive mode, often left enabled for compatibility with pre-shared-key peers.",
                       "preconditions": ["Network access to UDP/500", "A weak or guessable pre-shared key for the offline attack to succeed"]},
    "unidentified_service": {"root_cause": "A service listens on a port that no probe could identify; its owner and purpose are not recorded.",
                             "preconditions": ["Network access to the port"]},
    "snmpv3_noauth": {"root_cause": "An SNMPv3 user was created at security level noAuthNoPriv.",
                      "preconditions": ["Network access to UDP/161", "Knowledge of the user name (often a documented default)"]},
    "ftp_anonymous_write": {"root_cause": "The anonymous FTP account has write permission on at least one directory.",
                            "preconditions": ["Network access to the FTP port"]},
    "smbv1": {"root_cause": "SMBv1 was never disabled on a server that still carries the legacy feature.",
              "preconditions": ["Network access to the SMB port", "An exploit for an unpatched SMBv1 flaw"]},
    "smb_null_session": {"root_cause": "The host allows anonymous enumeration (restrict-anonymous not set).",
                         "preconditions": ["Network access to the SMB port"]},
    "tls_certificate": {"root_cause": "The certificate was not renewed, was issued internally without trust distribution, or was generated with a weak key or signature algorithm.",
                        "preconditions": ["A client connecting to the service", "For interception: a network position between client and server"]},
    "msrpc_exposed": {"root_cause": "The RPC endpoint mapper is reachable from segments that do not need it.",
                      "preconditions": ["Network access to TCP/135"]},
    "eol_os": {"root_cause": "The platform was not upgraded before its vendor support ended.",
               "preconditions": ["Network access to any vulnerable service on the host"]},
    "dns_zone_transfer": {"root_cause": "Zone transfers are not restricted to the authorised secondary servers.",
                          "preconditions": ["Network access to the DNS service"]},
    "ldap_anonymous": {"root_cause": "The directory permits anonymous bind or search.",
                       "preconditions": ["Network access to the directory port"]},
    "smtp_enumeration": {"root_cause": "The mail server answers address-verification commands.",
                         "preconditions": ["Network access to the SMTP port"]},
    "web_methods": {"root_cause": "The server or application permits more HTTP methods than the site needs.",
                    "preconditions": ["Network access to the web service"]},
    "web_hsts": {"root_cause": "The site does not send an HSTS header.",
                 "preconditions": ["A victim on a network the attacker controls", "A request made over plain HTTP"]},
    "dns_disclosure": {"root_cause": "The DNS software answers version queries with its real banner.",
                       "preconditions": ["Network access to the DNS service"]},
    "rtsp_exposed": {"root_cause": "A camera or media service is reachable from networks that do not need it.",
                     "preconditions": ["Network access to the RTSP port"]},
    "adb_unauth": {"root_cause": "ADB over TCP was enabled and left without an authorised-key requirement.",
                   "preconditions": ["Network access to the ADB port"]},
    "mgmt_plane": {"root_cause": "Management interfaces were left reachable from general networks instead of a dedicated management segment.",
                   "preconditions": ["Network access to the management interface"]},
    "container_api": {"root_cause": "The container or orchestration API is bound to a network interface without authentication or TLS.",
                      "preconditions": ["Network access to the API port"]},
    "generic": {"root_cause": "The service is exposed or configured beyond what its role requires.",
                "preconditions": ["Network access to the affected service"]},
}


def cause_for(finding: Any) -> dict[str, Any]:
    """Standard root cause and preconditions for the finding's category."""
    return _CAUSE.get(content_category(finding), _CAUSE["generic"])


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
