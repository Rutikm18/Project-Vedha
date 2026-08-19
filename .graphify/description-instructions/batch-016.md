# Node Description Batch 17 of 227

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

- "workflow_execution": "execution.py" | kind=code-symbol | source=probe/workflow/execution.py:L1 | neighbors=[engine.py, b4b12a9 Rename project and update files, test_passive_collector.py, test_workflow_execution.py, scanner_base.py, classify_scanner_error()]
- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L144 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, _run_inventory(), _run_passive(), .close(), .__init__()]
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L871 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L226 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L29 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…]
- "assistant_assistantprovider": "AssistantProvider.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L1 | neighbors=[layout.tsx, AssistantDrawer.tsx, AssistantFab.tsx, AssistantDrawer(), AssistantFab(), AssistantCtx]
- "auth_middleware": "middleware.py" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L1 | neighbors=[database.py, agent_jwt_path_allows(), _is_public_enrollment_request(), TenantIsolationMiddleware, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "commands_interactive_divider": "divider()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L112 | neighbors=[interactive.ts, ln(), mainMenu(), wizardAdmin(), wizardAsk(), wizardEngagement()]
- "commands_report": "report.ts" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L1 | neighbors=[apiFetch(), requireAuth(), AiReport, buildReportCommand(), Engagement, errExit()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1af3404cd899c56eec3439d379b9f621f044baf9": "1af3404 feat(deploy): probe-free manager stack + port-80 edge ingress" | kind=Commit | source=git | neighbors=[0e22dbf feat(probe): bounded auto-troub…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2c53ae99b6e203a1fefff8d7998d849e906ee0c1": "2c53ae9 evasion(scanner): randomized scan order + jittered scan-delay (task C1/…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, main, 37fa611 harden(scanner): XML-entity gua…, port_scanner.py, scanner_base.py, syn_scanner.py]
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L18 | neighbors=[page.tsx, page.tsx, PageShell.tsx, page.tsx, page.tsx, page.tsx]
- "components_toastprovider": "ToastProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, Toast, TOAST_STYLES, ToastContext, ToastContextValue]
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
- "main_scripts_findings_data": "_data()" | kind=code-symbol | source=probe/main_scripts/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_rdp(), _rule_smb(), _rule_snmp(), _rule_tls()]
- "main_scripts_ja4s": "ja4s.py" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "main_scripts_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _auth_shaped_json_body(), _known_false_positive(), main(), _mcp_oauth_signal()]
- "main_scripts_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, _have_nmap(), main(), NmapExecutionError, _parse_nmap_xml()]
- "main_scripts_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _coverage(), _device_hint(), _is_readable(), _listener_error_code(), main()]
- "main_scripts_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L251 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "main_scripts_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L245 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._build_results(), ._fallback_scan(), .__init__()]
- "main_scripts_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, classify_cipher(), _get_cert_der(), grade_tls_posture(), main(), _parse_cert_der()]

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
