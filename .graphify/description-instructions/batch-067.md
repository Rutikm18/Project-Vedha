# Node Description Batch 68 of 380

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

- "scanner_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L251 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…, Full, debuggable classification for att…, Full, debuggable classification for att…]
- "scanner_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L448 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…]
- "scanner_scanner_base_raise_fd_limit": "raise_fd_limit()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1066 | neighbors=[scanner_base.py, get_fd_limit(), Raise the soft fd limit toward the hard…, safe_connect_concurrency(), Raise the soft fd limit toward the hard…]
- "scanner_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/service_enum.py:L494 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target(), Connect to one port and read whatever i…]
- "scanner_smb_enum_scanner_decode": "_decode()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L212 | neighbors=[smb_enum_scanner.py, _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _safe()]
- "scanner_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "scanner_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "scanner_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "scanner_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]
- "scanner_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()]
- "scanner_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()]
- "scanner_ssh_scanner_cursor": "_Cursor" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L72 | neighbors=[ssh_scanner.py, .__init__(), .read(), .read_name_list(), parse_kexinit()]
- "scanner_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L178 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "scanner_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L63 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()]
- "scanner_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L137 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "scanner_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L242 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "scanner_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L185 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "scanner_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L283 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L313 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L295 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe(), Acquire the concurrency gate (adaptive …, Acquire the concurrency gate (adaptive …]
- "scanner_va_campaign_progressreporter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L174 | neighbors=[ProgressReporter, _monotonic(), _now(), ._flush(), StageState]
- "scanner_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …]
- "schemas_ai_aiproviderstatus": "AiProviderStatus" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L38 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_ai_aistatusresponse": "AiStatusResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L48 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetIn, AssetOut, BulkAssetImportResult, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_asset_assetin": "AssetIn" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L9 | neighbors=[asset.py, BaseModel, .validate_ip(), AssetCriticality, AssetType]
- "schemas_common": "common.py" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ErrorDetail, paginate(), PaginatedResponse, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_engagement_engagementout": "EngagementOut" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L92 | neighbors=[engagement.py, EngagementDetail, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_finding_findingfilter": "FindingFilter" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L15 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L112 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slaitem": "SlaItem" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L92 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slasummary": "SlaSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L102 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_log_warn": "log_warn()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L85 | neighbors=[seed_admin.py, _detect_drift(), _log(), _seed_with_retry(), _validate_env()]
- "scripts_seed_admin_main": "main()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L331 | neighbors=[seed_admin.py, log_error(), log_info(), _seed_with_retry(), _validate_env()]
- "services_agent_policy_evaluate_action": "evaluate_action()" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L86 | neighbors=[agent_policy.py, classify_action(), Decision, _deny(), Decide whether `action` may proceed und…]
- "services_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, compute_exposure(), _sev(), Exposure analytics — protocol risk + zo…, 2885afa Add comprehensive probe testing…]
- "services_evidence_summary_summarize_evidence": "summarize_evidence()" | kind=code-symbol | source=manager/backend/app/services/evidence_summary.py:L118 | neighbors=[evidence_summary.py, Return a short, ordered, human-readable…, _enrichment_facts(), _format_value(), _sentence_case()]
- "services_finding_ai_generate_content_overrides": "generate_content_overrides()" | kind=code-symbol | source=manager/backend/app/services/finding_ai.py:L110 | neighbors=[finding_ai.py, _build_prompt(), _extract_json(), _validate(), Return an AI-authored ``content_overrid…]
- "services_finding_content_exploitation_signals": "exploitation_signals()" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L258 | neighbors=[finding_content.py, _evidence(), _float_or_none(), finding_content(), Extract the raw exploitation signals fr…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-067.json

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
