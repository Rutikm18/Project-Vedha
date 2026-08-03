# Node Description Batch 10 of 131

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

- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=probe/agent/task_runner.py:L1 | neighbors=[JobResult, TaskRunner, use_cases.py, task_runner.py — orchestrates the full …, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "agent_transport_transport_update_state": ".update_state()" | kind=code-symbol | source=probe/agent/transport.py:L179 | neighbors=[Merge and atomically persist private st…, Transport, .activate_enrollment(), .clear_state(), .refresh_device_access(), .refresh_registration()]
- "ai_llm_report": "llm_report.py" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[_collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, LLMUnavailableError, _uuid()]
- "ai_prioritizer_vulnprioritizer": "VulnPrioritizer" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L99 | neighbors=[prioritizer.py, .explain_prediction(), .fallback_score(), ._formula_contributions(), .__init__(), .is_trained()]
- "approve_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/approve/route.ts:L1 | neighbors=[POST(), backend.ts, backend(), BackendError, bearerFrom(), 10dfc80 Add comprehensive probe testing…]
- "auth_exceptions_authenticationerror": "AuthenticationError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L28 | neighbors=[exceptions.py, VedhaAuthError, BcryptFailureError, DatabaseFailureError, DisabledTenantError, DisabledUserError]
- "commands_admin": "admin.ts" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildAdminCommand(), c, PermittedUser, 10dfc80 Add comprehensive probe testing…]
- "commands_login": "login.ts" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L1 | neighbors=[loadSession(), saveSession(), serverUrl(), buildLoginCommand(), prompt(), promptSilent()]
- "detection_correlator_detectiongap": "DetectionGap" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L61 | neighbors=[correlator.py, .generate_gap_report(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_siem_elasticsiem": "ElasticSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L184 | neighbors=[siem.py, .build_query(), .parse_response(), .query_alerts(), SIEMQueryEngine, Elasticsearch via the _search API (KQL/…]
- "detection_siem_sentinelsiem": "SentinelSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L134 | neighbors=[siem.py, Microsoft Sentinel via the Azure Monito…, .build_kql(), .parse_response(), .query_alerts(), SIEMQueryEngine]
- "detection_siem_splunksiem": "SplunkSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L81 | neighbors=[siem.py, Splunk via the REST search endpoint (``…, SIEMQueryEngine, .build_spl(), .parse_response(), .query_alerts()]
- "discovery_worker_discoveryjobpayload": "DiscoveryJobPayload" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L42 | neighbors=[worker.py, .__post_init__(), RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost]
- "engine_types_discoveredhost": "DiscoveredHost" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L63 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "exploit_orchestrator_rationale_1": "ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[orchestrator.py, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_107": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L107 | neighbors=[MetasploitRPCClient, .validate_safety(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_114": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L114 | neighbors=[MetasploitRPCClient, .validate_scope(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_134": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L134 | neighbors=[MetasploitRPCClient, .execute(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_256": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L256 | neighbors=[MetasploitRPCClient, .generate_dns_callback_token(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_269": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L269 | neighbors=[MetasploitRPCClient, ._check_blast_radius(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_300": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L300 | neighbors=[MetasploitRPCClient, ._check_approval_required(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_46": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L46 | neighbors=[MetasploitRPCClient, ExploitOrchestrator, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_71": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L71 | neighbors=[MetasploitRPCClient, .select_exploit(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "graph_builder_graphbuilder_build_asset_graph": ".build_asset_graph()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L99 | neighbors=[GraphBuilder, asset_node_id(), _enum_value(), finding_node_id(), ._add_credential_edges(), .add_exploit_edges()]
- "hooks_usetoast": "useToast.ts" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, page.tsx, page.tsx, page.tsx, ToastContext, useToast()]
- "lib_target_parser": "target-parser.ts" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, COMMON_RANGES, estimateHostCount(), isPrivateRange(), isValidTarget(), ParseResult]
- "native_dir_bust": "dir-bust.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, BUILTIN_PATHS, DirBustResult, loadWordlist()]
- "reject_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, backend.ts, backend(), BackendError]
- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L288 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_agents_jobresultrequest": "JobResultRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L280 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_detection_runrequest": "RunRequest" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L51 | neighbors=[detection.py, BaseModel, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig]
- "routers_detection_siemconfigin": "SIEMConfigIn" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L44 | neighbors=[detection.py, BaseModel, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig]
- "routers_engagements_rationale_128": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L128 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_129": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L129 | neighbors=[re_detect(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_161": "Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s" | kind=entity | source=manager/backend/app/routers/engagements.py:L161 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_162": "Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s" | kind=entity | source=manager/backend/app/routers/engagements.py:L162 | neighbors=[_read_capped(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_179": "Parse a probe export into (facts, scan_type).      Accepts two shapes the probe" | kind=entity | source=manager/backend/app/routers/engagements.py:L179 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_180": "Parse a probe export into (facts, scan_type).      Accepts two shapes the probe" | kind=entity | source=manager/backend/app/routers/engagements.py:L180 | neighbors=[_parse_probe_file(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_226": "Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen" | kind=entity | source=manager/backend/app/routers/engagements.py:L226 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_227": "Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen" | kind=entity | source=manager/backend/app/routers/engagements.py:L227 | neighbors=[_promote_from_facts(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]

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
