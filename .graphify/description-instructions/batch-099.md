# Node Description Batch 100 of 131

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

- "routers_detection_get_gaps": "get_gaps()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L187 | neighbors=[detection.py]
- "routers_detection_run_validation": "run_validation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L96 | neighbors=[detection.py]
- "routers_engagements_engagementupdate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L496 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L512 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L506 | neighbors=[EngagementUpdate]
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L432 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L626 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L598 | neighbors=[engagements.py]
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L371 | neighbors=[engagements.py]
- "routers_exploits_list_audit_logs": "list_audit_logs()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L337 | neighbors=[exploits.py]
- "routers_findings_finding_summary": "finding_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L153 | neighbors=[findings.py]
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L68 | neighbors=[findings.py]
- "routers_health_health": "health()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L40 | neighbors=[health.py]
- "routers_health_rationale_1": "Health endpoints.  GET /health          — liveness: DB + Redis reachability (fas" | kind=entity | source=manager/backend/app/routers/health.py:L1 | neighbors=[health.py]
- "routers_health_rationale_165": "Returns the cached report from the last startup diagnostics run.     If the repo" | kind=entity | source=manager/backend/app/routers/health.py:L165 | neighbors=[health_startup()]
- "routers_health_rationale_82": "Validates the authentication subsystem without touching login state.     Returns" | kind=entity | source=manager/backend/app/routers/health.py:L82 | neighbors=[health_auth()]
- "routers_probe_enrollment_list_enrollment_requests": "list_enrollment_requests()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L428 | neighbors=[probe_enrollment.py]
- "routers_probe_enrollment_rationale_1": "Device-code enrollment for probes; no human credential is installed on a probe." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[probe_enrollment.py]
- "routers_probe_enrollment_rationale_246": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L246 | neighbors=[_provision_agent_for_site()]
- "routers_probe_enrollment_rationale_62": "Return (raw_token, token_hash, token_prefix). Raw is shown once." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[generate_enroll_token()]
- "routers_probe_enrollment_rationale_68": "A token can auto-approve only while live, unrevoked, and under max_uses." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L68 | neighbors=[enroll_token_is_usable()]
- "routers_probe_enrollment_revoke_enroll_token": "revoke_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L682 | neighbors=[probe_enrollment.py]
- "routers_probe_enrollment_sitepolicyinput_require_site_reference": ".require_site_reference()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L167 | neighbors=[SitePolicyInput]
- "routers_probe_enrollment_sitepolicyinput_validate_networks": ".validate_networks()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L163 | neighbors=[SitePolicyInput]
- "routers_vuln_scans_import_findings": "import_findings()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L215 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nessus_scan": "launch_nessus_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L66 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nuclei_scan": "launch_nuclei_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L119 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_scan_status": "scan_status()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L165 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_trigger_enrichment": "trigger_enrichment()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L194 | neighbors=[vuln_scans.py]
- "run_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L5 | neighbors=[route.ts]
- "scan_page_cat": "Cat" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L121 | neighbors=[page.tsx]
- "scan_page_cats": "CATS" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L120 | neighbors=[page.tsx]
- "scan_page_dispatchreceipt": "DispatchReceipt()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L509 | neighbors=[page.tsx]
- "scan_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L39 | neighbors=[page.tsx]
- "scan_page_enginemanifest": "EngineManifest" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L72 | neighbors=[page.tsx]
- "scan_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L166 | neighbors=[page.tsx]
- "scan_page_fleetstrip": "FleetStrip()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L190 | neighbors=[page.tsx]
- "scan_page_hudframe": "HudFrame()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L175 | neighbors=[page.tsx]
- "scan_page_intensity": "Intensity" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L125 | neighbors=[page.tsx]
- "scan_page_intensitydial": "IntensityDial()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L287 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-099.json

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
