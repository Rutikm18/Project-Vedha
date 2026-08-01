# Node Description Batch 48 of 119

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
- "ad_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/ad/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
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
- "agent_agent_containsstring": "containsString()" | kind=code-symbol | source=probe-go/agent/agent.go:L921 | neighbors=[agent.py, .wsSession()] | lang=en
- "agent_agent_defaultscantype": "defaultScanType()" | kind=code-symbol | source=probe-go/agent/agent.go:L833 | neighbors=[agent.py, mapToJob()] | lang=en
- "agent_agent_firststr": "firstStr()" | kind=code-symbol | source=probe-go/agent/agent.go:L912 | neighbors=[agent.py, mapToJob()] | lang=en
- "agent_agent_floator": "floatOr()" | kind=code-symbol | source=probe-go/agent/agent.go:L930 | neighbors=[agent.py, mapToJob()] | lang=en
- "agent_agent_isblocked": "isBlocked()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L62 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_agent_requiresapproval": "requiresApproval()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L54 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_agent_ws_test_booltoint": "boolToInt()" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L451 | neighbors=[agent_ws_test.go, TestWSSessionExecutesOnlyAfterPositiveC…] | lang=en
- "agent_agent_ws_test_readjsonfile": "readJSONFile()" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L458 | neighbors=[agent_ws_test.go, TestWSSessionRetainsResultUntilMatching…] | lang=en
- "agent_agent_ws_test_testwssessionexecutesonlyafterpositiveclaim": "TestWSSessionExecutesOnlyAfterPositiveClaim()" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L109 | neighbors=[agent_ws_test.go, boolToInt()] | lang=en
- "agent_agent_ws_test_testwssessionretainsresultuntilmatchingack": "TestWSSessionRetainsResultUntilMatchingAck()" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L288 | neighbors=[agent_ws_test.go, readJSONFile()] | lang=en
- "agent_cli_cmd_whoami": "cmd_whoami()" | kind=code-symbol | source=probe/agent/cli.py:L296 | neighbors=[cli.py, cmd_auth_status()] | lang=en
- "agent_cli_doctor_check": "_doctor_check()" | kind=code-symbol | source=probe/agent/cli.py:L300 | neighbors=[cli.py, cmd_doctor()] | lang=en
- "agent_cli_main": "main()" | kind=code-symbol | source=probe/agent/cli.py:L1129 | neighbors=[cli.py, build_parser()] | lang=en
- "agent_cli_manager_is_local": "_manager_is_local()" | kind=code-symbol | source=probe/agent/cli.py:L568 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_cli_managerclient_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L104 | neighbors=[ManagerClient, normalize_manager_url()] | lang=en
- "agent_cli_write_private_json": "_write_private_json()" | kind=code-symbol | source=probe/agent/cli.py:L534 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_engine_env_number": "_env_number()" | kind=code-symbol | source=probe/agent/engine.py:L45 | neighbors=[engine.py, Read a bounded numeric safety setting w…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-047.json

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
