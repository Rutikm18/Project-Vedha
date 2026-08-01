# Node Description Batch 48 of 119

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

- "workers_outbox_rationale_67": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L67 | neighbors=[OutboxEvent, ScanResult, enqueue()]
- "workers_outbox_rationale_83": "Run the deterministic detection pipeline on a submitted facts payload.     Re-re" | kind=entity | source=manager/backend/app/workers/outbox.py:L83 | neighbors=[OutboxEvent, ScanResult, _handle_facts_ready()]
- "workers_reaper_rationale_1": "reaper.py — requeue jobs abandoned by a dead probe.  A job is claimed with a lea" | kind=entity | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[ScanJobStatus, ScanJob, reaper.py]
- "workers_reaper_rationale_32": "Requeue every running job whose lease has expired. Returns the job ids." | kind=entity | source=manager/backend/app/workers/reaper.py:L32 | neighbors=[ScanJobStatus, ScanJob, reap_once()]
- "workers_reaper_rationale_55": "Poll loop: requeue expired jobs every reaper_interval_seconds until stopped." | kind=entity | source=manager/backend/app/workers/reaper.py:L55 | neighbors=[ScanJobStatus, ScanJob, run_reaper()]
- "workers_reaper_reap_once": "reap_once()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L31 | neighbors=[reaper.py, Requeue every running job whose lease h…, run_reaper()]
- "workers_reaper_run_reaper": "run_reaper()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L54 | neighbors=[reaper.py, Poll loop: requeue expired jobs every r…, reap_once()]
- "workflow_asset_asset_merge_host_discovery": "._merge_host_discovery()" | kind=code-symbol | source=probe/workflow/asset.py:L99 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_asset_asset_merge_port_scan": "._merge_port_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L109 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_asset_asset_merge_result": ".merge_result()" | kind=code-symbol | source=probe/workflow/asset.py:L83 | neighbors=[Asset, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…]
- "workflow_asset_asset_merge_udp_scan": "._merge_udp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L147 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_cache_classify_certainty": "classify_certainty()" | kind=code-symbol | source=probe/workflow/cache.py:L46 | neighbors=[cache.py, .get(), .put()]
- "workflow_cache_workflowcache_get": ".get()" | kind=code-symbol | source=probe/workflow/cache.py:L109 | neighbors=[classify_certainty(), WorkflowCache, .should_recheck()]
- "workflow_cache_workflowcache_load": "._load()" | kind=code-symbol | source=probe/workflow/cache.py:L89 | neighbors=[WorkflowCache, .__init__(), .from_jsonl_dict()]
- "workflow_cache_workflowcache_put": ".put()" | kind=code-symbol | source=probe/workflow/cache.py:L112 | neighbors=[WorkflowCache, CacheEntry, classify_certainty()]
- "workflow_cache_workflowcache_should_recheck": ".should_recheck()" | kind=code-symbol | source=probe/workflow/cache.py:L120 | neighbors=[True if there's no cached entry, OR the…, WorkflowCache, .get()]
- "workflow_cli_parse_duration": "_parse_duration()" | kind=code-symbol | source=probe/workflow/cli.py:L28 | neighbors=[cli.py, 7d' / '12h' / '30m' -> timedelta. Simpl…, 7d' / '12h' / '30m' -> timedelta. Simpl…]
- "workflow_execution_executiontrace_failed": ".failed()" | kind=code-symbol | source=probe/workflow/execution.py:L350 | neighbors=[ExecutionTrace, ._has_active_coverage(), True when execution produced errors and…]
- "workflow_execution_executiontrace_has_active_coverage": "._has_active_coverage()" | kind=code-symbol | source=probe/workflow/execution.py:L360 | neighbors=[ExecutionTrace, .as_list(), .failed()]
- "workflow_execution_executiontrace_record": ".record()" | kind=code-symbol | source=probe/workflow/execution.py:L259 | neighbors=[ExecutionTrace, ._ensure(), .reused()]
- "workflow_execution_executiontrace_skip": ".skip()" | kind=code-symbol | source=probe/workflow/execution.py:L328 | neighbors=[ExecutionTrace, .finalize(), ._ensure()]
- "workflow_execution_scanner_failure_result": "scanner_failure_result()" | kind=code-symbol | source=probe/workflow/execution.py:L209 | neighbors=[execution.py, Represent an unexpected component excep…, classify_scanner_error()]
- "workflow_gates_gate_5_branch_eligible": "gate_5_branch_eligible()" | kind=code-symbol | source=probe/workflow/gates.py:L71 | neighbors=[gates.py, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …]
- "workflow_init": "__init__.py" | kind=code-symbol | source=probe/workflow/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, workflow — conditional, caching, depend…, 298a9d4 trim frontend to 7 core pages; …]
- "workflow_modes_discovery": "discovery()" | kind=code-symbol | source=probe/workflow/modes.py:L60 | neighbors=[modes.py, EngagementMode, Host discovery plus the profile's TCP p…]
- "workflow_modes_host_discovery": "host_discovery()" | kind=code-symbol | source=probe/workflow/modes.py:L71 | neighbors=[modes.py, EngagementMode, Liveness checks only.]
- "workflow_modes_port_scan": "port_scan()" | kind=code-symbol | source=probe/workflow/modes.py:L82 | neighbors=[modes.py, EngagementMode, Liveness checks plus the profile's TCP …]
- "workflow_modes_service_fingerprint": "service_fingerprint()" | kind=code-symbol | source=probe/workflow/modes.py:L93 | neighbors=[modes.py, Liveness, TCP ports, and service banner…, EngagementMode]
- "workflow_router_looks_like_http": "looks_like_http()" | kind=code-symbol | source=probe/workflow/router.py:L45 | neighbors=[router.py, looks_like_db(), route_branches()]
- "workflow_workflow_engine_run_inventory": "_run_inventory()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L166 | neighbors=[workflow_engine.py, run_engagement(), _Sink]
- "workflow_workflow_engine_run_passive": "_run_passive()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L149 | neighbors=[workflow_engine.py, run_engagement(), _Sink]
- "ad_adcs_adcschecker_has_low_priv": "._has_low_priv()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L127 | neighbors=[ADCSChecker, .check_esc1()]
- "ad_asreproast_asreproastchecker_get_no_preauth_accounts": ".get_no_preauth_accounts()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L42 | neighbors=[ASREPRoastChecker, Usernames of enabled accounts with pre-…]
- "ad_bloodhound_bloodhoundcollector_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L229 | neighbors=[BloodHoundCollector, Build a Finding summarising the shortes…]
- "ad_bloodhound_bloodhoundcollector_query_da_paths": ".query_da_paths()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L195 | neighbors=[BloodHoundCollector, Return shortest attack paths from any n…]
- "ad_bloodhound_bloodhoundcollector_run_collection": ".run_collection()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L52 | neighbors=[BloodHoundCollector, Run bloodhound-python and return the li…]
- "ad_bloodhound_rationale_1": "BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges" | kind=entity | source=manager/backend/app/ad/bloodhound.py:L1 | neighbors=[bloodhound.py, FindingSeverity]
- "ad_bloodhound_rationale_124": "Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu" | kind=entity | source=manager/backend/app/ad/bloodhound.py:L124 | neighbors=[.import_to_neo4j(), FindingSeverity]
- "ad_bloodhound_rationale_157": "Ingest one BloodHound collector file. Returns (#nodes, #rels)." | kind=entity | source=manager/backend/app/ad/bloodhound.py:L157 | neighbors=[._ingest_collection(), FindingSeverity]
- "ad_bloodhound_rationale_196": "Return shortest attack paths from any non-DA principal to a Domain Admins" | kind=entity | source=manager/backend/app/ad/bloodhound.py:L196 | neighbors=[.query_da_paths(), FindingSeverity]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-047.json

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
