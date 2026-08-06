# Node Description Batch 8 of 134

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

- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2041 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()] | lang=en
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L34 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…] | lang=en
- "launch_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, a789cca scanner: real use-case library,…, INTENSITY_PRESETS, LaunchBody] | lang=en
- "lib_findings_store_getallfindings": "getAllFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L33 | neighbors=[ask.ts, findings.ts, interactive.ts, findings-store.ts, deleteFinding(), ensureDir()] | lang=en
- "lib_job_store": "job-store.ts" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId()] | lang=en
- "lib_scanner_request_validation": "scanner-request-validation.ts" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L1 | neighbors=[b4b12a9 Rename project and update files, isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest] | lang=en
- "models_agent_agent": "Agent" | kind=code-symbol | source=manager/backend/app/models/agent.py:L18 | neighbors=[agent.py, Base, TimestampMixin, Base, TimestampMixin, AgentRegisterRequest] | lang=en
- "routers_ai_report_reviewrequest": "ReviewRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L52 | neighbors=[ai_report.py, RejectRequest, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset] | lang=en
- "routers_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2cddd52 fix(posture): tenant-scope run …, 9de087a feat(posture): add GET /analyti…, a0b870c fix(posture): score over open f…, dependencies.py, exposure()] | lang=en
- "routers_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, configure_siem(), get_coverage(), get_gaps()] | lang=en
- "routers_vuln_scans_findingimport": "FindingImport" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L49 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_vuln_scans_nessusscanrequest": "NessusScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L35 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_vuln_scans_nucleiscanrequest": "NucleiScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L43 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus] | lang=en
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _auth_shaped_json_body(), _known_false_positive(), main()] | lang=en
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _get_cert_der(), main()] | lang=en
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, bce780a feat(probe): enumerate HTTP met…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _fetch()] | lang=en
- "scripts_startup_validator": "startup_validator.py" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator] | lang=en
- "tests_test_ad_assessment_testbuildadfinding": "TestBuildADFinding" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L58 | neighbors=[test_ad_assessment.py, .test_attack_narrative_carried_in_evide…, .test_invalid_severity_falls_back_to_in…, .test_required_fields_present(), ADCSChecker, CertTemplate] | lang=en
- "tests_test_agents_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L22 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()] | lang=en
- "tests_test_detection_core_rationale_1": "Detection engine test suite — unit tests for the core detection/correlation pipe" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB] | lang=en
- "tools_manifest": "manifest.ts" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, currentPlatform(), Platform, TOOL_MANIFEST] | lang=en
- "ad_ldap_enum_aduser": "ADUser" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L55 | neighbors=[ldap_enum.py, .get_users(), ADConnectionError, DependencyMissingError, _FakeAttr, _FakeEntry] | lang=en
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=probe/agent/engine.py:L386 | neighbors=[engine.py, Execute a scan and return the enriched …, _build_run_stats(), _error_result(), _facts_from_cache(), _job_runtime_seconds()] | lang=en
- "agent_license": "license.py" | kind=code-symbol | source=probe/agent/license.py:L1 | neighbors=[agent.py, _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError] | lang=en
- "auth_startup_run_startup_diagnostics": "run_startup_diagnostics()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L282 | neighbors=[startup.py, Run all startup checks concurrently.   …, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()] | lang=en
- "commands_interactive_ask": "ask()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L39 | neighbors=[interactive.ts, choose(), confirm(), ensureAuthenticated(), pickHostSubset(), pickTargets()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@30261ebec685fe061217d7e71faa08b5a4b6d5ea": "30261eb feat: enhance advisor flow with structured brief and probe selection- A…" | kind=Commit | source=git | neighbors=[AdvisorFlow.tsx, AssistantDrawer.tsx, main, worktree-fleet-already-downloaded-cmd, a4b970c feat(fleet): add run command fo…, route.ts] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a789cca150b7688941e2f9229631f493d3fab094": "a789cca scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, main, spike/probe-go, worktree-fleet-already-downloaded-cmd, 10dfc80 Add comprehensive probe testing…] | lang=pt
- "detection_engine_cpe_normalizer": "cpe_normalizer.py" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), CPECandidate, normalize()] | lang=en
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, ManagerAiResponse, POST(), assistant.ts] | lang=en
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), OtpEntry, otpStore, OtpVerifyResult] | lang=en
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, counters, generateFindingId(), resetCounters()] | lang=en
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, countBySeverity(), NucleiMatch, nucleiMatchToFinding()] | lang=en
- "lib_with_backend_withbackend": "withBackend()" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L22 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, str, Base, TimestampMixin, AgentRegisterRequest, AgentRegisterResponse] | lang=en
- "native_http_probe": "http-probe.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractTitle(), fingerprint(), HttpProbeResult] | lang=en
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L249 | neighbors=[agents.py, BaseModel, bootstrap_agent(), register_agent(), Asset, Engagement] | lang=en
- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L46 | neighbors=[ai_report.py, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath] | lang=en
- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L56 | neighbors=[ai_report.py, ReviewRequest, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath] | lang=en
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L86 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError] | lang=en

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
