# Node Description Batch 312 of 336

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
- "tests_test_scope_validator_testfetchengagementscope_test_returns_scope_from_http_get": ".test_returns_scope_from_http_get()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L171 | neighbors=[TestFetchEngagementScope]
- "tests_test_scope_validator_testmergeexclusions_test_both_empty": ".test_both_empty()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L161 | neighbors=[TestMergeExclusions]
- "tests_test_scope_validator_testmergeexclusions_test_empty_engagement_excludes": ".test_empty_engagement_excludes()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L157 | neighbors=[TestMergeExclusions]
- "tests_test_scope_validator_testmergeexclusions_test_empty_job_excludes": ".test_empty_job_excludes()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L149 | neighbors=[TestMergeExclusions]
- "tests_test_scope_validator_testmergeexclusions_test_merges_no_duplicates": ".test_merges_no_duplicates()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L145 | neighbors=[TestMergeExclusions]
- "tests_test_scope_validator_testmergeexclusions_test_none_job_excludes": ".test_none_job_excludes()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L153 | neighbors=[TestMergeExclusions]
- "tests_test_scope_validator_testmergeexclusions_test_strips_whitespace": ".test_strips_whitespace()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L165 | neighbors=[TestMergeExclusions]
- "tests_test_scope_validator_testtargetsinexcludes_test_all_excluded_returns_empty": ".test_all_excluded_returns_empty()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L136 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_drops_excluded_ip": ".test_drops_excluded_ip()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L94 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_drops_excluded_subnet": ".test_drops_excluded_subnet()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L101 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_fully_excluded_cidr_is_dropped": ".test_fully_excluded_cidr_is_dropped()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L129 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_hostname_passes_through": ".test_hostname_passes_through()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L115 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_no_excludes_returns_all": ".test_no_excludes_returns_all()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L108 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_port_suffix_is_not_treated_as_an_ip": ".test_port_suffix_is_not_treated_as_an_ip()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L122 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_port_suffix_stripped": ".test_port_suffix_stripped()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L91 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_cidr_must_be_fully_contained": ".test_cidr_must_be_fully_contained()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L62 | neighbors=[TestValidateTargetsInScope]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-311.json

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
