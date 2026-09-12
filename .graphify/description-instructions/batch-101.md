# Node Description Batch 102 of 380

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

- "agent_local_run_parse_args": "_parse_args()" | kind=code-symbol | source=probe/agent/local_run.py:L120 | neighbors=[local_run.py, _main(), Validate positional args (args[0]=targe…]
- "agent_local_run_port_label": "_port_label()" | kind=code-symbol | source=probe/agent/local_run.py:L75 | neighbors=[local_run.py, Render a port fact unambiguously: '445/…, summarize()]
- "agent_local_run_ports_from_env": "_ports_from_env()" | kind=code-symbol | source=probe/agent/local_run.py:L42 | neighbors=[local_run.py, _main(), Resolve the port set from PROBE_LOCAL_P…]
- "agent_local_run_run": "run()" | kind=code-symbol | source=probe/agent/local_run.py:L199 | neighbors=[local_run.py, Synchronous entrypoint for the `local-r…, _main()]
- "agent_local_run_usage_error": "_usage_error()" | kind=code-symbol | source=probe/agent/local_run.py:L109 | neighbors=[local_run.py, _main(), Actionable input error on stderr → exit…]
- "agent_obs_mask_addr": "_mask_addr()" | kind=code-symbol | source=probe/agent/obs.py:L45 | neighbors=[obs.py, build_diagnostics(), mask_ip()]
- "agent_obs_mask_ip": "mask_ip()" | kind=code-symbol | source=probe/agent/obs.py:L37 | neighbors=[obs.py, _mask_addr(), Mask the host octet so an own-IP never …]
- "agent_release_sbom_from_requirements": "sbom_from_requirements()" | kind=code-symbol | source=probe/agent/release.py:L50 | neighbors=[release.py, main(), parse_requirements()]
- "agent_release_sha256_file": "sha256_file()" | kind=code-symbol | source=probe/agent/release.py:L17 | neighbors=[release.py, sha256_manifest(), verify_manifest()]
- "agent_result_queue_resultqueue_bytes": "._bytes()" | kind=code-symbol | source=probe/agent/result_queue.py:L140 | neighbors=[ResultQueue, ._enforce_size_bounds(), .stats()]
- "agent_result_queue_resultqueue_init": ".__init__()" | kind=code-symbol | source=probe/agent/result_queue.py:L76 | neighbors=[ResultQueue, NullCipher, ._max_seq()]
- "agent_result_queue_resultqueue_max_seq": "._max_seq()" | kind=code-symbol | source=probe/agent/result_queue.py:L95 | neighbors=[ResultQueue, .__init__(), ._files()]
- "agent_result_spool_resultspool_spool_bytes": ".spool_bytes()" | kind=code-symbol | source=probe/agent/result_spool.py:L222 | neighbors=[Total bytes held by pending result file…, ResultSpool, .exists()]
- "agent_scope_crypt_decrypt_scope": "decrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L97 | neighbors=[scope_crypt.py, decrypt_scope_b64(), Decrypt a scope blob using the probe's …]
- "agent_scope_crypt_decrypt_scope_b64": "decrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L155 | neighbors=[scope_crypt.py, decrypt_scope(), decrypt_scope() accepting a base64 stri…]
- "agent_scope_crypt_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L55 | neighbors=[scope_crypt.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…]
- "agent_scope_crypt_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L150 | neighbors=[scope_crypt.py, encrypt_scope(), encrypt_scope() returning a base64 stri…]
- "agent_scope_model_is_denied": "is_denied()" | kind=code-symbol | source=probe/agent/scope_model.py:L62 | neighbors=[scope_model.py, True if `target` (an IP or CIDR) must N…, target_allowed()]
- "agent_scope_model_parse_linux_ip_json": "parse_linux_ip_json()" | kind=code-symbol | source=probe/agent/scope_model.py:L165 | neighbors=[scope_model.py, classify_interface(), Interface]
- "agent_scope_model_target_allowed": "target_allowed()" | kind=code-symbol | source=probe/agent/scope_model.py:L112 | neighbors=[scope_model.py, Independent of the Manager: a target is…, is_denied()]
- "agent_scope_validator_fetch_engagement_scope": "fetch_engagement_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L54 | neighbors=[scope_validator.py, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…]
- "agent_scope_validator_merge_exclusions": "merge_exclusions()" | kind=code-symbol | source=probe/agent/scope_validator.py:L154 | neighbors=[scope_validator.py, Merge engagement-level exclusions with …, Merge engagement-level exclusions with …]
- "agent_self_scan_detect_host_container": "detect_host_container()" | kind=code-symbol | source=probe/agent/self_scan.py:L90 | neighbors=[self_scan.py, _read(), run()]
- "agent_self_scan_execute": "execute()" | kind=code-symbol | source=probe/agent/self_scan.py:L45 | neighbors=[self_scan.py, Write the own-IP scope file, run the en…, run_from()]
- "agent_self_scan_main": "main()" | kind=code-symbol | source=probe/agent/self_scan.py:L111 | neighbors=[self_scan.py, run(), Runnable entry: `python -m agent.self_s…]
- "agent_service_install": "install()" | kind=code-symbol | source=probe/agent/service.py:L110 | neighbors=[service.py, commands_for(), render_unit()]
- "agent_service_render_unit": "render_unit()" | kind=code-symbol | source=probe/agent/service.py:L60 | neighbors=[service.py, install(), Return (target_path, body). Windows ret…]
- "agent_setup_cmd_uninstall": "cmd_uninstall()" | kind=code-symbol | source=probe/agent/setup.py:L119 | neighbors=[setup.py, _os_name(), _state_dir()]
- "agent_setup_is_privileged": "_is_privileged()" | kind=code-symbol | source=probe/agent/setup.py:L24 | neighbors=[setup.py, cmd_collect_diagnostics(), cmd_doctor()]
- "agent_setup_os_name": "_os_name()" | kind=code-symbol | source=probe/agent/setup.py:L33 | neighbors=[setup.py, cmd_connect(), cmd_uninstall()]
- "agent_supervisor": "supervisor.py" | kind=code-symbol | source=probe/agent/supervisor.py:L1 | neighbors=[supervise(), supervisor.py — restart supervisor with…, 42b9cf2 Phase 3: exit-state protocol + …]
- "agent_task_runner_result_dir": "_result_dir()" | kind=code-symbol | source=probe/agent/task_runner.py:L49 | neighbors=[task_runner.py, prepare_result_dir(), ._archive_result()]
- "agent_task_runner_taskrunner_already_committed": "._already_committed()" | kind=code-symbol | source=probe/agent/task_runner.py:L182 | neighbors=[Hosts the manager already holds for thi…, TaskRunner, .run_job()]
- "agent_task_runner_taskrunner_chunk_sink": "._chunk_sink()" | kind=code-symbol | source=probe/agent/task_runner.py:L161 | neighbors=[A callback the scan engine invokes when…, TaskRunner, .run_job()]
- "agent_transport_transport_clear_manager_binding": ".clear_manager_binding()" | kind=code-symbol | source=probe/agent/transport.py:L329 | neighbors=[Forget everything a SPECIFIC manager is…, Transport, .update_state()]
- "agent_transport_transport_committed_hosts": ".committed_hosts()" | kind=code-symbol | source=probe/agent/transport.py:L830 | neighbors=[Hosts the manager already holds for thi…, Transport, .ensure_device_access()]
- "agent_transport_transport_create_enrollment_request": ".create_enrollment_request()" | kind=code-symbol | source=probe/agent/transport.py:L452 | neighbors=[Transport, DeviceAlreadyEnrolledError, _enrollment_conflict_detail()]
- "agent_validation_validate_ground_truth": "validate_ground_truth()" | kind=code-symbol | source=probe/agent/validation.py:L106 | neighbors=[validation.py, Validate the small, explicit inventory …, score_inventory()]
- "ai_agent_agentdecisionengine_list_findings": "._list_findings()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L288 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), _val()]
- "ai_agent_val": "_val()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L398 | neighbors=[agent.py, ._list_findings(), ._overview()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-101.json

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
