# Node Description Batch 29 of 336

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

- "routers_agents_rationale_106": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L106 | neighbors=[_scope_is_reachable(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=pt
- "routers_agents_rationale_142": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L142 | neighbors=[_job_reachability_scope(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_agents_rationale_210": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L210 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_709": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L709 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_93": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L93 | neighbors=[_required_scan_type(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_engagements_import_facts": "import_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L321 | neighbors=[engagements.py, _parse_probe_file(), _promote_from_facts(), _read_capped(), _refresh_overview_cache(), Offline ingest path: upload a probe's s…] | lang=en
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L31 | neighbors=[findings.py, finding_timeline(), get_finding(), patch_finding(), Fetch a finding scoped to the caller's …, reopen_finding()] | lang=en
- "routers_users": "users.py" | kind=code-symbol | source=manager/backend/app/routers/users.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, dependencies.py, activate_user(), deactivate_user(), get_user(), list_users()] | lang=en
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L270 | neighbors=[vuln_scans.py, Run Nuclei and always leave its job in …, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result()] | lang=en
- "scanner_accuracy_gate": "accuracy_gate.py" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, check_thresholds(), CorpusError, format_gate_report(), is_independent(), load_corpora()] | lang=en
- "scanner_ftp_scanner_ftpscanner": "FTPScanner" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L62 | neighbors=[ftp_scanner.py, BaseScanner, ._cmd(), .__init__(), ._list_bounded(), ._probe()] | lang=en
- "scanner_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L405 | neighbors=[OSFingerprintScanner, accept_echo_reply(), build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…] | lang=en
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L530 | neighbors=[PortScanner, ._attempt(), ._note_probe_outcome(), One port's terminal result, gated by th…, One port's terminal result, gated by th…, .scan_target()] | lang=en
- "scanner_rsync_scanner": "rsync_scanner.py" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _handshake(), main(), parse_modules(), _recv_until()] | lang=en
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1105 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…] | lang=en
- "scanner_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L429 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…, Simple async rate limiter: at most `rat…] | lang=en
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L266 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …] | lang=en
- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/scanner/service_banner.py:L321 | neighbors=[service_banner.py, BaseScanner, ._connect(), ._grab(), .__init__(), ._ladder_for()] | lang=en
- "scanner_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L384 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()] | lang=en
- "scanner_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L87 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()] | lang=en
- "scanner_vnc_scanner": "vnc_scanner.py" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, classify_security_types(), main(), parse_rfb_version(), _read_security_types(), _recv_exact()] | lang=en
- "scripts_startup_validator_run_all_validators": "run_all_validators()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L396 | neighbors=[startup_validator.py, Run all validators. Use in FastAPI life…, CheckResult, DatabaseConnectivityValidator, RedisConnectivityValidator, ValidationReport] | lang=en
- "services_agent_policy": "agent_policy.py" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, classify_action(), Decision, _deny(), evaluate_action()] | lang=en
- "services_remediation_kb": "remediation_kb.py" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, classify_finding(), _cves(), os_key(), recipe_for_finding()] | lang=en
- "supporting_research_test_evidence_store": "test_evidence_store.py" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, build_fleet(), demo(), openssh_below(), smb_obs(), ssh_obs()] | lang=en
- "supporting_research_test_evidence_store_testretroactivedetection": "TestRetroactiveDetection" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L140 | neighbors=[test_evidence_store.py, .setUp(), .test_a_brand_new_rule_answers_against_…, .test_cannot_answer_is_reported_rather_…, .test_collected_but_unusable_evidence_i…, .test_current_state_comes_from_latest_e…] | lang=en
- "tests_test_accuracy_gate": "test_accuracy_gate.py" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _port_fact(), TestCli, TestCorpusValidation, TestProvenance, TestShippedCorpora] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine": "TestWindowStateMachine" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L27 | neighbors=[test_adaptive_rate.py, .test_congestion_avoidance_grows_sublin…, .test_initial_window(), .test_loss_halves_window(), .test_loss_sets_ssthresh_to_half(), .test_recovery_after_loss_enters_conges…] | lang=en
- "tests_test_agent_read_tools": "test_agent_read_tools.py" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L1 | neighbors=[3ad95f4 feat: Optimize asset service fe…, _asset(), _FakeSession, _Result, _svc(), test_list_assets_batches_services_no_n_…] | lang=en
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "tests_test_auth_login_make_user": "_make_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L44 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future(), .test_raises_expired_password()] | lang=en
- "tests_test_auth_login_testreasoncodes": "TestReasonCodes" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L223 | neighbors=[test_auth_login.py, Ensure every exception class has the ex…, .test_bcrypt_failure_code(), .test_database_failure_code(), .test_disabled_tenant_code(), .test_disabled_user_code()] | lang=en
- "tests_test_campaign_progress_running_run": "_running_run()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L316 | neighbors=[test_campaign_progress.py, _job(), _progress(), _run(), test_a_briefly_running_run_with_a_dead_…, test_a_dead_worker_is_called_out_quickl…] | lang=en
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()] | lang=en
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L96 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()] | lang=en
- "tests_test_engine_bridge_posture": "test_engine_bridge_posture.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 26ea68c Add comprehensive tests for OS …, 42f4e28 feat: enhance security operatio…, 6bb51ab feat: add detection-explain end…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…] | lang=en
- "tests_test_exploitability_testapplytofindings": "TestApplyToFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L110 | neighbors=[test_exploitability.py, .test_declared_severity_is_never_rewrit…, .test_idempotent_across_repeated_applic…, .test_kev_raises_the_score_and_priority…, .test_no_databases_is_a_no_op(), .test_priority_bands_match_posture_rule…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-028.json

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
