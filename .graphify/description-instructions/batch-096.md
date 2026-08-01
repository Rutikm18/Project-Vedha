# Node Description Batch 97 of 119

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

- "summary_route_apisummary": "ApiSummary" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L5 | neighbors=[route.ts]
- "summary_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L18 | neighbors=[route.ts]
- "tests_findings_store_test_makefinding": "makeFinding()" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L25 | neighbors=[findings-store.test.ts]
- "tests_findings_store_test_tmp_dir": "TMP_DIR" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L8 | neighbors=[findings-store.test.ts]
- "tests_findings_store_test_tmp_file": "TMP_FILE" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L9 | neighbors=[findings-store.test.ts]
- "tests_parsers_test_naabu_line": "NAABU_LINE" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L81 | neighbors=[parsers.test.ts]
- "tests_parsers_test_nuclei_valid": "NUCLEI_VALID" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L56 | neighbors=[parsers.test.ts]
- "tests_parsers_test_testssl_valid": "TESTSSL_VALID" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L73 | neighbors=[parsers.test.ts]
- "tests_test_ad_assessment_fakeattr_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L32 | neighbors=[_FakeAttr]
- "tests_test_ad_assessment_fakeentry_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L37 | neighbors=[_FakeEntry]
- "tests_test_ad_assessment_testadcschecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L280 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc1_negative_when_manager_approval": ".test_esc1_negative_when_manager_approval()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L292 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc1_negative_without_low_priv_enrollment": ".test_esc1_negative_without_low_priv_enrollment()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L299 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc1_positive": ".test_esc1_positive()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L283 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc4_negative_when_deny_ace": ".test_esc4_negative_when_deny_ace()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L313 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc4_positive": ".test_esc4_positive()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L306 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc8_negative_no_web_enrollment": ".test_esc8_negative_no_web_enrollment()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L332 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc8_negative_with_epa_and_https": ".test_esc8_negative_with_epa_and_https()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L326 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc8_positive": ".test_esc8_positive()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L320 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_generate_findings_produces_esc1_and_esc8": ".test_generate_findings_produces_esc1_and_esc8()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L335 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testasreproastchecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L217 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_finding_shape": ".test_finding_shape()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L229 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_get_no_preauth_accounts": ".test_get_no_preauth_accounts()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L220 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_no_finding_when_empty": ".test_no_finding_when_empty()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L235 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_request_asrep_without_impacket": ".test_request_asrep_without_impacket()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L238 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testbloodhoundcollector_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L358 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_da_path_finding_critical_when_short": ".test_da_path_finding_critical_when_short()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L361 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_da_path_finding_high_when_long": ".test_da_path_finding_high_when_long()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L368 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_import_without_neo4j": ".test_import_without_neo4j()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L379 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_no_finding_without_paths": ".test_no_finding_without_paths()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L373 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_query_da_paths_without_driver": ".test_query_da_paths_without_driver()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L376 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbuildadfinding_test_attack_narrative_carried_in_evidence": ".test_attack_narrative_carried_in_evidence()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L84 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testbuildadfinding_test_invalid_severity_falls_back_to_info": ".test_invalid_severity_falls_back_to_info()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L76 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testbuildadfinding_test_required_fields_present": ".test_required_fields_present()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L60 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testkerberoastchecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L170 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_finding_critical_when_privileged": ".test_finding_critical_when_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L189 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_finding_high_when_not_privileged": ".test_finding_high_when_not_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L197 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_no_finding_when_empty": ".test_no_finding_when_empty()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L202 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_request_tgs_without_impacket_returns_none": ".test_request_tgs_without_impacket_returns_none()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L205 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_domain_to_base_dn": ".test_domain_to_base_dn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L99 | neighbors=[TestLDAPEnumeratorParsing]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-096.json

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
