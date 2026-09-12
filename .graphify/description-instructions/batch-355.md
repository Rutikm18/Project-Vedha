# Node Description Batch 356 of 380

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

- "tests_test_seed_admin_testvalidateenv_test_allows_weak_password_in_development": ".test_allows_weak_password_in_development()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L51 | neighbors=[TestValidateEnv]
- "tests_test_seed_admin_testvalidateenv_test_raises_on_weak_password_in_production": ".test_raises_on_weak_password_in_production()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L44 | neighbors=[TestValidateEnv]
- "tests_test_seed_admin_testvalidateenv_test_raises_when_email_missing": ".test_raises_when_email_missing()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L39 | neighbors=[TestValidateEnv]
- "tests_test_seed_admin_testvalidateenv_test_returns_force_reset_true": ".test_returns_force_reset_true()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L58 | neighbors=[TestValidateEnv]
- "tests_test_self_scan_fakequeue_enqueue": ".enqueue()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L37 | neighbors=[FakeQueue]
- "tests_test_self_scan_fakequeue_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L36 | neighbors=[FakeQueue]
- "tests_test_self_scan_rationale_1": "Phase 5 — self-scan: own-IP-only, manager-less. Decision logic is pure; execute(" | kind=entity | source=probe/tests/test_self_scan.py:L1 | neighbors=[test_self_scan.py]
- "tests_test_self_scan_test_execute_refusal_returns_fatal_config_and_skips_engine": "test_execute_refusal_returns_fatal_config_and_skips_engine()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L57 | neighbors=[test_self_scan.py]
- "tests_test_self_scan_test_plan_allows_normal_own_ip_scoped_to_self": "test_plan_allows_normal_own_ip_scoped_to_self()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L9 | neighbors=[test_self_scan.py]
- "tests_test_self_scan_test_plan_refuses_denylisted_own_ip": "test_plan_refuses_denylisted_own_ip()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L29 | neighbors=[test_self_scan.py]
- "tests_test_self_scan_test_plan_refuses_inside_container": "test_plan_refuses_inside_container()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L19 | neighbors=[test_self_scan.py]
- "tests_test_self_scan_test_plan_refuses_without_an_ip": "test_plan_refuses_without_an_ip()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L24 | neighbors=[test_self_scan.py]
- "tests_test_service_banner_ident_rationale_1": "test_service_banner_ident.py — the service-identification upgrade.  Covers: the" | kind=entity | source=probe/tests/test_service_banner_ident.py:L1 | neighbors=[test_service_banner_ident.py]
- "tests_test_service_banner_ident_rationale_171": "A speak-first daemon that delays its 220 (reverse-DNS stall) must not be     rep" | kind=entity | source=probe/tests/test_service_banner_ident.py:L171 | neighbors=[test_slow_greeting_still_identifies()]
- "tests_test_service_banner_ident_rationale_217": "The banner and the match must come from the SAME rung (an earlier, longer     bu" | kind=entity | source=probe/tests/test_service_banner_ident.py:L217 | neighbors=[test_matched_rung_banner_is_the_one_rep…]
- "tests_test_service_banner_ident_rationale_274": "The HTTPS-on-9443 case: plaintext rungs see nothing useful, the TLS rung     com" | kind=entity | source=probe/tests/test_service_banner_ident.py:L274 | neighbors=[test_https_on_arbitrary_port_identifies…]
- "tests_test_service_banner_ident_serve": "_serve()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L165 | neighbors=[test_service_banner_ident.py]
- "tests_test_service_banner_ident_test_basic_auth_over_plaintext_is_recorded": "test_basic_auth_over_plaintext_is_recorded()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L314 | neighbors=[test_service_banner_ident.py]
- "tests_test_service_banner_ident_test_closed_port_yields_nothing": "test_closed_port_yields_nothing()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L236 | neighbors=[test_service_banner_ident.py]
- "tests_test_service_banner_ident_test_cpe_for_new_products": "test_cpe_for_new_products()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L95 | neighbors=[test_service_banner_ident.py]
- "tests_test_service_banner_ident_test_existing_matches_unchanged": "test_existing_matches_unchanged()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L87 | neighbors=[test_service_banner_ident.py]
- "tests_test_service_banner_ident_test_match_service_table": "test_match_service_table()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L79 | neighbors=[test_service_banner_ident.py]
- "tests_test_service_banner_ident_testladder_test_tls_rung_present_after_http": ".test_tls_rung_present_after_http()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L143 | neighbors=[TestLadder]
- "tests_test_service_banner_ident_testparsehttphead_test_bare_lf_headers": ".test_bare_lf_headers()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L123 | neighbors=[TestParseHttpHead]
- "tests_test_service_banner_ident_testparsehttphead_test_basic_auth_challenge": ".test_basic_auth_challenge()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L118 | neighbors=[TestParseHttpHead]
- "tests_test_service_banner_ident_testparsehttphead_test_non_http_is_empty": ".test_non_http_is_empty()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L128 | neighbors=[TestParseHttpHead]
- "tests_test_service_banner_ident_testparsehttphead_test_rtsp_is_http_shaped": ".test_rtsp_is_http_shaped()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L132 | neighbors=[TestParseHttpHead]
- "tests_test_service_banner_ident_testparsehttphead_test_status_server_title": ".test_status_server_title()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L109 | neighbors=[TestParseHttpHead]
- "tests_test_service_identifier_testserviceidentifier_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L7 | neighbors=[TestServiceIdentifier]
- "tests_test_service_match_rationale_1": "test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi" | kind=entity | source=probe/tests/test_service_match.py:L1 | neighbors=[test_service_match.py]
- "tests_test_service_match_testhttpmatch_test_apache_version": ".test_apache_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L42 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_iis_version": ".test_iis_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L47 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_version": ".test_nginx_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L36 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_without_version": ".test_nginx_without_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L52 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testnomatch_test_empty_returns_none": ".test_empty_returns_none()" | kind=code-symbol | source=probe/tests/test_service_match.py:L91 | neighbors=[TestNoMatch]
- "tests_test_service_match_testnomatch_test_unrecognized_returns_none": ".test_unrecognized_returns_none()" | kind=code-symbol | source=probe/tests/test_service_match.py:L88 | neighbors=[TestNoMatch]
- "tests_test_service_match_testotherservices_test_mariadb_handshake": ".test_mariadb_handshake()" | kind=code-symbol | source=probe/tests/test_service_match.py:L70 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_info": ".test_redis_info()" | kind=code-symbol | source=probe/tests/test_service_match.py:L77 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_noauth": ".test_redis_noauth()" | kind=code-symbol | source=probe/tests/test_service_match.py:L82 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_smtp_postfix": ".test_smtp_postfix()" | kind=code-symbol | source=probe/tests/test_service_match.py:L65 | neighbors=[TestOtherServices]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-355.json

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
