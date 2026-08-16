# Node Description Batch 66 of 209

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
- "main_scripts_findings_summarize": "summarize()" | kind=code-symbol | source=probe/main_scripts/findings.py:L648 | neighbors=[findings.py, _main(), _tally()]
- "main_scripts_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L395 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…]
- "main_scripts_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L195 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…]
- "main_scripts_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L111 | neighbors=[host_discovery.py, parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "main_scripts_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L260 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line()]
- "main_scripts_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()]
- "main_scripts_iot_scanner_coap_get_wellknown_core": "_coap_get_wellknown_core()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L346 | neighbors=[iot_scanner.py, _probe_coap_sync(), CoAP Confirmable GET for /.well-known/c…]
- "main_scripts_iot_scanner_decode_mdns_name": "_decode_mdns_name()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L129 | neighbors=[iot_scanner.py, _parse_mdns_response(), Decode a DNS wire-format name, followin…]
- "main_scripts_iot_scanner_fetch_upnp_root_desc": "_fetch_upnp_root_desc()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L57 | neighbors=[iot_scanner.py, _probe_ssdp_sync(), HTTP GET the UPnP rootDesc.xml and extr…]
- "main_scripts_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L257 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "main_scripts_iot_scanner_parse_coap_response": "_parse_coap_response()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L359 | neighbors=[iot_scanner.py, _probe_coap_sync(), Extract CoAP response code and content.]
- "main_scripts_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L381 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "main_scripts_iot_scanner_probe_cwmp": "_probe_cwmp()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L403 | neighbors=[iot_scanner.py, .scan_target(), HTTP GET to CWMP port — detect ACS or C…]
- "main_scripts_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L89 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
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
- "main_scripts_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L173 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…]
- "main_scripts_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L151 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…]
- "main_scripts_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L160 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-065.json

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
