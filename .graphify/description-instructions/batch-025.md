# Node Description Batch 26 of 92

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

- "tests_test_wire_identity_testmoduleconstantsunbranded": "TestModuleConstantsUnbranded" | kind=code-symbol | source=tests/test_wire_identity.py:L80 | neighbors=[test_wire_identity.py, Import-time probe constants built from …, .test_iot_rtsp_options(), .test_service_banner_http_probe()]
- "tests_test_workflow_execution_concurrencyscanner": "_ConcurrencyScanner" | kind=code-symbol | source=tests/test_workflow_execution.py:L46 | neighbors=[test_workflow_execution.py, .__init__(), .scan_target(), test_host_fanout_is_bounded()]
- "tools_issue_license_main": "main()" | kind=code-symbol | source=tools/issue_license.py:L75 | neighbors=[issue_license.py, issue(), keygen(), pubkey()]
- "workflow_asset_parse_ts": "_parse_ts()" | kind=code-symbol | source=workflow/asset.py:L31 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_asset_portfact": "PortFact" | kind=code-symbol | source=workflow/asset.py:L36 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_cache_cacheentry": "CacheEntry" | kind=code-symbol | source=workflow/cache.py:L55 | neighbors=[cache.py, .from_jsonl_dict(), .to_jsonl_dict(), .put()]
- "workflow_cli_main": "_main()" | kind=code-symbol | source=workflow/cli.py:L95 | neighbors=[cli.py, _build_creds(), _build_mode(), build_parser()]
- "workflow_execution_classify_scanner_error": "classify_scanner_error()" | kind=code-symbol | source=workflow/execution.py:L153 | neighbors=[execution.py, ErrorDetail, Map low-level failures into stable, ope…, scanner_failure_result()]
- "workflow_execution_executiontrace_ensure": "._ensure()" | kind=code-symbol | source=workflow/execution.py:L239 | neighbors=[ExecutionTrace, .__init__(), .record(), .skip()]
- "workflow_router_looks_like_db": "looks_like_db()" | kind=code-symbol | source=workflow/router.py:L62 | neighbors=[router.py, looks_like_http(), True when a service banner carries a da…, route_branches()]
- "agent_agent_is_local_manager_url": "_is_local_manager_url()" | kind=code-symbol | source=agent/agent.py:L56 | neighbors=[agent.py, main(), Recognize only explicit single-host dev…]
- "agent_agent_job_intent": "_job_intent()" | kind=code-symbol | source=agent/agent.py:L92 | neighbors=[agent.py, Human label for what a job will actuall…, _ws_run_job()]
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=agent/agent.py:L64 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…]
- "agent_agent_load_or_create_signing_identity": "_load_or_create_signing_identity()" | kind=code-symbol | source=agent/agent.py:L1024 | neighbors=[agent.py, _obtain_identity(), Load or atomically create the probe's E…]
- "agent_agent_poll_jobs_or_empty": "_poll_jobs_or_empty()" | kind=code-symbol | source=agent/agent.py:L198 | neighbors=[agent.py, main(), Poll for work. Auth failures (Transport…]
- "agent_agent_ws_heartbeat_sender": "_ws_heartbeat_sender()" | kind=code-symbol | source=agent/agent.py:L845 | neighbors=[agent.py, Send periodic heartbeats over WebSocket., _run_ws_push_loop()]
- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=agent/agent.py:L691 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop()]
- "agent_cli_cmd_auth_logout": "cmd_auth_logout()" | kind=code-symbol | source=agent/cli.py:L290 | neighbors=[cli.py, ConfigStore, .remove_profile()]
- "agent_cli_cmd_daemon_run": "cmd_daemon_run()" | kind=code-symbol | source=agent/cli.py:L911 | neighbors=[cli.py, resolve_profile(), split_values()]
- "agent_cli_configstore_get_profile": ".get_profile()" | kind=code-symbol | source=agent/cli.py:L85 | neighbors=[ConfigStore, .load(), resolve_profile()]
- "agent_cli_configstore_save": ".save()" | kind=code-symbol | source=agent/cli.py:L73 | neighbors=[ConfigStore, .remove_profile(), .set_profile()]
- "agent_cli_default_config_path": "default_config_path()" | kind=code-symbol | source=agent/cli.py:L38 | neighbors=[cli.py, build_parser(), _env()]
- "agent_cli_fetch_all_findings": "_fetch_all_findings()" | kind=code-symbol | source=agent/cli.py:L547 | neighbors=[cli.py, cmd_validate(), .request()]
- "agent_cli_parse_param_pairs": "parse_param_pairs()" | kind=code-symbol | source=agent/cli.py:L163 | neighbors=[cli.py, cmd_scan_run(), CliError]
- "agent_device_identity_verify_site_policy": "verify_site_policy()" | kind=code-symbol | source=agent/device_identity.py:L37 | neighbors=[device_identity.py, Verify a Manager-signed policy and retu…, decode_key()]
- "agent_engine_run_with_cancellation": "_run_with_cancellation()" | kind=code-symbol | source=agent/engine.py:L518 | neighbors=[engine.py, run_scan(), LeaseLostError]
- "agent_engine_runtime_manifest": "_runtime_manifest()" | kind=code-symbol | source=agent/engine.py:L65 | neighbors=[engine.py, _error_result(), run_scan()]
- "agent_engine_string_list": "_string_list()" | kind=code-symbol | source=agent/engine.py:L171 | neighbors=[engine.py, run_scan(), _targets()]
- "agent_engine_targets": "_targets()" | kind=code-symbol | source=agent/engine.py:L187 | neighbors=[engine.py, run_scan(), _string_list()]
- "agent_hw_bind_get_hw_id": "get_hw_id()" | kind=code-symbol | source=agent/hw_bind.py:L23 | neighbors=[hw_bind.py, check_hw_bind(), Deterministic per-machine fingerprint b…]
- "agent_init": "__init__.py" | kind=code-symbol | source=agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…]
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=agent/license.py:L101 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…]
- "agent_local_run_clean": "_clean()" | kind=code-symbol | source=agent/local_run.py:L68 | neighbors=[local_run.py, Drop internal bookkeeping keys (_collec…, summarize()]
- "agent_local_run_parse_args": "_parse_args()" | kind=code-symbol | source=agent/local_run.py:L120 | neighbors=[local_run.py, _main(), Validate positional args (args[0]=targe…]
- "agent_local_run_port_label": "_port_label()" | kind=code-symbol | source=agent/local_run.py:L75 | neighbors=[local_run.py, Render a port fact unambiguously: '445/…, summarize()]
- "agent_local_run_ports_from_env": "_ports_from_env()" | kind=code-symbol | source=agent/local_run.py:L42 | neighbors=[local_run.py, _main(), Resolve the port set from PROBE_LOCAL_P…]
- "agent_local_run_run": "run()" | kind=code-symbol | source=agent/local_run.py:L199 | neighbors=[local_run.py, Synchronous entrypoint for the `local-r…, _main()]
- "agent_local_run_usage_error": "_usage_error()" | kind=code-symbol | source=agent/local_run.py:L109 | neighbors=[local_run.py, _main(), Actionable input error on stderr → exit…]
- "agent_result_spool_resultspool_spool_bytes": ".spool_bytes()" | kind=code-symbol | source=agent/result_spool.py:L222 | neighbors=[Total bytes held by pending result file…, ResultSpool, .exists()]
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=agent/result_spool.py:L215 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-025.json

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
