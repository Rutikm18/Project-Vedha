# Node Description Batch 245 of 332

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

- "scanner_mass_scan_main": "main()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L341 | neighbors=[mass_scan.py] | lang=en
- "scanner_mass_scan_rationale_1": "mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con" | kind=entity | source=probe/scanner/mass_scan.py:L1 | neighbors=[mass_scan.py] | lang=en
- "scanner_mass_scan_rationale_148": "Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin" | kind=entity | source=probe/scanner/mass_scan.py:L148 | neighbors=[_parse_masscan_json()] | lang=en
- "scanner_mass_scan_rationale_176": "target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them." | kind=entity | source=probe/scanner/mass_scan.py:L176 | neighbors=[run_mass_scan()] | lang=en
- "scanner_mass_scan_rationale_216": "Excluded networks -> masscan --exclude specs, so they get ZERO packets." | kind=entity | source=probe/scanner/mass_scan.py:L216 | neighbors=[_masscan_excludes()] | lang=en
- "scanner_mass_scan_rationale_221": "A CIDR spec is in scope only if it is fully contained in an allowed network." | kind=entity | source=probe/scanner/mass_scan.py:L221 | neighbors=[_spec_in_scope()] | lang=en
- "scanner_mass_scan_rationale_243": "target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them." | kind=entity | source=probe/scanner/mass_scan.py:L243 | neighbors=[run_mass_scan()] | lang=en
- "scanner_mass_scan_rationale_308": "Excluded networks -> masscan --exclude specs, so they get ZERO packets." | kind=entity | source=probe/scanner/mass_scan.py:L308 | neighbors=[_masscan_excludes()] | lang=en
- "scanner_mass_scan_rationale_313": "A CIDR spec is in scope only if it is fully contained in an allowed network." | kind=entity | source=probe/scanner/mass_scan.py:L313 | neighbors=[_spec_in_scope()] | lang=en
- "scanner_mass_scan_rationale_55": "Run masscan over the given target specs and return its parsed JSON records." | kind=entity | source=probe/scanner/mass_scan.py:L55 | neighbors=[_run_masscan()] | lang=en
- "scanner_mass_scan_rationale_66": "Run masscan over the given target specs and return its parsed JSON records." | kind=entity | source=probe/scanner/mass_scan.py:L66 | neighbors=[_run_masscan()] | lang=en
- "scanner_mass_scan_rationale_90": "Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin" | kind=entity | source=probe/scanner/mass_scan.py:L90 | neighbors=[_parse_masscan_json()] | lang=en
- "scanner_mcp_ai_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L323 | neighbors=[mcp_ai_scanner.py] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L202 | neighbors=[MCPAIScanner] | lang=en
- "scanner_mcp_ai_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L111 | neighbors=[_NoRedirect] | lang=en
- "scanner_mcp_ai_scanner_rationale_1": "mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH" | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[mcp_ai_scanner.py] | lang=en
- "scanner_mcp_ai_scanner_rationale_152": "Server/body fingerprint match against known non-AI squatters, or None." | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L152 | neighbors=[_known_false_positive()] | lang=en
- "scanner_mcp_ai_scanner_rationale_153": "Server/body fingerprint match against known non-AI squatters, or None." | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L153 | neighbors=[_known_false_positive()] | lang=en
- "scanner_mcp_ai_scanner_rationale_161": "The strongest possible evidence for a real MCP server: a WWW-Authenticate     he" | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L161 | neighbors=[_mcp_oauth_signal()] | lang=en
- "scanner_mcp_ai_scanner_rationale_162": "The strongest possible evidence for a real MCP server: a WWW-Authenticate     he" | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L162 | neighbors=[_mcp_oauth_signal()] | lang=en
- "scanner_mcp_ai_scanner_rationale_174": "JSON-typed body that actually talks about auth, not just any error text." | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L174 | neighbors=[_auth_shaped_json_body()] | lang=en
- "scanner_mcp_ai_scanner_rationale_175": "JSON-typed body that actually talks about auth, not just any error text." | kind=entity | source=probe/scanner/mcp_ai_scanner.py:L175 | neighbors=[_auth_shaped_json_body()] | lang=en
- "scanner_mcp_ai_scanner_request": "_request()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L128 | neighbors=[mcp_ai_scanner.py] | lang=en
- "scanner_mobile_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L340 | neighbors=[mobile_scanner.py] | lang=en
- "scanner_mobile_scanner_rationale_1": "mobile_scanner.py — mobile device exposure detection.  Covers playbook 13 (Mobil" | kind=entity | source=probe/scanner/mobile_scanner.py:L1 | neighbors=[mobile_scanner.py] | lang=en
- "scanner_mobile_scanner_rationale_152": "Attempt TCP connect to lockdownd port 62078.     Port open = iOS device present" | kind=entity | source=probe/scanner/mobile_scanner.py:L152 | neighbors=[_probe_lockdownd()] | lang=en
- "scanner_mobile_scanner_rationale_188": "Build a DNS PTR query in mDNS wire format with QU bit set." | kind=entity | source=probe/scanner/mobile_scanner.py:L188 | neighbors=[_build_mdns_query()] | lang=en
- "scanner_mobile_scanner_rationale_199": "Extract PTR target names (service instance names) from mDNS reply." | kind=entity | source=probe/scanner/mobile_scanner.py:L199 | neighbors=[_parse_mdns_ptr_names()] | lang=en
- "scanner_mobile_scanner_rationale_259": "Send one mDNS PTR query to target:5353 and return instance names." | kind=entity | source=probe/scanner/mobile_scanner.py:L259 | neighbors=[_probe_mdns_mobile_sync()] | lang=en
- "scanner_mobile_scanner_rationale_279": "Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO" | kind=entity | source=probe/scanner/mobile_scanner.py:L279 | neighbors=[MobileScanner] | lang=en
- "scanner_mobile_scanner_rationale_60": "Build an ADB A_CNXN (CONNECT) message — the standard handshake initiator." | kind=entity | source=probe/scanner/mobile_scanner.py:L60 | neighbors=[_build_adb_cnxn()] | lang=en
- "scanner_mobile_scanner_rationale_71": "Parse a 24-byte ADB message header.  Returns parsed fields or None." | kind=entity | source=probe/scanner/mobile_scanner.py:L71 | neighbors=[_parse_adb_header()] | lang=pt
- "scanner_mobile_scanner_rationale_96": "Send ADB CNXN and read the device's CNXN reply.     Returns a dict with connecti" | kind=entity | source=probe/scanner/mobile_scanner.py:L96 | neighbors=[_probe_adb()] | lang=en
- "scanner_msrpc_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L172 | neighbors=[msrpc_scanner.py] | lang=en
- "scanner_msrpc_scanner_msrpcscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L85 | neighbors=[MSRPCScanner] | lang=en
- "scanner_msrpc_scanner_rationale_1": "msrpc_scanner.py — MSRPC endpoint-mapper (EPM) enumeration over port 135 (VA che" | kind=entity | source=probe/scanner/msrpc_scanner.py:L1 | neighbors=[msrpc_scanner.py] | lang=it
- "scanner_msrpc_scanner_rationale_52": "Parse ncacn_ip_tcp bindings → (all_tcp_ports, dynamic_tcp_ports).      Pure and" | kind=entity | source=probe/scanner/msrpc_scanner.py:L52 | neighbors=[_extract_tcp_ports()] | lang=en
- "scanner_msrpc_scanner_rationale_70": "Reduce the raw endpoint list to distinct interfaces and dynamic ports." | kind=entity | source=probe/scanner/msrpc_scanner.py:L70 | neighbors=[_summarize()] | lang=en
- "scanner_msrpc_scanner_rationale_90": "Blocking: EPM ept_lookup via impacket. Monkeypatchable for tests." | kind=entity | source=probe/scanner/msrpc_scanner.py:L90 | neighbors=[._enumerate()] | lang=en
- "scanner_nfs_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L282 | neighbors=[nfs_scanner.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-244.json

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
