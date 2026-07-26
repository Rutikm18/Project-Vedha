# Node Description Batch 38 of 104

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

- "scanner_discover_containsstr": "containsStr()" | kind=code-symbol | source=probe-go/scanner/discover.go:L79 | neighbors=[discover.go, findStr(), isRefused()] | lang=en
- "scanner_discover_isrefused": "isRefused()" | kind=code-symbol | source=probe-go/scanner/discover.go:L68 | neighbors=[discover.go, containsStr(), probeAlive()] | lang=en
- "scanner_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L32 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…] | lang=en
- "scanner_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L215 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan()] | lang=en
- "scanner_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L89 | neighbors=[mass_scan.py, Parse masscan -oJ output robustly: hand…, _run_masscan()] | lang=en
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L53 | neighbors=[mass_scan.py, Run masscan over the given target specs…, _parse_masscan_json()] | lang=en
- "scanner_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L220 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan()] | lang=en
- "scanner_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L173 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…] | lang=en
- "scanner_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L151 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…] | lang=en
- "scanner_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L160 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L211 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()] | lang=en
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L97 | neighbors=[passive_collector.py, .run(), Open ONE recv-only UDP listener. Return…] | lang=en
- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L64 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …] | lang=en
- "scanner_port": "port.go" | kind=code-symbol | source=probe-go/scanner/port.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, PortRange(), ScanPorts()] | lang=en
- "scanner_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L204 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()] | lang=en
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L462 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…] | lang=en
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L341 | neighbors=[.run(), ResultWriter, .to_json()] | lang=en
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L93 | neighbors=[run_cli(), ScopeGuard, ScopeError] | lang=en
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L141 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()] | lang=en
- "scanner_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe-go/scanner/scope.go:L12 | neighbors=[scope.go, .ExpandCIDRs(), .InScope()] | lang=en
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L107 | neighbors=[SMBScanner, _smb1_negotiate(), _smb2_negotiate()] | lang=en
- "scanner_tls_probetls": "ProbeTLS()" | kind=code-symbol | source=probe-go/scanner/tls.go:L23 | neighbors=[tls.go, enumerateWeakCiphers(), parseCert()] | lang=en
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L83 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()] | lang=en
- "scanner_udp_testsnmpcommunity": "testSNMPCommunity()" | kind=code-symbol | source=probe-go/scanner/udp.go:L199 | neighbors=[udp.go, ProbeAllSNMPCommunities(), buildSNMPGetRequest()] | lang=en
- "scanner_vulncheck_checkservice": "checkService()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L173 | neighbors=[vulncheck.go, versionLessThan(), Correlate()] | lang=en
- "scanner_vulncheck_checktls": "checkTLS()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L208 | neighbors=[vulncheck.go, toStrings(), Correlate()] | lang=en
- "scanner_vulncheck_checkweb": "checkWeb()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L250 | neighbors=[vulncheck.go, toStrings(), Correlate()] | lang=en
- "scanner_vulncheck_dedupandrank": "dedupAndRank()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L311 | neighbors=[vulncheck.go, Correlate(), severityRank()] | lang=en
- "scanner_vulncheck_tostrings": "toStrings()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L336 | neighbors=[vulncheck.go, checkTLS(), checkWeb()] | lang=en
- "scanner_vulncheck_versionlessthan": "versionLessThan()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L364 | neighbors=[vulncheck.go, checkService(), splitVersion()] | lang=en
- "scanner_web": "web.go" | kind=code-symbol | source=probe-go/scanner/web.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, detectTech(), ProbeHTTP()] | lang=en
- "services_job_result_service_process_job_result": "process_job_result()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L27 | neighbors=[job_result_service.py, _promote_assets(), Process a scan job result.  Called from…] | lang=en
- "services_job_result_service_promote_assets": "_promote_assets()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L135 | neighbors=[job_result_service.py, process_job_result(), Upsert discovered hosts/services into t…] | lang=en
- "services_scope_crypto_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L34 | neighbors=[scope_crypto.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…] | lang=en
- "services_scope_crypto_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L77 | neighbors=[scope_crypto.py, encrypt_scope(), Convenience: dict → JSON → encrypt → ba…] | lang=en
- "services_sla_rationale_1": "SLA policy engine.  Turns a severity + \"first seen\" timestamp into a remediation" | kind=entity | source=manager/backend/app/services/sla.py:L1 | neighbors=[FindingStatus, Finding, sla.py] | lang=pt
- "services_sla_rationale_101": "Aggregate SLA states across a set of findings.      Returns counts per state plu" | kind=entity | source=manager/backend/app/services/sla.py:L101 | neighbors=[FindingStatus, Finding, summarize()] | lang=en
- "services_sla_rationale_61": "Compute the SLA state for one finding. Never raises on missing data." | kind=entity | source=manager/backend/app/services/sla.py:L61 | neighbors=[FindingStatus, Finding, compute()] | lang=en
- "services_sla_summarize": "summarize()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L100 | neighbors=[sla.py, Aggregate SLA states across a set of fi…, compute()] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_computers_flags_dc": ".test_get_computers_flags_dc()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L132 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-037.json

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
