# Node Description Batch 76 of 236

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

- "main_scripts_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync()]
- "main_scripts_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "main_scripts_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync()]
- "main_scripts_udp_scanner_ipmi_probe": "_ipmi_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L139 | neighbors=[udp_scanner.py, RMCP Ping (ASF Presence Ping) to detect…, RMCP Ping (ASF Presence Ping) to detect…]
- "main_scripts_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L158 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…, mDNS PTR query for _services._dns-sd._u…]
- "main_scripts_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "main_scripts_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L146 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…, UPnP/SSDP M-SEARCH — unicast to target:…]
- "main_scripts_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "main_scripts_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "models_agent_recommendation_rationale_1": "agent_recommendation.py — decisions/actions proposed by the agentic AI advisor." | kind=entity | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[agent_recommendation.py, Base, TimestampMixin]
- "models_attack_path": "attack_path.py" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackPath, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline": "attack_timeline.py" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackTimeline, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline_rationale_12": "Append-only ledger of every attack action performed during an engagement.      W" | kind=entity | source=manager/backend/app/models/attack_timeline.py:L12 | neighbors=[AttackTimeline, Base, TimestampMixin]
- "models_audit_log": "audit_log.py" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AuditLog, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/models/detection.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config": "detection_config.py" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionConfig, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config_rationale_11": "Per-engagement SIEM + EDR connection settings used by the detection     validati" | kind=entity | source=manager/backend/app/models/detection_config.py:L11 | neighbors=[DetectionConfig, Base, TimestampMixin]
- "models_detection_run_rationale_1": "detection_run.py — one execution of the deterministic detection engine over a fa" | kind=entity | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[detection_run.py, Base, TimestampMixin]
- "models_exploit_approval_rationale_20": "Created when a high-risk target requires manager sign-off.     Auto-queues the e" | kind=entity | source=manager/backend/app/models/exploit_approval.py:L20 | neighbors=[ExploitApprovalRequest, Base, TimestampMixin]
- "models_exploit_result_rationale_12": "Immutable record of every exploit attempt.     Never updated after creation — ap" | kind=entity | source=manager/backend/app/models/exploit_result.py:L12 | neighbors=[ExploitResult, Base, TimestampMixin]
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
- "native_port_scan_nativeportscan": "nativePortScan()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L221 | neighbors=[tool-runners.ts, port-scan.ts, resolvePorts()]
- "portscan_classify_os_error": "classify_os_error()" | kind=code-symbol | source=portscan.py:L73 | neighbors=[portscan.py, ._attempt(), Map a connect()-time OSError to (state,…]
- "portscan_portscanner_run": ".run()" | kind=code-symbol | source=portscan.py:L195 | neighbors=[main(), PortScanner, .scan_port()]
- "prompts_report": "report.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ai-engine.ts, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-075.json

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
