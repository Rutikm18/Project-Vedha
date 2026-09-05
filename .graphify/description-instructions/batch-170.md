# Node Description Batch 171 of 336

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

- "vuln_enrichment_rationale_110": "Add NVD CVSS, EPSS, KEV flag, MITRE techniques, and composite risk.         Muta" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L110 | neighbors=[.enrich(), AssetCriticality]
- "vuln_enrichment_rationale_164": "Returns {cvss_v3, cvss_vector, description, references, published_date}." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L164 | neighbors=[.fetch_nvd(), AssetCriticality]
- "vuln_enrichment_rationale_216": "Returns {epss_score: float, percentile: float} or {}." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L216 | neighbors=[.fetch_epss(), AssetCriticality]
- "vuln_enrichment_rationale_245": "True if CVE is in the CISA Known Exploited Vulnerabilities catalog." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L245 | neighbors=[.check_cisa_kev(), AssetCriticality]
- "vuln_enrichment_rationale_271": "Returns MITRE ATT&CK technique IDs linked to this CVE.         Uses hardcoded hi" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L271 | neighbors=[.fetch_mitre_techniques(), AssetCriticality]
- "vuln_enrichment_rationale_28": "LRU + TTL eviction. Expired keys are purged on access; when ``maxsize``     is e" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L28 | neighbors=[TTLCache, AssetCriticality]
- "vuln_enrichment_rationale_307": "Returns composite risk score on 0-1000 scale.          Formula:           (cvss*" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L307 | neighbors=[.compute_composite_risk(), AssetCriticality]
- "vuln_enrichment_rationale_342": "Fetch NVD, EPSS, KEV and MITRE concurrently." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L342 | neighbors=[._fetch_all(), AssetCriticality]
- "vuln_enrichment_rationale_352": "SHA-256 of (asset_id, cve_id, plugin_id) for deduplication." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L352 | neighbors=[.dedup_hash(), AssetCriticality]
- "vuln_enrichment_rationale_92": "Enriches Finding objects with NVD, EPSS, CISA KEV, and MITRE data." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L92 | neighbors=[VulnEnrichmentService, AssetCriticality]
- "vuln_enrichment_vulnenrichmentservice_dedup_hash": ".dedup_hash()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L351 | neighbors=[SHA-256 of (asset_id, cve_id, plugin_id…, VulnEnrichmentService]
- "vuln_enrichment_vulnenrichmentservice_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L94 | neighbors=[VulnEnrichmentService, TTLCache]
- "vuln_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/vuln/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_nessus_nessusscanner_auth_headers": "._auth_headers()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L59 | neighbors=[NessusScanner, ._get_client()]
- "vuln_nessus_nessusscanner_get_plugin_detail": "._get_plugin_detail()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L193 | neighbors=[NessusScanner, .get_results()]
- "vuln_nessus_nessusscanner_get_template_uuid": "._get_template_uuid()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L124 | neighbors=[NessusScanner, .create_scan()]
- "vuln_nuclei_nucleiscanner_read_stderr": "._read_stderr()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L313 | neighbors=[NucleiScanner, .run_scan()]
- "vuln_nuclei_nucleiscanner_stop_process": "._stop_process()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L324 | neighbors=[NucleiScanner, .run_scan()]
- "vuln_tasks_fire_critical_webhook": "_fire_critical_webhook()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L135 | neighbors=[tasks.py, run_post_scan_enrichment()]
- "websocket_manager_graphwebsocketmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L358 | neighbors=[GraphWebSocketManager, ConnectionManager]
- "websocket_manager_rationale_209": "Push a job to the first online agent in the requested tenant.          Returns t" | kind=entity | source=manager/backend/app/websocket/manager.py:L209 | neighbors=[.push_job_to_first_online(), .get_agent_status()]
- "websocket_manager_rationale_213": "Push a job to the first online agent in the requested tenant.          Returns t" | kind=entity | source=manager/backend/app/websocket/manager.py:L213 | neighbors=[.push_job_to_first_online(), .agent_stale_after()]
- "websocket_manager_rationale_243": "Deliver a job-push to an agent wherever its socket is connected.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L243 | neighbors=[.deliver_job(), .online_agents()]
- "websocket_manager_rationale_245": "Deliver a job-push to an agent wherever its socket is connected.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L245 | neighbors=[.deliver_job(), .online_agents()]
- "websocket_manager_rationale_298": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L298 | neighbors=[.is_online(), .handle_client()]
- "workers_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/workers/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "workers_outbox_main": "main()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L446 | neighbors=[outbox.py, Event]
- "workers_outbox_mark_done": "_mark_done()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L358 | neighbors=[outbox.py, _process()]
- "workers_outbox_rationale_130": "Fan a notification out to the tenant's enabled email/Slack/Jira integrations." | kind=entity | source=manager/backend/app/workers/outbox.py:L130 | neighbors=[_handle_notify(), _claim_batch()]
- "workers_outbox_rationale_204": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L204 | neighbors=[_requeue_stale_stmt(), _reclaim_stale()]
- "workflow_asset_utcnow": "_utcnow()" | kind=code-symbol | source=probe/workflow/asset.py:L27 | neighbors=[asset.py, .needs_recheck_live()]
- "workflow_branches_branchspec_host_level": ".host_level()" | kind=code-symbol | source=probe/workflow/branches.py:L101 | neighbors=[BranchSpec, True when the fact describes the host r…]
- "workflow_branches_db_kwargs": "_db_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L68 | neighbors=[branches.py, Ports with a known database engine get …]
- "workflow_branches_no_kwargs": "_no_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L54 | neighbors=[branches.py, For scanners that take no `ports` argum…]
- "workflow_branches_ports_kwargs": "_ports_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L49 | neighbors=[branches.py, The default: hand the scanner the ports…]
- "workflow_branches_web_kwargs": "_web_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L60 | neighbors=[branches.py, Tell the web scanner which of these por…]
- "workflow_cache_cacheentry_from_jsonl_dict": ".from_jsonl_dict()" | kind=code-symbol | source=probe/workflow/cache.py:L92 | neighbors=[CacheEntry, ._load()]
- "workflow_cache_cacheentry_to_jsonl_dict": ".to_jsonl_dict()" | kind=code-symbol | source=probe/workflow/cache.py:L86 | neighbors=[CacheEntry, .save()]
- "workflow_cache_workflowcache_init": ".__init__()" | kind=code-symbol | source=probe/workflow/cache.py:L104 | neighbors=[WorkflowCache, ._load()]
- "workflow_cache_workflowcache_save": ".save()" | kind=code-symbol | source=probe/workflow/cache.py:L122 | neighbors=[WorkflowCache, .to_jsonl_dict()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-170.json

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
