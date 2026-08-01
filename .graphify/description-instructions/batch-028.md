# Node Description Batch 29 of 119

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

- "ad_kerberoast_kerberoastchecker_request_tgs": ".request_tgs()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L85 | neighbors=[KerberoastChecker, ._encode_tgs_rep(), Request a TGS for ``spn`` and return th…, Request a TGS for ``spn`` and return th…]
- "ad_ldap_enum_adcomputer": "ADComputer" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L67 | neighbors=[ldap_enum.py, ADConnectionError, DependencyMissingError, .get_computers()]
- "ad_ldap_enum_adgroup": "ADGroup" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L76 | neighbors=[ldap_enum.py, ADConnectionError, DependencyMissingError, .get_groups()]
- "ad_ldap_enum_domain_to_base_dn": "_domain_to_base_dn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L104 | neighbors=[ldap_enum.py, .connect(), corp.local -> DC=corp,DC=local, corp.local -> DC=corp,DC=local]
- "ad_ldap_enum_ldapenumerator_check_anonymous_bind": ".check_anonymous_bind()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L285 | neighbors=[LDAPEnumerator, .unbind(), True if the DC accepts an anonymous bin…, True if the DC accepts an anonymous bin…]
- "ad_ldap_enum_ldapenumerator_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L127 | neighbors=[LDAPEnumerator, _domain_to_base_dn(), Bind to the domain controller. Returns …, Bind to the domain controller. Returns …]
- "ad_ldap_enum_ldapenumerator_get_computers": ".get_computers()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L239 | neighbors=[LDAPEnumerator, ADComputer, ._attr(), ._search()]
- "ad_ntlm_relay": "ntlm_relay.py" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L1 | neighbors=[NTLMRelayChecker, NTLMRelayChecker — detect missing SMB/L…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[ADAssessmentRunner, ADAssessmentRunner — runs the full Acti…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L45 | neighbors=[agent.py, main(), Return an integer environment setting c…, Return an integer environment setting c…]
- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=probe/agent/agent.py:L469 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop(), Acknowledge an offer without executing …]
- "agent_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/agent/cli.py:L931 | neighbors=[cli.py, default_config_path(), _env(), main()]
- "agent_cli_cmd_agents_list": "cmd_agents_list()" | kind=code-symbol | source=probe/agent/cli.py:L407 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_list": "cmd_engagements_list()" | kind=code-symbol | source=probe/agent/cli.py:L424 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_scope": "cmd_engagements_scope()" | kind=code-symbol | source=probe/agent/cli.py:L472 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_scan_status": "cmd_scan_status()" | kind=code-symbol | source=probe/agent/cli.py:L528 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_use_cases": "cmd_use_cases()" | kind=code-symbol | source=probe/agent/cli.py:L391 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_configstore_remove_profile": ".remove_profile()" | kind=code-symbol | source=probe/agent/cli.py:L94 | neighbors=[cmd_auth_logout(), ConfigStore, .load(), .save()]
- "agent_cli_configstore_set_profile": ".set_profile()" | kind=code-symbol | source=probe/agent/cli.py:L88 | neighbors=[cmd_auth_login(), ConfigStore, .load(), .save()]
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=probe/agent/engine.py:L167 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan()]
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=probe/agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…]
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…]
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L101 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…, Combined startup gauntlet: HW bind → li…]
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L41 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()]
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=probe/agent/result_spool.py:L179 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists(), Number of pending (unsubmitted) results…]
- "agent_result_spool_resultspool_sync_directory": "._sync_directory()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .remove(), .save(), .exists()]
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()]
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target(), Remove targets that fall inside any exc…]
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target(), Fetch the engagement's authoritative sc…]
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=probe/agent/task_runner.py:L27 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job(), Structured result from running one scan…]
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=probe/agent/task_runner.py:L46 | neighbors=[Args:             http_get:       Callb…, TaskRunner, Args:             http_get:       Callb…, Args:             http_get:       Callb…]
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=probe/agent/transport.py:L34 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()]
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=probe/agent/transport.py:L350 | neighbors=[Fetch the engagement's authoritative sc…, Transport, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…]
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L307 | neighbors=[Send a heartbeat to the manager.       …, Transport, Send a heartbeat to the manager.       …, Send a heartbeat to the manager.       …]
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=probe/agent/transport.py:L420 | neighbors=[Generic authenticated GET, returns pars…, Transport, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…]
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=probe/agent/transport.py:L162 | neighbors=[True if we have both an agent_id and a …, Transport, True if we have both an agent_id and a …, True if we have both an agent_id and a …]
- "agent_transport_transport_is_ws_connected": ".is_ws_connected()" | kind=code-symbol | source=probe/agent/transport.py:L476 | neighbors=[True if the WebSocket connection is act…, Transport, True if the WebSocket connection is act…, Fetch the engagement's authoritative sc…]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L267 | neighbors=[Refresh routing metadata using the cach…, Transport, TransportError, Refresh routing metadata using the cach…]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L369 | neighbors=[Submit a scan result to the manager.   …, Transport, Submit a scan result to the manager.   …, Submit a scan result to the manager.   …]
- "agent_transport_transport_ws_url": ".ws_url()" | kind=code-symbol | source=probe/agent/transport.py:L436 | neighbors=[Return the WebSocket endpoint without e…, Transport, Return the WebSocket endpoint without e…, Return the WebSocket connection URL wit…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-028.json

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
