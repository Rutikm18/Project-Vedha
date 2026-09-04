# Node Description Batch 171 of 332

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

- "workflow_workflow_engine_rationale_112": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L112 | neighbors=[_gather_per_host(), _port_candidates()]
- "workflow_workflow_engine_rationale_80": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L80 | neighbors=[_gather_per_host(), _port_candidates()]
- "workflow_workflow_engine_rationale_94": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L94 | neighbors=[_scan_one(), _split_cached()]
- "activity_route_apiactivity": "ApiActivity" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L9 | neighbors=[route.ts]
- "activity_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L14 | neighbors=[route.ts]
- "ad_asreproast_asreproastchecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L106 | neighbors=[ASREPRoastChecker]
- "ad_bloodhound_bloodhoundcollector_close": ".close()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L267 | neighbors=[BloodHoundCollector]
- "ad_bloodhound_bloodhoundcollector_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L46 | neighbors=[BloodHoundCollector]
- "ad_ldap_enum_ldapenumerator_connection": ".connection()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L185 | neighbors=[LDAPEnumerator]
- "ad_ldap_enum_ldapenumerator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L120 | neighbors=[LDAPEnumerator]
- "ad_orchestrator_adassessmentrunner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L42 | neighbors=[ADAssessmentRunner]
- "agent_agent_agentdeps": "AgentDeps" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L39 | neighbors=[agent.py]
- "agent_agent_agentopts": "AgentOpts" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L26 | neighbors=[agent.py]
- "agent_agent_rationale_1016": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1016 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_1020": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L1020 | neighbors=[_check_anti_debug()]
- "agent_agent_rationale_1025": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1025 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_103": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=probe/agent/agent.py:L103 | neighbors=[_job_intent()]
- "agent_agent_rationale_1032": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L1032 | neighbors=[_check_anti_debug()]
- "agent_agent_rationale_104": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=probe/agent/agent.py:L104 | neighbors=[_job_intent()]
- "agent_agent_rationale_1049": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1049 | neighbors=[_enroll_device()]
- "agent_agent_rationale_1058": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1058 | neighbors=[_enroll_device()]
- "agent_agent_rationale_1068": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L1068 | neighbors=[_load_or_create_identity()]
- "agent_agent_rationale_107": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L107 | neighbors=[_result_summary()]
- "agent_agent_rationale_1080": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L1080 | neighbors=[_load_or_create_identity()]
- "agent_agent_rationale_1117": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1117 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_1129": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1129 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_1150": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1150 | neighbors=[_enroll_device()]
- "agent_agent_rationale_1163": "Request UI approval, poll, prove key possession, and activate.      `_recreate_b" | kind=entity | source=probe/agent/agent.py:L1163 | neighbors=[_enroll_device()]
- "agent_agent_rationale_117": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L117 | neighbors=[_result_summary()]
- "agent_agent_rationale_118": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L118 | neighbors=[_result_summary()]
- "agent_agent_rationale_1187": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1187 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_1213": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1213 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_1231": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1231 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_131": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=probe/agent/agent.py:L131 | neighbors=[_classify_connection_error()]
- "agent_agent_rationale_1323": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1323 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_1371": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1371 | neighbors=[_obtain_identity()]
- "agent_agent_rationale_141": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=probe/agent/agent.py:L141 | neighbors=[_classify_connection_error()]
- "agent_agent_rationale_142": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=probe/agent/agent.py:L142 | neighbors=[_classify_connection_error()]
- "agent_agent_rationale_157": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L157 | neighbors=[_manager_reachable()]
- "agent_agent_rationale_167": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L167 | neighbors=[_manager_reachable()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-170.json

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
