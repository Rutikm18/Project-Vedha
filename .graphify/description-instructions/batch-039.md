# Node Description Batch 40 of 104

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

- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L543 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L550 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=probe/tests/test_probe_core.py:L476 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L477 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L484 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L558 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L495 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L496 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L502 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L509 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L534 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L518 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L567 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L526 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L463 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=probe/tests/test_probe_core.py:L779 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_scope_crypt_testkeygeneration": "TestKeyGeneration" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L15 | neighbors=[test_scope_crypt.py, .test_generates_32_byte_keys(), .test_generates_different_keys_each_cal…]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier.]
- "tests_test_task_runner_testrunnerscantypes": "TestRunnerScanTypes" | kind=code-symbol | source=probe/tests/test_task_runner.py:L257 | neighbors=[test_task_runner.py, .test_ot_passive_profile(), .test_web_triage_scan_type()]
- "tests_test_task_runner_testrunnersubmission": "TestRunnerSubmission" | kind=code-symbol | source=probe/tests/test_task_runner.py:L199 | neighbors=[test_task_runner.py, .test_calls_submit_with_result(), .test_uses_spool_when_available()]
- "tests_test_transport_testfetchscope": "TestFetchScope" | kind=code-symbol | source=probe/tests/test_transport.py:L162 | neighbors=[test_transport.py, .test_http_error_returns_none(), .test_returns_scope()]
- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser.]
- "tools_installer_liststatus": "listStatus()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L264 | neighbors=[tools.ts, installer.ts, readInstalled()]
- "tools_installer_writeinstalled": "writeInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L42 | neighbors=[installer.ts, installTool(), removeTool()]
- "tools_issue_license_issue": "issue()" | kind=code-symbol | source=probe/tools/issue_license.py:L48 | neighbors=[issue_license.py, _b64(), main()]
- "tools_issue_license_main": "main()" | kind=code-symbol | source=probe/tools/issue_license.py:L61 | neighbors=[issue_license.py, issue(), keygen()]
- "tools_manifest_tool_manifest": "TOOL_MANIFEST" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L74 | neighbors=[tools.ts, installer.ts, manifest.ts]
- "ui_output_findingdetail": "findingDetail()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L238 | neighbors=[output.ts, ln(), rule()]
- "ui_output_findingline": "findingLine()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L184 | neighbors=[output.ts, ln(), sevBadge()]
- "ui_output_scanheader": "scanHeader()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L63 | neighbors=[output.ts, ln(), rule()]
- "ui_output_stageerror": "stageError()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L133 | neighbors=[output.ts, ln(), w()]
- "ui_output_summary": "summary()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L194 | neighbors=[output.ts, ln(), rule()]
- "ui_output_w": "w()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L29 | neighbors=[output.ts, stageError(), stageProgress()]
- "utils_csv_parser_rationale_26": "Parse CSV text into a list of AssetIn models and error strings." | kind=entity | source=manager/backend/app/utils/csv_parser.py:L26 | neighbors=[AssetCriticality, AssetType, parse_csv_assets()]
- "utils_db": "db.py" | kind=code-symbol | source=manager/backend/app/utils/db.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, get_or_404(), Shared database helpers — single source…]
- "utils_hash": "hash.py" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, dedup_hash(), Shared hashing utilities — deduplicatio…]
- "vuln_enrichment_vulnenrichmentservice_get_kev_catalog": "._get_kev_catalog()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L249 | neighbors=[VulnEnrichmentService, .check_cisa_kev(), .get()]
- "vuln_nessus_nessusscanner_export_nessus_file": ".export_nessus_file()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L257 | neighbors=[NessusScanner, ._get_client(), Request + poll + download .nessus XML f…]
- "vuln_nessus_nessusscanner_launch_scan": ".launch_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L140 | neighbors=[NessusScanner, ._get_client(), Returns scan_uuid (token for tracking).]
- "vuln_nessus_nessusscanner_poll_status": ".poll_status()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L151 | neighbors=[NessusScanner, ._get_client(), Returns {status, progress_percent, host…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-039.json

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
