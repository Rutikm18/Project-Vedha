# Node Description Batch 11 of 236

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

- "models_detection_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/backend/app/models/detection.py:L12 | neighbors=[detection.py, Base, TimestampMixin, Base, TimestampMixin, DetectionStatus] | lang=en
- "native_port_scan": "port-scan.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, CheckOpts, checkPort(), expandTarget()] | lang=en
- "portal_portalshell": "PortalShell.tsx" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L1 | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, c52feb4 feat(portal): reskin User Porta…, f8ff229 feat(ui): remove decorative ses…, page.tsx, page.tsx, ThemeProvider.tsx] | lang=en
- "routers_engagements_engagementupdate": "EngagementUpdate" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L484 | neighbors=[engagements.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), Asset] | lang=en
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 95904f1 feat(probe): detect SMB signing…, d1b4dd3 trim frontend to 7 core pages; …, main()] | lang=en
- "schemas_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…, ClientEngagementOut, ClientFindingOut] | lang=en
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
- "tests_test_remediation_routes": "test_remediation_routes.py" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, _db_scalar(), _FakeDB, _finding(), _GenAI] | lang=en
- "tests_test_scan_funnel_make_funnel": "_make_funnel()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L64 | neighbors=[test_scan_funnel.py, FakeDiscovery, FakePortScanner, _scope(), Build a funnel with fakes; return (funn…, .test_db_scanner_invoked_with_db_port()] | lang=en
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()] | lang=en
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr] | lang=en
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=probe/agent/cli.py:L125 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()] | lang=en
- "auth_startup_run_startup_diagnostics": "run_startup_diagnostics()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L280 | neighbors=[startup.py, Run all startup checks concurrently.   …, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()] | lang=en
- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2041 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@027f4e4a2d8ac673df4346462728ac22849b0cf0": "027f4e4 feat(integrations): per-tenant email/Slack/Jira config store + CRUD (it…" | kind=Commit | source=git | neighbors=[main.py, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@08e0594c53bb049b1860e796d7c8315f1a5afd7e": "08e0594 deployement ready" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2a36f8a328c12c4fd1f8d9d7a61f80bddc044304": "2a36f8a fix: update docker compose commands to use .env file for environment va…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@4733f247081202b702e7044b11dc325fdf01bc04": "4733f24 evasion(scanner): --source-port for stateless-ACL bypass (subtask #2a)" | kind=Commit | source=git | neighbors=[2534404 scanner(service_enum): commit o…, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@54503ae3d26d1926e1232f1dc9803e8cfd20faec": "54503ae feat(scanner): SYN path harvests OS-fingerprint intel + RTT-adaptive ti…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b6acb87b50e17f444fd6433cdaaf57cca5c2918": "6b6acb8 fix: update AWS compose command and set default MANAGER_PUBLIC_URL in d…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@879cdfa25f56102c23df1efdc671934f88d1b793": "879cdfa docs: probe fleet automation design spec (Phase 0 detailed)" | kind=Commit | source=git | neighbors=[41b692a Update project files, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9347a9a16f87a98cc882c39ad050f50544b65e0b": "9347a9a feat(posture): surface posture scorecard + patch matrix on dashboard" | kind=Commit | source=git | neighbors=[page.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0791783d160c85c688ea511dc20396a7ac4e2e2": "a079178 fix(posture): full-width posture section; avoid blank grid column on de…" | kind=Commit | source=git | neighbors=[9347a9a feat(posture): surface posture …, page.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@aa560a0292202728647e1f6cde4e0ca942782cd6": "aa560a0 feat(posture): add dashboard PostureScorecard component" | kind=Commit | source=git | neighbors=[2cddd52 fix(posture): tenant-scope run …, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@ca41cbf25bddbb70f2808dcfbb236405c24bfc69": "ca41cbf docs: pre-auth probe enrollment token design spec" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d2eb44c3d2c1f5ac6a3398dc1bf865c46447a9a8": "d2eb44c feat(posture): add dashboard PatchComparisonMatrix component" | kind=Commit | source=git | neighbors=[aa560a0 feat(posture): add dashboard Po…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-010.json

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
