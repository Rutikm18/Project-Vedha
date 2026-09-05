# Node Description Batch 233 of 336

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "main_scripts_va_campaign_rationale_624": "Wire a campaign with the real scanners (or injected stages for tests)." | kind=entity | source=probe/main_scripts/va_campaign.py:L624 | neighbors=[build_campaign()] | lang=en
- "main_scripts_va_campaign_rationale_650": "Renders campaign progress to a stream. On a TTY it re-draws one live block     i" | kind=entity | source=probe/main_scripts/va_campaign.py:L650 | neighbors=[CliProgressView] | lang=en
- "main_scripts_va_campaign_rationale_98": "Everything that changes WHAT the campaign does (not HOW it reports)." | kind=entity | source=probe/main_scripts/va_campaign.py:L98 | neighbors=[CampaignOptions] | lang=en
- "main_scripts_va_campaign_vacampaign_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L297 | neighbors=[VACampaign] | lang=en
- "main_scripts_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "main_scripts_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=probe/main_scripts/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "main_scripts_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "main_scripts_vnc_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L150 | neighbors=[vnc_scanner.py] | lang=en
- "main_scripts_vnc_scanner_rationale_1": "vnc_scanner.py — VNC/RFB authentication exposure (VA checklist: unauthenticated" | kind=entity | source=probe/main_scripts/vnc_scanner.py:L1 | neighbors=[vnc_scanner.py] | lang=en
- "main_scripts_vnc_scanner_rationale_109": "Blocking: RFB version handshake + read offered security types.         Monkeypat" | kind=entity | source=probe/main_scripts/vnc_scanner.py:L109 | neighbors=[._probe()] | lang=en
- "main_scripts_vnc_scanner_rationale_47": "Parse a 'RFB 003.008' banner into (major, minor), or None if not RFB." | kind=entity | source=probe/main_scripts/vnc_scanner.py:L47 | neighbors=[parse_rfb_version()] | lang=pt
- "main_scripts_vnc_scanner_rationale_61": "Turn a list of offered security-type ids into a verdict." | kind=entity | source=probe/main_scripts/vnc_scanner.py:L61 | neighbors=[classify_security_types()] | lang=pt
- "main_scripts_vnc_scanner_rationale_82": "Read the offered security types, handling the RFB 3.3 (single 4-byte type)     v" | kind=entity | source=probe/main_scripts/vnc_scanner.py:L82 | neighbors=[_read_security_types()] | lang=en
- "main_scripts_vnc_scanner_vncscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L104 | neighbors=[VNCScanner] | lang=en
- "main_scripts_web_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L182 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L56 | neighbors=[_NoRedirect] | lang=en
- "main_scripts_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_rationale_149": "Preferred scheme first, the other as a fallback: a scheme guess must         nev" | kind=entity | source=probe/main_scripts/web_scanner.py:L149 | neighbors=[._schemes_for()] | lang=pt
- "main_scripts_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en
- "main_scripts_web_scanner_rationale_46": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/main_scripts/web_scanner.py:L46 | neighbors=[parse_allow_header()] | lang=en
- "main_scripts_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L139 | neighbors=[WebScanner] | lang=en
- "main_scripts_windows_collector_main": "main()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "main_scripts_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "main_scripts_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=probe/main_scripts/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "main_scripts_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "main_scripts_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "me_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L10 | neighbors=[route.ts] | lang=en
- "models_base_uuidmixin": "UUIDMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L25 | neighbors=[base.py] | lang=en
- "models_enums_rationale_16": "Operator-set lifecycle. `ongoing` (assessment underway) and `running`     (activ" | kind=entity | source=manager/backend/app/models/enums.py:L16 | neighbors=[EngagementStatus] | lang=en
- "models_enums_rationale_71": "A single entry in a finding's lifecycle audit trail. Stored as a plain     strin" | kind=entity | source=manager/backend/app/models/enums.py:L71 | neighbors=[FindingEventType] | lang=pt
- "models_finding_event_rationale_12": "Append-only lifecycle audit trail for a single finding — one row per     transit" | kind=entity | source=manager/backend/app/models/finding_event.py:L12 | neighbors=[FindingEvent] | lang=en
- "models_integration_rationale_1": "integration.py — a tenant's notification integration config (email / Slack / Jir" | kind=entity | source=manager/backend/app/models/integration.py:L1 | neighbors=[integration.py] | lang=pt
- "models_probe_enrollment_rationale_73": "Pre-authorized, Site-bound enrollment token.      Lets a probe auto-enroll (no o" | kind=entity | source=manager/backend/app/models/probe_enrollment.py:L73 | neighbors=[ProbeEnrollmentToken] | lang=pt
- "models_remediation_plan_rationale_1": "remediation_plan.py — a generated, OS-specific remediation plan for a finding." | kind=entity | source=manager/backend/app/models/remediation_plan.py:L1 | neighbors=[remediation_plan.py] | lang=pt
- "models_scan_job_attempt_rationale_12": "One immutable, fenced execution claim for a logical scan job." | kind=entity | source=manager/backend/app/models/scan_job_attempt.py:L12 | neighbors=[ScanJobAttempt] | lang=en
- "models_scan_job_stamp_reference": "_stamp_reference()" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L80 | neighbors=[scan_job.py] | lang=en
- "models_scan_request_rationale_1": "scan_request.py — a customer-initiated, operator-approved request to run a scan" | kind=entity | source=manager/backend/app/models/scan_request.py:L1 | neighbors=[scan_request.py] | lang=pt
- "models_sla_policy_rationale_1": "sla_policy.py — a tenant's custom SLA remediation windows (hours per severity)." | kind=entity | source=manager/backend/app/models/sla_policy.py:L1 | neighbors=[sla_policy.py] | lang=en
- "models_validation_request_rationale_1": "validation_request.py — an approval-gated request to safely re-check a finding l" | kind=entity | source=manager/backend/app/models/validation_request.py:L1 | neighbors=[validation_request.py] | lang=en
- "models_worker_heartbeat_rationale_1": "worker_heartbeat.py — one row per background worker process, refreshed every tic" | kind=entity | source=manager/backend/app/models/worker_heartbeat.py:L1 | neighbors=[worker_heartbeat.py] | lang=it

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-232.json

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
