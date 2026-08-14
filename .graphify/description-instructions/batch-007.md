# Node Description Batch 8 of 186

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "auth_router": "router.py" | kind=code-symbol | source=manager/backend/app/auth/router.py:L1 | neighbors=[database.py, dependencies.py, ratelimit.py, _authenticate(), create_personal_access_token(), list_personal_access_tokens()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@30261ebec685fe061217d7e71faa08b5a4b6d5ea": "30261eb feat: enhance advisor flow with structured brief and probe selection- A…" | kind=Commit | source=git | neighbors=[AdvisorFlow.tsx, AssistantDrawer.tsx, feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a789cca150b7688941e2f9229631f493d3fab094": "a789cca scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, feat/coverage-gated-auto-resolution, integration/all-branches, main, spike/probe-go] | lang=pt
- "detection_siem_siemalert": "SIEMAlert" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L24 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response(), AttackAction, DetectionCorrelator] | lang=en
- "detection_sigma_sigmarulegenerator": "SigmaRuleGenerator" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L107 | neighbors=[sigma.py, ._customise_detection(), .generate_sigma_for_technique(), ._lookup_template(), AttackAction, DetectionCorrelator] | lang=en
- "discovery_service_id_servicefingerprint": "ServiceFingerprint" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L13 | neighbors=[service_id.py, .identify(), NucleiRunReport, NucleiScanError, NucleiScanner, NucleiScanner — async subprocess wrappe…] | lang=en
- "graph_analyzer_pathanalyzer": "PathAnalyzer" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L60 | neighbors=[analyzer.py, ._exploit_info(), .find_blast_radius(), .find_paths_to_target(), .identify_chokepoints(), .__init__()] | lang=en
- "lib_exploit_store": "exploit-store.ts" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest] | lang=en
- "main_scripts_findings_finding": "Finding" | kind=code-symbol | source=probe/main_scripts/findings.py:L63 | neighbors=[findings.py, _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay(), .to_dict(), One vulnerability finding, always backe…] | lang=en
- "models_attack_path_attackpath": "AttackPath" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L11 | neighbors=[attack_path.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…] | lang=en
- "models_detection_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/backend/app/models/detection.py:L12 | neighbors=[detection.py, Base, TimestampMixin, Base, TimestampMixin, DetectionStatus] | lang=en
- "native_port_scan": "port-scan.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, CheckOpts, checkPort(), expandTarget()] | lang=en
- "routers_engagements_engagementupdate": "EngagementUpdate" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L483 | neighbors=[engagements.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), Asset] | lang=en
- "routers_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 3c277ba feat(lifecycle): add POST /find…, 8ebc053 feat(risk-rank-ui): surface ver…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/scanner/passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, _coverage(), _device_hint(), _is_readable()] | lang=en
- "tests_test_ai_engine_testhallucinationguard": "TestHallucinationGuard" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L104 | neighbors=[test_ai_engine.py, .setup_method(), .test_cve_all_known_valid(), .test_cve_invention_flagged(), .test_cvss_match_passes(), .test_cvss_mismatch_flagged()] | lang=en
- "tests_test_attack_paths_testgraphbuilder": "TestGraphBuilder" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L52 | neighbors=[test_attack_paths.py, .test_asset_node_attributes(), .test_connects_to_and_same_segment_edge…, .test_credential_reuse_edges(), .test_exploit_complexity_falls_back_to_…, .test_exploit_complexity_from_vector()] | lang=en
- "tests_test_auth_login": "test_auth_login.py" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, _make_db(), _make_tenant(), _make_user(), TestAuthenticateBcryptFailure] | lang=en
- "tests_test_detection_core_testcleanrpmversion": "TestCleanRpmVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L988 | neighbors=[test_detection_core.py, .test_strips_release(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testcpecandidatecpe23": "TestCPECandidateCpe23" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L907 | neighbors=[test_detection_core.py, .test_cpe23_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testfactref": "TestFactRef" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L174 | neighbors=[test_detection_core.py, .test_ref_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testfindingtodict": "TestFindingToDict" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L166 | neighbors=[test_detection_core.py, .test_enums_serialized_to_values(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testnormalizeweb": "TestNormalizeWeb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L925 | neighbors=[test_detection_core.py, .test_server_header(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_validation_testsplunkintegration": "TestSplunkIntegration" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L296 | neighbors=[test_detection_validation.py, .skip_without_flag(), .test_live_query(), AttackAction, DetectionCorrelator, DetectionGap] | lang=en
- "tests_test_exploit_engine": "test_exploit_engine.py" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator] | lang=en
- "tests_test_exploit_engine_testvalidatemodule": "TestValidateModule" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L103 | neighbors=[test_exploit_engine.py, .test_dos_blocked(), .test_encoder_blocked(), .test_exploit_module_allowed(), .test_fuzzer_blocked(), .test_scanner_module_allowed()] | lang=en
- "tests_test_exploit_engine_testvalidatescope": "TestValidateScope" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L128 | neighbors=[test_exploit_engine.py, .test_excluded_cidr_takes_priority(), .test_invalid_ip_fails(), .test_ip_in_excluded_fails(), .test_ip_in_scope_passes(), .test_ip_out_of_scope_fails()] | lang=en
- "tests_test_outbox_reclaim": "test_outbox_reclaim.py" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, _mock_session(), _now(), _sql(), test_boundary_at_exactly_the_lease_is_r…, test_dead_letter_and_requeue_are_mutual…] | lang=en
- "tests_test_pipeline_empty_epss": "_empty_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L36 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…] | lang=en
- "tests_test_pipeline_empty_kev": "_empty_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L32 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…] | lang=en
- "tests_test_scan_funnel_make_funnel": "_make_funnel()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L64 | neighbors=[test_scan_funnel.py, FakeDiscovery, FakePortScanner, _scope(), Build a funnel with fakes; return (funn…, .test_db_scanner_invoked_with_db_port()] | lang=en
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()] | lang=en
- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L235 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _finalize_trace(), _gather_per_host(), _port_candidates(), _record()] | lang=en
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr] | lang=en
- "agent_agent_say": "say()" | kind=code-symbol | source=probe/agent/agent.py:L76 | neighbors=[agent.py, _check_anti_debug(), _enroll_device(), _flush_spool_over_http(), _load_or_create_identity(), main()] | lang=en
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=probe/agent/cli.py:L125 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()] | lang=en
- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2041 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()] | lang=en
- "console_primitives": "Primitives.tsx" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, Delta(), Meter(), Panel(), Readout(), SeverityChip()] | lang=en
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L34 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…] | lang=en
- "launch_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, a789cca scanner: real use-case library,…, INTENSITY_PRESETS, LaunchBody] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-007.json

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
