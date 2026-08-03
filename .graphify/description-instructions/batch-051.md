# Node Description Batch 52 of 131

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

- "vuln_nuclei_rationale_79": "Machine-readable state for the most recent scanner invocation." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L79 | neighbors=[NucleiRunReport, FindingSeverity, FindingStatus]
- "vuln_nuclei_rationale_90": "Fatal Nuclei failure, optionally carrying findings emitted before failure." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L90 | neighbors=[NucleiScanError, FindingSeverity, FindingStatus]
- "vuln_tasks_dedup_hash": "_dedup_hash()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L167 | neighbors=[tasks.py, Deprecated — use app.utils.hash.dedup_h…, Deprecated — use app.utils.hash.dedup_h…]
- "websocket_manager_agentconnectionmanager_record_features": ".record_features()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L163 | neighbors=[AgentConnectionManager, Record transport features explicitly ad…, Record transport features explicitly ad…]
- "websocket_manager_agentconnectionmanager_record_heartbeat": ".record_heartbeat()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L151 | neighbors=[AgentConnectionManager, Record a heartbeat from an agent., Record a heartbeat from an agent.]
- "websocket_manager_agentconnectionmanager_register": ".register()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L97 | neighbors=[AgentConnectionManager, Register an agent's WebSocket connectio…, Register an agent's WebSocket connectio…]
- "websocket_manager_connectionmanager_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L33 | neighbors=[ConnectionManager, .handle_client(), Accept connection and add to room.]
- "workers_outbox_dead_letter_stale_stmt": "_dead_letter_stale_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L168 | neighbors=[outbox.py, Stranded events that already exhausted …, _reclaim_stale()]
- "workers_outbox_is_stale_processing": "is_stale_processing()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L42 | neighbors=[outbox.py, Return whether a claimed event was stra…, Return whether a claimed event was stra…]
- "workers_outbox_rationale_1": "outbox.py (worker) — durable consumer for the transactional outbox.  Run as its" | kind=entity | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[outbox.py, OutboxEvent, ScanResult]
- "workers_outbox_rationale_110": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L110 | neighbors=[OutboxEvent, ScanResult, _claim_batch()]
- "workers_outbox_rationale_152": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L152 | neighbors=[OutboxEvent, ScanResult, _mark_retry_or_dead()]
- "workers_outbox_rationale_56": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L56 | neighbors=[OutboxEvent, ScanResult, register()]
- "workers_outbox_rationale_67": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L67 | neighbors=[OutboxEvent, ScanResult, enqueue()]
- "workers_outbox_rationale_83": "Run the deterministic detection pipeline on a submitted facts payload.     Re-re" | kind=entity | source=manager/backend/app/workers/outbox.py:L83 | neighbors=[OutboxEvent, ScanResult, _handle_facts_ready()]
- "workers_outbox_requeue_stale_stmt": "_requeue_stale_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L185 | neighbors=[outbox.py, Stranded events with retry budget left …, _reclaim_stale()]
- "workers_outbox_stale_cutoff": "_stale_cutoff()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L163 | neighbors=[outbox.py, The `locked_at` boundary before which a…, _reclaim_stale()]
- "workers_reaper_expire_attempt": "expire_attempt()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L33 | neighbors=[reaper.py, Expire one fenced attempt; return True …, reap_once()]
- "workers_reaper_rationale_1": "reaper.py — requeue jobs abandoned by a dead probe.  A job is claimed with a lea" | kind=entity | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[reaper.py, ScanJobStatus, ScanJob]
- "workers_reaper_rationale_32": "Requeue every running job whose lease has expired. Returns the job ids." | kind=entity | source=manager/backend/app/workers/reaper.py:L32 | neighbors=[ScanJobStatus, ScanJob, reap_once()]
- "workers_reaper_rationale_55": "Poll loop: requeue expired jobs every reaper_interval_seconds until stopped." | kind=entity | source=manager/backend/app/workers/reaper.py:L55 | neighbors=[ScanJobStatus, ScanJob, run_reaper()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-051.json

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
