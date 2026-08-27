# Node Description Batch 232 of 236

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

- "workers_outbox_rationale_231": "Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat" | kind=entity | source=manager/backend/app/workers/outbox.py:L231 | neighbors=[_reclaim_stale()]
- "workers_outbox_rationale_233": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L233 | neighbors=[_mark_retry_or_dead()]
- "workers_outbox_rationale_250": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L250 | neighbors=[run_worker()]
- "workers_outbox_rationale_251": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L251 | neighbors=[_mark_retry_or_dead()]
- "workers_outbox_rationale_260": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L260 | neighbors=[_mark_retry_or_dead()]
- "workers_outbox_rationale_267": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L267 | neighbors=[run_worker()]
- "workers_outbox_rationale_285": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L285 | neighbors=[run_worker()]
- "workers_outbox_rationale_294": "Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so" | kind=entity | source=manager/backend/app/workers/outbox.py:L294 | neighbors=[run_worker()]
- "workers_outbox_rationale_47": "Return whether a claimed event was stranded by a dead worker.      `_claim_batch" | kind=entity | source=manager/backend/app/workers/outbox.py:L47 | neighbors=[is_stale_processing()]
- "workers_outbox_rationale_48": "Return whether a claimed event was stranded by a dead worker.      `_claim_batch" | kind=entity | source=manager/backend/app/workers/outbox.py:L48 | neighbors=[is_stale_processing()]
- "workers_outbox_rationale_76": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L76 | neighbors=[register()]
- "workers_outbox_rationale_77": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L77 | neighbors=[register()]
- "workers_outbox_rationale_87": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L87 | neighbors=[enqueue()]
- "workers_outbox_rationale_88": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L88 | neighbors=[enqueue()]
- "workers_reaper_rationale_34": "Expire one fenced attempt; return True when the job may be retried." | kind=entity | source=manager/backend/app/workers/reaper.py:L34 | neighbors=[expire_attempt()]
- "workers_reaper_rationale_57": "Expire current attempts and requeue only jobs within their retry budget." | kind=entity | source=manager/backend/app/workers/reaper.py:L57 | neighbors=[reap_once()]
- "workers_reaper_rationale_88": "Poll loop: requeue expired jobs every reaper_interval_seconds until stopped." | kind=entity | source=manager/backend/app/workers/reaper.py:L88 | neighbors=[run_reaper()]
- "workflow_asset_asset_merge_db_scan": "._merge_db_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L151 | neighbors=[Asset]
- "workflow_asset_asset_merge_dns_scan": "._merge_dns_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L167 | neighbors=[Asset]
- "workflow_asset_asset_merge_ftp_scan": "._merge_ftp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L179 | neighbors=[Asset]
- "workflow_asset_asset_merge_ipmi_scan": "._merge_ipmi_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L191 | neighbors=[Asset]
- "workflow_asset_asset_merge_ldap_scan": "._merge_ldap_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L163 | neighbors=[Asset]
- "workflow_asset_asset_merge_mcp_ai_scan": "._merge_mcp_ai_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L155 | neighbors=[Asset]
- "workflow_asset_asset_merge_msrpc_scan": "._merge_msrpc_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L199 | neighbors=[Asset]
- "workflow_asset_asset_merge_nfs_scan": "._merge_nfs_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L175 | neighbors=[Asset]
- "workflow_asset_asset_merge_os_fingerprint": "._merge_os_fingerprint()" | kind=code-symbol | source=probe/workflow/asset.py:L171 | neighbors=[Asset]
- "workflow_asset_asset_merge_passive_collect": "._merge_passive_collect()" | kind=code-symbol | source=probe/workflow/asset.py:L215 | neighbors=[Asset]
- "workflow_asset_asset_merge_printer_scan": "._merge_printer_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L203 | neighbors=[Asset]
- "workflow_asset_asset_merge_rsync_scan": "._merge_rsync_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L183 | neighbors=[Asset]
- "workflow_asset_asset_merge_service_banner": "._merge_service_banner()" | kind=code-symbol | source=probe/workflow/asset.py:L129 | neighbors=[Asset]
- "workflow_asset_asset_merge_service_enum": "._merge_service_enum()" | kind=code-symbol | source=probe/workflow/asset.py:L175 | neighbors=[Asset]
- "workflow_asset_asset_merge_smb_enum_scan": "._merge_smb_enum_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L171 | neighbors=[Asset]
- "workflow_asset_asset_merge_smb_scan": "._merge_smb_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L141 | neighbors=[Asset]
- "workflow_asset_asset_merge_smtp_scan": "._merge_smtp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L195 | neighbors=[Asset]
- "workflow_asset_asset_merge_snmp_scan": "._merge_snmp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L147 | neighbors=[Asset]
- "workflow_asset_asset_merge_ssh_inventory": "._merge_ssh_inventory()" | kind=code-symbol | source=probe/workflow/asset.py:L221 | neighbors=[Asset]
- "workflow_asset_asset_merge_ssh_scan": "._merge_ssh_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L159 | neighbors=[Asset]
- "workflow_asset_asset_merge_tls_scan": "._merge_tls_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L133 | neighbors=[Asset]
- "workflow_asset_asset_merge_vnc_scan": "._merge_vnc_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L187 | neighbors=[Asset]
- "workflow_asset_asset_merge_web_scan": "._merge_web_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L137 | neighbors=[Asset]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-231.json

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
