# 05 — Windows Estate (Core-Level Playbook)

> **Goal:** Assess a Windows/Active Directory environment from a single host: enumerate the domain,
> find misconfigurations and known-vulnerable services, and map attack paths — grounded in how
> SMB, MS-RPC, LDAP, Kerberos, and NTLM actually work on the wire.

---

## 1. Core theory: Windows networking is a stack of protocols on a few ports

An AD environment concentrates on a handful of TCP/UDP ports, each a rich protocol:

| Port | Protocol | Core role |
|------|----------|-----------|
| 445/tcp | SMB/CIFS | File sharing, named pipes → carries MS-RPC (SAMR, LSARPC, SVCCTL, etc.) |
| 139/tcp + 137-138/udp | NetBIOS | Legacy name service/session; NBNS name leaks |
| 135/tcp | MS-RPC EPM | Endpoint Mapper — "which dynamic port hosts which RPC interface" |
| 49152-65535/tcp | Dynamic RPC | Actual RPC service endpoints (DCOM, etc.) |
| 389/tcp+udp | LDAP | Directory queries (users, groups, computers, ACLs, GPOs) |
| 636/tcp | LDAPS | LDAP over TLS |
| 3268/3269 | Global Catalog | Forest-wide LDAP |
| 88/tcp+udp | Kerberos | Authentication (TGT/TGS tickets) |
| 464 | kpasswd | Password change |
| 53 | DNS | AD is DNS-dependent; SRV records locate DCs |
| 3389 | RDP | Remote desktop |
| 5985/5986 | WinRM | PowerShell remoting (HTTP/HTTPS) |
| 5357 | WSDAPI | Device discovery |

**Finding domain controllers** = find hosts serving 88+389+445+53 together, or query DNS SRV
records: `_ldap._tcp.dc._msdcs.<domain>`, `_kerberos._tcp.<domain>`.

### 1.1 Authentication internals you exploit
- **NTLM** (challenge/response over SMB/RPC/HTTP): relayable and crackable. **SMB signing** is the
  control — if signing is *not required*, NTLM relay (e.g., to LDAP/SMB) enables auth coercion
  attacks. This is a first-order finding.
- **Kerberos** (tickets, port 88): the AS-REQ/AS-REP and TGS-REQ/TGS-REP exchanges enable:
  - **AS-REP roasting** — accounts with "Do not require pre-auth" leak an AS-REP encrypted with the
    user's key → offline crack.
  - **Kerberoasting** — any authenticated user can request a **TGS** for any service account (SPN);
    the ticket is encrypted with the service account's NTLM hash → offline crack.
  - **Clock skew matters** (Kerberos requires <5 min skew) — a low-level gotcha.
- **LDAP** exposes the entire directory: users, `servicePrincipalName` (SPNs → kerberoast targets),
  `userAccountControl` flags (pre-auth, delegation), ACLs (attack paths), GPOs, and often
  passwords in description fields or GPP `cpassword` (legacy).

---

## 2. The high-value finding classes (vuln logic)

1. **Null/anonymous access:** anonymous SMB session, anonymous LDAP bind, RID cycling via SAMR →
   full user list with no creds.
2. **SMB signing not required** → NTLM relay / coercion (PetitPotam, PrinterBug via MS-RPC
   `MS-EFSR`/`MS-RPRN`) → relay to AD CS / LDAP → privilege escalation.
3. **Legacy critical RCE:** **MS17-010 (EternalBlue)** in SMBv1, SMBGhost (CVE-2020-0796) in SMBv3,
   Zerologon (CVE-2020-1472, Netlogon MS-RPC), PrintNightmare (spooler).
4. **Kerberoastable / AS-REP-roastable accounts** → offline hash crack → valid creds.
5. **Weak/legacy protocols enabled:** SMBv1, NTLMv1, LLMNR/NBT-NS poisoning (Responder) → hash
   capture. LLMNR/NBNS are the classic internal-network credential capture path.
6. **AD misconfig / attack paths:** unconstrained/constrained delegation, dangerous ACLs,
   `AdminCount`, GPO abuse — mapped with BloodHound.
7. **AD CS (ESC1-ESC8):** vulnerable certificate templates → domain privilege escalation.

---

## 3. Approach from a single system (methodology + commands)

