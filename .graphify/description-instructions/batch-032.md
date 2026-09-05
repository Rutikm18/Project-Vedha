# Node Description Batch 33 of 336

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

- "scanner_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L569 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), ._udp_liveness(), is_locally_administered()]
- "scanner_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()]
- "scanner_msrpc_scanner": "msrpc_scanner.py" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _extract_tcp_ports(), main(), MSRPCScanner, _summarize()]
- "scanner_nfs_scanner_xdr": "_XDR" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L56 | neighbors=[nfs_scanner.py, parse_mount_export(), parse_portmap_dump(), Minimal, BOUNDED big-endian XDR reader …, .__init__(), .opaque()]
- "scanner_printer_scanner_printerscanner": "PrinterScanner" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L96 | neighbors=[printer_scanner.py, BaseScanner, .__init__(), ._probe(), ._probe_ipp(), ._probe_pjl()]
- "scanner_rsync_scanner_rsyncscanner": "RsyncScanner" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L93 | neighbors=[rsync_scanner.py, BaseScanner, .__init__(), ._list_modules(), ._probe(), ._scan_port()]
- "scanner_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L129 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "scanner_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L868 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…]
- "scanner_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L619 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli(), Accepts CIDRs ('10.0.0.0/24'), single I…, Accepts CIDRs ('10.0.0.0/24'), single I…, Accepts CIDRs ('10.0.0.0/24'), single I…]
- "scanner_scanner_base_parse_ports": "parse_ports()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L880 | neighbors=[scanner_base.py, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…]
- "scanner_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/scanner/service_banner.py:L366 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), ._connect(), ._read_some(), One probe-ladder rung on its own connec…]
- "scanner_smtp_scanner_smtpscanner": "SMTPScanner" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L60 | neighbors=[smtp_scanner.py, BaseScanner, ._cmd(), .__init__(), ._probe(), ._read_response()]
- "scanner_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()]
- "scanner_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L181 | neighbors=[syn_scanner.py, parse_tcp_options(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking(), _parse_mss(), Parse a raw IPv4+TCP packet (as receive…]
- "scanner_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L201 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…]
- "scanner_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L262 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…]
- "scanner_va_campaign_progressreporter_snapshot": ".snapshot()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L246 | neighbors=[ProgressReporter, ._flush(), _now(), ._current(), ._eta_seconds(), ._percent()]
- "scanner_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/scanner/windows_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "scanner_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/scanner/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "schemas_finding_findingpatch": "FindingPatch" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[finding.py, BaseModel, .normalize_action_reason(), All fields optional — PATCH semantics., All fields optional — PATCH semantics., DetectionStatus]
- "services_job_result_service_rationale_1": "job_result_service.py — shared job result processing. Single source of truth for" | kind=entity | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[job_result_service.py, Asset, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_140": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_145": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L145 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_35": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L35 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_llm_managerllmservice_generate_with_fallback": ".generate_with_fallback()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L363 | neighbors=[ManagerLlmService, AiRuntimeError, ._build_system(), ._dispatch(), ._ensure_installed_ollama_model(), ._fallback_candidates()]
- "services_llm_runtime": "Runtime" | kind=code-symbol | source=manager/backend/app/services/llm.py:L29 | neighbors=[llm.py, ._default_runtime(), ._fallback_candidates(), ._runtime(), Settings, AiGenerateRequest]
- "services_notifications": "notifications.py" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, deliver(), enqueue_notification(), notify_tenant(), _send_email(), _send_jira()]
- "services_portal_metrics": "portal_metrics.py" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _is_closed(), MetricFinding, open_closed_counts(), _period(), severity_breakdown()]
- "services_reference": "reference.py" | kind=code-symbol | source=manager/backend/app/services/reference.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _encode(), is_reference(), make_reference(), normalize(), scan_job_reference()]
- "status_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "tests_operator_routes_test": "operator-routes.test.ts" | kind=code-symbol | source=manager/frontend/tests/operator-routes.test.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, assistant-access.ts, canMountAssistant(), isAssistantRoute()]
- "tests_test_accuracy_gate_testcorpusvalidation": "TestCorpusValidation" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L89 | neighbors=[test_accuracy_gate.py, .test_corpus_without_any_labels_is_reje…, .test_corpus_without_facts_is_rejected(), .test_ground_truth_states_alone_is_a_va…, .test_malformed_json_is_a_gate_error_no…, .test_missing_directory_is_rejected()]
- "tests_test_accuracy_gate_testshippedcorpora": "TestShippedCorpora" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L42 | neighbors=[test_accuracy_gate.py, .test_an_independently_labeled_corpus_i…, .test_every_independent_corpus_scores_p…, .test_every_shipped_corpus_declares_pro…, .test_gate_passes_on_the_committed_corp…, .test_regression_only_directory_still_w…]
- "tests_test_accuracy_gate_testthresholds": "TestThresholds" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L148 | neighbors=[test_accuracy_gate.py, .test_clean_result_produces_no_violatio…, .test_false_positive_finding_trips_prec…, .test_matching_port_state_scores_perfec…, .test_missed_open_port_trips_open_recal…, .test_phantom_open_port_trips_open_prec…]
- "tests_test_active_validation_escalation": "test_active_validation_escalation.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, _ev(), test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…]
- "tests_test_adaptive_rate": "test_adaptive_rate.py" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating]
- "tests_test_agent_auth_boundary": "test_agent_auth_boundary.py" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _boundary_test_client(), test_admin_enrollment_approval_is_not_p…, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…, test_legacy_agent_jwt_allows_only_workl…]
- "tests_test_agent_dispatch_testtenantwebsocketselection": "TestTenantWebSocketSelection" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L95 | neighbors=[test_agent_dispatch.py, .test_displaced_socket_cannot_unregiste…, .test_first_online_push_cannot_cross_te…, .test_online_heartbeat_clears_finished_…, .test_only_returns_online_agents_in_req…, ScanJobStatus]
- "tests_test_agent_read_tools_result": "_Result" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L19 | neighbors=[test_agent_read_tools.py, Mimics the subset of a SQLAlchemy Resul…, .all(), .__init__(), .scalars(), test_list_assets_batches_services_no_n_…]
- "tests_test_auth_login_make_tenant": "_make_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L61 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_not_expired_when_future(), .test_raises_expired_password(), .test_raises_password_mismatch()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-032.json

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
