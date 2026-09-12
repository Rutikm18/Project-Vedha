# Node Description Batch 313 of 380

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

- "tests_test_config_model_test_precedence_cli_beats_env_beats_probe_env_beats_default": "test_precedence_cli_beats_env_beats_probe_env_beats_default()" | kind=code-symbol | source=probe/tests/test_config_model.py:L14 | neighbors=[test_config_model.py]
- "tests_test_config_model_test_render_effective_lists_value_and_source": "test_render_effective_lists_value_and_source()" | kind=code-symbol | source=probe/tests/test_config_model.py:L43 | neighbors=[test_config_model.py]
- "tests_test_config_model_test_verify_tls_is_coerced_to_bool": "test_verify_tls_is_coerced_to_bool()" | kind=code-symbol | source=probe/tests/test_config_model.py:L31 | neighbors=[test_config_model.py]
- "tests_test_connect_rationale_1": "Phase 6 — optional connect + uplink security. Enrollment env mapping is pure; si" | kind=entity | source=probe/tests/test_connect.py:L1 | neighbors=[test_connect.py]
- "tests_test_connect_test_kill_switch_detects_stop_file": "test_kill_switch_detects_stop_file()" | kind=code-symbol | source=probe/tests/test_connect.py:L98 | neighbors=[test_connect.py]
- "tests_test_connect_test_pairing_sets_no_credential_env": "test_pairing_sets_no_credential_env()" | kind=code-symbol | source=probe/tests/test_connect.py:L16 | neighbors=[test_connect.py]
- "tests_test_connect_test_pat_mode_sets_vedha_pat": "test_pat_mode_sets_vedha_pat()" | kind=code-symbol | source=probe/tests/test_connect.py:L22 | neighbors=[test_connect.py]
- "tests_test_connect_test_token_mode_sets_probe_enroll_token": "test_token_mode_sets_probe_enroll_token()" | kind=code-symbol | source=probe/tests/test_connect.py:L27 | neighbors=[test_connect.py]
- "tests_test_customer_access_rationale_1": "test_customer_access.py — Phase 1: operator provisioning + scan-request inbox. H" | kind=entity | source=manager/backend/tests/test_customer_access.py:L1 | neighbors=[test_customer_access.py]
- "tests_test_customer_access_rationale_125": "An email already used elsewhere in the tenant (the operator's own login," | kind=entity | source=manager/backend/tests/test_customer_access.py:L125 | neighbors=[.test_duplicate_email_in_tenant_is_conf…]
- "tests_test_customer_access_rationale_28": "db.execute yields the given scalar_one_or_none values in order." | kind=entity | source=manager/backend/tests/test_customer_access.py:L28 | neighbors=[_mock_db()]
- "tests_test_customer_access_test_generate_password_is_unique_and_nonempty": "test_generate_password_is_unique_and_nonempty()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L82 | neighbors=[test_customer_access.py]
- "tests_test_customer_access_testbuildscanjob_test_dispatches_on_the_assigned_agent": ".test_dispatches_on_the_assigned_agent()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L59 | neighbors=[TestBuildScanJob]
- "tests_test_customer_access_testbuildscanjob_test_no_assigned_agent_raises": ".test_no_assigned_agent_raises()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L75 | neighbors=[TestBuildScanJob]
- "tests_test_customer_access_testbuildscanjob_test_unknown_scan_type_falls_back_to_vuln_scan": ".test_unknown_scan_type_falls_back_to_vuln_scan()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L70 | neighbors=[TestBuildScanJob]
- "tests_test_customer_reveal_rationale_1": "test_customer_reveal.py — operator reveal of a customer login password (item 1)." | kind=entity | source=manager/backend/tests/test_customer_reveal.py:L1 | neighbors=[test_customer_reveal.py]
- "tests_test_cve_correlation_db": "db()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L107 | neighbors=[test_cve_correlation.py]
- "tests_test_cve_correlation_rationale_1": "test_cve_correlation.py — the offline CVE-correlation layer (cve/ package).  Thi" | kind=entity | source=probe/tests/test_cve_correlation.py:L1 | neighbors=[test_cve_correlation.py]
- "tests_test_cve_correlation_testcli_test_correlate_writes_findings": ".test_correlate_writes_findings()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L351 | neighbors=[TestCli]
- "tests_test_cve_correlation_testcli_test_ingest_stdout_is_clean_json": ".test_ingest_stdout_is_clean_json()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L371 | neighbors=[TestCli]
- "tests_test_cve_correlation_testcorrelate_test_backport_banner_downgrades_confidence": ".test_backport_banner_downgrades_confidence()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L203 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_clean_banner_stays_medium": ".test_clean_banner_stays_medium()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L212 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_dedup_by_cve_target_port": ".test_dedup_by_cve_target_port()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L190 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_exposed_top_finding": ".test_exposed_top_finding()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L168 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_facts_without_cpe_ignored": ".test_facts_without_cpe_ignored()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L186 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_never_asserts_confidence_is_medium": ".test_never_asserts_confidence_is_medium()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L176 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_sorted_by_risk_desc": ".test_sorted_by_risk_desc()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L181 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_summarize": ".test_summarize()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L199 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcorrelate_test_to_dict_tags_type": ".test_to_dict_tags_type()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L195 | neighbors=[TestCorrelate]
- "tests_test_cve_correlation_testcpe_test_datastore_map_entries": ".test_datastore_map_entries()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L95 | neighbors=[TestCpe]
- "tests_test_cve_correlation_testcpe_test_mysql_vs_mariadb_vendor": ".test_mysql_vs_mariadb_vendor()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L85 | neighbors=[TestCpe]
- "tests_test_cve_correlation_testcpe_test_no_version_returns_none": ".test_no_version_returns_none()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L92 | neighbors=[TestCpe]
- "tests_test_cve_correlation_testcpe_test_openssh": ".test_openssh()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L76 | neighbors=[TestCpe]
- "tests_test_cve_correlation_testcpe_test_unknown_product_returns_none": ".test_unknown_product_returns_none()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L89 | neighbors=[TestCpe]
- "tests_test_cve_correlation_testcpe_test_version_pulled_from_product_string": ".test_version_pulled_from_product_string()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L81 | neighbors=[TestCpe]
- "tests_test_cve_correlation_testingestfeeds_test_epss_tolerates_plain_csv": ".test_epss_tolerates_plain_csv()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L313 | neighbors=[TestIngestFeeds]
- "tests_test_cve_correlation_testingestfeeds_test_ingest_all_stamps_last_ingest": ".test_ingest_all_stamps_last_ingest()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L318 | neighbors=[TestIngestFeeds]
- "tests_test_cve_correlation_testingestfeeds_test_kev_and_epss": ".test_kev_and_epss()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L295 | neighbors=[TestIngestFeeds]
- "tests_test_cve_correlation_testingestparse_test_cvss_fallback": ".test_cvss_fallback()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L253 | neighbors=[TestIngestParse]
- "tests_test_cve_correlation_testingestparse_test_ingest_idempotent": ".test_ingest_idempotent()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L245 | neighbors=[TestIngestParse]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-312.json

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
