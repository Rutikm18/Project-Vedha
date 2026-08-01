# Node Description Batch 10 of 119

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L271 | neighbors=[agents.py, BaseModel, Asset, Engagement, AssetType, ScanJobStatus]
- "routers_agents_heartbeatrequest": "HeartbeatRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L249 | neighbors=[agents.py, BaseModel, Asset, Engagement, AssetType, ScanJobStatus]
- "routers_agents_jobresultrequest": "JobResultRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L265 | neighbors=[agents.py, BaseModel, Asset, Engagement, AssetType, ScanJobStatus]
- "routers_detection_runrequest": "RunRequest" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L51 | neighbors=[detection.py, BaseModel, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig]
- "routers_detection_siemconfigin": "SIEMConfigIn" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L44 | neighbors=[detection.py, BaseModel, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig]
- "routers_engagements_rationale_128": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L128 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_129": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L129 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_161": "Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s" | kind=entity | source=manager/backend/app/routers/engagements.py:L161 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_162": "Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s" | kind=entity | source=manager/backend/app/routers/engagements.py:L162 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_179": "Parse a probe export into (facts, scan_type).      Accepts two shapes the probe" | kind=entity | source=manager/backend/app/routers/engagements.py:L179 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_180": "Parse a probe export into (facts, scan_type).      Accepts two shapes the probe" | kind=entity | source=manager/backend/app/routers/engagements.py:L180 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_226": "Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen" | kind=entity | source=manager/backend/app/routers/engagements.py:L226 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_227": "Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen" | kind=entity | source=manager/backend/app/routers/engagements.py:L227 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_300": "Offline ingest path: upload a probe's scan export and run it through the     SAM" | kind=entity | source=manager/backend/app/routers/engagements.py:L300 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_301": "Offline ingest path: upload a probe's scan export and run it through the     SAM" | kind=entity | source=manager/backend/app/routers/engagements.py:L301 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_398": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L398 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_399": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L399 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_40": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L40 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_41": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L41 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_645": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L645 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_668": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L668 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_97": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_98": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L98 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_exploits_rationale_1": "Exploit validation API.  POST /exploits/run              — request exploit valid" | kind=entity | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_exploits_rationale_456": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L456 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_vuln_scans_rationale_272": "Background task: run nuclei, persist findings, trigger enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L272 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_safe": "safe.go" | kind=code-symbol | source=probe-go/scanner/safe.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, CircuitBreaker, RetryConfig, backoff(), DialContext(), IsRefused()]
- "scanner_udp": "udp.go" | kind=code-symbol | source=probe-go/scanner/udp.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, buildSNMPGetRequest(), dnsVersionQuery(), extractSNMPCommunity(), netbiosNameQuery(), ntpRequest()]
- "tests_test_ad_assessment_rationale_1": "Unit tests for the Active Directory assessment module (Prompt 5).  All directory" | kind=entity | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker, ACE]
- "tests_test_agents_testagentjobcompatibility": "TestAgentJobCompatibility" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L377 | neighbors=[test_agents.py, ScanJobType, .test_agent_network_segments_are_normal…, .test_declared_segment_must_cover_entir…, .test_declared_segment_rejects_missing_…, .test_empty_capabilities_receive_no_job…]
- "tests_test_nuclei_scanner_fakeprocess": "FakeProcess" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L30 | neighbors=[test_nuclei_scanner.py, .__init__(), .kill(), .terminate(), .wait(), NucleiScanError]
- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=probe/tests/test_probe_core.py:L300 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_explicit_snmp_does_not_require_tc…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port()]
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=probe/tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_explicit_empty_targets_never_expa…, .test_rejects_empty_targets(), .test_rejects_non_object_params(), .test_rejects_non_string_target()]
- "tests_test_use_cases": "test_use_cases.py" | kind=code-symbol | source=probe/tests/test_use_cases.py:L1 | neighbors=[01f4398 feat(probe): IoT survey reaches…, 5c8e696 docs(probe): correct overclaimi…, 95904f1 feat(probe): detect SMB signing…, bce780a feat(probe): enumerate HTTP met…, fe868e6 feat(probe): real UDP amplifica…, use_cases.py]
- "tests_test_xml_parser_testnmapxmlparser": "TestNmapXMLParser" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L42 | neighbors=[test_xml_parser.py, NmapXMLParser, .setup_method(), .test_cpe_extraction(), .test_empty_scan(), .test_empty_string()]
- "tools_installer_installtool": "installTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L156 | neighbors=[tools.ts, installer.ts, installAll(), downloadFile(), extract(), getInstalledRecord()]
- "workflow_execution": "execution.py" | kind=code-symbol | source=probe/workflow/execution.py:L1 | neighbors=[engine.py, b4b12a9 Rename project and update files, test_passive_collector.py, test_workflow_execution.py, scanner_base.py, classify_scanner_error()]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L226 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L29 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()]
- "app_main": "main.py" | kind=code-symbol | source=manager/backend/app/main.py:L1 | neighbors=[config.py, dependencies.py, GzipRequestMiddleware, lifespan(), _service_root(), unhandled_exception_handler()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-009.json

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
