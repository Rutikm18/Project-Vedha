# Graph Report - .  (2026-08-19)

## Corpus Check
- Large corpus: 966 files · ~821,835 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 9080 nodes · 18302 edges · 472 communities detected
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 2776 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 3977 · calls: 3026 · uses: 2776 · rationale_for: 2254 · method: 2079 · MODIFIES: 1647 · ON_BRANCH: 1133 · imports: 539 · imports_from: 488 · inherits: 252 · PARENT_OF: 131


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 966 · Candidates: 2144
- Excluded: 103 untracked · 64076 ignored · 9 sensitive · 2 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `c7f226f`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `FindingSeverity` - 175 edges
2. `FindingStatus` - 136 edges
3. `Engagement` - 126 edges
4. `Finding` - 114 edges
5. `Asset` - 105 edges
6. `ScanJob` - 95 edges
7. `Service` - 80 edges
8. `ScanJobType` - 75 edges
9. `ScanJobStatus` - 74 edges
10. `SourceConfidence` - 72 edges

## Surprising Connections (you probably didn't know these)
- `BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges` --uses--> `FindingSeverity`  [INFERRED]
  manager/backend/app/ad/bloodhound.py → manager/backend/app/models/enums.py
- `Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu` --uses--> `FindingSeverity`  [INFERRED]
  manager/backend/app/ad/bloodhound.py → manager/backend/app/models/enums.py
- `Ingest one BloodHound collector file. Returns (#nodes, #rels).` --uses--> `FindingSeverity`  [INFERRED]
  manager/backend/app/ad/bloodhound.py → manager/backend/app/models/enums.py
- `Return shortest attack paths from any non-DA principal to a Domain Admins` --uses--> `FindingSeverity`  [INFERRED]
  manager/backend/app/ad/bloodhound.py → manager/backend/app/models/enums.py
- `Build a Finding summarising the shortest paths to Domain Admins.` --uses--> `FindingSeverity`  [INFERRED]
  manager/backend/app/ad/bloodhound.py → manager/backend/app/models/enums.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (69): BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL, HallucinationGuard — post-generation validation of LLM report text against the g, get_read_db(), Read-only session (no commit) routed to the replica when configured.     For SEL, Read-only session (no commit) routed to the replica when configured.     For SEL, client_ip(), rate_limit() (+61 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (136): PROFILE_TOOLS, ModuleCategory, ModuleInput, ModuleOutput, modulesForPorts(), ScanModule, bySeverityCount(), runScan() (+128 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (139): agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Bump severity one rung when the finding's service is internet-reachable     (Ser, ServiceIdentifier, DiscoveryJobPayload, DiscoveryWorker (+131 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (91): Exception, MetasploitRPCClient, MetasploitRPCError, Returns {status, output, uuid}., Returns True if job was successfully killed., Poll until job completes or max_wait exceeded., Authenticated RPC call — prepends token., Async Metasploit RPC client using msgpack-over-HTTPS. (+83 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (88): hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit, result_spool.py — local result persistence with upload retry.  When the probe co, fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), scope_validator.py — defense-in-depth scope re-validation for the probe.  The pr, Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl (+80 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (91): ApiActivity, GET, AiMessage, ManagerAiResponse, POST(), validMessages(), ManagerAiResponse, 0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner UI (+83 more)

### Community 6 - "Community 6"
Cohesion: 0.02
Nodes (76): metadata, AssistantProvider(), PageShell(), PageShellProps, QueryProvider(), NAV_SECTIONS, NavItem, Sidebar() (+68 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (88): ADError, Shared building blocks for the Active Directory assessment module.  Every AD che, Assemble a Finding-compatible dict.      All findings carry — as required by the, Base class for Active Directory assessment errors., Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, A previously-remediated finding whose issue reappeared this run: reopen     the (+80 more)

### Community 8 - "Community 8"
Cohesion: 0.02
Nodes (62): 4d0377d Add unit tests for SMB scanner, SYN scanner, and TLS functionality- Implemented unit tests for SMB scanner to validate security mode parsing and error handling.- Added a new SYN scanner test suite to cover packet crafting, checksum validation, and SYN cookie functionality.- Introduced tests for TLS fingerprinting and posture grading, ensuring accurate classification of cipher suites and TLS versions.- Created integration tests for the TLS scanner against a loopback server to verify posture grading and cipher analysis., 54503ae feat(scanner): SYN path harvests OS-fingerprint intel + RTT-adaptive timing, ae08d19 feat(scanner): adaptive timeout, SYN retransmit, top-100 default (accuracy roadmap 1-3), classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj (+54 more)

### Community 9 - "Community 9"
Cohesion: 0.03
Nodes (25): Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG, _scan_result(), TestAssetMergeCredentialed, TestAssetMergeHostDiscovery, TestAssetMergePassiveCollect, TestAssetMergePortScan, TestAssetMergeServiceBanner, TestAssetMergeSmbScan (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.02
Nodes (30): Single source of truth for the deployed application version.  The value is injec, 22701ea Add tests for scanner parity and enhance use case resolution- Introduced  to ensure that the scanner directory is in sync with the main_scripts directory, preventing silent code drift.- Updated  to include additional assertions for use case resolution, intensity handling, and validation of unique use case codes.- Enhanced  to clarify the build process for sealed probes.- Added  command to  for printing the vendor public key derived from the private key.- Implemented  to introduce a new intensity knob for scanning, allowing operators to specify scan depth and breadth.- Modified  to support port overrides based on intensity settings and introduced a SYN scanning method for efficiency.- Created  script to verify that the sealed binary matches the source manifest, ensuring build integrity., b5ffcb0 Refactor Vedha probe installer and enhance device identity tests- Updated the installer script to require only the manager endpoint in dry run mode, removing unnecessary prompts for credentials.- Changed the default behavior of LICENSE_ENFORCED to false.- Improved error handling for unknown arguments and missing required parameters in the installer.- Added tests for device identity generation, signing, and verification, ensuring robust handling of key encoding and site policy enforcement.- Enhanced HTTP lease tests to cover edge cases for lease renewal and cancellation.- Introduced tests for installer contract to ensure no human credentials are present in the source.- Updated result spool tests to handle permanent rejections and ensure proper quarantine behavior.- Improved transport tests to validate device enrollment and access token rotation.- Enhanced WebSocket claim protocol tests to verify job claiming with additional parameters., c0f3b4c feat(probe-enroll): trust-on-first-use auto-enrollment + gen-env policy-key fix, c4386e4 feat(customers): operator Customers dashboard + per-customer portal slug, ClientUser, ScanReq, scan_health.py — turn the probe's per-host scan completeness/health metrics into (+22 more)

### Community 11 - "Community 11"
Cohesion: 0.19
Nodes (88): use_cases.py — the finite, pre-defined library of scan scenarios the manager can, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/probe-usecase-alignment, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive (+80 more)

### Community 12 - "Community 12"
Cohesion: 0.04
Nodes (44): apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl(), Session, SESSION_DIR (+36 more)

### Community 13 - "Community 13"
Cohesion: 0.04
Nodes (50): ComplianceRef, COVERAGE_COLOR, DetectionCoverage, ExploitMaturity, Finding, FindingDetail(), FindingPage, FindingsPage() (+42 more)

### Community 14 - "Community 14"
Cohesion: 0.06
Nodes (51): feat/complete-pending-work, main, 00c6648 feat(settings): editable email/Slack/Jira integrations wired to backend (item 3 UI), 027f4e4 feat(integrations): per-tenant email/Slack/Jira config store + CRUD (item 3 backend), 0e22dbf feat(probe): bounded auto-troubleshoot for Manager connectivity, 185e648 docs: pending-work inventory (buckets A-G), 1af3404 feat(deploy): probe-free manager stack + port-80 edge ingress, 22e4f8d chore: update version (+43 more)

### Community 15 - "Community 15"
Cohesion: 0.04
Nodes (39): GRADE_STYLE, GRADE_VAR, portalApi(), PortalEngagement, PortalFinding, PortalPosture, PortalReport, PortalScanRequest (+31 more)

### Community 16 - "Community 16"
Cohesion: 0.04
Nodes (51): assess_tarpit(), bracket_host(), choose_source_port(), classify_os_error(), describe_os_error(), inet_checksum(), jittered_delay(), parse_ports() (+43 more)

### Community 17 - "Community 17"
Cohesion: 0.05
Nodes (58): _applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _derive_post_stage(), _env_number(), _error_result(), _facts_from_cache() (+50 more)

### Community 18 - "Community 18"
Cohesion: 0.04
Nodes (56): _agent_can_execute_job(), _agent_ownership_check(), AgentBootstrapRequest, bootstrap_agent(), _encrypt_scope_for_agent(), enqueue_agent_job(), get_agent_jobs(), get_job_status() (+48 more)

### Community 19 - "Community 19"
Cohesion: 0.04
Nodes (48): async_udp_probe(), async_udp_probe_retry(), BaseScanner, main_entrypoint(), One observation about one target. Pure fact, no interpretation.      Network-sta, One observation about one target. Pure fact, no interpretation.      Network-sta, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, Send one UDP datagram and await the first reply — fully on the event loop. (+40 more)

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (55): A, ask(), askSecret(), banner(), buildInteractiveCommand(), choose(), chooseNextPhase(), confirm() (+47 more)

### Community 21 - "Community 21"
Cohesion: 0.06
Nodes (34): Delta(), Meter(), Panel(), Readout(), Agent, AGENT_STATUS, AgentStatus, Exposure (+26 more)

### Community 22 - "Community 22"
Cohesion: 0.05
Nodes (22): DBScanner, interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act, FakeReader, FakeWriter, _probe() (+14 more)

### Community 23 - "Community 23"
Cohesion: 0.05
Nodes (42): c7f226f chore: bundle pending working-tree work for release, main(), summarize(), scan_requests.use_case_id — the capability use-case a customer requested.  The p, _finalize_trace(), _gather_per_host(), _port_candidates(), workflow_engine.py — the async DAG executor. Loops through gates, checks precond (+34 more)

### Community 24 - "Community 24"
Cohesion: 0.05
Nodes (27): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it. (+19 more)

### Community 25 - "Community 25"
Cohesion: 0.05
Nodes (38): _ike_probe(), interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats(), interpret_ntp_monlist(), interpret_sip() (+30 more)

### Community 26 - "Community 26"
Cohesion: 0.05
Nodes (42): build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip(), _parse_mss(), parse_packet(), Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header). (+34 more)

### Community 27 - "Community 27"
Cohesion: 0.05
Nodes (42): build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip(), _parse_mss(), parse_packet(), Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header). (+34 more)

### Community 28 - "Community 28"
Cohesion: 0.05
Nodes (47): _claim_batch(), _dead_letter_stale_stmt(), enqueue(), Event, _handle_facts_ready(), _handle_notify(), is_stale_processing(), main() (+39 more)

### Community 29 - "Community 29"
Cohesion: 0.09
Nodes (45): _as_dict(), build_service_index(), _by_target(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay(), _data(), Finding (+37 more)

### Community 30 - "Community 30"
Cohesion: 0.07
Nodes (40): activate_enrollment(), approve_enrollment(), approve_request_simple(), _authenticated_request(), auto_enroll_cidrs(), create_enroll_token(), create_enrollment_request(), _decode_public_key() (+32 more)

### Community 31 - "Community 31"
Cohesion: 0.06
Nodes (41): accept_echo_reply(), build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), fingerprint_os(), hop_estimate(), _icmp(), icmp_supported() (+33 more)

### Community 32 - "Community 32"
Cohesion: 0.06
Nodes (37): BaseModel, ActivityItem, recent_activity(), AssetIn, AssetOut, BulkAssetImportResult, LoginRequest, PersonalAccessTokenCreate (+29 more)

### Community 33 - "Community 33"
Cohesion: 0.10
Nodes (34): correlate_smb_patch(), dedup_findings(), _product_from_cpe(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Suppress a suspected/potential (inferred-source) finding when the     SAME host (+26 more)

### Community 34 - "Community 34"
Cohesion: 0.08
Nodes (7): _finding(), TestAggregate, TestClassifyTier, TestComputePriority, TestDedupFindings, TestFindingConsistency, TestVerify

### Community 35 - "Community 35"
Cohesion: 0.06
Nodes (38): accept_echo_reply(), build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), fingerprint_os(), hop_estimate(), _icmp(), icmp_supported() (+30 more)

### Community 36 - "Community 36"
Cohesion: 0.07
Nodes (16): _fact(), Tests for ai_normalizer.py — 0% prior coverage.  Covers:   - extract_raw_text: p, Any exception from the AI client yields [] — never raises, never         blocks, When the cache already has an answer, the client must not be called., A candidate dict without a 'product' key must be silently skipped., If the client returns something that isn't a list, return []., Every candidate produced by propose_candidates must be tagged         ai_assiste, source_confidence on the resulting CPECandidate must match the         originati (+8 more)

### Community 37 - "Community 37"
Cohesion: 0.11
Nodes (28): _banner_jsonl(), _empty_epss(), _empty_jsonl(), _empty_kev(), _mock_vuln_db(), _openssh_vuln_db(), Tests for pipeline.py — the orchestrator with 0% prior coverage.  Covers the cri, A completely empty file must not produce any findings. (+20 more)

### Community 38 - "Community 38"
Cohesion: 0.10
Nodes (22): _added(), _client(), _db_first(), _db_for_create(), _db_list(), _db_scalar(), _engagement(), _finding() (+14 more)

### Community 39 - "Community 39"
Cohesion: 0.07
Nodes (26): AdvisorFlow(), PATCH_PILL, AssistantDrawer(), ExplainResponse, Msg, Served, AssistantFab(), AssistantCtx (+18 more)

### Community 40 - "Community 40"
Cohesion: 0.06
Nodes (40): approve_scan_request(), AssignAgentBody, build_scan_job(), ClientUserCreate, ClientUserOut, ClientUserPatch, CustomerListItem, _existing_client_user() (+32 more)

### Community 41 - "Community 41"
Cohesion: 0.06
Nodes (30): classify_os_error(), _family_of(), PortScanner, Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets (+22 more)

### Community 42 - "Community 42"
Cohesion: 0.07
Nodes (16): _make_db(), _make_tenant(), _make_user(), Tests for authentication login flow.  Covers:   - login success   - user_not_fou, Ensure every exception class has the expected reason_code attribute.     These c, AsyncSession mock that returns user on first execute, tenant on second., TestAuthenticateBcryptFailure, TestAuthenticateDatabaseFailure (+8 more)

### Community 43 - "Community 43"
Cohesion: 0.14
Nodes (33): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+25 more)

### Community 44 - "Community 44"
Cohesion: 0.06
Nodes (32): DEMO_ASSET, DEMO_ENGAGEMENT, DEMO_FINDING, AssetInput, chat(), CRITICALITY_SCORE, DESTRUCTIVE_PATTERNS, EPSS_MOCK (+24 more)

### Community 45 - "Community 45"
Cohesion: 0.08
Nodes (9): _asset(), TestAssetNeedsRecheckLive, TestAssetOpenPortsForDeepScan, TestGate2, TestGate3, TestGate4, TestGate5, TestGate6 (+1 more)

### Community 46 - "Community 46"
Cohesion: 0.07
Nodes (28): Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result., Remove the spool file for a successfully uploaded result., Attempt to upload a result with retries and local spool as fallback.          Ar, Move a terminally rejected result out of the retry queue., Re-attempt upload of all previously spooled results.          Called once at pro, Attempt to upload a result with retries and local spool as fallback.          Ar, Number of pending (unsubmitted) results in the spool. (+20 more)

### Community 47 - "Community 47"
Cohesion: 0.08
Nodes (36): all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), normalize(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web() (+28 more)

### Community 48 - "Community 48"
Cohesion: 0.10
Nodes (39): _as_dict(), build_service_index(), _by_target(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay(), _data(), Finding (+31 more)

### Community 49 - "Community 49"
Cohesion: 0.11
Nodes (10): _candidate(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db(), TestEnrichFinding, TestEpssDb, TestKevDb, TestMatchCandidate (+2 more)

### Community 50 - "Community 50"
Cohesion: 0.11
Nodes (37): _ids(), test_main_scripts_findings.py — the findings interpretation layer.  Pure-logic,, _run(), test_accepts_scanresult_objects_not_just_dicts(), test_all_security_headers_present_no_finding(), test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_double_report(), test_confirmed_ftp_cleartext_is_high_confidence() (+29 more)

### Community 51 - "Community 51"
Cohesion: 0.07
Nodes (35): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response() (+27 more)

### Community 52 - "Community 52"
Cohesion: 0.07
Nodes (35): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response() (+27 more)

### Community 53 - "Community 53"
Cohesion: 0.09
Nodes (23): AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator, DatabaseConnectivityValidator, DatabaseURLValidator, DetectionEngineValidator (+15 more)

### Community 54 - "Community 54"
Cohesion: 0.07
Nodes (26): ConnectionManager, GraphWebSocketManager, High-level manager for graph-specific WebSocket operations., Handle a new WebSocket client connection., Handle incoming WebSocket messages., Manages WebSocket connections with room-based broadcasting., Broadcast graph data update to all subscribers., Broadcast a single node update. (+18 more)

### Community 55 - "Community 55"
Cohesion: 0.12
Nodes (23): ADConnectionError, build_ad_finding(), DependencyMissingError, severity_from_str(), ACE, ADComputer, ADGroup, ADUser (+15 more)

### Community 56 - "Community 56"
Cohesion: 0.07
Nodes (24): _boundary_versions(), _clear_caches(), _content_hash(), _default_products(), load_snapshot(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Raw OSV vulnerability records for this product, or [] if the         snapshot do, The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre- (+16 more)

### Community 57 - "Community 57"
Cohesion: 0.06
Nodes (24): _family_of(), PortScanner, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation. (+16 more)

### Community 58 - "Community 58"
Cohesion: 0.11
Nodes (27): _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _decode_oid(), _decode_value(), _encode_oid() (+19 more)

### Community 59 - "Community 59"
Cohesion: 0.09
Nodes (31): config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES, Client, ClientJiraConfig, ClientNotifyConfig (+23 more)

### Community 60 - "Community 60"
Cohesion: 0.07
Nodes (29): classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology(), main(), mdns_hostname(), _nb_encode() (+21 more)

### Community 61 - "Community 61"
Cohesion: 0.07
Nodes (29): classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology(), main(), mdns_hostname(), _nb_encode() (+21 more)

### Community 62 - "Community 62"
Cohesion: 0.11
Nodes (16): _db_scalar(), _FakeDB, _finding(), _GenAI, _GenUnavailable, _one_result(), _operator(), test_remediation_routes.py — Section 5: operator remediation endpoints + wiring. (+8 more)

### Community 63 - "Community 63"
Cohesion: 0.12
Nodes (31): Base, DeclarativeBase, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., AttackTimeline, Append-only ledger of every attack action performed during an engagement.      W, Base, TimestampMixin, DetectionConfig (+23 more)

### Community 64 - "Community 64"
Cohesion: 0.12
Nodes (30): buildToolsCommand(), C, ln(), showSpinner(), downloadFile(), extract(), getInstalledRecord(), installAll() (+22 more)

### Community 65 - "Community 65"
Cohesion: 0.08
Nodes (14): aggregate(), ConsistencyReport, FindingConsistency, format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, run_findings: one list of Findings per run (N runs). Aggregated by     the deter, The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen (+6 more)

### Community 66 - "Community 66"
Cohesion: 0.11
Nodes (25): AuthContext, Handler, generateOtp(), OtpEntry, otpStore, OtpVerifyResult, SessionPayload, verifyOtp() (+17 more)

### Community 67 - "Community 67"
Cohesion: 0.09
Nodes (31): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+23 more)

### Community 68 - "Community 68"
Cohesion: 0.09
Nodes (31): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+23 more)

### Community 69 - "Community 69"
Cohesion: 0.07
Nodes (15): Tests for loader error paths in vuln_db.py and enrichment_db.py.  These are the, The FileNotFoundError message should mention re-syncing, so         operators kn, The ValueError for a hash mismatch must include truncated hashes         in the, A path that doesn't exist must raise FileNotFoundError with a         helpful me, A snapshot whose records don't match the stored content_hash must         raise, Completely broken JSON must propagate as an exception — never         silently y, A JSON file that is valid JSON but missing the 'records' key         must raise, A well-formed snapshot must load without error and return a VulnDB         that (+7 more)

### Community 70 - "Community 70"
Cohesion: 0.12
Nodes (20): AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient, propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Test double — a fixed lookup table, no network. Used to validate the     surroun (+12 more)

### Community 71 - "Community 71"
Cohesion: 0.09
Nodes (31): _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), has_ambiguous_epoch() (+23 more)

### Community 72 - "Community 72"
Cohesion: 0.09
Nodes (16): AssetCriticality, UserRole, OrderedDict, str, parse_csv_assets(), Parse CSV text into a list of AssetIn models and error strings., Add NVD CVSS, EPSS, KEV flag, MITRE techniques, and composite risk.         Muta, Returns {cvss_v3, cvss_vector, description, references, published_date}. (+8 more)

### Community 73 - "Community 73"
Cohesion: 0.15
Nodes (13): AiGenerateRequest, AiGenerateResponse, AiMessage, AiProviderStatus, AiStatusResponse, AiRuntimeError, _is_local_ollama_model(), ManagerLlmService (+5 more)

### Community 74 - "Community 74"
Cohesion: 0.09
Nodes (29): AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError, ExpiredPasswordError, JWTFailureError (+21 more)

### Community 75 - "Community 75"
Cohesion: 0.08
Nodes (20): FindingSeverity, NucleiMatch, boundedEnvMs(), OpenVASFinding, OpenVASHelperOutput, OpenVASTaskState, parseOpenVASHelperOutput(), runOpenVASScanBackground() (+12 more)

### Community 76 - "Community 76"
Cohesion: 0.10
Nodes (17): _compute_priority(), _cache_key(), _clear_caches(), EpssDB, KevDB, load_epss(), load_kev(), enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as vuln_d (+9 more)

### Community 77 - "Community 77"
Cohesion: 0.08
Nodes (15): ATTACK_TIMELINE, AttackAction, correlationRuns, CoverageStats, DetectionOutcome, DetectionResult, detectionStore, EDR_DETECTIONS (+7 more)

### Community 78 - "Community 78"
Cohesion: 0.09
Nodes (25): device_hint(), fuse_liveness(), HostDiscoveryScanner, is_locally_administered(), Neighbor, normalize_mac(), _now(), parse_neighbor_line() (+17 more)

### Community 79 - "Community 79"
Cohesion: 0.07
Nodes (4): _ConcurrencyScanner, _ExplodingScanner, test_host_fanout_is_bounded(), test_per_target_exception_preserves_other_results()

### Community 80 - "Community 80"
Cohesion: 0.08
Nodes (11): Asset, _parse_ts(), PortFact, asset.py — per-host fact model the workflow engine reasons about.  This is an OR, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Dispatch a real ScanResult into the right sub-structure, keyed         on result (+3 more)

### Community 81 - "Community 81"
Cohesion: 0.10
Nodes (19): _metric(), _not_scored(), Pure helpers for controlled Probe capability and accuracy validation., Validate the small, explicit inventory used for accuracy scoring., Score promoted inventory against explicit host/port/service/CVE truth., Resolve suites plus explicit use-cases, preserving first-seen order., Require every IP/CIDR target to be fully allowed and not excluded., Return the conservative number of addresses represented by targets. (+11 more)

### Community 82 - "Community 82"
Cohesion: 0.11
Nodes (9): EvidenceTier, IntEnum, _fact(), TestAsset, TestCorrelateSmbPatch, TestFactRef, TestNormalize, TestNormalizeBanner (+1 more)

### Community 83 - "Community 83"
Cohesion: 0.07
Nodes (19): AdaptiveRateController, expand_targets(), RateLimiter, Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second., A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window). (+11 more)

