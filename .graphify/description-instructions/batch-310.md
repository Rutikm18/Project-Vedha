# Node Description Batch 311 of 380

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

- "tests_test_auth_surface_rationale_1": "Auth-surface observation — what login a web service ASKS for.  This is the probe" | kind=entity | source=probe/tests/test_auth_surface.py:L1 | neighbors=[test_auth_surface.py] | lang=en
- "tests_test_auth_surface_rationale_38": "web_scanner lowercases header keys; other callers may not." | kind=entity | source=probe/tests/test_auth_surface.py:L38 | neighbors=[.test_header_lookup_is_case_insensitive…] | lang=en
- "tests_test_auth_surface_rationale_68": "An explicit challenge is stronger evidence than a heuristic form match." | kind=entity | source=probe/tests/test_auth_surface.py:L68 | neighbors=[.test_challenge_wins_over_form()] | lang=en
- "tests_test_auth_surface_rationale_94": "A scanner must never crash on a response it didn't get." | kind=entity | source=probe/tests/test_auth_surface.py:L94 | neighbors=[.test_none_inputs_are_survivable()] | lang=pt
- "tests_test_auth_surface_rationale_99": "A huge body must not make vendor-hunting expensive." | kind=entity | source=probe/tests/test_auth_surface.py:L99 | neighbors=[.test_body_scan_is_bounded()] | lang=pt
- "tests_test_auth_surface_testauthchallenge_test_basic_realm_is_parsed": ".test_basic_realm_is_parsed()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L24 | neighbors=[TestAuthChallenge] | lang=en
- "tests_test_auth_surface_testauthchallenge_test_digest_realm_is_parsed": ".test_digest_realm_is_parsed()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L30 | neighbors=[TestAuthChallenge] | lang=en
- "tests_test_auth_surface_testauthchallenge_test_realm_absent_from_challenge": ".test_realm_absent_from_challenge()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L48 | neighbors=[TestAuthChallenge] | lang=en
- "tests_test_auth_surface_testauthchallenge_test_unknown_challenge_scheme_is_other_not_a_guess": ".test_unknown_challenge_scheme_is_other_not_a_guess()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L43 | neighbors=[TestAuthChallenge] | lang=en
- "tests_test_auth_surface_testloginform_test_ordinary_page_has_no_auth_surface": ".test_ordinary_page_has_no_auth_surface()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L62 | neighbors=[TestLoginForm] | lang=en
- "tests_test_auth_surface_testloginform_test_password_input_is_detected_as_a_form": ".test_password_input_is_detected_as_a_form()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L54 | neighbors=[TestLoginForm] | lang=en
- "tests_test_auth_surface_testloginform_test_single_quoted_password_input_is_detected": ".test_single_quoted_password_input_is_detected()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L58 | neighbors=[TestLoginForm] | lang=en
- "tests_test_auth_surface_testrobustness_test_empty_inputs_are_survivable": ".test_empty_inputs_are_survivable()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L89 | neighbors=[TestRobustness] | lang=en
- "tests_test_auth_surface_testvendorhint_test_unknown_vendor_is_none_not_a_guess": ".test_unknown_vendor_is_none_not_a_guess()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L83 | neighbors=[TestVendorHint] | lang=en
- "tests_test_auth_surface_testvendorhint_test_vendor_found_in_body": ".test_vendor_found_in_body()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L79 | neighbors=[TestVendorHint] | lang=en
- "tests_test_auth_surface_testvendorhint_test_vendor_found_in_realm": ".test_vendor_found_in_realm()" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L75 | neighbors=[TestVendorHint] | lang=en
- "tests_test_bootstrap_rationale_1": "Phase 7 — bootstrap logic: per-OS Python install command, and the optional stric" | kind=entity | source=probe/tests/test_bootstrap.py:L1 | neighbors=[test_bootstrap.py] | lang=en
- "tests_test_bootstrap_test_python_install_cmd_per_pm": "test_python_install_cmd_per_pm()" | kind=code-symbol | source=probe/tests/test_bootstrap.py:L11 | neighbors=[test_bootstrap.py] | lang=en
- "tests_test_bootstrap_test_security_mode_defaults_permissive_but_strict_available": "test_security_mode_defaults_permissive_but_strict_available()" | kind=code-symbol | source=probe/tests/test_bootstrap.py:L20 | neighbors=[test_bootstrap.py] | lang=en
- "tests_test_bootstrap_test_verify_download_match_is_ok_in_both_modes": "test_verify_download_match_is_ok_in_both_modes()" | kind=code-symbol | source=probe/tests/test_bootstrap.py:L28 | neighbors=[test_bootstrap.py] | lang=en
- "tests_test_bootstrap_test_verify_download_mismatch_fails_strict_but_warns_permissive": "test_verify_download_mismatch_fails_strict_but_warns_permissive()" | kind=code-symbol | source=probe/tests/test_bootstrap.py:L37 | neighbors=[test_bootstrap.py] | lang=en
- "tests_test_bootstrap_test_verify_download_missing_checksum_fails_strict_only": "test_verify_download_missing_checksum_fails_strict_only()" | kind=code-symbol | source=probe/tests/test_bootstrap.py:L45 | neighbors=[test_bootstrap.py] | lang=en
- "tests_test_branch_registry_rationale_1": "test_branch_registry.py — the deep-scan branch registry and the invariants it ex" | kind=entity | source=probe/tests/test_branch_registry.py:L1 | neighbors=[test_branch_registry.py] | lang=en
- "tests_test_branch_registry_rationale_113": "Before the registry, these five planned NOTHING while the engine ran five     co" | kind=entity | source=probe/tests/test_branch_registry.py:L113 | neighbors=[test_service_specific_plan_matches_what…] | lang=en
- "tests_test_branch_registry_rationale_143": "An SNMP-only job must not fall back to a broad TCP sweep." | kind=entity | source=probe/tests/test_branch_registry.py:L143 | neighbors=[test_datagram_branches_need_no_tcp_stag…] | lang=en
- "tests_test_branch_registry_rationale_158": "smb's fact describes the host, so it must be keyed by (host, None) — not     by" | kind=entity | source=probe/tests/test_branch_registry.py:L158 | neighbors=[test_host_level_branch_is_cached_under_…] | lang=en
- "tests_test_branch_registry_rationale_185": "The database branch is the one spec that runs its scanner twice: known     engin" | kind=entity | source=probe/tests/test_branch_registry.py:L185 | neighbors=[test_db_branch_splits_known_and_router_…] | lang=en
- "tests_test_branch_registry_rationale_205": "SNMPScanner's signature has no `ports`; passing one would TypeError." | kind=entity | source=probe/tests/test_branch_registry.py:L205 | neighbors=[test_snmp_scanner_is_constructed_withou…] | lang=en
- "tests_test_branch_registry_rationale_36": "A spec the profile tables don't know about could never run." | kind=entity | source=probe/tests/test_branch_registry.py:L36 | neighbors=[.test_every_branch_is_gateable()] | lang=en
- "tests_test_branch_registry_rationale_41": "gate_5 intersects open ports with its own table; the engine uses the         spe" | kind=entity | source=probe/tests/test_branch_registry.py:L41 | neighbors=[.test_port_tables_match_gates()] | lang=en
- "tests_test_branch_registry_rationale_66": "A fact whose scanner name has no merge handler is collected, cached,         shi" | kind=entity | source=probe/tests/test_branch_registry.py:L66 | neighbors=[.test_every_component_can_be_merged_int…] | lang=en
- "tests_test_branch_registry_rationale_72": "An unlisted scanner falls back to 'uncertain' (re-probed every pass).         Th" | kind=entity | source=probe/tests/test_branch_registry.py:L72 | neighbors=[.test_every_component_has_a_cache_certa…] | lang=en
- "tests_test_branch_registry_test_full_assessment_plans_every_branch": "test_full_assessment_plans_every_branch()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L132 | neighbors=[test_branch_registry.py] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_branch_component_map_is_derived": ".test_branch_component_map_is_derived()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L62 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_catalog_entries_are_labelled": ".test_catalog_entries_are_labelled()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L58 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_components_are_unique": ".test_components_are_unique()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L77 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_every_branch_has_a_scanner_the_engine_can_resolve": ".test_every_branch_has_a_scanner_the_engine_can_resolve()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L49 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_every_component_is_in_the_plan_catalog": ".test_every_component_is_in_the_plan_catalog()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L53 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_kwargs_builders_have_the_expected_signature": ".test_kwargs_builders_have_the_expected_signature()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L81 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_rule_coverage_rationale_1": "test_branch_rule_coverage.py — every deep branch must be ASSESSED, not just coll" | kind=entity | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L1 | neighbors=[test_branch_rule_coverage.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-310.json

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
