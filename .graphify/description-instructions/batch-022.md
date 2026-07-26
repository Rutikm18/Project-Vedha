# Node Description Batch 23 of 104

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

- "tools_installer_readinstalled": "readInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L33 | neighbors=[installer.ts, getInstalledRecord(), installTool(), listStatus(), removeTool()] | lang=en
- "tools_installer_removetool": "removeTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L243 | neighbors=[tools.ts, installer.ts, managedPath(), readInstalled(), writeInstalled()] | lang=en
- "ui_output_rule": "rule()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L50 | neighbors=[output.ts, findingDetail(), ln(), scanHeader(), summary()] | lang=en
- "vuln_enrichment": "enrichment.py" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, TTLCache, VulnEnrichmentService, VulnEnrichmentService  External data so…] | lang=en
- "vuln_enrichment_vulnenrichmentservice_enrich": ".enrich()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L105 | neighbors=[Add NVD CVSS, EPSS, KEV flag, MITRE tec…, VulnEnrichmentService, .get(), .compute_composite_risk(), ._fetch_all()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_mitre_techniques": ".fetch_mitre_techniques()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L270 | neighbors=[Returns MITRE ATT&CK technique IDs link…, VulnEnrichmentService, ._fetch_all(), .get(), .fetch_nvd()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_nvd": ".fetch_nvd()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L163 | neighbors=[Returns {cvss_v3, cvss_vector, descript…, VulnEnrichmentService, ._fetch_all(), .fetch_mitre_techniques(), .get()] | lang=en
- "websocket_manager_connectionmanager_disconnect": ".disconnect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L41 | neighbors=[ConnectionManager, .broadcast(), .send_personal(), .handle_client(), Remove connection from room.] | lang=en
- "websocket_manager_connectionmanager_send_personal": ".send_personal()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L66 | neighbors=[ConnectionManager, .disconnect(), .handle_client(), ._handle_message(), Send message to a specific connection.] | lang=en
- "websocket_manager_graphwebsocketmanager_handle_message": "._handle_message()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L256 | neighbors=[GraphWebSocketManager, .handle_client(), .broadcast(), .send_personal(), Handle incoming WebSocket messages.] | lang=en
- "workers_outbox_run_worker": "run_worker()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L185 | neighbors=[outbox.py, Main loop: claim → process → repeat. Sl…, _claim_batch(), Event, _process()] | lang=en
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=probe/workflow/modes.py:L16 | neighbors=[modes.py, assessment(), re_scan(), service_specific(), triage()] | lang=en
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…] | lang=en
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "ad_adcs_adcschecker_check_esc1": ".check_esc1()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L132 | neighbors=[ADCSChecker, ._has_low_priv(), .generate_findings(), ESC1: enrollee supplies subject + clien…] | lang=en
- "ad_adcs_adcschecker_enumerate_templates": ".enumerate_templates()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L62 | neighbors=[ADCSChecker, ._enrollment_principals(), CertTemplate, Read pKICertificateTemplate objects fro…] | lang=en
- "ad_adcs_adcschecker_generate_findings": ".generate_findings()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L182 | neighbors=[ADCSChecker, .check_esc1(), .check_esc4(), .check_esc8()] | lang=en
- "ad_adcs_rationale_1": "ADCSChecker — Active Directory Certificate Services template misconfiguration an" | kind=entity | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[adcs.py, ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_117": "Principals with an enrollment ExtendedRight or broad write on the template." | kind=entity | source=manager/backend/app/ad/adcs.py:L117 | neighbors=[._enrollment_principals(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_133": "ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +" | kind=entity | source=manager/backend/app/ad/adcs.py:L133 | neighbors=[.check_esc1(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_148": "ESC4: a low-privilege principal holds a dangerous write right on the template." | kind=entity | source=manager/backend/app/ad/adcs.py:L148 | neighbors=[.check_esc4(), ACE, LDAPEnumerator, FindingSeverity] | lang=pt
- "ad_adcs_rationale_161": "ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM" | kind=entity | source=manager/backend/app/ad/adcs.py:L161 | neighbors=[.check_esc8(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_adcs_rationale_63": "Read pKICertificateTemplate objects from the Configuration NC." | kind=entity | source=manager/backend/app/ad/adcs.py:L63 | neighbors=[.enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity] | lang=en
- "ad_ldap_enum_adcomputer": "ADComputer" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L68 | neighbors=[ldap_enum.py, ADConnectionError, DependencyMissingError, .get_computers()] | lang=en
- "ad_ldap_enum_adgroup": "ADGroup" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L77 | neighbors=[ldap_enum.py, ADConnectionError, DependencyMissingError, .get_groups()] | lang=en
- "ad_ldap_enum_ldapenumerator_get_computers": ".get_computers()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L240 | neighbors=[LDAPEnumerator, ADComputer, ._attr(), ._search()] | lang=en
- "agent_agent_count_by_severity": "count_by_severity()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L128 | neighbors=[agent.py, execute_smb_validation(), execute_tls_scan(), execute_vuln_scan()] | lang=en
- "agent_agent_jobtype": "JobType" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L47 | neighbors=[agent.py, Enum, str, ._poll_and_execute()] | lang=en
- "agent_agent_runwsloop": ".runWSLoop()" | kind=code-symbol | source=probe-go/agent/agent.go:L87 | neighbors=[agent.py, .Run(), say(), .wsSession()] | lang=en
- "agent_agent_scanningagent_execute_job": "._execute_job()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L693 | neighbors=[ScanningAgent, ._api_call(), .get_credentials(), ._poll_and_execute()] | lang=en
- "agent_agent_scanningagent_run": ".run()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L732 | neighbors=[ScanningAgent, check_tool_availability(), ._heartbeat_loop(), ._poll_and_execute()] | lang=en
- "agent_agent_ws_heartbeat_sender": "_ws_heartbeat_sender()" | kind=code-symbol | source=probe/agent/agent.py:L469 | neighbors=[agent.py, Send periodic heartbeats over WebSocket., _run_ws_push_loop(), Send periodic heartbeats over WebSocket.] | lang=en
- "agent_agent_wssession": ".wsSession()" | kind=code-symbol | source=probe-go/agent/agent.go:L110 | neighbors=[agent.py, .runWSLoop(), .runJob(), say()] | lang=en
- "agent_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/agent/cli.py:L552 | neighbors=[cli.py, default_config_path(), _env(), main()] | lang=en
- "agent_cli_cmd_agents_list": "cmd_agents_list()" | kind=code-symbol | source=probe/agent/cli.py:L405 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_engagements_list": "cmd_engagements_list()" | kind=code-symbol | source=probe/agent/cli.py:L422 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_engagements_scope": "cmd_engagements_scope()" | kind=code-symbol | source=probe/agent/cli.py:L470 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_scan_status": "cmd_scan_status()" | kind=code-symbol | source=probe/agent/cli.py:L526 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_use_cases": "cmd_use_cases()" | kind=code-symbol | source=probe/agent/cli.py:L389 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_configstore_remove_profile": ".remove_profile()" | kind=code-symbol | source=probe/agent/cli.py:L92 | neighbors=[cmd_auth_logout(), ConfigStore, .load(), .save()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-022.json

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
