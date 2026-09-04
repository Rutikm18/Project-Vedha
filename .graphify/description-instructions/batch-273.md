# Node Description Batch 274 of 332

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
- "tests_test_cve_correlation_testingestparse_test_ingest_one_cve": ".test_ingest_one_cve()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L234 | neighbors=[TestIngestParse]
- "tests_test_cve_correlation_testingestparse_test_parse_criteria": ".test_parse_criteria()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L260 | neighbors=[TestIngestParse]
- "tests_test_cve_correlation_testmirrorage_test_fresh_has_no_warning": ".test_fresh_has_no_warning()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L333 | neighbors=[TestMirrorAge]
- "tests_test_cve_correlation_testmirrorage_test_stale_warns": ".test_stale_warns()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L340 | neighbors=[TestMirrorAge]
- "tests_test_cve_correlation_testmirrorage_test_unknown_when_no_stamp": ".test_unknown_when_no_stamp()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L330 | neighbors=[TestMirrorAge]
- "tests_test_cve_correlation_testmirrorage_test_unparseable_stamp_is_graceful": ".test_unparseable_stamp_is_graceful()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L344 | neighbors=[TestMirrorAge]
- "tests_test_cve_correlation_testriskscore_test_bands": ".test_bands()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L151 | neighbors=[TestRiskScore]
- "tests_test_cve_correlation_testriskscore_test_capped_at_100": ".test_capped_at_100()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L163 | neighbors=[TestRiskScore]
- "tests_test_cve_correlation_testriskscore_test_kev_and_exposure_weight": ".test_kev_and_exposure_weight()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L157 | neighbors=[TestRiskScore]
- "tests_test_cve_correlation_testversion_test_compare": ".test_compare()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L51 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_in_range_end_exclusive": ".test_in_range_end_exclusive()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L56 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_in_range_exact": ".test_in_range_exact()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L65 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_in_range_start_inclusive": ".test_in_range_start_inclusive()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L61 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_in_range_unconstrained_is_false": ".test_in_range_unconstrained_is_false()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L69 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_debian_epoch_and_distro_suffix": ".test_parse_debian_epoch_and_distro_suffix()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L41 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_leading_v_and_empty": ".test_parse_leading_v_and_empty()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L46 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_openssh_portable": ".test_parse_openssh_portable()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L35 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_openssl_letter_suffix": ".test_parse_openssl_letter_suffix()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L38 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testvulndb_test_counts": ".test_counts()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L137 | neighbors=[TestVulnDB]
- "tests_test_cve_correlation_testvulndb_test_cves_for_cpe_in_range": ".test_cves_for_cpe_in_range()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L120 | neighbors=[TestVulnDB]
- "tests_test_cve_correlation_testvulndb_test_kev_sorts_first": ".test_kev_sorts_first()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L125 | neighbors=[TestVulnDB]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-273.json

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
