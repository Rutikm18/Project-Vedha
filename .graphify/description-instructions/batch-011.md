# Node Description Batch 12 of 92

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

- "main_scripts_mass_scan_rationale_148": "Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin" | kind=entity | source=main_scripts/mass_scan.py:L148 | neighbors=[_parse_masscan_json(), BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mass_scan_rationale_243": "target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them." | kind=entity | source=main_scripts/mass_scan.py:L243 | neighbors=[run_mass_scan(), BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mass_scan_rationale_308": "Excluded networks -> masscan --exclude specs, so they get ZERO packets." | kind=entity | source=main_scripts/mass_scan.py:L308 | neighbors=[_masscan_excludes(), BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mass_scan_rationale_313": "A CIDR spec is in scope only if it is fully contained in an allowed network." | kind=entity | source=main_scripts/mass_scan.py:L313 | neighbors=[_spec_in_scope(), BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mass_scan_rationale_66": "Run masscan over the given target specs and return its parsed JSON records." | kind=entity | source=main_scripts/mass_scan.py:L66 | neighbors=[_run_masscan(), BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L110 | neighbors=[mcp_ai_scanner.py, .redirect_request(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L298 | neighbors=[OSFingerprintScanner, accept_echo_reply(), build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…] | lang=en
- "main_scripts_port_scanner_rationale_1": "port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD" | kind=entity | source=main_scripts/port_scanner.py:L1 | neighbors=[AdaptiveTimeout, port_scanner.py, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_port_scanner_rationale_131": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=main_scripts/port_scanner.py:L131 | neighbors=[AdaptiveTimeout, resolve_profile(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_port_scanner_rationale_157": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=main_scripts/port_scanner.py:L157 | neighbors=[AdaptiveTimeout, ScanMetrics, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_port_scanner_rationale_185": "Tally exactly one terminal per-port observation." | kind=entity | source=main_scripts/port_scanner.py:L185 | neighbors=[AdaptiveTimeout, .record(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_port_scanner_rationale_204": "Requested ports that were never recorded — the silent-skip proof." | kind=entity | source=main_scripts/port_scanner.py:L204 | neighbors=[AdaptiveTimeout, .missing_ports(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_port_scanner_rationale_211": "Ports recorded more than once (a port must get exactly one verdict)." | kind=entity | source=main_scripts/port_scanner.py:L211 | neighbors=[AdaptiveTimeout, .duplicate_ports(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_port_scanner_rationale_326": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=main_scripts/port_scanner.py:L326 | neighbors=[AdaptiveTimeout, ._attempt(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_port_scanner_rationale_405": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=main_scripts/port_scanner.py:L405 | neighbors=[AdaptiveTimeout, .scan_target(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_port_scanner_rationale_93": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=main_scripts/port_scanner.py:L93 | neighbors=[AdaptiveTimeout, _family_of(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), RDPScanner] | lang=en
- "main_scripts_run_all_main": "main()" | kind=code-symbol | source=main_scripts/run_all.py:L98 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()] | lang=en
- "main_scripts_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L142 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()] | lang=en
- "main_scripts_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()] | lang=en
- "main_scripts_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()] | lang=en
- "main_scripts_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L200 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…] | lang=en
- "main_scripts_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L261 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…] | lang=en
- "main_scripts_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L244 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()] | lang=en
- "main_scripts_udp_scanner_rationale_1": "udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO" | kind=entity | source=main_scripts/udp_scanner.py:L1 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_rationale_114": "SIP OPTIONS request — safe fingerprint method." | kind=entity | source=main_scripts/udp_scanner.py:L114 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, _sip_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_133": "TFTP RRQ for a non-existent file.  Error reply confirms TFTP service." | kind=entity | source=main_scripts/udp_scanner.py:L133 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, _tftp_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_140": "RMCP Ping (ASF Presence Ping) to detect IPMI/BMC." | kind=entity | source=main_scripts/udp_scanner.py:L140 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, _ipmi_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_147": "UPnP/SSDP M-SEARCH — unicast to target:1900." | kind=entity | source=main_scripts/udp_scanner.py:L147 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, _ssdp_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_159": "mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)." | kind=entity | source=main_scripts/udp_scanner.py:L159 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, _mdns_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_189": "Parse IKEv1 or IKEv2 response header." | kind=entity | source=main_scripts/udp_scanner.py:L189 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, interpret_ike()] | lang=en
- "main_scripts_udp_scanner_rationale_205": "Extract SIP version + server header from a SIP response." | kind=entity | source=main_scripts/udp_scanner.py:L205 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, interpret_sip()] | lang=en
- "main_scripts_udp_scanner_rationale_220": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=main_scripts/udp_scanner.py:L220 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, interpret_ipmi()] | lang=en
- "main_scripts_udp_scanner_rationale_233": "Extract Location and Server from SSDP response." | kind=entity | source=main_scripts/udp_scanner.py:L233 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, interpret_ssdp()] | lang=en
- "main_scripts_udp_scanner_rationale_248": "Return byte count and check QR bit (1 = response)." | kind=entity | source=main_scripts/udp_scanner.py:L248 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, interpret_mdns()] | lang=en
- "main_scripts_udp_scanner_rationale_291": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=main_scripts/udp_scanner.py:L291 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, ._gated_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_78": "Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-" | kind=entity | source=main_scripts/udp_scanner.py:L78 | neighbors=[AdaptiveRateController, BaseScanner, ResultWriter, ScanResult, ScopeGuard, _ike_probe()] | lang=fr
- "main_scripts_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=main_scripts/vantage_matrix.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …, test_main_scripts_vantage.py] | lang=en
- "main_scripts_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=main_scripts/web_scanner.py:L55 | neighbors=[web_scanner.py, BaseScanner, ResultWriter, ScanResult, ScopeGuard, .redirect_request()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-011.json

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
