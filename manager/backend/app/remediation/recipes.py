"""
recipes.py — the rule-keyed remediation recipe catalogue.

One recipe per detection rule (every ``POSTURE-*`` rule in
``manager/detection_engine/posture_rules.py``), per exposed-service category
(``POSTURE-EXPOSED-<CATEGORY>``), plus ``CVE-PATCH`` for version-matched CVEs and
``GENERIC`` as the last resort. A coverage test fails the build when a new rule
ships without a recipe, so nothing silently falls back to generic advice.

Vocabulary follows published standards:
  * remediation_type — OASIS CSAF 2.0 §3.2.3.12 categories
  * risk_response    — NIST SP 800-40 Rev.4 risk responses
  * tiers            — contain now → fix properly → stop it recurring

Templates may use {host} {ip} {port} {product} {version} {os} {service}
{fixed_version} {target} {package}; a missing fact renders "not recorded". Every command
is hand-authored and non-destructive (checked against HallucinationGuard).
Benchmarks are cited by section NAME only — never an invented control number.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

REMEDIATION_TYPES = ("vendor_fix", "workaround", "mitigation", "none_available", "no_fix_planned")
RISK_RESPONSES = ("mitigate", "avoid", "transfer", "accept")
TIERS = ("containment", "fix", "hardening")
OS_KEYS = ("windows", "linux", "macos", "network", "generic")


@dataclass(frozen=True)
class Step:
    tier: str
    title: str
    description: str
    commands: dict[str, tuple[str, ...]] = field(default_factory=dict)
    pre_checks: tuple[str, ...] = ()
    reboot_required: bool | None = None
    downtime: str = "none expected"
    rollback: str = ""
    risk: str = "low"


@dataclass(frozen=True)
class Verification:
    scanner: str
    check: str
    expected: str
    manual: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Recipe:
    recipe_id: str
    version: int
    title: str
    remediation_type: str
    risk_response: str
    target_state: str
    steps: tuple[Step, ...]
    compensating_controls: str
    verification: Verification
    references: tuple[str, ...] = ()
    effort: str = "medium"
    long_term: tuple[str, ...] = ()


def S(tier: str, title: str, description: str, *, win: tuple[str, ...] = (),
      lin: tuple[str, ...] = (), mac: tuple[str, ...] = (), net: tuple[str, ...] = (),
      gen: tuple[str, ...] = (), pre: tuple[str, ...] = (), reboot: bool | None = None,
      downtime: str = "none expected", rollback: str = "", risk: str = "low") -> Step:
    cmds: dict[str, tuple[str, ...]] = {}
    for key, val in (("windows", win), ("linux", lin), ("macos", mac), ("network", net), ("generic", gen)):
        if val:
            cmds[key] = tuple(val)
    return Step(tier, title, description, cmds, tuple(pre), reboot, downtime, rollback, risk)


def V(scanner: str, check: str, expected: str, **manual: str) -> Verification:
    return Verification(scanner, check, expected, dict(manual))


_FIREWALL_CONTAIN = S(
    "containment", "Restrict {service} on port {port} to trusted networks",
    "Until the fix lands, allow port {port} on {host} ({ip}) only from the management "
    "or application subnets that need it.",
    win=("New-NetFirewallRule -DisplayName 'Restrict {port}' -Direction Inbound -Protocol TCP "
         "-LocalPort {port} -RemoteAddress <trusted-subnet> -Action Allow",),
    lin=("sudo ufw allow from <trusted-subnet> to any port {port} proto tcp",
         "sudo ufw deny {port}/tcp"),
    net=("Add an ACL on the upstream firewall permitting {port}/tcp to {ip} only from <trusted-subnet>",),
    gen=("Restrict {port}/tcp on {ip} to <trusted-subnet> at the nearest firewall",),
    pre=("Confirm which clients legitimately use {port} (connection logs / netstat) before restricting.",),
    rollback="Remove the rule to restore the previous reachability.", risk="low")


# ═══════════════════════════════════════════════════════════════════════════
# Posture rules (29 original + 12 in _P_V2 below) — keyed by rule_id
# ═══════════════════════════════════════════════════════════════════════════

_P: list[Recipe] = [
    Recipe(
        "POSTURE-SMB-V1-ENABLED", 1, "Disable SMBv1 on {host}", "mitigation", "mitigate",
        "SMBv1 disabled; SMB 2/3 only",
        (
            S("containment", "Block SMB from user segments",
              "Block 445/tcp to {host} from user VLANs and the internet while SMBv1 is still enabled "
              "(the EternalBlue/WannaCry transport).",
              gen=("Deny 445/tcp to {ip} from user VLANs at the segment firewall",)),
            S("fix", "Turn off the SMBv1 server protocol",
              "Disable SMBv1 on {host} ({os}). The server setting takes effect without a restart; "
              "removing the feature fully needs one.",
              win=("Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force",
                   "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart"),
              lin=("# Samba: in [global] of /etc/samba/smb.conf set:  server min protocol = SMB2_10",
                   "sudo testparm -s && sudo systemctl restart smbd"),
              net=("Disable SMBv1 / 'NT1' dialect in the appliance's file-sharing settings",),
              pre=("Find remaining SMBv1 clients first: Get-SmbSession | Select ClientComputerName,Dialect "
                   "(or enable 'Audit SMB1 access' and review the SMBServer/Audit log).",),
              reboot=False, downtime="brief SMB session reset for connected clients",
              rollback="Set-SmbServerConfiguration -EnableSMB1Protocol $true (Samba: restore the previous "
                       "server min protocol)", risk="medium"),
            S("hardening", "Remove SMBv1 fleet-wide by policy",
              "Enforce SMBv1 removal through the build baseline so new hosts never ship with it.",
              win=("GPO: Computer Configuration > Administrative Templates > MS Security Guide > "
                   "'Configure SMB v1 server' = Disabled",),
              gen=("Add 'SMBv1 disabled' to the golden-image / configuration baseline",)),
        ),
        "Block 445/tcp at every segment boundary and monitor for SMBv1 negotiation until removed.",
        V("smb_scan", "SMB negotiate no longer accepts the NT1 (SMBv1) dialect on {ip}:445",
          "SMB negotiation offers only SMB 2.x/3.x dialects",
          windows="Get-SmbServerConfiguration | Select EnableSMB1Protocol   # expect False",
          linux="smbclient -L //{ip} -N -m NT1   # expect protocol negotiation failure"),
        ("CWE-477", "MITRE T1210", "Microsoft: How to detect, enable and disable SMBv1",
         "CIS Benchmark — 'Configure SMB v1 server' (MS Security Guide section)"),
        effort="low", long_term=("Track SMBv1 client dependencies (legacy scanners, NAS) and retire them.",)),

    Recipe(
        "POSTURE-SMB-SIGNING-OFF", 1, "Require SMB signing on {host}", "mitigation", "mitigate",
        "SMB signing required (server and client)",
        (
            S("fix", "Require SMB server signing",
              "Require signing on {host} so SMB/NTLM relay (T1557.001) cannot reuse sessions.",
              win=("Set-SmbServerConfiguration -RequireSecuritySignature $true -Force",
                   "Set-SmbClientConfiguration -RequireSecuritySignature $true -Force"),
              lin=("# Samba: in [global] of /etc/samba/smb.conf set:  server signing = mandatory",
                   "sudo testparm -s && sudo systemctl restart smbd"),
              net=("Enable 'require SMB signing' in the appliance's SMB/CIFS settings",),
              pre=("Check for legacy clients/appliances that cannot sign (old NAS, printers) before enforcing.",),
              reboot=False, downtime="none expected; new sessions negotiate signing",
              rollback="Set-SmbServerConfiguration -RequireSecuritySignature $false", risk="medium"),
            S("hardening", "Enforce signing by Group Policy",
              "Apply signing to every domain member so the setting cannot drift.",
              win=("GPO: 'Microsoft network server: Digitally sign communications (always)' = Enabled",
                   "GPO: 'Microsoft network client: Digitally sign communications (always)' = Enabled"),
              gen=("Add SMB signing to the configuration baseline",)),
        ),
        "Segment SMB to server VLANs and disable NTLM where possible until signing is enforced.",
        V("smb_scan", "SMB negotiate reports signing required on {ip}:445", "Signing: required",
          windows="Get-SmbServerConfiguration | Select RequireSecuritySignature   # expect True"),
        ("CWE-306", "MITRE T1557.001",
         "CIS Benchmark — 'Microsoft network server: Digitally sign communications (always)'"),
        effort="low"),

    Recipe(
        "POSTURE-RDP-NO-NLA", 1, "Require Network Level Authentication for RDP on {host}", "mitigation",
        "mitigate", "RDP requires NLA (CredSSP) before a session is created",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Enable NLA",
              "Require NLA so the RDP stack is not reachable before authentication.",
              win=("Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\\"
                   "WinStations\\RDP-Tcp' -Name UserAuthentication -Value 1",),
              gen=("Enable 'Require user authentication for remote connections by using NLA'",),
              pre=("Confirm all RDP clients support CredSSP (Windows 7+/current mstsc).",),
              reboot=False, downtime="new RDP sessions only",
              rollback="Set UserAuthentication back to 0", risk="low"),
            S("hardening", "Enforce NLA by policy and front RDP with a gateway",
              "Apply the setting by GPO and require RDP through a VPN/RD Gateway with MFA.",
              win=("GPO: Remote Desktop Session Host > Security > 'Require user authentication for "
                   "remote connections by using Network Level Authentication' = Enabled",)),
        ),
        "Allow RDP only through a VPN or RD Gateway with MFA.",
        V("rdp_scan", "RDP negotiation on {ip}:{port} requires CredSSP/NLA", "HYBRID/CredSSP required",
          windows="(Get-WmiObject -Class Win32_TSGeneralSetting -Namespace root\\cimv2\\terminalservices)"
                  ".UserAuthenticationRequired   # expect 1"),
        ("CWE-287", "MITRE T1210", "CIS Benchmark — Remote Desktop Services 'Require NLA'"), effort="low"),

    Recipe(
        "POSTURE-RDP-NO-TLS", 1, "Force TLS security layer for RDP on {host}", "mitigation", "mitigate",
        "RDP security layer = TLS with a trusted certificate",
        (
            S("fix", "Set the RDP security layer to TLS",
              "Legacy standard RDP security uses RC4-family crypto with no server authentication.",
              win=("Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\\"
                   "WinStations\\RDP-Tcp' -Name SecurityLayer -Value 2",
                   "Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server\\"
                   "WinStations\\RDP-Tcp' -Name UserAuthentication -Value 1"),
              gen=("Set RDP 'Security Layer' to SSL/TLS and require NLA",),
              reboot=False, downtime="new RDP sessions only",
              rollback="Set SecurityLayer back to its previous value", risk="low"),
            S("hardening", "Install a CA-issued RDP certificate",
              "Bind a certificate from the internal CA so clients can authenticate the server.",
              win=("GPO: Remote Desktop Session Host > Security > 'Server authentication certificate "
                   "template' = <your RDP template>",)),
        ),
        "Tunnel RDP through a VPN until TLS is enforced.",
        V("rdp_scan", "RDP on {ip}:{port} negotiates TLS or CredSSP, not standard RDP security",
          "Standard RDP security refused"),
        ("CWE-326", "MITRE T1040"), effort="low"),

    Recipe(
        "POSTURE-RDP-EXPOSED", 1, "Restrict RDP exposure on {host}", "mitigation", "mitigate",
        "RDP reachable only via VPN / jump host with NLA + MFA",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Move RDP behind a VPN or RD Gateway",
              "RDP on {host} is reachable from the scan vantage ({port}/tcp). Publish it only through "
              "a gateway that enforces MFA.",
              gen=("Publish RDP via RD Gateway / VPN with MFA and remove the direct inbound rule",),
              pre=("List who connects directly today (Security log event 4624 LogonType 10).",),
              rollback="Re-add the direct inbound rule", risk="low"),
            S("hardening", "Enforce NLA and account lockout",
              "Require NLA and an account lockout policy on every RDP host.",
              win=("GPO: 'Require user authentication ... by using Network Level Authentication' = Enabled",)),
        ),
        "Enable account lockout and alert on repeated RDP logon failures.",
        V("rdp_scan", "RDP no longer reachable from the scan vantage on {ip}:{port}",
          "Port {port} filtered from untrusted segments"),
        ("CWE-284", "MITRE T1021.001"), effort="low"),

    Recipe(
        "POSTURE-TLS-DEPRECATED-VERSION", 1, "Disable legacy SSL/TLS on {host}:{port}", "mitigation",
        "mitigate", "Only TLS 1.2 and TLS 1.3 accepted on {port}",
        (
            S("fix", "Disable SSLv3, TLS 1.0 and TLS 1.1 on {service}",
              "{product} {version} on {host}:{port} still accepts deprecated protocol versions.",
              win=("New-Item 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\SCHANNEL\\"
                   "Protocols\\TLS 1.0\\Server' -Force | New-ItemProperty -Name Enabled -Value 0 "
                   "-PropertyType DWord -Force",
                   "New-Item 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\SCHANNEL\\"
                   "Protocols\\TLS 1.1\\Server' -Force | New-ItemProperty -Name Enabled -Value 0 "
                   "-PropertyType DWord -Force"),
              lin=("# nginx:  ssl_protocols TLSv1.2 TLSv1.3;",
                   "# Apache: SSLProtocol -all +TLSv1.2 +TLSv1.3",
                   "sudo nginx -t && sudo systemctl reload nginx   # or: sudo apachectl configtest && "
                   "sudo systemctl reload apache2"),
              net=("Set the appliance's minimum TLS version to 1.2 in its SSL/TLS profile",),
              pre=("Identify clients that still negotiate TLS 1.0/1.1 (server logs) before disabling.",),
              reboot=None, downtime="Windows Schannel changes need a restart of the host to apply; "
                                    "web servers need only a reload",
              rollback="Re-enable the protocol keys / restore the previous ssl_protocols line", risk="medium"),
            S("hardening", "Add a TLS baseline",
              "Apply one TLS profile (1.2+, AEAD ciphers) across all services via configuration management.",
              gen=("Adopt the Mozilla 'intermediate' TLS profile as the organisation baseline",)),
        ),
        "Terminate TLS on a reverse proxy/WAF that enforces TLS 1.2+ in front of the service.",
        V("tls_scan", "TLS handshake on {ip}:{port} rejects SSLv3/TLS 1.0/TLS 1.1", "Only TLS 1.2/1.3 accepted",
          linux="openssl s_client -connect {ip}:{port} -tls1_1 </dev/null   # expect handshake failure"),
        ("CWE-326", "MITRE T1040", "NIST SP 800-52 Rev.2 (TLS guidelines)",
         "Mozilla Server Side TLS — intermediate profile"), effort="low"),

    Recipe(
        "POSTURE-TLS-WEAK-CIPHER", 1, "Remove weak TLS cipher suites on {host}:{port}", "mitigation",
        "mitigate", "Only AEAD cipher suites (AES-GCM / ChaCha20-Poly1305) offered on {port}",
        (
            S("fix", "Restrict the cipher list",
              "Remove NULL/EXPORT/RC4/DES/3DES/anonymous suites from {product} on {host}:{port}.",
              win=("Disable-TlsCipherSuite -Name 'TLS_RSA_WITH_3DES_EDE_CBC_SHA'",
                   "Get-TlsCipherSuite | Where Name -match 'RC4|DES|NULL|EXPORT' | "
                   "ForEach-Object {{ Disable-TlsCipherSuite -Name $_.Name }}"),
              lin=("# nginx:  ssl_ciphers 'ECDHE+AESGCM:ECDHE+CHACHA20'; ssl_prefer_server_ciphers on;",
                   "sudo nginx -t && sudo systemctl reload nginx"),
              net=("Edit the appliance's SSL cipher profile to AEAD-only suites",),
              downtime="reload only", rollback="Restore the previous cipher string", risk="low"),
        ),
        "Front the service with a TLS-terminating proxy using a modern cipher profile.",
        V("tls_scan", "Cipher enumeration on {ip}:{port} shows no NULL/EXPORT/RC4/DES/3DES suites",
          "Weak suites absent",
          linux="nmap --script ssl-enum-ciphers -p {port} {ip}"),
        ("CWE-327", "MITRE T1040", "Mozilla Server Side TLS — intermediate profile"), effort="low"),

    Recipe(
        "POSTURE-TLS-SELF-SIGNED", 1, "Replace the self-signed certificate on {host}:{port}", "mitigation",
        "mitigate", "Certificate issued by a trusted (internal or public) CA",
        (
            S("fix", "Issue and install a CA-signed certificate",
              "Request a certificate for {host} from the internal CA (or a public CA if internet-facing) "
              "and bind it to {service} on {port}.",
              lin=("sudo openssl req -new -newkey rsa:3072 -nodes -keyout {host}.key -out {host}.csr "
                   "-subj '/CN={host}'",),
              win=("Get-Certificate -Template WebServer -DnsName {host} -CertStoreLocation cert:\\LocalMachine\\My",),
              gen=("Submit a CSR for {host} to the CA and install the issued chain on the service",),
              downtime="service reload", rollback="Rebind the previous certificate", risk="low"),
            S("hardening", "Automate certificate lifecycle",
              "Enrol the host in ACME / internal CA auto-enrolment so certificates never lapse or regress.",
              gen=("Enable ACME or CA auto-enrolment for {host}",)),
        ),
        "Pin the current certificate fingerprint on the few clients that must connect until replaced.",
        V("tls_scan", "Certificate on {ip}:{port} chains to a trusted CA", "Issuer is not the subject"),
        ("CWE-295", "MITRE T1557"), effort="low"),

    Recipe(
        "POSTURE-TLS-EXPIRED-CERT", 1, "Renew the expired certificate on {host}:{port}", "vendor_fix",
        "mitigate", "Valid, unexpired certificate with automated renewal",
        (
            S("fix", "Renew and install the certificate",
              "The certificate served on {host}:{port} has expired; renew it and reload {service}.",
              lin=("sudo certbot renew --cert-name {host}   # ACME-managed hosts",),
              gen=("Renew the certificate for {host} with the issuing CA and install the new chain",),
              downtime="service reload", rollback="None needed — the expired certificate is not usable",
              risk="low"),
            S("hardening", "Monitor and automate renewal",
              "Alert 30 days before expiry and automate renewal (ACME).",
              gen=("Add certificate-expiry monitoring for {host}:{port}",)),
        ),
        "None effective — clients will reject or be trained to accept invalid certificates.",
        V("tls_scan", "Certificate on {ip}:{port} is within its validity period", "notAfter in the future",
          linux="echo | openssl s_client -connect {ip}:{port} 2>/dev/null | openssl x509 -noout -enddate"),
        ("CWE-298", "MITRE T1557"), effort="low"),

    Recipe(
        "POSTURE-MSRPC-EPMAP-EXPOSED", 1, "Restrict the RPC endpoint mapper on {host}", "mitigation",
        "mitigate", "TCP/135 and the dynamic RPC range reachable only from trusted zones",
        (
            S("fix", "Firewall 135/tcp and the dynamic RPC range",
              "The endpoint map discloses running services and their dynamic ports to anonymous callers.",
              win=("New-NetFirewallRule -DisplayName 'Restrict RPC EPMAP' -Direction Inbound -Protocol TCP "
                   "-LocalPort 135 -RemoteAddress <trusted-subnet> -Action Allow",),
              gen=("Block 135/tcp and 49152-65535/tcp to {ip} from untrusted zones",),
              pre=("Confirm management tooling (WMI, DCOM, backup agents) source subnets first.",),
              rollback="Remove the restricting rule", risk="medium"),
            S("hardening", "Restrict anonymous RPC",
              "Enable 'Restrict Unauthenticated RPC clients' where supported.",
              win=("GPO: System > Remote Procedure Call > 'Restrict Unauthenticated RPC clients' = Authenticated",)),
        ),
        "Monitor for RPC enumeration from unusual sources.",
        V("msrpc_scan", "Anonymous endpoint-map enumeration on {ip}:135 fails from the scan vantage",
          "Endpoint map not enumerable"),
        ("CWE-200", "MITRE T1135"), effort="medium"),

    Recipe(
        "POSTURE-UDP-AMPLIFIER", 1, "Close the UDP amplification vector on {host}:{port}", "mitigation",
        "mitigate", "{service} not answering amplification-class queries from untrusted networks",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Disable the amplifying feature",
              "Disable NTP monlist / open DNS recursion / SSDP-chargen style responders on {host}.",
              lin=("# ntpd: add 'disable monitor' and 'restrict default noquery' to /etc/ntp.conf",
                   "# BIND: options {{ recursion no; allow-query-cache {{ trusted; }}; }};",
                   "sudo systemctl restart ntp   # or named"),
              net=("Disable the service's open-responder mode and enable response-rate limiting",),
              downtime="brief service restart", rollback="Restore the previous configuration", risk="low"),
            S("hardening", "Enable response-rate limiting",
              "Apply RRL / rate limits so the service cannot be abused at volume.",
              gen=("Enable response-rate limiting on {service}",)),
        ),
        "Rate-limit UDP {port} at the edge.",
        V("udp_scan", "Amplification query to {ip}:{port}/udp gets no amplified response", "No response / refused"),
        ("CWE-406", "MITRE T1498.002", "CISA — UDP-Based Amplification Attacks (TA14-017A)"), effort="low"),

    Recipe(
        "POSTURE-SNMP-DEFAULT-COMMUNITY", 1, "Replace the default SNMP community on {host}", "mitigation",
        "mitigate", "SNMPv3 with auth+priv; no default community strings",
        (
            S("fix", "Remove default communities and move to SNMPv3",
              "{host} answers a vendor-default SNMP community string.",
              lin=("# net-snmp: remove 'rocommunity public' from /etc/snmp/snmpd.conf and add:",
                   "#   createUser vedhaMon SHA <auth-pass> AES <priv-pass>",
                   "#   rouser vedhaMon priv",
                   "sudo systemctl restart snmpd"),
              net=("no snmp-server community public", "no snmp-server community private",
                   "snmp-server group MON v3 priv", "snmp-server user vedhaMon MON v3 auth sha <auth> priv aes 128 <priv>"),
              pre=("Update the monitoring platform with the new SNMPv3 credentials before removing the old community.",),
              downtime="monitoring gap until the NMS uses the new credentials",
              rollback="Re-add the previous community (not recommended)", risk="medium"),
            S("hardening", "Restrict SNMP by ACL",
              "Allow SNMP only from the monitoring servers.",
              net=("snmp-server group MON v3 priv access <acl-monitoring-servers>",),
              gen=("Allow 161/udp only from the NMS subnet",)),
        ),
        "Allow 161/udp only from monitoring servers.",
        V("snmp_scan", "Default community strings rejected by {ip}:161/udp", "No response to default communities",
          linux="snmpwalk -v2c -c public {ip} system   # expect timeout"),
        ("CWE-1392", "MITRE T1078"), effort="low"),

    Recipe(
        "POSTURE-OS-END-OF-LIFE", 1, "Replace the end-of-life OS on {host}", "no_fix_planned", "avoid",
        "Vendor-supported OS release (currently {os})",
        (
            S("containment", "Isolate the unsupported host",
              "{host} runs {os} {os_version}, which receives no security patches.",
              gen=("Move {ip} to a restricted segment allowing only required flows",)),
            S("fix", "Upgrade or migrate to a supported release",
              "Plan an in-place upgrade or rebuild onto a supported release, then migrate the workload.",
              gen=("Upgrade {host} to a vendor-supported OS release",),
              pre=("Confirm application compatibility on the target release in staging.",),
              reboot=True, downtime="maintenance window for upgrade/migration",
              rollback="Keep the old system image until the migration is verified", risk="high"),
            S("hardening", "Track OS lifecycle",
              "Add end-of-support dates to the asset inventory and plan upgrades a year ahead.",
              gen=("Record the vendor end-of-support date for every OS in the CMDB",)),
        ),
        "If upgrade is impossible: isolate, allow-list applications, and buy extended security updates where offered.",
        V("os_fingerprint", "OS fingerprint for {ip} reports a supported release", "Supported OS version"),
        ("CWE-1104", "MITRE T1190", "NIST SP 800-40 Rev.4 — unpatchable assets"), effort="high"),

    Recipe(
        "POSTURE-DEFAULT-CRED-CANDIDATE", 1, "Change the vendor default credentials on {host}", "mitigation",
        "mitigate", "No vendor-default account/password accepted",
        (
            S("fix", "Change the default administrator password",
              "{product} on {host}:{port} may still accept the vendor default login.",
              gen=("Log in to the {product} admin interface and set a unique, vaulted administrator password",),
              net=("Change the default admin password; disable or rename the default account if supported",),
              pre=("Record the new credential in the password vault before changing it.",),
              rollback="Restore from the vault entry", risk="low"),
            S("hardening", "Force password change on first login",
              "Enable 'change password on first login' and disable unused default accounts.",
              gen=("Disable unused vendor accounts on {product}",)),
        ),
        "Restrict the management interface to the admin subnet.",
        V("web_scan", "Default-credential login attempt against {ip}:{port} is refused", "Login rejected"),
        ("CWE-1392", "MITRE T1078.001"), effort="low"),

    Recipe(
        "POSTURE-SSH-TERRAPIN", 1, "Mitigate Terrapin (CVE-2023-48795) on {host}", "vendor_fix", "mitigate",
        "OpenSSH ≥ 9.6 (or vendor backport) offering strict key exchange",
        (
            S("fix", "Upgrade OpenSSH",
              "{product} {version} on {host}:{port} lacks strict key exchange.",
              lin=("sudo apt-get update && sudo apt-get install --only-upgrade openssh-server   # Debian/Ubuntu",
                   "sudo dnf upgrade openssh-server   # RHEL family"),
              net=("Upgrade the appliance firmware to a release with the Terrapin fix",),
              downtime="sshd restart; existing sessions stay up", rollback="Reinstall the previous package",
              risk="low"),
            S("containment", "Disable affected cipher modes until patched",
              "Remove ChaCha20-Poly1305 and CBC-with-EtM MACs.",
              lin=("# /etc/ssh/sshd_config: Ciphers -chacha20-poly1305@openssh.com",
                   "#                       MACs -*-etm@openssh.com",
                   "sudo sshd -t && sudo systemctl reload sshd")),
        ),
        "Restrict SSH to the admin network.",
        V("ssh_scan", "SSH KEXINIT on {ip}:{port} advertises kex-strict-s-v00@openssh.com", "strict kex offered"),
        ("CVE-2023-48795", "CWE-354", "MITRE T1557"), effort="low"),

    Recipe(
        "POSTURE-SSH-WEAK-ALGORITHMS", 1, "Remove weak SSH algorithms on {host}", "mitigation", "mitigate",
        "Only current KEX/cipher/MAC/host-key algorithms offered",
        (
            S("fix", "Restrict sshd algorithms",
              "{product} {version} on {host}:{port} offers deprecated algorithms (CBC, SHA-1 MACs, DH group1).",
              lin=("# /etc/ssh/sshd_config:",
                   "#   KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512",
                   "#   Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes128-ctr",
                   "#   MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com",
                   "sudo sshd -t && sudo systemctl reload sshd"),
              net=("Set the appliance's SSH profile to modern algorithms only (disable CBC, SHA-1)",),
              pre=("Keep an existing session open while testing a new login.",),
              downtime="none (reload)", rollback="Restore the previous sshd_config and reload", risk="medium"),
        ),
        "Restrict SSH to the admin network.",
        V("ssh_scan", "SSH algorithm negotiation on {ip}:{port} offers no CBC/SHA-1/group1 algorithms",
          "Weak algorithms absent", linux="ssh -Q kex; nmap --script ssh2-enum-algos -p {port} {ip}"),
        ("CWE-327", "MITRE T1040", "CIS Benchmark — SSH Server Configuration (ciphers/MACs/KEX)"), effort="low"),

    Recipe(
        "POSTURE-SSH-LEGACY-ALGORITHMS", 1, "Retire legacy SSH algorithms on {host}", "mitigation", "mitigate",
        "Only current KEX/cipher/MAC/host-key algorithms offered",
        (
            S("fix", "Trim deprecated algorithms from sshd",
              "{product} {version} on {host}:{port} still offers deprecated (not broken) algorithms such "
              "as SHA-1 MACs or CBC ciphers. Remove them once your clients no longer need them.",
              lin=("# /etc/ssh/sshd_config:",
                   "#   MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com",
                   "#   Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes128-ctr",
                   "sudo sshd -t && sudo systemctl reload sshd"),
              net=("Set the appliance's SSH profile to modern algorithms only",),
              pre=("Check that no automation still depends on the deprecated algorithms.",),
              downtime="none (reload)", rollback="Restore the previous sshd_config and reload", risk="low"),
        ),
        "Review the SSH algorithm policy at each OpenSSH upgrade.",
        V("ssh_scan", "SSH algorithm negotiation on {ip}:{port} offers no SHA-1 or CBC algorithms",
          "Legacy algorithms absent", linux="ssh -Q mac; nmap --script ssh2-enum-algos -p {port} {ip}"),
        ("CWE-327", "MITRE T1040", "CIS Benchmark — SSH Server Configuration (ciphers/MACs/KEX)"), effort="low"),

    Recipe(
        "POSTURE-FTP-ANONYMOUS-LOGIN", 1, "Disable anonymous FTP on {host}", "mitigation", "mitigate",
        "Anonymous FTP login refused",
        (
            S("fix", "Disable the anonymous account",
              "{product} on {host}:{port} accepts anonymous logins.",
              lin=("# vsftpd: set anonymous_enable=NO in /etc/vsftpd.conf", "sudo systemctl restart vsftpd"),
              win=("Set-WebConfigurationProperty -Filter /system.ftpServer/security/authentication/"
                   "anonymousAuthentication -Name enabled -Value False -PSPath IIS:\\",),
              downtime="brief FTP restart", rollback="Re-enable anonymous access", risk="low"),
            S("hardening", "Replace FTP with SFTP",
              "Move file transfer to SFTP/FTPS so credentials and data are encrypted.",
              gen=("Migrate consumers to SFTP and retire the FTP service",)),
        ),
        "Restrict 21/tcp to known partners only.",
        V("ftp_scan", "Anonymous login to {ip}:{port} is refused", "530 Login incorrect"),
        ("CWE-287", "MITRE T1078.001"), effort="low"),

    Recipe(
        "POSTURE-DNS-ZONE-TRANSFER", 1, "Restrict DNS zone transfers on {host}", "mitigation", "mitigate",
        "AXFR allowed only to authorised secondaries (TSIG)",
        (
            S("fix", "Restrict AXFR",
              "{host} returns full zone transfers to any client.",
              lin=("# BIND named.conf: options {{ allow-transfer {{ <secondary-ips>; }}; }};",
                   "sudo named-checkconf && sudo rndc reload"),
              win=("Set-DnsServerPrimaryZone -Name <zone> -SecureSecondaries TransferToSecureServers "
                   "-SecondaryServers <secondary-ips>",),
              downtime="none (reload)", rollback="Restore the previous allow-transfer", risk="low"),
            S("hardening", "Authenticate transfers with TSIG",
              "Use TSIG keys between primary and secondaries.",
              lin=("sudo tsig-keygen xfer-key >> /etc/bind/named.conf.keys",)),
        ),
        "Block 53/tcp from untrusted networks.",
        V("dns_scan", "AXFR request to {ip}:53 is refused", "Transfer failed / REFUSED",
          linux="dig axfr <zone> @{ip}   # expect 'Transfer failed'"),
        ("CWE-200", "MITRE T1590.002"), effort="low"),

    Recipe(
        "POSTURE-NFS-WORLD-READABLE-EXPORT", 1, "Restrict NFS exports on {host}", "mitigation", "mitigate",
        "Exports limited to named hosts/subnets, root_squash on",
        (
            S("fix", "Replace wildcard export clients",
              "{host} exports a share to any host.",
              lin=("# /etc/exports: /data 10.0.5.0/24(ro,root_squash,sec=sys)", "sudo exportfs -ra"),
              net=("Limit the NAS export to explicit client subnets and enable root squash",),
              pre=("List current clients with showmount -a before narrowing.",),
              downtime="clients outside the new list lose access", rollback="Restore /etc/exports and exportfs -ra",
              risk="medium"),
            S("hardening", "Use Kerberos NFS",
              "Move sensitive exports to sec=krb5p.",
              lin=("# /etc/exports: ...(sec=krb5p)",)),
        ),
        "Block 2049/tcp and rpcbind from untrusted segments.",
        V("nfs_scan", "showmount -e {ip} lists no wildcard (*) clients", "No world-readable export",
          linux="showmount -e {ip}"),
        ("CWE-732", "MITRE T1039"), effort="low"),

    Recipe(
        "POSTURE-LDAP-ANONYMOUS-BIND", 1, "Disable anonymous LDAP bind on {host}", "mitigation", "mitigate",
        "Anonymous bind limited to RootDSE; no naming context enumerable",
        (
            S("fix", "Disable anonymous bind",
              "{host}:{port} allows anonymous directory reads.",
              lin=("# OpenLDAP (cn=config): olcDisallows: bind_anon ; olcRequires: authc",),
              win=("Set dsHeuristics 7th character to 0 (ADSI Edit: CN=Directory Service,CN=Windows NT,"
                   "CN=Services,CN=Configuration)",),
              downtime="none", rollback="Restore the previous ACL", risk="medium"),
        ),
        "Restrict 389/636 to domain members and application servers.",
        V("ldap_scan", "Anonymous search on {ip}:{port} returns no naming context", "Operations error / no entries"),
        ("CWE-306", "MITRE T1087.002"), effort="low"),

    Recipe(
        "POSTURE-VNC-NO-AUTH", 1, "Require authentication on VNC at {host}", "mitigation", "mitigate",
        "VNC requires authentication and is reachable only via SSH/VPN",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Enable VNC authentication",
              "An unauthenticated VNC endpoint on {host}:{port} is a full interactive desktop.",
              lin=("vncpasswd   # set a password, then set SecurityTypes=VncAuth,TLSVnc in the server config",),
              win=("Set 'Authentication: VNC password' (or Windows auth) in the VNC server options",),
              gen=("Enable authentication in the VNC server and restart it",),
              downtime="active viewers disconnected", rollback="None — do not revert to no-auth", risk="low"),
            S("hardening", "Tunnel VNC",
              "Bind VNC to localhost and reach it through SSH or VPN.",
              lin=("ssh -L 5901:localhost:5901 user@{host}",)),
        ),
        "Block {port} at the host firewall immediately.",
        V("vnc_scan", "VNC handshake on {ip}:{port} no longer offers security type None", "Auth required"),
        ("CWE-306", "MITRE T1021.005"), effort="low"),

    Recipe(
        "POSTURE-VNC-WEAK-AUTH", 1, "Replace legacy VNC authentication on {host}", "mitigation", "mitigate",
        "VNC offers a modern security type or is tunnelled",
        (
            S("fix", "Move to a modern VNC security type",
              "Legacy DES challenge auth caps passwords at 8 characters and is offline-crackable.",
              gen=("Upgrade the VNC server and enable TLS/VeNCrypt or OS authentication",),
              downtime="viewer reconnect", rollback="Re-enable VncAuth", risk="low"),
            S("hardening", "Tunnel VNC over SSH/VPN", "Bind to localhost and tunnel.",
              lin=("ssh -L 5901:localhost:5901 user@{host}",)),
        ),
        "Restrict {port} to admin hosts.",
        V("vnc_scan", "VNC on {ip}:{port} no longer offers only security type 2", "Modern security type offered"),
        ("CWE-327", "MITRE T1021.005"), effort="low"),

    Recipe(
        "POSTURE-SMTP-USER-ENUMERATION", 1, "Disable VRFY/EXPN on {host}", "mitigation", "mitigate",
        "SMTP VRFY and EXPN disabled",
        (
            S("fix", "Disable VRFY and EXPN",
              "{product} on {host}:{port} confirms which mailboxes exist.",
              lin=("sudo postconf -e 'disable_vrfy_command = yes' && sudo postfix reload   # Postfix",
                   "# Sendmail: O PrivacyOptions=goaway"),
              win=("Exchange: VRFY/EXPN are disabled by default — confirm no third-party relay re-enables them",),
              downtime="none (reload)", rollback="postconf -e 'disable_vrfy_command = no'", risk="low"),
        ),
        "Rate-limit SMTP sessions from unknown sources.",
        V("smtp_scan", "VRFY/EXPN on {ip}:{port} return 252/502, not account data", "Enumeration refused"),
        ("CWE-200", "MITRE T1087.003"), effort="low"),

    Recipe(
        "POSTURE-SMTP-NO-STARTTLS", 1, "Enable STARTTLS on {host}", "mitigation", "mitigate",
        "STARTTLS advertised with a valid certificate",
        (
            S("fix", "Enable STARTTLS",
              "{product} on {host}:{port} carries mail and AUTH credentials in cleartext.",
              lin=("sudo postconf -e 'smtpd_tls_cert_file=/etc/ssl/certs/{host}.pem' "
                   "'smtpd_tls_key_file=/etc/ssl/private/{host}.key' 'smtpd_tls_security_level=may'",
                   "sudo postfix reload"),
              gen=("Install a certificate and enable STARTTLS on the SMTP listener",),
              downtime="none (reload)", rollback="Set smtpd_tls_security_level=none", risk="low"),
            S("hardening", "Require TLS for authentication", "Refuse AUTH before STARTTLS.",
              lin=("sudo postconf -e 'smtpd_tls_auth_only=yes' && sudo postfix reload",)),
        ),
        "Allow SMTP AUTH only from the internal network.",
        V("smtp_scan", "EHLO on {ip}:{port} advertises STARTTLS", "250-STARTTLS"),
        ("CWE-319", "MITRE T1040"), effort="low"),

    Recipe(
        "POSTURE-RSYNC-ANONYMOUS-MODULE", 1, "Require authentication on rsync modules at {host}", "mitigation",
        "mitigate", "Every rsync module requires auth users + secrets file",
        (
            S("fix", "Add authentication to every module",
              "rsyncd on {host}:{port} exposes a module without credentials.",
              lin=("# /etc/rsyncd.conf per module: auth users = backup ; secrets file = /etc/rsyncd.secrets",
                   "sudo chmod 600 /etc/rsyncd.secrets && sudo systemctl restart rsync"),
              downtime="brief daemon restart", rollback="Restore rsyncd.conf", risk="low"),
            S("hardening", "Bind to a management interface", "Listen only on the backup network.",
              lin=("# /etc/rsyncd.conf: address = <mgmt-ip>",)),
        ),
        "Restrict 873/tcp to the backup server.",
        V("rsync_scan", "Module listing on {ip}:{port} requires authentication", "@ERROR: auth failed"),
        ("CWE-306", "MITRE T1039"), effort="low"),

    Recipe(
        "POSTURE-SMB-NULL-SESSION", 1, "Block SMB null sessions on {host}", "mitigation", "mitigate",
        "Anonymous enumeration of shares/users/SID refused",
        (
            S("fix", "Restrict anonymous access",
              "{host} allows anonymous (null session) enumeration.",
              win=("Set-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa' -Name RestrictAnonymous -Value 1",
                   "Set-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa' -Name RestrictAnonymousSAM -Value 1"),
              lin=("# Samba [global]: restrict anonymous = 2", "sudo systemctl restart smbd"),
              pre=("Check for legacy apps relying on anonymous enumeration.",),
              downtime="none", rollback="Restore the previous registry values", risk="medium"),
        ),
        "Block 139/445 from untrusted segments.",
        V("smb_enum_scan", "Null-session share/user enumeration on {ip} fails", "NT_STATUS_ACCESS_DENIED",
          linux="smbclient -L //{ip} -N   # expect access denied"),
        ("CWE-306", "MITRE T1087.002",
         "CIS Benchmark — 'Network access: Do not allow anonymous enumeration of SAM accounts and shares'"),
        effort="low"),

    Recipe(
        "POSTURE-IPMI-CIPHER-ZERO", 1, "Disable IPMI cipher suite 0 on {host}", "mitigation", "mitigate",
        "IPMI cipher 0 disabled; BMC on an isolated management VLAN",
        (
            S("containment", "Isolate the BMC",
              "Cipher 0 accepts any password and grants full out-of-band control of {host}.",
              gen=("Move the BMC interface {ip} to the isolated management VLAN",)),
            S("fix", "Disable cipher suite 0",
              "Turn off cipher 0 in the BMC's IPMI configuration.",
              lin=("ipmitool lan set 1 cipher_privs XXXaXXXXXXXXXXX   # cipher 0 → no access (X), keep 3 = admin (a)",),
              net=("Disable IPMI-over-LAN cipher 0 in the iDRAC/iLO/BMC web settings",),
              downtime="none", rollback="Restore previous cipher_privs", risk="low"),
            S("hardening", "Update BMC firmware and rotate credentials",
              "Apply current BMC firmware and change the BMC admin password.",
              gen=("Update BMC firmware on {host} and rotate its credentials",)),
        ),
        "Block 623/udp from everything except the management jump host.",
        V("ipmi_scan", "IPMI RAKP with cipher 0 on {ip}:623 is refused", "Cipher 0 rejected",
          linux="ipmitool -I lanplus -C 0 -H {ip} -U admin -P x chassis status   # expect failure"),
        ("CWE-287", "MITRE T1078"), effort="low"),

    Recipe(
        "POSTURE-DB-UNAUTHENTICATED-ACCESS", 1, "Require authentication on {product} at {host}", "mitigation",
        "mitigate", "Database requires authentication and listens only on the application network",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Enable authentication",
              "{product} on {host}:{port} served data without credentials. Treat its data as disclosed.",
              lin=("# Redis: requirepass <strong-secret> (or ACL users) and bind <app-ip>; then restart",
                   "# MongoDB: security.authorization: enabled in /etc/mongod.conf; create an admin user first",
                   "# Elasticsearch: xpack.security.enabled: true"),
              pre=("Create the admin/application users and update app connection strings before enabling auth.",),
              downtime="service restart; apps without credentials will fail", risk="high",
              rollback="Disable authorization (only in an emergency, with the port firewalled)"),
            S("hardening", "Bind to the application network and rotate secrets",
              "Listen only on the app tier interface; rotate any secrets that were stored in this data.",
              gen=("Bind {service} to the application network interface only",)),
        ),
        "Firewall {port} to application servers only, immediately.",
        V("db_scan", "Unauthenticated read against {ip}:{port} is refused", "NOAUTH / auth required"),
        ("CWE-306", "MITRE T1213"), effort="medium"),

    Recipe(
        "POSTURE-DB-CLEARTEXT-TRANSPORT", 1, "Enable TLS on {product} at {host}", "mitigation", "mitigate",
        "Database listener requires encrypted connections",
        (
            S("fix", "Enable and require TLS",
              "{product} on {host}:{port} cannot negotiate TLS; credentials and rows cross the network in clear.",
              lin=("# MySQL: require_secure_transport=ON with ssl_cert/ssl_key set",
                   "# PostgreSQL: ssl=on in postgresql.conf and hostssl-only rules in pg_hba.conf"),
              win=("SQL Server Configuration Manager: Protocols > Force Encryption = Yes (bind a certificate)",),
              pre=("Confirm client drivers support TLS and trust the server certificate.",),
              downtime="database restart", rollback="Set the require/force flag off", risk="medium"),
        ),
        "Restrict {port} to the application tier.",
        V("db_scan", "TLS negotiation on {ip}:{port} succeeds and plaintext is refused", "TLS required"),
        ("CWE-319", "MITRE T1040"), effort="medium"),

    # ── enhanced-scanner posture rules (TLS cert quality, web, DNS, LDAP, SNMP,
    #    IoT/OT and mobile/AI surfaces added with the expanded detection set) ──
    Recipe(
        "POSTURE-TLS-WEAK-KEY", 1, "Reissue the TLS certificate on {host} with a strong key",
        "mitigation", "mitigate",
        "TLS endpoint serves a certificate with a 2048-bit+ RSA or P-256+ ECDSA key",
        (
            S("fix", "Generate a strong key and reissue the certificate",
              "The certificate on {host}:{port} uses a key below current strength. Generate a new 2048-bit+ RSA "
              "(or P-256+ ECDSA) key, have a fresh certificate issued for it, and install it on {service}.",
              lin=("openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out newkey.pem",
                   "openssl req -new -key newkey.pem -out newcsr.pem   # submit the CSR to your CA, then install the issued cert"),
              gen=("Reissue the {service} certificate for {host}:{port} with a 2048-bit+ RSA or P-256+ ECDSA key and install the new chain",),
              pre=("Confirm the CA and the clients accept the chosen key type before cutover.",),
              downtime="brief {service} reload to load the new certificate",
              rollback="Keep the previous certificate and key until the new one is confirmed, then retire the weak key.",
              risk="medium"),
            S("hardening", "Enforce a minimum key strength at issuance",
              "Set the CA / ACME profile to refuse keys below 2048-bit RSA or P-256 ECDSA so a weak key cannot be reissued.",
              gen=("Add a minimum-key-strength policy to the certificate issuance profile",)),
        ),
        "Terminate TLS for {host}:{port} at a gateway presenting a strong certificate until the endpoint is reissued.",
        V("tls_scan", "the certificate presented on {ip}:{port} uses a strong public key",
          "public key is 2048-bit+ RSA or P-256+ ECDSA",
          generic="openssl s_client -connect {ip}:{port} </dev/null 2>/dev/null | openssl x509 -noout -text | grep -A1 'Public-Key'"),
        ("CWE-326", "MITRE T1040"), effort="medium"),

    Recipe(
        "POSTURE-TLS-WEAK-SIGNATURE", 1, "Reissue the TLS certificate on {host} with a SHA-256 signature",
        "mitigation", "mitigate",
        "TLS certificate chain is signed with SHA-256 or stronger (no MD5/SHA-1)",
        (
            S("fix", "Reissue the certificate with a modern signature algorithm",
              "The certificate on {host}:{port} is signed with MD5 or SHA-1, which is forgeable. Have the CA "
              "reissue it with a SHA-256+ signature and install the new chain on {service}.",
              gen=("Request a SHA-256-signed replacement certificate for {host}:{port} from the issuing CA and install it",),
              pre=("Check the whole chain: an intermediate may carry the weak signature, not the leaf.",),
              downtime="brief {service} reload",
              rollback="Retain the prior certificate until the new chain verifies.", risk="medium"),
            S("hardening", "Reject weak signatures going forward",
              "Configure the CA profile and TLS policy to refuse MD5/SHA-1 signatures.",
              gen=("Set issuance and TLS policy to require SHA-256+ signatures",)),
        ),
        "Front {host}:{port} with a gateway presenting a SHA-256-signed certificate until it is reissued.",
        V("tls_scan", "the certificate chain on {ip}:{port} is signed with SHA-256 or stronger",
          "no MD5 or SHA-1 signatures anywhere in the chain",
          generic="openssl s_client -connect {ip}:{port} </dev/null 2>/dev/null | openssl x509 -noout -text | grep 'Signature Algorithm'"),
        ("CWE-328", "MITRE T1557"), effort="medium"),

    Recipe(
        "POSTURE-WEB-DANGEROUS-METHODS", 1, "Disable dangerous HTTP methods on {host}", "mitigation", "mitigate",
        "Web service answers only the methods it needs (typically GET/POST/HEAD); PUT/DELETE/TRACE/CONNECT refused",
        (
            S("fix", "Restrict the allowed HTTP methods",
              "The {service} on {host}:{port} accepts methods such as PUT, DELETE or TRACE that let a caller write "
              "files or reflect headers. Limit it to the methods the application actually uses.",
              lin=("# nginx: in the server block, return 405 for anything but the needed methods",
                   "# Apache: use LimitExcept for GET/POST/HEAD, and set TraceEnable off"),
              gen=("Configure {service} on {host}:{port} to allow only GET/POST/HEAD and refuse PUT/DELETE/TRACE/CONNECT",),
              pre=("Confirm the application does not rely on WebDAV or REST verbs before disabling them.",),
              rollback="Re-enable the specific method the application is shown to need.", risk="low"),
        ),
        "Add a WAF or reverse-proxy rule dropping PUT/DELETE/TRACE/CONNECT to {host}:{port} until the server config is changed.",
        V("web_scan", "{ip}:{port} refuses PUT/DELETE/TRACE with 405/501", "only the required methods are accepted",
          generic="curl -sS -X OPTIONS http://{ip}:{port}/ -i | grep -i '^Allow:'"),
        ("CWE-650", "MITRE T1505"), effort="low"),

    Recipe(
        "POSTURE-WEB-NO-HSTS", 1, "Enable HSTS on {host}", "mitigation", "mitigate",
        "HTTPS service sends a Strict-Transport-Security header with a reasonable max-age",
        (
            S("fix", "Send the Strict-Transport-Security header",
              "The HTTPS service on {host}:{port} does not set HSTS, so the first request can be forced over "
              "cleartext HTTP and intercepted. Add the header on every HTTPS response.",
              lin=("# nginx: add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\" always;",
                   "# Apache: Header always set Strict-Transport-Security \"max-age=31536000; includeSubDomains\""),
              gen=("Set Strict-Transport-Security with max-age=31536000 and includeSubDomains on HTTPS responses from {host}:{port}",),
              pre=("Make sure every subdomain is HTTPS-ready before adding includeSubDomains.",),
              rollback="Remove the header or lower max-age if a subdomain breaks.", risk="low"),
        ),
        "Enforce HTTPS and HSTS at the CDN or load balancer in front of {host} until the origin sets it.",
        V("web_scan", "the HTTPS response from {ip}:{port} carries a Strict-Transport-Security header",
          "Strict-Transport-Security present with a max-age",
          generic="curl -sS -I https://{ip}:{port}/ | grep -i strict-transport-security"),
        ("CWE-319", "MITRE T1040"), effort="low"),

    Recipe(
        "POSTURE-DNS-VERSION-DISCLOSURE", 1, "Stop version disclosure on the DNS server {host}", "mitigation", "mitigate",
        "DNS server no longer returns its build in a version.bind / version.server query",
        (
            S("fix", "Mask the version response",
              "The DNS server on {host}:{port} answers version.bind with its real build, which tells an attacker "
              "which CVEs to try. Override the version string.",
              lin=("# BIND: in the options block set   version \"not disclosed\";   then  sudo rndc reconfig",
                   "# PowerDNS: set  version-string=anonymous  in pdns.conf and restart"),
              gen=("Configure {service} on {host} to return a static or empty version string for version.bind",),
              rollback="Restore the default version directive if your monitoring needs the build.", risk="low"),
            S("hardening", "Keep the resolver patched",
              "Masking the banner is not a patch; keep {service} on a supported, current build.",
              gen=("Track {service} releases and apply security updates on a schedule",)),
        ),
        "Restrict recursion and version queries on {host}:{port} to trusted clients at the firewall.",
        V("dns_scan", "a version.bind CHAOS TXT query to {ip} no longer returns the real build",
          "version response is static, empty, or refused",
          generic="dig @{ip} version.bind chaos txt +short"),
        ("CWE-200", "MITRE T1590.002"), effort="low"),

    Recipe(
        "POSTURE-LDAP-ANONYMOUS-SEARCH", 1, "Disable anonymous LDAP search on {host}", "mitigation", "mitigate",
        "Directory on {host}:{port} requires authentication before it returns entries",
        (
            S("fix", "Require authentication for directory reads",
              "The directory on {host}:{port} lets an anonymous client enumerate users and groups. Disable "
              "anonymous bind and anonymous search.",
              lin=("# OpenLDAP: set  olcDisallows: bind_anon  and  olcRequires: authc  then restart slapd",),
              win=("Active Directory: set dsHeuristics so anonymous operations are disabled (7th character not 2)",),
              gen=("Configure {service} on {host} to deny anonymous bind and anonymous search",),
              pre=("Confirm no application relies on anonymous read (some address books do) before disabling.",),
              rollback="Re-enable anonymous read for the one subtree an application is shown to need.", risk="medium"),
        ),
        "Restrict {port} on {host} to the application and admin subnets that use the directory.",
        V("ldap_scan", "an anonymous bind to {ip}:{port} can no longer read directory entries",
          "anonymous search returns no entries or is refused",
          generic="ldapsearch -x -H ldap://{ip}:{port} -b '' -s base   # expect no directory content"),
        ("CWE-287", "MITRE T1087.002"), effort="medium"),

    Recipe(
        "POSTURE-SNMP-AMPLIFIER", 1, "Stop {host} being usable as an SNMP amplifier", "mitigation", "mitigate",
        "SNMP on {host}:{port} answers only authorized management hosts and no default community",
        (
            S("containment", "Restrict UDP {port} to the management network",
              "A reflected SNMP GETBULK can be amplified against a third party. Limit UDP {port} on {host} to the "
              "monitoring hosts that poll it.",
              gen=("Allow UDP {port} to {ip} only from the monitoring/management subnet at the firewall; drop it elsewhere",),
              risk="low"),
            S("fix", "Remove default communities and prefer SNMPv3",
              "Replace the public/private communities and move {service} to SNMPv3 with auth and privacy so an "
              "unauthenticated query cannot be reflected.",
              lin=("# snmpd.conf: remove the 'rocommunity public' line, define an SNMPv3 authPriv user, then restart snmpd",),
              gen=("Delete default SNMP communities on {host} and require SNMPv3 authPriv",),
              pre=("Confirm the monitoring system supports SNMPv3 before removing the community strings.",),
              rollback="Restore a read-only community scoped to the monitoring host if the v3 cutover slips.", risk="medium"),
        ),
        "Rate-limit or block inbound UDP {port} to {host} at the edge until the communities are removed.",
        V("snmp_scan", "an SNMP query to {ip}:{port} with a default community is refused",
          "default communities rejected; only SNMPv3 or authorized access works",
          generic="snmpget -v2c -c public {ip} sysDescr.0   # expect timeout / no response"),
        ("CWE-406", "MITRE T1498.002"), effort="medium"),

    Recipe(
        "POSTURE-MQTT-UNAUTHENTICATED", 1, "Require authentication on the MQTT broker {host}", "mitigation", "mitigate",
        "MQTT broker on {host}:{port} requires credentials and TLS; anonymous clients refused",
        (
            S("containment", "Limit the broker to its device network",
              "While anonymous access is open, restrict {port} on {host} to the device and application subnets.",
              gen=("Allow {port}/tcp to {ip} only from the IoT and application subnets at the firewall",), risk="low"),
            S("fix", "Turn off anonymous access and require credentials",
              "Configure {service} on {host}:{port} to reject anonymous clients, require per-client credentials, "
              "and enable TLS on the secured listener.",
              lin=("# Mosquitto: set  allow_anonymous false  and a password_file, then restart the broker",),
              gen=("Disable anonymous access on {service}, add per-client credentials, and enable TLS",),
              pre=("Provision credentials for every legitimate publisher and subscriber before enforcing.",),
              downtime="clients reconnect with credentials",
              rollback="Re-enable anonymous on an internal-only listener if a device cannot be updated in time.", risk="medium"),
        ),
        "Keep {port} on {host} firewalled to the device subnet and watch for anonymous CONNECTs until auth is enforced.",
        V("iot_scan", "an anonymous MQTT CONNECT to {ip}:{port} is refused",
          "broker requires credentials; anonymous CONNECT denied",
          generic="mosquitto_sub -h {ip} -p {port} -t test -C 1   # expect connection refused / not authorized"),
        ("CWE-306", "MITRE T1133"), effort="medium"),

    Recipe(
        "POSTURE-CWMP-EXPOSED", 1, "Restrict the TR-069/CWMP interface on {host}", "mitigation", "mitigate",
        "CWMP management port on {host}:{port} is reachable only from the provider ACS",
        (
            S("fix", "Bind CWMP to the ACS only",
              "The TR-069/CWMP interface on {host}:{port} is internet-reachable, which has been used for mass "
              "device takeover. Restrict it to the managing ACS, or disable it if no ACS is used.",
              gen=("Configure the device so CWMP on {port} accepts connections only from the provider ACS address, "
                   "or disable TR-069 if you do not use an ACS",),
              net=("ACL on the upstream firewall: permit {port}/tcp to {ip} only from the ACS address, deny elsewhere",),
              pre=("Confirm whether an ACS legitimately manages {host} before disabling CWMP.",),
              rollback="Re-permit the ACS address if remote management stops working.", risk="medium"),
        ),
        "Block {port}/tcp to {host} from the internet at the edge until CWMP is bound to the ACS.",
        V("iot_scan", "CWMP on {ip}:{port} is not reachable from outside the ACS network",
          "TR-069 endpoint refused from untrusted sources",
          generic="curl -sS -m 5 http://{ip}:{port}/ -o /dev/null   # from an untrusted host, expect a timeout"),
        ("CWE-284", "MITRE T1190"), effort="medium"),

    Recipe(
        "POSTURE-RTSP-EXPOSED", 1, "Lock down the RTSP endpoint on {host}", "mitigation", "mitigate",
        "RTSP service on {host}:{port} requires authentication and is reachable only from trusted viewers",
        (
            S("containment", "Restrict {port} to the camera VLAN and VMS",
              "An exposed RTSP stream leaks video and is often unauthenticated. Restrict {port} on {host} to the "
              "video-management server and operator subnet.",
              gen=("Allow {port}/tcp to {ip} only from the VMS and operator subnets at the firewall",), risk="low"),
            S("fix", "Require authentication on the stream",
              "Enable per-user credentials on {service} and remove any default account so the stream cannot be "
              "opened anonymously.",
              gen=("Set a strong RTSP username and password on {host}, remove default or blank credentials, and enable TLS/SRTP if supported",),
              pre=("Record which viewers and NVRs pull the stream before changing credentials.",),
              downtime="viewers re-authenticate",
              rollback="Restore the prior credential on an internal-only listener if an NVR breaks.", risk="medium"),
        ),
        "Keep {port} on {host} firewalled to the camera VLAN until authentication is enforced.",
        V("iot_scan", "an unauthenticated RTSP DESCRIBE to {ip}:{port} is refused",
          "RTSP requires credentials; anonymous DESCRIBE returns 401",
          generic="curl -sS -m 5 rtsp://{ip}:{port}/   # expect 401 Unauthorized"),
        ("CWE-306", "MITRE T1021"), effort="medium"),

    Recipe(
        "POSTURE-ADB-UNAUTHENTICATED", 1, "Disable network ADB on {host}", "mitigation", "avoid",
        "Android Debug Bridge is not reachable over the network on {host}:{port}",
        (
            S("containment", "Block {port} immediately",
              "An open ADB port is a remote root shell. Block {port}/tcp to {host} at the nearest firewall right away.",
              gen=("Deny {port}/tcp to {ip} at the segment firewall now; allow only a named debug host if one is truly needed",),
              risk="low"),
            S("fix", "Turn off ADB over the network",
              "Disable network ADB on the device so it no longer listens on {port}. Debugging over USB with "
              "authorized keys is the supported path.",
              gen=("On the device, turn off wireless debugging / ADB over network and, if managed, disable USB debugging by MDM policy",),
              pre=("Confirm no automated test rig depends on this device's network ADB before disabling.",),
              rollback="Re-enable wireless debugging only on an isolated lab network with key authorization.", risk="medium"),
        ),
        "Keep {port}/tcp to {host} blocked at the firewall until network ADB is turned off on the device.",
        V("mobile_scan", "a connection to ADB on {ip}:{port} is refused",
          "no ADB service answers on the network port",
          generic="nc -vz -w 5 {ip} {port}   # expect connection refused / timeout"),
        ("CWE-306", "MITRE T1021"), effort="low"),

    Recipe(
        "POSTURE-AI-ENDPOINT-UNAUTHENTICATED", 1, "Put authentication in front of the AI endpoint on {host}",
        "mitigation", "mitigate",
        "AI/MCP inference endpoint on {host}:{port} requires authentication and is not openly reachable",
        (
            S("containment", "Restrict {port} to known callers",
              "An open inference or MCP endpoint lets anyone spend tokens, read prompts, or reach connected tools. "
              "Restrict {port} on {host} to the application hosts that call it.",
              gen=("Allow {port}/tcp to {ip} only from the application and service subnet at the firewall",), risk="low"),
            S("fix", "Require authentication on the endpoint",
              "Front {service} on {host}:{port} with an API key or gateway auth, and bind the model server to the "
              "loopback address so only the authenticated proxy reaches it.",
              gen=("Require an API key or gateway token on every request to {host}:{port}, and bind the inference server to 127.0.0.1 behind that proxy",),
              pre=("Issue keys to the legitimate callers before turning on enforcement.",),
              downtime="callers add an auth header",
              rollback="Scope access to an internal-only listener if a caller cannot add auth immediately.", risk="medium"),
        ),
        "Keep {port} on {host} firewalled to the application tier and monitor for unauthenticated calls until auth is enforced.",
        V("mcp_ai_scan", "an unauthenticated request to {ip}:{port} is rejected",
          "endpoint returns 401 or 403 without a valid key",
          generic="curl -sS -m 5 http://{ip}:{port}/   # expect 401/403 without credentials"),
        ("CWE-306", "MITRE T1133"), effort="medium"),
]




# ═══════════════════════════════════════════════════════════════════════════
# Posture rules added by the detection-enhancement pass (12) — previously
# unconsumed probe facts. Same structure and verification discipline as above.
# ═══════════════════════════════════════════════════════════════════════════

_P_V2: list[Recipe] = [
    Recipe(
        "POSTURE-TLS-WEAK-KEY", 1, "Reissue the weak-key certificate on {host}:{port}",
        "vendor_fix", "mitigate", "Certificate key is RSA >= 2048 bits or EC >= 256 bits",
        (
            S("fix", "Generate a strong key and reissue the certificate",
              "Create a new private key of adequate size, request a certificate for it, and install "
              "it for the service on port {port}.",
              lin=("openssl req -new -newkey rsa:3072 -nodes -keyout server.key -out server.csr",),
              win=("certreq -new request.inf request.req   # set KeyLength = 3072 in request.inf",),
              gen=("Reissue the certificate from your CA with a >=2048-bit RSA or P-256+ EC key",),
              pre=("Note which clients pin the current certificate before replacing it.",),
              downtime="service reload to pick up the new certificate",
              rollback="Reinstall the previous certificate and key from backup.", risk="low"),
            S("hardening", "Enforce minimum key sizes in issuance policy",
              "Configure the CA / ACME client so keys below the floor cannot be issued.",
              gen=("Set the CA certificate template minimum key size to 2048 (RSA) / 256 (EC)",)),
        ),
        "Restrict the service to trusted clients until the certificate is replaced.",
        V("tls_scan", "Certificate public key on {ip}:{port} is RSA >= 2048 or EC >= 256 bits",
          "public_key_bits meets the minimum for its key type",
          linux="openssl s_client -connect {ip}:{port} </dev/null 2>/dev/null | openssl x509 -noout -text | grep 'Public-Key'"),
        ("CWE-326", "MITRE T1040", "NIST SP 800-57 Part 1 — key length recommendations",
         "CA/Browser Forum Baseline Requirements — key sizes"), effort="low"),

    Recipe(
        "POSTURE-TLS-WEAK-SIGNATURE", 1, "Reissue the SHA-1/MD5-signed certificate on {host}:{port}",
        "vendor_fix", "mitigate", "Certificate signed with SHA-256 or stronger",
        (
            S("fix", "Reissue with a SHA-256 signature",
              "Request a new certificate signed with SHA-256 or stronger and install it on port {port}.",
              lin=("openssl req -new -sha256 -key server.key -out server.csr",),
              gen=("Reissue the certificate from your CA with a SHA-256 (or stronger) signature",),
              downtime="service reload to pick up the new certificate",
              rollback="Reinstall the previous certificate from backup.", risk="low"),
            S("hardening", "Retire legacy signature hashes at the CA",
              "Disable MD5/SHA-1 signing on any internal CA so legacy certificates cannot be reissued.",
              gen=("Set the internal CA hash algorithm to SHA256 or stronger",)),
        ),
        "Restrict the service to trusted clients until the certificate is replaced.",
        V("tls_scan", "Certificate on {ip}:{port} is signed with SHA-256 or stronger",
          "sig_algorithm is not md5 / sha1",
          linux="openssl s_client -connect {ip}:{port} </dev/null 2>/dev/null | openssl x509 -noout -text | grep 'Signature Algorithm'"),
        ("CWE-327", "MITRE T1557", "CA/Browser Forum — SHA-1 deprecation"), effort="low"),

    Recipe(
        "POSTURE-WEB-DANGEROUS-METHODS", 1, "Disable dangerous HTTP methods on {host}:{port}",
        "workaround", "mitigate", "Only GET/HEAD/POST (and methods the API needs) are allowed",
        (
            S("containment", "Block write/trace methods at the edge",
              "Reject PUT, DELETE, TRACE and CONNECT at the reverse proxy or WAF in front of {host}.",
              gen=("Add a WAF / proxy rule rejecting PUT, DELETE, TRACE, CONNECT to {ip}:{port}",)),
            S("fix", "Restrict methods in the web server",
              "Allow only the methods the application uses; disable TRACE explicitly.",
              lin=("# Apache: TraceEnable Off  and  <LimitExcept GET POST HEAD> Require all denied </LimitExcept>",
                   "# nginx: if ($request_method !~ ^(GET|HEAD|POST)$) return 405;",
                   "sudo apachectl configtest || sudo nginx -t"),
              win=("Import-Module WebAdministration; Get-WebConfiguration system.webServer/security/requestFiltering/verbs",),
              downtime="web server reload", rollback="Restore the previous server configuration.",
              risk="medium"),
        ),
        "Front the service with a proxy that only forwards the methods the application needs.",
        V("web_scan", "OPTIONS on {ip}:{port} no longer advertises PUT/DELETE/TRACE/CONNECT",
          "dangerous_methods is empty",
          linux="curl -s -o /dev/null -D - -X OPTIONS http://{ip}:{port}/ | grep -i '^allow'"),
        ("CWE-650", "MITRE T1505", "OWASP Testing Guide — Test HTTP Methods"), effort="low"),

    Recipe(
        "POSTURE-WEB-NO-HSTS", 1, "Enable HSTS on {host}:{port}", "workaround", "mitigate",
        "Strict-Transport-Security header sent with a long max-age",
        (
            S("fix", "Send the Strict-Transport-Security header",
              "Add HSTS to every HTTPS response so browsers refuse to downgrade to cleartext.",
              lin=("# nginx: add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\" always;",
                   "# Apache: Header always set Strict-Transport-Security \"max-age=31536000; includeSubDomains\""),
              gen=("Configure the load balancer / proxy to add Strict-Transport-Security on HTTPS responses",),
              pre=("Confirm every subdomain serves valid HTTPS before using includeSubDomains.",),
              downtime="web server reload", rollback="Remove the header (browsers keep cached HSTS until max-age).",
              risk="medium"),
        ),
        "Redirect all HTTP to HTTPS at the edge until HSTS is deployed.",
        V("web_scan", "HTTPS responses from {ip}:{port} include Strict-Transport-Security",
          "strict-transport-security not in security_headers_missing",
          linux="curl -sk -D - -o /dev/null https://{ip}:{port}/ | grep -i strict-transport-security"),
        ("CWE-319", "MITRE T1040", "RFC 6797 — HTTP Strict Transport Security"), effort="low"),

    Recipe(
        "POSTURE-DNS-VERSION-DISCLOSURE", 1, "Hide the DNS server version on {host}", "workaround",
        "mitigate", "version.bind returns no software version",
        (
            S("fix", "Override the version.bind response",
              "Configure the resolver to answer CHAOS TXT version.bind with no version string.",
              lin=("# BIND named.conf options: version \"not disclosed\";",
                   "sudo named-checkconf && sudo rndc reconfig"),
              win=("dnscmd /config /EnableVersionQuery 0",),
              rollback="Remove the override and reload.", risk="low"),
        ),
        "Restrict DNS queries to internal clients so the version is not exposed externally.",
        V("dns_scan", "CHAOS TXT version.bind on {ip} returns no version",
          "version_bind is empty or refused",
          linux="dig @{ip} version.bind chaos txt +short"),
        ("CWE-200", "MITRE T1590.002", "ISC BIND 9 ARM — version option"), effort="low"),

    Recipe(
        "POSTURE-LDAP-ANONYMOUS-SEARCH", 1, "Disable anonymous LDAP search on {host}", "mitigation",
        "mitigate", "Anonymous callers can read at most the RootDSE",
        (
            S("containment", "Restrict LDAP to trusted networks",
              "Limit 389/636 on {host} to domain members and management hosts until the ACL is fixed.",
              gen=("Restrict 389/tcp and 636/tcp to {ip} from trusted subnets at the firewall",)),
            S("fix", "Remove anonymous read access",
              "Disable anonymous operations so directory content requires authentication.",
              win=("# AD: ensure the 7th character of dsHeuristics is not 2 (anonymous operations disabled)",
                   "Get-ADObject 'CN=Directory Service,CN=Windows NT,CN=Services,CN=Configuration,DC=example,DC=com' -Properties dsHeuristics"),
              lin=("# OpenLDAP: olcDisallows: bind_anon  and an ACL denying anonymous read beyond the RootDSE",),
              pre=("Identify legacy apps that bind anonymously (directory access logs) before disabling.",),
              rollback="Restore the previous dsHeuristics / ACL value.", risk="medium"),
        ),
        "Monitor anonymous LDAP searches and restrict LDAP to trusted networks.",
        V("ldap_scan", "Anonymous search against {ip} returns no directory entries",
          "anonymous_search_allowed is false",
          linux="ldapsearch -x -H ldap://{ip} -b '' -s base   # RootDSE only; a subtree search must fail"),
        ("CWE-200", "MITRE T1087.002", "Microsoft — Anonymous LDAP operations (dsHeuristics)"),
        effort="medium"),

    Recipe(
        "POSTURE-SNMP-AMPLIFIER", 1, "Stop {host} being an SNMP amplifier", "mitigation", "mitigate",
        "SNMP reachable only from trusted managers, v3 only",
        (
            S("containment", "Block SNMP from untrusted sources",
              "Allow 161/udp on {host} only from the network-management stations.",
              gen=("Restrict 161/udp to {ip} from the NMS subnet at the firewall",)),
            S("fix", "Move to SNMPv3 and restrict the agent",
              "Disable v1/v2c communities and bind the agent to management interfaces.",
              net=("no snmp-server community public", "snmp-server group NMS v3 priv"),
              lin=("# net-snmp: remove rocommunity lines; add createUser + rouser for v3",
                   "sudo systemctl restart snmpd"),
              rollback="Restore the previous agent configuration.", risk="medium"),
        ),
        "Rate-limit SNMP at the edge and alert on large SNMP response volumes.",
        V("snmp_scan", "SNMP GETBULK from an untrusted source to {ip} gets no response",
          "amplification_factor not measured / below threshold",
          linux="snmpbulkwalk -v2c -c public {ip} 1.3.6.1.2.1.2.2   # expect timeout"),
        ("CWE-406", "MITRE T1498.002", "US-CERT TA14-017A — UDP-based amplification attacks"),
        effort="low"),

    Recipe(
        "POSTURE-MQTT-UNAUTHENTICATED", 1, "Require authentication on the MQTT broker {host}",
        "mitigation", "mitigate", "Broker rejects anonymous CONNECT",
        (
            S("containment", "Restrict the broker to known clients",
              "Allow 1883/8883 on {host} only from the device and application networks.",
              gen=("Restrict 1883/tcp and 8883/tcp to {ip} from trusted subnets",)),
            S("fix", "Disable anonymous access",
              "Require credentials or client certificates for every CONNECT.",
              lin=("# mosquitto.conf: allow_anonymous false  and  password_file /etc/mosquitto/passwd",
                   "sudo systemctl restart mosquitto"),
              rollback="Set allow_anonymous back to its previous value.", risk="medium"),
            S("hardening", "Use TLS and topic ACLs",
              "Serve MQTT over TLS (8883) and restrict each client to the topics it needs.",
              gen=("Enable listener 8883 with TLS and an acl_file per client",)),
        ),
        "Restrict the broker to trusted networks and monitor for unexpected subscribers to '#'.",
        V("iot_scan", "Anonymous MQTT CONNECT to {ip}:{port} is refused",
          "CONNACK return code 4/5 (not authorized)",
          linux="mosquitto_sub -h {ip} -p {port} -t '#' -C 1 -W 5   # expect 'not authorised'"),
        ("CWE-306", "MITRE T1133", "OASIS MQTT 3.1.1 — security considerations"), effort="low"),

    Recipe(
        "POSTURE-CWMP-EXPOSED", 1, "Restrict TR-069/CWMP on {host}", "mitigation", "mitigate",
        "CWMP reachable only from the ACS",
        (
            S("containment", "Block 7547 from untrusted networks",
              "Allow the CWMP port on {host} only from the provider's ACS addresses.",
              gen=("Restrict 7547/tcp to {ip} from the ACS addresses only",)),
            S("fix", "Disable or update the CWMP service",
              "Turn off remote management if unused, otherwise update the device firmware.",
              net=("Disable TR-069 / remote management in the device admin UI if it is not required",),
              gen=("Update the device firmware to the vendor's current release",),
              rollback="Re-enable remote management in the admin UI.", risk="low"),
        ),
        "Firewall the port at the edge; monitor for inbound connections to 7547.",
        V("iot_scan", "CWMP endpoint on {ip}:{port} is not reachable from the scan vantage",
          "cwmp_indicators false / port closed",
          linux="curl -s -m 5 http://{ip}:{port}/ -o /dev/null -w '%{{http_code}}'   # expect timeout"),
        ("CWE-284", "MITRE T1190", "Broadband Forum TR-069 — security considerations"), effort="low"),

    Recipe(
        "POSTURE-RTSP-EXPOSED", 1, "Restrict the RTSP stream on {host}", "mitigation", "mitigate",
        "RTSP reachable only from the video-management network, with authentication",
        (
            S("containment", "Restrict RTSP to the video network",
              "Allow 554/8554 on {host} only from the NVR / video-management subnet.",
              gen=("Restrict 554/tcp and 8554/tcp to {ip} from the video-management subnet",)),
            S("fix", "Require authentication and change default credentials",
              "Enable stream authentication on the camera and set a unique password.",
              net=("Enable RTSP authentication and set a unique admin password in the camera UI",),
              gen=("Update the camera firmware to the vendor's current release",),
              rollback="Revert the camera configuration from its backup.", risk="low"),
        ),
        "Isolate cameras on a dedicated VLAN with no route to user networks.",
        V("iot_scan", "Unauthenticated RTSP DESCRIBE to {ip}:{port} is refused",
          "RTSP responds 401 or the port is not reachable",
          linux="curl -s -m 5 -X OPTIONS rtsp://{ip}:{port}/   # expect 401 or timeout"),
        ("CWE-284", "MITRE T1021"), effort="low"),

    Recipe(
        "POSTURE-ADB-UNAUTHENTICATED", 1, "Disable network ADB on {host}", "mitigation", "mitigate",
        "ADB not listening on the network",
        (
            S("containment", "Block 5555 immediately",
              "Block 5555/tcp to {host}: an open ADB daemon is a remote shell.",
              gen=("Deny 5555/tcp to {ip} at the nearest firewall",)),
            S("fix", "Turn off ADB over TCP",
              "Disable network debugging on the device (or via MDM) and reboot it.",
              gen=("Settings > Developer options > turn off 'ADB over network' / 'Wireless debugging'",
                   "Enforce 'disable USB/ADB debugging' through the MDM policy"),
              reboot=True, downtime="device reboot",
              rollback="Re-enable developer options only on an isolated test network.", risk="low"),
        ),
        "Isolate the device until ADB is disabled; treat it as possibly compromised.",
        V("mobile_scan", "ADB CNXN to {ip}:5555 gets no reply or an AUTH challenge",
          "unauthenticated_shell is false",
          linux="adb connect {ip}:5555   # expect failure / unauthorized"),
        ("CWE-306", "MITRE T1021", "Android developer documentation — ADB over Wi-Fi"), effort="low"),

    Recipe(
        "POSTURE-AI-ENDPOINT-UNAUTHENTICATED", 1, "Require authentication on the AI endpoint {host}:{port}",
        "mitigation", "mitigate", "Inference / MCP endpoint requires authentication",
        (
            S("containment", "Restrict the endpoint to the application network",
              "Allow port {port} on {host} only from the services that call it.",
              gen=("Restrict {port}/tcp to {ip} from the application subnet",)),
            S("fix", "Put authentication in front of the endpoint",
              "Bind the model server to localhost and expose it only through an authenticating proxy.",
              lin=("# Ollama: set OLLAMA_HOST=127.0.0.1 in the service environment",
                   "sudo systemctl restart ollama"),
              gen=("Front the endpoint with a reverse proxy enforcing API keys or OAuth",
                   "For MCP servers, enable the server's OAuth authorization"),
              rollback="Restore the previous bind address / proxy configuration.", risk="medium"),
        ),
        "Monitor request volume and model usage; rotate any secrets the endpoint could expose.",
        V("mcp_ai_scan", "Discovery request to {ip}:{port} is refused without credentials",
          "unauthenticated_access is false",
          linux="curl -s -o /dev/null -w '%{{http_code}}' http://{ip}:{port}/api/tags   # expect 401/403"),
        ("CWE-306", "MITRE T1133", "OWASP Top 10 for LLM Applications"), effort="low"),
]

# ═══════════════════════════════════════════════════════════════════════════
# Exposed-service categories (port_intel) — POSTURE-EXPOSED-<CATEGORY>
# ═══════════════════════════════════════════════════════════════════════════

_E: list[Recipe] = [
    Recipe(
        "POSTURE-EXPOSED-BACKDOOR", 1, "Investigate the suspected backdoor listener on {host}:{port}",
        "mitigation", "avoid", "No backdoor/C2-class listener on {port}",
        (
            S("containment", "Isolate and preserve evidence",
              "Port {port} on {host} matches a backdoor/RAT/C2 default. Treat as a possible compromise: "
              "isolate the host, do not wipe it, and capture volatile evidence.",
              win=("Get-NetTCPConnection -LocalPort {port} | Select OwningProcess",
                   "Get-Process -Id <OwningProcess> | Select Path,StartTime"),
              lin=("sudo ss -ltnp 'sport = :{port}'", "sudo ls -l /proc/<pid>/exe"),
              gen=("Isolate {ip} at the switch/EDR and engage incident response",), risk="medium"),
            S("fix", "Remove the listener after triage",
              "Once IR has identified the owning process, remove it and its persistence.",
              gen=("Remove the process and its persistence mechanism as directed by incident response",),
              pre=("Incident response sign-off that evidence has been captured.",), risk="high",
              rollback="Not applicable — do not restore a malicious listener"),
        ),
        "Block {port} inbound and outbound at the perimeter; hunt for the same listener fleet-wide.",
        V("port_scan", "Port {port} on {ip} is closed", "closed/filtered"),
        ("MITRE T1571", "NIST SP 800-61 Rev.2 (incident handling)"), effort="high"),

    Recipe(
        "POSTURE-EXPOSED-CONTAINER", 1, "Lock down the container API on {host}:{port}", "mitigation",
        "mitigate", "Container/orchestrator API not reachable without mutual TLS",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Disable the unauthenticated API socket",
              "{service} on {host}:{port} gives root-equivalent control of the host.",
              lin=("# Docker: remove '-H tcp://0.0.0.0:{port}' from the daemon; if remote access is required use "
                   "tlsverify with client certificates", "sudo systemctl restart docker"),
              downtime="daemon restart (containers restart per their policy)", risk="medium",
              rollback="Restore the previous daemon flags"),
        ),
        "Firewall {port} to the orchestration controllers only.",
        V("port_scan", "Container API on {ip}:{port} refuses unauthenticated requests or is closed", "closed / TLS required"),
        ("CWE-306", "MITRE T1610", "CIS Docker Benchmark — 'Docker daemon configuration'"), effort="medium"),

    Recipe(
        "POSTURE-EXPOSED-DATASTORE", 1, "Restrict the exposed datastore on {host}:{port}", "mitigation",
        "mitigate", "{service} reachable only from the application tier with authentication",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Bind to the application network and require auth",
              "{service} ({product}) on {host}:{port} is reachable beyond its clients.",
              lin=("# set bind to the app interface and enable authentication in the service config",),
              gen=("Bind {service} to the application interface and enable authentication",),
              downtime="service restart", risk="medium", rollback="Restore the previous bind address"),
        ),
        "Firewall {port} to the application servers.",
        V("port_scan", "{ip}:{port} not reachable from the scan vantage", "filtered"),
        ("CWE-284", "MITRE T1213"), effort="medium"),

    Recipe(
        "POSTURE-EXPOSED-DATABASE", 1, "Restrict the exposed database listener on {host}:{port}", "mitigation",
        "mitigate", "Database listener reachable only from the application tier",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Bind the listener to the application network",
              "{product} on {host}:{port} is reachable from the scan vantage ({service}).",
              lin=("# MySQL: bind-address = <app-ip> ; PostgreSQL: listen_addresses = '<app-ip>'",),
              win=("SQL Server: restrict via Windows Firewall scope to the application servers",),
              downtime="database restart", risk="medium", rollback="Restore the previous listen address"),
        ),
        "Firewall {port} to application servers.",
        V("port_scan", "{ip}:{port} not reachable from untrusted segments", "filtered"),
        ("CWE-284", "MITRE T1190"), effort="medium"),

    Recipe(
        "POSTURE-EXPOSED-CLEARTEXT", 1, "Replace the cleartext protocol on {host}:{port}", "mitigation",
        "mitigate", "Encrypted equivalent in use; {service} disabled",
        (
            S("fix", "Disable {service} and use its encrypted equivalent",
              "{service} on {host}:{port} sends credentials in cleartext (e.g. Telnet → SSH, FTP → SFTP, "
              "HTTP admin → HTTPS).",
              lin=("sudo systemctl disable --now telnet.socket   # Telnet example",),
              net=("no service telnet ; transport input ssh   (vty lines)",),
              gen=("Disable {service} on {host} and enable the encrypted alternative",),
              pre=("Confirm every user/tool can use the encrypted alternative.",),
              downtime="users of {service} must switch", risk="medium", rollback="Re-enable {service}"),
        ),
        "Restrict {port} to the admin subnet until replaced.",
        V("port_scan", "{ip}:{port} closed", "closed"),
        ("CWE-319", "MITRE T1040"), effort="low"),

    Recipe(
        "POSTURE-EXPOSED-REMOTE_ACCESS", 1, "Restrict remote administration on {host}:{port}", "mitigation",
        "mitigate", "{service} reachable only via VPN / jump host",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Publish remote administration through a gateway",
              "{service} on {host}:{port} is reachable from the scan vantage.",
              gen=("Require VPN/jump-host access with MFA for {service}; remove direct inbound access",),
              risk="low", rollback="Restore the direct rule"),
        ),
        "Alert on logons to {service} from outside the admin network.",
        V("port_scan", "{ip}:{port} not reachable from untrusted segments", "filtered"),
        ("CWE-284", "MITRE T1021"), effort="low"),

    Recipe(
        "POSTURE-EXPOSED-ADMIN_UI", 1, "Restrict the management UI on {host}:{port}", "mitigation",
        "mitigate", "Admin interface reachable only from the admin network over HTTPS",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Move the admin interface to the management network",
              "{service} ({product}) admin UI on {host}:{port} is exposed.",
              gen=("Bind the admin UI to the management interface / ACL it to the admin subnet",),
              risk="low", rollback="Restore the previous listen address"),
            S("hardening", "Enforce MFA and HTTPS", "Require MFA and HTTPS on the admin UI.",
              gen=("Enable MFA and HTTPS-only for {product} administration",)),
        ),
        "Restrict {port} to admin hosts.",
        V("port_scan", "{ip}:{port} not reachable from untrusted segments", "filtered"),
        ("CWE-284", "MITRE T1133"), effort="low"),

    Recipe(
        "POSTURE-EXPOSED-PRINTER", 1, "Restrict the raw print port on {host}:{port}", "mitigation",
        "mitigate", "Raw printing (9100) reachable only from the print servers",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Allow raw printing only from the print servers",
              "The raw print port on {host}:{port} accepts print jobs and PJL commands from "
              "anyone who can reach it, with no authentication.",
              gen=("ACL {port}/tcp on the printer (or its switch port) to the print servers",
                   "Route user printing through the print server (IPP/SMB) instead of direct 9100"),
              risk="low", rollback="Restore the previous printer ACL"),
            S("hardening", "Disable PJL file-system and configuration access",
              "PJL can read stored jobs and files and change settings on many printers.",
              gen=("In the printer's admin settings, disable PJL file-system access and "
                   "PJL configuration changes, and set an admin password",)),
        ),
        "Allow {port}/tcp to the printer only from the print servers.",
        V("port_scan", "{ip}:{port} not reachable from user and untrusted segments", "filtered"),
        ("CWE-306", "MITRE T1046"), effort="low"),
]


# ═══════════════════════════════════════════════════════════════════════════
# Version-matched CVEs and the generic fallback
# ═══════════════════════════════════════════════════════════════════════════

CVE_PATCH = Recipe(
    "CVE-PATCH", 1, "Upgrade {product} on {host}", "vendor_fix", "mitigate", "{target}",
    (
        S("fix", "Apply the vendor fix",
          "{product} {version} on {host}:{port} is in the affected range. Upgrade to {target}.",
          lin=("sudo apt-get update && sudo apt-get install --only-upgrade {package}   # Debian/Ubuntu",
               "sudo dnf upgrade {package}   # RHEL family (package name may differ)"),
          win=("Install the vendor update (Windows Update / WSUS / vendor installer) for {product}",),
          mac=("softwareupdate --list ; install the {product} update from the vendor",),
          net=("Upgrade the appliance firmware/software to a fixed release",),
          gen=("Upgrade {product} to {target}",),
          pre=("Check the distribution changelog — distros often backport the fix without changing the "
               "upstream version number.", "Take a snapshot/backup before upgrading."),
          reboot=None, downtime="service restart; kernel/OS components may need a maintenance window",
          rollback="Reinstall the previous package version from the repository cache", risk="medium"),
        S("hardening", "Keep {product} on a patch cadence",
          "Add {product} to the monthly patch cycle and subscribe to the vendor's security advisories.",
          gen=("Subscribe to the {product} security advisory feed",)),
    ),
    "Restrict network access to {port} and monitor for exploitation until the upgrade is applied.",
    V("service_banner", "Detection re-matches the observed {product} version on {ip}:{port} against the "
      "vulnerability DB", "Observed version outside the affected range"),
    ("NVD", "Vendor security advisory"), effort="medium")

GENERIC = Recipe(
    "GENERIC", 1, "Remediate {title} on {host}", "mitigation", "mitigate",
    "Exposure reduced and vendor hardening applied",
    (
        S("containment", "Restrict the affected service",
          "Limit {service} on {host}:{port} to trusted networks while the fix is prepared.",
          gen=("Restrict {port}/tcp on {ip} to <trusted-subnet>",)),
        S("fix", "Apply the vendor guidance",
          "Apply the vendor's hardening guide and ensure {product} runs a supported, patched version.",
          gen=("Apply the vendor's security guidance for {product}",), risk="low"),
    ),
    "Segment and monitor the asset.",
    V("detection-engine", "A follow-up scan of {ip} no longer reports this finding", "Finding not re-observed"),
    (), effort="medium")


# ── Rules for UDP facts the agent already collected (M6) ──────────────────────

_P_UDP: list[Recipe] = [
    Recipe(
        "POSTURE-SIP-EXPOSED", 1, "Restrict the SIP service on {host}:{port}", "mitigation",
        "mitigate", "SIP reachable only from the trunks and phones that need it",
        (
            S("containment", "Limit SIP to known peers",
              "Allow UDP/TCP 5060 and TLS 5061 on {host} ({ip}) only from your SIP trunk providers "
              "and internal phone networks.",
              lin=("sudo ufw allow from <trusted-subnet> to any port 5060 proto udp",
                   "sudo ufw deny 5060/udp"),
              net=("Add an ACL on the upstream firewall permitting 5060/5061 to {ip} only from <trusted-subnet>",),
              gen=("Restrict 5060/5061 on {ip} to <trusted-subnet> at the nearest firewall",),
              rollback="Remove the rule to restore the previous reachability."),
            S("fix", "Harden registration and calling",
              "Require authentication on REGISTER/INVITE, rate-limit failed registrations, and block "
              "international or premium-rate dial plans that are not needed.",
              gen=("Enable SIP digest authentication, fail2ban-style lockout and call-barring on the PBX/SBC",)),
        ),
        "Place the PBX behind an SBC and allow SIP only from provider address ranges.",
        V("udp_scan", "SIP OPTIONS to {ip}:{port}/udp from an untrusted network gets no SIP reply",
          "No response / filtered"),
        ("CWE-200", "MITRE T1595.002"), effort="low"),

    Recipe(
        "POSTURE-UPNP-IGD-EXPOSED", 1, "Turn off UPnP IGD on the gateway {host}", "mitigation",
        "mitigate", "No UPnP Internet Gateway Device answering on this segment or the WAN",
        (
            S("containment", "Remove port mappings nobody owns",
              "List the gateway's current UPnP port mappings and delete any that no approved "
              "service needs.",
              gen=("In the router/firewall admin UI, open the UPnP mapping table and remove unknown mappings",),
              rollback="Re-add a mapping only with a change request naming its owner."),
            S("fix", "Disable UPnP IGD",
              "Turn off UPnP/IGD on {host} ({ip}); where a consumer segment needs it, enable it "
              "on that VLAN only, never on the WAN interface.",
              net=("Disable UPnP IGD (or limit it to the consumer VLAN) in the gateway configuration",),
              gen=("Disable UPnP Internet Gateway Device support on {ip}",),
              rollback="Re-enable UPnP on the one VLAN that needs it."),
        ),
        "Publish inbound services only through reviewed static NAT rules.",
        V("iot_scan", "Unicast M-SEARCH to {ip}:1900/udp gets no InternetGatewayDevice reply",
          "No IGD in the SSDP reply"),
        ("CWE-306", "MITRE T1599"), effort="low"),

    Recipe(
        "POSTURE-UPNP-EXPOSED", 1, "Disable UPnP/SSDP on {host}", "mitigation",
        "mitigate", "UPnP/SSDP off, or limited to the segment that needs discovery",
        (
            S("fix", "Turn off UPnP discovery",
              "Disable UPnP/SSDP on {host} ({ip}) unless a documented use needs it, and block "
              "UDP/1900 between segments.",
              net=("Block UDP/1900 between VLANs and at the perimeter",),
              gen=("Disable UPnP / SSDP / DLNA discovery in the device settings of {ip}",),
              rollback="Re-enable discovery on the device."),
        ),
        "Keep discovery protocols on the segment that uses them.",
        V("iot_scan", "Unicast M-SEARCH to {ip}:1900/udp gets no reply from an untrusted segment",
          "No SSDP reply"),
        ("CWE-200", "MITRE T1046"), effort="low"),

    Recipe(
        "POSTURE-NETBIOS-EXPOSED", 1, "Close the NetBIOS name service on {host}", "mitigation",
        "mitigate", "NetBIOS name service not reachable from untrusted networks",
        (
            S("containment", "Block NetBIOS at the boundary",
              "Drop UDP/137 and 138 and TCP/139 to {host} ({ip}) from networks that do not need "
              "Windows name resolution.",
              net=("Deny udp/137, udp/138 and tcp/139 to {ip} from <untrusted-subnet>",),
              gen=("Block UDP 137/138 and TCP 139 to {ip} from untrusted networks",)),
            S("fix", "Disable NetBIOS over TCP/IP where it is not needed",
              "Disable NetBIOS over TCP/IP on the interface of {host}; keep DNS for name resolution.",
              win=("Get-NetAdapter | ForEach-Object {{ (Get-WmiObject Win32_NetworkAdapterConfiguration "
                   "-Filter \"Index=$($_.InterfaceIndex)\").SetTcpipNetbios(2) }}",),
              lin=("# Samba: in [global] of /etc/samba/smb.conf set:  disable netbios = yes",
                   "sudo testparm -s && sudo systemctl restart smbd"),
              gen=("Disable NetBIOS over TCP/IP in the host's network settings",),
              downtime="legacy name lookups stop working", rollback="Re-enable NetBIOS over TCP/IP"),
        ),
        "Use DNS only for name resolution and disable LLMNR/NBT-NS by policy.",
        V("udp_scan", "NetBIOS node-status query to {ip}:{port}/udp from an untrusted network gets no reply",
          "No response / filtered"),
        ("CWE-200", "MITRE T1046"), effort="low"),

    Recipe(
        "POSTURE-MDNS-EXPOSED", 1, "Keep mDNS on the local link for {host}", "mitigation",
        "mitigate", "Multicast DNS not answering queries from routed networks",
        (
            S("containment", "Block mDNS from routed networks",
              "Drop UDP/5353 to {host} ({ip}) from anything other than the local segment.",
              net=("Deny udp/5353 to {ip} from routed (non-local) networks",),
              gen=("Block UDP 5353 to {ip} from routed networks",)),
            S("fix", "Disable the responder where discovery is not needed",
              "Stop the Avahi/Bonjour responder on {host} if no service discovery is required.",
              lin=("sudo systemctl disable --now avahi-daemon.socket avahi-daemon.service",),
              win=("Set-Service -Name 'Bonjour Service' -StartupType Disabled -ErrorAction SilentlyContinue",),
              gen=("Disable the mDNS/Bonjour/Avahi responder",),
              downtime="local service discovery stops", rollback="Re-enable the responder"),
        ),
        "Restrict service discovery to the segments that need it.",
        V("udp_scan", "A unicast mDNS query to {ip}:{port}/udp gets no response", "No response"),
        ("CWE-200", "MITRE T1046"), effort="low"),

    Recipe(
        "POSTURE-IKE-AGGRESSIVE-MODE", 1, "Disable IKE aggressive mode on {host}", "mitigation",
        "mitigate", "IKEv1 aggressive mode disabled; IKEv2 or main mode with strong authentication",
        (
            S("fix", "Turn off aggressive mode",
              "Disable IKEv1 aggressive mode on the VPN gateway {host} and move peers to main mode "
              "or IKEv2.",
              net=("Disable IKE aggressive mode in the gateway's IKE/ISAKMP policy",),
              lin=("# strongSwan: in ipsec.conf set  aggressive=no  and  keyexchange=ikev2",
                   "sudo ipsec reload"),
              gen=("Disable IKEv1 aggressive mode in the VPN gateway configuration",),
              downtime="peers using aggressive mode must be reconfigured", rollback="Restore the previous IKE policy"),
            S("hardening", "Replace weak pre-shared keys",
              "Rotate any pre-shared key that was used with aggressive mode to a long random value, "
              "or move to certificate authentication.",
              gen=("Rotate the pre-shared key (>= 20 random characters) or use certificates",)),
        ),
        "Prefer certificate-based IKEv2 and monitor for repeated aggressive-mode requests.",
        V("udp_scan", "An IKE probe to {ip}:{port}/udp is not answered in aggressive mode",
          "Exchange type is not 4 (aggressive)"),
        ("CWE-522", "MITRE T1110.002"), effort="medium"),

    Recipe(
        "POSTURE-SNMPV3-NOAUTH-USER", 1, "Require authentication for SNMPv3 on {host}", "mitigation",
        "mitigate", "Every SNMPv3 user is authPriv (SHA-2 + AES); no noAuthNoPriv users",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Delete noAuthNoPriv users and require authPriv",
              "An SNMPv3 user on {host} answers reads with no authentication or encryption. Remove it "
              "and configure users with SHA-2 authentication and AES privacy.",
              lin=("# net-snmp: remove the user from /var/lib/snmp/snmpd.conf and snmpd.conf, then:",
                   "sudo net-snmp-create-v3-user -ro -A '<auth-passphrase>' -a SHA -X '<priv-passphrase>' -x AES <user>",
                   "sudo systemctl restart snmpd"),
              net=("Delete SNMPv3 users at noAuthNoPriv and require authPriv in the SNMP group settings",),
              downtime="brief SNMP agent restart", rollback="Restore the previous SNMP configuration"),
        ),
        "Restrict SNMP to the management network and monitor for unauthenticated reads.",
        V("snmp_scan", "An SNMPv3 noAuthNoPriv read to {ip}:{port}/udp returns a Report, not a GetResponse",
          "No noAuthNoPriv user answers"),
        ("CWE-306", "MITRE T1078"), effort="low"),

    Recipe(
        "POSTURE-FTP-ANONYMOUS-WRITE", 1, "Remove anonymous upload on {host}", "mitigation", "mitigate",
        "Anonymous FTP cannot create, modify or delete files",
        (
            _FIREWALL_CONTAIN,
            S("fix", "Revoke write permission from the anonymous account",
              "{product} on {host}:{port} accepted an anonymous upload. Remove write access, or "
              "disable anonymous access altogether.",
              lin=("# vsftpd: in /etc/vsftpd.conf set",
                   "#   anonymous_enable=NO   (or: anon_upload_enable=NO, anon_mkdir_write_enable=NO, anon_other_write_enable=NO)",
                   "sudo systemctl restart vsftpd"),
              win=("Set-WebConfigurationProperty -Filter /system.ftpServer/security/authentication/"
                   "anonymousAuthentication -Name enabled -Value False -PSPath IIS:\\",),
              gen=("Disable anonymous FTP or make its directories read-only",),
              pre=("Check the FTP root for unexpected files an attacker may already have uploaded.",),
              downtime="brief FTP service restart", rollback="Restore the previous FTP configuration",
              risk="low"),
        ),
        "Replace FTP with SFTP and authenticated access.",
        V("ftp_scan", "An anonymous upload to {ip}:{port}/tcp is refused (550/553)", "Write refused"),
        ("CWE-732", "MITRE T1105"), effort="low"),

    Recipe(
        "POSTURE-UNIDENTIFIED-SERVICE", 1, "Identify and review the service on {host}:{port}",
        "mitigation", "mitigate", "The listener is identified, approved and restricted, or closed",
        (
            S("containment", "Restrict the unknown listener",
              "Until it is identified, allow port {port} on {host} ({ip}) only from the networks "
              "that must reach it.",
              lin=("sudo ufw allow from <trusted-subnet> to any port {port} proto tcp",
                   "sudo ufw deny {port}/tcp"),
              win=("New-NetFirewallRule -DisplayName 'Restrict {port}' -Direction Inbound -Protocol TCP "
                   "-LocalPort {port} -RemoteAddress <trusted-subnet> -Action Allow",),
              net=("Add an ACL on the upstream firewall permitting {port}/tcp to {ip} only from <trusted-subnet>",),
              gen=("Restrict {port}/tcp on {ip} to <trusted-subnet> at the nearest firewall",),
              rollback="Remove the rule to restore the previous reachability."),
            S("fix", "Identify the owner of the listener",
              "Find the process behind port {port} on {host}, confirm it is approved, then close it "
              "or document it.",
              lin=("sudo ss -ltnp | grep ':{port} '",),
              win=("Get-NetTCPConnection -LocalPort {port} | Select-Object OwningProcess; "
                   "Get-Process -Id (Get-NetTCPConnection -LocalPort {port}).OwningProcess",),
              gen=("Identify the application listening on {port}/tcp and confirm it is approved",)),
        ),
        "Keep a register of approved listening services per host and alert on new ones.",
        V("service_banner", "A banner probe of {ip}:{port}/tcp identifies the service or the port is closed",
          "identified is true, or the port is closed"),
        ("CWE-1188", "MITRE T1046"), effort="low"),
]

RECIPES: dict[str, Recipe] = {r.recipe_id: r for r in (*_P, *_P_V2, *_P_UDP, *_E, CVE_PATCH, GENERIC)}

# Legacy keyword categories (remediation_kb.classify_finding) → recipe ids, for
# findings that carry no structured rule id (imports, older probe paths).
LEGACY_CATEGORY: dict[str, str] = {
    "weak_tls": "POSTURE-TLS-DEPRECATED-VERSION",
    "smb_signing": "POSTURE-SMB-SIGNING-OFF",
    "exposed_rdp": "POSTURE-RDP-EXPOSED",
    "default_credentials": "POSTURE-DEFAULT-CRED-CANDIDATE",
    "missing_patch": "CVE-PATCH",
    "open_mgmt_port": "POSTURE-EXPOSED-REMOTE_ACCESS",
    "anon_ftp": "POSTURE-FTP-ANONYMOUS-LOGIN",
    "outdated_ssh": "POSTURE-SSH-WEAK-ALGORITHMS",
}


# A composite attack-path finding (CORR-*) is fixed by fixing the weakness it is built from, so it
# borrows that weakness's recipe instead of falling to the generic one.
CORRELATION_RECIPE: dict[str, str] = {
    "CORR-NTLM-RELAY-PATH": "POSTURE-SMB-SIGNING-OFF",
    "CORR-LEGACY-WINDOWS-SURFACE": "POSTURE-SMB-V1-ENABLED",
    "CORR-CLEARTEXT-CLUSTER": "POSTURE-EXPOSED-CLEARTEXT",
    "CORR-DB-UNAUTH-EXPOSED": "POSTURE-DB-UNAUTHENTICATED-ACCESS",
    "CORR-SNMP-PUBLIC-LATERAL": "POSTURE-SNMP-DEFAULT-COMMUNITY",
    "CORR-AD-EXPOSURE": "POSTURE-LDAP-ANONYMOUS-BIND",
    "CORR-MGMT-PLANE-EXPOSED": "POSTURE-RDP-EXPOSED",       # IPMI variant chosen below
}


def _correlation_recipe_id(rule_id: str, finding: Any) -> str | None:
    target = CORRELATION_RECIPE.get(rule_id)
    if target is None:
        return None
    if rule_id == "CORR-MGMT-PLANE-EXPOSED":
        ev = getattr(finding, "evidence", None)
        blob = str((ev or {}).get("correlated") if isinstance(ev, dict) else "")
        text = f"{getattr(finding, 'title', '')} {getattr(finding, 'description', '')} {blob}".lower()
        if "ipmi" in text or "bmc" in text:
            return "POSTURE-IPMI-CIPHER-ZERO"
    return target


def resolve_recipe(ctx: Any, finding: Any) -> Recipe:
    """rule id → composite's component → exposed-service category → CVE → legacy keyword class → generic."""
    if ctx.rule_id and ctx.rule_id in RECIPES:
        return RECIPES[ctx.rule_id]
    corr = _correlation_recipe_id(ctx.rule_id or "", finding) if ctx.rule_id else None
    if corr and corr in RECIPES:
        return RECIPES[corr]
    if ctx.category:
        key = f"POSTURE-EXPOSED-{ctx.category.upper()}"
        if key in RECIPES:
            return RECIPES[key]
    if ctx.cve_ids:
        return CVE_PATCH
    from app.services.remediation_kb import classify_finding
    mapped = LEGACY_CATEGORY.get(classify_finding(finding))
    return RECIPES[mapped] if mapped else GENERIC
