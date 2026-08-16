# Node Description Batch 166 of 209

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

- "scripts_seed_admin_seed": "seed()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L40 | neighbors=[seed_admin.py]
- "scripts_startup_validator_rationale_1": "Vedha Startup Validator ======================= Runs at application boot — befor" | kind=entity | source=manager/backend/scripts/startup_validator.py:L1 | neighbors=[startup_validator.py]
- "scripts_startup_validator_rationale_121": "Validates secrets meet minimum strength requirements." | kind=entity | source=manager/backend/scripts/startup_validator.py:L121 | neighbors=[SecretsValidator]
- "scripts_startup_validator_rationale_152": "Validates APP_ENV and related production flags." | kind=entity | source=manager/backend/scripts/startup_validator.py:L152 | neighbors=[AppEnvironmentValidator]
- "scripts_startup_validator_rationale_175": "Validates CORS_ORIGINS is production-safe." | kind=entity | source=manager/backend/scripts/startup_validator.py:L175 | neighbors=[CorsValidator]
- "scripts_startup_validator_rationale_215": "Validates secure cookie configuration." | kind=entity | source=manager/backend/scripts/startup_validator.py:L215 | neighbors=[CookieValidator]
- "scripts_startup_validator_rationale_245": "Validates DATABASE_URL format and safety." | kind=entity | source=manager/backend/scripts/startup_validator.py:L245 | neighbors=[DatabaseURLValidator]
- "scripts_startup_validator_rationale_28": "Raised when a required configuration invariant is violated at boot." | kind=entity | source=manager/backend/scripts/startup_validator.py:L28 | neighbors=[StartupValidationError]
- "scripts_startup_validator_rationale_280": "Validates the baked-in detection engine is present." | kind=entity | source=manager/backend/scripts/startup_validator.py:L280 | neighbors=[DetectionEngineValidator]
- "scripts_startup_validator_rationale_311": "Verifies actual database connectivity at startup." | kind=entity | source=manager/backend/scripts/startup_validator.py:L311 | neighbors=[DatabaseConnectivityValidator]
- "scripts_startup_validator_rationale_355": "Verifies Redis connectivity at startup." | kind=entity | source=manager/backend/scripts/startup_validator.py:L355 | neighbors=[RedisConnectivityValidator]
- "scripts_startup_validator_rationale_397": "Run all validators. Use in FastAPI lifespan:          from scripts.startup_valid" | kind=entity | source=manager/backend/scripts/startup_validator.py:L397 | neighbors=[run_all_validators()]
- "scripts_startup_validator_rationale_73": "Validates required env vars are present and non-default." | kind=entity | source=manager/backend/scripts/startup_validator.py:L73 | neighbors=[ConfigValidator]
- "scripts_startup_validator_validationreport_errors": ".errors()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L49 | neighbors=[ValidationReport]
- "scripts_startup_validator_validationreport_warnings": ".warnings()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L53 | neighbors=[ValidationReport]
- "services_analytics_rationale_1": "Exposure analytics — protocol risk + zone health.  Derives two dashboard aggrega" | kind=entity | source=manager/backend/app/services/analytics.py:L1 | neighbors=[analytics.py]
- "services_audit_rationale_1": "audit.py — the append-only audit-log writer, shared by the operator and portal r" | kind=entity | source=manager/backend/app/services/audit.py:L1 | neighbors=[audit.py]
- "services_audit_rationale_16": "Append one immutable audit row (caller flushes within its own txn)." | kind=entity | source=manager/backend/app/services/audit.py:L16 | neighbors=[record_audit()]
- "services_job_attempt_service_rationale_31": "Atomically claim a pending job and create its fenced attempt ledger row." | kind=entity | source=manager/backend/app/services/job_attempt_service.py:L31 | neighbors=[claim_job_attempt()]
- "services_job_attempt_service_rationale_94": "Renew only the currently installed running attempt/fence." | kind=entity | source=manager/backend/app/services/job_attempt_service.py:L94 | neighbors=[renew_job_attempt()]
- "services_job_result_service_rationale_137": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L137 | neighbors=[process_job_result()]
- "services_job_result_service_rationale_30": "Stable idempotency checksum for one attempt completion payload." | kind=entity | source=manager/backend/app/services/job_result_service.py:L30 | neighbors=[result_checksum()]
- "services_job_result_service_rationale_327": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L327 | neighbors=[_promote_assets()]
- "services_job_result_service_rationale_356": "Stamp the probe's evidence-based device role onto an Asset (create/update)." | kind=entity | source=manager/backend/app/services/job_result_service.py:L356 | neighbors=[_apply_device_profile()]
- "services_job_result_service_rationale_379": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L379 | neighbors=[_promote_assets()]
- "services_job_result_service_rationale_42": "Return network identities that could create assets or findings.      Scanner-lev" | kind=entity | source=manager/backend/app/services/job_result_service.py:L42 | neighbors=[_result_network_identities()]
- "services_job_result_service_rationale_72": "Parse a probe identity as an IP, tolerating common host:port notation." | kind=entity | source=manager/backend/app/services/job_result_service.py:L72 | neighbors=[_identity_ip()]
- "services_job_result_service_rationale_91": "Return result identities outside the job's authoritative IP scope.      Fail clo" | kind=entity | source=manager/backend/app/services/job_result_service.py:L91 | neighbors=[validate_result_scope()]
- "services_llm_airuntimeerror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L22 | neighbors=[AiRuntimeError]
- "services_llm_managerllmservice_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L75 | neighbors=[ManagerLlmService]
- "services_llm_rationale_259": "Call one provider and normalize failures to AiRuntimeError.         Preserves th" | kind=entity | source=manager/backend/app/services/llm.py:L259 | neighbors=[._dispatch()]
- "services_llm_rationale_301": "Ordered runtimes to try: requested/default first, then the OpenRouter         fr" | kind=entity | source=manager/backend/app/services/llm.py:L301 | neighbors=[._fallback_candidates()]
- "services_llm_rationale_325": "Try each candidate until one succeeds. On ANY provider failure (credit         e" | kind=entity | source=manager/backend/app/services/llm.py:L325 | neighbors=[.generate_with_fallback()]
- "services_llm_rationale_85": "First configured cloud provider, or None. Cloud-only: never Ollama." | kind=entity | source=manager/backend/app/services/llm.py:L85 | neighbors=[._auto_cloud_provider()]
- "services_portal_metrics_metricfinding": "MetricFinding" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L21 | neighbors=[portal_metrics.py]
- "services_portal_metrics_rationale_1": "portal_metrics.py — pure aggregations for the customer dashboard.  Kept pure (no" | kind=entity | source=manager/backend/app/services/portal_metrics.py:L1 | neighbors=[portal_metrics.py]
- "services_portal_metrics_rationale_33": "Count findings by severity (all five buckets always present, zero-filled).     o" | kind=entity | source=manager/backend/app/services/portal_metrics.py:L33 | neighbors=[severity_breakdown()]
- "services_portal_metrics_rationale_45": "(open, closed) totals over the given findings." | kind=entity | source=manager/backend/app/services/portal_metrics.py:L45 | neighbors=[open_closed_counts()]
- "services_portal_metrics_rationale_56": "Per-month {period, opened, closed} for the last `months` months.      opened = f" | kind=entity | source=manager/backend/app/services/portal_metrics.py:L56 | neighbors=[status_timeline()]
- "services_posture_rationale_1": "Posture scoring & patch-comparison — the single source of truth behind the dashb" | kind=entity | source=manager/backend/app/services/posture.py:L1 | neighbors=[posture.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-165.json

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
