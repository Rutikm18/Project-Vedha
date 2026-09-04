# Node Description Batch 60 of 332

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

- "scanner_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L156 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…, Extract PTR target names from mDNS resp…]
- "scanner_ipv6_discovery_read_neighbor_cache": "_read_neighbor_cache()" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L112 | neighbors=[ipv6_discovery.py, discover_ipv6_hosts(), parse_ip_neigh6(), parse_ndp(), _run()]
- "scanner_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=probe/scanner/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…]
- "scanner_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…, Parse masscan -oJ output robustly: hand…, _run_masscan()]
- "scanner_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "scanner_nfs_scanner_nfsscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L232 | neighbors=[NFSScanner, ._mount_export(), ._portmap_dump(), ._portmap_getport(), Blocking: portmap DUMP + mountd EXPORT.…]
- "scanner_nfs_scanner_nfsscanner_rpc": "._rpc()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L194 | neighbors=[NFSScanner, ._mount_export(), ._portmap_dump(), ._portmap_getport(), _rpc_call()]
- "scanner_nfs_scanner_parse_portmap_dump": "parse_portmap_dump()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L82 | neighbors=[nfs_scanner.py, ._portmap_dump(), _XDR, .u32(), Parse a PMAPPROC_DUMP reply — the list …]
- "scanner_nfs_scanner_rpc_call": "_rpc_call()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L124 | neighbors=[nfs_scanner.py, ._rpc(), Send one ONC-RPC CALL (AUTH_NULL) over …, _parse_rpc_reply(), _recv_record()]
- "scanner_os_fingerprint_icmp_supported": "icmp_supported()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L320 | neighbors=[os_fingerprint.py, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_scan_target": "._icmp_scan_target()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L493 | neighbors=[OSFingerprintScanner, fingerprint_os(), ._tcp_ttl_result(), remote_clock(), .scan_target()]
- "scanner_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L94 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), _strip_ip_header(), Parse an ICMP reply. Handles both raw-s…, Parse an ICMP reply. Handles both raw-s…]
- "scanner_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…, Best-effort device label from an announ…]
- "scanner_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…, Await readability on any listener witho…]
- "scanner_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/scanner/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), RuntimeError, .__init__(), All passive sources failed before the l…]
- "scanner_port_scanner_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L126 | neighbors=[port_scanner.py, ._attempt(), Map a connect()-time OSError to (state,…, ._scan_port(), Map a connect()-time OSError to (state,…]
- "scanner_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L213 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…]
- "scanner_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L293 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics, Ports recorded more than once (a port m…, Ports recorded more than once (a port m…, Ports recorded more than once (a port m…]
- "scanner_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L286 | neighbors=[Requested ports that were never recorde…, ScanMetrics, Requested ports that were never recorde…, Requested ports that were never recorde…, Requested ports that were never recorde…]
- "scanner_printer_scanner_printerscanner_probe_ipp": "._probe_ipp()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L115 | neighbors=[PrinterScanner, ._probe(), build_ipp_get_printer_attributes(), parse_ipp_make_model(), _recv_bounded()]
- "scanner_rdp_scanner_parse_connection_confirm": "parse_connection_confirm()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L56 | neighbors=[rdp_scanner.py, _posture_from_selected(), probe_rdp(), Parse a Connection Confirm. Returns Non…, Parse a Connection Confirm. Returns Non…]
- "scanner_rsync_scanner_handshake": "_handshake()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L73 | neighbors=[rsync_scanner.py, _recv_until(), Read the @RSYNCD greeting and echo it b…, ._list_modules(), ._test_anon()]
- "scanner_rsync_scanner_rsyncscanner_list_modules": "._list_modules()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L100 | neighbors=[RsyncScanner, _handshake(), parse_modules(), _recv_until(), ._probe()]
- "scanner_rsync_scanner_rsyncscanner_test_anon": "._test_anon()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L113 | neighbors=[Select a module without a secret: OK =>…, RsyncScanner, ._probe(), _handshake(), _recv_until()]
- "scanner_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L268 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…, Wire the funnel with the package's real…, Wire the funnel with the package's real…]
- "scanner_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L117 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host(), The port set worth scanning = union of …, Map a host's open ports onto the deep-s…]
- "scanner_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L103 | neighbors=[scan_funnel.py, The full outcome of funnelling one host., .run_host(), The full outcome of funnelling one host., Canonical open-TCP set for a host = ded…]
- "scanner_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L85 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host(), Map a host's open ports onto the deep-s…, Map a host's open ports onto the deep-s…]
- "scanner_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L989 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "scanner_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L235 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …, Map a connect()/socket-time OSError to …, Map a connect()/socket-time OSError to …]
- "scanner_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L251 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…, Full, debuggable classification for att…, Full, debuggable classification for att…]
- "scanner_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L448 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…]
- "scanner_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/service_enum.py:L494 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target(), Connect to one port and read whatever i…]
- "scanner_smb_enum_scanner_decode": "_decode()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L212 | neighbors=[smb_enum_scanner.py, _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _safe()]
- "scanner_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "scanner_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "scanner_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "scanner_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]
- "scanner_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-059.json

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
