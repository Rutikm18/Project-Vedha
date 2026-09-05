# Node Description Batch 89 of 336

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

- "workflow_cli_main": "_main()" | kind=code-symbol | source=probe/workflow/cli.py:L95 | neighbors=[cli.py, _build_creds(), _build_mode(), build_parser()]
- "workflow_execution_executiontrace_failed": ".failed()" | kind=code-symbol | source=probe/workflow/execution.py:L380 | neighbors=[ExecutionTrace, ._has_active_coverage(), True when execution produced errors and…, True when execution produced errors and…]
- "workflow_execution_scanner_failure_result": "scanner_failure_result()" | kind=code-symbol | source=probe/workflow/execution.py:L221 | neighbors=[execution.py, Represent an unexpected component excep…, classify_scanner_error(), Represent an unexpected component excep…]
- "workflow_host_health_heartbeat_misses": "_heartbeat_misses()" | kind=code-symbol | source=probe/workflow/host_health.py:L95 | neighbors=[host_health.py, _env_int(), .watch(), Consecutive missed heartbeats before a …]
- "workflow_host_health_hosthealthmonitor_mark_offline": "._mark_offline()" | kind=code-symbol | source=probe/workflow/host_health.py:L244 | neighbors=[HostHealthMonitor, .confirm(), ._state(), .watch()]
- "workflow_host_health_hosthealthmonitor_observe": ".observe()" | kind=code-symbol | source=probe/workflow/host_health.py:L152 | neighbors=[HostHealthMonitor, ._is_silence(), ._state(), Feed one component's results in.       …]
- "workflow_host_health_strike_threshold": "_strike_threshold()" | kind=code-symbol | source=probe/workflow/host_health.py:L82 | neighbors=[host_health.py, .__init__(), Consecutive silent components before we…, _env_int()]
- "workflow_modes_assessment": "assessment()" | kind=code-symbol | source=probe/workflow/modes.py:L111 | neighbors=[modes.py, EngagementMode, Full funnel, every branch the profile a…, Full funnel, every branch the profile a…]
- "workflow_modes_re_scan": "re_scan()" | kind=code-symbol | source=probe/workflow/modes.py:L126 | neighbors=[modes.py, Loads a prior engagement's cache; only …, EngagementMode, Loads a prior engagement's cache; only …]
- "workflow_modes_triage": "triage()" | kind=code-symbol | source=probe/workflow/modes.py:L104 | neighbors=[modes.py, Discovery + ports + banner only — no de…, EngagementMode, Discovery + ports + banner only — no de…]
- "workflow_router_looks_like_ssh": "looks_like_ssh()" | kind=code-symbol | source=probe/workflow/router.py:L114 | neighbors=[router.py, True when a service banner is an SSH id…, route_branches(), True when the port was OBSERVED speakin…]
- "workflow_workflow_engine_timed": "_timed()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L269 | neighbors=[workflow_engine.py, Accumulate wall time for a stage. No-op…, _run_branch(), run_engagement()]
- "ad_adcs_adcschecker_check_esc4": ".check_esc4()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L147 | neighbors=[ADCSChecker, .generate_findings(), ESC4: a low-privilege principal holds a…]
- "ad_adcs_adcschecker_check_esc8": ".check_esc8()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L160 | neighbors=[ADCSChecker, .generate_findings(), ESC8: the CA exposes a web-enrollment (…]
- "ad_adcs_adcschecker_enrollment_principals": "._enrollment_principals()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L116 | neighbors=[ADCSChecker, .enumerate_templates(), Principals with an enrollment ExtendedR…]
- "ad_asreproast_asreproastchecker_format_asrep_hash": "._format_asrep_hash()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L90 | neighbors=[ASREPRoastChecker, .request_asrep(), Render an AS-REP as a hashcat $krb5asre…]
- "ad_asreproast_asreproastchecker_request_asrep": ".request_asrep()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L54 | neighbors=[ASREPRoastChecker, ._format_asrep_hash(), Request an AS-REP for ``username`` with…]
- "ad_asreproast_rationale_1": "ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and" | kind=entity | source=manager/backend/app/ad/asreproast.py:L1 | neighbors=[asreproast.py, LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_35": "Enumerate AS-REP roastable accounts and capture AS-REP evidence." | kind=entity | source=manager/backend/app/ad/asreproast.py:L35 | neighbors=[ASREPRoastChecker, LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_43": "Usernames of enabled accounts with pre-authentication not required." | kind=entity | source=manager/backend/app/ad/asreproast.py:L43 | neighbors=[.get_no_preauth_accounts(), LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_55": "Request an AS-REP for ``username`` with no credentials and return the         $k" | kind=entity | source=manager/backend/app/ad/asreproast.py:L55 | neighbors=[.request_asrep(), LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_91": "Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)." | kind=entity | source=manager/backend/app/ad/asreproast.py:L91 | neighbors=[._format_asrep_hash(), LDAPEnumerator, FindingSeverity]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-088.json

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
