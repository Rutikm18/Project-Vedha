# Graph Report - .  (2026-08-27)

## Corpus Check
- 203 files · ~217,232 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3676 nodes · 6776 edges · 282 communities detected
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 1516 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 1516 · contains: 1413 · calls: 1353 · rationale_for: 1048 · method: 1046 · MODIFIES: 216 · imports_from: 122 · inherits: 50 · ON_BRANCH: 7 · PARENT_OF: 4 · imports: 1


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 203 · Candidates: 377
- Excluded: 499 untracked · 5533 ignored · 0 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `a1430fb`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `ScanResult` - 268 edges
2. `ScopeGuard` - 244 edges
3. `ResultWriter` - 206 edges
4. `BaseScanner` - 169 edges
5. `SynScanner` - 61 edges
6. `MCPAIScanner` - 57 edges
7. `UDPScanner` - 57 edges
8. `DBScanner` - 56 edges
9. `SMBScanner` - 55 edges
10. `TLSScanner` - 55 edges

## Surprising Connections (you probably didn't know these)
- `local_run.py — run the probe's REAL pipeline (workflow.run_engagement) directly` --uses--> `ScopeGuard`  [INFERRED]
  agent/local_run.py → main_scripts/scanner_base.py
- `Actionable input error on stderr → exit code 2. No traceback: this is     operat` --uses--> `ScopeGuard`  [INFERRED]
  agent/local_run.py → main_scripts/scanner_base.py
- `Synchronous entrypoint for the `local-run` CLI subcommand.` --uses--> `ScopeGuard`  [INFERRED]
  agent/local_run.py → main_scripts/scanner_base.py
- `Resolve the port set from PROBE_LOCAL_PORTS.        unset      → [22, 80, 443]` --uses--> `ScopeGuard`  [INFERRED]
  agent/local_run.py → main_scripts/scanner_base.py
- `Drop internal bookkeeping keys (_collected_at, _via…) for readable output.` --uses--> `ScopeGuard`  [INFERRED]
  agent/local_run.py → main_scripts/scanner_base.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (93): engine.py — adapt a manager scan job to scanner_module's workflow engine and ret, AdaptiveTimeout, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act, IoTScanner, iot_scanner.py — IoT / embedded device fingerprint and exposure scanner.  Covers, Decode a DNS wire-format name, following pointers.  Returns (name, end_offset). (+85 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (60): agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit, task_runner.py — orchestrates the full lifecycle of a single scan job.  Given a, use_cases.py — the finite, pre-defined library of scan scenarios the manager can, feat/wire-osfp-service-enum, main, 56508b2 Add unit tests for XML parsing, address-family selection, tarpit detection, wire identity, and local probe execution, a1430fb Add local_run.py for direct probe execution and verify_windows_ground_truth.ps1 for cross-checking scan results, a548359 feat(auto-enrollment): implement trust-on-first-use for probe enrollment- Added settings for automatic probe enrollment and CIDR policies.- Enhanced probe enrollment logic to support auto-approval for trusted networks.- Updated deployment scripts and documentation to reflect new auto-enrollment features.- Introduced tests to validate default settings and CIDR parsing for auto-enrollment. (+52 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (59): BaseScanner, DBScanner, HostDiscoveryScanner, MCPAIScanner, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive() (+51 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (24): _atomic_write_private_state(), _enrollment_conflict_detail(), transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, True if we have both an agent_id and a token for API calls., Merge and atomically persist private state while preserving fields., Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed). (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (16): fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), scope_validator.py — defense-in-depth scope re-validation for the probe.  The pr, Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)., Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Parse one IP, CIDR, or inclusive IP range into covering networks.      ``None``, Fetch the engagement's authoritative scope from the manager.      Args: (+8 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (29): _ike_probe(), interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats(), interpret_ntp_monlist(), interpret_sip() (+21 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (18): Asset, _parse_ts(), PortFact, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (42): _ids(), test_main_scripts_findings.py — the findings interpretation layer.  Pure-logic,, _run(), test_accepts_scanresult_objects_not_just_dicts(), test_all_security_headers_present_no_finding(), test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_double_report(), test_confirmed_ftp_cleartext_is_high_confidence() (+34 more)

### Community 8 - "Community 8"
Cohesion: 0.14
Nodes (33): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+25 more)

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (37): _check_anti_debug(), _is_local_manager_url(), _load_env(), _load_or_create_signing_identity(), _poll_jobs_or_empty(), Load or atomically create the probe's Ed25519 enrollment identity., Request UI approval, poll, prove key possession, and activate., One-line, transparent summary of what a scan actually found so the operator (+29 more)

### Community 10 - "Community 10"
Cohesion: 0.07
Nodes (13): DBScanner, interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act, FakeReader, FakeWriter, _probe() (+5 more)

### Community 11 - "Community 11"
Cohesion: 0.05
Nodes (5): result_spool.py — local result persistence with upload retry.  When the probe co, Tests for agent/result_spool.py, ResultSpool with tiny retry delay for fast tests., spool(), TestResultSpool

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (30): accept_echo_reply(), build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), fingerprint_os(), hop_estimate(), _icmp(), icmp_supported() (+22 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (27): _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _decode_oid(), _decode_value(), _encode_oid() (+19 more)

### Community 14 - "Community 14"
Cohesion: 0.07
Nodes (29): classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology(), main(), mdns_hostname(), _nb_encode() (+21 more)

### Community 15 - "Community 15"
Cohesion: 0.08
Nodes (25): device_hint(), fuse_liveness(), HostDiscoveryScanner, is_locally_administered(), Neighbor, normalize_mac(), _now(), parse_neighbor_line() (+17 more)

### Community 16 - "Community 16"
Cohesion: 0.07
Nodes (29): classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology(), main(), mdns_hostname(), _nb_encode() (+21 more)

### Community 17 - "Community 17"
Cohesion: 0.11
Nodes (34): _data(), Finding, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only, Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e (+26 more)

### Community 18 - "Community 18"
Cohesion: 0.09
Nodes (28): accept_echo_reply(), build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), fingerprint_os(), hop_estimate(), _icmp(), infer_initial_ttl() (+20 more)

### Community 19 - "Community 19"
Cohesion: 0.11
Nodes (34): _data(), Finding, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only, Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e (+26 more)

### Community 20 - "Community 20"
Cohesion: 0.09
Nodes (23): build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip(), _parse_mss(), parse_packet(), syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).  WH (+15 more)

### Community 21 - "Community 21"
Cohesion: 0.07
Nodes (4): _ConcurrencyScanner, _ExplodingScanner, test_host_fanout_is_bounded(), test_per_target_exception_preserves_other_results()

### Community 22 - "Community 22"
Cohesion: 0.10
Nodes (19): _metric(), _not_scored(), Pure helpers for controlled Probe capability and accuracy validation., Validate the small, explicit inventory used for accuracy scoring., Score promoted inventory against explicit host/port/service/CVE truth., Resolve suites plus explicit use-cases, preserving first-seen order., Require every IP/CIDR target to be fully allowed and not excluded., Return the conservative number of addresses represented by targets. (+11 more)

