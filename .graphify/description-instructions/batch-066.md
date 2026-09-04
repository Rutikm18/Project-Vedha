# Node Description Batch 67 of 330

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
- "agent_agent_job_intent": "_job_intent()" | kind=code-symbol | source=probe/agent/agent.py:L102 | neighbors=[agent.py, Human label for what a job will actuall…, _ws_run_job(), Human label for what a job will actuall…] | lang=en
- "agent_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/agent/cli.py:L933 | neighbors=[cli.py, default_config_path(), _env(), main()] | lang=en
- "agent_cli_cmd_agents_list": "cmd_agents_list()" | kind=code-symbol | source=probe/agent/cli.py:L409 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_engagements_list": "cmd_engagements_list()" | kind=code-symbol | source=probe/agent/cli.py:L426 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_engagements_scope": "cmd_engagements_scope()" | kind=code-symbol | source=probe/agent/cli.py:L474 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_scan_status": "cmd_scan_status()" | kind=code-symbol | source=probe/agent/cli.py:L530 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_cmd_use_cases": "cmd_use_cases()" | kind=code-symbol | source=probe/agent/cli.py:L393 | neighbors=[cli.py, client_from_args(), .request(), output()] | lang=en
- "agent_cli_configstore_remove_profile": ".remove_profile()" | kind=code-symbol | source=probe/agent/cli.py:L96 | neighbors=[cmd_auth_logout(), ConfigStore, .load(), .save()] | lang=en
- "agent_cli_configstore_set_profile": ".set_profile()" | kind=code-symbol | source=probe/agent/cli.py:L90 | neighbors=[cmd_auth_login(), ConfigStore, .load(), .save()] | lang=en
- "agent_engine_env_number": "_env_number()" | kind=code-symbol | source=probe/agent/engine.py:L51 | neighbors=[engine.py, Read a bounded numeric safety setting w…, Read a bounded numeric safety setting w…, Read a bounded numeric safety setting w…] | lang=en
- "agent_engine_results_by_target": "_results_by_target()" | kind=code-symbol | source=probe/agent/engine.py:L453 | neighbors=[engine.py, _derive_devices(), _derive_exposure(), _derive_post_stage()] | lang=en
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=probe/agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…] | lang=en
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…] | lang=en
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L101 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…, Combined startup gauntlet: HW bind → li…] | lang=en
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L41 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()] | lang=en
- "agent_local_run_summarize": "summarize()" | kind=code-symbol | source=probe/agent/local_run.py:L90 | neighbors=[local_run.py, _main(), _clean(), _port_label()] | lang=en
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()] | lang=en
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target(), Remove targets that fall inside any exc…] | lang=en
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target(), Fetch the engagement's authoritative sc…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-066.json

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
