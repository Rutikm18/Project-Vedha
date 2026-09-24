# Asset intelligence tags, domain-expert AI, and BFSI deployment — design

Date: 2026-09-24 · Branch: `feat/intel-tags-domain-ai` · Status: approved to build (Hybrid-first)

Three linked sub-projects. They ship in this order because each feeds the next:
tags tell the AI *what kind of estate* it is talking about, and the deployment
profile tells the AI *where it is allowed to run*.

---

## Part 1 — Asset intelligence tags

### Problem
`Asset.tags` (JSONB) exists but nothing writes it. Everything we already know about
a host — classifier role, open services, exposure, FQDN/AD domain, OS — is scattered
across columns and `services` rows, so nothing downstream (filters, AI, compliance
scoping) can ask "show me every internet-facing payment host".

### Design
- **Pure tagger** `app/intel/tagging.py`: `derive_tags(AssetFacts) -> list[Tag]`.
  No DB, no I/O, fully unit-testable, deterministic. Each rule is a small function
  in a registry (same pattern as `branches.py`), so adding a rule is one entry.
- **Tag shape** (namespaced `key:value`, with provenance so tags explain themselves):
  ```json
  {"key": "role", "value": "database", "source": "auto", "rule": "svc.database",
   "confidence": 0.9, "evidence": "tcp/1433 ms-sql-s"}
  ```
- **Namespaces** (v1):
  | key | examples | from |
  |---|---|---|
  | `host_type` | server, workstation, network, printer, hypervisor, iot | asset_type/device_role |
  | `os_family` | windows, linux, macos, network_os, embedded | os string |
  | `role` | domain_controller, web, database, mail, dns, file_share, remote_access, directory, monitoring, container_platform, backup, voip, ics | services + role_detail |
  | `domain` | corp.bank.local (AD/DNS domain), apex domain of FQDN | fqdn/hostname |
  | `exposure` | internet_facing, internal_only | services.exposure |
  | `zone` | 10.20.30.0/24 (network segment) | ip |
  | `sector_fn` | payments, card_processing, swift, hsm, core_banking, atm, trading | BFSI port/banner signatures (lower confidence, evidence required) |
  | `compliance_scope` | pci_cde_candidate, swift_cscf_scope | derived from sector_fn |
  | `data_sensitivity` | restricted / confidential / internal | derived — feeds the AI gateway |
- **Storage**: `Asset.tags = {"auto": [Tag...], "manual": [Tag...], "v": 1}`.
  Auto tags are *recomputed wholesale* each time; manual tags are never touched by
  the tagger. No migration in v1 (column exists). A GIN index migration comes later
  when tag filtering needs to scale.
- **Hooks**: re-tag every asset touched by `_promote_assets` (after services are
  upserted, same transaction, using the in-memory service cache — zero extra
  queries). Plus `POST /engagements/{id}/assets/retag` to backfill existing data.
- **API**: tags returned on asset responses; `PUT /assets/{id}/tags` for manual tags
  (operator only, audited); `?tag=role:database` filter on asset list.
- **Honesty rule**: a tag is only emitted with evidence. BFSI `sector_fn` tags are
  heuristic (port/banner signatures) and carry confidence ≤ 0.6 unless a banner
  names the product.

---

## Part 2 — Domain-expert AI + global compliance intelligence

### Current state
One `ManagerLlmService`, fixed `_TASK_RULES` per task, context fenced as untrusted
data, no sector awareness, compliance = 5 global frameworks keyed by finding category.

### Target architecture
```
request ─► Skill router ─► Context builder ─► AI Gateway ─► provider
             (sector,        (findings, tags,    (classify, pseudonymize,
              jurisdiction,   compliance pack     policy route, audit)
              audience)       controls, KB)             │
                                                        ▼
            answer ◄─ Re-hydrate ◄─ Grounding check (citations must exist in packs)
```

1. **Engagement profile** — `sector` (banking, payments_fintech, insurance,
   capital_markets, nbfc, healthcare, government, generic) + `jurisdictions`
   (IN, EU, UK, US, SA, AE, SG, HK, …). Stored in `rules_of_engagement.profile`
   (JSONB — no migration). Operator sets it; portal reads it.
