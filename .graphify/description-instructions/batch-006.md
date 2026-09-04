# Node Description Batch 7 of 332

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@5c8e696210c1e7beaf5f6911e452bd38c701b1e8": "5c8e696 docs(probe): correct overclaiming use-case descriptions to match curren…" | kind=Commit | source=git | neighbors=[10dfc80 Add comprehensive probe testing…, use_cases.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "commit:repo:github.com/Rutikm18/Project-Vedha@75650c143e0e92e93ca7fed76c46893953456bf8": "75650c1 feat: add Posture & Patch-Comparison Scorecard design spec" | kind=Commit | source=git | neighbors=[agent.py, config.py, ModelSwitcher.tsx, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cdee859546b57100944ef98e4f180fc049700dbe": "cdee859 feat(probe): add container/cloud/infra ports to IT catalog" | kind=Commit | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@e8262a30bd57c27b86d69584e3fee5ac6cd0af2b": "e8262a3 feat(probe): explicit unauthenticated_read fact for Redis exposure" | kind=Commit | source=git | neighbors=[95904f1 feat(probe): detect SMB signing…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "detection_correlator_detectioncorrelator": "DetectionCorrelator" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L95 | neighbors=[correlator.py, .compute_coverage(), .correlate(), .generate_gap_report(), ._host_for(), ._in_window()]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …]
- "main_scripts_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, _align8(), build_ntlmssp_negotiate(), _der()]
- "main_scripts_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, 8f6bf49 Refactor code structure and rem…]
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 72f68af feat(verification): expose veri…, 7d8d3f3 merge: resolve conflicts with o…, 85e4537 feat(risk-rank): expose risk_ra…]
- "tests_parsers_test": "parsers.test.ts" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, finding-id.ts, resetCounters(), httpx-parser.ts, HttpxJsonlDecoder]
- "tests_test_ad_assessment_testadcschecker": "TestADCSChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L278 | neighbors=[test_ad_assessment.py, .setup_method(), .test_esc1_negative_when_manager_approv…, .test_esc1_negative_without_low_priv_en…, .test_esc1_positive(), .test_esc4_negative_when_deny_ace()]
- "tests_test_ai_normalizer_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L32 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]
- "tests_test_async_udp": "test_async_udp.py" | kind=code-symbol | source=probe/tests/test_async_udp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, _SinkProtocol]
- "tests_test_detection_core_testmatchcandidate": "TestMatchCandidate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L433 | neighbors=[test_detection_core.py, .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding(), .test_no_match_returns_empty()]
- "tests_test_detection_core_testvulndb": "TestVulnDB" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L936 | neighbors=[test_detection_core.py, .test_content_hash_deterministic(), .test_covers(), .test_cvss_vector_index(), .test_cvss_vector_missing(), .test_known_products_sorted()]
- "tests_test_os_stage_wiring": "test_os_stage_wiring.py" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, scanner_base.py, _asset(), _open(), test_cached_os_fact_is_reused_not_repro…]
- "tests_test_portal_assistant": "test_portal_assistant.py" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _ask(), _client(), _db(), _engagement()]
- "tests_test_syn_scanner": "test_syn_scanner.py" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, 8f6bf49 Refactor code structure and rem…, ae08d19 feat(scanner): adaptive timeout…, scanner_base.py]
- "tests_test_vuln_enrichment": "test_vuln_enrichment.py" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _make_http_mock(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_dedup_hash_case_insensitive_cve()]
- "ad_ntlm_relay_ntlmrelaychecker": "NTLMRelayChecker" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L30 | neighbors=[ntlm_relay.py, .check_ldap_signing(), .check_smb_signing(), .generate_finding(), ._probe_smb_host(), Probe SMB/LDAP signing posture across a…]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1366 | neighbors=[agent.py, main(), _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device()]
- "commands_scan": "scan.ts" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L1 | neighbors=[requireAuth(), buildScanCommand(), printAiComment(), PROFILE_TOOLS, resolveTargets(), scanCommand()]
- "commands_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L1 | neighbors=[buildToolsCommand(), C, ln(), showSpinner(), w(), installer.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@0b7bcb82f82922f901d24413b10ed114e096a3a7": "0b7bcb8 feat: probe bootstrap key — self-register without admin login" | kind=Commit | source=git | neighbors=[agent.py, transport.py, config.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5c6aa54b98c0dc182941305bf241ca956f806193": "5c6aa54 feat(portal-ui): portal shell/pages restyle + settings page" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@ae08d19a6e9e90cc033a56b4aaeea1424c557da7": "ae08d19 feat(scanner): adaptive timeout, SYN retransmit, top-100 default (accur…" | kind=Commit | source=git | neighbors=[65e5684 feat(probe): transparent job lo…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c76b4287cfd451cab1e1212934ab3f6f36445eb6": "c76b428 backend and login page error handling update" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "generate_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, POST(), backend.ts, backend()]
- "lib_clients_store": "clients-store.ts" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, ClientJiraConfig, ClientNotifyConfig, ClientSettings, ClientsFile]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L29 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, EngagementStatusControl.tsx, page.tsx, page.tsx]
- "lib_openvas_client": "openvas-client.ts" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, findings-store.ts, FindingSeverity, boundedEnvMs()]
- "main_scripts_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, device_hint()]
- "main_scripts_service_enum": "service_enum.py" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L1 | neighbors=[2534404 scanner(service_enum): commit o…, 78d51c5 opsec(scanner): de-sign service…, 8f6bf49 Refactor code structure and rem…, daf3de2 feat(scanner): add service enum…, classify_roles(), _dns_read_name()]
- "models_enums_assetcriticality": "AssetCriticality" | kind=code-symbol | source=manager/backend/app/models/enums.py:L40 | neighbors=[enums.py, str, Asset, Attack path analysis API (AttackPathSer…, AssetIn, AssetOut]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …]
- "schemas_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, 7a637eb feat: network VA accuracy, KEV …, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…, f473173 merge: network VA accuracy, KEV…]
- "services_llm_managerllmservice": "ManagerLlmService" | kind=code-symbol | source=manager/backend/app/services/llm.py:L111 | neighbors=[llm.py, ._anthropic(), ._auto_cloud_provider(), ._build_system(), ._client(), ._default_runtime()]
- "tests_test_detection_core_testdeceptionscore": "TestDeceptionScore" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L685 | neighbors=[test_detection_core.py, .test_capped_at_1(), .test_combined_high(), .test_contradictory_os(), .test_high_product_count(), .test_low_product_count()]
- "tests_test_main_scripts_rdp": "test_main_scripts_rdp.py" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, _cc(), _run(), test_cc_without_negotiation_is_standard…, test_confirmed_rdp_wins_dedup_over_port…]
- "vuln_nuclei_nucleiscanerror": "NucleiScanError" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L89 | neighbors=[nuclei.py, RuntimeError, .__init__(), ._partial_or_raise(), .run_scan(), Fatal Nuclei failure, optionally carryi…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-006.json

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
