# Node Description Batch 105 of 330

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

- "scanner_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L66 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_build_icmp_timestamp": "build_icmp_timestamp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L70 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_timestamp()] | lang=en
- "scanner_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L162 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()] | lang=en
- "scanner_os_fingerprint_osfingerprintscanner_apply_smb_build": "._apply_smb_build()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L382 | neighbors=[OSFingerprintScanner, ._smb_build(), Fuse an SMB2 NTLM build into an OS resu…] | lang=en
- "scanner_os_fingerprint_osfingerprintscanner_smb_build": "._smb_build()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L370 | neighbors=[OSFingerprintScanner, ._apply_smb_build(), Best-effort exact Windows build via SMB…] | lang=en
- "scanner_os_fingerprint_rationale_205": "p0f-style match on (initial TTL, option layout, window scale) → a specific     s" | kind=entity | source=probe/scanner/os_fingerprint.py:L205 | neighbors=[match_stack_signature(), _open_icmp_socket(), OSFingerprintScanner] | lang=pt
- "scanner_port_scanner_harvest_tcp_stack": "_harvest_tcp_stack()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L94 | neighbors=[port_scanner.py, ._attempt(), Peer TCP-stack signals readable from a …] | lang=en
- "scanner_port_scanner_portscanner_is_ambiguous": "._is_ambiguous()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L569 | neighbors=[PortScanner, .scan_target(), True for the one state a retry can legi…] | lang=en
- "scanner_port_scanner_portscanner_reprobe_ambiguous": "._reprobe_ambiguous()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L574 | neighbors=[PortScanner, .scan_target(), Gentle second look at ports that stayed…] | lang=en
- "scanner_printer_scanner_parse_ipp_make_model": "parse_ipp_make_model()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L65 | neighbors=[printer_scanner.py, ._probe_ipp(), Best-effort extraction of printer-make-…] | lang=en
- "scanner_printer_scanner_parse_pjl_id": "parse_pjl_id()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L38 | neighbors=[printer_scanner.py, ._probe_pjl(), Extract the model string from a PJL INF…] | lang=en
- "scanner_printer_scanner_printerscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L135 | neighbors=[PrinterScanner, ._probe_ipp(), ._probe_pjl()] | lang=en
- "scanner_printer_scanner_recv_bounded": "_recv_bounded()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L83 | neighbors=[printer_scanner.py, ._probe_ipp(), ._probe_pjl()] | lang=en
- "scanner_rdp_scanner_posture_from_selected": "_posture_from_selected()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L76 | neighbors=[rdp_scanner.py, parse_connection_confirm(), Map an RDP selectedProtocol bitmask to …] | lang=en
- "scanner_rdp_scanner_probe_rdp_posture": "probe_rdp_posture()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L110 | neighbors=[rdp_scanner.py, probe_rdp(), Two-probe RDP posture (MS-RDPBCGR 2.2.1…] | lang=en
- "scanner_rsync_scanner_parse_modules": "parse_modules()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L37 | neighbors=[rsync_scanner.py, Parse the daemon's module listing into …, ._list_modules()] | lang=en
- "scanner_run_all_advertised_dynamic_ports": "_advertised_dynamic_ports()" | kind=code-symbol | source=probe/scanner/run_all.py:L98 | neighbors=[run_all.py, main(), EPM-advertised dynamic RPC ports from t…] | lang=en
- "scanner_run_all_log": "_log()" | kind=code-symbol | source=probe/scanner/run_all.py:L50 | neighbors=[run_all.py, main(), _run_stage()] | lang=en
- "scanner_scan_funnel_reconcile_ports": "reconcile_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L72 | neighbors=[scan_funnel.py, Canonical open-TCP set for a host = ded…, .run_host()] | lang=en
- "scanner_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L113 | neighbors=[scan_funnel.py, Protocol, .scan_target()] | lang=en
- "scanner_scanner_base_assess_tarpit": "assess_tarpit()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L154 | neighbors=[scanner_base.py, Heuristic: is this host a tarpit / hone…, Heuristic: is this host a tarpit / hone…] | lang=en
- "scanner_scanner_base_choose_source_port": "choose_source_port()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L134 | neighbors=[scanner_base.py, The TCP source port for probes. A FIXED…, The TCP source port for probes. A FIXED…] | lang=en
- "scanner_scanner_base_get_fd_limit": "get_fd_limit()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1032 | neighbors=[scanner_base.py, raise_fd_limit(), Return (soft, hard) open-file-descripto…] | lang=en
- "scanner_scanner_base_jittered_delay": "jittered_delay()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L144 | neighbors=[scanner_base.py, A per-probe delay of `base` seconds ± u…, A per-probe delay of `base` seconds ± u…] | lang=en
- "scanner_scanner_base_probe_payload": "probe_payload()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L127 | neighbors=[scanner_base.py, Benign, non-attributing payload for ICM…, Benign, non-attributing payload for ICM…] | lang=en
- "scanner_scanner_base_project_file_stamp": "project_file_stamp()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L95 | neighbors=[scanner_base.py, project_now(), Compact project-local stamp for FILE an…] | lang=en
- "scanner_scanner_base_project_timestamp": "project_timestamp()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L90 | neighbors=[scanner_base.py, project_now(), ISO-8601 instant in the project timezon…] | lang=en
- "scanner_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L437 | neighbors=[.acquire(), .run(), RateLimiter] | lang=en
- "scanner_scanner_base_rationale_252": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=probe/scanner/scanner_base.py:L252 | neighbors=[describe_os_error(), ScopeGuard, .window()] | lang=en
- "scanner_scanner_base_resolve_candidates": "resolve_candidates()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L704 | neighbors=[scanner_base.py, EVERY distinct (family, sockaddr) for `…, resolve_ip_candidates()] | lang=en
- "scanner_scanner_base_resolve_ip_candidates": "resolve_ip_candidates()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L747 | neighbors=[scanner_base.py, Just the candidate IP strings for `targ…, resolve_candidates()] | lang=en
- "scanner_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L938 | neighbors=[async_udp_probe(), ResultWriter, run_cli()] | lang=en
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L929 | neighbors=[.run(), ResultWriter, .to_json()] | lang=en
- "scanner_scanner_base_safe_connect_concurrency": "safe_connect_concurrency()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1061 | neighbors=[scanner_base.py, Cap concurrent connections comfortably …, raise_fd_limit()] | lang=en
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L340 | neighbors=[run_cli(), ScopeGuard, ScopeError] | lang=en
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L388 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()] | lang=en
- "scanner_scanner_base_user_agent": "user_agent()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L121 | neighbors=[scanner_base.py, HTTP/RTSP User-Agent to send — a generi…, HTTP/RTSP User-Agent to send — a generi…] | lang=en
- "scanner_service_banner_parse_http_head": "parse_http_head()" | kind=code-symbol | source=probe/scanner/service_banner.py:L267 | neighbors=[service_banner.py, Pull status code, the identifying heade…, ._grab()] | lang=en
- "scanner_service_banner_servicebannerscanner_read_some": "._read_some()" | kind=code-symbol | source=probe/scanner/service_banner.py:L348 | neighbors=[Read up to read_bytes: wait `first_wait…, ServiceBannerScanner, ._rung()] | lang=en
- "scanner_service_enum_smb_dialects": "smb_dialects()" | kind=code-symbol | source=probe/scanner/service_enum.py:L322 | neighbors=[service_enum.py, Negotiate against 445; report whether S…, Negotiate against 445; report whether S…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-104.json

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
