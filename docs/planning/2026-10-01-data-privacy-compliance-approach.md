# Data privacy and compliance — approach for the agent and the platform

Date: 2026-10-01 · Status: **approach for review — nothing implemented** · Companion to
[`2026-10-01-agent-install-approach.md`](2026-10-01-agent-install-approach.md)

> This is an engineering approach, not legal advice. The contract documents in §6 should be
> reviewed by counsel before they go to customers.

## 1. Summary

Vedha puts an agent inside a customer's network and sends what it finds to a cloud manager, and
optionally to AI providers. For Indian BFSI customers that sits under four sets of rules at once:
**DPDP Act 2023 + DPDP Rules 2025**, **CERT-In Directions 2022**, **RBI IT-outsourcing directions**
and **SEBI CSCRF**. EU customers add **GDPR**.

The platform already has a good base (agent data minimisation, encrypted agent queue, India
hosting in AWS Mumbai, AI pseudonymisation and a no-cloud-AI mode, encrypted credentials, audit
log, compliance packs). **The gaps are retention, deletion, logs, AI defaults, sensitive evidence,
and the contract paperwork customers will ask for.**

Recommended stance: **Vedha acts as a data processor for scan data; everything stays in India by
default; nothing leaves India or reaches an AI model unless the customer has switched it on; every
piece of data has a retention period and can be deleted on request with a deletion certificate.**

## 2. Which rules apply, and what they ask of a vendor like Vedha

| Rule | Applies because | What it means for Vedha | Status / date |
|---|---|---|---|
| **DPDP Act 2023 + Rules 2025** | Scan data contains personal data: IP and MAC addresses, hostnames and account names that identify employees; portal accounts hold names and emails | Customer = data fiduciary, Vedha = **data processor** for scan data, under a contract. Vedha = fiduciary for its own users' accounts. Rule 6 security safeguards: encryption, access control, monitoring, **logs kept for one year**. Breach: inform the Board within **72 hours** (via the fiduciary). Cross-border: allowed unless a country is blacklisted | Rules notified **13 Nov 2025**; most obligations apply ~18 months later (**~May 2027**). Build now. |
| **CERT-In Directions 2022** | Vedha is a body corporate / service provider running ICT systems | Keep **logs of all ICT systems for 180 days within India**; report listed incidents (incl. targeted scanning, data breach) within **6 hours**; sync clocks to NTP | In force |
| **RBI IT Outsourcing Directions 2023** (banks, NBFCs) | A scanning SaaS holding bank data is outsourced IT / cloud | Contract must cover: **data stored only in India** where required, **audit rights** for the bank, RBI and their auditors, breach notice, list of sub-contractors, exit and data return, NDA | In force since 1 Oct 2023 |
| **SEBI CSCRF 2024** (brokers, AMCs, exchanges) | Same | Regulated data stored in India; vendor security assurance; cloud framework controls | In force (phased by entity size) |
| **IRDAI ISG 2023** (insurers) | Same | Similar vendor and data-location controls | In force |
| **GDPR** (EU customers) | IP addresses are personal data (EDPB) | Art. 28 processor contract (DPA), records of processing, transfers out of the EU need SCCs, EU hosting often required in practice | In force |

## 3. What data Vedha holds (data map)

