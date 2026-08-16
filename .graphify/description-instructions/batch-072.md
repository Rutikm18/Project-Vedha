# Node Description Batch 73 of 209

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

- "services_job_attempt_service_claim_job_attempt": "claim_job_attempt()" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L24 | neighbors=[job_attempt_service.py, AttemptClaim, Atomically claim a pending job and crea…] | lang=en
- "services_job_result_service_apply_device_profile": "_apply_device_profile()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L355 | neighbors=[job_result_service.py, _promote_assets(), Stamp the probe's evidence-based device…] | lang=en
- "services_job_result_service_identity_ip": "_identity_ip()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L71 | neighbors=[job_result_service.py, Parse a probe identity as an IP, tolera…, validate_result_scope()] | lang=en
- "services_job_result_service_result_checksum": "result_checksum()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L29 | neighbors=[job_result_service.py, process_job_result(), Stable idempotency checksum for one att…] | lang=en
- "services_job_result_service_result_network_identities": "_result_network_identities()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L41 | neighbors=[job_result_service.py, Return network identities that could cr…, validate_result_scope()] | lang=en
- "services_llm_is_local_ollama_model": "_is_local_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L15 | neighbors=[llm.py, ._runtime(), .status()] | lang=en
- "services_llm_managerllmservice_auto_cloud_provider": "._auto_cloud_provider()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L84 | neighbors=[ManagerLlmService, ._default_runtime(), First configured cloud provider, or Non…] | lang=en
- "services_llm_managerllmservice_build_system": "._build_system()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L241 | neighbors=[ManagerLlmService, .generate(), .generate_with_fallback()] | lang=en
- "services_portal_metrics_is_closed": "_is_closed()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L28 | neighbors=[portal_metrics.py, open_closed_counts(), severity_breakdown()] | lang=en
- "services_portal_metrics_open_closed_counts": "open_closed_counts()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L44 | neighbors=[portal_metrics.py, _is_closed(), (open, closed) totals over the given fi…] | lang=en
- "services_portal_metrics_severity_breakdown": "severity_breakdown()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L32 | neighbors=[portal_metrics.py, Count findings by severity (all five bu…, _is_closed()] | lang=en
- "services_portal_metrics_status_timeline": "status_timeline()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L54 | neighbors=[portal_metrics.py, Per-month {period, opened, closed} for …, _period()] | lang=en
- "services_posture_clamp01": "_clamp01()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L43 | neighbors=[posture.py, aggregate(), _exploit_prob()] | lang=en
- "services_posture_exploit_prob": "_exploit_prob()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L67 | neighbors=[posture.py, compute_scores(), _clamp01()] | lang=en
- "services_posture_to_utc": "_to_utc()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L98 | neighbors=[posture.py, build_posture(), _present_in_run()] | lang=en
- "services_risk_rank": "risk_rank.py" | kind=code-symbol | source=manager/backend/app/services/risk_rank.py:L1 | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, compute_risk_rank(), risk_rank.py — one explainable 0-1000 p…] | lang=en
- "services_scope_crypto_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L34 | neighbors=[scope_crypto.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…] | lang=en
- "services_scope_crypto_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L77 | neighbors=[scope_crypto.py, encrypt_scope(), Convenience: dict → JSON → encrypt → ba…] | lang=en
- "services_scope_targets_expand_requested": "_expand_requested()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L37 | neighbors=[scope_targets.py, Expand raw target tokens (IP / CIDR / `…, validate_targets_in_scope()] | lang=en
- "services_sla_rationale_1": "SLA policy engine.  Turns a severity + \"first seen\" timestamp into a remediation" | kind=entity | source=manager/backend/app/services/sla.py:L1 | neighbors=[sla.py, FindingStatus, Finding] | lang=pt
- "services_sla_rationale_101": "Aggregate SLA states across a set of findings.      Returns counts per state plu" | kind=entity | source=manager/backend/app/services/sla.py:L101 | neighbors=[summarize(), FindingStatus, Finding] | lang=en
- "services_sla_rationale_61": "Compute the SLA state for one finding. Never raises on missing data." | kind=entity | source=manager/backend/app/services/sla.py:L61 | neighbors=[compute(), FindingStatus, Finding] | lang=en
- "services_sla_summarize": "summarize()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L100 | neighbors=[sla.py, Aggregate SLA states across a set of fi…, compute()] | lang=en
- "services_validation_ingest_apply_validation_outcome": "apply_validation_outcome()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L32 | neighbors=[validation_ingest.py, ingest_validation_result(), Apply a validation verdict to a finding…] | lang=en
- "services_validation_ingest_looks_like_validation_result": "looks_like_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L44 | neighbors=[validation_ingest.py, ingest_validation_result(), Cheap gate so normal scan submissions n…] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_computers_flags_dc": ".test_get_computers_flags_dc()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L132 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_groups_marks_privileged": ".test_get_groups_marks_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L150 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_disabled_account": ".test_get_users_disabled_account()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L123 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_parses_uac_and_spn": ".test_get_users_parses_uac_and_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L103 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_adaptive_rate_echoprotocol": "_EchoProtocol" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L177 | neighbors=[test_adaptive_rate.py, .connection_made(), .datagram_received()] | lang=en
- "tests_test_agent_auth_boundary_boundary_test_client": "_boundary_test_client()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L47 | neighbors=[test_agent_auth_boundary.py, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…] | lang=en
- "tests_test_agents_testaccesstokenexpiry": "TestAccessTokenExpiry" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L759 | neighbors=[test_agents.py, .test_custom_expiry_overrides_default(), ScanJobType] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_complete_retries_then_succeeds": ".test_complete_retries_then_succeeds()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L226 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_detection_rule_explanation": ".test_detection_rule_explanation()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L243 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_executive_summary_persists_pending": ".test_executive_summary_persists_pending()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L180 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()] | lang=en
- "tests_test_ai_engine_testllmreportgenerator_test_unavailable_without_client": ".test_unavailable_without_client()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L217 | neighbors=[TestLLMReportGenerator, _finding(), _mock_db()] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_explain_prediction_fallback_shape": ".test_explain_prediction_fallback_shape()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L78 | neighbors=[TestVulnPrioritizer, _asset(), _finding()] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_extract_features_order_and_values": ".test_extract_features_order_and_values()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L55 | neighbors=[TestVulnPrioritizer, _asset(), _finding()] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_higher_cvss_scores_higher": ".test_higher_cvss_scores_higher()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L73 | neighbors=[TestVulnPrioritizer, _asset(), _finding()] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_predict_priority_uses_fallback_when_untrained": ".test_predict_priority_uses_fallback_when_untrained()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L67 | neighbors=[TestVulnPrioritizer, _asset(), _finding()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-072.json

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