### Community 84 - "Community 84"
Cohesion: 0.08
Nodes (21): assert_client(), client_scoped(), portal_scope.py — the customer-portal authorization boundary.  Every customer-po, Return the client's bound engagement id, or 403.      403 (never 404) is deliber, Return the client's bound engagement id, or 403.      403 (never 404) is deliber, The safe engagement id to filter by.      A caller-supplied engagement_id is hon, The safe engagement id to filter by.      A caller-supplied engagement_id is hon, The single choke point every portal SELECT must pass through: restricts the (+13 more)

### Community 85 - "Community 85"
Cohesion: 0.12
Nodes (21): _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database(), _check_jwt_secret(), _check_redis(), _check_required_env_vars() (+13 more)

### Community 86 - "Community 86"
Cohesion: 0.10
Nodes (26): _apply_regression_reopen(), create_findings_from_facts(), detect_findings_from_facts(), _engagement_device_roles(), _ensure_importable(), _find_remediated_match(), _persist_attack_paths(), A previously-remediated finding whose issue reappeared this run: reopen     the (+18 more)

### Community 87 - "Community 87"
Cohesion: 0.10
Nodes (20): _netbios_session(), parse_smb2_security_mode(), smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout, _smb1_negotiate(), _smb2_negotiate(), SMBScanner, An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this (+12 more)

### Community 88 - "Community 88"
Cohesion: 0.07
Nodes (6): _EchoProtocol, test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit., TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating, TestWindowStateMachine

### Community 89 - "Community 89"
Cohesion: 0.07
Nodes (8): test_scope_targets.py — the pure scope-authorization core shared by the dispatch, Whatever the validator accepts must be provably inside the scope., test_property_every_accepted_target_is_subnet_of_scope(), TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected, TestTargetsWithinScope

