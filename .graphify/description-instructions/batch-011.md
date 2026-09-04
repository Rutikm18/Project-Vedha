# Node Description Batch 12 of 330

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

- "detection_edr_edrdetection": "EDRDetection" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L31 | neighbors=[edr.py, .parse_response(), .is_prevented(), .parse_response(), .parse_response(), AttackAction]
- "detection_engine_cpe_normalizer": "cpe_normalizer.py" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, d0d1931 feat(detection): NVD/CPE vuln f…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, all_osv_source_packages(), clean_debian_version()]
- "engine_scan_modules": "scan-modules.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L1 | neighbors=[interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, defaultModules(), depthDefaults(), moduleById(), ModuleCategory]
- "exploit_msf_client_metasploitrpcerror": "MetasploitRPCError" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L23 | neighbors=[msf_client.py, ._call(), .connect(), ._raw_call(), .run_module(), Exception]
- "lib_security_context": "security-context.ts" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L1 | neighbors=[route.ts, route.ts, 1fe16c8 stable but some dead code, need…, route.ts, adapters.ts, toUiFinding()]
- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …]
- "main_scripts_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…]
- "models_llm_output_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L12 | neighbors=[llm_output.py, Base, TimestampMixin, Every LLM generation is persisted here …, LLMReportGenerator, LLMUnavailableError]
- "routers_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _all_paths_to_critical(), _asset_labels(), attack_graph()]
- "scanner_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 37fa611 harden(scanner): XML-entity gua…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _have_nmap(), main()]
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 37376de hardening(scanner): OPSEC de-si…, 7a637eb feat: network VA accuracy, KEV …, bce780a feat(probe): enumerate HTTP met…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…]
- "scope_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/scope/page.tsx:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, portal-client.ts, portalApi(), PortalScan]
- "services_posture": "posture.py" | kind=code-symbol | source=manager/backend/app/services/posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 237a831 feat(posture): add run comparis…, 5238865 feat(posture): add pure scoring…, aggregate(), build_posture(), _clamp01()]
- "tests_test_ad_assessment_testasreproastchecker": "TestASREPRoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L215 | neighbors=[test_ad_assessment.py, .setup_method(), .test_finding_shape(), .test_get_no_preauth_accounts(), .test_no_finding_when_empty(), .test_request_asrep_without_impacket()]
- "tests_test_ad_assessment_testntlmrelaychecker": "TestNTLMRelayChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L247 | neighbors=[test_ad_assessment.py, .setup_method(), .test_finding_for_ldap_signing_only(), .test_finding_includes_ntlmrelayx_comma…, .test_no_finding_when_all_secure(), .test_smb_signing_without_impacket_mark…]
- "tests_test_detection_core_testallosvsourcepackages": "TestAllOsvSourcePackages" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1062 | neighbors=[test_detection_core.py, .test_returns_list(), .test_sorted(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testclassifyconfidence": "TestClassifyConfidence" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L208 | neighbors=[test_detection_core.py, .test_authoritative_scanners(), .test_inferred_scanners(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testfindingpostinit": "TestFindingPostInit" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L119 | neighbors=[test_detection_core.py, .test_accepts_nonempty_evidence_refs(), .test_refuses_zero_evidence_refs(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testisip": "TestIsIp" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L218 | neighbors=[test_detection_core.py, .test_hostname(), .test_valid_ipv4(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testkevdb": "TestKevDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L907 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_is_kev(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testnormalize": "TestNormalize" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1029 | neighbors=[test_detection_core.py, .test_dispatches_banner(), .test_unknown_scanner_returns_empty(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testnormalizebanner": "TestNormalizeBanner" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L982 | neighbors=[test_detection_core.py, .test_empty_banner(), .test_ssh_banner(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testproductfromcpe": "TestProductFromCpe" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L621 | neighbors=[test_detection_core.py, .test_extracts_product(), .test_short_cpe_returns_cpe(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_exploit_engine_testmetasploitrpcclient": "TestMetasploitRPCClient" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L181 | neighbors=[test_exploit_engine.py, ._make_client(), .test_call_without_connect_raises(), .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit()]
- "tests_test_exploit_engine_testrequiresapproval": "TestRequiresApproval" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L153 | neighbors=[test_exploit_engine.py, .test_adcs_server(), .test_critical_asset_needs_approval(), .test_dc02_pattern(), .test_dc_hostname_needs_approval(), .test_exchange_server()]
- "tests_test_integration": "test_integration.py" | kind=code-symbol | source=probe/tests/test_integration.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, result_spool.py, scope_crypt.py, scope_validator.py, task_runner.py, transport.py]
- "tests_test_ipv6_wiring": "test_ipv6_wiring.py" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, scanner_base.py, _run(), test_component_is_in_the_catalog(), test_disabled_by_default()]
- "tests_test_main_scripts_findings_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L19 | neighbors=[test_main_scripts_findings.py, test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_ntp_monlist_and_dns_open_recursion…, test_open_filtered_never_raises_exposur…]
- "tests_test_new_scanners_testsnmpberutilities": "TestSNMPBerUtilities" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L24 | neighbors=[test_new_scanners.py, .test_ber_len_long_form_one_byte(), .test_ber_len_long_form_two_bytes(), .test_ber_len_short_form(), .test_ber_parse_empty(), .test_ber_parse_two_tlvs()]
- "tests_test_pipeline_empty_epss": "_empty_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L36 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_pipeline_empty_kev": "_empty_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L32 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_risk_port_coverage": "test_risk_port_coverage.py" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _port_intel(), _risk_ports(), _swept_by_network_va(), test_branch_tables_still_contribute()]
- "tests_test_router_signals": "test_router_signals.py" | kind=code-symbol | source=probe/tests/test_router_signals.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, scanner_base.py, web_scanner.py, _open(), test_https_on_odd_port_routes_tls_and_w…]
- "tests_test_scan_funnel_make_funnel": "_make_funnel()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L66 | neighbors=[test_scan_funnel.py, FakeDiscovery, FakePortScanner, _scope(), Build a funnel with fakes; return (funn…, .test_db_scanner_invoked_with_db_port()]
- "agent_agent_say": "say()" | kind=code-symbol | source=probe/agent/agent.py:L86 | neighbors=[agent.py, _check_anti_debug(), _enroll_device(), _flush_spool_over_http(), _load_or_create_identity(), main()]
- "agent_transport_transport_update_state": ".update_state()" | kind=code-symbol | source=probe/agent/transport.py:L271 | neighbors=[Merge and atomically persist private st…, Transport, .activate_enrollment(), .clear_state(), .refresh_device_access_ex(), .refresh_registration()]
- "auth_exceptions": "exceptions.py" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L1 | neighbors=[AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError]
- "campaign_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/campaign/page.tsx:L1 | neighbors=[ago(), CampaignListPage(), CampaignSummary, EngagementSummary, fetchJson(), PageShell.tsx]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1d5ae943f799b5d9bba43f41c366d70ed4c00b1a": "1d5ae94 feat(fleet): live \"Connected probes\" status section" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@25c014d75e19e4bf82d8f4033426ad02425be6f8": "25c014d feat: enhance campaign progress tracking and add raw facts inspection- …" | kind=Commit | source=git | neighbors=[addcapabilities-fable, main, ui-ux-backend-updates0109, 6bb51ab feat: add detection-explain end…, FleetJobs.tsx, page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-011.json

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
