# Node Description Batch 280 of 330

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

- "tests_test_finding_resolution_schema_test_finding_has_resolution_lifecycle_columns": "test_finding_has_resolution_lifecycle_columns()" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L6 | neighbors=[test_finding_resolution_schema.py] | lang=en
- "tests_test_finding_risk_rank_api_test_finding_schema_exposes_risk_rank": "test_finding_schema_exposes_risk_rank()" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L6 | neighbors=[test_finding_risk_rank_api.py] | lang=en
- "tests_test_finding_schema_test_finding_patch_accepts_documented_maximum_risk_score": "test_finding_patch_accepts_documented_maximum_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L9 | neighbors=[test_finding_schema.py] | lang=en
- "tests_test_finding_schema_test_finding_patch_rejects_risk_score_above_scale": "test_finding_patch_rejects_risk_score_above_scale()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L15 | neighbors=[test_finding_schema.py] | lang=en
- "tests_test_finding_schema_test_finding_summary_exposes_full_open_severity_breakdown": "test_finding_summary_exposes_full_open_severity_breakdown()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L20 | neighbors=[test_finding_schema.py] | lang=en
- "tests_test_finding_section_rationale_1": "test_finding_section.py — the scanner-module trust view + the finding section." | kind=entity | source=probe/tests/test_finding_section.py:L1 | neighbors=[test_finding_section.py] | lang=en
- "tests_test_finding_section_testscannerregistry_test_registry_aligns_with_manager_validated_set": ".test_registry_aligns_with_manager_validated_set()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L38 | neighbors=[TestScannerRegistry] | lang=en
- "tests_test_finding_section_testscannerregistry_test_unknown_scanner_is_not_trusted": ".test_unknown_scanner_is_not_trusted()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L28 | neighbors=[TestScannerRegistry] | lang=en
- "tests_test_finding_section_testscannerregistry_test_unvalidated_scanners_are_not_verified": ".test_unvalidated_scanners_are_not_verified()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L24 | neighbors=[TestScannerRegistry] | lang=en
- "tests_test_finding_section_testscannerregistry_test_user_validated_scanners_are_verified": ".test_user_validated_scanners_are_verified()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L18 | neighbors=[TestScannerRegistry] | lang=en
- "tests_test_finding_section_testscannerregistry_test_verification_report_shape": ".test_verification_report_shape()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L32 | neighbors=[TestScannerRegistry] | lang=en
- "tests_test_finding_verification_api_test_finding_schema_exposes_verification_fields": "test_finding_schema_exposes_verification_fields()" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_api.py:L6 | neighbors=[test_finding_verification_api.py] | lang=en
- "tests_test_finding_verification_schema_test_finding_has_verification_columns": "test_finding_has_verification_columns()" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_schema.py:L6 | neighbors=[test_finding_verification_schema.py] | lang=en
- "tests_test_fleet_jobs_rationale_1": "Fleet: tenant-wide job feed with probe + engagement name resolution and filters." | kind=entity | source=manager/backend/tests/test_fleet_jobs.py:L1 | neighbors=[test_fleet_jobs.py] | lang=en
- "tests_test_ftp_scanner_rationale_1": "test_ftp_scanner.py — FTP anonymous-access check.  Pure control-protocol logic +" | kind=entity | source=probe/tests/test_ftp_scanner.py:L1 | neighbors=[test_ftp_scanner.py] | lang=en
- "tests_test_ftp_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L76 | neighbors=[TestParity] | lang=en
- "tests_test_ftp_scanner_testpurelogic_test_banner_software": ".test_banner_software()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L23 | neighbors=[TestPureLogic] | lang=en
- "tests_test_ftp_scanner_testpurelogic_test_parse_pasv": ".test_parse_pasv()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L19 | neighbors=[TestPureLogic] | lang=en
- "tests_test_host_discovery_mobile_rationale_1": "Pure-logic tests for the ARP/MAC/mobile-detection helpers in host_discovery. No" | kind=entity | source=probe/tests/test_host_discovery_mobile.py:L1 | neighbors=[test_host_discovery_mobile.py] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_iphone_lockdownd_port": ".test_iphone_lockdownd_port()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L53 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_mobile_vendor": ".test_mobile_vendor()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L59 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_no_signal": ".test_no_signal()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L65 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_plain_vendor_passthrough": ".test_plain_vendor_passthrough()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L62 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_randomized_mac_is_mobile": ".test_randomized_mac_is_mobile()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L56 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testlocallyadministered_test_globally_unique_macs": ".test_globally_unique_macs()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L39 | neighbors=[TestLocallyAdministered] | lang=en
- "tests_test_host_discovery_mobile_testlocallyadministered_test_randomized_phone_macs": ".test_randomized_phone_macs()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L33 | neighbors=[TestLocallyAdministered] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_extracts_from_arp_line": ".test_extracts_from_arp_line()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L17 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_lowercases": ".test_lowercases()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L14 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_broadcast": ".test_rejects_broadcast()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L21 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_garbage": ".test_rejects_garbage()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L27 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_multicast": ".test_rejects_multicast()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L24 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_zero_pads_octets": ".test_zero_pads_octets()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L10 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testvendorlookup_test_known_oui": ".test_known_oui()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L45 | neighbors=[TestVendorLookup] | lang=en
- "tests_test_host_discovery_mobile_testvendorlookup_test_unknown_oui": ".test_unknown_oui()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L48 | neighbors=[TestVendorLookup] | lang=en
- "tests_test_host_discovery_udp_closed_udp_port": "_closed_udp_port()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L110 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_no_neighbor": "no_neighbor()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L120 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_rationale_1": "test_host_discovery_udp.py — the unprivileged UDP liveness tier + name facts.  C" | kind=entity | source=probe/tests/test_host_discovery_udp.py:L1 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_rationale_233": "A RST mid-handshake (ConnectionResetError) is the target's stack talking." | kind=entity | source=probe/tests/test_host_discovery_udp.py:L233 | neighbors=[test_tcp_reset_counts_as_proof_of_life()] | lang=en
- "tests_test_host_discovery_udp_rationale_25": "Build a NetBIOS node-status response (RFC 1002 §4.2.18)." | kind=entity | source=probe/tests/test_host_discovery_udp.py:L25 | neighbors=[_nbstat_reply()] | lang=pt
- "tests_test_host_discovery_udp_rationale_252": "On-LAN INCOMPLETE/FAILED = nobody owns the address right now; spending     datag" | kind=entity | source=probe/tests/test_host_discovery_udp.py:L252 | neighbors=[test_udp_tier_skipped_when_arp_definiti…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-279.json

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
