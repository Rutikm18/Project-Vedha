# Node Description Batch 316 of 336

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

- "tests_test_ssh_scanner_testevaluate_test_arcfour_is_rc4_failure": ".test_arcfour_is_rc4_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L114 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_cbc_cipher_is_warning_not_failure": ".test_cbc_cipher_is_warning_not_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L108 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_group1_sha1_is_failure_with_modulus_and_sha1_reasons": ".test_group1_sha1_is_failure_with_modulus_and_sha1_reasons()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L99 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_hmac_md5_is_failure": ".test_hmac_md5_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L119 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_modern_set_is_clean": ".test_modern_set_is_clean()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L129 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_ssh_rsa_hostkey_is_sha1_failure": ".test_ssh_rsa_hostkey_is_sha1_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L124 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_unknown_algorithm_is_recorded_not_failed": ".test_unknown_algorithm_is_recorded_not_failed()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L135 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testfulldbcoverage_test_3des_ctr_cipher_is_failure": ".test_3des_ctr_cipher_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L252 | neighbors=[TestFullDBCoverage]
- "tests_test_ssh_scanner_testfulldbcoverage_test_gss_kex_offered_by_server_is_failure": ".test_gss_kex_offered_by_server_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L262 | neighbors=[TestFullDBCoverage]
- "tests_test_ssh_scanner_testfulldbcoverage_test_hmac_ripemd160_is_failure": ".test_hmac_ripemd160_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L257 | neighbors=[TestFullDBCoverage]
- "tests_test_ssh_scanner_testfulldbcoverage_test_rijndael_cbc_cipher_is_failure": ".test_rijndael_cbc_cipher_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L247 | neighbors=[TestFullDBCoverage]
- "tests_test_ssh_scanner_testmainscriptsparity_test_main_scripts_vendored_db_matches_scanner_tree": ".test_main_scripts_vendored_db_matches_scanner_tree()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L331 | neighbors=[TestMainScriptsParity]
- "tests_test_ssh_scanner_testnofalsepositives_test_ed25519_hostkey_is_clean": ".test_ed25519_hostkey_is_clean()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L283 | neighbors=[TestNoFalsePositives]
- "tests_test_ssh_scanner_testnofalsepositives_test_rsa_sha2_hostkeys_are_not_failures": ".test_rsa_sha2_hostkeys_are_not_failures()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L276 | neighbors=[TestNoFalsePositives]
- "tests_test_ssh_scanner_testparsebanner_test_dropbear_no_comments_from_bytes": ".test_dropbear_no_comments_from_bytes()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L58 | neighbors=[TestParseBanner]
- "tests_test_ssh_scanner_testparsebanner_test_openssh_with_comments": ".test_openssh_with_comments()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L52 | neighbors=[TestParseBanner]
- "tests_test_ssh_scanner_testparsebanner_test_rejects_non_ssh": ".test_rejects_non_ssh()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L63 | neighbors=[TestParseBanner]
- "tests_test_ssh_scanner_testsshscanner_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L165 | neighbors=[TestSSHScanner]
- "tests_test_ssh_scanner_testsshscanner_test_no_response_is_filtered": ".test_no_response_is_filtered()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L183 | neighbors=[TestSSHScanner]
- "tests_test_ssh_scanner_testsshstatustaxonomy_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L340 | neighbors=[TestSSHStatusTaxonomy]
- "tests_test_ssh_scanner_testsshstatustaxonomy_test_connect_failure_is_filtered": ".test_connect_failure_is_filtered()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L354 | neighbors=[TestSSHStatusTaxonomy]
- "tests_test_ssh_scanner_testsshstatustaxonomy_test_open_but_no_banner_is_open_not_ssh": ".test_open_but_no_banner_is_open_not_ssh()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L372 | neighbors=[TestSSHStatusTaxonomy]
- "tests_test_ssh_scanner_testsshstatustaxonomy_test_open_non_ssh_is_open_not_filtered": ".test_open_non_ssh_is_open_not_filtered()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L344 | neighbors=[TestSSHStatusTaxonomy]
- "tests_test_ssh_scanner_testvendoreddb_test_full_db_is_large_not_a_subset": ".test_full_db_is_large_not_a_subset()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L220 | neighbors=[TestVendoredDB]
- "tests_test_ssh_scanner_testvendoreddb_test_gss_wildcard_match": ".test_gss_wildcard_match()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L233 | neighbors=[TestVendoredDB]
- "tests_test_ssh_scanner_testvendoreddb_test_lookup_exact_and_unknown": ".test_lookup_exact_and_unknown()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L227 | neighbors=[TestVendoredDB]
- "tests_test_stage2_reconcile_cm_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L170 | neighbors=[_CM]
- "tests_test_stage2_reconcile_cm_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L171 | neighbors=[_CM]
- "tests_test_stage2_reconcile_cm_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L169 | neighbors=[_CM]
- "tests_test_stage2_reconcile_rationale_1": "Stage 2 — reconciled campaign completion + worker liveness.  Proves the correctn" | kind=entity | source=manager/backend/tests/test_stage2_reconcile.py:L1 | neighbors=[test_stage2_reconcile.py]
- "tests_test_stage2_reconcile_test_reap_stmt_targets_running_detection_runs": "test_reap_stmt_targets_running_detection_runs()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L186 | neighbors=[test_stage2_reconcile.py]
- "tests_test_stage2_reconcile_test_reconcile_dead_letter_wins_over_a_completed_run": "test_reconcile_dead_letter_wins_over_a_completed_run()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L81 | neighbors=[test_stage2_reconcile.py]
- "tests_test_stage2_reconcile_test_reconcile_status_precedence": "test_reconcile_status_precedence()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L76 | neighbors=[test_stage2_reconcile.py]
- "tests_test_syn_scanner_rationale_1": "test_syn_scanner.py — stateless SYN scan (Tier 1.1).  The raw-socket send/receiv" | kind=entity | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[test_syn_scanner.py]
- "tests_test_syn_scanner_rationale_205": "The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa" | kind=entity | source=probe/tests/test_syn_scanner.py:L205 | neighbors=[TestSynRetransmit]
- "tests_test_syn_scanner_rationale_208": "The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa" | kind=entity | source=probe/tests/test_syn_scanner.py:L208 | neighbors=[TestSynRetransmit]
- "tests_test_syn_scanner_rationale_327": "A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)." | kind=entity | source=probe/tests/test_syn_scanner.py:L327 | neighbors=[_synack_with_options()]
- "tests_test_syn_scanner_rationale_328": "A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)." | kind=entity | source=probe/tests/test_syn_scanner.py:L328 | neighbors=[_synack_with_options()]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_adaptive_on_by_default": ".test_adaptive_on_by_default()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L430 | neighbors=[TestAdaptiveTimeoutToggle]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_can_disable": ".test_can_disable()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L434 | neighbors=[TestAdaptiveTimeoutToggle]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-315.json

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
