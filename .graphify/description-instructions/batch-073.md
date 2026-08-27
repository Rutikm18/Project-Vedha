# Node Description Batch 74 of 236

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

- "login_route_setsessioncookies": "setSessionCookies()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L12 | neighbors=[route.ts, POST(), PUT()]
- "main_scripts_accuracy_main": "_main()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "main_scripts_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "main_scripts_accuracy_ratio": "_ratio()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "main_scripts_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "main_scripts_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "main_scripts_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "main_scripts_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L121 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…]
- "main_scripts_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L138 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string.]
- "main_scripts_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L296 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…]
- "main_scripts_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L53 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…]
- "main_scripts_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L308 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…]
- "main_scripts_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L91 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…]
- "main_scripts_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L98 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…]
- "main_scripts_findings_is_open": "_is_open()" | kind=code-symbol | source=probe/main_scripts/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "main_scripts_findings_summarize": "summarize()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1151 | neighbors=[findings.py, _main(), _tally()]
- "main_scripts_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L195 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…]
- "main_scripts_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L111 | neighbors=[host_discovery.py, parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "main_scripts_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()]
- "main_scripts_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "main_scripts_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "main_scripts_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "main_scripts_ja4s_compute_ja4s": "compute_ja4s()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L115 | neighbors=[ja4s.py, ja4s_from_parsed(), Do one standard TLS handshake and compu…]
- "main_scripts_ja4s_ext_types": "_ext_types()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L65 | neighbors=[ja4s.py, _walk_extensions(), ja4s_from_parsed()]
- "main_scripts_ja4s_ja4s_from_serverhello": "ja4s_from_serverhello()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L109 | neighbors=[ja4s.py, ja4s_from_parsed(), JA4S from raw ServerHello record bytes …]
- "main_scripts_ja4x_hash_oids": "_hash_oids()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L68 | neighbors=[ja4x.py, oid_to_hex(), ja4x_from_oid_lists()]
- "main_scripts_ja4x_ja4x_from_der": "ja4x_from_der()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L93 | neighbors=[ja4x.py, ja4x_from_cert(), JA4X from raw DER bytes. `cryptography`…]
- "main_scripts_ja4x_oid_to_hex": "oid_to_hex()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L39 | neighbors=[ja4x.py, _hash_oids(), DER-encode an OID's content octets and …]
- "main_scripts_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan()]
- "main_scripts_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…]
- "main_scripts_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "main_scripts_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L212 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "main_scripts_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "main_scripts_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "main_scripts_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]
- "main_scripts_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…]
- "main_scripts_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…]
- "main_scripts_os_fingerprint_accept_echo_reply": "accept_echo_reply()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L137 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), True only for an ICMP ECHO reply that a…]
- "main_scripts_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L66 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-073.json

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
