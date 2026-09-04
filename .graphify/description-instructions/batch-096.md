# Node Description Batch 97 of 332

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

- "lib_openvas_client_startopenvasscan": "startOpenVASScan()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L111 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), setTask()]
- "lib_permissions_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L20 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_isscopeallowed": "isScopeAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L109 | neighbors=[permissions-store.ts, getUser(), read()]
- "lib_permissions_store_removeuser": "removeUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L91 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_updatescopes": "updateScopes()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L100 | neighbors=[permissions-store.ts, read(), write()]
- "lib_portal_client_grade_var": "GRADE_VAR" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L135 | neighbors=[portal-client.ts, page.tsx, page.tsx]
- "lib_portal_client_portalscan": "PortalScan" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L76 | neighbors=[portal-client.ts, page.tsx, page.tsx]
- "lib_portal_client_portalsummary": "PortalSummary" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L101 | neighbors=[portal-client.ts, page.tsx, page.tsx]
- "lib_portal_client_portaltrends": "PortalTrends" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L110 | neighbors=[portal-client.ts, page.tsx, page.tsx]
- "lib_portal_client_severitychip": "severityChip()" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L126 | neighbors=[page.tsx, portal-client.ts, page.tsx]
- "lib_scanner_request_validation_isrecord": "isRecord()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L34 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_isvalidhostname": "isValidHostname()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L38 | neighbors=[scanner-request-validation.ts, isValidScannerTarget(), validateHost()]
- "lib_scanner_request_validation_validatehost": "validateHost()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L90 | neighbors=[scanner-request-validation.ts, isValidHostname(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_validatesafestring": "validateSafeString()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L96 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_validatescannertargets": "validateScannerTargets()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L66 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_security_context_publiccverecord": "publicCveRecord()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L18 | neighbors=[security-context.ts, SecurityContextError, resolveSecurityReference()]
- "lib_severity_riskscorecolor": "riskScoreColor()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L64 | neighbors=[page.tsx, severity.ts, page.tsx]
- "lib_severity_sev_palette": "SEV_PALETTE" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L79 | neighbors=[page.tsx, severity.ts, page.tsx]
- "lib_severity_severity_order": "SEVERITY_ORDER" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L115 | neighbors=[LiveOverview.tsx, severity.ts, page.tsx]
- "lib_target_parser_isvalidtarget": "isValidTarget()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L19 | neighbors=[target-parser.ts, validOctets(), parseTargets()]
- "lib_tenant_resolvetenantsubdomain": "resolveTenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L45 | neighbors=[proxy.ts, tenant.ts, subdomainFromHost()]
- "lib_tenant_subdomainfromhost": "subdomainFromHost()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L22 | neighbors=[tenant.ts, resolveTenantSubdomain(), rootDomain()]
- "lib_testssl_parser_mapseverity": "mapSeverity()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L14 | neighbors=[testssl-parser.ts, parseTestsslJsonChecked(), parseTestsslJson()]
- "lib_whatweb_parser_parsewhatweboutput": "parseWhatWebOutput()" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L12 | neighbors=[tool-runners.ts, whatweb-parser.ts, scanner-adapters.test.ts]
- "login_route_isclienttoken": "isClientToken()" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L49 | neighbors=[route.ts, POST(), PUT()]
- "login_route_setportalcookies": "setPortalCookies()" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L27 | neighbors=[route.ts, POST(), PUT()]
- "login_route_setsessioncookies": "setSessionCookies()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L12 | neighbors=[route.ts, POST(), PUT()]
- "main_scripts_accuracy_gate_check_thresholds": "check_thresholds()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L105 | neighbors=[accuracy_gate.py, Threshold violations for one scored cor…, run_gate()]
- "main_scripts_accuracy_gate_is_independent": "is_independent()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L100 | neighbors=[accuracy_gate.py, True when this corpus's labels can supp…, run_gate()]
- "main_scripts_accuracy_gate_main": "_main()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L204 | neighbors=[accuracy_gate.py, format_gate_report(), run_gate()]
- "main_scripts_accuracy_main": "_main()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "main_scripts_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "main_scripts_accuracy_ratio": "_ratio()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "main_scripts_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "main_scripts_cpe_extract_version": "_extract_version()" | kind=code-symbol | source=probe/main_scripts/cpe.py:L103 | neighbors=[cpe.py, Prefer an explicit version field; else …, to_cpe()]
- "main_scripts_cpe_to_cpe": "to_cpe()" | kind=code-symbol | source=probe/main_scripts/cpe.py:L116 | neighbors=[cpe.py, Return {vendor, product, version, cpe23…, _extract_version()]
- "main_scripts_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "main_scripts_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "main_scripts_dns_scanner_derive_zones": "derive_zones()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L55 | neighbors=[dns_scanner.py, ._probe(), Candidate zone names to try AXFR / DNSS…]
- "main_scripts_dns_scanner_dnsscanner_axfr": "._axfr()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L139 | neighbors=[DNSScanner, ._probe(), Attempt a zone transfer, reading increm…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-096.json

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
