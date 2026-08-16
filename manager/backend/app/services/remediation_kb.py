"""
remediation_kb.py — the deterministic remediation knowledge base.

Pure (no DB, no network, no AI): given a finding it returns a structured,
OS-aware remediation plan instantly. This is the ALWAYS-AVAILABLE fallback so the
remediation endpoints never render an empty state — even with no AI key, no cached
plan, or a provider outage, an operator/customer still gets concrete, safe steps.

Findings have no `category` column, so `classify_finding` maps a finding to a KB
category by keyword/CVE/port hints. `recipe_for_finding(finding, os)` then filters
each step's commands to the requested OS and returns the plan dict the API serves.

Every command here is hand-authored and non-destructive. (AI-generated commands go
through HallucinationGuard.validate_remediation_commands; these do not need to
because they are curated.)
"""
from __future__ import annotations

from typing import Any

# Supported OS/target keys. "network" and unknown values collapse to "generic",
# which yields vendor-neutral guidance strings rather than shell commands.
_OS_KEYS = ("linux", "windows", "macos", "generic")


def _os_key(os: str | None) -> str:
    o = (os or "").strip().lower()
    if o in ("linux", "unix"):
        return "linux"
    if o in ("windows", "win"):
        return "windows"
    if o in ("macos", "osx", "darwin", "mac"):
        return "macos"
    return "generic"          # network / appliance / unknown → guidance


def _text(finding: Any) -> str:
    parts = [
        str(getattr(finding, "title", "") or ""),
        str(getattr(finding, "description", "") or ""),
        str(getattr(finding, "remediation", "") or ""),
    ]
    return " ".join(parts).lower()


def _cves(finding: Any) -> list[str]:
    return [str(c).upper() for c in (getattr(finding, "cve_ids", None) or [])]


# Ordered most-specific → least. First matching category wins, so put narrow
# signatures (anon FTP, SMB signing) before broad ones (missing patch).
_CATEGORY_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("anon_ftp",             ("anonymous ftp", "ftp anonymous", "anonymous login")),
    ("smb_signing",          ("smb signing", "smb2 signing", "message signing")),
    ("exposed_rdp",          ("rdp", "remote desktop", "3389", "terminal services")),
    # outdated_ssh is checked BEFORE weak_tls so "OpenSSH weak ciphers" routes to
    # SSH hardening, not the TLS recipe (both mention "cipher").
    ("outdated_ssh",         ("openssh", "ssh weak", "ssh cbc", "ssh-rsa", "weak kex", "ssh protocol 1")),
    ("weak_tls",             ("sslv2", "sslv3", "tls 1.0", "tls 1.1", "tlsv1", "weak cipher",
                              "weak tls", "cipher suite", "rc4", "poodle", "beast", "weak ssl",
                              "self-signed", "expired certificate")),
    ("default_credentials",  ("default credential", "default password", "weak password",
                              "default login", "well-known credential")),
    ("open_mgmt_port",       ("telnet", "management interface exposed", "exposed to the internet",
                              "publicly accessible", "database exposed", "admin interface")),
    ("missing_patch",        ("missing patch", "outdated", "end of life", "unsupported version",
                              "security update", "unpatched")),
]


def classify_finding(finding: Any) -> str:
    """Map a finding to a KB category key using title/description/CVE hints.

    Deterministic and order-sensitive (first match wins); returns "generic" when
    nothing matches so there is always a recipe to serve."""
    text = _text(finding)
    for category, needles in _CATEGORY_KEYWORDS:
        if any(n in text for n in needles):
            return category
    # A CVE with no keyword hit is still almost certainly a patch/upgrade fix.
    if _cves(finding):
        return "missing_patch"
    return "generic"


def _step(title: str, description: str, *, linux: list[str] | None = None,
          windows: list[str] | None = None, macos: list[str] | None = None,
          generic: list[str], verification: str = "", risk: str = "low") -> dict:
    """One remediation step. `generic` is REQUIRED (the vendor-neutral fallback);
    per-OS command lists are optional and fall back to `generic` when absent."""
    return {
        "title": title,
        "description": description,
        "commands": {
            "linux": linux if linux is not None else generic,
            "windows": windows if windows is not None else generic,
            "macos": macos if macos is not None else generic,
            "generic": generic,
        },
        "verification": verification,
        "risk": risk,
    }


