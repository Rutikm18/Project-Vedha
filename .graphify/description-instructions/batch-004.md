# Node Description Batch 5 of 236

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

- "scanner_findings_scanner": "_scanner()" | kind=code-symbol | source=probe/scanner/findings.py:L110 | neighbors=[findings.py, build_service_index(), _rule_cleartext_and_exposure(), _rule_dns(), _rule_ftp(), _rule_ipmi()]
- "scanner_os_fingerprint": "os_fingerprint.py" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, dec1e7c fix(scanner): resolve() family …, accept_echo_reply()]
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L726 | neighbors=[test_detection_core.py, .test_cvss_critical(), .test_cvss_high(), .test_cvss_low(), .test_cvss_medium(), .test_elevated_epss_high()]
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=probe/tests/test_result_spool.py:L18 | neighbors=[test_result_spool.py, .test_byte_high_water_mark_pauses_new_w…, .test_custom_retry_config(), .test_exists(), .test_file_high_water_mark_pauses_new_w…, .test_flush_quarantines_permanent_rejec…]
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L108 | neighbors=[nuclei.py, ._consume_stdout(), .__init__(), ._map_finding(), .parse_output(), ._partial_or_raise()]
- "websocket_manager_agentconnectionmanager": "AgentConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L78 | neighbors=[manager.py, .agent_stale_after(), .connected_agents(), .connected_count(), .deliver_job(), .get_agent_status()]
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()]
- "agent_use_cases": "use_cases.py" | kind=code-symbol | source=probe/agent/use_cases.py:L1 | neighbors=[agent.py, task_runner.py, _as_int(), normalize_intensity(), resolve(), use_case_for_code()]
- "ai_llm_report_llmreportgenerator": "LLMReportGenerator" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L82 | neighbors=[llm_report.py, .available(), ._complete(), ._generate_and_store(), .generate_detection_rule_explanation(), .generate_executive_summary()]
- "app_main": "main.py" | kind=code-symbol | source=manager/backend/app/main.py:L1 | neighbors=[config.py, dependencies.py, GzipRequestMiddleware, lifespan(), _service_root(), unhandled_exception_handler()]
- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[AiMessage, evidenceText(), ManagerAiResponse, POST(), validMessages(), assistant.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c52feb410341da146973ec21b59b90f8985b8c73": "c52feb4 feat(portal): reskin User Portal to console theme + comprehensive dashb…" | kind=Commit | source=git | neighbors=[35f02a9 feat(portal): rich scan request…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fd5dc9658c8f71049864680b5317900dde34f0eb": "fd5dc96 feat(remediation): AI + deterministic-KB per-finding remediation plans" | kind=Commit | source=git | neighbors=[54503ae feat(scanner): SYN path harvest…, llm_report.py, main.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux]
- "dashboard_patchcomparisonmatrix": "PatchComparisonMatrix.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, d2eb44c feat(posture): add dashboard Pa…, DashboardGrid.tsx, Primitives.tsx, Meter(), cell]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L42 | neighbors=[orchestrator.py, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute(), .generate_dns_callback_token()]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser()]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, computeOverallProgress()]
- "main_scripts_findings_data": "_data()" | kind=code-symbol | source=probe/main_scripts/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[0f0097b feat(posture): mirror posture s…, 1fe16c8 stable but some dead code, need…, a0b870c fix(posture): score over open f…, d1b4dd3 trim frontend to 7 core pages; …, fadb4f5 fix(posture): hoist report-sect…, dependencies.py]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit()]
- "scanner_findings_data": "_data()" | kind=code-symbol | source=probe/scanner/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()]
- "tests_test_agents": "test_agents.py" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, f3bb8db feat(manager): cross-worker WS …]
- "tests_test_posture": "test_posture.py" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 0f0097b feat(posture): mirror posture s…, 237a831 feat(posture): add run comparis…, 2cddd52 fix(posture): tenant-scope run …, 5238865 feat(posture): add pure scoring…, 9de087a feat(posture): add GET /analyti…]
- "tests_test_use_cases": "test_use_cases.py" | kind=code-symbol | source=probe/tests/test_use_cases.py:L1 | neighbors=[01f4398 feat(probe): IoT survey reaches…, 22701ea Add tests for scanner parity an…, 5c8e696 docs(probe): correct overclaimi…, 95904f1 feat(probe): detect SMB signing…, bce780a feat(probe): enumerate HTTP met…, fe868e6 feat(probe): real UDP amplifica…]
- "workers_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 21ebc46 feat(detection): unified priori…, 6be8259 feat(integrations): outbox deli…, 81c81cb feat: implement outbox reclaim …, database.py, _claim_batch()]
- "ad_asreproast_asreproastchecker": "ASREPRoastChecker" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L34 | neighbors=[asreproast.py, ._format_asrep_hash(), .generate_finding(), .get_no_preauth_accounts(), .request_asrep(), Enumerate AS-REP roastable accounts and…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c4386e4cbc0ee346a71c211a96326772b677c561": "c4386e4 feat(customers): operator Customers dashboard + per-customer portal slug" | kind=Commit | source=git | neighbors=[ae08d19 feat(scanner): adaptive timeout…, main.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "detection_correlator_detectioncorrelator": "DetectionCorrelator" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L75 | neighbors=[correlator.py, .compute_coverage(), .correlate(), .generate_gap_report(), ._host_for(), ._in_window()]
- "fleet_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L1 | neighbors=[1d5ae94 feat(fleet): live "Connected pr…, 2b4ff71 feat(fleet): one-click Approve …, 30261eb feat: enhance advisor flow with…, a4b970c feat(fleet): add run command fo…, b5ffcb0 Refactor Vedha probe installer …, c4386e4 feat(customers): operator Custo…]
- "main_scripts_os_fingerprint": "os_fingerprint.py" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L1 | neighbors=[2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, dec1e7c fix(scanner): resolve() family …, accept_echo_reply(), build_icmp_addrmask()]
- "tests_parsers_test": "parsers.test.ts" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, finding-id.ts, resetCounters(), httpx-parser.ts, HttpxJsonlDecoder]
- "tests_test_ad_assessment_testadcschecker": "TestADCSChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L278 | neighbors=[test_ad_assessment.py, .setup_method(), .test_esc1_negative_when_manager_approv…, .test_esc1_negative_without_low_priv_en…, .test_esc1_positive(), .test_esc4_negative_when_deny_ace()]
- "tests_test_ai_normalizer_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L32 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]
- "tests_test_detection_core_testmatchcandidate": "TestMatchCandidate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L391 | neighbors=[test_detection_core.py, .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding(), .test_no_match_returns_empty()]
- "tests_test_detection_core_testvulndb": "TestVulnDB" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L867 | neighbors=[test_detection_core.py, .test_content_hash_deterministic(), .test_covers(), .test_cvss_vector_index(), .test_cvss_vector_missing(), .test_known_products_sorted()]
- "tests_test_vuln_enrichment": "test_vuln_enrichment.py" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _make_http_mock(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_dedup_hash_case_insensitive_cve()]
- "ad_ntlm_relay_ntlmrelaychecker": "NTLMRelayChecker" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L30 | neighbors=[ntlm_relay.py, .check_ldap_signing(), .check_smb_signing(), .generate_finding(), ._probe_smb_host(), Probe SMB/LDAP signing posture across a…]

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
