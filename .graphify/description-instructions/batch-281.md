# Node Description Batch 282 of 336

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

- "tests_test_dns_scanner_rationale_1": "test_dns_scanner.py — DNS AXFR / DNSSEC / version.bind audit.  The live dnspytho" | kind=entity | source=probe/tests/test_dns_scanner.py:L1 | neighbors=[test_dns_scanner.py]
- "tests_test_dns_scanner_testaxfrbounded_test_axfr_refused_reports_not_transferred": ".test_axfr_refused_reports_not_transferred()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L78 | neighbors=[TestAxfrBounded]
- "tests_test_dns_scanner_testaxfrbounded_test_axfr_stops_at_cap": ".test_axfr_stops_at_cap()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L50 | neighbors=[TestAxfrBounded]
- "tests_test_dns_scanner_testderivezones_test_bounded": ".test_bounded()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L41 | neighbors=[TestDeriveZones]
- "tests_test_dns_scanner_testderivezones_test_explicit_zone_used_as_is": ".test_explicit_zone_used_as_is()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L33 | neighbors=[TestDeriveZones]
- "tests_test_dns_scanner_testderivezones_test_extra_before_target_derived": ".test_extra_before_target_derived()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L36 | neighbors=[TestDeriveZones]
- "tests_test_dns_scanner_testderivezones_test_hostname_target_reduces_to_registrable_and_parent": ".test_hostname_target_reduces_to_registrable_and_parent()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L26 | neighbors=[TestDeriveZones]
- "tests_test_dns_scanner_testderivezones_test_ip_target_derives_nothing": ".test_ip_target_derives_nothing()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L29 | neighbors=[TestDeriveZones]
- "tests_test_dns_scanner_testparity_test_scanner_and_findings_in_main_scripts": ".test_scanner_and_findings_in_main_scripts()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L159 | neighbors=[TestParity]
- "tests_test_dualstack_fallback_rationale_1": "test_dualstack_fallback.py — roadmap #9 / #4.1, the CALL-SITE migration.  `resol" | kind=entity | source=probe/tests/test_dualstack_fallback.py:L1 | neighbors=[test_dualstack_fallback.py]
- "tests_test_dualstack_fallback_rationale_52": "A socket whose connect() fails for `dead_family`, succeeds otherwise." | kind=entity | source=probe/tests/test_dualstack_fallback.py:L52 | neighbors=[._fake_socket()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-281.json

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
