# Node Description Batch 25 of 332

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

- "main_scripts_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 8f6bf49 Refactor code structure and rem…, build_connection_request(), main(), parse_connection_confirm()]
- "main_scripts_smb_scanner_ntlm_os_build": "ntlm_os_build()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L337 | neighbors=[smb_scanner.py, build_ntlmssp_negotiate(), _netbios_session(), parse_ntlm_challenge(), _recv_smb_frame(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "main_scripts_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _fetch(), main()]
- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[agent_recommendation.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, TimestampMixin, Per-engagement SIEM + EDR connection se…, Base, TimestampMixin]
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()]
- "portal_timestamp_timestamp": "Timestamp()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L79 | neighbors=[page.tsx, page.tsx, page.tsx, Timestamp.tsx, formatCompact(), formatExact()]
- "remediation_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, backend.ts, backend(), BackendError]
- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig]
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus]
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus]
- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L222 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_agents_bootstrap_agent": "bootstrap_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L630 | neighbors=[agents.py, AgentRegisterResponse, Allows a probe to register without an a…, Allows a probe to register without an a…, Allows a probe to register without an a…, Allows a probe to register without an a…]
- "runtimeerror": "RuntimeError" | kind=code-symbol | neighbors=[LeaseLostError, HWBindError, AgentUnavailableError, LLMUnavailableError, StartupAbortError, PassiveListenerError]
- "scanner_accuracy": "accuracy.py" | kind=code-symbol | source=probe/scanner/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "scanner_dns_scanner_dnsscanner": "DNSScanner" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L88 | neighbors=[dns_scanner.py, BaseScanner, ._axfr(), ._chaos_txt(), ._dnssec_present(), .__init__()]
- "scanner_nfs_scanner_nfsscanner": "NFSScanner" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L187 | neighbors=[nfs_scanner.py, BaseScanner, .__init__(), ._mount_export(), ._portmap_dump(), ._portmap_getport()]
- "scanner_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L224 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), match_stack_signature(), ._icmp_scan_target(), ._tcp_ttl_result()]
- "scanner_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/scanner/port_scanner.py:L339 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._is_ambiguous()]
- "scanner_printer_scanner": "printer_scanner.py" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_ipp_get_printer_attributes(), _ipp_attr(), main(), parse_ipp_make_model(), parse_pjl_id()]
- "scanner_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L817 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…]
- "scanner_smb_scanner_ntlm_os_build": "ntlm_os_build()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L337 | neighbors=[smb_scanner.py, build_ntlmssp_negotiate(), _netbios_session(), parse_ntlm_challenge(), _recv_smb_frame(), _smb2_negotiate()]
- "services_job_result_service_process_job_result": "process_job_result()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L172 | neighbors=[job_result_service.py, _promote_assets(), result_checksum(), sanitize_jsonb(), validate_result_scope(), Process a scan job result.  Called from…]
- "services_job_result_service_promote_assets": "_promote_assets()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L456 | neighbors=[job_result_service.py, process_job_result(), _apply_device_profile(), Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…]
- "services_llm_managerllmservice_dispatch": "._dispatch()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L292 | neighbors=[ManagerLlmService, AiRuntimeError, ._anthropic(), ._ollama(), ._openai(), ._openrouter()]
- "services_sla": "sla.py" | kind=code-symbol | source=manager/backend/app/services/sla.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, c5ebd38 feat(sla): per-tenant custom SL…, config.py, compute(), default_windows(), SlaResult]
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET]
- "states_datastate_datastate": "DataState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L108 | neighbors=[DashboardGrid.tsx, page.tsx, page.tsx, page.tsx, page.tsx, page.tsx]
- "summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, backend.ts, backend()]
- "tests_engagement_adapters_test": "engagement-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/engagement-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7a637eb feat: network VA accuracy, KEV …, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, adapters.ts]
- "tests_test_accuracy_gate_write": "_write()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L25 | neighbors=[test_accuracy_gate.py, .test_corpus_without_any_labels_is_reje…, .test_corpus_without_facts_is_rejected(), .test_ground_truth_states_alone_is_a_va…, .test_unknown_provenance_is_rejected(), .test_unlabeled_provenance_is_rejected()]
- "tests_test_agent_dispatch": "test_agent_dispatch.py" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, _claim_fixture(), TestAgentWebSocketAuthentication]
- "tests_test_agent_identity": "test_agent_identity.py" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, agent.py, engine.py, transport.py, _cached_transport()]
- "tests_test_agents_redis": "_redis()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L26 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_agents_testpromoteassets": "TestPromoteAssets" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L701 | neighbors=[test_agents.py, Discovery results → assets/services pro…, .test_creates_asset_and_services_with_c…, .test_dedupes_duplicate_services_in_sam…, .test_empty_result_is_noop(), .test_skips_host_without_ip()]
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard]
- "tests_test_ai_normalizer_testproposecandidates": "TestProposeCandidates" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L153 | neighbors=[test_ai_normalizer.py, .test_ai_assisted_flag_set_on_candidate…, .test_cache_hit_bypasses_client(), .test_client_failure_returns_empty(), .test_malformed_response_missing_produc…, .test_malformed_response_not_a_list_ret…]
- "tests_test_attack_path_correlation_get": "_get()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L19 | neighbors=[test_attack_path_correlation.py, test_cleartext_cluster_needs_two(), test_device_role_from_facts_also_amplif…, test_exposed_db_with_unauth_is_critical…, test_legacy_windows_smbv1_plus_rdp(), test_ntlm_relay_high_when_smbv1_also_en…]
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, .test_run_without_connection_returns_em…, .test_run_write_noop_without_connection…, .test_sync_to_neo4j_noop_without_client…, PathAnalyzer, GraphBuilder]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-024.json

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
