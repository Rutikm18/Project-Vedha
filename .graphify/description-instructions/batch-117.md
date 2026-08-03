# Node Description Batch 118 of 131

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
- "tests_test_probe_core_testusecasesresolve_test_use_cases_count": ".test_use_cases_count()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L944 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_valid_use_case": ".test_valid_use_case()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L912 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testworkflowcache_test_get_missing": ".test_get_missing()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L754 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_load_handles_corrupt_lines": ".test_load_handles_corrupt_lines()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L805 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_save_raises_without_path": ".test_save_raises_without_path()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L800 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_missing": ".test_should_recheck_missing()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L758 | neighbors=[TestWorkflowCache]
- "tests_test_probe_enrollment_test_device_access_token_has_dedicated_audience_and_generation": "test_device_access_token_has_dedicated_audience_and_generation()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L18 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_ed25519_proof_of_possession_rejects_tampering": "test_ed25519_proof_of_possession_rejects_tampering()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L39 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_enroll_token_create_defaults_and_bounds": "test_enroll_token_create_defaults_and_bounds()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L113 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_enrollment_create_accepts_optional_enroll_token": "test_enrollment_create_accepts_optional_enroll_token()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L125 | neighbors=[test_probe_enrollment.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-117.json

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
