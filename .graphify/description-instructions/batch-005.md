# Node Description Batch 6 of 330

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@3c9062a2ad7bbd5d67a2343aa035a835d02e3818": "3c9062a refactor: Update dashboard components for improved styling and function…" | kind=Commit | source=git | neighbors=[page.tsx, addcapabilities-fable, main, ui-ux-backend-updates0109, 83d2039 docs: add prompt output documen…, DashboardCharts.tsx]
- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c4386e4cbc0ee346a71c211a96326772b677c561": "c4386e4 feat(customers): operator Customers dashboard + per-customer portal slug" | kind=Commit | source=git | neighbors=[ae08d19 feat(scanner): adaptive timeout…, main.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[neo4j_client.py, .available(), .close(), .connect(), .ensure_schema(), .__init__()]
- "lib_assistant": "assistant.ts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L1 | neighbors=[page.tsx, AdvisorFlow.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, 1fe16c8 stable but some dead code, need…]
- "main_scripts_findings_data": "_data()" | kind=code-symbol | source=probe/main_scripts/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()]
- "scanner_findings_data": "_data()" | kind=code-symbol | source=probe/scanner/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()]
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…]
- "scanner_va_campaign": "va_campaign.py" | kind=code-symbol | source=probe/scanner/va_campaign.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _alive(), _atomic_write_json(), _bounded_gather()]
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L795 | neighbors=[test_detection_core.py, .test_cvss_critical(), .test_cvss_high(), .test_cvss_low(), .test_cvss_medium(), .test_elevated_epss_high()]
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=probe/tests/test_result_spool.py:L18 | neighbors=[test_result_spool.py, .test_byte_high_water_mark_pauses_new_w…, .test_custom_retry_config(), .test_exists(), .test_file_high_water_mark_pauses_new_w…, .test_flush_quarantines_permanent_rejec…]
- "tests_test_service_posture_rules_fire": "_fire()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L50 | neighbors=[test_service_posture_rules.py, _fact(), test_rule_fires_on_captured_shape(), test_smb_null_session_fires_when_permit…, test_smb_null_session_is_silent_on_the_…, test_ssh_rules_against_live_capture()]
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L108 | neighbors=[nuclei.py, ._consume_stdout(), .__init__(), ._map_finding(), .parse_output(), ._partial_or_raise()]
- "workflow_asset": "asset.py" | kind=code-symbol | source=probe/workflow/asset.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3ad95f4 feat: Optimize asset service fe…, 3c9062a refactor: Update dashboard comp…, 64e8290 feat(campaign): implement VA ca…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …]
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()]
- "ai_llm_report_llmreportgenerator": "LLMReportGenerator" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L82 | neighbors=[llm_report.py, .available(), ._complete(), ._generate_and_store(), .generate_detection_rule_explanation(), .generate_executive_summary()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@10ceacaffacf60f95eeb0e9b2b247b62bfa5dfb8": "10ceaca feat: implement AI model fallback mechanism and enhance model selection…" | kind=Commit | source=git | neighbors=[AssistantDrawer.tsx, ModelSwitcher.tsx, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "commit:repo:github.com/Rutikm18/Project-Vedha@8ebc0534dda8a1316f41c2fccf928f42acf9ed46": "8ebc053 feat(risk-rank-ui): surface verification + lifecycle state on findings …" | kind=Commit | source=git | neighbors=[6a1c958 docs(plans): record execution s…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bb0ef3d473623bac3404761b5c3d34baa72612dd": "bb0ef3d feat(probe): route DB services on non-standard ports via banner signatu…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L42 | neighbors=[orchestrator.py, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute(), .generate_dns_callback_token()]
- "lib_campaign_store": "campaign-store.ts" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L1 | neighbors=[route.ts, 07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…, route.ts]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser()]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, computeOverallProgress()]
- "main_scripts_va_campaign": "va_campaign.py" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _alive(), _atomic_write_json(), _bounded_gather()]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[0f0097b feat(posture): mirror posture s…, 1fe16c8 stable but some dead code, need…, a0b870c fix(posture): score over open f…, d1b4dd3 trim frontend to 7 core pages; …, fadb4f5 fix(posture): hoist report-sect…, dependencies.py]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit()]
- "routers_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 3c277ba feat(lifecycle): add POST /find…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, 8ebc053 feat(risk-rank-ui): surface ver…]
- "scanner_service_enum": "service_enum.py" | kind=code-symbol | source=probe/scanner/service_enum.py:L1 | neighbors=[2534404 scanner(service_enum): commit o…, 78d51c5 opsec(scanner): de-sign service…, 8f6bf49 Refactor code structure and rem…, classify_roles(), _dns_read_name(), Enrichment]
- "scanner_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, 8f6bf49 Refactor code structure and rem…]
- "tests_test_agents": "test_agents.py" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, f3bb8db feat(manager): cross-worker WS …]
- "tests_test_detection_core_testingestfile": "TestIngestFile" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L226 | neighbors=[test_detection_core.py, .test_authoritative_scanner_creates_aut…, .test_empty_file(), .test_hostname_target_not_ip_keyed(), .test_multi_file_accumulation(), .test_quarantines_malformed()]
- "tests_test_host_health_r": "_r()" | kind=code-symbol | source=probe/tests/test_host_health.py:L24 | neighbors=[test_host_health.py, .test_flaky_note_is_not_an_error(), .test_offline_fact_carries_an_error_so_…, .test_healthy_host_produces_no_facts_at…, .test_offline_fact_marks_the_scan_incom…, .test_offline_host_stops_accumulating_o…]
- "tests_test_posture": "test_posture.py" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 0f0097b feat(posture): mirror posture s…, 237a831 feat(posture): add run comparis…, 2cddd52 fix(posture): tenant-scope run …, 5238865 feat(posture): add pure scoring…, 9de087a feat(posture): add GET /analyti…]
- "tests_test_use_cases": "test_use_cases.py" | kind=code-symbol | source=probe/tests/test_use_cases.py:L1 | neighbors=[01f4398 feat(probe): IoT survey reaches…, 22701ea Add tests for scanner parity an…, 5c8e696 docs(probe): correct overclaimi…, 95904f1 feat(probe): detect SMB signing…, bce780a feat(probe): enumerate HTTP met…, fe868e6 feat(probe): real UDP amplifica…]
- "workflow_modes": "modes.py" | kind=code-symbol | source=probe/workflow/modes.py:L1 | neighbors=[engine.py, explain_plan.py, local_run.py, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …]
- "ad_asreproast_asreproastchecker": "ASREPRoastChecker" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L34 | neighbors=[asreproast.py, ._format_asrep_hash(), .generate_finding(), .get_no_preauth_accounts(), .request_asrep(), Enumerate AS-REP roastable accounts and…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@01f43989ed63ef32dcf3abe8b305659ff281c464": "01f4398 feat(probe): IoT survey reaches the banner stage (service_fingerprint)" | kind=Commit | source=git | neighbors=[use_cases.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@50d65540db573b6b680c257d3d693b216940069f": "50d6554 feat(active-validation): approve→enqueue endpoint + result ingestion (P…" | kind=Commit | source=git | neighbors=[3c277ba feat(lifecycle): add POST /find…, main.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]

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
