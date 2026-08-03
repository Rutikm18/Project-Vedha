# Node Description Batch 2 of 131

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

- "tests_test_probe_core_asset": "_asset()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L71 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "tests_test_detection_core": "test_detection_core.py" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, _candidate(), _fact(), _finding(), _mock_epss_db(), _mock_kev_db()]
- "detection_engine_consistency_findingconsistency": "FindingConsistency" | kind=code-symbol | source=manager/detection_engine/consistency.py:L50 | neighbors=[consistency.py, aggregate(), .ci(), .classification(), .rate(), Finding]
- "engine_scanner": "scanner.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L1 | neighbors=[tools.ts, interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, modulesForPorts(), bySeverityCount()]
- "detection_engine_consistency_consistencyreport": "ConsistencyReport" | kind=code-symbol | source=manager/detection_engine/consistency.py:L86 | neighbors=[consistency.py, aggregate(), .intermittent(), .stable(), Finding, Detection engine test suite — unit test…]
- "detection_engine_verifier_evidencetier": "EvidenceTier" | kind=code-symbol | source=manager/detection_engine/verifier.py:L41 | neighbors=[verifier.py, IntEnum, Finding, FindingState, SourceConfidence, Detection engine test suite — unit test…]
- "exploit_safety_approvalrequirederror": "ApprovalRequiredError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L28 | neighbors=[safety.py, Exception, .__init__(), Raised when a high-risk target requires…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "lib_backend": "backend.ts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L1 | neighbors=[route.ts, route.ts, route.ts, route.ts, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "exploit_safety_blastradiusexceedederror": "BlastRadiusExceededError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L24 | neighbors=[safety.py, Exception, Raised when a job would exceed the maxi…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "exploit_safety_safetyviolationerror": "SafetyViolationError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L16 | neighbors=[safety.py, Raised when a requested payload or modu…, Exception, validate_module(), validate_payload(), ApprovalOut]
- "id_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), useToast.ts]
- "routers_agents": "agents.py" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1 | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, a789cca scanner: real use-case library,…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …]
- "detection_engine_vuln_db_snapshotmeta": "SnapshotMeta" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L70 | neighbors=[vuln_db.py, load_snapshot(), Detection engine test suite — unit test…, TestAggregate, TestAllOsvSourcePackages, TestAsset]
- "aibrain_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L1 | neighbors=[AIBrainPage(), AiStatus, Engagement, Message, providerLabel(), STARTER_PROMPTS]
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L51 | neighbors=[enums.py, str, AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO]
- "scan_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, a789cca scanner: real use-case library,…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx]
- "agent_cli": "cli.py" | kind=code-symbol | source=probe/agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]
- "agent_engine": "engine.py" | kind=code-symbol | source=probe/agent/engine.py:L1 | neighbors=[_applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _env_number(), _error_result()]
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, buildAdminCommand(), buildAskCommand(), buildDoctorCommand(), buildEngagementCommand(), buildFindingsCommand()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cac022c40e254cd92ba6e8c73c79c0987b8650d2": "cac022c Everything is done and verified. Here's the wrap-up.What I did (as an a…" | kind=Commit | source=git | neighbors=[c5e2d0e chore: retire probe-go to spike…, kerberoast.py, ldap_enum.py, agent.py, license.py, task_runner.py]
- "tests_test_workflow_execution": "test_workflow_execution.py" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, port_scanner.py, scanner_base.py, _ConcurrencyScanner, _ExplodingScanner]
- "workflow_workflow_engine": "workflow_engine.py" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, bb0ef3d feat(probe): route DB services …, d1b4dd3 trim frontend to 7 core pages; …, test_passive_collector.py, test_workflow_execution.py]
- "branch:repo:github.com/Rutikm18/Project-Vedha#main": "main" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[base.py, DeclarativeBase, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…]
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, AgentJob]
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[safety.py, Exception, Raised when a target IP is outside the …, validate_scope(), ApprovalOut, ApproveRequest]
- "settings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), fetcher.ts]
- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, DiscoveredHost, LiveFinding, ScanSummary]
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, Evidence, LiveFinding, Severity]
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, ADJ, adjacency(), ATTACK_PATHS, AttackPath]
- "models_exploit_approval_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L19 | neighbors=[exploit_approval.py, Base, TimestampMixin, Created when a high-risk target require…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "models_exploit_result_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L11 | neighbors=[exploit_result.py, Base, TimestampMixin, Immutable record of every exploit attem…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract()]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=probe/agent/transport.py:L77 | neighbors=[transport.py, HTTP (+ future WebSocket) transport to …, .activate_enrollment(), .agent_id(), .agent_token(), .auth_header()]
- "scanner_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, base_argparser()]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "models_audit_log_auditlog": "AuditLog" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L11 | neighbors=[audit_log.py, Base, Immutable, append-only audit trail for …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "models_base_timestampmixin": "TimestampMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L13 | neighbors=[base.py, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset]
- "models_exploit_approval_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L12 | neighbors=[exploit_approval.py, str, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…]
- "routers_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, config.py, dependencies.py, activate_enrollment(), approve_enrollment(), _authenticated_request()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-001.json

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
