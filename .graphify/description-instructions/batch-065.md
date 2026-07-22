# Node Description Batch 66 of 76

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

- "scanner_host_discovery_rationale_33": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L33 | neighbors=[._probe()] | lang=en
- "scanner_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=probe/scanner/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "scanner_mass_scan_connectsweep_init": ".__init__()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L142 | neighbors=[_ConnectSweep] | lang=en
- "scanner_mass_scan_main": "main()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L242 | neighbors=[mass_scan.py] | lang=en
- "scanner_mass_scan_rationale_1": "mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con" | kind=entity | source=probe/scanner/mass_scan.py:L1 | neighbors=[mass_scan.py] | lang=en
- "scanner_mass_scan_rationale_176": "target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them." | kind=entity | source=probe/scanner/mass_scan.py:L176 | neighbors=[run_mass_scan()] | lang=en
- "scanner_mass_scan_rationale_216": "Excluded networks -> masscan --exclude specs, so they get ZERO packets." | kind=entity | source=probe/scanner/mass_scan.py:L216 | neighbors=[_masscan_excludes()] | lang=en
- "scanner_mass_scan_rationale_221": "A CIDR spec is in scope only if it is fully contained in an allowed network." | kind=entity | source=probe/scanner/mass_scan.py:L221 | neighbors=[_spec_in_scope()] | lang=en
- "scanner_mass_scan_rationale_55": "Run masscan over the given target specs and return its parsed JSON records." | kind=entity | source=probe/scanner/mass_scan.py:L55 | neighbors=[_run_masscan()] | lang=en
- "scanner_mass_scan_rationale_90": "Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin" | kind=entity | source=probe/scanner/mass_scan.py:L90 | neighbors=[_parse_masscan_json()] | lang=en
- "scanner_mcp_ai_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L322 | neighbors=[mcp_ai_scanner.py] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L201 | neighbors=[MCPAIScanner] | lang=en
- "scanner_mcp_ai_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L110 | neighbors=[_NoRedirect] | lang=en
- "scanner_mcp_ai_scanner_rationale_1": "mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH" | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[mcp_ai_scanner.py] | lang=en
- "scanner_mcp_ai_scanner_rationale_152": "Server/body fingerprint match against known non-AI squatters, or None." | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L152 | neighbors=[_known_false_positive()] | lang=en
- "scanner_mcp_ai_scanner_rationale_161": "The strongest possible evidence for a real MCP server: a WWW-Authenticate     he" | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L161 | neighbors=[_mcp_oauth_signal()] | lang=en
- "scanner_mcp_ai_scanner_rationale_174": "JSON-typed body that actually talks about auth, not just any error text." | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L174 | neighbors=[_auth_shaped_json_body()] | lang=en
- "scanner_mcp_ai_scanner_request": "_request()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L127 | neighbors=[mcp_ai_scanner.py] | lang=en
- "scanner_nmap_wrapper_have_nmap": "_have_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_main": "main()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L128 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L63 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_rationale_1": "nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:" | kind=entity | source=probe/scanner/nmap_wrapper.py:L1 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_rationale_72": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/scanner/nmap_wrapper.py:L72 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L46 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_passive_collector_main": "main()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L230 | neighbors=[passive_collector.py] | lang=en
- "scanner_passive_collector_passivecollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L130 | neighbors=[PassiveCollector] | lang=en
- "scanner_passive_collector_rationale_1": "passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)." | kind=entity | source=probe/scanner/passive_collector.py:L1 | neighbors=[passive_collector.py] | lang=en
- "scanner_passive_collector_rationale_123": "Listen-only discovery. No active probing. Reports in-scope hosts that     announ" | kind=entity | source=probe/scanner/passive_collector.py:L123 | neighbors=[PassiveCollector] | lang=en
- "scanner_passive_collector_rationale_205": "Await readability on any listener without blocking the event loop." | kind=entity | source=probe/scanner/passive_collector.py:L205 | neighbors=[._select()] | lang=en
- "scanner_passive_collector_rationale_65": "Pull short printable ASCII runs from a payload, for human-readable evidence." | kind=entity | source=probe/scanner/passive_collector.py:L65 | neighbors=[_printable_strings()] | lang=en
- "scanner_passive_collector_rationale_82": "Best-effort device label from an announcement payload (recv-only parsing)." | kind=entity | source=probe/scanner/passive_collector.py:L82 | neighbors=[_device_hint()] | lang=en
- "scanner_passive_collector_rationale_98": "Open ONE recv-only UDP listener. Returns None (with a warning) on failure." | kind=entity | source=probe/scanner/passive_collector.py:L98 | neighbors=[_open_listener()] | lang=en
- "scanner_port_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L71 | neighbors=[port_scanner.py] | lang=en
- "scanner_port_scanner_portscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L30 | neighbors=[PortScanner] | lang=en
- "scanner_port_scanner_rationale_1": "port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec" | kind=entity | source=probe/scanner/port_scanner.py:L1 | neighbors=[port_scanner.py] | lang=pt
- "scanner_scanner_base_base_argparser": "base_argparser()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L437 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_ratelimiter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L185 | neighbors=[RateLimiter] | lang=en
- "scanner_scanner_base_rationale_1": "scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD" | kind=entity | source=probe/scanner/scanner_base.py:L1 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_rationale_170": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L170 | neighbors=[.networks()] | lang=en
- "scanner_scanner_base_rationale_175": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/scanner/scanner_base.py:L175 | neighbors=[.excludes()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-065.json

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
