# Node Description Batch 144 of 330

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

- "schemas_ai_aigenerateresponse": "AiGenerateResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L59 | neighbors=[ai.py, BaseModel]
- "schemas_ai_aimessage": "AiMessage" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L13 | neighbors=[ai.py, BaseModel]
- "schemas_auth_loginrequest": "LoginRequest" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L9 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreate": "PersonalAccessTokenCreate" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L35 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreated": "PersonalAccessTokenCreated" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L41 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokenout": "PersonalAccessTokenOut" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L52 | neighbors=[auth.py, BaseModel]
- "schemas_auth_tokenresponse": "TokenResponse" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L14 | neighbors=[auth.py, BaseModel]
- "schemas_common_errordetail": "ErrorDetail" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L18 | neighbors=[common.py, BaseModel]
- "schemas_common_paginate": "paginate()" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L22 | neighbors=[common.py, PaginatedResponse]
- "schemas_engagement_engagementcreate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L66 | neighbors=[EngagementCreate, validate_engagement_dates()]
- "schemas_engagement_engagementcreate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L62 | neighbors=[EngagementCreate, validate_scope_entries()]
- "schemas_engagement_rationale_13": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L13 | neighbors=[validate_scope_entries(), EngagementStatus]
- "schemas_engagement_validate_engagement_dates": "validate_engagement_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L30 | neighbors=[engagement.py, .validate_dates()]
- "schemas_finding_findingassetcontext": "FindingAssetContext" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L55 | neighbors=[finding.py, BaseModel]
- "schemas_finding_findingtimeline": "FindingTimeline" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L83 | neighbors=[finding.py, BaseModel]
- "schemas_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/schemas/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_portal_clientassistantreply": "ClientAssistantReply" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L150 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clientengagementout": "ClientEngagementOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L40 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clientpostureout": "ClientPostureOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L51 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clientreportcontent": "ClientReportContent" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L88 | neighbors=[portal.py, ClientReportOut]
- "schemas_portal_clientscanout": "ClientScanOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L92 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clientscanrequestout": "ClientScanRequestOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L117 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clienttrendpoint": "ClientTrendPoint" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L69 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clienttrendsout": "ClientTrendsOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L75 | neighbors=[portal.py, BaseModel]
- "schemas_remediation_remediationplanout": "RemediationPlanOut" | kind=code-symbol | source=manager/backend/app/schemas/remediation.py:L48 | neighbors=[remediation.py, BaseModel]
- "scripts_seed_admin_hash": "_hash()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L135 | neighbors=[seed_admin.py, _seed_once()]
- "scripts_seed_admin_verify_hash": "_verify_hash()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L139 | neighbors=[seed_admin.py, _seed_once()]
- "scripts_startup_validator_validationreport_print_summary": ".print_summary()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L56 | neighbors=[run_all_validators(), ValidationReport]
- "services_agent_policy_rulesofengagement": "RulesOfEngagement" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L55 | neighbors=[agent_policy.py, The deterministic authorization envelop…]
- "services_agent_policy_usagecounters": "UsageCounters" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L67 | neighbors=[agent_policy.py, Running engagement usage, checked again…]
- "services_analytics_compute_exposure": "compute_exposure()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L35 | neighbors=[analytics.py, _sev()]
- "services_analytics_sev": "_sev()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L31 | neighbors=[analytics.py, compute_exposure()]
- "services_audit_record_audit": "record_audit()" | kind=code-symbol | source=manager/backend/app/services/audit.py:L13 | neighbors=[audit.py, Append one immutable audit row (caller …]
- "services_finding_events_decorate": "_decorate()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L201 | neighbors=[finding_events.py, merge_timeline()]
- "services_finding_events_detected_detail": "_detected_detail()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L96 | neighbors=[finding_events.py, synthesize_events()]
- "services_finding_events_ev": "_ev()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L61 | neighbors=[finding_events.py, synthesize_events()]
- "services_finding_events_row_to_dict": "_row_to_dict()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L187 | neighbors=[finding_events.py, build_timeline()]
- "services_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/services/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "services_job_attempt_service_attemptclaim": "AttemptClaim" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L17 | neighbors=[job_attempt_service.py, claim_job_attempt()]
- "services_job_attempt_service_renew_job_attempt": "renew_job_attempt()" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L86 | neighbors=[job_attempt_service.py, Renew only the currently installed runn…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-143.json

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
