# Node Description Batch 94 of 131

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

- "lib_detection_store_isinwindow": "isInWindow()" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L88 | neighbors=[detection-store.ts]
- "lib_detection_store_issamehost": "isSameHost()" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L92 | neighbors=[detection-store.ts]
- "lib_detection_store_siem_alerts": "SIEM_ALERTS" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L48 | neighbors=[detection-store.ts]
- "lib_detection_store_siemalert": "SIEMAlert" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L35 | neighbors=[detection-store.ts]
- "lib_detection_store_siemconfigs": "siemConfigs" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L410 | neighbors=[detection-store.ts]
- "lib_detection_store_sigma_templates": "SIGMA_TEMPLATES" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L153 | neighbors=[detection-store.ts]
- "lib_detection_store_sigmarule": "SigmaRule" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L145 | neighbors=[detection-store.ts]
- "lib_engagements_store_activity": "ACTIVITY" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L98 | neighbors=[engagements-store.ts]
- "lib_engagements_store_credential": "Credential" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L3 | neighbors=[engagements-store.ts]
- "lib_engagements_store_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L10 | neighbors=[engagements-store.ts]
- "lib_engagements_store_engagementsstore": "engagementsStore" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L122 | neighbors=[engagements-store.ts]
- "lib_engagements_store_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[engagements-store.ts]
- "lib_engagements_store_findings_timeline": "FINDINGS_TIMELINE" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L109 | neighbors=[engagements-store.ts]
- "lib_engagements_store_genid": "genId()" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L32 | neighbors=[engagements-store.ts]
- "lib_engagements_store_now": "now" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L108 | neighbors=[engagements-store.ts]
- "lib_engagements_store_store": "STORE" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L34 | neighbors=[engagements-store.ts]
- "lib_errors_adversaerror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L65 | neighbors=[AdversaError]
- "lib_errors_adversaerror_render": ".render()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L94 | neighbors=[AdversaError]
- "lib_errors_adversaerror_tojson": ".toJSON()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L76 | neighbors=[AdversaError]
- "lib_errors_adversaerroropts": "AdversaErrorOpts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L48 | neighbors=[errors.ts]
- "lib_errors_errorcode": "ErrorCode" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L14 | neighbors=[errors.ts]
- "lib_errors_vedhaerror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L65 | neighbors=[VedhaError]
- "lib_errors_vedhaerror_render": ".render()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L94 | neighbors=[VedhaError]
- "lib_errors_vedhaerror_tojson": ".toJSON()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L76 | neighbors=[VedhaError]
- "lib_errors_vedhaerroropts": "VedhaErrorOpts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L48 | neighbors=[errors.ts]
- "lib_exploit_store_approvals": "approvals" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L78 | neighbors=[exploit-store.ts]
- "lib_exploit_store_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L3 | neighbors=[exploit-store.ts]
- "lib_exploit_store_auditentry": "AuditEntry" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L54 | neighbors=[exploit-store.ts]
- "lib_exploit_store_auditlog": "auditLog" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L79 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L36 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitevidence": "ExploitEvidence" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L5 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitjob": "ExploitJob" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L20 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L13 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitstore": "exploitStore" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L81 | neighbors=[exploit-store.ts]
- "lib_exploit_store_genid": "genId()" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L68 | neighbors=[exploit-store.ts]
- "lib_exploit_store_jobs": "jobs" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L77 | neighbors=[exploit-store.ts]
- "lib_exploit_store_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L2 | neighbors=[exploit-store.ts]
- "lib_exploit_store_nowiso": "nowIso()" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L72 | neighbors=[exploit-store.ts]
- "lib_exploit_store_payloadtype": "PayloadType" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[exploit-store.ts]
- "lib_fetcher_apierror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L10 | neighbors=[ApiError]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-093.json

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
