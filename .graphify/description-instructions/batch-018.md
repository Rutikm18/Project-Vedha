# Node Description Batch 19 of 336

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

- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L22 | neighbors=[page.tsx, page.tsx, page.tsx, PageShell.tsx, page.tsx, page.tsx]
- "customers_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, c4386e4 feat(customers): operator Custo…, e3958e7 feat(customers): reveal + copy …, PageShell.tsx, PageShell(), ClientUserResp]
- "cve_cli": "cli.py" | kind=code-symbol | source=probe/cve/cli.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_parser(), cmd_correlate(), cmd_ingest(), cmd_status(), main()]
- "cve_correlator": "correlator.py" | kind=code-symbol | source=probe/cve/correlator.py:L1 | neighbors=[6e2818f Add support for additional serv…, _as_dict(), _backport_marker(), correlate(), CVEFinding, mirror_age_note()]
- "detection_correlator_detectiongap": "DetectionGap" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L62 | neighbors=[correlator.py, .generate_gap_report(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_engine_correlate": "correlate.py" | kind=code-symbol | source=manager/detection_engine/correlate.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, correlate_smb_patch(), dedup_findings()]
- "detection_engine_pipeline": "pipeline.py" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 26ea68c Add comprehensive tests for OS …, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …]
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[0236a60 fix(detection): full EPSS catal…, d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context()]
- "detection_siem_elasticsiem": "ElasticSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L184 | neighbors=[siem.py, .build_query(), .parse_response(), .query_alerts(), SIEMQueryEngine, Elasticsearch via the _search API (KQL/…]
- "detection_siem_sentinelsiem": "SentinelSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L134 | neighbors=[siem.py, Microsoft Sentinel via the Azure Monito…, .build_kql(), .parse_response(), .query_alerts(), SIEMQueryEngine]
- "detection_siem_splunksiem": "SplunkSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L81 | neighbors=[siem.py, Splunk via the REST search endpoint (``…, SIEMQueryEngine, .build_spl(), .parse_response(), .query_alerts()]
- "discovery_worker_discoveryjobpayload": "DiscoveryJobPayload" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L42 | neighbors=[worker.py, .__post_init__(), RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost]
- "engine_types_discoveredhost": "DiscoveredHost" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L63 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "exception": "Exception" | kind=code-symbol | neighbors=[ADError, CliError, LicenseError, TransportError, VedhaAuthError, MetasploitRPCError]
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
- "lib_target_parser": "target-parser.ts" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, COMMON_RANGES, estimateHostCount(), isPrivateRange(), isValidTarget(), ParseResult]
- "main_scripts_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, DBScanner, interpret_redis_info(), main(), _probe_mongodb(), _probe_mssql()]
- "main_scripts_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, Delta, DeltaEngine, _extract_service(), _extract_version()]
- "main_scripts_mobile_scanner": "mobile_scanner.py" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), main(), MobileScanner]
- "main_scripts_nfs_scanner": "nfs_scanner.py" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, is_world_readable(), main(), NFSScanner, parse_mount_export(), parse_portmap_dump()]
- "main_scripts_run_all": "run_all.py" | kind=code-symbol | source=probe/main_scripts/run_all.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _advertised_dynamic_ports(), _log()]
- "main_scripts_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L315 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "main_scripts_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L309 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._build_results(), ._fallback_scan(), .__init__()]
- "main_scripts_va_campaign_progressreporter": "ProgressReporter" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L169 | neighbors=[va_campaign.py, build_campaign(), ._current(), ._eta_seconds(), .finish(), ._flush()]
- "native_dir_bust": "dir-bust.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, BUILTIN_PATHS, DirBustResult, loadWordlist()]
- "reject_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, backend.ts, backend(), BackendError]
- "reopen_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, 8ebc053 feat(risk-rank-ui): surface ver…, f473173 merge: network VA accuracy, KEV…, adapters.ts, toUiFinding()]
- "routers_agents_jobresultrequest": "JobResultRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L266 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_detection_runrequest": "RunRequest" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L51 | neighbors=[detection.py, BaseModel, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig]
- "routers_detection_siemconfigin": "SIEMConfigIn" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L44 | neighbors=[detection.py, BaseModel, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig]
- "routers_engagements_rationale_128": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L128 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-018.json

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
