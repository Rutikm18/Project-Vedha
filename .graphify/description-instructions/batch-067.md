# Node Description Batch 68 of 119

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

- "tools_manifest_adversa_manifest_file": "ADVERSA_MANIFEST_FILE" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L22 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_adversa_tools_dir": "ADVERSA_TOOLS_DIR" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L21 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_currentplatform": "currentPlatform()" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L54 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_toolsource": "ToolSource" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L29 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_toolspec": "ToolSpec" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L40 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_vedha_manifest_file": "VEDHA_MANIFEST_FILE" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L22 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_vedha_tools_dir": "VEDHA_TOOLS_DIR" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L21 | neighbors=[installer.ts, manifest.ts]
- "ui_output_banner": "banner()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L53 | neighbors=[output.ts, ln()]
- "ui_output_findingstable": "findingsTable()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L210 | neighbors=[output.ts, ln()]
- "ui_output_hostline": "hostLine()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L149 | neighbors=[output.ts, ln()]
- "ui_output_info": "info()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L273 | neighbors=[output.ts, ln()]
- "ui_output_sevbadge": "sevBadge()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L43 | neighbors=[output.ts, findingLine()]
- "ui_output_stagecomplete": "stageComplete()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L126 | neighbors=[output.ts, ln()]
- "ui_output_stageprogress": "stageProgress()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L122 | neighbors=[output.ts, w()]
- "ui_output_stagestart": "stageStart()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L116 | neighbors=[output.ts, ln()]
- "utils_csv_parser_parse_csv_assets": "parse_csv_assets()" | kind=code-symbol | source=manager/backend/app/utils/csv_parser.py:L25 | neighbors=[csv_parser.py, Parse CSV text into a list of AssetIn m…]
- "utils_db_get_or_404": "get_or_404()" | kind=code-symbol | source=manager/backend/app/utils/db.py:L17 | neighbors=[db.py, Fetch a row by primary key, optionally …]
- "utils_hash_dedup_hash": "dedup_hash()" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L10 | neighbors=[hash.py, SHA-256 of (asset_id, cve_id, plugin_id…]
- "utils_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/utils/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "utils_pagination_paginate_query": "paginate_query()" | kind=code-symbol | source=manager/backend/app/utils/pagination.py:L6 | neighbors=[pagination.py, Returns (items, total). Applies OFFSET/…]
- "vuln_enrichment_rationale_1": "VulnEnrichmentService  External data sources:   NVD 2.0     https://services.nvd" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L1 | neighbors=[AssetCriticality, enrichment.py]
- "vuln_enrichment_rationale_110": "Add NVD CVSS, EPSS, KEV flag, MITRE techniques, and composite risk.         Muta" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L110 | neighbors=[AssetCriticality, .enrich()]
- "vuln_enrichment_rationale_164": "Returns {cvss_v3, cvss_vector, description, references, published_date}." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L164 | neighbors=[AssetCriticality, .fetch_nvd()]
- "vuln_enrichment_rationale_216": "Returns {epss_score: float, percentile: float} or {}." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L216 | neighbors=[AssetCriticality, .fetch_epss()]
- "vuln_enrichment_rationale_245": "True if CVE is in the CISA Known Exploited Vulnerabilities catalog." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L245 | neighbors=[AssetCriticality, .check_cisa_kev()]
- "vuln_enrichment_rationale_271": "Returns MITRE ATT&CK technique IDs linked to this CVE.         Uses hardcoded hi" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L271 | neighbors=[AssetCriticality, .fetch_mitre_techniques()]
- "vuln_enrichment_rationale_28": "LRU + TTL eviction. Expired keys are purged on access; when ``maxsize``     is e" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L28 | neighbors=[AssetCriticality, TTLCache]
- "vuln_enrichment_rationale_307": "Returns composite risk score on 0-1000 scale.          Formula:           (cvss*" | kind=entity | source=manager/backend/app/vuln/enrichment.py:L307 | neighbors=[AssetCriticality, .compute_composite_risk()]
- "vuln_enrichment_rationale_342": "Fetch NVD, EPSS, KEV and MITRE concurrently." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L342 | neighbors=[AssetCriticality, ._fetch_all()]
- "vuln_enrichment_rationale_352": "SHA-256 of (asset_id, cve_id, plugin_id) for deduplication." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L352 | neighbors=[AssetCriticality, .dedup_hash()]
- "vuln_enrichment_rationale_92": "Enriches Finding objects with NVD, EPSS, CISA KEV, and MITRE data." | kind=entity | source=manager/backend/app/vuln/enrichment.py:L92 | neighbors=[AssetCriticality, VulnEnrichmentService]
- "vuln_enrichment_vulnenrichmentservice_dedup_hash": ".dedup_hash()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L351 | neighbors=[SHA-256 of (asset_id, cve_id, plugin_id…, VulnEnrichmentService]
- "vuln_enrichment_vulnenrichmentservice_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L94 | neighbors=[VulnEnrichmentService, TTLCache]
- "vuln_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/vuln/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_nessus_nessusscanner_auth_headers": "._auth_headers()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L60 | neighbors=[NessusScanner, ._get_client()]
- "vuln_nessus_nessusscanner_authenticate": ".authenticate()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L73 | neighbors=[NessusScanner, Prefer API key auth (stateless, no sess…]
- "vuln_nessus_nessusscanner_get_plugin_detail": "._get_plugin_detail()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L194 | neighbors=[NessusScanner, .get_results()]
- "vuln_nessus_nessusscanner_get_template_uuid": "._get_template_uuid()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L125 | neighbors=[NessusScanner, .create_scan()]
- "vuln_nessus_nessusscanner_map_finding": ".map_finding()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L206 | neighbors=[NessusScanner, Map a raw Nessus vulnerability dict → F…]
- "vuln_nuclei_nucleiscanner_read_stderr": "._read_stderr()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L314 | neighbors=[NucleiScanner, .run_scan()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-067.json

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
