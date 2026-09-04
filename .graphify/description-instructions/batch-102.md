# Node Description Batch 103 of 330

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

- "routers_exploits_get_exploit_result": "get_exploit_result()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L205 | neighbors=[exploits.py, _get_result_or_404(), _result_out()]
- "routers_exploits_run_approved_exploit": "_run_approved_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L445 | neighbors=[exploits.py, Background task: run the exploit after …, Background task: run the exploit after …]
- "routers_findings_finding_detail_out": "_finding_detail_out()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L49 | neighbors=[findings.py, get_finding(), Build the detail contract with bounded …]
- "routers_findings_finding_timeline": "finding_timeline()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L264 | neighbors=[findings.py, _tenant_finding(), The finding's full lifecycle, oldest-fi…]
- "routers_findings_get_finding": "get_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L253 | neighbors=[findings.py, _finding_detail_out(), _tenant_finding()]
- "routers_health_health_startup": "health_startup()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L162 | neighbors=[health.py, Returns the cached report from the last…, Returns the cached report from the last…]
- "routers_integrations_integrationout": "IntegrationOut" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L36 | neighbors=[integrations.py, BaseModel, _out()]
- "routers_integrations_put_integration": "put_integration()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L65 | neighbors=[integrations.py, _out(), _row()]
- "routers_integrations_row": "_row()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L48 | neighbors=[integrations.py, delete_integration(), put_integration()]
- "routers_portal_assistant_finding_view": "_assistant_finding_view()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L416 | neighbors=[portal.py, portal_assistant_chat(), The whitelist that reaches the model — …]
- "routers_portal_portal_posture": "portal_posture()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L170 | neighbors=[portal.py, _posture_view(), _enum_val()]
- "routers_portal_portal_summary": "portal_summary()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L202 | neighbors=[portal.py, _metric_finding(), _posture_view()]
- "routers_probe_enrollment_approve_enrollment": "approve_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L615 | neighbors=[probe_enrollment.py, _keyed_hash(), _provision_agent_for_site()]
- "routers_probe_enrollment_enrollmentcreate": "EnrollmentCreate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L113 | neighbors=[probe_enrollment.py, BaseModel, .validate_key()]
- "routers_probe_enrollment_enrollmentsecret": "EnrollmentSecret" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L140 | neighbors=[probe_enrollment.py, EnrollmentActivate, BaseModel]
- "routers_probe_enrollment_keyed_hash": "_keyed_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L41 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request()]
- "routers_probe_enrollment_next_probe_name": "_next_probe_name()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L546 | neighbors=[probe_enrollment.py, approve_request_simple(), Auto-assign the next sequential vedha-a…]
- "routers_probe_enrollment_poll_enrollment": "poll_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L491 | neighbors=[probe_enrollment.py, _authenticated_request(), _rate_limit()]
- "routers_remediation_cached_plan": "_cached_plan()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L54 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_remediation_serialize": "_serialize()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L105 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_sla_policy_get_sla_policy": "get_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L81 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_put_sla_policy": "put_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L86 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_slapolicyout": "SlaPolicyOut" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L30 | neighbors=[sla_policy.py, _out(), BaseModel]
- "routers_users_userout": "UserOut" | kind=code-symbol | source=manager/backend/app/routers/users.py:L30 | neighbors=[users.py, _out(), BaseModel]
- "routers_validation_approve_validation": "approve_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L214 | neighbors=[validation.py, _get_request_or_404(), _roe_allows_active_validation()]
- "routers_validation_default_check_kind": "_default_check_kind()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L88 | neighbors=[validation.py, create_validation_request(), Pick a safe check for the finding. TLS …]
- "routers_validation_get_request_or_404": "_get_request_or_404()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L115 | neighbors=[validation.py, approve_validation(), reject_validation()]
- "routers_validation_validationrequestout": "ValidationRequestOut" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L63 | neighbors=[validation.py, _request_out(), BaseModel]
- "routers_vuln_scans_finish_cancelled_nuclei_job": "_finish_cancelled_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L516 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "routers_vuln_scans_set_nuclei_job_state": "_set_nuclei_job_state()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L493 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "scanner_accuracy_gate_check_thresholds": "check_thresholds()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L105 | neighbors=[accuracy_gate.py, Threshold violations for one scored cor…, run_gate()]
- "scanner_accuracy_gate_is_independent": "is_independent()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L100 | neighbors=[accuracy_gate.py, True when this corpus's labels can supp…, run_gate()]
- "scanner_accuracy_gate_main": "_main()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L204 | neighbors=[accuracy_gate.py, format_gate_report(), run_gate()]
- "scanner_accuracy_main": "_main()" | kind=code-symbol | source=probe/scanner/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "scanner_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=probe/scanner/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "scanner_accuracy_ratio": "_ratio()" | kind=code-symbol | source=probe/scanner/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "scanner_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, AdaptiveTimeout, from_rtts()]
- "scanner_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "scanner_cpe_extract_version": "_extract_version()" | kind=code-symbol | source=probe/scanner/cpe.py:L103 | neighbors=[cpe.py, Prefer an explicit version field; else …, to_cpe()]
- "scanner_cpe_to_cpe": "to_cpe()" | kind=code-symbol | source=probe/scanner/cpe.py:L116 | neighbors=[cpe.py, Return {vendor, product, version, cpe23…, _extract_version()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-102.json

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
