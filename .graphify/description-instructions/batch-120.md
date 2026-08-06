# Node Description Batch 121 of 134

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

- "tests_test_probe_core_testparseports_test_single_port": ".test_single_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L190 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_sorted": ".test_sorted()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L205 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testratelimiter_test_min_interval": ".test_min_interval()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L248 | neighbors=[TestRateLimiter]
- "tests_test_probe_core_testratelimiter_test_wait_returns_immediately_at_zero_rate": ".test_wait_returns_immediately_at_zero_rate()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L256 | neighbors=[TestRateLimiter]
- "tests_test_probe_core_testratelimiter_test_zero_rate": ".test_zero_rate()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L252 | neighbors=[TestRateLimiter]
- "tests_test_probe_core_testresolvescantype_test_default": ".test_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L823 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_from_job_type": ".test_from_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L820 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_from_params": ".test_from_params()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L817 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_params_override_job_type": ".test_params_override_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L826 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testscanresult_test_default_status_observed": ".test_default_status_observed()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L238 | neighbors=[TestScanResult]
- "tests_test_probe_core_testscanresult_test_default_timestamp_present": ".test_default_timestamp_present()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L234 | neighbors=[TestScanResult]
- "tests_test_probe_core_testscopeguard_test_assert_in_scope_passes": ".test_assert_in_scope_passes()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L114 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_assert_in_scope_raises": ".test_assert_in_scope_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L109 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_excludes_larger_subnet": ".test_excludes_larger_subnet()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L104 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_excludes_override_allowlist": ".test_excludes_override_allowlist()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L99 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_filter_yields_only_in_scope": ".test_filter_yields_only_in_scope()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L118 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_file": ".test_from_file()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L123 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_file_empty_raises": ".test_from_file_empty_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L130 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_file_missing_raises": ".test_from_file_missing_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L136 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_list_hostname": ".test_from_list_hostname()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L90 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_list_ip_in_cidr": ".test_from_list_ip_in_cidr()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L80 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_from_list_single_ip": ".test_from_list_single_ip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L85 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testscopeguard_test_hostname_case_insensitive": ".test_hostname_case_insensitive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L95 | neighbors=[TestScopeGuard]
- "tests_test_probe_core_testtargets_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L857 | neighbors=[TestTargets]
- "tests_test_probe_core_testtargets_test_list": ".test_list()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L848 | neighbors=[TestTargets]
- "tests_test_probe_core_testtargets_test_scope_cidrs": ".test_scope_cidrs()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L854 | neighbors=[TestTargets]
- "tests_test_probe_core_testtargets_test_single_string": ".test_single_string()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L851 | neighbors=[TestTargets]
- "tests_test_probe_core_testtuningfromparams_test_clamped_rate": ".test_clamped_rate()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L868 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_defaults": ".test_defaults()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L862 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_no_ssh_creds_without_user": ".test_no_ssh_creds_without_user()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L876 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_passive_listen_seconds": ".test_passive_listen_seconds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L888 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_recheck_hours": ".test_recheck_hours()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L884 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_ssh_creds": ".test_ssh_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L872 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_win_creds": ".test_win_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L880 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testusecasesresolve_test_default_discovery": ".test_default_discovery()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L940 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_fallback_to_job_type": ".test_fallback_to_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L936 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_fallback_to_scan_type": ".test_fallback_to_scan_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L931 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_full_assessment": ".test_full_assessment()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L917 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_ot_passive": ".test_ot_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L922 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_unknown_use_case_raises": ".test_unknown_use_case_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L927 | neighbors=[TestUseCasesResolve]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-120.json

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
