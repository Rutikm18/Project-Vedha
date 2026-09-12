# Node Description Batch 101 of 380

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

- "ad_ldap_enum_rationale_312": "Parse the nTSecurityDescriptor of an object into a list of ACEs for ACL" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L312 | neighbors=[ADConnectionError, DependencyMissingError, .get_aces()]
- "ad_ldap_enum_rationale_85": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L85 | neighbors=[ACE, ADConnectionError, DependencyMissingError]
- "ad_ldap_enum_rationale_86": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L86 | neighbors=[ADConnectionError, DependencyMissingError, ACE]
- "ad_ntlm_relay_ntlmrelaychecker_check_smb_signing": ".check_smb_signing()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L38 | neighbors=[NTLMRelayChecker, ._probe_smb_host(), For each IP, returns {signing_enabled, …]
- "ad_orchestrator_adassessmentrunner_run": ".run()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L50 | neighbors=[ADAssessmentRunner, ._anonymous_bind_finding(), Returns {findings: [...], stats: {...},…]
- "agent_agent_rationale_557": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L557 | neighbors=[_run_ws_push_loop(), _ws_stage_job_offer(), _ws_http_poll_fallback()]
- "agent_agent_runautonomousengagement": "runAutonomousEngagement()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L95 | neighbors=[agent.py, isBlocked(), requiresApproval()]
- "agent_cli_cmd_auth_logout": "cmd_auth_logout()" | kind=code-symbol | source=probe/agent/cli.py:L292 | neighbors=[cli.py, ConfigStore, .remove_profile()]
- "agent_cli_cmd_daemon_run": "cmd_daemon_run()" | kind=code-symbol | source=probe/agent/cli.py:L913 | neighbors=[cli.py, resolve_profile(), split_values()]
- "agent_cli_configstore_get_profile": ".get_profile()" | kind=code-symbol | source=probe/agent/cli.py:L87 | neighbors=[ConfigStore, .load(), resolve_profile()]
- "agent_cli_configstore_save": ".save()" | kind=code-symbol | source=probe/agent/cli.py:L75 | neighbors=[ConfigStore, .remove_profile(), .set_profile()]
- "agent_cli_default_config_path": "default_config_path()" | kind=code-symbol | source=probe/agent/cli.py:L40 | neighbors=[cli.py, build_parser(), _env()]
- "agent_cli_fetch_all_findings": "_fetch_all_findings()" | kind=code-symbol | source=probe/agent/cli.py:L549 | neighbors=[cli.py, cmd_validate(), .request()]
- "agent_cli_parse_param_pairs": "parse_param_pairs()" | kind=code-symbol | source=probe/agent/cli.py:L165 | neighbors=[cli.py, cmd_scan_run(), CliError]
- "agent_connect_admit_job": "admit_job()" | kind=code-symbol | source=probe/agent/connect.py:L65 | neighbors=[connect.py, verify_job(), The independent ceiling: a job is admit…]
- "agent_connect_canonical_job_bytes": "canonical_job_bytes()" | kind=code-symbol | source=probe/agent/connect.py:L35 | neighbors=[connect.py, Deterministic bytes the Manager signs a…, verify_job()]
- "agent_deps_venv_python": "venv_python()" | kind=code-symbol | source=probe/agent/deps.py:L20 | neighbors=[deps.py, ensure_venv(), venv_dir()]
- "agent_device_identity_verify_site_policy": "verify_site_policy()" | kind=code-symbol | source=probe/agent/device_identity.py:L37 | neighbors=[device_identity.py, Verify a Manager-signed policy and retu…, decode_key()]
- "agent_doctor_check_clock": "check_clock()" | kind=code-symbol | source=probe/agent/doctor.py:L37 | neighbors=[doctor.py, Check, run()]
- "agent_doctor_check_disk": "check_disk()" | kind=code-symbol | source=probe/agent/doctor.py:L48 | neighbors=[doctor.py, Check, run()]
- "agent_doctor_check_privilege": "check_privilege()" | kind=code-symbol | source=probe/agent/doctor.py:L71 | neighbors=[doctor.py, Check, run()]
- "agent_doctor_check_python": "check_python()" | kind=code-symbol | source=probe/agent/doctor.py:L30 | neighbors=[doctor.py, Check, run()]
- "agent_doctor_classify_connectivity": "classify_connectivity()" | kind=code-symbol | source=probe/agent/doctor.py:L55 | neighbors=[doctor.py, Check, run()]
- "agent_doctor_offset_from_date_header": "_offset_from_date_header()" | kind=code-symbol | source=probe/agent/doctor.py:L116 | neighbors=[doctor.py, Pure: server clock offset (seconds) fro…, _server_date_offset()]
- "agent_doctor_server_date_offset": "_server_date_offset()" | kind=code-symbol | source=probe/agent/doctor.py:L128 | neighbors=[doctor.py, run(), _offset_from_date_header()]
- "agent_engine_run_with_cancellation": "_run_with_cancellation()" | kind=code-symbol | source=probe/agent/engine.py:L572 | neighbors=[engine.py, run_scan(), LeaseLostError]
- "agent_engine_runtime_manifest": "_runtime_manifest()" | kind=code-symbol | source=probe/agent/engine.py:L68 | neighbors=[engine.py, _error_result(), run_scan()]
- "agent_engine_string_list": "_string_list()" | kind=code-symbol | source=probe/agent/engine.py:L196 | neighbors=[engine.py, run_scan(), _targets()]
- "agent_engine_targets": "_targets()" | kind=code-symbol | source=probe/agent/engine.py:L212 | neighbors=[engine.py, run_scan(), _string_list()]
- "agent_exit_state_class_for_reason": "class_for_reason()" | kind=code-symbol | source=probe/agent/exit_state.py:L44 | neighbors=[exit_state.py, code_for_reason(), make()]
- "agent_exit_state_code_for_class": "code_for_class()" | kind=code-symbol | source=probe/agent/exit_state.py:L50 | neighbors=[exit_state.py, code_for_reason(), make()]
- "agent_exit_state_code_for_reason": "code_for_reason()" | kind=code-symbol | source=probe/agent/exit_state.py:L54 | neighbors=[exit_state.py, class_for_reason(), code_for_class()]
- "agent_exit_state_exitstate": "ExitState" | kind=code-symbol | source=probe/agent/exit_state.py:L63 | neighbors=[exit_state.py, from_json(), make()]
- "agent_exit_state_from_json": "from_json()" | kind=code-symbol | source=probe/agent/exit_state.py:L89 | neighbors=[exit_state.py, ExitState, read()]
- "agent_explain_plan_print_table": "_print_table()" | kind=code-symbol | source=probe/agent/explain_plan.py:L78 | neighbors=[explain_plan.py, main(), _why()]
- "agent_explain_plan_why": "_why()" | kind=code-symbol | source=probe/agent/explain_plan.py:L43 | neighbors=[explain_plan.py, _print_table(), Recreate this branch's decision and say…]
- "agent_hw_bind_get_hw_id": "get_hw_id()" | kind=code-symbol | source=probe/agent/hw_bind.py:L23 | neighbors=[hw_bind.py, check_hw_bind(), Deterministic per-machine fingerprint b…]
- "agent_instance_lock_holder_hint": "_holder_hint()" | kind=code-symbol | source=probe/agent/instance_lock.py:L62 | neighbors=[instance_lock.py, acquire_instance_lock(), Best-effort description of the current …]
- "agent_instance_lock_lock_path_for": "lock_path_for()" | kind=code-symbol | source=probe/agent/instance_lock.py:L55 | neighbors=[instance_lock.py, acquire_instance_lock(), Sidecar lock path for a state file. Nev…]
- "agent_local_run_clean": "_clean()" | kind=code-symbol | source=probe/agent/local_run.py:L68 | neighbors=[local_run.py, Drop internal bookkeeping keys (_collec…, summarize()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-100.json

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
