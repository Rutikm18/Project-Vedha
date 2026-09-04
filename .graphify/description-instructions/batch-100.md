# Node Description Batch 101 of 330

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

- "main_scripts_va_campaign_cliprogressview_redraw": "._redraw()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L669 | neighbors=[CliProgressView, .__call__(), ._format()]
- "main_scripts_va_campaign_monotonic": "_monotonic()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L276 | neighbors=[va_campaign.py, ._eta_seconds(), .__init__()]
- "main_scripts_va_campaign_progressreporter_eta_seconds": "._eta_seconds()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L236 | neighbors=[ProgressReporter, _monotonic(), .snapshot()]
- "main_scripts_va_campaign_progressreporter_finish": ".finish()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L217 | neighbors=[ProgressReporter, ._flush(), .run()]
- "main_scripts_va_campaign_progressreporter_set_totals": ".set_totals()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L213 | neighbors=[ProgressReporter, ._flush(), ._refresh_totals()]
- "main_scripts_va_campaign_run_campaign": "run_campaign()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L639 | neighbors=[va_campaign.py, build_campaign(), .run()]
- "main_scripts_va_campaign_stagestate": "StageState" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L151 | neighbors=[va_campaign.py, .__init__(), .to_dict()]
- "main_scripts_va_campaign_vacampaign_refresh_totals": "._refresh_totals()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L322 | neighbors=[VACampaign, .set_totals(), .run()]
- "main_scripts_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "main_scripts_vnc_scanner_classify_security_types": "classify_security_types()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L60 | neighbors=[vnc_scanner.py, Turn a list of offered security-type id…, ._probe()]
- "main_scripts_vnc_scanner_parse_rfb_version": "parse_rfb_version()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L46 | neighbors=[vnc_scanner.py, Parse a 'RFB 003.008' banner into (majo…, ._probe()]
- "main_scripts_vnc_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L71 | neighbors=[vnc_scanner.py, _read_security_types(), ._probe()]
- "main_scripts_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L155 | neighbors=[WebScanner, ._schemes_for(), .scan_target()]
- "main_scripts_web_scanner_webscanner_schemes_for": "._schemes_for()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L148 | neighbors=[Preferred scheme first, the other as a …, WebScanner, ._scan_port()]
- "models_agent_recommendation_rationale_1": "agent_recommendation.py — decisions/actions proposed by the agentic AI advisor." | kind=entity | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[agent_recommendation.py, Base, TimestampMixin]
- "models_attack_path": "attack_path.py" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackPath, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline": "attack_timeline.py" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackTimeline, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline_rationale_12": "Append-only ledger of every attack action performed during an engagement.      W" | kind=entity | source=manager/backend/app/models/attack_timeline.py:L12 | neighbors=[AttackTimeline, Base, TimestampMixin]
- "models_audit_log": "audit_log.py" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AuditLog, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/models/detection.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config": "detection_config.py" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionConfig, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config_rationale_11": "Per-engagement SIEM + EDR connection settings used by the detection     validati" | kind=entity | source=manager/backend/app/models/detection_config.py:L11 | neighbors=[DetectionConfig, Base, TimestampMixin]
- "models_detection_run_rationale_1": "detection_run.py — one execution of the deterministic detection engine over a fa" | kind=entity | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[detection_run.py, Base, TimestampMixin]
- "models_enums_findingeventtype": "FindingEventType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L70 | neighbors=[enums.py, str, A single entry in a finding's lifecycle…]
- "models_exploit_approval_rationale_20": "Created when a high-risk target requires manager sign-off.     Auto-queues the e" | kind=entity | source=manager/backend/app/models/exploit_approval.py:L20 | neighbors=[ExploitApprovalRequest, Base, TimestampMixin]
- "models_exploit_result_rationale_12": "Immutable record of every exploit attempt.     Never updated after creation — ap" | kind=entity | source=manager/backend/app/models/exploit_result.py:L12 | neighbors=[ExploitResult, Base, TimestampMixin]
- "models_finding_event_findingevent": "FindingEvent" | kind=code-symbol | source=manager/backend/app/models/finding_event.py:L11 | neighbors=[finding_event.py, Base, Append-only lifecycle audit trail for a…]
- "models_integration": "integration.py" | kind=code-symbol | source=manager/backend/app/models/integration.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, Integration, integration.py — a tenant's notificatio…]
- "models_integration_integration": "Integration" | kind=code-symbol | source=manager/backend/app/models/integration.py:L21 | neighbors=[integration.py, Base, TimestampMixin]
- "models_llm_output": "llm_output.py" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, LLMOutput, 298a9d4 trim frontend to 7 core pages; …]
- "models_outbox_rationale_1": "outbox.py — transactional outbox for durable, exactly-once background work.  THE" | kind=entity | source=manager/backend/app/models/outbox.py:L1 | neighbors=[outbox.py, Base, TimestampMixin]
- "models_probe_enrollment_agentcredential": "AgentCredential" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L51 | neighbors=[probe_enrollment.py, Base, TimestampMixin]
- "models_probe_enrollment_probeenrollmentrequest": "ProbeEnrollmentRequest" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L11 | neighbors=[probe_enrollment.py, Base, TimestampMixin]
- "models_probe_site_probesite": "ProbeSite" | kind=code-symbol | source=manager/backend/app/models/probe_site.py:L10 | neighbors=[probe_site.py, Base, TimestampMixin]
- "models_remediation_plan": "remediation_plan.py" | kind=code-symbol | source=manager/backend/app/models/remediation_plan.py:L1 | neighbors=[fd5dc96 feat(remediation): AI + determi…, RemediationPlan, remediation_plan.py — a generated, OS-s…]
- "models_remediation_plan_remediationplan": "RemediationPlan" | kind=code-symbol | source=manager/backend/app/models/remediation_plan.py:L24 | neighbors=[remediation_plan.py, Base, TimestampMixin]
- "models_scan_request_scanrequest": "ScanRequest" | kind=code-symbol | source=manager/backend/app/models/scan_request.py:L26 | neighbors=[scan_request.py, Base, TimestampMixin]
- "models_scan_result_rationale_11": "Append-only raw probe facts (P3-#10).      Decoupled from scan_jobs so:       (a" | kind=entity | source=manager/backend/app/models/scan_result.py:L11 | neighbors=[ScanResult, Base, TimestampMixin]
- "models_sla_policy": "sla_policy.py" | kind=code-symbol | source=manager/backend/app/models/sla_policy.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, SlaPolicy, sla_policy.py — a tenant's custom SLA r…]
- "models_sla_policy_slapolicy": "SlaPolicy" | kind=code-symbol | source=manager/backend/app/models/sla_policy.py:L20 | neighbors=[sla_policy.py, Base, TimestampMixin]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-100.json

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
