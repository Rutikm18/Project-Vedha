# Node Description Batch 21 of 92

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

- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=agent/agent.py:L709 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say()]
- "agent_cli_build_parser": "build_parser()" | kind=code-symbol | source=agent/cli.py:L931 | neighbors=[cli.py, default_config_path(), _env(), main()]
- "agent_cli_cmd_agents_list": "cmd_agents_list()" | kind=code-symbol | source=agent/cli.py:L407 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_list": "cmd_engagements_list()" | kind=code-symbol | source=agent/cli.py:L424 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_scope": "cmd_engagements_scope()" | kind=code-symbol | source=agent/cli.py:L472 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_scan_status": "cmd_scan_status()" | kind=code-symbol | source=agent/cli.py:L528 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_use_cases": "cmd_use_cases()" | kind=code-symbol | source=agent/cli.py:L391 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_configstore_remove_profile": ".remove_profile()" | kind=code-symbol | source=agent/cli.py:L94 | neighbors=[cmd_auth_logout(), ConfigStore, .load(), .save()]
- "agent_cli_configstore_set_profile": ".set_profile()" | kind=code-symbol | source=agent/cli.py:L88 | neighbors=[cmd_auth_login(), ConfigStore, .load(), .save()]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=agent/engine.py:L282 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count unique open network endpoints, no…]
- "agent_engine_derive_devices": "_derive_devices()" | kind=code-symbol | source=agent/engine.py:L469 | neighbors=[engine.py, _results_by_target(), _derive_post_stage(), Classify each target's device role from…]
- "agent_engine_derive_exposure": "_derive_exposure()" | kind=code-symbol | source=agent/engine.py:L489 | neighbors=[engine.py, _results_by_target(), _derive_post_stage(), Reconcile each target's per-vantage rea…]
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=agent/engine.py:L72 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan()]
- "agent_engine_hosts_from_facts": "_hosts_from_facts()" | kind=code-symbol | source=agent/engine.py:L303 | neighbors=[engine.py, _build_run_stats(), Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…]
- "agent_engine_results_by_target": "_results_by_target()" | kind=code-symbol | source=agent/engine.py:L432 | neighbors=[engine.py, _derive_devices(), _derive_exposure(), _derive_post_stage()]
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…]
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=agent/license.py:L35 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license()]
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=agent/license.py:L41 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()]
- "agent_local_run_summarize": "summarize()" | kind=code-symbol | source=agent/local_run.py:L90 | neighbors=[local_run.py, _main(), _clean(), _port_label()]
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=agent/result_spool.py:L99 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path()]
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()]
- "agent_task_runner_taskrunner_run_job": ".run_job()" | kind=code-symbol | source=agent/task_runner.py:L88 | neighbors=[Execute a complete scan job lifecycle. …, TaskRunner, JobResult, ._submit_or_spool()]
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=agent/transport.py:L83 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state()]
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=agent/transport.py:L73 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()]
- "agent_transport_transport_bootstrap": ".bootstrap()" | kind=code-symbol | source=agent/transport.py:L307 | neighbors=[Register using a manager-side shared bo…, Transport, .save_state(), TransportError]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=agent/transport.py:L672 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=agent/transport.py:L542 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError]
- "agent_transport_transport_refresh_device_access": ".refresh_device_access()" | kind=code-symbol | source=agent/transport.py:L397 | neighbors=[Transport, .ensure_device_access(), .load_state(), .update_state()]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=agent/transport.py:L252 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=agent/transport.py:L239 | neighbors=[Transport, .bootstrap(), .register(), .update_state()]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=agent/transport.py:L581 | neighbors=[Submit a scan result to the manager.   …, Transport, _strip_nul(), .ensure_device_access()]
- "branch:repo:local/probe@20f2a9dc#main": "main" | kind=Branch | source=git | neighbors=[56508b2 Add unit tests for XML parsing,…, a1430fb Add local_run.py for direct pro…, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…]
- "main_scripts_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=main_scripts/adaptive_timeout.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, AdaptiveTimeout, from_rtts(), test_main_scripts_adaptive_timeout.py]
- "main_scripts_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=main_scripts/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "main_scripts_delta_scanner_delta": "Delta" | kind=code-symbol | source=main_scripts/delta_scanner.py:L69 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…]
- "main_scripts_findings_as_dict": "_as_dict()" | kind=code-symbol | source=main_scripts/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "main_scripts_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=main_scripts/findings.py:L254 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=main_scripts/findings.py:L277 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_ssh": "_rule_ssh()" | kind=code-symbol | source=main_scripts/findings.py:L564 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_tls": "_rule_tls()" | kind=code-symbol | source=main_scripts/findings.py:L175 | neighbors=[findings.py, _data(), Finding, _scanner()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-020.json

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
