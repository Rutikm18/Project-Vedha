# Node Description Batch 98 of 336

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
- "main_scripts_findings_finding_row": "_finding_row()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1257 | neighbors=[findings.py, One finding as the finding-section show…, summarize()]
- "main_scripts_findings_is_open": "_is_open()" | kind=code-symbol | source=probe/main_scripts/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "main_scripts_ftp_scanner_banner_software": "banner_software()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L55 | neighbors=[ftp_scanner.py, ._probe(), Best-effort software token from the 220…]
- "main_scripts_ftp_scanner_parse_pasv": "parse_pasv()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L44 | neighbors=[ftp_scanner.py, ._list_bounded(), Extract the passive data PORT from a 22…]
- "main_scripts_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "main_scripts_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "main_scripts_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "main_scripts_ipmi_scanner_build_open_session_request": "build_open_session_request()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L36 | neighbors=[ipmi_scanner.py, ._probe(), A fixed RMCP+ Open Session Request offe…]
- "main_scripts_ipmi_scanner_parse_open_session_response": "parse_open_session_response()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L52 | neighbors=[ipmi_scanner.py, ._probe(), Parse an RMCP+ Open Session Response; N…]
- "main_scripts_ipv6_discovery_is_ipv6": "_is_ipv6()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L34 | neighbors=[ipv6_discovery.py, parse_ip_neigh6(), parse_ndp()]
- "main_scripts_ipv6_discovery_own_ipv6_addresses": "_own_ipv6_addresses()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L80 | neighbors=[ipv6_discovery.py, discover_ipv6_hosts(), Best-effort set of this host's own IPv6…]
- "main_scripts_ipv6_discovery_run": "_run()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L94 | neighbors=[ipv6_discovery.py, _ping_all_nodes(), _read_neighbor_cache()]
- "main_scripts_ja4s_compute_ja4s": "compute_ja4s()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L115 | neighbors=[ja4s.py, ja4s_from_parsed(), Do one standard TLS handshake and compu…]
- "main_scripts_ja4s_ext_types": "_ext_types()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L65 | neighbors=[ja4s.py, _walk_extensions(), ja4s_from_parsed()]
- "main_scripts_ja4s_ja4s_from_serverhello": "ja4s_from_serverhello()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L109 | neighbors=[ja4s.py, ja4s_from_parsed(), JA4S from raw ServerHello record bytes …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-097.json

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
