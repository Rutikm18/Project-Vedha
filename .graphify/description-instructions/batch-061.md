# Node Description Batch 62 of 119

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

- "tests_test_agents_rationale_207": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L207 | neighbors=[ScanJobType, .test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_242": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L242 | neighbors=[ScanJobType, .test_agent_token_is_long_lived()]
- "tests_test_agents_rationale_260": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L260 | neighbors=[ScanJobType, TestPromoteAssets]
- "tests_test_agents_rationale_288": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L288 | neighbors=[ScanJobType, .test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_rationale_530": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L530 | neighbors=[ScanJobType, .test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_565": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L565 | neighbors=[ScanJobType, .test_agent_token_is_long_lived()]
- "tests_test_agents_rationale_583": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L583 | neighbors=[ScanJobType, TestPromoteAssets]
- "tests_test_agents_rationale_611": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L611 | neighbors=[ScanJobType, .test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_testenqueueagentjob_test_404_when_engagement_missing": ".test_404_when_engagement_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L53 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_materializes_direct_job_capability_for_probe": ".test_materializes_direct_job_capability_for_probe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L87 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_rejects_server_side_type": ".test_rejects_server_side_type()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L46 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_scope_fields_cannot_override_engagement_scope": ".test_scope_fields_cannot_override_engagement_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L115 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_success_creates_pending_job": ".test_success_creates_pending_job()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L62 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testlistagents_test_fresh_disconnected_agent_is_not_reported_online": ".test_fresh_disconnected_agent_is_not_reported_online()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L503 | neighbors=[TestListAgents, _user()]
- "tests_test_agents_testlistagents_test_lists_with_online_flag": ".test_lists_with_online_flag()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L481 | neighbors=[TestListAgents, _user()]
- "tests_test_agents_testotprofilegate_test_allows_passive_discovery_on_ot_engagement": ".test_allows_passive_discovery_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L183 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_blocks_active_scan_type_on_ot_engagement": ".test_blocks_active_scan_type_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L159 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_blocks_explicit_active_scan_type_override_on_ot_engagement": ".test_blocks_explicit_active_scan_type_override_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L170 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_it_and_iot_profiles_unaffected": ".test_it_and_iot_profiles_unaffected()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L195 | neighbors=[TestOTProfileGate, _user()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-061.json

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
