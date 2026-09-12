# Node Description Batch 9 of 380

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@f1da96f64e70aef9d0275a6cdcdbf89b7334e948": "f1da96f fix: update environment variables and resource limits in docker-compose…" | kind=Commit | source=git | neighbors=[2a36f8a fix: update docker compose comm…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3c359163f16baf103a46a5170e40a9e95edda9d": "f3c3591 docs: Phase 0 queue-control implementation plan (8 TDD tasks)" | kind=Commit | source=git | neighbors=[879cdfa docs: probe fleet automation de…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L42 | neighbors=[orchestrator.py, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute(), .generate_dns_callback_token()]
- "lib_campaign_store": "campaign-store.ts" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L1 | neighbors=[route.ts, 07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…, route.ts]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser()]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, computeOverallProgress()]
- "main_scripts_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…]
- "main_scripts_va_campaign": "va_campaign.py" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _alive(), _atomic_write_json(), _bounded_gather()]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[0f0097b feat(posture): mirror posture s…, 1fe16c8 stable but some dead code, need…, a0b870c fix(posture): score over open f…, d1b4dd3 trim frontend to 7 core pages; …, fadb4f5 fix(posture): hoist report-sect…, dependencies.py]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit()]
- "scanner_service_enum": "service_enum.py" | kind=code-symbol | source=probe/scanner/service_enum.py:L1 | neighbors=[2534404 scanner(service_enum): commit o…, 78d51c5 opsec(scanner): de-sign service…, 8f6bf49 Refactor code structure and rem…, classify_roles(), _dns_read_name(), Enrichment]
- "tests_test_detection_core_testingestfile": "TestIngestFile" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L226 | neighbors=[test_detection_core.py, .test_authoritative_scanner_creates_aut…, .test_empty_file(), .test_hostname_target_not_ip_keyed(), .test_multi_file_accumulation(), .test_quarantines_malformed()]
- "tests_test_host_health_r": "_r()" | kind=code-symbol | source=probe/tests/test_host_health.py:L24 | neighbors=[test_host_health.py, .test_flaky_note_is_not_an_error(), .test_offline_fact_carries_an_error_so_…, .test_healthy_host_produces_no_facts_at…, .test_offline_fact_marks_the_scan_incom…, .test_offline_host_stops_accumulating_o…]
- "tests_test_posture": "test_posture.py" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 0f0097b feat(posture): mirror posture s…, 237a831 feat(posture): add run comparis…, 2cddd52 fix(posture): tenant-scope run …, 5238865 feat(posture): add pure scoring…, 9de087a feat(posture): add GET /analyti…]
- "tests_test_use_cases": "test_use_cases.py" | kind=code-symbol | source=probe/tests/test_use_cases.py:L1 | neighbors=[01f4398 feat(probe): IoT survey reaches…, 22701ea Add tests for scanner parity an…, 5c8e696 docs(probe): correct overclaimi…, 95904f1 feat(probe): detect SMB signing…, bce780a feat(probe): enumerate HTTP met…, fe868e6 feat(probe): real UDP amplifica…]
- "workflow_modes": "modes.py" | kind=code-symbol | source=probe/workflow/modes.py:L1 | neighbors=[engine.py, explain_plan.py, local_run.py, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …]
- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L379 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _default_host_concurrency(), _finalize_trace(), _gather_per_host(), _port_candidates()]
- "ad_asreproast_asreproastchecker": "ASREPRoastChecker" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L34 | neighbors=[asreproast.py, ._format_asrep_hash(), .generate_finding(), .get_no_preauth_accounts(), .request_asrep(), Enumerate AS-REP roastable accounts and…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1d5ae943f799b5d9bba43f41c366d70ed4c00b1a": "1d5ae94 feat(fleet): live \"Connected probes\" status section" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2c53ae99b6e203a1fefff8d7998d849e906ee0c1": "2c53ae9 evasion(scanner): randomized scan order + jittered scan-delay (task C1/…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65e568441bfb43e313c743db52bd2f65fb7e86fe": "65e5684 feat(probe): transparent job logging (real use-case + result summary)" | kind=Commit | source=git | neighbors=[1af3404 feat(deploy): probe-free manage…, agent.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer]
- "commit:repo:github.com/Rutikm18/Project-Vedha@6a1c958273a695fdfb8a8e43254742b6436b3b8e": "6a1c958 docs(plans): record execution status for active-validation + risk-rank …" | kind=Commit | source=git | neighbors=[50d6554 feat(active-validation): approv…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@88c92781d5435f80d9b62fb0869cca708fc4920b": "88c9278 feat(ai): pin manager LLM pipeline to Claude Sonnet 4.6" | kind=Commit | source=git | neighbors=[1d5ae94 feat(fleet): live "Connected pr…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@e3958e7d0893279d1784154afd4ac1719633063f": "e3958e7 feat(customers): reveal + copy customer login password from dashboard (…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work]
- "components_sidebar": "Sidebar.tsx" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…]
- "detection_correlator_detectioncorrelator": "DetectionCorrelator" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L95 | neighbors=[correlator.py, .compute_coverage(), .correlate(), .generate_gap_report(), ._host_for(), ._in_window()]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …]
- "main_scripts_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, _align8(), build_ntlmssp_negotiate(), _der()]
- "path_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, 3ddc104 feat: unify customer and manage…, 3e6b187 feat: unify customer and manage…, backend.ts, backend(), BackendError]
- "schemas_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, 7a637eb feat: network VA accuracy, KEV …, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…]
- "services_llm_managerllmservice": "ManagerLlmService" | kind=code-symbol | source=manager/backend/app/services/llm.py:L182 | neighbors=[llm.py, ._anthropic(), ._auto_cloud_provider(), ._build_system(), ._client(), ._default_runtime()]
- "tests_parsers_test": "parsers.test.ts" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, finding-id.ts, resetCounters(), httpx-parser.ts, HttpxJsonlDecoder]
- "tests_test_ad_assessment_testadcschecker": "TestADCSChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L278 | neighbors=[test_ad_assessment.py, .setup_method(), .test_esc1_negative_when_manager_approv…, .test_esc1_negative_without_low_priv_en…, .test_esc1_positive(), .test_esc4_negative_when_deny_ace()]
- "tests_test_ai_normalizer_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L32 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]
- "tests_test_async_udp": "test_async_udp.py" | kind=code-symbol | source=probe/tests/test_async_udp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, _SinkProtocol]
- "tests_test_detection_core_testmatchcandidate": "TestMatchCandidate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L433 | neighbors=[test_detection_core.py, .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding(), .test_no_match_returns_empty()]
- "tests_test_detection_core_testvulndb": "TestVulnDB" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L936 | neighbors=[test_detection_core.py, .test_content_hash_deterministic(), .test_covers(), .test_cvss_vector_index(), .test_cvss_vector_missing(), .test_known_products_sorted()]
- "tests_test_os_stage_wiring": "test_os_stage_wiring.py" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, scanner_base.py, _asset(), _open(), test_cached_os_fact_is_reused_not_repro…]
- "tests_test_portal_assistant": "test_portal_assistant.py" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _ask(), _client(), _db(), _engagement()]
- "tests_test_syn_scanner": "test_syn_scanner.py" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, 8f6bf49 Refactor code structure and rem…, ae08d19 feat(scanner): adaptive timeout…, scanner_base.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-008.json

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
