# Node Description Batch 158 of 380

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

- "routers_portal_assert_portal_job": "_assert_portal_job()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L810 | neighbors=[portal.py, portal_workspace_scan_cancel()]
- "routers_portal_create_scan_request": "create_scan_request()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L407 | neighbors=[portal.py, _portal_use_cases()]
- "routers_portal_portal_assistant_chat": "portal_assistant_chat()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L521 | neighbors=[portal.py, _assistant_finding_view()]
- "routers_portal_portal_engagement": "portal_engagement()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L110 | neighbors=[portal.py, _enum_val()]
- "routers_portal_portal_scans": "portal_scans()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L361 | neighbors=[portal.py, _enum_val()]
- "routers_portal_portal_trends": "portal_trends()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L321 | neighbors=[portal.py, _metric_finding()]
- "routers_portal_portal_workspace_ai_status": "portal_workspace_ai_status()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L591 | neighbors=[portal.py, Expose the same non-secret runtime cata…]
- "routers_portal_portal_workspace_engagement": "portal_workspace_engagement()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L673 | neighbors=[portal.py, Return the canonical engagement-detail …]
- "routers_portal_portal_workspace_fleet_approve": "portal_workspace_fleet_approve()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L889 | neighbors=[portal.py, Complete device-code enrollment without…]
- "routers_portal_portal_workspace_scan_cancel": "portal_workspace_scan_cancel()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L821 | neighbors=[portal.py, _assert_portal_job()]
- "routers_portal_portal_workspace_update_engagement": "portal_workspace_update_engagement()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L689 | neighbors=[portal.py, Use the manager's canonical update work…]
- "routers_probe_enrollment_create_enroll_token": "create_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L770 | neighbors=[probe_enrollment.py, generate_enroll_token()]
- "routers_probe_enrollment_derive_refresh_secret": "_derive_refresh_secret()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L49 | neighbors=[probe_enrollment.py, activate_enrollment()]
- "routers_probe_enrollment_enrollmentactivate": "EnrollmentActivate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L144 | neighbors=[probe_enrollment.py, EnrollmentSecret]
- "routers_probe_enrollment_enrollmentcreate_validate_key": ".validate_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L128 | neighbors=[EnrollmentCreate, _decode_public_key()]
- "routers_probe_enrollment_enrolltokencreate": "EnrollTokenCreate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L133 | neighbors=[probe_enrollment.py, BaseModel]
- "routers_probe_enrollment_list_enroll_tokens": "list_enroll_tokens()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L818 | neighbors=[probe_enrollment.py, enroll_token_is_usable()]
- "routers_probe_enrollment_policy": "_policy()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L194 | neighbors=[probe_enrollment.py, activate_enrollment()]
- "routers_probe_enrollment_tokenrefresh": "TokenRefresh" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L186 | neighbors=[probe_enrollment.py, BaseModel]
- "routers_scan_schedules_delete_schedule": "delete_schedule()" | kind=code-symbol | source=manager/backend/app/routers/scan_schedules.py:L162 | neighbors=[scan_schedules.py, _schedule_or_404()]
- "routers_scan_schedules_engagement_or_404": "_engagement_or_404()" | kind=code-symbol | source=manager/backend/app/routers/scan_schedules.py:L70 | neighbors=[scan_schedules.py, create_schedule()]
- "routers_scan_schedules_list_schedules": "list_schedules()" | kind=code-symbol | source=manager/backend/app/routers/scan_schedules.py:L127 | neighbors=[scan_schedules.py, _out()]
- "routers_scan_schedules_schedulein": "ScheduleIn" | kind=code-symbol | source=manager/backend/app/routers/scan_schedules.py:L40 | neighbors=[scan_schedules.py, BaseModel]
- "routers_scan_schedules_scheduleupdate": "ScheduleUpdate" | kind=code-symbol | source=manager/backend/app/routers/scan_schedules.py:L51 | neighbors=[scan_schedules.py, BaseModel]
- "routers_sla_policy_slapolicyin": "SlaPolicyIn" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L39 | neighbors=[sla_policy.py, BaseModel]
- "routers_sla_policy_windows_of": "_windows_of()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L53 | neighbors=[sla_policy.py, resolve_windows()]
- "routers_sla_policy_windows_of_named": "_windows_of_named()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L74 | neighbors=[sla_policy.py, _out()]
- "routers_users_get_user": "get_user()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L73 | neighbors=[users.py, _out()]
- "routers_users_list_users": "list_users()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L55 | neighbors=[users.py, _out()]
- "routers_validation_list_validation_requests": "list_validation_requests()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L186 | neighbors=[validation.py, _request_out()]
- "routers_validation_load_finding_and_eng": "_load_finding_and_eng()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L99 | neighbors=[validation.py, create_validation_request()]
- "routers_validation_reject_validation": "reject_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L271 | neighbors=[validation.py, _get_request_or_404()]
- "routers_validation_rejectbody": "RejectBody" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L59 | neighbors=[validation.py, BaseModel]
- "routers_validation_validaterequest": "ValidateRequest" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L53 | neighbors=[validation.py, BaseModel]
- "routers_vuln_scans_nuclei_finding": "_nuclei_finding()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L407 | neighbors=[vuln_scans.py, _run_nuclei_and_save()]
- "routers_vuln_scans_nuclei_terminal_result": "_nuclei_terminal_result()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L430 | neighbors=[vuln_scans.py, _run_nuclei_and_save()]
- "scan_page_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L154 | neighbors=[page.tsx, getToken()]
- "scan_page_gettoken": "getToken()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L110 | neighbors=[page.tsx, apiFetch()]
- "scan_page_scannerworkspace": "ScannerWorkspace()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L672 | neighbors=[page.tsx, page.tsx]
- "scanner_accuracy_expected_keys": "_expected_keys()" | kind=code-symbol | source=probe/scanner/accuracy.py:L37 | neighbors=[accuracy.py, score_findings()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-157.json

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
