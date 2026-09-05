# Node Description Batch 323 of 336

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

- "tests_test_verification_llm_test_llm_error_falls_back_to_deterministic": "test_llm_error_falls_back_to_deterministic()" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L19 | neighbors=[test_verification_llm.py] | lang=en
- "tests_test_verification_llm_test_no_llm_matches_deterministic": "test_no_llm_matches_deterministic()" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L11 | neighbors=[test_verification_llm.py] | lang=en
- "tests_test_version_compare_rationale_1": "Cross-validates the pure-Python Debian version comparator against the real `dpkg" | kind=entity | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[test_version_compare.py] | lang=en
- "tests_test_version_compare_test_dpkg_compare_public_api": "test_dpkg_compare_public_api()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L65 | neighbors=[test_version_compare.py] | lang=en
- "tests_test_version_compare_test_pure_python_matches_known_pairs": "test_pure_python_matches_known_pairs()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L45 | neighbors=[test_version_compare.py] | lang=en
- "tests_test_version_compare_test_pure_python_matches_real_dpkg_binary": "test_pure_python_matches_real_dpkg_binary()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L52 | neighbors=[test_version_compare.py] | lang=en
- "tests_test_vnc_scanner_rationale_1": "test_vnc_scanner.py — VNC/RFB authentication exposure.  Pure RFB parsing/classif" | kind=entity | source=probe/tests/test_vnc_scanner.py:L1 | neighbors=[test_vnc_scanner.py] | lang=en
- "tests_test_vnc_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L77 | neighbors=[TestParity] | lang=en
- "tests_test_vnc_scanner_testpurelogic_test_classify": ".test_classify()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L25 | neighbors=[TestPureLogic] | lang=en
- "tests_test_vnc_scanner_testpurelogic_test_parse_version": ".test_parse_version()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L19 | neighbors=[TestPureLogic] | lang=en
- "tests_test_vuln_enrichment_test_dedup_hash_case_insensitive_cve": "test_dedup_hash_case_insensitive_cve()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L242 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_dedup_hash_different_inputs": "test_dedup_hash_different_inputs()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L248 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_dedup_hash_stable": "test_dedup_hash_stable()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L236 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_fetch_epss_empty": "test_fetch_epss_empty()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L114 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_fetch_mitre_known_cve": "test_fetch_mitre_known_cve()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L148 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_fetch_nvd_not_found": "test_fetch_nvd_not_found()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L82 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_kev_bonus_increases_score": "test_kev_bonus_increases_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L186 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_max_risk_score": "test_max_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L164 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_risk_score_bounds": "test_risk_score_bounds()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L193 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_vuln_enrichment_test_zero_risk_score": "test_zero_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L175 | neighbors=[test_vuln_enrichment.py] | lang=en
- "tests_test_weakness_map_db": "db()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L29 | neighbors=[test_weakness_map.py] | lang=en
- "tests_test_weakness_map_rationale_1": "test_weakness_map.py — the weakness -> canonical-CVE bridge (cve/weakness_map.py" | kind=entity | source=probe/tests/test_weakness_map.py:L1 | neighbors=[test_weakness_map.py] | lang=en
- "tests_test_weakness_map_rationale_44": "A detect-stage fact: ScanResult('findings', ..., data=Finding.to_dict())." | kind=entity | source=probe/tests/test_weakness_map.py:L44 | neighbors=[_wrapped()] | lang=en
- "tests_test_weakness_map_rationale_51": "A bare Finding dict (findings.py --json output)." | kind=entity | source=probe/tests/test_weakness_map.py:L51 | neighbors=[_raw()] | lang=pt
- "tests_test_weakness_map_testclicorrelatemerges_disk_db": "._disk_db()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L181 | neighbors=[TestCliCorrelateMerges] | lang=en
- "tests_test_weakness_map_testclistatus_disk_db": "._disk_db()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L157 | neighbors=[TestCliStatus] | lang=en
- "tests_test_weakness_map_testclistatus_test_status_reports_counts_and_gaps": ".test_status_reports_counts_and_gaps()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L167 | neighbors=[TestCliStatus] | lang=en
- "tests_test_weakness_map_testfindingview_test_non_finding_ignored": ".test_non_finding_ignored()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L65 | neighbors=[TestFindingView] | lang=en
- "tests_test_weakness_map_testmirrorgap_test_every_mapping_has_at_least_one_cve": ".test_every_mapping_has_at_least_one_cve()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L149 | neighbors=[TestMirrorGap] | lang=en
- "tests_test_weakness_map_testmirrorgap_test_missing_from_mirror_lists_absent_canonical_cves": ".test_missing_from_mirror_lists_absent_canonical_cves()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L143 | neighbors=[TestMirrorGap] | lang=en
- "tests_test_web_methods_test_dangerous_methods_flagged": "test_dangerous_methods_flagged()" | kind=code-symbol | source=probe/tests/test_web_methods.py:L4 | neighbors=[test_web_methods.py] | lang=en
- "tests_test_web_methods_test_no_allow_header": "test_no_allow_header()" | kind=code-symbol | source=probe/tests/test_web_methods.py:L17 | neighbors=[test_web_methods.py] | lang=en
- "tests_test_web_methods_test_safe_methods_only": "test_safe_methods_only()" | kind=code-symbol | source=probe/tests/test_web_methods.py:L12 | neighbors=[test_web_methods.py] | lang=en
- "tests_test_wire_identity_rationale_1": "test_wire_identity.py — the scanner must NOT sign its own packets.  A brand stri" | kind=entity | source=probe/tests/test_wire_identity.py:L1 | neighbors=[test_wire_identity.py] | lang=en
- "tests_test_wire_identity_rationale_39": "Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs." | kind=entity | source=probe/tests/test_wire_identity.py:L39 | neighbors=[TestChooseSourcePort] | lang=pt
- "tests_test_wire_identity_rationale_58": "Evasion: blur a fixed scan cadence with a bounded random per-probe delay." | kind=entity | source=probe/tests/test_wire_identity.py:L58 | neighbors=[TestJitteredDelay] | lang=pt
- "tests_test_wire_identity_rationale_81": "Import-time probe constants built from user_agent() must be signature-free." | kind=entity | source=probe/tests/test_wire_identity.py:L81 | neighbors=[TestModuleConstantsUnbranded] | lang=en
- "tests_test_wire_identity_testchoosesourceport_test_boundary_ports_are_valid": ".test_boundary_ports_are_valid()" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L52 | neighbors=[TestChooseSourcePort] | lang=en
- "tests_test_wire_identity_testchoosesourceport_test_none_gives_random_ephemeral": ".test_none_gives_random_ephemeral()" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L45 | neighbors=[TestChooseSourcePort] | lang=en
- "tests_test_wire_identity_testchoosesourceport_test_out_of_range_falls_back_to_random": ".test_out_of_range_falls_back_to_random()" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L48 | neighbors=[TestChooseSourcePort] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-322.json

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
