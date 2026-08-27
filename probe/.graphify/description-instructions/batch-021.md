# Node Description Batch 22 of 92

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

- "main_scripts_findings_rule_udp_amplification": "_rule_udp_amplification()" | kind=code-symbol | source=main_scripts/findings.py:L308 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_web": "_rule_web()" | kind=code-symbol | source=main_scripts/findings.py:L419 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=main_scripts/host_discovery.py:L142 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …]
- "main_scripts_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=main_scripts/host_discovery.py:L125 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…]
- "main_scripts_iot_scanner_iotscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L452 | neighbors=[IoTScanner, _probe_cwmp(), _probe_mqtt(), _probe_rtsp()]
- "main_scripts_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L271 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding.]
- "main_scripts_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L283 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "main_scripts_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L156 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…]
- "main_scripts_iot_scanner_probe_mqtt": "_probe_mqtt()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L291 | neighbors=[iot_scanner.py, .scan_target(), _mqtt_connect(), _mqtt_subscribe_all()]
- "main_scripts_ja4s_selected_alpn": "_selected_alpn()" | kind=code-symbol | source=main_scripts/ja4s.py:L69 | neighbors=[ja4s.py, ja4s_from_parsed(), The single ALPN protocol the server cho…, _walk_extensions()]
- "main_scripts_ja4s_walk_extensions": "_walk_extensions()" | kind=code-symbol | source=main_scripts/ja4s.py:L56 | neighbors=[ja4s.py, _ext_types(), Yield (type, value) for each extension …, _selected_alpn()]
- "main_scripts_ja4x_ja4x_from_cert": "ja4x_from_cert()" | kind=code-symbol | source=main_scripts/ja4x.py:L82 | neighbors=[ja4x.py, ja4x_from_oid_lists(), ja4x_from_der(), JA4X from a `cryptography` x509 Certifi…]
- "main_scripts_ja4x_ja4x_from_oid_lists": "ja4x_from_oid_lists()" | kind=code-symbol | source=main_scripts/ja4x.py:L75 | neighbors=[ja4x.py, ja4x_from_cert(), _hash_oids(), Pure JA4X from the three ordered OID li…]
- "main_scripts_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=main_scripts/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed()]
- "main_scripts_mobile_scanner_build_adb_cnxn": "_build_adb_cnxn()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L59 | neighbors=[mobile_scanner.py, _adb_checksum(), _probe_adb(), Build an ADB A_CNXN (CONNECT) message —…]
- "main_scripts_mobile_scanner_probe_mdns_mobile_sync": "_probe_mdns_mobile_sync()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L257 | neighbors=[mobile_scanner.py, _build_mdns_query(), _parse_mdns_ptr_names(), Send one mDNS PTR query to target:5353 …]
- "main_scripts_nmap_wrapper_rationale_1": "nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:" | kind=entity | source=main_scripts/nmap_wrapper.py:L1 | neighbors=[nmap_wrapper.py, ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_nmap_wrapper_rationale_191": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=main_scripts/nmap_wrapper.py:L191 | neighbors=[nmap_wrapper.py, ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_nmap_wrapper_rationale_43": "Actionable subprocess failure; never reinterpret it as zero findings." | kind=entity | source=main_scripts/nmap_wrapper.py:L43 | neighbors=[NmapExecutionError, ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_nmap_wrapper_rationale_70": "Allow tuning only; target, script, and output controls stay owned here." | kind=entity | source=main_scripts/nmap_wrapper.py:L70 | neighbors=[_validated_extra_args(), ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L270 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), ._icmp_timestamp(), Return (socket, is_raw). Prefer datagra…]
- "main_scripts_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L94 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), _strip_ip_header(), Parse an ICMP reply. Handles both raw-s…]
- "main_scripts_os_fingerprint_parse_icmp_timestamps": "parse_icmp_timestamps()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L108 | neighbors=[os_fingerprint.py, ._icmp_timestamp(), _strip_ip_header(), Parse an ICMP timestamp reply (type 14)…]
- "main_scripts_os_fingerprint_strip_ip_header": "_strip_ip_header()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L81 | neighbors=[os_fingerprint.py, parse_icmp_reply(), parse_icmp_timestamps(), Return (ttl, icmp_bytes). Raw-socket de…]
- "main_scripts_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=main_scripts/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…]
- "main_scripts_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=main_scripts/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…]
- "main_scripts_passive_collector_rationale_1": "passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)." | kind=entity | source=main_scripts/passive_collector.py:L1 | neighbors=[passive_collector.py, ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_passive_collector_rationale_107": "All passive sources failed before the listen window could start." | kind=entity | source=main_scripts/passive_collector.py:L107 | neighbors=[PassiveListenerError, ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_passive_collector_rationale_120": "Open one recv-only UDP listener or raise the socket error.      Multicast groups" | kind=entity | source=main_scripts/passive_collector.py:L120 | neighbors=[_open_listener(), ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_passive_collector_rationale_211": "Listen-only discovery. No active probing. Reports in-scope hosts that     announ" | kind=entity | source=main_scripts/passive_collector.py:L211 | neighbors=[PassiveCollector, ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_passive_collector_rationale_332": "Await readability on any listener without blocking the event loop." | kind=entity | source=main_scripts/passive_collector.py:L332 | neighbors=[._select(), ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_passive_collector_rationale_74": "Pull short printable ASCII runs from a payload, for human-readable evidence." | kind=entity | source=main_scripts/passive_collector.py:L74 | neighbors=[_printable_strings(), ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_passive_collector_rationale_91": "Best-effort device label from an announcement payload (recv-only parsing)." | kind=entity | source=main_scripts/passive_collector.py:L91 | neighbors=[_device_hint(), ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/port_scanner.py:L404 | neighbors=[PortScanner, ScanMetrics, .summary(), Bounded worker-pool scan of every reque…]
- "main_scripts_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L83 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), One synchronous RDP handshake. Best-eff…]
- "main_scripts_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=main_scripts/scanner_base.py:L756 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "main_scripts_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=main_scripts/scanner_base.py:L247 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "main_scripts_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=main_scripts/scanner_base.py:L340 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "main_scripts_service_banner_match_service": "match_service()" | kind=code-symbol | source=main_scripts/service_banner.py:L91 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab()]
- "main_scripts_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=main_scripts/service_banner.py:L173 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-021.json

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
