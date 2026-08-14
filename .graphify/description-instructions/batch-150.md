# Node Description Batch 151 of 186

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
- "tests_test_ad_assessment_testldapenumeratorparsing_test_search_without_connection_raises": ".test_search_without_connection_raises()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L158 | neighbors=[TestLDAPEnumeratorParsing]
- "tests_test_ad_assessment_testntlmrelaychecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L249 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_finding_for_ldap_signing_only": ".test_finding_for_ldap_signing_only()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L265 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_finding_includes_ntlmrelayx_command": ".test_finding_includes_ntlmrelayx_command()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L258 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_no_finding_when_all_secure": ".test_no_finding_when_all_secure()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L270 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_smb_signing_without_impacket_marks_unreachable": ".test_smb_signing_without_impacket_marks_unreachable()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L252 | neighbors=[TestNTLMRelayChecker]
- "tests_test_adaptive_rate_echoprotocol_connection_made": ".connection_made()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L178 | neighbors=[_EchoProtocol]
- "tests_test_adaptive_rate_echoprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L181 | neighbors=[_EchoProtocol]
- "tests_test_adaptive_rate_rationale_1": "test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit." | kind=entity | source=probe/tests/test_adaptive_rate.py:L1 | neighbors=[test_adaptive_rate.py]
- "tests_test_adaptive_rate_testudpretransmit_test_retries_exhaust_on_silence": ".test_retries_exhaust_on_silence()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L146 | neighbors=[TestUdpRetransmit]
- "tests_test_adaptive_rate_testudpretransmit_test_retry_recovers_dropped_reply": ".test_retry_recovers_dropped_reply()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L159 | neighbors=[TestUdpRetransmit]
- "tests_test_adaptive_rate_testudpretransmit_test_returns_immediately_on_closed": ".test_returns_immediately_on_closed()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L133 | neighbors=[TestUdpRetransmit]
- "tests_test_adaptive_rate_testudpretransmit_test_returns_immediately_on_reply": ".test_returns_immediately_on_reply()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L120 | neighbors=[TestUdpRetransmit]
- "tests_test_adaptive_rate_testudpscanneradaptive_test_adaptive_scanner_creates_controller": ".test_adaptive_scanner_creates_controller()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L186 | neighbors=[TestUdpScannerAdaptive]
- "tests_test_adaptive_rate_testudpscanneradaptive_test_adaptive_scanner_detects_open_on_loopback": ".test_adaptive_scanner_detects_open_on_loopback()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L198 | neighbors=[TestUdpScannerAdaptive]
- "tests_test_adaptive_rate_testudpscanneradaptive_test_non_adaptive_scanner_has_no_controller": ".test_non_adaptive_scanner_has_no_controller()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L192 | neighbors=[TestUdpScannerAdaptive]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-150.json

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
