# Node Description Batch 33 of 76

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

- "ad_bloodhound_bloodhoundcollector_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L229 | neighbors=[BloodHoundCollector, Build a Finding summarising the shortes…] | lang=en
- "ad_bloodhound_bloodhoundcollector_query_da_paths": ".query_da_paths()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L195 | neighbors=[BloodHoundCollector, Return shortest attack paths from any n…] | lang=en
- "ad_bloodhound_bloodhoundcollector_run_collection": ".run_collection()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L52 | neighbors=[BloodHoundCollector, Run bloodhound-python and return the li…] | lang=en
- "ad_bloodhound_rationale_1": "BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges" | kind=entity | source=manager/backend/app/ad/bloodhound.py:L1 | neighbors=[bloodhound.py, FindingSeverity] | lang=en
- "ad_bloodhound_rationale_124": "Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu" | kind=entity | source=manager/backend/app/ad/bloodhound.py:L124 | neighbors=[.import_to_neo4j(), FindingSeverity] | lang=en
- "ad_bloodhound_rationale_157": "Ingest one BloodHound collector file. Returns (#nodes, #rels)." | kind=entity | source=manager/backend/app/ad/bloodhound.py:L157 | neighbors=[._ingest_collection(), FindingSeverity] | lang=en
- "ad_bloodhound_rationale_196": "Return shortest attack paths from any non-DA principal to a Domain Admins" | kind=entity | source=manager/backend/app/ad/bloodhound.py:L196 | neighbors=[.query_da_paths(), FindingSeverity] | lang=en
- "ad_bloodhound_rationale_230": "Build a Finding summarising the shortest paths to Domain Admins." | kind=entity | source=manager/backend/app/ad/bloodhound.py:L230 | neighbors=[.generate_finding(), FindingSeverity] | lang=en
- "ad_bloodhound_rationale_61": "Run bloodhound-python and return the list of produced JSON file paths.         R" | kind=entity | source=manager/backend/app/ad/bloodhound.py:L61 | neighbors=[.run_collection(), FindingSeverity] | lang=en
- "ad_findings_severity_from_str": "severity_from_str()" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L96 | neighbors=[findings.py, build_ad_finding()] | lang=en
- "ad_kerberoast_kerberoastchecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L145 | neighbors=[KerberoastChecker, One aggregate Finding for all kerberoas…] | lang=en
- "ad_kerberoast_kerberoastchecker_pwd_last_set": "._pwd_last_set()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L71 | neighbors=[KerberoastChecker, .get_spn_accounts()] | lang=en
- "ad_ldap_enum_ldapenumerator_unbind": ".unbind()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L380 | neighbors=[LDAPEnumerator, .check_anonymous_bind()] | lang=en
- "ad_ntlm_relay_ntlmrelaychecker_check_ldap_signing": ".check_ldap_signing()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L80 | neighbors=[NTLMRelayChecker, Returns True if the DC *enforces* LDAP …] | lang=en
- "ad_ntlm_relay_ntlmrelaychecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L113 | neighbors=[NTLMRelayChecker, Build a Finding for hosts missing SMB s…] | lang=en
- "ad_ntlm_relay_ntlmrelaychecker_probe_smb_host": "._probe_smb_host()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L60 | neighbors=[NTLMRelayChecker, .check_smb_signing()] | lang=en
- "ad_ntlm_relay_rationale_1": "NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L1 | neighbors=[ntlm_relay.py, FindingSeverity] | lang=en
- "ad_ntlm_relay_rationale_118": "Build a Finding for hosts missing SMB signing. The attack_narrative         incl" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L118 | neighbors=[.generate_finding(), FindingSeverity] | lang=en
- "ad_ntlm_relay_rationale_31": "Probe SMB/LDAP signing posture across a host list." | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L31 | neighbors=[NTLMRelayChecker, FindingSeverity] | lang=pt
- "ad_ntlm_relay_rationale_39": "For each IP, returns {signing_enabled, signing_required}.          A host is rel" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L39 | neighbors=[.check_smb_signing(), FindingSeverity] | lang=en
- "ad_ntlm_relay_rationale_81": "Returns True if the DC *enforces* LDAP signing / channel binding.          We at" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L81 | neighbors=[.check_ldap_signing(), FindingSeverity] | lang=en
- "ad_orchestrator_adassessmentrunner_anonymous_bind_finding": "._anonymous_bind_finding()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L186 | neighbors=[ADAssessmentRunner, .run()] | lang=en
- "agent_agent_build_ssl_context": "build_ssl_context()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L93 | neighbors=[agent.py, .__init__()] | lang=en
- "agent_agent_check_tool_availability": "check_tool_availability()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L101 | neighbors=[agent.py, .run()] | lang=en
- "agent_agent_execute_cloud_scan": "execute_cloud_scan()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L605 | neighbors=[agent.py, Cloud infrastructure scan (AWS/Azure/GC…] | lang=en
- "agent_agent_execute_discovery": "execute_discovery()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L201 | neighbors=[agent.py, Nmap service enumeration. Accepts port …] | lang=en
- "agent_agent_execute_lateral_movement": "execute_lateral_movement()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L596 | neighbors=[agent.py, Safe lateral movement checks — no actua…] | lang=en
- "agent_agent_execute_naabu": "execute_naabu()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L137 | neighbors=[agent.py, Fast port discovery with naabu. Feeds p…] | lang=en
- "agent_agent_isblocked": "isBlocked()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L62 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_agent_parse_spn_output": "parse_spn_output()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L294 | neighbors=[agent.py, execute_ad_enum()] | lang=en
- "agent_agent_requiresapproval": "requiresApproval()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L54 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_agent_scanjob": "ScanJob" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L62 | neighbors=[agent.py, ._poll_and_execute()] | lang=en
- "agent_agent_scanningagent_report_progress": "._report_progress()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L665 | neighbors=[ScanningAgent, ._api_call()] | lang=en
- "agent_engine_targets": "_targets()" | kind=code-symbol | source=probe/agent/engine.py:L71 | neighbors=[engine.py, run_scan()] | lang=en
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=probe/agent/license.py:L48 | neighbors=[license.py, verify_license()] | lang=en
- "agent_tools_agentstate": "AgentState" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L16 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_persistagentfindings": "persistAgentFindings()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L314 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_risk": "Risk" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L25 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_tool_registry": "TOOL_REGISTRY" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L99 | neighbors=[agent.py, tools.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-032.json

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
