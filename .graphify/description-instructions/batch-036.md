# Node Description Batch 37 of 119

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
- "ad_ldap_enum_rationale_85": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L85 | neighbors=[ADConnectionError, DependencyMissingError, ACE]
- "ad_ldap_enum_rationale_86": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L86 | neighbors=[ADConnectionError, DependencyMissingError, ACE]
- "ad_ntlm_relay_ntlmrelaychecker_check_smb_signing": ".check_smb_signing()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L38 | neighbors=[NTLMRelayChecker, ._probe_smb_host(), For each IP, returns {signing_enabled, …]
- "ad_orchestrator_adassessmentrunner_run": ".run()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L50 | neighbors=[ADAssessmentRunner, ._anonymous_bind_finding(), Returns {findings: [...], stats: {...},…]
- "agent_agent_is_local_manager_url": "_is_local_manager_url()" | kind=code-symbol | source=probe/agent/agent.py:L54 | neighbors=[agent.py, main(), Recognize only explicit single-host dev…]
- "agent_agent_runautonomousengagement": "runAutonomousEngagement()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L95 | neighbors=[agent.py, isBlocked(), requiresApproval()]
- "agent_cli_cmd_auth_logout": "cmd_auth_logout()" | kind=code-symbol | source=probe/agent/cli.py:L290 | neighbors=[cli.py, ConfigStore, .remove_profile()]
- "agent_cli_cmd_daemon_run": "cmd_daemon_run()" | kind=code-symbol | source=probe/agent/cli.py:L911 | neighbors=[cli.py, resolve_profile(), split_values()]
- "agent_cli_configstore_get_profile": ".get_profile()" | kind=code-symbol | source=probe/agent/cli.py:L85 | neighbors=[ConfigStore, .load(), resolve_profile()]
- "agent_cli_configstore_save": ".save()" | kind=code-symbol | source=probe/agent/cli.py:L73 | neighbors=[ConfigStore, .remove_profile(), .set_profile()]
- "agent_cli_default_config_path": "default_config_path()" | kind=code-symbol | source=probe/agent/cli.py:L38 | neighbors=[cli.py, build_parser(), _env()]
- "agent_cli_fetch_all_findings": "_fetch_all_findings()" | kind=code-symbol | source=probe/agent/cli.py:L547 | neighbors=[cli.py, cmd_validate(), .request()]
- "agent_cli_parse_param_pairs": "parse_param_pairs()" | kind=code-symbol | source=probe/agent/cli.py:L163 | neighbors=[cli.py, cmd_scan_run(), CliError]
- "agent_engine_applied_tuning": "_applied_tuning()" | kind=code-symbol | source=probe/agent/engine.py:L304 | neighbors=[engine.py, _build_run_stats(), Serialize effective limits without ever…]
- "agent_engine_hosts_from_facts": "_hosts_from_facts()" | kind=code-symbol | source=probe/agent/engine.py:L256 | neighbors=[engine.py, _build_run_stats(), Build promotion-ready hosts without dup…]
- "agent_engine_runtime_manifest": "_runtime_manifest()" | kind=code-symbol | source=probe/agent/engine.py:L60 | neighbors=[engine.py, _error_result(), run_scan()]
- "agent_engine_string_list": "_string_list()" | kind=code-symbol | source=probe/agent/engine.py:L132 | neighbors=[engine.py, run_scan(), _targets()]
- "agent_engine_targets": "_targets()" | kind=code-symbol | source=probe/agent/engine.py:L148 | neighbors=[engine.py, run_scan(), _string_list()]
- "agent_hw_bind_get_hw_id": "get_hw_id()" | kind=code-symbol | source=probe/agent/hw_bind.py:L23 | neighbors=[hw_bind.py, check_hw_bind(), Deterministic per-machine fingerprint b…]
- "agent_scope_crypt_decrypt_scope": "decrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L97 | neighbors=[scope_crypt.py, decrypt_scope_b64(), Decrypt a scope blob using the probe's …]
- "agent_scope_crypt_decrypt_scope_b64": "decrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L155 | neighbors=[scope_crypt.py, decrypt_scope(), decrypt_scope() accepting a base64 stri…]
- "agent_scope_crypt_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L55 | neighbors=[scope_crypt.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…]
- "agent_scope_crypt_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L150 | neighbors=[scope_crypt.py, encrypt_scope(), encrypt_scope() returning a base64 stri…]
- "agent_scope_validator_fetch_engagement_scope": "fetch_engagement_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L54 | neighbors=[scope_validator.py, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…]
- "agent_scope_validator_merge_exclusions": "merge_exclusions()" | kind=code-symbol | source=probe/agent/scope_validator.py:L154 | neighbors=[scope_validator.py, Merge engagement-level exclusions with …, Merge engagement-level exclusions with …]
- "agent_transport_transport_load_state": ".load_state()" | kind=code-symbol | source=probe/agent/transport.py:L168 | neighbors=[Transport, .__init__(), .update_state()]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L199 | neighbors=[Transport, .register(), .update_state()]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L118 | neighbors=[use_cases.py, Return (scan_type, profile) for a job. …, Return (scan_type, profile) for a job. …]
- "agent_validation_validate_ground_truth": "validate_ground_truth()" | kind=code-symbol | source=probe/agent/validation.py:L106 | neighbors=[validation.py, Validate the small, explicit inventory …, score_inventory()]
- "ai_agent_agentdecisionengine_list_findings": "._list_findings()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L283 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), _val()]
- "ai_agent_val": "_val()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L382 | neighbors=[agent.py, ._list_findings(), ._overview()]
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
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-036.json

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
