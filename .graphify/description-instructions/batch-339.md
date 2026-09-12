# Node Description Batch 340 of 380

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

- "tests_test_pipeline_rationale_281": "With use_ai_assist=False (the default) and no ai_client, the pipeline         pr" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L281 | neighbors=[.test_ai_assist_off_by_default()]
- "tests_test_pipeline_rationale_291": "The same (asset, CVE) can't appear twice in the output — dedup         must coll" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L291 | neighbors=[.test_findings_deduped_within_same_host…]
- "tests_test_pipeline_rationale_292": "ab_evaluate must return a dict with the expected structure." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L292 | neighbors=[.test_ab_evaluate_returns_expected_keys…]
- "tests_test_pipeline_rationale_304": "When FakeAIClient returns nothing new, there must be no precision         regres" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L304 | neighbors=[.test_ab_evaluate_no_precision_regressi…]
- "tests_test_pipeline_rationale_325": "With use_ai_assist=False (the default) and no ai_client, the pipeline         pr" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L325 | neighbors=[.test_ai_assist_off_by_default()]
- "tests_test_pipeline_rationale_336": "ab_evaluate must return a dict with the expected structure." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L336 | neighbors=[.test_ab_evaluate_returns_expected_keys…]
- "tests_test_pipeline_rationale_348": "When FakeAIClient returns nothing new, there must be no precision         regres" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L348 | neighbors=[.test_ab_evaluate_no_precision_regressi…]
- "tests_test_pipeline_rationale_50": "Returns a VulnDB with a record that matches openssh 8.4p1 (vulnerable).      The" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L50 | neighbors=[_openssh_vuln_db()]
- "tests_test_pipeline_rationale_74": "Upstream boundary for a banner-vs-inventory suppression scenario." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L74 | neighbors=[_openssh_upstream_vuln_db()]
- "tests_test_port_catalog_test_modern_infra_ports_present": "test_modern_infra_ports_present()" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L4 | neighbors=[test_port_catalog.py]
- "tests_test_port_scan_budget_rationale_1": "Per-host wall-clock budget with honest partial results.  \"No checkpointing or ch" | kind=entity | source=probe/tests/test_port_scan_budget.py:L1 | neighbors=[test_port_scan_budget.py]
- "tests_test_port_scan_budget_rationale_107": "Consumers can branch on it without a key check." | kind=entity | source=probe/tests/test_port_scan_budget.py:L107 | neighbors=[.test_budget_flag_is_always_present()]
- "tests_test_port_scan_budget_rationale_53": "Every requested port is accounted for as either attempted or         not-scanned" | kind=entity | source=probe/tests/test_port_scan_budget.py:L53 | neighbors=[.test_accounting_stays_honest_when_cut_…]
- "tests_test_port_scan_budget_rationale_66": "The core honesty property: running out of clock is not evidence of a         fir" | kind=entity | source=probe/tests/test_port_scan_budget.py:L66 | neighbors=[.test_unscanned_ports_are_not_reported_…]
- "tests_test_port_scan_budget_rationale_94": "A budget that is never reached must behave exactly like no budget." | kind=entity | source=probe/tests/test_port_scan_budget.py:L94 | neighbors=[.test_generous_budget_does_not_interfer…]
- "tests_test_port_scan_host_isolation_rationale_1": "Congestion state must belong to ONE host, even when one scanner object scans sev" | kind=entity | source=probe/tests/test_port_scan_host_isolation.py:L1 | neighbors=[test_port_scan_host_isolation.py]
- "tests_test_port_scan_host_isolation_rationale_45": "One scanner object, two hosts in flight — exactly what the port stage does." | kind=entity | source=probe/tests/test_port_scan_host_isolation.py:L45 | neighbors=[_run_both_hosts_concurrently()]
- "tests_test_port_scan_host_isolation_rationale_82": "The safety property. Isolating the state must not disable it." | kind=entity | source=probe/tests/test_port_scan_host_isolation.py:L82 | neighbors=[.test_a_genuinely_silent_host_still_bac…]
- "tests_test_port_scan_host_isolation_rationale_89": "Isolation must not cost coverage." | kind=entity | source=probe/tests/test_port_scan_host_isolation.py:L89 | neighbors=[.test_every_port_is_still_classified_fo…]
- "tests_test_port_scan_result_retention_rationale_1": "A host's scan must not hold one result object per PORT.  `scan_target` filtered" | kind=entity | source=probe/tests/test_port_scan_result_retention.py:L1 | neighbors=[test_port_scan_result_retention.py]
- "tests_test_port_scan_result_retention_rationale_141": "The audit path deliberately keeps everything; retention must follow         the" | kind=entity | source=probe/tests/test_port_scan_result_retention.py:L141 | neighbors=[.test_report_closed_still_emits_every_p…]
- "tests_test_port_scan_result_retention_rationale_43": "Returns (attempt_fn, live_at_end) where live_at_end is filled in with the     nu" | kind=entity | source=probe/tests/test_port_scan_result_retention.py:L43 | neighbors=[_live_probe()]
- "tests_test_port_scan_result_retention_rationale_93": "Silence is the ONE state a re-probe can legitimately change, so it         must" | kind=entity | source=probe/tests/test_port_scan_result_retention.py:L93 | neighbors=[.test_ambiguous_results_are_still_retai…]
- "tests_test_portal_assistant_rationale_1": "test_portal_assistant.py — the customer-facing AI assistant.  Free-form chat was" | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L1 | neighbors=[test_portal_assistant.py]
- "tests_test_portal_assistant_rationale_114": "The schema has no context field, so a client cannot inject its own     'evidence" | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L114 | neighbors=[test_request_body_cannot_carry_context()]
- "tests_test_portal_assistant_rationale_120": "Internal triage/evidence fields must never leave the operator side." | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L120 | neighbors=[test_only_the_whitelisted_finding_field…]
- "tests_test_portal_assistant_rationale_136": "403 would confirm the id exists somewhere — a cross-tenant oracle." | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L136 | neighbors=[test_focus_finding_outside_the_engageme…]
- "tests_test_portal_assistant_rationale_61": "execute() → engagement, then findings, then (optionally) the focus finding." | kind=entity | source=manager/backend/tests/test_portal_assistant.py:L61 | neighbors=[_db()]
- "tests_test_portal_assistant_runtime": "_Runtime" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L80 | neighbors=[test_portal_assistant.py]
- "tests_test_portal_assistant_test_the_task_rules_confine_the_model_to_security": "test_the_task_rules_confine_the_model_to_security()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L176 | neighbors=[test_portal_assistant.py]
- "tests_test_portal_assistant_testbounds_test_accepts_a_normal_exchange": ".test_accepts_a_normal_exchange()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L210 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_last_message_must_be_the_user": ".test_last_message_must_be_the_user()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L206 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_an_empty_conversation": ".test_rejects_an_empty_conversation()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L188 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_an_oversized_conversation": ".test_rejects_an_oversized_conversation()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L196 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_an_oversized_turn": ".test_rejects_an_oversized_turn()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L192 | neighbors=[TestBounds]
- "tests_test_portal_assistant_testbounds_test_rejects_too_many_turns": ".test_rejects_too_many_turns()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L201 | neighbors=[TestBounds]
- "tests_test_portal_finding_actions_test_workspace_list_serializes_through_the_manager_finding_contract": "test_workspace_list_serializes_through_the_manager_finding_contract()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L62 | neighbors=[test_portal_finding_actions.py]
- "tests_test_portal_metrics_rationale_1": "test_portal_metrics.py — pure dashboard aggregations." | kind=entity | source=manager/backend/tests/test_portal_metrics.py:L1 | neighbors=[test_portal_metrics.py]
- "tests_test_portal_metrics_testseveritybreakdown_test_all_buckets_present_zero_filled": ".test_all_buckets_present_zero_filled()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L20 | neighbors=[TestSeverityBreakdown]
- "tests_test_portal_metrics_teststatustimeline_test_emits_continuous_zero_filled_months": ".test_emits_continuous_zero_filled_months()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L42 | neighbors=[TestStatusTimeline]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-339.json

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
