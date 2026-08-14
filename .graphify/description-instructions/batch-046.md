# Node Description Batch 47 of 186

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

- "routers_probe_enrollment_provision_agent_for_site": "_provision_agent_for_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L234 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request(), Bind a request to a Site policy and cre…]
- "routers_probe_enrollment_refresh_device_token": "refresh_device_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L564 | neighbors=[probe_enrollment.py, _rate_limit(), _secret_hash(), _verify_signature()]
- "routers_probe_enrollment_sitepolicyinput": "SitePolicyInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L147 | neighbors=[probe_enrollment.py, BaseModel, .require_site_reference(), .validate_networks()]
- "routers_probe_enrollment_verify_signature": "_verify_signature()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L87 | neighbors=[probe_enrollment.py, activate_enrollment(), refresh_device_token(), _decode_public_key()]
- "routers_validation_request_out": "_request_out()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L128 | neighbors=[validation.py, create_validation_request(), list_validation_requests(), ValidationRequestOut]
- "routers_validation_roe_allows_active_validation": "_roe_allows_active_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L81 | neighbors=[validation.py, approve_validation(), create_validation_request(), RoE gate: active validation is allowed …]
- "routers_vuln_scans_finish_failed_nuclei_job": "_finish_failed_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L525 | neighbors=[vuln_scans.py, _finish_cancelled_nuclei_job(), _set_nuclei_job_state(), _run_nuclei_and_save()]
- "scanner_delta_scanner_delta": "Delta" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L69 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…]
- "scanner_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L111 | neighbors=[host_discovery.py, parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…, Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "scanner_init": "__init__.py" | kind=code-symbol | source=probe/scanner/__init__.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, VA scanner module — pure collection/sca…, 298a9d4 trim frontend to 7 core pages; …]
- "scanner_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L443 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…]
- "scanner_iot_scanner_iotscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L450 | neighbors=[IoTScanner, _probe_cwmp(), _probe_mqtt(), _probe_rtsp()]
- "scanner_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L269 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding.]
- "scanner_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L281 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "scanner_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L155 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…]
- "scanner_iot_scanner_probe_mqtt": "_probe_mqtt()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L289 | neighbors=[iot_scanner.py, .scan_target(), _mqtt_connect(), _mqtt_subscribe_all()]
- "scanner_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan(), Excluded networks -> masscan --exclude …]
- "scanner_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan(), A CIDR spec is in scope only if it is f…]
- "scanner_mobile_scanner_build_adb_cnxn": "_build_adb_cnxn()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L59 | neighbors=[mobile_scanner.py, _adb_checksum(), _probe_adb(), Build an ADB A_CNXN (CONNECT) message —…]
- "scanner_mobile_scanner_mobilescanner": "MobileScanner" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L278 | neighbors=[mobile_scanner.py, BaseScanner, .scan_target(), Detects mobile device exposure on the n…]
- "scanner_mobile_scanner_probe_mdns_mobile_sync": "_probe_mdns_mobile_sync()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L257 | neighbors=[mobile_scanner.py, _build_mdns_query(), _parse_mdns_ptr_names(), Send one mDNS PTR query to target:5353 …]
- "scanner_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L204 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…]
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…, Open ONE recv-only UDP listener. Return…]
- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …, Pull short printable ASCII runs from a …]
- "scanner_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L89 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…]
- "scanner_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L276 | neighbors=[PortScanner, ._attempt(), ._maybe(), ._scan_port()]
- "scanner_port_scanner_portscanner_maybe": "._maybe()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L197 | neighbors=[PortScanner, ._build(), ._scan_port(), Emit a non-open result only when report…]
- "scanner_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L362 | neighbors=[AdaptiveRateController, Current integer window (>= min_window)., Current integer window (>= min_window)., Current integer window (>= min_window).]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L676 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L176 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L269 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L286 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…]
- "scanner_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L281 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard, Read-only view of allowed networks (for…, Read-only view of allowed networks (for…]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L170 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]
- "scanner_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/scanner/service_banner.py:L128 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), One probe-ladder rung on its own connec…]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "scanner_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "scanner_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-046.json

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
