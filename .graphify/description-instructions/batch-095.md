# Node Description Batch 96 of 134

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

- "lib_cases_store_caseseverity": "CaseSeverity" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L4 | neighbors=[cases-store.ts]
- "lib_cases_store_casestatus": "CaseStatus" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L5 | neighbors=[cases-store.ts]
- "lib_cases_store_data_file": "DATA_FILE" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L51 | neighbors=[cases-store.ts]
- "lib_cases_store_getslainfo": "getSlaInfo()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L320 | neighbors=[cases-store.ts]
- "lib_cases_store_seed_cases": "SEED_CASES" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L61 | neighbors=[cases-store.ts]
- "lib_cases_store_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L53 | neighbors=[cases-store.ts]
- "lib_clients_store_clientjiraconfig": "ClientJiraConfig" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L8 | neighbors=[clients-store.ts]
- "lib_clients_store_clientnotifyconfig": "ClientNotifyConfig" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L15 | neighbors=[clients-store.ts]
- "lib_clients_store_clientsettings": "ClientSettings" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L21 | neighbors=[clients-store.ts]
- "lib_clients_store_clientsfile": "ClientsFile" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L36 | neighbors=[clients-store.ts]
- "lib_clients_store_clientstatus": "ClientStatus" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L6 | neighbors=[clients-store.ts]
- "lib_clients_store_data_path": "DATA_PATH" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L4 | neighbors=[clients-store.ts]
- "lib_clients_store_seed": "SEED" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L41 | neighbors=[clients-store.ts]
- "lib_detection_store_attack_timeline": "ATTACK_TIMELINE" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L22 | neighbors=[detection-store.ts]
- "lib_detection_store_attackaction": "AttackAction" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L8 | neighbors=[detection-store.ts]
- "lib_detection_store_computecoverage": "computeCoverage()" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L131 | neighbors=[detection-store.ts]
- "lib_detection_store_correlate": "correlate()" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L97 | neighbors=[detection-store.ts]
- "lib_detection_store_correlationruns": "correlationRuns" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L413 | neighbors=[detection-store.ts]
- "lib_detection_store_coveragestats": "CoverageStats" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L78 | neighbors=[detection-store.ts]
- "lib_detection_store_detectionoutcome": "DetectionOutcome" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L4 | neighbors=[detection-store.ts]
- "lib_detection_store_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L65 | neighbors=[detection-store.ts]
- "lib_detection_store_edr_detections": "EDR_DETECTIONS" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L56 | neighbors=[detection-store.ts]
- "lib_detection_store_edrdetection": "EDRDetection" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L41 | neighbors=[detection-store.ts]
- "lib_detection_store_generatesigma": "generateSigma()" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L359 | neighbors=[detection-store.ts]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-095.json

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
