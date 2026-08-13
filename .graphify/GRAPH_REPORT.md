# Graph Report - .  (2026-08-11)

## Corpus Check
- Large corpus: 658 files · ~530,165 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 5724 nodes · 12444 edges · 321 communities detected
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 2776 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 2776 · contains: 2638 · calls: 1835 · method: 1327 · MODIFIES: 1265 · rationale_for: 1204 · imports: 474 · imports_from: 434 · ON_BRANCH: 229 · inherits: 185 · PARENT_OF: 77


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 658 · Candidates: 1508
- Excluded: 130 untracked · 63672 ignored · 6 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `3c277ba`
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
Nodes (37): BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL, HallucinationGuard — post-generation validation of LLM report text against the g, 298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, d1b4dd3 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, AttackLogger — records every attack action to the ``attack_timeline`` table.  Al, RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en, NucleiExploitRunner — CVE PoC validation using Nuclei templates.  Enforces templ (+29 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (59): check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, Raised when the binary is running on an unauthorized machine., Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B, agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit (+51 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (82): PROFILE_TOOLS, ModuleCategory, ModuleInput, ModuleOutput, modulesForPorts(), ScanModule, bySeverityCount(), runScan() (+74 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (71): engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, A previously-remediated finding whose issue reappeared this run: reopen     the, Background entry point (P1: keep detection OFF the probe-result request     path, (content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev, facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur, DetectionRun, Engagement, EngagementStatus (+63 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (53): ServiceFingerprint, FindingImport, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), NessusScanRequest, _nuclei_finding(), _nuclei_terminal_result(), NucleiScanRequest (+45 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (76): Agent, AgentStatus, Asset, AssetType, ScanJobStatus, ScanJobType, ScanJob, ScanResult (+68 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (45): _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database(), _check_jwt_secret(), _check_redis(), _check_required_env_vars() (+37 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (37): apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl(), Session, SESSION_DIR (+29 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (52): bin(), binName(), collectProcess(), hasBinary(), hasSystemBinary(), httpBannerGrab(), HttpxLine, isWindows() (+44 more)

### Community 9 - "Community 9"
Cohesion: 0.04
Nodes (46): ComplianceRef, COVERAGE_COLOR, DetectionCoverage, ExploitMaturity, Finding, FindingDetail(), FindingPage, FindingsPage() (+38 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (50): task_runner.py — orchestrates the full lifecycle of a single scan job.  Given a, use_cases.py — the finite, pre-defined library of scan scenarios the manager can, backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/probe-usecase-alignment, main, spike/probe-go, worktree-fleet-already-downloaded-cmd (+42 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (55): A, ask(), askSecret(), banner(), buildInteractiveCommand(), choose(), chooseNextPhase(), confirm() (+47 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (35): 5d5c158 refactor: remove unused dashboard components and mock data- Deleted SlaSummaryCell and ZoneRow components as they are no longer needed.- Removed mock data file mock-dashboard.ts, which contained static data for the dashboard.- Updated severity handling in severity.ts to support new dashboard design.- Added console-tokens.css for dashboard-specific styles, ensuring theme compatibility., Delta(), Meter(), Panel(), Readout(), Agent, AGENT_STATUS, AgentStatus (+27 more)

### Community 13 - "Community 13"
Cohesion: 0.05
Nodes (40): FindingSeverity, NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), NucleiMatch, boundedEnvMs(), OpenVASFinding (+32 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (29): get_read_db(), Read-only session (no commit) routed to the replica when configured.     For SEL, Read-only session (no commit) routed to the replica when configured.     For SEL, close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, Single source of truth for the deployed application version.  The value is injec (+21 more)

### Community 15 - "Community 15"
Cohesion: 0.08
Nodes (43): all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), normalize(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web() (+35 more)

### Community 16 - "Community 16"
Cohesion: 0.07
Nodes (8): _finding(), TestAggregate, TestClassifyTier, TestComputePriority, TestDedupFindings, TestFindingConsistency, TestSuppressNegated, TestVerify

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (44): ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is, Raises SafetyViolationError if module or payload is not permitted., Raises SafetyViolationError if module or payload is not permitted., Raises OutOfScopeError if target_ip not in engagement scope., Raises OutOfScopeError if target_ip not in engagement scope., Full exploit execution pipeline with safety, scope, blast radius,         audit, Full exploit execution pipeline with safety, scope, blast radius,         audit, Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo (+36 more)

### Community 18 - "Community 18"
Cohesion: 0.06
Nodes (21): interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act, FakeReader, FakeWriter, _probe(), Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol ( (+13 more)

### Community 19 - "Community 19"
Cohesion: 0.05
Nodes (12): result_spool.py — local result persistence with upload retry.  When the probe co, transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap, b5ffcb0 Refactor Vedha probe installer and enhance device identity tests- Updated the installer script to require only the manager endpoint in dry run mode, removing unnecessary prompts for credentials.- Changed the default behavior of LICENSE_ENFORCED to false.- Improved error handling for unknown arguments and missing required parameters in the installer.- Added tests for device identity generation, signing, and verification, ensuring robust handling of key encoding and site policy enforcement.- Enhanced HTTP lease tests to cover edge cases for lease renewal and cancellation.- Introduced tests for installer contract to ensure no human credentials are present in the source.- Updated result spool tests to handle permanent rejections and ensure proper quarantine behavior.- Improved transport tests to validate device enrollment and access token rotation.- Enhanced WebSocket claim protocol tests to verify job claiming with additional parameters., _objects(), test_expired_attempt_fails_job_when_retry_budget_is_exhausted(), test_expired_attempt_requeues_with_fence_history_preserved(), Tests for agent/result_spool.py, ResultSpool with tiny retry delay for fast tests. (+4 more)

### Community 20 - "Community 20"
Cohesion: 0.07
Nodes (16): _make_db(), _make_tenant(), _make_user(), Tests for authentication login flow.  Covers:   - login success   - user_not_fou, Ensure every exception class has the expected reason_code attribute.     These c, AsyncSession mock that returns user on first execute, tenant on second., TestAuthenticateBcryptFailure, TestAuthenticateDatabaseFailure (+8 more)

### Community 21 - "Community 21"
Cohesion: 0.14
Nodes (33): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+25 more)

### Community 22 - "Community 22"
Cohesion: 0.08
Nodes (9): _asset(), TestAssetNeedsRecheckLive, TestAssetOpenPortsForDeepScan, TestGate2, TestGate3, TestGate4, TestGate5, TestGate6 (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.07
Nodes (28): Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result., Remove the spool file for a successfully uploaded result., Attempt to upload a result with retries and local spool as fallback.          Ar, Move a terminally rejected result out of the retry queue., Re-attempt upload of all previously spooled results.          Called once at pro, Attempt to upload a result with retries and local spool as fallback.          Ar, Number of pending (unsubmitted) results in the spool. (+20 more)

### Community 24 - "Community 24"
Cohesion: 0.09
Nodes (26): AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Raised when the Anthropic SDK or API key is not configured., _tool_result(), _val() (+18 more)

### Community 25 - "Community 25"
Cohesion: 0.06
Nodes (40): _claim_batch(), _dead_letter_stale_stmt(), enqueue(), Event, _handle_facts_ready(), is_stale_processing(), main(), _mark_done() (+32 more)

### Community 26 - "Community 26"
Cohesion: 0.10
Nodes (21): DEMO_ASSET, DEMO_ENGAGEMENT, DEMO_FINDING, BASE, aiReportStore, hallucinationGuard, llmReportGenerator, ReportSection (+13 more)

### Community 27 - "Community 27"
Cohesion: 0.07
Nodes (24): _clean(), _Collector, Make a per-host scanner instance share ONE rate limiter + semaphore with all, Make a raw banner safe and readable for the summary line.      Many services ans, _rollup(), _run_active(), _shared(), main() (+16 more)

### Community 28 - "Community 28"
Cohesion: 0.10
Nodes (23): asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder, is_internet_exposed(), GraphBuilder — turns engagement assets/services/findings into an attack graph., Build the full multi-type attack graph. Returns the populated DiGraph         (a (+15 more)

### Community 29 - "Community 29"
Cohesion: 0.05
Nodes (20): _fake_run_scan(), Integration tests — full probe lifecycles exercised through the public APIs of a, Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., Phase 1: combined scope validation (validate + excludes)., Phase 1: result spool with upload retry., Phase 4 + Phase 1: Transport sends public_key during registration. (+12 more)

### Community 30 - "Community 30"
Cohesion: 0.05
Nodes (12): Tests for agent/transport.py, Create a Transport with a real state file path but no actual HTTP calls., Create a Transport with a real state file path but no actual HTTP calls., TestDeviceEnrollment, TestFetchScope, TestHeartbeat, TestHttpGet, TestPollJobs (+4 more)

### Community 31 - "Community 31"
Cohesion: 0.07
Nodes (26): ConnectionManager, GraphWebSocketManager, High-level manager for graph-specific WebSocket operations., Handle a new WebSocket client connection., Handle incoming WebSocket messages., Manages WebSocket connections with room-based broadcasting., Broadcast graph data update to all subscribers., Broadcast a single node update. (+18 more)

### Community 32 - "Community 32"
Cohesion: 0.12
Nodes (16): get_settings(), Settings, BaseSettings, AiGenerateRequest, AiGenerateResponse, AiMessage, AiProviderStatus, AiStatusResponse (+8 more)

### Community 33 - "Community 33"
Cohesion: 0.08
Nodes (28): BaseModel, ActivityItem, Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant, recent_activity(), AgentBootstrapRequest, LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated (+20 more)

### Community 34 - "Community 34"
Cohesion: 0.06
Nodes (21): PageShell(), PageShellProps, NAV_SECTIONS, NavItem, Sidebar(), SidebarProps, ActivityItem, ComplianceControl (+13 more)

### Community 35 - "Community 35"
Cohesion: 0.11
Nodes (16): RateLimiter, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim, ServiceIdentifier — banner + port → structured service fingerprint. Handles: HTT, ServiceIdentifier, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner (+8 more)

### Community 36 - "Community 36"
Cohesion: 0.12
Nodes (10): _candidate(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db(), TestCPECandidateCpe23, TestEnrichFinding, TestEpssDb, TestKevDb (+2 more)

### Community 37 - "Community 37"
Cohesion: 0.09
Nodes (20): AdvisorFlow(), PATCH_PILL, AssistantDrawer(), ExplainResponse, Msg, Served, FactCard(), AiStatus (+12 more)

### Community 38 - "Community 38"
Cohesion: 0.07
Nodes (19): 9a36729 feat(resolution): coverage builder from completed-scanner facts, bd409f5 feat(resolution): async applier over engine-managed open findings, cbf5d6c feat(resolution): pure decision core (coverage + confirm window + db guard), ddb51f2 feat(resolution): add finding resolution-lifecycle columns + migration, apply_manual_reopen(), build_coverage(), decide_resolution(), evaluate_resolutions() (+11 more)

### Community 39 - "Community 39"
Cohesion: 0.08
Nodes (24): _boundary_versions(), _clear_caches(), _content_hash(), _default_products(), load_snapshot(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Raw OSV vulnerability records for this product, or [] if the         snapshot do, The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre- (+16 more)

### Community 40 - "Community 40"
Cohesion: 0.09
Nodes (31): config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES, Client, ClientJiraConfig, ClientNotifyConfig (+23 more)

### Community 41 - "Community 41"
Cohesion: 0.08
Nodes (18): AssetCriticality, OrderedDict, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path, AssetIn, AssetOut, BulkAssetImportResult, parse_csv_assets(), Parse CSV text into a list of AssetIn models and error strings. (+10 more)

### Community 42 - "Community 42"
Cohesion: 0.08
Nodes (29): device_hint(), fuse_liveness(), HostDiscoveryScanner, is_locally_administered(), Neighbor, normalize_mac(), _now(), parse_neighbor_line() (+21 more)

### Community 43 - "Community 43"
Cohesion: 0.08
Nodes (24): ApiActivity, GET, 0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner UI, GET, POST, Exposure, GET, INTENSITY_PRESETS (+16 more)

### Community 44 - "Community 44"
Cohesion: 0.12
Nodes (30): buildToolsCommand(), C, ln(), showSpinner(), downloadFile(), extract(), getInstalledRecord(), installAll() (+22 more)

### Community 45 - "Community 45"
Cohesion: 0.07
Nodes (26): AssetInput, chat(), CRITICALITY_SCORE, DESTRUCTIVE_PATTERNS, EPSS_MOCK, FindingInput, generateReport(), getClient() (+18 more)

### Community 46 - "Community 46"
Cohesion: 0.11
Nodes (28): activate_enrollment(), approve_enrollment(), _authenticated_request(), create_enroll_token(), create_enrollment_request(), _decode_public_key(), _derive_refresh_secret(), enroll_token_is_usable() (+20 more)

### Community 47 - "Community 47"
Cohesion: 0.07
Nodes (19): ToastContext, EnrollmentRequest, FleetResponse, inputStyle, useToast(), ActivityItem, AssetRow, displayDate() (+11 more)

### Community 48 - "Community 48"
Cohesion: 0.12
Nodes (21): AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient, propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Test double — a fixed lookup table, no network. Used to validate the     surroun (+13 more)

### Community 49 - "Community 49"
Cohesion: 0.11
Nodes (25): AuthContext, Handler, generateOtp(), OtpEntry, otpStore, OtpVerifyResult, SessionPayload, verifyOtp() (+17 more)

### Community 50 - "Community 50"
Cohesion: 0.13
Nodes (20): ADConnectionError, DependencyMissingError, Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., ADComputer, ADGroup, ADUser, _as_list() (+12 more)

### Community 51 - "Community 51"
Cohesion: 0.09
Nodes (31): _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), has_ambiguous_epoch() (+23 more)

### Community 52 - "Community 52"
Cohesion: 0.09
Nodes (24): NucleiExploitRunner, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Parse nuclei JSONL output for a single CVE PoC result., Parse nuclei JSONL output for a single CVE PoC result., Run Nuclei CVE PoC templates against a single target.     Every template is safe, Run Nuclei CVE PoC templates against a single target.     Every template is safe, Parse template YAML and validate it contains no write/delete/DoS actions. (+16 more)

### Community 53 - "Community 53"
Cohesion: 0.09
Nodes (29): AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError, ExpiredPasswordError, JWTFailureError (+21 more)

### Community 54 - "Community 54"
Cohesion: 0.08
Nodes (14): aggregate(), ConsistencyReport, FindingConsistency, format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, run_findings: one list of Findings per run (N runs). Aggregated by     the deter, The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen (+6 more)

### Community 55 - "Community 55"
Cohesion: 0.11
Nodes (24): GET, POST, ApiActivity, fail(), GET, PUT(), DETECTION_TO_UI, ENG_STATUS_TO_API (+16 more)

### Community 56 - "Community 56"
Cohesion: 0.08
Nodes (15): ATTACK_TIMELINE, AttackAction, correlationRuns, CoverageStats, DetectionOutcome, DetectionResult, detectionStore, EDR_DETECTIONS (+7 more)

### Community 57 - "Community 57"
Cohesion: 0.10
Nodes (19): _metric(), _not_scored(), Pure helpers for controlled Probe capability and accuracy validation., Validate the small, explicit inventory used for accuracy scoring., Score promoted inventory against explicit host/port/service/CVE truth., Resolve suites plus explicit use-cases, preserving first-seen order., Require every IP/CIDR target to be fully allowed and not excluded., Return the conservative number of addresses represented by targets. (+11 more)

### Community 58 - "Community 58"
Cohesion: 0.10
Nodes (17): 045c9ae fix(posture): normalize run_at in _present_in_run; drop dead scores_prev call; tidy test import, 237a831 feat(posture): add run comparison, matrix, and response builder, 2cddd52 fix(posture): tenant-scope run helper; test null asset/score paths; tidy test import, 5238865 feat(posture): add pure scoring core (noisy-OR risk/exploit/posture), 9de087a feat(posture): add GET /analytics/posture endpoint, _finding_views(), posture(), Map joined (Finding, Asset.criticality) rows to duck-typed views. (+9 more)

### Community 59 - "Community 59"
Cohesion: 0.08
Nodes (13): 0fbec7d feat(verification): add finding verification verdict columns + migration, caf1e5d feat(verification): deterministic passive verdict core, de2d1c9 feat(verification): optional fail-closed LLM rationale + FP-triage, compute_verdict(), _int_confidence(), _qualifies_for_llm(), verification.py — normalized, dashboard-facing verification verdict.  The determ, Deterministic passive verdict from a detection finding's evidence dict. (+5 more)

### Community 60 - "Community 60"
Cohesion: 0.11
Nodes (9): EvidenceTier, IntEnum, _fact(), TestAsset, TestCorrelateSmbPatch, TestFactRef, TestNormalize, TestNormalizeBanner (+1 more)

### Community 61 - "Community 61"
Cohesion: 0.11
Nodes (6): _scan_result(), TestAssetMergeCredentialed, TestAssetMergeHostDiscovery, TestAssetMergePortScan, TestClassifyCertainty, TestWorkflowCache

### Community 62 - "Community 62"
Cohesion: 0.11
Nodes (24): _finalize_trace(), _gather_per_host(), _port_candidates(), workflow_engine.py — the async DAG executor. Loops through gates, checks precond, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Return TCP ports worth scanning for this profile and requested branch set., In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass (+16 more)

### Community 63 - "Community 63"
Cohesion: 0.13
Nodes (17): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., ADError, build_ad_finding() (+9 more)

### Community 64 - "Community 64"
Cohesion: 0.10
Nodes (14): _cache_key(), _clear_caches(), EpssDB, KevDB, load_epss(), load_kev(), enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as vuln_d, {'epss': float, 'percentile': float} or None if not covered. (+6 more)

### Community 65 - "Community 65"
Cohesion: 0.13
Nodes (22): _compute_priority(), enrich_finding(), enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier., Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr, Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li, match_candidate(), matcher.py — does this CPE candidate's version fall inside a vulnerable range, p, dpkg_compare, but None instead of a misleading answer when one side     has an e (+14 more)

### Community 66 - "Community 66"
Cohesion: 0.14
Nodes (14): ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM, Read pKICertificateTemplate objects from the Configuration NC. (+6 more)

### Community 67 - "Community 67"
Cohesion: 0.10
Nodes (22): Agent, AgentCapability, AGENTS, agentsStore, AgentStatus, ensureDataDir(), FIELD_AGENTS_FILE, FieldAgent (+14 more)

### Community 68 - "Community 68"
Cohesion: 0.08
Nodes (2): _ExplodingScanner, test_per_target_exception_preserves_other_results()

### Community 69 - "Community 69"
Cohesion: 0.13
Nodes (11): CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender, _parse_dt(), EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender, Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi, SentinelOne via the REST ``/web/api/v2.1/threats`` endpoint.     config: {base_u (+3 more)

### Community 70 - "Community 70"
Cohesion: 0.13
Nodes (11): ElasticSIEM, _parse_dt(), SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi, Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_, Abstract SIEM connector., Splunk via the REST search endpoint (``/services/search/jobs/export``) with an, SentinelSIEM (+3 more)

### Community 71 - "Community 71"
Cohesion: 0.08
Nodes (15): apiFetch(), Cat, CATS, Engagement, EngineManifest, getToken(), Intensity, JobStatus (+7 more)

### Community 72 - "Community 72"
Cohesion: 0.11
Nodes (24): assessment(), discovery(), EngagementMode, host_discovery(), includes_stage(), port_scan(), modes.py — engagement mode configurations. Each mode is a thin config that tunes, Discovery + ports + banner only — no deep dives, no credentials. (+16 more)

### Community 73 - "Community 73"
Cohesion: 0.09
Nodes (16): Agent, AIBrainPage(), AiStatus, criticalChain, defaultAgents, Engagement, Finding, findings (+8 more)

### Community 74 - "Community 74"
Cohesion: 0.13
Nodes (12): Exception, MetasploitRPCClient, MetasploitRPCError, MetasploitRPCClient — async client for msfrpcd.  Protocol: MessagePack RPC over, Returns {status, output, uuid}., Returns True if job was successfully killed., Poll until job completes or max_wait exceeded., Authenticated RPC call — prepends token. (+4 more)

### Community 75 - "Community 75"
Cohesion: 0.09
Nodes (18): ADJ, ATTACK_PATHS, AttackPath, BlastRadiusResult, buildAttackPaths(), Chokepoint, CHOKEPOINTS, edgesForPath() (+10 more)

### Community 76 - "Community 76"
Cohesion: 0.08
Nodes (1): TestResultSpool

### Community 77 - "Community 77"
Cohesion: 0.08
Nodes (8): Tests for seed_admin.py.  Covers:   - first deployment: creates tenant + admin,, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset, TestFirstDeployment, TestHashHelpers, TestPasswordRotation, TestValidateEnv

### Community 78 - "Community 78"
Cohesion: 0.14
Nodes (15): KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline, Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., One aggregate Finding for all kerberoastable accounts.         Severity is Criti, One aggregate Finding for all kerberoastable accounts.         Severity is Criti, Enumerate kerberoastable accounts and capture TGS evidence., Enumerate kerberoastable accounts and capture TGS evidence. (+7 more)

### Community 79 - "Community 79"
Cohesion: 0.09
Nodes (11): 02b6341 feat(active-validation): pure escalation decision core, 58c2d10 feat(active-validation): ValidationRequest model + migration, 7bd104a feat(active-validation): pure result interpretation, interpret_validation(), active_validation.py — manager-side decision core for safe active validation.  P, True iff this finding warrants an approval-gated active re-check.     Escalate o, Map a probe safe-check result to a verdict transition. Anything that isn't     a, should_escalate() (+3 more)

### Community 80 - "Community 80"
Cohesion: 0.11
Nodes (13): 0d6be85 feat(risk-rank): explainable 0-1000 finding priority, 3c277ba feat(lifecycle): add POST /findings/{id}/reopen endpoint, 3c7740e feat(lifecycle): pure manual-reopen helper, 85e4537 feat(risk-rank): expose risk_rank on findings API; add P2/P3/P4 plans, get_finding(), patch_finding(), Operator reverses a resolution (auto or manual). Only a `remediated`     finding, reopen_finding() (+5 more)

### Community 81 - "Community 81"
Cohesion: 0.09
Nodes (10): AiStatus, ConfigField, DEFAULT_RULES, DeploymentStatus, EMAIL_FIELDS, EnvSetting, INTEGRATIONS, JIRA_FIELDS (+2 more)

### Community 82 - "Community 82"
Cohesion: 0.13
Nodes (17): 8cf23c2 feat(resolution): wire coverage ledger + auto-resolution into detection run, 937737b feat(resolution): reopen + flag regressions on the original finding row, _apply_regression_reopen(), create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), _find_remediated_match(), A remediated finding with the same (engagement, asset, title) — the     regressi (+9 more)

### Community 83 - "Community 83"
Cohesion: 0.09
Nodes (15): _ike_probe(), interpret_ipmi(), interpret_sip(), _ipmi_probe(), _mdns_probe(), udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, TFTP RRQ for a non-existent file.  Error reply confirms TFTP service., RMCP Ping (ASF Presence Ping) to detect IPMI/BMC. (+7 more)

### Community 84 - "Community 84"
Cohesion: 0.11
Nodes (6): _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_background_job_failed(), test_partial_nuclei_run_preserves_findings_and_diagnostics()

### Community 85 - "Community 85"
Cohesion: 0.13
Nodes (11): _make_http_mock(), Unit tests for VulnEnrichmentService — all external HTTP calls mocked., Create a mock httpx.AsyncClient that returns different responses per URL., test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full(), test_fetch_epss_success() (+3 more)

### Community 86 - "Community 86"
Cohesion: 0.14
Nodes (19): _env_number(), _error_result(), _facts_from_cache(), _job_runtime_seconds(), LeaseLostError, engine.py — adapt a manager scan job to scanner_module's workflow engine and ret, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Return the effective whole-job deadline; callers can only reduce it. (+11 more)

### Community 87 - "Community 87"
Cohesion: 0.21
Nodes (14): AttackAction, _aware(), DetectionCorrelator, DetectionResultDTO, _host_matches(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale, Normalise naive datetimes to UTC so comparisons never raise., AttackTimeline (+6 more)

### Community 88 - "Community 88"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 89 - "Community 89"
Cohesion: 0.10
Nodes (9): Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG, TestAssetMergePassiveCollect, TestAssetMergeServiceBanner, TestAssetMergeSmbScan, TestAssetMergeTlsScan, TestAssetMergeUnknownScanner, TestAssetMergeWebScan, TestCacheEntry (+1 more)

### Community 90 - "Community 90"
Cohesion: 0.11
Nodes (17): JobResult, Structured result from running one scan job., Submit the result, with spool-and-retry if available., Structured result from running one scan job., Submit the result, with spool-and-retry if available., Submit the result, with spool-and-retry if available., Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Orchestrates one scan job's lifecycle.      The runner holds injected dependenci (+9 more)

### Community 91 - "Community 91"
Cohesion: 0.13
Nodes (12): _decode_value(), _encode_oid(), _extract_sysdescr(), _oid_in_subtree(), Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli, Return (community, sysdescr) for the first responding community, or None., GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]., One GETBULK request — measure response/request size ratio. (+4 more)

### Community 92 - "Community 92"
Cohesion: 0.17
Nodes (19): aggregate(), build_posture(), _clamp01(), compare(), compute_scores(), _exploit_prob(), FindingView, grade_for() (+11 more)

### Community 93 - "Community 93"
Cohesion: 0.21
Nodes (6): _asset(), _finding(), _mock_db(), _resp(), TestLLMReportGenerator, TestVulnPrioritizer

### Community 94 - "Community 94"
Cohesion: 0.11
Nodes (7): BloodHoundCollector, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., Run bloodhound-python and return the list of produced JSON file paths.         R, TestASREPRoastChecker

### Community 95 - "Community 95"
Cohesion: 0.12
Nodes (12): metadata, QueryProvider(), Theme, ThemeContext, ThemeContextValue, ThemeProvider(), useTheme(), Toast (+4 more)

### Community 96 - "Community 96"
Cohesion: 0.15
Nodes (11): ApiError, clearAuth(), errorMessage(), fetchJson(), getStoredToken(), isUnauthorized(), storeToken(), btn (+3 more)

### Community 97 - "Community 97"
Cohesion: 0.15
Nodes (10): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+2 more)

### Community 98 - "Community 98"
Cohesion: 0.12
Nodes (14): interpret_dns_recursion(), interpret_ike(), interpret_mdns(), interpret_memcached_stats(), interpret_ntp_monlist(), interpret_ssdp(), _ntp_monlist_probe(), SIP OPTIONS request — safe fingerprint method. (+6 more)

### Community 99 - "Community 99"
Cohesion: 0.14
Nodes (4): Asset, _parse_ts(), PortFact, asset.py — per-host fact model the workflow engine reasons about.  This is an OR

### Community 100 - "Community 100"
Cohesion: 0.17
Nodes (16): _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError, license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the (+8 more)

### Community 101 - "Community 101"
Cohesion: 0.33
Nodes (15): LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses, Raised when the Anthropic SDK or API key is not configured., DetectionResult, ReviewStatus, LLMOutput, Every LLM generation is persisted here for human-in-the-loop review.      AI out (+7 more)

### Community 102 - "Community 102"
Cohesion: 0.18
Nodes (10): AiMessage, ManagerAiResponse, POST(), validMessages(), ManagerAiResponse, ManagerAiResponse, parseAdvisor(), publicCveRecord() (+2 more)

### Community 103 - "Community 103"
Cohesion: 0.11
Nodes (3): 1fe16c8 stable but some dead code, need to optimize, Product-boundary tests for the single-dashboard Manager API., Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises

### Community 104 - "Community 104"
Cohesion: 0.12
Nodes (11): ActivityItem, DashboardCharts(), Engagement, Finding, FindingPage, FindingSummary, SEV, STATUS_STYLE (+3 more)

### Community 105 - "Community 105"
Cohesion: 0.15
Nodes (12): correlate_smb_patch(), dedup_findings(), _product_from_cpe(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Suppress a suspected/potential (inferred-source) finding when the     SAME host (+4 more)

### Community 106 - "Community 106"
Cohesion: 0.14
Nodes (14): _coverage(), _device_hint(), _listener_error_code(), _open_listener(), PassiveListenerError, _printable_strings(), passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)., All passive sources failed before the listen window could start. (+6 more)

### Community 107 - "Community 107"
Cohesion: 0.15
Nodes (8): _cloud(), Settings with provider unset and all cloud keys pinned, so .env cannot     leak, test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter(), test_default_auto_detects_the_configured_cloud_provider(), test_default_runtime_fails_closed_without_any_cloud_key(), test_fallback_never_includes_local_ollama(), test_generate_fails_closed_when_no_cloud_provider_configured(), test_status_fails_safe_without_cloud_key()

### Community 108 - "Community 108"
Cohesion: 0.21
Nodes (1): TestServiceIdentifier

### Community 109 - "Community 109"
Cohesion: 0.13
Nodes (17): _flush_spool_over_http(), Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Poll pending jobs even while WS is connected.      This makes result delivery re (+9 more)

### Community 110 - "Community 110"
Cohesion: 0.13
Nodes (13): GzipRequestMiddleware, Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., _service_root(), agent_jwt_path_allows(), _is_public_enrollment_request(), Extracts JWT from Authorization header and injects tenant_id + user     claims i, Extracts JWT from Authorization header and injects tenant_id + user     claims i (+5 more)

### Community 111 - "Community 111"
Cohesion: 0.15
Nodes (14): SeverityChip(), deadlineTitle(), elapsedPct(), pct(), Sev, SEV_STYLE, SlaItem, SlaRowView() (+6 more)

### Community 112 - "Community 112"
Cohesion: 0.18
Nodes (15): addComment(), Case, CaseActivity, CaseComment, CaseSeverity, CaseStatus, createCase(), DATA_FILE (+7 more)

### Community 113 - "Community 113"
Cohesion: 0.18
Nodes (9): classify_os_error(), _family_of(), PortScanner, port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD, Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, One connect() and its classification. Always returns a ScanResult         (open (+1 more)

### Community 114 - "Community 114"
Cohesion: 0.24
Nodes (15): _detect_drift(), _hash(), _log(), log_error(), log_info(), log_warn(), main(), Warn if the tenant has multiple admins or a stale admin email. (+7 more)

### Community 115 - "Community 115"
Cohesion: 0.15
Nodes (16): _bounded_env_int(), _is_local_manager_url(), main(), _poll_jobs_or_empty(), Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease. (+8 more)

### Community 116 - "Community 116"
Cohesion: 0.14
Nodes (15): bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity(), pubkey_to_bytes(), scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.  T (+7 more)

### Community 117 - "Community 117"
Cohesion: 0.13
Nodes (7): Agent, AGENT_STATUS, AgentStatus, PATH_STATUS, SEV_LABEL, DashboardGrid(), useMouseGradient()

### Community 118 - "Community 118"
Cohesion: 0.17
Nodes (6): DetectionGap, Return a Sigma rule (YAML string) for the technique, customised with the, SigmaRuleGenerator, _stable_rule_id(), Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc, TestEDRParsing

### Community 119 - "Community 119"
Cohesion: 0.18
Nodes (13): approve_report(), _build_engagement_summary(), build_posture_report_section(), get_draft(), _output_out(), _pending_outputs(), Deterministic report section from the same posture payload the dashboard uses., Background task: build the summary, generate every section, persist as pending. (+5 more)

### Community 120 - "Community 120"
Cohesion: 0.15
Nodes (11): BaseScanner, main_entrypoint(), Subclasses implement `scan_target(self, target)` (async), returning a list     o, One observation about one target. Pure fact, no interpretation., One observation about one target. Pure fact, no interpretation., Run a scanner CLI's body with consistent, operator-friendly error handling., Subclasses implement `scan_target(self, target)` (async), returning a list     o, Subclasses implement `scan_target(self, target)` (async), returning a list     o (+3 more)

### Community 121 - "Community 121"
Cohesion: 0.15
Nodes (8): Read-only view of allowed networks (for CIDR-level engines)., Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude)., Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, ScopeError, ScopeGuard

### Community 122 - "Community 122"
Cohesion: 0.18
Nodes (14): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None. (+6 more)

### Community 123 - "Community 123"
Cohesion: 0.25
Nodes (15): _mock_session(), _now(), _sql(), test_boundary_at_exactly_the_lease_is_reclaimed(), test_dead_letter_and_requeue_are_mutually_exclusive(), test_dead_letter_stmt_targets_exhausted_stranded_rows(), test_expired_processing_lock_is_reclaimed(), test_fresh_processing_lock_is_not_reclaimed() (+7 more)

### Community 124 - "Community 124"
Cohesion: 0.14
Nodes (6): NTLMRelayChecker, Build a Finding for hosts missing SMB signing. The attack_narrative         incl, Probe SMB/LDAP signing posture across a host list., For each IP, returns {signing_enabled, signing_required}.          A host is rel, Returns True if the DC *enforces* LDAP signing / channel binding.          We at, TestNTLMRelayChecker

### Community 125 - "Community 125"
Cohesion: 0.13
Nodes (15): Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Release a staged job only after the manager confirms its claim., Re-submit previously spooled results over WebSocket. (+7 more)

### Community 126 - "Community 126"
Cohesion: 0.16
Nodes (14): fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), scope_validator.py — defense-in-depth scope re-validation for the probe.  The pr, Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)., Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Parse one IP, CIDR, or inclusive IP range into covering networks.      ``None`` (+6 more)

### Community 127 - "Community 127"
Cohesion: 0.17
Nodes (7): Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh a device token before expiry; legacy identities are unchanged., Refresh routing metadata using the cached agent identity.          Returns True

### Community 128 - "Community 128"
Cohesion: 0.19
Nodes (8): extract_features(), Fit an XGBoost regressor on historical findings. ``historical_findings_df``, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)., Build the model's feature vector from a Finding (+ optional Asset + extra     co, _to_float(), VulnPrioritizer

### Community 129 - "Community 129"
Cohesion: 0.13
Nodes (6): verification_graph.py — optional LangGraph orchestration for passive verificatio, Run passive verification. Uses the LangGraph StateGraph when available;     othe, run_verification(), 2fcec73 feat(verification): stamp verdicts on detection-run findings (flagged), 72f68af feat(verification): expose verification verdict + needs_review on findings API, c02c465 feat(verification): optional LangGraph orchestration skin

### Community 130 - "Community 130"
Cohesion: 0.20
Nodes (7): PathAnalyzer, Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for, Assets reachable (and thus at risk) if ``compromised_asset_id`` is owned., Best (easiest) exploitable finding on an asset: {cvss, weight, finding}., Build (and cache) the Asset→Asset movement projection. Edge weight is the, _safe_float()

### Community 131 - "Community 131"
Cohesion: 0.13
Nodes (12): approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest, ExploitEvidence, ExploitJob, ExploitResult (+4 more)

### Community 132 - "Community 132"
Cohesion: 0.13
Nodes (12): bracket_host(), inet_checksum(), scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD, Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP,, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h (+4 more)

### Community 133 - "Community 133"
Cohesion: 0.21
Nodes (4): TestEnqueueAgentJob, TestListAgents, TestOTProfileGate, _user()

### Community 134 - "Community 134"
Cohesion: 0.22
Nodes (2): _action(), TestDetectionCorrelator

### Community 135 - "Community 135"
Cohesion: 0.17
Nodes (10): looks_like_db(), looks_like_http(), looks_like_tls(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, True when this port's banner result is exactly the silent-on-garbage     signatu, For every open port with a banner fact, returns {port: {branches}}     that obse, True when a service banner carries a database greeting signature, so a DB     on (+2 more)

### Community 136 - "Community 136"
Cohesion: 0.13
Nodes (5): When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., TestRunnerScopeValidation

### Community 137 - "Community 137"
Cohesion: 0.14
Nodes (14): _check_anti_debug(), Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block (+6 more)

### Community 138 - "Community 138"
Cohesion: 0.14
Nodes (14): _enroll_device(), _load_or_create_signing_identity(), _obtain_identity(), Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Load or atomically create the probe's Ed25519 enrollment identity. (+6 more)

### Community 139 - "Community 139"
Cohesion: 0.18
Nodes (12): AgentDeps, AgentOpts, isBlocked(), requiresApproval(), runAutonomousEngagement(), Rung, RUNG_LABELS, AgentState (+4 more)

### Community 140 - "Community 140"
Cohesion: 0.22
Nodes (13): client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId, PhaseRecommendation, planExploit() (+5 more)

### Community 141 - "Community 141"
Cohesion: 0.23
Nodes (13): DeclarativeBase, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., Append-only ledger of every attack action performed during an engagement.      W, Immutable, append-only audit trail for all exploit actions.     No TimestampMixi, Base, TimestampMixin, UUIDMixin, Per-engagement SIEM + EDR connection settings used by the detection     validati (+5 more)

### Community 142 - "Community 142"
Cohesion: 0.23
Nodes (13): _all_known_cve_ids(), main(), _query_osv(), update_snapshot.py — the ONLY module in this package that talks to the network., The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, EPSS scores for exactly the CVE IDs this detection run actually cares     about, Some macOS python.org installs ship expecting `Install Certificates.     command, All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n (+5 more)

### Community 143 - "Community 143"
Cohesion: 0.16
Nodes (7): AdversaError, AdversaErrorOpts, diagnoseSpawnError(), ErrorCode, Errors, VedhaError, VedhaErrorOpts

### Community 144 - "Community 144"
Cohesion: 0.27
Nodes (13): createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), Job, JOBS_FILE (+5 more)

### Community 145 - "Community 145"
Cohesion: 0.16
Nodes (10): OSError, NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here., # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree (+2 more)

### Community 146 - "Community 146"
Cohesion: 0.19
Nodes (12): _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them., Excluded networks -> masscan --exclude specs, so they get ZERO packets., A CIDR spec is in scope only if it is fully contained in an allowed network., target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them. (+4 more)

### Community 147 - "Community 147"
Cohesion: 0.14
Nodes (12): async_udp_probe(), async_udp_probe_retry(), Send one UDP datagram and await the first reply — fully on the event loop., Writes ScanResult objects as JSONL to a file and/or stdout., Send one UDP datagram and await the first reply — fully on the event loop., Writes ScanResult objects as JSONL to a file and/or stdout., Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de (+4 more)

### Community 148 - "Community 148"
Cohesion: 0.14
Nodes (6): Unit tests for the agent/probe protocol changes:   * agent polling is restricted, TestAccessTokenExpiry, TestAgentExecutableTypes, TestAgentRegistrationRefresh, TestHeartbeat, TestLegacyBootstrap

### Community 149 - "Community 149"
Cohesion: 0.14
Nodes (1): TestValidateTargetsInScope

### Community 150 - "Community 150"
Cohesion: 0.20
Nodes (5): CacheEntry, classify_certainty(), True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, WorkflowCache

### Community 151 - "Community 151"
Cohesion: 0.22
Nodes (3): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., True when execution produced errors and no usable or cached facts.

### Community 152 - "Community 152"
Cohesion: 0.17
Nodes (10): Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed)., Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable). (+2 more)

### Community 153 - "Community 153"
Cohesion: 0.18
Nodes (9): EMPTY_FORM, Engagement, EngagementsPage(), EngagementsResponse, EngagementStatus, FormState, hasValidDateRange(), splitEntries() (+1 more)

### Community 154 - "Community 154"
Cohesion: 0.36
Nodes (12): _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius(), _build_analyzer(), _critical_asset_ids(), _explain_hop(), get_attack_path() (+4 more)

### Community 155 - "Community 155"
Cohesion: 0.29
Nodes (4): _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator

### Community 156 - "Community 156"
Cohesion: 0.22
Nodes (7): _mock_response(), Unit tests for NessusScanner — all HTTP calls mocked., test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()

### Community 157 - "Community 157"
Cohesion: 0.26
Nodes (7): FakeProcess, _finding_line(), test_nonzero_exit_retains_and_marks_partial_findings(), test_nonzero_exit_without_findings_raises_with_stderr(), test_run_scan_streams_jsonl_and_separates_timeouts(), test_template_initialization_failure_cannot_be_clean_zero(), test_timeout_retains_findings_emitted_before_termination()

### Community 158 - "Community 158"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 159 - "Community 159"
Cohesion: 0.18
Nodes (3): decode_key(), Verify a Manager-signed policy and return its public key for TOFU pinning., verify_site_policy()

### Community 160 - "Community 160"
Cohesion: 0.26
Nodes (7): HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber(), isOptionalString(), normalizePort(), parseHttpxJsonLine()

### Community 161 - "Community 161"
Cohesion: 0.18
Nodes (9): CheckOpts, groupResults(), NativePortResult, nativePortScan(), NativeScanOpts, PORT_NAMES, PortRange, resolvePorts() (+1 more)

### Community 162 - "Community 162"
Cohesion: 0.39
Nodes (10): _ber_len(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _oid_tlv(), snmp_scanner.py — full SNMP enumeration: community discovery, targeted MIB walk,, _req_id_tlv(), _snmp_msg() (+2 more)

### Community 163 - "Community 163"
Cohesion: 0.29
Nodes (3): _enum_with_entries(), _FakeEntry, TestLDAPEnumeratorParsing

### Community 164 - "Community 164"
Cohesion: 0.21
Nodes (4): _claim_fixture(), TestAgentWebSocketAuthentication, TestAtomicWebSocketClaim, TestJobSecretBoundary

### Community 165 - "Community 165"
Cohesion: 0.17
Nodes (1): TestAgentJobCompatibility

### Community 166 - "Community 166"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 167 - "Community 167"
Cohesion: 0.24
Nodes (5): _Socket, test_collector_raises_when_no_listener_binds(), test_ot_udp_backend_never_joins_or_transmits(), test_subset_listener_failure_reports_degraded_coverage(), _Writer

### Community 168 - "Community 168"
Cohesion: 0.17
Nodes (2): Tests that use the real engine but with no-op callbacks., TestRunnerHeadless

### Community 169 - "Community 169"
Cohesion: 0.18
Nodes (11): Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation., Send periodic heartbeats over WebSocket., Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket. (+3 more)

### Community 170 - "Community 170"
Cohesion: 0.25
Nodes (10): _identity_ip(), process_job_result(), Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu, Stable idempotency checksum for one attempt completion payload., Return network identities that could create assets or findings.      Scanner-lev, Parse a probe identity as an IP, tolerating common host:port notation., Return result identities outside the job's authoritative IP scope.      Fail clo, result_checksum() (+2 more)

### Community 171 - "Community 171"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 172 - "Community 172"
Cohesion: 0.18
Nodes (7): Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., TestPromoteAssets

### Community 173 - "Community 173"
Cohesion: 0.18
Nodes (1): TestHallucinationGuard

### Community 174 - "Community 174"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 175 - "Community 175"
Cohesion: 0.18
Nodes (1): TestNucleiExploitRunner

### Community 176 - "Community 176"
Cohesion: 0.18
Nodes (1): TestValidatePayload

### Community 177 - "Community 177"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 178 - "Community 178"
Cohesion: 0.20
Nodes (2): test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses(), _token()

### Community 179 - "Community 179"
Cohesion: 0.18
Nodes (1): TestNmapXMLParser

### Community 180 - "Community 180"
Cohesion: 0.22
Nodes (10): classify_scanner_error(), engine_manifest(), ErrorDetail, planned_components(), Execution telemetry and failure normalization for the probe workflow., Resolve the exact collector plan for one workflow invocation., Map low-level failures into stable, operator-actionable categories., Represent an unexpected component exception without aborting other hosts. (+2 more)

### Community 181 - "Community 181"
Cohesion: 0.20
Nodes (5): HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Transport

### Community 182 - "Community 182"
Cohesion: 0.24
Nodes (4): BaseScanner, DBScanner, _netbios_session(), SMBScanner

### Community 183 - "Community 183"
Cohesion: 0.33
Nodes (1): ExploitOrchestrator

### Community 184 - "Community 184"
Cohesion: 0.27
Nodes (7): COMMON_RANGES, estimateHostCount(), isValidTarget(), ParseResult, parseTargets(), RFC1918, validOctets()

### Community 185 - "Community 185"
Cohesion: 0.27
Nodes (5): check(), _fact(), _free_port(), _Handler, main()

### Community 186 - "Community 186"
Cohesion: 0.20
Nodes (10): _agent_token_from_websocket(), agent_websocket_endpoint(), _claim_pushed_job(), Persistent WebSocket for probe → manager push communication.      Authentication, Persistent WebSocket for probe → manager push communication.      Authentication, Read an agent bearer token exclusively from the non-logged auth header., Read an agent bearer token exclusively from the non-logged auth header., Persistent WebSocket for probe → manager push communication.      Query params: (+2 more)

### Community 187 - "Community 187"
Cohesion: 0.24
Nodes (4): AdaptiveRateController, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window)., Current integer window (>= min_window).

### Community 188 - "Community 188"
Cohesion: 0.20
Nodes (7): Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., TestRegisterAgent

### Community 189 - "Community 189"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 191 - "Community 191"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 192 - "Community 192"
Cohesion: 0.20
Nodes (2): Each encryption uses a fresh ephemeral key, so blobs are different., TestEncryptDecryptRoundtrip

### Community 193 - "Community 193"
Cohesion: 0.20
Nodes (1): TestSubmitResult

### Community 194 - "Community 194"
Cohesion: 0.20
Nodes (7): Push a job to the first online connected agent.          Returns the agent_id th, Push a job to the first online agent in the requested tenant.          Returns t, Push a job to the first online agent in the requested tenant.          Returns t, Return idle connected agents belonging to exactly one tenant., Return idle connected agents belonging to exactly one tenant., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'.

### Community 195 - "Community 195"
Cohesion: 0.20
Nodes (6): AgentConnectionManager, Record transport features explicitly advertised by a connected probe., Record transport features explicitly advertised by a connected probe., Tracks WebSocket connections from probes/agents for direct job push.      Each c, Register an agent's WebSocket connection.          If the agent already has a co, Register an agent's WebSocket connection.          If the agent already has a co

### Community 196 - "Community 196"
Cohesion: 0.22
Nodes (9): _applied_tuning(), _build_run_stats(), _count_open_port_facts(), _hosts_from_facts(), Count concrete open services, not generic host-liveness observations., Count unique open network endpoints, not every confirming scanner fact., Build promotion-ready hosts without duplicating scanner facts per port., Serialize effective limits without ever echoing credential values. (+1 more)

### Community 197 - "Community 197"
Cohesion: 0.22
Nodes (7): Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active.

### Community 198 - "Community 198"
Cohesion: 0.31
Nodes (5): HallucinationGuard, Run all relevant checks and return a combined verdict:         ``{valid, issues,, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide.

### Community 199 - "Community 199"
Cohesion: 0.28
Nodes (4): _collect_cves_scores(), _enum(), _finding_scores(), _uuid()

### Community 200 - "Community 200"
Cohesion: 0.28
Nodes (5): _authenticate(), create_personal_access_token(), login(), Validates credentials and returns the User on success.     Raises a typed Authen, refresh()

### Community 201 - "Community 201"
Cohesion: 0.31
Nodes (8): create_findings_from_probe_result(), _find_open_duplicate(), _map_severity(), Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Convert a probe's self-assessed `findings` list into persisted Finding rows., _resolve_asset()

### Community 202 - "Community 202"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 203 - "Community 203"
Cohesion: 0.22
Nodes (9): expand_targets(), A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Wire argparse args into a scanner instance and execute it., Wire argparse args into a scanner instance and execute it., Wire argparse args into a scanner instance and execute it., Wire argparse args into a scanner instance and execute it. (+1 more)

### Community 204 - "Community 204"
Cohesion: 0.22
Nodes (1): TestUseCasesResolve

### Community 205 - "Community 205"
Cohesion: 0.39
Nodes (7): _rank(), test_bounds(), test_confirmed_exploitable_outranks_contradicted(), test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lowers(), test_kev_raises_rank(), test_low_confidence_lowers_rank()

### Community 206 - "Community 206"
Cohesion: 0.22
Nodes (1): TestTargetsInExcludes

### Community 207 - "Community 207"
Cohesion: 0.22
Nodes (6): _fake_run_scan(), Tests for agent/task_runner.py, Return a minimal successful result without doing any real I/O., TaskRunner with no-op dependencies (no real scanning)., runner(), TestRunnerScanTypes

### Community 208 - "Community 208"
Cohesion: 0.22
Nodes (1): TestIdentity

### Community 209 - "Community 209"
Cohesion: 0.31
Nodes (8): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 210 - "Community 210"
Cohesion: 0.36
Nodes (6): create_access_token(), create_device_access_token(), create_refresh_token(), _now(), Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation.

### Community 211 - "Community 211"
Cohesion: 0.39
Nodes (7): DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci

### Community 212 - "Community 212"
Cohesion: 0.36
Nodes (7): extractScripts(), NmapHost, NmapScriptResult, NmapService, parseNmapXml(), parser, toArray()

### Community 213 - "Community 213"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, loadWordlist(), nativeDirBust(), NativeDirOpts, probe(), ProbeResp

### Community 214 - "Community 214"
Cohesion: 0.29
Nodes (8): MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, Run masscan over the given target specs and return its parsed JSON records., Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, _run_masscan()

### Community 215 - "Community 215"
Cohesion: 0.25
Nodes (6): _is_readable(), PassiveCollector, Listen-only discovery. No active probing. Reports in-scope hosts that     announ, Await readability on any listener without blocking the event loop., Listen-only discovery. No active probing. Reports in-scope hosts that     announ, Await readability on any listener without blocking the event loop.

### Community 216 - "Community 216"
Cohesion: 0.25
Nodes (4): One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, _UDPProbeProtocol

### Community 217 - "Community 217"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 218 - "Community 218"
Cohesion: 0.43
Nodes (1): WindowsCollector

### Community 219 - "Community 219"
Cohesion: 0.46
Nodes (7): _ev(), test_confirmed_authoritative_does_not_escalate(), test_high_severity_suspected_escalates_when_roe_allows(), test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_escalate(), test_ot_profile_never_escalates(), test_roe_forbids_blocks_escalation()

### Community 220 - "Community 220"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 221 - "Community 221"
Cohesion: 0.32
Nodes (3): _boundary_test_client(), test_agent_jwt_is_blocked_before_human_route_handler(), test_human_jwt_still_reaches_human_route_handler()

### Community 222 - "Community 222"
Cohesion: 0.43
Nodes (1): TestMetasploitRPCClient

### Community 223 - "Community 223"
Cohesion: 0.25
Nodes (1): TestRequiresApproval

### Community 224 - "Community 224"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 225 - "Community 225"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 227 - "Community 227"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 228 - "Community 228"
Cohesion: 0.29
Nodes (7): _load_or_create_identity(), Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu

### Community 229 - "Community 229"
Cohesion: 0.38
Nodes (5): AssistantFab(), AssistantCtx, AssistantProvider(), Ctx, useAssistant()

### Community 230 - "Community 230"
Cohesion: 0.48
Nodes (5): build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()

### Community 231 - "Community 231"
Cohesion: 0.67
Nodes (7): agents/greeting-introduction, main, 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit

### Community 232 - "Community 232"
Cohesion: 0.38
Nodes (6): base_score(), parse_vector(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network, CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r, Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin, _roundup()

### Community 233 - "Community 233"
Cohesion: 0.29
Nodes (4): GET, STATUS_TO_API, VALID_SEVERITIES, VALID_SORTS

### Community 234 - "Community 234"
Cohesion: 0.29
Nodes (3): RateLimiter, Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second.

### Community 235 - "Community 235"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 236 - "Community 236"
Cohesion: 0.29
Nodes (1): TestNeo4jClient

### Community 237 - "Community 237"
Cohesion: 0.29
Nodes (1): TestDeceptionScore

### Community 238 - "Community 238"
Cohesion: 0.29
Nodes (1): TestIngestFile

### Community 239 - "Community 239"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 240 - "Community 240"
Cohesion: 0.29
Nodes (1): TestValidateModule

### Community 241 - "Community 241"
Cohesion: 0.29
Nodes (1): TestValidateScope

### Community 242 - "Community 242"
Cohesion: 0.38
Nodes (3): _dry_run(), test_installer_accepts_enroll_token_and_insecure_for_http_manager(), test_installer_without_token_still_shows_manual_approval()

### Community 243 - "Community 243"
Cohesion: 0.29
Nodes (1): TestMergeExclusions

### Community 244 - "Community 244"
Cohesion: 0.29
Nodes (5): Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., TestRunnerSubmission

### Community 245 - "Community 245"
Cohesion: 0.29
Nodes (5): Remove an agent's WebSocket registration., Remove the current registration, optionally only for one socket.          Return, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job

### Community 246 - "Community 246"
Cohesion: 0.33
Nodes (6): _clamp(), Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Translate operator-supplied job params into run_engagement() kwargs.      This i, Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Translate operator-supplied job params into run_engagement() kwargs.      This i, _tuning_from_params()

### Community 247 - "Community 247"
Cohesion: 0.33
Nodes (5): _atomic_write_private_state(), Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., _sync_directory()

### Community 248 - "Community 248"
Cohesion: 0.33
Nodes (4): _deterministic_layout(), GraphVisualizer, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag

### Community 249 - "Community 249"
Cohesion: 0.53
Nodes (4): list_use_cases(), main(), _print_summary(), _split()

### Community 250 - "Community 250"
Cohesion: 0.47
Nodes (2): One probe-ladder rung on its own connection. Returns banner bytes, b""         (, ServiceBannerScanner

### Community 251 - "Community 251"
Cohesion: 0.33
Nodes (6): _ber_parse(), _decode_oid(), _parse_varbinds(), Shallow parse of BER TLVs starting at offset. Returns [(tag, value), ...]., Extract (oid_dotted, value_tag, value_bytes) from a GET/GETNEXT/GETBULK response, BER-encoded OID bytes → dotted-notation string.

### Community 252 - "Community 252"
Cohesion: 0.33
Nodes (3): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect()

### Community 253 - "Community 253"
Cohesion: 0.40
Nodes (5): AttemptClaim, claim_job_attempt(), Atomically claim a pending job and create its fenced attempt ledger row., Renew only the currently installed running attempt/fence., renew_job_attempt()

### Community 254 - "Community 254"
Cohesion: 0.53
Nodes (4): compute(), SlaResult, summarize(), _windows()

### Community 255 - "Community 255"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 256 - "Community 256"
Cohesion: 0.33
Nodes (1): TestCvss

### Community 257 - "Community 257"
Cohesion: 0.33
Nodes (1): TestIngestValidation

### Community 258 - "Community 258"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 259 - "Community 259"
Cohesion: 0.60
Nodes (5): Unit tests for the dashboard list endpoints (jobs + assets)., _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user()

### Community 260 - "Community 260"
Cohesion: 0.33
Nodes (1): TestClamp

### Community 261 - "Community 261"
Cohesion: 0.33
Nodes (1): TestEngagementModes

### Community 262 - "Community 262"
Cohesion: 0.73
Nodes (5): _db_returning(), _finding(), test_covered_clean_medium_finding_is_auto_resolved(), test_db_version_change_blocks_resolution(), test_uncovered_finding_is_left_open()

### Community 263 - "Community 263"
Cohesion: 0.33
Nodes (1): TestFetchEngagementScope

### Community 265 - "Community 265"
Cohesion: 0.33
Nodes (3): diff_assets(), report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d, re-scan mode's delta report: what changed between two engagements.

### Community 266 - "Community 266"
Cohesion: 0.40
Nodes (5): _load_env(), Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience.

### Community 267 - "Community 267"
Cohesion: 0.40
Nodes (4): True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls.

### Community 268 - "Community 268"
Cohesion: 0.40
Nodes (4): Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce

### Community 269 - "Community 269"
Cohesion: 0.40
Nodes (4): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of

### Community 270 - "Community 270"
Cohesion: 0.40
Nodes (4): Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons

### Community 271 - "Community 271"
Cohesion: 0.40
Nodes (4): Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used

### Community 272 - "Community 272"
Cohesion: 0.40
Nodes (4): Return the WebSocket connection URL with auth token.          The token is passe, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica

### Community 273 - "Community 273"
Cohesion: 0.40
Nodes (4): Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns

### Community 274 - "Community 274"
Cohesion: 0.40
Nodes (3): _as_uuid(), AttackLogger, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 275 - "Community 275"
Cohesion: 0.40
Nodes (5): parse_ports(), Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535).

### Community 276 - "Community 276"
Cohesion: 0.40
Nodes (1): TestTenantWebSocketSelection

### Community 277 - "Community 277"
Cohesion: 0.40
Nodes (1): TestGetAgentJobs

### Community 278 - "Community 278"
Cohesion: 0.40
Nodes (1): TestGraphVisualizer

### Community 279 - "Community 279"
Cohesion: 0.40
Nodes (1): TestCheckHwBind

### Community 280 - "Community 280"
Cohesion: 0.40
Nodes (1): TestEngineSummary

### Community 281 - "Community 281"
Cohesion: 0.40
Nodes (1): TestLooksLikeHttp

### Community 282 - "Community 282"
Cohesion: 0.40
Nodes (1): TestLooksLikeTls

### Community 283 - "Community 283"
Cohesion: 0.40
Nodes (1): TestResolveScanType

### Community 284 - "Community 284"
Cohesion: 0.40
Nodes (1): TestTargets

### Community 285 - "Community 285"
Cohesion: 0.60
Nodes (3): _smb2_negotiate_response(), test_signing_not_required(), test_signing_required_smb311()

### Community 286 - "Community 286"
Cohesion: 0.83
Nodes (3): die(), load_facts(), main()

### Community 287 - "Community 287"
Cohesion: 0.67
Nodes (1): _ConnectSweep

### Community 288 - "Community 288"
Cohesion: 0.67
Nodes (1): TLSScanner

### Community 289 - "Community 289"
Cohesion: 0.67
Nodes (1): WebScanner

### Community 290 - "Community 290"
Cohesion: 0.50
Nodes (1): TestGate0

### Community 291 - "Community 291"
Cohesion: 0.50
Nodes (1): TestRateLimiter

### Community 292 - "Community 292"
Cohesion: 0.50
Nodes (1): TestScanResult

### Community 294 - "Community 294"
Cohesion: 0.50
Nodes (2): _ConcurrencyScanner, test_host_fanout_is_bounded()

### Community 295 - "Community 295"
Cohesion: 0.50
Nodes (1): Add is_active to users and tenants; add password_expires_at to users.  All exist

### Community 296 - "Community 296"
Cohesion: 0.50
Nodes (3): Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag

### Community 297 - "Community 297"
Cohesion: 0.50
Nodes (3): Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs.

### Community 298 - "Community 298"
Cohesion: 0.50
Nodes (3): Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.

### Community 299 - "Community 299"
Cohesion: 0.50
Nodes (3): Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy).

### Community 300 - "Community 300"
Cohesion: 0.50
Nodes (3): Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job).

### Community 301 - "Community 301"
Cohesion: 0.50
Nodes (3): Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, _utcnow()

### Community 302 - "Community 302"
Cohesion: 0.67
Nodes (3): Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, resolve()

### Community 303 - "Community 303"
Cohesion: 0.67
Nodes (2): _priority(), Assets that appear in more than ``threshold`` (default 50%) of all paths —

### Community 304 - "Community 304"
Cohesion: 0.67
Nodes (3): approve_exploit(), _get_approval_or_404(), reject_exploit()

### Community 305 - "Community 305"
Cohesion: 0.67
Nodes (2): Record a heartbeat from an agent., Record a heartbeat from an agent.

### Community 306 - "Community 306"
Cohesion: 0.67
Nodes (2): Dispatch a real ScanResult into the right sub-structure, keyed         on result, Dispatch a real ScanResult into the right sub-structure, keyed         on result

### Community 307 - "Community 307"
Cohesion: 1.00
Nodes (1): Fast port discovery with naabu. Feeds port list to Nmap.

### Community 308 - "Community 308"
Cohesion: 1.00
Nodes (1): Nmap service enumeration. Accepts port list from Naabu.

### Community 309 - "Community 309"
Cohesion: 1.00
Nodes (1): Nuclei vulnerability scan — production-ready.

### Community 310 - "Community 310"
Cohesion: 1.00
Nodes (1): Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.

### Community 311 - "Community 311"
Cohesion: 1.00
Nodes (1): NetExec SMB validation: signing, null sessions, SMBv1.

### Community 312 - "Community 312"
Cohesion: 1.00
Nodes (1): testssl.sh TLS/SSL analysis.

### Community 313 - "Community 313"
Cohesion: 1.00
Nodes (1): Extract HTTP/HTTPS URLs from nmap XML output.

### Community 314 - "Community 314"
Cohesion: 1.00
Nodes (1): EyeWitness screenshot evidence collection.

### Community 315 - "Community 315"
Cohesion: 1.00
Nodes (1): Safe lateral movement checks — no actual exploitation.

### Community 316 - "Community 316"
Cohesion: 1.00
Nodes (1): Cloud infrastructure scan (AWS/Azure/GCP).

### Community 317 - "Community 317"
Cohesion: 1.00
Nodes (1): Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.

### Community 318 - "Community 318"
Cohesion: 1.00
Nodes (1): Read a KV-v2 secret from Vault.

### Community 319 - "Community 319"
Cohesion: 1.00
Nodes (1): Verify the Python probe can open what the TypeScript manager sealed (T14 interop

### Community 320 - "Community 320"
Cohesion: 1.00
Nodes (1): Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO

### Community 321 - "Community 321"
Cohesion: 1.00
Nodes (1): Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).

### Community 322 - "Community 322"
Cohesion: 1.00
Nodes (1): End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.

### Community 323 - "Community 323"
Cohesion: 1.00
Nodes (1): Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 324 - "Community 324"
Cohesion: 1.00
Nodes (1): ThreadingHTTPServer

## Knowledge Gaps
- **1312 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+1307 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 68`** (2 nodes): `_ExplodingScanner`, `test_per_target_exception_preserves_other_results()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `TestResultSpool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 134`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 149`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 158`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 165`** (1 nodes): `TestAgentJobCompatibility`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 166`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (2 nodes): `Tests that use the real engine but with no-op callbacks.`, `TestRunnerHeadless`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 171`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 173`** (1 nodes): `TestHallucinationGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 174`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 175`** (1 nodes): `TestNucleiExploitRunner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 176`** (1 nodes): `TestValidatePayload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 177`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 178`** (2 nodes): `test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()`, `_token()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 179`** (1 nodes): `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 183`** (1 nodes): `ExploitOrchestrator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 189`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 191`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 192`** (2 nodes): `Each encryption uses a fresh ephemeral key, so blobs are different.`, `TestEncryptDecryptRoundtrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 193`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 204`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (1 nodes): `WindowsCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (1 nodes): `TestMetasploitRPCClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (1 nodes): `TestRequiresApproval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (1 nodes): `TestNeo4jClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (1 nodes): `TestDeceptionScore`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (1 nodes): `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 240`** (1 nodes): `TestValidateModule`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (1 nodes): `TestValidateScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (1 nodes): `TestMergeExclusions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (2 nodes): `One probe-ladder rung on its own connection. Returns banner bytes, b""         (`, `ServiceBannerScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (1 nodes): `TestCvss`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (1 nodes): `TestIngestValidation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (1 nodes): `TestClamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (1 nodes): `TestEngagementModes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (1 nodes): `TestFetchEngagementScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (1 nodes): `TestTenantWebSocketSelection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (1 nodes): `TestGetAgentJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 278`** (1 nodes): `TestGraphVisualizer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (1 nodes): `TestCheckHwBind`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (1 nodes): `TestEngineSummary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (1 nodes): `TestLooksLikeHttp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (1 nodes): `TestLooksLikeTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (1 nodes): `TestResolveScanType`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (1 nodes): `TestTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 287`** (1 nodes): `_ConnectSweep`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 288`** (1 nodes): `TLSScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 289`** (1 nodes): `WebScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 290`** (1 nodes): `TestGate0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 291`** (1 nodes): `TestRateLimiter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 292`** (1 nodes): `TestScanResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 294`** (2 nodes): `_ConcurrencyScanner`, `test_host_fanout_is_bounded()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 295`** (1 nodes): `Add is_active to users and tenants; add password_expires_at to users.  All exist`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 303`** (2 nodes): `_priority()`, `Assets that appear in more than ``threshold`` (default 50%) of all paths —`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 305`** (2 nodes): `Record a heartbeat from an agent.`, `Record a heartbeat from an agent.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 306`** (2 nodes): `Dispatch a real ScanResult into the right sub-structure, keyed         on result`, `Dispatch a real ScanResult into the right sub-structure, keyed         on result`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 307`** (1 nodes): `Fast port discovery with naabu. Feeds port list to Nmap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 308`** (1 nodes): `Nmap service enumeration. Accepts port list from Naabu.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 309`** (1 nodes): `Nuclei vulnerability scan — production-ready.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 310`** (1 nodes): `Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 311`** (1 nodes): `NetExec SMB validation: signing, null sessions, SMBv1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 312`** (1 nodes): `testssl.sh TLS/SSL analysis.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 313`** (1 nodes): `Extract HTTP/HTTPS URLs from nmap XML output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 314`** (1 nodes): `EyeWitness screenshot evidence collection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 315`** (1 nodes): `Safe lateral movement checks — no actual exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 316`** (1 nodes): `Cloud infrastructure scan (AWS/Azure/GCP).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 317`** (1 nodes): `Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 318`** (1 nodes): `Read a KV-v2 secret from Vault.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 319`** (1 nodes): `Verify the Python probe can open what the TypeScript manager sealed (T14 interop`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (1 nodes): `Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 321`** (1 nodes): `Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 322`** (1 nodes): `End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 323`** (1 nodes): `Deterministic stand-ins emitting realistic output for 127.0.0.1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 324`** (1 nodes): `ThreadingHTTPServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 63` to `Community 5`, `Community 66`, `Community 94`, `Community 0`, `Community 50`, `Community 78`, `Community 124`, `Community 3`, `Community 201`, `Community 4`, `Community 33`, `Community 163`, `Community 171`, `Community 235`, `Community 220`, `Community 52`, `Community 155`, `Community 222`, `Community 175`, `Community 223`, `Community 240`, `Community 176`, `Community 241`, `Community 156`, `Community 1`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `Transport` connect `Community 181` to `Community 19`, `Community 127`, `Community 152`, `Community 247`, `Community 273`, `Community 197`, `Community 268`, `Community 271`, `Community 267`, `Community 269`, `Community 270`, `Community 272`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `Finding` connect `Community 3` to `Community 1`, `Community 24`, `Community 201`, `Community 183`, `Community 17`, `Community 28`, `Community 141`, `Community 87`, `Community 63`, `Community 33`, `Community 101`, `Community 4`, `Community 254`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 173 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 173 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R` to the rest of the system?**
  _1312 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.023498062015503876 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.02440884820747521 - nodes in this community are weakly interconnected._