### Community 23 - "Community 23"
Cohesion: 0.11
Nodes (22): VA scanner module — pure collection/scanning layer.  Each submodule is an indepe, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed() (+14 more)

### Community 24 - "Community 24"
Cohesion: 0.10
Nodes (26): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response() (+18 more)

### Community 25 - "Community 25"
Cohesion: 0.11
Nodes (24): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+16 more)

### Community 26 - "Community 26"
Cohesion: 0.07
Nodes (10): test_syn_scanner.py — stateless SYN scan (Tier 1.1).  The raw-socket send/receiv, A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)., _synack_with_options(), TestAdaptiveTimeoutToggle, TestCapabilityDetection, TestChecksum, TestClassify, TestParsePacketSignals (+2 more)

### Community 27 - "Community 27"
Cohesion: 0.08
Nodes (23): assess_tarpit(), bracket_host(), choose_source_port(), classify_os_error(), describe_os_error(), inet_checksum(), jittered_delay(), parse_ports() (+15 more)

### Community 28 - "Community 28"
Cohesion: 0.11
Nodes (8): FakeDiscovery, FakePortScanner, _make_funnel(), Build a funnel with fakes; return (funnel, discovery, port_scanner, created)., _scope(), TestBuildDefaultFunnel, TestScanFunnel, TestScanFunnelRun

### Community 29 - "Community 29"
Cohesion: 0.14
Nodes (12): Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result., Move a terminally rejected result out of the retry queue., Attempt to upload a result with retries and local spool as fallback.          Ar, Re-attempt upload of all previously spooled results.          Called once at pro, Number of pending (unsubmitted) results in the spool., Total bytes held by pending result files, ignoring vanished files., Whether new jobs must pause until pending results are uploaded.          These a (+4 more)

### Community 30 - "Community 30"
Cohesion: 0.12
Nodes (20): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+12 more)

### Community 31 - "Community 31"
Cohesion: 0.11
Nodes (21): device_hint(), fuse_liveness(), is_locally_administered(), Neighbor, normalize_mac(), _now(), parse_neighbor_line(), host_discovery.py — determine which hosts are alive, with graded confidence.  ME (+13 more)

### Community 32 - "Community 32"
Cohesion: 0.12
Nodes (20): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+12 more)

### Community 33 - "Community 33"
Cohesion: 0.08
Nodes (10): test_wire_identity.py — the scanner must NOT sign its own packets.  A brand stri, Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs., Evasion: blur a fixed scan cadence with a bounded random per-probe delay., Import-time probe constants built from user_agent() must be signature-free., TestChooseSourcePort, TestEvasionFlags, TestJitteredDelay, TestModuleConstantsUnbranded (+2 more)

### Community 34 - "Community 34"
Cohesion: 0.12
Nodes (15): _ike_probe(), interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats(), interpret_ntp_monlist(), interpret_sip() (+7 more)

### Community 35 - "Community 35"
Cohesion: 0.25
Nodes (22): _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device(), _flush_spool_over_http(), _job_intent(), _load_or_create_identity(), main() (+14 more)

### Community 36 - "Community 36"
Cohesion: 0.13
Nodes (11): make_smb2_error(), make_smb2_success(), test_main_scripts_hardening.py — verifies the Phase-1 correctness fixes applied, A 64-byte SMB2 header. Caller prepends a 4-byte NBT transport prefix, so     Pro, STATUS_INVALID_PARAMETER error response: same header, body StructureSize 9,, _run(), _scope(), _smb2_header() (+3 more)

### Community 37 - "Community 37"
Cohesion: 0.11
Nodes (15): _Socket, test_collector_raises_when_no_listener_binds(), test_ot_udp_backend_never_joins_or_transmits(), test_subset_listener_failure_reports_degraded_coverage(), _Writer, classify_scanner_error(), engine_manifest(), ErrorDetail (+7 more)

### Community 38 - "Community 38"
Cohesion: 0.11
Nodes (7): _cache_with(), test_probe_next_features.py — the probe_next plan: run the improved main_scripts, test_device_inventory_post_stage_classifies_from_open_ports(), test_device_inventory_skips_hosts_without_evidence(), test_exposure_matrix_flags_internet_reachable_ports(), test_exposure_matrix_internal_only_from_lan_vantage(), test_no_post_stage_for_ordinary_scan_types()

