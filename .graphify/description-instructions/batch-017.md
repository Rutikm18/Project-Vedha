# Node Description Batch 18 of 332

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

- "tests_test_ad_assessment": "test_ad_assessment.py" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _enum_with_entries(), _FakeAttr, _FakeEntry, TestADCSChecker, TestASREPRoastChecker]
- "tests_test_agents_testagentjobcompatibility": "TestAgentJobCompatibility" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L413 | neighbors=[test_agents.py, .test_agent_network_segments_are_normal…, .test_declared_segment_must_cover_entir…, .test_declared_segment_rejects_missing_…, .test_empty_capabilities_receive_no_job…, .test_empty_segments_are_fail_closed()]
- "tests_test_ai_normalizer_testextractrawtext": "TestExtractRawText" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L47 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]
- "tests_test_detection_coverage": "test_detection_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _job(), _rows(), _run(), _scalars(), test_aggregating_reason_names_the_outbo…]
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, _action(), pytest_addoption()]
- "tests_test_e2e_engagement_to_findings": "test_e2e_engagement_to_findings.py" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, task_runner.py, _accept_loop(), _manager(), _plant(), test_correlated_findings_cite_their_bas…]
- "tests_test_external_engine_wrappers": "test_external_engine_wrappers.py" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L1 | neighbors=[b4b12a9 Rename project and update files, mass_scan.py, nmap_wrapper.py, scanner_base.py, test_masscan_nonzero_with_valid_output_…, test_masscan_range_must_be_fully_in_sco…]
- "tests_test_main_scripts_accuracy": "test_main_scripts_accuracy.py" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_by_rule_breakdown(), test_clean_host_has_zero_false_positive…, test_corpus_flags_a_missed_expected_fin…, test_corpus_matches_real_engine_output(), test_corpus_scores_port_states_when_gro…]
- "tests_test_main_scripts_ja4x": "test_main_scripts_ja4x.py" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _fake_cert(), test_empty_list_hashes_to_sentinel(), test_ja4x_format_is_three_12hex_fields(), test_ja4x_from_cert_handles_garbage(), test_ja4x_from_cert_matches_pure_core()]
- "tests_test_new_scanners": "test_new_scanners.py" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, snmp_scanner.py, delta_engine(), _make_scan_record(), TestDeltaEngine]
- "tests_test_probe_core_testscopeguard": "TestScopeGuard" | kind=code-symbol | source=probe/tests/test_probe_core.py:L79 | neighbors=[test_probe_core.py, .test_assert_in_scope_passes(), .test_assert_in_scope_raises(), .test_excludes_larger_subnet(), .test_excludes_override_allowlist(), .test_filter_yields_only_in_scope()]
- "tests_test_scanner_congestion": "test_scanner_congestion.py" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, scanner_base.py, _fake_gai(), _FakeSock, _scanner(), _tcp_info_buf()]
- "tests_test_vantage_fusion": "test_vantage_fusion.py" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _probe(), test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_…, test_empty_and_malformed_are_safe(), test_external_vantage_open_makes_port_e…]
- "tests_test_weakness_map": "test_weakness_map.py" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L1 | neighbors=[6e2818f Add support for additional serv…, cli.py, vulndb.py, weakness_map.py, db(), _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses": "TestCorrelateWeaknesses" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L69 | neighbors=[test_weakness_map.py, .test_cve_absent_from_mirror_still_emit…, .test_dedup_by_cve_target_port(), .test_exposure_boosts_risk(), .test_no_db_degrades_gracefully(), .test_obsolete_tls_both_when_both_offer…]
- "ui_output_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L30 | neighbors=[output.ts, banner(), findingDetail(), findingLine(), findingsTable(), hostLine()]
- "workers_outbox_run_worker": "run_worker()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L401 | neighbors=[outbox.py, Main loop: claim → process → repeat. Sl…, _claim_batch(), Event, _process(), _reap_stale_runs()]
- "agent_agent_enroll_device": "_enroll_device()" | kind=code-symbol | source=probe/agent/agent.py:L1154 | neighbors=[agent.py, _bounded_env_int(), _classify_connection_error(), _dbg(), say(), _obtain_identity()]
- "agent_agent_flush_spool_over_http": "_flush_spool_over_http()" | kind=code-symbol | source=probe/agent/agent.py:L971 | neighbors=[agent.py, say(), Retry durable result files using the ac…, _run_ws_push_loop(), _ws_http_poll_fallback(), Retry durable result files using the ac…]
- "agent_agent_ws_heartbeat_sender": "_ws_heartbeat_sender()" | kind=code-symbol | source=probe/agent/agent.py:L949 | neighbors=[agent.py, Send periodic heartbeats over WebSocket., _run_ws_push_loop(), Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket.]
- "agent_cli_output": "output()" | kind=code-symbol | source=probe/agent/cli.py:L179 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()]
- "ai_prioritizer_vulnprioritizer": "VulnPrioritizer" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L99 | neighbors=[prioritizer.py, .explain_prediction(), .fallback_score(), ._formula_contributions(), .__init__(), .is_trained()]
- "assistant_factcard": "FactCard.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard(), lifecycleSummary(), Pip(), assistant.ts]
- "auth_exceptions_authenticationerror": "AuthenticationError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L28 | neighbors=[exceptions.py, VedhaAuthError, BcryptFailureError, DatabaseFailureError, DisabledTenantError, DisabledUserError]
- "commands_admin": "admin.ts" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildAdminCommand(), c, PermittedUser, 10dfc80 Add comprehensive probe testing…]
- "commands_login": "login.ts" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L1 | neighbors=[loadSession(), saveSession(), serverUrl(), buildLoginCommand(), prompt(), promptSilent()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@25344045b42fb3f74183072c0b432ee8c30db287": "2534404 scanner(service_enum): commit owner's in-progress changes as-is + re-sy…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@35691030666303cbdc4b5214a09373d49b3d2bcf": "3569103 docs(agent): research + design for Vedha Autonomous Engagement Agent" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3bb8dba0a692bc5cd7881b8be1ce1529f8f659a": "f3bb8db feat(manager): cross-worker WS backplane + agent job-history + fleet qu…" | kind=Commit | source=git | neighbors=[3565ada fix(ingest): NUL-safe result su…, main.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109]
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L22 | neighbors=[page.tsx, page.tsx, page.tsx, PageShell.tsx, page.tsx, page.tsx]
- "customers_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, c4386e4 feat(customers): operator Custo…, e3958e7 feat(customers): reveal + copy …, PageShell.tsx, PageShell(), ClientUserResp]
- "cve_cli": "cli.py" | kind=code-symbol | source=probe/cve/cli.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_parser(), cmd_correlate(), cmd_ingest(), cmd_status(), main()]
- "cve_correlator": "correlator.py" | kind=code-symbol | source=probe/cve/correlator.py:L1 | neighbors=[6e2818f Add support for additional serv…, _as_dict(), _backport_marker(), correlate(), CVEFinding, mirror_age_note()]
- "detection_correlator_detectiongap": "DetectionGap" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L62 | neighbors=[correlator.py, .generate_gap_report(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_engine_correlate": "correlate.py" | kind=code-symbol | source=manager/detection_engine/correlate.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, correlate_smb_patch(), dedup_findings()]
- "detection_engine_pipeline": "pipeline.py" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 26ea68c Add comprehensive tests for OS …, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …]
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[0236a60 fix(detection): full EPSS catal…, d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context()]
- "detection_siem_elasticsiem": "ElasticSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L184 | neighbors=[siem.py, .build_query(), .parse_response(), .query_alerts(), SIEMQueryEngine, Elasticsearch via the _search API (KQL/…]
- "detection_siem_sentinelsiem": "SentinelSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L134 | neighbors=[siem.py, Microsoft Sentinel via the Azure Monito…, .build_kql(), .parse_response(), .query_alerts(), SIEMQueryEngine]
- "detection_siem_splunksiem": "SplunkSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L81 | neighbors=[siem.py, Splunk via the REST search endpoint (``…, SIEMQueryEngine, .build_spl(), .parse_response(), .query_alerts()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-017.json

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
