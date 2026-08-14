# Node Description Batch 45 of 186

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

- "main_scripts_iot_scanner_iotscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L450 | neighbors=[IoTScanner, _probe_cwmp(), _probe_mqtt(), _probe_rtsp()]
- "main_scripts_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L269 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding.]
- "main_scripts_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L281 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "main_scripts_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L155 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…]
- "main_scripts_iot_scanner_probe_mqtt": "_probe_mqtt()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L289 | neighbors=[iot_scanner.py, .scan_target(), _mqtt_connect(), _mqtt_subscribe_all()]
- "main_scripts_ja4x_ja4x_from_cert": "ja4x_from_cert()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L82 | neighbors=[ja4x.py, ja4x_from_oid_lists(), ja4x_from_der(), JA4X from a `cryptography` x509 Certifi…]
- "main_scripts_ja4x_ja4x_from_oid_lists": "ja4x_from_oid_lists()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L75 | neighbors=[ja4x.py, ja4x_from_cert(), _hash_oids(), Pure JA4X from the three ordered OID li…]
- "main_scripts_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed()]
- "main_scripts_mobile_scanner_build_adb_cnxn": "_build_adb_cnxn()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L59 | neighbors=[mobile_scanner.py, _adb_checksum(), _probe_adb(), Build an ADB A_CNXN (CONNECT) message —…]
- "main_scripts_mobile_scanner_mobilescanner": "MobileScanner" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L278 | neighbors=[mobile_scanner.py, BaseScanner, .scan_target(), Detects mobile device exposure on the n…]
- "main_scripts_mobile_scanner_probe_mdns_mobile_sync": "_probe_mdns_mobile_sync()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L257 | neighbors=[mobile_scanner.py, _build_mdns_query(), _parse_mdns_ptr_names(), Send one mDNS PTR query to target:5353 …]
- "main_scripts_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…]
- "main_scripts_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…]
- "main_scripts_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L366 | neighbors=[PortScanner, ScanMetrics, .summary(), Bounded worker-pool scan of every reque…]
- "main_scripts_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L45 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log()]
- "main_scripts_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L676 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "main_scripts_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L176 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "main_scripts_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L269 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "main_scripts_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L170 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]
- "main_scripts_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L128 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), One probe-ladder rung on its own connec…]
- "main_scripts_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "main_scripts_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "main_scripts_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "main_scripts_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "main_scripts_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "main_scripts_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L99 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "main_scripts_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L133 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie()]
- "main_scripts_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L140 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie()]
- "main_scripts_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "main_scripts_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "main_scripts_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "main_scripts_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L184 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "main_scripts_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "main_scripts_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L155 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni()]
- "main_scripts_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, DetectionRun, detection_run.py — one execution of the…, 2885afa Add comprehensive probe testing…]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder — production-gr…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-044.json

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
