# Node Description Batch 9 of 119

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

- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors]
- "lib_with_backend_withbackend": "withBackend()" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L22 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[AttackLogger, AttackLogger — records every attack act…, Persist a single attack action. Returns…, attack_timeline.py, Base, Base]
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, AssetCriticality, AssetType, DetectionStatus, EngagementStatus]
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L46 | neighbors=[outbox.py, Base, Base, TimestampMixin, TimestampMixin, Event]
- "routers_agents_agentregisterrequest": "AgentRegisterRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L220 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L241 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L61 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L47 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L65 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, finding_summary()]
- "routers_vuln_scans_rationale_278": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L278 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _have_nmap(), main(), NmapExecutionError, _parse_nmap_xml()]
- "tests_test_ad_assessment": "test_ad_assessment.py" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _enum_with_entries(), _FakeAttr, _FakeEntry, TestADCSChecker, TestASREPRoastChecker]
- "tests_test_external_engine_wrappers": "test_external_engine_wrappers.py" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L1 | neighbors=[b4b12a9 Rename project and update files, mass_scan.py, nmap_wrapper.py, scanner_base.py, test_masscan_nonzero_with_valid_output_…, test_masscan_range_must_be_fully_in_sco…]
- "tests_test_probe_core_testscopeguard": "TestScopeGuard" | kind=code-symbol | source=probe/tests/test_probe_core.py:L79 | neighbors=[test_probe_core.py, .test_assert_in_scope_passes(), .test_assert_in_scope_raises(), .test_excludes_larger_subnet(), .test_excludes_override_allowlist(), .test_filter_yields_only_in_scope()]
- "ui_output_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L30 | neighbors=[output.ts, banner(), findingDetail(), findingLine(), findingsTable(), hostLine()]
- "workflow_execution_executiontrace": "ExecutionTrace" | kind=code-symbol | source=probe/workflow/execution.py:L231 | neighbors=[execution.py, .as_list(), .degraded(), ._ensure(), .failed(), .finalize()]
- "agent_cli_cmd_validate": "cmd_validate()" | kind=code-symbol | source=probe/agent/cli.py:L573 | neighbors=[cli.py, CliError, _fetch_all_findings(), _manager_is_local(), ManagerClient, .request()]
- "agent_cli_output": "output()" | kind=code-symbol | source=probe/agent/cli.py:L177 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()]
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=probe/agent/engine.py:L366 | neighbors=[engine.py, Execute a scan and return the enriched …, _build_run_stats(), _error_result(), _facts_from_cache(), _job_runtime_seconds()]
- "ai_llm_report": "llm_report.py" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[_collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, LLMUnavailableError, _uuid()]
- "ai_prioritizer_vulnprioritizer": "VulnPrioritizer" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L99 | neighbors=[prioritizer.py, .explain_prediction(), .fallback_score(), ._formula_contributions(), .__init__(), .is_trained()]
- "approve_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/approve/route.ts:L1 | neighbors=[POST(), backend.ts, backend(), BackendError, bearerFrom(), 10dfc80 Add comprehensive probe testing…]
- "commands_admin": "admin.ts" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildAdminCommand(), c, PermittedUser, 10dfc80 Add comprehensive probe testing…]
- "commands_login": "login.ts" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L1 | neighbors=[loadSession(), saveSession(), serverUrl(), buildLoginCommand(), prompt(), promptSilent()]
- "components_sidebar": "Sidebar.tsx" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, NAV_SECTIONS, NavItem]
- "detection_correlator_detectiongap": "DetectionGap" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L61 | neighbors=[correlator.py, .generate_gap_report(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_siem_elasticsiem": "ElasticSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L184 | neighbors=[siem.py, .build_query(), .parse_response(), .query_alerts(), SIEMQueryEngine, Elasticsearch via the _search API (KQL/…]
- "detection_siem_sentinelsiem": "SentinelSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L134 | neighbors=[siem.py, Microsoft Sentinel via the Azure Monito…, .build_kql(), .parse_response(), .query_alerts(), SIEMQueryEngine]
- "detection_siem_splunksiem": "SplunkSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L81 | neighbors=[siem.py, Splunk via the REST search endpoint (``…, SIEMQueryEngine, .build_spl(), .parse_response(), .query_alerts()]
- "discovery_worker_discoveryjobpayload": "DiscoveryJobPayload" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L42 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, .__post_init__(), NmapXMLParser, ParsedHost]
- "engine_types_discoveredhost": "DiscoveredHost" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L63 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "exploit_orchestrator_rationale_1": "ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[MetasploitRPCClient, orchestrator.py, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_107": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L107 | neighbors=[MetasploitRPCClient, .validate_safety(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_114": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L114 | neighbors=[MetasploitRPCClient, .validate_scope(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]

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
