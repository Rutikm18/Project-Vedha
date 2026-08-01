# Node Description Batch 73 of 119

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

- "agent_spool_test_testspoolflushdeletesonlyacknowledgedresults": "TestSpoolFlushDeletesOnlyAcknowledgedResults()" | kind=code-symbol | source=probe-go/agent/spool_test.go:L57 | neighbors=[spool_test.go] | lang=en
- "agent_state_test_testidentitystaterejectsdifferentmanager": "TestIdentityStateRejectsDifferentManager()" | kind=code-symbol | source=probe-go/agent/state_test.go:L189 | neighbors=[state_test.go] | lang=en
- "agent_task_runner_rationale_1": "task_runner.py — orchestrates the full lifecycle of a single scan job.  Given a" | kind=entity | source=probe/agent/task_runner.py:L1 | neighbors=[task_runner.py] | lang=en
- "agent_task_runner_rationale_283": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L283 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_30": "Structured result from running one scan job." | kind=entity | source=probe/agent/task_runner.py:L30 | neighbors=[JobResult] | lang=en
- "agent_task_runner_rationale_399": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L399 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_42": "Orchestrates one scan job's lifecycle.      The runner holds injected dependenci" | kind=entity | source=probe/agent/task_runner.py:L42 | neighbors=[TaskRunner] | lang=en
- "agent_task_runner_rationale_57": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L57 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_58": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L58 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_80": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=probe/agent/task_runner.py:L80 | neighbors=[.run_job()] | lang=pt
- "agent_task_runner_rationale_89": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=probe/agent/task_runner.py:L89 | neighbors=[.run_job()] | lang=pt
- "agent_tools_mergehosts": "mergeHosts()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L81 | neighbors=[tools.ts] | lang=en
- "agent_tools_runonephase": "runOnePhase()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L40 | neighbors=[tools.ts] | lang=en
- "agent_transport_rationale_1": "transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap" | kind=entity | source=probe/agent/transport.py:L1 | neighbors=[transport.py] | lang=en
- "agent_transport_rationale_111": "True if we have both an agent_id and a token for API calls." | kind=entity | source=probe/agent/transport.py:L111 | neighbors=[.is_authenticated()] | lang=en
- "agent_transport_rationale_142": "Register the probe with the manager.          Args:             name: Probe name" | kind=entity | source=probe/agent/transport.py:L142 | neighbors=[.register()] | lang=en
- "agent_transport_rationale_166": "True if we have both an agent_id and a token for API calls." | kind=entity | source=probe/agent/transport.py:L166 | neighbors=[.is_authenticated()] | lang=en
- "agent_transport_rationale_186": "Merge and atomically persist private state while preserving fields." | kind=entity | source=probe/agent/transport.py:L186 | neighbors=[.update_state()] | lang=en
- "agent_transport_rationale_190": "Send a heartbeat to the manager.          Returns True if the heartbeat was acce" | kind=entity | source=probe/agent/transport.py:L190 | neighbors=[.heartbeat()] | lang=en
- "agent_transport_rationale_215": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L215 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_225": "Register the probe with the manager.          Args:             name: Probe name" | kind=entity | source=probe/agent/transport.py:L225 | neighbors=[.register()] | lang=en
- "agent_transport_rationale_233": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L233 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_252": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L252 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_277": "Refresh routing metadata using the cached agent identity.          Returns True" | kind=entity | source=probe/agent/transport.py:L277 | neighbors=[.refresh_registration()] | lang=en
- "agent_transport_rationale_303": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L303 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_311": "Send a heartbeat to the manager.          Returns True if the heartbeat was acce" | kind=entity | source=probe/agent/transport.py:L311 | neighbors=[.heartbeat()] | lang=en
- "agent_transport_rationale_319": "Return the WebSocket connection URL with auth token.          The token is passe" | kind=entity | source=probe/agent/transport.py:L319 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_33": "Raised when a transport operation fails permanently (not retryable)." | kind=entity | source=probe/agent/transport.py:L33 | neighbors=[TransportError] | lang=pt
- "agent_transport_rationale_330": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L330 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_336": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L336 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_34": "Raised when a transport operation fails permanently (not retryable)." | kind=entity | source=probe/agent/transport.py:L34 | neighbors=[TransportError] | lang=pt
- "agent_transport_rationale_37": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L37 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_373": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L373 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_424": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L424 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_440": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L440 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_450": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L450 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_48": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L48 | neighbors=[_atomic_write_private_state()] | lang=en
- "agent_transport_rationale_480": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L480 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_80": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L80 | neighbors=[Transport] | lang=en
- "agent_transport_test_testconnectwshonorstlsverificationandmanagerendpoint": "TestConnectWSHonorsTLSVerificationAndManagerEndpoint()" | kind=code-symbol | source=probe-go/agent/transport_test.go:L17 | neighbors=[transport_test.go] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-072.json

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