### Community 90 - "Community 90"
Cohesion: 0.10
Nodes (22): Agent, AgentCapability, AGENTS, agentsStore, AgentStatus, ensureDataDir(), FIELD_AGENTS_FILE, FieldAgent (+14 more)

### Community 91 - "Community 91"
Cohesion: 0.10
Nodes (20): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+12 more)

### Community 92 - "Community 92"
Cohesion: 0.09
Nodes (13): port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD, Resolve a named scan profile to a concrete, de-duplicated port list.      'full', Resolve a named scan profile to a concrete, de-duplicated port list.      'full', Resolve a named scan profile to a concrete, de-duplicated port list.      'full', resolve_profile(), test_tarpit.py — tarpit / honeypot detection (task C5).  A tarpit (LaBrea), hone, TestAssessTarpit, TestPortScannerTarpitFlag (+5 more)

### Community 93 - "Community 93"
Cohesion: 0.15
Nodes (12): _added(), _mock_db(), _operator(), _pending_request(), test_customer_access.py — Phase 1: operator provisioning + scan-request inbox. H, An email already used elsewhere in the tenant (the operator's own login,, db.execute yields the given scalar_one_or_none values in order., TestApproveScanRequest (+4 more)

### Community 94 - "Community 94"
Cohesion: 0.13
Nodes (11): ElasticSIEM, _parse_dt(), SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi, Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_, Abstract SIEM connector., Splunk via the REST search endpoint (``/services/search/jobs/export``) with an, SentinelSIEM (+3 more)

### Community 95 - "Community 95"
Cohesion: 0.09
Nodes (14): PortalScan, PortalUseCase, NAV, PortalShell(), PortalShellProps, INTENSITIES, JobCard(), JobMeta (+6 more)

### Community 96 - "Community 96"
Cohesion: 0.12
Nodes (20): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+12 more)

### Community 97 - "Community 97"
Cohesion: 0.12
Nodes (20): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+12 more)

### Community 98 - "Community 98"
Cohesion: 0.11
Nodes (11): Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., TestEnqueueAgentJob, TestListAgents (+3 more)

### Community 99 - "Community 99"
Cohesion: 0.10
Nodes (6): _finding(), test_remediation_generator.py — Section 3: the AI remediation-plan helpers.  Pur, TestGenerateRemediationPlan, TestNormalizeAiPlan, TestParseJsonResponse, TestSafeCommands

### Community 100 - "Community 100"
Cohesion: 0.08
Nodes (7): test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi, TestHttpMatch, TestNoMatch, TestOtherServices, TestProbeLadder, TestScannerIntegration, TestSshMatch

### Community 101 - "Community 101"
Cohesion: 0.11
Nodes (24): assessment(), discovery(), EngagementMode, host_discovery(), includes_stage(), port_scan(), modes.py — engagement mode configurations. Each mode is a thin config that tunes, Discovery + ports + banner only — no deep dives, no credentials. (+16 more)

### Community 102 - "Community 102"
Cohesion: 0.09
Nodes (16): Agent, AIBrainPage(), AiStatus, criticalChain, defaultAgents, Engagement, Finding, findings (+8 more)

### Community 103 - "Community 103"
Cohesion: 0.09
Nodes (18): ADJ, ATTACK_PATHS, AttackPath, BlastRadiusResult, buildAttackPaths(), Chokepoint, CHOKEPOINTS, edgesForPath() (+10 more)

### Community 104 - "Community 104"
Cohesion: 0.13
Nodes (20): NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS (+12 more)

### Community 105 - "Community 105"
Cohesion: 0.08
Nodes (1): TestResultSpool

### Community 106 - "Community 106"
Cohesion: 0.14
Nodes (15): KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline, Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., One aggregate Finding for all kerberoastable accounts.         Severity is Criti, One aggregate Finding for all kerberoastable accounts.         Severity is Criti, Enumerate kerberoastable accounts and capture TGS evidence., Enumerate kerberoastable accounts and capture TGS evidence. (+7 more)

### Community 107 - "Community 107"
Cohesion: 0.15
Nodes (13): _collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, _parse_json_response(), Generate a STRUCTURED, OS-specific remediation plan (dict, not prose)., Generate a STRUCTURED, OS-specific remediation plan (dict, not prose)., Build the structured-remediation prompt. Exploitation signals (EPSS,     exploit (+5 more)

### Community 108 - "Community 108"
Cohesion: 0.13
Nodes (11): make_smb2_error(), make_smb2_success(), test_main_scripts_hardening.py — verifies the Phase-1 correctness fixes applied, A 64-byte SMB2 header. Caller prepends a 4-byte NBT transport prefix, so     Pro, STATUS_INVALID_PARAMETER error response: same header, body StructureSize 9,, _run(), _scope(), _smb2_header() (+3 more)

### Community 109 - "Community 109"
Cohesion: 0.11
Nodes (15): _Socket, test_collector_raises_when_no_listener_binds(), test_ot_udp_backend_never_joins_or_transmits(), test_subset_listener_failure_reports_degraded_coverage(), _Writer, classify_scanner_error(), engine_manifest(), ErrorDetail (+7 more)

### Community 110 - "Community 110"
Cohesion: 0.11
Nodes (7): _cache_with(), test_probe_next_features.py — the probe_next plan: run the improved main_scripts, test_device_inventory_post_stage_classifies_from_open_ports(), test_device_inventory_skips_hosts_without_evidence(), test_exposure_matrix_flags_internet_reachable_ports(), test_exposure_matrix_internal_only_from_lan_vantage(), test_no_post_stage_for_ordinary_scan_types()

### Community 111 - "Community 111"
Cohesion: 0.10
Nodes (22): _bounded_env_int(), _classify_connection_error(), _enroll_device(), _manager_reachable(), _obtain_identity(), Request UI approval, poll, prove key possession, and activate., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64). (+14 more)

### Community 112 - "Community 112"
Cohesion: 0.10
Nodes (18): GzipRequestMiddleware, Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard. (+10 more)

### Community 113 - "Community 113"
Cohesion: 0.14
Nodes (10): CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender, _parse_dt(), EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender, Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi, SentinelOne via the REST ``/web/api/v2.1/threats`` endpoint.     config: {base_u (+2 more)

### Community 114 - "Community 114"
Cohesion: 0.12
Nodes (13): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+5 more)

### Community 115 - "Community 115"
Cohesion: 0.12
Nodes (13): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+5 more)

### Community 116 - "Community 116"
Cohesion: 0.11
Nodes (6): _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_background_job_failed(), test_partial_nuclei_run_preserves_findings_and_diagnostics()

### Community 117 - "Community 117"
Cohesion: 0.13
Nodes (11): _make_http_mock(), Unit tests for VulnEnrichmentService — all external HTTP calls mocked., Create a mock httpx.AsyncClient that returns different responses per URL., test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full(), test_fetch_epss_success() (+3 more)

### Community 118 - "Community 118"
Cohesion: 0.10
Nodes (18): JobResult, Structured result from running one scan job., Submit the result, with spool-and-retry if available., Structured result from running one scan job., Submit the result, with spool-and-retry if available., Submit the result, with spool-and-retry if available., Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Orchestrates one scan job's lifecycle.      The runner holds injected dependenci (+10 more)

### Community 119 - "Community 119"
Cohesion: 0.18
Nodes (9): AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), Raised when the Anthropic SDK or API key is not configured., _tool_result(), _val(), AgentRecommendation (+1 more)

### Community 120 - "Community 120"
Cohesion: 0.13
Nodes (15): attack_path_findings(), _exposed_db_unauth(), _group(), _HostSignals, _is_domain_controller(), _is_network_device(), _legacy_windows(), _ntlm_relay() (+7 more)

### Community 121 - "Community 121"
Cohesion: 0.14
Nodes (16): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con (+8 more)

### Community 122 - "Community 122"
Cohesion: 0.13
Nodes (18): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), MobileScanner, _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd() (+10 more)

### Community 123 - "Community 123"
Cohesion: 0.13
Nodes (15): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+7 more)

### Community 124 - "Community 124"
Cohesion: 0.12
Nodes (15): Protocol, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun (+7 more)

### Community 125 - "Community 125"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 126 - "Community 126"
Cohesion: 0.11
Nodes (20): Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation. (+12 more)

### Community 127 - "Community 127"
Cohesion: 0.14
Nodes (9): DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci, TestGraphVisualizer (+1 more)

### Community 128 - "Community 128"
Cohesion: 0.14
Nodes (11): ApiError, clearAuth(), errorMessage(), fetchJson(), getStoredToken(), isUnauthorized(), storeToken(), btn (+3 more)

### Community 129 - "Community 129"
Cohesion: 0.13
Nodes (14): build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun, Map a host's open ports onto the deep-scanner routes that handle them.     Retur (+6 more)

### Community 130 - "Community 130"
Cohesion: 0.15
Nodes (15): create_scan_request(), _enum_val(), _metric_finding(), portal_engagement(), portal_finding_remediation(), portal_posture(), portal_scans(), portal_summary() (+7 more)

### Community 131 - "Community 131"
Cohesion: 0.13
Nodes (12): _decode_value(), _encode_oid(), _extract_sysdescr(), _oid_in_subtree(), Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli, Return (community, sysdescr) for the first responding community, or None., GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]., One GETBULK request — measure response/request size ratio. (+4 more)

### Community 132 - "Community 132"
Cohesion: 0.17
Nodes (19): aggregate(), build_posture(), _clamp01(), compare(), compute_scores(), _exploit_prob(), FindingView, grade_for() (+11 more)

### Community 133 - "Community 133"
Cohesion: 0.17
Nodes (4): test_agent_policy.py — the pure deterministic agent policy engine., _roe(), TestClassifyAction, TestEvaluateAction

### Community 134 - "Community 134"
Cohesion: 0.10
Nodes (3): _EchoProtocol, test_async_udp.py — tests for the true-async UDP probe helper in scanner_base., _SinkProtocol

### Community 135 - "Community 135"
Cohesion: 0.10
Nodes (1): TestUDPProbeConstruction

### Community 136 - "Community 136"
Cohesion: 0.11
Nodes (5): test_tls_fingerprint.py — Tier 2.3: active TLS fingerprint (JARM methodology)., _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello

### Community 137 - "Community 137"
Cohesion: 0.13
Nodes (10): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., ADAssessmentRunner, ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu (+2 more)

### Community 138 - "Community 138"
Cohesion: 0.13
Nodes (7): BaseScanner, TLSFingerprintScanner, TLSScanner, MobileScanner, Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO, TLSFingerprintScanner, TLSScanner

