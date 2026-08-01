# Node Description Batch 26 of 119

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

- "models_exploit_approval": "exploit_approval.py" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, ApprovalStatus, ExploitApprovalRequest, 298a9d4 trim frontend to 7 core pages; …]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ScanJob, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "pathid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, graphStore, GET(), 298a9d4 trim frontend to 7 core pages; …, graph-store.ts]
- "probe_pipeline_run_active": "_run_active()" | kind=code-symbol | source=probe/pipeline.py:L144 | neighbors=[pipeline.py, _Collector, .write(), _rollup(), _shared()]
- "results_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, GET(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "routers_agent_advisor_rationale_1": "agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag" | kind=entity | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, AgentRecommendation, Engagement, agent_advisor.py]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L130 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L135 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L89 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…]
- "routers_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, dependencies.py, ai_generate(), ai_status()]
- "routers_attack_paths_build_analyzer": "_build_analyzer()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L175 | neighbors=[attack_paths.py, attack_graph(), blast_radius(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_list_chokepoints": "list_chokepoints()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L117 | neighbors=[attack_paths.py, _all_paths_to_critical(), _asset_labels(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_recompute_and_store": "_recompute_and_store()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L199 | neighbors=[attack_paths.py, list_attack_paths(), _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_detection_runs_rationale_1": "detection_runs.py — temporal detection API (\"what changed since last time\").  GE" | kind=entity | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[DetectionRun, Engagement, FindingStatus, Finding, detection_runs.py]
- "routers_engagements_compute_overview": "_compute_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L40 | neighbors=[engagements.py, engagements_overview(), Shared aggregation — used by both the c…, _refresh_overview_cache(), Shared aggregation — used by both the c…]
- "routers_engagements_engagements_overview": "engagements_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L398 | neighbors=[engagements.py, _compute_overview(), _overview_cache_key(), P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…]
- "routers_findings_rationale_29": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L29 | neighbors=[Engagement, FindingStatus, Finding, sla_summary(), PaginatedResponse]
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L24 | neighbors=[findings.py, get_finding(), patch_finding(), Fetch a finding scoped to the caller's …, Fetch a finding scoped to the caller's …]
- "routers_health": "health.py" | kind=code-symbol | source=manager/backend/app/routers/health.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, database.py, dependencies.py, health(), 298a9d4 trim frontend to 7 core pages; …]
- "run_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, POST(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "scanner_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/scanner/host_discovery.py:L29 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target()]
- "scanner_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…, Parse masscan -oJ output robustly: hand…, _run_masscan()]
- "scanner_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…, Best-effort device label from an announ…]
- "scanner_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…, Await readability on any listener witho…]
- "scanner_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/scanner/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), RuntimeError, .__init__(), All passive sources failed before the l…]
- "scanner_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/scanner/port_scanner.py:L27 | neighbors=[port_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L401 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "scanner_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L182 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…]
- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/scanner/service_banner.py:L34 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), .scan_target()]
- "scanner_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L104 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]
- "scanner_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L75 | neighbors=[snmp_scanner.py, BaseScanner, .__init__(), ._query(), .scan_target()]
- "scanner_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L155 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/scanner/web_scanner.py:L135 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "schemas_ai_aiproviderstatus": "AiProviderStatus" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L37 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_ai_aistatusresponse": "AiStatusResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L47 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetIn, AssetOut, BulkAssetImportResult, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_asset_assetin": "AssetIn" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L9 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType, .validate_ip()]
- "schemas_common": "common.py" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ErrorDetail, paginate(), PaginatedResponse, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_engagement_engagementout": "EngagementOut" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L92 | neighbors=[engagement.py, EngagementDetail, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_finding_findingfilter": "FindingFilter" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L10 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-025.json

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
