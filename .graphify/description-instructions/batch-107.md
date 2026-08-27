# Node Description Batch 108 of 236

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

- "services_remediation_kb_text": "_text()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L45 | neighbors=[remediation_kb.py, classify_finding()]
- "services_scope_crypto_public_key_from_b64": "public_key_from_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L85 | neighbors=[scope_crypto.py, Decode a base64-encoded X25519 public k…]
- "services_scope_targets_parse_networks": "_parse_networks()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L28 | neighbors=[scope_targets.py, validate_targets_in_scope()]
- "status_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L15 | neighbors=[route.ts, readiness()]
- "status_route_readiness": "readiness()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L10 | neighbors=[route.ts, GET()]
- "tests_conftest": "conftest.py" | kind=code-symbol | source=probe/tests/conftest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "tests_init": "__init__.py" | kind=code-symbol | source=manager/backend/tests/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
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
- "tests_test_agent_identity_test_cached_identity_refreshes_current_capabilities": "test_cached_identity_refreshes_current_capabilities()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L42 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_identity_test_cached_identity_retries_transient_refresh_failure": "test_cached_identity_retries_transient_refresh_failure()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L69 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_identity_test_rejected_cached_token_falls_back_to_idempotent_registration": "test_rejected_cached_token_falls_back_to_idempotent_registration()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L92 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_policy_testevaluateaction_test_decision_carries_action_and_tier": ".test_decision_carries_action_and_tier()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L94 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_denylisted_module_denied": ".test_denylisted_module_denied()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L68 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_excluded_target_denied": ".test_excluded_target_denied()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L63 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_exploit_attempt_cap_denied": ".test_exploit_attempt_cap_denied()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L77 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_halted_engagement_denies_everything": ".test_halted_engagement_denies_everything()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L73 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_host_cap_denied": ".test_host_cap_denied()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L83 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_intrusive_above_ceiling_needs_approval": ".test_intrusive_above_ceiling_needs_approval()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L45 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_intrusive_auto_when_ceiling_raised": ".test_intrusive_auto_when_ceiling_raised()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L49 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_irreversible_always_needs_approval_even_with_max_ceiling": ".test_irreversible_always_needs_approval_even_with_max_ceiling()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L54 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_no_targets_skips_scope_check": ".test_no_targets_skips_scope_check()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L89 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_passive_action_auto_authorized": ".test_passive_action_auto_authorized()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L37 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_reversible_within_default_ceiling_auto": ".test_reversible_within_default_ceiling_auto()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L41 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agent_policy_testevaluateaction_test_target_out_of_scope_denied": ".test_target_out_of_scope_denied()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L59 | neighbors=[TestEvaluateAction, _roe()]
- "tests_test_agents_rationale_1": "Unit tests for the agent/probe protocol changes:   * agent polling is restricted" | kind=entity | source=manager/backend/tests/test_agents.py:L1 | neighbors=[test_agents.py, ScanJobType]
- "tests_test_agents_rationale_207": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L207 | neighbors=[ScanJobType, .test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_242": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L242 | neighbors=[ScanJobType, .test_agent_token_is_long_lived()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-107.json

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
