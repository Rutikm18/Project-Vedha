# Node Description Batch 74 of 131

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

- "agent_agent_agentdeps": "AgentDeps" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L39 | neighbors=[agent.py] | lang=en
- "agent_agent_agentopts": "AgentOpts" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L26 | neighbors=[agent.py] | lang=en
- "agent_agent_rationale_258": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L258 | neighbors=[_run_ws_push_loop()] | lang=en
- "agent_agent_rationale_263": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L263 | neighbors=[_run_ws_push_loop()] | lang=en
- "agent_agent_rationale_293": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L293 | neighbors=[_run_polled_job_with_heartbeats()] | lang=en
- "agent_agent_rationale_302": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L302 | neighbors=[_run_polled_job_with_heartbeats()] | lang=en
- "agent_agent_rationale_327": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L327 | neighbors=[_run_ws_push_loop()] | lang=en
- "agent_agent_rationale_336": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L336 | neighbors=[_run_ws_push_loop()] | lang=en
- "agent_agent_rationale_373": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L373 | neighbors=[_run_polled_job_with_heartbeats()] | lang=en
- "agent_agent_rationale_382": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L382 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_387": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L387 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_422": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L422 | neighbors=[_run_ws_push_loop()] | lang=en
- "agent_agent_rationale_43": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L43 | neighbors=[_load_env()] | lang=en
- "agent_agent_rationale_437": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L437 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_442": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L442 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_45": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L45 | neighbors=[_bounded_env_int()] | lang=en
- "agent_agent_rationale_46": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L46 | neighbors=[_bounded_env_int()] | lang=en
- "agent_agent_rationale_463": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L463 | neighbors=[_ws_stage_job_offer()] | lang=en
- "agent_agent_rationale_475": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L475 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_48": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L48 | neighbors=[_bounded_env_int()] | lang=en
- "agent_agent_rationale_481": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L481 | neighbors=[_ws_take_confirmed_job()] | lang=en
- "agent_agent_rationale_485": "Re-submit previously spooled results over WebSocket." | kind=entity | source=probe/agent/agent.py:L485 | neighbors=[_ws_flush_spool()] | lang=en
- "agent_agent_rationale_488": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L488 | neighbors=[_ws_take_confirmed_job()] | lang=en
- "agent_agent_rationale_490": "Re-submit previously spooled results over WebSocket." | kind=entity | source=probe/agent/agent.py:L490 | neighbors=[_ws_flush_spool()] | lang=en
- "agent_agent_rationale_507": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L507 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_511": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L511 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_514": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L514 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_516": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L516 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_54": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L54 | neighbors=[_load_env()] | lang=en
- "agent_agent_rationale_55": "Recognize only explicit single-host development/Compose manager names." | kind=entity | source=probe/agent/agent.py:L55 | neighbors=[_is_local_manager_url()] | lang=en
- "agent_agent_rationale_550": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L550 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_559": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L559 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_564": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L564 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_57": "Recognize only explicit single-host development/Compose manager names." | kind=entity | source=probe/agent/agent.py:L57 | neighbors=[_is_local_manager_url()] | lang=en
- "agent_agent_rationale_575": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L575 | neighbors=[_ws_take_confirmed_job()] | lang=en
- "agent_agent_rationale_586": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L586 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_593": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L593 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_601": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L601 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_607": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L607 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_608": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L608 | neighbors=[_flush_spool_over_http()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-073.json

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
