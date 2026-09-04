# Node Description Batch 9 of 332

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

- "agent_agent_run_ws_push_loop": "_run_ws_push_loop()" | kind=code-symbol | source=probe/agent/agent.py:L653 | neighbors=[agent.py, main(), Persistent WebSocket push loop.      Re…, _flush_spool_over_http(), say(), _ws_heartbeat_sender()] | lang=en
- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=probe/agent/task_runner.py:L1 | neighbors=[JobResult, prepare_result_dir(), _result_dir(), TaskRunner, use_cases.py, scanner_base.py] | lang=en
- "branch:repo:github.com/Rutikm18/Project-Vedha#spike/probe-go": "spike/probe-go" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0fbec7dfc54f7cd50921f99169270a9330d111d0": "0fbec7d feat(verification): add finding verification verdict columns + migration" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2fcec73635c396d5433940b61f8b85a02e532d50": "2fcec73 feat(verification): stamp verdicts on detection-run findings (flagged)" | kind=Commit | source=git | neighbors=[config.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@41b692a77a1dd6d2e5666f2fa2f8aa4b1e084e64": "41b692a Update project files" | kind=Commit | source=git | neighbors=[08e0594 deployement ready, AssistantFab.tsx, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@80b6dbcc5515152a76b93176716127f4f997f356": "80b6dbc Remove environment secrets from repository" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0b870c8a083dca715a6f06baf63cd015adb389d": "a0b870c fix(posture): score over open findings only; lock grade-band boundary t…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@c0f3b4c86830cc30f1c8a4da8694f7aa5c0807dc": "c0f3b4c feat(probe-enroll): trust-on-first-use auto-enrollment + gen-env policy…" | kind=Commit | source=git | neighbors=[22701ea Add tests for scanner parity an…, agent.py, config.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5ebd3818a42f2cb9d5f6661004e3f5737bb605a": "c5ebd38 feat(sla): per-tenant custom SLA policies (item 4 backend)" | kind=Commit | source=git | neighbors=[2b4ff71 feat(fleet): one-click Approve …, main.py, addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c7f226f03ff7acd5ce8d6938c21a4e8b7e8997b4": "c7f226f chore: bundle pending working-tree work for release" | kind=Commit | source=git | neighbors=[656e909 feat(ui): polish login page, to…, addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ddb51f2d79c6e862a9478d09389375d3f223afc3": "ddb51f2 feat(resolution): add finding resolution-lifecycle columns + migration" | kind=Commit | source=git | neighbors=[5d5c158 refactor: remove unused dashboa…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L47 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), Run Nuclei CVE PoC templates against a …] | lang=en
- "main_scripts_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext()] | lang=en
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…] | lang=en
- "scripts_seed_admin": "seed_admin.py" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _detect_drift(), _hash()] | lang=en
- "tests_test_ad_assessment_testkerberoastchecker": "TestKerberoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L168 | neighbors=[test_ad_assessment.py, ._ldap_with_users(), .setup_method(), .test_finding_critical_when_privileged(), .test_finding_high_when_not_privileged(), .test_get_spn_accounts_filters_krbtgt_a…] | lang=en
- "tests_test_detection_core_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L38 | neighbors=[test_detection_core.py, .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports(), .test_smbv1_with_missing_hotfixes_retur…] | lang=en
- "tests_test_detection_core_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L81 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()] | lang=en
- "tests_test_detection_core_testaggregate": "TestAggregate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1122 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), ConsistencyReport] | lang=en
- "tests_test_detection_core_testclassifytier": "TestClassifyTier" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L664 | neighbors=[test_detection_core.py, .test_authoritative_tier4(), .test_multi_signal_tier2(), .test_protocol_scanner_tier3(), .test_single_banner_tier1(), ConsistencyReport] | lang=en
- "tests_test_detection_core_testcorrelatesmbpatch": "TestCorrelateSmbPatch" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L629 | neighbors=[test_detection_core.py, .test_no_smb_facts_returns_none(), .test_smbv1_with_missing_hotfixes_retur…, .test_smbv1_with_patched_host_returns_n…, .test_smbv1_without_hotfix_data_returns…, ConsistencyReport] | lang=en
- "tests_test_detection_core_testdedupfindings": "TestDedupFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L525 | neighbors=[test_detection_core.py, .test_authoritative_upgrades_state(), .test_different_ids_preserved(), .test_evidence_refs_dedup_preserving_or…, .test_merges_same_id(), ConsistencyReport] | lang=en
- "tests_test_detection_core_testfindingconsistency": "TestFindingConsistency" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1096 | neighbors=[test_detection_core.py, .test_classification_intermittent(), .test_classification_mostly_stable(), .test_classification_stable(), .test_rate(), ConsistencyReport] | lang=en
- "tests_test_detection_core_testwilsonci": "TestWilsonCi" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1077 | neighbors=[test_detection_core.py, .test_all_appearances(), .test_perfect_appearance(), .test_zero_appearances(), .test_zero_n(), ConsistencyReport] | lang=en
- "tests_test_detection_validation_testsiemparsing": "TestSIEMParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L213 | neighbors=[test_detection_validation.py, .test_elastic_parse(), .test_factory(), .test_sentinel_parse(), .test_splunk_parse(), .test_splunk_spl_includes_host_and_time…] | lang=en
- "tests_test_os_fingerprint": "test_os_fingerprint.py" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, TestAcceptEchoReply] | lang=en
- "tests_test_pipeline": "test_pipeline.py" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 4d0377d Add unit tests for SMB scanner,…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, _banner_jsonl(), _empty_epss()] | lang=en
- "tests_test_remediation_routes": "test_remediation_routes.py" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, _db_scalar()] | lang=en
- "tests_test_service_banner_ident": "test_service_banner_ident.py" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, scanner_base.py, service_banner.py, _scanner(), _self_signed()] | lang=en
- "tests_test_service_identifier_testserviceidentifier": "TestServiceIdentifier" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L6 | neighbors=[test_service_identifier.py, ._id(), .setup_method(), .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined()] | lang=en
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, explain_plan.py, 10dfc80 Add comprehensive probe testing…, 3ad95f4 feat: Optimize asset service fe…, 7a637eb feat: network VA accuracy, KEV …, c7f226f chore: bundle pending working-t…] | lang=en
- "workflow_execution": "execution.py" | kind=code-symbol | source=probe/workflow/execution.py:L1 | neighbors=[engine.py, explain_plan.py, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, f473173 merge: network VA accuracy, KEV…] | lang=en
- "ad_orchestrator_adassessmentrunner": "ADAssessmentRunner" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L39 | neighbors=[orchestrator.py, ._anonymous_bind_finding(), .__init__(), .run(), Coordinates all AD checkers for a singl…, ADCSChecker] | lang=en
- "ai_agent_agentdecisionengine": "AgentDecisionEngine" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L161 | neighbors=[agent.py, .available(), ._count(), ._create(), ._exec_read_tool(), .__init__()] | lang=en
- "ai_llm_report": "llm_report.py" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[_collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, LLMUnavailableError, _normalize_ai_plan()] | lang=en
- "ai_llm_report_llmunavailableerror": "LLMUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L47 | neighbors=[llm_report.py, ._complete(), RuntimeError, Raised when the Anthropic SDK or API ke…, Raised when the Anthropic SDK or API ke…, HallucinationGuard] | lang=en
- "assistant_assistantprovider": "AssistantProvider.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L1 | neighbors=[layout.tsx, AssistantDrawer.tsx, AssistantFab.tsx, AssistantDrawer(), AssistantFab(), AssistantCtx] | lang=en
- "auth_router": "router.py" | kind=code-symbol | source=manager/backend/app/auth/router.py:L1 | neighbors=[database.py, dependencies.py, ratelimit.py, _authenticate(), create_personal_access_token(), list_personal_access_tokens()] | lang=en

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
