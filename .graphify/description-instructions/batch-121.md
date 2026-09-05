# Node Description Batch 122 of 336

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
- "workers_outbox_reap_runs_stmt": "_reap_runs_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L286 | neighbors=[outbox.py, DetectionRuns stuck RUNNING → mark FAIL…, _reap_stale_runs()]
- "workers_outbox_write_heartbeat": "_write_heartbeat()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L322 | neighbors=[outbox.py, Upsert this worker's heartbeat. A stale…, run_worker()]
- "workers_reaper_expire_attempt": "expire_attempt()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L33 | neighbors=[reaper.py, Expire one fenced attempt; return True …, reap_once()]
- "workers_reaper_rationale_1": "reaper.py — requeue jobs abandoned by a dead probe.  A job is claimed with a lea" | kind=entity | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[reaper.py, ScanJobStatus, ScanJob]
- "workers_reaper_rationale_32": "Requeue every running job whose lease has expired. Returns the job ids." | kind=entity | source=manager/backend/app/workers/reaper.py:L32 | neighbors=[ScanJobStatus, ScanJob, reap_once()]
- "workers_reaper_rationale_55": "Poll loop: requeue expired jobs every reaper_interval_seconds until stopped." | kind=entity | source=manager/backend/app/workers/reaper.py:L55 | neighbors=[ScanJobStatus, ScanJob, run_reaper()]
- "workflow_asset_asset_merge_host_discovery": "._merge_host_discovery()" | kind=code-symbol | source=probe/workflow/asset.py:L118 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_asset_asset_merge_port_scan": "._merge_port_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L134 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_asset_asset_merge_udp_scan": "._merge_udp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L240 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_branches_branchspec": "BranchSpec" | kind=code-symbol | source=probe/workflow/branches.py:L85 | neighbors=[branches.py, .host_level(), One deep-scan branch. `branch` is the g…]
- "workflow_cache_classify_certainty": "classify_certainty()" | kind=code-symbol | source=probe/workflow/cache.py:L67 | neighbors=[cache.py, .get(), .put()]
- "workflow_cache_workflowcache_get": ".get()" | kind=code-symbol | source=probe/workflow/cache.py:L130 | neighbors=[classify_certainty(), WorkflowCache, .should_recheck()]
- "workflow_cache_workflowcache_load": "._load()" | kind=code-symbol | source=probe/workflow/cache.py:L110 | neighbors=[WorkflowCache, .__init__(), .from_jsonl_dict()]
- "workflow_cache_workflowcache_put": ".put()" | kind=code-symbol | source=probe/workflow/cache.py:L133 | neighbors=[WorkflowCache, CacheEntry, classify_certainty()]
- "workflow_cli_parse_duration": "_parse_duration()" | kind=code-symbol | source=probe/workflow/cli.py:L28 | neighbors=[cli.py, 7d' / '12h' / '30m' -> timedelta. Simpl…, 7d' / '12h' / '30m' -> timedelta. Simpl…]
- "workflow_execution_engine_manifest": "engine_manifest()" | kind=code-symbol | source=probe/workflow/execution.py:L66 | neighbors=[execution.py, Return the runtime engine inventory wit…, Return the runtime engine inventory wit…]
- "workflow_execution_executiontrace_has_active_coverage": "._has_active_coverage()" | kind=code-symbol | source=probe/workflow/execution.py:L390 | neighbors=[ExecutionTrace, .as_list(), .failed()]
- "workflow_execution_executiontrace_record": ".record()" | kind=code-symbol | source=probe/workflow/execution.py:L289 | neighbors=[ExecutionTrace, ._ensure(), .reused()]
- "workflow_execution_executiontrace_skip": ".skip()" | kind=code-symbol | source=probe/workflow/execution.py:L358 | neighbors=[ExecutionTrace, .finalize(), ._ensure()]
- "workflow_execution_executiontrace_timing": ".timing()" | kind=code-symbol | source=probe/workflow/execution.py:L273 | neighbors=[ExecutionTrace, ._ensure(), Accumulate wall time for one component.…]
- "workflow_execution_planned_components": "planned_components()" | kind=code-symbol | source=probe/workflow/execution.py:L104 | neighbors=[execution.py, Resolve the exact collector plan for on…, Resolve the exact collector plan for on…]
- "workflow_gates_gate_4b_os_fingerprint": "gate_4b_os_fingerprint()" | kind=code-symbol | source=probe/workflow/gates.py:L122 | neighbors=[gates.py, gate_0_is_passive_profile(), OS identity for a host already proven a…]
- "workflow_host_health_env_int": "_env_int()" | kind=code-symbol | source=probe/workflow/host_health.py:L75 | neighbors=[host_health.py, _heartbeat_misses(), _strike_threshold()]
- "workflow_host_health_heartbeat_interval": "_heartbeat_interval()" | kind=code-symbol | source=probe/workflow/host_health.py:L87 | neighbors=[host_health.py, .watch(), Seconds between liveness heartbeats whi…]
- "workflow_host_health_hosthealthmonitor_is_offline": ".is_offline()" | kind=code-symbol | source=probe/workflow/host_health.py:L186 | neighbors=[HostHealthMonitor, ._state(), .watch()]
- "workflow_host_health_hosthealthmonitor_is_silence": "._is_silence()" | kind=code-symbol | source=probe/workflow/host_health.py:L133 | neighbors=[HostHealthMonitor, .observe(), True when a component ran and got nothi…]
- "workflow_host_health_hosthealthmonitor_suspect": ".suspect()" | kind=code-symbol | source=probe/workflow/host_health.py:L182 | neighbors=[HostHealthMonitor, .confirm(), ._state()]
- "workflow_init": "__init__.py" | kind=code-symbol | source=probe/workflow/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, workflow — conditional, caching, depend…, 298a9d4 trim frontend to 7 core pages; …]
- "workflow_intensity_intensity_port_override": "intensity_port_override()" | kind=code-symbol | source=probe/workflow/intensity.py:L79 | neighbors=[intensity.py, resolve_intensity(), Concrete TCP port list for this intensi…]
- "workflow_intensity_resolve_intensity": "resolve_intensity()" | kind=code-symbol | source=probe/workflow/intensity.py:L64 | neighbors=[intensity.py, intensity_port_override(), Return a COPY of the preset for `name` …]
- "workflow_modes_discovery": "discovery()" | kind=code-symbol | source=probe/workflow/modes.py:L60 | neighbors=[modes.py, EngagementMode, Host discovery plus the profile's TCP p…]
- "workflow_modes_host_discovery": "host_discovery()" | kind=code-symbol | source=probe/workflow/modes.py:L71 | neighbors=[modes.py, EngagementMode, Liveness checks only.]
- "workflow_modes_port_scan": "port_scan()" | kind=code-symbol | source=probe/workflow/modes.py:L82 | neighbors=[modes.py, EngagementMode, Liveness checks plus the profile's TCP …]
- "workflow_modes_service_fingerprint": "service_fingerprint()" | kind=code-symbol | source=probe/workflow/modes.py:L93 | neighbors=[modes.py, Liveness, TCP ports, and service banner…, EngagementMode]
- "workflow_router_looks_like_http": "looks_like_http()" | kind=code-symbol | source=probe/workflow/router.py:L63 | neighbors=[router.py, looks_like_db(), route_branches()]
- "workflow_workflow_engine_default_host_concurrency": "_default_host_concurrency()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L251 | neighbors=[workflow_engine.py, Hosts scanned in parallel during the de…, run_engagement()]
- "workflow_workflow_engine_record": "_record()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L234 | neighbors=[workflow_engine.py, _run_branch(), run_engagement()]
- "workflow_workflow_engine_record_reused": "_record_reused()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L278 | neighbors=[workflow_engine.py, _run_branch(), run_engagement()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-121.json

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
