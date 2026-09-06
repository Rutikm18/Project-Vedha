"""verification_kb.py — deterministic retest ("how to prove the fix worked")
guidance for a finding.

Pure (no DB, no network, no AI). Mirrors ``remediation_kb``: classify the finding,
return a structured retest block. This fills the report's Verification section —
without a pass criterion a retest cannot be judged and the finding cannot be
closed with confidence, so every finding gets at least the generic re-scan test.

Shape: ``{method, expected, command?, retain?}`` where ``expected`` is the pass
criterion the client (and a re-tester) checks against.
"""
from __future__ import annotations

from typing import Any

from app.services.remediation_kb import classify_finding

# category (from remediation_kb.classify_finding) → retest block.
_VERIFICATION: dict[str, dict[str, str]] = {
    "generic": {
        "method": "Re-run the same check that produced this finding against the affected asset.",
        "expected": "The finding is no longer reported.",
        "retain": "The dated clean re-scan output, kept alongside the original.",
    },
    "missing_patch": {
        "method": "Re-check the installed version / patch level on the host.",
        "expected": "The installed version is at or above the vendor's fixed release.",
        "retain": "The post-patch version banner or package listing.",
    },
    "weak_tls": {
        "method": "Re-enumerate the service's TLS configuration.",
        "command": "nmap --script ssl-enum-ciphers -p 443 <host>",
        "expected": "Only TLS 1.2+ is offered and no weak ciphers (RC4/3DES/EXPORT/NULL) remain.",
        "retain": "The ssl-enum-ciphers output showing the hardened cipher list.",
    },
    "outdated_ssh": {
        "method": "Re-audit the SSH server's offered algorithms.",
        "command": "ssh-audit <host>",
        "expected": "No weak KEX, CBC ciphers or ssh-rsa host keys are offered.",
        "retain": "The ssh-audit report captured after the change.",
    },
    "anon_ftp": {
        "method": "Attempt an anonymous FTP login.",
        "command": "curl --user anonymous: ftp://<host>/",
        "expected": "Anonymous authentication is refused.",
    },
    "smb_signing": {
        "method": "Re-check whether the server requires SMB signing.",
        "expected": "SMB signing is required (not merely enabled) on the host.",
    },
    "exposed_rdp": {
        "method": "Re-test RDP reachability from an untrusted network.",
        "expected": "RDP (3389) is not reachable from untrusted networks and NLA is enforced.",
    },
    "default_credentials": {
        "method": "Attempt authentication with the default / previously-working credentials.",
        "expected": "The default credentials no longer authenticate.",
    },
    "open_mgmt_port": {
        "method": "Re-scan the management port from an untrusted network.",
        "expected": "The management interface is not reachable from untrusted networks.",
    },
}


def verification_for_finding(finding: Any) -> dict[str, str]:
    """Return a deterministic retest block for the finding.

    Always returns a block (falls back to the generic re-scan) so the report's
    Verification section and delivery-readiness always have a pass criterion.
    """
    block = _VERIFICATION.get(classify_finding(finding)) or _VERIFICATION["generic"]
    return dict(block)
