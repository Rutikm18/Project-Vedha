# Node Description Batch 81 of 134

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

- "agent_transport_rationale_33": "Raised when a transport operation fails permanently (not retryable)." | kind=entity | source=probe/agent/transport.py:L33 | neighbors=[TransportError] | lang=pt
- "agent_transport_rationale_330": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L330 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_333": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L333 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_336": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L336 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_34": "Raised when a transport operation fails permanently (not retryable)." | kind=entity | source=probe/agent/transport.py:L34 | neighbors=[TransportError] | lang=pt
- "agent_transport_rationale_351": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L351 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_37": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L37 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_370": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L370 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_373": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L373 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_395": "Refresh a device token before expiry; legacy identities are unchanged." | kind=entity | source=probe/agent/transport.py:L395 | neighbors=[.ensure_device_access()] | lang=en
- "agent_transport_rationale_419": "Refresh routing metadata using the cached agent identity.          Returns True" | kind=entity | source=probe/agent/transport.py:L419 | neighbors=[.refresh_registration()] | lang=en
- "agent_transport_rationale_421": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L421 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_424": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L424 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_437": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L437 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_440": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L440 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_447": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L447 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_45": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L45 | neighbors=[_atomic_write_private_state()] | lang=en
- "agent_transport_rationale_450": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L450 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_46": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L46 | neighbors=[_atomic_write_private_state()] | lang=en
- "agent_transport_rationale_470": "Send a heartbeat to the manager.          Returns True if the heartbeat was acce" | kind=entity | source=probe/agent/transport.py:L470 | neighbors=[.heartbeat()] | lang=en
- "agent_transport_rationale_477": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L477 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_48": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L48 | neighbors=[_atomic_write_private_state()] | lang=en
- "agent_transport_rationale_480": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L480 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_499": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L499 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_519": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L519 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_538": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L538 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_601": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L601 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_617": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L617 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_627": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L627 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_659": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L659 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_77": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L77 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_78": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L78 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_80": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L80 | neighbors=[Transport] | lang=en
- "agent_transport_transport_agent_id": ".agent_id()" | kind=code-symbol | source=probe/agent/transport.py:L145 | neighbors=[Transport] | lang=en
- "agent_transport_transport_agent_token": ".agent_token()" | kind=code-symbol | source=probe/agent/transport.py:L153 | neighbors=[Transport] | lang=en
- "agent_transport_transport_auth_header": ".auth_header()" | kind=code-symbol | source=probe/agent/transport.py:L161 | neighbors=[Transport] | lang=en
- "agent_transport_transport_create_enrollment_request": ".create_enrollment_request()" | kind=code-symbol | source=probe/agent/transport.py:L312 | neighbors=[Transport] | lang=en
- "agent_transport_transport_poll_enrollment": ".poll_enrollment()" | kind=code-symbol | source=probe/agent/transport.py:L317 | neighbors=[Transport] | lang=en
- "agent_use_cases_rationale_1": "use_cases.py — the finite, pre-defined library of scan scenarios the manager can" | kind=entity | source=probe/agent/use_cases.py:L1 | neighbors=[use_cases.py] | lang=en
- "agent_use_cases_rationale_119": "Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id" | kind=entity | source=probe/agent/use_cases.py:L119 | neighbors=[resolve()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-080.json

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
