# Node Description Batch 131 of 186

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

- "main_scripts_os_fingerprint_rationale_188": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/main_scripts/os_fingerprint.py:L188 | neighbors=[icmp_supported()] | lang=en
- "main_scripts_os_fingerprint_rationale_205": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/main_scripts/os_fingerprint.py:L205 | neighbors=[_open_icmp_socket()] | lang=en
- "main_scripts_os_fingerprint_rationale_221": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L221 | neighbors=[OSFingerprintScanner] | lang=en
- "main_scripts_os_fingerprint_rationale_233": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/main_scripts/os_fingerprint.py:L233 | neighbors=[._icmp_echo_ttl()] | lang=en
- "main_scripts_os_fingerprint_rationale_58": "Build an ICMP message (header + rest) with a valid checksum." | kind=entity | source=probe/main_scripts/os_fingerprint.py:L58 | neighbors=[_icmp()] | lang=en
- "main_scripts_os_fingerprint_rationale_80": "Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L80 | neighbors=[parse_icmp_reply()] | lang=en
- "main_scripts_passive_collector_main": "main()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L357 | neighbors=[passive_collector.py] | lang=en
- "main_scripts_passive_collector_passivecollector_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L218 | neighbors=[PassiveCollector] | lang=en
- "main_scripts_passive_collector_passivelistenererror_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L109 | neighbors=[PassiveListenerError] | lang=en
- "main_scripts_passive_collector_rationale_1": "passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)." | kind=entity | source=probe/main_scripts/passive_collector.py:L1 | neighbors=[passive_collector.py] | lang=en
- "main_scripts_passive_collector_rationale_107": "All passive sources failed before the listen window could start." | kind=entity | source=probe/main_scripts/passive_collector.py:L107 | neighbors=[PassiveListenerError] | lang=en
- "main_scripts_passive_collector_rationale_120": "Open one recv-only UDP listener or raise the socket error.      Multicast groups" | kind=entity | source=probe/main_scripts/passive_collector.py:L120 | neighbors=[_open_listener()] | lang=en
- "main_scripts_passive_collector_rationale_211": "Listen-only discovery. No active probing. Reports in-scope hosts that     announ" | kind=entity | source=probe/main_scripts/passive_collector.py:L211 | neighbors=[PassiveCollector] | lang=en
- "main_scripts_passive_collector_rationale_332": "Await readability on any listener without blocking the event loop." | kind=entity | source=probe/main_scripts/passive_collector.py:L332 | neighbors=[._select()] | lang=en
- "main_scripts_passive_collector_rationale_74": "Pull short printable ASCII runs from a payload, for human-readable evidence." | kind=entity | source=probe/main_scripts/passive_collector.py:L74 | neighbors=[_printable_strings()] | lang=en
- "main_scripts_passive_collector_rationale_91": "Best-effort device label from an announcement payload (recv-only parsing)." | kind=entity | source=probe/main_scripts/passive_collector.py:L91 | neighbors=[_device_hint()] | lang=en
- "main_scripts_port_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L418 | neighbors=[port_scanner.py] | lang=en
- "main_scripts_port_scanner_portscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L253 | neighbors=[PortScanner] | lang=en
- "main_scripts_port_scanner_rationale_1": "port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD" | kind=entity | source=probe/main_scripts/port_scanner.py:L1 | neighbors=[port_scanner.py] | lang=en
- "main_scripts_port_scanner_rationale_128": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=probe/main_scripts/port_scanner.py:L128 | neighbors=[resolve_profile()] | lang=pt
- "main_scripts_port_scanner_rationale_154": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=probe/main_scripts/port_scanner.py:L154 | neighbors=[ScanMetrics] | lang=en
- "main_scripts_port_scanner_rationale_182": "Tally exactly one terminal per-port observation." | kind=entity | source=probe/main_scripts/port_scanner.py:L182 | neighbors=[.record()] | lang=en
- "main_scripts_port_scanner_rationale_201": "Requested ports that were never recorded — the silent-skip proof." | kind=entity | source=probe/main_scripts/port_scanner.py:L201 | neighbors=[.missing_ports()] | lang=en
- "main_scripts_port_scanner_rationale_208": "Ports recorded more than once (a port must get exactly one verdict)." | kind=entity | source=probe/main_scripts/port_scanner.py:L208 | neighbors=[.duplicate_ports()] | lang=pt
- "main_scripts_port_scanner_rationale_301": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=probe/main_scripts/port_scanner.py:L301 | neighbors=[._attempt()] | lang=en
- "main_scripts_port_scanner_rationale_367": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/main_scripts/port_scanner.py:L367 | neighbors=[.scan_target()] | lang=en
- "main_scripts_port_scanner_rationale_90": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/main_scripts/port_scanner.py:L90 | neighbors=[_family_of()] | lang=en
- "main_scripts_port_scanner_scanmetrics_classified": ".classified()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L196 | neighbors=[ScanMetrics] | lang=en
- "main_scripts_port_scanner_scanmetrics_complete": ".complete()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L212 | neighbors=[ScanMetrics] | lang=en
- "main_scripts_port_scanner_scanmetrics_degraded": ".degraded()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L224 | neighbors=[ScanMetrics] | lang=en
- "main_scripts_run_all_rationale_46": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=probe/main_scripts/run_all.py:L46 | neighbors=[_run_stage()] | lang=en
- "main_scripts_scan_funnel_main": "main()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L261 | neighbors=[scan_funnel.py] | lang=en
- "main_scripts_scan_funnel_rationale_1": "scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0" | kind=entity | source=probe/main_scripts/scan_funnel.py:L1 | neighbors=[scan_funnel.py] | lang=en
- "main_scripts_scan_funnel_rationale_181": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=probe/main_scripts/scan_funnel.py:L181 | neighbors=[.run()] | lang=en
- "main_scripts_scan_funnel_rationale_208": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=probe/main_scripts/scan_funnel.py:L208 | neighbors=[build_default_funnel()] | lang=en
- "main_scripts_scan_funnel_rationale_56": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=probe/main_scripts/scan_funnel.py:L56 | neighbors=[route_ports()] | lang=en
- "main_scripts_scan_funnel_rationale_73": "The full outcome of funnelling one host." | kind=entity | source=probe/main_scripts/scan_funnel.py:L73 | neighbors=[FunnelResult] | lang=en
- "main_scripts_scan_funnel_rationale_87": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=probe/main_scripts/scan_funnel.py:L87 | neighbors=[_candidate_ports()] | lang=en
- "main_scripts_scan_funnel_rationale_99": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=probe/main_scripts/scan_funnel.py:L99 | neighbors=[ScanFunnel] | lang=en
- "main_scripts_scan_funnel_scanfunnel_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L114 | neighbors=[ScanFunnel] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-130.json

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
