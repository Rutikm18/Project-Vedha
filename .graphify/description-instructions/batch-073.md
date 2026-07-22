# Node Description Batch 74 of 76

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

- "ui_output_stage_label": "STAGE_LABEL" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L78 | neighbors=[output.ts]
- "use_cases_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/use-cases/route.ts:L6 | neighbors=[route.ts]
- "utils_db_rationale_1": "Shared database helpers — single source of truth for patterns duplicated across" | kind=entity | source=manager/backend/app/utils/db.py:L1 | neighbors=[db.py]
- "utils_db_rationale_24": "Fetch a row by primary key, optionally scoped to a tenant.     Raises 404 if mis" | kind=entity | source=manager/backend/app/utils/db.py:L24 | neighbors=[get_or_404()]
- "utils_hash_rationale_1": "Shared hashing utilities — deduplication keys, fingerprinting." | kind=entity | source=manager/backend/app/utils/hash.py:L1 | neighbors=[hash.py]
- "utils_hash_rationale_11": "SHA-256 of (asset_id, cve_id, plugin_id) for finding deduplication.      Used by" | kind=entity | source=manager/backend/app/utils/hash.py:L11 | neighbors=[dedup_hash()]
- "utils_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/utils/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …]
- "utils_pagination_rationale_12": "Returns (items, total). Applies OFFSET/LIMIT to `query`." | kind=entity | source=manager/backend/app/utils/pagination.py:L12 | neighbors=[paginate_query()]
- "verify_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L6 | neighbors=[route.ts]
- "versions_0001_initial_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L174 | neighbors=[0001_initial.py]
- "versions_0001_initial_rationale_1": "Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19" | kind=entity | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[0001_initial.py]
- "versions_0001_initial_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L19 | neighbors=[0001_initial.py]
- "versions_0002_services_agents_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L59 | neighbors=[0002_services_agents.py]
- "versions_0002_services_agents_rationale_1": "Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202" | kind=entity | source=manager/backend/alembic/versions/0002_services_agents.py:L1 | neighbors=[0002_services_agents.py]
- "versions_0002_services_agents_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L19 | neighbors=[0002_services_agents.py]
- "versions_0003_vuln_scan_fields_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L43 | neighbors=[0003_vuln_scan_fields.py]
- "versions_0003_vuln_scan_fields_rationale_1": "Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R" | kind=entity | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L1 | neighbors=[0003_vuln_scan_fields.py]
- "versions_0003_vuln_scan_fields_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L18 | neighbors=[0003_vuln_scan_fields.py]
- "versions_0004_exploit_tables_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L93 | neighbors=[0004_exploit_tables.py]
- "versions_0004_exploit_tables_rationale_1": "Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000" | kind=entity | source=manager/backend/alembic/versions/0004_exploit_tables.py:L1 | neighbors=[0004_exploit_tables.py]
- "versions_0004_exploit_tables_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L19 | neighbors=[0004_exploit_tables.py]
- "versions_0005_detection_validation_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0005_detection_validation.py:L80 | neighbors=[0005_detection_validation.py]
- "versions_0005_detection_validation_rationale_1": "Detection validation: attack_timeline, detection_configs, extend detection_resul" | kind=entity | source=manager/backend/alembic/versions/0005_detection_validation.py:L1 | neighbors=[0005_detection_validation.py]
- "versions_0005_detection_validation_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0005_detection_validation.py:L19 | neighbors=[0005_detection_validation.py]
- "versions_0006_llm_outputs_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L48 | neighbors=[0006_llm_outputs.py]
- "versions_0006_llm_outputs_rationale_1": "AI engine: llm_outputs table + reviewstatus enum  Revision ID: 0006 Revises: 000" | kind=entity | source=manager/backend/alembic/versions/0006_llm_outputs.py:L1 | neighbors=[0006_llm_outputs.py]
- "versions_0006_llm_outputs_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L19 | neighbors=[0006_llm_outputs.py]
- "versions_0007_scale_indexes_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L35 | neighbors=[0007_scale_indexes.py]
- "versions_0007_scale_indexes_rationale_1": "P3: composite indexes for the hot aggregate + poll query paths.  The dashboard's" | kind=entity | source=manager/backend/alembic/versions/0007_scale_indexes.py:L1 | neighbors=[0007_scale_indexes.py]
- "versions_0007_scale_indexes_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L22 | neighbors=[0007_scale_indexes.py]
- "versions_0008_scan_results_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L39 | neighbors=[0008_scan_results.py]
- "versions_0008_scan_results_rationale_1": "P3-#10: append-only scan_results table (raw facts).  Decouples the (large) raw f" | kind=entity | source=manager/backend/alembic/versions/0008_scan_results.py:L1 | neighbors=[0008_scan_results.py]
- "versions_0008_scan_results_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L21 | neighbors=[0008_scan_results.py]
- "vuln_enrichment_ttlcache_contains": ".__contains__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L36 | neighbors=[TTLCache]
- "vuln_enrichment_ttlcache_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L43 | neighbors=[TTLCache]
- "vuln_enrichment_ttlcache_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L31 | neighbors=[TTLCache]
- "vuln_enrichment_ttlcache_setitem": ".__setitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L51 | neighbors=[TTLCache]
- "vuln_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/vuln/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …]
- "vuln_nessus_nessusscanner_close": ".close()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L67 | neighbors=[NessusScanner]
- "vuln_nessus_nessusscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L41 | neighbors=[NessusScanner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-073.json

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
