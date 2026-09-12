# Node Description Batch 150 of 380

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

- "lib_portal_client_portalreport": "PortalReport" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L83 | neighbors=[portal-client.ts, page.tsx]
- "lib_portal_client_portalusecase": "PortalUseCase" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L105 | neighbors=[portal-client.ts, page.tsx]
- "lib_portal_client_severity_style": "SEVERITY_STYLE" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L81 | neighbors=[page.tsx, portal-client.ts]
- "lib_reports_workspace_api_createreportsworkspaceapi": "createReportsWorkspaceApi()" | kind=code-symbol | source=manager/frontend/lib/reports-workspace-api.ts:L55 | neighbors=[reports-workspace-api.ts, page.tsx]
- "lib_reports_workspace_api_reportsworkspacesurface": "ReportsWorkspaceSurface" | kind=code-symbol | source=manager/frontend/lib/reports-workspace-api.ts:L5 | neighbors=[reports-workspace-api.ts, page.tsx]
- "lib_scanner_request_validation_isvalidscannertarget": "isValidScannerTarget()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L46 | neighbors=[scanner-request-validation.ts, isValidHostname()]
- "lib_settings_workspace_api_createsettingsworkspaceapi": "createSettingsWorkspaceApi()" | kind=code-symbol | source=manager/frontend/lib/settings-workspace-api.ts:L6 | neighbors=[settings-workspace-api.ts, page.tsx]
- "lib_settings_workspace_api_settingsworkspacesurface": "SettingsWorkspaceSurface" | kind=code-symbol | source=manager/frontend/lib/settings-workspace-api.ts:L4 | neighbors=[settings-workspace-api.ts, page.tsx]
- "lib_severity_coverage_color": "COVERAGE_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L44 | neighbors=[page.tsx, severity.ts]
- "lib_severity_epsscolor": "epssColor()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L72 | neighbors=[page.tsx, severity.ts]
- "lib_severity_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L56 | neighbors=[page.tsx, severity.ts]
- "lib_severity_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L40 | neighbors=[page.tsx, severity.ts]
- "lib_severity_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L48 | neighbors=[page.tsx, severity.ts]
- "lib_severity_priority_label": "PRIORITY_LABEL" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L52 | neighbors=[page.tsx, severity.ts]
- "lib_severity_sev": "sev()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L123 | neighbors=[severity.ts, toSeverity()]
- "lib_severity_sevvars": "sevVars()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L128 | neighbors=[Primitives.tsx, severity.ts]
- "lib_severity_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L28 | neighbors=[page.tsx, severity.ts]
- "lib_severity_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L35 | neighbors=[page.tsx, severity.ts]
- "lib_target_parser_estimatehostcount": "estimateHostCount()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L40 | neighbors=[target-parser.ts, parseTargets()]
- "lib_target_parser_validoctets": "validOctets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L12 | neighbors=[target-parser.ts, isValidTarget()]
- "lib_tenant_rootdomain": "rootDomain()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L17 | neighbors=[tenant.ts, subdomainFromHost()]
- "lib_tenant_server_clientfromrequest": "clientFromRequest()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L16 | neighbors=[tenant-server.ts, readTenantSubdomain()]
- "lib_tenant_server_currentclient": "currentClient()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L26 | neighbors=[tenant-server.ts, tenantSubdomain()]
- "lib_tenant_server_readtenantsubdomain": "readTenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L12 | neighbors=[tenant-server.ts, clientFromRequest()]
- "lib_tenant_server_tenantsubdomain": "tenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L21 | neighbors=[tenant-server.ts, currentClient()]
- "lib_testssl_parser_parsetestssloutput": "parseTestsslOutput()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L34 | neighbors=[testssl-parser.ts, parseTestsslJson()]
- "main_scripts_accuracy_expected_keys": "_expected_keys()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L37 | neighbors=[accuracy.py, score_findings()]
- "main_scripts_accuracy_finding_key": "_finding_key()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L31 | neighbors=[accuracy.py, score_findings()]
- "main_scripts_accuracy_format_report": "format_report()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L145 | neighbors=[accuracy.py, _main()]
- "main_scripts_accuracy_gate_format_gate_report": "format_gate_report()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L175 | neighbors=[accuracy_gate.py, _main()]
- "main_scripts_adaptive_timeout_adaptivetimeout_timeout": ".timeout()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L44 | neighbors=[AdaptiveTimeout, Current timeout: base until we have a s…]
- "main_scripts_db_scanner_build_tds_prelogin": "_build_tds_prelogin()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L130 | neighbors=[db_scanner.py, A well-formed PRELOGIN request (MS-TDS …]
- "main_scripts_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L463 | neighbors=[DBScanner, ._scan_port()]
- "main_scripts_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L498 | neighbors=[DBScanner, ._scan_port()]
- "main_scripts_db_scanner_probe_mssql": "_probe_mssql()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L214 | neighbors=[db_scanner.py, parse_tds_prelogin()]
- "main_scripts_db_scanner_probe_mysql": "_probe_mysql()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L88 | neighbors=[db_scanner.py, parse_mysql_greeting()]
- "main_scripts_db_scanner_probe_redis": "_probe_redis()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L241 | neighbors=[db_scanner.py, interpret_redis_info()]
- "main_scripts_delta_scanner_delta_to_dict": ".to_dict()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L87 | neighbors=[Delta, main()]
- "main_scripts_delta_scanner_deltaengine_summary": ".summary()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L290 | neighbors=[DeltaEngine, main()]
- "main_scripts_dns_scanner_dnsscanner_chaos_txt": "._chaos_txt()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L98 | neighbors=[DNSScanner, ._probe()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-149.json

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
