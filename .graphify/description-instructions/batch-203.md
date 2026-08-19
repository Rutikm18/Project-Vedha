# Node Description Batch 204 of 227

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

- "tests_test_pipeline_rationale_124": "Passing an empty path list must return empty findings and no facts." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L124 | neighbors=[.test_no_paths_returns_empty()] | lang=en
- "tests_test_pipeline_rationale_140": "A credentialed package at a version inside a vulnerable range must         produ" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L140 | neighbors=[.test_ssh_inventory_vulnerable_package_…] | lang=pt
- "tests_test_pipeline_rationale_151": "Findings from an authoritative (credentialed) source must be         confirmed —" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L151 | neighbors=[.test_ssh_inventory_finding_is_confirme…] | lang=en
- "tests_test_pipeline_rationale_164": "A banner-derived (inferred) source match can only produce 'suspected'         —" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L164 | neighbors=[.test_banner_finding_is_suspected_not_c…] | lang=pt
- "tests_test_pipeline_rationale_177": "A host running the fixed version must not produce a finding." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L177 | neighbors=[.test_no_finding_for_patched_version()] | lang=pt
- "tests_test_pipeline_rationale_188": "When all three dbs are injected, the pipeline must not try to read         the d" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L188 | neighbors=[.test_injected_dbs_used_no_file_io()] | lang=en
- "tests_test_pipeline_rationale_217": "Without an exposure dict the fields stay None — pipeline never guesses." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L217 | neighbors=[.test_no_exposure_fields_are_none()] | lang=en
- "tests_test_pipeline_rationale_234": "Different IPs must produce independent findings — dedup is per         (asset, C" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L234 | neighbors=[.test_two_identical_hosts_each_get_thei…] | lang=en
- "tests_test_pipeline_rationale_247": "The same (asset, CVE) can't appear twice in the output — dedup         must coll" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L247 | neighbors=[.test_findings_deduped_within_same_host…] | lang=en
- "tests_test_pipeline_rationale_281": "With use_ai_assist=False (the default) and no ai_client, the pipeline         pr" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L281 | neighbors=[.test_ai_assist_off_by_default()] | lang=en
- "tests_test_pipeline_rationale_292": "ab_evaluate must return a dict with the expected structure." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L292 | neighbors=[.test_ab_evaluate_returns_expected_keys…] | lang=en
- "tests_test_pipeline_rationale_304": "When FakeAIClient returns nothing new, there must be no precision         regres" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L304 | neighbors=[.test_ab_evaluate_no_precision_regressi…] | lang=en
- "tests_test_pipeline_rationale_50": "Returns a VulnDB with a record that matches openssh 8.4p1 (vulnerable).      The" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L50 | neighbors=[_openssh_vuln_db()] | lang=en
- "tests_test_port_catalog_test_modern_infra_ports_present": "test_modern_infra_ports_present()" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L4 | neighbors=[test_port_catalog.py] | lang=en
- "tests_test_portal_metrics_rationale_1": "test_portal_metrics.py — pure dashboard aggregations." | kind=entity | source=manager/backend/tests/test_portal_metrics.py:L1 | neighbors=[test_portal_metrics.py] | lang=en
- "tests_test_portal_metrics_testseveritybreakdown_test_all_buckets_present_zero_filled": ".test_all_buckets_present_zero_filled()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L20 | neighbors=[TestSeverityBreakdown] | lang=en
- "tests_test_portal_metrics_teststatustimeline_test_emits_continuous_zero_filled_months": ".test_emits_continuous_zero_filled_months()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L42 | neighbors=[TestStatusTimeline] | lang=en
- "tests_test_portal_read_rationale_1": "test_portal_read.py — Phase 2: the customer-facing read API. Verifies the two da" | kind=entity | source=manager/backend/tests/test_portal_read.py:L1 | neighbors=[test_portal_read.py] | lang=en
- "tests_test_portal_read_rationale_153": "Each db.execute(...) → result whose .scalars().first() is the next value;     pl" | kind=entity | source=manager/backend/tests/test_portal_read.py:L153 | neighbors=[_db_first()] | lang=en
- "tests_test_portal_read_rationale_217": "Mock the create_scan_request db flow: execute#1 → engagement lookup     (.scalar" | kind=entity | source=manager/backend/tests/test_portal_read.py:L217 | neighbors=[_db_for_create()] | lang=en
- "tests_test_portal_read_rationale_36": "Each db.execute(...) → result whose .scalars().all() is the next list." | kind=entity | source=manager/backend/tests/test_portal_read.py:L36 | neighbors=[_db_list()] | lang=en
- "tests_test_portal_read_rationale_59": "A finding-like ORM object carrying BOTH whitelisted and internal fields." | kind=entity | source=manager/backend/tests/test_portal_read.py:L59 | neighbors=[_finding_with_internal()] | lang=en
- "tests_test_portal_read_testclientfindingwhitelist_test_schema_is_a_whitelist": ".test_schema_is_a_whitelist()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L83 | neighbors=[TestClientFindingWhitelist] | lang=en
- "tests_test_portal_remediation_rationale_1": "test_portal_remediation.py — Section 6: the customer-facing remediation route." | kind=entity | source=manager/backend/tests/test_portal_remediation.py:L1 | neighbors=[test_portal_remediation.py] | lang=en
- "tests_test_portal_remediation_rationale_33": "Each db.execute(...) → result whose .scalar_one_or_none() is the next val." | kind=entity | source=manager/backend/tests/test_portal_remediation.py:L33 | neighbors=[_db_scalar()] | lang=en
- "tests_test_portal_scope_rationale_1": "test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping au" | kind=entity | source=manager/backend/tests/test_portal_scope.py:L1 | neighbors=[test_portal_scope.py] | lang=en
- "tests_test_portal_scope_testassertclient_test_client_without_engagement_is_forbidden": ".test_client_without_engagement_is_forbidden()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L47 | neighbors=[TestAssertClient] | lang=en
- "tests_test_portal_scope_testportaltokenclaims_test_client_role_enum_exists": ".test_client_role_enum_exists()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L99 | neighbors=[TestPortalTokenClaims] | lang=en
- "tests_test_portal_scope_testportaltokenclaims_test_client_token_carries_portal_aud_and_engagement": ".test_client_token_carries_portal_aud_and_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L85 | neighbors=[TestPortalTokenClaims] | lang=en
- "tests_test_portal_scope_testportaltokenclaims_test_operator_and_portal_audiences_differ": ".test_operator_and_portal_audiences_differ()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L96 | neighbors=[TestPortalTokenClaims] | lang=en
- "tests_test_posture_row_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L110 | neighbors=[_Row] | lang=en
- "tests_test_posture_test_aggregate_is_bounded_and_empty_is_zero": "test_aggregate_is_bounded_and_empty_is_zero()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L22 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_aggregate_is_monotonic": "test_aggregate_is_monotonic()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L31 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_build_posture_no_runs": "test_build_posture_no_runs()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L72 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_compute_scores_empty_is_perfect": "test_compute_scores_empty_is_perfect()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L48 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_grade_bands": "test_grade_bands()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L37 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_posture_report_section_omitted_without_runs": "test_posture_report_section_omitted_without_runs()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L167 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_posture_report_section_renders_scores_and_matrix": "test_posture_report_section_renders_scores_and_matrix()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L149 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_sev_str_passes_through_plain_string": "test_sev_str_passes_through_plain_string()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L143 | neighbors=[test_posture.py] | lang=en
- "tests_test_probe_auto_enroll_rationale_1": "test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.  T" | kind=entity | source=manager/backend/tests/test_probe_auto_enroll.py:L1 | neighbors=[test_probe_auto_enroll.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-203.json

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
