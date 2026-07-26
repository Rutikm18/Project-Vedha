# Node Description Batch 83 of 104

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L575 | neighbors=[engagements.py]
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L370 | neighbors=[engagements.py]
- "routers_exploits_list_audit_logs": "list_audit_logs()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L338 | neighbors=[exploits.py]
- "routers_findings_get_finding": "get_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L84 | neighbors=[findings.py]
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L49 | neighbors=[findings.py]
- "routers_findings_patch_finding": "patch_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L93 | neighbors=[findings.py]
- "routers_health_health": "health()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L16 | neighbors=[health.py]
- "routers_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/routers/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …]
- "routers_vuln_scans_import_findings": "import_findings()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L209 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nessus_scan": "launch_nessus_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L65 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nuclei_scan": "launch_nuclei_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L118 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_scan_status": "scan_status()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L159 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_trigger_enrichment": "trigger_enrichment()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L188 | neighbors=[vuln_scans.py]
- "run_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L5 | neighbors=[route.ts]
- "scan_page_cat": "Cat" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L92 | neighbors=[page.tsx]
- "scan_page_cats": "CATS" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L91 | neighbors=[page.tsx]
- "scan_page_dispatchreceipt": "DispatchReceipt()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L393 | neighbors=[page.tsx]
- "scan_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L39 | neighbors=[page.tsx]
- "scan_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L147 | neighbors=[page.tsx]
- "scan_page_fleetstrip": "FleetStrip()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L171 | neighbors=[page.tsx]
- "scan_page_hudframe": "HudFrame()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L156 | neighbors=[page.tsx]
- "scan_page_intensity": "Intensity" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L96 | neighbors=[page.tsx]
- "scan_page_intensitydial": "IntensityDial()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L261 | neighbors=[page.tsx]
- "scan_page_jobpanel": "JobPanel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L309 | neighbors=[page.tsx]
- "scan_page_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L47 | neighbors=[page.tsx]
- "scan_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L307 | neighbors=[page.tsx]
- "scan_page_probe": "Probe" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L27 | neighbors=[page.tsx]
- "scan_page_profile_badge": "PROFILE_BADGE" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L85 | neighbors=[page.tsx]
- "scan_page_risk": "RISK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L78 | neighbors=[page.tsx]
- "scan_page_scanpage": "ScanPage()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L441 | neighbors=[page.tsx]
- "scan_page_sectionlabel": "SectionLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L136 | neighbors=[page.tsx]
- "scan_page_uc_meta": "UC_META" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L64 | neighbors=[page.tsx]
- "scan_page_usecase": "UseCase" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L18 | neighbors=[page.tsx]
- "scan_page_usecasecard": "UseCaseCard()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L231 | neighbors=[page.tsx]
- "scanid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/scan/stream/[scanId]/route.ts:L7 | neighbors=[route.ts]
- "scanner_banner_parsehttpresponse": "ParseHTTPResponse()" | kind=code-symbol | source=probe-go/scanner/banner.go:L112 | neighbors=[banner.go]
- "scanner_circuitbreaker_allow": ".Allow()" | kind=code-symbol | source=probe-go/scanner/safe.go:L160 | neighbors=[CircuitBreaker]
- "scanner_circuitbreaker_recordfailure": ".RecordFailure()" | kind=code-symbol | source=probe-go/scanner/safe.go:L174 | neighbors=[CircuitBreaker]
- "scanner_circuitbreaker_recordsuccess": ".RecordSuccess()" | kind=code-symbol | source=probe-go/scanner/safe.go:L167 | neighbors=[CircuitBreaker]
- "scanner_circuitbreaker_tripped": ".Tripped()" | kind=code-symbol | source=probe-go/scanner/safe.go:L184 | neighbors=[CircuitBreaker]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-082.json

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
