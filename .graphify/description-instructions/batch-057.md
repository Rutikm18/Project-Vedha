# Node Description Batch 58 of 119

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

- "routers_exploits_get_result_or_404": "_get_result_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L395 | neighbors=[exploits.py, get_exploit_result()]
- "routers_exploits_list_approvals": "list_approvals()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L217 | neighbors=[exploits.py, _approval_out()]
- "routers_exploits_list_exploit_results": "list_exploit_results()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L176 | neighbors=[exploits.py, _result_out()]
- "routers_exploits_load_finding_and_eng": "_load_finding_and_eng()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L368 | neighbors=[exploits.py, run_exploit()]
- "routers_exploits_reject_exploit": "reject_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L302 | neighbors=[exploits.py, _get_approval_or_404()]
- "routers_exploits_run_exploit": "run_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L110 | neighbors=[exploits.py, _load_finding_and_eng()]
- "routers_findings_get_finding": "get_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L200 | neighbors=[findings.py, _tenant_finding()]
- "routers_findings_patch_finding": "patch_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L209 | neighbors=[findings.py, _tenant_finding()]
- "routers_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/routers/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "routers_vuln_scans_nuclei_finding": "_nuclei_finding()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L407 | neighbors=[vuln_scans.py, _run_nuclei_and_save()]
- "routers_vuln_scans_nuclei_terminal_result": "_nuclei_terminal_result()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L430 | neighbors=[vuln_scans.py, _run_nuclei_and_save()]
- "scan_page_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L135 | neighbors=[page.tsx, getToken()]
- "scan_page_gettoken": "getToken()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L110 | neighbors=[page.tsx, apiFetch()]
- "scanner_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L247 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L281 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_probe_redis": "_probe_redis()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L114 | neighbors=[db_scanner.py, interpret_redis_info()]
- "scanner_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L54 | neighbors=[HostDiscoveryScanner, ._probe()]
- "scanner_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L213 | neighbors=[_ConnectSweep, .scan_target()]
- "scanner_mass_scan_connectsweep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L229 | neighbors=[_ConnectSweep, ._probe()]
- "scanner_mass_scan_have_masscan": "_have_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L60 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L184 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=probe/scanner/mass_scan.py:L51 | neighbors=[mass_scan.py, _run_masscan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L205 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L315 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L182 | neighbors=[mcp_ai_scanner.py, ._result()]
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L109 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L154 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L115 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_validated_extra_args": "_validated_extra_args()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L69 | neighbors=[nmap_wrapper.py, Allow tuning only; target, script, and …]
- "scanner_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "scanner_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "scanner_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L36 | neighbors=[PortScanner, .scan_target()]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L65 | neighbors=[PortScanner, ._scan_port()]
- "scanner_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L378 | neighbors=[BaseScanner, RateLimiter]
- "scanner_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L386 | neighbors=[BaseScanner, ._guarded()]
- "scanner_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L280 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…]
- "scanner_scanner_base_parse_ports": "parse_ports()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L292 | neighbors=[scanner_base.py, Parse '22,80,443,8000-8100' into a sort…]
- "scanner_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L190 | neighbors=[.run(), RateLimiter]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L265 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-057.json

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
