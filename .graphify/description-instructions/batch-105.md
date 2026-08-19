# Node Description Batch 106 of 227

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
- "tests_test_agents_rationale_260": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L260 | neighbors=[ScanJobType, TestPromoteAssets]
- "tests_test_agents_rationale_288": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L288 | neighbors=[ScanJobType, .test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_rationale_530": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L530 | neighbors=[ScanJobType, .test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_565": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L565 | neighbors=[ScanJobType, .test_agent_token_is_long_lived()]
- "tests_test_agents_rationale_583": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L583 | neighbors=[ScanJobType, TestPromoteAssets]
- "tests_test_agents_rationale_611": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L611 | neighbors=[ScanJobType, .test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_testenqueueagentjob_test_404_when_engagement_missing": ".test_404_when_engagement_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L53 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_materializes_direct_job_capability_for_probe": ".test_materializes_direct_job_capability_for_probe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L93 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_rejects_server_side_type": ".test_rejects_server_side_type()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L46 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_scope_fields_cannot_override_engagement_scope": ".test_scope_fields_cannot_override_engagement_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L121 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_success_creates_pending_job": ".test_success_creates_pending_job()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L62 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L574 | neighbors=[test_agents.py, .test_online_heartbeat_clears_completed…]
- "tests_test_agents_testlegacybootstrap": "TestLegacyBootstrap" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L610 | neighbors=[test_agents.py, .test_shared_secret_bootstrap_is_disabl…]
- "tests_test_agents_testlistagents_test_fresh_disconnected_agent_is_not_reported_online": ".test_fresh_disconnected_agent_is_not_reported_online()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L551 | neighbors=[TestListAgents, _user()]
- "tests_test_agents_testlistagents_test_lists_with_online_flag": ".test_lists_with_online_flag()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L529 | neighbors=[TestListAgents, _user()]
- "tests_test_agents_testotprofilegate_test_allows_passive_discovery_on_ot_engagement": ".test_allows_passive_discovery_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L197 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_blocks_active_scan_type_on_ot_engagement": ".test_blocks_active_scan_type_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L165 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_blocks_explicit_active_scan_type_override_on_ot_engagement": ".test_blocks_explicit_active_scan_type_override_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L180 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_it_and_iot_profiles_unaffected": ".test_it_and_iot_profiles_unaffected()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L213 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testregisteragent_test_creates_when_none_exists": ".test_creates_when_none_exists()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L663 | neighbors=[TestRegisterAgent, _user()]
- "tests_test_ai_normalizer_testextractrawtext_test_db_scan_with_engine_and_version": ".test_db_scan_with_engine_and_version()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L85 | neighbors=[TestExtractRawText, _fact()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-105.json

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
