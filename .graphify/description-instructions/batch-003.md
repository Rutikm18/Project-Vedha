# Node Description Batch 4 of 236

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

- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts] | lang=en
- "tests_test_detection_core_testverify": "TestVerify" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L637 | neighbors=[test_detection_core.py, .test_ai_cap_at_60(), .test_ai_no_cap_if_already_below(), .test_auth_enforced_penalty(), .test_authoritative_tier_base_95(), .test_backport_penalty()] | lang=en
- "tests_test_probe_next_features": "test_probe_next_features.py" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, engine.py, use_cases.py, scanner_base.py, _cache_with(), test_device_inventory_post_stage_classi…] | lang=en
- "timestampmixin": "TimestampMixin" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, DetectionConfig] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@81c81cbb1d1a039f73bc699431d61b9dd84648fe": "81c81cb feat: implement outbox reclaim tests and add enrollment token functiona…" | kind=Commit | source=git | neighbors=[agent.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "dashboard_dashboardgrid": "DashboardGrid.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L1 | neighbors=[page.tsx, 5d5c158 refactor: remove unused dashboa…, Primitives.tsx, Panel(), Agent, AGENT_STATUS] | lang=en
- "dashboard_liveoverview": "LiveOverview.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5d5c158 refactor: remove unused dashboa…, d1b4dd3 trim frontend to 7 core pages; …, DashboardGrid.tsx, Primitives.tsx] | lang=en
- "lib_agents_store": "agents-store.ts" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Agent, AgentCapability, AGENTS, agentsStore, AgentStatus] | lang=en
- "portal_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, 5c6aa54 feat(portal-ui): portal shell/p…, c52feb4 feat(portal): reskin User Porta…, portal-client.ts, GRADE_VAR, portalApi()] | lang=en
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _ber_len(), _ber_parse()] | lang=en
- "schemas_common_paginatedresponse": "PaginatedResponse" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L8 | neighbors=[common.py, paginate(), BaseModel, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …] | lang=en
- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, d1b4dd3 trim frontend to 7 core pages; …, DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx] | lang=en
- "tests_test_detection_validation_testdetectioncorrelator": "TestDetectionCorrelator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L49 | neighbors=[test_detection_validation.py, .setup_method(), .test_compute_coverage(), .test_coverage_empty(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking()] | lang=en
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L61 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()] | lang=en
- "assistant_assistantdrawer": "AssistantDrawer.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L1 | neighbors=[AdvisorFlow.tsx, AdvisorFlow(), AssistantDrawer(), ExplainResponse, Msg, Served] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@5d5c158ce109aafccb3ad1e6407c6d6bf231a1f3": "5d5c158 refactor: remove unused dashboard components and mock data- Deleted Sla…" | kind=Commit | source=git | neighbors=[layout.tsx, page.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "components_dashboardcharts": "DashboardCharts.tsx" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5d5c158 refactor: remove unused dashboa…, d1b4dd3 trim frontend to 7 core pages; …, ActivityItem] | lang=en
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 656e909 feat(ui): polish login page, to…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "lib_portal_client": "portal-client.ts" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, b393dbe feat: Enhance Sidebar UI and in…, c140451 fix(portal): clean 409 on dupli…, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…, page.tsx] | lang=en
- "routers_engagements": "engagements.py" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b393dbe feat: Enhance Sidebar UI and in…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py] | lang=en
- "vuln_enrichment_vulnenrichmentservice": "VulnEnrichmentService" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L91 | neighbors=[enrichment.py, Enriches Finding objects with NVD, EPSS…, .check_cisa_kev(), .compute_composite_risk(), .dedup_hash(), .enrich()] | lang=en
- "vuln_nessus_nessusscanner": "NessusScanner" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L37 | neighbors=[nessus.py, ._auth_headers(), .authenticate(), .close(), .create_scan(), .export_nessus_file()] | lang=en
- "ad_adcs_adcschecker": "ADCSChecker" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L52 | neighbors=[adcs.py, .check_esc1(), .check_esc4(), .check_esc8(), ._enrollment_principals(), .enumerate_templates()] | lang=en
- "commands_doctor": "doctor.ts" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L1 | neighbors=[auth.ts, loadSession(), serverUrl(), buildDoctorCommand(), C, checkDataDir()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@30261ebec685fe061217d7e71faa08b5a4b6d5ea": "30261eb feat: enhance advisor flow with structured brief and probe selection- A…" | kind=Commit | source=git | neighbors=[AdvisorFlow.tsx, AssistantDrawer.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@35f02a999c05b5ec503c4c44f7f158f5d0018937": "35f02a9 feat(portal): rich scan request (type/targets/intensity) + dashboard en…" | kind=Commit | source=git | neighbors=[portal_scope.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@a789cca150b7688941e2f9229631f493d3fab094": "a789cca scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=pt
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…, PageShell.tsx, PageShell()] | lang=en
- "main_scripts_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _dns_probe(), _ike_probe(), interpret_dns_recursion(), interpret_ike()] | lang=en
- "tests_test_detection_core_testversioninranges": "TestVersionInRanges" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L312 | neighbors=[test_detection_core.py, .test_empty_ranges(), .test_ignores_unknown_type(), .test_introduced_fixed(), .test_last_affected(), .test_no_match_returns_false_none()] | lang=en
- "ad_kerberoast_kerberoastchecker": "KerberoastChecker" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L39 | neighbors=[kerberoast.py, ._encode_tgs_rep(), .generate_finding(), .get_spn_accounts(), ._pwd_last_set(), .request_tgs()] | lang=en
- "ad_ldap_enum_ace": "ACE" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L84 | neighbors=[ldap_enum.py, ._parse_security_descriptor(), A simplified access-control entry parse…, ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…] | lang=en
- "agent_transport": "transport.py" | kind=code-symbol | source=probe/agent/transport.py:L1 | neighbors=[agent.py, _atomic_write_private_state(), DeviceAlreadyEnrolledError, _enrollment_conflict_detail(), _strip_nul(), _sync_directory()] | lang=en
- "cli_auth": "auth.ts" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L1 | neighbors=[apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl()] | lang=en
- "cli_llm": "llm.ts" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L1 | neighbors=[client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@37376de4dd5dbfb3ed764fc548cb277c51ad2077": "37376de hardening(scanner): OPSEC de-sign packets + os_fingerprint correctness/…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main] | lang=en
- "dashboard_posturescorecard": "PostureScorecard.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, aa560a0 feat(posture): add dashboard Po…, DashboardGrid.tsx, PatchComparisonMatrix.tsx, Primitives.tsx, Delta()] | lang=en
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[neo4j_client.py, .available(), .close(), .connect(), .ensure_schema(), .__init__()] | lang=en
- "main_scripts_findings_scanner": "_scanner()" | kind=code-symbol | source=probe/main_scripts/findings.py:L110 | neighbors=[findings.py, build_service_index(), _rule_cleartext_and_exposure(), _rule_dns(), _rule_ftp(), _rule_ipmi()] | lang=en
- "routers_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, b393dbe feat: Enhance Sidebar UI and in…, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…, fbe7450 Add comprehensive documentation…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-003.json

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
