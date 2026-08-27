# Node Description Batch 18 of 236

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

- "customers_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L1 | neighbors=[c4386e4 feat(customers): operator Custo…, e3958e7 feat(customers): reveal + copy …, PageShell.tsx, PageShell(), ClientUserResp, Customer]
- "detection_edr_crowdstrikefalcon": "CrowdStrikeFalcon" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L91 | neighbors=[edr.py, .parse_response(), .query_detections(), EDRQueryEngine, Falcon: query detection IDs then fetch …, Unit tests for the detection validation…]
- "detection_edr_microsoftdefender": "MicrosoftDefender" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L140 | neighbors=[edr.py, EDRQueryEngine, .parse_response(), .query_detections(), Microsoft Defender via the Graph Securi…, Unit tests for the detection validation…]
- "detection_edr_sentinelone": "SentinelOne" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L186 | neighbors=[edr.py, SentinelOne via the REST ``/web/api/v2.…, EDRQueryEngine, .parse_response(), .query_detections(), Unit tests for the detection validation…]
- "detection_engine_ai_normalizer_ainormalizercache": "AINormalizerCache" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L139 | neighbors=[ai_normalizer.py, .get(), ._key(), .__post_init__(), .put(), propose_candidates()]
- "detection_engine_bridge_create_findings_from_facts": "create_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L219 | neighbors=[engine_bridge.py, _apply_regression_reopen(), detect_findings_from_facts(), _find_remediated_match(), _persist_attack_paths(), _stamp_verification()]
- "discovery_rate_limiter_ratelimiter": "RateLimiter" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L27 | neighbors=[rate_limiter.py, .acquire(), ._consume_token(), .__init__(), .is_within_window(), ._resolve_cidr()]
- "discovery_worker_rationale_1": "DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner" | kind=entity | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_worker_rationale_56": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L56 | neighbors=[DiscoveryWorker, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_worker_rationale_58": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L58 | neighbors=[RateLimiter, ServiceIdentifier, DiscoveryWorker, NmapXMLParser, ParsedHost, ParsedPort]
- "engagements_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET, POST, toApiEngagementCreate(), toUiEngagement(), backend()]
- "engine_tool_runners_runnmapnse": "runNmapNse()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1043 | neighbors=[tool-runners.ts, runLdapEnum(), runNetbiosEnum(), runNfsEnum(), bin(), collectProcess()]
- "exploit_safety": "safety.py" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, requires_approval(), SafetyViolationError]
- "graph_builder": "builder.py" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder]
- "lib_auth_middleware": "auth-middleware.ts" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, AuthContext, Handler, withAuth(), verifyToken()]
- "lib_nmap_parser": "nmap-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractScripts(), NmapHost, NmapScriptResult, NmapService]
- "main_scripts_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, Delta, DeltaEngine, _extract_service(), _extract_version(), main()]
- "main_scripts_ja4s": "ja4s.py" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "main_scripts_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _auth_shaped_json_body(), _known_false_positive(), main(), _mcp_oauth_signal()]
- "main_scripts_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, _have_nmap(), main(), NmapExecutionError, _parse_nmap_xml()]
- "main_scripts_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _coverage(), _device_hint(), _is_readable(), _listener_error_code(), main()]
- "main_scripts_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L251 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "main_scripts_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L245 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._build_results(), ._fallback_scan(), .__init__()]
- "main_scripts_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, classify_cipher(), _get_cert_der(), grade_tls_posture(), main(), _parse_cert_der()]
- "models_detection_run_detectionrun": "DetectionRun" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L40 | neighbors=[detection_run.py, Base, TimestampMixin, engine_bridge.py — run the deterministi…, A previously-remediated finding whose i…, Background entry point (P1: keep detect…]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 58c2d10 feat(active-validation): Valida…, 81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …]
- "path_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, backend.ts, backend(), BackendError, bearerFrom(), cookieFrom()]
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, database.py, _agent_token_from_websocket()]
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L606 | neighbors=[agents.py, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…]
- "routers_agents_rationale_1": "Agent registration, heartbeat, job polling, and result submission." | kind=entity | source=manager/backend/app/routers/agents.py:L1 | neighbors=[agents.py, Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_208": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L208 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_246": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L246 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_265": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L265 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_459": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L459 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_detection_rationale_1": "Detection validation API (DetectionValidationAPI).  POST /engagements/{id}/detec" | kind=entity | source=manager/backend/app/routers/detection.py:L1 | neighbors=[detection.py, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_detection_rationale_240": "Background task: pull SIEM/EDR telemetry, correlate, persist results." | kind=entity | source=manager/backend/app/routers/detection.py:L240 | neighbors=[_run_correlation(), AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_remediation": "remediation.py" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, dependencies.py, _build_upsert_stmt(), _cached_plan(), generate_remediation()]
- "scanner_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, Delta, DeltaEngine, _extract_service(), _extract_version(), main()]
- "scanner_ja4s": "ja4s.py" | kind=code-symbol | source=probe/scanner/ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "scanner_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), main()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-017.json

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
