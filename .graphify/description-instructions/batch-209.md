# Node Description Batch 210 of 336

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

- "lib_auth_store_otpentry": "OtpEntry" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L8 | neighbors=[auth-store.ts]
- "lib_auth_store_otpstore": "otpStore" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L15 | neighbors=[auth-store.ts]
- "lib_auth_store_otpverifyresult": "OtpVerifyResult" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L34 | neighbors=[auth-store.ts]
- "lib_auth_store_sessionpayload": "SessionPayload" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L17 | neighbors=[auth-store.ts]
- "lib_backend_backenderror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L18 | neighbors=[BackendError]
- "lib_backend_backendopts": "BackendOpts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L25 | neighbors=[backend.ts]
- "lib_backend_base": "BASE" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L11 | neighbors=[backend.ts]
- "lib_campaign_store_campaignstatus": "CampaignStatus" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L25 | neighbors=[campaign-store.ts]
- "lib_campaign_store_campaignsummary": "CampaignSummary" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L58 | neighbors=[campaign-store.ts]
- "lib_campaign_store_campaigntotals": "CampaignTotals" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L38 | neighbors=[campaign-store.ts]
- "lib_campaign_store_default_dir": "DEFAULT_DIR" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L72 | neighbors=[campaign-store.ts]
- "lib_campaign_store_normalizestage": "normalizeStage()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L122 | neighbors=[campaign-store.ts]
- "lib_campaign_store_stagesnapshot": "StageSnapshot" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L27 | neighbors=[campaign-store.ts]
- "lib_campaign_store_stagestatus": "StageStatus" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L24 | neighbors=[campaign-store.ts]
- "lib_cases_store_case": "Case" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L24 | neighbors=[cases-store.ts]
- "lib_cases_store_caseactivity": "CaseActivity" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L14 | neighbors=[cases-store.ts]
- "lib_cases_store_casecomment": "CaseComment" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L7 | neighbors=[cases-store.ts]
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
- "lib_console_source_consolecapability": "ConsoleCapability" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L48 | neighbors=[console-source.tsx]
- "lib_console_source_consolequeryoptions": "ConsoleQueryOptions" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L152 | neighbors=[console-source.tsx]
- "lib_console_source_consolesource": "ConsoleSource" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L56 | neighbors=[console-source.tsx]
- "lib_console_source_consolesourcecontext": "ConsoleSourceContext" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L103 | neighbors=[console-source.tsx]
- "lib_console_source_consolesourceprovider": "ConsoleSourceProvider()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L105 | neighbors=[console-source.tsx]
- "lib_console_source_operator_source": "OPERATOR_SOURCE" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L66 | neighbors=[console-source.tsx]
- "lib_console_source_portal_source": "PORTAL_SOURCE" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L87 | neighbors=[console-source.tsx]
- "lib_detection_store_attack_timeline": "ATTACK_TIMELINE" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L22 | neighbors=[detection-store.ts]
- "lib_detection_store_attackaction": "AttackAction" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L8 | neighbors=[detection-store.ts]
- "lib_detection_store_computecoverage": "computeCoverage()" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L131 | neighbors=[detection-store.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-209.json

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
