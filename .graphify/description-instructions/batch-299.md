# Node Description Batch 300 of 336

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

- "tests_test_pipeline_rationale_325": "With use_ai_assist=False (the default) and no ai_client, the pipeline         pr" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L325 | neighbors=[.test_ai_assist_off_by_default()] | lang=en
- "tests_test_pipeline_rationale_336": "ab_evaluate must return a dict with the expected structure." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L336 | neighbors=[.test_ab_evaluate_returns_expected_keys…] | lang=en
- "tests_test_pipeline_rationale_348": "When FakeAIClient returns nothing new, there must be no precision         regres" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L348 | neighbors=[.test_ab_evaluate_no_precision_regressi…] | lang=en
- "tests_test_pipeline_rationale_50": "Returns a VulnDB with a record that matches openssh 8.4p1 (vulnerable).      The" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L50 | neighbors=[_openssh_vuln_db()] | lang=en
- "tests_test_pipeline_rationale_74": "Upstream boundary for a banner-vs-inventory suppression scenario." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L74 | neighbors=[_openssh_upstream_vuln_db()] | lang=en
- "tests_test_port_catalog_test_modern_infra_ports_present": "test_modern_infra_ports_present()" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L4 | neighbors=[test_port_catalog.py] | lang=en
- "tests_test_portal_assistant_rationale_1": "test_portal_assistant.py — the customer-facing AI assistant.  Free-form chat was" | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L1 | neighbors=[test_portal_assistant.py] | lang=en
- "tests_test_portal_assistant_rationale_114": "The schema has no context field, so a client cannot inject its own     'evidence" | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L114 | neighbors=[test_request_body_cannot_carry_context()] | lang=en
- "tests_test_portal_assistant_rationale_120": "Internal triage/evidence fields must never leave the operator side." | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L120 | neighbors=[test_only_the_whitelisted_finding_field…] | lang=en
- "tests_test_portal_assistant_rationale_136": "403 would confirm the id exists somewhere — a cross-tenant oracle." | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L136 | neighbors=[test_focus_finding_outside_the_engageme…] | lang=en
- "tests_test_portal_assistant_rationale_61": "execute() → engagement, then findings, then (optionally) the focus finding." | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L61 | neighbors=[_db()] | lang=en
- "tests_test_portal_assistant_runtime": "_Runtime" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L80 | neighbors=[test_portal_assistant.py] | lang=en
- "tests_test_portal_assistant_test_the_task_rules_confine_the_model_to_security": "test_the_task_rules_confine_the_model_to_security()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L176 | neighbors=[test_portal_assistant.py] | lang=en
- "tests_test_portal_assistant_testbounds_test_accepts_a_normal_exchange": ".test_accepts_a_normal_exchange()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L210 | neighbors=[TestBounds] | lang=en
- "tests_test_portal_assistant_testbounds_test_last_message_must_be_the_user": ".test_last_message_must_be_the_user()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L206 | neighbors=[TestBounds] | lang=en
- "tests_test_portal_assistant_testbounds_test_rejects_an_empty_conversation": ".test_rejects_an_empty_conversation()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L188 | neighbors=[TestBounds] | lang=en
- "tests_test_portal_assistant_testbounds_test_rejects_an_oversized_conversation": ".test_rejects_an_oversized_conversation()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L196 | neighbors=[TestBounds] | lang=en
- "tests_test_portal_assistant_testbounds_test_rejects_an_oversized_turn": ".test_rejects_an_oversized_turn()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L192 | neighbors=[TestBounds] | lang=en
- "tests_test_portal_assistant_testbounds_test_rejects_too_many_turns": ".test_rejects_too_many_turns()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L201 | neighbors=[TestBounds] | lang=en
- "tests_test_portal_metrics_rationale_1": "test_portal_metrics.py — pure dashboard aggregations." | kind=entity | source=manager/backend/tests/test_portal_metrics.py:L1 | neighbors=[test_portal_metrics.py] | lang=en
- "tests_test_portal_metrics_testseveritybreakdown_test_all_buckets_present_zero_filled": ".test_all_buckets_present_zero_filled()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L20 | neighbors=[TestSeverityBreakdown] | lang=en
- "tests_test_portal_metrics_teststatustimeline_test_emits_continuous_zero_filled_months": ".test_emits_continuous_zero_filled_months()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L42 | neighbors=[TestStatusTimeline] | lang=en
- "tests_test_portal_read_rationale_1": "test_portal_read.py — Phase 2: the customer-facing read API. Verifies the two da" | kind=entity | source=manager/backend/tests/test_portal_read.py:L1 | neighbors=[test_portal_read.py] | lang=en
- "tests_test_portal_read_rationale_153": "Each db.execute(...) → result whose .scalars().first() is the next value;     pl" | kind=entity | source=manager/backend/tests/test_portal_read.py:L153 | neighbors=[_db_first()] | lang=en
- "tests_test_portal_read_rationale_217": "Mock the create_scan_request db flow: execute#1 → engagement lookup     (.scalar" | kind=entity | source=manager/backend/tests/test_portal_read.py:L217 | neighbors=[_db_for_create()] | lang=en
- "tests_test_portal_read_rationale_36": "Each db.execute(...) → result whose .scalars().all() is the next list." | kind=entity | source=manager/backend/tests/test_portal_read.py:L36 | neighbors=[_db_list()] | lang=en
- "tests_test_portal_read_rationale_59": "A finding-like ORM object carrying BOTH whitelisted and internal fields." | kind=entity | source=manager/backend/tests/test_portal_read.py:L59 | neighbors=[_finding_with_internal()] | lang=en
- "tests_test_portal_read_testclientfindingwhitelist_test_schema_is_a_whitelist": ".test_schema_is_a_whitelist()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L83 | neighbors=[TestClientFindingWhitelist] | lang=en
- "tests_test_portal_remediation_rationale_1": "test_portal_remediation.py — Section 6: the customer-facing remediation route." | kind=entity | source=manager/backend/tests/test_portal_remediation.py:L1 | neighbors=[test_portal_remediation.py] | lang=en
- "tests_test_portal_remediation_rationale_33": "Each db.execute(...) → result whose .scalar_one_or_none() is the next val." | kind=entity | source=manager/backend/tests/test_portal_remediation.py:L33 | neighbors=[_db_scalar()] | lang=en
- "tests_test_portal_scope_rationale_1": "test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping au" | kind=entity | source=manager/backend/tests/test_portal_scope.py:L1 | neighbors=[test_portal_scope.py] | lang=en
- "tests_test_portal_scope_rationale_108": "`jwt.py` states the portal audience exists \"so it can be rejected on     operato" | kind=entity | source=manager/backend/tests/test_portal_scope.py:L108 | neighbors=[TestPortalTokenIsConfinedToPortalRoutes] | lang=en
- "tests_test_portal_scope_rationale_134": "`/portal` must not authorize `/portalsomething` or a crafted path." | kind=entity | source=manager/backend/tests/test_portal_scope.py:L134 | neighbors=[.test_prefix_lookalikes_do_not_slip_thr…] | lang=pt
- "tests_test_portal_scope_rationale_141": "`/auth/refresh` must re-mint the SAME credential class the login issued.      Lo" | kind=entity | source=manager/backend/tests/test_portal_scope.py:L141 | neighbors=[TestRefreshPreservesAudienceAndScope] | lang=en
- "tests_test_portal_scope_rationale_187": "Same rule as login: never mint an unscoped client token." | kind=entity | source=manager/backend/tests/test_portal_scope.py:L187 | neighbors=[.test_unbound_client_cannot_refresh_int…] | lang=en
- "tests_test_portal_scope_testassertclient_test_client_without_engagement_is_forbidden": ".test_client_without_engagement_is_forbidden()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L51 | neighbors=[TestAssertClient] | lang=en
- "tests_test_portal_scope_testportaltokenclaims_test_client_role_enum_exists": ".test_client_role_enum_exists()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L103 | neighbors=[TestPortalTokenClaims] | lang=en
- "tests_test_portal_scope_testportaltokenclaims_test_client_token_carries_portal_aud_and_engagement": ".test_client_token_carries_portal_aud_and_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L89 | neighbors=[TestPortalTokenClaims] | lang=en
- "tests_test_portal_scope_testportaltokenclaims_test_operator_and_portal_audiences_differ": ".test_operator_and_portal_audiences_differ()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L100 | neighbors=[TestPortalTokenClaims] | lang=en
- "tests_test_portal_scope_testportaltokenisconfinedtoportalroutes_test_auth_routes_are_allowed": ".test_auth_routes_are_allowed()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L119 | neighbors=[TestPortalTokenIsConfinedToPortalRoutes] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-299.json

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
