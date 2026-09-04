# Node Description Batch 268 of 330

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

- "tests_test_agents_testgetagentjobs_test_404_when_agent_unknown": ".test_404_when_agent_unknown()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L405 | neighbors=[TestGetAgentJobs] | lang=en
- "tests_test_agents_testgetagentjobs_test_jobs_include_params": ".test_jobs_include_params()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L301 | neighbors=[TestGetAgentJobs] | lang=en
- "tests_test_agents_testgetagentjobs_test_skips_job_outside_declared_network_segments": ".test_skips_job_outside_declared_network_segments()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L375 | neighbors=[TestGetAgentJobs] | lang=en
- "tests_test_agents_testgetagentjobs_test_skips_job_when_capability_is_missing": ".test_skips_job_when_capability_is_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L345 | neighbors=[TestGetAgentJobs] | lang=en
- "tests_test_agents_testheartbeat_test_online_heartbeat_clears_completed_job": ".test_online_heartbeat_clears_completed_job()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L585 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_agents_testlegacybootstrap_test_shared_secret_bootstrap_is_disabled_by_default": ".test_shared_secret_bootstrap_is_disabled_by_default()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L621 | neighbors=[TestLegacyBootstrap] | lang=en
- "tests_test_agents_testpromoteassets_test_creates_asset_and_services_with_cpe": ".test_creates_asset_and_services_with_cpe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L705 | neighbors=[TestPromoteAssets] | lang=en
- "tests_test_agents_testpromoteassets_test_empty_result_is_noop": ".test_empty_result_is_noop()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L762 | neighbors=[TestPromoteAssets] | lang=en
- "tests_test_agents_testpromoteassets_test_skips_host_without_ip": ".test_skips_host_without_ip()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L755 | neighbors=[TestPromoteAssets] | lang=en
- "tests_test_ai_engine_testhallucinationguard_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L106 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_cve_all_known_valid": ".test_cve_all_known_valid()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L117 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_cve_invention_flagged": ".test_cve_invention_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L109 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_cvss_match_passes": ".test_cvss_match_passes()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L126 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_cvss_mismatch_flagged": ".test_cvss_mismatch_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L121 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_destructive_command_flagged": ".test_destructive_command_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L130 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_drop_table_flagged": ".test_drop_table_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L135 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_safe_remediation_passes": ".test_safe_remediation_passes()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L139 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_validate_aggregate_confidence": ".test_validate_aggregate_confidence()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L143 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_validate_clean_text": ".test_validate_clean_text()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L152 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L49 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_fallback_score_capped": ".test_fallback_score_capped()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L88 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_starts_untrained": ".test_starts_untrained()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L52 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_train_without_xgboost_raises": ".test_train_without_xgboost_raises()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L92 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_normalizer_rationale_1": "Tests for ai_normalizer.py — 0% prior coverage.  Covers:   - extract_raw_text: p" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L1 | neighbors=[test_ai_normalizer.py] | lang=en
- "tests_test_ai_normalizer_rationale_155": "Any exception from the AI client yields [] — never raises, never         blocks" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L155 | neighbors=[.test_client_failure_returns_empty()] | lang=en
- "tests_test_ai_normalizer_rationale_168": "When the cache already has an answer, the client must not be called." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L168 | neighbors=[.test_cache_hit_bypasses_client()] | lang=en
- "tests_test_ai_normalizer_rationale_185": "A candidate dict without a 'product' key must be silently skipped." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L185 | neighbors=[.test_malformed_response_missing_produc…] | lang=pt
- "tests_test_ai_normalizer_rationale_194": "If the client returns something that isn't a list, return []." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L194 | neighbors=[.test_malformed_response_not_a_list_ret…] | lang=en
- "tests_test_ai_normalizer_rationale_206": "Every candidate produced by propose_candidates must be tagged         ai_assiste" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L206 | neighbors=[.test_ai_assisted_flag_set_on_candidate…] | lang=en
- "tests_test_ai_normalizer_rationale_219": "source_confidence on the resulting CPECandidate must match the         originati" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L219 | neighbors=[.test_source_confidence_propagated_from…] | lang=en
- "tests_test_ai_normalizer_rationale_231": "When the AI response includes a version, it lands on the candidate." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L231 | neighbors=[.test_version_propagated_when_present()] | lang=en
- "tests_test_ai_normalizer_rationale_243": "A candidate without a version key produces version_raw=None." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L243 | neighbors=[.test_version_none_when_absent()] | lang=pt
- "tests_test_ai_normalizer_rationale_253": "The result of a first successful client call must be stored in the         cache" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L253 | neighbors=[.test_result_is_cached_after_first_call…] | lang=en
- "tests_test_ai_normalizer_rationale_96": "ssh_inventory facts have no banner-style text for the AI to normalise." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L96 | neighbors=[.test_ssh_inventory_returns_none()] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_cache_persists_across_instances": ".test_cache_persists_across_instances()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L134 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_get_returns_none_on_miss": ".test_get_returns_none_on_miss()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L124 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_key_is_content_hash_not_plaintext": ".test_key_is_content_hash_not_plaintext()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L141 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_put_and_get_roundtrip": ".test_put_and_get_roundtrip()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L128 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testfakeaiclient_test_returns_empty_for_unknown_text": ".test_returns_empty_for_unknown_text()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L114 | neighbors=[TestFakeAIClient] | lang=en
- "tests_test_ai_normalizer_testfakeaiclient_test_returns_registered_response": ".test_returns_registered_response()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L110 | neighbors=[TestFakeAIClient] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-267.json

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
