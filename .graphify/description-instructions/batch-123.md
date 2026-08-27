# Node Description Batch 124 of 236

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

- "ad_ldap_enum_ldapenumerator_connection": ".connection()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L185 | neighbors=[LDAPEnumerator]
- "ad_ldap_enum_ldapenumerator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L120 | neighbors=[LDAPEnumerator]
- "ad_orchestrator_adassessmentrunner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L42 | neighbors=[ADAssessmentRunner]
- "agent_agent_agentdeps": "AgentDeps" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L39 | neighbors=[agent.py]
- "agent_agent_agentopts": "AgentOpts" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L26 | neighbors=[agent.py]
- "agent_agent_rationale_1016": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1016 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_1025": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1025 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_1049": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1049 | neighbors=[_enroll_device()]
- "agent_agent_rationale_1058": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1058 | neighbors=[_enroll_device()]
- "agent_agent_rationale_107": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L107 | neighbors=[_result_summary()]
- "agent_agent_rationale_1187": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1187 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_1213": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1213 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_1231": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1231 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_131": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=probe/agent/agent.py:L131 | neighbors=[_classify_connection_error()]
- "agent_agent_rationale_157": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L157 | neighbors=[_manager_reachable()]
- "agent_agent_rationale_172": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=probe/agent/agent.py:L172 | neighbors=[_wait_for_manager()]
- "agent_agent_rationale_199": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=probe/agent/agent.py:L199 | neighbors=[_poll_jobs_or_empty()]
- "agent_agent_rationale_258": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L258 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_263": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L263 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_293": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L293 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_302": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L302 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_327": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L327 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_336": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L336 | neighbors=[_run_ws_push_loop()]
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
- "agent_agent_rationale_48": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L48 | neighbors=[_bounded_env_int()]
- "agent_agent_rationale_481": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L481 | neighbors=[_ws_take_confirmed_job()]
- "agent_agent_rationale_485": "Re-submit previously spooled results over WebSocket." | kind=entity | source=probe/agent/agent.py:L485 | neighbors=[_ws_flush_spool()]
- "agent_agent_rationale_488": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L488 | neighbors=[_ws_take_confirmed_job()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-123.json

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
