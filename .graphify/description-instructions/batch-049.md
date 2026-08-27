# Node Description Batch 50 of 236

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

- "websocket_manager_agentconnectionmanager_agent_stale_after": ".agent_stale_after()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L336 | neighbors=[AgentConnectionManager, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…] | lang=en
- "websocket_manager_agentconnectionmanager_connected_agents": ".connected_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L300 | neighbors=[AgentConnectionManager, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…] | lang=en
- "websocket_manager_agentconnectionmanager_get_agent_status": ".get_agent_status()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L332 | neighbors=[AgentConnectionManager, Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Push a job to the first online agent in…] | lang=en
- "websocket_manager_agentconnectionmanager_is_online": ".is_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L295 | neighbors=[AgentConnectionManager, Check if a specific agent is online (co…, Check if a specific agent is online (co…, Check if a specific agent is online (co…, Check if a specific agent is online (co…] | lang=en
- "websocket_manager_agentconnectionmanager_online_agents": ".online_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L305 | neighbors=[AgentConnectionManager, Return agent IDs whose status is 'onlin…, Return agent IDs whose status is 'onlin…, Deliver a job-push to an agent wherever…, Return agent IDs whose status is 'onlin…] | lang=en
- "websocket_manager_agentconnectionmanager_online_agents_for_tenant": ".online_agents_for_tenant()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L309 | neighbors=[AgentConnectionManager, .push_job_to_first_online(), Return idle connected agents belonging …, Return idle connected agents belonging …, Return idle connected agents belonging …] | lang=en
- "websocket_manager_agentconnectionmanager_unregister": ".unregister()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L124 | neighbors=[AgentConnectionManager, .push_job(), Remove the current registration, option…, .push_job_to_first_online(), Remove an agent's WebSocket registratio…] | lang=en
- "websocket_manager_connectionmanager_disconnect": ".disconnect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L41 | neighbors=[ConnectionManager, .broadcast(), .send_personal(), .handle_client(), Remove connection from room.] | lang=en
- "websocket_manager_connectionmanager_send_personal": ".send_personal()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L66 | neighbors=[ConnectionManager, .disconnect(), .handle_client(), ._handle_message(), Send message to a specific connection.] | lang=en
- "workers_outbox_dead_letter_stale_stmt": "_dead_letter_stale_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L195 | neighbors=[outbox.py, Stranded events that already exhausted …, _reclaim_stale(), Stranded events that already exhausted …, Stranded events that already exhausted …] | lang=en
- "workers_outbox_requeue_stale_stmt": "_requeue_stale_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L212 | neighbors=[outbox.py, Stranded events with retry budget left …, _reclaim_stale(), Stranded events with retry budget left …, Stranded events with retry budget left …] | lang=en
- "workers_outbox_stale_cutoff": "_stale_cutoff()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L190 | neighbors=[outbox.py, The `locked_at` boundary before which a…, _reclaim_stale(), The `locked_at` boundary before which a…, The `locked_at` boundary before which a…] | lang=en
- "workers_reaper_reap_once": "reap_once()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L56 | neighbors=[reaper.py, Expire current attempts and requeue onl…, expire_attempt(), run_reaper(), Requeue every running job whose lease h…] | lang=en
- "workflow_asset_asset_merge_result": ".merge_result()" | kind=code-symbol | source=probe/workflow/asset.py:L95 | neighbors=[Asset, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…] | lang=en
- "ad_adcs_adcschecker_check_esc1": ".check_esc1()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L132 | neighbors=[ADCSChecker, ._has_low_priv(), .generate_findings(), ESC1: enrollee supplies subject + clien…] | lang=en
- "ad_adcs_adcschecker_enumerate_templates": ".enumerate_templates()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L62 | neighbors=[ADCSChecker, ._enrollment_principals(), CertTemplate, Read pKICertificateTemplate objects fro…] | lang=en
- "ad_adcs_adcschecker_generate_findings": ".generate_findings()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L182 | neighbors=[ADCSChecker, .check_esc1(), .check_esc4(), .check_esc8()] | lang=en
- "ad_adcs_rationale_1": "ADCSChecker — Active Directory Certificate Services template misconfiguration an" | kind=entity | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[adcs.py, ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_117": "Principals with an enrollment ExtendedRight or broad write on the template." | kind=entity | source=manager/backend/app/ad/adcs.py:L117 | neighbors=[._enrollment_principals(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_133": "ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +" | kind=entity | source=manager/backend/app/ad/adcs.py:L133 | neighbors=[.check_esc1(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_148": "ESC4: a low-privilege principal holds a dangerous write right on the template." | kind=entity | source=manager/backend/app/ad/adcs.py:L148 | neighbors=[.check_esc4(), ACE, LDAPEnumerator, FindingSeverity] | lang=pt
- "ad_adcs_rationale_161": "ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM" | kind=entity | source=manager/backend/app/ad/adcs.py:L161 | neighbors=[.check_esc8(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_63": "Read pKICertificateTemplate objects from the Configuration NC." | kind=entity | source=manager/backend/app/ad/adcs.py:L63 | neighbors=[.enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_asreproast": "asreproast.py" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L1 | neighbors=[ASREPRoastChecker, ASREPRoastChecker — find accounts with …, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "ad_bloodhound": "bloodhound.py" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L1 | neighbors=[BloodHoundCollector, BloodHoundCollector — wrapper around th…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "ad_kerberoast_kerberoastchecker_encode_tgs_rep": "._encode_tgs_rep()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L130 | neighbors=[KerberoastChecker, .request_tgs(), Render the TGS as a hashcat $krb5tgs$ s…, Render the TGS as a hashcat $krb5tgs$ s…] | lang=en
- "ad_kerberoast_kerberoastchecker_get_spn_accounts": ".get_spn_accounts()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L47 | neighbors=[KerberoastChecker, ._pwd_last_set(), Returns user accounts that have a servi…, Returns user accounts that have a servi…] | lang=en
- "ad_kerberoast_kerberoastchecker_request_tgs": ".request_tgs()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L85 | neighbors=[KerberoastChecker, ._encode_tgs_rep(), Request a TGS for ``spn`` and return th…, Request a TGS for ``spn`` and return th…] | lang=en
- "ad_ldap_enum_adcomputer": "ADComputer" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L67 | neighbors=[ldap_enum.py, .get_computers(), ADConnectionError, DependencyMissingError] | lang=en
- "ad_ldap_enum_adgroup": "ADGroup" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L76 | neighbors=[ldap_enum.py, .get_groups(), ADConnectionError, DependencyMissingError] | lang=en
- "ad_ldap_enum_domain_to_base_dn": "_domain_to_base_dn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L104 | neighbors=[ldap_enum.py, .connect(), corp.local -> DC=corp,DC=local, corp.local -> DC=corp,DC=local] | lang=en
- "ad_ldap_enum_ldapenumerator_check_anonymous_bind": ".check_anonymous_bind()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L285 | neighbors=[LDAPEnumerator, .unbind(), True if the DC accepts an anonymous bin…, True if the DC accepts an anonymous bin…] | lang=en
- "ad_ldap_enum_ldapenumerator_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L127 | neighbors=[LDAPEnumerator, _domain_to_base_dn(), Bind to the domain controller. Returns …, Bind to the domain controller. Returns …] | lang=en
- "ad_ldap_enum_ldapenumerator_get_computers": ".get_computers()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L239 | neighbors=[LDAPEnumerator, ADComputer, ._attr(), ._search()] | lang=en
- "ad_ntlm_relay": "ntlm_relay.py" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L1 | neighbors=[NTLMRelayChecker, NTLMRelayChecker — detect missing SMB/L…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "ad_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[ADAssessmentRunner, ADAssessmentRunner — runs the full Acti…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "agent_agent_is_local_manager_url": "_is_local_manager_url()" | kind=code-symbol | source=probe/agent/agent.py:L56 | neighbors=[agent.py, main(), Recognize only explicit single-host dev…, Recognize only explicit single-host dev…] | lang=en
- "agent_agent_manager_reachable": "_manager_reachable()" | kind=code-symbol | source=probe/agent/agent.py:L156 | neighbors=[agent.py, _classify_connection_error(), GET /health. Returns (ok, human-detail)…, _wait_for_manager()] | lang=en
- "agent_agent_result_summary": "_result_summary()" | kind=code-symbol | source=probe/agent/agent.py:L106 | neighbors=[agent.py, main(), One-line, transparent summary of what a…, _ws_run_job()] | lang=en
- "agent_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/agent/cli.py:L931 | neighbors=[cli.py, default_config_path(), _env(), main()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-049.json

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
