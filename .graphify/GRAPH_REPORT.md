# Graph Report - .  (2026-08-16)

## Corpus Check
- Large corpus: 885 files · ~758,020 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 8323 nodes · 16585 edges · 479 communities detected
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 2776 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 3760 · calls: 2832 · uses: 2776 · method: 1930 · rationale_for: 1929 · MODIFIES: 1514 · ON_BRANCH: 527 · imports: 516 · imports_from: 468 · inherits: 237 · PARENT_OF: 96


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 885 · Candidates: 1931
- Excluded: 159 untracked · 64026 ignored · 6 sensitive · 1 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `54503ae`
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
Nodes (126): _env_number(), engine.py — adapt a manager scan job to scanner_module's workflow engine and ret, Read a bounded numeric safety setting without trusting the environment., Read a bounded numeric safety setting without trusting the environment., hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit, license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, result_spool.py — local result persistence with upload retry.  When the probe co (+118 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (136): PROFILE_TOOLS, ModuleCategory, ModuleInput, ModuleOutput, modulesForPorts(), ScanModule, bySeverityCount(), runScan() (+128 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (58): BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL, HallucinationGuard — post-generation validation of LLM report text against the g, 298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, d1b4dd3 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, base_score(), parse_vector(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network (+50 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (80): ApiActivity, GET, ManagerAiResponse, 0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner UI, GET, GET, POST, GET (+72 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (69): metadata, AssistantProvider(), PageShell(), PageShellProps, QueryProvider(), Sidebar(), Theme, ThemeContext (+61 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (103): Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Bump severity one rung when the finding's service is internet-reachable     (Ser, GraphBuilder — turns engagement assets/services/findings into an attack graph., Build the full multi-type attack graph. Returns the populated DiGraph         (a, For each exploitable finding add an EXPLOITS edge Finding→Asset with         ``w, Add CONNECTS_TO (directed reachability) and SAME_SEGMENT edges from         segm (+95 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (80): ADError, Shared building blocks for the Active Directory assessment module.  Every AD che, Assemble a Finding-compatible dict.      All findings carry — as required by the, Base class for Active Directory assessment errors., Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, A previously-remediated finding whose issue reappeared this run: reopen     the (+72 more)

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (75): use_cases.py — the finite, pre-defined library of scan scenarios the manager can, backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/probe-usecase-alignment, feat/syn-scanner-osfp-adaptive, feat/user-portal-reskin-scan-request, integration/all-branches, main (+67 more)

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (44): apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl(), Session, SESSION_DIR (+36 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (43): Agent, AGENT_STATUS, AgentStatus, PATH_STATUS, SEV_LABEL, 5d5c158 refactor: remove unused dashboard components and mock data- Deleted SlaSummaryCell and ZoneRow components as they are no longer needed.- Removed mock data file mock-dashboard.ts, which contained static data for the dashboard.- Updated severity handling in severity.ts to support new dashboard design.- Added console-tokens.css for dashboard-specific styles, ensuring theme compatibility., DashboardCharts(), Delta() (+35 more)

### Community 10 - "Community 10"
Cohesion: 0.04
Nodes (50): ComplianceRef, COVERAGE_COLOR, DetectionCoverage, ExploitMaturity, Finding, FindingDetail(), FindingPage, FindingsPage() (+42 more)

### Community 11 - "Community 11"
Cohesion: 0.04
Nodes (61): Agent, AgentStatus, _agent_can_execute_job(), _agent_ownership_check(), AgentRegisterRequest, AgentRegisterResponse, bootstrap_agent(), _encrypt_scope_for_agent() (+53 more)

### Community 12 - "Community 12"
Cohesion: 0.03
Nodes (25): 4d0377d Add unit tests for SMB scanner, SYN scanner, and TLS functionality- Implemented unit tests for SMB scanner to validate security mode parsing and error handling.- Added a new SYN scanner test suite to cover packet crafting, checksum validation, and SYN cookie functionality.- Introduced tests for TLS fingerprinting and posture grading, ensuring accurate classification of cipher suites and TLS versions.- Created integration tests for the TLS scanner against a loopback server to verify posture grading and cipher analysis., 65e5684 feat(probe): transparent job logging (real use-case + result summary), ae08d19 feat(scanner): adaptive timeout, SYN retransmit, top-100 default (accuracy roadmap 1-3), VA scanner module — pure collection/scanning layer.  Each submodule is an indepe, port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD, Resolve a named scan profile to a concrete, de-duplicated port list.      'full', Resolve a named scan profile to a concrete, de-duplicated port list.      'full', resolve_profile() (+17 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (55): A, ask(), askSecret(), banner(), buildInteractiveCommand(), choose(), chooseNextPhase(), confirm() (+47 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (22): DBScanner, interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act, FakeReader, FakeWriter, _probe() (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (37): correlate_smb_patch(), dedup_findings(), _product_from_cpe(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Suppress a suspected/potential (inferred-source) finding when the     SAME host (+29 more)

### Community 16 - "Community 16"
Cohesion: 0.06
Nodes (38): BaseModel, ActivityItem, recent_activity(), AgentBootstrapRequest, AssetIn, AssetOut, BulkAssetImportResult, LoginRequest (+30 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (44): ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is, Raises SafetyViolationError if module or payload is not permitted., Raises SafetyViolationError if module or payload is not permitted., Raises OutOfScopeError if target_ip not in engagement scope., Raises OutOfScopeError if target_ip not in engagement scope., Full exploit execution pipeline with safety, scope, blast radius,         audit, Full exploit execution pipeline with safety, scope, blast radius,         audit, Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo (+36 more)

### Community 18 - "Community 18"
Cohesion: 0.07
Nodes (28): AdvisorFlow(), PATCH_PILL, ExplainResponse, Msg, Served, FactCard(), AiStatus, ModelSelection (+20 more)

### Community 19 - "Community 19"
Cohesion: 0.09
Nodes (45): _as_dict(), build_service_index(), _by_target(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay(), _data(), Finding (+37 more)

### Community 20 - "Community 20"
Cohesion: 0.05
Nodes (29): _ike_probe(), interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats(), interpret_ntp_monlist(), interpret_sip() (+21 more)

### Community 21 - "Community 21"
Cohesion: 0.06
Nodes (35): 54503ae feat(scanner): SYN path harvests OS-fingerprint intel + RTT-adaptive timing, c52feb4 feat(portal): reskin User Portal to console theme + comprehensive dashboard + rich scan form, NAV, build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip() (+27 more)

### Community 22 - "Community 22"
Cohesion: 0.08
Nodes (7): _finding(), TestAggregate, TestClassifyTier, TestComputePriority, TestDedupFindings, TestFindingConsistency, TestVerify

### Community 23 - "Community 23"
Cohesion: 0.07
Nodes (16): _fact(), Tests for ai_normalizer.py — 0% prior coverage.  Covers:   - extract_raw_text: p, Any exception from the AI client yields [] — never raises, never         blocks, When the cache already has an answer, the client must not be called., A candidate dict without a 'product' key must be silently skipped., If the client returns something that isn't a list, return []., Every candidate produced by propose_candidates must be tagged         ai_assiste, source_confidence on the resulting CPECandidate must match the         originati (+8 more)

### Community 24 - "Community 24"
Cohesion: 0.11
Nodes (28): _banner_jsonl(), _empty_epss(), _empty_jsonl(), _empty_kev(), _mock_vuln_db(), _openssh_vuln_db(), Tests for pipeline.py — the orchestrator with 0% prior coverage.  Covers the cri, A completely empty file must not produce any findings. (+20 more)

### Community 25 - "Community 25"
Cohesion: 0.10
Nodes (22): _added(), _client(), _db_first(), _db_for_create(), _db_list(), _db_scalar(), _engagement(), _finding() (+14 more)

### Community 26 - "Community 26"
Cohesion: 0.07
Nodes (16): _make_db(), _make_tenant(), _make_user(), Tests for authentication login flow.  Covers:   - login success   - user_not_fou, Ensure every exception class has the expected reason_code attribute.     These c, AsyncSession mock that returns user on first execute, tenant on second., TestAuthenticateBcryptFailure, TestAuthenticateDatabaseFailure (+8 more)

### Community 27 - "Community 27"
Cohesion: 0.14
Nodes (33): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+25 more)

### Community 28 - "Community 28"
Cohesion: 0.06
Nodes (32): DEMO_ASSET, DEMO_ENGAGEMENT, DEMO_FINDING, AssetInput, chat(), CRITICALITY_SCORE, DESTRUCTIVE_PATTERNS, EPSS_MOCK (+24 more)

### Community 29 - "Community 29"
Cohesion: 0.08
Nodes (9): _asset(), TestAssetNeedsRecheckLive, TestAssetOpenPortsForDeepScan, TestGate2, TestGate3, TestGate4, TestGate5, TestGate6 (+1 more)

### Community 30 - "Community 30"
Cohesion: 0.07
Nodes (28): Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result., Remove the spool file for a successfully uploaded result., Attempt to upload a result with retries and local spool as fallback.          Ar, Move a terminally rejected result out of the retry queue., Re-attempt upload of all previously spooled results.          Called once at pro, Attempt to upload a result with retries and local spool as fallback.          Ar, Number of pending (unsubmitted) results in the spool. (+20 more)

### Community 31 - "Community 31"
Cohesion: 0.09
Nodes (26): AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Raised when the Anthropic SDK or API key is not configured., _tool_result(), _val() (+18 more)

### Community 32 - "Community 32"
Cohesion: 0.08
Nodes (36): all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), normalize(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web() (+28 more)

### Community 33 - "Community 33"
Cohesion: 0.08
Nodes (35): activate_enrollment(), approve_enrollment(), _authenticated_request(), auto_enroll_cidrs(), create_enroll_token(), create_enrollment_request(), _decode_public_key(), _derive_refresh_secret() (+27 more)

### Community 34 - "Community 34"
Cohesion: 0.10
Nodes (39): _as_dict(), build_service_index(), _by_target(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay(), _data(), Finding (+31 more)

### Community 35 - "Community 35"
Cohesion: 0.06
Nodes (40): _claim_batch(), _dead_letter_stale_stmt(), enqueue(), Event, _handle_facts_ready(), is_stale_processing(), main(), _mark_done() (+32 more)

### Community 36 - "Community 36"
Cohesion: 0.07
Nodes (32): build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip(), _parse_mss(), parse_packet(), syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).  WH (+24 more)

### Community 37 - "Community 37"
Cohesion: 0.07
Nodes (29): _ike_probe(), interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats(), interpret_ntp_monlist(), interpret_sip() (+21 more)

### Community 38 - "Community 38"
Cohesion: 0.05
Nodes (20): NAV, PortalShell(), PortalShellProps, ActivityItem, ComplianceControl, ComplianceFramework, ComplianceFrameworkData, Engagement (+12 more)

### Community 39 - "Community 39"
Cohesion: 0.11
Nodes (10): _candidate(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db(), TestEnrichFinding, TestEpssDb, TestKevDb, TestMatchCandidate (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.11
Nodes (37): _ids(), test_main_scripts_findings.py — the findings interpretation layer.  Pure-logic,, _run(), test_accepts_scanresult_objects_not_just_dicts(), test_all_security_headers_present_no_finding(), test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_double_report(), test_confirmed_ftp_cleartext_is_high_confidence() (+29 more)

### Community 41 - "Community 41"
Cohesion: 0.09
Nodes (23): AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator, DatabaseConnectivityValidator, DatabaseURLValidator, DetectionEngineValidator (+15 more)

### Community 42 - "Community 42"
Cohesion: 0.07
Nodes (26): ConnectionManager, GraphWebSocketManager, High-level manager for graph-specific WebSocket operations., Handle a new WebSocket client connection., Handle incoming WebSocket messages., Manages WebSocket connections with room-based broadcasting., Broadcast graph data update to all subscribers., Broadcast a single node update. (+18 more)

### Community 43 - "Community 43"
Cohesion: 0.12
Nodes (23): ADConnectionError, build_ad_finding(), DependencyMissingError, severity_from_str(), ACE, ADComputer, ADGroup, ADUser (+15 more)

### Community 44 - "Community 44"
Cohesion: 0.07
Nodes (24): _boundary_versions(), _clear_caches(), _content_hash(), _default_products(), load_snapshot(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Raw OSV vulnerability records for this product, or [] if the         snapshot do, The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre- (+16 more)

### Community 45 - "Community 45"
Cohesion: 0.11
Nodes (27): _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _decode_oid(), _decode_value(), _encode_oid() (+19 more)

### Community 46 - "Community 46"
Cohesion: 0.07
Nodes (23): classify_os_error(), _family_of(), PortScanner, Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets (+15 more)

### Community 47 - "Community 47"
Cohesion: 0.09
Nodes (31): config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES, Client, ClientJiraConfig, ClientNotifyConfig (+23 more)

### Community 48 - "Community 48"
Cohesion: 0.06
Nodes (32): _finalize_trace(), _gather_per_host(), _port_candidates(), In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl (+24 more)

### Community 49 - "Community 49"
Cohesion: 0.12
Nodes (30): buildToolsCommand(), C, ln(), showSpinner(), downloadFile(), extract(), getInstalledRecord(), installAll() (+22 more)

### Community 50 - "Community 50"
Cohesion: 0.07
Nodes (25): async_udp_probe(), async_udp_probe_retry(), bracket_host(), classify_os_error(), describe_os_error(), expand_targets(), inet_checksum(), parse_ports() (+17 more)

### Community 51 - "Community 51"
Cohesion: 0.06
Nodes (7): test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe +, TestFingerprintOs, TestIcmpBuilders, TestIcmpCapability, TestIcmpParse, TestInetChecksum, TestTtlInference

### Community 52 - "Community 52"
Cohesion: 0.08
Nodes (14): aggregate(), ConsistencyReport, FindingConsistency, format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, run_findings: one list of Findings per run (N runs). Aggregated by     the deter, The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen (+6 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (25): AuthContext, Handler, generateOtp(), OtpEntry, otpStore, OtpVerifyResult, SessionPayload, verifyOtp() (+17 more)

### Community 54 - "Community 54"
Cohesion: 0.09
Nodes (21): GRADE_STYLE, GRADE_VAR, portalApi(), PortalEngagement, PortalFinding, PortalPosture, PortalReport, PortalScan (+13 more)

### Community 55 - "Community 55"
Cohesion: 0.09
Nodes (31): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+23 more)

### Community 56 - "Community 56"
Cohesion: 0.09
Nodes (17): AssetCriticality, UserRole, OrderedDict, str, parse_csv_assets(), Parse CSV text into a list of AssetIn models and error strings., Add NVD CVSS, EPSS, KEV flag, MITRE techniques, and composite risk.         Muta, Returns {cvss_v3, cvss_vector, description, references, published_date}. (+9 more)

### Community 57 - "Community 57"
Cohesion: 0.09
Nodes (31): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+23 more)

### Community 58 - "Community 58"
Cohesion: 0.15
Nodes (13): AiGenerateRequest, AiGenerateResponse, AiMessage, AiProviderStatus, AiStatusResponse, AiRuntimeError, _is_local_ollama_model(), ManagerLlmService (+5 more)

### Community 59 - "Community 59"
Cohesion: 0.07
Nodes (15): Tests for loader error paths in vuln_db.py and enrichment_db.py.  These are the, The FileNotFoundError message should mention re-syncing, so         operators kn, The ValueError for a hash mismatch must include truncated hashes         in the, A path that doesn't exist must raise FileNotFoundError with a         helpful me, A snapshot whose records don't match the stored content_hash must         raise, Completely broken JSON must propagate as an exception — never         silently y, A JSON file that is valid JSON but missing the 'records' key         must raise, A well-formed snapshot must load without error and return a VulnDB         that (+7 more)

### Community 60 - "Community 60"
Cohesion: 0.12
Nodes (20): AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient, propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Test double — a fixed lookup table, no network. Used to validate the     surroun (+12 more)

### Community 61 - "Community 61"
Cohesion: 0.09
Nodes (31): _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), has_ambiguous_epoch() (+23 more)

### Community 62 - "Community 62"
Cohesion: 0.12
Nodes (14): RateLimiter, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim, ServiceIdentifier, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner, Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr (+6 more)

### Community 63 - "Community 63"
Cohesion: 0.09
Nodes (24): NucleiExploitRunner, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Parse nuclei JSONL output for a single CVE PoC result., Parse nuclei JSONL output for a single CVE PoC result., Run Nuclei CVE PoC templates against a single target.     Every template is safe, Run Nuclei CVE PoC templates against a single target.     Every template is safe, Parse template YAML and validate it contains no write/delete/DoS actions. (+16 more)

### Community 64 - "Community 64"
Cohesion: 0.09
Nodes (29): AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError, ExpiredPasswordError, JWTFailureError (+21 more)

### Community 65 - "Community 65"
Cohesion: 0.08
Nodes (20): FindingSeverity, NucleiMatch, boundedEnvMs(), OpenVASFinding, OpenVASHelperOutput, OpenVASTaskState, parseOpenVASHelperOutput(), runOpenVASScanBackground() (+12 more)

### Community 66 - "Community 66"
Cohesion: 0.10
Nodes (17): _compute_priority(), _cache_key(), _clear_caches(), EpssDB, KevDB, load_epss(), load_kev(), enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as vuln_d (+9 more)

### Community 67 - "Community 67"
Cohesion: 0.08
Nodes (15): ATTACK_TIMELINE, AttackAction, correlationRuns, CoverageStats, DetectionOutcome, DetectionResult, detectionStore, EDR_DETECTIONS (+7 more)

### Community 68 - "Community 68"
Cohesion: 0.10
Nodes (29): _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device(), main(), _manager_reachable(), _obtain_identity(), _poll_jobs_or_empty() (+21 more)

### Community 69 - "Community 69"
Cohesion: 0.10
Nodes (19): _metric(), _not_scored(), Pure helpers for controlled Probe capability and accuracy validation., Validate the small, explicit inventory used for accuracy scoring., Score promoted inventory against explicit host/port/service/CVE truth., Resolve suites plus explicit use-cases, preserving first-seen order., Require every IP/CIDR target to be fully allowed and not excluded., Return the conservative number of addresses represented by targets. (+11 more)

### Community 70 - "Community 70"
Cohesion: 0.10
Nodes (26): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response() (+18 more)

### Community 71 - "Community 71"
Cohesion: 0.08
Nodes (17): _family_of(), PortScanner, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation., Requested ports that were never recorded — the silent-skip proof., Requested ports that were never recorded — the silent-skip proof. (+9 more)

### Community 72 - "Community 72"
Cohesion: 0.10
Nodes (26): approve_scan_request(), AssignAgentBody, build_scan_job(), ClientUserCreate, ClientUserOut, ClientUserPatch, CustomerListItem, _existing_client_user() (+18 more)

### Community 73 - "Community 73"
Cohesion: 0.10
Nodes (26): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response() (+18 more)

### Community 74 - "Community 74"
Cohesion: 0.10
Nodes (24): build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), fingerprint_os(), hop_estimate(), _icmp(), icmp_supported(), infer_initial_ttl() (+16 more)

### Community 75 - "Community 75"
Cohesion: 0.08
Nodes (12): _cache_with(), test_probe_next_features.py — the probe_next plan: run the improved main_scripts, test_device_inventory_post_stage_classifies_from_open_ports(), test_device_inventory_skips_hosts_without_evidence(), test_exposure_matrix_flags_internet_reachable_ports(), test_exposure_matrix_internal_only_from_lan_vantage(), test_no_post_stage_for_ordinary_scan_types(), intensity_port_override() (+4 more)

### Community 76 - "Community 76"
Cohesion: 0.11
Nodes (9): EvidenceTier, IntEnum, _fact(), TestAsset, TestCorrelateSmbPatch, TestFactRef, TestNormalize, TestNormalizeBanner (+1 more)

### Community 77 - "Community 77"
Cohesion: 0.11
Nodes (6): _scan_result(), TestAssetMergeCredentialed, TestAssetMergeHostDiscovery, TestAssetMergePortScan, TestClassifyCertainty, TestWorkflowCache

### Community 78 - "Community 78"
Cohesion: 0.11
Nodes (22): device_hint(), fuse_liveness(), HostDiscoveryScanner, is_locally_administered(), Neighbor, normalize_mac(), _now(), parse_neighbor_line() (+14 more)

### Community 79 - "Community 79"
Cohesion: 0.07
Nodes (8): test_scope_targets.py — the pure scope-authorization core shared by the dispatch, Whatever the validator accepts must be provably inside the scope., test_property_every_accepted_target_is_subnet_of_scope(), TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected, TestTargetsWithinScope

### Community 80 - "Community 80"
Cohesion: 0.14
Nodes (19): _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database(), _check_jwt_secret(), _check_redis(), _check_required_env_vars() (+11 more)

### Community 81 - "Community 81"
Cohesion: 0.08
Nodes (26): _apply_regression_reopen(), create_findings_from_facts(), detect_findings_from_facts(), _engagement_device_roles(), _ensure_importable(), _find_remediated_match(), _persist_attack_paths(), A previously-remediated finding whose issue reappeared this run: reopen     the (+18 more)

### Community 82 - "Community 82"
Cohesion: 0.10
Nodes (22): Agent, AgentCapability, AGENTS, agentsStore, AgentStatus, ensureDataDir(), FIELD_AGENTS_FILE, FieldAgent (+14 more)

### Community 83 - "Community 83"
Cohesion: 0.11
Nodes (21): build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), fingerprint_os(), hop_estimate(), _icmp(), icmp_supported(), infer_initial_ttl() (+13 more)

### Community 84 - "Community 84"
Cohesion: 0.15
Nodes (12): _added(), _mock_db(), _operator(), _pending_request(), test_customer_access.py — Phase 1: operator provisioning + scan-request inbox. H, An email already used elsewhere in the tenant (the operator's own login,, db.execute yields the given scalar_one_or_none values in order., TestApproveScanRequest (+4 more)

### Community 85 - "Community 85"
Cohesion: 0.08
Nodes (2): _ExplodingScanner, test_per_target_exception_preserves_other_results()

### Community 86 - "Community 86"
Cohesion: 0.13
Nodes (11): CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender, _parse_dt(), EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender, Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi, SentinelOne via the REST ``/web/api/v2.1/threats`` endpoint.     config: {base_u (+3 more)

### Community 87 - "Community 87"
Cohesion: 0.13
Nodes (11): ElasticSIEM, _parse_dt(), SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi, Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_, Abstract SIEM connector., Splunk via the REST search endpoint (``/services/search/jobs/export``) with an, SentinelSIEM (+3 more)

### Community 88 - "Community 88"
Cohesion: 0.12
Nodes (20): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+12 more)

### Community 89 - "Community 89"
Cohesion: 0.12
Nodes (20): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+12 more)

### Community 90 - "Community 90"
Cohesion: 0.11
Nodes (11): Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., TestEnqueueAgentJob, TestListAgents (+3 more)

### Community 91 - "Community 91"
Cohesion: 0.08
Nodes (7): test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi, TestHttpMatch, TestNoMatch, TestOtherServices, TestProbeLadder, TestScannerIntegration, TestSshMatch

### Community 92 - "Community 92"
Cohesion: 0.11
Nodes (24): assessment(), discovery(), EngagementMode, host_discovery(), includes_stage(), port_scan(), modes.py — engagement mode configurations. Each mode is a thin config that tunes, Discovery + ports + banner only — no deep dives, no credentials. (+16 more)

### Community 93 - "Community 93"
Cohesion: 0.14
Nodes (14): _collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, _normalize_ai_plan(), _parse_json_response(), Generate a STRUCTURED, OS-specific remediation plan (dict, not prose)., Build the structured-remediation prompt. Exploitation signals (EPSS,     exploit (+6 more)

### Community 94 - "Community 94"
Cohesion: 0.09
Nodes (16): Agent, AIBrainPage(), AiStatus, criticalChain, defaultAgents, Engagement, Finding, findings (+8 more)

### Community 95 - "Community 95"
Cohesion: 0.09
Nodes (18): ADJ, ATTACK_PATHS, AttackPath, BlastRadiusResult, buildAttackPaths(), Chokepoint, CHOKEPOINTS, edgesForPath() (+10 more)

### Community 96 - "Community 96"
Cohesion: 0.13
Nodes (20): NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS (+12 more)

### Community 97 - "Community 97"
Cohesion: 0.08
Nodes (1): TestResultSpool

### Community 98 - "Community 98"
Cohesion: 0.08
Nodes (8): Tests for seed_admin.py.  Covers:   - first deployment: creates tenant + admin,, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset, TestFirstDeployment, TestHashHelpers, TestPasswordRotation, TestValidateEnv

### Community 99 - "Community 99"
Cohesion: 0.11
Nodes (8): BaseScanner, TLSFingerprintScanner, TLSScanner, MobileScanner, Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO, TLSFingerprintScanner, TLSScanner, WebScanner

### Community 100 - "Community 100"
Cohesion: 0.09
Nodes (11): 02b6341 feat(active-validation): pure escalation decision core, 58c2d10 feat(active-validation): ValidationRequest model + migration, 7bd104a feat(active-validation): pure result interpretation, interpret_validation(), active_validation.py — manager-side decision core for safe active validation.  P, True iff this finding warrants an approval-gated active re-check.     Escalate o, Map a probe safe-check result to a verdict transition. Anything that isn't     a, should_escalate() (+3 more)

### Community 101 - "Community 101"
Cohesion: 0.20
Nodes (16): AttackAction, _aware(), DetectionCorrelator, DetectionResultDTO, _host_matches(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale, Normalise naive datetimes to UTC so comparisons never raise., AttackLogger — records every attack action to the ``attack_timeline`` table.  Al (+8 more)

### Community 102 - "Community 102"
Cohesion: 0.13
Nodes (11): make_smb2_error(), make_smb2_success(), test_main_scripts_hardening.py — verifies the Phase-1 correctness fixes applied, A 64-byte SMB2 header. Caller prepends a 4-byte NBT transport prefix, so     Pro, STATUS_INVALID_PARAMETER error response: same header, body StructureSize 9,, _run(), _scope(), _smb2_header() (+3 more)

### Community 103 - "Community 103"
Cohesion: 0.14
Nodes (15): KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline, Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., One aggregate Finding for all kerberoastable accounts.         Severity is Criti, One aggregate Finding for all kerberoastable accounts.         Severity is Criti, Enumerate kerberoastable accounts and capture TGS evidence., Enumerate kerberoastable accounts and capture TGS evidence. (+7 more)

### Community 104 - "Community 104"
Cohesion: 0.15
Nodes (11): Exception, MetasploitRPCClient, MetasploitRPCError, Returns {status, output, uuid}., Returns True if job was successfully killed., Poll until job completes or max_wait exceeded., Authenticated RPC call — prepends token., Async Metasploit RPC client using msgpack-over-HTTPS. (+3 more)

### Community 105 - "Community 105"
Cohesion: 0.12
Nodes (13): _dec(), match_service(), service_banner.py — grab service banners and light version strings.  METHOD (col, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., Soft-match collected bytes to {service, product, version}; None if unknown., ServiceBannerScanner (+5 more)

### Community 106 - "Community 106"
Cohesion: 0.11
Nodes (6): _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_background_job_failed(), test_partial_nuclei_run_preserves_findings_and_diagnostics()

### Community 107 - "Community 107"
Cohesion: 0.13
Nodes (11): _make_http_mock(), Unit tests for VulnEnrichmentService — all external HTTP calls mocked., Create a mock httpx.AsyncClient that returns different responses per URL., test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full(), test_fetch_epss_success() (+3 more)

### Community 108 - "Community 108"
Cohesion: 0.10
Nodes (18): JobResult, Structured result from running one scan job., Submit the result, with spool-and-retry if available., Structured result from running one scan job., Submit the result, with spool-and-retry if available., Submit the result, with spool-and-retry if available., Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Orchestrates one scan job's lifecycle.      The runner holds injected dependenci (+10 more)

### Community 109 - "Community 109"
Cohesion: 0.10
Nodes (17): GzipRequestMiddleware, Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., _service_root() (+9 more)

### Community 110 - "Community 110"
Cohesion: 0.13
Nodes (15): attack_path_findings(), _exposed_db_unauth(), _group(), _HostSignals, _is_domain_controller(), _is_network_device(), _legacy_windows(), _ntlm_relay() (+7 more)

### Community 111 - "Community 111"
Cohesion: 0.10
Nodes (9): classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj, Convenience adapter: extract classifier inputs from a list of ScanResult     obj, test_main_scripts_device.py — device-role classification (P0 "Device classificat, TestClassifyDevice (+1 more)

### Community 112 - "Community 112"
Cohesion: 0.14
Nodes (16): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con (+8 more)

### Community 113 - "Community 113"
Cohesion: 0.13
Nodes (18): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), MobileScanner, _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd() (+10 more)

### Community 114 - "Community 114"
Cohesion: 0.13
Nodes (15): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+7 more)

### Community 115 - "Community 115"
Cohesion: 0.12
Nodes (15): Protocol, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun (+7 more)

### Community 116 - "Community 116"
Cohesion: 0.10
Nodes (16): One observation about one target. Pure fact, no interpretation.      Network-sta, Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., One observation about one target. Pure fact, no interpretation., One observation about one target. Pure fact, no interpretation., Writes ScanResult objects as JSONL to a file and/or stdout., Wire argparse args into a scanner instance and execute it., Writes ScanResult objects as JSONL to a file and/or stdout. (+8 more)

### Community 117 - "Community 117"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 118 - "Community 118"
Cohesion: 0.10
Nodes (9): Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG, TestAssetMergePassiveCollect, TestAssetMergeServiceBanner, TestAssetMergeSmbScan, TestAssetMergeTlsScan, TestAssetMergeUnknownScanner, TestAssetMergeWebScan, TestCacheEntry (+1 more)

### Community 119 - "Community 119"
Cohesion: 0.11
Nodes (20): Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation. (+12 more)

### Community 120 - "Community 120"
Cohesion: 0.14
Nodes (9): DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci, TestGraphVisualizer (+1 more)

### Community 121 - "Community 121"
Cohesion: 0.14
Nodes (11): ApiError, clearAuth(), errorMessage(), fetchJson(), getStoredToken(), isUnauthorized(), storeToken(), btn (+3 more)

### Community 122 - "Community 122"
Cohesion: 0.13
Nodes (14): build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun, Map a host's open ports onto the deep-scanner routes that handle them.     Retur (+6 more)

### Community 123 - "Community 123"
Cohesion: 0.13
Nodes (12): _decode_value(), _encode_oid(), _extract_sysdescr(), _oid_in_subtree(), Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli, Return (community, sysdescr) for the first responding community, or None., GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]., One GETBULK request — measure response/request size ratio. (+4 more)

### Community 124 - "Community 124"
Cohesion: 0.14
Nodes (18): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it. (+10 more)

### Community 125 - "Community 125"
Cohesion: 0.17
Nodes (19): aggregate(), build_posture(), _clamp01(), compare(), compute_scores(), _exploit_prob(), FindingView, grade_for() (+11 more)

### Community 126 - "Community 126"
Cohesion: 0.10
Nodes (3): _EchoProtocol, test_async_udp.py — tests for the true-async UDP probe helper in scanner_base., _SinkProtocol

### Community 127 - "Community 127"
Cohesion: 0.10
Nodes (1): TestUDPProbeConstruction

### Community 128 - "Community 128"
Cohesion: 0.11
Nodes (5): test_tls_fingerprint.py — Tier 2.3: active TLS fingerprint (JARM methodology)., _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello

### Community 129 - "Community 129"
Cohesion: 0.12
Nodes (4): _modern(), test_tls_posture.py — Tier 2.4: cipher-suite classification + TLS posture gradin, TestClassifyCipher, TestGradeTlsPosture

### Community 130 - "Community 130"
Cohesion: 0.13
Nodes (10): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., ADAssessmentRunner, ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu (+2 more)

### Community 131 - "Community 131"
Cohesion: 0.15
Nodes (10): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+2 more)

### Community 132 - "Community 132"
Cohesion: 0.14
Nodes (16): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd(), _probe_mdns_mobile_sync() (+8 more)

### Community 133 - "Community 133"
Cohesion: 0.11
Nodes (14): async_udp_probe(), async_udp_probe_retry(), One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, Send one UDP datagram and await the first reply — fully on the event loop., One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, Send one UDP datagram and await the first reply — fully on the event loop., Send one UDP datagram and await the first reply — fully on the event loop. (+6 more)

### Community 134 - "Community 134"
Cohesion: 0.12
Nodes (11): Read-only view of allowed networks (for CIDR-level engines)., Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude)., Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i (+3 more)

### Community 135 - "Community 135"
Cohesion: 0.15
Nodes (7): _client(), _operator(), test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping au, TestAssertClient, TestClientScoped, TestPortalTokenClaims, TestResolveScope

### Community 136 - "Community 136"
Cohesion: 0.14
Nodes (4): Asset, _parse_ts(), PortFact, asset.py — per-host fact model the workflow engine reasons about.  This is an OR

### Community 137 - "Community 137"
Cohesion: 0.19
Nodes (7): CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, _enum_with_entries(), _FakeAttr, _FakeEntry, Unit tests for the Active Directory assessment module (Prompt 5).  All directory, TestLDAPEnumeratorParsing

### Community 138 - "Community 138"
Cohesion: 0.16
Nodes (9): PathAnalyzer, _priority(), Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for, Assets that appear in more than ``threshold`` (default 50%) of all paths —, Assets reachable (and thus at risk) if ``compromised_asset_id`` is owned., Best (easiest) exploitable finding on an asset: {cvss, weight, finding}., Build (and cache) the Asset→Asset movement projection. Edge weight is the (+1 more)

### Community 139 - "Community 139"
Cohesion: 0.12
Nodes (6): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples., test_main_scripts_adaptive_timeout.py — Phase 7: per-host adaptive probe timeout

### Community 140 - "Community 140"
Cohesion: 0.13
Nodes (8): BaseScanner, main_entrypoint(), RateLimiter, One observation about one target. Pure fact, no interpretation.      Network-sta, Simple async rate limiter: at most `rate` operations per second., Subclasses implement `scan_target(self, target)` (async), returning a list     o, Run a scanner CLI's body with consistent, operator-friendly error handling., ScanResult

### Community 141 - "Community 141"
Cohesion: 0.14
Nodes (8): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =, test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive, _run(), test_protected_redis_raises_no_unauth_finding(), test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_flagged()

### Community 142 - "Community 142"
Cohesion: 0.15
Nodes (13): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them., Excluded networks -> masscan --exclude specs, so they get ZERO packets., A CIDR spec is in scope only if it is fully contained in an allowed network. (+5 more)

### Community 143 - "Community 143"
Cohesion: 0.14
Nodes (14): _coverage(), _device_hint(), _listener_error_code(), _open_listener(), PassiveListenerError, _printable_strings(), passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)., All passive sources failed before the listen window could start. (+6 more)

### Community 144 - "Community 144"
Cohesion: 0.22
Nodes (16): _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _decode_oid(), _oid_tlv(), _parse_varbinds() (+8 more)

### Community 145 - "Community 145"
Cohesion: 0.11
Nodes (5): _EchoProtocol, test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit., TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating

### Community 146 - "Community 146"
Cohesion: 0.20
Nodes (15): _get(), _ids(), test_attack_path_correlation.py — manager-native composite correlation over prob, test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_device_role_from_facts_also_amplifies(), test_exposed_db_with_unauth_is_critical(), test_exposed_db_without_unauth_does_not_fire() (+7 more)

### Community 147 - "Community 147"
Cohesion: 0.15
Nodes (8): _cloud(), Settings with provider unset and all cloud keys pinned, so .env cannot     leak, test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter(), test_default_auto_detects_the_configured_cloud_provider(), test_default_runtime_fails_closed_without_any_cloud_key(), test_fallback_never_includes_local_ollama(), test_generate_fails_closed_when_no_cloud_provider_configured(), test_status_fails_safe_without_cloud_key()

### Community 148 - "Community 148"
Cohesion: 0.14
Nodes (14): clean_guard_cache(), Tests for the P1+P2 performance optimization of the detection engine.  P1 — vers, dpkg_compare must use the pure-Python comparator in the hot path.     Shelling o, Isolate the guard's in-memory + on-disk validation cache per test., No dpkg binary → nothing to cross-check against; return [] and never     attempt, When the binary disagrees with pure-Python on an adjacent pair, that pair     is, test_clear_caches_forces_reload(), test_dpkg_compare_does_not_call_the_binary() (+6 more)

### Community 149 - "Community 149"
Cohesion: 0.21
Nodes (1): TestServiceIdentifier

### Community 150 - "Community 150"
Cohesion: 0.13
Nodes (7): BloodHoundCollector, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., Run bloodhound-python and return the list of produced JSON file paths.         R, TestBuildADFinding

### Community 151 - "Community 151"
Cohesion: 0.14
Nodes (15): AgentDeps, AgentOpts, _is_local_manager_url(), isBlocked(), Recognize only explicit single-host development/Compose manager names., Recognize only explicit single-host development/Compose manager names., requiresApproval(), runAutonomousEngagement() (+7 more)

### Community 152 - "Community 152"
Cohesion: 0.18
Nodes (9): extract_features(), VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal, Fit an XGBoost regressor on historical findings. ``historical_findings_df``, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)., Build the model's feature vector from a Finding (+ optional Asset + extra     co, _to_float() (+1 more)

### Community 153 - "Community 153"
Cohesion: 0.15
Nodes (16): assert_client(), client_scoped(), portal_scope.py — the customer-portal authorization boundary.  Every customer-po, Return the client's bound engagement id, or 403.      403 (never 404) is deliber, Return the client's bound engagement id, or 403.      403 (never 404) is deliber, The safe engagement id to filter by.      A caller-supplied engagement_id is hon, The safe engagement id to filter by.      A caller-supplied engagement_id is hon, The single choke point every portal SELECT must pass through: restricts the (+8 more)

### Community 154 - "Community 154"
Cohesion: 0.13
Nodes (8): 1d5ae94 feat(fleet): live "Connected probes" status section, 88c9278 feat(ai): pin manager LLM pipeline to Claude Sonnet 4.6, c4386e4 feat(customers): operator Customers dashboard + per-customer portal slug, EnrollmentRequest, FleetResponse, inputStyle, Probe, Client portal slug — the customer's stable 'user as domain' handle.  Adds users.

### Community 155 - "Community 155"
Cohesion: 0.13
Nodes (10): ActivityItem, Engagement, Finding, FindingPage, FindingSummary, SEV, STATUS_STYLE, TimelinePoint (+2 more)

### Community 156 - "Community 156"
Cohesion: 0.15
Nodes (14): SeverityChip(), deadlineTitle(), elapsedPct(), pct(), Sev, SEV_STYLE, SlaItem, SlaRowView() (+6 more)

### Community 157 - "Community 157"
Cohesion: 0.18
Nodes (15): addComment(), Case, CaseActivity, CaseComment, CaseSeverity, CaseStatus, createCase(), DATA_FILE (+7 more)

### Community 158 - "Community 158"
Cohesion: 0.14
Nodes (5): DBScanner, interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act

### Community 159 - "Community 159"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 160 - "Community 160"
Cohesion: 0.18
Nodes (11): _enum_val(), _metric_finding(), portal_engagement(), portal_finding_remediation(), portal_posture(), portal_scans(), portal_summary(), portal_trends() (+3 more)

### Community 161 - "Community 161"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 162 - "Community 162"
Cohesion: 0.13
Nodes (11): AdaptiveRateController, expand_targets(), A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window)., Current integer window (>= min_window)., Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10 (+3 more)

### Community 163 - "Community 163"
Cohesion: 0.13
Nodes (14): bracket_host(), classify_os_error(), describe_os_error(), inet_checksum(), scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD, Full, debuggable classification for attaching to a ScanResult: state,     reason, Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP,, Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h (+6 more)

### Community 164 - "Community 164"
Cohesion: 0.24
Nodes (15): _detect_drift(), _hash(), _log(), log_error(), log_info(), log_warn(), main(), Warn if the tenant has multiple admins or a stale admin email. (+7 more)

### Community 165 - "Community 165"
Cohesion: 0.22
Nodes (6): _mk_scanner(), test_main_scripts_coverage.py — P0 coverage + self-health capabilities added to, _scope(), _summary(), TestDefaultsAndAdaptiveTimeout, TestWorkerPoolAndMetrics

### Community 166 - "Community 166"
Cohesion: 0.12
Nodes (1): TestSNMPBerUtilities

### Community 167 - "Community 167"
Cohesion: 0.15
Nodes (7): _fv(), _Row, test_build_posture_buckets_resolved_new_persisting(), test_build_posture_single_run_has_no_prev(), test_compute_scores_uses_risk_epss_exploit_and_asset_criticality(), test_finding_views_handles_null_asset_and_scores(), test_finding_views_maps_columns_and_asset_criticality()

### Community 168 - "Community 168"
Cohesion: 0.12
Nodes (1): Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only

### Community 169 - "Community 169"
Cohesion: 0.13
Nodes (16): _check_anti_debug(), Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block (+8 more)

### Community 170 - "Community 170"
Cohesion: 0.13
Nodes (16): _flush_spool_over_http(), Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Re-submit previously spooled results over WebSocket., Re-submit previously spooled results over WebSocket., Poll pending jobs even while WS is connected.      This makes result delivery re, Retry durable result files using the acknowledged HTTP result path., Run one job while keeping WS status/result frames best-effort. (+8 more)

### Community 171 - "Community 171"
Cohesion: 0.15
Nodes (15): _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Stable per-machine ID, derived from hw_bind's hardware fingerprint. (+7 more)

### Community 172 - "Community 172"
Cohesion: 0.14
Nodes (11): 35f02a9 feat(portal): rich scan request (type/targets/intensity) + dashboard endpoints, c140451 fix(portal): clean 409 on duplicate-email provision + 7-day session refresh, f00ce5f fix(ui): session-timer persistence, hydration-safe count-up, security headers, page-title polish, scan_request.py — a customer-initiated, operator-approved request to run a scan, _expand_requested(), _parse_networks(), scope_targets.py — the single source of truth for "is this scan target inside th, Expand raw target tokens (IP / CIDR / ``a-b`` range) into networks.      Returns (+3 more)

### Community 173 - "Community 173"
Cohesion: 0.17
Nodes (6): DetectionGap, Return a Sigma rule (YAML string) for the technique, customised with the, SigmaRuleGenerator, _stable_rule_id(), Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc, TestEDRParsing

### Community 174 - "Community 174"
Cohesion: 0.28
Nodes (8): asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder, is_internet_exposed(), service_node_id(), _to_float()

### Community 175 - "Community 175"
Cohesion: 0.18
Nodes (13): approve_report(), _build_engagement_summary(), build_posture_report_section(), get_draft(), _output_out(), _pending_outputs(), Deterministic report section from the same posture payload the dashboard uses., Background task: build the summary, generate every section, persist as pending. (+5 more)

### Community 176 - "Community 176"
Cohesion: 0.20
Nodes (15): approve_validation(), create_validation_request(), _default_check_kind(), _get_request_or_404(), list_validation_requests(), _load_finding_and_eng(), Approval-gated safe active-validation API (P3).  POST /engagements/{id}/findings, RoE gate: active validation is allowed unless the engagement's RoE     explicitl (+7 more)

### Community 177 - "Community 177"
Cohesion: 0.25
Nodes (15): _mock_session(), _now(), _sql(), test_boundary_at_exactly_the_lease_is_reclaimed(), test_dead_letter_and_requeue_are_mutually_exclusive(), test_dead_letter_stmt_targets_exhausted_stranded_rows(), test_expired_processing_lock_is_reclaimed(), test_fresh_processing_lock_is_not_reclaimed() (+7 more)

### Community 178 - "Community 178"
Cohesion: 0.14
Nodes (6): NTLMRelayChecker, Build a Finding for hosts missing SMB signing. The attack_narrative         incl, Probe SMB/LDAP signing posture across a host list., For each IP, returns {signing_enabled, signing_required}.          A host is rel, Returns True if the DC *enforces* LDAP signing / channel binding.          We at, TestASREPRoastChecker

### Community 179 - "Community 179"
Cohesion: 0.17
Nodes (7): Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh a device token before expiry; legacy identities are unchanged., Refresh routing metadata using the cached agent identity.          Returns True

### Community 180 - "Community 180"
Cohesion: 0.17
Nodes (14): apply_manual_reopen(), build_coverage(), decide_resolution(), evaluate_resolutions(), host_of(), resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c, Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r, IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin (+6 more)

### Community 181 - "Community 181"
Cohesion: 0.13
Nodes (12): approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest, ExploitEvidence, ExploitJob, ExploitResult (+4 more)

### Community 182 - "Community 182"
Cohesion: 0.23
Nodes (7): classify_os_error(), family_of(), main(), parse_ports(), PortScanner, RateLimiter, Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('

### Community 183 - "Community 183"
Cohesion: 0.22
Nodes (2): _action(), TestDetectionCorrelator

### Community 184 - "Community 184"
Cohesion: 0.21
Nodes (12): _cc(), test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detec, A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU., _run(), test_cc_without_negotiation_is_standard_rdp(), test_confirmed_rdp_wins_dedup_over_port_hint(), test_confirmed_rdp_with_nla_has_no_nla_finding(), test_confirmed_rdp_without_nla_is_high_finding() (+4 more)

### Community 185 - "Community 185"
Cohesion: 0.17
Nodes (10): looks_like_db(), looks_like_http(), looks_like_tls(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, True when this port's banner result is exactly the silent-on-garbage     signatu, For every open port with a banner fact, returns {port: {branches}}     that obse, True when a service banner carries a database greeting signature, so a DB     on (+2 more)

### Community 186 - "Community 186"
Cohesion: 0.17
Nodes (13): An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this, The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was     rea, A response with the wrong body StructureSize is not a valid NEGOTIATE., Step 13: expose signing_supported (protocol-precise), not only the     ambiguous, Offering SMB 3.1.1 with no preauth-integrity negotiate context makes     Windows, _smb2_error_response(), _smb2_negotiate_response(), test_error_response_not_parsed_as_signing() (+5 more)

### Community 187 - "Community 187"
Cohesion: 0.13
Nodes (5): When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., TestRunnerScopeValidation

### Community 188 - "Community 188"
Cohesion: 0.22
Nodes (13): client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId, PhaseRecommendation, planExploit() (+5 more)

### Community 189 - "Community 189"
Cohesion: 0.23
Nodes (13): _all_known_cve_ids(), main(), _query_osv(), update_snapshot.py — the ONLY module in this package that talks to the network., The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, EPSS scores for exactly the CVE IDs this detection run actually cares     about, Some macOS python.org installs ship expecting `Install Certificates.     command, All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n (+5 more)

### Community 190 - "Community 190"
Cohesion: 0.27
Nodes (13): createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), Job, JOBS_FILE (+5 more)

### Community 191 - "Community 191"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 192 - "Community 192"
Cohesion: 0.22
Nodes (12): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None. (+4 more)

### Community 193 - "Community 193"
Cohesion: 0.20
Nodes (4): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect(), WindowsCollector

### Community 194 - "Community 194"
Cohesion: 0.16
Nodes (10): OSError, NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here., # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree (+2 more)

### Community 195 - "Community 195"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 196 - "Community 196"
Cohesion: 0.22
Nodes (12): _manager(), _plant(), test_e2e_engagement_to_findings.py — the whole pipeline in one place.      manag, Exactly what the probe's smb/port scanners emit for a vulnerable host., Return (http_get, submit_result, captured) simulating the manager side., test_correlated_findings_cite_their_base_findings(), test_engagement_dispatch_reaches_probe_and_enforces_scope(), test_manager_correlation_finds_all_three_attack_paths() (+4 more)

### Community 197 - "Community 197"
Cohesion: 0.14
Nodes (4): Pure-logic tests for the ARP/MAC/mobile-detection helpers in host_discovery. No, TestDeviceHint, TestLocallyAdministered, TestVendorLookup

### Community 198 - "Community 198"
Cohesion: 0.33
Nodes (13): _get(), _ids(), test_main_scripts_correlation.py — Epic 2: correlation findings.  Composite, hig, _run(), test_cleartext_cluster_fires_on_two_cleartext_services(), test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_rdp() (+5 more)

### Community 199 - "Community 199"
Cohesion: 0.14
Nodes (1): TestMobileScanner

### Community 200 - "Community 200"
Cohesion: 0.14
Nodes (3): test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te, TestStableHostId, TestVersionChange

### Community 201 - "Community 201"
Cohesion: 0.14
Nodes (1): TestValidateTargetsInScope

### Community 202 - "Community 202"
Cohesion: 0.23
Nodes (11): _probe(), test_vantage_fusion.py — fleet-level reconciliation of exposure_matrix across pr, Build a one-target probe exposure result. `ports` maps 'proto/port' →     {vanta, test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_hint_name(), test_external_vantage_open_makes_port_external(), test_fused_service_exposure_is_keyed_for_service_rows(), test_internal_only_when_no_external_probe_sees_open() (+3 more)

### Community 203 - "Community 203"
Cohesion: 0.20
Nodes (5): CacheEntry, classify_certainty(), True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, WorkflowCache

### Community 204 - "Community 204"
Cohesion: 0.22
Nodes (3): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., True when execution produced errors and no usable or cached facts.

### Community 205 - "Community 205"
Cohesion: 0.22
Nodes (6): ADCSChecker, Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM, Read pKICertificateTemplate objects from the Configuration NC.

### Community 206 - "Community 206"
Cohesion: 0.15
Nodes (13): _load_or_create_identity(), Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Release a staged job only after the manager confirms its claim. (+5 more)

### Community 207 - "Community 207"
Cohesion: 0.17
Nodes (10): Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed)., Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable). (+2 more)

### Community 208 - "Community 208"
Cohesion: 0.23
Nodes (12): create_findings_from_probe_result(), create_scan_health_finding(), _escalate_by_exposure(), _find_open_duplicate(), _finding_port(), _map_severity(), A still-relevant Finding with the same (engagement, asset, title), if any., Convert a probe's self-assessed `findings` list into persisted Finding rows. (+4 more)

### Community 209 - "Community 209"
Cohesion: 0.19
Nodes (5): Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., ScopeError, ScopeGuard

### Community 210 - "Community 210"
Cohesion: 0.36
Nodes (12): _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius(), _build_analyzer(), _critical_asset_ids(), _explain_hop(), get_attack_path() (+4 more)

### Community 211 - "Community 211"
Cohesion: 0.24
Nodes (8): bulk_import_assets(), _compute_overview(), create_engagement(), engagements_overview(), get_engagement_scope(), _overview_cache_key(), _refresh_overview_cache(), update_engagement()

### Community 212 - "Community 212"
Cohesion: 0.19
Nodes (8): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), Server/body fingerprint match against known non-AI squatters, or None., The strongest possible evidence for a real MCP server: a WWW-Authenticate     he, JSON-typed body that actually talks about auth, not just any error text.

### Community 213 - "Community 213"
Cohesion: 0.29
Nodes (4): _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator

### Community 214 - "Community 214"
Cohesion: 0.15
Nodes (1): test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor

### Community 215 - "Community 215"
Cohesion: 0.17
Nodes (3): _fake_cert(), test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced capa, test_ja4x_from_cert_matches_pure_core()

### Community 216 - "Community 216"
Cohesion: 0.36
Nodes (2): _make_scan_record(), TestDeltaEngine

### Community 217 - "Community 217"
Cohesion: 0.26
Nodes (7): FakeProcess, _finding_line(), test_nonzero_exit_retains_and_marks_partial_findings(), test_nonzero_exit_without_findings_raises_with_stderr(), test_run_scan_streams_jsonl_and_separates_timeouts(), test_template_initialization_failure_cannot_be_clean_zero(), test_timeout_retains_findings_emitted_before_termination()

### Community 218 - "Community 218"
Cohesion: 0.22
Nodes (5): _f(), test_portal_metrics.py — pure dashboard aggregations., TestOpenClosed, TestSeverityBreakdown, TestStatusTimeline

### Community 219 - "Community 219"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 220 - "Community 220"
Cohesion: 0.27
Nodes (3): _make_funnel(), Build a funnel with fakes; return (funnel, discovery, port_scanner, created)., TestScanFunnel

### Community 221 - "Community 221"
Cohesion: 0.15
Nodes (5): FakeDiscovery, FakePortScanner, test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel, RecordingDeep, TestScanFunnelRun

### Community 222 - "Community 222"
Cohesion: 0.18
Nodes (3): decode_key(), Verify a Manager-signed policy and return its public key for TOFU pinning., verify_site_policy()

### Community 223 - "Community 223"
Cohesion: 0.20
Nodes (12): _clamp(), _job_runtime_seconds(), Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Return the effective whole-job deadline; callers can only reduce it., Translate operator-supplied job params into run_engagement() kwargs.      This i, Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Return the effective whole-job deadline; callers can only reduce it. (+4 more)

### Community 224 - "Community 224"
Cohesion: 0.27
Nodes (12): DeclarativeBase, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., Append-only ledger of every attack action performed during an engagement.      W, Immutable, append-only audit trail for all exploit actions.     No TimestampMixi, Base, TimestampMixin, Per-engagement SIEM + EDR connection settings used by the detection     validati, detection_run.py — one execution of the deterministic detection engine over a fa (+4 more)

### Community 225 - "Community 225"
Cohesion: 0.26
Nodes (7): HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber(), isOptionalString(), normalizePort(), parseHttpxJsonLine()

### Community 226 - "Community 226"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 227 - "Community 227"
Cohesion: 0.20
Nodes (8): NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here., _run_nmap(), _validated_extra_args()

### Community 228 - "Community 228"
Cohesion: 0.23
Nodes (8): build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure., RDPScanner

### Community 229 - "Community 229"
Cohesion: 0.23
Nodes (7): _netbios_session(), parse_smb2_security_mode(), smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout, _smb1_negotiate(), _smb2_negotiate(), SMBScanner

### Community 230 - "Community 230"
Cohesion: 0.20
Nodes (6): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only., WebScanner

### Community 231 - "Community 231"
Cohesion: 0.27
Nodes (6): _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result(), _run_nuclei_and_save(), _set_nuclei_job_state()

### Community 232 - "Community 232"
Cohesion: 0.17
Nodes (12): Neighbor, normalize_mac(), parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower., Return {ip: normalized_mac} from the OS neighbor cache.      Tries `ip neigh` (L, One OS neighbor-cache observation about a target, with graded freshness., Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo, Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads (+4 more)

### Community 233 - "Community 233"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 234 - "Community 234"
Cohesion: 0.23
Nodes (8): build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure., RDPScanner

### Community 235 - "Community 235"
Cohesion: 0.18
Nodes (10): BaseScanner, main_entrypoint(), Subclasses implement `scan_target(self, target)` (async), returning a list     o, Run a scanner CLI's body with consistent, operator-friendly error handling., Subclasses implement `scan_target(self, target)` (async), returning a list     o, Subclasses implement `scan_target(self, target)` (async), returning a list     o, Run a scanner CLI's body with consistent, operator-friendly error handling., Run a scanner CLI's body with consistent, operator-friendly error handling. (+2 more)

### Community 236 - "Community 236"
Cohesion: 0.17
Nodes (1): TestAgentJobCompatibility

### Community 237 - "Community 237"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 238 - "Community 238"
Cohesion: 0.17
Nodes (1): test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper

### Community 239 - "Community 239"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()

### Community 240 - "Community 240"
Cohesion: 0.24
Nodes (5): _Socket, test_collector_raises_when_no_listener_binds(), test_ot_udp_backend_never_joins_or_transmits(), test_subset_listener_failure_reports_degraded_coverage(), _Writer

### Community 241 - "Community 241"
Cohesion: 0.17
Nodes (2): Tests that use the real engine but with no-op callbacks., TestRunnerHeadless

### Community 242 - "Community 242"
Cohesion: 0.27
Nodes (9): _exec(), _finding(), Unit tests for P3 Task 7: validation-result ingestion → finding verdict.  Pure t, test_confirmed_never_overrides_human_closed_finding(), test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_without_touching_status(), test_inconclusive_leaves_finding_unchanged(), test_ingest_confirmed_updates_request_and_finding() (+1 more)

### Community 243 - "Community 243"
Cohesion: 0.18
Nodes (11): _job_intent(), One-line, transparent summary of what a scan actually found so the operator, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort. (+3 more)

### Community 244 - "Community 244"
Cohesion: 0.20
Nodes (11): _as_int(), normalize_intensity(), Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile, intensity) for a job.      Resolution order:     1., Coerce an int-or-numeric-string to int, else None (non-numeric)., Map a numeric use-case code → use_case_id (raises on an unknown code)., Accept an intensity as a number (1/2/3) OR a name; return the name.      None st (+3 more)

### Community 245 - "Community 245"
Cohesion: 0.22
Nodes (7): _dec(), match_service(), One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., Soft-match collected bytes to {service, product, version}; None if unknown., ServiceBannerScanner

### Community 246 - "Community 246"
Cohesion: 0.24
Nodes (10): _is_closed(), MetricFinding, open_closed_counts(), _period(), portal_metrics.py — pure aggregations for the customer dashboard.  Kept pure (no, Count findings by severity (all five buckets always present, zero-filled).     o, (open, closed) totals over the given findings., Per-month {period, opened, closed} for the last `months` months.      opened = f (+2 more)

### Community 247 - "Community 247"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 248 - "Community 248"
Cohesion: 0.18
Nodes (7): Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., TestPromoteAssets

### Community 249 - "Community 249"
Cohesion: 0.29
Nodes (3): _asset(), _finding(), TestVulnPrioritizer

### Community 250 - "Community 250"
Cohesion: 0.18
Nodes (1): TestHallucinationGuard

### Community 251 - "Community 251"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 252 - "Community 252"
Cohesion: 0.18
Nodes (1): TestNucleiExploitRunner

### Community 253 - "Community 253"
Cohesion: 0.18
Nodes (1): TestValidatePayload

### Community 254 - "Community 254"
Cohesion: 0.22
Nodes (4): _ext(), test_main_scripts_ja4s.py — JA4S TLS ServerHello fingerprint (advanced capabilit, _serverhello(), test_ja4s_from_serverhello_tls13()

### Community 255 - "Community 255"
Cohesion: 0.31
Nodes (3): _r(), test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ "Multi-vantag, TestReconcileVantages

### Community 256 - "Community 256"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 257 - "Community 257"
Cohesion: 0.20
Nodes (2): test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses(), _token()

### Community 258 - "Community 258"
Cohesion: 0.18
Nodes (1): TestNmapXMLParser

### Community 259 - "Community 259"
Cohesion: 0.22
Nodes (10): classify_scanner_error(), engine_manifest(), ErrorDetail, planned_components(), Execution telemetry and failure normalization for the probe workflow., Resolve the exact collector plan for one workflow invocation., Map low-level failures into stable, operator-actionable categories., Represent an unexpected component exception without aborting other hosts. (+2 more)

### Community 260 - "Community 260"
Cohesion: 0.20
Nodes (10): fetch_engagement_scope(), _networks_for_target(), Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)., Parse one IP, CIDR, or inclusive IP range into covering networks.      ``None``, Fetch the engagement's authoritative scope from the manager.      Args:, Fetch the engagement's authoritative scope from the manager.      Args:, Check targets against the authoritative scope CIDRs.      Returns (allowed, reje, Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped). (+2 more)

### Community 261 - "Community 261"
Cohesion: 0.20
Nodes (5): HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Transport

### Community 262 - "Community 262"
Cohesion: 0.31
Nodes (9): _collect(), fuse_exposure_results(), fused_service_exposure(), _is_external(), vantage_fusion.py — fuse the exposure_matrix results of MULTIPLE probes.  A sing, (ip, proto, port) → fused exposure verdict, ready to stamp onto Service rows., (ip → {(proto,port): {vantage: status}}, ip → set(vantages))., Fuse several probes' exposure_matrix results into one per-target matrix.      `r (+1 more)

### Community 263 - "Community 263"
Cohesion: 0.31
Nodes (9): compute_verdict(), _int_confidence(), _qualifies_for_llm(), verification.py — normalized, dashboard-facing verification verdict.  The determ, Deterministic passive verdict from a detection finding's evidence dict., Only spend an LLM call where a rationale / FP-triage is worth it:     uncertain, Deterministic verdict, optionally enriched by an LLM rationale. The LLM     (duc, VerificationVerdict (+1 more)

### Community 264 - "Community 264"
Cohesion: 0.33
Nodes (1): ExploitOrchestrator

### Community 265 - "Community 265"
Cohesion: 0.20
Nodes (8): ACTIVITY, Credential, Engagement, engagementsStore, EngagementStatus, FINDINGS_TIMELINE, now, STORE

### Community 266 - "Community 266"
Cohesion: 0.27
Nodes (7): COMMON_RANGES, estimateHostCount(), isValidTarget(), ParseResult, parseTargets(), RFC1918, validOctets()

### Community 267 - "Community 267"
Cohesion: 0.20
Nodes (10): _agent_token_from_websocket(), agent_websocket_endpoint(), _claim_pushed_job(), Persistent WebSocket for probe → manager push communication.      Authentication, Persistent WebSocket for probe → manager push communication.      Authentication, Read an agent bearer token exclusively from the non-logged auth header., Read an agent bearer token exclusively from the non-logged auth header., Persistent WebSocket for probe → manager push communication.      Query params: (+2 more)

### Community 268 - "Community 268"
Cohesion: 0.24
Nodes (6): HostDiscoveryScanner, Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., vendor_for_mac()

### Community 269 - "Community 269"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 271 - "Community 271"
Cohesion: 0.44
Nodes (9): _metrics(), test_main_scripts_completeness.py — Epic 4: set-based scan-completeness invarian, _rec(), test_duplicate_port_is_detected(), test_fallback_count_based_when_no_requested_set(), test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely_complete() (+1 more)

### Community 272 - "Community 272"
Cohesion: 0.29
Nodes (6): _oserr(), test_main_scripts_errno.py — Phase 2: shared TCP/UDP errno classification.  Veri, test_definitive_states(), test_describe_os_error_is_fully_debuggable(), test_scanner_side_errors_are_error_not_filtered(), test_unknown_errno_is_self_identifying_and_never_filtered()

### Community 273 - "Community 273"
Cohesion: 0.20
Nodes (1): TestIoTScanner

### Community 274 - "Community 274"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 275 - "Community 275"
Cohesion: 0.20
Nodes (2): Each encryption uses a fresh ephemeral key, so blobs are different., TestEncryptDecryptRoundtrip

### Community 276 - "Community 276"
Cohesion: 0.29
Nodes (5): test_tls_integration.py — Tier 2.4 live check: run the real TLSScanner against a, _self_signed(), test_tls_fingerprint_is_nonzero_and_stable(), test_tls_scanner_reports_posture_grade(), _TLSServer

### Community 277 - "Community 277"
Cohesion: 0.20
Nodes (1): TestSubmitResult

### Community 278 - "Community 278"
Cohesion: 0.44
Nodes (9): _exec(), _mock_db(), Mocked-session unit tests for the P3 active-validation endpoints (Task 4).  No D, test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job(), test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_derives_tls_check(), test_reject_marks_rejected() (+1 more)

### Community 279 - "Community 279"
Cohesion: 0.20
Nodes (7): Push a job to the first online connected agent.          Returns the agent_id th, Push a job to the first online agent in the requested tenant.          Returns t, Push a job to the first online agent in the requested tenant.          Returns t, Return idle connected agents belonging to exactly one tenant., Return idle connected agents belonging to exactly one tenant., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'.

### Community 280 - "Community 280"
Cohesion: 0.20
Nodes (6): AgentConnectionManager, Record transport features explicitly advertised by a connected probe., Record transport features explicitly advertised by a connected probe., Tracks WebSocket connections from probes/agents for direct job push.      Each c, Register an agent's WebSocket connection.          If the agent already has a co, Register an agent's WebSocket connection.          If the agent already has a co

### Community 281 - "Community 281"
Cohesion: 0.25
Nodes (9): _facts_from_cache(), Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, run_scan(), _string_list() (+1 more)

### Community 282 - "Community 282"
Cohesion: 0.22
Nodes (9): check_hw_bind(), get_hw_id(), HWBindError, Raised when the binary is running on an unauthorized machine., Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B, RuntimeError, Raised when a required configuration invariant is violated at boot. (+1 more)

### Community 283 - "Community 283"
Cohesion: 0.22
Nodes (7): Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active.

### Community 284 - "Community 284"
Cohesion: 0.31
Nodes (5): HallucinationGuard, Run all relevant checks and return a combined verdict:         ``{valid, issues,, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide.

### Community 285 - "Community 285"
Cohesion: 0.22
Nodes (9): close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, FastAPI dependency that enforces role-based access.      Usage:         @router., require_role(), CurrentUser, Parsed from JWT claims — attached to request.state and injected as dependency. (+1 more)

### Community 286 - "Community 286"
Cohesion: 0.31
Nodes (7): create_access_token(), create_device_access_token(), create_refresh_token(), _now(), Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation.

### Community 287 - "Community 287"
Cohesion: 0.22
Nodes (4): 0e22dbf feat(probe): bounded auto-troubleshoot for Manager connectivity, 1af3404 feat(deploy): probe-free manager stack + port-80 edge ingress, c0f3b4c feat(probe-enroll): trust-on-first-use auto-enrollment + gen-env policy-key fix, test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.  T

### Community 288 - "Community 288"
Cohesion: 0.28
Nodes (3): AdaptiveRateController, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window).

### Community 289 - "Community 289"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 290 - "Community 290"
Cohesion: 0.28
Nodes (5): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples.

### Community 291 - "Community 291"
Cohesion: 0.22
Nodes (9): _apply_device_profile(), process_job_result(), _promote_assets(), Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu, Stable idempotency checksum for one attempt completion payload., Upsert discovered hosts/services into the asset inventory.      Keyed by (engage, Stamp the probe's evidence-based device role onto an Asset (create/update)., Upsert discovered hosts/services into the asset inventory.      Keyed by (engage (+1 more)

### Community 292 - "Community 292"
Cohesion: 0.31
Nodes (7): compute(), SLA policy engine.  Turns a severity + "first seen" timestamp into a remediation, Aggregate SLA states across a set of findings.      Returns counts per state plu, Compute the SLA state for one finding. Never raises on missing data., SlaResult, summarize(), _windows()

### Community 293 - "Community 293"
Cohesion: 0.22
Nodes (1): TestWindowStateMachine

### Community 294 - "Community 294"
Cohesion: 0.47
Nodes (3): _mock_db(), _resp(), TestLLMReportGenerator

### Community 295 - "Community 295"
Cohesion: 0.22
Nodes (1): TestUseCasesResolve

### Community 296 - "Community 296"
Cohesion: 0.39
Nodes (7): _rank(), test_bounds(), test_confirmed_exploitable_outranks_contradicted(), test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lowers(), test_kev_raises_rank(), test_low_confidence_lowers_rank()

### Community 297 - "Community 297"
Cohesion: 0.28
Nodes (8): _py_files(), test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1, Every scanner module authored in main_scripts must exist in scanner/., scanner/ must not carry modules that main_scripts/ does not — otherwise the, Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py., test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_files(), test_scanner_module_matches_main_scripts()

### Community 298 - "Community 298"
Cohesion: 0.22
Nodes (1): TestTargetsInExcludes

### Community 299 - "Community 299"
Cohesion: 0.22
Nodes (1): TestIdentity

### Community 300 - "Community 300"
Cohesion: 0.31
Nodes (8): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 301 - "Community 301"
Cohesion: 0.25
Nodes (8): _build_run_stats(), _hosts_from_facts(), Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port., Build one consistent result summary for complete and interrupted runs., Build one consistent result summary for complete and interrupted runs., Build one consistent result summary for complete and interrupted runs.

### Community 302 - "Community 302"
Cohesion: 0.46
Nodes (8): LLMUnavailableError, LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses, Raised when the Anthropic SDK or API key is not configured., Raised when the Anthropic SDK or API key is not configured., ReviewStatus, LLMOutput, Every LLM generation is persisted here for human-in-the-loop review.      AI out, Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API

### Community 303 - "Community 303"
Cohesion: 0.36
Nodes (7): extractScripts(), NmapHost, NmapScriptResult, NmapService, parseNmapXml(), parser, toArray()

### Community 304 - "Community 304"
Cohesion: 0.46
Nodes (7): _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., _read_jsonl(), _run_stage()

### Community 305 - "Community 305"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 306 - "Community 306"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, loadWordlist(), nativeDirBust(), NativeDirOpts, probe(), ProbeResp

### Community 307 - "Community 307"
Cohesion: 0.32
Nodes (7): attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon(), nativePtrSweep(), PtrSweepResult, safe()

### Community 308 - "Community 308"
Cohesion: 0.29
Nodes (8): MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, Run masscan over the given target specs and return its parsed JSON records., Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, _run_masscan()

### Community 309 - "Community 309"
Cohesion: 0.25
Nodes (6): _is_readable(), PassiveCollector, Listen-only discovery. No active probing. Reports in-scope hosts that     announ, Await readability on any listener without blocking the event loop., Listen-only discovery. No active probing. Reports in-scope hosts that     announ, Await readability on any listener without blocking the event loop.

### Community 310 - "Community 310"
Cohesion: 0.46
Nodes (7): _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., _read_jsonl(), _run_stage()

### Community 311 - "Community 311"
Cohesion: 0.25
Nodes (4): RateLimiter, Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second.

### Community 312 - "Community 312"
Cohesion: 0.29
Nodes (5): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only.

### Community 313 - "Community 313"
Cohesion: 0.43
Nodes (1): WindowsCollector

### Community 314 - "Community 314"
Cohesion: 0.32
Nodes (7): apply_validation_outcome(), ingest_validation_result(), looks_like_validation_result(), validation_ingest.py — turn a probe's safe active-validation result into a findi, Apply a validation verdict to a finding object (pure — no DB/session)., Cheap gate so normal scan submissions never trigger a lookup: a probe     valida, If ``job_id`` belongs to a ValidationRequest, store the result, set its     outc

### Community 315 - "Community 315"
Cohesion: 0.46
Nodes (7): _ev(), test_confirmed_authoritative_does_not_escalate(), test_high_severity_suspected_escalates_when_roe_allows(), test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_escalate(), test_ot_profile_never_escalates(), test_roe_forbids_blocks_escalation()

### Community 316 - "Community 316"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 317 - "Community 317"
Cohesion: 0.32
Nodes (3): _boundary_test_client(), test_agent_jwt_is_blocked_before_human_route_handler(), test_human_jwt_still_reaches_human_route_handler()

### Community 318 - "Community 318"
Cohesion: 0.25
Nodes (1): test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure

### Community 319 - "Community 319"
Cohesion: 0.43
Nodes (1): TestMetasploitRPCClient

### Community 320 - "Community 320"
Cohesion: 0.25
Nodes (1): TestRequiresApproval

### Community 321 - "Community 321"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 322 - "Community 322"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 323 - "Community 323"
Cohesion: 0.25
Nodes (1): test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model

### Community 325 - "Community 325"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 326 - "Community 326"
Cohesion: 0.36
Nodes (5): test_scan_health.py — the probe scan-metrics → coverage/health verdict.  Guards, _summary(), test_clean_scan_is_healthy_and_does_not_warn(), test_local_resource_errors_flag_degraded(), test_missing_ports_flag_incomplete()

### Community 327 - "Community 327"
Cohesion: 0.25
Nodes (8): expire_attempt(), Requeue every running job whose lease has expired. Returns the job ids., Expire one fenced attempt; return True when the job may be retried., Poll loop: requeue expired jobs every reaper_interval_seconds until stopped., Expire current attempts and requeue only jobs within their retry budget., Poll loop: requeue expired jobs every reaper_interval_seconds until stopped., reap_once(), run_reaper()

### Community 328 - "Community 328"
Cohesion: 0.38
Nodes (5): AssistantDrawer(), AssistantFab(), AssistantCtx, Ctx, useAssistant()

### Community 329 - "Community 329"
Cohesion: 0.48
Nodes (5): build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()

### Community 330 - "Community 330"
Cohesion: 0.67
Nodes (7): agents/greeting-introduction, main, 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit

### Community 331 - "Community 331"
Cohesion: 0.29
Nodes (5): _deterministic_layout(), GraphVisualizer, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path

### Community 332 - "Community 332"
Cohesion: 0.38
Nodes (6): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages()

### Community 333 - "Community 333"
Cohesion: 0.43
Nodes (5): _finding_views(), posture(), Map joined (Finding, Asset.criticality) rows to duck-typed views., _sev_str(), _two_latest_completed_runs()

### Community 334 - "Community 334"
Cohesion: 0.38
Nodes (5): fuse_liveness(), _now(), host_discovery.py — determine which hosts are alive, with graded confidence.  ME, Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a, _state_for_confidence()

### Community 335 - "Community 335"
Cohesion: 0.38
Nodes (6): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages()

### Community 336 - "Community 336"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 337 - "Community 337"
Cohesion: 0.29
Nodes (1): TestDeceptionScore

### Community 338 - "Community 338"
Cohesion: 0.29
Nodes (1): TestIngestFile

### Community 339 - "Community 339"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 340 - "Community 340"
Cohesion: 0.29
Nodes (1): TestValidateModule

### Community 341 - "Community 341"
Cohesion: 0.29
Nodes (1): TestValidateScope

### Community 342 - "Community 342"
Cohesion: 0.29
Nodes (1): test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.

### Community 343 - "Community 343"
Cohesion: 0.48
Nodes (6): _base(), FindingOut computes the explainable risk_rank at serialization (P4 Task 5 wiring, test_confirmed_exploited_outranks_contradicted(), test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_risk_rank_is_computed_not_none()

### Community 344 - "Community 344"
Cohesion: 0.29
Nodes (1): TestNormalizeMac

### Community 345 - "Community 345"
Cohesion: 0.38
Nodes (3): _dry_run(), test_installer_accepts_enroll_token_and_insecure_for_http_manager(), test_installer_without_token_still_shows_manual_approval()

### Community 346 - "Community 346"
Cohesion: 0.29
Nodes (1): TestProfiles

### Community 347 - "Community 347"
Cohesion: 0.29
Nodes (1): TestMergeExclusions

### Community 348 - "Community 348"
Cohesion: 0.43
Nodes (3): The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, TestSynRetransmit

### Community 349 - "Community 349"
Cohesion: 0.29
Nodes (5): Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., TestRunnerSubmission

### Community 351 - "Community 351"
Cohesion: 0.48
Nodes (6): _b64(), issue(), keygen(), main(), pubkey(), Print the vendor PUBLIC key (hex) derived from the private key.      build/seal-

### Community 352 - "Community 352"
Cohesion: 0.29
Nodes (5): Remove an agent's WebSocket registration., Remove the current registration, optionally only for one socket.          Return, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job

### Community 353 - "Community 353"
Cohesion: 0.33
Nodes (6): Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., _run_polled_job_with_heartbeats()

### Community 354 - "Community 354"
Cohesion: 0.33
Nodes (6): _applied_tuning(), syn' for wide sweeps (deep intensity / full-port audit), else 'connect'., Serialize effective limits without ever echoing credential values., Serialize effective limits without ever echoing credential values., Serialize effective limits without ever echoing credential values., _scan_method_for()

### Community 355 - "Community 355"
Cohesion: 0.33
Nodes (5): _atomic_write_private_state(), Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., _sync_directory()

### Community 356 - "Community 356"
Cohesion: 0.40
Nodes (5): exposure_fusion_service.py — apply multi-probe vantage fusion to Service rows., Reconstruct one {"exposure": [...]} dict per probe from persisted facts.      Ea, Fuse all probes' exposure_matrix observations for an engagement and stamp     th, recompute_fused_exposure(), _results_from_scan_rows()

### Community 357 - "Community 357"
Cohesion: 0.40
Nodes (5): asset_type_for(), device_profiles(), device_profile.py — map a probe device_inventory result onto asset fields.  The, The AssetType for a classifier device_type, or None to keep the existing., ip → {asset_type, device_role, role_detail, role_confidence} from a probe     de

### Community 358 - "Community 358"
Cohesion: 0.33
Nodes (5): escalate_for_exposure(), exposure.py — reachability-aware risk from the probe's exposure_matrix use-case., (ip, proto, port) → exposure verdict, from a probe exposure_matrix result., Bump a finding one severity rung when its service is internet-reachable.      On, service_exposure()

### Community 359 - "Community 359"
Cohesion: 0.33
Nodes (3): Apply constraints + indexes (idempotent)., Run a Cypher statement and return records as dicts. [] if not connected., Run a parametrised write with UNWIND batching for bulk node/edge loads.

### Community 360 - "Community 360"
Cohesion: 0.40
Nodes (5): classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj

### Community 361 - "Community 361"
Cohesion: 0.33
Nodes (6): device_hint(), is_locally_administered(), True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc, Best-effort device classification from the L2/L3 evidence., True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc, Best-effort device classification from the L2/L3 evidence.

### Community 362 - "Community 362"
Cohesion: 0.33
Nodes (2): _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH

### Community 363 - "Community 363"
Cohesion: 0.33
Nodes (6): parse_ports(), Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535).

### Community 364 - "Community 364"
Cohesion: 0.40
Nodes (5): AttemptClaim, claim_job_attempt(), Atomically claim a pending job and create its fenced attempt ledger row., Renew only the currently installed running attempt/fence., renew_job_attempt()

### Community 365 - "Community 365"
Cohesion: 0.33
Nodes (1): TestNTLMRelayChecker

### Community 366 - "Community 366"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 367 - "Community 367"
Cohesion: 0.33
Nodes (1): TestCvss

### Community 368 - "Community 368"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 369 - "Community 369"
Cohesion: 0.60
Nodes (5): Unit tests for the dashboard list endpoints (jobs + assets)., _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user()

### Community 370 - "Community 370"
Cohesion: 0.33
Nodes (4): Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., TestTaskRunnerWithEncryptedScope

### Community 371 - "Community 371"
Cohesion: 0.33
Nodes (2): Phase 1: combined scope validation (validate + excludes)., TestScopeValidationPipeline

### Community 372 - "Community 372"
Cohesion: 0.33
Nodes (2): Phase 2: WebSocket message parsing., TestWebSocketMessageProtocol

### Community 373 - "Community 373"
Cohesion: 0.33
Nodes (4): Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup., TestStartupGauntlet

### Community 375 - "Community 375"
Cohesion: 0.33
Nodes (1): test_main_scripts_device_ties.py — Phase 23: device classification never resolve

### Community 376 - "Community 376"
Cohesion: 0.33
Nodes (1): TestClamp

### Community 377 - "Community 377"
Cohesion: 0.33
Nodes (1): TestEngagementModes

### Community 378 - "Community 378"
Cohesion: 0.53
Nodes (5): _manifest(), test_probe_manifest.py — the `agent.agent manifest` command that the seal-parity, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_contract()

### Community 379 - "Community 379"
Cohesion: 0.73
Nodes (5): _db_returning(), _finding(), test_covered_clean_medium_finding_is_auto_resolved(), test_db_version_change_blocks_resolution(), test_uncovered_finding_is_left_open()

### Community 381 - "Community 381"
Cohesion: 0.33
Nodes (1): TestFetchEngagementScope

### Community 382 - "Community 382"
Cohesion: 0.60
Nodes (1): TestBuildResultsEnrichment

### Community 384 - "Community 384"
Cohesion: 0.40
Nodes (5): _load_env(), Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience.

### Community 385 - "Community 385"
Cohesion: 0.40
Nodes (5): _count_open_port_facts(), Count concrete open services, not generic host-liveness observations., Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact.

### Community 386 - "Community 386"
Cohesion: 0.40
Nodes (5): _error_result(), Single factory for error result dicts — no copy-paste., Single factory for error result dicts — no copy-paste., Single factory for error result dicts — no copy-paste., _runtime_manifest()

### Community 387 - "Community 387"
Cohesion: 0.40
Nodes (5): LeaseLostError, Raised when Manager fencing revokes the running attempt., Raised when Manager fencing revokes the running attempt., Raised when Manager fencing revokes the running attempt., _run_with_cancellation()

### Community 388 - "Community 388"
Cohesion: 0.40
Nodes (4): True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls.

### Community 389 - "Community 389"
Cohesion: 0.40
Nodes (4): Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce

### Community 390 - "Community 390"
Cohesion: 0.40
Nodes (4): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of

### Community 391 - "Community 391"
Cohesion: 0.40
Nodes (4): Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons

### Community 392 - "Community 392"
Cohesion: 0.40
Nodes (4): Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used

### Community 393 - "Community 393"
Cohesion: 0.40
Nodes (4): Return the WebSocket connection URL with auth token.          The token is passe, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica

### Community 394 - "Community 394"
Cohesion: 0.40
Nodes (4): Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns

### Community 395 - "Community 395"
Cohesion: 0.40
Nodes (3): verification_graph.py — optional LangGraph orchestration for passive verificatio, Run passive verification. Uses the LangGraph StateGraph when available;     othe, run_verification()

### Community 396 - "Community 396"
Cohesion: 0.40
Nodes (3): get_settings(), Settings, BaseSettings

### Community 397 - "Community 397"
Cohesion: 0.40
Nodes (2): ClientUser, ScanReq

### Community 398 - "Community 398"
Cohesion: 0.40
Nodes (3): _as_uuid(), AttackLogger, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 399 - "Community 399"
Cohesion: 0.40
Nodes (5): Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, resolve()

### Community 400 - "Community 400"
Cohesion: 0.50
Nodes (3): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =

### Community 401 - "Community 401"
Cohesion: 0.60
Nodes (2): _claim_fixture(), TestAtomicWebSocketClaim

### Community 402 - "Community 402"
Cohesion: 0.40
Nodes (1): TestTenantWebSocketSelection

### Community 403 - "Community 403"
Cohesion: 0.40
Nodes (1): TestGetAgentJobs

### Community 405 - "Community 405"
Cohesion: 0.40
Nodes (1): TestCheckHwBind

### Community 406 - "Community 406"
Cohesion: 0.40
Nodes (2): Phase 1: result spool with upload retry., TestResultSpoolWithRetry

### Community 407 - "Community 407"
Cohesion: 0.40
Nodes (3): Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine., TestTransportWithIdentity

### Community 409 - "Community 409"
Cohesion: 0.40
Nodes (1): TestEngineSummary

### Community 410 - "Community 410"
Cohesion: 0.40
Nodes (1): TestLooksLikeHttp

### Community 411 - "Community 411"
Cohesion: 0.40
Nodes (1): TestLooksLikeTls

### Community 412 - "Community 412"
Cohesion: 0.40
Nodes (1): TestResolveScanType

### Community 413 - "Community 413"
Cohesion: 0.40
Nodes (1): TestTargets

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
Nodes (1): TestDeviceEnrollment

### Community 418 - "Community 418"
Cohesion: 0.40
Nodes (1): TestWebSocket

### Community 419 - "Community 419"
Cohesion: 0.40
Nodes (2): Device-role inventory: persist the probe device_classifier's role on assets.  Ad, # NOTE: Postgres cannot DROP a single enum value; the added 'printer' /

### Community 420 - "Community 420"
Cohesion: 0.50
Nodes (4): _load_or_create_signing_identity(), Load or atomically create the probe's Ed25519 enrollment identity., Load or atomically create the probe's Ed25519 enrollment identity., Load or atomically create the probe's Ed25519 enrollment identity.

### Community 421 - "Community 421"
Cohesion: 0.50
Nodes (4): _derive_post_stage(), Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, _results_by_target()

### Community 422 - "Community 422"
Cohesion: 0.50
Nodes (3): scan_health.py — turn the probe's per-host scan completeness/health metrics into, Aggregate result['scan_metrics'] into a coverage/health verdict.        degraded, scan_health_summary()

### Community 423 - "Community 423"
Cohesion: 0.67
Nodes (1): SSHCollector

### Community 424 - "Community 424"
Cohesion: 0.50
Nodes (3): audit.py — the append-only audit-log writer, shared by the operator and portal r, Append one immutable audit row (caller flushes within its own txn)., record_audit()

### Community 425 - "Community 425"
Cohesion: 0.83
Nodes (3): _db_with(), test_reopen_non_remediated_is_conflict(), test_reopen_remediated_finding_sets_open_and_audits()

### Community 427 - "Community 427"
Cohesion: 0.50
Nodes (1): TestGate0

### Community 428 - "Community 428"
Cohesion: 0.50
Nodes (1): TestRateLimiter

### Community 429 - "Community 429"
Cohesion: 0.50
Nodes (1): TestScanResult

### Community 430 - "Community 430"
Cohesion: 0.83
Nodes (3): _objects(), test_expired_attempt_fails_job_when_retry_budget_is_exhausted(), test_expired_attempt_requeues_with_fence_history_preserved()

### Community 432 - "Community 432"
Cohesion: 0.50
Nodes (1): TestHeartbeat

### Community 433 - "Community 433"
Cohesion: 0.50
Nodes (1): TestHttpGet

### Community 434 - "Community 434"
Cohesion: 0.50
Nodes (1): TestPollJobs

### Community 435 - "Community 435"
Cohesion: 0.50
Nodes (1): TestRefreshRegistration

### Community 436 - "Community 436"
Cohesion: 0.50
Nodes (1): TestRegister

### Community 439 - "Community 439"
Cohesion: 0.50
Nodes (2): _ConcurrencyScanner, test_host_fanout_is_bounded()

### Community 440 - "Community 440"
Cohesion: 0.50
Nodes (1): Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises

### Community 441 - "Community 441"
Cohesion: 0.50
Nodes (1): Add is_active to users and tenants; add password_expires_at to users.  All exist

### Community 442 - "Community 442"
Cohesion: 0.50
Nodes (1): Add fenced execution attempts for agent-dispatched scan jobs.  Revision ID: 0017

### Community 443 - "Community 443"
Cohesion: 0.50
Nodes (1): Add Manager-approved device-key probe enrollment and Site policy.  Revision ID:

### Community 444 - "Community 444"
Cohesion: 0.50
Nodes (1): Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision

### Community 445 - "Community 445"
Cohesion: 0.50
Nodes (1): Finding verification verdict columns (P2 passive verification).  Revision ID: 00

### Community 446 - "Community 446"
Cohesion: 0.50
Nodes (1): Customer portal foundation (Part 2, Phase 0): client role, engagement↔agent assi

### Community 447 - "Community 447"
Cohesion: 0.50
Nodes (1): Service exposure: persist the exposure_matrix reachability verdict.  Adds servic

### Community 448 - "Community 448"
Cohesion: 0.50
Nodes (3): Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag

### Community 449 - "Community 449"
Cohesion: 0.50
Nodes (3): Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs.

### Community 450 - "Community 450"
Cohesion: 0.50
Nodes (3): Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.

### Community 451 - "Community 451"
Cohesion: 0.50
Nodes (3): Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy).

### Community 452 - "Community 452"
Cohesion: 0.50
Nodes (3): Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job).

### Community 453 - "Community 453"
Cohesion: 0.50
Nodes (3): Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, _utcnow()

### Community 454 - "Community 454"
Cohesion: 0.67
Nodes (3): approve_exploit(), _get_approval_or_404(), reject_exploit()

### Community 455 - "Community 455"
Cohesion: 0.67
Nodes (1): risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se

### Community 456 - "Community 456"
Cohesion: 0.67
Nodes (1): TestAgentWebSocketAuthentication

### Community 457 - "Community 457"
Cohesion: 0.67
Nodes (1): TestJobSecretBoundary

### Community 458 - "Community 458"
Cohesion: 0.67
Nodes (1): TestAgentExecutableTypes

### Community 459 - "Community 459"
Cohesion: 0.67
Nodes (1): TestAgentRegistrationRefresh

### Community 460 - "Community 460"
Cohesion: 0.67
Nodes (1): TestGetHwId

### Community 461 - "Community 461"
Cohesion: 0.67
Nodes (3): ResultSpool with tiny retry delay for fast tests., ResultSpool with tiny retry delay for fast tests., spool()

### Community 462 - "Community 462"
Cohesion: 0.67
Nodes (1): TestKeyGeneration

### Community 463 - "Community 463"
Cohesion: 0.67
Nodes (1): TestRunnerScanTypes

### Community 464 - "Community 464"
Cohesion: 0.67
Nodes (3): Create a Transport with a real state file path but no actual HTTP calls., Create a Transport with a real state file path but no actual HTTP calls., transport()

### Community 465 - "Community 465"
Cohesion: 0.67
Nodes (1): TestFetchScope

### Community 467 - "Community 467"
Cohesion: 0.67
Nodes (2): Record a heartbeat from an agent., Record a heartbeat from an agent.

### Community 468 - "Community 468"
Cohesion: 0.67
Nodes (2): Dispatch a real ScanResult into the right sub-structure, keyed         on result, Dispatch a real ScanResult into the right sub-structure, keyed         on result

### Community 470 - "Community 470"
Cohesion: 1.00
Nodes (1): Open the driver and verify connectivity. Returns False on any failure.

### Community 471 - "Community 471"
Cohesion: 1.00
Nodes (1): TestAccessTokenExpiry

### Community 480 - "Community 480"
Cohesion: 1.00
Nodes (1): Fast port discovery with naabu. Feeds port list to Nmap.

### Community 481 - "Community 481"
Cohesion: 1.00
Nodes (1): Nmap service enumeration. Accepts port list from Naabu.

### Community 482 - "Community 482"
Cohesion: 1.00
Nodes (1): Nuclei vulnerability scan — production-ready.

### Community 483 - "Community 483"
Cohesion: 1.00
Nodes (1): Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.

### Community 484 - "Community 484"
Cohesion: 1.00
Nodes (1): NetExec SMB validation: signing, null sessions, SMBv1.

### Community 485 - "Community 485"
Cohesion: 1.00
Nodes (1): testssl.sh TLS/SSL analysis.

### Community 486 - "Community 486"
Cohesion: 1.00
Nodes (1): Extract HTTP/HTTPS URLs from nmap XML output.

### Community 487 - "Community 487"
Cohesion: 1.00
Nodes (1): EyeWitness screenshot evidence collection.

### Community 488 - "Community 488"
Cohesion: 1.00
Nodes (1): Safe lateral movement checks — no actual exploitation.

### Community 489 - "Community 489"
Cohesion: 1.00
Nodes (1): Cloud infrastructure scan (AWS/Azure/GCP).

### Community 490 - "Community 490"
Cohesion: 1.00
Nodes (1): Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.

### Community 491 - "Community 491"
Cohesion: 1.00
Nodes (1): Read a KV-v2 secret from Vault.

### Community 492 - "Community 492"
Cohesion: 1.00
Nodes (1): Verify the Python probe can open what the TypeScript manager sealed (T14 interop

### Community 493 - "Community 493"
Cohesion: 1.00
Nodes (1): Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO

### Community 494 - "Community 494"
Cohesion: 1.00
Nodes (1): Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).

### Community 495 - "Community 495"
Cohesion: 1.00
Nodes (1): End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.

### Community 496 - "Community 496"
Cohesion: 1.00
Nodes (1): Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 497 - "Community 497"
Cohesion: 1.00
Nodes (1): Make a per-host scanner instance share ONE rate limiter + semaphore with all

### Community 498 - "Community 498"
Cohesion: 1.00
Nodes (1): Make a raw banner safe and readable for the summary line.      Many services ans

### Community 499 - "Community 499"
Cohesion: 1.00
Nodes (1): # NOTE: credentialed collectors (ssh_collector, windows_collector) are run

### Community 500 - "Community 500"
Cohesion: 1.00
Nodes (1): ThreadingHTTPServer

## Knowledge Gaps
- **2054 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+2049 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 85`** (2 nodes): `_ExplodingScanner`, `test_per_target_exception_preserves_other_results()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (1 nodes): `TestResultSpool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 127`** (1 nodes): `TestUDPProbeConstruction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 149`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 166`** (1 nodes): `TestSNMPBerUtilities`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (1 nodes): `Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 183`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 199`** (1 nodes): `TestMobileScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 201`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (1 nodes): `test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 216`** (2 nodes): `_make_scan_record()`, `TestDeltaEngine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (1 nodes): `TestAgentJobCompatibility`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (1 nodes): `test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (2 nodes): `Tests that use the real engine but with no-op callbacks.`, `TestRunnerHeadless`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (1 nodes): `TestHallucinationGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 251`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (1 nodes): `TestNucleiExploitRunner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (1 nodes): `TestValidatePayload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (2 nodes): `test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()`, `_token()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (1 nodes): `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (1 nodes): `ExploitOrchestrator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 273`** (1 nodes): `TestIoTScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (2 nodes): `Each encryption uses a fresh ephemeral key, so blobs are different.`, `TestEncryptDecryptRoundtrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (1 nodes): `TestWindowStateMachine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 295`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 298`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 299`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 305`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 313`** (1 nodes): `WindowsCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 316`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 318`** (1 nodes): `test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 319`** (1 nodes): `TestMetasploitRPCClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (1 nodes): `TestRequiresApproval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 323`** (1 nodes): `test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 325`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 336`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 337`** (1 nodes): `TestDeceptionScore`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 338`** (1 nodes): `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 339`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 340`** (1 nodes): `TestValidateModule`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 341`** (1 nodes): `TestValidateScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 342`** (1 nodes): `test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 344`** (1 nodes): `TestNormalizeMac`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 346`** (1 nodes): `TestProfiles`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 347`** (1 nodes): `TestMergeExclusions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 362`** (2 nodes): `_NoRedirect`, `mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 365`** (1 nodes): `TestNTLMRelayChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 367`** (1 nodes): `TestCvss`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 368`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 371`** (2 nodes): `Phase 1: combined scope validation (validate + excludes).`, `TestScopeValidationPipeline`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 372`** (2 nodes): `Phase 2: WebSocket message parsing.`, `TestWebSocketMessageProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 375`** (1 nodes): `test_main_scripts_device_ties.py — Phase 23: device classification never resolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 376`** (1 nodes): `TestClamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 377`** (1 nodes): `TestEngagementModes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 381`** (1 nodes): `TestFetchEngagementScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 382`** (1 nodes): `TestBuildResultsEnrichment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 397`** (2 nodes): `ClientUser`, `ScanReq`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 401`** (2 nodes): `_claim_fixture()`, `TestAtomicWebSocketClaim`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 402`** (1 nodes): `TestTenantWebSocketSelection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 403`** (1 nodes): `TestGetAgentJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 405`** (1 nodes): `TestCheckHwBind`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 406`** (2 nodes): `Phase 1: result spool with upload retry.`, `TestResultSpoolWithRetry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 409`** (1 nodes): `TestEngineSummary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 410`** (1 nodes): `TestLooksLikeHttp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 411`** (1 nodes): `TestLooksLikeTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 412`** (1 nodes): `TestResolveScanType`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 413`** (1 nodes): `TestTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 414`** (2 nodes): `_scope()`, `TestBuildDefaultFunnel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 415`** (1 nodes): `TestRoutePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 416`** (1 nodes): `TestVerifyReplyCookie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 417`** (1 nodes): `TestDeviceEnrollment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 418`** (1 nodes): `TestWebSocket`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 419`** (2 nodes): `Device-role inventory: persist the probe device_classifier's role on assets.  Ad`, `# NOTE: Postgres cannot DROP a single enum value; the added 'printer' /`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 423`** (1 nodes): `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 427`** (1 nodes): `TestGate0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 428`** (1 nodes): `TestRateLimiter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 429`** (1 nodes): `TestScanResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 432`** (1 nodes): `TestHeartbeat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 433`** (1 nodes): `TestHttpGet`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 434`** (1 nodes): `TestPollJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 435`** (1 nodes): `TestRefreshRegistration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 436`** (1 nodes): `TestRegister`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 439`** (2 nodes): `_ConcurrencyScanner`, `test_host_fanout_is_bounded()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 440`** (1 nodes): `Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 441`** (1 nodes): `Add is_active to users and tenants; add password_expires_at to users.  All exist`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 442`** (1 nodes): `Add fenced execution attempts for agent-dispatched scan jobs.  Revision ID: 0017`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 443`** (1 nodes): `Add Manager-approved device-key probe enrollment and Site policy.  Revision ID:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 444`** (1 nodes): `Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 445`** (1 nodes): `Finding verification verdict columns (P2 passive verification).  Revision ID: 00`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 446`** (1 nodes): `Customer portal foundation (Part 2, Phase 0): client role, engagement↔agent assi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 447`** (1 nodes): `Service exposure: persist the exposure_matrix reachability verdict.  Adds servic`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 455`** (1 nodes): `risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 456`** (1 nodes): `TestAgentWebSocketAuthentication`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 457`** (1 nodes): `TestJobSecretBoundary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 458`** (1 nodes): `TestAgentExecutableTypes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 459`** (1 nodes): `TestAgentRegistrationRefresh`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 460`** (1 nodes): `TestGetHwId`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 462`** (1 nodes): `TestKeyGeneration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 463`** (1 nodes): `TestRunnerScanTypes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 465`** (1 nodes): `TestFetchScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 467`** (2 nodes): `Record a heartbeat from an agent.`, `Record a heartbeat from an agent.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 468`** (2 nodes): `Dispatch a real ScanResult into the right sub-structure, keyed         on result`, `Dispatch a real ScanResult into the right sub-structure, keyed         on result`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 470`** (1 nodes): `Open the driver and verify connectivity. Returns False on any failure.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 471`** (1 nodes): `TestAccessTokenExpiry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 480`** (1 nodes): `Fast port discovery with naabu. Feeds port list to Nmap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 481`** (1 nodes): `Nmap service enumeration. Accepts port list from Naabu.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 482`** (1 nodes): `Nuclei vulnerability scan — production-ready.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 483`** (1 nodes): `Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 484`** (1 nodes): `NetExec SMB validation: signing, null sessions, SMBv1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 485`** (1 nodes): `testssl.sh TLS/SSL analysis.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 486`** (1 nodes): `Extract HTTP/HTTPS URLs from nmap XML output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 487`** (1 nodes): `EyeWitness screenshot evidence collection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 488`** (1 nodes): `Safe lateral movement checks — no actual exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 489`** (1 nodes): `Cloud infrastructure scan (AWS/Azure/GCP).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 490`** (1 nodes): `Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 491`** (1 nodes): `Read a KV-v2 secret from Vault.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 492`** (1 nodes): `Verify the Python probe can open what the TypeScript manager sealed (T14 interop`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 493`** (1 nodes): `Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 494`** (1 nodes): `Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 495`** (1 nodes): `End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 496`** (1 nodes): `Deterministic stand-ins emitting realistic output for 127.0.0.1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 497`** (1 nodes): `Make a per-host scanner instance share ONE rate limiter + semaphore with all`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 498`** (1 nodes): `Make a raw banner safe and readable for the summary line.      Many services ans`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 499`** (1 nodes): `# NOTE: credentialed collectors (ssh_collector, windows_collector) are run`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 500`** (1 nodes): `ThreadingHTTPServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 6` to `Community 56`, `Community 205`, `Community 137`, `Community 130`, `Community 150`, `Community 2`, `Community 43`, `Community 103`, `Community 178`, `Community 5`, `Community 247`, `Community 336`, `Community 316`, `Community 365`, `Community 63`, `Community 213`, `Community 319`, `Community 252`, `Community 320`, `Community 340`, `Community 253`, `Community 341`, `Community 16`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `Transport` connect `Community 261` to `Community 0`, `Community 179`, `Community 207`, `Community 355`, `Community 394`, `Community 283`, `Community 389`, `Community 392`, `Community 388`, `Community 390`, `Community 391`, `Community 393`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `FindingStatus` connect `Community 6` to `Community 56`, `Community 43`, `Community 5`, `Community 292`, `Community 137`, `Community 247`, `Community 178`, `Community 336`, `Community 150`, `Community 316`, `Community 365`, `Community 63`, `Community 213`, `Community 319`, `Community 252`, `Community 320`, `Community 340`, `Community 253`, `Community 341`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 173 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 173 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R` to the rest of the system?**
  _2054 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.015110650069156293 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.025137787337007663 - nodes in this community are weakly interconnected._