# Node Description Batch 193 of 336

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "cve_init_rationale_1": "cve — vulnerability (CVE) correlation layer.  SEPARATE from the probe's collecti" | kind=entity | source=probe/cve/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "cve_online_rationale_1": "online.py — OPT-IN live enrichment for CVE findings.  The offline mirror (vulndb" | kind=entity | source=probe/cve/online.py:L1 | neighbors=[online.py] | lang=en
- "cve_online_rationale_134": "Enrich CVE findings in place from live sources and return the same list.      `o" | kind=entity | source=probe/cve/online.py:L134 | neighbors=[enrich_findings()] | lang=en
- "cve_online_rationale_175": "Fold one CVE's live result into a finding. FILLS a missing CVSS (and     recompu" | kind=entity | source=probe/cve/online.py:L175 | neighbors=[_apply()] | lang=pt
- "cve_online_rationale_215": "Recover whether the exposure boost was applied, so a re-scored (gap-filled)" | kind=entity | source=probe/cve/online.py:L215 | neighbors=[_was_exposed()] | lang=en
- "cve_online_rationale_52": "What a live lookup could establish for one CVE (any field may be None when     t" | kind=entity | source=probe/cve/online.py:L52 | neighbors=[OnlineResult] | lang=en
- "cve_online_rationale_68": "Query live NVD 2.0 for one CVE. Returns an OnlineResult, or None on any     netw" | kind=entity | source=probe/cve/online.py:L68 | neighbors=[lookup_nvd()] | lang=en
- "cve_online_rationale_93": "Ask Vulners whether a public exploit is catalogued for `cve_id`. Returns     Tru" | kind=entity | source=probe/cve/online.py:L93 | neighbors=[lookup_vulners()] | lang=en
- "cve_version_rationale_1": "version.py — loose version comparison for CVE range matching.  Real service bann" | kind=entity | source=probe/cve/version.py:L1 | neighbors=[version.py] | lang=en
- "cve_version_rationale_29": "Normalize a version string into a comparable tuple of ints." | kind=entity | source=probe/cve/version.py:L29 | neighbors=[parse_version()] | lang=pt
- "cve_version_rationale_48": "Return -1/0/1 for version a vs b (zero-padded tuple comparison)." | kind=entity | source=probe/cve/version.py:L48 | neighbors=[compare()] | lang=en
- "cve_version_rationale_58": "Is `version` inside the NVD-style bound set? An `exact` match (no range     boun" | kind=entity | source=probe/cve/version.py:L58 | neighbors=[in_range()] | lang=en
- "cve_vulndb_rationale_1": "vulndb.py — the offline vulnerability mirror (SQLite) and its query surface.  Ho" | kind=entity | source=probe/cve/vulndb.py:L1 | neighbors=[vulndb.py] | lang=en
- "cve_vulndb_rationale_120": "All vulnerable CVEs whose CPE applicability covers (vendor, product,         ver" | kind=entity | source=probe/cve/vulndb.py:L120 | neighbors=[.cves_for_cpe()] | lang=en
- "cve_vulndb_vulndb_close": ".close()" | kind=code-symbol | source=probe/cve/vulndb.py:L110 | neighbors=[VulnDB] | lang=en
- "cve_vulndb_vulndb_counts": ".counts()" | kind=code-symbol | source=probe/cve/vulndb.py:L113 | neighbors=[VulnDB] | lang=en
- "cve_vulndb_vulndb_get_meta": ".get_meta()" | kind=code-symbol | source=probe/cve/vulndb.py:L103 | neighbors=[VulnDB] | lang=en
- "cve_vulndb_vulndb_replace_cpe_matches": ".replace_cpe_matches()" | kind=code-symbol | source=probe/cve/vulndb.py:L89 | neighbors=[VulnDB] | lang=en
- "cve_vulndb_vulndb_set_meta": ".set_meta()" | kind=code-symbol | source=probe/cve/vulndb.py:L100 | neighbors=[VulnDB] | lang=en
- "cve_vulndb_vulndb_upsert_cve": ".upsert_cve()" | kind=code-symbol | source=probe/cve/vulndb.py:L72 | neighbors=[VulnDB] | lang=en
- "cve_vulndb_vulndb_upsert_epss": ".upsert_epss()" | kind=code-symbol | source=probe/cve/vulndb.py:L96 | neighbors=[VulnDB] | lang=en
- "cve_weakness_map_has_version": "_has_version()" | kind=code-symbol | source=probe/cve/weakness_map.py:L52 | neighbors=[weakness_map.py] | lang=en
- "cve_weakness_map_rationale_1": "weakness_map.py — bridge the probe's deterministic weakness findings to canonica" | kind=entity | source=probe/cve/weakness_map.py:L1 | neighbors=[weakness_map.py] | lang=en
- "cve_weakness_map_rationale_121": "Return the Finding dict from a fact, or None if the fact is not a finding." | kind=entity | source=probe/cve/weakness_map.py:L121 | neighbors=[_finding_view()] | lang=en
- "cve_weakness_map_rationale_142": "Pull CVSS/KEV/EPSS for one CVE straight from the mirror tables. Degrades to" | kind=entity | source=probe/cve/weakness_map.py:L142 | neighbors=[_mirror_cve()] | lang=en
- "cve_weakness_map_rationale_165": "Map observed weakness findings to their canonical CVE(s), enriched with live" | kind=entity | source=probe/cve/weakness_map.py:L165 | neighbors=[correlate_weaknesses()] | lang=en
- "cve_weakness_map_rationale_217": "Every canonical CVE referenced by the weakness map that the mirror does NOT" | kind=entity | source=probe/cve/weakness_map.py:L217 | neighbors=[missing_from_mirror()] | lang=en
- "cve_weakness_map_rationale_38": "One canonical CVE a weakness can map to, optionally gated on the finding's     s" | kind=entity | source=probe/cve/weakness_map.py:L38 | neighbors=[_Assoc] | lang=en
- "cve_weakness_map_weaknessmapping": "WeaknessMapping" | kind=code-symbol | source=probe/cve/weakness_map.py:L46 | neighbors=[weakness_map.py] | lang=en
- "dashboard_dashboardgrid_agent": "Agent" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L38 | neighbors=[DashboardGrid.tsx] | lang=en
- "dashboard_dashboardgrid_agent_status": "AGENT_STATUS" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L40 | neighbors=[DashboardGrid.tsx] | lang=en
- "dashboard_dashboardgrid_agentmonitor": "AgentMonitor()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L75 | neighbors=[DashboardGrid.tsx] | lang=en
- "dashboard_dashboardgrid_agentrow": "AgentRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L46 | neighbors=[DashboardGrid.tsx] | lang=en
- "dashboard_dashboardgrid_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L37 | neighbors=[DashboardGrid.tsx] | lang=en
- "dashboard_dashboardgrid_freshnote": "FreshNote()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L126 | neighbors=[DashboardGrid.tsx] | lang=en
- "dashboard_exposurecards_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L25 | neighbors=[ExposureCards.tsx] | lang=en
- "dashboard_exposurecards_healthband": "healthBand()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L47 | neighbors=[ExposureCards.tsx] | lang=en
- "dashboard_exposurecards_meterrow": "MeterRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L56 | neighbors=[ExposureCards.tsx] | lang=en
- "dashboard_exposurecards_riskband": "riskBand()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L39 | neighbors=[ExposureCards.tsx] | lang=en
- "dashboard_exposurecards_scalenote": "scaleNote" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L150 | neighbors=[ExposureCards.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-192.json

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
