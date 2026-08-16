# Node Description Batch 89 of 209

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

- "lib_severity_epsscolor": "epssColor()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L71 | neighbors=[page.tsx, severity.ts]
- "lib_severity_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L55 | neighbors=[page.tsx, severity.ts]
- "lib_severity_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L43 | neighbors=[page.tsx, severity.ts]
- "lib_severity_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L51 | neighbors=[page.tsx, severity.ts]
- "lib_severity_riskscorecolor": "riskScoreColor()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L63 | neighbors=[page.tsx, severity.ts]
- "lib_severity_sev": "sev()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L122 | neighbors=[severity.ts, toSeverity()]
- "lib_severity_severity_order": "SEVERITY_ORDER" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L114 | neighbors=[LiveOverview.tsx, severity.ts]
- "lib_severity_sevvars": "sevVars()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L127 | neighbors=[Primitives.tsx, severity.ts]
- "lib_severity_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L33 | neighbors=[page.tsx, severity.ts]
- "lib_severity_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L38 | neighbors=[page.tsx, severity.ts]
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
- "main_scripts_adaptive_timeout_adaptivetimeout_timeout": ".timeout()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L44 | neighbors=[AdaptiveTimeout, Current timeout: base until we have a s…]
- "main_scripts_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L247 | neighbors=[DBScanner, ._scan_port()]
- "main_scripts_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L281 | neighbors=[DBScanner, ._scan_port()]
- "main_scripts_db_scanner_probe_redis": "_probe_redis()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L114 | neighbors=[db_scanner.py, interpret_redis_info()]
- "main_scripts_delta_scanner_delta_to_dict": ".to_dict()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L85 | neighbors=[Delta, main()]
- "main_scripts_delta_scanner_deltaengine_summary": ".summary()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L288 | neighbors=[DeltaEngine, main()]
- "main_scripts_findings_finding_to_dict": ".to_dict()" | kind=code-symbol | source=probe/main_scripts/findings.py:L78 | neighbors=[Finding, _main()]
- "main_scripts_findings_tally": "_tally()" | kind=code-symbol | source=probe/main_scripts/findings.py:L660 | neighbors=[findings.py, summarize()]
- "main_scripts_host_discovery_now": "_now()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L290 | neighbors=[host_discovery.py, fuse_liveness()]
- "main_scripts_host_discovery_state_for_confidence": "_state_for_confidence()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L294 | neighbors=[host_discovery.py, fuse_liveness()]
- "main_scripts_host_discovery_vendor_for_mac": "vendor_for_mac()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L136 | neighbors=[host_discovery.py, .scan_target()]
- "main_scripts_init": "__init__.py" | kind=code-symbol | source=probe/main_scripts/__init__.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, VA scanner module — pure collection/sca…]
- "main_scripts_iot_scanner_parse_ssdp_headers": "_parse_ssdp_headers()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L48 | neighbors=[iot_scanner.py, _probe_ssdp_sync()]
- "main_scripts_iot_scanner_probe_mdns_sync": "_probe_mdns_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L189 | neighbors=[iot_scanner.py, _parse_mdns_response()]
- "main_scripts_iot_scanner_probe_rtsp": "_probe_rtsp()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L214 | neighbors=[iot_scanner.py, .scan_target()]
- "main_scripts_ja4s_alpn_code": "_alpn_code()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L78 | neighbors=[ja4s.py, ja4s_from_fields()]
- "main_scripts_ja4s_version_str": "_version_str()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L52 | neighbors=[ja4s.py, ja4s_from_fields()]
- "main_scripts_ja4x_match_suspicious": "match_suspicious()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L117 | neighbors=[ja4x.py, Return a threat-intel label if this JA4…]
- "main_scripts_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L213 | neighbors=[_ConnectSweep, .scan_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-088.json

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
