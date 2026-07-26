# Node Description Batch 15 of 104

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

- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, backend.ts, backend(), BackendError, POST()] | lang=en
- "models_user_user": "User" | kind=code-symbol | source=manager/backend/app/models/user.py:L11 | neighbors=[user.py, Base, Base, TimestampMixin, UserRole, TimestampMixin] | lang=en
- "pipeline_route_runpipelinebackground": "runPipelineBackground()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L475 | neighbors=[route.ts, POST(), runEyewitnessStage(), runNaabuStage(), runNmapStage(), runNucleiStage()] | lang=en
- "request_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, auth-store.ts, generateOtp(), permissions-store.ts, isEmailAllowed()] | lang=en
- "routers_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, dependencies.py, exposure(), ExposureAnalytics, ProtocolRisk, ZoneHealth] | lang=en
- "routers_analytics_exposureanalytics": "ExposureAnalytics" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L37 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding] | lang=en
- "routers_analytics_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L27 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding] | lang=en
- "routers_analytics_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L32 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding] | lang=en
- "routers_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, dependencies.py, get_finding(), list_findings(), patch_finding()] | lang=en
- "scanner_discover": "discover.go" | kind=code-symbol | source=probe-go/scanner/discover.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, containsStr(), DiscoverHosts(), findStr(), intStr(), isRefused()] | lang=en
- "scanner_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/scanner/host_discovery.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, HostDiscoveryScanner, main(), host_discovery.py — determine which hos…] | lang=en
- "scanner_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L170 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L198 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L236 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()] | lang=en
- "scanner_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _have_nmap(), main(), _parse_nmap_xml(), _run_nmap(), nmap_wrapper.py — orchestrate nmap and …] | lang=en
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), PortScanner, port_scanner.py — TCP connect scan.  ME…] | lang=en
- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L490 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()] | lang=en
- "scanner_udp_probeudpport": "probeUDPPort()" | kind=code-symbol | source=probe-go/scanner/udp.go:L34 | neighbors=[udp.go, ProbeUDP(), dnsVersionQuery(), extractSNMPCommunity(), netbiosNameQuery(), ntpRequest()] | lang=en
- "scanner_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/scanner/windows_collector.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…] | lang=en
- "schemas_auth_currentuser": "CurrentUser" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L20 | neighbors=[Close the global Redis connection pool.…, Reads user claims injected by TenantIso…, FastAPI dependency that enforces role-b…, auth.py, BaseModel, Parsed from JWT claims — attached to re…] | lang=en
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, FindingFilter, FindingOut, FindingPatch, SlaItem] | lang=en
- "services_sla": "sla.py" | kind=code-symbol | source=manager/backend/app/services/sla.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, config.py, compute(), SlaResult, summarize(), _windows()] | lang=en
- "states_datastate_skeletonrows": "SkeletonRows()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L24 | neighbors=[page.tsx, Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx, page.tsx, page.tsx] | lang=en
- "tests_test_agents_testpromoteassets": "TestPromoteAssets" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L259 | neighbors=[test_agents.py, Discovery results → assets/services pro…, ScanJobType, .test_creates_asset_and_services_with_c…, .test_dedupes_duplicate_services_in_sam…, .test_empty_result_is_noop()] | lang=en
- "tests_test_ai_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L24 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_unavailable_without_client(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher()] | lang=en
- "tests_test_attack_paths_rationale_1": "Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci" | kind=entity | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient, GraphVisualizer] | lang=en
- "tests_test_probe_core_testclassifycertainty": "TestClassifyCertainty" | kind=code-symbol | source=probe/tests/test_probe_core.py:L592 | neighbors=[test_probe_core.py, .test_error_overrides(), .test_host_discovery_uncertain(), .test_service_banner_deterministic(), .test_tcp_port_scan_deterministic(), .test_udp_port_scan_uncertain()] | lang=en
- "tests_test_scope_validator": "test_scope_validator.py" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, scope_validator.py, TestFetchEngagementScope, TestMergeExclusions, TestTargetsInExcludes, TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testmergeexclusions": "TestMergeExclusions" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L106 | neighbors=[test_scope_validator.py, .test_both_empty(), .test_empty_engagement_excludes(), .test_empty_job_excludes(), .test_merges_no_duplicates(), .test_none_job_excludes()] | lang=en
- "tests_test_scope_validator_testtargetsinexcludes": "TestTargetsInExcludes" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L62 | neighbors=[test_scope_validator.py, .test_all_excluded_returns_empty(), .test_drops_excluded_ip(), .test_drops_excluded_subnet(), .test_hostname_passes_through(), .test_no_excludes_returns_all()] | lang=en
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=probe/tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_rejects_empty_targets(), .test_rejects_unknown_use_case(), .test_resolves_full_assessment(), .test_resolves_use_case_correctly()] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=probe/tests/test_task_runner.py:L103 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_manager_job_without_scope_fails_c…, .test_merge_engagement_and_job_excludes…, .test_rejects_excluded_target(), .test_rejects_out_of_scope_target()] | lang=en
- "vuln_enrichment_ttlcache_get": ".get()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L56 | neighbors=[TTLCache, .compute_composite_risk(), .enrich(), .fetch_epss(), .fetch_mitre_techniques(), .fetch_nvd()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_all": "._fetch_all()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L341 | neighbors=[Fetch NVD, EPSS, KEV and MITRE concurre…, VulnEnrichmentService, .enrich(), .check_cisa_kev(), .fetch_epss(), .fetch_mitre_techniques()] | lang=en
- "vuln_nessus_nessusscanner_get_client": "._get_client()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L50 | neighbors=[NessusScanner, .create_scan(), .export_nessus_file(), ._auth_headers(), .get_results(), .launch_scan()] | lang=en
- "vuln_tasks_rationale_1": "Background tasks triggered after a vuln scan completes.  Pipeline:   1. Load all" | kind=entity | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=pt
- "vuln_tasks_rationale_171": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L171 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "vuln_tasks_rationale_38": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L38 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "websocket_manager_connectionmanager_broadcast": ".broadcast()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L49 | neighbors=[ConnectionManager, .disconnect(), .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), ._handle_message()] | lang=en
- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L126 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _gather_per_host(), _port_candidates(), _run_passive(), _Sink] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-014.json

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
