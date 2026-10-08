# #13 CERT-In's 15 controls: what Vedha really produces evidence for

**Done when:** this verified mapping table exists. It's the source of truth for #15 (the public guide and one-page PDF), the partner kit, and every sales line that mentions CERT-In.

## How it was verified

- **Code:** every rule ID below exists in `manager/detection_engine/posture_rules.py`, `correlate.py` or the probe scanners (grep of the repo, 4 Oct).
- **Shipped status:** only rows marked ✅ in `NETWORK_VA_USE_CASES.md` count; 🟡 pipeline items are excluded.
- **Real output:** where possible, the evidence shape was matched to actual probe runs in `probe/scans/` (no customer data).
- **Owner scope (4 Oct):** backup, password and patching checks are **not offered**, even where code exists.

**About the 15 controls list:** cert-in.org.in is blocked from this environment, so the names come from law-firm and security-firm summaries of **CISG-2025-03 (1 Sep 2025, 45 recommendations under 15 controls)**. The **order of #14 and #15 isn't confirmed.** Check names and order against the PDF before #15 is published.

## Summary: 3 with evidence · 4 partial · 2 not offered (owner decision) · 6 not covered

| # | Control | Vedha | What Vedha produces | Don't claim |
|---|---|---|---|---|
| 1 | Effective Asset Management (EAM) | ✅ Evidence | Network discovery + device inventory and classification (UC 1, UC 2); OS fusion (ASSET-OS-IDENTIFIED); open-port inventory per host | Network-visible devices only: no software licences, owners, purchase records or devices that are switched off |
| 2 | Network and Email Security (NES) | ◐ Partial | Network: SVC-RDP-EXPOSED, MSRPC-ENDPOINTS-EXPOSED, SMB-SIGNING-NOT-REQUIRED, UDP-AMPLIFIER-EXPOSED / UDP-DNS-OPEN-RESOLVER / UDP-NTP-MONLIST, SVC-DATASTORE-EXPOSED, internet-exposure mapping (UC 81). Email: only POSTURE-SMTP-NO-STARTTLS and SMTP-USER-ENUM on mail servers inside the network | Email security (spam/phishing filtering, SPF/DKIM/DMARC, cloud mailboxes) is NOT checked; office networks only, not cloud |
| 3 | Endpoint & Mobile Security (EMS) | ✗ Not covered | None in the 7-day check. A separate macOS endpoint agent exists but is still in validation (15 of 42 collectors passing) | Don't claim. The network view of endpoints (exposed RDP/SMB) is under NES and SC |
| 4 | Secure Configurations (SC) | ✅ Evidence | POSTURE-SMB-V1-ENABLED, POSTURE-SMB-SIGNING-OFF, POSTURE-SMB-NULL-SESSION, POSTURE-RDP-NO-NLA, POSTURE-RDP-NO-TLS, POSTURE-VNC-NO-AUTH / WEAK-AUTH, POSTURE-FTP-ANONYMOUS-LOGIN, POSTURE-NFS-WORLD-READABLE-EXPORT, POSTURE-RSYNC-ANONYMOUS-MODULE, POSTURE-LDAP-ANONYMOUS-BIND, POSTURE-DNS-ZONE-TRANSFER, POSTURE-TLS-* (deprecated version, weak cipher, self-signed, expired), POSTURE-SSH-WEAK-ALGORITHMS, SVC-TELNET-CLEARTEXT, WEB-MISSING-SECURITY-HEADERS | Configurations visible from the network only; no host hardening baselines (GPOs, local policies) |
| 5 | Patch Management (PM) | ⊘ Not offered | Code exists: POSTURE-OS-END-OF-LIFE (EOL catalog) and CVE correlation with CISA KEV / EPSS | Owner decision (4 Oct): patching checks are NOT offered in the 7-day check. Don't claim |
| 6 | Incident Management (IM) | ✗ Not covered | None. (The compliance pack knows the CERT-In 6-hour reporting clock, but Vedha doesn't run incident response) | Don't claim |
| 7 | Logging and Monitoring (LM) | ✗ Not covered | None. Re-scan change detection (UC 11) is still in the pipeline, not shipped | Don't claim; a 7-day check isn't monitoring |
| 8 | Awareness and Training (AT) | ✗ Not covered | None | Don't claim |
| 9 | Third Party Risk Management (TPRM) | ✗ Not covered | None for the customer's vendors. Vedha's own data-handling statement can go into the customer's vendor file | Don't claim beyond 'our own vendor documentation' |
| 10 | Data Protection, Backup and Recovery (DPBR) | ◐ Partial | Data exposure on the network only: CORR-ANON-DATA-EXPOSURE, POSTURE-NFS-WORLD-READABLE-EXPORT, POSTURE-DB-UNAUTHENTICATED-ACCESS, POSTURE-DB-CLEARTEXT-TRANSPORT | Backup and recovery are NOT checked (owner decision). Claim only 'shared folders or databases readable without a password' |
| 11 | Governance and Compliance (GC) | ◐ Partial | A dated, evidence-backed report and a re-check record the auditor can file; compliance citations with the disclaimer 'not legal advice or a compliance attestation' | Vedha provides evidence for the file, not governance or compliance itself |
| 12 | Robust Password Policy (RPP) | ⊘ Not offered | Code exists: POSTURE-DEFAULT-CRED-CANDIDATE, POSTURE-SNMP-DEFAULT-COMMUNITY, POSTURE-IPMI-CIPHER-ZERO | Owner decision (4 Oct): password checks are NOT offered. Don't claim |
| 13 | Access Control and Identity Management (ACIM) | ◐ Partial | Network-visible access control: remote access exposed (SVC-RDP-EXPOSED, VNC, WinRM), anonymous access (FTP, NFS, rsync, LDAP, SMB null session), unauthenticated databases (SVC-UNAUTH-DATASTORE-ACCESS) | Identity management (user accounts, MFA, privileges, joiners and leavers) is NOT checked |
| 14 | Physical Security (PS) [order to verify] | ✗ Not covered | None | Don't claim |
| 15 | Vulnerability Audits and Assessments (VAA) [order to verify] | ✅ Evidence | The core product: network vulnerability assessment with evidence, confidence (confirmed vs suspected) and a re-check after fixes | The guideline asks for audits BY CERT-In empanelled auditors. Vedha produces the evidence an auditor uses; it is NOT the audit and not empanelled |

Full table with the 'verified against' column: `mapping.csv`.

## The honest one-liner (use this in #15 and in partner messages)

> Vedha produces network evidence for **3 of CERT-In's 15 MSME controls** (asset management, secure configurations, vulnerability assessment) and **part of 4 more** (network security, data exposure, access control, governance records). The rest need other work, and your IT partner or a CERT-In empanelled auditor covers them.

## What to never say

- "CERT-In compliant", "CERT-In approved" or "CERT-In certified". Vedha isn't empanelled and doesn't certify anyone.
- "Covers all 15 controls" or any count higher than the table above.
- Anything about patching, passwords or backups (owner scope).

## Product gap this exposed (for the roadmap, not marketing)

`app/compliance/packs/india.py` maps findings to RBI, SEBI, IRDAI, CERT-In Directions 2022 and DPDP, but **not to CISG-2025-03 (the MSME controls)**. Adding a `certin_msme_2025` pack using this table (EAM, NES, SC, ACIM, DPBR-exposure, VAA) would let every report cite the MSME control each finding supports. That's the evidence auditors will ask for.

Sources for the control list: [CERT-In PDF](https://www.cert-in.org.in/PDF/Elemental_Cyber_Defense_Controls_for_MSME.pdf), [Lexology](https://www.lexology.com/library/detail.aspx?g=7f1ac82f-8d75-4cf4-84df-97355ed9dc54), [Deccan Chronicle](https://www.deccanchronicle.com/southern-states/telangana/15-elemental-cyber-defense-controls-to-secure-msmes-1906169), [Mondaq](https://www.mondaq.com/india/security/1712906/cert-in-issues-guidelines-to-strengthen-cybersecurity-in-msmes).
