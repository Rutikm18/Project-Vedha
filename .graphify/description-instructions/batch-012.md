# Node Description Batch 13 of 119

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

- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig] | lang=en
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, ADAssessmentRunner, BaseModel, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, ADAssessmentRunner, BaseModel, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L255 | neighbors=[agents.py, BaseModel, Asset, Engagement, AssetType, ScanJobStatus] | lang=en
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), PortScanner] | lang=en
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L68 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()] | lang=en
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), ServiceBannerScanner] | lang=en
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated] | lang=en
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, FindingFilter, FindingOut, FindingPatch, FindingSummary] | lang=en
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET] | lang=en
- "tests_scanner_adapters_test": "scanner-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-adapters.test.ts:L1 | neighbors=[b4b12a9 Rename project and update files, netexec-parser.ts, parseNetExecLog(), openvas-client.ts, parseOpenVASHelperOutput(), scanner-request-validation.ts] | lang=en
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard] | lang=en
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient] | lang=en
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _action(), pytest_addoption(), TestDetectionCorrelator, TestEDRParsing, TestSIEMParsing] | lang=en
- "tests_test_exploit_engine_rationale_1": "Unit tests for the exploitation engine.  All external connections (Metasploit RP" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=en
- "tests_test_exploit_engine_rationale_420": "Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L420 | neighbors=[MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=pt
- "tests_test_exploit_engine_rationale_465": "Register --msf-host CLI option for integration tests." | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L465 | neighbors=[MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=en
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L167 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()] | lang=en
- "tests_test_vuln_enrichment_make_http_mock": "_make_http_mock()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L52 | neighbors=[test_vuln_enrichment.py, Create a mock httpx.AsyncClient that re…, test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full()] | lang=en
- "verify_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, verifyOtp(), addUser(), getUser(), POST()] | lang=en
- "vuln_enrichment_ttlcache": "TTLCache" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L27 | neighbors=[enrichment.py, LRU + TTL eviction. Expired keys are pu…, AssetCriticality, OrderedDict, .__contains__(), .get()] | lang=en
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L119 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, ._consume_stdout(), ._partial_or_raise(), ._read_stderr()] | lang=en
- "workflow_cli": "cli.py" | kind=code-symbol | source=probe/workflow/cli.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, scanner_base.py, _build_creds(), _build_mode(), build_parser()] | lang=en
- "workflow_router": "router.py" | kind=code-symbol | source=probe/workflow/router.py:L1 | neighbors=[bb0ef3d feat(probe): route DB services …, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_router_db.py, looks_like_db(), looks_like_http()] | lang=en
- "agent_agent_ws_http_poll_fallback": "_ws_http_poll_fallback()" | kind=code-symbol | source=probe/agent/agent.py:L540 | neighbors=[agent.py, Poll pending jobs even while WS is conn…, _run_ws_push_loop(), _flush_spool_over_http(), say(), _ws_run_job()] | lang=en
- "agent_agent_wssession": ".wsSession()" | kind=code-symbol | source=probe-go/agent/agent.go:L150 | neighbors=[agent.py, .runWSLoop(), containsString(), .flushSpool(), resultPayload(), .runJob()] | lang=en
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=probe/agent/cli.py:L237 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient] | lang=en
- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=probe/agent/task_runner.py:L1 | neighbors=[JobResult, TaskRunner, use_cases.py, task_runner.py — orchestrates the full …, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files] | lang=en
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L19 | neighbors=[GzipRequestMiddleware, Identify the Manager API without exposi…, middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch()] | lang=en
- "commands_logout": "logout.ts" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L1 | neighbors=[clearSession(), loadSession(), buildLogoutCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts] | lang=en
- "commands_status": "status.ts" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildStatusCommand(), ScanRow, STATUS_COLOR, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "commands_whoami": "whoami.ts" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildWhoamiCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts] | lang=en
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L18 | neighbors=[page.tsx, page.tsx, PageShell.tsx, page.tsx, page.tsx, page.tsx] | lang=en
- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackAction, _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO] | lang=en
- "detection_engine_ingest_ingest_file": "ingest_file()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L99 | neighbors=[ingest.py, _classify_confidence(), _extract_aliases(), IngestResult, .get_or_create_asset(), QuarantinedLine] | lang=en
- "detection_engine_pipeline_rationale_1": "pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.    ingest" | kind=entity | source=manager/detection_engine/pipeline.py:L1 | neighbors=[AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB, IngestResult] | lang=en
- "detection_engine_pipeline_rationale_110": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L110 | neighbors=[AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB, IngestResult] | lang=en
- "detection_engine_pipeline_rationale_40": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L40 | neighbors=[AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB, IngestResult] | lang=en
- "detection_engine_verifier": "verifier.py" | kind=code-symbol | source=manager/detection_engine/verifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, classify_tier(), deception_score(), _evidence_scanners(), EvidenceTier, verify()] | lang=en
- "discovery_finding_translator": "finding_translator.py" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_probe_result(), _find_open_duplicate(), _map_severity(), _resolve_asset()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-012.json

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
