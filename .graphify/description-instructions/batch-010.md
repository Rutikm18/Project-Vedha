# Node Description Batch 11 of 227

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

- "routers_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, configure_siem(), get_coverage(), get_gaps()] | lang=en
- "routers_validation": "validation.py" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, dependencies.py, approve_validation(), create_validation_request(), _default_check_kind(), _get_request_or_404()] | lang=en
- "routers_vuln_scans_findingimport": "FindingImport" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L49 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_vuln_scans_nessusscanrequest": "NessusScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L35 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_vuln_scans_nucleiscanrequest": "NucleiScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L43 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus] | lang=en
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 37376de hardening(scanner): OPSEC de-si…, d1b4dd3 trim frontend to 7 core pages; …, _auth_shaped_json_body(), _known_false_positive(), main()] | lang=en
- "scanner_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _have_nmap(), main(), NmapExecutionError] | lang=en
- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/scanner/passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _coverage(), _device_hint(), _is_readable(), _listener_error_code()] | lang=en
- "scripts_startup_validator": "startup_validator.py" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator] | lang=en
- "tests_test_ad_assessment_testbuildadfinding": "TestBuildADFinding" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L58 | neighbors=[test_ad_assessment.py, .test_attack_narrative_carried_in_evide…, .test_invalid_severity_falls_back_to_in…, .test_required_fields_present(), ADCSChecker, CertTemplate] | lang=en
- "tests_test_agents_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L22 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()] | lang=en
- "tests_test_detection_core_rationale_1": "Detection engine test suite — unit tests for the core detection/correlation pipe" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB] | lang=en
- "tests_test_os_fingerprint": "test_os_fingerprint.py" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L1 | neighbors=[2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, TestAcceptEchoReply, TestFingerprintOs] | lang=en
- "tests_test_pipeline": "test_pipeline.py" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _banner_jsonl(), _empty_epss(), _empty_jsonl(), _empty_kev(), _mock_vuln_db()] | lang=en
- "tests_test_pipeline_openssh_vuln_db": "_openssh_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L49 | neighbors=[test_pipeline.py, _mock_vuln_db(), Returns a VulnDB with a record that mat…, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default()] | lang=en
- "tools_manifest": "manifest.ts" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, currentPlatform(), Platform, TOOL_MANIFEST] | lang=en
- "ad_ldap_enum_aduser": "ADUser" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L55 | neighbors=[ldap_enum.py, .get_users(), ADConnectionError, DependencyMissingError, _FakeAttr, _FakeEntry] | lang=en
- "agent_agent_main": "main()" | kind=code-symbol | source=probe/agent/agent.py:L205 | neighbors=[agent.py, _bounded_env_int(), _classify_connection_error(), _dbg(), _is_local_manager_url(), _load_env()] | lang=en
- "agent_license": "license.py" | kind=code-symbol | source=probe/agent/license.py:L1 | neighbors=[agent.py, _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError] | lang=en
- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=probe/agent/task_runner.py:L1 | neighbors=[JobResult, TaskRunner, use_cases.py, task_runner.py — orchestrates the full …, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…] | lang=en
- "commands_interactive_ask": "ask()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L39 | neighbors=[interactive.ts, choose(), confirm(), ensureAuthenticated(), pickHostSubset(), pickTargets()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@02b63412fd2723bf5ed084158210ecdfe3da8183": "02b6341 feat(active-validation): pure escalation decision core" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@045c9ae0769ca5697260d9485812cc159ef0734c": "045c9ae fix(posture): normalize run_at in _present_in_run; drop dead scores_pre…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0d6be8593e79e58693a30c36cf650836a1cbb684": "0d6be85 feat(risk-rank): explainable 0-1000 finding priority" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0e22dbf9a3d7b87c329cbfa701b15bcc9e540c8c": "0e22dbf feat(probe): bounded auto-troubleshoot for Manager connectivity" | kind=Commit | source=git | neighbors=[agent.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0f0097bd1d03cc4d36e8d8e0f8dbe4bf2d68ae0a": "0f0097b feat(posture): mirror posture scorecard into generated reports" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@237a8319dd25a9eada7aec7f140dc7dba66b7dcd": "237a831 feat(posture): add run comparison, matrix, and response builder" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2cddd526f80b7999775f6cfdc6726ad8e77325ac": "2cddd52 fix(posture): tenant-scope run helper; test null asset/score paths; tid…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c277ba6178b4f0198b100b89c77054277f136d7": "3c277ba feat(lifecycle): add POST /findings/{id}/reopen endpoint" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c7740e5aee15e561362096ff219155ee7220b17": "3c7740e feat(lifecycle): pure manual-reopen helper" | kind=Commit | source=git | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@52388652e83dde75d08604b07cfbeea2a3929271": "5238865 feat(posture): add pure scoring core (noisy-OR risk/exploit/posture)" | kind=Commit | source=git | neighbors=[10ceaca feat: implement AI model fallba…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6be8259eadeca140adc8b3b0d2d0566889bae772": "6be8259 feat(integrations): outbox delivery worker + Send test (email/Slack/Jir…" | kind=Commit | source=git | neighbors=[00c6648 feat(settings): editable email/…, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, testing/all-features] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6c1f014f6e8fbacb7080f4aeed9329f17df208fe": "6c1f014 feat(correlation): implement composite findings for NTLM relay, legacy …" | kind=Commit | source=git | neighbors=[4d0377d Add unit tests for SMB scanner,…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@72f68af6099a8d2994b17533d41b44a3d1462134": "72f68af feat(verification): expose verification verdict + needs_review on findi…" | kind=Commit | source=git | neighbors=[2fcec73 feat(verification): stamp verdi…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7bd104a4484e9f6a90aad27a805339e333f13edf": "7bd104a feat(active-validation): pure result interpretation" | kind=Commit | source=git | neighbors=[02b6341 feat(active-validation): pure e…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@85e45373dae6a51a7abbd155431cc14324239f15": "85e4537 feat(risk-rank): expose risk_rank on findings API; add P2/P3/P4 plans" | kind=Commit | source=git | neighbors=[3c7740e feat(lifecycle): pure manual-re…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8cf23c236eb3cc74c9a7c7c156243658165f54e3": "8cf23c2 feat(resolution): wire coverage ledger + auto-resolution into detection…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@937737b010d12e40761c6d3593787c0bd0f87d6b": "937737b feat(resolution): reopen + flag regressions on the original finding row" | kind=Commit | source=git | neighbors=[8cf23c2 feat(resolution): wire coverage…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9a36729c7f6547ad20b1c35fee4ab54d4d603e9d": "9a36729 feat(resolution): coverage builder from completed-scanner facts" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9de087aedb96212596b5b8b4229dfe6215bbd2de": "9de087a feat(posture): add GET /analytics/posture endpoint" | kind=Commit | source=git | neighbors=[045c9ae fix(posture): normalize run_at …, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en

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
