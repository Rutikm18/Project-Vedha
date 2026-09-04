# Node Description Batch 237 of 330

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "routers_remediation_rationale_97": "Execute the atomic upsert and return the RETURNING row for serialization." | kind=entity | source=manager/backend/app/routers/remediation.py:L97 | neighbors=[_upsert_plan()]
- "routers_sla_policy_rationale_1": "sla_policy.py — operator management of the tenant's custom SLA remediation windo" | kind=entity | source=manager/backend/app/routers/sla_policy.py:L1 | neighbors=[sla_policy.py]
- "routers_sla_policy_rationale_59": "The tenant's custom SLA windows if set, else the env defaults. Shared by any" | kind=entity | source=manager/backend/app/routers/sla_policy.py:L59 | neighbors=[resolve_windows()]
- "routers_users_activate_user": "activate_user()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L118 | neighbors=[users.py]
- "routers_users_deactivate_user": "deactivate_user()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L92 | neighbors=[users.py]
- "routers_users_rationale_1": "Tenant user management — list and deactivate operator accounts.  Exposed endpoin" | kind=entity | source=manager/backend/app/routers/users.py:L1 | neighbors=[users.py]
- "routers_validation_rationale_1": "Approval-gated safe active-validation API (P3).  POST /engagements/{id}/findings" | kind=entity | source=manager/backend/app/routers/validation.py:L1 | neighbors=[validation.py]
- "routers_validation_rationale_82": "RoE gate: active validation is allowed unless the engagement's RoE     explicitl" | kind=entity | source=manager/backend/app/routers/validation.py:L82 | neighbors=[_roe_allows_active_validation()]
- "routers_validation_rationale_89": "Pick a safe check for the finding. TLS findings → tls_handshake, else a     bann" | kind=entity | source=manager/backend/app/routers/validation.py:L89 | neighbors=[_default_check_kind()]
- "routers_vuln_scans_import_findings": "import_findings()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L215 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nessus_scan": "launch_nessus_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L66 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nuclei_scan": "launch_nuclei_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L119 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_scan_status": "scan_status()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L165 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_trigger_enrichment": "trigger_enrichment()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L194 | neighbors=[vuln_scans.py]
- "run_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L5 | neighbors=[route.ts]
- "scan_page_cat": "Cat" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L140 | neighbors=[page.tsx]
- "scan_page_cats": "CATS" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L139 | neighbors=[page.tsx]
- "scan_page_dispatchreceipt": "DispatchReceipt()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L639 | neighbors=[page.tsx]
- "scan_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L42 | neighbors=[page.tsx]
- "scan_page_enginemanifest": "EngineManifest" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L75 | neighbors=[page.tsx]
- "scan_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L185 | neighbors=[page.tsx]
- "scan_page_fleetstrip": "FleetStrip()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L209 | neighbors=[page.tsx]
- "scan_page_hudframe": "HudFrame()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L194 | neighbors=[page.tsx]
- "scan_page_intensity": "Intensity" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L144 | neighbors=[page.tsx]
- "scan_page_intensitydial": "IntensityDial()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L410 | neighbors=[page.tsx]
- "scan_page_jobpanel": "JobPanel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L465 | neighbors=[page.tsx]
- "scan_page_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L50 | neighbors=[page.tsx]
- "scan_page_network_va_fallback": "NETWORK_VA_FALLBACK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L100 | neighbors=[page.tsx]
- "scan_page_networkvahero": "NetworkVaHero()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L282 | neighbors=[page.tsx]
- "scan_page_nva_stages": "NVA_STAGES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L280 | neighbors=[page.tsx]
- "scan_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L456 | neighbors=[page.tsx]
- "scan_page_probe": "Probe" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L30 | neighbors=[page.tsx]
- "scan_page_profile_badge": "PROFILE_BADGE" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L133 | neighbors=[page.tsx]
- "scan_page_rec_st": "REC_ST" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L458 | neighbors=[page.tsx]
- "scan_page_risk": "RISK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L126 | neighbors=[page.tsx]
- "scan_page_scannerrun": "ScannerRun" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L63 | neighbors=[page.tsx]
- "scan_page_scanpage": "ScanPage()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L684 | neighbors=[page.tsx]
- "scan_page_sectionlabel": "SectionLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L174 | neighbors=[page.tsx]
- "scan_page_uc_meta": "UC_META" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L110 | neighbors=[page.tsx]
- "scan_page_usecase": "UseCase" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L20 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-236.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
