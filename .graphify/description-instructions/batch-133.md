# Node Description Batch 134 of 332

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
Write every description in Portuguese (pt). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "main_scripts_ja4s_alpn_code": "_alpn_code()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L78 | neighbors=[ja4s.py, ja4s_from_fields()]
- "main_scripts_ja4s_version_str": "_version_str()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L52 | neighbors=[ja4s.py, ja4s_from_fields()]
- "main_scripts_ja4x_match_suspicious": "match_suspicious()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L117 | neighbors=[ja4x.py, Return a threat-intel label if this JA4…]
- "main_scripts_ldap_scanner_first": "_first()" | kind=code-symbol | source=probe/main_scripts/ldap_scanner.py:L40 | neighbors=[ldap_scanner.py, ._probe()]
- "main_scripts_ldap_scanner_ldapscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/ldap_scanner.py:L134 | neighbors=[LDAPScanner, .scan_target()]
- "main_scripts_ldap_scanner_ldapscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/ldap_scanner.py:L156 | neighbors=[LDAPScanner, ._scan_port()]
- "main_scripts_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L213 | neighbors=[_ConnectSweep, .scan_target()]
- "main_scripts_mass_scan_connectsweep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L229 | neighbors=[_ConnectSweep, ._probe()]
- "main_scripts_mass_scan_have_masscan": "_have_masscan()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L60 | neighbors=[mass_scan.py, run_mass_scan()]
- "main_scripts_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L184 | neighbors=[mass_scan.py, run_mass_scan()]
- "main_scripts_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L51 | neighbors=[mass_scan.py, _run_masscan()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L206 | neighbors=[MCPAIScanner, ._probe_port()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L316 | neighbors=[MCPAIScanner, ._probe_port()]
- "main_scripts_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L183 | neighbors=[mcp_ai_scanner.py, ._result()]
- "main_scripts_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L110 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "main_scripts_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()]
- "main_scripts_msrpc_scanner_msrpcscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L144 | neighbors=[MSRPCScanner, .scan_target()]
- "main_scripts_msrpc_scanner_msrpcscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L167 | neighbors=[MSRPCScanner, ._scan_port()]
- "main_scripts_nfs_scanner_nfsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L259 | neighbors=[NFSScanner, .scan_target()]
- "main_scripts_nfs_scanner_nfsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L277 | neighbors=[NFSScanner, ._scan_port()]
- "main_scripts_nfs_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L156 | neighbors=[nfs_scanner.py, _recv_record()]
- "main_scripts_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L160 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "main_scripts_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L121 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "main_scripts_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()]
- "main_scripts_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "main_scripts_os_fingerprint_rationale_205": "p0f-style match on (initial TTL, option layout, window scale) → a specific     s" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L205 | neighbors=[match_stack_signature(), _open_icmp_socket()]
- "main_scripts_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "main_scripts_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "main_scripts_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "main_scripts_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L416 | neighbors=[PortScanner, ._attempt()]
- "main_scripts_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L315 | neighbors=[.scan_target(), ScanMetrics]
- "main_scripts_printer_scanner_ipp_attr": "_ipp_attr()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L49 | neighbors=[printer_scanner.py, build_ipp_get_printer_attributes()]
- "main_scripts_printer_scanner_printerscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L138 | neighbors=[PrinterScanner, .scan_target()]
- "main_scripts_printer_scanner_printerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L155 | neighbors=[PrinterScanner, ._scan_port()]
- "main_scripts_rdp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L173 | neighbors=[rdp_scanner.py, RDPScanner]
- "main_scripts_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L142 | neighbors=[RDPScanner, .scan_target()]
- "main_scripts_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L168 | neighbors=[RDPScanner, ._scan_port()]
- "main_scripts_rsync_scanner_rsyncscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L144 | neighbors=[RsyncScanner, .scan_target()]
- "main_scripts_rsync_scanner_rsyncscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L162 | neighbors=[RsyncScanner, ._scan_port()]
- "main_scripts_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L92 | neighbors=[run_all.py, main()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-133.json

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
