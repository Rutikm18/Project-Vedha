# Node Description Batch 9 of 131

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

- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_cidr_must_be_fully_contained(), .test_empty_targets(), .test_explicit_hostname_scope_allows_ex…, .test_hostname_rejected_when_scope_is_i…, .test_invalid_cidr_ignored()] | lang=en
- "tests_test_validation": "test_validation.py" | kind=code-symbol | source=probe/tests/test_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, validation.py, FakeClient, _preflight_responses(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…] | lang=en
- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L224 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _finalize_trace(), _gather_per_host(), _port_candidates(), _record()] | lang=en
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()] | lang=en
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator] | lang=en
- "auth_startup_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L51 | neighbors=[startup.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a789cca150b7688941e2f9229631f493d3fab094": "a789cca scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, main, spike/probe-go, 10dfc80 Add comprehensive probe testing…, route.ts] | lang=pt
- "components_sidebar": "Sidebar.tsx" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, NAV_SECTIONS] | lang=en
- "components_themeprovider": "ThemeProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L1 | neighbors=[layout.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, subscribeToHydration()] | lang=en
- "detection_engine_ingest": "ingest.py" | kind=code-symbol | source=manager/detection_engine/ingest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _classify_confidence(), _extract_aliases(), ingest_file(), ingest_files()] | lang=en
- "detection_engine_version_compare": "version_compare.py" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _char_order(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python()] | lang=en
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L40 | neighbors=[xml_parser.py, .parse(), ._parse_host(), ._parse_port(), Parse nmap -oX XML into a list of Parse…, DiscoveryJobPayload] | lang=en
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L83 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()] | lang=en
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts] | lang=en
- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore] | lang=en
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors] | lang=en
- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …, backend.ts, backend()] | lang=en
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[attack_timeline.py, Base, TimestampMixin, Append-only ledger of every attack acti…, AttackLogger, AttackLogger — records every attack act…] | lang=en
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, AssetCriticality, AssetType, DetectionStatus, EngagementStatus] | lang=en
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L46 | neighbors=[outbox.py, Base, TimestampMixin, Base, TimestampMixin, Event] | lang=en
- "routers_agents_agentregisterrequest": "AgentRegisterRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L228 | neighbors=[agents.py, BaseModel, .validate_network_segments(), Asset, Engagement, ScanJobStatus] | lang=en
- "routers_agents_heartbeatrequest": "HeartbeatRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L254 | neighbors=[agents.py, BaseModel, .require_fence_for_running_job(), Asset, Engagement, ScanJobStatus] | lang=en
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult] | lang=en
- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[_run_generation(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult] | lang=en
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[_run_regeneration(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult] | lang=en
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L61 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=en
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L47 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=en
- "routers_exploits_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L65 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError] | lang=en
- "routers_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, finding_summary()] | lang=en
- "routers_vuln_scans_rationale_278": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L278 | neighbors=[_run_nuclei_and_save(), Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "scanner_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _have_nmap(), main(), NmapExecutionError, _parse_nmap_xml()] | lang=en
- "tests_test_ad_assessment": "test_ad_assessment.py" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _enum_with_entries(), _FakeAttr, _FakeEntry, TestADCSChecker, TestASREPRoastChecker] | lang=en
- "tests_test_agents_testagentjobcompatibility": "TestAgentJobCompatibility" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L405 | neighbors=[test_agents.py, .test_agent_network_segments_are_normal…, .test_declared_segment_must_cover_entir…, .test_declared_segment_rejects_missing_…, .test_empty_capabilities_receive_no_job…, .test_empty_segments_are_fail_closed()] | lang=en
- "tests_test_external_engine_wrappers": "test_external_engine_wrappers.py" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L1 | neighbors=[b4b12a9 Rename project and update files, mass_scan.py, nmap_wrapper.py, scanner_base.py, test_masscan_nonzero_with_valid_output_…, test_masscan_range_must_be_fully_in_sco…] | lang=en
- "tests_test_probe_core_testscopeguard": "TestScopeGuard" | kind=code-symbol | source=probe/tests/test_probe_core.py:L79 | neighbors=[test_probe_core.py, .test_assert_in_scope_passes(), .test_assert_in_scope_raises(), .test_excludes_larger_subnet(), .test_excludes_override_allowlist(), .test_filter_yields_only_in_scope()] | lang=en
- "ui_output_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L30 | neighbors=[output.ts, banner(), findingDetail(), findingLine(), findingsTable(), hostLine()] | lang=en
- "workflow_execution_executiontrace": "ExecutionTrace" | kind=code-symbol | source=probe/workflow/execution.py:L231 | neighbors=[execution.py, .as_list(), .degraded(), ._ensure(), .failed(), .finalize()] | lang=en
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L992 | neighbors=[agent.py, main(), _enroll_device(), _load_or_create_identity(), _load_or_create_signing_identity(), say()] | lang=en
- "agent_cli_cmd_validate": "cmd_validate()" | kind=code-symbol | source=probe/agent/cli.py:L573 | neighbors=[cli.py, CliError, _fetch_all_findings(), _manager_is_local(), ManagerClient, .request()] | lang=en
- "agent_cli_output": "output()" | kind=code-symbol | source=probe/agent/cli.py:L177 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()] | lang=en

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
