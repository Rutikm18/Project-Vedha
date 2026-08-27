# Node Description Batch 37 of 236

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

- "scanner_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L142 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()]
- "scanner_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L627 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L531 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…]
- "scanner_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/scanner/service_banner.py:L91 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…, Soft-match collected bytes to {service,…]
- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/scanner/service_banner.py:L123 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), ._rung(), .scan_target()]
- "scanner_service_enum_serviceenumscanner": "ServiceEnumScanner" | kind=code-symbol | source=probe/scanner/service_enum.py:L449 | neighbors=[service_enum.py, BaseScanner, .__init__(), ._open(), ._probe_port(), .scan_target()]
- "scanner_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community(), ._query()]
- "scanner_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "scanner_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]
- "scanner_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L151 | neighbors=[syn_scanner.py, _parse_mss(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking(), Parse a raw IPv4+TCP packet (as receive…, Parse a raw IPv4+TCP packet (as receive…]
- "scanner_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L190 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie(), Keyed 32-bit ISN for (dst_ip, dst_port,…, Keyed 32-bit ISN for (dst_ip, dst_port,…]
- "scanner_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L197 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie(), A genuine reply to our SYN acknowledges…, A genuine reply to our SYN acknowledges…]
- "scanner_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L274 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L227 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version(), Never send an IP literal as SNI — non-c…, Never send an IP literal as SNI — non-c…]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L155 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni(), Attempt a handshake forcing one protoco…, Attempt a handshake forcing one protoco…]
- "scanner_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "schemas_ai_aigeneraterequest": "AiGenerateRequest" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L18 | neighbors=[ai.py, BaseModel, .validate_bounded_input(), AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_finding_findingout": "FindingOut" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L68 | neighbors=[finding.py, BaseModel, ._populate_risk_rank(), DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_seed_with_retry": "_seed_with_retry()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L294 | neighbors=[seed_admin.py, main(), Exponential-backoff retry for transient…, log_error(), log_warn(), _seed_once()]
- "services_job_result_service_validate_result_scope": "validate_result_scope()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L106 | neighbors=[job_result_service.py, process_job_result(), Return result identities outside the jo…, _identity_ip(), _result_network_identities(), Return result identities outside the jo…]
- "services_llm_managerllmservice_fallback_candidates": "._fallback_candidates()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L300 | neighbors=[ManagerLlmService, ._default_runtime(), ._runtime(), Runtime, .generate_with_fallback(), Ordered runtimes to try: requested/defa…]
- "services_llm_managerllmservice_runtime": "._runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L114 | neighbors=[ManagerLlmService, ._fallback_candidates(), .generate(), AiRuntimeError, _is_local_ollama_model(), Runtime]
- "services_scope_crypto": "scope_crypto.py" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt…, 2885afa Add comprehensive probe testing…]
- "services_sla_compute": "compute()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L60 | neighbors=[sla.py, SlaResult, _windows(), Compute the SLA state for one finding. …, summarize(), Compute the SLA state for one finding. …]
- "states_datastate_errorstate": "ErrorState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L52 | neighbors=[ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, DataState.tsx]
- "test_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/integrations/test/route.ts:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, backend.ts, backend(), with-backend.ts, withBackend(), POST]
- "tests_engagement_adapters_test": "engagement-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/engagement-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, adapters.ts, toApiEngagementCreate(), toApiEngagementPatch(), toApiFindingPatch(), toUiFinding()]
- "tests_test_agent_dispatch_testagentwebsocketauthentication": "TestAgentWebSocketAuthentication" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L16 | neighbors=[test_agent_dispatch.py, .test_accepts_bearer_header(), .test_rejects_query_string_credentials(), ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_dispatch_testjobsecretboundary": "TestJobSecretBoundary" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L67 | neighbors=[test_agent_dispatch.py, .test_allows_non_secret_scan_tuning(), .test_detects_persisted_secret_material…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_policy": "test_agent_policy.py" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, _roe(), TestClassifyAction, TestEvaluateAction, test_agent_policy.py — the pure determi…]
- "tests_test_agents_testgetagentjobs": "TestGetAgentJobs" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L298 | neighbors=[test_agents.py, .test_404_when_agent_unknown(), .test_jobs_include_params(), .test_skips_job_outside_declared_networ…, .test_skips_job_when_capability_is_miss…, ScanJobType]
- "tests_test_agents_testotprofilegate": "TestOTProfileGate" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L170 | neighbors=[test_agents.py, .test_allows_passive_discovery_on_ot_en…, .test_blocks_active_scan_type_on_ot_eng…, .test_blocks_explicit_active_scan_type_…, .test_it_and_iot_profiles_unaffected(), ScanJobType]
- "tests_test_agents_testregisteragent_test_agent_token_is_long_lived": ".test_agent_token_is_long_lived()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L683 | neighbors=[Agent token must outlive the 15-min acc…, TestRegisterAgent, _user(), Agent token must outlive the 15-min acc…, Agent token must outlive the 15-min acc…, Agent token must outlive the 15-min acc…]
- "tests_test_agents_testregisteragent_test_reuses_existing_probe_by_name": ".test_reuses_existing_probe_by_name()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L648 | neighbors=[Re-registering the same-named probe mus…, TestRegisterAgent, _user(), Re-registering the same-named probe mus…, Re-registering the same-named probe mus…, Re-registering the same-named probe mus…]
- "tests_test_ai_engine_asset": "_asset()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L36 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher(), .test_predict_priority_uses_fallback_wh…]
- "tests_test_ai_engine_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L170 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_ai_engine_rationale_1": "Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API" | kind=entity | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_db_scanner_testmysqlxvsoracle": "TestMysqlxVsOracle" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L53 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle(), .test_oracle_rejects_garbage_with_type_…, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]

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