### Community 39 - "Community 39"
Cohesion: 0.10
Nodes (10): _family_of(), PortScanner, Per-target scan accounting — the completeness + self-health record.      It lets, Tally exactly one terminal per-port observation., Requested ports that were never recorded — the silent-skip proof., Ports recorded more than once (a port must get exactly one verdict)., One connect() and its classification. Always returns a ScanResult         (open, Bounded worker-pool scan of every requested port.          A fixed pool of `conc (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.16
Nodes (4): _asset(), TestAssetNeedsRecheckLive, TestGate5, TestGate6

### Community 41 - "Community 41"
Cohesion: 0.13
Nodes (21): assessment(), discovery(), EngagementMode, host_discovery(), includes_stage(), port_scan(), modes.py — engagement mode configurations. Each mode is a thin config that tunes, Discovery + ports + banner only — no deep dives, no credentials. (+13 more)

### Community 42 - "Community 42"
Cohesion: 0.11
Nodes (13): NmapExecutionError, _parse_nmap_xml(), _run_nmap(), _validated_extra_args(), OSError, NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY: (+5 more)

### Community 43 - "Community 43"
Cohesion: 0.13
Nodes (15): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+7 more)

### Community 44 - "Community 44"
Cohesion: 0.13
Nodes (14): _decode_oid(), _decode_value(), _encode_oid(), _parse_varbinds(), Extract (oid_dotted, value_tag, value_bytes) from a GET/GETNEXT/GETBULK response, Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli, Return (community, sysdescr) for the first responding community, or None., GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]. (+6 more)

### Community 45 - "Community 45"
Cohesion: 0.14
Nodes (16): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con (+8 more)

### Community 46 - "Community 46"
Cohesion: 0.13
Nodes (18): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), MobileScanner, _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd() (+10 more)

### Community 47 - "Community 47"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 48 - "Community 48"
Cohesion: 0.14
Nodes (4): _scan_result(), TestCacheEntry, TestClassifyCertainty, TestWorkflowCache

### Community 49 - "Community 49"
Cohesion: 0.14
Nodes (11): _env_number(), LeaseLostError, Raised when Manager fencing revokes the running attempt., Read a bounded numeric safety setting without trusting the environment., Raised when Manager fencing revokes the running attempt., _run_with_cancellation(), CacheEntry, classify_certainty() (+3 more)

### Community 50 - "Community 50"
Cohesion: 0.10
Nodes (1): TestUDPProbeConstruction

### Community 51 - "Community 51"
Cohesion: 0.11
Nodes (5): test_tls_fingerprint.py — Tier 2.3: active TLS fingerprint (JARM methodology)., _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello

### Community 52 - "Community 52"
Cohesion: 0.14
Nodes (16): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd(), _probe_mdns_mobile_sync() (+8 more)

### Community 53 - "Community 53"
Cohesion: 0.15
Nodes (10): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+2 more)

### Community 54 - "Community 54"
Cohesion: 0.11
Nodes (3): _EchoProtocol, test_async_udp.py — tests for the true-async UDP probe helper in scanner_base., _SinkProtocol

### Community 55 - "Community 55"
Cohesion: 0.19
Nodes (15): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response(), _parse_mdns_response() (+7 more)

### Community 56 - "Community 56"
Cohesion: 0.14
Nodes (8): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =, test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive, _run(), test_protected_redis_raises_no_unauth_finding(), test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_flagged()

### Community 57 - "Community 57"
Cohesion: 0.16
Nodes (13): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, _printable_strings(), passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS). (+5 more)

### Community 58 - "Community 58"
Cohesion: 0.11
Nodes (5): _EchoProtocol, test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit., TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating

### Community 59 - "Community 59"
Cohesion: 0.18
Nodes (16): _clean(), _main(), _parse_args(), _port_label(), _ports_from_env(), local_run.py — run the probe's REAL pipeline (workflow.run_engagement) directly, Actionable input error on stderr → exit code 2. No traceback: this is     operat, Validate positional args (args[0]=target, [1]=profile, [2]=stage, [3]=filter) (+8 more)

### Community 60 - "Community 60"
Cohesion: 0.12
Nodes (17): _corr_ntlm_relay(), SMB signing not required => a viable NTLM relay target. If SMBv1 is also on,, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, SMB signing not required => a viable NTLM relay target. If SMBv1 is also on,, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, SMB signing not required => a viable NTLM relay target. If SMBv1 is also on, (+9 more)

### Community 61 - "Community 61"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 62 - "Community 62"
Cohesion: 0.12
Nodes (17): _corr_ntlm_relay(), SMB signing not required => a viable NTLM relay target. If SMBv1 is also on,, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, SMB signing not required => a viable NTLM relay target. If SMBv1 is also on,, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, SMB signing not required => a viable NTLM relay target. If SMBv1 is also on, (+9 more)

### Community 63 - "Community 63"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 64 - "Community 64"
Cohesion: 0.12
Nodes (1): TestSNMPBerUtilities

### Community 65 - "Community 65"
Cohesion: 0.12
Nodes (1): Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only

### Community 66 - "Community 66"
Cohesion: 0.14
Nodes (15): bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity(), pubkey_to_bytes(), scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.  T (+7 more)

### Community 67 - "Community 67"
Cohesion: 0.26
Nodes (14): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+6 more)

### Community 68 - "Community 68"
Cohesion: 0.18
Nodes (13): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None. (+5 more)

### Community 69 - "Community 69"
Cohesion: 0.14
Nodes (11): gate_0_is_passive_profile(), gate_2_host_discovery(), gate_3_port_scan(), gates.py — precondition functions deciding whether each stage of the workflow ru, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti (+3 more)

### Community 70 - "Community 70"
Cohesion: 0.16
Nodes (8): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), _model_count(), mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None., The strongest possible evidence for a real MCP server: a WWW-Authenticate     he, JSON-typed body that actually talks about auth, not just any error text.

### Community 71 - "Community 71"
Cohesion: 0.21
Nodes (12): _cc(), test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detec, A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU., _run(), test_cc_without_negotiation_is_standard_rdp(), test_confirmed_rdp_wins_dedup_over_port_hint(), test_confirmed_rdp_with_nla_has_no_nla_finding(), test_confirmed_rdp_without_nla_is_high_finding() (+4 more)

### Community 72 - "Community 72"
Cohesion: 0.18
Nodes (10): looks_like_db(), looks_like_http(), looks_like_ssh(), looks_like_tls(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, True when a service banner carries a database greeting signature, so a DB     on, True when a service banner is an SSH identification string, so an SSH     server (+2 more)

### Community 73 - "Community 73"
Cohesion: 0.17
Nodes (13): An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this, The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was     rea, A response with the wrong body StructureSize is not a valid NEGOTIATE., Step 13: expose signing_supported (protocol-precise), not only the     ambiguous, Offering SMB 3.1.1 with no preauth-integrity negotiate context makes     Windows, _smb2_error_response(), _smb2_negotiate_response(), test_error_response_not_parsed_as_signing() (+5 more)

### Community 74 - "Community 74"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 75 - "Community 75"
Cohesion: 0.14
Nodes (4): from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Convenience: build an estimator and fold in a sequence of RTT samples., test_main_scripts_adaptive_timeout.py — Phase 7: per-host adaptive probe timeout

### Community 76 - "Community 76"
Cohesion: 0.21
Nodes (13): _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl. (+5 more)

### Community 77 - "Community 77"
Cohesion: 0.24
Nodes (10): build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip(), _parse_mss(), parse_packet(), syn_cookie() (+2 more)

### Community 78 - "Community 78"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 79 - "Community 79"
Cohesion: 0.21
Nodes (13): _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl. (+5 more)

### Community 80 - "Community 80"
Cohesion: 0.20
Nodes (4): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect(), WindowsCollector

### Community 81 - "Community 81"
Cohesion: 0.22
Nodes (12): _manager(), _plant(), test_e2e_engagement_to_findings.py — the whole pipeline in one place.      manag, Exactly what the probe's smb/port scanners emit for a vulnerable host., Return (http_get, submit_result, captured) simulating the manager side., test_correlated_findings_cite_their_base_findings(), test_engagement_dispatch_reaches_probe_and_enforces_scope(), test_manager_correlation_finds_all_three_attack_paths() (+4 more)

### Community 82 - "Community 82"
Cohesion: 0.33
Nodes (13): _get(), _ids(), test_main_scripts_correlation.py — Epic 2: correlation findings.  Composite, hig, _run(), test_cleartext_cluster_fires_on_two_cleartext_services(), test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_rdp() (+5 more)

### Community 83 - "Community 83"
Cohesion: 0.25
Nodes (5): _mk_scanner(), _scope(), _summary(), TestDefaultsAndAdaptiveTimeout, TestWorkerPoolAndMetrics

### Community 84 - "Community 84"
Cohesion: 0.14
Nodes (3): test_main_scripts_device.py — device-role classification (P0 "Device classificat, TestClassifyDevice, TestClassifyFromResults

### Community 85 - "Community 85"
Cohesion: 0.14
Nodes (1): TestMobileScanner

### Community 86 - "Community 86"
Cohesion: 0.22
Nodes (3): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., True when execution produced errors and no usable or cached facts.

### Community 87 - "Community 87"
Cohesion: 0.15
Nodes (7): expand_targets(), main_entrypoint(), Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Run a scanner CLI's body with consistent, operator-friendly error handling., Wire argparse args into a scanner instance and execute it., run_cli(), ScopeError

### Community 88 - "Community 88"
Cohesion: 0.19
Nodes (5): Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., ScopeError, ScopeGuard

### Community 89 - "Community 89"
Cohesion: 0.15
Nodes (1): test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor

### Community 90 - "Community 90"
Cohesion: 0.17
Nodes (3): _fake_cert(), test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced capa, test_ja4x_from_cert_matches_pure_core()

### Community 91 - "Community 91"
Cohesion: 0.36
Nodes (2): _make_scan_record(), TestDeltaEngine

### Community 92 - "Community 92"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 93 - "Community 93"
Cohesion: 0.15
Nodes (3): When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., TestRunnerScopeValidation

### Community 94 - "Community 94"
Cohesion: 0.15
Nodes (10): In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, _run_inventory() (+2 more)

### Community 95 - "Community 95"
Cohesion: 0.18
Nodes (3): decode_key(), Verify a Manager-signed policy and return its public key for TOFU pinning., verify_site_policy()

### Community 96 - "Community 96"
Cohesion: 0.27
Nodes (11): _b64d(), check_license(), gauntlet(), host_fingerprint(), license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Stable per-machine ID, derived from hw_bind's hardware fingerprint., Returns the license payload dict if valid; raises LicenseError otherwise.     To (+3 more)

### Community 97 - "Community 97"
Cohesion: 0.18
Nodes (12): _as_int(), normalize_intensity(), Coerce an int-or-numeric-string to int, else None (non-numeric)., Map a numeric use-case code → use_case_id (raises on an unknown code)., Coerce an int-or-numeric-string to int, else None (non-numeric)., Accept an intensity as a number (1/2/3) OR a name; return the name.      None st, Map a numeric use-case code → use_case_id (raises on an unknown code)., Accept an intensity as a number (1/2/3) OR a name; return the name.      None st (+4 more)

### Community 98 - "Community 98"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 99 - "Community 99"
Cohesion: 0.23
Nodes (8): build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure., RDPScanner

### Community 100 - "Community 100"
Cohesion: 0.23
Nodes (7): _dec(), match_service(), test_main_scripts_datastore_probe.py — safe read-only datastore probes make the, _svc(), test_elasticsearch_and_couchdb_win_over_generic_http(), test_memcached_version_and_stat_identify_as_memcached(), test_redis_info_and_noauth_identify_as_redis()

### Community 101 - "Community 101"
Cohesion: 0.39
Nodes (10): _ber_len(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _oid_in_subtree(), _oid_tlv(), _req_id_tlv(), _snmp_msg() (+2 more)

### Community 102 - "Community 102"
Cohesion: 0.24
Nodes (2): _smb_registry_collect(), WindowsCollector

### Community 103 - "Community 103"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 104 - "Community 104"
Cohesion: 0.23
Nodes (8): build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure., RDPScanner

### Community 105 - "Community 105"
Cohesion: 0.18
Nodes (8): expand_targets(), main_entrypoint(), Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Writes ScanResult objects as JSONL to a file and/or stdout., Run a scanner CLI's body with consistent, operator-friendly error handling., Wire argparse args into a scanner instance and execute it., ResultWriter, run_cli()

### Community 106 - "Community 106"
Cohesion: 0.18
Nodes (5): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only.

### Community 107 - "Community 107"
Cohesion: 0.17
Nodes (2): Tests that use the real engine but with no-op callbacks., TestRunnerHeadless

### Community 108 - "Community 108"
Cohesion: 0.17
Nodes (12): _finalize_trace(), Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass (+4 more)

### Community 109 - "Community 109"
Cohesion: 0.18
Nodes (11): load_facts_jsonl(), Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo (+3 more)

### Community 110 - "Community 110"
Cohesion: 0.18
Nodes (6): async_udp_probe(), async_udp_probe_retry(), One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, _UDPProbeProtocol

### Community 111 - "Community 111"
Cohesion: 0.18
Nodes (11): load_facts_jsonl(), Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo (+3 more)

### Community 112 - "Community 112"
Cohesion: 0.18
Nodes (6): async_udp_probe(), async_udp_probe_retry(), One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, _UDPProbeProtocol

### Community 113 - "Community 113"
Cohesion: 0.22
Nodes (4): _ext(), test_main_scripts_ja4s.py — JA4S TLS ServerHello fingerprint (advanced capabilit, _serverhello(), test_ja4s_from_serverhello_tls13()

### Community 114 - "Community 114"
Cohesion: 0.31
Nodes (3): _r(), test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ "Multi-vantag, TestReconcileVantages

### Community 115 - "Community 115"
Cohesion: 0.18
Nodes (1): TestFingerprintOs

### Community 116 - "Community 116"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 117 - "Community 117"
Cohesion: 0.22
Nodes (2): interpret_redis_info(), _probe_redis()

### Community 118 - "Community 118"
Cohesion: 0.20
Nodes (10): _by_target(), _corr_anon_data_exposure(), _corr_mgmt_plane_exposed(), _corr_user_enum_plus_weak_auth(), Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h, A disclosed user list (SMB null session) plus a weak/exposed login surface on, Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h, Out-of-band / console management surfaces reachable on one host — these grant (+2 more)

### Community 119 - "Community 119"
Cohesion: 0.20
Nodes (9): _main(), CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma (+1 more)

### Community 120 - "Community 120"
Cohesion: 0.29
Nodes (9): _as_dict(), build_service_index(), _is_open(), A definitively open TCP port. `open|filtered` is NOT open — we never     raise a, Map (target, port) -> confirmed-service info from service_banner facts.      Onl, Accept a raw JSONL dict or a ScanResult; return a plain dict view., _rule_cleartext_and_exposure(), summarize() (+1 more)

### Community 121 - "Community 121"
Cohesion: 0.20
Nodes (10): _by_target(), _corr_anon_data_exposure(), _corr_mgmt_plane_exposed(), _corr_user_enum_plus_weak_auth(), Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h, A disclosed user list (SMB null session) plus a weak/exposed login surface on, Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h, Out-of-band / console management surfaces reachable on one host — these grant (+2 more)

### Community 122 - "Community 122"
Cohesion: 0.20
Nodes (9): _main(), CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma, CLI: derive findings from one or more scanner JSONL files.          python -m ma (+1 more)

### Community 123 - "Community 123"
Cohesion: 0.29
Nodes (9): _as_dict(), build_service_index(), _is_open(), A definitively open TCP port. `open|filtered` is NOT open — we never     raise a, Map (target, port) -> confirmed-service info from service_banner facts.      Onl, Accept a raw JSONL dict or a ScanResult; return a plain dict view., _rule_cleartext_and_exposure(), summarize() (+1 more)

### Community 125 - "Community 125"
Cohesion: 0.20
Nodes (3): Tests for agent/hw_bind.py, TestCheckHwBind, TestGetHwId

### Community 126 - "Community 126"
Cohesion: 0.20
Nodes (5): _fake_run_scan(), Integration tests — full probe lifecycles exercised through the public APIs of a, Phase 1: combined scope validation (validate + excludes)., Return a minimal valid scan result (no real network I/O)., TestScopeValidationPipeline

### Community 127 - "Community 127"
Cohesion: 0.44
Nodes (9): _metrics(), test_main_scripts_completeness.py — Epic 4: set-based scan-completeness invarian, _rec(), test_duplicate_port_is_detected(), test_fallback_count_based_when_no_requested_set(), test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely_complete() (+1 more)

### Community 128 - "Community 128"
Cohesion: 0.29
Nodes (6): _oserr(), test_main_scripts_errno.py — Phase 2: shared TCP/UDP errno classification.  Veri, test_definitive_states(), test_describe_os_error_is_fully_debuggable(), test_scanner_side_errors_are_error_not_filtered(), test_unknown_errno_is_self_identifying_and_never_filtered()

### Community 129 - "Community 129"
Cohesion: 0.20
Nodes (1): TestIoTScanner

### Community 130 - "Community 130"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 131 - "Community 131"
Cohesion: 0.20
Nodes (1): TestUseCasesResolve

### Community 132 - "Community 132"
Cohesion: 0.20
Nodes (2): Each encryption uses a fresh ephemeral key, so blobs are different., TestEncryptDecryptRoundtrip

### Community 133 - "Community 133"
Cohesion: 0.29
Nodes (5): test_tls_integration.py — Tier 2.4 live check: run the real TLSScanner against a, _self_signed(), test_tls_fingerprint_is_nonzero_and_stable(), test_tls_scanner_reports_posture_grade(), _TLSServer

### Community 134 - "Community 134"
Cohesion: 0.22
Nodes (9): _build_run_stats(), _count_open_port_facts(), _hosts_from_facts(), Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact., Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port., Build one consistent result summary for complete and interrupted runs. (+1 more)

### Community 135 - "Community 135"
Cohesion: 0.22
Nodes (9): _clamp(), _job_runtime_seconds(), Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Return the effective whole-job deadline; callers can only reduce it., Return the effective whole-job deadline; callers can only reduce it., Translate operator-supplied job params into run_engagement() kwargs.      This i, Translate operator-supplied job params into run_engagement() kwargs.      This i (+1 more)

### Community 136 - "Community 136"
Cohesion: 0.28
Nodes (9): _error_result(), _facts_from_cache(), Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Single factory for error result dicts — no copy-paste., run_scan(), _runtime_manifest(), _string_list() (+1 more)

### Community 137 - "Community 137"
Cohesion: 0.22
Nodes (9): _corr_cleartext_cluster(), Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests (+1 more)

### Community 138 - "Community 138"
Cohesion: 0.22
Nodes (9): _corr_legacy_windows(), SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas (+1 more)

### Community 139 - "Community 139"
Cohesion: 0.42
Nodes (7): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _scan_tls_sync(), _sni(), _try_version()

### Community 140 - "Community 140"
Cohesion: 0.28
Nodes (5): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples.

### Community 141 - "Community 141"
Cohesion: 0.22
Nodes (9): _corr_cleartext_cluster(), Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests, Two or more cleartext services on one host — any sniffing position harvests (+1 more)

### Community 142 - "Community 142"
Cohesion: 0.22
Nodes (9): _corr_legacy_windows(), SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas (+1 more)

### Community 143 - "Community 143"
Cohesion: 0.22
Nodes (8): Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, ScanFunnel

### Community 144 - "Community 144"
Cohesion: 0.28
Nodes (3): AdaptiveRateController, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window).

### Community 145 - "Community 145"
Cohesion: 0.28
Nodes (5): _dec(), match_service(), One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., ServiceBannerScanner

### Community 146 - "Community 146"
Cohesion: 0.22
Nodes (6): _netbios_session(), parse_smb2_security_mode(), Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout, _smb1_negotiate(), _smb2_negotiate(), SMBScanner

### Community 147 - "Community 147"
Cohesion: 0.22
Nodes (1): TestWindowStateMachine

### Community 148 - "Community 148"
Cohesion: 0.22
Nodes (1): TestTtlInference

### Community 149 - "Community 149"
Cohesion: 0.31
Nodes (4): _infos(), test_resolve.py — resolve() address-family selection (task A9)., Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr)., TestResolveFamily

### Community 150 - "Community 150"
Cohesion: 0.28
Nodes (8): _py_files(), test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1, Every scanner module authored in main_scripts must exist in scanner/., scanner/ must not carry modules that main_scripts/ does not — otherwise the, Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py., test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_files(), test_scanner_module_matches_main_scripts()

### Community 151 - "Community 151"
Cohesion: 0.31
Nodes (2): _modern(), TestGradeTlsPosture

### Community 152 - "Community 152"
Cohesion: 0.22
Nodes (1): TestClassifyCipher

### Community 153 - "Community 153"
Cohesion: 0.22
Nodes (1): TestIdentity

### Community 154 - "Community 154"
Cohesion: 0.22
Nodes (1): TestSubmitResult

### Community 155 - "Community 155"
Cohesion: 0.32
Nodes (8): _derive_devices(), _derive_exposure(), _derive_post_stage(), Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, Classify each target's device role from its collected facts (no I/O).     Return, Reconcile each target's per-vantage reachability into an exposure matrix     (no, _results_by_target()

### Community 156 - "Community 156"
Cohesion: 0.32
Nodes (4): _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()

### Community 157 - "Community 157"
Cohesion: 0.29
Nodes (5): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only.

### Community 158 - "Community 158"
Cohesion: 0.29
Nodes (4): Protocol, _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, _Scanner

### Community 159 - "Community 159"
Cohesion: 0.25
Nodes (8): build_default_funnel(), Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun

### Community 160 - "Community 160"
Cohesion: 0.25
Nodes (8): _candidate_ports(), The port set worth scanning = union of every route's ports (deduped)., The port set worth scanning = union of every route's ports (deduped)., The port set worth scanning = union of every route's ports (deduped)., The port set worth scanning = union of every route's ports (deduped)., The port set worth scanning = union of every route's ports (deduped)., The port set worth scanning = union of every route's ports (deduped)., The port set worth scanning = union of every route's ports (deduped).

### Community 161 - "Community 161"
Cohesion: 0.25
Nodes (8): FunnelResult, The full outcome of funnelling one host., The full outcome of funnelling one host., The full outcome of funnelling one host., The full outcome of funnelling one host., The full outcome of funnelling one host., The full outcome of funnelling one host., The full outcome of funnelling one host.

### Community 162 - "Community 162"
Cohesion: 0.25
Nodes (7): Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result.

### Community 163 - "Community 163"
Cohesion: 0.25
Nodes (8): Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, route_ports()

### Community 164 - "Community 164"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 165 - "Community 165"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 166 - "Community 166"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 167 - "Community 167"
Cohesion: 0.25
Nodes (1): test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model

### Community 168 - "Community 168"
Cohesion: 0.25
Nodes (2): test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te, TestVersionChange

### Community 169 - "Community 169"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 170 - "Community 170"
Cohesion: 0.36
Nodes (7): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 171 - "Community 171"
Cohesion: 0.25
Nodes (8): gate_5_branch_eligible(), Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep

### Community 172 - "Community 172"
Cohesion: 0.25
Nodes (8): _gather_per_host(), Run per-host probes with bounded fan-out and failure isolation., Run per-host probes with bounded fan-out and failure isolation., Run per-host probes with bounded fan-out and failure isolation., Run per-host probes with bounded fan-out and failure isolation., Run per-host probes with bounded fan-out and failure isolation., Run per-host probes with bounded fan-out and failure isolation., Run per-host probes with bounded fan-out and failure isolation.

### Community 173 - "Community 173"
Cohesion: 0.25
Nodes (8): _port_candidates(), Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set.

### Community 174 - "Community 174"
Cohesion: 0.25
Nodes (8): Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, _split_cached()

### Community 175 - "Community 175"
Cohesion: 0.25
Nodes (8): Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., _scan_one()

### Community 176 - "Community 176"
Cohesion: 0.33
Nodes (1): SSHCollector

### Community 177 - "Community 177"
Cohesion: 0.38
Nodes (6): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages()

### Community 178 - "Community 178"
Cohesion: 0.33
Nodes (4): BaseScanner, One observation about one target. Pure fact, no interpretation.      Network-sta, Subclasses implement `scan_target(self, target)` (async), returning a list     o, ScanResult

### Community 179 - "Community 179"
Cohesion: 0.38
Nodes (6): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages()

### Community 180 - "Community 180"
Cohesion: 0.29
Nodes (1): TestNormalizeMac

### Community 181 - "Community 181"
Cohesion: 0.38
Nodes (3): _dry_run(), test_installer_accepts_enroll_token_and_insecure_for_http_manager(), test_installer_without_token_still_shows_manual_approval()

### Community 182 - "Community 182"
Cohesion: 0.29
Nodes (1): TestProfiles

### Community 183 - "Community 183"
Cohesion: 0.48
Nodes (1): TestAcceptEchoReply

### Community 184 - "Community 184"
Cohesion: 0.29
Nodes (1): TestDeviceEnrollment

### Community 185 - "Community 185"
Cohesion: 0.29
Nodes (4): Tests for agent/transport.py, Create a Transport with a real state file path but no actual HTTP calls., TestFetchScope, transport()

### Community 186 - "Community 186"
Cohesion: 0.48
Nodes (6): _b64(), issue(), keygen(), main(), pubkey(), Print the vendor PUBLIC key (hex) derived from the private key.      build/seal-

### Community 187 - "Community 187"
Cohesion: 0.33
Nodes (6): _applied_tuning(), syn' for wide sweeps (deep intensity / full-port audit), else 'connect'., syn' for wide sweeps (deep intensity / full-port audit), else 'connect'., Serialize effective limits without ever echoing credential values., Serialize effective limits without ever echoing credential values., _scan_method_for()

### Community 188 - "Community 188"
Cohesion: 0.40
Nodes (5): check_hw_bind(), get_hw_id(), hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B

### Community 189 - "Community 189"
Cohesion: 0.33
Nodes (4): JobResult, Structured result from running one scan job., Submit the result, with spool-and-retry if available., Execute a complete scan job lifecycle.          Args:             job: Job dict

### Community 190 - "Community 190"
Cohesion: 0.40
Nodes (5): classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj

### Community 191 - "Community 191"
Cohesion: 0.47
Nodes (2): One probe-ladder rung on its own connection. Returns banner bytes, b""         (, ServiceBannerScanner

### Community 192 - "Community 192"
Cohesion: 0.40
Nodes (5): classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj

### Community 193 - "Community 193"
Cohesion: 0.33
Nodes (2): RateLimiter, Simple async rate limiter: at most `rate` operations per second.

### Community 194 - "Community 194"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 195 - "Community 195"
Cohesion: 0.33
Nodes (1): TestDeviceHint

### Community 196 - "Community 196"
Cohesion: 0.33
Nodes (4): Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., TestTaskRunnerWithEncryptedScope

### Community 197 - "Community 197"
Cohesion: 0.33
Nodes (2): Phase 2: WebSocket message parsing., TestWebSocketMessageProtocol

### Community 198 - "Community 198"
Cohesion: 0.33
Nodes (4): Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup., TestStartupGauntlet

### Community 199 - "Community 199"
Cohesion: 0.33
Nodes (1): test_main_scripts_device_ties.py — Phase 23: device classification never resolve

### Community 200 - "Community 200"
Cohesion: 0.33
Nodes (1): TestStableHostId

### Community 201 - "Community 201"
Cohesion: 0.33
Nodes (2): test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti, TestNmapEntityGuard

### Community 202 - "Community 202"
Cohesion: 0.33
Nodes (1): TestClamp

### Community 203 - "Community 203"
Cohesion: 0.33
Nodes (1): TestEngagementModes

### Community 204 - "Community 204"
Cohesion: 0.53
Nodes (5): _manifest(), test_probe_manifest.py — the `agent.agent manifest` command that the seal-parity, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_contract()

### Community 205 - "Community 205"
Cohesion: 0.33
Nodes (1): TestOtherServices

### Community 206 - "Community 206"
Cohesion: 0.53
Nodes (2): The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, TestSynRetransmit

### Community 207 - "Community 207"
Cohesion: 0.60
Nodes (1): TestBuildResultsEnrichment

### Community 208 - "Community 208"
Cohesion: 0.33
Nodes (1): TestOptionParsing

### Community 209 - "Community 209"
Cohesion: 0.33
Nodes (1): TestAssessTarpit

### Community 210 - "Community 210"
Cohesion: 0.33
Nodes (3): diff_assets(), report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d, re-scan mode's delta report: what changed between two engagements.

### Community 211 - "Community 211"
Cohesion: 0.50
Nodes (3): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =

### Community 212 - "Community 212"
Cohesion: 0.40
Nodes (2): Phase 1: result spool with upload retry., TestResultSpoolWithRetry

### Community 213 - "Community 213"
Cohesion: 0.40
Nodes (3): Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine., TestTransportWithIdentity

### Community 214 - "Community 214"
Cohesion: 0.40
Nodes (1): TestIcmpBuilders

### Community 215 - "Community 215"
Cohesion: 0.50
Nodes (1): TestIcmpParse

### Community 216 - "Community 216"
Cohesion: 0.60
Nodes (1): TestIcmpTimestamps

### Community 217 - "Community 217"
Cohesion: 0.40
Nodes (1): TestEngineSummary

### Community 218 - "Community 218"
Cohesion: 0.40
Nodes (1): TestGate2

### Community 219 - "Community 219"
Cohesion: 0.40
Nodes (1): TestLooksLikeHttp

### Community 220 - "Community 220"
Cohesion: 0.40
Nodes (1): TestLooksLikeTls

### Community 221 - "Community 221"
Cohesion: 0.40
Nodes (1): TestResolveScanType

### Community 222 - "Community 222"
Cohesion: 0.40
Nodes (1): TestTargets

### Community 223 - "Community 223"
Cohesion: 0.40
Nodes (1): TestRoutePorts

### Community 224 - "Community 224"
Cohesion: 0.40
Nodes (2): test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel, RecordingDeep

### Community 225 - "Community 225"
Cohesion: 0.40
Nodes (2): Tests for agent/scope_crypt.py, TestKeyGeneration

### Community 226 - "Community 226"
Cohesion: 0.40
Nodes (1): TestHttpMatch

### Community 227 - "Community 227"
Cohesion: 0.40
Nodes (1): TestPacketRoundTrip

### Community 228 - "Community 228"
Cohesion: 0.40
Nodes (1): TestSynCookie

### Community 229 - "Community 229"
Cohesion: 0.70
Nodes (1): TestVerifyReplyCookie

### Community 230 - "Community 230"
Cohesion: 0.80
Nodes (1): TestPortScannerTarpitFlag

### Community 231 - "Community 231"
Cohesion: 0.40
Nodes (3): Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., TestRunnerSubmission

### Community 232 - "Community 232"
Cohesion: 0.40
Nodes (1): TestWebSocket

### Community 233 - "Community 233"
Cohesion: 0.67
Nodes (1): TLSFingerprintScanner

### Community 234 - "Community 234"
Cohesion: 0.50
Nodes (3): RuntimeError, PassiveListenerError, All passive sources failed before the listen window could start.

### Community 235 - "Community 235"
Cohesion: 0.67
Nodes (1): TLSScanner

### Community 236 - "Community 236"
Cohesion: 0.67
Nodes (1): WebScanner

### Community 237 - "Community 237"
Cohesion: 0.83
Nodes (1): TestTimestampFallback

### Community 238 - "Community 238"
Cohesion: 0.50
Nodes (1): TestGate0

### Community 239 - "Community 239"
Cohesion: 0.50
Nodes (1): TestGate3

### Community 240 - "Community 240"
Cohesion: 0.50
Nodes (1): TestGate4

### Community 241 - "Community 241"
Cohesion: 0.50
Nodes (1): TestRateLimiter

### Community 242 - "Community 242"
Cohesion: 0.50
Nodes (1): TestRouteBranches

### Community 243 - "Community 243"
Cohesion: 0.50
Nodes (1): TestScanResult

### Community 244 - "Community 244"
Cohesion: 0.50
Nodes (1): TestSshMatch

### Community 245 - "Community 245"
Cohesion: 0.50
Nodes (1): TestHeartbeat

### Community 246 - "Community 246"
Cohesion: 0.50
Nodes (1): TestHttpGet

### Community 247 - "Community 247"
Cohesion: 0.50
Nodes (1): TestPollJobs

### Community 248 - "Community 248"
Cohesion: 0.50
Nodes (1): TestRefreshRegistration

### Community 249 - "Community 249"
Cohesion: 0.50
Nodes (1): TestRegister

### Community 250 - "Community 250"
Cohesion: 0.67
Nodes (3): Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, _rule_ftp()

### Community 251 - "Community 251"
Cohesion: 0.67
Nodes (3): rsync daemon exposure. Anonymously-selectable modules are the high finding     (, rsync daemon exposure. Anonymously-selectable modules are the high finding     (, _rule_rsync()

### Community 252 - "Community 252"
Cohesion: 0.67
Nodes (3): IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, _rule_ipmi()

### Community 253 - "Community 253"
Cohesion: 0.67
Nodes (3): SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., _rule_smtp()

### Community 254 - "Community 254"
Cohesion: 0.67
Nodes (3): Windows RPC endpoint-mapper disclosure — the internal RPC service map., Windows RPC endpoint-mapper disclosure — the internal RPC service map., _rule_msrpc()

### Community 255 - "Community 255"
Cohesion: 0.67
Nodes (3): Exposed network printer — an information leak and an attack surface., Exposed network printer — an information leak and an attack surface., _rule_printer()

### Community 256 - "Community 256"
Cohesion: 0.67
Nodes (3): Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, _rule_ftp()

### Community 257 - "Community 257"
Cohesion: 0.67
Nodes (3): rsync daemon exposure. Anonymously-selectable modules are the high finding     (, rsync daemon exposure. Anonymously-selectable modules are the high finding     (, _rule_rsync()

### Community 258 - "Community 258"
Cohesion: 0.67
Nodes (3): IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, _rule_ipmi()

### Community 259 - "Community 259"
Cohesion: 0.67
Nodes (3): SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., _rule_smtp()

### Community 260 - "Community 260"
Cohesion: 0.67
Nodes (3): Windows RPC endpoint-mapper disclosure — the internal RPC service map., Windows RPC endpoint-mapper disclosure — the internal RPC service map., _rule_msrpc()

### Community 261 - "Community 261"
Cohesion: 0.67
Nodes (3): Exposed network printer — an information leak and an attack surface., Exposed network printer — an information leak and an attack surface., _rule_printer()

### Community 262 - "Community 262"
Cohesion: 0.67
Nodes (1): TestIcmpCapability

### Community 263 - "Community 263"
Cohesion: 0.67
Nodes (1): TestInetChecksum

### Community 264 - "Community 264"
Cohesion: 0.67
Nodes (1): TestRemoteClock

### Community 265 - "Community 265"
Cohesion: 0.67
Nodes (1): TestAssetMergeCredentialed

### Community 266 - "Community 266"
Cohesion: 0.67
Nodes (1): TestAssetMergeHostDiscovery

### Community 267 - "Community 267"
Cohesion: 0.67
Nodes (1): TestAssetMergePortScan

### Community 268 - "Community 268"
Cohesion: 0.67
Nodes (1): TestAssetOpenPortsForDeepScan

### Community 269 - "Community 269"
Cohesion: 0.67
Nodes (1): TestCapabilities

### Community 270 - "Community 270"
Cohesion: 0.67
Nodes (1): TestNoMatch

### Community 271 - "Community 271"
Cohesion: 0.67
Nodes (1): TestProbeLadder

### Community 272 - "Community 272"
Cohesion: 0.67
Nodes (1): TestRunnerScanTypes

### Community 273 - "Community 273"
Cohesion: 1.00
Nodes (1): Args:             http_get:       Callback for authenticated GET (from Transport

### Community 274 - "Community 274"
Cohesion: 1.00
Nodes (1): Current integer window (>= min_window).

### Community 275 - "Community 275"
Cohesion: 1.00
Nodes (1): Read-only view of allowed networks (for CIDR-level engines).

### Community 276 - "Community 276"
Cohesion: 1.00
Nodes (1): Read-only view of excluded networks (to build masscan --exclude).

### Community 277 - "Community 277"
Cohesion: 1.00
Nodes (1): TestAssetMergePassiveCollect

### Community 278 - "Community 278"
Cohesion: 1.00
Nodes (1): TestAssetMergeServiceBanner

### Community 279 - "Community 279"
Cohesion: 1.00
Nodes (1): TestAssetMergeSmbScan

### Community 280 - "Community 280"
Cohesion: 1.00
Nodes (1): TestAssetMergeTlsScan

### Community 281 - "Community 281"
Cohesion: 1.00
Nodes (1): TestAssetMergeUnknownScanner

### Community 282 - "Community 282"
Cohesion: 1.00
Nodes (1): TestAssetMergeWebScan

## Knowledge Gaps
- **776 isolated node(s):** `agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit`, `Run a bounded capability suite and optionally score known ground truth.`, `Verify a Manager-signed policy and return its public key for TOFU pinning.`, `hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina`, `Raised when the binary is running on an unauthorized machine.` (+771 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 50`** (1 nodes): `TestUDPProbeConstruction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `TestSNMPBerUtilities`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `TestMobileScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (2 nodes): `_make_scan_record()`, `TestDeltaEngine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (2 nodes): `_smb_registry_collect()`, `WindowsCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (2 nodes): `Tests that use the real engine but with no-op callbacks.`, `TestRunnerHeadless`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (1 nodes): `TestFingerprintOs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 116`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 117`** (2 nodes): `interpret_redis_info()`, `_probe_redis()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 129`** (1 nodes): `TestIoTScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 130`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 131`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 132`** (2 nodes): `Each encryption uses a fresh ephemeral key, so blobs are different.`, `TestEncryptDecryptRoundtrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 147`** (1 nodes): `TestWindowStateMachine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 148`** (1 nodes): `TestTtlInference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 151`** (2 nodes): `_modern()`, `TestGradeTlsPosture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 152`** (1 nodes): `TestClassifyCipher`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 153`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 154`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 164`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (1 nodes): `test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (2 nodes): `test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te`, `TestVersionChange`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 169`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 176`** (1 nodes): `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 180`** (1 nodes): `TestNormalizeMac`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 182`** (1 nodes): `TestProfiles`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 183`** (1 nodes): `TestAcceptEchoReply`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 184`** (1 nodes): `TestDeviceEnrollment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 191`** (2 nodes): `One probe-ladder rung on its own connection. Returns banner bytes, b""         (`, `ServiceBannerScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 193`** (2 nodes): `RateLimiter`, `Simple async rate limiter: at most `rate` operations per second.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 195`** (1 nodes): `TestDeviceHint`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 197`** (2 nodes): `Phase 2: WebSocket message parsing.`, `TestWebSocketMessageProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 199`** (1 nodes): `test_main_scripts_device_ties.py — Phase 23: device classification never resolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 200`** (1 nodes): `TestStableHostId`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 201`** (2 nodes): `test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti`, `TestNmapEntityGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 202`** (1 nodes): `TestClamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 203`** (1 nodes): `TestEngagementModes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 205`** (1 nodes): `TestOtherServices`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (2 nodes): `The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa`, `TestSynRetransmit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (1 nodes): `TestBuildResultsEnrichment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (1 nodes): `TestOptionParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 209`** (1 nodes): `TestAssessTarpit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 212`** (2 nodes): `Phase 1: result spool with upload retry.`, `TestResultSpoolWithRetry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (1 nodes): `TestIcmpBuilders`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (1 nodes): `TestIcmpParse`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 216`** (1 nodes): `TestIcmpTimestamps`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (1 nodes): `TestEngineSummary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (1 nodes): `TestGate2`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (1 nodes): `TestLooksLikeHttp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (1 nodes): `TestLooksLikeTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (1 nodes): `TestResolveScanType`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (1 nodes): `TestTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (1 nodes): `TestRoutePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (2 nodes): `test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel`, `RecordingDeep`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (2 nodes): `Tests for agent/scope_crypt.py`, `TestKeyGeneration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (1 nodes): `TestHttpMatch`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (1 nodes): `TestPacketRoundTrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 228`** (1 nodes): `TestSynCookie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (1 nodes): `TestVerifyReplyCookie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (1 nodes): `TestPortScannerTarpitFlag`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (1 nodes): `TestWebSocket`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 233`** (1 nodes): `TLSFingerprintScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (1 nodes): `TLSScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (1 nodes): `WebScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (1 nodes): `TestTimestampFallback`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (1 nodes): `TestGate0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (1 nodes): `TestGate3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 240`** (1 nodes): `TestGate4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (1 nodes): `TestRateLimiter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 242`** (1 nodes): `TestRouteBranches`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (1 nodes): `TestScanResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 244`** (1 nodes): `TestSshMatch`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (1 nodes): `TestHeartbeat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (1 nodes): `TestHttpGet`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (1 nodes): `TestPollJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 248`** (1 nodes): `TestRefreshRegistration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (1 nodes): `TestRegister`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (1 nodes): `TestIcmpCapability`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (1 nodes): `TestInetChecksum`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (1 nodes): `TestRemoteClock`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (1 nodes): `TestAssetMergeCredentialed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (1 nodes): `TestAssetMergeHostDiscovery`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (1 nodes): `TestAssetMergePortScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (1 nodes): `TestAssetOpenPortsForDeepScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (1 nodes): `TestCapabilities`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 270`** (1 nodes): `TestNoMatch`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (1 nodes): `TestProbeLadder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 272`** (1 nodes): `TestRunnerScanTypes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 273`** (1 nodes): `Args:             http_get:       Callback for authenticated GET (from Transport`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (1 nodes): `Current integer window (>= min_window).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (1 nodes): `Read-only view of allowed networks (for CIDR-level engines).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (1 nodes): `Read-only view of excluded networks (to build masscan --exclude).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (1 nodes): `TestAssetMergePassiveCollect`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 278`** (1 nodes): `TestAssetMergeServiceBanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (1 nodes): `TestAssetMergeSmbScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (1 nodes): `TestAssetMergeTlsScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (1 nodes): `TestAssetMergeUnknownScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (1 nodes): `TestAssetMergeWebScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ScanResult` connect `Community 0` to `Community 49`, `Community 187`, `Community 135`, `Community 134`, `Community 155`, `Community 136`, `Community 2`, `Community 31`, `Community 23`, `Community 70`, `Community 52`, `Community 42`, `Community 18`, `Community 43`, `Community 99`, `Community 76`, `Community 27`, `Community 87`, `Community 191`, `Community 14`, `Community 44`, `Community 176`, `Community 233`, `Community 157`, `Community 102`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `ScopeGuard` connect `Community 0` to `Community 49`, `Community 187`, `Community 135`, `Community 134`, `Community 155`, `Community 136`, `Community 59`, `Community 2`, `Community 23`, `Community 70`, `Community 52`, `Community 42`, `Community 18`, `Community 43`, `Community 99`, `Community 27`, `Community 276`, `Community 87`, `Community 275`, `Community 191`, `Community 44`, `Community 176`, `Community 233`, `Community 157`, `Community 102`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `Asset` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 263 inferred relationships involving `ScanResult` (e.g. with `LeaseLostError` and `engine.py — adapt a manager scan job to scanner_module's workflow engine and ret`) actually correct?**
  _`ScanResult` has 263 INFERRED edges - model-reasoned connections that need verification._
- **Are the 234 inferred relationships involving `ScopeGuard` (e.g. with `LeaseLostError` and `engine.py — adapt a manager scan job to scanner_module's workflow engine and ret`) actually correct?**
  _`ScopeGuard` has 234 INFERRED edges - model-reasoned connections that need verification._
- **Are the 200 inferred relationships involving `ResultWriter` (e.g. with `DBScanner` and `db_scanner.py — fingerprint database services.  WHY: databases are everywhere on`) actually correct?**
  _`ResultWriter` has 200 INFERRED edges - model-reasoned connections that need verification._
- **Are the 163 inferred relationships involving `BaseScanner` (e.g. with `DBScanner` and `db_scanner.py — fingerprint database services.  WHY: databases are everywhere on`) actually correct?**
  _`BaseScanner` has 163 INFERRED edges - model-reasoned connections that need verification._