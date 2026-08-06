# Node Description Batch 123 of 134

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

- "tests_test_router_db_test_mysql_greeting_on_odd_port": "test_mysql_greeting_on_odd_port()" | kind=code-symbol | source=probe/tests/test_router_db.py:L4 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_plain_http_is_not_db": "test_plain_http_is_not_db()" | kind=code-symbol | source=probe/tests/test_router_db.py:L13 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_redis_noauth_signature": "test_redis_noauth_signature()" | kind=code-symbol | source=probe/tests/test_router_db.py:L9 | neighbors=[test_router_db.py]
- "tests_test_runtime_topology_rationale_1": "Product-boundary tests for the single-dashboard Manager API." | kind=entity | source=manager/backend/tests/test_runtime_topology.py:L1 | neighbors=[test_runtime_topology.py]
- "tests_test_runtime_topology_test_manager_does_not_mount_a_static_dashboard": "test_manager_does_not_mount_a_static_dashboard()" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L6 | neighbors=[test_runtime_topology.py]
- "tests_test_runtime_topology_test_manager_root_is_service_metadata": "test_manager_root_is_service_metadata()" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L13 | neighbors=[test_runtime_topology.py]
- "tests_test_scope_crypt_rationale_1": "Tests for agent/scope_crypt.py" | kind=entity | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[test_scope_crypt.py]
- "tests_test_scope_crypt_rationale_79": "Each encryption uses a fresh ephemeral key, so blobs are different." | kind=entity | source=probe/tests/test_scope_crypt.py:L79 | neighbors=[.test_multiple_encrypts_different()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_b64_roundtrip": ".test_b64_roundtrip()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L70 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_plaintexts_are_distinct": ".test_different_plaintexts_are_distinct()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L64 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_recipient_cannot_decrypt": ".test_different_recipient_cannot_decrypt()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L43 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_empty_scope": ".test_roundtrip_empty_scope()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L36 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_plaintext": ".test_roundtrip_plaintext()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L29 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_tampered_blob": ".test_tampered_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L51 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_too_short_blob": ".test_too_short_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L59 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testkeygeneration_test_generates_32_byte_keys": ".test_generates_32_byte_keys()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L16 | neighbors=[TestKeyGeneration]
- "tests_test_scope_crypt_testkeygeneration_test_generates_different_keys_each_call": ".test_generates_different_keys_each_call()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L21 | neighbors=[TestKeyGeneration]
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
- "tests_test_scope_validator_testvalidatetargetsinscope_test_empty_targets": ".test_empty_targets()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L44 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_explicit_hostname_scope_allows_exact_hostname_only": ".test_explicit_hostname_scope_allows_exact_hostname_only()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L36 | neighbors=[TestValidateTargetsInScope]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-122.json

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
