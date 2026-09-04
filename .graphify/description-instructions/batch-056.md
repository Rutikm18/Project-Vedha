# Node Description Batch 57 of 332

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

- "main_scripts_findings_corr_user_enum_plus_weak_auth": "_corr_user_enum_plus_weak_auth()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1175 | neighbors=[findings.py, _by_target(), Finding, A disclosed user list (SMB null session…, A disclosed user list (SMB null session…]
- "main_scripts_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=probe/main_scripts/findings.py:L340 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()]
- "main_scripts_findings_rule_os_identification": "_rule_os_identification()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1010 | neighbors=[findings.py, Fuse OS signals across scanners into ON…, _data(), Finding, _scanner()]
- "main_scripts_findings_summarize": "summarize()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1279 | neighbors=[findings.py, _main(), Roll up findings for the finding sectio…, _finding_row(), _tally()]
- "main_scripts_ftp_scanner_ftpscanner_read_response": "._read_response()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L69 | neighbors=[FTPScanner, ._cmd(), ._list_bounded(), ._probe(), Read one (possibly multi-line) FTP repl…]
- "main_scripts_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L239 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …, Best-effort device classification from …]
- "main_scripts_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L516 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…]
- "main_scripts_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L222 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…]
- "main_scripts_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L208 | neighbors=[host_discovery.py, parse_nbstat(), parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…, Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "main_scripts_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L362 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line(), Bulk {ip: normalized_mac} snapshot of t…, Bulk {ip: normalized_mac} snapshot of t…]
- "main_scripts_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L445 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…, Surveys a target for IoT/embedded devic…]
- "main_scripts_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L271 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding., MQTT variable-length encoding.]
- "main_scripts_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L283 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…, MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "main_scripts_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L156 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…, Extract PTR target names from mDNS resp…]
- "main_scripts_ipv6_discovery_read_neighbor_cache": "_read_neighbor_cache()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L112 | neighbors=[ipv6_discovery.py, discover_ipv6_hosts(), parse_ip_neigh6(), parse_ndp(), _run()]
- "main_scripts_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…]
- "main_scripts_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "main_scripts_nfs_scanner_nfsscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L232 | neighbors=[NFSScanner, ._mount_export(), ._portmap_dump(), ._portmap_getport(), Blocking: portmap DUMP + mountd EXPORT.…]
- "main_scripts_nfs_scanner_nfsscanner_rpc": "._rpc()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L194 | neighbors=[NFSScanner, ._mount_export(), ._portmap_dump(), ._portmap_getport(), _rpc_call()]
- "main_scripts_nfs_scanner_parse_portmap_dump": "parse_portmap_dump()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L82 | neighbors=[nfs_scanner.py, ._portmap_dump(), _XDR, .u32(), Parse a PMAPPROC_DUMP reply — the list …]
- "main_scripts_nfs_scanner_rpc_call": "_rpc_call()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L124 | neighbors=[nfs_scanner.py, ._rpc(), Send one ONC-RPC CALL (AUTH_NULL) over …, _parse_rpc_reply(), _recv_record()]
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_scan_target": "._icmp_scan_target()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L493 | neighbors=[OSFingerprintScanner, fingerprint_os(), ._tcp_ttl_result(), remote_clock(), .scan_target()]
- "main_scripts_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L94 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), _strip_ip_header(), Parse an ICMP reply. Handles both raw-s…, Parse an ICMP reply. Handles both raw-s…]
- "main_scripts_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…]
- "main_scripts_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), .__init__(), RuntimeError, All passive sources failed before the l…]
- "main_scripts_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L213 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…]
- "main_scripts_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L293 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics, Ports recorded more than once (a port m…, Ports recorded more than once (a port m…, Ports recorded more than once (a port m…]
- "main_scripts_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L286 | neighbors=[Requested ports that were never recorde…, ScanMetrics, Requested ports that were never recorde…, Requested ports that were never recorde…, Requested ports that were never recorde…]
- "main_scripts_printer_scanner_printerscanner_probe_ipp": "._probe_ipp()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L115 | neighbors=[PrinterScanner, ._probe(), build_ipp_get_printer_attributes(), parse_ipp_make_model(), _recv_bounded()]
- "main_scripts_rdp_scanner_parse_connection_confirm": "parse_connection_confirm()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L56 | neighbors=[rdp_scanner.py, _posture_from_selected(), probe_rdp(), Parse a Connection Confirm. Returns Non…, Parse a Connection Confirm. Returns Non…]
- "main_scripts_rsync_scanner_handshake": "_handshake()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L73 | neighbors=[rsync_scanner.py, _recv_until(), Read the @RSYNCD greeting and echo it b…, ._list_modules(), ._test_anon()]
- "main_scripts_rsync_scanner_rsyncscanner_list_modules": "._list_modules()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L100 | neighbors=[RsyncScanner, _handshake(), parse_modules(), _recv_until(), ._probe()]
- "main_scripts_rsync_scanner_rsyncscanner_test_anon": "._test_anon()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L113 | neighbors=[Select a module without a secret: OK =>…, RsyncScanner, ._probe(), _handshake(), _recv_until()]
- "main_scripts_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L268 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…, Wire the funnel with the package's real…, Wire the funnel with the package's real…]
- "main_scripts_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L117 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host(), The port set worth scanning = union of …, Map a host's open ports onto the deep-s…]
- "main_scripts_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L103 | neighbors=[scan_funnel.py, The full outcome of funnelling one host., .run_host(), The full outcome of funnelling one host., Canonical open-TCP set for a host = ded…]
- "main_scripts_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L85 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host(), Map a host's open ports onto the deep-s…, Map a host's open ports onto the deep-s…]
- "main_scripts_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L848 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…]
- "main_scripts_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L989 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "main_scripts_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L235 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …, Map a connect()/socket-time OSError to …, Map a connect()/socket-time OSError to …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-056.json

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