| Data | Where it lives | Personal data? | Sensitivity | Who controls it |
|---|---|---|---|---|
| Scan facts: IPs, MACs, hostnames, open ports, service versions, OS | Agent queue (encrypted, transient) → manager DB | Yes (identifiers of people's devices) | Confidential | Customer |
| AD findings: account names, SPNs, password-last-set; **Kerberoast `$krb5tgs$` hashes** | Manager DB as evidence | Yes | **Highly sensitive — crackable credential material** | Customer |
| Scan credentials (SSH/WinRM/AD) | Manager DB, encrypted (`credential_crypto`) | Indirectly | Secret | Customer |
| Findings, reports, remediation notes, exports | Manager DB, browser downloads | Yes (via identifiers) | Confidential | Customer |
| Portal / operator accounts: name, email, login IPs | Manager DB, audit log | Yes | Personal | Vedha (customer for its own users) |
| AI prompts and answers | Sent to Anthropic / OpenAI / Google / Groq / OpenRouter (US); AI audit chain | Yes, unless pseudonymised | Confidential | Customer data, Vedha's sub-processors |
| Application and access logs | Docker json-file on the EC2 host | Yes (IPs, emails) | Personal | Vedha |
| Backups | Not configured / not verified | — | — | — |

## 4. What already exists (verified on `main`)

| Control | Where |
|---|---|
| Agent minimises collection (normalised service/version, no indiscriminate banners), encrypted queue, deletes on delivery, redacted logs and diagnostics | `probe/DATA_HANDLING.md`, agent code |
| Scope enforcement; signed authorisation (rules of engagement) in the client prerequisites | agent + manager, `docs/deployment/CLIENT_PREREQUISITES.md` |
| Hosting in India (EC2 `ap-south-1`, Mumbai) | production box |
| TLS 1.2+ end to end (Let's Encrypt), HSTS | `scripts/enable-tls.sh` |
| AI egress profiles: `cloud` (raw), `hybrid` (pseudonymised), `sovereign` (local models only); free tiers always pseudonymised; AI audit chain | `app/ai/gateway.py`, `config.py` |
| Encrypted stored credentials | `services/credential_crypto.py` |
| Append-only audit log of operator and customer actions | `services/audit.py` |
| Compliance packs incl. India (RBI, SEBI, IRDAI, CERT-In, DPDP) with reporting clocks | `app/compliance/packs/` |

## 5. Gaps found

| # | Gap | Evidence | Why it matters |
|---|---|---|---|
| P1 | **No deletion.** No way to delete a customer's engagement, hosts, findings or reports; the agent docs promise "delete this host's data" but the manager has no such operation | only `DELETE` routes: integrations, enrol tokens, schedules | DPDP erasure via the fiduciary, RBI exit clause, GDPR Art. 17, every customer offboarding |
| P2 | **No retention limits.** Nothing is ever purged | no retention job | DPDP storage limitation; contracts will ask for a period |
| P3 | **Logs last days, not 180 days / 1 year.** Docker json-file 10–20 MB × 3 per container, on the instance only | `manager/docker-compose.yml` logging | CERT-In 180 days in India; DPDP Rule 6 one year |
| P4 | **AI default is `cloud`**: raw IPs and hostnames go to US AI providers unless someone changes the setting | `DEPLOYMENT_PROFILE=${…:-cloud}` | Cross-border transfer of customer data without the customer's choice; BFSI customers will refuse |
| P5 | **Crackable hashes stored as evidence** (Kerberoast `$krb5tgs$`) | `app/ad/kerberoast.py` | A database leak would hand out crackable service-account credentials |
| P6 | **Disk encryption and backups unverified** on production | checklist item only in `aws-deployment.md` | Rule 6 safeguards; data loss |
| P7 | **No contract pack**: no DPA, sub-processor list, privacy notice, security whitepaper, RBI outsourcing annex | — | Blocks procurement at banks and regulated entities |
| P8 | **No breach-response runbook** wired to the clocks (CERT-In 6 h, RBI/SEBI 6 h, DPDP 72 h, customer contract) | packs know the clocks; no runbook | Missed deadlines are the costliest failure |
| P9 | **No per-customer privacy settings**: AI profile, retention, region are global, not per engagement | `config.py` globals | Different customers need different answers |
| P10 | **Data export for the customer** limited to report exports | — | Data portability and exit |

## 6. Recommended approach

### 6.1 Principles (what every customer is told)
1. **Processor, not owner.** Scan data belongs to the customer; Vedha processes it only to provide
   the service, under a signed DPA and rules of engagement.
2. **India by default.** Manager, database, backups and logs in AWS Mumbai. Other regions or an
   on-premise manager only by contract.
3. **No AI without consent.** AI features are off for a customer until switched on, and when on,
   they use `hybrid` (pseudonymised) by default; `sovereign` (in-customer models) for banks that ask.
4. **Every record has a lifetime.** A default retention period, visible to the customer, and
   deletion on request with a certificate.
5. **Least collection.** The agent collects what detection needs; credential material is never
   stored in a usable form.

### 6.2 Product changes, in priority order

| Priority | Change | Closes |
|---|---|---|
| **1** | **Per-customer privacy settings** on the plan (next to POC / licence): AI on/off and profile (`hybrid` default, `sovereign`), retention period, data region label | P4, P9 |
| **1** | **Change the platform default to `hybrid`** so no raw customer identifiers reach a cloud model by default | P4 |
| **1** | **Redact crackable evidence**: store a fingerprint (hash type, account, length, SHA-256 of the blob) instead of the `$krb5tgs$` string; keep the full value only in the customer's own export if they opt in | P5 |
| **2** | **Retention engine**: per engagement, default e.g. 12 months after last scan for findings, 90 days for raw facts, 30 days after contract end for everything; nightly purge job; purge logged in the audit trail | P2 |
| **2** | **Delete and export**: "Export all data" (JSON + reports) and "Delete customer data" (engagement, hosts, findings, facts, reports, AI outputs, files), two-step confirmation, deletion certificate (PDF: what, when, by whom, hash of the deletion log) | P1, P10 |
| **2** | **Logs to CloudWatch Logs in ap-south-1**, 1-year retention (covers CERT-In 180 days and DPDP one year), redaction kept, access restricted | P3 |
| **3** | **Verify and document** EBS encryption (KMS), encrypted automated backups (Postgres dump to S3 in Mumbai with lifecycle expiry matching retention), restore tested | P6 |
| **3** | **Breach runbook**: who decides, 6-hour CERT-In form, customer notice template within 24 h, DPDP 72-hour report input, RBI/SEBI notice; tabletop once a quarter | P8 |

### 6.3 Contract and trust pack (no code)
- **Data Processing Agreement** (DPDP + GDPR Art. 28 clauses): purpose, instructions, security
  measures, sub-processors, breach notice (e.g. 24 h to the customer), assistance, deletion/return
  at end, audit rights.
- **Sub-processor list**: AWS (Mumbai, hosting), each AI provider and its region, with the data each
  receives and whether it is pseudonymised; Let's Encrypt (certificates only, no customer data).
- **RBI / SEBI outsourcing annex**: India data location, audit and inspection rights for the
  regulated entity and the regulator, sub-contractor disclosure, exit and data return, NDA.
- **Security and privacy whitepaper** with the data-flow diagram, the agent's data-handling
  statement, encryption, access control, logging, retention, AI handling.
- **Privacy notice** for portal users (Vedha as fiduciary for account data).
- **Records of processing** (internal).
- Roadmap to **ISO 27001 + ISO 27701** (privacy extension), then **SOC 2 Type II** for global
  customers. For BFSI, a **CERT-In empanelled auditor** report on the platform itself.

### 6.4 At agent install time (ties into P0-3)
- The "Add agent" wizard shows a **data notice**: what the agent collects, where it goes (India),
  retention, whether AI is on for this customer. The customer's admin acknowledges it once; the
  acknowledgement is stored in the audit log with the signed rules of engagement.
- AD / credentialed modules stay **off unless enabled per engagement**, with their own notice
  (they touch account names and credential material).
- **Uninstall + purge** removes the agent's identity and queue; Fleet offers "revoke and delete
  this agent's data".

## 7. Decisions needed

1. Default retention periods (proposed: raw facts 90 days, findings 12 months after last scan,
   all data 30 days after contract end).
2. AI default for new customers: **off** until enabled (recommended) or `hybrid` on.
3. Kerberoast evidence: fingerprint only (recommended), or keep full hashes encrypted.
4. EU customers: decline for now, host in an EU region, or on-premise manager only?
5. Certification path and timing (ISO 27001 + 27701 first is the usual Indian BFSI ask).
6. Who signs off the DPA and annexes (counsel).

## Sources
- DPDP Rules 2025 notified 13 Nov 2025: [Legal 500](https://www.legal500.com/intelligence/india/privacy/digital-personal-data-protection-rules-2025-%E2%80%93-notified) ·
  breach rule and 72 hours: [dpdpa.com analysis](https://www.dpdpa.com/blogs/DPDP%20Rules%202025-%20Analysis%20of%20Industry%20implications.html),
  [Scrut](https://www.scrut.io/post/dpdp-rules)
- CERT-In Directions, 28 Apr 2022 (180-day logs in India, 6-hour reporting): [CERT-In PDF](https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf)
- RBI Master Direction on Outsourcing of IT Services 2023 (data in India, audit rights): [RBI](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12486)
- SEBI CSCRF FAQs (Jun 2025): [SEBI](https://www.sebi.gov.in/sebi_data/faqfiles/jun-2025/1749647139924.pdf)
- IP addresses as personal data under GDPR: [European Commission](https://commission.europa.eu/law/law-topic/data-protection/data-protection-explained_en), [TechGDPR](https://techgdpr.com/blog/is-an-ip-address-considered-personal-data/)
