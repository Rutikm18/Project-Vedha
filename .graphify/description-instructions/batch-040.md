# Node Description Batch 41 of 104

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

- "vuln_nessus_rationale_1": "NessusScanner — wraps the Tenable Nessus REST API v6.  Endpoints used:   POST /s" | kind=entity | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[FindingSeverity, FindingStatus, nessus.py] | lang=en
- "vuln_nessus_rationale_102": "Returns nessus scan_id as string." | kind=entity | source=manager/backend/app/vuln/nessus.py:L102 | neighbors=[FindingSeverity, FindingStatus, .create_scan()] | lang=en
- "vuln_nessus_rationale_141": "Returns scan_uuid (token for tracking)." | kind=entity | source=manager/backend/app/vuln/nessus.py:L141 | neighbors=[FindingSeverity, FindingStatus, .launch_scan()] | lang=en
- "vuln_nessus_rationale_152": "Returns {status, progress_percent, host_count}." | kind=entity | source=manager/backend/app/vuln/nessus.py:L152 | neighbors=[FindingSeverity, FindingStatus, .poll_status()] | lang=en
- "vuln_nessus_rationale_168": "Returns list of raw finding dicts from all hosts." | kind=entity | source=manager/backend/app/vuln/nessus.py:L168 | neighbors=[FindingSeverity, FindingStatus, .get_results()] | lang=en
- "vuln_nessus_rationale_207": "Map a raw Nessus vulnerability dict → Finding-compatible dict.         Returns a" | kind=entity | source=manager/backend/app/vuln/nessus.py:L207 | neighbors=[FindingSeverity, FindingStatus, .map_finding()] | lang=pt
- "vuln_nessus_rationale_258": "Request + poll + download .nessus XML for evidence storage." | kind=entity | source=manager/backend/app/vuln/nessus.py:L258 | neighbors=[FindingSeverity, FindingStatus, .export_nessus_file()] | lang=en
- "vuln_nessus_rationale_39": "Async Nessus API client. One instance per engagement scan session." | kind=entity | source=manager/backend/app/vuln/nessus.py:L39 | neighbors=[FindingSeverity, FindingStatus, NessusScanner] | lang=it
- "vuln_nessus_rationale_74": "Prefer API key auth (stateless, no session expiry).         Falls back to userna" | kind=entity | source=manager/backend/app/vuln/nessus.py:L74 | neighbors=[FindingSeverity, FindingStatus, .authenticate()] | lang=en
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, NucleiScanner, NucleiScanner — async subprocess wrappe…] | lang=en
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L74 | neighbors=[NucleiScanner, .parse_output(), Runs nuclei as an async subprocess.    …] | lang=en
- "vuln_tasks_run_post_scan_enrichment": "run_post_scan_enrichment()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L37 | neighbors=[tasks.py, Triggered by the vuln scan API after a …, _fire_critical_webhook()] | lang=en
- "websocket_manager_agentconnectionmanager_push_job": ".push_job()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L146 | neighbors=[AgentConnectionManager, .unregister(), Push a job to a specific agent over Web…] | lang=en
- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L164 | neighbors=[AgentConnectionManager, .unregister(), Push a job to the first online connecte…] | lang=en
- "websocket_manager_connectionmanager_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L33 | neighbors=[ConnectionManager, .handle_client(), Accept connection and add to room.] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_graph_update": ".broadcast_graph_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L279 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast graph data update to all subs…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_layout_update": ".broadcast_layout_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L298 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast layout change to all subscrib…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_node_update": ".broadcast_node_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L288 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast a single node update.] | lang=en
- "workers_outbox_mark_retry_or_dead": "_mark_retry_or_dead()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L151 | neighbors=[outbox.py, _process(), Reschedule with exponential backoff, or…] | lang=en
- "workers_outbox_rationale_1": "outbox.py (worker) — durable consumer for the transactional outbox.  Run as its" | kind=entity | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[OutboxEvent, ScanResult, outbox.py] | lang=en
- "workers_outbox_rationale_110": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L110 | neighbors=[OutboxEvent, ScanResult, _claim_batch()] | lang=en
- "workers_outbox_rationale_152": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L152 | neighbors=[OutboxEvent, ScanResult, _mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_186": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L186 | neighbors=[OutboxEvent, ScanResult, run_worker()] | lang=en
- "workers_outbox_rationale_56": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L56 | neighbors=[OutboxEvent, ScanResult, register()] | lang=en
- "workers_outbox_rationale_67": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L67 | neighbors=[OutboxEvent, ScanResult, enqueue()] | lang=en
- "workers_outbox_rationale_83": "Run the deterministic detection pipeline on a submitted facts payload.     Re-re" | kind=entity | source=manager/backend/app/workers/outbox.py:L83 | neighbors=[OutboxEvent, ScanResult, _handle_facts_ready()] | lang=en
- "workers_reaper_rationale_1": "reaper.py — requeue jobs abandoned by a dead probe.  A job is claimed with a lea" | kind=entity | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[ScanJobStatus, ScanJob, reaper.py] | lang=en
- "workers_reaper_rationale_32": "Requeue every running job whose lease has expired. Returns the job ids." | kind=entity | source=manager/backend/app/workers/reaper.py:L32 | neighbors=[ScanJobStatus, ScanJob, reap_once()] | lang=en
- "workers_reaper_rationale_55": "Poll loop: requeue expired jobs every reaper_interval_seconds until stopped." | kind=entity | source=manager/backend/app/workers/reaper.py:L55 | neighbors=[ScanJobStatus, ScanJob, run_reaper()] | lang=en
- "workers_reaper_reap_once": "reap_once()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L31 | neighbors=[reaper.py, Requeue every running job whose lease h…, run_reaper()] | lang=en
- "workers_reaper_run_reaper": "run_reaper()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L54 | neighbors=[reaper.py, Poll loop: requeue expired jobs every r…, reap_once()] | lang=en
- "workflow_asset_asset_merge_host_discovery": "._merge_host_discovery()" | kind=code-symbol | source=probe/workflow/asset.py:L95 | neighbors=[Asset, _parse_ts(), PortFact] | lang=en
- "workflow_asset_asset_merge_port_scan": "._merge_port_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L105 | neighbors=[Asset, _parse_ts(), PortFact] | lang=en
- "workflow_asset_asset_merge_udp_scan": "._merge_udp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L143 | neighbors=[Asset, _parse_ts(), PortFact] | lang=en
- "workflow_asset_asset_needs_recheck_live": ".needs_recheck_live()" | kind=code-symbol | source=probe/workflow/asset.py:L71 | neighbors=[Asset, _utcnow(), Is liveness unknown, or stale past `thr…] | lang=en
- "workflow_cache_classify_certainty": "classify_certainty()" | kind=code-symbol | source=probe/workflow/cache.py:L46 | neighbors=[cache.py, .get(), .put()] | lang=en
- "workflow_cache_workflowcache_get": ".get()" | kind=code-symbol | source=probe/workflow/cache.py:L109 | neighbors=[classify_certainty(), WorkflowCache, .should_recheck()] | lang=en
- "workflow_cache_workflowcache_load": "._load()" | kind=code-symbol | source=probe/workflow/cache.py:L89 | neighbors=[WorkflowCache, .__init__(), .from_jsonl_dict()] | lang=en
- "workflow_cache_workflowcache_put": ".put()" | kind=code-symbol | source=probe/workflow/cache.py:L112 | neighbors=[WorkflowCache, CacheEntry, classify_certainty()] | lang=en
- "workflow_cache_workflowcache_should_recheck": ".should_recheck()" | kind=code-symbol | source=probe/workflow/cache.py:L120 | neighbors=[True if there's no cached entry, OR the…, WorkflowCache, .get()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-040.json

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
