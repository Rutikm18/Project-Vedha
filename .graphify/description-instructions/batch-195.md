# Node Description Batch 196 of 380

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "agent_agent_rationale_1522": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1522 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_157": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L157 | neighbors=[_manager_reachable()]
- "agent_agent_rationale_167": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L167 | neighbors=[_manager_reachable()]
- "agent_agent_rationale_172": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=probe/agent/agent.py:L172 | neighbors=[_wait_for_manager()]
- "agent_agent_rationale_179": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L179 | neighbors=[_manager_reachable()]
- "agent_agent_rationale_182": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=probe/agent/agent.py:L182 | neighbors=[_wait_for_manager()]
- "agent_agent_rationale_183": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L183 | neighbors=[_manager_reachable()]
- "agent_agent_rationale_198": "Best-effort primary IPv4 of this host — the address a scan sources from.     Use" | kind=entity | source=probe/agent/agent.py:L198 | neighbors=[_detect_primary_ipv4()]
- "agent_agent_rationale_199": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=probe/agent/agent.py:L199 | neighbors=[_poll_jobs_or_empty()]
- "agent_agent_rationale_210": "Auto-troubleshoot the single silent killer of job execution: a scan     ceiling" | kind=entity | source=probe/agent/agent.py:L210 | neighbors=[_preflight_scope_check()]
- "agent_agent_rationale_212": "Install a root log handler for the daemon.      Nothing on the daemon path calle" | kind=entity | source=probe/agent/agent.py:L212 | neighbors=[configure_logging()]
- "agent_agent_rationale_214": "Auto-troubleshoot the single silent killer of job execution: a scan     ceiling" | kind=entity | source=probe/agent/agent.py:L214 | neighbors=[_preflight_scope_check()]
- "agent_agent_rationale_224": "Install a root log handler for the daemon.      Nothing on the daemon path calle" | kind=entity | source=probe/agent/agent.py:L224 | neighbors=[configure_logging()]
- "agent_agent_rationale_248": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=probe/agent/agent.py:L248 | neighbors=[_wait_for_manager()]
- "agent_agent_rationale_252": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=probe/agent/agent.py:L252 | neighbors=[_wait_for_manager()]
- "agent_agent_rationale_258": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L258 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_263": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L263 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_267": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=probe/agent/agent.py:L267 | neighbors=[_poll_jobs_or_empty()]
- "agent_agent_rationale_278": "Install a root log handler for the daemon.      Nothing on the daemon path calle" | kind=entity | source=probe/agent/agent.py:L278 | neighbors=[configure_logging()]
- "agent_agent_rationale_279": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=probe/agent/agent.py:L279 | neighbors=[_poll_jobs_or_empty()]
- "agent_agent_rationale_282": "Install a root log handler for the daemon.      Nothing on the daemon path calle" | kind=entity | source=probe/agent/agent.py:L282 | neighbors=[configure_logging()]
- "agent_agent_rationale_293": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L293 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_302": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L302 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_327": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L327 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_333": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=probe/agent/agent.py:L333 | neighbors=[_poll_jobs_or_empty()]
- "agent_agent_rationale_336": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L336 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_337": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=probe/agent/agent.py:L337 | neighbors=[_poll_jobs_or_empty()]
- "agent_agent_rationale_372": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L372 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_373": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L373 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_382": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L382 | neighbors=[_ws_run_job()]
- "agent_agent_rationale_387": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L387 | neighbors=[_ws_run_job()]
- "agent_agent_rationale_421": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L421 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_422": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L422 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_43": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L43 | neighbors=[_load_env()]
- "agent_agent_rationale_437": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L437 | neighbors=[_ws_http_poll_fallback()]
- "agent_agent_rationale_442": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L442 | neighbors=[_ws_http_poll_fallback()]
- "agent_agent_rationale_45": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L45 | neighbors=[_bounded_env_int()]
- "agent_agent_rationale_46": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L46 | neighbors=[_bounded_env_int()]
- "agent_agent_rationale_463": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L463 | neighbors=[_ws_stage_job_offer()]
- "agent_agent_rationale_475": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L475 | neighbors=[_ws_heartbeat_sender()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-195.json

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
