# Node Description Batch 146 of 332

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

- "settings_page_integrationsection": "IntegrationSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L570 | neighbors=[page.tsx, inlineInput()]
- "status_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L15 | neighbors=[route.ts, readiness()]
- "status_route_readiness": "readiness()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L10 | neighbors=[route.ts, GET()]
- "supporting_research_evidence_store_coverage_summary": "coverage_summary()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L362 | neighbors=[evidence_store.py, What a customer should actually be show…]
- "supporting_research_evidence_store_naive_ip_identity": "naive_ip_identity()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L257 | neighbors=[evidence_store.py, The industry default, for comparison. I…]
- "supporting_research_evidence_store_record_observation": "record_observation()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L113 | neighbors=[evidence_store.py, _iso()]
- "supporting_research_test_evidence_store_smb_obs": "smb_obs()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L45 | neighbors=[test_evidence_store.py, build_fleet()]
- "supporting_research_test_evidence_store_testidentity_setup": ".setUp()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L96 | neighbors=[TestIdentity, build_fleet()]
- "supporting_research_test_evidence_store_testidentity_test_hostname_never_overrides_a_fingerprint": ".test_hostname_never_overrides_a_fingerprint()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L119 | neighbors=[TestIdentity, ssh_obs()]
- "supporting_research_test_evidence_store_testidentity_test_ip_identity_is_wrong_in_both_directions": ".test_ip_identity_is_wrong_in_both_directions()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L104 | neighbors=[Not merely coarse -- wrong. It splits o…, TestIdentity]
- "supporting_research_test_evidence_store_testretroactivedetection_setup": ".setUp()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L141 | neighbors=[TestRetroactiveDetection, build_fleet()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_collected_but_unusable_evidence_is_distinguished_from_absent": ".test_collected_but_unusable_evidence_is_distinguished_from_absent()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L194 | neighbors=[Drifted payload: the probe ran, the fie…, TestRetroactiveDetection]
- "supporting_research_test_evidence_store_testretroactivedetection_test_remediation_is_verified_by_evidence_not_by_a_ticket": ".test_remediation_is_verified_by_evidence_not_by_a_ticket()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L162 | neighbors=[TestRetroactiveDetection, openssh_below()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_third_party_conclusions_are_kept_separate_from_first_party_evidence": ".test_third_party_conclusions_are_kept_separate_from_first_party_evidence()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L206 | neighbors=[TestRetroactiveDetection, ssh_obs()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_time_travel_recovers_the_historical_answer": ".test_time_travel_recovers_the_historical_answer()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L151 | neighbors=[TestRetroactiveDetection, openssh_below()]
- "tests_conftest_isolate_result_archive": "_isolate_result_archive()" | kind=code-symbol | source=probe/tests/conftest.py:L10 | neighbors=[conftest.py, Keep the local result archive out of th…]
- "tests_init": "__init__.py" | kind=code-symbol | source=manager/backend/tests/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_accuracy_gate_testcorpusvalidation_test_corpus_without_any_labels_is_rejected": ".test_corpus_without_any_labels_is_rejected()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L101 | neighbors=[TestCorpusValidation, _write()]
- "tests_test_accuracy_gate_testcorpusvalidation_test_corpus_without_facts_is_rejected": ".test_corpus_without_facts_is_rejected()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L107 | neighbors=[TestCorpusValidation, _write()]
- "tests_test_accuracy_gate_testcorpusvalidation_test_unknown_provenance_is_rejected": ".test_unknown_provenance_is_rejected()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L95 | neighbors=[TestCorpusValidation, _write()]
- "tests_test_accuracy_gate_testcorpusvalidation_test_unlabeled_provenance_is_rejected": ".test_unlabeled_provenance_is_rejected()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L90 | neighbors=[TestCorpusValidation, _write()]
- "tests_test_accuracy_gate_testshippedcorpora_test_an_independently_labeled_corpus_is_committed": ".test_an_independently_labeled_corpus_is_committed()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L57 | neighbors=[Without one of these the gate proves on…, TestShippedCorpora]
- "tests_test_accuracy_gate_testshippedcorpora_test_every_independent_corpus_scores_perfectly": ".test_every_independent_corpus_scores_perfectly()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L63 | neighbors=[Locks in the measured results: every po…, TestShippedCorpora]
- "tests_test_accuracy_gate_testshippedcorpora_test_gate_passes_on_the_committed_corpora": ".test_gate_passes_on_the_committed_corpora()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L43 | neighbors=[CI's actual assertion: the engine still…, TestShippedCorpora]
- "tests_test_active_validation_escalation_test_confirmed_authoritative_does_not_escalate": "test_confirmed_authoritative_does_not_escalate()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L21 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_high_severity_suspected_escalates_when_roe_allows": "test_high_severity_suspected_escalates_when_roe_allows()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L13 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_kev_escalates_even_if_medium": "test_kev_escalates_even_if_medium()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L17 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_low_severity_non_kev_does_not_escalate": "test_low_severity_non_kev_does_not_escalate()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L34 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_ot_profile_never_escalates": "test_ot_profile_never_escalates()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L30 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_roe_forbids_blocks_escalation": "test_roe_forbids_blocks_escalation()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L26 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_ad_assessment_fakeentry_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L41 | neighbors=[_FakeEntry, _FakeAttr]
- "tests_test_ad_assessment_testkerberoastchecker_ldap_with_users": "._ldap_with_users()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L173 | neighbors=[TestKerberoastChecker, .test_get_spn_accounts_filters_krbtgt_a…]
- "tests_test_ad_assessment_testkerberoastchecker_test_get_spn_accounts_filters_krbtgt_and_no_spn": ".test_get_spn_accounts_filters_krbtgt_and_no_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L179 | neighbors=[TestKerberoastChecker, ._ldap_with_users()]
- "tests_test_agent_auth_boundary_test_agent_jwt_is_blocked_before_human_route_handler": "test_agent_jwt_is_blocked_before_human_route_handler()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L58 | neighbors=[test_agent_auth_boundary.py, _boundary_test_client()]
- "tests_test_agent_auth_boundary_test_human_jwt_still_reaches_human_route_handler": "test_human_jwt_still_reaches_human_route_handler()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L69 | neighbors=[test_agent_auth_boundary.py, _boundary_test_client()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_claim_commits_before_confirmation": ".test_claim_commits_before_confirmation()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L223 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_incompatible_capability_is_never_claimed": ".test_incompatible_capability_is_never_claimed()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L251 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_lost_atomic_update_is_reported_as_unclaimed": ".test_lost_atomic_update_is_reported_as_unclaimed()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L275 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_identity_test_cached_identity_refreshes_current_capabilities": "test_cached_identity_refreshes_current_capabilities()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L46 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_identity_test_cached_identity_retries_transient_refresh_failure": "test_cached_identity_retries_transient_refresh_failure()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L73 | neighbors=[test_agent_identity.py, _cached_transport()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-145.json

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
