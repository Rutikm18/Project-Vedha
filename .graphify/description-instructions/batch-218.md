# Node Description Batch 219 of 380

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

- "dashboard_dashboardworkspace_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardWorkspace.tsx:L10 | neighbors=[DashboardWorkspace.tsx]
- "dashboard_dashboardworkspace_slapayload": "SlaPayload" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardWorkspace.tsx:L11 | neighbors=[DashboardWorkspace.tsx]
- "dashboard_exposurecards_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L25 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_healthband": "healthBand()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L47 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_meterrow": "MeterRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L56 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_riskband": "riskBand()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L39 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_scalenote": "scaleNote" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L150 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_showallbutton": "ShowAllButton()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L156 | neighbors=[ExposureCards.tsx]
- "dashboard_liveoverview_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L32 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_finding": "Finding" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L23 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L34 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isactiveengagement": "isActiveEngagement()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L41 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isopen": "isOpen()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L34 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_kpi": "Kpi()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L43 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L22 | neighbors=[LiveOverview.tsx]
- "dashboard_patchcomparisonmatrix_cell": "cell" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L24 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_head": "head" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L33 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_netchip": "NetChip()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L49 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_netlabel": "netLabel()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L19 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L14 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_posturescorecard_delta": "Delta()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L45 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_dial": "Dial()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L57 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_grade": "GRADE" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L44 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_grade_color": "GRADE_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L39 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_metrictile": "MetricTile()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L95 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_posture": "Posture" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L29 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_readout": "Readout()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L82 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_scores": "Scores" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L23 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_statcard": "StatCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L55 | neighbors=[PostureScorecard.tsx]
- "dashboard_slastatus_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L17 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_sev_style": "SEV_STYLE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L37 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slaitem": "SlaItem" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L33 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slastate": "SlaState" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L31 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slasummary": "SlaSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L38 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_state": "STATE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L43 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_state_color": "STATE_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L30 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_statecell": "StateCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L83 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_summarycell": "SummaryCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L61 | neighbors=[SlaStatus.tsx]
- "declarativebase": "DeclarativeBase" | kind=code-symbol | neighbors=[Base]
- "detection_active_validation_rationale_1": "active_validation.py — manager-side decision core for safe active validation.  P" | kind=entity | source=manager/backend/app/detection/active_validation.py:L1 | neighbors=[active_validation.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-218.json

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
