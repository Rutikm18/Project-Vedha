# Node Description Batch 204 of 332

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

- "id_campaignprogress_coverage": "Coverage" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L43 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L110 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L37 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_findingsempty": "FindingsEmpty()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L469 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_job": "Job" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L31 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_jobbar": "jobBar()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L84 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_jobsummary": "JobSummary" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L27 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_phase": "Phase" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L26 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_phase_label": "PHASE_LABEL" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L100 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_phasestate": "PhaseState" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L25 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_progress": "Progress" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L47 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_remediationsteps": "remediationSteps()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L120 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L104 | neighbors=[CampaignProgress.tsx]
- "id_campaignprogress_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L68 | neighbors=[CampaignProgress.tsx]
- "id_page_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L38 | neighbors=[page.tsx]
- "id_page_activitytab": "ActivityTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L318 | neighbors=[page.tsx]
- "id_page_assetrow": "AssetRow" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L46 | neighbors=[page.tsx]
- "id_page_assetstab": "AssetsTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L276 | neighbors=[page.tsx]
- "id_page_campaignsnapshot": "CampaignSnapshot" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L18 | neighbors=[page.tsx]
- "id_page_cardskeleton": "CardSkeleton()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L43 | neighbors=[page.tsx]
- "id_page_edit_statuses": "EDIT_STATUSES" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L378 | neighbors=[page.tsx]
- "id_page_editengagementmodal": "EditEngagementModal()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L380 | neighbors=[page.tsx]
- "id_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L20 | neighbors=[page.tsx]
- "id_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L55 | neighbors=[page.tsx]
- "id_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L70 | neighbors=[page.tsx]
- "id_page_findingrow": "FindingRow" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L62 | neighbors=[page.tsx]
- "id_page_findingstab": "FindingsTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L225 | neighbors=[page.tsx]
- "id_page_importscanbutton": "ImportScanButton()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L335 | neighbors=[page.tsx]
- "id_page_linkedtab": "LinkedTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L139 | neighbors=[page.tsx]
- "id_page_sevcolor": "sevColor()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L27 | neighbors=[page.tsx]
- "id_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L18 | neighbors=[page.tsx]
- "id_page_severity_color": "SEVERITY_COLOR" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L78 | neighbors=[page.tsx]
- "id_page_stagebadge": "stageBadge()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L28 | neighbors=[page.tsx]
- "id_page_stagesnapshot": "StageSnapshot" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L14 | neighbors=[page.tsx]
- "id_page_stagestatus": "StageStatus" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L13 | neighbors=[page.tsx]
- "id_page_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L84 | neighbors=[page.tsx]
- "id_page_tabkey": "TabKey" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L17 | neighbors=[page.tsx]
- "id_page_totals": "Totals()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L207 | neighbors=[page.tsx]
- "id_rawfacts_chip": "Chip()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/RawFacts.tsx:L135 | neighbors=[RawFacts.tsx]
- "id_rawfacts_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/RawFacts.tsx:L30 | neighbors=[RawFacts.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-203.json

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
