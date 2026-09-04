# Node Description Batch 21 of 332

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

- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=probe/tests/test_probe_core.py:L322 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_explicit_snmp_does_not_require_tc…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port()]
- "tests_test_probe_enrollment": "test_probe_enrollment.py" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, test_device_access_token_has_dedicated_…, test_ed25519_proof_of_possession_reject…, test_enroll_token_create_defaults_and_b…, test_enroll_token_usable_only_while_liv…]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=probe/tests/test_task_runner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, task_runner.py, _fake_run_scan(), runner()]
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=probe/tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_explicit_empty_targets_never_expa…, .test_rejects_empty_targets(), .test_rejects_non_object_params(), .test_rejects_non_string_target()]
- "tests_test_tier1_wiring_gate": "test_tier1_wiring_gate.py" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L1 | neighbors=[64e8290 feat(campaign): implement VA ca…, 6e2818f Add support for additional serv…, scan_funnel.py, scanner_base.py, _funnel(), test_every_it_branch_has_port_table_ent…]
- "tests_test_validation_ingest": "test_validation_ingest.py" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _finding(), test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…]
- "tests_test_xml_parser_testnmapxmlparser": "TestNmapXMLParser" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L42 | neighbors=[test_xml_parser.py, .setup_method(), .test_cpe_extraction(), .test_empty_scan(), .test_empty_string(), .test_malformed_xml_returns_empty()]
- "tools_installer_installtool": "installTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L156 | neighbors=[tools.ts, installer.ts, installAll(), downloadFile(), extract(), getInstalledRecord()]
- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, f3bb8db feat(manager): cross-worker WS …]
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L355 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()]
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()]
- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=probe/agent/agent.py:L591 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, _bounded_env_int(), say(), Run an HTTP-claimed job while renewing …]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L228 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L31 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L802 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError, Generic authenticated GET, returns pars…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L654 | neighbors=[Backwards-compatible bool form of `hear…, Transport, .heartbeat_ex(), Backwards-compatible bool form of `hear…, Refresh a device token before expiry; l…, .ensure_device_access()]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L672 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L557 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError, Refresh routing metadata using the cach…]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L318 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …, Register the probe with the manager.   …]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L711 | neighbors=[Submit a scan result to the manager.   …, Transport, _strip_nul(), .ensure_device_access(), Submit a scan result to the manager.   …, Submit a scan result to the manager.   …]
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()]
- "auth_middleware": "middleware.py" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L1 | neighbors=[database.py, agent_jwt_path_allows(), _is_public_enrollment_request(), TenantIsolationMiddleware, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "commands_interactive_divider": "divider()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L112 | neighbors=[interactive.ts, ln(), mainMenu(), wizardAdmin(), wizardAsk(), wizardEngagement()]
- "commands_report": "report.ts" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L1 | neighbors=[apiFetch(), requireAuth(), AiReport, buildReportCommand(), Engagement, errExit()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2de251b6a34cad99831e042cf014ca1bcfa6aed2": "2de251b feat(scanner): ICMP timestamp fallback — echo-filter bypass + clock har…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, ui-ux-backend-updates0109]
- "commit:repo:github.com/Rutikm18/Project-Vedha@daf3de2734a3efdd04df485c8544d56209bd5554": "daf3de2 feat(scanner): add service enumeration and enrichment layer" | kind=Commit | source=git | neighbors=[6be8259 feat(integrations): outbox deli…, addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "components_engagementstatuscontrol": "EngagementStatusControl.tsx" | kind=code-symbol | source=manager/frontend/components/EngagementStatusControl.tsx:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, ENGAGEMENT_STATES, EngagementStatusControl(), EngagementStatusControlProps, STATUS_COLOR]
- "detection_edr_crowdstrikefalcon": "CrowdStrikeFalcon" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L91 | neighbors=[edr.py, .parse_response(), .query_detections(), EDRQueryEngine, Falcon: query detection IDs then fetch …, Unit tests for the detection validation…]
- "detection_edr_microsoftdefender": "MicrosoftDefender" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L140 | neighbors=[edr.py, EDRQueryEngine, .parse_response(), .query_detections(), Microsoft Defender via the Graph Securi…, Unit tests for the detection validation…]
- "detection_edr_sentinelone": "SentinelOne" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L186 | neighbors=[edr.py, SentinelOne via the REST ``/web/api/v2.…, EDRQueryEngine, .parse_response(), .query_detections(), Unit tests for the detection validation…]
- "detection_engine_ai_normalizer_ainormalizercache": "AINormalizerCache" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L139 | neighbors=[ai_normalizer.py, .get(), ._key(), .__post_init__(), .put(), propose_candidates()]
- "detection_engine_port_intel": "port_intel.py" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _banner_confirms_backdoor(), classify_port()]
- "detection_prioritization": "prioritization.py" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 21ebc46 feat(detection): unified priori…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, composite_risk_score()]
- "discovery_rate_limiter_ratelimiter": "RateLimiter" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L27 | neighbors=[rate_limiter.py, .acquire(), ._consume_token(), .__init__(), .is_within_window(), ._resolve_cidr()]
- "discovery_worker_rationale_1": "DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner" | kind=entity | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_worker_rationale_56": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L56 | neighbors=[DiscoveryWorker, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_worker_rationale_58": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L58 | neighbors=[RateLimiter, ServiceIdentifier, DiscoveryWorker, NmapXMLParser, ParsedHost, ParsedPort]
- "engagements_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET, POST, toApiEngagementCreate(), toUiEngagement(), backend()]
- "engine_tool_runners_runnmapnse": "runNmapNse()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1043 | neighbors=[tool-runners.ts, runLdapEnum(), runNetbiosEnum(), runNfsEnum(), bin(), collectProcess()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-020.json

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
