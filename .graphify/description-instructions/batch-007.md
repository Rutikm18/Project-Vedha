# Node Description Batch 8 of 119

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

- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L53 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, configure_siem(), get_coverage(), get_gaps(), get_results()]
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L87 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L70 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "routers_vuln_scans_rationale_279": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L279 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "str": "str" | kind=code-symbol | neighbors=[FindingState, SourceConfidence, AgentStatus, AssetCriticality, AssetType, DetectionStatus]
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection, MicrosoftDefender]
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError]
- "tests_test_nessus_scanner": "test_nessus_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _mock_response(), scanner(), test_authenticate_api_key(), test_create_scan(), test_create_scan_with_credentials()]
- "tests_test_nuclei_background_fakesession": "_FakeSession" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L30 | neighbors=[test_nuclei_background.py, ScanJobStatus, .add(), .__aenter__(), .__aexit__(), .begin_nested()]
- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_cidr_must_be_fully_contained(), .test_empty_targets(), .test_explicit_hostname_scope_allows_ex…, .test_hostname_rejected_when_scope_is_i…, .test_invalid_cidr_ignored()]
- "workers_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, database.py, _claim_batch(), enqueue(), Event, _handle_facts_ready()]
- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L224 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _finalize_trace(), _gather_per_host(), _port_candidates(), _record()]
- "agent_agent_run_ws_push_loop": "_run_ws_push_loop()" | kind=code-symbol | source=probe/agent/agent.py:L319 | neighbors=[agent.py, main(), Persistent WebSocket push loop.      Re…, _flush_spool_over_http(), say(), _ws_heartbeat_sender()]
- "agent_license": "license.py" | kind=code-symbol | source=probe/agent/license.py:L1 | neighbors=[agent.py, _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError]
- "agent_result_spool_resultspool": "ResultSpool" | kind=code-symbol | source=probe/agent/result_spool.py:L26 | neighbors=[result_spool.py, Persists scan results locally and retri…, .exists(), .flush_spool(), .__init__(), .load()]
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()]
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator]
- "auth_router": "router.py" | kind=code-symbol | source=manager/backend/app/auth/router.py:L1 | neighbors=[database.py, dependencies.py, ratelimit.py, create_personal_access_token(), list_personal_access_tokens(), login()]
- "detection_engine_ingest": "ingest.py" | kind=code-symbol | source=manager/detection_engine/ingest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _classify_confidence(), _extract_aliases(), ingest_file(), ingest_files()]
- "detection_engine_version_compare": "version_compare.py" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _char_order(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python()]
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L83 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()]
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "launch_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, a789cca scanner: real use-case library,…, INTENSITY_PRESETS, LaunchBody, POST, backend.ts]
- "lib_backend_backenderror": "BackendError" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L13 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors]
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[AttackLogger, AttackLogger — records every attack act…, Persist a single attack action. Returns…, attack_timeline.py, Base, Base]
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, AssetCriticality, AssetType, DetectionStatus, EngagementStatus]
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L46 | neighbors=[outbox.py, Base, Base, TimestampMixin, TimestampMixin, Event]
- "routers_agents_agentregisterrequest": "AgentRegisterRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L223 | neighbors=[agents.py, BaseModel, Asset, Engagement, AssetType, ScanJobStatus]
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L244 | neighbors=[agents.py, BaseModel, Asset, Engagement, AssetType, ScanJobStatus]
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L62 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L48 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]

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
