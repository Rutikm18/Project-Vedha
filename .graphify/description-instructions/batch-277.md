# Node Description Batch 278 of 330

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

- "tests_test_exploit_engine_testvalidatemodule_test_encoder_blocked": ".test_encoder_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L123 | neighbors=[TestValidateModule] | lang=en
- "tests_test_exploit_engine_testvalidatemodule_test_exploit_module_allowed": ".test_exploit_module_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L120 | neighbors=[TestValidateModule] | lang=en
- "tests_test_exploit_engine_testvalidatemodule_test_fuzzer_blocked": ".test_fuzzer_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L112 | neighbors=[TestValidateModule] | lang=en
- "tests_test_exploit_engine_testvalidatemodule_test_scanner_module_allowed": ".test_scanner_module_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L105 | neighbors=[TestValidateModule] | lang=en
- "tests_test_exploit_engine_testvalidatemodule_test_shell_to_meterpreter_blocked": ".test_shell_to_meterpreter_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L116 | neighbors=[TestValidateModule] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_allowed_payload_passes": ".test_allowed_payload_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L64 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_bind_shell_blocked": ".test_bind_shell_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L76 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_encrypt_payload_blocked": ".test_encrypt_payload_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L98 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_generic_none_always_allowed": ".test_generic_none_always_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L95 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_meterpreter_blocked": ".test_meterpreter_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L68 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_reverse_tcp_blocked": ".test_reverse_tcp_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L72 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_unknown_payload_blocked": ".test_unknown_payload_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L80 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_windows_exec_bad_command_blocked": ".test_windows_exec_bad_command_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L87 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_windows_exec_rm_rf_blocked": ".test_windows_exec_rm_rf_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L91 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatepayload_test_windows_exec_whoami_allowed": ".test_windows_exec_whoami_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L84 | neighbors=[TestValidatePayload] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_excluded_cidr_takes_priority": ".test_excluded_cidr_takes_priority()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L148 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_invalid_ip_fails": ".test_invalid_ip_fails()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L144 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_ip_in_excluded_fails": ".test_ip_in_excluded_fails()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L137 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_ip_in_scope_passes": ".test_ip_in_scope_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L130 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_ip_out_of_scope_fails": ".test_ip_out_of_scope_fails()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L133 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_multiple_scope_cidrs": ".test_multiple_scope_cidrs()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L141 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploitability_rationale_1": "test_exploitability.py — CISA KEV + FIRST EPSS on the POSTURE track.  The CVE tr" | kind=entity | source=manager/detection_engine/tests/test_exploitability.py:L1 | neighbors=[test_exploitability.py] | lang=en
- "tests_test_exploitability_rationale_120": "Severity is the rule's judgement of the weakness. Exploitation         evidence" | kind=entity | source=manager/detection_engine/tests/test_exploitability.py:L120 | neighbors=[.test_declared_severity_is_never_rewrit…] | lang=en
- "tests_test_exploitability_rationale_151": "A re-rank here must never disagree with the original scoring, so the         two" | kind=entity | source=manager/detection_engine/tests/test_exploitability.py:L151 | neighbors=[.test_priority_bands_match_posture_rule…] | lang=en
- "tests_test_exploitability_rationale_163": "The pipeline may enrich the same finding twice (a re-run, or a caller         th" | kind=entity | source=manager/detection_engine/tests/test_exploitability.py:L163 | neighbors=[.test_idempotent_across_repeated_applic…] | lang=en
- "tests_test_exploitability_rationale_191": "If a curated link names a CVE the shipped snapshot does not list, the     boost" | kind=entity | source=manager/detection_engine/tests/test_exploitability.py:L191 | neighbors=[test_linked_cves_are_actually_on_the_pi…] | lang=en
- "tests_test_exploitability_rationale_62": "A stale or narrowed KEV snapshot must be VISIBLE, not silently drop         the" | kind=entity | source=manager/detection_engine/tests/test_exploitability.py:L62 | neighbors=[.test_a_link_not_on_the_kev_list_is_kep…] | lang=en
- "tests_test_exploitability_testneverclaimsthecveispresent_test_every_link_states_a_relation": ".test_every_link_states_a_relation()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L46 | neighbors=[TestNeverClaimsTheCveIsPresent] | lang=en
- "tests_test_exposed_services_rationale_1": "test_exposed_services.py — the exposed-service / suspicious-port detection layer" | kind=entity | source=manager/detection_engine/tests/test_exposed_services.py:L1 | neighbors=[test_exposed_services.py] | lang=en
- "tests_test_exposed_services_rationale_189": "A catalog entry is a guess about what a port means. When service_banner     posi" | kind=entity | source=manager/detection_engine/tests/test_exposed_services.py:L189 | neighbors=[TestPortHypothesisContradiction] | lang=pt
- "tests_test_exposed_services_rationale_211": "A shell answering on a benign-listed port is still a backdoor: the         contr" | kind=entity | source=manager/detection_engine/tests/test_exposed_services.py:L211 | neighbors=[.test_backdoor_evidence_is_never_suppre…] | lang=pt
- "tests_test_exposed_services_test_ingest_aliases_from_host_discovery_names": "test_ingest_aliases_from_host_discovery_names()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L178 | neighbors=[test_exposed_services.py] | lang=en
- "tests_test_exposed_services_testclassify_test_backdoor_ports": ".test_backdoor_ports()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L35 | neighbors=[TestClassify] | lang=en
- "tests_test_exposed_services_testclassify_test_banner_confirms_backdoor_on_any_port": ".test_banner_confirms_backdoor_on_any_port()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L58 | neighbors=[TestClassify] | lang=en
- "tests_test_exposed_services_testclassify_test_benign_port_is_none": ".test_benign_port_is_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L63 | neighbors=[TestClassify] | lang=en
- "tests_test_exposed_services_testclassify_test_cleartext_telnet_is_high": ".test_cleartext_telnet_is_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L54 | neighbors=[TestClassify] | lang=en
- "tests_test_exposed_services_testclassify_test_container_apis_are_high": ".test_container_apis_are_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L40 | neighbors=[TestClassify] | lang=en
- "tests_test_exposed_services_testclassify_test_databases": ".test_databases()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L50 | neighbors=[TestClassify] | lang=en
- "tests_test_exposed_services_testclassify_test_escalate": ".test_escalate()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L68 | neighbors=[TestClassify] | lang=en
- "tests_test_exposed_services_testclassify_test_unauth_data_stores": ".test_unauth_data_stores()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L45 | neighbors=[TestClassify] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-277.json

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
