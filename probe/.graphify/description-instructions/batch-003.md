# Node Description Batch 4 of 92

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "main_scripts_scan_funnel_rationale_1": "scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0" | kind=entity | source=main_scripts/scan_funnel.py:L1 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, scan_funnel.py, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_100": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=main_scripts/scan_funnel.py:L100 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, ScanFunnel, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_102": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=main_scripts/scan_funnel.py:L102 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, ScanFunnel, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_103": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=main_scripts/scan_funnel.py:L103 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, ScanFunnel, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_106": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=main_scripts/scan_funnel.py:L106 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, ScanFunnel, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_107": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=main_scripts/scan_funnel.py:L107 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, ScanFunnel, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_109": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=main_scripts/scan_funnel.py:L109 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, ScanFunnel, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_110": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=main_scripts/scan_funnel.py:L110 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, ScanFunnel, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_182": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=main_scripts/scan_funnel.py:L182 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, .run(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_184": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=main_scripts/scan_funnel.py:L184 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, .run(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_185": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=main_scripts/scan_funnel.py:L185 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, .run(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_188": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=main_scripts/scan_funnel.py:L188 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, .run(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_189": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=main_scripts/scan_funnel.py:L189 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, .run(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_191": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=main_scripts/scan_funnel.py:L191 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, .run(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_192": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=main_scripts/scan_funnel.py:L192 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, .run(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_209": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=main_scripts/scan_funnel.py:L209 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_211": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=main_scripts/scan_funnel.py:L211 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_212": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=main_scripts/scan_funnel.py:L212 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_215": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=main_scripts/scan_funnel.py:L215 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_216": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=main_scripts/scan_funnel.py:L216 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_218": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=main_scripts/scan_funnel.py:L218 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_219": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=main_scripts/scan_funnel.py:L219 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_57": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=main_scripts/scan_funnel.py:L57 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, route_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_59": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=main_scripts/scan_funnel.py:L59 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, route_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_60": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=main_scripts/scan_funnel.py:L60 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, route_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_63": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=main_scripts/scan_funnel.py:L63 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, route_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_64": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=main_scripts/scan_funnel.py:L64 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, route_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_66": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=main_scripts/scan_funnel.py:L66 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, route_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_67": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=main_scripts/scan_funnel.py:L67 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, route_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_74": "The full outcome of funnelling one host." | kind=entity | source=main_scripts/scan_funnel.py:L74 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, FunnelResult, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_76": "The full outcome of funnelling one host." | kind=entity | source=main_scripts/scan_funnel.py:L76 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, FunnelResult, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_77": "The full outcome of funnelling one host." | kind=entity | source=main_scripts/scan_funnel.py:L77 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, FunnelResult, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_80": "The full outcome of funnelling one host." | kind=entity | source=main_scripts/scan_funnel.py:L80 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, FunnelResult, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_81": "The full outcome of funnelling one host." | kind=entity | source=main_scripts/scan_funnel.py:L81 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, FunnelResult, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_83": "The full outcome of funnelling one host." | kind=entity | source=main_scripts/scan_funnel.py:L83 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, FunnelResult, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_84": "The full outcome of funnelling one host." | kind=entity | source=main_scripts/scan_funnel.py:L84 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, FunnelResult, ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_88": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=main_scripts/scan_funnel.py:L88 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, _candidate_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_90": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=main_scripts/scan_funnel.py:L90 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, _candidate_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_91": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=main_scripts/scan_funnel.py:L91 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, _candidate_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_94": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=main_scripts/scan_funnel.py:L94 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, _candidate_ports(), ResultWriter, ScanResult]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-003.json

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