**Unauthenticated (from a foothold with no creds):**
```bash
# Find DCs & Windows hosts
nmap -p 88,135,139,389,445,636,3268,3389,5985 -sV --script "smb-os-discovery,smb2-security-mode,ldap-rootdse" -iL live.txt -oX win.xml

# SMB posture: dialects, signing, null session
crackmapexec smb <cidr>                      # one-line: hostname, domain, signing, SMBv1
crackmapexec smb <cidr> -u '' -p '' --shares # null session shares
enum4linux-ng -A <host>                      # users, groups, shares, policy via null/guest

# Legacy vuln checks (safe NSE)
nmap -p445 --script smb-vuln-ms17-010,smb-vuln-cve-2020-0796 <hosts>

# LDAP anonymous
ldapsearch -x -H ldap://<dc> -s base namingContexts
nmap -p389 --script ldap-rootdse,ldap-search <dc>

# LLMNR/NBT-NS/mDNS poisoning capture (in scope!)
responder -I eth0 -A            # analyze-only first; then active capture with authorization
```

**Authenticated (with any domain user — even low-priv):**
```bash
# Full directory enumeration
ldapdomaindump -u 'DOMAIN\user' -p 'pass' <dc>
bloodhound-python -u user -p pass -d domain.local -c All   # collect attack-path graph

# Kerberoast + AS-REP roast
GetUserSPNs.py domain/user:pass -dc-ip <dc> -request       # → crackable TGS hashes
GetNPUsers.py domain/ -usersfile users.txt -dc-ip <dc>     # AS-REP roast
# Zerologon / other DC checks — carefully, non-destructive scanners only
```

**Then:** feed BloodHound graph → shortest path to Domain Admin; crack roasted hashes offline;
map SMB-signing-disabled hosts for relay.

---

## 4. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| SMBv1 disabled → MS17-010 N/A | Modern hardening | Pivot to SMBv3 (SMBGhost), Netlogon (Zerologon), Kerberos roasting, relay |
| Null sessions blocked | `RestrictAnonymous` | Need any credential; capture via LLMNR/Responder or password spray |
| Kerberos clock skew errors | >5 min offset | Sync to DC time (`ntpdate`/`net time`); Kerberos is time-sensitive |
| Dynamic RPC ports | EPM maps interfaces to high ports | Query 135 Endpoint Mapper first (`rpcdump.py`), then hit the mapped port |
| Account lockout on spray | Domain lockout policy | Read policy first (`--pass-pol`); spray ≤ N-1 attempts per window, slow, one password many users |
| EDR/AV detects tooling | Signatured tools (mimikatz, CME) | Prefer read-only enumeration; obfuscate only within authorized red-team scope |
| LDAP signing/channel binding required | Hardening against relay | Note as *good* control; adjust relay targets; use LDAPS |
| Noisy Responder poisons prod | Active LLMNR spoofing affects real users | Analyze-mode first; get explicit sign-off before active poisoning |
| Segmentation blocks 445 | Firewalled DCs | Find any reachable member server; pivot; abuse allowed protocols (WinRM/RDP) |
| False DC identification | Member server with some ports | Confirm via LDAP rootDSE / SRV records, not port heuristics alone |

---

## 5. Considerations & guardrails

- **Kerberoasting and enumeration are low-noise but logged (event IDs 4768/4769).** Coordinate
  with blue team; these are also great detections to validate.
- **NTLM relay and coercion can disrupt services** — scope carefully.
- **Password spraying risks lockouts** — always read lockout policy first.
- **Domain-wide impact:** Zerologon/DC attacks can break the domain — use non-destructive
  detection only unless explicitly authorized on a lab.

---

## 6. References

- Microsoft Open Specs: MS-SMB2, MS-RPCE, MS-NRPC (Netlogon), MS-KILE (Kerberos), MS-ADTS (AD).
- RFC 4120 (Kerberos v5), RFC 4511 (LDAP).
- CVEs: MS17-010, CVE-2020-1472 (Zerologon), CVE-2020-0796 (SMBGhost), PrintNightmare
  (CVE-2021-34527), PetitPotam (MS-EFSR).
- Tooling: Impacket, CrackMapExec/NetExec, BloodHound/SharpHound, Responder, Certipy (AD CS),
  enum4linux-ng.
- MITRE ATT&CK: Credential Access (TA0006), Lateral Movement (TA0008), T1558 (Kerberos),
  T1557 (Adversary-in-the-Middle / LLMNR).
