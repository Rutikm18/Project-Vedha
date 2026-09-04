# Node Description Batch 220 of 332

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

- "main_scripts_port_scanner_rationale_90": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/main_scripts/port_scanner.py:L90 | neighbors=[_family_of()] | lang=en
- "main_scripts_port_scanner_rationale_91": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/main_scripts/port_scanner.py:L91 | neighbors=[_family_of()] | lang=en
- "main_scripts_port_scanner_rationale_93": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/main_scripts/port_scanner.py:L93 | neighbors=[_family_of()] | lang=en
- "main_scripts_port_scanner_rationale_95": "Peer TCP-stack signals readable from a COMPLETED connect(), for OS/link     fing" | kind=entity | source=probe/main_scripts/port_scanner.py:L95 | neighbors=[_harvest_tcp_stack()] | lang=en
- "main_scripts_port_scanner_scanmetrics_classified": ".classified()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L282 | neighbors=[ScanMetrics] | lang=en
- "main_scripts_port_scanner_scanmetrics_complete": ".complete()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L298 | neighbors=[ScanMetrics] | lang=en
- "main_scripts_port_scanner_scanmetrics_degraded": ".degraded()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L310 | neighbors=[ScanMetrics] | lang=en
- "main_scripts_printer_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L160 | neighbors=[printer_scanner.py] | lang=en
- "main_scripts_printer_scanner_printerscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L99 | neighbors=[PrinterScanner] | lang=en
- "main_scripts_printer_scanner_rationale_1": "printer_scanner.py — network printer exposure (VA checklist: exposed print servi" | kind=entity | source=probe/main_scripts/printer_scanner.py:L1 | neighbors=[printer_scanner.py] | lang=en
- "main_scripts_printer_scanner_rationale_39": "Extract the model string from a PJL INFO ID response." | kind=entity | source=probe/main_scripts/printer_scanner.py:L39 | neighbors=[parse_pjl_id()] | lang=en
- "main_scripts_printer_scanner_rationale_55": "A minimal IPP/1.1 Get-Printer-Attributes request body (RFC 8010)." | kind=entity | source=probe/main_scripts/printer_scanner.py:L55 | neighbors=[build_ipp_get_printer_attributes()] | lang=pt
- "main_scripts_printer_scanner_rationale_66": "Best-effort extraction of printer-make-and-model / printer-name from an IPP" | kind=entity | source=probe/main_scripts/printer_scanner.py:L66 | neighbors=[parse_ipp_make_model()] | lang=en
- "main_scripts_rdp_scanner_rationale_111": "Two-probe RDP posture (MS-RDPBCGR 2.2.1.1.1 / 2.2.1.2.1).      Probe A offers SS" | kind=entity | source=probe/main_scripts/rdp_scanner.py:L111 | neighbors=[probe_rdp_posture()] | lang=pt
- "main_scripts_rdp_scanner_rationale_44": "TPKT + X.224 Connection Request carrying an RDP Negotiation Request." | kind=entity | source=probe/main_scripts/rdp_scanner.py:L44 | neighbors=[build_connection_request()] | lang=en
- "main_scripts_rdp_scanner_rationale_45": "TPKT + X.224 Connection Request carrying an RDP Negotiation Request." | kind=entity | source=probe/main_scripts/rdp_scanner.py:L45 | neighbors=[build_connection_request()] | lang=en
- "main_scripts_rdp_scanner_rationale_56": "Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the" | kind=entity | source=probe/main_scripts/rdp_scanner.py:L56 | neighbors=[parse_connection_confirm()] | lang=en
- "main_scripts_rdp_scanner_rationale_57": "Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the" | kind=entity | source=probe/main_scripts/rdp_scanner.py:L57 | neighbors=[parse_connection_confirm()] | lang=en
- "main_scripts_rdp_scanner_rationale_77": "Map an RDP selectedProtocol bitmask to (nla, tls) posture.      MS-RDPBCGR 5.4.5" | kind=entity | source=probe/main_scripts/rdp_scanner.py:L77 | neighbors=[_posture_from_selected()] | lang=en
- "main_scripts_rdp_scanner_rationale_84": "One synchronous RDP handshake. Best-effort; None on any failure." | kind=entity | source=probe/main_scripts/rdp_scanner.py:L84 | neighbors=[probe_rdp()] | lang=en
- "main_scripts_rdp_scanner_rationale_98": "One synchronous RDP handshake offering `requested_protocols`. Best-effort;     N" | kind=entity | source=probe/main_scripts/rdp_scanner.py:L98 | neighbors=[probe_rdp()] | lang=en
- "main_scripts_rdp_scanner_rdpscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L138 | neighbors=[RDPScanner] | lang=en
- "main_scripts_rsync_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L167 | neighbors=[rsync_scanner.py] | lang=en
- "main_scripts_rsync_scanner_rationale_1": "rsync_scanner.py — rsync daemon anonymous-module exposure (VA checklist: anonymo" | kind=entity | source=probe/main_scripts/rsync_scanner.py:L1 | neighbors=[rsync_scanner.py] | lang=en
- "main_scripts_rsync_scanner_rationale_114": "Select a module without a secret: OK => anonymous, AUTHREQD => auth." | kind=entity | source=probe/main_scripts/rsync_scanner.py:L114 | neighbors=[._test_anon()] | lang=pt
- "main_scripts_rsync_scanner_rationale_131": "Blocking: list modules, then anon-test each. Monkeypatchable for tests." | kind=entity | source=probe/main_scripts/rsync_scanner.py:L131 | neighbors=[._probe()] | lang=en
- "main_scripts_rsync_scanner_rationale_38": "Parse the daemon's module listing into [{name, comment}]. Lines are     'name<wh" | kind=entity | source=probe/main_scripts/rsync_scanner.py:L38 | neighbors=[parse_modules()] | lang=en
- "main_scripts_rsync_scanner_rationale_74": "Read the @RSYNCD greeting and echo it back VERBATIM. Returns the negotiated" | kind=entity | source=probe/main_scripts/rsync_scanner.py:L74 | neighbors=[_handshake()] | lang=en
- "main_scripts_rsync_scanner_rsyncscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L96 | neighbors=[RsyncScanner] | lang=en
- "main_scripts_run_all_rationale_46": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=probe/main_scripts/run_all.py:L46 | neighbors=[_run_stage()] | lang=en
- "main_scripts_run_all_rationale_56": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=probe/main_scripts/run_all.py:L56 | neighbors=[_run_stage()] | lang=en
- "main_scripts_run_all_rationale_60": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=probe/main_scripts/run_all.py:L60 | neighbors=[_run_stage()] | lang=en
- "main_scripts_run_all_rationale_99": "EPM-advertised dynamic RPC ports from the msrpc stage (same field the funnel" | kind=entity | source=probe/main_scripts/run_all.py:L99 | neighbors=[_advertised_dynamic_ports()] | lang=en
- "main_scripts_scan_funnel_main": "main()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L386 | neighbors=[scan_funnel.py] | lang=en
- "main_scripts_scan_funnel_rationale_1": "scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0" | kind=entity | source=probe/main_scripts/scan_funnel.py:L1 | neighbors=[scan_funnel.py] | lang=en
- "main_scripts_scan_funnel_rationale_104": "The full outcome of funnelling one host." | kind=entity | source=probe/main_scripts/scan_funnel.py:L104 | neighbors=[FunnelResult] | lang=en
- "main_scripts_scan_funnel_rationale_110": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=probe/main_scripts/scan_funnel.py:L110 | neighbors=[ScanFunnel] | lang=en
- "main_scripts_scan_funnel_rationale_118": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=probe/main_scripts/scan_funnel.py:L118 | neighbors=[_candidate_ports()] | lang=en
- "main_scripts_scan_funnel_rationale_130": "Orchestrates discovery → port scan → routed deep scanners for each host.      Pa" | kind=entity | source=probe/main_scripts/scan_funnel.py:L130 | neighbors=[ScanFunnel] | lang=en
- "main_scripts_scan_funnel_rationale_181": "Funnel many hosts with bounded concurrency, writing every result." | kind=entity | source=probe/main_scripts/scan_funnel.py:L181 | neighbors=[.run()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-219.json

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
