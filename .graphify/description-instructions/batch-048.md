# Node Description Batch 49 of 336

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

- "scanner_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L421 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…]
- "scanner_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L416 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard, Read-only view of allowed networks (for…, Read-only view of allowed networks (for…, Read-only view of allowed networks (for…, Map a connect()/socket-time OSError to …]
- "scanner_scanner_base_sendpacer": "SendPacer" | kind=code-symbol | source=probe/scanner/scanner_base.py:L535 | neighbors=[scanner_base.py, Blocking packets-per-second pacer with …, .__init__(), .observe_round(), .pace(), .stats()]
- "scanner_scanner_registry": "scanner_registry.py" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, info(), is_verified(), ScannerInfo, verification_report(), scanner_registry.py — the single source…]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L426 | neighbors=[ServiceBannerScanner, match_service(), parse_http_head(), ._ladder_for(), ._rung(), .scan_target()]
- "scanner_service_enum_serviceenumscanner": "ServiceEnumScanner" | kind=code-symbol | source=probe/scanner/service_enum.py:L478 | neighbors=[service_enum.py, BaseScanner, .__init__(), ._open(), ._probe_port(), .scan_target()]
- "scanner_smb_enum_scanner_smbenumscanner": "SMBEnumScanner" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L218 | neighbors=[smb_enum_scanner.py, BaseScanner, ._enumerate(), .__init__(), ._scan_port(), .scan_target()]
- "scanner_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L273 | neighbors=[smb_scanner.py, ntlm_os_build(), _align8(), _encryption_context(), _preauth_integrity_context(), .scan_target()]
- "scanner_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L362 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), ._ntlm_fingerprint(), .scan_target()]
- "scanner_smtp_scanner_smtpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L87 | neighbors=[Blocking: greeting → EHLO → STARTTLS/VR…, SMTPScanner, parse_ehlo_capabilities(), ._cmd(), ._read_response(), vrfy_leaks()]
- "scanner_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community(), ._query()]
- "scanner_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "scanner_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]
- "scanner_ssh_scanner_parse_kexinit": "parse_kexinit()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L106 | neighbors=[ssh_scanner.py, _Cursor, .read(), .read_name_list(), Parse a SSH_MSG_KEXINIT body into its n…, ._scan_port()]
- "scanner_ssh_scanner_sshscanner": "SSHScanner" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L242 | neighbors=[ssh_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_ssh_scanner_sshscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L279 | neighbors=[SSHScanner, _dedup(), evaluate_algorithms(), parse_kexinit(), parse_ssh_banner(), .scan_target()]
- "scanner_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L91 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…]
- "scanner_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L115 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …]
- "scanner_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L213 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking(), SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…]
- "scanner_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L295 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking(), A genuine reply to our SYN acknowledges…, Outbound-interface IP for reaching dst_…, Outbound-interface IP for reaching dst_…]
- "scanner_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L176 | neighbors=[syn_scanner.py, parse_tcp_options(), Back-compat shim: MSS only. New code us…, parse_packet(), Walk a TCP options field for the MSS va…, Walk a TCP options field for the MSS va…]
- "scanner_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L273 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__(), True only when a real SYN scan can work…, True only when a real SYN scan can work…, True only when a real SYN scan can work…]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L274 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version(), Never send an IP literal as SNI — non-c…, Never send an IP literal as SNI — non-c…]
- "scanner_va_campaign_vacampaign": "VACampaign" | kind=code-symbol | source=probe/scanner/va_campaign.py:L290 | neighbors=[va_campaign.py, build_campaign(), Runs the ordered stages sequentially, e…, .__init__(), ._refresh_totals(), .run()]
- "scanner_va_campaign_vacampaign_run": ".run()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L301 | neighbors=[run_campaign(), VACampaign, .finish(), .mark(), .snapshot(), ._refresh_totals()]
- "scanner_vnc_scanner_vncscanner": "VNCScanner" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L101 | neighbors=[vnc_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_vnc_scanner_vncscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L108 | neighbors=[Blocking: RFB version handshake + read …, VNCScanner, classify_security_types(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "scanner_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/scanner/web_scanner.py:L136 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), ._schemes_for()]
- "scanner_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "schemas_ai_aigeneraterequest": "AiGenerateRequest" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L18 | neighbors=[ai.py, BaseModel, .validate_bounded_input(), AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_finding_findingout": "FindingOut" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L121 | neighbors=[finding.py, BaseModel, ._populate_risk_rank(), DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_remediation": "remediation.py" | kind=code-symbol | source=manager/backend/app/schemas/remediation.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, RemediationPlanDetailOut, RemediationPlanOut, RemediationStepOut]
- "scripts_seed_admin_seed_with_retry": "_seed_with_retry()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L294 | neighbors=[seed_admin.py, main(), Exponential-backoff retry for transient…, log_error(), log_warn(), _seed_once()]
- "services_llm_managerllmservice_runtime": "._runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L155 | neighbors=[ManagerLlmService, ._fallback_candidates(), .generate(), AiRuntimeError, _is_local_ollama_model(), Runtime]
- "services_scope_crypto": "scope_crypto.py" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt…, 2885afa Add comprehensive probe testing…]
- "services_sla_compute": "compute()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L60 | neighbors=[sla.py, SlaResult, _windows(), Compute the SLA state for one finding. …, summarize(), Compute the SLA state for one finding. …]
- "states_datastate_errorstate": "ErrorState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L52 | neighbors=[ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, DataState.tsx]
- "supporting_research_test_evidence_store_openssh_below": "openssh_below()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L54 | neighbors=[test_evidence_store.py, demo(), .test_a_brand_new_rule_answers_against_…, .test_current_state_comes_from_latest_e…, .test_remediation_is_verified_by_eviden…, .test_time_travel_recovers_the_historic…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-048.json

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
