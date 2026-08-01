# Node Description Batch 108 of 119

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_probe_core_testparseports_test_comma_separated": ".test_comma_separated()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L171 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_duplicates_removed": ".test_duplicates_removed()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L180 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_mixed": ".test_mixed()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L177 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_out_of_range_raises": ".test_out_of_range_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L186 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_range": ".test_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L174 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_reversed_range_raises": ".test_reversed_range_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L196 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_single_port": ".test_single_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L168 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_sorted": ".test_sorted()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L183 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testratelimiter_test_min_interval": ".test_min_interval()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L226 | neighbors=[TestRateLimiter]
- "tests_test_probe_core_testratelimiter_test_wait_returns_immediately_at_zero_rate": ".test_wait_returns_immediately_at_zero_rate()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L234 | neighbors=[TestRateLimiter]
- "tests_test_probe_core_testratelimiter_test_zero_rate": ".test_zero_rate()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L230 | neighbors=[TestRateLimiter]
- "tests_test_probe_core_testresolvescantype_test_default": ".test_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L801 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_from_job_type": ".test_from_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L798 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_from_params": ".test_from_params()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L795 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_params_override_job_type": ".test_params_override_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L804 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testscanresult_test_default_status_observed": ".test_default_status_observed()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L216 | neighbors=[TestScanResult]
- "tests_test_probe_core_testscanresult_test_default_timestamp_present": ".test_default_timestamp_present()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L212 | neighbors=[TestScanResult]
- "tests_test_probe_core_testscopeguard_test_assert_in_scope_passes": ".test_assert_in_scope_passes()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L92 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_assert_in_scope_raises": ".test_assert_in_scope_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L87 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_excludes_larger_subnet": ".test_excludes_larger_subnet()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L82 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_excludes_override_allowlist": ".test_excludes_override_allowlist()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L77 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_filter_yields_only_in_scope": ".test_filter_yields_only_in_scope()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L96 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_file": ".test_from_file()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L101 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_file_empty_raises": ".test_from_file_empty_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L108 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_file_missing_raises": ".test_from_file_missing_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L114 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_list_hostname": ".test_from_list_hostname()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L68 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_list_ip_in_cidr": ".test_from_list_ip_in_cidr()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L58 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_list_single_ip": ".test_from_list_single_ip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L63 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_hostname_case_insensitive": ".test_hostname_case_insensitive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L73 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testtargets_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L835 | neighbors=[TestTargets]
- "tests_test_probe_core_testtargets_test_list": ".test_list()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L826 | neighbors=[TestTargets]
- "tests_test_probe_core_testtargets_test_scope_cidrs": ".test_scope_cidrs()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L832 | neighbors=[TestTargets]
- "tests_test_probe_core_testtargets_test_single_string": ".test_single_string()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L829 | neighbors=[TestTargets]
- "tests_test_probe_core_testtuningfromparams_test_clamped_rate": ".test_clamped_rate()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L846 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_defaults": ".test_defaults()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L840 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_no_ssh_creds_without_user": ".test_no_ssh_creds_without_user()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L854 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_passive_listen_seconds": ".test_passive_listen_seconds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L866 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_recheck_hours": ".test_recheck_hours()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L862 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_ssh_creds": ".test_ssh_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L850 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_win_creds": ".test_win_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L858 | neighbors=[TestTuningFromParams]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-107.json

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
