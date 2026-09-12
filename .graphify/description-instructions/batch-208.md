# Node Description Batch 209 of 380

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

- "agent_transport_rationale_752": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L752 | neighbors=[.submit_result()]
- "agent_transport_rationale_767": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L767 | neighbors=[.ws_url()]
- "agent_transport_rationale_77": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L77 | neighbors=[Transport]
- "agent_transport_rationale_771": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L771 | neighbors=[.fetch_scope()]
- "agent_transport_rationale_78": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L78 | neighbors=[Transport]
- "agent_transport_rationale_790": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L790 | neighbors=[.submit_result()]
- "agent_transport_rationale_791": "Commit ONE finished host while the job is still running.          Best-effort by" | kind=entity | source=probe/agent/transport.py:L791 | neighbors=[.submit_chunk()]
- "agent_transport_rationale_793": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L793 | neighbors=[.ws_url()]
- "agent_transport_rationale_80": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L80 | neighbors=[Transport]
- "agent_transport_rationale_803": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L803 | neighbors=[.connect_ws()]
- "agent_transport_rationale_809": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L809 | neighbors=[.is_ws_connected()]
- "agent_transport_rationale_817": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L817 | neighbors=[.http_get()]
- "agent_transport_rationale_831": "Hosts the manager already holds for this job, so a retry can skip them." | kind=entity | source=probe/agent/transport.py:L831 | neighbors=[.committed_hosts()]
- "agent_transport_rationale_833": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L833 | neighbors=[.ws_url()]
- "agent_transport_rationale_835": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L835 | neighbors=[.is_ws_connected()]
- "agent_transport_rationale_84": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L84 | neighbors=[_atomic_write_private_state()]
- "agent_transport_rationale_843": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L843 | neighbors=[.connect_ws()]
- "agent_transport_rationale_853": "Submit a scan result to the manager.          Returns True ONLY on a 2xx respons" | kind=entity | source=probe/agent/transport.py:L853 | neighbors=[.submit_result()]
- "agent_transport_rationale_855": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L855 | neighbors=[.http_get()]
- "agent_transport_rationale_871": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L871 | neighbors=[.ws_url()]
- "agent_transport_rationale_875": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L875 | neighbors=[.is_ws_connected()]
- "agent_transport_rationale_881": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L881 | neighbors=[.connect_ws()]
- "agent_transport_rationale_913": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L913 | neighbors=[.is_ws_connected()]
- "agent_transport_rationale_918": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L918 | neighbors=[.http_get()]
- "agent_transport_rationale_93": "Stable identity for the manager a credential belongs to.      Device credentials" | kind=entity | source=probe/agent/transport.py:L93 | neighbors=[manager_fingerprint()]
- "agent_transport_rationale_934": "Return the WebSocket endpoint without embedding credentials.          Authentica" | kind=entity | source=probe/agent/transport.py:L934 | neighbors=[.ws_url()]
- "agent_transport_rationale_944": "Establish an authenticated WebSocket connection to the manager.          Returns" | kind=entity | source=probe/agent/transport.py:L944 | neighbors=[.connect_ws()]
- "agent_transport_rationale_976": "True if the WebSocket connection is active." | kind=entity | source=probe/agent/transport.py:L976 | neighbors=[.is_ws_connected()]
- "agent_transport_rationale_98": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L98 | neighbors=[Transport]
- "agent_transport_transport_agent_id": ".agent_id()" | kind=code-symbol | source=probe/agent/transport.py:L249 | neighbors=[Transport]
- "agent_transport_transport_agent_token": ".agent_token()" | kind=code-symbol | source=probe/agent/transport.py:L257 | neighbors=[Transport]
- "agent_transport_transport_auth_header": ".auth_header()" | kind=code-symbol | source=probe/agent/transport.py:L265 | neighbors=[Transport]
- "agent_use_cases_rationale_1": "use_cases.py — the finite, pre-defined library of scan scenarios the manager can" | kind=entity | source=probe/agent/use_cases.py:L1 | neighbors=[use_cases.py]
- "agent_use_cases_rationale_119": "Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id" | kind=entity | source=probe/agent/use_cases.py:L119 | neighbors=[resolve()]
- "agent_use_cases_rationale_120": "Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id" | kind=entity | source=probe/agent/use_cases.py:L120 | neighbors=[resolve()]
- "agent_use_cases_rationale_167": "Return (scan_type, profile, intensity) for a job.      Resolution order:     1." | kind=entity | source=probe/agent/use_cases.py:L167 | neighbors=[resolve()]
- "agent_use_cases_rationale_196": "Coerce an int-or-numeric-string to int, else None (non-numeric)." | kind=entity | source=probe/agent/use_cases.py:L196 | neighbors=[_as_int()]
- "agent_use_cases_rationale_207": "Map a numeric use-case code → use_case_id (raises on an unknown code)." | kind=entity | source=probe/agent/use_cases.py:L207 | neighbors=[use_case_for_code()]
- "agent_use_cases_rationale_218": "Accept an intensity as a number (1/2/3) OR a name; return the name.      None st" | kind=entity | source=probe/agent/use_cases.py:L218 | neighbors=[normalize_intensity()]
- "agent_use_cases_rationale_237": "Return (scan_type, profile, intensity) for a job.      Resolution order:     1." | kind=entity | source=probe/agent/use_cases.py:L237 | neighbors=[resolve()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-208.json

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
