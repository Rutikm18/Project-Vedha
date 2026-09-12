# Node Description Batch 354 of 380

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

- "tests_test_scope_model_test_classify_physical_default": "test_classify_physical_default()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L24 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_classify_tunnel": "test_classify_tunnel()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L14 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_denylist_allows_normal_private_ranges": "test_denylist_allows_normal_private_ranges()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L39 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_denylist_blocks_manager_address": "test_denylist_blocks_manager_address()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L43 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_denylist_blocks_special_ranges": "test_denylist_blocks_special_ranges()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L30 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_detect_container_signals": "test_detect_container_signals()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L87 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_ipv6_note_when_no_v4": "test_ipv6_note_when_no_v4()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L100 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_never_segment_must_be_inactive": "test_never_segment_must_be_inactive()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L58 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_ot_active_is_rejected_in_v1": "test_ot_active_is_rejected_in_v1()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L53 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_parse_linux_ip_json": "test_parse_linux_ip_json()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L106 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_refusal_reason_for_container": "test_refusal_reason_for_container()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L93 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_target_allowed_inside_it_segment": "test_target_allowed_inside_it_segment()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L73 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_target_in_ot_segment_is_refused": "test_target_in_ot_segment_is_refused()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L77 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_target_on_denylist_is_refused": "test_target_on_denylist_is_refused()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L81 | neighbors=[test_scope_model.py]
- "tests_test_scope_model_test_valid_it_segment_passes": "test_valid_it_segment_passes()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L49 | neighbors=[test_scope_model.py]
- "tests_test_scope_targets_rationale_1": "test_scope_targets.py — the pure scope-authorization core shared by the dispatch" | kind=entity | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[test_scope_targets.py]
- "tests_test_scope_targets_rationale_99": "Whatever the validator accepts must be provably inside the scope." | kind=entity | source=manager/backend/tests/test_scope_targets.py:L99 | neighbors=[test_property_every_accepted_target_is_…]
- "tests_test_scope_targets_testexclusions_test_target_clear_of_exclusions_is_allowed": ".test_target_clear_of_exclusions_is_allowed()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L82 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testexclusions_test_target_inside_an_exclusion_is_rejected": ".test_target_inside_an_exclusion_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L71 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testexclusions_test_target_overlapping_an_exclusion_is_rejected": ".test_target_overlapping_an_exclusion_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L76 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testipversionsafety_test_v6_in_v6_scope": ".test_v6_in_v6_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L92 | neighbors=[TestIpVersionSafety]
- "tests_test_scope_targets_testipversionsafety_test_v6_target_against_v4_scope_is_rejected": ".test_v6_target_against_v4_scope_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L89 | neighbors=[TestIpVersionSafety]
- "tests_test_scope_targets_testnoscopeauthorizesnothing_test_empty_scope_denies_all": ".test_empty_scope_denies_all()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L17 | neighbors=[TestNoScopeAuthorizesNothing]
- "tests_test_scope_targets_testoutofscopeisrejected_test_blank_token_is_rejected": ".test_blank_token_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L63 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_cidr_broader_than_scope": ".test_cidr_broader_than_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L48 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_explicit_empty_list_is_rejected": ".test_explicit_empty_list_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L57 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_hostname_is_not_routable": ".test_hostname_is_not_routable()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L60 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_ip_outside_scope": ".test_ip_outside_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L45 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_one_bad_target_rejects_the_whole_request": ".test_one_bad_target_rejects_the_whole_request()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L52 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_reversed_range_is_rejected": ".test_reversed_range_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L66 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testtargetswithinscope_test_cidr_subset_in_scope": ".test_cidr_subset_in_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L30 | neighbors=[TestTargetsWithinScope]
- "tests_test_scope_targets_testtargetswithinscope_test_no_targets_returns_whole_scope": ".test_no_targets_returns_whole_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L38 | neighbors=[TestTargetsWithinScope]
- "tests_test_scope_targets_testtargetswithinscope_test_range_expands_to_covered_networks": ".test_range_expands_to_covered_networks()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L33 | neighbors=[TestTargetsWithinScope]
- "tests_test_scope_targets_testtargetswithinscope_test_single_ip_in_scope": ".test_single_ip_in_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L24 | neighbors=[TestTargetsWithinScope]
- "tests_test_scope_targets_testtargetswithinscope_test_string_target_is_accepted": ".test_string_target_is_accepted()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L27 | neighbors=[TestTargetsWithinScope]
- "tests_test_scope_validator_rationale_1": "Tests for agent/scope_validator.py" | kind=entity | source=probe/tests/test_scope_validator.py:L1 | neighbors=[test_scope_validator.py]
- "tests_test_scope_validator_testfetchengagementscope_test_http_get_raises": ".test_http_get_raises()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L195 | neighbors=[TestFetchEngagementScope]
- "tests_test_scope_validator_testfetchengagementscope_test_http_get_returns_incomplete": ".test_http_get_returns_incomplete()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L203 | neighbors=[TestFetchEngagementScope]
- "tests_test_scope_validator_testfetchengagementscope_test_http_get_returns_none": ".test_http_get_returns_none()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L187 | neighbors=[TestFetchEngagementScope]
- "tests_test_scope_validator_testfetchengagementscope_test_returns_excludes": ".test_returns_excludes()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L180 | neighbors=[TestFetchEngagementScope]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-353.json

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
