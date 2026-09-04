# Node Description Batch 189 of 330

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

- "cve_vulndb_rationale_120": "All vulnerable CVEs whose CPE applicability covers (vendor, product,         ver" | kind=entity | source=probe/cve/vulndb.py:L120 | neighbors=[.cves_for_cpe()]
- "cve_vulndb_vulndb_close": ".close()" | kind=code-symbol | source=probe/cve/vulndb.py:L110 | neighbors=[VulnDB]
- "cve_vulndb_vulndb_counts": ".counts()" | kind=code-symbol | source=probe/cve/vulndb.py:L113 | neighbors=[VulnDB]
- "cve_vulndb_vulndb_get_meta": ".get_meta()" | kind=code-symbol | source=probe/cve/vulndb.py:L103 | neighbors=[VulnDB]
- "cve_vulndb_vulndb_replace_cpe_matches": ".replace_cpe_matches()" | kind=code-symbol | source=probe/cve/vulndb.py:L89 | neighbors=[VulnDB]
- "cve_vulndb_vulndb_set_meta": ".set_meta()" | kind=code-symbol | source=probe/cve/vulndb.py:L100 | neighbors=[VulnDB]
- "cve_vulndb_vulndb_upsert_cve": ".upsert_cve()" | kind=code-symbol | source=probe/cve/vulndb.py:L72 | neighbors=[VulnDB]
- "cve_vulndb_vulndb_upsert_epss": ".upsert_epss()" | kind=code-symbol | source=probe/cve/vulndb.py:L96 | neighbors=[VulnDB]
- "cve_weakness_map_has_version": "_has_version()" | kind=code-symbol | source=probe/cve/weakness_map.py:L52 | neighbors=[weakness_map.py]
- "cve_weakness_map_rationale_1": "weakness_map.py — bridge the probe's deterministic weakness findings to canonica" | kind=entity | source=probe/cve/weakness_map.py:L1 | neighbors=[weakness_map.py]
- "cve_weakness_map_rationale_121": "Return the Finding dict from a fact, or None if the fact is not a finding." | kind=entity | source=probe/cve/weakness_map.py:L121 | neighbors=[_finding_view()]
- "cve_weakness_map_rationale_142": "Pull CVSS/KEV/EPSS for one CVE straight from the mirror tables. Degrades to" | kind=entity | source=probe/cve/weakness_map.py:L142 | neighbors=[_mirror_cve()]
- "cve_weakness_map_rationale_165": "Map observed weakness findings to their canonical CVE(s), enriched with live" | kind=entity | source=probe/cve/weakness_map.py:L165 | neighbors=[correlate_weaknesses()]
- "cve_weakness_map_rationale_217": "Every canonical CVE referenced by the weakness map that the mirror does NOT" | kind=entity | source=probe/cve/weakness_map.py:L217 | neighbors=[missing_from_mirror()]
- "cve_weakness_map_rationale_38": "One canonical CVE a weakness can map to, optionally gated on the finding's     s" | kind=entity | source=probe/cve/weakness_map.py:L38 | neighbors=[_Assoc]
- "cve_weakness_map_weaknessmapping": "WeaknessMapping" | kind=code-symbol | source=probe/cve/weakness_map.py:L46 | neighbors=[weakness_map.py]
- "dashboard_dashboardgrid_agent": "Agent" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L38 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agent_status": "AGENT_STATUS" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L40 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agentmonitor": "AgentMonitor()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L75 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agentrow": "AgentRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L46 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L37 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_freshnote": "FreshNote()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L126 | neighbors=[DashboardGrid.tsx]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-188.json

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
