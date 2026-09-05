# Node Description Batch 106 of 336

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

- "scanner_rdp_scanner_posture_from_selected": "_posture_from_selected()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L76 | neighbors=[rdp_scanner.py, parse_connection_confirm(), Map an RDP selectedProtocol bitmask to …]
- "scanner_rdp_scanner_probe_rdp_posture": "probe_rdp_posture()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L110 | neighbors=[rdp_scanner.py, probe_rdp(), Two-probe RDP posture (MS-RDPBCGR 2.2.1…]
- "scanner_rsync_scanner_parse_modules": "parse_modules()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L37 | neighbors=[rsync_scanner.py, Parse the daemon's module listing into …, ._list_modules()]
- "scanner_run_all_advertised_dynamic_ports": "_advertised_dynamic_ports()" | kind=code-symbol | source=probe/scanner/run_all.py:L98 | neighbors=[run_all.py, main(), EPM-advertised dynamic RPC ports from t…]
- "scanner_run_all_log": "_log()" | kind=code-symbol | source=probe/scanner/run_all.py:L50 | neighbors=[run_all.py, main(), _run_stage()]
- "scanner_scan_funnel_reconcile_ports": "reconcile_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L72 | neighbors=[scan_funnel.py, Canonical open-TCP set for a host = ded…, .run_host()]
- "scanner_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L113 | neighbors=[scan_funnel.py, Protocol, .scan_target()]
- "scanner_scanner_base_assess_tarpit": "assess_tarpit()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L154 | neighbors=[scanner_base.py, Heuristic: is this host a tarpit / hone…, Heuristic: is this host a tarpit / hone…]
- "scanner_scanner_base_choose_source_port": "choose_source_port()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L134 | neighbors=[scanner_base.py, The TCP source port for probes. A FIXED…, The TCP source port for probes. A FIXED…]
- "scanner_scanner_base_get_fd_limit": "get_fd_limit()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1032 | neighbors=[scanner_base.py, raise_fd_limit(), Return (soft, hard) open-file-descripto…]
- "scanner_scanner_base_jittered_delay": "jittered_delay()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L144 | neighbors=[scanner_base.py, A per-probe delay of `base` seconds ± u…, A per-probe delay of `base` seconds ± u…]
- "scanner_scanner_base_probe_payload": "probe_payload()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L127 | neighbors=[scanner_base.py, Benign, non-attributing payload for ICM…, Benign, non-attributing payload for ICM…]
- "scanner_scanner_base_project_file_stamp": "project_file_stamp()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L95 | neighbors=[scanner_base.py, project_now(), Compact project-local stamp for FILE an…]
- "scanner_scanner_base_project_timestamp": "project_timestamp()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L90 | neighbors=[scanner_base.py, project_now(), ISO-8601 instant in the project timezon…]
- "scanner_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L437 | neighbors=[.acquire(), .run(), RateLimiter]
- "scanner_scanner_base_rationale_252": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=probe/scanner/scanner_base.py:L252 | neighbors=[describe_os_error(), ScopeGuard, .window()]
- "scanner_scanner_base_resolve_candidates": "resolve_candidates()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L704 | neighbors=[scanner_base.py, EVERY distinct (family, sockaddr) for `…, resolve_ip_candidates()]
- "scanner_scanner_base_resolve_ip_candidates": "resolve_ip_candidates()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L747 | neighbors=[scanner_base.py, Just the candidate IP strings for `targ…, resolve_candidates()]
- "scanner_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L938 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L929 | neighbors=[.run(), ResultWriter, .to_json()]
- "scanner_scanner_base_safe_connect_concurrency": "safe_connect_concurrency()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1061 | neighbors=[scanner_base.py, Cap concurrent connections comfortably …, raise_fd_limit()]
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L340 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L388 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "scanner_scanner_base_user_agent": "user_agent()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L121 | neighbors=[scanner_base.py, HTTP/RTSP User-Agent to send — a generi…, HTTP/RTSP User-Agent to send — a generi…]
- "scanner_service_banner_parse_http_head": "parse_http_head()" | kind=code-symbol | source=probe/scanner/service_banner.py:L267 | neighbors=[service_banner.py, Pull status code, the identifying heade…, ._grab()]
- "scanner_service_banner_servicebannerscanner_read_some": "._read_some()" | kind=code-symbol | source=probe/scanner/service_banner.py:L348 | neighbors=[Read up to read_bytes: wait `first_wait…, ServiceBannerScanner, ._rung()]
- "scanner_service_enum_smb_dialects": "smb_dialects()" | kind=code-symbol | source=probe/scanner/service_enum.py:L322 | neighbors=[service_enum.py, Negotiate against 445; report whether S…, Negotiate against 445; report whether S…]
- "scanner_service_enum_tls_accepts_old": "tls_accepts_old()" | kind=code-symbol | source=probe/scanner/service_enum.py:L287 | neighbors=[service_enum.py, Which deprecated TLS/SSL versions the s…, Which deprecated TLS/SSL versions the s…]
- "scanner_service_enum_tls_info": "tls_info()" | kind=code-symbol | source=probe/scanner/service_enum.py:L264 | neighbors=[service_enum.py, One permissive TLS handshake: negotiate…, One permissive TLS handshake: negotiate…]
- "scanner_smb_enum_scanner_merge_users": "_merge_users()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L200 | neighbors=[smb_enum_scanner.py, Merge user lists, de-duplicated by (nam…, ._enumerate()]
- "scanner_smb_enum_scanner_parse_rid_ranges": "parse_rid_ranges()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L52 | neighbors=[smb_enum_scanner.py, Parse 'a-b,c-d,e' into a sorted, de-dup…, .__init__()]
- "scanner_smb_enum_scanner_safe": "_safe()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L300 | neighbors=[smb_enum_scanner.py, _decode(), ._enumerate()]
- "scanner_smb_scanner_align8": "_align8()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L249 | neighbors=[smb_scanner.py, Pad to the 8-byte boundary MS-SMB2 requ…, _smb2_negotiate()]
- "scanner_smb_scanner_build_ntlmssp_negotiate": "build_ntlmssp_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L115 | neighbors=[smb_scanner.py, ntlm_os_build(), NTLMSSP NEGOTIATE (Type-1). Sets NEGOTI…]
- "scanner_smb_scanner_der": "_der()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L111 | neighbors=[smb_scanner.py, _der_len(), _spnego_init()]
- "scanner_smb_scanner_encryption_context": "_encryption_context()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L265 | neighbors=[smb_scanner.py, SMB2_ENCRYPTION_CAPABILITIES (MS-SMB2 2…, _smb2_negotiate()]
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L33 | neighbors=[smb_scanner.py, ntlm_os_build(), ._negotiate()]
- "scanner_smb_scanner_preauth_integrity_context": "_preauth_integrity_context()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L254 | neighbors=[smb_scanner.py, SMB2_PREAUTH_INTEGRITY_CAPABILITIES (MS…, _smb2_negotiate()]
- "scanner_smb_scanner_recv_smb_frame": "_recv_smb_frame()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L316 | neighbors=[smb_scanner.py, ntlm_os_build(), Read one length-prefixed (Direct-TCP/NB…]
- "scanner_smb_scanner_smb2_session_setup": "_smb2_session_setup()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L203 | neighbors=[smb_scanner.py, ntlm_os_build(), SMB2 SESSION_SETUP request (MessageId 1…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-105.json

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
