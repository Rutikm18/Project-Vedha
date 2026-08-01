# Node Description Batch 60 of 119

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

- "schemas_auth_personalaccesstokenout": "PersonalAccessTokenOut" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L49 | neighbors=[auth.py, BaseModel]
- "schemas_auth_tokenresponse": "TokenResponse" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L14 | neighbors=[auth.py, BaseModel]
- "schemas_common_errordetail": "ErrorDetail" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L18 | neighbors=[common.py, BaseModel]
- "schemas_common_paginate": "paginate()" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L22 | neighbors=[common.py, PaginatedResponse]
- "schemas_engagement_engagementcreate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L66 | neighbors=[EngagementCreate, validate_engagement_dates()]
- "schemas_engagement_engagementcreate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L62 | neighbors=[EngagementCreate, validate_scope_entries()]
- "schemas_engagement_rationale_13": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L13 | neighbors=[EngagementStatus, validate_scope_entries()]
- "schemas_engagement_validate_engagement_dates": "validate_engagement_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L30 | neighbors=[engagement.py, .validate_dates()]
- "schemas_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/schemas/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "services_analytics_compute_exposure": "compute_exposure()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L35 | neighbors=[analytics.py, _sev()]
- "services_analytics_sev": "_sev()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L31 | neighbors=[analytics.py, compute_exposure()]
- "services_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/services/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "services_scope_crypto_public_key_from_b64": "public_key_from_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L85 | neighbors=[scope_crypto.py, Decode a base64-encoded X25519 public k…]
- "services_sla_windows": "_windows()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L34 | neighbors=[sla.py, compute()]
- "status_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L15 | neighbors=[route.ts, readiness()]
- "status_route_readiness": "readiness()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L10 | neighbors=[route.ts, GET()]
- "tests_conftest": "conftest.py" | kind=code-symbol | source=probe/tests/conftest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "tests_init": "__init__.py" | kind=code-symbol | source=manager/backend/tests/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_ad_assessment_fakeentry_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L41 | neighbors=[_FakeEntry, _FakeAttr]
- "tests_test_ad_assessment_testkerberoastchecker_ldap_with_users": "._ldap_with_users()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L173 | neighbors=[TestKerberoastChecker, .test_get_spn_accounts_filters_krbtgt_a…]
- "tests_test_ad_assessment_testkerberoastchecker_test_get_spn_accounts_filters_krbtgt_and_no_spn": ".test_get_spn_accounts_filters_krbtgt_and_no_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L179 | neighbors=[TestKerberoastChecker, ._ldap_with_users()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_claim_commits_before_confirmation": ".test_claim_commits_before_confirmation()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L205 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_incompatible_capability_is_never_claimed": ".test_incompatible_capability_is_never_claimed()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L230 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_lost_atomic_update_is_reported_as_unclaimed": ".test_lost_atomic_update_is_reported_as_unclaimed()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L253 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_identity_test_cached_identity_refreshes_current_capabilities": "test_cached_identity_refreshes_current_capabilities()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L42 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_identity_test_cached_identity_retries_transient_refresh_failure": "test_cached_identity_retries_transient_refresh_failure()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L69 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_identity_test_rejected_cached_token_falls_back_to_idempotent_registration": "test_rejected_cached_token_falls_back_to_idempotent_registration()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L92 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agents_rationale_1": "Unit tests for the agent/probe protocol changes:   * agent polling is restricted" | kind=entity | source=manager/backend/tests/test_agents.py:L1 | neighbors=[ScanJobType, test_agents.py]
- "tests_test_agents_rationale_207": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L207 | neighbors=[ScanJobType, .test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_242": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L242 | neighbors=[ScanJobType, .test_agent_token_is_long_lived()]
- "tests_test_agents_rationale_260": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L260 | neighbors=[ScanJobType, TestPromoteAssets]
- "tests_test_agents_rationale_288": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L288 | neighbors=[ScanJobType, .test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_rationale_530": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L530 | neighbors=[ScanJobType, .test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_565": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L565 | neighbors=[ScanJobType, .test_agent_token_is_long_lived()]
- "tests_test_agents_rationale_583": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L583 | neighbors=[ScanJobType, TestPromoteAssets]
- "tests_test_agents_rationale_611": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L611 | neighbors=[ScanJobType, .test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_testenqueueagentjob_test_404_when_engagement_missing": ".test_404_when_engagement_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L53 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_materializes_direct_job_capability_for_probe": ".test_materializes_direct_job_capability_for_probe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L87 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_rejects_server_side_type": ".test_rejects_server_side_type()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L46 | neighbors=[TestEnqueueAgentJob, _user()]
- "tests_test_agents_testenqueueagentjob_test_scope_fields_cannot_override_engagement_scope": ".test_scope_fields_cannot_override_engagement_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L115 | neighbors=[TestEnqueueAgentJob, _user()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-059.json

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