# ── the seeded recipes ────────────────────────────────────────────────────────

RECIPES: dict[str, dict] = {
    "weak_tls": {
        "summary": "Disable legacy SSL/TLS protocols and weak ciphers; serve only TLS 1.2+.",
        "effort": "low",
        "remediation_risk": "low",
        "steps": [
            _step(
                "Disable SSLv3/TLS 1.0/1.1 and weak ciphers",
                "Restrict the service to TLS 1.2 and 1.3 and a modern cipher suite.",
                linux=["# nginx: in the server block",
                       "ssl_protocols TLSv1.2 TLSv1.3;",
                       "ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';",
                       "sudo nginx -t && sudo systemctl reload nginx"],
                windows=["# Disable TLS 1.0 via registry (Schannel), then reboot",
                         "New-Item -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\SCHANNEL\\Protocols\\TLS 1.0\\Server' -Force",
                         "New-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\SCHANNEL\\Protocols\\TLS 1.0\\Server' -Name Enabled -Value 0 -PropertyType DWord -Force"],
                generic=["On the appliance management UI, disable SSLv3/TLS 1.0/1.1 and "
                         "restrict ciphers to TLS 1.2+ AEAD suites."],
                verification="Re-scan the port; only TLS 1.2/1.3 should negotiate.",
                risk="low"),
            _step(
                "Replace weak or expired certificates",
                "Issue a certificate with a 2048-bit+ RSA or ECDSA key from a trusted CA.",
                generic=["Reissue the certificate (>=2048-bit RSA / ECDSA P-256) and "
                         "install the full chain; remove self-signed certs from prod."],
                verification="Certificate chains to a trusted root and is within validity.",
                risk="low"),
        ],
        "verification": ["A TLS scan reports no SSLv2/SSLv3/TLS 1.0/1.1 and no weak ciphers."],
        "long_term_recommendations": ["Automate certificate renewal (ACME) and adopt a "
                                      "central TLS policy baseline."],
        "compensating_controls": "Terminate TLS at a hardened reverse proxy/load balancer.",
    },
    "smb_signing": {
        "summary": "Require SMB signing to prevent NTLM relay / man-in-the-middle.",
        "effort": "low",
        "remediation_risk": "medium",
        "steps": [
            _step(
                "Require SMB signing",
                "Force message signing on the server (and clients) so sessions cannot be relayed.",
                windows=["# Require signing (server) via Group Policy or registry",
                         "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\LanManServer\\Parameters' -Name RequireSecuritySignature -Value 1"],
                linux=["# Samba: in [global] of /etc/samba/smb.conf",
                       "server signing = mandatory",
                       "sudo systemctl restart smbd"],
                generic=["Enable 'require message signing' for SMB on the host/appliance."],
                verification="Re-scan: SMB signing shows required/enforced.",
                risk="medium"),
        ],
        "verification": ["An SMB scan reports signing required on the target."],
        "long_term_recommendations": ["Disable SMBv1 entirely; prefer SMBv3 with encryption."],
        "compensating_controls": "Segment SMB to trusted management VLANs only.",
    },
    "exposed_rdp": {
        "summary": "Restrict RDP exposure, require Network Level Authentication, and gate behind a VPN/bastion.",
        "effort": "medium",
        "remediation_risk": "medium",
        "steps": [
            _step(
                "Remove RDP from untrusted networks",
                "RDP (3389) must never face the internet; place it behind VPN/bastion + firewall allow-list.",
                windows=["# Restrict 3389 to the management subnet",
                         "New-NetFirewallRule -DisplayName 'RDP mgmt only' -Direction Inbound -Protocol TCP -LocalPort 3389 -RemoteAddress 10.0.0.0/24 -Action Allow"],
                generic=["Block TCP/3389 at the perimeter firewall; require VPN or a "
                         "bastion host for administrative access."],
                verification="External scan shows 3389 filtered from untrusted sources.",
                risk="medium"),
            _step(
                "Require Network Level Authentication (NLA)",
                "NLA forces authentication before a session is established.",
                windows=["Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp' -Name UserAuthentication -Value 1"],
                generic=["Enable Network Level Authentication for the RDP service."],
                verification="RDP requires NLA (CredSSP) on connect.",
                risk="low"),
        ],
        "verification": ["3389 is not reachable from untrusted networks and NLA is enforced."],
        "long_term_recommendations": ["Adopt just-in-time admin access and MFA on the bastion."],
        "compensating_controls": "Rate-limit and geo-block RDP; alert on brute-force attempts.",
    },
    "default_credentials": {
        "summary": "Rotate default/weak credentials immediately and enforce a strong-password policy.",
        "effort": "low",
        "remediation_risk": "medium",
        "steps": [
            _step(
                "Rotate the affected credentials",
                "Change every default/shared password to a unique, strong secret; store it in a vault.",
                generic=["Change the default account password to a unique 16+ char secret; "
                         "where possible rename or disable the default account."],
                verification="Default credentials no longer authenticate.",
                risk="medium"),
            _step(
                "Enforce a password policy + MFA",
                "Apply length/complexity/lockout and enable MFA on administrative access.",
                generic=["Enforce minimum length, lockout on repeated failure, and MFA "
                         "for administrative logins."],
                verification="Policy rejects weak passwords; MFA is required for admins.",
                risk="low"),
        ],
        "verification": ["The default credential is rotated and MFA is enforced for admins."],
        "long_term_recommendations": ["Inventory default accounts across the estate; "
                                      "integrate with a secrets manager."],
        "compensating_controls": "Restrict the management interface to a trusted network.",
    },
    "missing_patch": {
        "summary": "Apply the vendor security update for the affected component.",
        "effort": "medium",
        "remediation_risk": "medium",
        "steps": [
            _step(
                "Patch the affected software",
                "Install the vendor-published security update, then restart the service.",
                linux=["sudo apt-get update && sudo apt-get upgrade   # Debian/Ubuntu",
                       "sudo dnf upgrade --security                    # RHEL/Fedora"],
                windows=["# Install pending security updates",
                         "Install-WindowsUpdate -AcceptAll -AutoReboot   # PSWindowsUpdate module"],
                macos=["sudo softwareupdate -ia"],
                generic=["Apply the vendor security update for the affected version, "
                         "then restart the service."],
                verification="Re-scan: the installed version is at or above the fixed release.",
                risk="medium"),
        ],
        "verification": ["The component reports a patched version and the CVE no longer applies."],
        "long_term_recommendations": ["Adopt a monthly patch SLA and automated update tooling."],
        "compensating_controls": "Virtual-patch at the WAF/IPS until the update is deployed.",
    },
    "open_mgmt_port": {
        "summary": "Restrict exposed management/service ports to trusted networks; disable cleartext protocols.",
        "effort": "medium",
        "remediation_risk": "medium",
        "steps": [
            _step(
                "Firewall the exposed port",
                "Allow the service only from trusted management ranges; deny by default.",
                linux=["sudo ufw default deny incoming",
                       "sudo ufw allow from 10.0.0.0/24 to any port 22 proto tcp",
                       "sudo ufw enable"],
                windows=["New-NetFirewallRule -DisplayName 'Mgmt allow-list' -Direction Inbound -Protocol TCP -LocalPort 22 -RemoteAddress 10.0.0.0/24 -Action Allow"],
                generic=["Restrict the port to trusted management subnets at the "
                         "perimeter/host firewall; deny all other sources."],
                verification="External scan shows the port filtered from untrusted sources.",
                risk="medium"),
            _step(
                "Disable cleartext management protocols",
                "Replace Telnet/HTTP/FTP management with SSH/HTTPS/SFTP.",
                generic=["Disable Telnet/plain-HTTP/FTP admin access; use SSH/HTTPS/SFTP."],
                verification="Cleartext admin protocols are no longer listening.",
                risk="low"),
        ],
        "verification": ["The management port is unreachable from untrusted networks."],
        "long_term_recommendations": ["Move management to an out-of-band network."],
        "compensating_controls": "Require VPN + MFA for all administrative access.",
    },
    "anon_ftp": {
        "summary": "Disable anonymous FTP access, or replace FTP with SFTP.",
        "effort": "low",
        "remediation_risk": "low",
        "steps": [
            _step(
                "Disable anonymous FTP",
                "Turn off anonymous login; require authenticated accounts, or migrate to SFTP.",
                linux=["# vsftpd: in /etc/vsftpd.conf",
                       "anonymous_enable=NO",
                       "sudo systemctl restart vsftpd"],
                windows=["# IIS FTP: disable anonymous authentication",
                         "Set-WebConfigurationProperty -Filter '/system.ftpServer/security/authentication/anonymousAuthentication' -Name enabled -Value False -PSPath 'IIS:\\'"],
                generic=["Disable anonymous FTP; prefer SFTP with per-user accounts."],
                verification="Anonymous login is refused; only authenticated users connect.",
                risk="low"),
        ],
        "verification": ["Anonymous FTP login is rejected on the target."],
        "long_term_recommendations": ["Retire FTP in favour of SFTP/FTPS across the estate."],
        "compensating_controls": "Restrict FTP to a trusted network segment.",
    },
    "outdated_ssh": {
        "summary": "Upgrade OpenSSH and harden the server to modern key-exchange, ciphers, and MACs.",
        "effort": "low",
        "remediation_risk": "low",
        "steps": [
            _step(
                "Update OpenSSH",
                "Install the current OpenSSH package to clear known CVEs.",
                linux=["sudo apt-get update && sudo apt-get install --only-upgrade openssh-server"],
                generic=["Upgrade the SSH server to the current supported release."],
                verification="`ssh -V` reports a current, supported version.",
                risk="low"),
            _step(
                "Harden sshd configuration",
                "Disable weak KEX/ciphers/MACs and legacy protocol 1.",
                linux=["# /etc/ssh/sshd_config",
                       "KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org",
                       "Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com",
                       "MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com",
                       "sudo sshd -t && sudo systemctl reload sshd"],
                generic=["Restrict the SSH server to curve25519 KEX, AEAD ciphers, and "
                         "ETM MACs; disable SSH protocol 1 and CBC ciphers."],
                verification="An SSH scan reports only strong KEX/ciphers/MACs.",
                risk="low"),
        ],
        "verification": ["The SSH server offers only modern algorithms and a current version."],
        "long_term_recommendations": ["Move to certificate-based SSH auth and disable passwords."],
        "compensating_controls": "Gate SSH behind a bastion with MFA.",
    },
    "generic": {
        "summary": "Reduce exposure of the affected service and apply vendor hardening guidance.",
        "effort": "medium",
        "remediation_risk": "low",
        "steps": [
            _step(
                "Restrict and harden the service",
                "Limit the service to trusted networks and apply the vendor's hardening baseline.",
                generic=["Restrict the service to trusted networks, apply the vendor "
                         "hardening guide, and ensure it runs a supported, patched version."],
                verification="Re-scan confirms the exposure is reduced.",
                risk="low"),
            _step(
                "Confirm the finding and track to closure",
                "Validate the issue in context, assign an owner, and re-scan after the fix.",
                generic=["Validate the finding, assign an owner and due date, then re-scan "
                         "to confirm remediation."],
                verification="A follow-up scan no longer reports the finding.",
                risk="low"),
        ],
        "verification": ["A follow-up scan no longer reports the finding."],
        "long_term_recommendations": ["Feed this class of finding into your hardening baseline."],
        "compensating_controls": "Apply network segmentation and monitoring around the asset.",
    },
}


