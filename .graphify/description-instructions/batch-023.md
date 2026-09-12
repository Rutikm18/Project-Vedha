# Node Description Batch 24 of 380

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, f3bb8db feat(manager): cross-worker WS …] | lang=en
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L355 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()] | lang=en
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()] | lang=en
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L62 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), Return an integer environment setting c…, _run_polled_job_with_heartbeats()] | lang=en
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L228 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()] | lang=en
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L31 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()] | lang=en
- "agent_engine_applied_tuning": "_applied_tuning()" | kind=code-symbol | source=probe/agent/engine.py:L398 | neighbors=[engine.py, _scan_method_for(), _build_run_stats(), Serialize effective limits without ever…, Serialize effective limits without ever…, Serialize effective limits without ever…] | lang=en
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L221 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…, Coerce val to float and clamp to [lo, h…] | lang=en
- "agent_engine_leaselosterror": "LeaseLostError" | kind=code-symbol | source=probe/agent/engine.py:L568 | neighbors=[engine.py, RuntimeError, Raised when Manager fencing revokes the…, _run_with_cancellation(), Raised when Manager fencing revokes the…, Raised when Manager fencing revokes the…] | lang=en
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L241 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Translate operator-supplied job params …, Translate operator-supplied job params …] | lang=en
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…] | lang=en
- "agent_self_scan": "self_scan.py" | kind=code-symbol | source=probe/agent/self_scan.py:L1 | neighbors=[detect_host_container(), execute(), main(), plan_self_scan(), primary_ipv4(), _read()] | lang=en
- "agent_task_runner_taskrunner": "TaskRunner" | kind=code-symbol | source=probe/agent/task_runner.py:L106 | neighbors=[task_runner.py, Orchestrates one scan job's lifecycle. …, ._already_committed(), ._archive_result(), ._chunk_sink(), .__init__()] | lang=en
- "agent_task_runner_taskrunner_run_job": ".run_job()" | kind=code-symbol | source=probe/agent/task_runner.py:L198 | neighbors=[Execute a complete scan job lifecycle. …, TaskRunner, JobResult, ._already_committed(), ._chunk_sink(), ._submit_or_spool()] | lang=en
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L633 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), ._archive_result(), Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…] | lang=en
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=probe/agent/transport.py:L770 | neighbors=[Fetch the engagement's authoritative sc…, Transport, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…] | lang=en
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L59 | neighbors=[agent.py, .run(), RuntimeError, Raised when the Anthropic SDK or API ke…, Raised when the Anthropic SDK or API ke…, AgentRecommendation] | lang=en
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L264 | neighbors=[main.py, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…] | lang=en
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L77 | neighbors=[middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch(), BaseHTTPMiddleware, Extracts JWT from Authorization header …] | lang=en
- "commands_interactive_divider": "divider()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L112 | neighbors=[interactive.ts, ln(), mainMenu(), wizardAdmin(), wizardAsk(), wizardEngagement()] | lang=en
- "commands_report": "report.ts" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L1 | neighbors=[apiFetch(), requireAuth(), AiReport, buildReportCommand(), Engagement, errExit()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@00140b3bf16bb11003f143293dbdc3e5ced58425": "00140b3 Vendor FindingReport component + report-finding.css" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@906b972e0e0957f491a42c41f1ff43b82be00f57": "906b972 Wire admin Technical tab to FindingsSection; drop legacy FindingCard" | kind=Commit | source=git | neighbors=[86b4fb0 Add UI-Finding to RawFinding ad…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a222adcc137046ed1a26b05c80fa0769eff6087d": "a222adc Windows setup: fix source-mode run (LICENSE_ENFORCED=false + Defender e…" | kind=Commit | source=git | neighbors=[32651d6 Windows setup: auto-install Pyt…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@ac7c957e0d1bf7198fe9e22ed76c0f6ccadb0526": "ac7c957 Render portal All-Findings via FindingsSection (client mode)" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ac8d1ee2774da194020fbefd23215fd8d0f56e3a": "ac8d1ee Phase 7: dependency bootstrap + cross-OS shims + brain CLI (+13 tests)" | kind=Commit | source=git | neighbors=[bootstrap.py, deps.py, setup.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@aee1d86cdc8403896183e8ed3b2ef78deedae0d8": "aee1d86 Add assessor|client mode to FindingReport for portal reuse" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d7736e83afbbfc9536ae253dfae802327f3ed8fd": "d7736e8 Switch Evidence Vault to redacting EvidenceArtifact; remove EvidBlock" | kind=Commit | source=git | neighbors=[906b972 Wire admin Technical tab to Fin…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "detection_edr_crowdstrikefalcon": "CrowdStrikeFalcon" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L91 | neighbors=[edr.py, .parse_response(), .query_detections(), EDRQueryEngine, Falcon: query detection IDs then fetch …, Unit tests for the detection validation…] | lang=en
- "detection_edr_microsoftdefender": "MicrosoftDefender" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L140 | neighbors=[edr.py, EDRQueryEngine, .parse_response(), .query_detections(), Microsoft Defender via the Graph Securi…, Unit tests for the detection validation…] | lang=en
- "detection_edr_sentinelone": "SentinelOne" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L186 | neighbors=[edr.py, SentinelOne via the REST ``/web/api/v2.…, EDRQueryEngine, .parse_response(), .query_detections(), Unit tests for the detection validation…] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache": "AINormalizerCache" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L139 | neighbors=[ai_normalizer.py, .get(), ._key(), .__post_init__(), .put(), propose_candidates()] | lang=en
- "detection_engine_port_intel": "port_intel.py" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _banner_confirms_backdoor(), classify_port()] | lang=en
- "detection_prioritization": "prioritization.py" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 21ebc46 feat(detection): unified priori…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, composite_risk_score()] | lang=en
- "discovery_rate_limiter_ratelimiter": "RateLimiter" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L27 | neighbors=[rate_limiter.py, .acquire(), ._consume_token(), .__init__(), .is_within_window(), ._resolve_cidr()] | lang=en
- "discovery_worker_rationale_1": "DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner" | kind=entity | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort] | lang=en
- "discovery_worker_rationale_56": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L56 | neighbors=[DiscoveryWorker, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort] | lang=en
- "discovery_worker_rationale_58": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L58 | neighbors=[RateLimiter, ServiceIdentifier, DiscoveryWorker, NmapXMLParser, ParsedHost, ParsedPort] | lang=en
- "engagements_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET, POST, toApiEngagementCreate(), toUiEngagement(), backend()] | lang=en
- "engine_tool_runners_runnmapnse": "runNmapNse()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1043 | neighbors=[tool-runners.ts, runLdapEnum(), runNetbiosEnum(), runNfsEnum(), bin(), collectProcess()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-023.json

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
