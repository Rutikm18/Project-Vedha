# Node Description Batch 61 of 119

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_agents_testregisteragent_test_creates_when_none_exists": ".test_creates_when_none_exists()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L552 | neighbors=[TestRegisterAgent, _user()]
- "tests_test_cli_test_cmd_doctor_success_with_online_agent": "test_cmd_doctor_success_with_online_agent()" | kind=code-symbol | source=probe/tests/test_cli.py:L204 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_cmd_scan_run_builds_dispatch_payload": "test_cmd_scan_run_builds_dispatch_payload()" | kind=code-symbol | source=probe/tests/test_cli.py:L167 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_rejects_invalid_timing": "test_poll_job_rejects_invalid_timing()" | kind=code-symbol | source=probe/tests/test_cli.py:L291 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_returns_terminal_status": "test_poll_job_returns_terminal_status()" | kind=code-symbol | source=probe/tests/test_cli.py:L298 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_times_out": "test_poll_job_times_out()" | kind=code-symbol | source=probe/tests/test_cli.py:L308 | neighbors=[test_cli.py, FakeClient]
- "tests_test_db_scanner_run": "_run()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L33 | neighbors=[test_db_scanner.py, _probe()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_rejects_garbage_with_type_byte": ".test_oracle_rejects_garbage_with_type_byte()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L73 | neighbors=[TestMysqlxVsOracle, _probe()]
- "tests_test_detection_core_testaggregate_test_dedup_within_run": ".test_dedup_within_run()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1074 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_multi_run_intermittent": ".test_multi_run_intermittent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1068 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_multi_run_stable": ".test_multi_run_stable()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1061 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_single_run": ".test_single_run()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1054 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testasset_test_add_fact_updates_first_last_seen": ".test_add_fact_updates_first_last_seen()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L129 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testasset_test_as_of_cutoff": ".test_as_of_cutoff()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L150 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testasset_test_facts_by_scanner": ".test_facts_by_scanner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L136 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testasset_test_open_ports": ".test_open_ports()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L143 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testclassifytier_test_authoritative_tier4": ".test_authoritative_tier4()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L596 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testclassifytier_test_multi_signal_tier2": ".test_multi_signal_tier2()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L605 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testclassifytier_test_protocol_scanner_tier3": ".test_protocol_scanner_tier3()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L600 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testclassifytier_test_single_banner_tier1": ".test_single_banner_tier1()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L610 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_critical": ".test_cvss_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L756 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_high": ".test_cvss_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L762 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_low": ".test_cvss_low()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L774 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_medium": ".test_cvss_medium()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L768 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_elevated_epss_high": ".test_elevated_epss_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L749 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_high_epss_critical": ".test_high_epss_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L742 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_kev_alone_critical": ".test_kev_alone_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L736 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_kev_unauth_reachable_critical": ".test_kev_unauth_reachable_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L727 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_unknown_tier": ".test_unknown_tier()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L780 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcorrelatesmbpatch_test_smbv1_with_missing_hotfixes_returns_finding": ".test_smbv1_with_missing_hotfixes_returns_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L570 | neighbors=[TestCorrelateSmbPatch, _fact()]
- "tests_test_detection_core_testcorrelatesmbpatch_test_smbv1_with_patched_host_returns_none": ".test_smbv1_with_patched_host_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L582 | neighbors=[TestCorrelateSmbPatch, _fact()]
- "tests_test_detection_core_testcorrelatesmbpatch_test_smbv1_without_hotfix_data_returns_none": ".test_smbv1_without_hotfix_data_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L565 | neighbors=[TestCorrelateSmbPatch, _fact()]
- "tests_test_detection_core_testcpecandidatecpe23_test_cpe23_format": ".test_cpe23_format()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L908 | neighbors=[TestCPECandidateCpe23, _candidate()]
- "tests_test_detection_core_testdedupfindings_test_authoritative_upgrades_state": ".test_authoritative_upgrades_state()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L493 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testdedupfindings_test_different_ids_preserved": ".test_different_ids_preserved()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L503 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testdedupfindings_test_evidence_refs_dedup_preserving_order": ".test_evidence_refs_dedup_preserving_order()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L508 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testdedupfindings_test_merges_same_id": ".test_merges_same_id()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L484 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testepssdb_test_case_insensitive": ".test_case_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L858 | neighbors=[TestEpssDb, _mock_epss_db()]
- "tests_test_detection_core_testepssdb_test_get_existing": ".test_get_existing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L850 | neighbors=[TestEpssDb, _mock_epss_db()]
- "tests_test_detection_core_testepssdb_test_get_missing": ".test_get_missing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L854 | neighbors=[TestEpssDb, _mock_epss_db()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-060.json

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
