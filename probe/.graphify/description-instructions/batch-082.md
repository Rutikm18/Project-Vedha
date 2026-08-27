# Node Description Batch 83 of 92

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

- "tests_test_scope_validator_testvalidatetargetsinscope_test_explicit_hostname_scope_allows_exact_hostname_only": ".test_explicit_hostname_scope_allows_exact_hostname_only()" | kind=code-symbol | source=tests/test_scope_validator.py:L36 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_hostname_rejected_when_scope_is_ip_only": ".test_hostname_rejected_when_scope_is_ip_only()" | kind=code-symbol | source=tests/test_scope_validator.py:L29 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_invalid_cidr_ignored": ".test_invalid_cidr_ignored()" | kind=code-symbol | source=tests/test_scope_validator.py:L49 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_ip_in_cidr_allowed": ".test_ip_in_cidr_allowed()" | kind=code-symbol | source=tests/test_scope_validator.py:L15 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_ipv6_literal_is_validated_without_colon_truncation": ".test_ipv6_literal_is_validated_without_colon_truncation()" | kind=code-symbol | source=tests/test_scope_validator.py:L77 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_multiple_cidrs": ".test_multiple_cidrs()" | kind=code-symbol | source=tests/test_scope_validator.py:L84 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_outside_cidr_rejected": ".test_outside_cidr_rejected()" | kind=code-symbol | source=tests/test_scope_validator.py:L22 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_port_suffix_is_not_a_valid_network_target": ".test_port_suffix_is_not_a_valid_network_target()" | kind=code-symbol | source=tests/test_scope_validator.py:L55 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_range_must_be_fully_contained": ".test_range_must_be_fully_contained()" | kind=code-symbol | source=tests/test_scope_validator.py:L69 | neighbors=[TestValidateTargetsInScope]
- "tests_test_service_match_rationale_1": "test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi" | kind=entity | source=tests/test_service_match.py:L1 | neighbors=[test_service_match.py]
- "tests_test_service_match_testhttpmatch_test_apache_version": ".test_apache_version()" | kind=code-symbol | source=tests/test_service_match.py:L42 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_iis_version": ".test_iis_version()" | kind=code-symbol | source=tests/test_service_match.py:L47 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_version": ".test_nginx_version()" | kind=code-symbol | source=tests/test_service_match.py:L36 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_without_version": ".test_nginx_without_version()" | kind=code-symbol | source=tests/test_service_match.py:L52 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testnomatch_test_empty_returns_none": ".test_empty_returns_none()" | kind=code-symbol | source=tests/test_service_match.py:L91 | neighbors=[TestNoMatch]
- "tests_test_service_match_testnomatch_test_unrecognized_returns_none": ".test_unrecognized_returns_none()" | kind=code-symbol | source=tests/test_service_match.py:L88 | neighbors=[TestNoMatch]
- "tests_test_service_match_testotherservices_test_mariadb_handshake": ".test_mariadb_handshake()" | kind=code-symbol | source=tests/test_service_match.py:L70 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_info": ".test_redis_info()" | kind=code-symbol | source=tests/test_service_match.py:L77 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_noauth": ".test_redis_noauth()" | kind=code-symbol | source=tests/test_service_match.py:L82 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_smtp_postfix": ".test_smtp_postfix()" | kind=code-symbol | source=tests/test_service_match.py:L65 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_vsftpd": ".test_vsftpd()" | kind=code-symbol | source=tests/test_service_match.py:L59 | neighbors=[TestOtherServices]
- "tests_test_service_match_testprobeladder_test_ladder_has_http_and_generic": ".test_ladder_has_http_and_generic()" | kind=code-symbol | source=tests/test_service_match.py:L102 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testprobeladder_test_ladder_starts_with_null_probe": ".test_ladder_starts_with_null_probe()" | kind=code-symbol | source=tests/test_service_match.py:L96 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testscannerintegration_test_scanner_identifies_ssh_on_nonstandard_port": ".test_scanner_identifies_ssh_on_nonstandard_port()" | kind=code-symbol | source=tests/test_service_match.py:L109 | neighbors=[TestScannerIntegration]
- "tests_test_service_match_testsshmatch_test_dropbear": ".test_dropbear()" | kind=code-symbol | source=tests/test_service_match.py:L23 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_generic_ssh": ".test_generic_ssh()" | kind=code-symbol | source=tests/test_service_match.py:L29 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_openssh_version": ".test_openssh_version()" | kind=code-symbol | source=tests/test_service_match.py:L17 | neighbors=[TestSshMatch]
- "tests_test_smb_scanner_rationale_15": "An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this" | kind=entity | source=tests/test_smb_scanner.py:L15 | neighbors=[_smb2_error_response()]
- "tests_test_smb_scanner_rationale_51": "The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was     rea" | kind=entity | source=tests/test_smb_scanner.py:L51 | neighbors=[test_error_response_not_parsed_as_signi…]
- "tests_test_smb_scanner_rationale_63": "A response with the wrong body StructureSize is not a valid NEGOTIATE." | kind=entity | source=tests/test_smb_scanner.py:L63 | neighbors=[test_truncated_negotiate_body_not_parse…]
- "tests_test_smb_scanner_rationale_72": "Step 13: expose signing_supported (protocol-precise), not only the     ambiguous" | kind=entity | source=tests/test_smb_scanner.py:L72 | neighbors=[test_signing_supported_field_present()]
- "tests_test_smb_scanner_rationale_81": "Offering SMB 3.1.1 with no preauth-integrity negotiate context makes     Windows" | kind=entity | source=tests/test_smb_scanner.py:L81 | neighbors=[test_request_omits_311_without_preauth_…]
- "tests_test_smb_scanner_test_garbage_response": "test_garbage_response()" | kind=code-symbol | source=tests/test_smb_scanner.py:L44 | neighbors=[test_smb_scanner.py]
- "tests_test_syn_scanner_rationale_1": "test_syn_scanner.py — stateless SYN scan (Tier 1.1).  The raw-socket send/receiv" | kind=entity | source=tests/test_syn_scanner.py:L1 | neighbors=[test_syn_scanner.py]
- "tests_test_syn_scanner_rationale_205": "The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa" | kind=entity | source=tests/test_syn_scanner.py:L205 | neighbors=[TestSynRetransmit]
- "tests_test_syn_scanner_rationale_327": "A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)." | kind=entity | source=tests/test_syn_scanner.py:L327 | neighbors=[_synack_with_options()]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_adaptive_on_by_default": ".test_adaptive_on_by_default()" | kind=code-symbol | source=tests/test_syn_scanner.py:L382 | neighbors=[TestAdaptiveTimeoutToggle]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_can_disable": ".test_can_disable()" | kind=code-symbol | source=tests/test_syn_scanner.py:L386 | neighbors=[TestAdaptiveTimeoutToggle]
- "tests_test_syn_scanner_testcapabilitydetection_test_linux_with_raw_socket_is_supported": ".test_linux_with_raw_socket_is_supported()" | kind=code-symbol | source=tests/test_syn_scanner.py:L148 | neighbors=[TestCapabilityDetection]
- "tests_test_syn_scanner_testcapabilitydetection_test_linux_without_privilege_is_unsupported": ".test_linux_without_privilege_is_unsupported()" | kind=code-symbol | source=tests/test_syn_scanner.py:L143 | neighbors=[TestCapabilityDetection]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-082.json

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
