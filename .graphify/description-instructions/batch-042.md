# Node Description Batch 43 of 119

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

- "routers_exploits_get_exploit_result": "get_exploit_result()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L206 | neighbors=[exploits.py, _get_result_or_404(), _result_out()]
- "routers_findings_sla_summary": "sla_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L44 | neighbors=[findings.py, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…]
- "routers_vuln_scans_finish_cancelled_nuclei_job": "_finish_cancelled_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L517 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "routers_vuln_scans_set_nuclei_job_state": "_set_nuclei_job_state()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L494 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "scanner_db_probemongo": "probeMongo()" | kind=code-symbol | source=probe-go/scanner/db.go:L199 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_probemssql": "probeMSSQL()" | kind=code-symbol | source=probe-go/scanner/db.go:L136 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_probemysql": "probeMysql()" | kind=code-symbol | source=probe-go/scanner/db.go:L73 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_probepostgres": "probePostgres()" | kind=code-symbol | source=probe-go/scanner/db.go:L107 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_proberedis": "probeRedis()" | kind=code-symbol | source=probe-go/scanner/db.go:L176 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "scanner_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "scanner_discover_containsstr": "containsStr()" | kind=code-symbol | source=probe-go/scanner/discover.go:L79 | neighbors=[discover.go, findStr(), isRefused()]
- "scanner_discover_isrefused": "isRefused()" | kind=code-symbol | source=probe-go/scanner/discover.go:L68 | neighbors=[discover.go, containsStr(), probeAlive()]
- "scanner_init": "__init__.py" | kind=code-symbol | source=probe/scanner/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, VA scanner module — pure collection/sca…, 298a9d4 trim frontend to 7 core pages; …]
- "scanner_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "scanner_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L173 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…]
- "scanner_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L151 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…]
- "scanner_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L160 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…]
- "scanner_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L211 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "scanner_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L204 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()]
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L462 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…]
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L341 | neighbors=[.run(), ResultWriter, .to_json()]
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L93 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L141 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "scanner_scopeguard_isallowed": ".isAllowed()" | kind=code-symbol | source=probe-go/scanner/scope.go:L102 | neighbors=[ScopeGuard, .ExpandRequested(), .InScope()]
- "scanner_scopeguard_isexcluded": ".isExcluded()" | kind=code-symbol | source=probe-go/scanner/scope.go:L117 | neighbors=[ScopeGuard, .ExpandRequested(), .InScope()]
- "scanner_scopeguard_networkallowed": ".networkAllowed()" | kind=code-symbol | source=probe-go/scanner/scope.go:L210 | neighbors=[ScopeGuard, .ExpandRequested(), lastIP()]
- "scanner_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from an SMB2 NEGOT…, .scan_target()]
- "scanner_tls_probetls": "ProbeTLS()" | kind=code-symbol | source=probe-go/scanner/tls.go:L23 | neighbors=[tls.go, enumerateWeakCiphers(), parseCert()]
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L83 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "scanner_udp_testsnmpcommunity": "testSNMPCommunity()" | kind=code-symbol | source=probe-go/scanner/udp.go:L199 | neighbors=[udp.go, ProbeAllSNMPCommunities(), buildSNMPGetRequest()]
- "scanner_vulncheck_checkservice": "checkService()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L173 | neighbors=[vulncheck.go, versionLessThan(), Correlate()]
- "scanner_vulncheck_checktls": "checkTLS()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L208 | neighbors=[vulncheck.go, toStrings(), Correlate()]
- "scanner_vulncheck_checkweb": "checkWeb()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L250 | neighbors=[vulncheck.go, toStrings(), Correlate()]
- "scanner_vulncheck_dedupandrank": "dedupAndRank()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L311 | neighbors=[vulncheck.go, Correlate(), severityRank()]
- "scanner_vulncheck_tostrings": "toStrings()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L336 | neighbors=[vulncheck.go, checkTLS(), checkWeb()]
- "scanner_vulncheck_versionlessthan": "versionLessThan()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L364 | neighbors=[vulncheck.go, checkService(), splitVersion()]
- "scanner_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L44 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…]
- "schemas_engagement_rationale_14": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L14 | neighbors=[EngagementStatus, FindingSeverity, validate_scope_entries()]
- "schemas_engagement_validate_scope_entries": "validate_scope_entries()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L13 | neighbors=[engagement.py, .validate_scopes(), Validate and de-duplicate exact IP/CIDR…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-042.json

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
