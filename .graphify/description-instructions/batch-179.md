# Node Description Batch 180 of 236

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

- "scanner_port_scanner_rationale_367": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L367 | neighbors=[.scan_target()]
- "scanner_port_scanner_rationale_391": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L391 | neighbors=[.scan_target()]
- "scanner_port_scanner_rationale_405": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L405 | neighbors=[.scan_target()]
- "scanner_port_scanner_rationale_90": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/scanner/port_scanner.py:L90 | neighbors=[_family_of()]
- "scanner_port_scanner_rationale_91": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/scanner/port_scanner.py:L91 | neighbors=[_family_of()]
- "scanner_port_scanner_rationale_93": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/scanner/port_scanner.py:L93 | neighbors=[_family_of()]
- "scanner_port_scanner_scanmetrics_classified": ".classified()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L199 | neighbors=[ScanMetrics]
- "scanner_port_scanner_scanmetrics_complete": ".complete()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L215 | neighbors=[ScanMetrics]
- "scanner_port_scanner_scanmetrics_degraded": ".degraded()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L227 | neighbors=[ScanMetrics]
- "scanner_rdp_scanner_rationale_44": "TPKT + X.224 Connection Request carrying an RDP Negotiation Request." | kind=entity | source=probe/scanner/rdp_scanner.py:L44 | neighbors=[build_connection_request()]
- "scanner_rdp_scanner_rationale_56": "Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the" | kind=entity | source=probe/scanner/rdp_scanner.py:L56 | neighbors=[parse_connection_confirm()]
- "scanner_rdp_scanner_rationale_84": "One synchronous RDP handshake. Best-effort; None on any failure." | kind=entity | source=probe/scanner/rdp_scanner.py:L84 | neighbors=[probe_rdp()]
- "scanner_rdp_scanner_rdpscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L98 | neighbors=[RDPScanner]
- "scanner_run_all_rationale_46": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=probe/scanner/run_all.py:L46 | neighbors=[_run_stage()]
- "scanner_run_all_rationale_56": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=probe/scanner/run_all.py:L56 | neighbors=[_run_stage()]
- "scanner_scan_funnel_main": "main()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L327 | neighbors=[scan_funnel.py]
- "scanner_scan_funnel_rationale_1": "scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0" | kind=entity | source=probe/scanner/scan_funnel.py:L1 | neighbors=[scan_funnel.py]
- "scanner_scan_funnel_rationale_110": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=probe/scanner/scan_funnel.py:L110 | neighbors=[ScanFunnel]
- "scanner_scan_funnel_rationale_181": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=probe/scanner/scan_funnel.py:L181 | neighbors=[.run()]
- "scanner_scan_funnel_rationale_192": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=probe/scanner/scan_funnel.py:L192 | neighbors=[.run()]
- "scanner_scan_funnel_rationale_208": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=probe/scanner/scan_funnel.py:L208 | neighbors=[build_default_funnel()]
- "scanner_scan_funnel_rationale_219": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=probe/scanner/scan_funnel.py:L219 | neighbors=[build_default_funnel()]
- "scanner_scan_funnel_rationale_56": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=probe/scanner/scan_funnel.py:L56 | neighbors=[route_ports()]
- "scanner_scan_funnel_rationale_67": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=probe/scanner/scan_funnel.py:L67 | neighbors=[route_ports()]
- "scanner_scan_funnel_rationale_73": "The full outcome of funnelling one host." | kind=entity | source=probe/scanner/scan_funnel.py:L73 | neighbors=[FunnelResult]
- "scanner_scan_funnel_rationale_84": "The full outcome of funnelling one host." | kind=entity | source=probe/scanner/scan_funnel.py:L84 | neighbors=[FunnelResult]
- "scanner_scan_funnel_rationale_87": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=probe/scanner/scan_funnel.py:L87 | neighbors=[_candidate_ports()]
- "scanner_scan_funnel_rationale_98": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=probe/scanner/scan_funnel.py:L98 | neighbors=[_candidate_ports()]
- "scanner_scan_funnel_rationale_99": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=probe/scanner/scan_funnel.py:L99 | neighbors=[ScanFunnel]
- "scanner_scan_funnel_scanfunnel_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L125 | neighbors=[ScanFunnel]
- "scanner_scanner_base_adaptiveratecontroller_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L421 | neighbors=[AdaptiveRateController]
- "scanner_scanner_base_base_argparser": "base_argparser()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L804 | neighbors=[scanner_base.py]
- "scanner_scanner_base_ratelimiter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L368 | neighbors=[RateLimiter]
- "scanner_scanner_base_rationale_1": "scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD" | kind=entity | source=probe/scanner/scanner_base.py:L1 | neighbors=[scanner_base.py]
- "scanner_scanner_base_rationale_115": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=probe/scanner/scanner_base.py:L115 | neighbors=[describe_os_error()]
- "scanner_scanner_base_rationale_130": "One observation about one target. Pure fact, no interpretation.      Network-sta" | kind=entity | source=probe/scanner/scanner_base.py:L130 | neighbors=[ScanResult]
- "scanner_scanner_base_rationale_171": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L171 | neighbors=[.networks()]
- "scanner_scanner_base_rationale_175": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/scanner/scanner_base.py:L175 | neighbors=[.excludes()]
- "scanner_scanner_base_rationale_176": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/scanner/scanner_base.py:L176 | neighbors=[.excludes()]
- "scanner_scanner_base_rationale_181": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L181 | neighbors=[ScopeGuard]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-179.json

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
