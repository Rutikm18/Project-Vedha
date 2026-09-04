# Node Description Batch 278 of 332

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

- "tests_test_dualstack_fallback_testosfingerprintsmbbuildfallback_test_falls_back_across_families": ".test_falls_back_across_families()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L119 | neighbors=[TestOsFingerprintSmbBuildFallback]
- "tests_test_dualstack_fallback_testrdpfallback_test_none_when_no_family_speaks_rdp": ".test_none_when_no_family_speaks_rdp()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L150 | neighbors=[TestRdpFallback]
- "tests_test_dualstack_fallback_testrdpfallback_test_probes_next_family_when_first_is_silent": ".test_probes_next_family_when_first_is_silent()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L136 | neighbors=[TestRdpFallback]
- "tests_test_dualstack_fallback_testrdpfallback_test_unresolvable_host_is_survivable": ".test_unresolvable_host_is_survivable()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L158 | neighbors=[TestRdpFallback]
- "tests_test_dualstack_fallback_testresolveipcandidates_test_returns_ips_in_order": ".test_returns_ips_in_order()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L32 | neighbors=[TestResolveIpCandidates]
- "tests_test_dualstack_fallback_testresolveipcandidates_test_unresolvable_returns_empty_not_raises": ".test_unresolvable_returns_empty_not_raises()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L38 | neighbors=[TestResolveIpCandidates]
- "tests_test_dualstack_fallback_testsmbntlmfallback_test_empty_when_no_address_answers": ".test_empty_when_no_address_answers()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L110 | neighbors=[TestSmbNtlmFallback]
- "tests_test_dualstack_fallback_testsmbntlmfallback_test_first_answering_address_wins": ".test_first_answering_address_wins()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L97 | neighbors=[TestSmbNtlmFallback]
- "tests_test_dualstack_fallback_testsynscannerrequestsipv4_test_resolve_is_asked_for_ipv4": ".test_resolve_is_asked_for_ipv4()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L202 | neighbors=[TestSynScannerRequestsIPv4]
- "tests_test_dualstack_fallback_testtlsfingerprintfallback_test_none_when_no_family_speaks_tls": ".test_none_when_no_family_speaks_tls()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L185 | neighbors=[TestTlsFingerprintFallback]
- "tests_test_dualstack_fallback_testtlsfingerprintfallback_test_unresolvable_host_is_survivable": ".test_unresolvable_host_is_survivable()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L193 | neighbors=[TestTlsFingerprintFallback]
- "tests_test_dualstack_fallback_testtlsfingerprintfallback_test_uses_the_family_that_actually_speaks_tls": ".test_uses_the_family_that_actually_speaks_tls()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L170 | neighbors=[TestTlsFingerprintFallback]
- "tests_test_e2e_engagement_to_findings_accept_loop": "_accept_loop()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L27 | neighbors=[test_e2e_engagement_to_findings.py]
- "tests_test_e2e_engagement_to_findings_rationale_1": "test_e2e_engagement_to_findings.py — the whole pipeline in one place.      manag" | kind=entity | source=probe/tests/test_e2e_engagement_to_findings.py:L1 | neighbors=[test_e2e_engagement_to_findings.py]
- "tests_test_e2e_engagement_to_findings_rationale_138": "Exactly what the probe's smb/port scanners emit for a vulnerable host." | kind=entity | source=probe/tests/test_e2e_engagement_to_findings.py:L138 | neighbors=[_vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_rationale_52": "Return (http_get, submit_result, captured) simulating the manager side." | kind=entity | source=probe/tests/test_e2e_engagement_to_findings.py:L52 | neighbors=[_manager()]
- "tests_test_engagement_lists_rationale_1": "Unit tests for the dashboard list endpoints (jobs + assets)." | kind=entity | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[test_engagement_lists.py]
- "tests_test_engagement_validation_test_create_normalizes_name_scopes_and_duplicates": "test_create_normalizes_name_scopes_and_duplicates()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L10 | neighbors=[test_engagement_validation.py]
- "tests_test_engagement_validation_test_create_rejects_invalid_scope_entries": "test_create_rejects_invalid_scope_entries()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L31 | neighbors=[test_engagement_validation.py]
- "tests_test_engagement_validation_test_create_rejects_reversed_date_range": "test_create_rejects_reversed_date_range()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L36 | neighbors=[test_engagement_validation.py]
- "tests_test_engagement_validation_test_update_rejects_blank_name_invalid_scope_and_reversed_dates": "test_update_rejects_blank_name_invalid_scope_and_reversed_dates()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L46 | neighbors=[test_engagement_validation.py]
- "tests_test_engine_bridge_ingest_health_rationale_1": "test_engine_bridge_ingest_health.py — a zero-finding run must never be able to L" | kind=entity | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L1 | neighbors=[test_engine_bridge_ingest_health.py]
- "tests_test_engine_bridge_ingest_health_rationale_44": "Baseline: the shape the agent actually sends survives ingest and fires rules." | kind=entity | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L44 | neighbors=[test_healthy_facts_ingest_completely_an…]
- "tests_test_engine_bridge_ingest_health_rationale_56": "The regression. Drop the one field an agent rename could plausibly drop and" | kind=entity | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L56 | neighbors=[test_total_shape_drift_is_reported_not_…]
- "tests_test_engine_bridge_ingest_health_rationale_73": "A partly-bad batch must keep its good findings AND still admit what it lost." | kind=entity | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L73 | neighbors=[test_partial_drift_still_detects_but_re…]
- "tests_test_engine_bridge_ingest_health_rationale_85": "The census is best-effort by contract: an older engine returning no     IngestRe" | kind=entity | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L85 | neighbors=[test_census_survives_an_engine_that_ret…]
- "tests_test_engine_bridge_posture_rationale_1": "test_engine_bridge_posture.py — the posture/config-exposure track reaches Findin" | kind=entity | source=manager/backend/tests/test_engine_bridge_posture.py:L1 | neighbors=[test_engine_bridge_posture.py]
- "tests_test_engine_bridge_posture_test_no_posture_no_finding": "test_no_posture_no_finding()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L69 | neighbors=[test_engine_bridge_posture.py]
- "tests_test_engine_bridge_posture_test_posture_finding_becomes_a_finding_row": "test_posture_finding_becomes_a_finding_row()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L33 | neighbors=[test_engine_bridge_posture.py]
- "tests_test_engine_bridge_regression_test_reopen_flips_remediated_to_open_and_flags_regression": "test_reopen_flips_remediated_to_open_and_flags_regression()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_regression.py:L10 | neighbors=[test_engine_bridge_regression.py]
- "tests_test_engine_bridge_resolution_test_run_records_coverage_and_invokes_resolution": "test_run_records_coverage_and_invokes_resolution()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_resolution.py:L12 | neighbors=[test_engine_bridge_resolution.py]
- "tests_test_engine_bridge_verification_test_stamp_verification_sets_columns_when_enabled": "test_stamp_verification_sets_columns_when_enabled()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_verification.py:L13 | neighbors=[test_engine_bridge_verification.py]
- "tests_test_enqueue_intensity_rationale_1": "test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper" | kind=entity | source=manager/backend/tests/test_enqueue_intensity.py:L1 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_every_manager_code_maps_to_a_known_use_case": "test_every_manager_code_maps_to_a_known_use_case()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L76 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_intensity_accepts_code_or_name": "test_intensity_accepts_code_or_name()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L62 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_invalid_intensity_is_rejected_at_the_schema": "test_invalid_intensity_is_rejected_at_the_schema()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L35 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_normalize_intensity_name_maps_codes": "test_normalize_intensity_name_maps_codes()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L69 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_numeric_uc_code_accepted": "test_numeric_uc_code_accepted()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L52 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_omitted_intensity_is_none": "test_omitted_intensity_is_none()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L30 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_unknown_uc_code_rejected": "test_unknown_uc_code_rejected()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L57 | neighbors=[test_enqueue_intensity.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-277.json

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
