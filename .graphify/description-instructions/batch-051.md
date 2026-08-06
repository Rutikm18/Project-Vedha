# Node Description Batch 52 of 134

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

- "tests_test_task_runner_testrunnersubmission_test_calls_submit_with_result": ".test_calls_submit_with_result()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L390 | neighbors=[Verify the submit callback is called wi…, TestRunnerSubmission, Verify the submit callback is called wi…] | lang=en
- "tests_test_task_runner_testrunnersubmission_test_uses_spool_when_available": ".test_uses_spool_when_available()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L415 | neighbors=[When spool_submit is provided, it's use…, TestRunnerSubmission, When spool_submit is provided, it's use…] | lang=en
- "tests_test_transport_testfetchscope": "TestFetchScope" | kind=code-symbol | source=probe/tests/test_transport.py:L382 | neighbors=[test_transport.py, .test_http_error_returns_none(), .test_returns_scope()] | lang=en
- "tests_test_transport_transport": "transport()" | kind=code-symbol | source=probe/tests/test_transport.py:L17 | neighbors=[test_transport.py, Create a Transport with a real state fi…, Create a Transport with a real state fi…] | lang=en
- "tests_test_workflow_execution_explodingscanner": "_ExplodingScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L29 | neighbors=[test_workflow_execution.py, .scan_target(), test_per_target_exception_preserves_oth…] | lang=en
- "tools_installer_liststatus": "listStatus()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L264 | neighbors=[tools.ts, installer.ts, readInstalled()] | lang=en
- "tools_installer_writeinstalled": "writeInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L42 | neighbors=[installer.ts, installTool(), removeTool()] | lang=en
- "tools_issue_license_issue": "issue()" | kind=code-symbol | source=probe/tools/issue_license.py:L48 | neighbors=[issue_license.py, _b64(), main()] | lang=en
- "tools_issue_license_main": "main()" | kind=code-symbol | source=probe/tools/issue_license.py:L61 | neighbors=[issue_license.py, issue(), keygen()] | lang=en
- "tools_manifest_tool_manifest": "TOOL_MANIFEST" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L74 | neighbors=[tools.ts, installer.ts, manifest.ts] | lang=en
- "ui_output_findingdetail": "findingDetail()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L238 | neighbors=[output.ts, ln(), rule()] | lang=en
- "ui_output_findingline": "findingLine()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L184 | neighbors=[output.ts, ln(), sevBadge()] | lang=en
- "ui_output_scanheader": "scanHeader()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L63 | neighbors=[output.ts, ln(), rule()] | lang=en
- "ui_output_stageerror": "stageError()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L133 | neighbors=[output.ts, ln(), w()] | lang=en
- "ui_output_summary": "summary()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L194 | neighbors=[output.ts, ln(), rule()] | lang=en
- "ui_output_w": "w()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L29 | neighbors=[output.ts, stageError(), stageProgress()] | lang=en
- "utils_csv_parser": "csv_parser.py" | kind=code-symbol | source=manager/backend/app/utils/csv_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, parse_csv_assets(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "utils_csv_parser_rationale_26": "Parse CSV text into a list of AssetIn models and error strings." | kind=entity | source=manager/backend/app/utils/csv_parser.py:L26 | neighbors=[parse_csv_assets(), AssetCriticality, AssetType] | lang=en
- "utils_pagination": "pagination.py" | kind=code-symbol | source=manager/backend/app/utils/pagination.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, paginate_query(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "vuln_enrichment_vulnenrichmentservice_get_kev_catalog": "._get_kev_catalog()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L249 | neighbors=[VulnEnrichmentService, .check_cisa_kev(), .get()] | lang=en
- "vuln_nessus_nessusscanner_authenticate": ".authenticate()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L72 | neighbors=[NessusScanner, Prefer API key auth (stateless, no sess…, Prefer API key auth (stateless, no sess…] | lang=en
- "vuln_nessus_nessusscanner_map_finding": ".map_finding()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L205 | neighbors=[NessusScanner, Map a raw Nessus vulnerability dict → F…, Map a raw Nessus vulnerability dict → F…] | lang=en
- "vuln_nessus_rationale_1": "NessusScanner — wraps the Tenable Nessus REST API v6.  Endpoints used:   POST /s" | kind=entity | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[nessus.py, FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_101": "Returns nessus scan_id as string." | kind=entity | source=manager/backend/app/vuln/nessus.py:L101 | neighbors=[.create_scan(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_102": "Returns nessus scan_id as string." | kind=entity | source=manager/backend/app/vuln/nessus.py:L102 | neighbors=[FindingSeverity, FindingStatus, .create_scan()] | lang=en
- "vuln_nessus_rationale_140": "Returns scan_uuid (token for tracking)." | kind=entity | source=manager/backend/app/vuln/nessus.py:L140 | neighbors=[.launch_scan(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_141": "Returns scan_uuid (token for tracking)." | kind=entity | source=manager/backend/app/vuln/nessus.py:L141 | neighbors=[FindingSeverity, FindingStatus, .launch_scan()] | lang=en
- "vuln_nessus_rationale_151": "Returns {status, progress_percent, host_count}." | kind=entity | source=manager/backend/app/vuln/nessus.py:L151 | neighbors=[.poll_status(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_152": "Returns {status, progress_percent, host_count}." | kind=entity | source=manager/backend/app/vuln/nessus.py:L152 | neighbors=[FindingSeverity, FindingStatus, .poll_status()] | lang=en
- "vuln_nessus_rationale_167": "Returns list of raw finding dicts from all hosts." | kind=entity | source=manager/backend/app/vuln/nessus.py:L167 | neighbors=[.get_results(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_168": "Returns list of raw finding dicts from all hosts." | kind=entity | source=manager/backend/app/vuln/nessus.py:L168 | neighbors=[FindingSeverity, FindingStatus, .get_results()] | lang=en
- "vuln_nessus_rationale_206": "Map a raw Nessus vulnerability dict → Finding-compatible dict.         Returns a" | kind=entity | source=manager/backend/app/vuln/nessus.py:L206 | neighbors=[.map_finding(), FindingSeverity, FindingStatus] | lang=pt
- "vuln_nessus_rationale_207": "Map a raw Nessus vulnerability dict → Finding-compatible dict.         Returns a" | kind=entity | source=manager/backend/app/vuln/nessus.py:L207 | neighbors=[FindingSeverity, FindingStatus, .map_finding()] | lang=pt
- "vuln_nessus_rationale_257": "Request + poll + download .nessus XML for evidence storage." | kind=entity | source=manager/backend/app/vuln/nessus.py:L257 | neighbors=[.export_nessus_file(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_258": "Request + poll + download .nessus XML for evidence storage." | kind=entity | source=manager/backend/app/vuln/nessus.py:L258 | neighbors=[FindingSeverity, FindingStatus, .export_nessus_file()] | lang=en
- "vuln_nessus_rationale_38": "Async Nessus API client. One instance per engagement scan session." | kind=entity | source=manager/backend/app/vuln/nessus.py:L38 | neighbors=[NessusScanner, FindingSeverity, FindingStatus] | lang=it
- "vuln_nessus_rationale_39": "Async Nessus API client. One instance per engagement scan session." | kind=entity | source=manager/backend/app/vuln/nessus.py:L39 | neighbors=[FindingSeverity, FindingStatus, NessusScanner] | lang=it
- "vuln_nessus_rationale_73": "Prefer API key auth (stateless, no session expiry).         Falls back to userna" | kind=entity | source=manager/backend/app/vuln/nessus.py:L73 | neighbors=[.authenticate(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_74": "Prefer API key auth (stateless, no session expiry).         Falls back to userna" | kind=entity | source=manager/backend/app/vuln/nessus.py:L74 | neighbors=[FindingSeverity, FindingStatus, .authenticate()] | lang=en
- "vuln_nuclei_nucleiscanner_consume_stdout": "._consume_stdout()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L287 | neighbors=[NucleiScanner, ._map_finding(), .run_scan()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-051.json

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
