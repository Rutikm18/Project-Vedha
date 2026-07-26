# Node Description Batch 29 of 104

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

- "versions_0012_agent_recommendations": "0012_agent_recommendations.py" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, downgrade(), upgrade(), Agentic AI advisor: agent_recommendatio…]
- "versions_0013_agent_public_key": "0013_agent_public_key.py" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, downgrade(), upgrade(), Add agents.public_key (Phase-4 X25519 i…]
- "vuln_enrichment_vulnenrichmentservice_check_cisa_kev": ".check_cisa_kev()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L244 | neighbors=[True if CVE is in the CISA Known Exploi…, VulnEnrichmentService, ._get_kev_catalog(), ._fetch_all()]
- "vuln_enrichment_vulnenrichmentservice_compute_composite_risk": ".compute_composite_risk()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L297 | neighbors=[Returns composite risk score on 0-1000 …, VulnEnrichmentService, .get(), .enrich()]
- "vuln_enrichment_vulnenrichmentservice_fetch_epss": ".fetch_epss()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L215 | neighbors=[Returns {epss_score: float, percentile:…, VulnEnrichmentService, ._fetch_all(), .get()]
- "vuln_nessus": "nessus.py" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, NessusScanner, NessusScanner — wraps the Tenable Nessu…]
- "vuln_nessus_nessusscanner_create_scan": ".create_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L95 | neighbors=[NessusScanner, ._get_client(), ._get_template_uuid(), Returns nessus scan_id as string.]
- "vuln_nessus_nessusscanner_get_results": ".get_results()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L167 | neighbors=[NessusScanner, ._get_client(), ._get_plugin_detail(), Returns list of raw finding dicts from …]
- "vuln_nuclei_nucleiscanner_parse_output": ".parse_output()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L131 | neighbors=[NucleiScanner, ._map_finding(), .run_scan(), Parse nuclei JSONL output → list of Fin…]
- "vuln_nuclei_rationale_1": "NucleiScanner — async subprocess wrapper around the Nuclei CLI.  Nuclei outputs" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, nuclei.py]
- "vuln_nuclei_rationale_132": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L132 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_195": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L195 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_68": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L68 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_81": "Runs nuclei as an async subprocess.         Returns a list of parsed finding dic" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L81 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "websocket_manager_agentconnectionmanager_unregister": ".unregister()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L122 | neighbors=[AgentConnectionManager, .push_job(), .push_job_to_first_online(), Remove an agent's WebSocket registratio…]
- "workers_outbox_claim_batch": "_claim_batch()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L109 | neighbors=[outbox.py, Event, Atomically claim up to `batch_size` due…, run_worker()]
- "workers_outbox_process": "_process()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L173 | neighbors=[outbox.py, _mark_done(), _mark_retry_or_dead(), run_worker()]
- "workflow_asset_parse_ts": "_parse_ts()" | kind=code-symbol | source=probe/workflow/asset.py:L32 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_asset_portfact": "PortFact" | kind=code-symbol | source=probe/workflow/asset.py:L37 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_cache_cacheentry": "CacheEntry" | kind=code-symbol | source=probe/workflow/cache.py:L55 | neighbors=[cache.py, .from_jsonl_dict(), .to_jsonl_dict(), .put()]
- "workflow_cli_main": "_main()" | kind=code-symbol | source=probe/workflow/cli.py:L96 | neighbors=[cli.py, _build_creds(), _build_mode(), build_parser()]
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=probe/workflow/gates.py:L45 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), True means OT/ICS passive-only mode — a…]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=probe/workflow/router.py:L54 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_http(), looks_like_tls()]
- "ad_adcs_adcschecker_check_esc4": ".check_esc4()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L147 | neighbors=[ADCSChecker, .generate_findings(), ESC4: a low-privilege principal holds a…]
- "ad_adcs_adcschecker_check_esc8": ".check_esc8()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L160 | neighbors=[ADCSChecker, .generate_findings(), ESC8: the CA exposes a web-enrollment (…]
- "ad_adcs_adcschecker_enrollment_principals": "._enrollment_principals()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L116 | neighbors=[ADCSChecker, .enumerate_templates(), Principals with an enrollment ExtendedR…]
- "ad_asreproast": "asreproast.py" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L1 | neighbors=[ASREPRoastChecker, ASREPRoastChecker — find accounts with …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_asreproast_asreproastchecker_format_asrep_hash": "._format_asrep_hash()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L90 | neighbors=[ASREPRoastChecker, .request_asrep(), Render an AS-REP as a hashcat $krb5asre…]
- "ad_asreproast_asreproastchecker_request_asrep": ".request_asrep()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L54 | neighbors=[ASREPRoastChecker, ._format_asrep_hash(), Request an AS-REP for ``username`` with…]
- "ad_asreproast_rationale_1": "ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and" | kind=entity | source=manager/backend/app/ad/asreproast.py:L1 | neighbors=[asreproast.py, LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_35": "Enumerate AS-REP roastable accounts and capture AS-REP evidence." | kind=entity | source=manager/backend/app/ad/asreproast.py:L35 | neighbors=[ASREPRoastChecker, LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_43": "Usernames of enabled accounts with pre-authentication not required." | kind=entity | source=manager/backend/app/ad/asreproast.py:L43 | neighbors=[.get_no_preauth_accounts(), LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_55": "Request an AS-REP for ``username`` with no credentials and return the         $k" | kind=entity | source=manager/backend/app/ad/asreproast.py:L55 | neighbors=[.request_asrep(), LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_91": "Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)." | kind=entity | source=manager/backend/app/ad/asreproast.py:L91 | neighbors=[._format_asrep_hash(), LDAPEnumerator, FindingSeverity]
- "ad_bloodhound": "bloodhound.py" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L1 | neighbors=[BloodHoundCollector, BloodHoundCollector — wrapper around th…, 298a9d4 trim frontend to 7 core pages; …]
- "ad_bloodhound_bloodhoundcollector_import_to_neo4j": ".import_to_neo4j()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L117 | neighbors=[BloodHoundCollector, ._ingest_collection(), Load nodes (users/computers/groups) and…]
- "ad_bloodhound_bloodhoundcollector_ingest_collection": "._ingest_collection()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L156 | neighbors=[BloodHoundCollector, .import_to_neo4j(), Ingest one BloodHound collector file. R…]
- "ad_findings_build_ad_finding": "build_ad_finding()" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L103 | neighbors=[findings.py, severity_from_str(), Assemble a Finding-compatible dict.    …]
- "ad_findings_rationale_1": "Shared building blocks for the Active Directory assessment module.  Every AD che" | kind=entity | source=manager/backend/app/ad/findings.py:L1 | neighbors=[findings.py, FindingSeverity, FindingStatus]
- "ad_findings_rationale_119": "Assemble a Finding-compatible dict.      All findings carry — as required by the" | kind=entity | source=manager/backend/app/ad/findings.py:L119 | neighbors=[build_ad_finding(), FindingSeverity, FindingStatus]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-028.json

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
