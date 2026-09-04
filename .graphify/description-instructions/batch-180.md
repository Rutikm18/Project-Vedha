# Node Description Batch 181 of 332

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

- "agent_transport_rationale_50": "Raised when a transport operation fails permanently (not retryable)." | kind=entity | source=probe/agent/transport.py:L50 | neighbors=[TransportError] | lang=pt
- "agent_transport_rationale_519": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L519 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_525": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L525 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_54": "The probe's device signing key is already registered as an agent on the     mana" | kind=entity | source=probe/agent/transport.py:L54 | neighbors=[DeviceAlreadyEnrolledError] | lang=en
- "agent_transport_rationale_540": "Refresh a device token before expiry; legacy identities are unchanged." | kind=entity | source=probe/agent/transport.py:L540 | neighbors=[.ensure_device_access()] | lang=en
- "agent_transport_rationale_543": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L543 | neighbors=[.poll_jobs()] | lang=en
- "agent_transport_rationale_545": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L545 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_563": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L563 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_582": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L582 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_589": "Send a heartbeat and report WHY it failed, not just that it did.          Return" | kind=entity | source=probe/agent/transport.py:L589 | neighbors=[.heartbeat_ex()] | lang=en
- "agent_transport_rationale_601": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L601 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_615": "Send a heartbeat and report WHY it failed, not just that it did.          Return" | kind=entity | source=probe/agent/transport.py:L615 | neighbors=[.heartbeat_ex()] | lang=en
- "agent_transport_rationale_617": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L617 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_635": "Backwards-compatible bool form of `heartbeat_ex`.          Returns True only whe" | kind=entity | source=probe/agent/transport.py:L635 | neighbors=[.heartbeat()] | lang=en
- "agent_transport_rationale_643": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L643 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_653": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L653 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_659": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L659 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_66": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L66 | neighbors=[_atomic_write_private_state()] | lang=en
- "agent_transport_rationale_661": "Backwards-compatible bool form of `heartbeat_ex`.          Returns True only whe" | kind=entity | source=probe/agent/transport.py:L661 | neighbors=[.heartbeat()] | lang=en
- "agent_transport_rationale_663": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L663 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_667": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L667 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_685": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L685 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_686": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L686 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_693": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L693 | neighbors=[.fetch_scope()] | lang=en
- "agent_transport_rationale_705": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L705 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_712": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L712 | neighbors=[.submit_result()] | lang=en
- "agent_transport_rationale_751": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L751 | neighbors=[.http_get()] | lang=en
- "agent_transport_rationale_767": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L767 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_77": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L77 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_78": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L78 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_793": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L793 | neighbors=[.ws_url()] | lang=en
- "agent_transport_rationale_80": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L80 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_803": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L803 | neighbors=[.connect_ws()] | lang=en
- "agent_transport_rationale_809": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L809 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_835": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L835 | neighbors=[.is_ws_connected()] | lang=en
- "agent_transport_rationale_84": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L84 | neighbors=[_atomic_write_private_state()] | lang=en
- "agent_transport_rationale_93": "Stable identity for the manager a credential belongs to.      Device credentials" | kind=entity | source=probe/agent/transport.py:L93 | neighbors=[manager_fingerprint()] | lang=en
- "agent_transport_rationale_98": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L98 | neighbors=[Transport] | lang=en
- "agent_transport_transport_agent_id": ".agent_id()" | kind=code-symbol | source=probe/agent/transport.py:L249 | neighbors=[Transport] | lang=en
- "agent_transport_transport_agent_token": ".agent_token()" | kind=code-symbol | source=probe/agent/transport.py:L257 | neighbors=[Transport] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-180.json

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
