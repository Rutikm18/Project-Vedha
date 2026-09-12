# Node Description Batch 17 of 380

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

- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=probe/agent/agent.py:L690 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, _bounded_env_int(), say(), Run an HTTP-claimed job while renewing …] | lang=en
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L944 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…, Release a staged job only after the man…] | lang=en
- "agent_explain_plan": "explain_plan.py" | kind=code-symbol | source=probe/agent/explain_plan.py:L1 | neighbors=[main(), _print_table(), _why(), scanner_base.py, branches.py, cache.py] | lang=en
- "agent_license": "license.py" | kind=code-symbol | source=probe/agent/license.py:L1 | neighbors=[agent.py, _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError] | lang=en
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L943 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError, Establish an authenticated WebSocket co…, Establish an authenticated WebSocket co…] | lang=en
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L852 | neighbors=[Submit a scan result to the manager.   …, Transport, _strip_nul(), .ensure_device_access(), Submit a scan result to the manager.   …, Submit a scan result to the manager.   …] | lang=en
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=probe/agent/transport.py:L49 | neighbors=[transport.py, DeviceAlreadyEnrolledError, EnrollmentRequestNotFound, Raised when a transport operation fails…, .bootstrap(), .connect_ws()] | lang=en
- "commands_interactive_ask": "ask()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L39 | neighbors=[interactive.ts, choose(), confirm(), ensureAuthenticated(), pickHostSubset(), pickTargets()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0236a6011fa2a49e65e7f5cad6b04f643f83c6f7": "0236a60 fix(detection): full EPSS catalog so exploit-probability isn't blind" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/nvd-vuln-detection-and-ingest-hard…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@3ddc104d6808223a444b74861353f0c8c76b0c1a": "3ddc104 feat: unify customer and manager findings workflows" | kind=Commit | source=git | neighbors=[22c59d4 Add implementation plan: univer…, 1209_system_ui_backend_level_changes, cross-os-agent-installer, 57751e5 merge: cross-os installer docs …, page.tsx, backend.ts] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd853230be2d89a28a641677bd8900d3071b1186": "bd85323 feat(probe): self-heal re-enroll, local-run driver, WS send resilience" | kind=Commit | source=git | neighbors=[agent.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@dbcff7fc782d1da19c2bf749b8ac45146179b864": "dbcff7f feat: Update UseCaseCard component for improved description handling an…" | kind=Commit | source=git | neighbors=[b393dbe feat: Enhance Sidebar UI and in…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L24 | neighbors=[page.tsx, page.tsx, PageShell.tsx, page.tsx, DashboardWorkspace.tsx, page.tsx] | lang=en
- "components_toastprovider": "ToastProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L1 | neighbors=[layout.tsx, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, Toast] | lang=en
- "cve_vulndb_vulndb": "VulnDB" | kind=code-symbol | source=probe/cve/vulndb.py:L62 | neighbors=[vulndb.py, .add_cpe_match(), .close(), .commit(), .counts(), .cves_for_cpe()] | lang=en
- "detection_engine_posture_rules_detect_posture_traced": "detect_posture_traced()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1032 | neighbors=[posture_rules.py, detect_all_traced(), detect_posture(), _calibrate_host_findings(), compute_risk(), detect_exposed_services()] | lang=en
- "detection_resolution": "resolution.py" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, 5c59db1 Implement instance locking mech…, 9a36729 feat(resolution): coverage buil…, bd409f5 feat(resolution): async applier…, cbf5d6c feat(resolution): pure decision…, d98f654 feat(manager): network-VA campa…] | lang=en
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts] | lang=en
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, ManagerAiResponse, POST(), assistant.ts] | lang=en
- "fleet_fleetjobs": "FleetJobs.tsx" | kind=code-symbol | source=manager/frontend/app/fleet/FleetJobs.tsx:L1 | neighbors=[page.tsx, 07ba102 feat: enhance UI UX and detecti…, 198bae4 snapshot: uncommitted system/ui…, 25c014d feat: enhance campaign progress…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…] | lang=en
- "hooks_usetoast": "useToast.ts" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, EngagementStatusControl.tsx, page.tsx, page.tsx, page.tsx, page.tsx] | lang=en
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), OtpEntry, otpStore, OtpVerifyResult] | lang=en
- "lib_engagement_workspace_api": "engagement-workspace-api.ts" | kind=code-symbol | source=manager/frontend/lib/engagement-workspace-api.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, page.tsx, adapters.ts, toApiEngagementPatch(), toUiEngagement(), toUiFinding()] | lang=en
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, counters, generateFindingId(), resetCounters()] | lang=en
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, countBySeverity(), NucleiMatch, nucleiMatchToFinding()] | lang=en
- "main_scripts_ipv6_discovery": "ipv6_discovery.py" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, discover_ipv6_hosts(), _is_ipv6(), main()] | lang=en
- "main_scripts_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, _have_nmap(), main(), NmapExecutionError] | lang=en
- "main_scripts_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, build_default_funnel(), _candidate_ports(), FunnelResult] | lang=en
- "main_scripts_service_banner": "service_banner.py" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…] | lang=en
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, str, Base, TimestampMixin, AgentRegisterRequest, AgentRegisterResponse] | lang=en
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 58c2d10 feat(active-validation): Valida…, 6bb51ab feat: add detection-explain end…, 81c81cb feat: implement outbox reclaim …] | lang=en
- "native_http_probe": "http-probe.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractTitle(), fingerprint(), HttpProbeResult] | lang=en
- "portal_portalshell_portalshell": "PortalShell()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L11 | neighbors=[page.tsx, page.tsx, DashboardWorkspace.tsx, page.tsx, page.tsx, page.tsx] | lang=en
- "report_finding_model_assess": "assess()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L697 | neighbors=[finding-model.ts, attackerStatement(), confidenceOf(), parseCvss(), priorityOf(), readinessOf()] | lang=en
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L235 | neighbors=[agents.py, BaseModel, bootstrap_agent(), register_agent(), Asset, Engagement] | lang=en
- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L349 | neighbors=[agents.py, BaseModel, ._validate_intensity(), ._validate_uc(), Asset, Engagement] | lang=en
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L654 | neighbors=[agents.py, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…] | lang=en
- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L46 | neighbors=[ai_report.py, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath] | lang=en
- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L56 | neighbors=[ai_report.py, ReviewRequest, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath] | lang=en
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L86 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError] | lang=en

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
