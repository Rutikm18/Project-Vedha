# Node Description Batch 144 of 209

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

- "main_scripts_ja4s_rationale_70": "The single ALPN protocol the server chose (b'' if none)." | kind=entity | source=probe/main_scripts/ja4s.py:L70 | neighbors=[_selected_alpn()] | lang=en
- "main_scripts_ja4s_rationale_87": "Pure JA4S from already-extracted ServerHello fields." | kind=entity | source=probe/main_scripts/ja4s.py:L87 | neighbors=[ja4s_from_fields()] | lang=en
- "main_scripts_ja4x_rationale_118": "Return a threat-intel label if this JA4X is a known-suspicious fingerprint," | kind=entity | source=probe/main_scripts/ja4x.py:L118 | neighbors=[match_suspicious()] | lang=en
- "main_scripts_ja4x_rationale_40": "DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040" | kind=entity | source=probe/main_scripts/ja4x.py:L40 | neighbors=[oid_to_hex()] | lang=en
- "main_scripts_ja4x_rationale_77": "Pure JA4X from the three ordered OID lists (dotted-decimal strings)." | kind=entity | source=probe/main_scripts/ja4x.py:L77 | neighbors=[ja4x_from_oid_lists()] | lang=en
- "main_scripts_ja4x_rationale_83": "JA4X from a `cryptography` x509 Certificate object. None if unusable." | kind=entity | source=probe/main_scripts/ja4x.py:L83 | neighbors=[ja4x_from_cert()] | lang=en
- "main_scripts_ja4x_rationale_94": "JA4X from raw DER bytes. `cryptography` is imported lazily so this module     st" | kind=entity | source=probe/main_scripts/ja4x.py:L94 | neighbors=[ja4x_from_der()] | lang=en
- "main_scripts_mass_scan_connectsweep_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L209 | neighbors=[_ConnectSweep] | lang=en
- "main_scripts_mass_scan_main": "main()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L341 | neighbors=[mass_scan.py] | lang=en
- "main_scripts_mass_scan_rationale_1": "mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con" | kind=entity | source=probe/main_scripts/mass_scan.py:L1 | neighbors=[mass_scan.py] | lang=en
- "main_scripts_mass_scan_rationale_148": "Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin" | kind=entity | source=probe/main_scripts/mass_scan.py:L148 | neighbors=[_parse_masscan_json()] | lang=en
- "main_scripts_mass_scan_rationale_243": "target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them." | kind=entity | source=probe/main_scripts/mass_scan.py:L243 | neighbors=[run_mass_scan()] | lang=en
- "main_scripts_mass_scan_rationale_308": "Excluded networks -> masscan --exclude specs, so they get ZERO packets." | kind=entity | source=probe/main_scripts/mass_scan.py:L308 | neighbors=[_masscan_excludes()] | lang=en
- "main_scripts_mass_scan_rationale_313": "A CIDR spec is in scope only if it is fully contained in an allowed network." | kind=entity | source=probe/main_scripts/mass_scan.py:L313 | neighbors=[_spec_in_scope()] | lang=en
- "main_scripts_mass_scan_rationale_66": "Run masscan over the given target specs and return its parsed JSON records." | kind=entity | source=probe/main_scripts/mass_scan.py:L66 | neighbors=[_run_masscan()] | lang=en
- "main_scripts_mcp_ai_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L322 | neighbors=[mcp_ai_scanner.py] | lang=en
- "main_scripts_mcp_ai_scanner_mcpaiscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L201 | neighbors=[MCPAIScanner] | lang=en
- "main_scripts_mcp_ai_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L110 | neighbors=[_NoRedirect] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_1": "mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH" | kind=entity | source=probe/main_scripts/mcp_ai_scanner.py:L1 | neighbors=[mcp_ai_scanner.py] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_152": "Server/body fingerprint match against known non-AI squatters, or None." | kind=entity | source=probe/main_scripts/mcp_ai_scanner.py:L152 | neighbors=[_known_false_positive()] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_161": "The strongest possible evidence for a real MCP server: a WWW-Authenticate     he" | kind=entity | source=probe/main_scripts/mcp_ai_scanner.py:L161 | neighbors=[_mcp_oauth_signal()] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_174": "JSON-typed body that actually talks about auth, not just any error text." | kind=entity | source=probe/main_scripts/mcp_ai_scanner.py:L174 | neighbors=[_auth_shaped_json_body()] | lang=en
- "main_scripts_mcp_ai_scanner_request": "_request()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L127 | neighbors=[mcp_ai_scanner.py] | lang=en
- "main_scripts_mobile_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L340 | neighbors=[mobile_scanner.py] | lang=en
- "main_scripts_mobile_scanner_rationale_1": "mobile_scanner.py — mobile device exposure detection.  Covers playbook 13 (Mobil" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L1 | neighbors=[mobile_scanner.py] | lang=en
- "main_scripts_mobile_scanner_rationale_152": "Attempt TCP connect to lockdownd port 62078.     Port open = iOS device present" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L152 | neighbors=[_probe_lockdownd()] | lang=en
- "main_scripts_mobile_scanner_rationale_188": "Build a DNS PTR query in mDNS wire format with QU bit set." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L188 | neighbors=[_build_mdns_query()] | lang=en
- "main_scripts_mobile_scanner_rationale_199": "Extract PTR target names (service instance names) from mDNS reply." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L199 | neighbors=[_parse_mdns_ptr_names()] | lang=en
- "main_scripts_mobile_scanner_rationale_259": "Send one mDNS PTR query to target:5353 and return instance names." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L259 | neighbors=[_probe_mdns_mobile_sync()] | lang=en
- "main_scripts_mobile_scanner_rationale_279": "Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L279 | neighbors=[MobileScanner] | lang=en
- "main_scripts_mobile_scanner_rationale_60": "Build an ADB A_CNXN (CONNECT) message — the standard handshake initiator." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L60 | neighbors=[_build_adb_cnxn()] | lang=en
- "main_scripts_mobile_scanner_rationale_71": "Parse a 24-byte ADB message header.  Returns parsed fields or None." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L71 | neighbors=[_parse_adb_header()] | lang=pt
- "main_scripts_mobile_scanner_rationale_96": "Send ADB CNXN and read the device's CNXN reply.     Returns a dict with connecti" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L96 | neighbors=[_probe_adb()] | lang=en
- "main_scripts_nmap_wrapper_have_nmap": "_have_nmap()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L111 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_main": "main()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L239 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_nmapexecutionerror_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L45 | neighbors=[NmapExecutionError] | lang=en
- "main_scripts_nmap_wrapper_rationale_1": "nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:" | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L1 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_rationale_183": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L183 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_rationale_43": "Actionable subprocess failure; never reinterpret it as zero findings." | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L43 | neighbors=[NmapExecutionError] | lang=en
- "main_scripts_nmap_wrapper_rationale_70": "Allow tuning only; target, script, and output controls stay owned here." | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L70 | neighbors=[_validated_extra_args()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-143.json

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
