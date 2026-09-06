"""finding_compliance.py — deterministic finding → compliance-control mapping.

Pure/offline curated data: for each finding category (the same taxonomy as
``remediation_kb`` and ``finding_content``) it returns the specific controls that
category implicates across five frameworks:

    PCI DSS 4.0 · ISO/IEC 27001:2022 (Annex A) · NIST SP 800-53 Rev.5 ·
    SOC 2 (Trust Services Criteria) · HIPAA Security Rule (45 CFR §164.3xx)

Control identifiers are drawn from the published standards. The intent is
audit-usable *pointers* — "this finding is why control X exists" — not a legal
attestation; the rationale states the connection in one line so a reader who does
not have the framework memorised understands why it maps.

Every category maps to every framework (a missing framework falls back to the
``generic`` mapping) so a finding is never shown with a blank compliance section.
"""
from __future__ import annotations

from typing import Any

from app.services.remediation_kb import classify_finding

# Ordered display names — also the exact strings the API/UI group by.
FRAMEWORKS: tuple[str, ...] = (
    "PCI DSS 4.0",
    "ISO/IEC 27001:2022",
    "NIST SP 800-53 Rev.5",
    "SOC 2 (TSC)",
    "HIPAA Security Rule",
)

# _MAP[category][framework] = {"controls": [...], "rationale": "..."}.
_MAP: dict[str, dict[str, dict[str, Any]]] = {
    "weak_tls": {
        "PCI DSS 4.0": {
            "controls": ["Req 4.2.1 (strong cryptography in transit)", "Req 2.2.7 (encrypt non-console admin)"],
            "rationale": "Cardholder data crossing open networks must use strong, current cryptography.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.24 (Use of cryptography)", "A.8.20 (Networks security)", "A.5.14 (Information transfer)"],
            "rationale": "Cryptographic controls and network security govern protection of data in transit.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["SC-8 (Transmission Confidentiality & Integrity)", "SC-13 (Cryptographic Protection)", "SC-23 (Session Authenticity)"],
            "rationale": "Deprecated TLS/ciphers fail transmission-protection and cryptographic-strength controls.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.7 (Transmission & disposal of data)"],
            "rationale": "Data transmitted over the network must be protected during transit.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.312(e)(1) (Transmission Security)", "§164.312(e)(2)(ii) (Encryption)"],
            "rationale": "ePHI in transit must be guarded against interception, addressable by encryption.",
        },
    },
    "smb_signing": {
        "PCI DSS 4.0": {
            "controls": ["Req 2.2.1 (secure configuration standards)", "Req 4.2.1 (integrity of transmitted data)"],
            "rationale": "Requiring SMB signing is a secure-configuration and session-integrity baseline.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.20 (Networks security)", "A.8.24 (Use of cryptography)", "A.8.9 (Configuration management)"],
            "rationale": "Message signing protects the integrity and authenticity of network sessions.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["SC-23 (Session Authenticity)", "SC-8 (Transmission Integrity)", "CM-6 (Configuration Settings)"],
            "rationale": "Unsigned SMB permits session tampering/relay — a session-authenticity failure.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.6 (Boundary protection from external threats)"],
            "rationale": "Relay/MITM on the internal network is an access-boundary threat to control.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.312(c)(1) (Integrity)", "§164.312(e)(1) (Transmission Security)"],
            "rationale": "Signing preserves integrity of ePHI exchanged over SMB and blocks relay.",
        },
    },
    "exposed_rdp": {
        "PCI DSS 4.0": {
            "controls": ["Req 1.3/1.4 (restrict inbound to trusted networks)", "Req 8.4.2 (MFA for remote access)", "Req 2.2.7 (encrypt admin access)"],
            "rationale": "Remote administrative access must be network-restricted and MFA-protected.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.20 (Networks security)", "A.8.21 (Security of network services)", "A.5.15 (Access control)"],
            "rationale": "Exposed remote-access services are a network-services and access-control risk.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["AC-17 (Remote Access)", "SC-7 (Boundary Protection)", "IA-2(1) (MFA to privileged accounts)"],
            "rationale": "RDP exposure implicates remote-access, boundary-protection and MFA controls.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.1 (Logical access controls)", "CC6.6 (External threat boundary)"],
            "rationale": "Interactive remote access from untrusted networks is a logical-access exposure.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.312(a)(1) (Access Control)", "§164.308(a)(4) (Information Access Management)"],
            "rationale": "Remote interactive access to systems holding ePHI must be controlled.",
        },
    },
    "default_credentials": {
        "PCI DSS 4.0": {
            "controls": ["Req 2.2.2 (change/disable vendor defaults)", "Req 8.3.1 (strong authentication)"],
            "rationale": "Vendor-default and weak credentials must be removed or changed before deployment.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.5.17 (Authentication information)", "A.8.5 (Secure authentication)", "A.5.15 (Access control)"],
            "rationale": "Default/shared secrets violate secure-authentication and access-control controls.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["IA-5 (Authenticator Management)", "IA-5(1) (Password-based authentication)", "CM-6 (Configuration Settings)"],
            "rationale": "Default authenticators fail authenticator-management and hardening controls.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.1 (Logical access controls)", "CC6.3 (Credential management)"],
            "rationale": "Known/default credentials undermine logical access and credential management.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.312(d) (Person/Entity Authentication)", "§164.308(a)(5)(ii)(D) (Password Management)"],
            "rationale": "Authentication to ePHI systems must be unique and strong, not default.",
        },
    },
    "missing_patch": {
        "PCI DSS 4.0": {
            "controls": ["Req 6.3.3 (install security patches)", "Req 6.3.1 (identify vulnerabilities)"],
            "rationale": "Known vulnerabilities must be identified and patched within defined timeframes.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.8 (Management of technical vulnerabilities)", "A.8.32 (Change management)"],
            "rationale": "Technical-vulnerability management requires timely remediation of known flaws.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["SI-2 (Flaw Remediation)", "RA-5 (Vulnerability Monitoring & Scanning)"],
            "rationale": "Unpatched published CVEs are precisely what flaw-remediation controls address.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC7.1 (Vulnerability detection)", "CC7.2 (Monitoring)", "CC8.1 (Change management)"],
            "rationale": "Detecting and remediating vulnerabilities is a core system-operations control.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.308(a)(1)(ii)(B) (Risk Management)", "§164.308(a)(5)(ii)(B) (Protection from Malicious Software)"],
            "rationale": "Leaving known flaws open is an unmanaged risk to ePHI confidentiality/integrity.",
        },
    },
    "open_mgmt_port": {
        "PCI DSS 4.0": {
            "controls": ["Req 2.2.7 (encrypt non-console admin access)", "Req 1.3/1.4 (restrict to trusted networks)"],
            "rationale": "Management access must be network-restricted and never carried in cleartext.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.20 (Networks security)", "A.8.21 (Security of network services)", "A.8.24 (Use of cryptography)"],
            "rationale": "Exposed/cleartext management services violate network-security and crypto controls.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["SC-7 (Boundary Protection)", "AC-17(2) (Encrypt remote sessions)", "SC-8 (Transmission Confidentiality)"],
            "rationale": "Cleartext admin exposure fails boundary-protection and transmission controls.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.6 (External threat boundary)", "CC6.7 (Protected transmission)"],
            "rationale": "Exposed cleartext management is an access-boundary and transmission risk.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.312(e)(1) (Transmission Security)", "§164.312(a)(1) (Access Control)"],
            "rationale": "Cleartext/exposed administration of ePHI systems must be restricted and encrypted.",
        },
    },
    "anon_ftp": {
        "PCI DSS 4.0": {
            "controls": ["Req 7.2.1 (access on need-to-know)", "Req 8.2.1 (no shared/anonymous accounts)", "Req 2.2.7 (no cleartext)"],
            "rationale": "Anonymous, cleartext file access violates least-privilege and unique-ID controls.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.3 (Information access restriction)", "A.5.15 (Access control)", "A.8.24 (Use of cryptography)"],
            "rationale": "Unauthenticated file access defeats access-restriction and transfer controls.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["AC-3 (Access Enforcement)", "AC-6 (Least Privilege)", "SC-8 (Transmission Confidentiality)"],
            "rationale": "Anonymous access enforces no identity and transmits in the clear.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.1 (Logical access controls)", "CC6.3 (Access is authorized)"],
            "rationale": "Anonymous access grants unauthorized, unidentified logical access to data.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.312(a)(1) (Access Control)", "§164.308(a)(4) (Information Access Management)"],
            "rationale": "Unauthenticated access to stored data is an access-management failure for ePHI.",
        },
    },
    "outdated_ssh": {
        "PCI DSS 4.0": {
            "controls": ["Req 2.2.1 (secure configuration standards)", "Req 4.2.1 (strong cryptography)", "Req 6.3.3 (patching)"],
            "rationale": "Weak SSH crypto/versions fail configuration-hardening and cryptography controls.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.24 (Use of cryptography)", "A.8.8 (Technical vulnerabilities)", "A.8.9 (Configuration management)"],
            "rationale": "Weak algorithms and outdated versions are crypto and vulnerability-management gaps.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["SC-8 (Transmission Confidentiality & Integrity)", "SC-13 (Cryptographic Protection)", "SI-2 (Flaw Remediation)"],
            "rationale": "Weak KEX/ciphers/MACs and stale versions fail cryptographic and remediation controls.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.7 (Protected transmission)", "CC7.1 (Vulnerability detection)"],
            "rationale": "A weakened admin channel is both a transmission and a vulnerability-management issue.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.312(e)(1) (Transmission Security)", "§164.308(a)(1)(ii)(B) (Risk Management)"],
            "rationale": "The channel used to administer ePHI systems must use strong, current cryptography.",
        },
    },
    "generic": {
        "PCI DSS 4.0": {
            "controls": ["Req 2.2.1 (secure configuration standards)", "Req 6.3.1 (identify vulnerabilities)"],
            "rationale": "Exposed/misconfigured services fall under secure-configuration and vuln-ID controls.",
        },
        "ISO/IEC 27001:2022": {
            "controls": ["A.8.9 (Configuration management)", "A.8.8 (Technical vulnerabilities)", "A.5.15 (Access control)"],
            "rationale": "Configuration hardening and vulnerability management cover general exposures.",
        },
        "NIST SP 800-53 Rev.5": {
            "controls": ["CM-6 (Configuration Settings)", "SC-7 (Boundary Protection)", "RA-5 (Vulnerability Scanning)"],
            "rationale": "General exposure maps to hardening, boundary-protection and scanning controls.",
        },
        "SOC 2 (TSC)": {
            "controls": ["CC6.1 (Logical access controls)", "CC7.1 (Vulnerability detection)"],
            "rationale": "Access control and vulnerability detection cover unclassified exposures.",
        },
        "HIPAA Security Rule": {
            "controls": ["§164.308(a)(1)(ii)(A) (Risk Analysis)", "§164.312(a)(1) (Access Control)"],
            "rationale": "Any exposure of an ePHI system is subject to risk analysis and access control.",
        },
    },
}


def compliance_for(finding: Any) -> list[dict[str, Any]]:
    """Return ``[{framework, controls, rationale}]`` for a finding, one entry per
    framework in ``FRAMEWORKS`` order. Never empty and never a blank framework:
    an unmapped category falls back to the ``generic`` control set.
    """
    category = classify_finding(finding)
    category_map = _MAP.get(category, _MAP["generic"])
    generic_map = _MAP["generic"]
    out: list[dict[str, Any]] = []
    for framework in FRAMEWORKS:
        entry = category_map.get(framework) or generic_map[framework]
        out.append(
            {
                "framework": framework,
                "controls": list(entry["controls"]),
                "rationale": entry["rationale"],
            }
        )
    return out
