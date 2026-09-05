# Node Description Batch 141 of 336

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

- "routers_portal_portal_assistant_chat": "portal_assistant_chat()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L435 | neighbors=[portal.py, _assistant_finding_view()]
- "routers_portal_portal_engagement": "portal_engagement()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L88 | neighbors=[portal.py, _enum_val()]
- "routers_portal_portal_scans": "portal_scans()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L275 | neighbors=[portal.py, _enum_val()]
- "routers_portal_portal_trends": "portal_trends()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L235 | neighbors=[portal.py, _metric_finding()]
- "routers_probe_enrollment_create_enroll_token": "create_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L770 | neighbors=[probe_enrollment.py, generate_enroll_token()]
- "routers_probe_enrollment_derive_refresh_secret": "_derive_refresh_secret()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L49 | neighbors=[probe_enrollment.py, activate_enrollment()]
- "routers_probe_enrollment_enrollmentactivate": "EnrollmentActivate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L144 | neighbors=[probe_enrollment.py, EnrollmentSecret]
- "routers_probe_enrollment_enrollmentcreate_validate_key": ".validate_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L128 | neighbors=[EnrollmentCreate, _decode_public_key()]
- "routers_probe_enrollment_enrolltokencreate": "EnrollTokenCreate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L133 | neighbors=[probe_enrollment.py, BaseModel]
- "routers_probe_enrollment_list_enroll_tokens": "list_enroll_tokens()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L818 | neighbors=[probe_enrollment.py, enroll_token_is_usable()]
- "routers_probe_enrollment_policy": "_policy()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L194 | neighbors=[probe_enrollment.py, activate_enrollment()]
- "routers_probe_enrollment_tokenrefresh": "TokenRefresh" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L186 | neighbors=[probe_enrollment.py, BaseModel]
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
- "scanner_accuracy_expected_keys": "_expected_keys()" | kind=code-symbol | source=probe/scanner/accuracy.py:L37 | neighbors=[accuracy.py, score_findings()]
- "scanner_accuracy_finding_key": "_finding_key()" | kind=code-symbol | source=probe/scanner/accuracy.py:L31 | neighbors=[accuracy.py, score_findings()]
- "scanner_accuracy_format_report": "format_report()" | kind=code-symbol | source=probe/scanner/accuracy.py:L145 | neighbors=[accuracy.py, _main()]
- "scanner_accuracy_gate_format_gate_report": "format_gate_report()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L175 | neighbors=[accuracy_gate.py, _main()]
- "scanner_adaptive_timeout_adaptivetimeout_timeout": ".timeout()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L44 | neighbors=[AdaptiveTimeout, Current timeout: base until we have a s…]
- "scanner_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L247 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L281 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_probe_redis": "_probe_redis()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L114 | neighbors=[db_scanner.py, interpret_redis_info()]
- "scanner_delta_scanner_delta_to_dict": ".to_dict()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L87 | neighbors=[Delta, main()]
- "scanner_delta_scanner_deltaengine_summary": ".summary()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L290 | neighbors=[DeltaEngine, main()]
- "scanner_dns_scanner_dnsscanner_chaos_txt": "._chaos_txt()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L98 | neighbors=[DNSScanner, ._probe()]
- "scanner_dns_scanner_dnsscanner_dnssec_present": "._dnssec_present()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L161 | neighbors=[DNSScanner, ._probe()]
- "scanner_dns_scanner_dnsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L215 | neighbors=[DNSScanner, .scan_target()]
- "scanner_dns_scanner_dnsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L237 | neighbors=[DNSScanner, ._scan_port()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-140.json

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
