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

- "exploit_orchestrator_rationale_134": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L134 | neighbors=[MetasploitRPCClient, .execute(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_256": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L256 | neighbors=[MetasploitRPCClient, .generate_dns_callback_token(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_269": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L269 | neighbors=[MetasploitRPCClient, ._check_blast_radius(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_300": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L300 | neighbors=[MetasploitRPCClient, ._check_approval_required(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_46": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L46 | neighbors=[MetasploitRPCClient, ExploitOrchestrator, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_71": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L71 | neighbors=[MetasploitRPCClient, .select_exploit(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "graph_builder_graphbuilder_build_asset_graph": ".build_asset_graph()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L99 | neighbors=[GraphBuilder, asset_node_id(), _enum_value(), finding_node_id(), ._add_credential_edges(), .add_exploit_edges()]
- "lib_target_parser": "target-parser.ts" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, COMMON_RANGES, estimateHostCount(), isPrivateRange(), isValidTarget(), ParseResult]
- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, backend.ts, backend(), BackendError]
- "native_dir_bust": "dir-bust.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, BUILTIN_PATHS, DirBustResult, loadWordlist()]
- "reject_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, backend.ts, backend(), BackendError]
- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L268 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_agents_heartbeatrequest": "HeartbeatRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L246 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_agents_jobresultrequest": "JobResultRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L262 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
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
- "routers_exploits_rationale_455": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L455 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_exploits_rationale_456": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L456 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_vuln_scans_rationale_272": "Background task: run nuclei, persist findings, trigger enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L272 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "tests_test_ad_assessment_rationale_1": "Unit tests for the Active Directory assessment module (Prompt 5).  All directory" | kind=entity | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker, ACE]
- "tests_test_agents_testagentjobcompatibility": "TestAgentJobCompatibility" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L377 | neighbors=[test_agents.py, ScanJobType, .test_agent_network_segments_are_normal…, .test_declared_segment_must_cover_entir…, .test_declared_segment_rejects_missing_…, .test_empty_capabilities_receive_no_job…]

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