### Community 139 - "Community 139"
Cohesion: 0.18
Nodes (9): _aware(), DetectionCorrelator, DetectionResultDTO, _host_matches(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale, Normalise naive datetimes to UTC so comparisons never raise., Return a Sigma rule (YAML string) for the technique, customised with the, SigmaRuleGenerator (+1 more)

### Community 140 - "Community 140"
Cohesion: 0.14
Nodes (16): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd(), _probe_mdns_mobile_sync() (+8 more)

### Community 141 - "Community 141"
Cohesion: 0.15
Nodes (7): _client(), _operator(), test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping au, TestAssertClient, TestClientScoped, TestPortalTokenClaims, TestResolveScope

### Community 142 - "Community 142"
Cohesion: 0.19
Nodes (7): CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, _enum_with_entries(), _FakeAttr, _FakeEntry, Unit tests for the Active Directory assessment module (Prompt 5).  All directory, TestLDAPEnumeratorParsing

### Community 143 - "Community 143"
Cohesion: 0.17
Nodes (16): _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError, license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the (+8 more)

### Community 144 - "Community 144"
Cohesion: 0.16
Nodes (9): PathAnalyzer, _priority(), Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for, Assets that appear in more than ``threshold`` (default 50%) of all paths —, Assets reachable (and thus at risk) if ``compromised_asset_id`` is owned., Best (easiest) exploitable finding on an asset: {cvss, weight, finding}., Build (and cache) the Asset→Asset movement projection. Edge weight is the (+1 more)

### Community 145 - "Community 145"
Cohesion: 0.12
Nodes (6): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples., test_main_scripts_adaptive_timeout.py — Phase 7: per-host adaptive probe timeout

### Community 146 - "Community 146"
Cohesion: 0.14
Nodes (8): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =, test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive, _run(), test_protected_redis_raises_no_unauth_finding(), test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_flagged()

### Community 147 - "Community 147"
Cohesion: 0.17
Nodes (9): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages(), _r(), test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ "Multi-vantag (+1 more)

### Community 148 - "Community 148"
Cohesion: 0.15
Nodes (13): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them., Excluded networks -> masscan --exclude specs, so they get ZERO packets., A CIDR spec is in scope only if it is fully contained in an allowed network. (+5 more)

### Community 149 - "Community 149"
Cohesion: 0.22
Nodes (16): _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _decode_oid(), _oid_tlv(), _parse_varbinds() (+8 more)

### Community 150 - "Community 150"
Cohesion: 0.20
Nodes (15): _get(), _ids(), test_attack_path_correlation.py — manager-native composite correlation over prob, test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_device_role_from_facts_also_amplifies(), test_exposed_db_with_unauth_is_critical(), test_exposed_db_without_unauth_does_not_fire() (+7 more)

### Community 151 - "Community 151"
Cohesion: 0.15
Nodes (8): _cloud(), Settings with provider unset and all cloud keys pinned, so .env cannot     leak, test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter(), test_default_auto_detects_the_configured_cloud_provider(), test_default_runtime_fails_closed_without_any_cloud_key(), test_fallback_never_includes_local_ollama(), test_generate_fails_closed_when_no_cloud_provider_configured(), test_status_fails_safe_without_cloud_key()

### Community 152 - "Community 152"
Cohesion: 0.14
Nodes (14): clean_guard_cache(), Tests for the P1+P2 performance optimization of the detection engine.  P1 — vers, dpkg_compare must use the pure-Python comparator in the hot path.     Shelling o, Isolate the guard's in-memory + on-disk validation cache per test., No dpkg binary → nothing to cross-check against; return [] and never     attempt, When the binary disagrees with pure-Python on an adjacent pair, that pair     is, test_clear_caches_forces_reload(), test_dpkg_compare_does_not_call_the_binary() (+6 more)

### Community 153 - "Community 153"
Cohesion: 0.11
Nodes (7): Tests for seed_admin.py.  Covers:   - first deployment: creates tenant + admin,, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset, TestFirstDeployment, TestHashHelpers, TestPasswordRotation

### Community 154 - "Community 154"
Cohesion: 0.21
Nodes (1): TestServiceIdentifier

### Community 155 - "Community 155"
Cohesion: 0.16
Nodes (8): CacheEntry, classify_certainty(), cache.py — (host, port, scanner) -> CacheEntry, so deterministic facts are colle, True if there's no cached entry, OR the entry is uncertain         (always worth, True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, WorkflowCache

### Community 156 - "Community 156"
Cohesion: 0.13
Nodes (7): BloodHoundCollector, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., Run bloodhound-python and return the list of produced JSON file paths.         R, TestBuildADFinding

### Community 157 - "Community 157"
Cohesion: 0.15
Nodes (17): _dbg(), _is_local_manager_url(), main(), _poll_jobs_or_empty(), Bounded reachability preflight. Proceeds the moment the Manager answers     /hea, Poll for work. Auth failures (TransportError) and transient network     failures, Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease. (+9 more)

### Community 158 - "Community 158"
Cohesion: 0.13
Nodes (8): Agent, AGENT_STATUS, AgentStatus, PATH_STATUS, SEV_LABEL, DashboardCharts(), DashboardGrid(), useMouseGradient()

### Community 159 - "Community 159"
Cohesion: 0.13
Nodes (10): ActivityItem, Engagement, Finding, FindingPage, FindingSummary, SEV, STATUS_STYLE, TimelinePoint (+2 more)

### Community 160 - "Community 160"
Cohesion: 0.15
Nodes (14): SeverityChip(), deadlineTitle(), elapsedPct(), pct(), Sev, SEV_STYLE, SlaItem, SlaRowView() (+6 more)

### Community 161 - "Community 161"
Cohesion: 0.18
Nodes (15): addComment(), Case, CaseActivity, CaseComment, CaseSeverity, CaseStatus, createCase(), DATA_FILE (+7 more)

### Community 162 - "Community 162"
Cohesion: 0.14
Nodes (5): DBScanner, interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act

### Community 163 - "Community 163"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 164 - "Community 164"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 165 - "Community 165"
Cohesion: 0.13
Nodes (7): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only., Read the Allow header from an OPTIONS response. Read-only., WebScanner

### Community 166 - "Community 166"
Cohesion: 0.24
Nodes (15): _detect_drift(), _hash(), _log(), log_error(), log_info(), log_warn(), main(), Warn if the tenant has multiple admins or a stale admin email. (+7 more)

### Community 167 - "Community 167"
Cohesion: 0.12
Nodes (1): TestSNMPBerUtilities

### Community 168 - "Community 168"
Cohesion: 0.15
Nodes (7): _fv(), _Row, test_build_posture_buckets_resolved_new_persisting(), test_build_posture_single_run_has_no_prev(), test_compute_scores_uses_risk_epss_exploit_and_asset_criticality(), test_finding_views_handles_null_asset_and_scores(), test_finding_views_maps_columns_and_asset_criticality()

### Community 169 - "Community 169"
Cohesion: 0.18
Nodes (5): _f(), test_remediation_kb.py — the pure deterministic remediation knowledge base., TestClassify, TestRecipeForFinding, TestRecipeShape

### Community 170 - "Community 170"
Cohesion: 0.12
Nodes (1): Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only

### Community 171 - "Community 171"
Cohesion: 0.13
Nodes (16): _check_anti_debug(), Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block (+8 more)

### Community 172 - "Community 172"
Cohesion: 0.13
Nodes (16): _flush_spool_over_http(), Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Re-submit previously spooled results over WebSocket., Re-submit previously spooled results over WebSocket., Poll pending jobs even while WS is connected.      This makes result delivery re, Retry durable result files using the acknowledged HTTP result path., Run one job while keeping WS status/result frames best-effort. (+8 more)

### Community 173 - "Community 173"
Cohesion: 0.14
Nodes (15): bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity(), pubkey_to_bytes(), scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.  T (+7 more)

### Community 174 - "Community 174"
Cohesion: 0.16
Nodes (8): Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh a device token before expiry; legacy identities are unchanged., Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True

### Community 175 - "Community 175"
Cohesion: 0.28
Nodes (8): asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder, is_internet_exposed(), service_node_id(), _to_float()

### Community 176 - "Community 176"
Cohesion: 0.15
Nodes (8): Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., ScopeError, ScopeGuard

### Community 177 - "Community 177"
Cohesion: 0.18
Nodes (13): approve_report(), _build_engagement_summary(), build_posture_report_section(), get_draft(), _output_out(), _pending_outputs(), Deterministic report section from the same posture payload the dashboard uses., Background task: build the summary, generate every section, persist as pending. (+5 more)

### Community 178 - "Community 178"
Cohesion: 0.20
Nodes (15): approve_validation(), create_validation_request(), _default_check_kind(), _get_request_or_404(), list_validation_requests(), _load_finding_and_eng(), Approval-gated safe active-validation API (P3).  POST /engagements/{id}/findings, RoE gate: active validation is allowed unless the engagement's RoE     explicitl (+7 more)

### Community 179 - "Community 179"
Cohesion: 0.17
Nodes (15): _apply_device_profile(), _identity_ip(), process_job_result(), _promote_assets(), Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu, Stable idempotency checksum for one attempt completion payload., Upsert discovered hosts/services into the asset inventory.      Keyed by (engage, Stamp the probe's evidence-based device role onto an Asset (create/update). (+7 more)

### Community 180 - "Community 180"
Cohesion: 0.25
Nodes (15): _mock_session(), _now(), _sql(), test_boundary_at_exactly_the_lease_is_reclaimed(), test_dead_letter_and_requeue_are_mutually_exclusive(), test_dead_letter_stmt_targets_exhausted_stranded_rows(), test_expired_processing_lock_is_reclaimed(), test_fresh_processing_lock_is_not_reclaimed() (+7 more)

### Community 181 - "Community 181"
Cohesion: 0.14
Nodes (6): NTLMRelayChecker, Build a Finding for hosts missing SMB signing. The attack_narrative         incl, Probe SMB/LDAP signing posture across a host list., For each IP, returns {signing_enabled, signing_required}.          A host is rel, Returns True if the DC *enforces* LDAP signing / channel binding.          We at, TestASREPRoastChecker

### Community 182 - "Community 182"
Cohesion: 0.14
Nodes (12): Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed)., Register using a manager-side shared bootstrap key (no user login needed)., Raised when a transport operation fails permanently (not retryable). (+4 more)

### Community 183 - "Community 183"
Cohesion: 0.19
Nodes (8): extract_features(), Fit an XGBoost regressor on historical findings. ``historical_findings_df``, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)., Build the model's feature vector from a Finding (+ optional Asset + extra     co, _to_float(), VulnPrioritizer

### Community 184 - "Community 184"
Cohesion: 0.17
Nodes (14): apply_manual_reopen(), build_coverage(), decide_resolution(), evaluate_resolutions(), host_of(), resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c, Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r, IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin (+6 more)

### Community 185 - "Community 185"
Cohesion: 0.13
Nodes (12): approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest, ExploitEvidence, ExploitJob, ExploitResult (+4 more)

### Community 186 - "Community 186"
Cohesion: 0.15
Nodes (11): OSError, NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here. (+3 more)

