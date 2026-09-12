# Node Description Batch 21 of 380

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

- "agent_cli_output": "output()" | kind=code-symbol | source=probe/agent/cli.py:L179 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()] | lang=en
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L317 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…] | lang=en
- "agent_engine_derive_post_stage": "_derive_post_stage()" | kind=code-symbol | source=probe/agent/engine.py:L496 | neighbors=[engine.py, _derive_devices(), _derive_exposure(), Return (extra ScanResults to append as …, run_scan(), Return (extra ScanResults to append as …] | lang=en
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=probe/agent/transport.py:L917 | neighbors=[Generic authenticated GET, returns pars…, Transport, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…] | lang=en
- "agent_transport_transport_is_ws_connected": ".is_ws_connected()" | kind=code-symbol | source=probe/agent/transport.py:L975 | neighbors=[True if the WebSocket connection is act…, Transport, True if the WebSocket connection is act…, True if the WebSocket connection is act…, True if the WebSocket connection is act…, True if the WebSocket connection is act…] | lang=en
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L354 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …, Register the probe with the manager.   …] | lang=en
- "agent_transport_transport_ws_url": ".ws_url()" | kind=code-symbol | source=probe/agent/transport.py:L933 | neighbors=[Return the WebSocket endpoint without e…, Transport, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…] | lang=en
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()] | lang=en
- "ai_prioritizer_vulnprioritizer": "VulnPrioritizer" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L99 | neighbors=[prioritizer.py, .explain_prediction(), .fallback_score(), ._formula_contributions(), .__init__(), .is_trained()] | lang=en
- "assistant_factcard": "FactCard.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard(), lifecycleSummary(), Pip(), assistant.ts] | lang=en
- "auth_exceptions_authenticationerror": "AuthenticationError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L28 | neighbors=[exceptions.py, VedhaAuthError, BcryptFailureError, DatabaseFailureError, DisabledTenantError, DisabledUserError] | lang=en
- "commands_admin": "admin.ts" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildAdminCommand(), c, PermittedUser, 10dfc80 Add comprehensive probe testing…] | lang=en
- "commands_login": "login.ts" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L1 | neighbors=[loadSession(), saveSession(), serverUrl(), buildLoginCommand(), prompt(), promptSilent()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@36183652e72bdc0bb357314c0b2b08a6d5620771": "3618365 Vendor finding-model + port its spec into admin frontend" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6cf7e16ba4ab633924c9ee768177a7ebdd912411": "6cf7e16 Expose report enrichment on FindingOut (computed, no migration)" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7a12ab221f6f315ec47fd102566222dd903ee2a3": "7a12ab2 Restructure /reports into one continuous report document" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@83d2039c69cb442be6b6efdfdea7459270fb4598": "83d2039 docs: add prompt output documentation and bump version to 1.0.121" | kind=Commit | source=git | neighbors=[3c9062a refactor: Update dashboard comp…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f023fa528aa325ac135b85582945c05814960804": "f023fa5 Add portalToRawFinding adapter (curated by construction) + tests" | kind=Commit | source=git | neighbors=[aee1d86 Add assessor|client mode to Fin…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "components_engagementstatuscontrol": "EngagementStatusControl.tsx" | kind=code-symbol | source=manager/frontend/components/EngagementStatusControl.tsx:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, ENGAGEMENT_STATES, EngagementStatusControl(), EngagementStatusControlProps] | lang=en
- "customers_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, c4386e4 feat(customers): operator Custo…, e3958e7 feat(customers): reveal + copy …, PageShell.tsx, PageShell(), ClientUserResp] | lang=en
- "cve_cli": "cli.py" | kind=code-symbol | source=probe/cve/cli.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_parser(), cmd_correlate(), cmd_ingest(), cmd_status(), main()] | lang=en
- "cve_correlator": "correlator.py" | kind=code-symbol | source=probe/cve/correlator.py:L1 | neighbors=[6e2818f Add support for additional serv…, _as_dict(), _backport_marker(), correlate(), CVEFinding, mirror_age_note()] | lang=en
- "detection_correlator_detectiongap": "DetectionGap" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L62 | neighbors=[correlator.py, .generate_gap_report(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_correlate": "correlate.py" | kind=code-symbol | source=manager/detection_engine/correlate.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, correlate_smb_patch(), dedup_findings()] | lang=en
- "detection_engine_pipeline": "pipeline.py" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 26ea68c Add comprehensive tests for OS …, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[0236a60 fix(detection): full EPSS catal…, d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context()] | lang=en
- "detection_siem_elasticsiem": "ElasticSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L184 | neighbors=[siem.py, .build_query(), .parse_response(), .query_alerts(), SIEMQueryEngine, Elasticsearch via the _search API (KQL/…] | lang=en
- "detection_siem_sentinelsiem": "SentinelSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L134 | neighbors=[siem.py, Microsoft Sentinel via the Azure Monito…, .build_kql(), .parse_response(), .query_alerts(), SIEMQueryEngine] | lang=en
- "detection_siem_splunksiem": "SplunkSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L81 | neighbors=[siem.py, Splunk via the REST search endpoint (``…, SIEMQueryEngine, .build_spl(), .parse_response(), .query_alerts()] | lang=en
- "discovery_worker_discoveryjobpayload": "DiscoveryJobPayload" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L42 | neighbors=[worker.py, .__post_init__(), RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost] | lang=en
- "engine_types_discoveredhost": "DiscoveredHost" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L63 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts] | lang=en
- "exception": "Exception" | kind=code-symbol | neighbors=[ADError, CliError, LicenseError, TransportError, VedhaAuthError, MetasploitRPCError] | lang=en
- "exploit_orchestrator_rationale_1": "ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[orchestrator.py, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_107": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L107 | neighbors=[MetasploitRPCClient, .validate_safety(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError] | lang=en
- "exploit_orchestrator_rationale_114": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L114 | neighbors=[MetasploitRPCClient, .validate_scope(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError] | lang=en
- "exploit_orchestrator_rationale_134": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L134 | neighbors=[MetasploitRPCClient, .execute(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError] | lang=en
- "exploit_orchestrator_rationale_256": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L256 | neighbors=[MetasploitRPCClient, .generate_dns_callback_token(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError] | lang=en
- "exploit_orchestrator_rationale_269": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L269 | neighbors=[MetasploitRPCClient, ._check_blast_radius(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError] | lang=en
- "exploit_orchestrator_rationale_300": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L300 | neighbors=[MetasploitRPCClient, ._check_approval_required(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError] | lang=en
- "exploit_orchestrator_rationale_46": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L46 | neighbors=[MetasploitRPCClient, ExploitOrchestrator, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError] | lang=en

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
