# Node Description Batch 11 of 104

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

- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, agent_recommendation.py, Base] | lang=en
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, Base, TimestampMixin, TimestampMixin, Per-engagement SIEM + EDR connection se…] | lang=en
- "native_dir_bust": "dir-bust.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, BUILTIN_PATHS, DirBustResult, loadWordlist()] | lang=en
- "nuclei_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/nuclei/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, findings-store.ts, createFinding(), nuclei-parser.ts, countBySeverity()] | lang=en
- "probe_go_main": "main.go" | kind=code-symbol | source=probe-go/main.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, envFilePath(), findServiceLabel(), isDirWritable(), localScan(), main()] | lang=en
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, ADAssessmentRunner, BaseModel, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, ADAssessmentRunner, BaseModel, Engagement, FindingSeverity, FindingStatus] | lang=en
- "scanner_fingerprint": "fingerprint.go" | kind=code-symbol | source=probe-go/scanner/fingerprint.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, buildSignatures(), expandBackrefs(), Fingerprint(), firstLine(), matchSignature()] | lang=en
- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/scanner/passive_collector.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, pipeline.py, _device_hint(), _is_readable(), main(), _open_listener()] | lang=en
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L68 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()] | lang=en
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _fetch(), main()] | lang=en
- "status_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scans/[scanId]/status/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, types.ts, Severity, auth-store.ts, verifyToken(), findings-store.ts] | lang=en
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient] | lang=en
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()] | lang=en
- "tests_test_exploit_engine_rationale_1": "Unit tests for the exploitation engine.  All external connections (Metasploit RP" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=en
- "tests_test_exploit_engine_rationale_420": "Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L420 | neighbors=[MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=pt
- "tests_test_exploit_engine_rationale_465": "Register --msf-host CLI option for integration tests." | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L465 | neighbors=[MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=en
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L167 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()] | lang=en
- "tests_test_vuln_enrichment_make_http_mock": "_make_http_mock()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L52 | neighbors=[test_vuln_enrichment.py, Create a mock httpx.AsyncClient that re…, test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full()] | lang=en
- "vuln_enrichment_ttlcache": "TTLCache" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L27 | neighbors=[enrichment.py, LRU + TTL eviction. Expired keys are pu…, AssetCriticality, OrderedDict, .__contains__(), .get()] | lang=en
- "workflow_gates": "gates.py" | kind=code-symbol | source=probe/workflow/gates.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, test_probe_core.py, gate_0_is_passive_profile(), gate_2_host_discovery(), gate_3_port_scan()] | lang=en
- "workflow_modes": "modes.py" | kind=code-symbol | source=probe/workflow/modes.py:L1 | neighbors=[engine.py, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, test_probe_core.py, assessment(), EngagementMode] | lang=en
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()] | lang=en
- "agent_agent_run_ws_push_loop": "_run_ws_push_loop()" | kind=code-symbol | source=probe/agent/agent.py:L255 | neighbors=[agent.py, main(), Persistent WebSocket push loop.      Re…, say(), _ws_flush_spool(), _ws_heartbeat_sender()] | lang=en
- "agent_agent_scanningagent": "ScanningAgent" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L639 | neighbors=[agent.py, ._api_call(), ._execute_job(), ._handle_shutdown(), ._heartbeat_loop(), .__init__()] | lang=en
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=probe/agent/cli.py:L235 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient] | lang=en
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L194 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), CliError, ConfigStore] | lang=en
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()] | lang=en
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[index.ts, auth.ts, apiFetch(), requireAuth(), buildEngagementCommand(), Engagement] | lang=en
- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[index.ts, buildFindingsCommand(), types.ts, Severity, findings-store.ts, getAllFindings()] | lang=en
- "components_sidebar": "Sidebar.tsx" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L1 | neighbors=[page.tsx, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, NAV_SECTIONS, NavItem] | lang=en
- "components_themeprovider": "ThemeProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L1 | neighbors=[layout.tsx, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, Theme, ThemeContext] | lang=en
- "dashboard_slarow": "SlaRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, getSla(), SEV_BG, SEV_COLOR, SlaRow(), mock-dashboard.ts] | lang=en
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender] | lang=en
- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient] | lang=en
- "detection_engine_ingest_ingest_file": "ingest_file()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L99 | neighbors=[ingest.py, _classify_confidence(), _extract_aliases(), IngestResult, .get_or_create_asset(), QuarantinedLine] | lang=en
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()] | lang=en
- "detection_engine_pipeline_rationale_1": "pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.    ingest" | kind=entity | source=manager/detection_engine/pipeline.py:L1 | neighbors=[AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB, IngestResult] | lang=en
- "detection_engine_pipeline_rationale_110": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L110 | neighbors=[AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB, IngestResult] | lang=en
- "detection_engine_pipeline_rationale_40": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L40 | neighbors=[AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB, IngestResult] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-010.json

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