### Community 187 - "Community 187"
Cohesion: 0.23
Nodes (7): classify_os_error(), family_of(), main(), parse_ports(), PortScanner, RateLimiter, Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('

### Community 188 - "Community 188"
Cohesion: 0.22
Nodes (2): _action(), TestDetectionCorrelator

### Community 189 - "Community 189"
Cohesion: 0.21
Nodes (12): _cc(), test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detec, A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU., _run(), test_cc_without_negotiation_is_standard_rdp(), test_confirmed_rdp_wins_dedup_over_port_hint(), test_confirmed_rdp_with_nla_has_no_nla_finding(), test_confirmed_rdp_without_nla_is_high_finding() (+4 more)

### Community 190 - "Community 190"
Cohesion: 0.17
Nodes (10): looks_like_db(), looks_like_http(), looks_like_tls(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, True when this port's banner result is exactly the silent-on-garbage     signatu, For every open port with a banner fact, returns {port: {branches}}     that obse, True when a service banner carries a database greeting signature, so a DB     on (+2 more)

### Community 191 - "Community 191"
Cohesion: 0.13
Nodes (5): When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., TestRunnerScopeValidation

### Community 192 - "Community 192"
Cohesion: 0.18
Nodes (12): AgentDeps, AgentOpts, isBlocked(), requiresApproval(), runAutonomousEngagement(), Rung, RUNG_LABELS, AgentState (+4 more)

### Community 193 - "Community 193"
Cohesion: 0.22
Nodes (13): client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId, PhaseRecommendation, planExploit() (+5 more)

### Community 194 - "Community 194"
Cohesion: 0.19
Nodes (5): AttackAction, DetectionGap, Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc, TestEDRParsing, TestSplunkIntegration

### Community 195 - "Community 195"
Cohesion: 0.23
Nodes (13): _all_known_cve_ids(), main(), _query_osv(), update_snapshot.py — the ONLY module in this package that talks to the network., The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, EPSS scores for exactly the CVE IDs this detection run actually cares     about, Some macOS python.org installs ship expecting `Install Certificates.     command, All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n (+5 more)

### Community 196 - "Community 196"
Cohesion: 0.27
Nodes (13): createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), Job, JOBS_FILE (+5 more)

### Community 197 - "Community 197"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 198 - "Community 198"
Cohesion: 0.22
Nodes (12): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None. (+4 more)

### Community 199 - "Community 199"
Cohesion: 0.20
Nodes (4): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect(), WindowsCollector

### Community 200 - "Community 200"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 201 - "Community 201"
Cohesion: 0.16
Nodes (9): interpret_dns_recursion(), interpret_memcached_stats(), interpret_ntp_monlist(), _ntp_monlist_probe(), SIP OPTIONS request — safe fingerprint method., Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, _sip_probe() (+1 more)

### Community 202 - "Community 202"
Cohesion: 0.22
Nodes (12): _manager(), _plant(), test_e2e_engagement_to_findings.py — the whole pipeline in one place.      manag, Exactly what the probe's smb/port scanners emit for a vulnerable host., Return (http_get, submit_result, captured) simulating the manager side., test_correlated_findings_cite_their_base_findings(), test_engagement_dispatch_reaches_probe_and_enforces_scope(), test_manager_correlation_finds_all_three_attack_paths() (+4 more)

### Community 203 - "Community 203"
Cohesion: 0.14
Nodes (4): Pure-logic tests for the ARP/MAC/mobile-detection helpers in host_discovery. No, TestDeviceHint, TestLocallyAdministered, TestVendorLookup

### Community 204 - "Community 204"
Cohesion: 0.33
Nodes (13): _get(), _ids(), test_main_scripts_correlation.py — Epic 2: correlation findings.  Composite, hig, _run(), test_cleartext_cluster_fires_on_two_cleartext_services(), test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_rdp() (+5 more)

### Community 205 - "Community 205"
Cohesion: 0.25
Nodes (5): _mk_scanner(), _scope(), _summary(), TestDefaultsAndAdaptiveTimeout, TestWorkerPoolAndMetrics

### Community 206 - "Community 206"
Cohesion: 0.14
Nodes (1): TestMobileScanner

### Community 207 - "Community 207"
Cohesion: 0.14
Nodes (3): test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te, TestStableHostId, TestVersionChange

### Community 208 - "Community 208"
Cohesion: 0.14
Nodes (1): TestValidateTargetsInScope

### Community 209 - "Community 209"
Cohesion: 0.26
Nodes (7): _db(), _finding(), _operator(), test_sla_policy.py — per-tenant custom SLA windows (item 4)., _row(), TestPolicyAwareCompute, TestSlaPolicyRoutes

### Community 210 - "Community 210"
Cohesion: 0.23
Nodes (11): _probe(), test_vantage_fusion.py — fleet-level reconciliation of exposure_matrix across pr, Build a one-target probe exposure result. `ports` maps 'proto/port' →     {vanta, test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_hint_name(), test_external_vantage_open_makes_port_external(), test_fused_service_exposure_is_keyed_for_service_rows(), test_internal_only_when_no_external_probe_sees_open() (+3 more)

### Community 211 - "Community 211"
Cohesion: 0.22
Nodes (3): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., True when execution produced errors and no usable or cached facts.

### Community 212 - "Community 212"
Cohesion: 0.22
Nodes (6): ADCSChecker, Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM, Read pKICertificateTemplate objects from the Configuration NC.

### Community 213 - "Community 213"
Cohesion: 0.15
Nodes (13): _load_or_create_identity(), Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Release a staged job only after the manager confirms its claim. (+5 more)

### Community 214 - "Community 214"
Cohesion: 0.23
Nodes (12): create_findings_from_probe_result(), create_scan_health_finding(), _escalate_by_exposure(), _find_open_duplicate(), _finding_port(), _map_severity(), A still-relevant Finding with the same (engagement, asset, title), if any., Convert a probe's self-assessed `findings` list into persisted Finding rows. (+4 more)

### Community 215 - "Community 215"
Cohesion: 0.18
Nodes (9): NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here., _run_nmap() (+1 more)

### Community 216 - "Community 216"
Cohesion: 0.18
Nodes (9): _dec(), match_service(), One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., Soft-match collected bytes to {service, product, version}; None if unknown., Soft-match collected bytes to {service, product, version}; None if unknown. (+1 more)

### Community 217 - "Community 217"
Cohesion: 0.18
Nodes (7): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only., Read the Allow header from an OPTIONS response. Read-only., WebScanner

### Community 218 - "Community 218"
Cohesion: 0.36
Nodes (12): _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius(), _build_analyzer(), _critical_asset_ids(), _explain_hop(), get_attack_path() (+4 more)

### Community 219 - "Community 219"
Cohesion: 0.22
Nodes (12): delete_integration(), integration_secret(), IntegrationIn, IntegrationOut, list_integrations(), _out(), put_integration(), integrations.py — operator management of notification integrations (email/Slack/ (+4 more)

### Community 220 - "Community 220"
Cohesion: 0.18
Nodes (9): _dec(), match_service(), One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., Soft-match collected bytes to {service, product, version}; None if unknown., Soft-match collected bytes to {service, product, version}; None if unknown. (+1 more)

### Community 221 - "Community 221"
Cohesion: 0.21
Nodes (11): compute(), default_windows(), SLA policy engine.  Turns a severity + "first seen" timestamp into a remediation, Aggregate SLA states across a set of findings.      Returns counts per state plu, The env-configured SLA windows — the fallback when a tenant has no policy., Aggregate SLA states across a set of findings.      Returns counts per state plu, Compute the SLA state for one finding. Never raises on missing data., Compute the SLA state for one finding. Never raises on missing data.      `windo (+3 more)

### Community 222 - "Community 222"
Cohesion: 0.15
Nodes (1): test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor

### Community 223 - "Community 223"
Cohesion: 0.17
Nodes (3): _fake_cert(), test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced capa, test_ja4x_from_cert_matches_pure_core()

### Community 224 - "Community 224"
Cohesion: 0.36
Nodes (2): _make_scan_record(), TestDeltaEngine

### Community 225 - "Community 225"
Cohesion: 0.26
Nodes (7): FakeProcess, _finding_line(), test_nonzero_exit_retains_and_marks_partial_findings(), test_nonzero_exit_without_findings_raises_with_stderr(), test_run_scan_streams_jsonl_and_separates_timeouts(), test_template_initialization_failure_cannot_be_clean_zero(), test_timeout_retains_findings_emitted_before_termination()

### Community 226 - "Community 226"
Cohesion: 0.22
Nodes (5): _f(), test_portal_metrics.py — pure dashboard aggregations., TestOpenClosed, TestSeverityBreakdown, TestStatusTimeline

### Community 227 - "Community 227"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 228 - "Community 228"
Cohesion: 0.27
Nodes (3): _make_funnel(), Build a funnel with fakes; return (funnel, discovery, port_scanner, created)., TestScanFunnel

### Community 229 - "Community 229"
Cohesion: 0.15
Nodes (5): FakeDiscovery, FakePortScanner, test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel, RecordingDeep, TestScanFunnelRun

### Community 230 - "Community 230"
Cohesion: 0.18
Nodes (3): decode_key(), Verify a Manager-signed policy and return its public key for TOFU pinning., verify_site_policy()

### Community 231 - "Community 231"
Cohesion: 0.17
Nodes (12): check_hw_bind(), get_hw_id(), HWBindError, Raised when the binary is running on an unauthorized machine., Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B, Raised when one or more fatal checks fail — aborts app startup., Raised when one or more fatal checks fail — aborts app startup. (+4 more)

### Community 232 - "Community 232"
Cohesion: 0.26
Nodes (7): HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber(), isOptionalString(), normalizePort(), parseHttpxJsonLine()

### Community 233 - "Community 233"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 234 - "Community 234"
Cohesion: 0.23
Nodes (8): build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure., RDPScanner

### Community 235 - "Community 235"
Cohesion: 0.23
Nodes (7): _netbios_session(), parse_smb2_security_mode(), smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout, _smb1_negotiate(), _smb2_negotiate(), SMBScanner

### Community 236 - "Community 236"
Cohesion: 0.29
Nodes (11): _build_upsert_stmt(), _cached_plan(), generate_remediation(), get_remediation(), remediation.py — per-finding remediation plans (operator-facing).  Two routes on, Fetch a finding scoped to the caller's tenant via its engagement., Build the atomic INSERT … ON CONFLICT DO UPDATE for a cached plan.      Pure (no, Execute the atomic upsert and return the RETURNING row for serialization. (+3 more)

### Community 237 - "Community 237"
Cohesion: 0.29
Nodes (11): get_sla_policy(), _out(), put_sla_policy(), sla_policy.py — operator management of the tenant's custom SLA remediation windo, The tenant's custom SLA windows if set, else the env defaults. Shared by any, resolve_windows(), _row(), SlaPolicyIn (+3 more)

### Community 238 - "Community 238"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 239 - "Community 239"
Cohesion: 0.23
Nodes (8): build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure., RDPScanner

### Community 240 - "Community 240"
Cohesion: 0.17
Nodes (5): _ike_probe(), udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, TFTP RRQ for a non-existent file.  Error reply confirms TFTP service., Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-, _tftp_probe()

### Community 241 - "Community 241"
Cohesion: 0.23
Nodes (11): classify_action(), Decision, _deny(), evaluate_action(), agent_policy.py — the deterministic policy engine for the Autonomous Engagement, Map an action name to its risk tier; unknown actions fail closed., The deterministic authorization envelope for one engagement's agent., Running engagement usage, checked against the blast-radius caps. (+3 more)

### Community 242 - "Community 242"
Cohesion: 0.23
Nodes (11): classify_finding(), _cves(), os_key(), remediation_kb.py — the deterministic remediation knowledge base.  Pure (no DB,, Normalize an arbitrary OS/target string to a supported KB key.      Public becau, Return a structured, OS-filtered remediation plan for `finding`.      Always ret, Map a finding to a KB category key using title/description/CVE hints.      Deter, One remediation step. `generic` is REQUIRED (the vendor-neutral fallback);     p (+3 more)

### Community 243 - "Community 243"
Cohesion: 0.17
Nodes (1): TestAgentJobCompatibility

### Community 244 - "Community 244"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 245 - "Community 245"
Cohesion: 0.17
Nodes (1): test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper

### Community 246 - "Community 246"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()

### Community 247 - "Community 247"
Cohesion: 0.17
Nodes (2): Tests that use the real engine but with no-op callbacks., TestRunnerHeadless

### Community 248 - "Community 248"
Cohesion: 0.27
Nodes (9): _exec(), _finding(), Unit tests for P3 Task 7: validation-result ingestion → finding verdict.  Pure t, test_confirmed_never_overrides_human_closed_finding(), test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_without_touching_status(), test_inconclusive_leaves_finding_unchanged(), test_ingest_confirmed_updates_request_and_finding() (+1 more)

### Community 249 - "Community 249"
Cohesion: 0.18
Nodes (11): _job_intent(), One-line, transparent summary of what a scan actually found so the operator, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort. (+3 more)

### Community 250 - "Community 250"
Cohesion: 0.18
Nodes (9): Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active. (+1 more)

### Community 251 - "Community 251"
Cohesion: 0.18
Nodes (9): Generic authenticated GET, returns parsed JSON or None on failure.          Used, Establish an authenticated WebSocket connection to the manager.          Returns, Refresh a device token before expiry; legacy identities are unchanged., Generic authenticated GET, returns parsed JSON or None on failure.          Used, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used (+1 more)

### Community 252 - "Community 252"
Cohesion: 0.20
Nodes (11): _as_int(), normalize_intensity(), Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile, intensity) for a job.      Resolution order:     1., Coerce an int-or-numeric-string to int, else None (non-numeric)., Map a numeric use-case code → use_case_id (raises on an unknown code)., Accept an intensity as a number (1/2/3) OR a name; return the name.      None st (+3 more)

### Community 253 - "Community 253"
Cohesion: 0.22
Nodes (5): AdaptiveRateController, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window)., A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window).

### Community 254 - "Community 254"
Cohesion: 0.24
Nodes (8): get_finding(), patch_finding(), Operator reverses a resolution (auto or manual). Only a `remediated`     finding, Operator reverses a resolution (auto or manual). Only a `remediated`     finding, Operator reverses a resolution (auto or manual). Only a `remediated`     finding, Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi, reopen_finding(), _tenant_finding()

### Community 255 - "Community 255"
Cohesion: 0.22
Nodes (7): HostDiscoveryScanner, Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., vendor_for_mac()

