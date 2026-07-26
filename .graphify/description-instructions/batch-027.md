# Node Description Batch 28 of 104

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

- "schemas_engagement_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L31 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_finding_rationale_21": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[DetectionStatus, FindingSeverity, FindingStatus, FindingPatch]
- "scripts_seed_admin": "seed_admin.py" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, database.py, seed(), Idempotent admin seeder.  Creates a ten…]
- "scripts_seed_admin_rationale_1": "Idempotent admin seeder.  Creates a tenant + admin user so you can log in (there" | kind=entity | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[UserRole, Tenant, User, seed_admin.py]
- "services_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, compute_exposure(), _sev(), Exposure analytics — protocol risk + zo…]
- "services_job_result_service": "job_result_service.py" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, process_job_result(), _promote_assets(), job_result_service.py — shared job resu…]
- "states_datastate_datastate": "DataState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L106 | neighbors=[page.tsx, page.tsx, page.tsx, DataState.tsx]
- "states_datastate_errorstate": "ErrorState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L50 | neighbors=[Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx, DataState.tsx]
- "tests_test_agents_testagentexecutabletypes": "TestAgentExecutableTypes" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L28 | neighbors=[test_agents.py, ScanJobType, .test_network_types_included(), .test_server_side_types_excluded()]
- "tests_test_agents_testgetagentjobs": "TestGetAgentJobs" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L139 | neighbors=[test_agents.py, ScanJobType, .test_404_when_agent_unknown(), .test_jobs_include_params()]
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_exploit_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L38 | neighbors=[test_exploit_engine.py, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=probe/tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=probe/tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=probe/tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_nessus_scanner_rationale_1": "Unit tests for NessusScanner — all HTTP calls mocked." | kind=entity | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[FindingSeverity, FindingStatus, test_nessus_scanner.py, NessusScanner]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=probe/tests/test_probe_core.py:L449 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L243 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L272 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=probe/tests/test_probe_core.py:L286 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=probe/tests/test_probe_core.py:L225 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=probe/tests/test_probe_core.py:L393 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]
- "tests_test_probe_core_testscanresult": "TestScanResult" | kind=code-symbol | source=probe/tests/test_probe_core.py:L205 | neighbors=[test_probe_core.py, .test_default_status_observed(), .test_default_timestamp_present(), .test_to_json_roundtrip()]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_transport.py:L98 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=probe/tests/test_transport.py:L246 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=probe/tests/test_transport.py:L129 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=probe/tests/test_transport.py:L56 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "versions_0001_initial": "0001_initial.py" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), Initial schema — all tables  Revision I…]
- "versions_0002_services_agents": "0002_services_agents.py" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add services and agents tables  Revisio…]
- "versions_0003_vuln_scan_fields": "0003_vuln_scan_fields.py" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add enrichment fields index + webhook c…]
- "versions_0004_exploit_tables": "0004_exploit_tables.py" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), Exploit results, approvals, and audit l…]
- "versions_0005_detection_validation": "0005_detection_validation.py" | kind=code-symbol | source=manager/backend/alembic/versions/0005_detection_validation.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), Detection validation: attack_timeline, …]
- "versions_0006_llm_outputs": "0006_llm_outputs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), AI engine: llm_outputs table + reviewst…]
- "versions_0007_scale_indexes": "0007_scale_indexes.py" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3: composite indexes for the hot aggre…]
- "versions_0008_scan_results": "0008_scan_results.py" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3-#10: append-only scan_results table …]
- "versions_0009_outbox_events": "0009_outbox_events.py" | kind=code-symbol | source=manager/backend/alembic/versions/0009_outbox_events.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, downgrade(), upgrade(), Transactional outbox for durable backgr…]
- "versions_0010_detection_runs": "0010_detection_runs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, downgrade(), upgrade(), Temporal detection: detection_runs tabl…]
- "versions_0011_job_lease": "0011_job_lease.py" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, downgrade(), upgrade(), Job leasing: scan_jobs.lease_expires_at…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-027.json

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
