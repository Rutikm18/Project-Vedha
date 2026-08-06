# Node Description Batch 49 of 134

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

- "scanner_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L204 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()] | lang=en
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L462 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…] | lang=en
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L341 | neighbors=[.run(), ResultWriter, .to_json()] | lang=en
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L93 | neighbors=[run_cli(), ScopeGuard, ScopeError] | lang=en
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L141 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()] | lang=en
- "scanner_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from an SMB2 NEGOT…, .scan_target()] | lang=en
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L83 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()] | lang=en
- "scanner_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L44 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…] | lang=en
- "schemas_engagement_rationale_14": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L14 | neighbors=[EngagementStatus, FindingSeverity, validate_scope_entries()] | lang=en
- "scripts_startup_validator_appenvironmentvalidator": "AppEnvironmentValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L151 | neighbors=[startup_validator.py, .validate(), Validates APP_ENV and related productio…] | lang=en
- "scripts_startup_validator_appenvironmentvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L154 | neighbors=[AppEnvironmentValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_configvalidator": "ConfigValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L72 | neighbors=[startup_validator.py, .validate(), Validates required env vars are present…] | lang=en
- "scripts_startup_validator_configvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L93 | neighbors=[ConfigValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_cookievalidator": "CookieValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L214 | neighbors=[startup_validator.py, .validate(), Validates secure cookie configuration.] | lang=en
- "scripts_startup_validator_cookievalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L217 | neighbors=[CookieValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_corsvalidator": "CorsValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L174 | neighbors=[startup_validator.py, .validate(), Validates CORS_ORIGINS is production-sa…] | lang=en
- "scripts_startup_validator_corsvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L179 | neighbors=[CorsValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_databaseconnectivityvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L313 | neighbors=[DatabaseConnectivityValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_databaseurlvalidator": "DatabaseURLValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L244 | neighbors=[startup_validator.py, .validate(), Validates DATABASE_URL format and safet…] | lang=en
- "scripts_startup_validator_databaseurlvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L249 | neighbors=[DatabaseURLValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_detectionenginevalidator": "DetectionEngineValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L279 | neighbors=[startup_validator.py, .validate(), Validates the baked-in detection engine…] | lang=en
- "scripts_startup_validator_detectionenginevalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L282 | neighbors=[DetectionEngineValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_redisconnectivityvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L357 | neighbors=[RedisConnectivityValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_secretsvalidator": "SecretsValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L120 | neighbors=[startup_validator.py, Validates secrets meet minimum strength…, .validate()] | lang=en
- "scripts_startup_validator_secretsvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L125 | neighbors=[SecretsValidator, CheckResult, .add()] | lang=en
- "scripts_startup_validator_validationreport_raise_if_errors": ".raise_if_errors()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L62 | neighbors=[run_all_validators(), ValidationReport, StartupValidationError] | lang=en
- "services_job_attempt_service_claim_job_attempt": "claim_job_attempt()" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L24 | neighbors=[job_attempt_service.py, AttemptClaim, Atomically claim a pending job and crea…] | lang=en
- "services_job_result_service_identity_ip": "_identity_ip()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L71 | neighbors=[job_result_service.py, Parse a probe identity as an IP, tolera…, validate_result_scope()] | lang=en
- "services_job_result_service_result_checksum": "result_checksum()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L29 | neighbors=[job_result_service.py, process_job_result(), Stable idempotency checksum for one att…] | lang=en
- "services_job_result_service_result_network_identities": "_result_network_identities()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L41 | neighbors=[job_result_service.py, Return network identities that could cr…, validate_result_scope()] | lang=en
- "services_llm_is_local_ollama_model": "_is_local_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L15 | neighbors=[llm.py, ._runtime(), .status()] | lang=en
- "services_llm_managerllmservice_auto_cloud_provider": "._auto_cloud_provider()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L84 | neighbors=[ManagerLlmService, ._default_runtime(), First configured cloud provider, or Non…] | lang=en
- "services_llm_managerllmservice_build_system": "._build_system()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L241 | neighbors=[ManagerLlmService, .generate(), .generate_with_fallback()] | lang=en
- "services_posture_clamp01": "_clamp01()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L43 | neighbors=[posture.py, aggregate(), _exploit_prob()] | lang=en
- "services_posture_exploit_prob": "_exploit_prob()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L67 | neighbors=[posture.py, compute_scores(), _clamp01()] | lang=en
- "services_posture_to_utc": "_to_utc()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L98 | neighbors=[posture.py, build_posture(), _present_in_run()] | lang=en
- "services_scope_crypto_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L34 | neighbors=[scope_crypto.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…] | lang=en
- "services_scope_crypto_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L77 | neighbors=[scope_crypto.py, encrypt_scope(), Convenience: dict → JSON → encrypt → ba…] | lang=en
- "services_sla_rationale_1": "SLA policy engine.  Turns a severity + \"first seen\" timestamp into a remediation" | kind=entity | source=manager/backend/app/services/sla.py:L1 | neighbors=[sla.py, FindingStatus, Finding] | lang=pt
- "services_sla_rationale_101": "Aggregate SLA states across a set of findings.      Returns counts per state plu" | kind=entity | source=manager/backend/app/services/sla.py:L101 | neighbors=[summarize(), FindingStatus, Finding] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-048.json

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
