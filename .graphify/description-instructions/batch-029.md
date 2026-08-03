# Node Description Batch 30 of 131

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

- "versions_0006_llm_outputs": "0006_llm_outputs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), AI engine: llm_outputs table + reviewst…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "versions_0007_scale_indexes": "0007_scale_indexes.py" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3: composite indexes for the hot aggre…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "versions_0008_scan_results": "0008_scan_results.py" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3-#10: append-only scan_results table …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "versions_0009_outbox_events": "0009_outbox_events.py" | kind=code-symbol | source=manager/backend/alembic/versions/0009_outbox_events.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Transactional outbox for durable backgr…, 2885afa Add comprehensive probe testing…] | lang=en
- "versions_0010_detection_runs": "0010_detection_runs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Temporal detection: detection_runs tabl…, 2885afa Add comprehensive probe testing…] | lang=en
- "versions_0011_job_lease": "0011_job_lease.py" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Job leasing: scan_jobs.lease_expires_at…, 2885afa Add comprehensive probe testing…] | lang=en
- "versions_0012_agent_recommendations": "0012_agent_recommendations.py" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Agentic AI advisor: agent_recommendatio…, 2885afa Add comprehensive probe testing…] | lang=en
- "versions_0013_agent_public_key": "0013_agent_public_key.py" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Add agents.public_key (Phase-4 X25519 i…, 2885afa Add comprehensive probe testing…] | lang=en
- "vuln_enrichment_vulnenrichmentservice_enrich": ".enrich()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L105 | neighbors=[Add NVD CVSS, EPSS, KEV flag, MITRE tec…, VulnEnrichmentService, .get(), .compute_composite_risk(), ._fetch_all()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_mitre_techniques": ".fetch_mitre_techniques()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L270 | neighbors=[Returns MITRE ATT&CK technique IDs link…, VulnEnrichmentService, ._fetch_all(), .get(), .fetch_nvd()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_nvd": ".fetch_nvd()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L163 | neighbors=[Returns {cvss_v3, cvss_vector, descript…, VulnEnrichmentService, ._fetch_all(), .fetch_mitre_techniques(), .get()] | lang=en
- "vuln_nessus_nessusscanner_create_scan": ".create_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L94 | neighbors=[NessusScanner, ._get_client(), ._get_template_uuid(), Returns nessus scan_id as string., Returns nessus scan_id as string.] | lang=en
- "vuln_nessus_nessusscanner_get_results": ".get_results()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L166 | neighbors=[NessusScanner, ._get_client(), ._get_plugin_detail(), Returns list of raw finding dicts from …, Returns list of raw finding dicts from …] | lang=en
- "websocket_manager_agentconnectionmanager_unregister": ".unregister()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L124 | neighbors=[AgentConnectionManager, .push_job(), Remove the current registration, option…, .push_job_to_first_online(), Remove an agent's WebSocket registratio…] | lang=en
- "websocket_manager_connectionmanager_disconnect": ".disconnect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L41 | neighbors=[ConnectionManager, .broadcast(), .send_personal(), .handle_client(), Remove connection from room.] | lang=en
- "websocket_manager_connectionmanager_send_personal": ".send_personal()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L66 | neighbors=[ConnectionManager, .disconnect(), .handle_client(), ._handle_message(), Send message to a specific connection.] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_graph_update": ".broadcast_graph_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L342 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast graph data update to all subs…, Broadcast graph data update to all subs…, Broadcast graph data update to all subs…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_layout_update": ".broadcast_layout_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L361 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_node_update": ".broadcast_node_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L351 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast a single node update., Broadcast a single node update., Broadcast a single node update.] | lang=en
- "workers_outbox_mark_retry_or_dead": "_mark_retry_or_dead()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L232 | neighbors=[outbox.py, _process(), Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…] | lang=en
- "workers_reaper_reap_once": "reap_once()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L56 | neighbors=[reaper.py, Expire current attempts and requeue onl…, expire_attempt(), run_reaper(), Requeue every running job whose lease h…] | lang=en
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=probe/workflow/gates.py:L47 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…] | lang=en
- "workflow_workflow_engine_gather_per_host": "_gather_per_host()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L71 | neighbors=[workflow_engine.py, _scan_one(), Run per-host probes with bounded fan-ou…, run_engagement(), Runs scanner.scan_target(host) across h…] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-029.json

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
