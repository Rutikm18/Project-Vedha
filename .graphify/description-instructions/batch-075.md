# Node Description Batch 76 of 227

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

- "routers_validation_default_check_kind": "_default_check_kind()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L88 | neighbors=[validation.py, create_validation_request(), Pick a safe check for the finding. TLS …]
- "routers_validation_get_request_or_404": "_get_request_or_404()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L115 | neighbors=[validation.py, approve_validation(), reject_validation()]
- "routers_validation_validationrequestout": "ValidationRequestOut" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L63 | neighbors=[validation.py, _request_out(), BaseModel]
- "routers_vuln_scans_finish_cancelled_nuclei_job": "_finish_cancelled_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L516 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "routers_vuln_scans_set_nuclei_job_state": "_set_nuclei_job_state()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L493 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "scanner_accuracy_main": "_main()" | kind=code-symbol | source=probe/scanner/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "scanner_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=probe/scanner/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "scanner_accuracy_ratio": "_ratio()" | kind=code-symbol | source=probe/scanner/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "scanner_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, AdaptiveTimeout, from_rtts()]
- "scanner_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "scanner_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "scanner_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "scanner_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L121 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…]
- "scanner_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L138 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string.]
- "scanner_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L296 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…]
- "scanner_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L53 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…]
- "scanner_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L308 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…]
- "scanner_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L91 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…]
- "scanner_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L98 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…]
- "scanner_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L201 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…]
- "scanner_findings_is_open": "_is_open()" | kind=code-symbol | source=probe/scanner/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "scanner_findings_load_facts_jsonl": "load_facts_jsonl()" | kind=code-symbol | source=probe/scanner/findings.py:L668 | neighbors=[findings.py, _main(), Read a scanner's JSONL output into fact…]
- "scanner_findings_summarize": "summarize()" | kind=code-symbol | source=probe/scanner/findings.py:L648 | neighbors=[findings.py, _main(), _tally()]
- "scanner_host_discovery_hostdiscoveryscanner_arp_table": "._arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L177 | neighbors=[HostDiscoveryScanner, read_arp_table(), .scan_target()]
- "scanner_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/scanner/host_discovery.py:L195 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…]
- "scanner_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()]
- "scanner_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "scanner_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "scanner_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "scanner_ja4s_compute_ja4s": "compute_ja4s()" | kind=code-symbol | source=probe/scanner/ja4s.py:L115 | neighbors=[ja4s.py, ja4s_from_parsed(), Do one standard TLS handshake and compu…]
- "scanner_ja4s_ext_types": "_ext_types()" | kind=code-symbol | source=probe/scanner/ja4s.py:L65 | neighbors=[ja4s.py, _walk_extensions(), ja4s_from_parsed()]
- "scanner_ja4s_ja4s_from_serverhello": "ja4s_from_serverhello()" | kind=code-symbol | source=probe/scanner/ja4s.py:L109 | neighbors=[ja4s.py, ja4s_from_parsed(), JA4S from raw ServerHello record bytes …]
- "scanner_ja4x_hash_oids": "_hash_oids()" | kind=code-symbol | source=probe/scanner/ja4x.py:L68 | neighbors=[ja4x.py, oid_to_hex(), ja4x_from_oid_lists()]
- "scanner_ja4x_ja4x_from_der": "ja4x_from_der()" | kind=code-symbol | source=probe/scanner/ja4x.py:L93 | neighbors=[ja4x.py, ja4x_from_cert(), JA4X from raw DER bytes. `cryptography`…]
- "scanner_ja4x_oid_to_hex": "oid_to_hex()" | kind=code-symbol | source=probe/scanner/ja4x.py:L39 | neighbors=[ja4x.py, _hash_oids(), DER-encode an OID's content octets and …]
- "scanner_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L212 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "scanner_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "scanner_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "scanner_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-075.json

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
