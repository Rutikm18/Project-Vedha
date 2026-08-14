# Node Description Batch 37 of 186

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

- "routers_probe_enrollment_rate_limit": "_rate_limit()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L98 | neighbors=[probe_enrollment.py, activate_enrollment(), create_enrollment_request(), poll_enrollment(), refresh_device_token()]
- "routers_validation_create_validation_request": "create_validation_request()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L145 | neighbors=[validation.py, _default_check_kind(), _load_finding_and_eng(), _request_out(), _roe_allows_active_validation()]
- "run_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, POST(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "scanner_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L142 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …, Best-effort device classification from …]
- "scanner_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L304 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + neighbor signals into a c…]
- "scanner_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L125 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…]
- "scanner_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L260 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line(), ._arp_table(), Return {ip: normalized_mac} from the OS…]
- "scanner_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…, Parse masscan -oJ output robustly: hand…, _run_masscan()]
- "scanner_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "scanner_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L127 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), .scan_target(), Combine available stack signals into a …]
- "scanner_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L57 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…]
- "scanner_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L101 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), os_family_from_ttl(), Round the observed TTL up to the neares…]
- "scanner_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…, Best-effort device label from an announ…]
- "scanner_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…, Await readability on any listener witho…]
- "scanner_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/scanner/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), RuntimeError, .__init__(), All passive sources failed before the l…]
- "scanner_port_scanner_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L126 | neighbors=[port_scanner.py, ._attempt(), Map a connect()-time OSError to (state,…, ._scan_port(), Map a connect()-time OSError to (state,…]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L366 | neighbors=[PortScanner, ScanMetrics, .summary(), Bounded worker-pool scan of every reque…, ._scan_port()]
- "scanner_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L547 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…]
- "scanner_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L688 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L460 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…]
- "scanner_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/scanner/service_banner.py:L88 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…]
- "scanner_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L142 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]
- "scanner_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "scanner_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "scanner_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "scanner_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]
- "scanner_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()]
- "scanner_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()]
- "scanner_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L62 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()]
- "scanner_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L282 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L255 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/scanner/web_scanner.py:L135 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "schemas_ai_aiproviderstatus": "AiProviderStatus" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L37 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_ai_aistatusresponse": "AiStatusResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L47 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetIn, AssetOut, BulkAssetImportResult, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_asset_assetin": "AssetIn" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L9 | neighbors=[asset.py, BaseModel, .validate_ip(), AssetCriticality, AssetType]
- "schemas_common": "common.py" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ErrorDetail, paginate(), PaginatedResponse, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_engagement_engagementout": "EngagementOut" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L92 | neighbors=[engagement.py, EngagementDetail, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_finding_findingfilter": "FindingFilter" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L11 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-036.json

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