### Community 256 - "Community 256"
Cohesion: 0.20
Nodes (7): deliver(), enqueue_notification(), notify_tenant(), notifications.py — deliver a message to a tenant's configured integrations (emai, Producer API: enqueue a durable notify event (commits with the caller's txn)., Send via one integration. True on success; False on any handled failure     (log, Deliver to every ENABLED integration for the tenant. Returns the count sent.

### Community 257 - "Community 257"
Cohesion: 0.24
Nodes (10): _is_closed(), MetricFinding, open_closed_counts(), _period(), portal_metrics.py — pure aggregations for the customer dashboard.  Kept pure (no, Count findings by severity (all five buckets always present, zero-filled).     o, (open, closed) totals over the given findings., Per-month {period, opened, closed} for the last `months` months.      opened = f (+2 more)

### Community 258 - "Community 258"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 259 - "Community 259"
Cohesion: 0.18
Nodes (7): Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., TestPromoteAssets

### Community 260 - "Community 260"
Cohesion: 0.29
Nodes (3): _asset(), _finding(), TestVulnPrioritizer

### Community 261 - "Community 261"
Cohesion: 0.18
Nodes (1): TestHallucinationGuard

### Community 262 - "Community 262"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 263 - "Community 263"
Cohesion: 0.35
Nodes (3): _engagement(), _finding(), TestExploitOrchestrator

### Community 264 - "Community 264"
Cohesion: 0.22
Nodes (4): _ext(), test_main_scripts_ja4s.py — JA4S TLS ServerHello fingerprint (advanced capabilit, _serverhello(), test_ja4s_from_serverhello_tls13()

### Community 265 - "Community 265"
Cohesion: 0.18
Nodes (1): TestFingerprintOs

### Community 266 - "Community 266"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 267 - "Community 267"
Cohesion: 0.20
Nodes (2): test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses(), _token()

### Community 268 - "Community 268"
Cohesion: 0.24
Nodes (5): _db_names(), test_probe_simple_approve.py — one-click probe approval helpers (item 5)., db.execute(...).scalars().all() → the given agent-name list., TestNextProbeName, TestSimpleApproveInput

### Community 269 - "Community 269"
Cohesion: 0.18
Nodes (1): TestNmapXMLParser

### Community 270 - "Community 270"
Cohesion: 0.20
Nodes (6): HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Transport

### Community 271 - "Community 271"
Cohesion: 0.31
Nodes (9): _collect(), fuse_exposure_results(), fused_service_exposure(), _is_external(), vantage_fusion.py — fuse the exposure_matrix results of MULTIPLE probes.  A sing, (ip, proto, port) → fused exposure verdict, ready to stamp onto Service rows., (ip → {(proto,port): {vantage: status}}, ip → set(vantages))., Fuse several probes' exposure_matrix results into one per-target matrix.      `r (+1 more)

### Community 272 - "Community 272"
Cohesion: 0.31
Nodes (9): compute_verdict(), _int_confidence(), _qualifies_for_llm(), verification.py — normalized, dashboard-facing verification verdict.  The determ, Deterministic passive verdict from a detection finding's evidence dict., Only spend an LLM call where a rationale / FP-triage is worth it:     uncertain, Deterministic verdict, optionally enriched by an LLM rationale. The LLM     (duc, VerificationVerdict (+1 more)

### Community 273 - "Community 273"
Cohesion: 0.27
Nodes (7): COMMON_RANGES, estimateHostCount(), isValidTarget(), ParseResult, parseTargets(), RFC1918, validOctets()

### Community 274 - "Community 274"
Cohesion: 0.20
Nodes (6): main_entrypoint(), One observation about one target. Pure fact, no interpretation.      Network-sta, One observation about one target. Pure fact, no interpretation.      Network-sta, Run a scanner CLI's body with consistent, operator-friendly error handling., Run a scanner CLI's body with consistent, operator-friendly error handling., ScanResult

### Community 275 - "Community 275"
Cohesion: 0.20
Nodes (9): expand_targets(), Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., Wire argparse args into a scanner instance and execute it., Wire argparse args into a scanner instance and execute it., ResultWriter (+1 more)

### Community 276 - "Community 276"
Cohesion: 0.20
Nodes (10): _agent_token_from_websocket(), agent_websocket_endpoint(), _claim_pushed_job(), Persistent WebSocket for probe → manager push communication.      Authentication, Persistent WebSocket for probe → manager push communication.      Authentication, Read an agent bearer token exclusively from the non-logged auth header., Read an agent bearer token exclusively from the non-logged auth header., Persistent WebSocket for probe → manager push communication.      Query params: (+2 more)

### Community 277 - "Community 277"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 279 - "Community 279"
Cohesion: 0.36
Nodes (5): _db(), _operator(), test_integrations.py — operator notification-integration config (item 3)., TestListIntegrations, TestPutIntegration

### Community 280 - "Community 280"
Cohesion: 0.44
Nodes (9): _metrics(), test_main_scripts_completeness.py — Epic 4: set-based scan-completeness invarian, _rec(), test_duplicate_port_is_detected(), test_fallback_count_based_when_no_requested_set(), test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely_complete() (+1 more)

### Community 281 - "Community 281"
Cohesion: 0.20
Nodes (1): TestClassifyDevice

### Community 282 - "Community 282"
Cohesion: 0.29
Nodes (6): _oserr(), test_main_scripts_errno.py — Phase 2: shared TCP/UDP errno classification.  Veri, test_definitive_states(), test_describe_os_error_is_fully_debuggable(), test_scanner_side_errors_are_error_not_filtered(), test_unknown_errno_is_self_identifying_and_never_filtered()

### Community 283 - "Community 283"
Cohesion: 0.20
Nodes (1): TestIoTScanner

### Community 284 - "Community 284"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 285 - "Community 285"
Cohesion: 0.20
Nodes (2): Each encryption uses a fresh ephemeral key, so blobs are different., TestEncryptDecryptRoundtrip

### Community 286 - "Community 286"
Cohesion: 0.20
Nodes (1): TestSubmitResult

### Community 287 - "Community 287"
Cohesion: 0.44
Nodes (9): _exec(), _mock_db(), Mocked-session unit tests for the P3 active-validation endpoints (Task 4).  No D, test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job(), test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_derives_tls_check(), test_reject_marks_rejected() (+1 more)

### Community 288 - "Community 288"
Cohesion: 0.20
Nodes (7): Push a job to the first online connected agent.          Returns the agent_id th, Push a job to the first online agent in the requested tenant.          Returns t, Push a job to the first online agent in the requested tenant.          Returns t, Return idle connected agents belonging to exactly one tenant., Return idle connected agents belonging to exactly one tenant., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'.

### Community 289 - "Community 289"
Cohesion: 0.20
Nodes (6): AgentConnectionManager, Record transport features explicitly advertised by a connected probe., Record transport features explicitly advertised by a connected probe., Tracks WebSocket connections from probes/agents for direct job push.      Each c, Register an agent's WebSocket connection.          If the agent already has a co, Register an agent's WebSocket connection.          If the agent already has a co

### Community 290 - "Community 290"
Cohesion: 0.31
Nodes (5): HallucinationGuard, Run all relevant checks and return a combined verdict:         ``{valid, issues,, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide.

### Community 291 - "Community 291"
Cohesion: 0.22
Nodes (9): close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, FastAPI dependency that enforces role-based access.      Usage:         @router., require_role(), CurrentUser, Parsed from JWT claims — attached to request.state and injected as dependency. (+1 more)

### Community 292 - "Community 292"
Cohesion: 0.31
Nodes (7): create_access_token(), create_device_access_token(), create_refresh_token(), _now(), Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation.

### Community 293 - "Community 293"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 294 - "Community 294"
Cohesion: 0.28
Nodes (5): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples.

### Community 295 - "Community 295"
Cohesion: 0.22
Nodes (9): Neighbor, normalize_mac(), parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower., One OS neighbor-cache observation about a target, with graded freshness., Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo, Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads, Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower. (+1 more)

### Community 296 - "Community 296"
Cohesion: 0.47
Nodes (3): _mock_db(), _resp(), TestLLMReportGenerator

### Community 297 - "Community 297"
Cohesion: 0.22
Nodes (3): test_notifications.py — integration delivery fan-out (item 3 delivery worker)., TestDeliver, TestNotifyTenant

### Community 298 - "Community 298"
Cohesion: 0.22
Nodes (1): TestTtlInference

### Community 299 - "Community 299"
Cohesion: 0.44
Nodes (5): _client(), _db_scalar(), _finding(), Each db.execute(...) → result whose .scalar_one_or_none() is the next val., TestPortalRemediation

### Community 300 - "Community 300"
Cohesion: 0.22
Nodes (1): TestUseCasesResolve

### Community 301 - "Community 301"
Cohesion: 0.31
Nodes (4): _infos(), test_resolve.py — resolve() address-family selection (task A9)., Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr)., TestResolveFamily

### Community 302 - "Community 302"
Cohesion: 0.39
Nodes (7): _rank(), test_bounds(), test_confirmed_exploitable_outranks_contradicted(), test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lowers(), test_kev_raises_rank(), test_low_confidence_lowers_rank()

### Community 303 - "Community 303"
Cohesion: 0.28
Nodes (8): _py_files(), test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1, Every scanner module authored in main_scripts must exist in scanner/., scanner/ must not carry modules that main_scripts/ does not — otherwise the, Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py., test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_files(), test_scanner_module_matches_main_scripts()

### Community 304 - "Community 304"
Cohesion: 0.22
Nodes (1): TestTargetsInExcludes

### Community 305 - "Community 305"
Cohesion: 0.22
Nodes (1): TestIdentity

### Community 306 - "Community 306"
Cohesion: 0.31
Nodes (8): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 307 - "Community 307"
Cohesion: 0.46
Nodes (8): LLMUnavailableError, LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses, Raised when the Anthropic SDK or API key is not configured., Raised when the Anthropic SDK or API key is not configured., ReviewStatus, LLMOutput, Every LLM generation is persisted here for human-in-the-loop review.      AI out, Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API

### Community 308 - "Community 308"
Cohesion: 0.36
Nodes (3): RateLimiter, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim

### Community 309 - "Community 309"
Cohesion: 0.36
Nodes (7): extractScripts(), NmapHost, NmapScriptResult, NmapService, parseNmapXml(), parser, toArray()

### Community 310 - "Community 310"
Cohesion: 0.46
Nodes (7): _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., _read_jsonl(), _run_stage()

### Community 311 - "Community 311"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 312 - "Community 312"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, loadWordlist(), nativeDirBust(), NativeDirOpts, probe(), ProbeResp

### Community 313 - "Community 313"
Cohesion: 0.32
Nodes (7): attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon(), nativePtrSweep(), PtrSweepResult, safe()

### Community 314 - "Community 314"
Cohesion: 0.32
Nodes (6): fuse_liveness(), _now(), host_discovery.py — determine which hosts are alive, with graded confidence.  ME, Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a, Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a, _state_for_confidence()

### Community 315 - "Community 315"
Cohesion: 0.29
Nodes (8): MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, Run masscan over the given target specs and return its parsed JSON records., Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, _run_masscan()

### Community 316 - "Community 316"
Cohesion: 0.46
Nodes (7): _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., _read_jsonl(), _run_stage()

### Community 317 - "Community 317"
Cohesion: 0.43
Nodes (1): WindowsCollector

### Community 318 - "Community 318"
Cohesion: 0.32
Nodes (7): apply_validation_outcome(), ingest_validation_result(), looks_like_validation_result(), validation_ingest.py — turn a probe's safe active-validation result into a findi, Apply a validation verdict to a finding object (pure — no DB/session)., Cheap gate so normal scan submissions never trigger a lookup: a probe     valida, If ``job_id`` belongs to a ValidationRequest, store the result, set its     outc

### Community 319 - "Community 319"
Cohesion: 0.46
Nodes (7): _ev(), test_confirmed_authoritative_does_not_escalate(), test_high_severity_suspected_escalates_when_roe_allows(), test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_escalate(), test_ot_profile_never_escalates(), test_roe_forbids_blocks_escalation()

### Community 320 - "Community 320"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 321 - "Community 321"
Cohesion: 0.32
Nodes (3): _boundary_test_client(), test_agent_jwt_is_blocked_before_human_route_handler(), test_human_jwt_still_reaches_human_route_handler()

### Community 322 - "Community 322"
Cohesion: 0.54
Nodes (7): _db(), _operator(), test_customer_reveal.py — operator reveal of a customer login password (item 1)., test_reveal_missing_user_is_404(), test_reveal_null_ciphertext_returns_none(), test_reveal_returns_decrypted_password(), _user()

### Community 323 - "Community 323"
Cohesion: 0.25
Nodes (1): test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure

### Community 324 - "Community 324"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 325 - "Community 325"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 326 - "Community 326"
Cohesion: 0.36
Nodes (5): test_main_scripts_datastore_probe.py — safe read-only datastore probes make the, _svc(), test_elasticsearch_and_couchdb_win_over_generic_http(), test_memcached_version_and_stat_identify_as_memcached(), test_redis_info_and_noauth_identify_as_redis()

### Community 328 - "Community 328"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 329 - "Community 329"
Cohesion: 0.36
Nodes (5): test_scan_health.py — the probe scan-metrics → coverage/health verdict.  Guards, _summary(), test_clean_scan_is_healthy_and_does_not_warn(), test_local_resource_errors_flag_degraded(), test_missing_ports_flag_incomplete()

### Community 330 - "Community 330"
Cohesion: 0.29
Nodes (6): _atomic_write_private_state(), Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., _sync_directory()

### Community 331 - "Community 331"
Cohesion: 0.48
Nodes (5): build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()

### Community 332 - "Community 332"
Cohesion: 0.67
Nodes (7): agents/greeting-introduction, main, 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit

### Community 333 - "Community 333"
Cohesion: 0.33
Nodes (6): interpret_validation(), active_validation.py — manager-side decision core for safe active validation.  P, True iff this finding warrants an approval-gated active re-check.     Escalate o, Map a probe safe-check result to a verdict transition. Anything that isn't     a, should_escalate(), ValidationOutcome

### Community 334 - "Community 334"
Cohesion: 0.38
Nodes (6): base_score(), parse_vector(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network, CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r, Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin, _roundup()

### Community 335 - "Community 335"
Cohesion: 0.33
Nodes (4): _as_uuid(), AttackLogger, AttackLogger — records every attack action to the ``attack_timeline`` table.  Al, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 336 - "Community 336"
Cohesion: 0.29
Nodes (5): _deterministic_layout(), GraphVisualizer, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path

### Community 337 - "Community 337"
Cohesion: 0.29
Nodes (6): async_udp_probe(), async_udp_probe_retry(), Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de

### Community 338 - "Community 338"
Cohesion: 0.29
Nodes (3): One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, _UDPProbeProtocol

### Community 339 - "Community 339"
Cohesion: 0.38
Nodes (6): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages()

### Community 340 - "Community 340"
Cohesion: 0.38
Nodes (6): _expand_requested(), _parse_networks(), scope_targets.py — the single source of truth for "is this scan target inside th, Expand raw target tokens (IP / CIDR / ``a-b`` range) into networks.      Returns, Return the normalized list of authorized target networks, or ``None``.      * ``, validate_targets_in_scope()

### Community 341 - "Community 341"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 342 - "Community 342"
Cohesion: 0.29
Nodes (1): TestDeceptionScore

### Community 343 - "Community 343"
Cohesion: 0.29
Nodes (1): TestIngestFile

### Community 344 - "Community 344"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 345 - "Community 345"
Cohesion: 0.29
Nodes (1): test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.

### Community 346 - "Community 346"
Cohesion: 0.48
Nodes (6): _base(), FindingOut computes the explainable risk_rank at serialization (P4 Task 5 wiring, test_confirmed_exploited_outranks_contradicted(), test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_risk_rank_is_computed_not_none()

### Community 347 - "Community 347"
Cohesion: 0.29
Nodes (1): TestNormalizeMac

### Community 348 - "Community 348"
Cohesion: 0.38
Nodes (3): _dry_run(), test_installer_accepts_enroll_token_and_insecure_for_http_manager(), test_installer_without_token_still_shows_manual_approval()

### Community 349 - "Community 349"
Cohesion: 0.29
Nodes (1): TestProfiles

### Community 350 - "Community 350"
Cohesion: 0.48
Nodes (1): TestAcceptEchoReply

### Community 351 - "Community 351"
Cohesion: 0.29
Nodes (1): TestMergeExclusions

### Community 352 - "Community 352"
Cohesion: 0.43
Nodes (3): The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, TestSynRetransmit

### Community 353 - "Community 353"
Cohesion: 0.29
Nodes (5): Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., TestRunnerSubmission

### Community 354 - "Community 354"
Cohesion: 0.29
Nodes (1): TestDeviceEnrollment

### Community 356 - "Community 356"
Cohesion: 0.48
Nodes (6): _b64(), issue(), keygen(), main(), pubkey(), Print the vendor PUBLIC key (hex) derived from the private key.      build/seal-

### Community 357 - "Community 357"
Cohesion: 0.29
Nodes (5): Remove an agent's WebSocket registration., Remove the current registration, optionally only for one socket.          Return, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job

### Community 358 - "Community 358"
Cohesion: 0.38
Nodes (6): expire_attempt(), Expire one fenced attempt; return True when the job may be retried., Expire current attempts and requeue only jobs within their retry budget., Poll loop: requeue expired jobs every reaper_interval_seconds until stopped., reap_once(), run_reaper()

### Community 359 - "Community 359"
Cohesion: 0.33
Nodes (5): True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls.

### Community 360 - "Community 360"
Cohesion: 0.33
Nodes (5): Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce

### Community 361 - "Community 361"
Cohesion: 0.33
Nodes (5): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of

### Community 362 - "Community 362"
Cohesion: 0.33
Nodes (5): Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons

### Community 363 - "Community 363"
Cohesion: 0.33
Nodes (5): Return the WebSocket connection URL with auth token.          The token is passe, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica

### Community 364 - "Community 364"
Cohesion: 0.33
Nodes (6): _normalize_ai_plan(), Extract a step's command(s) and drop any the guard flags as destructive.     Ret, Extract a step's command(s) and drop any the guard flags as destructive.     Ret, Coerce a parsed AI response into the same schema the KB emits, running every, Coerce a parsed AI response into the same schema the KB emits, running every, _safe_commands()

### Community 365 - "Community 365"
Cohesion: 0.40
Nodes (5): exposure_fusion_service.py — apply multi-probe vantage fusion to Service rows., Reconstruct one {"exposure": [...]} dict per probe from persisted facts.      Ea, Fuse all probes' exposure_matrix observations for an engagement and stamp     th, recompute_fused_exposure(), _results_from_scan_rows()

### Community 366 - "Community 366"
Cohesion: 0.40
Nodes (5): asset_type_for(), device_profiles(), device_profile.py — map a probe device_inventory result onto asset fields.  The, The AssetType for a classifier device_type, or None to keep the existing., ip → {asset_type, device_role, role_detail, role_confidence} from a probe     de

### Community 367 - "Community 367"
Cohesion: 0.33
Nodes (5): escalate_for_exposure(), exposure.py — reachability-aware risk from the probe's exposure_matrix use-case., (ip, proto, port) → exposure verdict, from a probe exposure_matrix result., Bump a finding one severity rung when its service is internet-reachable.      On, service_exposure()

### Community 368 - "Community 368"
Cohesion: 0.33
Nodes (3): Apply constraints + indexes (idempotent)., Run a Cypher statement and return records as dicts. [] if not connected., Run a parametrised write with UNWIND batching for bulk node/edge loads.

### Community 369 - "Community 369"
Cohesion: 0.33
Nodes (3): RateLimiter, Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second.

### Community 370 - "Community 370"
Cohesion: 0.40
Nodes (3): BaseScanner, Subclasses implement `scan_target(self, target)` (async), returning a list     o, Subclasses implement `scan_target(self, target)` (async), returning a list     o

### Community 371 - "Community 371"
Cohesion: 0.40
Nodes (5): classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj

### Community 372 - "Community 372"
Cohesion: 0.33
Nodes (6): device_hint(), is_locally_administered(), True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc, Best-effort device classification from the L2/L3 evidence., True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc, Best-effort device classification from the L2/L3 evidence.

### Community 373 - "Community 373"
Cohesion: 0.33
Nodes (3): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect()

### Community 374 - "Community 374"
Cohesion: 0.33
Nodes (1): TestNTLMRelayChecker

### Community 375 - "Community 375"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 376 - "Community 376"
Cohesion: 0.33
Nodes (1): TestCvss

### Community 377 - "Community 377"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 378 - "Community 378"
Cohesion: 0.60
Nodes (5): Unit tests for the dashboard list endpoints (jobs + assets)., _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user()

### Community 379 - "Community 379"
Cohesion: 0.33
Nodes (4): Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., TestTaskRunnerWithEncryptedScope

### Community 380 - "Community 380"
Cohesion: 0.33
Nodes (2): Phase 1: combined scope validation (validate + excludes)., TestScopeValidationPipeline

### Community 381 - "Community 381"
Cohesion: 0.33
Nodes (2): Phase 2: WebSocket message parsing., TestWebSocketMessageProtocol

### Community 382 - "Community 382"
Cohesion: 0.33
Nodes (4): Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup., TestStartupGauntlet

### Community 383 - "Community 383"
Cohesion: 0.33
Nodes (1): test_main_scripts_device_ties.py — Phase 23: device classification never resolve

### Community 384 - "Community 384"
Cohesion: 0.33
Nodes (2): test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti, TestNmapEntityGuard

### Community 385 - "Community 385"
Cohesion: 0.53
Nodes (5): _manifest(), test_probe_manifest.py — the `agent.agent manifest` command that the seal-parity, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_contract()

### Community 386 - "Community 386"
Cohesion: 0.73
Nodes (5): _db_returning(), _finding(), test_covered_clean_medium_finding_is_auto_resolved(), test_db_version_change_blocks_resolution(), test_uncovered_finding_is_left_open()

### Community 388 - "Community 388"
Cohesion: 0.33
Nodes (1): TestFetchEngagementScope

### Community 389 - "Community 389"
Cohesion: 0.33
Nodes (1): TestValidateEnv

### Community 390 - "Community 390"
Cohesion: 0.60
Nodes (1): TestBuildResultsEnrichment

### Community 391 - "Community 391"
Cohesion: 0.33
Nodes (1): TestOptionParsing

### Community 394 - "Community 394"
Cohesion: 0.33
Nodes (2): Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs., TestChooseSourcePort

### Community 395 - "Community 395"
Cohesion: 0.33
Nodes (3): diff_assets(), report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d, re-scan mode's delta report: what changed between two engagements.

### Community 396 - "Community 396"
Cohesion: 0.40
Nodes (5): _load_env(), Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience.

### Community 397 - "Community 397"
Cohesion: 0.40
Nodes (4): DeviceAlreadyEnrolledError, _enrollment_conflict_detail(), The probe's device signing key is already registered as an agent on the     mana, Best-effort extraction of the manager's 409 ``detail`` message.

### Community 398 - "Community 398"
Cohesion: 0.40
Nodes (3): verification_graph.py — optional LangGraph orchestration for passive verificatio, Run passive verification. Uses the LangGraph StateGraph when available;     othe, run_verification()

### Community 399 - "Community 399"
Cohesion: 0.40
Nodes (3): get_settings(), Settings, BaseSettings

### Community 400 - "Community 400"
Cohesion: 0.40
Nodes (5): _finding_views(), posture(), Map joined (Finding, Asset.criticality) rows to duck-typed views., _sev_str(), _two_latest_completed_runs()

### Community 401 - "Community 401"
Cohesion: 0.50
Nodes (3): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =

### Community 403 - "Community 403"
Cohesion: 0.60
Nodes (2): _claim_fixture(), TestAtomicWebSocketClaim

### Community 404 - "Community 404"
Cohesion: 0.40
Nodes (1): TestTenantWebSocketSelection

### Community 405 - "Community 405"
Cohesion: 0.40
Nodes (1): TestGetAgentJobs

### Community 407 - "Community 407"
Cohesion: 0.40
Nodes (1): TestCheckHwBind

### Community 408 - "Community 408"
Cohesion: 0.40
Nodes (2): Phase 1: result spool with upload retry., TestResultSpoolWithRetry

### Community 409 - "Community 409"
Cohesion: 0.40
Nodes (3): Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine., TestTransportWithIdentity

### Community 410 - "Community 410"
Cohesion: 0.40
Nodes (1): TestIcmpBuilders

### Community 411 - "Community 411"
Cohesion: 0.50
Nodes (1): TestIcmpParse

### Community 412 - "Community 412"
Cohesion: 0.60
Nodes (1): TestIcmpTimestamps

### Community 413 - "Community 413"
Cohesion: 0.60
Nodes (4): test_remediation_upsert_integration.py — real-Postgres verification of the remed, _run(), _stmt(), test_upsert_resets_gate_and_is_race_safe()

### Community 414 - "Community 414"
Cohesion: 0.50
Nodes (2): _scope(), TestBuildDefaultFunnel

### Community 415 - "Community 415"
Cohesion: 0.40
Nodes (1): TestRoutePorts

### Community 416 - "Community 416"
Cohesion: 0.70
Nodes (1): TestVerifyReplyCookie

### Community 417 - "Community 417"
Cohesion: 0.40
Nodes (1): TestWebSocket

### Community 418 - "Community 418"
Cohesion: 0.40
Nodes (2): Evasion: blur a fixed scan cadence with a bounded random per-probe delay., TestJitteredDelay

### Community 419 - "Community 419"
Cohesion: 0.40
Nodes (2): Device-role inventory: persist the probe device_classifier's role on assets.  Ad, # NOTE: Postgres cannot DROP a single enum value; the added 'printer' /

### Community 420 - "Community 420"
Cohesion: 0.50
Nodes (4): _load_or_create_signing_identity(), Load or atomically create the probe's Ed25519 enrollment identity., Load or atomically create the probe's Ed25519 enrollment identity., Load or atomically create the probe's Ed25519 enrollment identity.

### Community 421 - "Community 421"
Cohesion: 0.50
Nodes (4): Return {ip: normalized_mac} from the OS neighbor cache.      Tries `ip neigh` (L, Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R, Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R, read_arp_table()

### Community 422 - "Community 422"
Cohesion: 0.67
Nodes (1): SSHCollector

### Community 423 - "Community 423"
Cohesion: 0.83
Nodes (3): _db_with(), test_reopen_non_remediated_is_conflict(), test_reopen_remediated_finding_sets_open_and_audits()

### Community 425 - "Community 425"
Cohesion: 0.83
Nodes (1): TestTimestampFallback

### Community 426 - "Community 426"
Cohesion: 0.83
Nodes (3): _objects(), test_expired_attempt_fails_job_when_retry_budget_is_exhausted(), test_expired_attempt_requeues_with_fence_history_preserved()

### Community 428 - "Community 428"
Cohesion: 0.50
Nodes (1): TestHeartbeat

### Community 429 - "Community 429"
Cohesion: 0.50
Nodes (1): TestHttpGet

### Community 430 - "Community 430"
Cohesion: 0.50
Nodes (1): TestPollJobs

### Community 431 - "Community 431"
Cohesion: 0.50
Nodes (1): TestRefreshRegistration

### Community 432 - "Community 432"
Cohesion: 0.50
Nodes (1): TestRegister

### Community 434 - "Community 434"
Cohesion: 0.50
Nodes (2): Import-time probe constants built from user_agent() must be signature-free., TestModuleConstantsUnbranded

### Community 435 - "Community 435"
Cohesion: 0.50
Nodes (1): Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises

### Community 436 - "Community 436"
Cohesion: 0.50
Nodes (1): Add is_active to users and tenants; add password_expires_at to users.  All exist

### Community 437 - "Community 437"
Cohesion: 0.50
Nodes (1): Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision

### Community 438 - "Community 438"
Cohesion: 0.50
Nodes (1): Finding verification verdict columns (P2 passive verification).  Revision ID: 00

### Community 439 - "Community 439"
Cohesion: 0.50
Nodes (1): Approval-gated safe active-validation requests (P3).  Revision ID: 0022 Revises:

### Community 440 - "Community 440"
Cohesion: 0.50
Nodes (1): Remediation plans — cached, OS-specific, structured remediation for a finding.

### Community 441 - "Community 441"
Cohesion: 0.50
Nodes (1): SLA policies — per-tenant custom remediation windows (hours per severity).  One

### Community 442 - "Community 442"
Cohesion: 0.50
Nodes (1): Integrations — per-tenant notification config (email / Slack / Jira).  One row p

### Community 443 - "Community 443"
Cohesion: 0.50
Nodes (3): Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag

### Community 444 - "Community 444"
Cohesion: 0.50
Nodes (3): Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs.

### Community 445 - "Community 445"
Cohesion: 0.50
Nodes (3): Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.

### Community 446 - "Community 446"
Cohesion: 0.50
Nodes (3): Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy).

### Community 447 - "Community 447"
Cohesion: 0.50
Nodes (3): Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job).

### Community 448 - "Community 448"
Cohesion: 0.67
Nodes (3): interpret_ike(), Parse IKEv1 or IKEv2 response header., Parse IKEv1 or IKEv2 response header.

### Community 449 - "Community 449"
Cohesion: 0.67
Nodes (3): interpret_ipmi(), Parse RMCP Pong; extract supported entities and IPMI capabilities., Parse RMCP Pong; extract supported entities and IPMI capabilities.

### Community 450 - "Community 450"
Cohesion: 0.67
Nodes (3): interpret_mdns(), Return byte count and check QR bit (1 = response)., Return byte count and check QR bit (1 = response).

### Community 451 - "Community 451"
Cohesion: 0.67
Nodes (3): interpret_sip(), Extract SIP version + server header from a SIP response., Extract SIP version + server header from a SIP response.

### Community 452 - "Community 452"
Cohesion: 0.67
Nodes (3): interpret_ssdp(), Extract Location and Server from SSDP response., Extract Location and Server from SSDP response.

### Community 453 - "Community 453"
Cohesion: 0.67
Nodes (3): _ipmi_probe(), RMCP Ping (ASF Presence Ping) to detect IPMI/BMC., RMCP Ping (ASF Presence Ping) to detect IPMI/BMC.

### Community 454 - "Community 454"
Cohesion: 0.67
Nodes (3): _mdns_probe(), mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)., mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353).

### Community 455 - "Community 455"
Cohesion: 0.67
Nodes (3): UPnP/SSDP M-SEARCH — unicast to target:1900., UPnP/SSDP M-SEARCH — unicast to target:1900., _ssdp_probe()

### Community 456 - "Community 456"
Cohesion: 0.67
Nodes (1): risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se

### Community 457 - "Community 457"
Cohesion: 0.67
Nodes (1): TestAgentWebSocketAuthentication

### Community 458 - "Community 458"
Cohesion: 0.67
Nodes (1): TestJobSecretBoundary

### Community 460 - "Community 460"
Cohesion: 0.67
Nodes (2): Record a heartbeat from an agent., Record a heartbeat from an agent.

### Community 462 - "Community 462"
Cohesion: 1.00
Nodes (1): Open the driver and verify connectivity. Returns False on any failure.

### Community 463 - "Community 463"
Cohesion: 1.00
Nodes (1): validation_request.py — an approval-gated request to safely re-check a finding l

### Community 473 - "Community 473"
Cohesion: 1.00
Nodes (1): Fast port discovery with naabu. Feeds port list to Nmap.

### Community 474 - "Community 474"
Cohesion: 1.00
Nodes (1): Nmap service enumeration. Accepts port list from Naabu.

### Community 475 - "Community 475"
Cohesion: 1.00
Nodes (1): Nuclei vulnerability scan — production-ready.

### Community 476 - "Community 476"
Cohesion: 1.00
Nodes (1): Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.

### Community 477 - "Community 477"
Cohesion: 1.00
Nodes (1): NetExec SMB validation: signing, null sessions, SMBv1.

### Community 478 - "Community 478"
Cohesion: 1.00
Nodes (1): testssl.sh TLS/SSL analysis.

### Community 479 - "Community 479"
Cohesion: 1.00
Nodes (1): Extract HTTP/HTTPS URLs from nmap XML output.

### Community 480 - "Community 480"
Cohesion: 1.00
Nodes (1): EyeWitness screenshot evidence collection.

### Community 481 - "Community 481"
Cohesion: 1.00
Nodes (1): Safe lateral movement checks — no actual exploitation.

### Community 482 - "Community 482"
Cohesion: 1.00
Nodes (1): Cloud infrastructure scan (AWS/Azure/GCP).

### Community 483 - "Community 483"
Cohesion: 1.00
Nodes (1): Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.

### Community 484 - "Community 484"
Cohesion: 1.00
Nodes (1): Read a KV-v2 secret from Vault.

### Community 485 - "Community 485"
Cohesion: 1.00
Nodes (1): Verify the Python probe can open what the TypeScript manager sealed (T14 interop

### Community 486 - "Community 486"
Cohesion: 1.00
Nodes (1): Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO

### Community 487 - "Community 487"
Cohesion: 1.00
Nodes (1): Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).

### Community 488 - "Community 488"
Cohesion: 1.00
Nodes (1): End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.

### Community 489 - "Community 489"
Cohesion: 1.00
Nodes (1): Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 490 - "Community 490"
Cohesion: 1.00
Nodes (1): Make a per-host scanner instance share ONE rate limiter + semaphore with all

### Community 491 - "Community 491"
Cohesion: 1.00
Nodes (1): Make a raw banner safe and readable for the summary line.      Many services ans

### Community 492 - "Community 492"
Cohesion: 1.00
Nodes (1): # NOTE: credentialed collectors (ssh_collector, windows_collector) are run

### Community 493 - "Community 493"
Cohesion: 1.00
Nodes (1): ThreadingHTTPServer

## Knowledge Gaps
- **2373 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+2368 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 105`** (1 nodes): `TestResultSpool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 135`** (1 nodes): `TestUDPProbeConstruction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 154`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (1 nodes): `TestSNMPBerUtilities`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 170`** (1 nodes): `Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 188`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (1 nodes): `TestMobileScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (1 nodes): `test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (2 nodes): `_make_scan_record()`, `TestDeltaEngine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (1 nodes): `TestAgentJobCompatibility`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 244`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (1 nodes): `test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (2 nodes): `Tests that use the real engine but with no-op callbacks.`, `TestRunnerHeadless`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (1 nodes): `TestHallucinationGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (1 nodes): `TestFingerprintOs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (2 nodes): `test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()`, `_token()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (1 nodes): `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (1 nodes): `TestClassifyDevice`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (1 nodes): `TestIoTScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 285`** (2 nodes): `Each encryption uses a fresh ephemeral key, so blobs are different.`, `TestEncryptDecryptRoundtrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 286`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 298`** (1 nodes): `TestTtlInference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 300`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 304`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 305`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 311`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 317`** (1 nodes): `WindowsCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 323`** (1 nodes): `test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 328`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 341`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 342`** (1 nodes): `TestDeceptionScore`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 343`** (1 nodes): `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 344`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 345`** (1 nodes): `test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 347`** (1 nodes): `TestNormalizeMac`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 349`** (1 nodes): `TestProfiles`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 350`** (1 nodes): `TestAcceptEchoReply`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 351`** (1 nodes): `TestMergeExclusions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 354`** (1 nodes): `TestDeviceEnrollment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 374`** (1 nodes): `TestNTLMRelayChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 376`** (1 nodes): `TestCvss`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 377`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 380`** (2 nodes): `Phase 1: combined scope validation (validate + excludes).`, `TestScopeValidationPipeline`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 381`** (2 nodes): `Phase 2: WebSocket message parsing.`, `TestWebSocketMessageProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 383`** (1 nodes): `test_main_scripts_device_ties.py — Phase 23: device classification never resolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 384`** (2 nodes): `test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti`, `TestNmapEntityGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 388`** (1 nodes): `TestFetchEngagementScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 389`** (1 nodes): `TestValidateEnv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 390`** (1 nodes): `TestBuildResultsEnrichment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 391`** (1 nodes): `TestOptionParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 394`** (2 nodes): `Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs.`, `TestChooseSourcePort`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 403`** (2 nodes): `_claim_fixture()`, `TestAtomicWebSocketClaim`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 404`** (1 nodes): `TestTenantWebSocketSelection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 405`** (1 nodes): `TestGetAgentJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 407`** (1 nodes): `TestCheckHwBind`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 408`** (2 nodes): `Phase 1: result spool with upload retry.`, `TestResultSpoolWithRetry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 410`** (1 nodes): `TestIcmpBuilders`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 411`** (1 nodes): `TestIcmpParse`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 412`** (1 nodes): `TestIcmpTimestamps`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 414`** (2 nodes): `_scope()`, `TestBuildDefaultFunnel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 415`** (1 nodes): `TestRoutePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 416`** (1 nodes): `TestVerifyReplyCookie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 417`** (1 nodes): `TestWebSocket`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 418`** (2 nodes): `Evasion: blur a fixed scan cadence with a bounded random per-probe delay.`, `TestJitteredDelay`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 419`** (2 nodes): `Device-role inventory: persist the probe device_classifier's role on assets.  Ad`, `# NOTE: Postgres cannot DROP a single enum value; the added 'printer' /`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 422`** (1 nodes): `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 425`** (1 nodes): `TestTimestampFallback`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 428`** (1 nodes): `TestHeartbeat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 429`** (1 nodes): `TestHttpGet`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 430`** (1 nodes): `TestPollJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 431`** (1 nodes): `TestRefreshRegistration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 432`** (1 nodes): `TestRegister`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 434`** (2 nodes): `Import-time probe constants built from user_agent() must be signature-free.`, `TestModuleConstantsUnbranded`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 435`** (1 nodes): `Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 436`** (1 nodes): `Add is_active to users and tenants; add password_expires_at to users.  All exist`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 437`** (1 nodes): `Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 438`** (1 nodes): `Finding verification verdict columns (P2 passive verification).  Revision ID: 00`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 439`** (1 nodes): `Approval-gated safe active-validation requests (P3).  Revision ID: 0022 Revises:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 440`** (1 nodes): `Remediation plans — cached, OS-specific, structured remediation for a finding.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 441`** (1 nodes): `SLA policies — per-tenant custom remediation windows (hours per severity).  One`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 442`** (1 nodes): `Integrations — per-tenant notification config (email / Slack / Jira).  One row p`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 456`** (1 nodes): `risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 457`** (1 nodes): `TestAgentWebSocketAuthentication`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 458`** (1 nodes): `TestJobSecretBoundary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 460`** (2 nodes): `Record a heartbeat from an agent.`, `Record a heartbeat from an agent.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 462`** (1 nodes): `Open the driver and verify connectivity. Returns False on any failure.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 463`** (1 nodes): `validation_request.py — an approval-gated request to safely re-check a finding l`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 473`** (1 nodes): `Fast port discovery with naabu. Feeds port list to Nmap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 474`** (1 nodes): `Nmap service enumeration. Accepts port list from Naabu.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 475`** (1 nodes): `Nuclei vulnerability scan — production-ready.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 476`** (1 nodes): `Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 477`** (1 nodes): `NetExec SMB validation: signing, null sessions, SMBv1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 478`** (1 nodes): `testssl.sh TLS/SSL analysis.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 479`** (1 nodes): `Extract HTTP/HTTPS URLs from nmap XML output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 480`** (1 nodes): `EyeWitness screenshot evidence collection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 481`** (1 nodes): `Safe lateral movement checks — no actual exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 482`** (1 nodes): `Cloud infrastructure scan (AWS/Azure/GCP).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 483`** (1 nodes): `Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 484`** (1 nodes): `Read a KV-v2 secret from Vault.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 485`** (1 nodes): `Verify the Python probe can open what the TypeScript manager sealed (T14 interop`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 486`** (1 nodes): `Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 487`** (1 nodes): `Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 488`** (1 nodes): `End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 489`** (1 nodes): `Deterministic stand-ins emitting realistic output for 127.0.0.1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 490`** (1 nodes): `Make a per-host scanner instance share ONE rate limiter + semaphore with all`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 491`** (1 nodes): `Make a raw banner safe and readable for the summary line.      Many services ans`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 492`** (1 nodes): `# NOTE: credentialed collectors (ssh_collector, windows_collector) are run`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 493`** (1 nodes): `ThreadingHTTPServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 7` to `Community 72`, `Community 212`, `Community 142`, `Community 137`, `Community 156`, `Community 0`, `Community 55`, `Community 106`, `Community 181`, `Community 2`, `Community 258`, `Community 341`, `Community 320`, `Community 374`, `Community 3`, `Community 263`, `Community 32`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `Transport` connect `Community 270` to `Community 4`, `Community 174`, `Community 182`, `Community 330`, `Community 251`, `Community 397`, `Community 250`, `Community 360`, `Community 359`, `Community 361`, `Community 362`, `Community 363`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `FindingStatus` connect `Community 7` to `Community 72`, `Community 55`, `Community 2`, `Community 221`, `Community 142`, `Community 258`, `Community 181`, `Community 341`, `Community 156`, `Community 320`, `Community 374`, `Community 3`, `Community 263`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 173 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 173 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R` to the rest of the system?**
  _2373 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.015873015873015872 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.025137787337007663 - nodes in this community are weakly interconnected._