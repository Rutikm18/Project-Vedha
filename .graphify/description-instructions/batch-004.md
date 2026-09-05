# Node Description Batch 5 of 336

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

- "workers_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 21ebc46 feat(detection): unified priori…, 6bb51ab feat: add detection-explain end…, 6be8259 feat(integrations): outbox deli…, 81c81cb feat: implement outbox reclaim …, 8f6bf49 Refactor code structure and rem…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@30261ebec685fe061217d7e71faa08b5a4b6d5ea": "30261eb feat: enhance advisor flow with structured brief and probe selection- A…" | kind=Commit | source=git | neighbors=[AdvisorFlow.tsx, AssistantDrawer.tsx, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@35f02a999c05b5ec503c4c44f7f158f5d0018937": "35f02a9 feat(portal): rich scan request (type/targets/intensity) + dashboard en…" | kind=Commit | source=git | neighbors=[portal_scope.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@a789cca150b7688941e2f9229631f493d3fab094": "a789cca scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=pt
- "lib_agents_store": "agents-store.ts" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Agent, AgentCapability, AGENTS, agentsStore, AgentStatus] | lang=en
- "lib_with_backend_withbackend": "withBackend()" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L22 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "scanner_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/scanner/host_discovery.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "scanner_os_fingerprint": "os_fingerprint.py" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…] | lang=en
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _ber_len(), _ber_parse()] | lang=en
- "schemas_common_paginatedresponse": "PaginatedResponse" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L8 | neighbors=[common.py, paginate(), BaseModel, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …] | lang=en
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L61 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()] | lang=en
- "assistant_assistantdrawer": "AssistantDrawer.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L1 | neighbors=[AdvisorFlow.tsx, AdvisorFlow(), AssistantDrawer(), ExplainResponse, Msg, Served] | lang=en
- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[AiMessage, evidenceText(), ManagerAiResponse, POST(), validMessages(), assistant.ts] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@37376de4dd5dbfb3ed764fc548cb277c51ad2077": "37376de hardening(scanner): OPSEC de-sign packets + os_fingerprint correctness/…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches] | lang=en
- "dashboard_patchcomparisonmatrix": "PatchComparisonMatrix.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, d2eb44c feat(posture): add dashboard Pa…, f473173 merge: network VA accuracy, KEV…, DashboardGrid.tsx] | lang=en
- "detection_engine_posture_rules_d": "_d()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L242 | neighbors=[posture_rules.py, _cert(), _dns_zone_transfer(), _ftp_anonymous(), _ipmi_cipher_zero(), _ldap_anonymous_bind()] | lang=en
- "lib_backend_backenderror": "BackendError" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L13 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "main_scripts_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _dns_probe(), _ike_probe(), interpret_dns_recursion()] | lang=en
- "portal_portalshell": "PortalShell.tsx" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L1 | neighbors=[page.tsx, 5c6aa54 feat(portal-ui): portal shell/p…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, c52feb4 feat(portal): reskin User Porta…, f473173 merge: network VA accuracy, KEV…] | lang=en
- "tests_test_manager_ai": "test_manager_ai.py" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 1fe16c8 stable but some dead code, need…, 75650c1 feat: add Posture & Patch-Compa…, 7d8d3f3 merge: resolve conflicts with o…, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…] | lang=en
- "vuln_enrichment_vulnenrichmentservice": "VulnEnrichmentService" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L91 | neighbors=[enrichment.py, Enriches Finding objects with NVD, EPSS…, .check_cisa_kev(), .compute_composite_risk(), .dedup_hash(), .enrich()] | lang=en
- "vuln_nessus_nessusscanner": "NessusScanner" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L37 | neighbors=[nessus.py, ._auth_headers(), .authenticate(), .close(), .create_scan(), .export_nessus_file()] | lang=en
- "ad_adcs_adcschecker": "ADCSChecker" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L52 | neighbors=[adcs.py, .check_esc1(), .check_esc4(), .check_esc8(), ._enrollment_principals(), .enumerate_templates()] | lang=en
- "commands_doctor": "doctor.ts" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L1 | neighbors=[auth.ts, loadSession(), serverUrl(), buildDoctorCommand(), C, checkDataDir()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c52feb410341da146973ec21b59b90f8985b8c73": "c52feb4 feat(portal): reskin User Portal to console theme + comprehensive dashb…" | kind=Commit | source=git | neighbors=[35f02a9 feat(portal): rich scan request…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@fd5dc9658c8f71049864680b5317900dde34f0eb": "fd5dc96 feat(remediation): AI + deterministic-KB per-finding remediation plans" | kind=Commit | source=git | neighbors=[54503ae feat(scanner): SYN path harvest…, llm_report.py, main.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work] | lang=en
- "dashboard_exposurecards": "ExposureCards.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, DashboardGrid.tsx] | lang=en
- "id_campaignprogress": "CampaignProgress.tsx" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L1 | neighbors=[page.tsx, 07ba102 feat: enhance UI UX and detecti…, 25c014d feat: enhance campaign progress…, 64e8290 feat(campaign): implement VA ca…, 6bb51ab feat: add detection-explain end…, 7d8d3f3 merge: resolve conflicts with o…] | lang=en
- "id_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 8f6bf49 Refactor code structure and rem…, a789cca scanner: real use-case library,…, d1b4dd3 trim frontend to 7 core pages; …, d98f654 feat(manager): network-VA campa…, ApiActivity] | lang=en
- "lib_backend_bearerfrom": "bearerFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L97 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "main_scripts_findings_scanner": "_scanner()" | kind=code-symbol | source=probe/main_scripts/findings.py:L110 | neighbors=[findings.py, build_service_index(), _rule_cleartext_and_exposure(), _rule_dns(), _rule_ftp(), _rule_ipmi()] | lang=en
- "main_scripts_os_fingerprint": "os_fingerprint.py" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, dec1e7c fix(scanner): resolve() family …] | lang=en
- "scanner_findings_scanner": "_scanner()" | kind=code-symbol | source=probe/scanner/findings.py:L110 | neighbors=[findings.py, build_service_index(), _rule_cleartext_and_exposure(), _rule_dns(), _rule_ftp(), _rule_ipmi()] | lang=en
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[engine.py, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…] | lang=en
- "tests_test_detection_core_testversioninranges": "TestVersionInRanges" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L354 | neighbors=[test_detection_core.py, .test_empty_ranges(), .test_ignores_unknown_type(), .test_introduced_fixed(), .test_last_affected(), .test_no_match_returns_false_none()] | lang=en
- "websocket_manager_agentconnectionmanager": "AgentConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L80 | neighbors=[manager.py, .agent_stale_after(), .connected_agents(), .connected_count(), .deliver_job(), .get_agent_status()] | lang=en
- "ad_kerberoast_kerberoastchecker": "KerberoastChecker" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L39 | neighbors=[kerberoast.py, ._encode_tgs_rep(), .generate_finding(), .get_spn_accounts(), ._pwd_last_set(), .request_tgs()] | lang=en
- "ad_ldap_enum_ace": "ACE" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L84 | neighbors=[ldap_enum.py, ._parse_security_descriptor(), A simplified access-control entry parse…, ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…] | lang=en
- "agent_use_cases": "use_cases.py" | kind=code-symbol | source=probe/agent/use_cases.py:L1 | neighbors=[agent.py, task_runner.py, _as_int(), normalize_intensity(), resolve(), use_case_for_code()] | lang=en
- "app_main": "main.py" | kind=code-symbol | source=manager/backend/app/main.py:L1 | neighbors=[config.py, dependencies.py, GzipRequestMiddleware, lifespan(), _service_root(), unhandled_exception_handler()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-004.json

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
