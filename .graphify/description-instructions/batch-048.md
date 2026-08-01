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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "agent_engine_facts_from_cache": "_facts_from_cache()" | kind=code-symbol | source=probe/agent/engine.py:L252 | neighbors=[engine.py, run_scan()]
- "agent_job_mapping_test_testmaptojobfailsclosedonunverifiablescope": "TestMapToJobFailsClosedOnUnverifiableScope()" | kind=code-symbol | source=probe-go/agent/job_mapping_test.go:L115 | neighbors=[job_mapping_test.go, managerJob()]
- "agent_job_mapping_test_testmaptojobmergesauthoritativeexclusions": "TestMapToJobMergesAuthoritativeExclusions()" | kind=code-symbol | source=probe-go/agent/job_mapping_test.go:L97 | neighbors=[job_mapping_test.go, managerJob()]
- "agent_job_mapping_test_testmaptojobresolvescanonicalusecases": "TestMapToJobResolvesCanonicalUseCases()" | kind=code-symbol | source=probe-go/agent/job_mapping_test.go:L29 | neighbors=[job_mapping_test.go, managerJob()]
- "agent_job_mapping_test_testmaptojobusesparamsscantypeandpreservesnarrowtargets": "TestMapToJobUsesParamsScanTypeAndPreservesNarrowTargets()" | kind=code-symbol | source=probe-go/agent/job_mapping_test.go:L75 | neighbors=[job_mapping_test.go, managerJob()]
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=probe/agent/license.py:L48 | neighbors=[license.py, verify_license()]
- "agent_scope_crypt_bytes_to_pubkey_b64": "bytes_to_pubkey_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L165 | neighbors=[scope_crypt.py, Encode raw X25519 public key bytes to a…]
- "agent_scope_crypt_generate_identity": "generate_identity()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L43 | neighbors=[scope_crypt.py, Generate a fresh X25519 keypair.      R…]
- "agent_scope_crypt_pubkey_to_bytes": "pubkey_to_bytes()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L160 | neighbors=[scope_crypt.py, Decode a base64-encoded X25519 public k…]
- "agent_scope_validator_rationale_58": "Fetch the engagement's authoritative scope from the manager.      Args:" | kind=entity | source=probe/agent/scope_validator.py:L58 | neighbors=[fetch_engagement_scope(), validate_targets_in_scope()]
- "agent_spool_test_entrynames": "entryNames()" | kind=code-symbol | source=probe-go/agent/spool_test.go:L88 | neighbors=[spool_test.go, TestSpoolSaveIsAtomicAndRejectsTraversa…]
- "agent_spool_test_testspoolsaveisatomicandrejectstraversal": "TestSpoolSaveIsAtomicAndRejectsTraversal()" | kind=code-symbol | source=probe-go/agent/spool_test.go:L10 | neighbors=[spool_test.go, entryNames()]
- "agent_state_loadidentitystate": "loadIdentityState()" | kind=code-symbol | source=probe-go/agent/state.go:L18 | neighbors=[state.go, secureStatePath()]
- "agent_state_syncstatedirectory": "syncStateDirectory()" | kind=code-symbol | source=probe-go/agent/state.go:L160 | neighbors=[state.go, saveIdentityState()]
- "agent_state_test_testconfiguredidentityrejectspartialcredentials": "TestConfiguredIdentityRejectsPartialCredentials()" | kind=code-symbol | source=probe-go/agent/state_test.go:L179 | neighbors=[state_test.go, identityTestConfig()]
- "agent_state_test_testconfiguredidentitytakesprecedenceoverstate": "TestConfiguredIdentityTakesPrecedenceOverState()" | kind=code-symbol | source=probe-go/agent/state_test.go:L157 | neighbors=[state_test.go, identityTestConfig()]
- "agent_state_test_writejson": "writeJSON()" | kind=code-symbol | source=probe-go/agent/state_test.go:L58 | neighbors=[state_test.go, newIdentityServer()]
- "agent_tools_agentstate": "AgentState" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L15 | neighbors=[agent.py, tools.ts]
- "agent_tools_persistagentfindings": "persistAgentFindings()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L313 | neighbors=[agent.py, tools.ts]
- "agent_tools_risk": "Risk" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L24 | neighbors=[agent.py, tools.ts]
- "agent_tools_tool_registry": "TOOL_REGISTRY" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L98 | neighbors=[agent.py, tools.ts]
- "agent_tools_tooldef": "ToolDef" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L26 | neighbors=[agent.py, tools.ts]
- "agent_transport_connectws": ".ConnectWS()" | kind=code-symbol | source=probe-go/agent/transport.go:L122 | neighbors=[transport.py, managerTLSConfig()]
- "agent_transport_get": ".get()" | kind=code-symbol | source=probe-go/agent/transport.go:L151 | neighbors=[transport.py, .PollJobs()]
- "agent_transport_login": ".Login()" | kind=code-symbol | source=probe-go/agent/transport.go:L46 | neighbors=[transport.py, .post()]
- "agent_transport_newtransport": "NewTransport()" | kind=code-symbol | source=probe-go/agent/transport.go:L27 | neighbors=[transport.py, managerTLSConfig()]
- "agent_transport_patch": ".patch()" | kind=code-symbol | source=probe-go/agent/transport.go:L161 | neighbors=[transport.py, .Heartbeat()]
- "agent_transport_polljobs": ".PollJobs()" | kind=code-symbol | source=probe-go/agent/transport.go:L108 | neighbors=[transport.py, .get()]
- "agent_transport_rationale_354": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L354 | neighbors=[.fetch_scope(), .is_ws_connected()]
- "agent_transport_refreshregistration": ".RefreshRegistration()" | kind=code-symbol | source=probe-go/agent/transport.go:L96 | neighbors=[transport.py, .post()]
- "agent_transport_register": ".Register()" | kind=code-symbol | source=probe-go/agent/transport.go:L57 | neighbors=[transport.py, .post()]
- "agent_transport_submitresult": ".SubmitResult()" | kind=code-symbol | source=probe-go/agent/transport.go:L116 | neighbors=[transport.py, .post()]
- "agent_transport_transport_clear_state": ".clear_state()" | kind=code-symbol | source=probe/agent/transport.py:L208 | neighbors=[Transport, .update_state()]
- "agent_transport_transport_close": ".close()" | kind=code-symbol | source=probe/agent/transport.py:L488 | neighbors=[_sync_directory(), Transport]
- "agent_transport_transport_init": ".__init__()" | kind=code-symbol | source=probe/agent/transport.py:L87 | neighbors=[Transport, .load_state()]
- "agent_wsjsonwriter": "wsJSONWriter" | kind=code-symbol | source=probe-go/agent/agent.go:L118 | neighbors=[agent.py, .Write()]
- "agent_wsjsonwriter_write": ".Write()" | kind=code-symbol | source=probe-go/agent/agent.go:L136 | neighbors=[.wsSession(), wsJSONWriter]
- "ai_agent_agentdecisionengine_count": "._count()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L329 | neighbors=[AgentDecisionEngine, ._overview()]
- "ai_agent_agentdecisionengine_create": "._create()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L235 | neighbors=[AgentDecisionEngine, .run()]
- "ai_agent_agentdecisionengine_list_assets": "._list_assets()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L296 | neighbors=[AgentDecisionEngine, ._exec_read_tool()]

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
