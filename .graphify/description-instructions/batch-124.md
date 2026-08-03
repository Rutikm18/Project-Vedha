# Node Description Batch 125 of 131

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

- "tests_test_ws_claim_protocol_test_staged_job_is_not_released_without_positive_confirmation": "test_staged_job_is_not_released_without_positive_confirmation()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L34 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_ws_job_does_not_duplicate_task_runner_result_submission": "test_ws_job_does_not_duplicate_task_runner_result_submission()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L96 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_xml_parser_testnmapxmlparser_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L43 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_cpe_extraction": ".test_cpe_extraction()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L71 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_empty_scan": ".test_empty_scan()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L76 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_empty_string": ".test_empty_string()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L84 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_malformed_xml_returns_empty": ".test_malformed_xml_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L80 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_multiple_hosts": ".test_multiple_hosts()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L90 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_none_safe": ".test_none_safe()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L87 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_open_ports_only": ".test_open_ports_only()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L59 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_parse_full_host": ".test_parse_full_host()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L46 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_port_details": ".test_port_details()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L65 | neighbors=[TestNmapXMLParser]
- "tools_installer_installedmanifest": "InstalledManifest" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L29 | neighbors=[installer.ts]
- "tools_installer_installedrecord": "InstalledRecord" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L20 | neighbors=[installer.ts]
- "tools_installer_installprogress": "InstallProgress" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L149 | neighbors=[installer.ts]
- "tools_installer_toolstatus": "ToolStatus" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L254 | neighbors=[installer.ts]
- "tools_manifest_platform": "Platform" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L24 | neighbors=[manifest.ts]
- "ui_output_a": "A" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L5 | neighbors=[output.ts]
- "ui_output_error": "error()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L269 | neighbors=[output.ts]
- "ui_output_line": "LINE" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L49 | neighbors=[output.ts]
- "ui_output_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L33 | neighbors=[output.ts]
- "ui_output_stage_col": "STAGE_COL" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L103 | neighbors=[output.ts]
- "ui_output_stage_label": "STAGE_LABEL" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L78 | neighbors=[output.ts]
- "use_cases_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/use-cases/route.ts:L6 | neighbors=[route.ts]
- "utils_db_rationale_1": "Shared database helpers — single source of truth for patterns duplicated across" | kind=entity | source=manager/backend/app/utils/db.py:L1 | neighbors=[db.py]
- "utils_db_rationale_24": "Fetch a row by primary key, optionally scoped to a tenant.     Raises 404 if mis" | kind=entity | source=manager/backend/app/utils/db.py:L24 | neighbors=[get_or_404()]
- "utils_hash_rationale_1": "Shared hashing utilities — deduplication keys, fingerprinting." | kind=entity | source=manager/backend/app/utils/hash.py:L1 | neighbors=[hash.py]
- "utils_hash_rationale_11": "SHA-256 of (asset_id, cve_id, plugin_id) for finding deduplication.      Used by" | kind=entity | source=manager/backend/app/utils/hash.py:L11 | neighbors=[dedup_hash()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-124.json

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
