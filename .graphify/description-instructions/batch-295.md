# Node Description Batch 296 of 332

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

- "tests_test_portal_assistant_runtime": "_Runtime" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L80 | neighbors=[test_portal_assistant.py]
- "tests_test_portal_assistant_test_the_task_rules_confine_the_model_to_security": "test_the_task_rules_confine_the_model_to_security()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L176 | neighbors=[test_portal_assistant.py]
- "tests_test_portal_assistant_testbounds_test_accepts_a_normal_exchange": ".test_accepts_a_normal_exchange()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L210 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_last_message_must_be_the_user": ".test_last_message_must_be_the_user()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L206 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_an_empty_conversation": ".test_rejects_an_empty_conversation()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L188 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_an_oversized_conversation": ".test_rejects_an_oversized_conversation()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L196 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_an_oversized_turn": ".test_rejects_an_oversized_turn()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L192 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_too_many_turns": ".test_rejects_too_many_turns()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L201 | neighbors=[TestBounds]
- "tests_test_portal_metrics_rationale_1": "test_portal_metrics.py — pure dashboard aggregations." | kind=entity | source=manager/backend/tests/test_portal_metrics.py:L1 | neighbors=[test_portal_metrics.py]
- "tests_test_portal_metrics_testseveritybreakdown_test_all_buckets_present_zero_filled": ".test_all_buckets_present_zero_filled()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L20 | neighbors=[TestSeverityBreakdown]
- "tests_test_portal_metrics_teststatustimeline_test_emits_continuous_zero_filled_months": ".test_emits_continuous_zero_filled_months()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L42 | neighbors=[TestStatusTimeline]
- "tests_test_portal_read_rationale_1": "test_portal_read.py — Phase 2: the customer-facing read API. Verifies the two da" | kind=entity | source=manager/backend/tests/test_portal_read.py:L1 | neighbors=[test_portal_read.py]
- "tests_test_portal_read_rationale_153": "Each db.execute(...) → result whose .scalars().first() is the next value;     pl" | kind=entity | source=manager/backend/tests/test_portal_read.py:L153 | neighbors=[_db_first()]
- "tests_test_portal_read_rationale_217": "Mock the create_scan_request db flow: execute#1 → engagement lookup     (.scalar" | kind=entity | source=manager/backend/tests/test_portal_read.py:L217 | neighbors=[_db_for_create()]
- "tests_test_portal_read_rationale_36": "Each db.execute(...) → result whose .scalars().all() is the next list." | kind=entity | source=manager/backend/tests/test_portal_read.py:L36 | neighbors=[_db_list()]
- "tests_test_portal_read_rationale_59": "A finding-like ORM object carrying BOTH whitelisted and internal fields." | kind=entity | source=manager/backend/tests/test_portal_read.py:L59 | neighbors=[_finding_with_internal()]
- "tests_test_portal_read_testclientfindingwhitelist_test_schema_is_a_whitelist": ".test_schema_is_a_whitelist()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L83 | neighbors=[TestClientFindingWhitelist]
- "tests_test_portal_remediation_rationale_1": "test_portal_remediation.py — Section 6: the customer-facing remediation route." | kind=entity | source=manager/backend/tests/test_portal_remediation.py:L1 | neighbors=[test_portal_remediation.py]
- "tests_test_portal_remediation_rationale_33": "Each db.execute(...) → result whose .scalar_one_or_none() is the next val." | kind=entity | source=manager/backend/tests/test_portal_remediation.py:L33 | neighbors=[_db_scalar()]
- "tests_test_portal_scope_rationale_1": "test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping au" | kind=entity | source=manager/backend/tests/test_portal_scope.py:L1 | neighbors=[test_portal_scope.py]
- "tests_test_portal_scope_testassertclient_test_client_without_engagement_is_forbidden": ".test_client_without_engagement_is_forbidden()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L47 | neighbors=[TestAssertClient]
- "tests_test_portal_scope_testportaltokenclaims_test_client_role_enum_exists": ".test_client_role_enum_exists()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L99 | neighbors=[TestPortalTokenClaims]
- "tests_test_portal_scope_testportaltokenclaims_test_client_token_carries_portal_aud_and_engagement": ".test_client_token_carries_portal_aud_and_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L85 | neighbors=[TestPortalTokenClaims]
- "tests_test_portal_scope_testportaltokenclaims_test_operator_and_portal_audiences_differ": ".test_operator_and_portal_audiences_differ()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L96 | neighbors=[TestPortalTokenClaims]
- "tests_test_posture_confidence_rationale_1": "test_posture_confidence.py — calibrated, auditable posture confidence with cross" | kind=entity | source=manager/detection_engine/tests/test_posture_confidence.py:L1 | neighbors=[test_posture_confidence.py]
- "tests_test_posture_confidence_testassessor_test_deception_penalty": ".test_deception_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L60 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_final_is_clamped_and_recorded": ".test_final_is_clamped_and_recorded()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L66 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_lone_chain_member_gets_no_floor": ".test_lone_chain_member_gets_no_floor()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L52 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_unreachable_downgrades_and_is_recorded": ".test_unreachable_downgrades_and_is_recorded()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L46 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_validated_base_higher_than_unvalidated": ".test_validated_base_higher_than_unvalidated()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L39 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testchains_test_chain_floor_never_lowers_confidence": ".test_chain_floor_never_lowers_confidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L82 | neighbors=[TestChains]
- "tests_test_posture_confidence_testchains_test_ntlm_relay_chain_floors_both": ".test_ntlm_relay_chain_floors_both()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L74 | neighbors=[TestChains]
- "tests_test_posture_row_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L110 | neighbors=[_Row]
- "tests_test_posture_rules_rationale_1": "test_posture_rules.py — the manager posture/config detection engine.  Covers: th" | kind=entity | source=manager/detection_engine/tests/test_posture_rules.py:L1 | neighbors=[test_posture_rules.py]
- "tests_test_posture_rules_rationale_96": "The live tls_scanner labels its probe list \"TLSv1_0\"/\"TLSv1_1\" (from         ssl" | kind=entity | source=manager/detection_engine/tests/test_posture_rules.py:L96 | neighbors=[.test_deprecated_tls_version_underscore…]
- "tests_test_posture_rules_testriskmodel_test_auth_enforced_deescalates": ".test_auth_enforced_deescalates()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L133 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testriskmodel_test_internet_facing_unauth_escalates": ".test_internet_facing_unauth_escalates()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L138 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testriskmodel_test_priority_buckets": ".test_priority_buckets()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L148 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testriskmodel_test_suspected_scores_below_confirmed": ".test_suspected_scores_below_confirmed()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L143 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testtrusttier_test_registry_contains_user_validated_set": ".test_registry_contains_user_validated_set()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L43 | neighbors=[TestTrustTier]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-295.json

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
