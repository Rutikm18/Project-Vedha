# Node Description Batch 104 of 236

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

- "scanner_accuracy_finding_key": "_finding_key()" | kind=code-symbol | source=probe/scanner/accuracy.py:L31 | neighbors=[accuracy.py, score_findings()]
- "scanner_accuracy_format_report": "format_report()" | kind=code-symbol | source=probe/scanner/accuracy.py:L145 | neighbors=[accuracy.py, _main()]
- "scanner_adaptive_timeout_adaptivetimeout_timeout": ".timeout()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L44 | neighbors=[AdaptiveTimeout, Current timeout: base until we have a s…]
- "scanner_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L247 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L281 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_probe_redis": "_probe_redis()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L114 | neighbors=[db_scanner.py, interpret_redis_info()]
- "scanner_delta_scanner_delta_to_dict": ".to_dict()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L85 | neighbors=[Delta, main()]
- "scanner_delta_scanner_deltaengine_summary": ".summary()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L288 | neighbors=[DeltaEngine, main()]
- "scanner_findings_finding_to_dict": ".to_dict()" | kind=code-symbol | source=probe/scanner/findings.py:L78 | neighbors=[Finding, _main()]
- "scanner_findings_tally": "_tally()" | kind=code-symbol | source=probe/scanner/findings.py:L1163 | neighbors=[findings.py, summarize()]
- "scanner_host_discovery_now": "_now()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L293 | neighbors=[host_discovery.py, fuse_liveness()]
- "scanner_host_discovery_state_for_confidence": "_state_for_confidence()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L297 | neighbors=[host_discovery.py, fuse_liveness()]
- "scanner_host_discovery_vendor_for_mac": "vendor_for_mac()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L136 | neighbors=[host_discovery.py, .scan_target()]
- "scanner_iot_scanner_parse_ssdp_headers": "_parse_ssdp_headers()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L49 | neighbors=[iot_scanner.py, _probe_ssdp_sync()]
- "scanner_iot_scanner_probe_mdns_sync": "_probe_mdns_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L190 | neighbors=[iot_scanner.py, _parse_mdns_response()]
- "scanner_iot_scanner_probe_rtsp": "_probe_rtsp()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L216 | neighbors=[iot_scanner.py, .scan_target()]
- "scanner_ja4s_alpn_code": "_alpn_code()" | kind=code-symbol | source=probe/scanner/ja4s.py:L78 | neighbors=[ja4s.py, ja4s_from_fields()]
- "scanner_ja4s_version_str": "_version_str()" | kind=code-symbol | source=probe/scanner/ja4s.py:L52 | neighbors=[ja4s.py, ja4s_from_fields()]
- "scanner_ja4x_match_suspicious": "match_suspicious()" | kind=code-symbol | source=probe/scanner/ja4x.py:L117 | neighbors=[ja4x.py, Return a threat-intel label if this JA4…]
- "scanner_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L213 | neighbors=[_ConnectSweep, .scan_target()]
- "scanner_mass_scan_connectsweep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L229 | neighbors=[_ConnectSweep, ._probe()]
- "scanner_mass_scan_have_masscan": "_have_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L60 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L184 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=probe/scanner/mass_scan.py:L51 | neighbors=[mass_scan.py, _run_masscan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L206 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L316 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L183 | neighbors=[mcp_ai_scanner.py, ._result()]
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L110 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "scanner_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()]
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L154 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L115 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_validated_extra_args": "_validated_extra_args()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L69 | neighbors=[nmap_wrapper.py, Allow tuning only; target, script, and …]
- "scanner_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()]
- "scanner_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "scanner_os_fingerprint_rationale_205": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/scanner/os_fingerprint.py:L205 | neighbors=[_open_icmp_socket(), OSFingerprintScanner]
- "scanner_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "scanner_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "scanner_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "scanner_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L232 | neighbors=[.scan_target(), ScanMetrics]
- "scanner_rdp_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L126 | neighbors=[rdp_scanner.py, RDPScanner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-103.json

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
