# Node Description Batch 96 of 104

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

- "tests_test_probe_core_testgate0_test_it_not_passive": ".test_it_not_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L247 | neighbors=[TestGate0]
- "tests_test_probe_core_testgate0_test_ot_is_passive": ".test_ot_is_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L244 | neighbors=[TestGate0]
- "tests_test_probe_core_testlookslikehttp_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L374 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_http_1_1": ".test_http_1_1()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L365 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_http_2": ".test_http_2()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L368 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_not_http": ".test_not_http()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L371 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlooksliketls_test_banner_present": ".test_banner_present()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L389 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_client_first_port_not_tls": ".test_client_first_port_not_tls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L383 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_no_banner_attempt": ".test_no_banner_attempt()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L386 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_silent_non_client_first_port": ".test_silent_non_client_first_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L380 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testparseports_test_bad_token_raises": ".test_bad_token_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L192 | neighbors=[TestParsePorts]
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
- "tests_test_probe_core_testresolvescantype_test_default": ".test_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L709 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_from_job_type": ".test_from_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L706 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_from_params": ".test_from_params()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L703 | neighbors=[TestResolveScanType]
- "tests_test_probe_core_testresolvescantype_test_params_override_job_type": ".test_params_override_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L712 | neighbors=[TestResolveScanType]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-095.json

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
