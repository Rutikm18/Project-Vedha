# Node Description Batch 329 of 330

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

- "workflow_router_rationale_73": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L73 | neighbors=[route_branches()]
- "workflow_router_rationale_85": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L85 | neighbors=[route_branches()]
- "workflow_workflow_engine_rationale_1": "workflow_engine.py — the async DAG executor. Loops through gates, checks precond" | kind=entity | source=probe/workflow/workflow_engine.py:L1 | neighbors=[workflow_engine.py]
- "workflow_workflow_engine_rationale_104": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L104 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_107": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L107 | neighbors=[_split_cached()]
- "workflow_workflow_engine_rationale_110": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L110 | neighbors=[_port_candidates()]
- "workflow_workflow_engine_rationale_111": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L111 | neighbors=[_port_candidates()]
- "workflow_workflow_engine_rationale_114": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L114 | neighbors=[_port_candidates()]
- "workflow_workflow_engine_rationale_124": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L124 | neighbors=[_port_candidates()]
- "workflow_workflow_engine_rationale_129": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L129 | neighbors=[_split_cached()]
- "workflow_workflow_engine_rationale_134": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L134 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_136": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L136 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_144": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L144 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_145": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L145 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_146": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L146 | neighbors=[_port_candidates()]
- "workflow_workflow_engine_rationale_147": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L147 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_175": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L175 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_179": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L179 | neighbors=[_Sink]
- "workflow_workflow_engine_rationale_236": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L236 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_247": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L247 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_249": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L249 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_251": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L251 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_252": "Hosts scanned in parallel during the deep-branch stage.      Env override: PROBE" | kind=entity | source=probe/workflow/workflow_engine.py:L252 | neighbors=[_default_host_concurrency()]
- "workflow_workflow_engine_rationale_270": "Accumulate wall time for a stage. No-op when tracing is off." | kind=entity | source=probe/workflow/workflow_engine.py:L270 | neighbors=[_timed()]
- "workflow_workflow_engine_rationale_283": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L283 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_309": "Run ONE deep-scan branch for one host: the gate -> split-cache -> scan ->     re" | kind=entity | source=probe/workflow/workflow_engine.py:L309 | neighbors=[_run_branch()]
- "workflow_workflow_engine_rationale_378": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L378 | neighbors=[run_engagement()]
- "workflow_workflow_engine_rationale_51": "Runs scanner.scan_target(host) across hosts concurrently; the     scanner's own" | kind=entity | source=probe/workflow/workflow_engine.py:L51 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_59": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L59 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_60": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L60 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_62": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L62 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_64": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L64 | neighbors=[_split_cached()]
- "workflow_workflow_engine_rationale_72": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L72 | neighbors=[_scan_one()]
- "workflow_workflow_engine_rationale_77": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L77 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_78": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L78 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_90": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L90 | neighbors=[_gather_per_host()]
- "workflow_workflow_engine_rationale_95": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L95 | neighbors=[_split_cached()]
- "workflow_workflow_engine_rationale_97": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L97 | neighbors=[_split_cached()]
- "workflow_workflow_engine_sink_close": ".close()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L186 | neighbors=[_Sink]
- "workflow_workflow_engine_sink_init": ".__init__()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L182 | neighbors=[_Sink]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-328.json

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
