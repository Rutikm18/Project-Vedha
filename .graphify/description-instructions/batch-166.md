# Node Description Batch 167 of 186

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

- "tests_test_perf_optimization_rationale_50": "Isolate the guard's in-memory + on-disk validation cache per test." | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L50 | neighbors=[clean_guard_cache()] | lang=en
- "tests_test_perf_optimization_rationale_58": "No dpkg binary → nothing to cross-check against; return [] and never     attempt" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L58 | neighbors=[test_guard_is_noop_without_dpkg()] | lang=en
- "tests_test_perf_optimization_rationale_76": "When the binary disagrees with pure-Python on an adjacent pair, that pair     is" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L76 | neighbors=[test_guard_reports_divergence_and_warns…] | lang=en
- "tests_test_perf_optimization_test_guard_passes_when_pure_python_agrees_with_dpkg": "test_guard_passes_when_pure_python_agrees_with_dpkg()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L67 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_perf_optimization_test_guard_validates_once_per_cache_key": "test_guard_validates_once_per_cache_key()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L86 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_perf_optimization_test_load_kev_and_epss_memoized": "test_load_kev_and_epss_memoized()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L142 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_pipeline_rationale_1": "Tests for pipeline.py — the orchestrator with 0% prior coverage.  Covers the cri" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L1 | neighbors=[test_pipeline.py] | lang=en
- "tests_test_pipeline_rationale_114": "A completely empty file must not produce any findings." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L114 | neighbors=[.test_empty_jsonl_returns_no_findings()] | lang=pt
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
- "tests_test_posture_row_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L110 | neighbors=[_Row] | lang=en
- "tests_test_posture_test_aggregate_is_bounded_and_empty_is_zero": "test_aggregate_is_bounded_and_empty_is_zero()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L22 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_aggregate_is_monotonic": "test_aggregate_is_monotonic()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L31 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_build_posture_no_runs": "test_build_posture_no_runs()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L72 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_compute_scores_empty_is_perfect": "test_compute_scores_empty_is_perfect()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L48 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_grade_bands": "test_grade_bands()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L37 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_posture_report_section_omitted_without_runs": "test_posture_report_section_omitted_without_runs()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L167 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_posture_report_section_renders_scores_and_matrix": "test_posture_report_section_renders_scores_and_matrix()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L149 | neighbors=[test_posture.py] | lang=en
- "tests_test_posture_test_sev_str_passes_through_plain_string": "test_sev_str_passes_through_plain_string()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L143 | neighbors=[test_posture.py] | lang=en
- "tests_test_probe_core_rationale_1": "Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG" | kind=entity | source=probe/tests/test_probe_core.py:L1 | neighbors=[test_probe_core.py] | lang=en
- "tests_test_probe_core_test_explicit_local_manager_urls": "test_explicit_local_manager_urls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L47 | neighbors=[test_probe_core.py] | lang=en
- "tests_test_probe_core_test_nonlocal_manager_urls": "test_nonlocal_manager_urls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L57 | neighbors=[test_probe_core.py] | lang=en
- "tests_test_probe_core_testcapabilities_test_capabilities_sorted": ".test_capabilities_sorted()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L894 | neighbors=[TestCapabilities] | lang=en
- "tests_test_probe_core_testcapabilities_test_known_scan_types": ".test_known_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L897 | neighbors=[TestCapabilities] | lang=en
- "tests_test_probe_core_testclamp_test_bad_value_uses_default": ".test_bad_value_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L840 | neighbors=[TestClamp] | lang=en
- "tests_test_probe_core_testclamp_test_clamped_high": ".test_clamped_high()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L834 | neighbors=[TestClamp] | lang=en
- "tests_test_probe_core_testclamp_test_clamped_low": ".test_clamped_low()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L837 | neighbors=[TestClamp] | lang=en
- "tests_test_probe_core_testclamp_test_in_range": ".test_in_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L831 | neighbors=[TestClamp] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-166.json

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