2. **Domain skills** `app/ai/skills/*.py` — one data pack per sector: persona,
   vocabulary map (e.g. "host" → "system in the cardholder data environment"),
   business-impact framing (payment downtime, regulator reporting clock, customer
   data), sector best practices, and which frameworks it pulls in. The router picks
   the skill from engagement profile → asset tags → fallback `generic`.
3. **Compliance packs** `app/compliance/packs/` — region framework registry
   (framework id, jurisdiction, sector applicability, controls, reporting
   obligations such as CERT-In 6h / DORA major-incident / NYDFS 72h) plus a
   category → control mapping, extending `finding_compliance`. v1 packs:
   - India: RBI CSF (2016) + RBI IT Governance Directions 2023, SEBI CSCRF 2024,
     CERT-In Directions 2022, DPDP Act 2023, IRDAI ISG
   - EU/UK: GDPR, DORA, NIS2, UK FCA/PRA operational resilience
   - ME/APAC: SAMA CSF, UAE CBUAE/NESA IAS, MAS TRM, HKMA C-RAF
   - US: NYDFS 23 NYCRR 500, GLBA Safeguards, FFIEC CAT
   Global (existing): PCI DSS 4.0, ISO 27001:2022, NIST 800-53, SOC 2, HIPAA; + SWIFT CSCF.
   Control IDs are *pointers for auditors*, never a legal attestation — every
   response says so.
4. **Grounding** — the model may cite only control IDs present in the supplied
   pack excerpt; a post-check strips/flags unknown IDs (extends `ai/hallucination.py`).
5. **New AI capabilities** — `compliance_brief` task (finding → obligations per
   jurisdiction, with regulator reporting clocks), sector-aware `client_assistant`
   and `advisor`, and an engagement-level "compliance posture by framework" view.

### AI Gateway (the security core for BFSI)
`app/ai/gateway.py` wraps every provider call:
- **Classify** context by the data-sensitivity tags (restricted/confidential/internal).
- **Pseudonymize** before egress: IPv4/IPv6, hostnames/FQDNs, e-mails, AD
  usernames/domains → stable tokens (`ASSET-17`, `HOST-4`, `USER-2`, `DOMAIN-1`),
  per-request map kept in memory only; re-hydrate the answer locally.
- **Policy route** by deployment profile: `sovereign` → local model only;
  `hybrid` → cloud allowed for pseudonymized payloads, restricted data never
  leaves; `cloud` → as today.
- **Audit** — hash-chained record (request hash, provider, model, profile, token
  counts, redaction counts) — never the raw prompt by default.

---

## Part 3 — BFSI deployment architecture

Three deployment profiles, one codebase (`VEDHA_DEPLOYMENT_PROFILE`):

| Profile | Buyer | Manager + data | AI | Intel updates |
|---|---|---|---|---|
| `sovereign` | Tier-1 banks, central-bank-regulated | Bank DC, no egress | Open-weight model on bank GPUs (vLLM/Ollama) | Signed offline bundles via one-way transfer |
| `hybrid` (default BFSI) | Banks, NBFCs, insurers | Bank DC / private cloud | Pseudonymized → in-region cloud model (e.g. Bedrock ap-south-1 / me-central-1 / eu-central-1) | Outbound-only allow-listed pull |
| `cloud` | Fintech, startups | Vedha single-tenant, in-region, BYOK | Cloud | Automatic |

Agent placement: one sealed probe per network zone (CDE, SWIFT zone, corporate,
DMZ), outbound-only mTLS to the on-prem manager, bank-CA certs where possible,
scan windows + maker-checker approval for intrusive scans, CERT-In 180-day log
retention, customer-managed keys (HSM/KMS) for secrets and evidence at rest.

Deliverable for Part 3: ADR + deployment guide + config flag and policy
enforcement in the gateway; offline intel-bundle signing reuses the probe's
Ed25519 signing.

---

## Testing
- Tagger: table-driven unit tests per rule + an end-to-end `_promote_assets` test.
- Skills/packs: schema validation test (every pack control referenced exists, every
  sector skill resolves its frameworks), router selection tests.
- Gateway: pseudonymize→rehydrate round-trip property tests, policy denial tests,
  "no raw IP ever reaches the transport" test using an httpx MockTransport.

## Out of scope (v1)
Vector RAG, fine-tuning, automated regulator filing, per-tag RBAC.
