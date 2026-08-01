# Node Description Batch 44 of 119

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

- "scanner_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…] | lang=en
- "scanner_init": "__init__.py" | kind=code-symbol | source=probe/scanner/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, VA scanner module — pure collection/sca…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "scanner_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()] | lang=en
- "scanner_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L173 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…] | lang=en
- "scanner_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L151 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…] | lang=en
- "scanner_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L160 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L211 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()] | lang=en
- "scanner_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L204 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()] | lang=en
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L462 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…] | lang=en
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L341 | neighbors=[.run(), ResultWriter, .to_json()] | lang=en
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L93 | neighbors=[run_cli(), ScopeGuard, ScopeError] | lang=en
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L141 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()] | lang=en
- "scanner_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from an SMB2 NEGOT…, .scan_target()] | lang=en
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L83 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()] | lang=en
- "scanner_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L44 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…] | lang=en
- "schemas_engagement_rationale_14": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L14 | neighbors=[EngagementStatus, FindingSeverity, validate_scope_entries()] | lang=en
- "services_llm_is_local_ollama_model": "_is_local_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L15 | neighbors=[llm.py, ._runtime(), .status()] | lang=en
- "services_llm_managerllmservice_anthropic": "._anthropic()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L317 | neighbors=[ManagerLlmService, ._client(), .generate()] | lang=en
- "services_llm_managerllmservice_ollama": "._ollama()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L263 | neighbors=[ManagerLlmService, .generate(), ._client()] | lang=en
- "services_llm_managerllmservice_openai": "._openai()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L300 | neighbors=[ManagerLlmService, .generate(), ._client()] | lang=en
- "services_llm_managerllmservice_openrouter": "._openrouter()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L279 | neighbors=[ManagerLlmService, .generate(), ._client()] | lang=en
- "services_scope_crypto_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L34 | neighbors=[scope_crypto.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…] | lang=en
- "services_scope_crypto_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L77 | neighbors=[scope_crypto.py, encrypt_scope(), Convenience: dict → JSON → encrypt → ba…] | lang=en
- "services_sla_rationale_1": "SLA policy engine.  Turns a severity + \"first seen\" timestamp into a remediation" | kind=entity | source=manager/backend/app/services/sla.py:L1 | neighbors=[FindingStatus, Finding, sla.py] | lang=pt
- "services_sla_rationale_101": "Aggregate SLA states across a set of findings.      Returns counts per state plu" | kind=entity | source=manager/backend/app/services/sla.py:L101 | neighbors=[FindingStatus, Finding, summarize()] | lang=en
- "services_sla_rationale_61": "Compute the SLA state for one finding. Never raises on missing data." | kind=entity | source=manager/backend/app/services/sla.py:L61 | neighbors=[FindingStatus, Finding, compute()] | lang=en
- "services_sla_summarize": "summarize()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L100 | neighbors=[sla.py, Aggregate SLA states across a set of fi…, compute()] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_computers_flags_dc": ".test_get_computers_flags_dc()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L132 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_groups_marks_privileged": ".test_get_groups_marks_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L150 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_disabled_account": ".test_get_users_disabled_account()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L123 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_parses_uac_and_spn": ".test_get_users_parses_uac_and_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L103 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_agents_testaccesstokenexpiry": "TestAccessTokenExpiry" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L648 | neighbors=[test_agents.py, ScanJobType, .test_custom_expiry_overrides_default()] | lang=en
- "tests_test_agents_testpromoteassets_test_dedupes_duplicate_services_in_same_probe_result": ".test_dedupes_duplicate_services_in_same_probe_result()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L610 | neighbors=[A single web scan can emit multiple fac…, TestPromoteAssets, A single web scan can emit multiple fac…] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_complete_retries_then_succeeds": ".test_complete_retries_then_succeeds()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L226 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_detection_rule_explanation": ".test_detection_rule_explanation()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L243 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_executive_summary_persists_pending": ".test_executive_summary_persists_pending()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L180 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_unavailable_without_client": ".test_unavailable_without_client()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L217 | neighbors=[TestLLMReportGenerator, _finding(), _mock_db()] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_explain_prediction_fallback_shape": ".test_explain_prediction_fallback_shape()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L78 | neighbors=[TestVulnPrioritizer, _asset(), _finding()] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_extract_features_order_and_values": ".test_extract_features_order_and_values()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L55 | neighbors=[TestVulnPrioritizer, _asset(), _finding()] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_higher_cvss_scores_higher": ".test_higher_cvss_scores_higher()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L73 | neighbors=[TestVulnPrioritizer, _asset(), _finding()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-043.json

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
