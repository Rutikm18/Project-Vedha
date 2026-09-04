# Node Description Batch 45 of 332

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

- "lib_errors_adversaerror": "AdversaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, .constructor(), .render(), .toJSON(), diagnoseSpawnError()]
- "lib_errors_vedhaerror": "VedhaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, diagnoseSpawnError(), .constructor(), .render(), .toJSON()]
- "lib_findings_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L22 | neighbors=[findings-store.ts, deleteFinding(), getAllFindings(), saveFindings(), updateFinding(), updateFindingStatus()]
- "lib_graph_store_graphstore": "graphStore" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L329 | neighbors=[route.ts, route.ts, route.ts, route.ts, graph-store.ts, route.ts]
- "lib_httpx_parser_parsehttpxjsonline": "parseHttpxJsonLine()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L41 | neighbors=[httpx-parser.ts, .decode(), isOptionalNumber(), isOptionalString(), normalizePort(), parsers.test.ts]
- "lib_netexec_parser": "netexec-parser.ts" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), scanner-adapters.test.ts]
- "lib_scan_events": "scan-events.ts" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, broadcastToScan(), Callback, scanListeners, subscribeScan(), 298a9d4 trim frontend to 7 core pages; …]
- "lib_scanner_request_validation_validateopenvasscanrequest": "validateOpenVASScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L112 | neighbors=[scanner-request-validation.ts, isRecord(), validateHost(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts]
- "lib_security_context_resolvesecurityreference": "resolveSecurityReference()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L37 | neighbors=[route.ts, route.ts, route.ts, security-context.ts, publicCveRecord(), SecurityContextError]
- "lib_severity_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L8 | neighbors=[Primitives.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx, severity.ts, page.tsx]
- "lib_testssl_parser_parsetestssljson": "parseTestsslJson()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L44 | neighbors=[testssl-parser.ts, parseTestsslJsonChecked(), parseTestsslOutput(), parsers.test.ts, tool-runners.ts, mapSeverity()]
- "lib_whatweb_parser": "whatweb-parser.ts" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, parseWhatWebOutput(), WhatWebParseResult, WhatWebResult, scanner-adapters.test.ts]
- "logout_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/logout/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, POST(), 2885afa Add comprehensive probe testing…]
- "main_scripts_accuracy_gate_run_gate": "run_gate()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L141 | neighbors=[accuracy_gate.py, _main(), Score every corpus in `directory` and c…, check_thresholds(), is_independent(), load_corpora()]
- "main_scripts_accuracy_score_findings": "score_findings()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L48 | neighbors=[accuracy.py, evaluate_corpus(), Precision / recall / F1 of produced fin…, _expected_keys(), _finding_key(), _ratio()]
- "main_scripts_cpe": "cpe.py" | kind=code-symbol | source=probe/main_scripts/cpe.py:L1 | neighbors=[6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _extract_version(), to_cpe(), cpe.py — derive a CPE 2.3 identity from…]
- "main_scripts_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "main_scripts_delta_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L319 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "main_scripts_dns_scanner": "dns_scanner.py" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, derive_zones(), DNSScanner, _is_ip(), main(), dns_scanner.py — DNS server hygiene: zo…]
- "main_scripts_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/main_scripts/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "main_scripts_findings_load_facts_jsonl": "load_facts_jsonl()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1319 | neighbors=[findings.py, _main(), Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Anonymous SMB (null-session) informatio…]
- "main_scripts_findings_rule_dns": "_rule_dns()" | kind=code-symbol | source=probe/main_scripts/findings.py:L707 | neighbors=[findings.py, DNS server hygiene: a full AXFR zone tr…, _data(), Finding, _scanner(), DNS server hygiene: a full AXFR zone tr…]
- "main_scripts_findings_rule_ftp": "_rule_ftp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L794 | neighbors=[findings.py, Confirmed FTP anonymous access (upgrade…, _data(), Finding, _scanner(), Confirmed FTP anonymous access (upgrade…]
- "main_scripts_findings_rule_ipmi": "_rule_ipmi()" | kind=code-symbol | source=probe/main_scripts/findings.py:L892 | neighbors=[findings.py, IPMI/BMC exposure. Cipher-zero is a cri…, _data(), Finding, _scanner(), IPMI/BMC exposure. Cipher-zero is a cri…]
- "main_scripts_findings_rule_ldap": "_rule_ldap()" | kind=code-symbol | source=probe/main_scripts/findings.py:L669 | neighbors=[findings.py, Anonymous LDAP exposure. An anonymous R…, _data(), Finding, _scanner(), Anonymous LDAP exposure. An anonymous R…]
- "main_scripts_findings_rule_msrpc": "_rule_msrpc()" | kind=code-symbol | source=probe/main_scripts/findings.py:L958 | neighbors=[findings.py, Windows RPC endpoint-mapper disclosure …, _data(), Finding, _scanner(), Windows RPC endpoint-mapper disclosure …]
- "main_scripts_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=probe/main_scripts/findings.py:L757 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner(), NFS anonymous export exposure. A world-…]
- "main_scripts_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=probe/main_scripts/findings.py:L985 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner(), Exposed network printer — an informatio…]
- "main_scripts_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L535 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner(), Confirmed RDP (X.224 handshake) + NLA d…]
- "main_scripts_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=probe/main_scripts/findings.py:L823 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner(), rsync daemon exposure. Anonymously-sele…]
- "main_scripts_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=probe/main_scripts/findings.py:L618 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner(), Anonymous SMB (null-session) informatio…]
- "main_scripts_findings_rule_smtp": "_rule_smtp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L924 | neighbors=[findings.py, SMTP hygiene: VRFY/EXPN user enumeratio…, _data(), Finding, _scanner(), SMTP hygiene: VRFY/EXPN user enumeratio…]
- "main_scripts_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L467 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner(), JA4X-based threat-intel match. Fires on…]
- "main_scripts_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L515 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner(), JA4S-based threat-intel match on the TL…]
- "main_scripts_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=probe/main_scripts/findings.py:L489 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner(), Proven UNAUTHENTICATED access to a data…]
- "main_scripts_findings_rule_vnc": "_rule_vnc()" | kind=code-symbol | source=probe/main_scripts/findings.py:L861 | neighbors=[findings.py, VNC/RFB authentication exposure. 'None'…, _data(), Finding, _scanner(), VNC/RFB authentication exposure. 'None'…]
- "main_scripts_ftp_scanner": "ftp_scanner.py" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, banner_software(), FTPScanner, main(), parse_pasv(), ftp_scanner.py — FTP anonymous-access c…]
- "main_scripts_ftp_scanner_ftpscanner_list_bounded": "._list_bounded()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L128 | neighbors=[FTPScanner, ._cmd(), ._read_response(), parse_pasv(), ._probe(), Confirm anonymous READ via PASV + LIST,…]
- "main_scripts_ftp_scanner_ftpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L95 | neighbors=[FTPScanner, banner_software(), ._cmd(), ._list_bounded(), ._read_response(), Blocking: greeting → anonymous login → …]
- "main_scripts_ipmi_scanner": "ipmi_scanner.py" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_open_session_request(), IPMIScanner, main(), parse_open_session_response(), ipmi_scanner.py — IPMI 2.0 cipher-zero …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-044.json

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
