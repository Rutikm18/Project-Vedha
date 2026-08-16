# Node Description Batch 67 of 209

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "main_scripts_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L211 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "main_scripts_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "main_scripts_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "main_scripts_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]
- "main_scripts_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…]
- "main_scripts_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…]
- "main_scripts_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L64 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()]
- "main_scripts_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L111 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()]
- "main_scripts_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L204 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), Return (socket, is_raw). Prefer datagra…]
- "main_scripts_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L79 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), Parse an ICMP reply. Handles both raw-s…]
- "main_scripts_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…]
- "main_scripts_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …]
- "main_scripts_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L128 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…]
- "main_scripts_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L208 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics, Ports recorded more than once (a port m…]
- "main_scripts_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L201 | neighbors=[Requested ports that were never recorde…, ScanMetrics, Requested ports that were never recorde…]
- "main_scripts_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L182 | neighbors=[Tally exactly one terminal per-port obs…, ScanMetrics, Tally exactly one terminal per-port obs…]
- "main_scripts_rdp_scanner_build_connection_request": "build_connection_request()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L41 | neighbors=[rdp_scanner.py, probe_rdp(), TPKT + X.224 Connection Request carryin…]
- "main_scripts_rdp_scanner_parse_connection_confirm": "parse_connection_confirm()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L55 | neighbors=[rdp_scanner.py, probe_rdp(), Parse a Connection Confirm. Returns Non…]
- "main_scripts_run_all_log": "_log()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L38 | neighbors=[run_all.py, main(), _run_stage()]
- "main_scripts_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L204 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…]
- "main_scripts_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L86 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host()]
- "main_scripts_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L72 | neighbors=[scan_funnel.py, The full outcome of funnelling one host., .run_host()]
- "main_scripts_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L54 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host()]
- "main_scripts_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L82 | neighbors=[scan_funnel.py, .scan_target(), Protocol]
- "main_scripts_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L547 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…]
- "main_scripts_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L98 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …]
- "main_scripts_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L114 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…]
- "main_scripts_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L399 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()]
- "main_scripts_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L749 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…]
- "main_scripts_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L302 | neighbors=[.acquire(), .run(), RateLimiter]
- "main_scripts_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L637 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "main_scripts_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L628 | neighbors=[.run(), ResultWriter, .to_json()]
- "main_scripts_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L205 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "main_scripts_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L253 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "main_scripts_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target()]
- "main_scripts_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "main_scripts_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]
- "main_scripts_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "main_scripts_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L124 | neighbors=[syn_scanner.py, parse_packet(), Walk a TCP options field for the MSS va…]
- "main_scripts_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L411 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-066.json

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
