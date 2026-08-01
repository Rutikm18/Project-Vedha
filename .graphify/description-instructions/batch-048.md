# Node Description Batch 49 of 119

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "ad_ldap_enum_ldapenumerator_unbind": ".unbind()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L379 | neighbors=[LDAPEnumerator, .check_anonymous_bind()] | lang=en
- "ad_ntlm_relay_ntlmrelaychecker_check_ldap_signing": ".check_ldap_signing()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L80 | neighbors=[NTLMRelayChecker, Returns True if the DC *enforces* LDAP …] | lang=en
- "ad_ntlm_relay_ntlmrelaychecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L113 | neighbors=[NTLMRelayChecker, Build a Finding for hosts missing SMB s…] | lang=en
- "ad_ntlm_relay_ntlmrelaychecker_probe_smb_host": "._probe_smb_host()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L60 | neighbors=[NTLMRelayChecker, .check_smb_signing()] | lang=en
- "ad_ntlm_relay_rationale_1": "NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L1 | neighbors=[ntlm_relay.py, FindingSeverity] | lang=en
- "ad_ntlm_relay_rationale_118": "Build a Finding for hosts missing SMB signing. The attack_narrative         incl" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L118 | neighbors=[.generate_finding(), FindingSeverity] | lang=en
- "ad_ntlm_relay_rationale_31": "Probe SMB/LDAP signing posture across a host list." | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L31 | neighbors=[NTLMRelayChecker, FindingSeverity] | lang=pt
- "ad_ntlm_relay_rationale_39": "For each IP, returns {signing_enabled, signing_required}.          A host is rel" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L39 | neighbors=[.check_smb_signing(), FindingSeverity] | lang=en
- "ad_ntlm_relay_rationale_81": "Returns True if the DC *enforces* LDAP signing / channel binding.          We at" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L81 | neighbors=[.check_ldap_signing(), FindingSeverity] | lang=en
- "ad_orchestrator_adassessmentrunner_anonymous_bind_finding": "._anonymous_bind_finding()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L186 | neighbors=[ADAssessmentRunner, .run()] | lang=en
- "agent_agent_isblocked": "isBlocked()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L62 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_agent_rationale_470": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L470 | neighbors=[_ws_stage_job_offer(), _ws_heartbeat_sender()] | lang=en
- "agent_agent_requiresapproval": "requiresApproval()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L54 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_cli_cmd_whoami": "cmd_whoami()" | kind=code-symbol | source=probe/agent/cli.py:L296 | neighbors=[cli.py, cmd_auth_status()] | lang=en
- "agent_cli_doctor_check": "_doctor_check()" | kind=code-symbol | source=probe/agent/cli.py:L300 | neighbors=[cli.py, cmd_doctor()] | lang=en
- "agent_cli_main": "main()" | kind=code-symbol | source=probe/agent/cli.py:L1129 | neighbors=[cli.py, build_parser()] | lang=en
- "agent_cli_manager_is_local": "_manager_is_local()" | kind=code-symbol | source=probe/agent/cli.py:L568 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_cli_managerclient_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L104 | neighbors=[ManagerClient, normalize_manager_url()] | lang=en
- "agent_cli_write_private_json": "_write_private_json()" | kind=code-symbol | source=probe/agent/cli.py:L534 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_engine_env_number": "_env_number()" | kind=code-symbol | source=probe/agent/engine.py:L45 | neighbors=[engine.py, Read a bounded numeric safety setting w…] | lang=en
- "agent_engine_facts_from_cache": "_facts_from_cache()" | kind=code-symbol | source=probe/agent/engine.py:L252 | neighbors=[engine.py, run_scan()] | lang=en
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=probe/agent/license.py:L45 | neighbors=[license.py, verify_license()] | lang=en
- "agent_scope_crypt_bytes_to_pubkey_b64": "bytes_to_pubkey_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L165 | neighbors=[scope_crypt.py, Encode raw X25519 public key bytes to a…] | lang=en
- "agent_scope_crypt_generate_identity": "generate_identity()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L43 | neighbors=[scope_crypt.py, Generate a fresh X25519 keypair.      R…] | lang=en
- "agent_scope_crypt_pubkey_to_bytes": "pubkey_to_bytes()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L160 | neighbors=[scope_crypt.py, Decode a base64-encoded X25519 public k…] | lang=en
- "agent_scope_validator_rationale_58": "Fetch the engagement's authoritative scope from the manager.      Args:" | kind=entity | source=probe/agent/scope_validator.py:L58 | neighbors=[fetch_engagement_scope(), validate_targets_in_scope()] | lang=en
- "agent_tools_agentstate": "AgentState" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L15 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_persistagentfindings": "persistAgentFindings()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L313 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_risk": "Risk" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L24 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_tool_registry": "TOOL_REGISTRY" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L98 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_tooldef": "ToolDef" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L26 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_transport_rationale_354": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L354 | neighbors=[.fetch_scope(), .is_ws_connected()] | lang=en
- "agent_transport_transport_clear_state": ".clear_state()" | kind=code-symbol | source=probe/agent/transport.py:L205 | neighbors=[Transport, .update_state()] | lang=en
- "agent_transport_transport_close": ".close()" | kind=code-symbol | source=probe/agent/transport.py:L485 | neighbors=[_sync_directory(), Transport] | lang=en
- "agent_transport_transport_init": ".__init__()" | kind=code-symbol | source=probe/agent/transport.py:L84 | neighbors=[Transport, .load_state()] | lang=en
- "agent_validation_metric": "_metric()" | kind=code-symbol | source=probe/agent/validation.py:L173 | neighbors=[validation.py, score_inventory()] | lang=en
- "agent_validation_not_scored": "_not_scored()" | kind=code-symbol | source=probe/agent/validation.py:L197 | neighbors=[validation.py, score_inventory()] | lang=en
- "agent_validation_resolve_use_cases": "resolve_use_cases()" | kind=code-symbol | source=probe/agent/validation.py:L38 | neighbors=[validation.py, Resolve suites plus explicit use-cases,…] | lang=en
- "agent_validation_target_address_count": "target_address_count()" | kind=code-symbol | source=probe/agent/validation.py:L93 | neighbors=[validation.py, Return the conservative number of addre…] | lang=en
- "agent_validation_validate_targets": "validate_targets()" | kind=code-symbol | source=probe/agent/validation.py:L55 | neighbors=[validation.py, Require every IP/CIDR target to be full…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-048.json

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
