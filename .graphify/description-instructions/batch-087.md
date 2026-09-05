# Node Description Batch 88 of 336

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

- "versions_0031_integrations": "0031_integrations.py" | kind=code-symbol | source=manager/backend/alembic/versions/0031_integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, downgrade(), upgrade(), Integrations — per-tenant notification …]
- "versions_0032_scan_request_use_case": "0032_scan_request_use_case.py" | kind=code-symbol | source=manager/backend/alembic/versions/0032_scan_request_use_case.py:L1 | neighbors=[c7f226f chore: bundle pending working-t…, downgrade(), upgrade(), scan_requests.use_case_id — the capabil…]
- "versions_0033_finding_events": "0033_finding_events.py" | kind=code-symbol | source=manager/backend/alembic/versions/0033_finding_events.py:L1 | neighbors=[d98f654 feat(manager): network-VA campa…, downgrade(), upgrade(), Finding lifecycle audit trail — append-…]
- "versions_0034_run_lease_worker_heartbeat": "0034_run_lease_worker_heartbeat.py" | kind=code-symbol | source=manager/backend/alembic/versions/0034_run_lease_worker_heartbeat.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, downgrade(), upgrade(), Stage 2b: DetectionRun lease + worker h…]
- "versions_0036_scan_job_reference": "0036_scan_job_reference.py" | kind=code-symbol | source=manager/backend/alembic/versions/0036_scan_job_reference.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, downgrade(), upgrade(), scan jobs get a human-readable referenc…]
- "versions_0037_scan_job_cancelled_status": "0037_scan_job_cancelled_status.py" | kind=code-symbol | source=manager/backend/alembic/versions/0037_scan_job_cancelled_status.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, downgrade(), upgrade(), scan jobs gain a terminal `cancelled` s…]
- "vuln_enrichment_vulnenrichmentservice_check_cisa_kev": ".check_cisa_kev()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L244 | neighbors=[True if CVE is in the CISA Known Exploi…, VulnEnrichmentService, ._get_kev_catalog(), ._fetch_all()]
- "vuln_enrichment_vulnenrichmentservice_compute_composite_risk": ".compute_composite_risk()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L297 | neighbors=[Returns composite risk score on 0-1000 …, VulnEnrichmentService, .get(), .enrich()]
- "vuln_enrichment_vulnenrichmentservice_fetch_epss": ".fetch_epss()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L215 | neighbors=[Returns {epss_score: float, percentile:…, VulnEnrichmentService, ._fetch_all(), .get()]
- "vuln_nessus_nessusscanner_export_nessus_file": ".export_nessus_file()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L256 | neighbors=[NessusScanner, ._get_client(), Request + poll + download .nessus XML f…, Request + poll + download .nessus XML f…]
- "vuln_nessus_nessusscanner_launch_scan": ".launch_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L139 | neighbors=[NessusScanner, ._get_client(), Returns scan_uuid (token for tracking)., Returns scan_uuid (token for tracking).]
- "vuln_nessus_nessusscanner_poll_status": ".poll_status()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L150 | neighbors=[NessusScanner, ._get_client(), Returns {status, progress_percent, host…, Returns {status, progress_percent, host…]
- "vuln_nuclei_nucleiscanner_partial_or_raise": "._partial_or_raise()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L337 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, .run_scan()]
- "vuln_nuclei_nucleiscanner_template_selector": ".template_selector()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L444 | neighbors=[NucleiScanner, Given a list of service names on an ass…, Given a list of service names on an ass…, Given a list of service names on an ass…]
- "vuln_nuclei_rationale_1": "NucleiScanner — async subprocess wrapper around the Nuclei CLI.  Nuclei outputs" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[nuclei.py, FindingSeverity, FindingStatus, ServiceFingerprint]
- "vuln_nuclei_rationale_110": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L110 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_127": "Run Nuclei and stream JSONL findings from stdout.          ``request_timeout_sec" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L127 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_132": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L132 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_195": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L195 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_383": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L383 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_446": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L446 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_68": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L68 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_80": "Machine-readable state for the most recent scanner invocation." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L80 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiRunReport]
- "vuln_nuclei_rationale_81": "Runs nuclei as an async subprocess.         Returns a list of parsed finding dic" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L81 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_91": "Fatal Nuclei failure, optionally carrying findings emitted before failure." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L91 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanError]
- "vuln_tasks_run_post_scan_enrichment": "run_post_scan_enrichment()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L34 | neighbors=[tasks.py, Triggered by the vuln scan API after a …, _fire_critical_webhook(), Triggered by the vuln scan API after a …]
- "websocket_manager_agentconnectionmanager_deliver_job": ".deliver_job()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L238 | neighbors=[AgentConnectionManager, .push_job(), Deliver a job-push to an agent wherever…, Deliver a job-push to an agent wherever…]
- "websocket_manager_agentconnectionmanager_record_features": ".record_features()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L165 | neighbors=[AgentConnectionManager, Record transport features explicitly ad…, Record transport features explicitly ad…, Record transport features explicitly ad…]
- "websocket_manager_agentconnectionmanager_record_heartbeat": ".record_heartbeat()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L153 | neighbors=[AgentConnectionManager, Record a heartbeat from an agent., Record a heartbeat from an agent., Record a heartbeat from an agent.]
- "websocket_manager_agentconnectionmanager_register": ".register()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L99 | neighbors=[AgentConnectionManager, Register an agent's WebSocket connectio…, Register an agent's WebSocket connectio…, Register an agent's WebSocket connectio…]
- "websocket_manager_connectionmanager_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L35 | neighbors=[ConnectionManager, .handle_client(), Accept connection and add to room., Accept connection and add to room.]
- "workers_outbox_handle_notify": "_handle_notify()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L194 | neighbors=[outbox.py, Fan a notification out to the tenant's …, Fan a notification out to the tenant's …, Fan a notification out to the tenant's …]
- "workers_outbox_is_stale_processing": "is_stale_processing()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L54 | neighbors=[outbox.py, Return whether a claimed event was stra…, Return whether a claimed event was stra…, Return whether a claimed event was stra…]
- "workers_outbox_process": "_process()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L389 | neighbors=[outbox.py, _mark_done(), _mark_retry_or_dead(), run_worker()]
- "workers_outbox_rationale_186": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L186 | neighbors=[_requeue_stale_stmt(), OutboxEvent, ScanResult, run_worker()]
- "workers_outbox_reap_stale_runs": "_reap_stale_runs()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L307 | neighbors=[outbox.py, Fail DetectionRuns a crashed worker lef…, _reap_runs_stmt(), run_worker()]
- "workers_reaper_run_reaper": "run_reaper()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L87 | neighbors=[reaper.py, Poll loop: requeue expired jobs every r…, reap_once(), Poll loop: requeue expired jobs every r…]
- "workflow_asset_parse_ts": "_parse_ts()" | kind=code-symbol | source=probe/workflow/asset.py:L31 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_asset_portfact": "PortFact" | kind=code-symbol | source=probe/workflow/asset.py:L36 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_cache_cacheentry": "CacheEntry" | kind=code-symbol | source=probe/workflow/cache.py:L76 | neighbors=[cache.py, .from_jsonl_dict(), .to_jsonl_dict(), .put()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-087.json

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
