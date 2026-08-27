# Node Description Batch 64 of 92

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

- "scanner_port_scanner_portscanner_init": ".__init__()" | kind=code-symbol | source=scanner/port_scanner.py:L259 | neighbors=[PortScanner] | lang=en
- "scanner_port_scanner_rationale_1": "port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD" | kind=entity | source=scanner/port_scanner.py:L1 | neighbors=[port_scanner.py] | lang=en
- "scanner_port_scanner_rationale_131": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=scanner/port_scanner.py:L131 | neighbors=[resolve_profile()] | lang=pt
- "scanner_port_scanner_rationale_157": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=scanner/port_scanner.py:L157 | neighbors=[ScanMetrics] | lang=en
- "scanner_port_scanner_rationale_185": "Tally exactly one terminal per-port observation." | kind=entity | source=scanner/port_scanner.py:L185 | neighbors=[.record()] | lang=en
- "scanner_port_scanner_rationale_204": "Requested ports that were never recorded — the silent-skip proof." | kind=entity | source=scanner/port_scanner.py:L204 | neighbors=[.missing_ports()] | lang=en
- "scanner_port_scanner_rationale_211": "Ports recorded more than once (a port must get exactly one verdict)." | kind=entity | source=scanner/port_scanner.py:L211 | neighbors=[.duplicate_ports()] | lang=pt
- "scanner_port_scanner_rationale_326": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=scanner/port_scanner.py:L326 | neighbors=[._attempt()] | lang=en
- "scanner_port_scanner_rationale_405": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=scanner/port_scanner.py:L405 | neighbors=[.scan_target()] | lang=en
- "scanner_port_scanner_rationale_93": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=scanner/port_scanner.py:L93 | neighbors=[_family_of()] | lang=en
- "scanner_port_scanner_scanmetrics_classified": ".classified()" | kind=code-symbol | source=scanner/port_scanner.py:L199 | neighbors=[ScanMetrics] | lang=en
- "scanner_port_scanner_scanmetrics_complete": ".complete()" | kind=code-symbol | source=scanner/port_scanner.py:L215 | neighbors=[ScanMetrics] | lang=en
- "scanner_port_scanner_scanmetrics_degraded": ".degraded()" | kind=code-symbol | source=scanner/port_scanner.py:L227 | neighbors=[ScanMetrics] | lang=en
- "scanner_rdp_scanner_rationale_44": "TPKT + X.224 Connection Request carrying an RDP Negotiation Request." | kind=entity | source=scanner/rdp_scanner.py:L44 | neighbors=[build_connection_request()] | lang=en
- "scanner_rdp_scanner_rationale_56": "Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the" | kind=entity | source=scanner/rdp_scanner.py:L56 | neighbors=[parse_connection_confirm()] | lang=en
- "scanner_rdp_scanner_rationale_84": "One synchronous RDP handshake. Best-effort; None on any failure." | kind=entity | source=scanner/rdp_scanner.py:L84 | neighbors=[probe_rdp()] | lang=en
- "scanner_rdp_scanner_rdpscanner_init": ".__init__()" | kind=code-symbol | source=scanner/rdp_scanner.py:L98 | neighbors=[RDPScanner] | lang=en
- "scanner_run_all_rationale_47": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=scanner/run_all.py:L47 | neighbors=[_run_stage()] | lang=en
- "scanner_run_all_rationale_48": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=scanner/run_all.py:L48 | neighbors=[_run_stage()] | lang=en
- "scanner_run_all_rationale_49": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=scanner/run_all.py:L49 | neighbors=[_run_stage()] | lang=en
- "scanner_run_all_rationale_52": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=scanner/run_all.py:L52 | neighbors=[_run_stage()] | lang=en
- "scanner_run_all_rationale_53": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=scanner/run_all.py:L53 | neighbors=[_run_stage()] | lang=en
- "scanner_run_all_rationale_55": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=scanner/run_all.py:L55 | neighbors=[_run_stage()] | lang=en
- "scanner_run_all_rationale_56": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=scanner/run_all.py:L56 | neighbors=[_run_stage()] | lang=en
- "scanner_scan_funnel_main": "main()" | kind=code-symbol | source=scanner/scan_funnel.py:L327 | neighbors=[scan_funnel.py] | lang=en
- "scanner_scan_funnel_rationale_1": "scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0" | kind=entity | source=scanner/scan_funnel.py:L1 | neighbors=[scan_funnel.py] | lang=en
- "scanner_scan_funnel_rationale_100": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=scanner/scan_funnel.py:L100 | neighbors=[ScanFunnel] | lang=en
- "scanner_scan_funnel_rationale_102": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=scanner/scan_funnel.py:L102 | neighbors=[ScanFunnel] | lang=en
- "scanner_scan_funnel_rationale_103": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=scanner/scan_funnel.py:L103 | neighbors=[ScanFunnel] | lang=en
- "scanner_scan_funnel_rationale_106": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=scanner/scan_funnel.py:L106 | neighbors=[ScanFunnel] | lang=en
- "scanner_scan_funnel_rationale_107": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=scanner/scan_funnel.py:L107 | neighbors=[ScanFunnel] | lang=en
- "scanner_scan_funnel_rationale_109": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=scanner/scan_funnel.py:L109 | neighbors=[ScanFunnel] | lang=en
- "scanner_scan_funnel_rationale_110": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=scanner/scan_funnel.py:L110 | neighbors=[ScanFunnel] | lang=en
- "scanner_scan_funnel_rationale_182": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=scanner/scan_funnel.py:L182 | neighbors=[.run()] | lang=en
- "scanner_scan_funnel_rationale_184": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=scanner/scan_funnel.py:L184 | neighbors=[.run()] | lang=en
- "scanner_scan_funnel_rationale_185": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=scanner/scan_funnel.py:L185 | neighbors=[.run()] | lang=en
- "scanner_scan_funnel_rationale_188": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=scanner/scan_funnel.py:L188 | neighbors=[.run()] | lang=en
- "scanner_scan_funnel_rationale_189": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=scanner/scan_funnel.py:L189 | neighbors=[.run()] | lang=en
- "scanner_scan_funnel_rationale_191": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=scanner/scan_funnel.py:L191 | neighbors=[.run()] | lang=en
- "scanner_scan_funnel_rationale_192": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=scanner/scan_funnel.py:L192 | neighbors=[.run()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-063.json

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
