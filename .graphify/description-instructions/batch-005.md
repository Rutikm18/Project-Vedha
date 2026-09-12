# Node Description Batch 6 of 380

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

- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[AiMessage, evidenceText(), ManagerAiResponse, POST(), validMessages(), assistant.ts] | lang=en
- "campaign_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/campaign/page.tsx:L1 | neighbors=[page.tsx, ago(), CampaignListPage(), CampaignSummary, CampaignWorkspace(), EngagementSummary] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0b7bcb82f82922f901d24413b10ed114e096a3a7": "0b7bcb8 feat: probe bootstrap key — self-register without admin login" | kind=Commit | source=git | neighbors=[agent.py, transport.py, config.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@5c6aa54b98c0dc182941305bf241ca956f806193": "5c6aa54 feat(portal-ui): portal shell/pages restyle + settings page" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@5c8e696210c1e7beaf5f6911e452bd38c701b1e8": "5c8e696 docs(probe): correct overclaiming use-case descriptions to match curren…" | kind=Commit | source=git | neighbors=[10dfc80 Add comprehensive probe testing…, use_cases.py, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ae08d19a6e9e90cc033a56b4aaeea1424c557da7": "ae08d19 feat(scanner): adaptive timeout, SYN retransmit, top-100 default (accur…" | kind=Commit | source=git | neighbors=[65e5684 feat(probe): transparent job lo…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c76b4287cfd451cab1e1212934ab3f6f36445eb6": "c76b428 backend and login page error handling update" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@e8262a30bd57c27b86d69584e3fee5ac6cd0af2b": "e8262a3 feat(probe): explicit unauthenticated_read fact for Redis exposure" | kind=Commit | source=git | neighbors=[95904f1 feat(probe): detect SMB signing…, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "lib_agents_store": "agents-store.ts" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Agent, AgentCapability, AGENTS, agentsStore, AgentStatus] | lang=en
- "lib_with_backend_withbackend": "withBackend()" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L22 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "scanner_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/scanner/host_discovery.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "scanner_os_fingerprint": "os_fingerprint.py" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…] | lang=en
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _ber_len(), _ber_parse()] | lang=en
- "schemas_common_paginatedresponse": "PaginatedResponse" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L8 | neighbors=[common.py, paginate(), BaseModel, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …] | lang=en
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L61 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()] | lang=en
- "assistant_assistantdrawer": "AssistantDrawer.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L1 | neighbors=[AdvisorFlow.tsx, AdvisorFlow(), AssistantDrawer(), ExplainResponse, Msg, Served] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@58c2d10f572ed4b7fce3da53bb9f95b696c4b94f": "58c2d10 feat(active-validation): ValidationRequest model + migration" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c140451c247068bc76251c851f7936cbeeb8a0ac": "c140451 fix(portal): clean 409 on duplicate-email provision + 7-day session ref…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c7f226f03ff7acd5ce8d6938c21a4e8b7e8997b4": "c7f226f chore: bundle pending working-tree work for release" | kind=Commit | source=git | neighbors=[656e909 feat(ui): polish login page, to…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f00ce5fb2e9537f4630e4bf1ff0326b3f6422ffe": "f00ce5f fix(ui): session-timer persistence, hydration-safe count-up, security h…" | kind=Commit | source=git | neighbors=[88c9278 feat(ai): pin manager LLM pipel…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@fbe7450ad544cc4fced845b4b28720d54fe802b9": "fbe7450 Add comprehensive documentation for Playwright CLI features- Introduced…" | kind=Commit | source=git | neighbors=[llm_report.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "dashboard_patchcomparisonmatrix": "PatchComparisonMatrix.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, d2eb44c feat(posture): add dashboard Pa…, f473173 merge: network VA accuracy, KEV…, DashboardGrid.tsx] | lang=en
- "lib_backend_backenderror": "BackendError" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L13 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "main_scripts_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _dns_probe(), _ike_probe(), interpret_dns_recursion()] | lang=en
- "vuln_enrichment_vulnenrichmentservice": "VulnEnrichmentService" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L91 | neighbors=[enrichment.py, Enriches Finding objects with NVD, EPSS…, .check_cisa_kev(), .compute_composite_risk(), .dedup_hash(), .enrich()] | lang=en
- "vuln_nessus_nessusscanner": "NessusScanner" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L37 | neighbors=[nessus.py, ._auth_headers(), .authenticate(), .close(), .create_scan(), .export_nessus_file()] | lang=en
- "ad_adcs_adcschecker": "ADCSChecker" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L52 | neighbors=[adcs.py, .check_esc1(), .check_esc4(), .check_esc8(), ._enrollment_principals(), .enumerate_templates()] | lang=en
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1517 | neighbors=[agent.py, main(), _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device()] | lang=en
- "app_main": "main.py" | kind=code-symbol | source=manager/backend/app/main.py:L1 | neighbors=[config.py, dependencies.py, GzipRequestMiddleware, lifespan(), _service_root(), unhandled_exception_handler()] | lang=en
- "commands_doctor": "doctor.ts" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L1 | neighbors=[auth.ts, loadSession(), serverUrl(), buildDoctorCommand(), C, checkDataDir()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0fbec7dfc54f7cd50921f99169270a9330d111d0": "0fbec7d feat(verification): add finding verification verdict columns + migration" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2fcec73635c396d5433940b61f8b85a02e532d50": "2fcec73 feat(verification): stamp verdicts on detection-run findings (flagged)" | kind=Commit | source=git | neighbors=[config.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@41b692a77a1dd6d2e5666f2fa2f8aa4b1e084e64": "41b692a Update project files" | kind=Commit | source=git | neighbors=[08e0594 deployement ready, AssistantFab.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@80b6dbcc5515152a76b93176716127f4f997f356": "80b6dbc Remove environment secrets from repository" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0b870c8a083dca715a6f06baf63cd015adb389d": "a0b870c fix(posture): score over open findings only; lock grade-band boundary t…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@b393dbe812e14abae4e65efa69a5640e3264827a": "b393dbe feat: Enhance Sidebar UI and introduce local run capabilities" | kind=Commit | source=git | neighbors=[3ad95f4 feat: Optimize asset service fe…, agent.py, local_run.py, use_cases.py, 1209_system_ui_backend_level_changes, addcapabilities-fable] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c0f3b4c86830cc30f1c8a4da8694f7aa5c0807dc": "c0f3b4c feat(probe-enroll): trust-on-first-use auto-enrollment + gen-env policy…" | kind=Commit | source=git | neighbors=[22701ea Add tests for scanner parity an…, agent.py, config.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5ebd3818a42f2cb9d5f6661004e3f5737bb605a": "c5ebd38 feat(sla): per-tenant custom SLA policies (item 4 backend)" | kind=Commit | source=git | neighbors=[2b4ff71 feat(fleet): one-click Approve …, main.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ddb51f2d79c6e862a9478d09389375d3f223afc3": "ddb51f2 feat(resolution): add finding resolution-lifecycle columns + migration" | kind=Commit | source=git | neighbors=[5d5c158 refactor: remove unused dashboa…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "dashboard_exposurecards": "ExposureCards.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, DashboardGrid.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-005.json

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
