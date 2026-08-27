# Node Description Batch 52 of 92

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

- "agent_task_runner_rationale_57": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=agent/task_runner.py:L57 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_94": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=agent/task_runner.py:L94 | neighbors=[.run_job()] | lang=pt
- "agent_transport_rationale_1": "transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap" | kind=entity | source=agent/transport.py:L1 | neighbors=[transport.py] | lang=en
- "agent_transport_rationale_116": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=agent/transport.py:L116 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_203": "True if we have both an agent_id and a token for API calls." | kind=entity | source=agent/transport.py:L203 | neighbors=[.is_authenticated()] | lang=en
- "agent_transport_rationale_223": "Merge and atomically persist private state while preserving fields." | kind=entity | source=agent/transport.py:L223 | neighbors=[.update_state()] | lang=en
- "agent_transport_rationale_262": "Register the probe with the manager.          Args:             name: Probe name" | kind=entity | source=agent/transport.py:L262 | neighbors=[.register()] | lang=en
- "agent_transport_rationale_317": "Register using a manager-side shared bootstrap key (no user login needed)." | kind=entity | source=agent/transport.py:L317 | neighbors=[.bootstrap()] | lang=pt
- "agent_transport_rationale_32": "Recursively remove NUL (U+0000) characters from every string in a payload." | kind=entity | source=agent/transport.py:L32 | neighbors=[_strip_nul()] | lang=en
- "agent_transport_rationale_439": "Refresh a device token before expiry; legacy identities are unchanged." | kind=entity | source=agent/transport.py:L439 | neighbors=[.ensure_device_access()] | lang=en
- "agent_transport_rationale_463": "Refresh routing metadata using the cached agent identity.          Returns True" | kind=entity | source=agent/transport.py:L463 | neighbors=[.refresh_registration()] | lang=en
- "agent_transport_rationale_50": "Raised when a transport operation fails permanently (not retryable)." | kind=entity | source=agent/transport.py:L50 | neighbors=[TransportError] | lang=pt
- "agent_transport_rationale_514": "Send a heartbeat to the manager.          Returns True if the heartbeat was acce" | kind=entity | source=agent/transport.py:L514 | neighbors=[.heartbeat()] | lang=en
- "agent_transport_rationale_54": "The probe's device signing key is already registered as an agent on the     mana" | kind=entity | source=agent/transport.py:L54 | neighbors=[DeviceAlreadyEnrolledError] | lang=en
- "agent_transport_rationale_543": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=agent/transport.py:L543 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_563": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=agent/transport.py:L563 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_582": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=agent/transport.py:L582 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_647": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=agent/transport.py:L647 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_65": "Best-effort extraction of the manager's 409 ``detail`` message." | kind=entity | source=agent/transport.py:L65 | neighbors=[_enrollment_conflict_detail()] | lang=en
- "agent_transport_rationale_663": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=agent/transport.py:L663 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_673": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=agent/transport.py:L673 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_705": "True if the WebSocket connection is active." | kind=entity | source=agent/transport.py:L705 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_84": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=agent/transport.py:L84 | neighbors=[_atomic_write_private_state()] | lang=en
- "agent_transport_transport_agent_id": ".agent_id()" | kind=code-symbol | source=agent/transport.py:L183 | neighbors=[Transport] | lang=en
- "agent_transport_transport_agent_token": ".agent_token()" | kind=code-symbol | source=agent/transport.py:L191 | neighbors=[Transport] | lang=en
- "agent_transport_transport_auth_header": ".auth_header()" | kind=code-symbol | source=agent/transport.py:L199 | neighbors=[Transport] | lang=en
- "agent_transport_transport_poll_enrollment": ".poll_enrollment()" | kind=code-symbol | source=agent/transport.py:L361 | neighbors=[Transport] | lang=en
- "agent_use_cases_rationale_1": "use_cases.py — the finite, pre-defined library of scan scenarios the manager can" | kind=entity | source=agent/use_cases.py:L1 | neighbors=[use_cases.py] | lang=en
- "agent_use_cases_rationale_240": "Coerce an int-or-numeric-string to int, else None (non-numeric)." | kind=entity | source=agent/use_cases.py:L240 | neighbors=[_as_int()] | lang=en
- "agent_use_cases_rationale_251": "Map a numeric use-case code → use_case_id (raises on an unknown code)." | kind=entity | source=agent/use_cases.py:L251 | neighbors=[use_case_for_code()] | lang=en
- "agent_use_cases_rationale_255": "Coerce an int-or-numeric-string to int, else None (non-numeric)." | kind=entity | source=agent/use_cases.py:L255 | neighbors=[_as_int()] | lang=en
- "agent_use_cases_rationale_262": "Accept an intensity as a number (1/2/3) OR a name; return the name.      None st" | kind=entity | source=agent/use_cases.py:L262 | neighbors=[normalize_intensity()] | lang=en
- "agent_use_cases_rationale_266": "Map a numeric use-case code → use_case_id (raises on an unknown code)." | kind=entity | source=agent/use_cases.py:L266 | neighbors=[use_case_for_code()] | lang=en
- "agent_use_cases_rationale_277": "Accept an intensity as a number (1/2/3) OR a name; return the name.      None st" | kind=entity | source=agent/use_cases.py:L277 | neighbors=[normalize_intensity()] | lang=en
- "agent_use_cases_rationale_281": "Return (scan_type, profile, intensity) for a job.      Resolution order:     1." | kind=entity | source=agent/use_cases.py:L281 | neighbors=[resolve()] | lang=en
- "agent_use_cases_rationale_296": "Return (scan_type, profile, intensity) for a job.      Resolution order:     1." | kind=entity | source=agent/use_cases.py:L296 | neighbors=[resolve()] | lang=en
- "agent_validation_rationale_1": "Pure helpers for controlled Probe capability and accuracy validation." | kind=entity | source=agent/validation.py:L1 | neighbors=[validation.py] | lang=en
- "agent_validation_rationale_107": "Validate the small, explicit inventory used for accuracy scoring." | kind=entity | source=agent/validation.py:L107 | neighbors=[validate_ground_truth()] | lang=en
- "agent_validation_rationale_206": "Score promoted inventory against explicit host/port/service/CVE truth." | kind=entity | source=agent/validation.py:L206 | neighbors=[score_inventory()] | lang=en
- "agent_validation_rationale_42": "Resolve suites plus explicit use-cases, preserving first-seen order." | kind=entity | source=agent/validation.py:L42 | neighbors=[resolve_use_cases()] | lang=fr

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-051.json

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
