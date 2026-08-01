# Node Description Batch 17 of 119

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

- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1697 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()]
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1622 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bb0ef3d473623bac3404761b5c3d34baa72612dd": "bb0ef3d feat(probe): route DB services on non-standard ports via banner signatu…" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/probe-usecase-alignment, b4b12a9 Rename project and update files, test_router_db.py, router.py, workflow_engine.py]
- "config_config_load": "Load()" | kind=code-symbol | source=probe-go/config/config.go:L32 | neighbors=[config.go, env(), envBool(), envDuration(), envInt(), hostname()]
- "dashboard_zonerow": "ZoneRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/ZoneRow.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ZoneRow(), ZoneHealth, 298a9d4 trim frontend to 7 core pages; …, Exposure.tsx, mock-dashboard.ts]
- "detection_edr_edrqueryengine": "EDRQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L62 | neighbors=[edr.py, CrowdStrikeFalcon, .__init__(), .query_detections(), ._request(), MicrosoftDefender]
- "detection_engine_ai_normalizer_ainormalizercache_get": ".get()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L152 | neighbors=[AINormalizerCache, ._key(), .propose_cpe(), extract_raw_text(), .propose_cpe(), propose_candidates()]
- "detection_engine_correlate": "correlate.py" | kind=code-symbol | source=manager/detection_engine/correlate.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, correlate_smb_patch(), dedup_findings(), _product_from_cpe(), suppress_negated(), correlate.py — dedup, authoritative-sup…]
- "detection_engine_enrichment_db": "enrichment_db.py" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, EpssDB, KevDB, load_epss(), load_kev(), enrichment_db.py — load the pinned KEV/…]
- "detection_sigma": "sigma.py" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma d…, 2885afa Add comprehensive probe testing…]
- "discovery_xml_parser_parsedhost": "ParsedHost" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L25 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, xml_parser.py, ._parse_host()]
- "engine_tool_runners_binname": "binName()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L77 | neighbors=[tool-runners.ts, bin(), isWindows(), runHostDiscovery(), runSshAudit(), runTestssl()]
- "engine_tool_runners_runnaabu": "runNaabu()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L146 | neighbors=[scanner.ts, tool-runners.ts, bin(), hasBinary(), spawnOpts(), streamProcess()]
- "engine_types_scancallbacks": "ScanCallbacks" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L109 | neighbors=[agent.py, tools.ts, interactive.ts, scan.ts, scanner.ts, tool-runners.ts]
- "engine_types_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[findings.ts, scanner.ts, types.ts, finding-id.ts, findings-store.ts, nuclei-parser.ts]
- "graph_builder_graphbuilder_add_exploit_edges": ".add_exploit_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L183 | neighbors=[GraphBuilder, asset_node_id(), exploit_complexity(), finding_node_id(), _to_float(), .build_asset_graph()]
- "graph_demo": "demo.py" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-p…]
- "graph_demo_demoasset": "DemoAsset" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L27 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "graph_demo_demofinding": "DemoFinding" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L45 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "hooks_usetoast_usetoast": "useToast()" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L6 | neighbors=[page.tsx, page.tsx, useToast.ts, page.tsx, page.tsx, page.tsx]
- "install_install": "install.go" | kind=code-symbol | source=probe-go/install/install.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, copyFile(), Install(), installLaunchd(), installSystemd(), Uninstall()]
- "lib_findings_store_savefindings": "saveFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L51 | neighbors=[tools.ts, findings-store.ts, createFinding(), ensureDir(), getAllFindings(), slaDeadline()]
- "lib_httpx_parser_httpxjsonldecoder": "HttpxJsonlDecoder" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L93 | neighbors=[tool-runners.ts, httpx-parser.ts, .decode(), .finish(), .malformedLines(), .push()]
- "lib_tenant": "tenant.ts" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, RESERVED, resolveTenantSubdomain(), rootDomain(), subdomainFromHost(), 298a9d4 trim frontend to 7 core pages; …]
- "me_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, backend(), withBackend(), GET, 298a9d4 trim frontend to 7 core pages; …, backend.ts]
- "models_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/models/agent.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, Enum, Agent, AgentStatus, 2885afa Add comprehensive probe testing…]
- "models_user_user": "User" | kind=code-symbol | source=manager/backend/app/models/user.py:L11 | neighbors=[user.py, Base, Base, TimestampMixin, UserRole, TimestampMixin]
- "native_tls_info": "tls-info.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, nativeTlsInfo(), TlsInfoResult, WEAK_PROTOCOLS, WEAK_SIGNATURES, 298a9d4 trim frontend to 7 core pages; …]
- "probes_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, backend(), withBackend(), GET, 0557559 scanner: real use-case library,…, backend.ts]
- "routers_agent_advisor": "agent_advisor.py" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dependencies.py, list_recommendations(), _rec_dict(), run_advisor(), agent_advisor.py — API for the agentic …]
- "routers_agents_agent_can_execute_job": "_agent_can_execute_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L204 | neighbors=[agents.py, _job_reachability_scope(), _required_scan_type(), _scope_is_reachable(), enqueue_agent_job(), get_agent_jobs()]
- "routers_agents_agent_ownership_check": "_agent_ownership_check()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L427 | neighbors=[agents.py, get_agent_jobs(), heartbeat(), Verify that the JWT token bearer IS the…, refresh_agent_registration(), submit_job_result()]
- "routers_analytics_exposureanalytics": "ExposureAnalytics" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L37 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_analytics_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L27 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_analytics_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L32 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_detection_runs": "detection_runs.py" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dependencies.py, latest_run_delta(), list_detection_runs(), _run_dict(), detection_runs.py — temporal detection …]
- "routers_engagements_import_facts": "import_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L294 | neighbors=[engagements.py, _parse_probe_file(), _promote_from_facts(), _read_capped(), _refresh_overview_cache(), Offline ingest path: upload a probe's s…]
- "routers_findings_rationale_26": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L26 | neighbors=[Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding, _tenant_finding()]
- "routers_findings_rationale_49": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L49 | neighbors=[Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding, sla_summary()]
- "scanner_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L198 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-016.json

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
