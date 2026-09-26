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
{fixed_version} {target}; a missing fact renders "not recorded". Every command
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
# Posture rules (29) — keyed by rule_id
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
]


# ═══════════════════════════════════════════════════════════════════════════
# Version-matched CVEs and the generic fallback
# ═══════════════════════════════════════════════════════════════════════════

CVE_PATCH = Recipe(
    "CVE-PATCH", 1, "Upgrade {product} on {host}", "vendor_fix", "mitigate", "{target}",
    (
        S("fix", "Apply the vendor fix",
          "{product} {version} on {host}:{port} is in the affected range. Upgrade to {target}.",
          lin=("sudo apt-get update && sudo apt-get install --only-upgrade <package>   # Debian/Ubuntu",
               "sudo dnf upgrade <package>   # RHEL family"),
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


RECIPES: dict[str, Recipe] = {r.recipe_id: r for r in (*_P, *_E, CVE_PATCH, GENERIC)}

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


def resolve_recipe(ctx: Any, finding: Any) -> Recipe:
    """rule id → exposed-service category → CVE → legacy keyword class → generic."""
    if ctx.rule_id and ctx.rule_id in RECIPES:
        return RECIPES[ctx.rule_id]
    if ctx.category:
        key = f"POSTURE-EXPOSED-{ctx.category.upper()}"
        if key in RECIPES:
            return RECIPES[key]
    if ctx.cve_ids:
        return CVE_PATCH
    from app.services.remediation_kb import classify_finding
    mapped = LEGACY_CATEGORY.get(classify_finding(finding))
    return RECIPES[mapped] if mapped else GENERIC
