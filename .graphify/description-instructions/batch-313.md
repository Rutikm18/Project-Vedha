# Node Description Batch 314 of 380

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

- "tests_test_cve_correlation_testingestparse_test_ingest_one_cve": ".test_ingest_one_cve()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L234 | neighbors=[TestIngestParse] | lang=en
- "tests_test_cve_correlation_testingestparse_test_parse_criteria": ".test_parse_criteria()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L260 | neighbors=[TestIngestParse] | lang=en
- "tests_test_cve_correlation_testmirrorage_test_fresh_has_no_warning": ".test_fresh_has_no_warning()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L333 | neighbors=[TestMirrorAge] | lang=en
- "tests_test_cve_correlation_testmirrorage_test_stale_warns": ".test_stale_warns()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L340 | neighbors=[TestMirrorAge] | lang=en
- "tests_test_cve_correlation_testmirrorage_test_unknown_when_no_stamp": ".test_unknown_when_no_stamp()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L330 | neighbors=[TestMirrorAge] | lang=en
- "tests_test_cve_correlation_testmirrorage_test_unparseable_stamp_is_graceful": ".test_unparseable_stamp_is_graceful()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L344 | neighbors=[TestMirrorAge] | lang=en
- "tests_test_cve_correlation_testriskscore_test_bands": ".test_bands()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L151 | neighbors=[TestRiskScore] | lang=en
- "tests_test_cve_correlation_testriskscore_test_capped_at_100": ".test_capped_at_100()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L163 | neighbors=[TestRiskScore] | lang=en
- "tests_test_cve_correlation_testriskscore_test_kev_and_exposure_weight": ".test_kev_and_exposure_weight()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L157 | neighbors=[TestRiskScore] | lang=en
- "tests_test_cve_correlation_testversion_test_compare": ".test_compare()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L51 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_in_range_end_exclusive": ".test_in_range_end_exclusive()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L56 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_in_range_exact": ".test_in_range_exact()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L65 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_in_range_start_inclusive": ".test_in_range_start_inclusive()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L61 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_in_range_unconstrained_is_false": ".test_in_range_unconstrained_is_false()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L69 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_parse_debian_epoch_and_distro_suffix": ".test_parse_debian_epoch_and_distro_suffix()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L41 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_parse_leading_v_and_empty": ".test_parse_leading_v_and_empty()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L46 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_parse_openssh_portable": ".test_parse_openssh_portable()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L35 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testversion_test_parse_openssl_letter_suffix": ".test_parse_openssl_letter_suffix()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L38 | neighbors=[TestVersion] | lang=en
- "tests_test_cve_correlation_testvulndb_test_counts": ".test_counts()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L137 | neighbors=[TestVulnDB] | lang=en
- "tests_test_cve_correlation_testvulndb_test_cves_for_cpe_in_range": ".test_cves_for_cpe_in_range()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L120 | neighbors=[TestVulnDB] | lang=en
- "tests_test_cve_correlation_testvulndb_test_kev_sorts_first": ".test_kev_sorts_first()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L125 | neighbors=[TestVulnDB] | lang=en
- "tests_test_cve_correlation_testvulndb_test_out_of_range_excluded": ".test_out_of_range_excluded()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L130 | neighbors=[TestVulnDB] | lang=en
- "tests_test_cve_correlation_testvulndb_test_vendor_norm": ".test_vendor_norm()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L134 | neighbors=[TestVulnDB] | lang=en
- "tests_test_dangling_agent_pin_rationale_1": "A job pinned to an agent that no longer exists must not be stranded forever.  OB" | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L1 | neighbors=[test_dangling_agent_pin.py] | lang=en
- "tests_test_dangling_agent_pin_rationale_110": "An ignored pin changes routing, so it must be visible in the log." | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L110 | neighbors=[.test_dangling_pin_is_logged_not_silent…] | lang=en
- "tests_test_dangling_agent_pin_rationale_116": "The safety property: ignoring a stale pin must NOT bypass capability         or" | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L116 | neighbors=[.test_fallback_still_runs_the_eligibili…] | lang=en
- "tests_test_dangling_agent_pin_rationale_32": "A db whose Agent.last_heartbeat lookup yields `value` (None = unknown)." | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L32 | neighbors=[_db_heartbeat()] | lang=pt
- "tests_test_dangling_agent_pin_rationale_43": "Row EXISTENCE is not the test — that was the first version and it was     wrong." | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L43 | neighbors=[TestPinnedAgentLiveness] | lang=en
- "tests_test_dangling_agent_pin_rationale_55": "The 15-minute window exists so a redeploy does not steal a job an         operat" | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L55 | neighbors=[.test_restarting_probe_keeps_its_pin()] | lang=en
- "tests_test_dangling_agent_pin_rationale_62": "The observed case: ~11 hours silent." | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L62 | neighbors=[.test_long_dead_agent_releases_its_pin()] | lang=en
- "tests_test_dangling_agent_pin_rationale_76": "Reusing the 90s online/offline threshold would release pins during an         or" | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L76 | neighbors=[.test_window_is_far_longer_than_the_90s…] | lang=en
- "tests_test_dangling_agent_pin_rationale_92": "Pins arrive from JSON params, so they are strings, not UUIDs." | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L92 | neighbors=[.test_string_form_of_a_real_id_is_accep…] | lang=en
- "tests_test_dangling_agent_pin_rationale_98": "Documents the rule the claim loop implements." | kind=entity | source=manager/backend/tests/test_dangling_agent_pin.py:L98 | neighbors=[TestPinSemantics] | lang=en
- "tests_test_dangling_agent_pin_testpinsemantics_test_live_pin_is_a_hard_constraint": ".test_live_pin_is_a_hard_constraint()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L100 | neighbors=[TestPinSemantics] | lang=en
- "tests_test_db_fact_shape_rationale_1": "test_db_fact_shape.py — the db_scan fact CONTRACT, not its protocol parsing.  WH" | kind=entity | source=probe/tests/test_db_fact_shape.py:L1 | neighbors=[test_db_fact_shape.py] | lang=en
- "tests_test_db_fact_shape_rationale_30": "A probe returning its own `db` key must not be able to unset the marker     the" | kind=entity | source=probe/tests/test_db_fact_shape.py:L30 | neighbors=[test_probe_output_never_overrides_the_m…] | lang=en
- "tests_test_db_fact_shape_rationale_37": "The one high-value DB signal already collected today must keep its shape     onc" | kind=entity | source=probe/tests/test_db_fact_shape.py:L37 | neighbors=[test_redis_unauth_shape_survives_stampi…] | lang=en
- "tests_test_db_fact_shape_test_existing_facts_are_preserved": "test_existing_facts_are_preserved()" | kind=code-symbol | source=probe/tests/test_db_fact_shape.py:L23 | neighbors=[test_db_fact_shape.py] | lang=en
- "tests_test_db_fact_shape_test_marker_is_stamped": "test_marker_is_stamped()" | kind=code-symbol | source=probe/tests/test_db_fact_shape.py:L19 | neighbors=[test_db_fact_shape.py] | lang=en
- "tests_test_db_mongodb_auth_rationale_1": "test_db_mongodb_auth.py — MongoDB auth posture, and the two ways to get it wrong" | kind=entity | source=probe/tests/test_db_mongodb_auth.py:L1 | neighbors=[test_db_mongodb_auth.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-313.json

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