def recipe_for_finding(finding: Any, os: str | None = None) -> dict:
    """Return a structured, OS-filtered remediation plan for `finding`.

    Always returns a plan (falls back to the `generic` recipe). Each step gains a
    `commands_for_os` list resolved for the requested OS; the full per-OS
    `commands` map is retained so the UI can offer an OS switch client-side.
    """
    category = classify_finding(finding)
    recipe = RECIPES.get(category, RECIPES["generic"])
    key = _os_key(os)
    steps = []
    for i, step in enumerate(recipe["steps"], start=1):
        cmds = step.get("commands") or {}
        steps.append({
            "step": i,
            "title": step["title"],
            "description": step["description"],
            "commands": cmds,
            "commands_for_os": cmds.get(key, cmds.get("generic", [])),
            "verification": step.get("verification", ""),
            "risk": step.get("risk", "low"),
        })
    return {
        "category": category,
        "os": key,
        "source": "deterministic_kb",
        "summary": recipe["summary"],
        "effort": recipe["effort"],
        "remediation_risk": recipe["remediation_risk"],
        "steps": steps,
        "verification": list(recipe.get("verification", [])),
        "long_term_recommendations": list(recipe.get("long_term_recommendations", [])),
        "compensating_controls": recipe.get("compensating_controls", ""),
    }
