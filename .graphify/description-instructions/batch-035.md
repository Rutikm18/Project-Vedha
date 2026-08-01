# Node Description Batch 36 of 119

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

- "ad_bloodhound_bloodhoundcollector_import_to_neo4j": ".import_to_neo4j()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L117 | neighbors=[BloodHoundCollector, ._ingest_collection(), Load nodes (users/computers/groups) and…]
- "ad_bloodhound_bloodhoundcollector_ingest_collection": "._ingest_collection()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L156 | neighbors=[BloodHoundCollector, .import_to_neo4j(), Ingest one BloodHound collector file. R…]
- "ad_findings_build_ad_finding": "build_ad_finding()" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L103 | neighbors=[findings.py, severity_from_str(), Assemble a Finding-compatible dict.    …]
- "ad_findings_rationale_1": "Shared building blocks for the Active Directory assessment module.  Every AD che" | kind=entity | source=manager/backend/app/ad/findings.py:L1 | neighbors=[findings.py, FindingSeverity, FindingStatus]
- "ad_findings_rationale_119": "Assemble a Finding-compatible dict.      All findings carry — as required by the" | kind=entity | source=manager/backend/app/ad/findings.py:L119 | neighbors=[build_ad_finding(), FindingSeverity, FindingStatus]
- "ad_findings_rationale_23": "Base class for Active Directory assessment errors." | kind=entity | source=manager/backend/app/ad/findings.py:L23 | neighbors=[ADError, FindingSeverity, FindingStatus]
- "ad_findings_rationale_27": "Raised when an LDAP/Kerberos/SMB connection to the DC fails." | kind=entity | source=manager/backend/app/ad/findings.py:L27 | neighbors=[ADConnectionError, FindingSeverity, FindingStatus]
- "ad_findings_rationale_31": "Raised when an optional offensive dependency (ldap3/impacket) is absent." | kind=entity | source=manager/backend/app/ad/findings.py:L31 | neighbors=[DependencyMissingError, FindingSeverity, FindingStatus]
- "ad_kerberoast_kerberoastchecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L144 | neighbors=[KerberoastChecker, One aggregate Finding for all kerberoas…, One aggregate Finding for all kerberoas…]
- "ad_kerberoast_rationale_1": "KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[kerberoast.py, LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_131": "Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)." | kind=entity | source=manager/backend/app/ad/kerberoast.py:L131 | neighbors=[._encode_tgs_rep(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_132": "Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)." | kind=entity | source=manager/backend/app/ad/kerberoast.py:L132 | neighbors=[._encode_tgs_rep(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_145": "One aggregate Finding for all kerberoastable accounts.         Severity is Criti" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L145 | neighbors=[.generate_finding(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_146": "One aggregate Finding for all kerberoastable accounts.         Severity is Criti" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L146 | neighbors=[.generate_finding(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_40": "Enumerate kerberoastable accounts and capture TGS evidence." | kind=entity | source=manager/backend/app/ad/kerberoast.py:L40 | neighbors=[KerberoastChecker, LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_41": "Enumerate kerberoastable accounts and capture TGS evidence." | kind=entity | source=manager/backend/app/ad/kerberoast.py:L41 | neighbors=[KerberoastChecker, LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_48": "Returns user accounts that have a servicePrincipalName set (and are not" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L48 | neighbors=[.get_spn_accounts(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_49": "Returns user accounts that have a servicePrincipalName set (and are not" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L49 | neighbors=[.get_spn_accounts(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_93": "Request a TGS for ``spn`` and return the $krb5tgs$ hash string for offline" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L93 | neighbors=[.request_tgs(), LDAPEnumerator, FindingSeverity]
- "ad_kerberoast_rationale_94": "Request a TGS for ``spn`` and return the $krb5tgs$ hash string for offline" | kind=entity | source=manager/backend/app/ad/kerberoast.py:L94 | neighbors=[.request_tgs(), LDAPEnumerator, FindingSeverity]
- "ad_ldap_enum_as_list": "_as_list()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L109 | neighbors=[ldap_enum.py, .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_parse_security_descriptor": "._parse_security_descriptor()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L343 | neighbors=[LDAPEnumerator, .get_aces(), ACE]
- "ad_ldap_enum_ldapenumerator_require_conn": "._require_conn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L188 | neighbors=[LDAPEnumerator, .get_aces(), ._search()]
- "ad_ldap_enum_rationale_1": "LDAPEnumerator — read-only Active Directory enumeration over LDAP/LDAPS.  Uses l" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ADConnectionError, DependencyMissingError, ldap_enum.py]
- "ad_ldap_enum_rationale_105": "corp.local -> DC=corp,DC=local" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L105 | neighbors=[ADConnectionError, DependencyMissingError, _domain_to_base_dn()]
- "ad_ldap_enum_rationale_106": "corp.local -> DC=corp,DC=local" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L106 | neighbors=[ADConnectionError, DependencyMissingError, _domain_to_base_dn()]
- "ad_ldap_enum_rationale_118": "Read-only AD enumeration. One instance == one bound connection." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L118 | neighbors=[ADConnectionError, DependencyMissingError, LDAPEnumerator]
- "ad_ldap_enum_rationale_119": "Read-only AD enumeration. One instance == one bound connection." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L119 | neighbors=[ADConnectionError, DependencyMissingError, LDAPEnumerator]
- "ad_ldap_enum_rationale_137": "Bind to the domain controller. Returns self for chaining.          Raises Depend" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L137 | neighbors=[ADConnectionError, DependencyMissingError, .connect()]
- "ad_ldap_enum_rationale_138": "Bind to the domain controller. Returns self for chaining.          Raises Depend" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L138 | neighbors=[ADConnectionError, DependencyMissingError, .connect()]
- "ad_ldap_enum_rationale_214": "All user accounts (excludes computer accounts)." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L214 | neighbors=[ADConnectionError, DependencyMissingError, .get_users()]
- "ad_ldap_enum_rationale_215": "All user accounts (excludes computer accounts)." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L215 | neighbors=[ADConnectionError, DependencyMissingError, .get_users()]
- "ad_ldap_enum_rationale_286": "True if the DC accepts an anonymous bind that can read directory data         (a" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L286 | neighbors=[ADConnectionError, DependencyMissingError, .check_anonymous_bind()]
- "ad_ldap_enum_rationale_287": "True if the DC accepts an anonymous bind that can read directory data         (a" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L287 | neighbors=[ADConnectionError, DependencyMissingError, .check_anonymous_bind()]
- "ad_ldap_enum_rationale_311": "Parse the nTSecurityDescriptor of an object into a list of ACEs for ACL" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L311 | neighbors=[ADConnectionError, DependencyMissingError, .get_aces()]
- "ad_ldap_enum_rationale_312": "Parse the nTSecurityDescriptor of an object into a list of ACEs for ACL" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L312 | neighbors=[ADConnectionError, DependencyMissingError, .get_aces()]
- "ad_ldap_enum_rationale_85": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L85 | neighbors=[ADConnectionError, DependencyMissingError, ACE]
- "ad_ldap_enum_rationale_86": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L86 | neighbors=[ADConnectionError, DependencyMissingError, ACE]
- "ad_ntlm_relay_ntlmrelaychecker_check_smb_signing": ".check_smb_signing()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L38 | neighbors=[NTLMRelayChecker, ._probe_smb_host(), For each IP, returns {signing_enabled, …]
- "ad_orchestrator_adassessmentrunner_run": ".run()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L50 | neighbors=[ADAssessmentRunner, ._anonymous_bind_finding(), Returns {findings: [...], stats: {...},…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-035.json

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
