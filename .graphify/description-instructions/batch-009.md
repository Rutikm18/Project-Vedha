# Node Description Batch 10 of 380

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

- "tests_test_vuln_enrichment": "test_vuln_enrichment.py" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _make_http_mock(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_dedup_hash_case_insensitive_cve()]
- "ad_ntlm_relay_ntlmrelaychecker": "NTLMRelayChecker" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L30 | neighbors=[ntlm_relay.py, .check_ldap_signing(), .check_smb_signing(), .generate_finding(), ._probe_smb_host(), Probe SMB/LDAP signing posture across a…]
- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=probe/agent/task_runner.py:L1 | neighbors=[JobResult, prepare_result_dir(), _result_dir(), TaskRunner, use_cases.py, scanner_base.py]
- "commands_scan": "scan.ts" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L1 | neighbors=[requireAuth(), buildScanCommand(), printAiComment(), PROFILE_TOOLS, resolveTargets(), scanCommand()]
- "commands_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L1 | neighbors=[buildToolsCommand(), C, ln(), showSpinner(), w(), installer.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1af3404cd899c56eec3439d379b9f621f044baf9": "1af3404 feat(deploy): probe-free manager stack + port-80 edge ingress" | kind=Commit | source=git | neighbors=[0e22dbf feat(probe): bounded auto-troub…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@64e8290422a4d984a2428bb30ee728d3b5f8f2c4": "64e8290 feat(campaign): implement VA campaign progress endpoint and UI integrat…" | kind=Commit | source=git | neighbors=[26ea68c Add comprehensive tests for OS …, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "lib_clients_store": "clients-store.ts" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, ClientJiraConfig, ClientNotifyConfig, ClientSettings, ClientsFile]
- "lib_openvas_client": "openvas-client.ts" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, findings-store.ts, FindingSeverity, boundedEnvMs()]
- "main_scripts_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, device_hint()]
- "main_scripts_service_enum": "service_enum.py" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L1 | neighbors=[2534404 scanner(service_enum): commit o…, 78d51c5 opsec(scanner): de-sign service…, 8f6bf49 Refactor code structure and rem…, daf3de2 feat(scanner): add service enum…, classify_roles(), _dns_read_name()]
- "models_enums_assetcriticality": "AssetCriticality" | kind=code-symbol | source=manager/backend/app/models/enums.py:L40 | neighbors=[enums.py, str, Asset, Attack path analysis API (AttackPathSer…, AssetIn, AssetOut]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …]
- "scope_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/scope/page.tsx:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, page.tsx, EngagementWorkspace()]
- "services_llm": "llm.py" | kind=code-symbol | source=manager/backend/app/services/llm.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, 7a637eb feat: network VA accuracy, KEV …]
- "tests_test_detection_core_testdeceptionscore": "TestDeceptionScore" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L685 | neighbors=[test_detection_core.py, .test_capped_at_1(), .test_combined_high(), .test_contradictory_os(), .test_high_product_count(), .test_low_product_count()]
- "tests_test_main_scripts_rdp": "test_main_scripts_rdp.py" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, _cc(), _run(), test_cc_without_negotiation_is_standard…, test_confirmed_rdp_wins_dedup_over_port…]
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=probe/tests/test_transport.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c59db1 Implement instance locking mech…, 63d9c9a fix(probe): recover from 409 wh…, 81c81cb feat: implement outbox reclaim …, b4b12a9 Rename project and update files]
- "vuln_nuclei_nucleiscanerror": "NucleiScanError" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L89 | neighbors=[nuclei.py, RuntimeError, .__init__(), ._partial_or_raise(), .run_scan(), Fatal Nuclei failure, optionally carryi…]
- "agent_agent_ws_http_poll_fallback": "_ws_http_poll_fallback()" | kind=code-symbol | source=probe/agent/agent.py:L1039 | neighbors=[agent.py, Poll pending jobs even while WS is conn…, _run_ws_push_loop(), _flush_spool_over_http(), say(), _ws_run_job()]
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=probe/agent/agent.py:L968 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), _dbg(), _job_intent()]
- "app_layout": "layout.tsx" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L1 | neighbors=[metadata, RootLayout(), AssistantProvider.tsx, AssistantProvider(), QueryProvider.tsx, QueryProvider()]
- "auth_router": "router.py" | kind=code-symbol | source=manager/backend/app/auth/router.py:L1 | neighbors=[database.py, dependencies.py, ratelimit.py, access_claims_for(), _authenticate(), create_personal_access_token()]
- "auth_startup": "startup.py" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L1 | neighbors=[config.py, database.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/probe-usecase-alignment": "feat/probe-usecase-alignment" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "commands_interactive_confirm": "confirm()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L79 | neighbors=[interactive.ts, ask(), mainMenu(), pickHostSubset(), pickModulesByCategory(), pickTargets()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@00c6648b4d38308e37ce245514b25f99cb5b3ae9": "00c6648 feat(settings): editable email/Slack/Jira integrations wired to backend…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@37fa611652538968dbf827eaf98cdcab59c052b2": "37fa611 harden(scanner): XML-entity guard + list-form argv (CWE-611/78/88)" | kind=Commit | source=git | neighbors=[2c53ae9 evasion(scanner): randomized sc…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9c973dd02e4777bcd7cebae84b6c80fd96fa001f": "9c973dd feat(scanner): tarpit/honeypot detection in port-scan summary (C5)" | kind=Commit | source=git | neighbors=[2de251b feat(scanner): ICMP timestamp f…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bc08715ed9a3be7d600b4595a6872f649784fd00": "bc08715 feat(agent): risk-tier action classification (fail-closed)" | kind=Commit | source=git | neighbors=[3569103 docs(agent): research + design …, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@dec1e7cfa829a295630af88da9f11a5f2e8175d4": "dec1e7c fix(scanner): resolve() family fallback for dual-stack hosts (task A9)" | kind=Commit | source=git | neighbors=[78d51c5 opsec(scanner): de-sign service…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@ecbb4adbc9733f25281faa5986dbcfdc1e7520ae": "ecbb4ad feat(agent): rules-of-engagement policy evaluation (verdict-vs-action, …" | kind=Commit | source=git | neighbors=[bc08715 feat(agent): risk-tier action c…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "discovery_worker_discoveryworker": "DiscoveryWorker" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L55 | neighbors=[worker.py, ._banner_grab_all(), ._grab_one(), .__init__(), .run(), ._run_nmap()]
- "main_scripts_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 4d0377d Add unit tests for SMB scanner,…, build_op_msg_command(), _build_tds_prelogin(), DBScanner, extract_mongo_version()]
- "main_scripts_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner]
- "main_scripts_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L1 | neighbors=[09c6c0a feat(probe): per-host wall-cloc…, 198bae4 snapshot: uncommitted system/ui…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…]
- "main_scripts_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, build_client_hello(), cipher_code(), _ext()]
- "report_adapt": "adapt.ts" | kind=code-symbol | source=manager/frontend/lib/report/adapt.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 315cf9c feat(frontend): refine reports …, 76240ac UI UX Update, 86b4fb0 Add UI-Finding to RawFinding ad…, be2f891 Frontend consumes backend repor…, f023fa5 Add portalToRawFinding adapter …]
- "reportsection_spec": "spec.ts" | kind=code-symbol | source=reportsection/spec.ts:L1 | neighbors=[ef14810 Implement instance locking mech…, assess(), confidenceOf(), priorityOf(), RawFinding, readinessOf()]
- "routers_agents_agent_ownership_check": "_agent_ownership_check()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L621 | neighbors=[agents.py, get_agent_jobs(), heartbeat(), list_result_chunks(), Verify that the JWT token bearer IS the…, refresh_agent_registration()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-009.json

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
