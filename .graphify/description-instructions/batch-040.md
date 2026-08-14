# Node Description Batch 41 of 186

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

- "ad_ldap_enum_adcomputer": "ADComputer" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L67 | neighbors=[ldap_enum.py, .get_computers(), ADConnectionError, DependencyMissingError]
- "ad_ldap_enum_adgroup": "ADGroup" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L76 | neighbors=[ldap_enum.py, .get_groups(), ADConnectionError, DependencyMissingError]
- "ad_ldap_enum_domain_to_base_dn": "_domain_to_base_dn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L104 | neighbors=[ldap_enum.py, .connect(), corp.local -> DC=corp,DC=local, corp.local -> DC=corp,DC=local]
- "ad_ldap_enum_ldapenumerator_check_anonymous_bind": ".check_anonymous_bind()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L285 | neighbors=[LDAPEnumerator, .unbind(), True if the DC accepts an anonymous bin…, True if the DC accepts an anonymous bin…]
- "ad_ldap_enum_ldapenumerator_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L127 | neighbors=[LDAPEnumerator, _domain_to_base_dn(), Bind to the domain controller. Returns …, Bind to the domain controller. Returns …]
- "ad_ldap_enum_ldapenumerator_get_computers": ".get_computers()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L239 | neighbors=[LDAPEnumerator, ADComputer, ._attr(), ._search()]
- "ad_ntlm_relay": "ntlm_relay.py" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L1 | neighbors=[NTLMRelayChecker, NTLMRelayChecker — detect missing SMB/L…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[ADAssessmentRunner, ADAssessmentRunner — runs the full Acti…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "agent_agent_is_local_manager_url": "_is_local_manager_url()" | kind=code-symbol | source=probe/agent/agent.py:L56 | neighbors=[agent.py, main(), Recognize only explicit single-host dev…, Recognize only explicit single-host dev…]
- "agent_agent_load_or_create_signing_identity": "_load_or_create_signing_identity()" | kind=code-symbol | source=probe/agent/agent.py:L879 | neighbors=[agent.py, _obtain_identity(), Load or atomically create the probe's E…, Load or atomically create the probe's E…]
- "agent_agent_poll_jobs_or_empty": "_poll_jobs_or_empty()" | kind=code-symbol | source=probe/agent/agent.py:L80 | neighbors=[agent.py, main(), say(), Return no work for transient poll failu…]
- "agent_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/agent/cli.py:L931 | neighbors=[cli.py, default_config_path(), _env(), main()]
- "agent_cli_cmd_agents_list": "cmd_agents_list()" | kind=code-symbol | source=probe/agent/cli.py:L407 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_list": "cmd_engagements_list()" | kind=code-symbol | source=probe/agent/cli.py:L424 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_scope": "cmd_engagements_scope()" | kind=code-symbol | source=probe/agent/cli.py:L472 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_scan_status": "cmd_scan_status()" | kind=code-symbol | source=probe/agent/cli.py:L528 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_use_cases": "cmd_use_cases()" | kind=code-symbol | source=probe/agent/cli.py:L391 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_configstore_remove_profile": ".remove_profile()" | kind=code-symbol | source=probe/agent/cli.py:L94 | neighbors=[cmd_auth_logout(), ConfigStore, .load(), .save()]
- "agent_cli_configstore_set_profile": ".set_profile()" | kind=code-symbol | source=probe/agent/cli.py:L88 | neighbors=[cmd_auth_login(), ConfigStore, .load(), .save()]
- "agent_engine_scan_method_for": "_scan_method_for()" | kind=code-symbol | source=probe/agent/engine.py:L147 | neighbors=[engine.py, _applied_tuning(), syn' for wide sweeps (deep intensity / …, run_scan()]
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=probe/agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…]
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…]
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L101 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…, Combined startup gauntlet: HW bind → li…]
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L41 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()]
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()]
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target(), Remove targets that fall inside any exc…]
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target(), Fetch the engagement's authoritative sc…]
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=probe/agent/task_runner.py:L27 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job(), Structured result from running one scan…]
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=probe/agent/task_runner.py:L46 | neighbors=[Args:             http_get:       Callb…, TaskRunner, Args:             http_get:       Callb…, Args:             http_get:       Callb…]
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=probe/agent/transport.py:L35 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()]
- "agent_transport_transport_bootstrap": ".bootstrap()" | kind=code-symbol | source=probe/agent/transport.py:L269 | neighbors=[Register using a manager-side shared bo…, Transport, .save_state(), TransportError]
- "agent_transport_transport_refresh_device_access": ".refresh_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L353 | neighbors=[Transport, .ensure_device_access(), .load_state(), .update_state()]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L201 | neighbors=[Transport, .bootstrap(), .register(), .update_state()]
- "agent_use_cases_as_int": "_as_int()" | kind=code-symbol | source=probe/agent/use_cases.py:L195 | neighbors=[use_cases.py, normalize_intensity(), Coerce an int-or-numeric-string to int,…, use_case_for_code()]
- "agent_use_cases_normalize_intensity": "normalize_intensity()" | kind=code-symbol | source=probe/agent/use_cases.py:L217 | neighbors=[use_cases.py, _as_int(), Accept an intensity as a number (1/2/3)…, resolve()]
- "agent_use_cases_use_case_for_code": "use_case_for_code()" | kind=code-symbol | source=probe/agent/use_cases.py:L206 | neighbors=[use_cases.py, Map a numeric use-case code → use_case_…, resolve(), _as_int()]
- "ai_agent_agentdecisionengine_overview": "._overview()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L264 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), ._count(), _val()]
- "ai_agent_agentdecisionengine_persist": "._persist()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L336 | neighbors=[AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), .run()]
- "ai_hallucination": "hallucination.py" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[HallucinationGuard, HallucinationGuard — post-generation va…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ai_llm_report_llmreportgenerator_generate_remediation_steps": ".generate_remediation_steps()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L222 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-040.json

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
