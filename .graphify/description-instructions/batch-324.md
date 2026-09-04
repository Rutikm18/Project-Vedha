# Node Description Batch 325 of 330

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

- "workers_outbox_rationale_182": "The `locked_at` boundary before which a PROCESSING row is considered dead." | kind=entity | source=manager/backend/app/workers/outbox.py:L182 | neighbors=[_stale_cutoff()] | lang=en
- "workers_outbox_rationale_187": "Stranded events that already exhausted their retry budget → dead-letter.     Bou" | kind=entity | source=manager/backend/app/workers/outbox.py:L187 | neighbors=[_dead_letter_stale_stmt()] | lang=en
- "workers_outbox_rationale_191": "The `locked_at` boundary before which a PROCESSING row is considered dead." | kind=entity | source=manager/backend/app/workers/outbox.py:L191 | neighbors=[_stale_cutoff()] | lang=en
- "workers_outbox_rationale_195": "Fan a notification out to the tenant's enabled email/Slack/Jira integrations." | kind=entity | source=manager/backend/app/workers/outbox.py:L195 | neighbors=[_handle_notify()] | lang=en
- "workers_outbox_rationale_196": "Stranded events that already exhausted their retry budget → dead-letter.     Bou" | kind=entity | source=manager/backend/app/workers/outbox.py:L196 | neighbors=[_dead_letter_stale_stmt()] | lang=en
- "workers_outbox_rationale_213": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L213 | neighbors=[_requeue_stale_stmt()] | lang=en
- "workers_outbox_rationale_214": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L214 | neighbors=[_claim_batch()] | lang=en
- "workers_outbox_rationale_216": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L216 | neighbors=[_mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_222": "Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat" | kind=entity | source=manager/backend/app/workers/outbox.py:L222 | neighbors=[_reclaim_stale()] | lang=en
- "workers_outbox_rationale_231": "Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat" | kind=entity | source=manager/backend/app/workers/outbox.py:L231 | neighbors=[_reclaim_stale()] | lang=en
- "workers_outbox_rationale_233": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L233 | neighbors=[_mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_247": "The `locked_at` boundary before which a PROCESSING row is considered dead." | kind=entity | source=manager/backend/app/workers/outbox.py:L247 | neighbors=[_stale_cutoff()] | lang=en
- "workers_outbox_rationale_250": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L250 | neighbors=[run_worker()] | lang=en
- "workers_outbox_rationale_251": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L251 | neighbors=[_mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_252": "Stranded events that already exhausted their retry budget → dead-letter.     Bou" | kind=entity | source=manager/backend/app/workers/outbox.py:L252 | neighbors=[_dead_letter_stale_stmt()] | lang=en
- "workers_outbox_rationale_260": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L260 | neighbors=[_mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_267": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L267 | neighbors=[run_worker()] | lang=en
- "workers_outbox_rationale_269": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L269 | neighbors=[_requeue_stale_stmt()] | lang=en
- "workers_outbox_rationale_285": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L285 | neighbors=[run_worker()] | lang=en
- "workers_outbox_rationale_287": "DetectionRuns stuck RUNNING → mark FAILED. Prefer the per-run LEASE     (`lease_" | kind=entity | source=manager/backend/app/workers/outbox.py:L287 | neighbors=[_reap_runs_stmt()] | lang=en
- "workers_outbox_rationale_294": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L294 | neighbors=[run_worker()] | lang=en
- "workers_outbox_rationale_308": "Fail DetectionRuns a crashed worker left RUNNING. Without this a campaign whose" | kind=entity | source=manager/backend/app/workers/outbox.py:L308 | neighbors=[_reap_stale_runs()] | lang=pt
- "workers_outbox_rationale_323": "Upsert this worker's heartbeat. A stale row tells campaign-progress the     dete" | kind=entity | source=manager/backend/app/workers/outbox.py:L323 | neighbors=[_write_heartbeat()] | lang=en
- "workers_outbox_rationale_339": "Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat" | kind=entity | source=manager/backend/app/workers/outbox.py:L339 | neighbors=[_reclaim_stale()] | lang=en
- "workers_outbox_rationale_368": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L368 | neighbors=[_mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_402": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L402 | neighbors=[run_worker()] | lang=en
- "workers_outbox_rationale_47": "Return whether a claimed event was stranded by a dead worker.      `_claim_batch" | kind=entity | source=manager/backend/app/workers/outbox.py:L47 | neighbors=[is_stale_processing()] | lang=en
- "workers_outbox_rationale_48": "Return whether a claimed event was stranded by a dead worker.      `_claim_batch" | kind=entity | source=manager/backend/app/workers/outbox.py:L48 | neighbors=[is_stale_processing()] | lang=en
- "workers_outbox_rationale_60": "Return whether a claimed event was stranded by a dead worker.      `_claim_batch" | kind=entity | source=manager/backend/app/workers/outbox.py:L60 | neighbors=[is_stale_processing()] | lang=en
- "workers_outbox_rationale_76": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L76 | neighbors=[register()] | lang=en
- "workers_outbox_rationale_77": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L77 | neighbors=[register()] | lang=en
- "workers_outbox_rationale_87": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L87 | neighbors=[enqueue()] | lang=en
- "workers_outbox_rationale_88": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L88 | neighbors=[enqueue()] | lang=en
- "workers_outbox_rationale_89": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L89 | neighbors=[register()] | lang=en
- "workers_reaper_rationale_34": "Expire one fenced attempt; return True when the job may be retried." | kind=entity | source=manager/backend/app/workers/reaper.py:L34 | neighbors=[expire_attempt()] | lang=en
- "workers_reaper_rationale_57": "Expire current attempts and requeue only jobs within their retry budget." | kind=entity | source=manager/backend/app/workers/reaper.py:L57 | neighbors=[reap_once()] | lang=en
- "workers_reaper_rationale_88": "Poll loop: requeue expired jobs every reaper_interval_seconds until stopped." | kind=entity | source=manager/backend/app/workers/reaper.py:L88 | neighbors=[run_reaper()] | lang=en
- "workflow_asset_asset_merge_db_scan": "._merge_db_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L180 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_dns_scan": "._merge_dns_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L196 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_ftp_scan": "._merge_ftp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L208 | neighbors=[Asset] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-324.json

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
