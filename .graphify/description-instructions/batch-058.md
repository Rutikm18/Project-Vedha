# Node Description Batch 59 of 186

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

- "lib_nmap_parser_extractscripts": "extractScripts()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L39 | neighbors=[nmap-parser.ts, toArray(), parseNmapXml()]
- "lib_nmap_parser_toarray": "toArray()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L34 | neighbors=[nmap-parser.ts, extractScripts(), parseNmapXml()]
- "lib_nuclei_parser_parsenucleiline": "parseNucleiLine()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L35 | neighbors=[tool-runners.ts, nuclei-parser.ts, parsers.test.ts]
- "lib_openvas_client_parseopenvashelperoutput": "parseOpenVASHelperOutput()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L69 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), scanner-adapters.test.ts]
- "lib_openvas_client_settask": "setTask()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L35 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), startOpenVASScan()]
- "lib_openvas_client_startopenvasscan": "startOpenVASScan()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L111 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), setTask()]
- "lib_permissions_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L20 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_isscopeallowed": "isScopeAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L109 | neighbors=[permissions-store.ts, getUser(), read()]
- "lib_permissions_store_removeuser": "removeUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L91 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_updatescopes": "updateScopes()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L100 | neighbors=[permissions-store.ts, read(), write()]
- "lib_scanner_request_validation_isrecord": "isRecord()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L34 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_isvalidhostname": "isValidHostname()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L38 | neighbors=[scanner-request-validation.ts, isValidScannerTarget(), validateHost()]
- "lib_scanner_request_validation_validatehost": "validateHost()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L90 | neighbors=[scanner-request-validation.ts, isValidHostname(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_validatesafestring": "validateSafeString()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L96 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_validatescannertargets": "validateScannerTargets()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L66 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_security_context_publiccverecord": "publicCveRecord()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L18 | neighbors=[security-context.ts, SecurityContextError, resolveSecurityReference()]
- "lib_severity_sev_palette": "SEV_PALETTE" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L78 | neighbors=[page.tsx, severity.ts, page.tsx]
- "lib_target_parser_isvalidtarget": "isValidTarget()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L19 | neighbors=[target-parser.ts, validOctets(), parseTargets()]
- "lib_tenant_resolvetenantsubdomain": "resolveTenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L45 | neighbors=[proxy.ts, tenant.ts, subdomainFromHost()]
- "lib_tenant_subdomainfromhost": "subdomainFromHost()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L22 | neighbors=[tenant.ts, resolveTenantSubdomain(), rootDomain()]
- "lib_testssl_parser_mapseverity": "mapSeverity()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L14 | neighbors=[testssl-parser.ts, parseTestsslJsonChecked(), parseTestsslJson()]
- "lib_whatweb_parser_parsewhatweboutput": "parseWhatWebOutput()" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L12 | neighbors=[tool-runners.ts, whatweb-parser.ts, scanner-adapters.test.ts]
- "login_route_setsessioncookies": "setSessionCookies()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L12 | neighbors=[route.ts, POST(), PUT()]
- "main_scripts_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "main_scripts_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "main_scripts_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L121 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…]
- "main_scripts_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L138 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string.]
- "main_scripts_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L296 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…]
- "main_scripts_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L53 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…]
- "main_scripts_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L308 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…]
- "main_scripts_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L91 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…]
- "main_scripts_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L98 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…]
- "main_scripts_findings_is_open": "_is_open()" | kind=code-symbol | source=probe/main_scripts/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "main_scripts_findings_summarize": "summarize()" | kind=code-symbol | source=probe/main_scripts/findings.py:L648 | neighbors=[findings.py, _main(), _tally()]
- "main_scripts_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L395 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…]
- "main_scripts_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L195 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…]
- "main_scripts_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L111 | neighbors=[host_discovery.py, parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "main_scripts_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L260 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line()]
- "main_scripts_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()]
- "main_scripts_iot_scanner_coap_get_wellknown_core": "_coap_get_wellknown_core()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L346 | neighbors=[iot_scanner.py, _probe_coap_sync(), CoAP Confirmable GET for /.well-known/c…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-058.json

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
