# Node Description Batch 119 of 119

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

- "agent_agent_rationale_606": "Cloud infrastructure scan (AWS/Azure/GCP)." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L606
- "agent_agent_rationale_76": "Fetches credentials from HashiCorp Vault at runtime. Never caches to disk." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L76
- "agent_agent_rationale_82": "Read a KV-v2 secret from Vault." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L82
- "e2e_interop_verify_rationale_1": "Verify the Python probe can open what the TypeScript manager sealed (T14 interop" | kind=entity | source=manager/frontend/tests/e2e/interop_verify.py:L1
- "e2e_mock_manager_rationale_1": "Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO" | kind=entity | source=manager/frontend/tests/e2e/mock_manager.py:L1
- "e2e_mock_manager_rationale_235": "Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64)." | kind=entity | source=manager/frontend/tests/e2e/mock_manager.py:L235
- "e2e_run_rationale_1": "End-to-end probe test: real probe process ↔ reference mock manager over HTTPS." | kind=entity | source=manager/frontend/tests/e2e/run.py:L1
- "e2e_run_rationale_30": "Deterministic stand-ins emitting realistic output for 127.0.0.1." | kind=entity | source=manager/frontend/tests/e2e/run.py:L30
- "threadinghttpserver": "ThreadingHTTPServer" | kind=code-symbol

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-118.json

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
