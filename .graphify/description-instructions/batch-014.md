# Node Description Batch 15 of 209

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

- "auth_middleware": "middleware.py" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L1 | neighbors=[database.py, agent_jwt_path_allows(), _is_public_enrollment_request(), TenantIsolationMiddleware, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…] | lang=en
- "commands_interactive_divider": "divider()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L112 | neighbors=[interactive.ts, ln(), mainMenu(), wizardAdmin(), wizardAsk(), wizardEngagement()] | lang=en
- "commands_report": "report.ts" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L1 | neighbors=[apiFetch(), requireAuth(), AiReport, buildReportCommand(), Engagement, errExit()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, spike/probe-go] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@58c2d10f572ed4b7fce3da53bb9f95b696c4b94f": "58c2d10 feat(active-validation): ValidationRequest model + migration" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 0d6be85 feat(risk-rank): explainable 0-…, __init__.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, spike/probe-go] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ae08d19a6e9e90cc033a56b4aaeea1424c557da7": "ae08d19 feat(scanner): adaptive timeout, SYN retransmit, top-100 default (accur…" | kind=Commit | source=git | neighbors=[65e5684 feat(probe): transparent job lo…, feat/syn-scanner-osfp-adaptive, main, c4386e4 feat(customers): operator Custo…, port_scanner.py, syn_scanner.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, spike/probe-go] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main] | lang=fr
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L18 | neighbors=[page.tsx, page.tsx, PageShell.tsx, page.tsx, page.tsx, page.tsx] | lang=en
- "components_toastprovider": "ToastProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, Toast, TOAST_STYLES, ToastContext, ToastContextValue] | lang=en
- "detection_edr_crowdstrikefalcon": "CrowdStrikeFalcon" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L91 | neighbors=[edr.py, .parse_response(), .query_detections(), EDRQueryEngine, Falcon: query detection IDs then fetch …, Unit tests for the detection validation…] | lang=en
- "detection_edr_microsoftdefender": "MicrosoftDefender" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L140 | neighbors=[edr.py, EDRQueryEngine, .parse_response(), .query_detections(), Microsoft Defender via the Graph Securi…, Unit tests for the detection validation…] | lang=en
- "detection_edr_sentinelone": "SentinelOne" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L186 | neighbors=[edr.py, SentinelOne via the REST ``/web/api/v2.…, EDRQueryEngine, .parse_response(), .query_detections(), Unit tests for the detection validation…] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache": "AINormalizerCache" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L139 | neighbors=[ai_normalizer.py, .get(), ._key(), .__post_init__(), .put(), propose_candidates()] | lang=en
- "detection_engine_bridge_create_findings_from_facts": "create_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L219 | neighbors=[engine_bridge.py, _apply_regression_reopen(), detect_findings_from_facts(), _find_remediated_match(), _persist_attack_paths(), _stamp_verification()] | lang=en
- "discovery_rate_limiter_ratelimiter": "RateLimiter" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L27 | neighbors=[rate_limiter.py, .acquire(), ._consume_token(), .__init__(), .is_within_window(), ._resolve_cidr()] | lang=en
- "discovery_worker_rationale_1": "DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner" | kind=entity | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort] | lang=en
- "discovery_worker_rationale_56": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L56 | neighbors=[DiscoveryWorker, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort] | lang=en
- "discovery_worker_rationale_58": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L58 | neighbors=[RateLimiter, ServiceIdentifier, DiscoveryWorker, NmapXMLParser, ParsedHost, ParsedPort] | lang=en
- "engagements_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET, POST, toApiEngagementCreate(), toUiEngagement(), backend()] | lang=en
- "engine_tool_runners_runnmapnse": "runNmapNse()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1043 | neighbors=[tool-runners.ts, runLdapEnum(), runNetbiosEnum(), runNfsEnum(), bin(), collectProcess()] | lang=en
- "exploit_safety": "safety.py" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, requires_approval(), SafetyViolationError] | lang=en
- "graph_builder": "builder.py" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder] | lang=en
- "lib_auth_middleware": "auth-middleware.ts" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, AuthContext, Handler, withAuth(), verifyToken()] | lang=en
- "lib_nmap_parser": "nmap-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractScripts(), NmapHost, NmapScriptResult, NmapService] | lang=en
- "main_scripts_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, Delta, DeltaEngine, _extract_service(), _extract_version(), main()] | lang=en
- "main_scripts_findings_data": "_data()" | kind=code-symbol | source=probe/main_scripts/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_rdp(), _rule_smb(), _rule_snmp(), _rule_tls()] | lang=en
- "main_scripts_ja4s": "ja4s.py" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()] | lang=en
- "main_scripts_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _coverage(), _device_hint(), _is_readable(), _listener_error_code(), main()] | lang=en
- "main_scripts_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, ae08d19 feat(scanner): adaptive timeout…, _family_of(), main(), PortScanner] | lang=en
- "main_scripts_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L154 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()] | lang=en
- "main_scripts_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, classify_cipher(), _get_cert_der(), grade_tls_posture(), main(), _parse_cert_der()] | lang=en
- "models_detection_run_detectionrun": "DetectionRun" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L40 | neighbors=[detection_run.py, Base, TimestampMixin, engine_bridge.py — run the deterministi…, A previously-remediated finding whose i…, Background entry point (P1: keep detect…] | lang=en
- "path_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, backend.ts, backend(), BackendError, bearerFrom(), cookieFrom()] | lang=en
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, database.py, _agent_token_from_websocket()] | lang=en
- "routers_agents_encrypt_scope_for_agent": "_encrypt_scope_for_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L476 | neighbors=[agents.py, enqueue_agent_job(), get_agent_jobs(), Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…] | lang=en
- "routers_agents_rationale_1": "Agent registration, heartbeat, job polling, and result submission." | kind=entity | source=manager/backend/app/routers/agents.py:L1 | neighbors=[agents.py, Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_208": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L208 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_246": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L246 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-014.json

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
