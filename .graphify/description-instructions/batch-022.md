# Node Description Batch 23 of 236

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

- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L132 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()] | lang=en
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L120 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()] | lang=en
- "exposure_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 5d5c158 refactor: remove unused dashboa…, Exposure, GET, backend.ts, backend()] | lang=en
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder] | lang=en
- "hooks_usetoast_usetoast": "useToast()" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L6 | neighbors=[page.tsx, page.tsx, page.tsx, page.tsx, useToast.ts, page.tsx] | lang=en
- "lib_clients_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L52 | neighbors=[clients-store.ts, createClient(), getClient(), getClientBySubdomain(), listClients(), ensureDir()] | lang=en
- "lib_permissions_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L25 | neighbors=[permissions-store.ts, addUser(), getAllUsers(), getUser(), isEmailAllowed(), isScopeAllowed()] | lang=en
- "main_scripts_service_banner": "service_banner.py" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _dec(), main(), match_service()] | lang=en
- "models_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/models/agent.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Enum, Agent] | lang=en
- "register_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, toUiAgent(), backend(), withBackend(), GET, 2885afa Add comprehensive probe testing…] | lang=en
- "reopen_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L1 | neighbors=[8ebc053 feat(risk-rank-ui): surface ver…, adapters.ts, toUiFinding(), backend.ts, backend(), BackendError] | lang=en
- "request_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), isEmailAllowed(), POST(), 2885afa Add comprehensive probe testing…] | lang=en
- "routers_ad_rationale_1": "Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun" | kind=entity | source=manager/backend/app/routers/ad.py:L1 | neighbors=[ad.py, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_ad_rationale_135": "Background task: run the AD assessment and persist findings + job result." | kind=entity | source=manager/backend/app/routers/ad.py:L135 | neighbors=[_run_ad_assessment_and_save(), ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_agents_bootstrap_agent": "bootstrap_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L629 | neighbors=[agents.py, AgentRegisterResponse, Allows a probe to register without an a…, Allows a probe to register without an a…, Allows a probe to register without an a…, Allows a probe to register without an a…] | lang=en
- "routers_agents_rationale_106": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L106 | neighbors=[_scope_is_reachable(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=pt
- "routers_agents_rationale_142": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L142 | neighbors=[_job_reachability_scope(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_agents_rationale_210": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L210 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_709": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L709 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_93": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L93 | neighbors=[_required_scan_type(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L270 | neighbors=[vuln_scans.py, Run Nuclei and always leave its job in …, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result()] | lang=en
- "scanner_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L286 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), ._icmp_timestamp(), .__init__(), .scan_target()] | lang=en
- "scanner_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L324 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…, One connect() and its classification. A…] | lang=en
- "scanner_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L596 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…] | lang=en
- "schemas_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, AiGenerateRequest, AiGenerateResponse] | lang=en
- "scripts_startup_validator_run_all_validators": "run_all_validators()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L396 | neighbors=[startup_validator.py, Run all validators. Use in FastAPI life…, CheckResult, DatabaseConnectivityValidator, RedisConnectivityValidator, ValidationReport] | lang=en
- "services_agent_policy": "agent_policy.py" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, classify_action(), Decision, _deny(), evaluate_action()] | lang=en
- "services_job_result_service_process_job_result": "process_job_result()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L147 | neighbors=[job_result_service.py, _promote_assets(), result_checksum(), sanitize_jsonb(), validate_result_scope(), Process a scan job result.  Called from…] | lang=en
- "services_job_result_service_promote_assets": "_promote_assets()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L422 | neighbors=[job_result_service.py, process_job_result(), _apply_device_profile(), Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…] | lang=en
- "services_llm_managerllmservice_dispatch": "._dispatch()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L251 | neighbors=[ManagerLlmService, AiRuntimeError, ._anthropic(), ._ollama(), ._openai(), ._openrouter()] | lang=en
- "services_remediation_kb": "remediation_kb.py" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, classify_finding(), _cves(), os_key(), recipe_for_finding()] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine": "TestWindowStateMachine" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L27 | neighbors=[test_adaptive_rate.py, .test_congestion_avoidance_grows_sublin…, .test_initial_window(), .test_loss_halves_window(), .test_loss_sets_ssthresh_to_half(), .test_recovery_after_loss_enters_conges…] | lang=en
- "tests_test_agent_read_tools": "test_agent_read_tools.py" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L1 | neighbors=[3ad95f4 feat: Optimize asset service fe…, _asset(), _FakeSession, _Result, _svc(), test_list_assets_batches_services_no_n_…] | lang=en
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "tests_test_auth_login_make_user": "_make_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L44 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future(), .test_raises_expired_password()] | lang=en
- "tests_test_auth_login_testreasoncodes": "TestReasonCodes" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L223 | neighbors=[test_auth_login.py, Ensure every exception class has the ex…, .test_bcrypt_failure_code(), .test_database_failure_code(), .test_disabled_tenant_code(), .test_disabled_user_code()] | lang=en
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-022.json

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
