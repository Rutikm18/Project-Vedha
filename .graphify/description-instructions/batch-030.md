# Node Description Batch 31 of 104

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

- "agent_agent_scanningagent_heartbeat_loop": "._heartbeat_loop()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L658 | neighbors=[ScanningAgent, ._api_call(), .run()]
- "agent_agent_scanningagent_init": ".__init__()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L640 | neighbors=[ScanningAgent, build_ssl_context(), VaultCredentialFetcher]
- "agent_agent_submitwithspool": ".submitWithSpool()" | kind=code-symbol | source=probe-go/agent/agent.go:L262 | neighbors=[agent.py, .runPollLoop(), say()]
- "agent_agent_vaultcredentialfetcher_get_credentials": ".get_credentials()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L81 | neighbors=[Read a KV-v2 secret from Vault., ._execute_job(), VaultCredentialFetcher]
- "agent_cli_cmd_auth_logout": "cmd_auth_logout()" | kind=code-symbol | source=probe/agent/cli.py:L288 | neighbors=[cli.py, ConfigStore, .remove_profile()]
- "agent_cli_cmd_daemon_run": "cmd_daemon_run()" | kind=code-symbol | source=probe/agent/cli.py:L532 | neighbors=[cli.py, resolve_profile(), split_values()]
- "agent_cli_configstore_get_profile": ".get_profile()" | kind=code-symbol | source=probe/agent/cli.py:L83 | neighbors=[ConfigStore, .load(), resolve_profile()]
- "agent_cli_configstore_save": ".save()" | kind=code-symbol | source=probe/agent/cli.py:L71 | neighbors=[ConfigStore, .remove_profile(), .set_profile()]
- "agent_cli_default_config_path": "default_config_path()" | kind=code-symbol | source=probe/agent/cli.py:L36 | neighbors=[cli.py, build_parser(), _env()]
- "agent_cli_parse_param_pairs": "parse_param_pairs()" | kind=code-symbol | source=probe/agent/cli.py:L161 | neighbors=[cli.py, cmd_scan_run(), CliError]
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L76 | neighbors=[engine.py, Coerce val to float and clamp to [lo, h…, _tuning_from_params()]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L144 | neighbors=[engine.py, Count concrete open services, not gener…, run_scan()]
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L28 | neighbors=[engine.py, Single factory for error result dicts —…, run_scan()]
- "agent_hw_bind_get_hw_id": "get_hw_id()" | kind=code-symbol | source=probe/agent/hw_bind.py:L23 | neighbors=[hw_bind.py, check_hw_bind(), Deterministic per-machine fingerprint b…]
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L104 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…]
- "agent_result_spool_resultspool_flush_spool": ".flush_spool()" | kind=code-symbol | source=probe/agent/result_spool.py:L129 | neighbors=[Re-attempt upload of all previously spo…, ResultSpool, .exists()]
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L65 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists()]
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=probe/agent/result_spool.py:L39 | neighbors=[Atomically write a result payload to th…, ResultSpool, .submit_with_retry()]
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=probe/agent/result_spool.py:L152 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists()]
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L82 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .save()]
- "agent_scope_crypt_decrypt_scope": "decrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L97 | neighbors=[scope_crypt.py, decrypt_scope_b64(), Decrypt a scope blob using the probe's …]
- "agent_scope_crypt_decrypt_scope_b64": "decrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L155 | neighbors=[scope_crypt.py, decrypt_scope(), decrypt_scope() accepting a base64 stri…]
- "agent_scope_crypt_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L55 | neighbors=[scope_crypt.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…]
- "agent_scope_crypt_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L150 | neighbors=[scope_crypt.py, encrypt_scope(), encrypt_scope() returning a base64 stri…]
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=probe/agent/task_runner.py:L29 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job()]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L282 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job()]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L329 | neighbors=[Establish an authenticated WebSocket co…, Transport, TransportError]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L214 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, TransportError]
- "ai_agent_agentdecisionengine_list_findings": "._list_findings()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L283 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), _val()]
- "ai_agent_val": "_val()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L382 | neighbors=[agent.py, ._list_findings(), ._overview()]
- "ai_hallucination": "hallucination.py" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[HallucinationGuard, HallucinationGuard — post-generation va…, 298a9d4 trim frontend to 7 core pages; …]
- "ai_hallucination_hallucinationguard_validate_cve_claims": ".validate_cve_claims()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L45 | neighbors=[HallucinationGuard, .validate(), Flag any CVE ID mentioned in ``text`` t…]
- "ai_hallucination_hallucinationguard_validate_cvss_scores": ".validate_cvss_scores()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L60 | neighbors=[HallucinationGuard, .validate(), Flag CVSS scores in the text that don't…]
- "ai_hallucination_hallucinationguard_validate_remediation_commands": ".validate_remediation_commands()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L89 | neighbors=[HallucinationGuard, .validate(), Flag destructive-looking commands that …]
- "ai_llm_report_enum": "_enum()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L310 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding()]
- "ai_llm_report_finding_scores": "_finding_scores()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L321 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding()]
- "ai_llm_report_llmreportgenerator_complete": "._complete()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L110 | neighbors=[LLMReportGenerator, LLMUnavailableError, ._generate_and_store()]
- "ai_llm_report_llmreportgenerator_generate_executive_summary": ".generate_executive_summary()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L171 | neighbors=[LLMReportGenerator, _collect_cves_scores(), ._generate_and_store()]
- "ai_prioritizer_vulnprioritizer_formula_contributions": "._formula_contributions()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L191 | neighbors=[VulnPrioritizer, .explain_prediction(), .fallback_score()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-030.json

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
