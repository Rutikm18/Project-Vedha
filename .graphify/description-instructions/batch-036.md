# Node Description Batch 37 of 380

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

- "scanner_rsync_scanner_rsyncscanner": "RsyncScanner" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L93 | neighbors=[rsync_scanner.py, BaseScanner, .__init__(), ._list_modules(), ._probe(), ._scan_port()]
- "scanner_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L129 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "scanner_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L870 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, Pacing telemetry for the scan summary (…, `async_udp_probe` with bounded per-port…]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L702 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…]
- "scanner_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/scanner/service_banner.py:L366 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), ._connect(), ._read_some(), One probe-ladder rung on its own connec…]
- "scanner_smtp_scanner_smtpscanner": "SMTPScanner" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L60 | neighbors=[smtp_scanner.py, BaseScanner, ._cmd(), .__init__(), ._probe(), ._read_response()]
- "scanner_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()]
- "scanner_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L181 | neighbors=[syn_scanner.py, parse_tcp_options(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking(), _parse_mss(), Parse a raw IPv4+TCP packet (as receive…]
- "scanner_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L201 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…]
- "scanner_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L262 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…]
- "scanner_va_campaign_progressreporter_snapshot": ".snapshot()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L246 | neighbors=[ProgressReporter, ._flush(), _now(), ._current(), ._eta_seconds(), ._percent()]
- "scanner_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/scanner/windows_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "scanner_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/scanner/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "schemas_finding_findingout": "FindingOut" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L125 | neighbors=[finding.py, BaseModel, ._populate_enrichment_light(), ._populate_report_enrichment(), ._populate_risk_rank(), DetectionStatus]
- "services_finding_content_finding_content": "finding_content()" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L377 | neighbors=[finding_content.py, _build_exploitation(), exploit_maturity(), exploitation_signals(), FindingContent, _scale_business_impact()]
- "services_job_result_service_rationale_1": "job_result_service.py — shared job result processing. Single source of truth for" | kind=entity | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[job_result_service.py, Asset, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_140": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_145": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L145 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_35": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L35 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_llm_managerllmservice_client": "._client()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L512 | neighbors=[ManagerLlmService, ._anthropic(), ._ensure_installed_ollama_model(), ._gemini(), ._ollama(), ._openai()]
- "services_llm_runtime": "Runtime" | kind=code-symbol | source=manager/backend/app/services/llm.py:L100 | neighbors=[llm.py, ._default_runtime(), ._fallback_candidates(), ._runtime(), Settings, AiGenerateRequest]
- "services_portal_metrics": "portal_metrics.py" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _is_closed(), MetricFinding, open_closed_counts(), _period(), severity_breakdown()]
- "services_reference": "reference.py" | kind=code-symbol | source=manager/backend/app/services/reference.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _encode(), is_reference(), make_reference(), normalize(), scan_job_reference()]
- "status_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "tests_operator_routes_test": "operator-routes.test.ts" | kind=code-symbol | source=manager/frontend/tests/operator-routes.test.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, assistant-access.ts, canMountAssistant(), isAssistantRoute()]
- "tests_report_portal_adapt_test": "report-portal-adapt.test.ts" | kind=code-symbol | source=manager/frontend/tests/report-portal-adapt.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, f023fa5 Add portalToRawFinding adapter …, adapt.ts, portalToRawFinding(), toRawFinding(), finding-model.ts]
- "tests_test_accuracy_gate_testcorpusvalidation": "TestCorpusValidation" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L89 | neighbors=[test_accuracy_gate.py, .test_corpus_without_any_labels_is_reje…, .test_corpus_without_facts_is_rejected(), .test_ground_truth_states_alone_is_a_va…, .test_malformed_json_is_a_gate_error_no…, .test_missing_directory_is_rejected()]
- "tests_test_accuracy_gate_testshippedcorpora": "TestShippedCorpora" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L42 | neighbors=[test_accuracy_gate.py, .test_an_independently_labeled_corpus_i…, .test_every_independent_corpus_scores_p…, .test_every_shipped_corpus_declares_pro…, .test_gate_passes_on_the_committed_corp…, .test_regression_only_directory_still_w…]
- "tests_test_accuracy_gate_testthresholds": "TestThresholds" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L148 | neighbors=[test_accuracy_gate.py, .test_clean_result_produces_no_violatio…, .test_false_positive_finding_trips_prec…, .test_matching_port_state_scores_perfec…, .test_missed_open_port_trips_open_recal…, .test_phantom_open_port_trips_open_prec…]
- "tests_test_active_validation_escalation": "test_active_validation_escalation.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, _ev(), test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…]
- "tests_test_adaptive_rate": "test_adaptive_rate.py" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating]
- "tests_test_agent_auth_boundary": "test_agent_auth_boundary.py" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _boundary_test_client(), test_admin_enrollment_approval_is_not_p…, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…, test_legacy_agent_jwt_allows_only_workl…]
- "tests_test_agent_dispatch_testtenantwebsocketselection": "TestTenantWebSocketSelection" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L95 | neighbors=[test_agent_dispatch.py, .test_displaced_socket_cannot_unregiste…, .test_first_online_push_cannot_cross_te…, .test_online_heartbeat_clears_finished_…, .test_only_returns_online_agents_in_req…, ScanJobStatus]
- "tests_test_agent_read_tools_result": "_Result" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L19 | neighbors=[test_agent_read_tools.py, Mimics the subset of a SQLAlchemy Resul…, .all(), .__init__(), .scalars(), test_list_assets_batches_services_no_n_…]
- "tests_test_auth_login_make_tenant": "_make_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L61 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_not_expired_when_future(), .test_raises_expired_password(), .test_raises_password_mismatch()]
- "tests_test_branch_rule_coverage": "test_branch_rule_coverage.py" | kind=code-symbol | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, _branch_components(), _scanners_with_rules(), test_db_scan_is_assessed(), test_every_deep_branch_has_at_least_one…, test_exemptions_are_still_real()]
- "tests_test_campaign_progress_job": "_job()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L197 | neighbors=[test_campaign_progress.py, _running_run(), test_a_briefly_running_run_is_not_calle…, test_a_wedged_detection_run_explains_it…, test_full_coverage_completes_at_100(), test_naive_started_at_does_not_crash_th…]
- "tests_test_campaign_progress_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L190 | neighbors=[test_campaign_progress.py, _running_run(), test_a_briefly_running_run_is_not_calle…, test_a_wedged_detection_run_explains_it…, test_full_coverage_completes_at_100(), test_naive_started_at_does_not_crash_th…]
- "tests_test_cli_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_cli.py:L152 | neighbors=[test_cli.py, .__init__(), .request(), test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…, test_poll_job_rejects_invalid_timing()]
- "tests_test_customer_reveal": "test_customer_reveal.py" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L1 | neighbors=[e3958e7 feat(customers): reveal + copy …, _db(), _operator(), test_reveal_missing_user_is_404(), test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-036.json

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
