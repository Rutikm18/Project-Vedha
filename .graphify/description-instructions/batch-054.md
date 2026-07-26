# Node Description Batch 55 of 104

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

- "schemas_auth_loginrequest": "LoginRequest" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L9 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreate": "PersonalAccessTokenCreate" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L32 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreated": "PersonalAccessTokenCreated" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L38 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokenout": "PersonalAccessTokenOut" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L49 | neighbors=[auth.py, BaseModel]
- "schemas_auth_tokenresponse": "TokenResponse" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L14 | neighbors=[auth.py, BaseModel]
- "schemas_common_errordetail": "ErrorDetail" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L18 | neighbors=[common.py, BaseModel]
- "schemas_common_paginate": "paginate()" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L22 | neighbors=[common.py, PaginatedResponse]
- "services_analytics_compute_exposure": "compute_exposure()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L35 | neighbors=[analytics.py, _sev()]
- "services_analytics_sev": "_sev()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L31 | neighbors=[analytics.py, compute_exposure()]
- "services_scope_crypto_public_key_from_b64": "public_key_from_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L85 | neighbors=[scope_crypto.py, Decode a base64-encoded X25519 public k…]
- "services_sla_windows": "_windows()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L34 | neighbors=[sla.py, compute()]
- "tests_test_ad_assessment_fakeentry_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L41 | neighbors=[_FakeEntry, _FakeAttr]
- "tests_test_ad_assessment_testkerberoastchecker_ldap_with_users": "._ldap_with_users()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L173 | neighbors=[TestKerberoastChecker, .test_get_spn_accounts_filters_krbtgt_a…]
- "tests_test_ad_assessment_testkerberoastchecker_test_get_spn_accounts_filters_krbtgt_and_no_spn": ".test_get_spn_accounts_filters_krbtgt_and_no_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L179 | neighbors=[TestKerberoastChecker, ._ldap_with_users()]
- "tests_test_agents_rationale_1": "Unit tests for the agent/probe protocol changes:   * agent polling is restricted" | kind=entity | source=manager/backend/tests/test_agents.py:L1 | neighbors=[ScanJobType, test_agents.py]
- "tests_test_agents_rationale_207": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L207 | neighbors=[ScanJobType, .test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_242": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L242 | neighbors=[ScanJobType, .test_agent_token_is_long_lived()]
- "tests_test_agents_rationale_260": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L260 | neighbors=[ScanJobType, TestPromoteAssets]
- "tests_test_agents_rationale_288": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L288 | neighbors=[ScanJobType, .test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_testenqueueagentjob_test_404_when_engagement_missing": ".test_404_when_engagement_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L53 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_rejects_server_side_type": ".test_rejects_server_side_type()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L46 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_success_creates_pending_job": ".test_success_creates_pending_job()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L62 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testlistagents_test_lists_with_online_flag": ".test_lists_with_online_flag()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L179 | neighbors=[TestListAgents, _user()]
- "tests_test_agents_testotprofilegate_test_allows_passive_discovery_on_ot_engagement": ".test_allows_passive_discovery_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L114 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_blocks_active_scan_type_on_ot_engagement": ".test_blocks_active_scan_type_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L90 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_blocks_explicit_active_scan_type_override_on_ot_engagement": ".test_blocks_explicit_active_scan_type_override_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L101 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testotprofilegate_test_it_and_iot_profiles_unaffected": ".test_it_and_iot_profiles_unaffected()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L125 | neighbors=[TestOTProfileGate, _user()]
- "tests_test_agents_testpromoteassets_test_dedupes_duplicate_services_in_same_probe_result": ".test_dedupes_duplicate_services_in_same_probe_result()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L287 | neighbors=[A single web scan can emit multiple fac…, TestPromoteAssets]
- "tests_test_agents_testregisteragent_test_creates_when_none_exists": ".test_creates_when_none_exists()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L229 | neighbors=[TestRegisterAgent, _user()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-054.json

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
