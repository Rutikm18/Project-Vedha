# Node Description Batch 23 of 76

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

- "vuln_nuclei_rationale_68": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L68 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_81": "Runs nuclei as an async subprocess.         Returns a list of parsed finding dic" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L81 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "websocket_manager_agentconnectionmanager_unregister": ".unregister()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L122 | neighbors=[AgentConnectionManager, .push_job(), .push_job_to_first_online(), Remove an agent's WebSocket registratio…]
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
- "ad_findings_rationale_23": "Base class for Active Directory assessment errors." | kind=entity | source=manager/backend/app/ad/findings.py:L23 | neighbors=[ADError, FindingSeverity, FindingStatus]
- "ad_findings_rationale_27": "Raised when an LDAP/Kerberos/SMB connection to the DC fails." | kind=entity | source=manager/backend/app/ad/findings.py:L27 | neighbors=[ADConnectionError, FindingSeverity, FindingStatus]
- "ad_findings_rationale_31": "Raised when an optional offensive dependency (ldap3/impacket) is absent." | kind=entity | source=manager/backend/app/ad/findings.py:L31 | neighbors=[DependencyMissingError, FindingSeverity, FindingStatus]
- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, 298a9d4 trim frontend to 7 core pages; …]
- "ad_kerberoast_kerberoastchecker_encode_tgs_rep": "._encode_tgs_rep()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L131 | neighbors=[KerberoastChecker, .request_tgs(), Render the TGS as a hashcat $krb5tgs$ s…]
- "ad_kerberoast_kerberoastchecker_get_spn_accounts": ".get_spn_accounts()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L48 | neighbors=[KerberoastChecker, ._pwd_last_set(), Returns user accounts that have a servi…]
- "ad_kerberoast_kerberoastchecker_request_tgs": ".request_tgs()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L86 | neighbors=[KerberoastChecker, ._encode_tgs_rep(), Request a TGS for ``spn`` and return th…]
- "ad_kerberoast_rationale_1": "KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[kerberoast.py, LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_132": "Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)." | kind=entity | source=manager/backend/app/ad/kerberoast.py:L132 | neighbors=[._encode_tgs_rep(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_146": "One aggregate Finding for all kerberoastable accounts.         Severity is Criti" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L146 | neighbors=[.generate_finding(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_41": "Enumerate kerberoastable accounts and capture TGS evidence." | kind=entity | source=manager/backend/app/ad/kerberoast.py:L41 | neighbors=[KerberoastChecker, LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_49": "Returns user accounts that have a servicePrincipalName set (and are not" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L49 | neighbors=[.get_spn_accounts(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_94": "Request a TGS for ``spn`` and return the $krb5tgs$ hash string for offline" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L94 | neighbors=[.request_tgs(), LDAPEnumerator, FindingSeverity]
- "ad_ldap_enum_as_list": "_as_list()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L110 | neighbors=[ldap_enum.py, .get_groups(), .get_users()]

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
