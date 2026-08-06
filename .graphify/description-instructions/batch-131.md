# Node Description Batch 132 of 134

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

- "websocket_manager_rationale_79": "Tracks WebSocket connections from probes/agents for direct job push.      Each c" | kind=entity | source=manager/backend/app/websocket/manager.py:L79 | neighbors=[AgentConnectionManager]
- "websocket_manager_rationale_98": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L98 | neighbors=[.register()]
- "websocket_manager_rationale_99": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L99 | neighbors=[.register()]
- "workers_outbox_rationale_103": "Run the deterministic detection pipeline on a submitted facts payload.     Re-re" | kind=entity | source=manager/backend/app/workers/outbox.py:L103 | neighbors=[_handle_facts_ready()]
- "workers_outbox_rationale_104": "Run the deterministic detection pipeline on a submitted facts payload.     Re-re" | kind=entity | source=manager/backend/app/workers/outbox.py:L104 | neighbors=[_handle_facts_ready()]
- "workers_outbox_rationale_130": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L130 | neighbors=[_claim_batch()]
- "workers_outbox_rationale_131": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L131 | neighbors=[_claim_batch()]
- "workers_outbox_rationale_163": "Requeue events a dead worker left in PROCESSING past the lease.      `attempts`" | kind=entity | source=manager/backend/app/workers/outbox.py:L163 | neighbors=[_reclaim_stale()]
- "workers_outbox_rationale_164": "The `locked_at` boundary before which a PROCESSING row is considered dead." | kind=entity | source=manager/backend/app/workers/outbox.py:L164 | neighbors=[_stale_cutoff()]
- "workers_outbox_rationale_169": "Stranded events that already exhausted their retry budget → dead-letter.     Bou" | kind=entity | source=manager/backend/app/workers/outbox.py:L169 | neighbors=[_dead_letter_stale_stmt()]
- "workers_outbox_rationale_204": "Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat" | kind=entity | source=manager/backend/app/workers/outbox.py:L204 | neighbors=[_reclaim_stale()]
- "workers_outbox_rationale_216": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L216 | neighbors=[_mark_retry_or_dead()]
- "workers_outbox_rationale_233": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L233 | neighbors=[_mark_retry_or_dead()]
- "workers_outbox_rationale_250": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L250 | neighbors=[run_worker()]
- "workers_outbox_rationale_267": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L267 | neighbors=[run_worker()]
- "workers_outbox_rationale_47": "Return whether a claimed event was stranded by a dead worker.      `_claim_batch" | kind=entity | source=manager/backend/app/workers/outbox.py:L47 | neighbors=[is_stale_processing()]
- "workers_outbox_rationale_48": "Return whether a claimed event was stranded by a dead worker.      `_claim_batch" | kind=entity | source=manager/backend/app/workers/outbox.py:L48 | neighbors=[is_stale_processing()]
- "workers_outbox_rationale_76": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L76 | neighbors=[register()]
- "workers_outbox_rationale_77": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L77 | neighbors=[register()]
- "workers_outbox_rationale_87": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L87 | neighbors=[enqueue()]
- "workers_outbox_rationale_88": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L88 | neighbors=[enqueue()]
- "workers_reaper_rationale_34": "Expire one fenced attempt; return True when the job may be retried." | kind=entity | source=manager/backend/app/workers/reaper.py:L34 | neighbors=[expire_attempt()]
- "workers_reaper_rationale_57": "Expire current attempts and requeue only jobs within their retry budget." | kind=entity | source=manager/backend/app/workers/reaper.py:L57 | neighbors=[reap_once()]
- "workers_reaper_rationale_88": "Poll loop: requeue expired jobs every reaper_interval_seconds until stopped." | kind=entity | source=manager/backend/app/workers/reaper.py:L88 | neighbors=[run_reaper()]
- "workflow_asset_asset_merge_db_scan": "._merge_db_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L139 | neighbors=[Asset]
- "workflow_asset_asset_merge_mcp_ai_scan": "._merge_mcp_ai_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L143 | neighbors=[Asset]
- "workflow_asset_asset_merge_passive_collect": "._merge_passive_collect()" | kind=code-symbol | source=probe/workflow/asset.py:L155 | neighbors=[Asset]
- "workflow_asset_asset_merge_service_banner": "._merge_service_banner()" | kind=code-symbol | source=probe/workflow/asset.py:L117 | neighbors=[Asset]
- "workflow_asset_asset_merge_smb_scan": "._merge_smb_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L129 | neighbors=[Asset]
- "workflow_asset_asset_merge_snmp_scan": "._merge_snmp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L135 | neighbors=[Asset]
- "workflow_asset_asset_merge_ssh_inventory": "._merge_ssh_inventory()" | kind=code-symbol | source=probe/workflow/asset.py:L161 | neighbors=[Asset]
- "workflow_asset_asset_merge_tls_scan": "._merge_tls_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L121 | neighbors=[Asset]
- "workflow_asset_asset_merge_web_scan": "._merge_web_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L125 | neighbors=[Asset]
- "workflow_asset_asset_merge_windows_inventory": "._merge_windows_inventory()" | kind=code-symbol | source=probe/workflow/asset.py:L165 | neighbors=[Asset]
- "workflow_asset_asset_open_ports_for_deep_scan": ".open_ports_for_deep_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L80 | neighbors=[Asset]
- "workflow_asset_rationale_1": "asset.py — per-host fact model the workflow engine reasons about.  This is an OR" | kind=entity | source=probe/workflow/asset.py:L1 | neighbors=[asset.py]
- "workflow_asset_rationale_71": "Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep" | kind=entity | source=probe/workflow/asset.py:L71 | neighbors=[.needs_recheck_live()]
- "workflow_asset_rationale_72": "Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep" | kind=entity | source=probe/workflow/asset.py:L72 | neighbors=[.needs_recheck_live()]
- "workflow_asset_rationale_84": "Dispatch a real ScanResult into the right sub-structure, keyed         on result" | kind=entity | source=probe/workflow/asset.py:L84 | neighbors=[.merge_result()]
- "workflow_asset_rationale_85": "Dispatch a real ScanResult into the right sub-structure, keyed         on result" | kind=entity | source=probe/workflow/asset.py:L85 | neighbors=[.merge_result()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-131.json

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
