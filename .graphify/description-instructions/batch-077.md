# Node Description Batch 78 of 119

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

- "components_sidebar_sidebarprops": "SidebarProps" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L43 | neighbors=[Sidebar.tsx]
- "components_themeprovider_subscribetohydration": "subscribeToHydration()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L24 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_theme": "Theme" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L12 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontext": "ThemeContext" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L19 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontextvalue": "ThemeContextValue" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L14 | neighbors=[ThemeProvider.tsx]
- "components_toastprovider_toast": "Toast" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L8 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toast_styles": "TOAST_STYLES" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L35 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastcontextvalue": "ToastContextValue" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L17 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastitem": "ToastItem()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L69 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toasttype": "ToastType" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L6 | neighbors=[ToastProvider.tsx]
- "config_config_test_testloadenvironmentoverridesenvfile": "TestLoadEnvironmentOverridesEnvFile()" | kind=code-symbol | source=probe-go/config/config_test.go:L9 | neighbors=[config_test.go]
- "dashboard_exposure_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/components/dashboard/Exposure.tsx:L19 | neighbors=[Exposure.tsx]
- "dashboard_liveoverview_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L23 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_finding": "Finding" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L23 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L24 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isactiveengagement": "isActiveEngagement()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L39 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isopen": "isOpen()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L34 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_kpi": "Kpi()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L43 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L22 | neighbors=[LiveOverview.tsx]
- "dashboard_slarow_sev_bg": "SEV_BG" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L19 | neighbors=[SlaRow.tsx]
- "dashboard_slarow_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L25 | neighbors=[SlaRow.tsx]
- "dashboard_slastatus_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L17 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_sev_style": "SEV_STYLE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L37 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slaitem": "SlaItem" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L20 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slastate": "SlaState" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L18 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slasummary": "SlaSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L25 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_state_color": "STATE_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L30 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_summarycell": "SummaryCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L61 | neighbors=[SlaStatus.tsx]
- "dashboard_slasummarycell_slasummarymetric": "SlaSummaryMetric" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaSummaryCell.tsx:L5 | neighbors=[SlaSummaryCell.tsx]
- "data_mock_dashboard_attackpath": "AttackPath" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L13 | neighbors=[mock-dashboard.ts]
- "data_mock_dashboard_top_findings": "TOP_FINDINGS" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L71 | neighbors=[mock-dashboard.ts]
- "declarativebase": "DeclarativeBase" | kind=code-symbol | neighbors=[Base]
- "detection_correlator_detectioncorrelator_compute_coverage": ".compute_coverage()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L159 | neighbors=[DetectionCorrelator]
- "detection_correlator_detectioncorrelator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L76 | neighbors=[DetectionCorrelator]
- "detection_edr_build_edr_engine": "build_edr_engine()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L235 | neighbors=[edr.py]
- "detection_edr_edrdetection_is_prevented": ".is_prevented()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L43 | neighbors=[EDRDetection]
- "detection_edr_edrqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L65 | neighbors=[EDRQueryEngine]
- "detection_edr_edrqueryengine_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L70 | neighbors=[EDRQueryEngine]
- "detection_edr_rationale_1": "EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender" | kind=entity | source=manager/backend/app/detection/edr.py:L1 | neighbors=[edr.py]
- "detection_edr_rationale_141": "Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi" | kind=entity | source=manager/backend/app/detection/edr.py:L141 | neighbors=[MicrosoftDefender]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-077.json

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
