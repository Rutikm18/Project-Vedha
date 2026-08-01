# Node Description Batch 92 of 119

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

- "routers_engagements_engagementupdate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L512 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L506 | neighbors=[EngagementUpdate]
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L432 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L626 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L598 | neighbors=[engagements.py]
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L371 | neighbors=[engagements.py]
- "routers_exploits_list_audit_logs": "list_audit_logs()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L337 | neighbors=[exploits.py]
- "routers_findings_finding_summary": "finding_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L153 | neighbors=[findings.py]
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L68 | neighbors=[findings.py]
- "routers_health_health": "health()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L16 | neighbors=[health.py]
- "routers_vuln_scans_import_findings": "import_findings()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L215 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nessus_scan": "launch_nessus_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L66 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nuclei_scan": "launch_nuclei_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L119 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_scan_status": "scan_status()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L165 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_trigger_enrichment": "trigger_enrichment()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L194 | neighbors=[vuln_scans.py]
- "run_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L5 | neighbors=[route.ts]
- "scan_page_cat": "Cat" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L121 | neighbors=[page.tsx]
- "scan_page_cats": "CATS" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L120 | neighbors=[page.tsx]
- "scan_page_dispatchreceipt": "DispatchReceipt()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L505 | neighbors=[page.tsx]
- "scan_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L39 | neighbors=[page.tsx]
- "scan_page_enginemanifest": "EngineManifest" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L72 | neighbors=[page.tsx]
- "scan_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L166 | neighbors=[page.tsx]
- "scan_page_fleetstrip": "FleetStrip()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L190 | neighbors=[page.tsx]
- "scan_page_hudframe": "HudFrame()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L175 | neighbors=[page.tsx]
- "scan_page_intensity": "Intensity" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L125 | neighbors=[page.tsx]
- "scan_page_intensitydial": "IntensityDial()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L283 | neighbors=[page.tsx]
- "scan_page_jobpanel": "JobPanel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L331 | neighbors=[page.tsx]
- "scan_page_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L47 | neighbors=[page.tsx]
- "scan_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L329 | neighbors=[page.tsx]
- "scan_page_probe": "Probe" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L27 | neighbors=[page.tsx]
- "scan_page_profile_badge": "PROFILE_BADGE" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L114 | neighbors=[page.tsx]
- "scan_page_risk": "RISK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L107 | neighbors=[page.tsx]
- "scan_page_scannerrun": "ScannerRun" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L60 | neighbors=[page.tsx]
- "scan_page_scanpage": "ScanPage()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L550 | neighbors=[page.tsx]
- "scan_page_sectionlabel": "SectionLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L155 | neighbors=[page.tsx]
- "scan_page_uc_meta": "UC_META" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L92 | neighbors=[page.tsx]
- "scan_page_usecase": "UseCase" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L18 | neighbors=[page.tsx]
- "scan_page_usecasecard": "UseCaseCard()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L253 | neighbors=[page.tsx]
- "scanner_db_scanner_dbscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L240 | neighbors=[DBScanner]
- "scanner_db_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L287 | neighbors=[db_scanner.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-091.json

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
