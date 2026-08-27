# Node Description Batch 9 of 236

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

- "agent_local_run": "local_run.py" | kind=code-symbol | source=probe/agent/local_run.py:L1 | neighbors=[agent.py, _clean(), _main(), _parse_args(), _port_label(), _ports_from_env()] | lang=en
- "agent_result_spool_resultspool": "ResultSpool" | kind=code-symbol | source=probe/agent/result_spool.py:L27 | neighbors=[result_spool.py, Persists scan results locally and retri…, .at_capacity(), .exists(), .flush_spool(), .__init__()] | lang=en
- "app_database": "database.py" | kind=code-symbol | source=manager/backend/app/database.py:L1 | neighbors=[config.py, get_db(), get_read_db(), dependencies.py, middleware.py, router.py] | lang=en
- "branch:repo:github.com/Rutikm18/Project-Vedha#backup-before-secret-removal": "backup-before-secret-removal" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 5c8e696 docs(probe): correct overclaimi…, 8d65c92 first commit, 95904f1 feat(probe): detect SMB signing…] | lang=en
- "commands_ask": "ask.ts" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L1 | neighbors=[requireAuth(), streamAsk(), buildAskCommand(), ConvMessage, runInteractive(), DiscoveredHost] | lang=en
- "commands_interactive_runiterativeengagement": "runIterativeEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L816 | neighbors=[interactive.ts, runHostDiscoveryOnly(), chooseNextPhase(), confirm(), ln(), phaseLabel()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0fbec7dfc54f7cd50921f99169270a9330d111d0": "0fbec7d feat(verification): add finding verification verdict columns + migration" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2fcec73635c396d5433940b61f8b85a02e532d50": "2fcec73 feat(verification): stamp verdicts on detection-run findings (flagged)" | kind=Commit | source=git | neighbors=[config.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@41b692a77a1dd6d2e5666f2fa2f8aa4b1e084e64": "41b692a Update project files" | kind=Commit | source=git | neighbors=[08e0594 deployement ready, AssistantFab.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@80b6dbcc5515152a76b93176716127f4f997f356": "80b6dbc Remove environment secrets from repository" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0b870c8a083dca715a6f06baf63cd015adb389d": "a0b870c fix(posture): score over open findings only; lock grade-band boundary t…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@c0f3b4c86830cc30f1c8a4da8694f7aa5c0807dc": "c0f3b4c feat(probe-enroll): trust-on-first-use auto-enrollment + gen-env policy…" | kind=Commit | source=git | neighbors=[22701ea Add tests for scanner parity an…, agent.py, config.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5ebd3818a42f2cb9d5f6661004e3f5737bb605a": "c5ebd38 feat(sla): per-tenant custom SLA policies (item 4 backend)" | kind=Commit | source=git | neighbors=[2b4ff71 feat(fleet): one-click Approve …, main.py, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c7f226f03ff7acd5ce8d6938c21a4e8b7e8997b4": "c7f226f chore: bundle pending working-tree work for release" | kind=Commit | source=git | neighbors=[656e909 feat(ui): polish login page, to…, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 63d9c9a fix(probe): recover from 409 wh…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ddb51f2d79c6e862a9478d09389375d3f223afc3": "ddb51f2 feat(resolution): add finding resolution-lifecycle columns + migration" | kind=Commit | source=git | neighbors=[5d5c158 refactor: remove unused dashboa…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "detection_edr_edrdetection": "EDRDetection" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L31 | neighbors=[edr.py, .parse_response(), .is_prevented(), .parse_response(), .parse_response(), AttackAction] | lang=en
- "engine_scan_modules": "scan-modules.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L1 | neighbors=[interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, defaultModules(), depthDefaults(), moduleById(), ModuleCategory] | lang=en
- "exploit_msf_client_metasploitrpcerror": "MetasploitRPCError" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L23 | neighbors=[msf_client.py, ._call(), .connect(), ._raw_call(), .run_module(), Exception] | lang=en
- "lib_security_context": "security-context.ts" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L1 | neighbors=[route.ts, route.ts, 1fe16c8 stable but some dead code, need…, route.ts, adapters.ts, toUiFinding()] | lang=en
- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "models_llm_output_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L12 | neighbors=[llm_output.py, Base, TimestampMixin, Every LLM generation is persisted here …, LLMReportGenerator, LLMUnavailableError] | lang=en
- "routers_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _all_paths_to_critical(), _asset_labels(), attack_graph()] | lang=en
- "routers_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 3c277ba feat(lifecycle): add POST /find…, 8ebc053 feat(risk-rank-ui): surface ver…, c5ebd38 feat(sla): per-tenant custom SL…, cac022c Everything is done and verified…] | lang=en
- "services_job_result_service": "job_result_service.py" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 21ebc46 feat(detection): unified priori…, 22701ea Add tests for scanner parity an…, 3565ada fix(ingest): NUL-safe result su…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …] | lang=en
- "services_posture": "posture.py" | kind=code-symbol | source=manager/backend/app/services/posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 237a831 feat(posture): add run comparis…, 5238865 feat(posture): add pure scoring…, aggregate(), build_posture(), _clamp01()] | lang=en
- "tests_test_ad_assessment_testasreproastchecker": "TestASREPRoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L215 | neighbors=[test_ad_assessment.py, .setup_method(), .test_finding_shape(), .test_get_no_preauth_accounts(), .test_no_finding_when_empty(), .test_request_asrep_without_impacket()] | lang=en
- "tests_test_ad_assessment_testntlmrelaychecker": "TestNTLMRelayChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L247 | neighbors=[test_ad_assessment.py, .setup_method(), .test_finding_for_ldap_signing_only(), .test_finding_includes_ntlmrelayx_comma…, .test_no_finding_when_all_secure(), .test_smb_signing_without_impacket_mark…] | lang=en
- "tests_test_detection_core_testallosvsourcepackages": "TestAllOsvSourcePackages" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L993 | neighbors=[test_detection_core.py, .test_returns_list(), .test_sorted(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testclassifyconfidence": "TestClassifyConfidence" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L202 | neighbors=[test_detection_core.py, .test_authoritative_scanners(), .test_inferred_scanners(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testfindingpostinit": "TestFindingPostInit" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L113 | neighbors=[test_detection_core.py, .test_accepts_nonempty_evidence_refs(), .test_refuses_zero_evidence_refs(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testisip": "TestIsIp" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L212 | neighbors=[test_detection_core.py, .test_hostname(), .test_valid_ipv4(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testkevdb": "TestKevDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L838 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_is_kev(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testnormalize": "TestNormalize" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L960 | neighbors=[test_detection_core.py, .test_dispatches_banner(), .test_unknown_scanner_returns_empty(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testnormalizebanner": "TestNormalizeBanner" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L913 | neighbors=[test_detection_core.py, .test_empty_banner(), .test_ssh_banner(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testproductfromcpe": "TestProductFromCpe" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L552 | neighbors=[test_detection_core.py, .test_extracts_product(), .test_short_cpe_returns_cpe(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_exploit_engine_testmetasploitrpcclient": "TestMetasploitRPCClient" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L181 | neighbors=[test_exploit_engine.py, ._make_client(), .test_call_without_connect_raises(), .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit()] | lang=en
- "tests_test_exploit_engine_testrequiresapproval": "TestRequiresApproval" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L153 | neighbors=[test_exploit_engine.py, .test_adcs_server(), .test_critical_asset_needs_approval(), .test_dc02_pattern(), .test_dc_hostname_needs_approval(), .test_exchange_server()] | lang=en
- "tests_test_integration": "test_integration.py" | kind=code-symbol | source=probe/tests/test_integration.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, result_spool.py, scope_crypt.py, scope_validator.py, task_runner.py, transport.py] | lang=en
- "tests_test_new_scanners_testsnmpberutilities": "TestSNMPBerUtilities" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L24 | neighbors=[test_new_scanners.py, .test_ber_len_long_form_one_byte(), .test_ber_len_long_form_two_bytes(), .test_ber_len_short_form(), .test_ber_parse_empty(), .test_ber_parse_two_tlvs()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-008.json

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
