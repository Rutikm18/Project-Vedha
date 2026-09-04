# Node Description Batch 259 of 330

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

- "schemas_finding_rationale_105": "Compute the explainable 0-1000 unified rank at serialization time so         eve" | kind=entity | source=manager/backend/app/schemas/finding.py:L105 | neighbors=[._populate_risk_rank()]
- "schemas_finding_rationale_161": "Compute the explainable 0-1000 unified rank at serialization time so         eve" | kind=entity | source=manager/backend/app/schemas/finding.py:L161 | neighbors=[._populate_risk_rank()]
- "schemas_finding_rationale_22": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L22 | neighbors=[FindingPatch]
- "schemas_finding_rationale_69": "One entry in a finding's lifecycle timeline. `id` is null for synthesized     ev" | kind=entity | source=manager/backend/app/schemas/finding.py:L69 | neighbors=[FindingEventOut]
- "schemas_portal_clientassistantask_bounded": "._bounded()" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L142 | neighbors=[ClientAssistantAsk]
- "schemas_portal_rationale_1": "schemas/portal.py — customer-safe response shapes.  CRITICAL: these are WHITELIS" | kind=entity | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[portal.py]
- "schemas_portal_rationale_101": "A customer's rich scan request. The customer may ask for any active scan     typ" | kind=entity | source=manager/backend/app/schemas/portal.py:L101 | neighbors=[ScanRequestCreate]
- "schemas_portal_rationale_129": "One turn of the customer's conversation. Bounded so a crafted client can't     p" | kind=entity | source=manager/backend/app/schemas/portal.py:L129 | neighbors=[ClientAssistantMessage]
- "schemas_portal_rationale_23": "A finding as a CUSTOMER may see it. model_validate(from_attributes=True)     rea" | kind=entity | source=manager/backend/app/schemas/portal.py:L23 | neighbors=[ClientFindingOut]
- "schemas_portal_rationale_60": "One call powering the dashboard header: posture + KPI counts + queue state." | kind=entity | source=manager/backend/app/schemas/portal.py:L60 | neighbors=[ClientSummaryOut]
- "schemas_remediation_remediationplandetailout_normalize_risk_levels": ".normalize_risk_levels()" | kind=code-symbol | source=manager/backend/app/schemas/remediation.py:L43 | neighbors=[RemediationPlanDetailOut]
- "schemas_remediation_remediationstepout_normalize_risk": ".normalize_risk()" | kind=code-symbol | source=manager/backend/app/schemas/remediation.py:L23 | neighbors=[RemediationStepOut]
- "scope_page_hostcount": "hostCount()" | kind=code-symbol | source=manager/frontend/app/portal/scope/page.tsx:L31 | neighbors=[page.tsx]
- "scope_page_kpi": "Kpi()" | kind=code-symbol | source=manager/frontend/app/portal/scope/page.tsx:L40 | neighbors=[page.tsx]
- "scope_page_portalscope": "PortalScope()" | kind=code-symbol | source=manager/frontend/app/portal/scope/page.tsx:L50 | neighbors=[page.tsx]
- "scope_page_splitcidr": "splitCidr()" | kind=code-symbol | source=manager/frontend/app/portal/scope/page.tsx:L24 | neighbors=[page.tsx]
- "scripts_seed_admin_rationale_151": "Warn if the tenant has multiple admins or a stale admin email." | kind=entity | source=manager/backend/scripts/seed_admin.py:L151 | neighbors=[_detect_drift()]
- "scripts_seed_admin_rationale_193": "All DB work in a single transaction. Rolls back on any failure.     Verifies the" | kind=entity | source=manager/backend/scripts/seed_admin.py:L193 | neighbors=[_seed_once()]
- "scripts_seed_admin_rationale_295": "Exponential-backoff retry for transient DB connectivity issues." | kind=entity | source=manager/backend/scripts/seed_admin.py:L295 | neighbors=[_seed_with_retry()]
- "scripts_seed_admin_rationale_96": "Returns (email, password, tenant_name, force_reset).     Raises SeedConfiguratio" | kind=entity | source=manager/backend/scripts/seed_admin.py:L96 | neighbors=[_validate_env()]
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
- "services_agent_policy_rationale_1": "agent_policy.py — the deterministic policy engine for the Autonomous Engagement" | kind=entity | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[agent_policy.py]
- "services_agent_policy_rationale_50": "Map an action name to its risk tier; unknown actions fail closed." | kind=entity | source=manager/backend/app/services/agent_policy.py:L50 | neighbors=[classify_action()]
- "services_agent_policy_rationale_56": "The deterministic authorization envelope for one engagement's agent." | kind=entity | source=manager/backend/app/services/agent_policy.py:L56 | neighbors=[RulesOfEngagement]
- "services_agent_policy_rationale_68": "Running engagement usage, checked against the blast-radius caps." | kind=entity | source=manager/backend/app/services/agent_policy.py:L68 | neighbors=[UsageCounters]
- "services_agent_policy_rationale_89": "Decide whether `action` may proceed under `roe`. Order is deliberate:     hard d" | kind=entity | source=manager/backend/app/services/agent_policy.py:L89 | neighbors=[evaluate_action()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-258.json

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
