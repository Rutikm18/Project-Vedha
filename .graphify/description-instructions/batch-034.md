# Node Description Batch 35 of 119

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

- "ad_ldap_enum_domain_to_base_dn": "_domain_to_base_dn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L105 | neighbors=[ldap_enum.py, .connect(), corp.local -> DC=corp,DC=local]
- "ad_ldap_enum_ldapenumerator_check_anonymous_bind": ".check_anonymous_bind()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L286 | neighbors=[LDAPEnumerator, .unbind(), True if the DC accepts an anonymous bin…]
- "ad_ldap_enum_ldapenumerator_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L128 | neighbors=[LDAPEnumerator, _domain_to_base_dn(), Bind to the domain controller. Returns …]
- "ad_ldap_enum_ldapenumerator_parse_security_descriptor": "._parse_security_descriptor()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L344 | neighbors=[LDAPEnumerator, .get_aces(), ACE]
- "ad_ldap_enum_ldapenumerator_require_conn": "._require_conn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L189 | neighbors=[LDAPEnumerator, .get_aces(), ._search()]
- "ad_ldap_enum_rationale_1": "LDAPEnumerator — read-only Active Directory enumeration over LDAP/LDAPS.  Uses l" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ADConnectionError, DependencyMissingError, ldap_enum.py]
- "ad_ldap_enum_rationale_106": "corp.local -> DC=corp,DC=local" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L106 | neighbors=[ADConnectionError, DependencyMissingError, _domain_to_base_dn()]
- "ad_ldap_enum_rationale_119": "Read-only AD enumeration. One instance == one bound connection." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L119 | neighbors=[ADConnectionError, DependencyMissingError, LDAPEnumerator]
- "ad_ldap_enum_rationale_138": "Bind to the domain controller. Returns self for chaining.          Raises Depend" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L138 | neighbors=[ADConnectionError, DependencyMissingError, .connect()]
- "ad_ldap_enum_rationale_215": "All user accounts (excludes computer accounts)." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L215 | neighbors=[ADConnectionError, DependencyMissingError, .get_users()]
- "ad_ldap_enum_rationale_287": "True if the DC accepts an anonymous bind that can read directory data         (a" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L287 | neighbors=[ADConnectionError, DependencyMissingError, .check_anonymous_bind()]
- "ad_ldap_enum_rationale_312": "Parse the nTSecurityDescriptor of an object into a list of ACEs for ACL" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L312 | neighbors=[ADConnectionError, DependencyMissingError, .get_aces()]
- "ad_ldap_enum_rationale_86": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L86 | neighbors=[ADConnectionError, DependencyMissingError, ACE]
- "ad_ntlm_relay_ntlmrelaychecker_check_smb_signing": ".check_smb_signing()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L38 | neighbors=[NTLMRelayChecker, ._probe_smb_host(), For each IP, returns {signing_enabled, …]
- "ad_orchestrator_adassessmentrunner_run": ".run()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L50 | neighbors=[ADAssessmentRunner, ._anonymous_bind_finding(), Returns {findings: [...], stats: {...},…]
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L44 | neighbors=[agent.py, main(), Return an integer environment setting c…]
- "agent_agent_dedupstrings": "dedupStrings()" | kind=code-symbol | source=probe-go/agent/agent.go:L895 | neighbors=[agent.py, mapToJob(), stringList()]
- "agent_agent_firsttargetlist": "firstTargetList()" | kind=code-symbol | source=probe-go/agent/agent.go:L846 | neighbors=[agent.py, stringList(), mapToJob()]
- "agent_agent_heartbeatwithretry": ".heartbeatWithRetry()" | kind=code-symbol | source=probe-go/agent/agent.go:L515 | neighbors=[agent.py, .runPolledJob(), .runPollLoop()]
- "agent_agent_normalizeresultpayload": "normalizeResultPayload()" | kind=code-symbol | source=probe-go/agent/agent.go:L630 | neighbors=[agent.py, .flushSpool(), resultPayload()]
- "agent_agent_obtainidentity": ".obtainIdentity()" | kind=code-symbol | source=probe-go/agent/agent.go:L641 | neighbors=[agent.py, say(), .Run()]
- "agent_agent_resulttomap": "resultToMap()" | kind=code-symbol | source=probe-go/agent/agent.go:L574 | neighbors=[agent.py, .rejectJob(), .runJob()]
- "agent_agent_runautonomousengagement": "runAutonomousEngagement()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L95 | neighbors=[agent.py, isBlocked(), requiresApproval()]
- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=probe/agent/agent.py:L462 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop()]
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
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L104 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…]
- "agent_scope_crypt_decrypt_scope": "decrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L97 | neighbors=[scope_crypt.py, decrypt_scope_b64(), Decrypt a scope blob using the probe's …]
- "agent_scope_crypt_decrypt_scope_b64": "decrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L155 | neighbors=[scope_crypt.py, decrypt_scope(), decrypt_scope() accepting a base64 stri…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-034.json

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
