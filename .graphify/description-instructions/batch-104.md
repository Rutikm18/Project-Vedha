# Node Description Batch 105 of 227

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

- "scripts_seed_admin_verify_hash": "_verify_hash()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L139 | neighbors=[seed_admin.py, _seed_once()]
- "scripts_startup_validator_validationreport_print_summary": ".print_summary()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L56 | neighbors=[run_all_validators(), ValidationReport]
- "services_agent_policy_rulesofengagement": "RulesOfEngagement" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L55 | neighbors=[agent_policy.py, The deterministic authorization envelop…]
- "services_agent_policy_usagecounters": "UsageCounters" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L67 | neighbors=[agent_policy.py, Running engagement usage, checked again…]
- "services_analytics_compute_exposure": "compute_exposure()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L35 | neighbors=[analytics.py, _sev()]
- "services_analytics_sev": "_sev()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L31 | neighbors=[analytics.py, compute_exposure()]
- "services_audit_record_audit": "record_audit()" | kind=code-symbol | source=manager/backend/app/services/audit.py:L13 | neighbors=[audit.py, Append one immutable audit row (caller …]
- "services_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/services/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "services_job_attempt_service_attemptclaim": "AttemptClaim" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L17 | neighbors=[job_attempt_service.py, claim_job_attempt()]
- "services_job_attempt_service_renew_job_attempt": "renew_job_attempt()" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L86 | neighbors=[job_attempt_service.py, Renew only the currently installed runn…]
- "services_notifications_enqueue_notification": "enqueue_notification()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L101 | neighbors=[notifications.py, Producer API: enqueue a durable notify …]
- "services_portal_metrics_period": "_period()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L50 | neighbors=[portal_metrics.py, status_timeline()]
- "services_posture_findingview": "FindingView" | kind=code-symbol | source=manager/backend/app/services/posture.py:L22 | neighbors=[posture.py, Duck-typed projection of a Finding + it…]
- "services_posture_grade_for": "grade_for()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L55 | neighbors=[posture.py, compute_scores()]
- "services_posture_risk_prob": "_risk_prob()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L62 | neighbors=[posture.py, compute_scores()]
- "services_posture_scores": "Scores" | kind=code-symbol | source=manager/backend/app/services/posture.py:L36 | neighbors=[posture.py, compute_scores()]
- "services_posture_severity": "_severity()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L116 | neighbors=[posture.py, compare()]
- "services_remediation_kb_cves": "_cves()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L54 | neighbors=[remediation_kb.py, classify_finding()]
- "services_remediation_kb_step": "_step()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L94 | neighbors=[remediation_kb.py, One remediation step. `generic` is REQU…]
- "services_remediation_kb_text": "_text()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L45 | neighbors=[remediation_kb.py, classify_finding()]
- "services_scope_crypto_public_key_from_b64": "public_key_from_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L85 | neighbors=[scope_crypto.py, Decode a base64-encoded X25519 public k…]
- "services_scope_targets_parse_networks": "_parse_networks()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L28 | neighbors=[scope_targets.py, validate_targets_in_scope()]
- "status_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L15 | neighbors=[route.ts, readiness()]
- "status_route_readiness": "readiness()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L10 | neighbors=[route.ts, GET()]
- "tests_conftest": "conftest.py" | kind=code-symbol | source=probe/tests/conftest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "tests_init": "__init__.py" | kind=code-symbol | source=manager/backend/tests/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_active_validation_escalation_test_confirmed_authoritative_does_not_escalate": "test_confirmed_authoritative_does_not_escalate()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L21 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_high_severity_suspected_escalates_when_roe_allows": "test_high_severity_suspected_escalates_when_roe_allows()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L13 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_kev_escalates_even_if_medium": "test_kev_escalates_even_if_medium()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L17 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_low_severity_non_kev_does_not_escalate": "test_low_severity_non_kev_does_not_escalate()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L34 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_ot_profile_never_escalates": "test_ot_profile_never_escalates()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L30 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_active_validation_escalation_test_roe_forbids_blocks_escalation": "test_roe_forbids_blocks_escalation()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L26 | neighbors=[test_active_validation_escalation.py, _ev()]
- "tests_test_ad_assessment_fakeentry_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L41 | neighbors=[_FakeEntry, _FakeAttr]
- "tests_test_ad_assessment_testkerberoastchecker_ldap_with_users": "._ldap_with_users()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L173 | neighbors=[TestKerberoastChecker, .test_get_spn_accounts_filters_krbtgt_a…]
- "tests_test_ad_assessment_testkerberoastchecker_test_get_spn_accounts_filters_krbtgt_and_no_spn": ".test_get_spn_accounts_filters_krbtgt_and_no_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L179 | neighbors=[TestKerberoastChecker, ._ldap_with_users()]
- "tests_test_agent_auth_boundary_test_agent_jwt_is_blocked_before_human_route_handler": "test_agent_jwt_is_blocked_before_human_route_handler()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L58 | neighbors=[test_agent_auth_boundary.py, _boundary_test_client()]
- "tests_test_agent_auth_boundary_test_human_jwt_still_reaches_human_route_handler": "test_human_jwt_still_reaches_human_route_handler()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L69 | neighbors=[test_agent_auth_boundary.py, _boundary_test_client()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_claim_commits_before_confirmation": ".test_claim_commits_before_confirmation()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L223 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_incompatible_capability_is_never_claimed": ".test_incompatible_capability_is_never_claimed()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L251 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim_test_lost_atomic_update_is_reported_as_unclaimed": ".test_lost_atomic_update_is_reported_as_unclaimed()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L275 | neighbors=[TestAtomicWebSocketClaim, _claim_fixture()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-104.json

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
