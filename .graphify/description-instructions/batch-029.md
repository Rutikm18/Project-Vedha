# Node Description Batch 30 of 104

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
- "ad_ldap_enum_domain_to_base_dn": "_domain_to_base_dn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L105 | neighbors=[ldap_enum.py, .connect(), corp.local -> DC=corp,DC=local]
- "ad_ldap_enum_ldapenumerator_check_anonymous_bind": ".check_anonymous_bind()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L286 | neighbors=[LDAPEnumerator, .unbind(), True if the DC accepts an anonymous bin…]
- "ad_ldap_enum_ldapenumerator_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L128 | neighbors=[LDAPEnumerator, _domain_to_base_dn(), Bind to the domain controller. Returns …]
- "ad_ldap_enum_ldapenumerator_parse_security_descriptor": "._parse_security_descriptor()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L344 | neighbors=[LDAPEnumerator, .get_aces(), ACE]
- "ad_ldap_enum_ldapenumerator_require_conn": "._require_conn()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L189 | neighbors=[LDAPEnumerator, .get_aces(), ._search()]
- "ad_ldap_enum_rationale_1": "LDAPEnumerator — read-only Active Directory enumeration over LDAP/LDAPS.  Uses l" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ADConnectionError, DependencyMissingError, ldap_enum.py]
- "ad_ldap_enum_rationale_106": "corp.local -> DC=corp,DC=local" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L106 | neighbors=[ADConnectionError, DependencyMissingError, _domain_to_base_dn()]
- "ad_ldap_enum_rationale_119": "Read-only AD enumeration. One instance == one bound connection." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L119 | neighbors=[ADConnectionError, DependencyMissingError, LDAPEnumerator]
- "ad_ldap_enum_rationale_138": "Bind to the domain controller. Returns self for chaining.          Raises Depend" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L138 | neighbors=[ADConnectionError, DependencyMissingError, .connect()]
- "ad_ldap_enum_rationale_215": "All user accounts (excludes computer accounts)." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L215 | neighbors=[ADConnectionError, DependencyMissingError, .get_users()]
- "ad_ldap_enum_rationale_287": "True if the DC accepts an anonymous bind that can read directory data         (a" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L287 | neighbors=[ADConnectionError, DependencyMissingError, .check_anonymous_bind()]
- "ad_ldap_enum_rationale_312": "Parse the nTSecurityDescriptor of an object into a list of ACEs for ACL" | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L312 | neighbors=[ADConnectionError, DependencyMissingError, .get_aces()]
- "ad_ldap_enum_rationale_86": "A simplified access-control entry parsed from nTSecurityDescriptor." | kind=entity | source=manager/backend/app/ad/ldap_enum.py:L86 | neighbors=[ADConnectionError, DependencyMissingError, ACE]
- "ad_ntlm_relay": "ntlm_relay.py" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L1 | neighbors=[NTLMRelayChecker, NTLMRelayChecker — detect missing SMB/L…, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ntlm_relay_ntlmrelaychecker_check_smb_signing": ".check_smb_signing()" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L38 | neighbors=[NTLMRelayChecker, ._probe_smb_host(), For each IP, returns {signing_enabled, …]
- "ad_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[ADAssessmentRunner, ADAssessmentRunner — runs the full Acti…, 298a9d4 trim frontend to 7 core pages; …]
- "ad_orchestrator_adassessmentrunner_run": ".run()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L50 | neighbors=[ADAssessmentRunner, ._anonymous_bind_finding(), Returns {findings: [...], stats: {...},…]
- "agent_agent_execute_ad_enum": "execute_ad_enum()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L303 | neighbors=[agent.py, parse_spn_output(), Impacket-based AD enumeration: Kerberoa…]
- "agent_agent_execute_eyewitness": "execute_eyewitness()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L527 | neighbors=[agent.py, extract_web_urls_from_nmap(), EyeWitness screenshot evidence collecti…]
- "agent_agent_execute_smb_validation": "execute_smb_validation()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L373 | neighbors=[agent.py, count_by_severity(), NetExec SMB validation: signing, null s…]
- "agent_agent_execute_tls_scan": "execute_tls_scan()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L453 | neighbors=[agent.py, count_by_severity(), testssl.sh TLS/SSL analysis.]
- "agent_agent_execute_vuln_scan": "execute_vuln_scan()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L238 | neighbors=[agent.py, count_by_severity(), Nuclei vulnerability scan — production-…]
- "agent_agent_extract_web_urls_from_nmap": "extract_web_urls_from_nmap()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L499 | neighbors=[agent.py, execute_eyewitness(), Extract HTTP/HTTPS URLs from nmap XML o…]
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=probe/agent/agent.py:L42 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…]
- "agent_agent_obtainidentity": ".obtainIdentity()" | kind=code-symbol | source=probe-go/agent/agent.go:L272 | neighbors=[agent.py, say(), .Run()]
- "agent_agent_runautonomousengagement": "runAutonomousEngagement()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L95 | neighbors=[agent.py, isBlocked(), requiresApproval()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-029.json

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
