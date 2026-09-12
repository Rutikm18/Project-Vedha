# Node Description Batch 114 of 380

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
- "models_validation_request": "validation_request.py" | kind=code-symbol | source=manager/backend/app/models/validation_request.py:L1 | neighbors=[58c2d10 feat(active-validation): Valida…, ValidationRequest, validation_request.py — an approval-gat…]
- "models_validation_request_validationrequest": "ValidationRequest" | kind=code-symbol | source=manager/backend/app/models/validation_request.py:L28 | neighbors=[validation_request.py, Base, TimestampMixin]
- "models_worker_heartbeat": "worker_heartbeat.py" | kind=code-symbol | source=manager/backend/app/models/worker_heartbeat.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, WorkerHeartbeat, worker_heartbeat.py — one row per backg…]
- "models_worker_heartbeat_workerheartbeat": "WorkerHeartbeat" | kind=code-symbol | source=manager/backend/app/models/worker_heartbeat.py:L21 | neighbors=[worker_heartbeat.py, Base, TimestampMixin]
- "native_port_scan_nativeportscan": "nativePortScan()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L221 | neighbors=[tool-runners.ts, port-scan.ts, resolvePorts()]
- "path_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L53 | neighbors=[route.ts, proxy(), proxyPortal()]
- "path_route_patch": "PATCH()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L57 | neighbors=[route.ts, proxy(), proxyPortal()]
- "path_route_portaltoken": "portalToken()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L12 | neighbors=[route.ts, proxyPortal(), proxy()]
- "path_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L55 | neighbors=[route.ts, proxy(), proxyPortal()]
- "portscan_classify_os_error": "classify_os_error()" | kind=code-symbol | source=portscan.py:L73 | neighbors=[portscan.py, ._attempt(), Map a connect()-time OSError to (state,…]
- "portscan_portscanner_run": ".run()" | kind=code-symbol | source=portscan.py:L195 | neighbors=[main(), PortScanner, .scan_port()]
- "prompts_report_confidence": "Confidence" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L30 | neighbors=[ai-engine.ts, report.ts, page.tsx]
- "prompts_report_reportfinding": "ReportFinding" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L76 | neighbors=[ai-engine.ts, report.ts, page.tsx]
- "prompts_report_scoredomain": "ScoreDomain" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L56 | neighbors=[ai-engine.ts, report.ts, page.tsx]
- "prompts_triage": "triage.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/triage.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ai-engine.ts, 298a9d4 trim frontend to 7 core pages; …]
- "protocol": "Protocol" | kind=code-symbol | neighbors=[AIClient, _Scanner, _Scanner]
- "report_adapt_derivedetectionmethod": "deriveDetectionMethod()" | kind=code-symbol | source=manager/frontend/lib/report/adapt.ts:L30 | neighbors=[adapt.ts, toRawFinding(), report-adapt.test.ts]
- "report_adapt_deriveinternetreachable": "deriveInternetReachable()" | kind=code-symbol | source=manager/frontend/lib/report/adapt.ts:L12 | neighbors=[adapt.ts, toRawFinding(), toReportAssets()]
- "report_finding_model_assessedfinding": "AssessedFinding" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L676 | neighbors=[finding-model.ts, FindingReport.tsx, FindingReport.tsx]
- "report_finding_model_attackerstatement": "attackerStatement()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L338 | neighbors=[finding-model.ts, assess(), joinList()]
- "report_finding_model_provenanceof": "provenanceOf()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L505 | neighbors=[finding-model.ts, FindingReport.tsx, FindingReport.tsx]
- "report_finding_model_rawevidence": "RawEvidence" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L34 | neighbors=[finding-model.ts, FindingReport.tsx, FindingReport.tsx]
- "report_finding_model_remediationsteps": "remediationSteps()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L622 | neighbors=[finding-model.ts, assess(), readinessOf()]
- "report_finding_model_remediationtier": "RemediationTier" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L58 | neighbors=[finding-model.ts, FindingReport.tsx, FindingReport.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-113.json

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
