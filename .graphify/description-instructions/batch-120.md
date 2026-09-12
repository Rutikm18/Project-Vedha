# Node Description Batch 121 of 380

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "scripts_startup_validator_databaseconnectivityvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L313 | neighbors=[DatabaseConnectivityValidator, CheckResult, .add()]
- "scripts_startup_validator_databaseurlvalidator": "DatabaseURLValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L244 | neighbors=[startup_validator.py, .validate(), Validates DATABASE_URL format and safet…]
- "scripts_startup_validator_databaseurlvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L249 | neighbors=[DatabaseURLValidator, CheckResult, .add()]
- "scripts_startup_validator_detectionenginevalidator": "DetectionEngineValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L279 | neighbors=[startup_validator.py, .validate(), Validates the baked-in detection engine…]
- "scripts_startup_validator_detectionenginevalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L282 | neighbors=[DetectionEngineValidator, CheckResult, .add()]
- "scripts_startup_validator_redisconnectivityvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L357 | neighbors=[RedisConnectivityValidator, CheckResult, .add()]
- "scripts_startup_validator_secretsvalidator": "SecretsValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L120 | neighbors=[startup_validator.py, Validates secrets meet minimum strength…, .validate()]
- "scripts_startup_validator_secretsvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L125 | neighbors=[SecretsValidator, CheckResult, .add()]
- "scripts_startup_validator_validationreport_raise_if_errors": ".raise_if_errors()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L62 | neighbors=[run_all_validators(), ValidationReport, StartupValidationError]
- "services_agent_policy_classify_action": "classify_action()" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L49 | neighbors=[agent_policy.py, evaluate_action(), Map an action name to its risk tier; un…]
- "services_agent_policy_decision": "Decision" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L74 | neighbors=[agent_policy.py, _deny(), evaluate_action()]
- "services_agent_policy_deny": "_deny()" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L82 | neighbors=[agent_policy.py, Decision, evaluate_action()]
- "services_audit": "audit.py" | kind=code-symbol | source=manager/backend/app/services/audit.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, record_audit(), audit.py — the append-only audit-log wr…]
- "services_evidence_summary_enrichment_facts": "_enrichment_facts()" | kind=code-symbol | source=manager/backend/app/services/evidence_summary.py:L106 | neighbors=[evidence_summary.py, _percentile(), summarize_evidence()]
- "services_evidence_summary_sentence_case": "_sentence_case()" | kind=code-symbol | source=manager/backend/app/services/evidence_summary.py:L66 | neighbors=[evidence_summary.py, _format_value(), summarize_evidence()]
- "services_finding_ai_extract_json": "_extract_json()" | kind=code-symbol | source=manager/backend/app/services/finding_ai.py:L71 | neighbors=[finding_ai.py, generate_content_overrides(), Pull the first JSON object out of a com…]
- "services_finding_ai_validate": "_validate()" | kind=code-symbol | source=manager/backend/app/services/finding_ai.py:L96 | neighbors=[finding_ai.py, generate_content_overrides(), Keep only well-formed override fields; …]
- "services_finding_compliance": "finding_compliance.py" | kind=code-symbol | source=manager/backend/app/services/finding_compliance.py:L1 | neighbors=[ef14810 Implement instance locking mech…, compliance_for(), finding_compliance.py — deterministic f…]
- "services_finding_content_build_exploitation": "_build_exploitation()" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L309 | neighbors=[finding_content.py, ExploitationView, finding_content()]
- "services_finding_content_exploit_maturity": "exploit_maturity()" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L277 | neighbors=[finding_content.py, finding_content(), Map exploitation signals to the fronten…]
- "services_finding_content_exploitationview": "ExploitationView" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L206 | neighbors=[finding_content.py, _build_exploitation(), The honest exploitation posture of a fi…]
- "services_finding_content_findingcontent": "FindingContent" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L223 | neighbors=[finding_content.py, finding_content(), .to_dict()]
- "services_finding_enrichment": "finding_enrichment.py" | kind=code-symbol | source=manager/backend/app/services/finding_enrichment.py:L1 | neighbors=[ef14810 Implement instance locking mech…, detail_enrichment(), finding_enrichment.py — assemble the pe…]
- "services_finding_events_detected_actor": "_detected_actor()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L81 | neighbors=[finding_events.py, Best label for who first produced this …, synthesize_events()]
- "services_finding_events_event_type_for_status": "event_type_for_status()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L173 | neighbors=[finding_events.py, _val(), Map a target FindingStatus to its speci…]
- "services_finding_events_record_event": "record_event()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L160 | neighbors=[finding_events.py, Append one immutable audit row. The cal…, _val()]
- "services_finding_metrics": "finding_metrics.py" | kind=code-symbol | source=manager/backend/app/services/finding_metrics.py:L1 | neighbors=[1727f4f feat(findings): MTTR + open-by-…, compute_mttr(), finding_metrics.py — mobilization metri…]
- "services_finding_priority_priority_key": "priority_key()" | kind=code-symbol | source=manager/backend/app/services/finding_priority.py:L49 | neighbors=[finding_priority.py, severity_rank(), In-memory urgency key: ``(severity_tier…]
- "services_finding_priority_severity_rank": "severity_rank()" | kind=code-symbol | source=manager/backend/app/services/finding_priority.py:L38 | neighbors=[finding_priority.py, priority_key(), Rank a severity (enum member or string,…]
- "services_job_attempt_service_claim_job_attempt": "claim_job_attempt()" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L24 | neighbors=[job_attempt_service.py, AttemptClaim, Atomically claim a pending job and crea…]
- "services_job_result_service_sanitize_jsonb": "sanitize_jsonb()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L29 | neighbors=[job_result_service.py, process_job_result(), Recursively strip NUL (U+0000) from eve…]
- "services_llm_anthropic_system_blocks": "_anthropic_system_blocks()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L52 | neighbors=[llm.py, ._anthropic(), Shape the system prompt into Anthropic …]
- "services_llm_http_client_asyncllmhttpclient": "AsyncLlmHttpClient" | kind=code-symbol | source=manager/backend/app/services/llm_http_client.py:L17 | neighbors=[llm_http_client.py, .open(), Create bounded ``httpx.AsyncClient`` in…]
- "services_llm_is_local_ollama_model": "_is_local_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L16 | neighbors=[llm.py, ._runtime(), .status()]
- "services_llm_managerllmservice_build_system": "._build_system()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L376 | neighbors=[ManagerLlmService, .generate(), .generate_with_fallback()]
- "services_llm_managerllmservice_gemini": "._gemini()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L633 | neighbors=[ManagerLlmService, ._dispatch(), ._client()]
- "services_notifications_enqueue_notification": "enqueue_notification()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L132 | neighbors=[notifications.py, Producer API: enqueue a durable notify …, Producer API: enqueue a durable notify …]
- "services_portal_metrics_is_closed": "_is_closed()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L28 | neighbors=[portal_metrics.py, open_closed_counts(), severity_breakdown()]
- "services_portal_metrics_open_closed_counts": "open_closed_counts()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L44 | neighbors=[portal_metrics.py, _is_closed(), (open, closed) totals over the given fi…]
- "services_portal_metrics_severity_breakdown": "severity_breakdown()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L32 | neighbors=[portal_metrics.py, Count findings by severity (all five bu…, _is_closed()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-120.json

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
