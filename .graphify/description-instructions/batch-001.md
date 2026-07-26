# Node Description Batch 2 of 104

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "detection_engine_vuln_db_snapshotmeta": "SnapshotMeta" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L70 | neighbors=[vuln_db.py, load_snapshot(), Detection engine test suite — unit test…, TestAggregate, TestAllOsvSourcePackages, TestAsset]
- "models_enums_assettype": "AssetType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L19 | neighbors=[Convert a probe's self-assessed `findin…, Find the Asset for a probe-reported tar…, A still-relevant Finding with the same …, Convert a probe's self-assessed `findin…, DiscoveryJobPayload, DiscoveryWorker]
- "models_scan_result_scanresult": "ScanResult" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L10 | neighbors=[scan_result.py, Append-only raw probe facts (P3-#10).  …, Base, Base, TimestampMixin, TimestampMixin]
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, llm.ts, ask.ts, findings.ts, interactive.ts]
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset, AttackPath]
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, admin.ts, buildAdminCommand(), ask.ts, buildAskCommand(), doctor.ts]
- "pipeline_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, findings-store.ts, createFinding(), nuclei-parser.ts, countBySeverity(), nucleiMatchToFinding()]
- "exploit_safety_approvalrequirederror": "ApprovalRequiredError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L28 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "exploit_safety_blastradiusexceedederror": "BlastRadiusExceededError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L24 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L51 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[findings.ts, interactive.ts, scan.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, types.ts]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[route.ts, route.ts, route.ts, route.ts, 298a9d4 trim frontend to 7 core pages; …, ADJ]
- "models_base_timestampmixin": "TimestampMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L13 | neighbors=[Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset, AttackPath]
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract()]
- "agent_cli": "cli.py" | kind=code-symbol | source=probe/agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]
- "scan_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1 | neighbors=[0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), useToast.ts]
- "tests_test_detection_core_testverify": "TestVerify" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L637 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "id_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), useToast.ts, useToast()]
- "lib_agents_store": "agents-store.ts" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, route.ts, Agent, AgentCapability, AGENTS, agentsStore]
- "tests_test_detection_validation_testdetectioncorrelator": "TestDetectionCorrelator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L49 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L39 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "lib_detection_store": "detection-store.ts" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, route.ts, ATTACK_TIMELINE, AttackAction, computeCoverage()]
- "ad_adcs_adcschecker": "ADCSChecker" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L52 | neighbors=[adcs.py, .check_esc1(), .check_esc4(), .check_esc8(), ._enrollment_principals(), .enumerate_templates()]
- "agent_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L1 | neighbors=[agent.py, AgentState, mergeHosts(), persistAgentFindings(), Risk, runOnePhase()]
- "app_dependencies": "dependencies.py" | kind=code-symbol | source=manager/backend/app/dependencies.py:L1 | neighbors=[config.py, database.py, close_redis(), get_current_user(), get_redis(), main.py]
- "scanner_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1 | neighbors=[engine.py, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, base_argparser()]
- "tests_test_detection_core_testversioninranges": "TestVersionInRanges" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L312 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[GraphBuilder, GraphBuilder — turns engagement assets/…, Build the full multi-type attack graph.…, For each exploitable finding add an EXP…, Add CONNECTS_TO (directed reachability)…, CREDENTIAL_REUSE edges between assets s…]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[admin.ts, 298a9d4 trim frontend to 7 core pages; …, auth-middleware.ts, addUser(), DATA_PATH, ensureDir()]
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L726 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "workflow_workflow_engine": "workflow_engine.py" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L1 | neighbors=[engine.py, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, db_scanner.py, host_discovery.py, mcp_ai_scanner.py]
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()]
- "ad_kerberoast_kerberoastchecker": "KerberoastChecker" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L40 | neighbors=[kerberoast.py, ._encode_tgs_rep(), .generate_finding(), .get_spn_accounts(), ._pwd_last_set(), .request_tgs()]
- "ad_ldap_enum_ace": "ACE" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L85 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…, ESC1: enrollee supplies subject + clien…, ESC4: a low-privilege principal holds a…]
- "lib_backend": "backend.ts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L1 | neighbors=[route.ts, route.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, route.ts, route.ts]
- "models_exploit_approval_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L19 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "models_exploit_result_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L11 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "vuln_enrichment_vulnenrichmentservice": "VulnEnrichmentService" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L91 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Background task: run nuclei, persist fi…, Unit tests for VulnEnrichmentService — …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-001.json

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
