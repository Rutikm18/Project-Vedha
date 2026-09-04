# Node Description Batch 261 of 332

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

- "scope_page_splitcidr": "splitCidr()" | kind=code-symbol | source=manager/frontend/app/portal/scope/page.tsx:L24 | neighbors=[page.tsx] | lang=en
- "scripts_seed_admin_rationale_151": "Warn if the tenant has multiple admins or a stale admin email." | kind=entity | source=manager/backend/scripts/seed_admin.py:L151 | neighbors=[_detect_drift()] | lang=en
- "scripts_seed_admin_rationale_193": "All DB work in a single transaction. Rolls back on any failure.     Verifies the" | kind=entity | source=manager/backend/scripts/seed_admin.py:L193 | neighbors=[_seed_once()] | lang=en
- "scripts_seed_admin_rationale_295": "Exponential-backoff retry for transient DB connectivity issues." | kind=entity | source=manager/backend/scripts/seed_admin.py:L295 | neighbors=[_seed_with_retry()] | lang=en
- "scripts_seed_admin_rationale_96": "Returns (email, password, tenant_name, force_reset).     Raises SeedConfiguratio" | kind=entity | source=manager/backend/scripts/seed_admin.py:L96 | neighbors=[_validate_env()] | lang=en
- "scripts_seed_admin_seed": "seed()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L40 | neighbors=[seed_admin.py] | lang=en
- "scripts_startup_validator_rationale_1": "Vedha Startup Validator ======================= Runs at application boot — befor" | kind=entity | source=manager/backend/scripts/startup_validator.py:L1 | neighbors=[startup_validator.py] | lang=en
- "scripts_startup_validator_rationale_121": "Validates secrets meet minimum strength requirements." | kind=entity | source=manager/backend/scripts/startup_validator.py:L121 | neighbors=[SecretsValidator] | lang=en
- "scripts_startup_validator_rationale_152": "Validates APP_ENV and related production flags." | kind=entity | source=manager/backend/scripts/startup_validator.py:L152 | neighbors=[AppEnvironmentValidator] | lang=en
- "scripts_startup_validator_rationale_175": "Validates CORS_ORIGINS is production-safe." | kind=entity | source=manager/backend/scripts/startup_validator.py:L175 | neighbors=[CorsValidator] | lang=en
- "scripts_startup_validator_rationale_215": "Validates secure cookie configuration." | kind=entity | source=manager/backend/scripts/startup_validator.py:L215 | neighbors=[CookieValidator] | lang=en
- "scripts_startup_validator_rationale_245": "Validates DATABASE_URL format and safety." | kind=entity | source=manager/backend/scripts/startup_validator.py:L245 | neighbors=[DatabaseURLValidator] | lang=en
- "scripts_startup_validator_rationale_28": "Raised when a required configuration invariant is violated at boot." | kind=entity | source=manager/backend/scripts/startup_validator.py:L28 | neighbors=[StartupValidationError] | lang=en
- "scripts_startup_validator_rationale_280": "Validates the baked-in detection engine is present." | kind=entity | source=manager/backend/scripts/startup_validator.py:L280 | neighbors=[DetectionEngineValidator] | lang=en
- "scripts_startup_validator_rationale_311": "Verifies actual database connectivity at startup." | kind=entity | source=manager/backend/scripts/startup_validator.py:L311 | neighbors=[DatabaseConnectivityValidator] | lang=en
- "scripts_startup_validator_rationale_355": "Verifies Redis connectivity at startup." | kind=entity | source=manager/backend/scripts/startup_validator.py:L355 | neighbors=[RedisConnectivityValidator] | lang=en
- "scripts_startup_validator_rationale_397": "Run all validators. Use in FastAPI lifespan:          from scripts.startup_valid" | kind=entity | source=manager/backend/scripts/startup_validator.py:L397 | neighbors=[run_all_validators()] | lang=en
- "scripts_startup_validator_rationale_73": "Validates required env vars are present and non-default." | kind=entity | source=manager/backend/scripts/startup_validator.py:L73 | neighbors=[ConfigValidator] | lang=en
- "scripts_startup_validator_validationreport_errors": ".errors()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L49 | neighbors=[ValidationReport] | lang=en
- "scripts_startup_validator_validationreport_warnings": ".warnings()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L53 | neighbors=[ValidationReport] | lang=en
- "services_agent_policy_rationale_1": "agent_policy.py — the deterministic policy engine for the Autonomous Engagement" | kind=entity | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[agent_policy.py] | lang=en
- "services_agent_policy_rationale_50": "Map an action name to its risk tier; unknown actions fail closed." | kind=entity | source=manager/backend/app/services/agent_policy.py:L50 | neighbors=[classify_action()] | lang=en
- "services_agent_policy_rationale_56": "The deterministic authorization envelope for one engagement's agent." | kind=entity | source=manager/backend/app/services/agent_policy.py:L56 | neighbors=[RulesOfEngagement] | lang=en
- "services_agent_policy_rationale_68": "Running engagement usage, checked against the blast-radius caps." | kind=entity | source=manager/backend/app/services/agent_policy.py:L68 | neighbors=[UsageCounters] | lang=en
- "services_agent_policy_rationale_89": "Decide whether `action` may proceed under `roe`. Order is deliberate:     hard d" | kind=entity | source=manager/backend/app/services/agent_policy.py:L89 | neighbors=[evaluate_action()] | lang=en
- "services_analytics_rationale_1": "Exposure analytics — protocol risk + zone health.  Derives two dashboard aggrega" | kind=entity | source=manager/backend/app/services/analytics.py:L1 | neighbors=[analytics.py] | lang=en
- "services_audit_rationale_1": "audit.py — the append-only audit-log writer, shared by the operator and portal r" | kind=entity | source=manager/backend/app/services/audit.py:L1 | neighbors=[audit.py] | lang=en
- "services_audit_rationale_16": "Append one immutable audit row (caller flushes within its own txn)." | kind=entity | source=manager/backend/app/services/audit.py:L16 | neighbors=[record_audit()] | lang=en
- "services_finding_events_rationale_1": "finding_events.py — the finding lifecycle audit trail.  Two sources feed one tim" | kind=entity | source=manager/backend/app/services/finding_events.py:L1 | neighbors=[finding_events.py] | lang=en
- "services_finding_events_rationale_109": "Derive the canonical lifecycle events that the finding's timestamp columns     a" | kind=entity | source=manager/backend/app/services/finding_events.py:L109 | neighbors=[synthesize_events()] | lang=en
- "services_finding_events_rationale_163": "Append one immutable audit row. The caller owns the transaction/flush." | kind=entity | source=manager/backend/app/services/finding_events.py:L163 | neighbors=[record_event()] | lang=en
- "services_finding_events_rationale_174": "Map a target FindingStatus to its specific event kind (so 'confirmed' reads" | kind=entity | source=manager/backend/app/services/finding_events.py:L174 | neighbors=[event_type_for_status()] | lang=en
- "services_finding_events_rationale_207": "Merge stored + synthesized events, oldest-first. A stored event of a given     k" | kind=entity | source=manager/backend/app/services/finding_events.py:L207 | neighbors=[merge_timeline()] | lang=pt
- "services_finding_events_rationale_217": "The finding's full lifecycle timeline: stored audit rows merged with the     eve" | kind=entity | source=manager/backend/app/services/finding_events.py:L217 | neighbors=[build_timeline()] | lang=en
- "services_finding_events_rationale_55": "Accept a FindingEventType/FindingStatus enum or a bare string." | kind=entity | source=manager/backend/app/services/finding_events.py:L55 | neighbors=[_val()] | lang=pt
- "services_finding_events_rationale_82": "Best label for who first produced this finding, from its provenance.     A netwo" | kind=entity | source=manager/backend/app/services/finding_events.py:L82 | neighbors=[_detected_actor()] | lang=en
- "services_job_attempt_service_rationale_31": "Atomically claim a pending job and create its fenced attempt ledger row." | kind=entity | source=manager/backend/app/services/job_attempt_service.py:L31 | neighbors=[claim_job_attempt()] | lang=en
- "services_job_attempt_service_rationale_94": "Renew only the currently installed running attempt/fence." | kind=entity | source=manager/backend/app/services/job_attempt_service.py:L94 | neighbors=[renew_job_attempt()] | lang=en
- "services_job_result_service_rationale_111": "Return result identities outside the job's authoritative IP scope.      Fail clo" | kind=entity | source=manager/backend/app/services/job_result_service.py:L111 | neighbors=[validate_result_scope()] | lang=en
- "services_job_result_service_rationale_117": "Parse a probe identity as an IP, tolerating common host:port notation." | kind=entity | source=manager/backend/app/services/job_result_service.py:L117 | neighbors=[_identity_ip()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-260.json

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
