# Node Description Batch 23 of 92

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

- "main_scripts_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=main_scripts/service_enum.py:L465 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target()]
- "main_scripts_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "main_scripts_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "main_scripts_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "main_scripts_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "main_scripts_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L118 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "main_scripts_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L151 | neighbors=[syn_scanner.py, _parse_mss(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking()]
- "main_scripts_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L190 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie()]
- "main_scripts_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L197 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie()]
- "main_scripts_tls_scanner_sni": "_sni()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "main_scripts_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L155 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni()]
- "main_scripts_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=main_scripts/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "runtimeerror": "RuntimeError" | kind=code-symbol | neighbors=[LeaseLostError, HWBindError, PassiveListenerError, PassiveListenerError]
- "scanner_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=scanner/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "scanner_delta_scanner_delta": "Delta" | kind=code-symbol | source=scanner/delta_scanner.py:L69 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…]
- "scanner_device_classifier": "device_classifier.py" | kind=code-symbol | source=scanner/device_classifier.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…]
- "scanner_findings_as_dict": "_as_dict()" | kind=code-symbol | source=scanner/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "scanner_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=scanner/findings.py:L254 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=scanner/findings.py:L277 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_ssh": "_rule_ssh()" | kind=code-symbol | source=scanner/findings.py:L564 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls": "_rule_tls()" | kind=code-symbol | source=scanner/findings.py:L175 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_udp_amplification": "_rule_udp_amplification()" | kind=code-symbol | source=scanner/findings.py:L308 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_web": "_rule_web()" | kind=code-symbol | source=scanner/findings.py:L419 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=scanner/host_discovery.py:L142 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …]
- "scanner_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=scanner/host_discovery.py:L125 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…]
- "scanner_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=scanner/iot_scanner.py:L445 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…]
- "scanner_iot_scanner_iotscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/iot_scanner.py:L452 | neighbors=[IoTScanner, _probe_cwmp(), _probe_mqtt(), _probe_rtsp()]
- "scanner_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=scanner/iot_scanner.py:L271 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding.]
- "scanner_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=scanner/iot_scanner.py:L283 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "scanner_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=scanner/iot_scanner.py:L156 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…]
- "scanner_iot_scanner_probe_mqtt": "_probe_mqtt()" | kind=code-symbol | source=scanner/iot_scanner.py:L291 | neighbors=[iot_scanner.py, .scan_target(), _mqtt_connect(), _mqtt_subscribe_all()]
- "scanner_ja4s_selected_alpn": "_selected_alpn()" | kind=code-symbol | source=scanner/ja4s.py:L69 | neighbors=[ja4s.py, ja4s_from_parsed(), The single ALPN protocol the server cho…, _walk_extensions()]
- "scanner_ja4s_walk_extensions": "_walk_extensions()" | kind=code-symbol | source=scanner/ja4s.py:L56 | neighbors=[ja4s.py, _ext_types(), Yield (type, value) for each extension …, _selected_alpn()]
- "scanner_ja4x_ja4x_from_cert": "ja4x_from_cert()" | kind=code-symbol | source=scanner/ja4x.py:L82 | neighbors=[ja4x.py, ja4x_from_oid_lists(), ja4x_from_der(), JA4X from a `cryptography` x509 Certifi…]
- "scanner_ja4x_ja4x_from_oid_lists": "ja4x_from_oid_lists()" | kind=code-symbol | source=scanner/ja4x.py:L75 | neighbors=[ja4x.py, ja4x_from_cert(), _hash_oids(), Pure JA4X from the three ordered OID li…]
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=scanner/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed()]
- "scanner_mobile_scanner_build_adb_cnxn": "_build_adb_cnxn()" | kind=code-symbol | source=scanner/mobile_scanner.py:L59 | neighbors=[mobile_scanner.py, _adb_checksum(), _probe_adb(), Build an ADB A_CNXN (CONNECT) message —…]
- "scanner_mobile_scanner_mobilescanner": "MobileScanner" | kind=code-symbol | source=scanner/mobile_scanner.py:L278 | neighbors=[mobile_scanner.py, BaseScanner, .scan_target(), Detects mobile device exposure on the n…]
- "scanner_mobile_scanner_probe_mdns_mobile_sync": "_probe_mdns_mobile_sync()" | kind=code-symbol | source=scanner/mobile_scanner.py:L257 | neighbors=[mobile_scanner.py, _build_mdns_query(), _parse_mdns_ptr_names(), Send one mDNS PTR query to target:5353 …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-022.json

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
