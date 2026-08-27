# Node Description Batch 41 of 92

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

- "main_scripts_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L158 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…]
- "main_scripts_udp_scanner_ntp_monlist_probe": "_ntp_monlist_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L50 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L146 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…]
- "main_scripts_udp_scanner_tftp_probe": "_tftp_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L132 | neighbors=[udp_scanner.py, TFTP RRQ for a non-existent file.  Erro…]
- "main_scripts_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L376 | neighbors=[UDPScanner, ._probe()]
- "main_scripts_unauth_access_as_text": "_as_text()" | kind=code-symbol | source=main_scripts/unauth_access.py:L40 | neighbors=[unauth_access.py, classify_unauth_access()]
- "main_scripts_vantage_matrix_is_external": "_is_external()" | kind=code-symbol | source=main_scripts/vantage_matrix.py:L34 | neighbors=[vantage_matrix.py, reconcile_vantages()]
- "main_scripts_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=main_scripts/web_scanner.py:L78 | neighbors=[web_scanner.py, parse_allow_header()]
- "main_scripts_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=main_scripts/web_scanner.py:L143 | neighbors=[WebScanner, .scan_target()]
- "main_scripts_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/web_scanner.py:L160 | neighbors=[WebScanner, ._scan_port()]
- "main_scripts_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=main_scripts/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "main_scripts_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=main_scripts/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=main_scripts/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=main_scripts/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=main_scripts/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=main_scripts/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "oserror": "OSError" | kind=code-symbol | neighbors=[NmapExecutionError, NmapExecutionError]
- "protocol": "Protocol" | kind=code-symbol | neighbors=[_Scanner, _Scanner]
- "scanner_accuracy_expected_keys": "_expected_keys()" | kind=code-symbol | source=scanner/accuracy.py:L37 | neighbors=[accuracy.py, score_findings()]
- "scanner_accuracy_finding_key": "_finding_key()" | kind=code-symbol | source=scanner/accuracy.py:L31 | neighbors=[accuracy.py, score_findings()]
- "scanner_accuracy_format_report": "format_report()" | kind=code-symbol | source=scanner/accuracy.py:L145 | neighbors=[accuracy.py, _main()]
- "scanner_adaptive_timeout_adaptivetimeout_timeout": ".timeout()" | kind=code-symbol | source=scanner/adaptive_timeout.py:L44 | neighbors=[AdaptiveTimeout, Current timeout: base until we have a s…]
- "scanner_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=scanner/db_scanner.py:L247 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/db_scanner.py:L281 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_probe_redis": "_probe_redis()" | kind=code-symbol | source=scanner/db_scanner.py:L114 | neighbors=[db_scanner.py, interpret_redis_info()]
- "scanner_delta_scanner_delta_to_dict": ".to_dict()" | kind=code-symbol | source=scanner/delta_scanner.py:L85 | neighbors=[Delta, main()]
- "scanner_delta_scanner_deltaengine_summary": ".summary()" | kind=code-symbol | source=scanner/delta_scanner.py:L288 | neighbors=[DeltaEngine, main()]
- "scanner_findings_finding_to_dict": ".to_dict()" | kind=code-symbol | source=scanner/findings.py:L78 | neighbors=[Finding, _main()]
- "scanner_findings_rationale_844": "VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo" | kind=entity | source=scanner/findings.py:L844 | neighbors=[_rule_vnc(), load_facts_jsonl()]
- "scanner_findings_rationale_903": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=scanner/findings.py:L903 | neighbors=[_corr_ntlm_relay(), run_findings()]
- "scanner_findings_tally": "_tally()" | kind=code-symbol | source=scanner/findings.py:L1187 | neighbors=[findings.py, summarize()]
- "scanner_host_discovery_now": "_now()" | kind=code-symbol | source=scanner/host_discovery.py:L293 | neighbors=[host_discovery.py, fuse_liveness()]
- "scanner_host_discovery_state_for_confidence": "_state_for_confidence()" | kind=code-symbol | source=scanner/host_discovery.py:L297 | neighbors=[host_discovery.py, fuse_liveness()]
- "scanner_host_discovery_vendor_for_mac": "vendor_for_mac()" | kind=code-symbol | source=scanner/host_discovery.py:L136 | neighbors=[host_discovery.py, .scan_target()]
- "scanner_iot_scanner_parse_ssdp_headers": "_parse_ssdp_headers()" | kind=code-symbol | source=scanner/iot_scanner.py:L49 | neighbors=[iot_scanner.py, _probe_ssdp_sync()]
- "scanner_iot_scanner_probe_mdns_sync": "_probe_mdns_sync()" | kind=code-symbol | source=scanner/iot_scanner.py:L190 | neighbors=[iot_scanner.py, _parse_mdns_response()]
- "scanner_iot_scanner_probe_rtsp": "_probe_rtsp()" | kind=code-symbol | source=scanner/iot_scanner.py:L216 | neighbors=[iot_scanner.py, .scan_target()]
- "scanner_ja4s_alpn_code": "_alpn_code()" | kind=code-symbol | source=scanner/ja4s.py:L78 | neighbors=[ja4s.py, ja4s_from_fields()]
- "scanner_ja4s_version_str": "_version_str()" | kind=code-symbol | source=scanner/ja4s.py:L52 | neighbors=[ja4s.py, ja4s_from_fields()]
- "scanner_ja4x_match_suspicious": "match_suspicious()" | kind=code-symbol | source=scanner/ja4x.py:L117 | neighbors=[ja4x.py, Return a threat-intel label if this JA4…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-040.json

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
