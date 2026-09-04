# Node Description Batch 332 of 332

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

- "e2e_run_rationale_1": "End-to-end probe test: real probe process ↔ reference mock manager over HTTPS." | kind=entity | source=manager/frontend/tests/e2e/run.py:L1
- "e2e_run_rationale_30": "Deterministic stand-ins emitting realistic output for 127.0.0.1." | kind=entity | source=manager/frontend/tests/e2e/run.py:L30
- "probe_pipeline_rationale_133": "Make a per-host scanner instance share ONE rate limiter + semaphore with all" | kind=entity | source=probe/pipeline.py:L133
- "probe_pipeline_rationale_252": "Make a raw banner safe and readable for the summary line.      Many services ans" | kind=entity | source=probe/pipeline.py:L252
- "probe_run_scan_rationale_42": "# NOTE: credentialed collectors (ssh_collector, windows_collector) are run" | kind=entity | source=probe/run_scan.py:L42
- "threadinghttpserver": "ThreadingHTTPServer" | kind=code-symbol

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-331.json

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
