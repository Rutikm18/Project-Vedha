# Node Description Batch 22 of 380

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

- "exploit_orchestrator_rationale_71": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L71 | neighbors=[MetasploitRPCClient, .select_exploit(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "graph_builder_graphbuilder_build_asset_graph": ".build_asset_graph()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L99 | neighbors=[GraphBuilder, asset_node_id(), _enum_value(), finding_node_id(), ._add_credential_edges(), .add_exploit_edges()]
- "lib_target_parser": "target-parser.ts" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, COMMON_RANGES, estimateHostCount(), isPrivateRange(), isValidTarget(), ParseResult]
- "main_scripts_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, Delta, DeltaEngine, _extract_service(), _extract_version()]
- "main_scripts_mobile_scanner": "mobile_scanner.py" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), main(), MobileScanner]
- "main_scripts_nfs_scanner": "nfs_scanner.py" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, is_world_readable(), main(), NFSScanner, parse_mount_export(), parse_portmap_dump()]
- "main_scripts_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L339 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._is_ambiguous()]
- "main_scripts_run_all": "run_all.py" | kind=code-symbol | source=probe/main_scripts/run_all.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _advertised_dynamic_ports(), _log()]
- "main_scripts_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L315 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "main_scripts_va_campaign_progressreporter": "ProgressReporter" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L169 | neighbors=[va_campaign.py, build_campaign(), ._current(), ._eta_seconds(), .finish(), ._flush()]
- "main_scripts_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[10fce13 feat(probe): observe web auth s…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _fetch()]
- "native_dir_bust": "dir-bust.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, BUILTIN_PATHS, DirBustResult, loadWordlist()]
- "reject_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, backend.ts, backend(), BackendError]
- "reopen_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, 8ebc053 feat(risk-rank-ui): surface ver…, f473173 merge: network VA accuracy, KEV…, adapters.ts, toUiFinding()]
- "routers_agents_bootstrap_agent": "bootstrap_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L677 | neighbors=[agents.py, AgentRegisterResponse, Allows a probe to register without an a…, Allows a probe to register without an a…, Allows a probe to register without an a…, Allows a probe to register without an a…]
- "routers_agents_jobresultrequest": "JobResultRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L266 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
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
- "routers_engagements_rationale_300": "Offline ingest path: upload a probe's scan export and run it through the     SAM" | kind=entity | source=manager/backend/app/routers/engagements.py:L300 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_301": "Offline ingest path: upload a probe's scan export and run it through the     SAM" | kind=entity | source=manager/backend/app/routers/engagements.py:L301 | neighbors=[import_facts(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_398": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L398 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_399": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L399 | neighbors=[engagements_overview(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_40": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L40 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_41": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L41 | neighbors=[_compute_overview(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_645": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L645 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_668": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L668 | neighbors=[get_engagement_scope(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_97": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_98": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L98 | neighbors=[_refresh_overview_cache(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_exploits_rationale_1": "Exploit validation API.  POST /exploits/run              — request exploit valid" | kind=entity | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[exploits.py, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "routers_exploits_rationale_455": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L455 | neighbors=[_run_approved_exploit(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "routers_exploits_rationale_456": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L456 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_health": "health.py" | kind=code-symbol | source=manager/backend/app/routers/health.py:L1 | neighbors=[3ad95f4 feat: Optimize asset service fe…, 65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, database.py, dependencies.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
