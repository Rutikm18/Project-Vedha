# Node Description Batch 92 of 92

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

- "workflow_workflow_engine_rationale_123": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=workflow/workflow_engine.py:L123 | neighbors=[_port_candidates()]
- "workflow_workflow_engine_rationale_124": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=workflow/workflow_engine.py:L124 | neighbors=[_port_candidates()]
- "workflow_workflow_engine_rationale_148": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=workflow/workflow_engine.py:L148 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_154": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=workflow/workflow_engine.py:L154 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_157": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=workflow/workflow_engine.py:L157 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_166": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=workflow/workflow_engine.py:L166 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_170": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=workflow/workflow_engine.py:L170 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_176": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=workflow/workflow_engine.py:L176 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_179": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=workflow/workflow_engine.py:L179 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_252": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=workflow/workflow_engine.py:L252 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_258": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=workflow/workflow_engine.py:L258 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_261": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=workflow/workflow_engine.py:L261 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_270": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=workflow/workflow_engine.py:L270 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_274": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=workflow/workflow_engine.py:L274 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_280": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=workflow/workflow_engine.py:L280 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_283": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=workflow/workflow_engine.py:L283 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_61": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=workflow/workflow_engine.py:L61 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_63": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=workflow/workflow_engine.py:L63 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_64": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=workflow/workflow_engine.py:L64 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_67": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=workflow/workflow_engine.py:L67 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_69": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=workflow/workflow_engine.py:L69 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_71": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=workflow/workflow_engine.py:L71 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_72": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=workflow/workflow_engine.py:L72 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_79": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=workflow/workflow_engine.py:L79 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_81": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=workflow/workflow_engine.py:L81 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_82": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=workflow/workflow_engine.py:L82 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_85": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=workflow/workflow_engine.py:L85 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_87": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=workflow/workflow_engine.py:L87 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_89": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=workflow/workflow_engine.py:L89 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_90": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=workflow/workflow_engine.py:L90 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_96": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=workflow/workflow_engine.py:L96 | neighbors=[_split_cached()]
- "workflow_workflow_engine_rationale_98": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=workflow/workflow_engine.py:L98 | neighbors=[_split_cached()]
- "workflow_workflow_engine_rationale_99": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=workflow/workflow_engine.py:L99 | neighbors=[_split_cached()]
- "workflow_workflow_engine_sink_close": ".close()" | kind=code-symbol | source=workflow/workflow_engine.py:L190 | neighbors=[_Sink]
- "workflow_workflow_engine_sink_init": ".__init__()" | kind=code-symbol | source=workflow/workflow_engine.py:L186 | neighbors=[_Sink]
- "workflow_workflow_engine_sink_write": ".write()" | kind=code-symbol | source=workflow/workflow_engine.py:L188 | neighbors=[_Sink]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-091.json

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
