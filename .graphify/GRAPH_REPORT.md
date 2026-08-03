# Graph Report - .  (2026-08-03)

## Corpus Check
- Large corpus: 603 files · ~479,572 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 5230 nodes · 11527 edges · 334 communities detected
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 2776 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 2776 · contains: 2405 · calls: 1652 · method: 1299 · MODIFIES: 1165 · rationale_for: 1038 · imports: 450 · imports_from: 416 · inherits: 183 · ON_BRANCH: 103 · PARENT_OF: 40


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 603 · Candidates: 1346
- Excluded: 78 untracked · 63544 ignored · 3 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `ca41cbf`
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
Nodes (43): BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL, HallucinationGuard — post-generation validation of LLM report text against the g, 298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, d1b4dd3 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru (+35 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (63): agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit, result_spool.py — local result persistence with upload retry.  When the probe co, bytes_to_pubkey_b64(), generate_identity(), pubkey_to_bytes(), scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.  T, Decode a base64-encoded X25519 public key to raw bytes., Encode raw X25519 public key bytes to a base64 string. (+55 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (108): agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Convert a probe's self-assessed `findings` list into persisted Finding rows., GraphBuilder — turns engagement assets/services/findings into an attack graph., Build the full multi-type attack graph. Returns the populated DiGraph         (a, For each exploitable finding add an EXPLOITS edge Finding→Asset with         ``w (+100 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (63): ServiceFingerprint, FindingStatus, FindingImport, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), NessusScanRequest, _nuclei_finding(), _nuclei_terminal_result() (+55 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (62): buildScanCommand(), PROFILE_TOOLS, ModuleCategory, ModuleInput, ModuleOutput, modulesForPorts(), ScanModule, bySeverityCount() (+54 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (42): HallucinationGuard, Run all relevant checks and return a combined verdict:         ``{valid, issues,, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide., _collect_cves_scores(), _enum(), _finding_scores() (+34 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (49): ApiActivity, GET, ManagerAiResponse, 0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner UI, 1fe16c8 stable but some dead code, need to optimize, c76b428 backend and login page error handling update, GET, POST (+41 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (29): aggregate(), ConsistencyReport, FindingConsistency, run_findings: one list of Findings per run (N runs). Aggregated by     the deter, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen, wilson_ci(), _compute_priority(), EpssDB (+21 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (35): apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl(), Session, SESSION_DIR (+27 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (55): A, ask(), askSecret(), banner(), buildInteractiveCommand(), choose(), chooseNextPhase(), confirm() (+47 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (41): ComplianceRef, COVERAGE_COLOR, DetectionCoverage, ExploitMaturity, Finding, FindingDetail(), FindingPage, FindingsPage() (+33 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (53): DeclarativeBase, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., Append-only ledger of every attack action performed during an engagement.      W, Immutable, append-only audit trail for all exploit actions.     No TimestampMixi, Base, TimestampMixin, Per-engagement SIEM + EDR connection settings used by the detection     validati, detection_run.py — one execution of the deterministic detection engine over a fa (+45 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (44): BaseModel, create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, New raw-facts path: detect CVE findings from result['facts'] and persist     the, Background entry point (P1: keep detection OFF the probe-result request     path, (content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev (+36 more)

### Community 13 - "Community 13"
Cohesion: 0.16
Nodes (50): Exception, ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is, Raises SafetyViolationError if module or payload is not permitted., Raises SafetyViolationError if module or payload is not permitted., Raises OutOfScopeError if target_ip not in engagement scope., Raises OutOfScopeError if target_ip not in engagement scope., Full exploit execution pipeline with safety, scope, blast radius,         audit, Full exploit execution pipeline with safety, scope, blast radius,         audit (+42 more)

### Community 14 - "Community 14"
Cohesion: 0.08
Nodes (46): bin(), binName(), collectProcess(), hasBinary(), hasSystemBinary(), httpBannerGrab(), HttpxLine, isWindows() (+38 more)

### Community 15 - "Community 15"
Cohesion: 0.08
Nodes (43): all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), normalize(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web() (+35 more)

### Community 16 - "Community 16"
Cohesion: 0.07
Nodes (8): _finding(), TestAggregate, TestClassifyTier, TestComputePriority, TestDedupFindings, TestFindingConsistency, TestSuppressNegated, TestVerify

### Community 17 - "Community 17"
Cohesion: 0.06
Nodes (38): _applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _env_number(), _error_result(), _facts_from_cache(), _hosts_from_facts() (+30 more)

### Community 18 - "Community 18"
Cohesion: 0.07
Nodes (32): Agent, AGENT_STATUS, AgentStatus, PATH_STATUS, SEV_LABEL, Exposure, ProtocolRiskCard(), useExposure() (+24 more)

### Community 19 - "Community 19"
Cohesion: 0.08
Nodes (25): AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient, propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Test double — a fixed lookup table, no network. Used to validate the     surroun (+17 more)

### Community 20 - "Community 20"
Cohesion: 0.07
Nodes (16): _make_db(), _make_tenant(), _make_user(), Tests for authentication login flow.  Covers:   - login success   - user_not_fou, Ensure every exception class has the expected reason_code attribute.     These c, AsyncSession mock that returns user on first execute, tenant on second., TestAuthenticateBcryptFailure, TestAuthenticateDatabaseFailure (+8 more)

### Community 21 - "Community 21"
Cohesion: 0.14
Nodes (33): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+25 more)

### Community 22 - "Community 22"
Cohesion: 0.06
Nodes (32): DEMO_ASSET, DEMO_ENGAGEMENT, DEMO_FINDING, AssetInput, chat(), CRITICALITY_SCORE, DESTRUCTIVE_PATTERNS, EPSS_MOCK (+24 more)

### Community 23 - "Community 23"
Cohesion: 0.07
Nodes (28): Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result., Remove the spool file for a successfully uploaded result., Attempt to upload a result with retries and local spool as fallback.          Ar, Move a terminally rejected result out of the retry queue., Re-attempt upload of all previously spooled results.          Called once at pro, Attempt to upload a result with retries and local spool as fallback.          Ar, Number of pending (unsubmitted) results in the spool. (+20 more)

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (34): use_cases.py — the finite, pre-defined library of scan scenarios the manager can, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, resolve(), backup-before-secret-removal, feat/probe-usecase-alignment, main, spike/probe-go (+26 more)

### Community 25 - "Community 25"
Cohesion: 0.12
Nodes (24): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline (+16 more)

### Community 26 - "Community 26"
Cohesion: 0.09
Nodes (23): AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator, DatabaseConnectivityValidator, DatabaseURLValidator, DetectionEngineValidator (+15 more)

### Community 27 - "Community 27"
Cohesion: 0.07
Nodes (26): ConnectionManager, GraphWebSocketManager, High-level manager for graph-specific WebSocket operations., Handle a new WebSocket client connection., Handle incoming WebSocket messages., Manages WebSocket connections with room-based broadcasting., Broadcast graph data update to all subscribers., Broadcast a single node update. (+18 more)

### Community 28 - "Community 28"
Cohesion: 0.07
Nodes (19): BaseScanner, expand_targets(), main_entrypoint(), RateLimiter, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Simple async rate limiter: at most `rate` operations per second., Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10 (+11 more)

### Community 29 - "Community 29"
Cohesion: 0.12
Nodes (10): _candidate(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db(), TestCPECandidateCpe23, TestEnrichFinding, TestEpssDb, TestKevDb (+2 more)

### Community 30 - "Community 30"
Cohesion: 0.11
Nodes (15): RateLimiter, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim, ServiceIdentifier, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner, Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr (+7 more)

### Community 31 - "Community 31"
Cohesion: 0.09
Nodes (31): config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES, Client, ClientJiraConfig, ClientNotifyConfig (+23 more)

### Community 32 - "Community 32"
Cohesion: 0.12
Nodes (22): ADConnectionError, DependencyMissingError, Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., ADComputer, ADGroup, ADUser, _as_list() (+14 more)

### Community 33 - "Community 33"
Cohesion: 0.12
Nodes (30): buildToolsCommand(), C, ln(), showSpinner(), downloadFile(), extract(), getInstalledRecord(), installAll() (+22 more)

### Community 34 - "Community 34"
Cohesion: 0.06
Nodes (19): NAV_SECTIONS, NavItem, Sidebar(), SidebarProps, ActivityItem, ComplianceControl, ComplianceFramework, ComplianceFrameworkData (+11 more)

### Community 35 - "Community 35"
Cohesion: 0.10
Nodes (26): AuthContext, Handler, generateOtp(), OtpEntry, otpStore, OtpVerifyResult, SessionPayload, verifyOtp() (+18 more)

### Community 36 - "Community 36"
Cohesion: 0.11
Nodes (28): activate_enrollment(), approve_enrollment(), _authenticated_request(), create_enroll_token(), create_enrollment_request(), _decode_public_key(), _derive_refresh_secret(), enroll_token_is_usable() (+20 more)

### Community 37 - "Community 37"
Cohesion: 0.10
Nodes (28): Agent, AgentStatus, _agent_can_execute_job(), _agent_ownership_check(), AgentBootstrapRequest, AgentRegisterRequest, AgentRegisterResponse, bootstrap_agent() (+20 more)

### Community 38 - "Community 38"
Cohesion: 0.09
Nodes (16): AssetCriticality, UserRole, OrderedDict, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path, str, Parse CSV text into a list of AssetIn models and error strings., Add NVD CVSS, EPSS, KEV flag, MITRE techniques, and composite risk.         Muta, Returns {cvss_v3, cvss_vector, description, references, published_date}. (+8 more)

### Community 39 - "Community 39"
Cohesion: 0.08
Nodes (20): Agent, AIBrainPage(), AiStatus, criticalChain, defaultAgents, Engagement, Finding, findings (+12 more)

### Community 40 - "Community 40"
Cohesion: 0.09
Nodes (29): AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError, ExpiredPasswordError, JWTFailureError (+21 more)

### Community 41 - "Community 41"
Cohesion: 0.08
Nodes (22): Engagement, Finding, FindingSummary, LiveOverview(), Sev, pct(), Sev, SEV_STYLE (+14 more)

### Community 42 - "Community 42"
Cohesion: 0.08
Nodes (20): FindingSeverity, NucleiMatch, boundedEnvMs(), OpenVASFinding, OpenVASHelperOutput, OpenVASTaskState, parseOpenVASHelperOutput(), runOpenVASScanBackground() (+12 more)

### Community 43 - "Community 43"
Cohesion: 0.08
Nodes (15): ATTACK_TIMELINE, AttackAction, correlationRuns, CoverageStats, DetectionOutcome, DetectionResult, detectionStore, EDR_DETECTIONS (+7 more)

### Community 44 - "Community 44"
Cohesion: 0.07
Nodes (4): _ConcurrencyScanner, _ExplodingScanner, test_host_fanout_is_bounded(), test_per_target_exception_preserves_other_results()

### Community 45 - "Community 45"
Cohesion: 0.10
Nodes (19): _metric(), _not_scored(), Pure helpers for controlled Probe capability and accuracy validation., Validate the small, explicit inventory used for accuracy scoring., Score promoted inventory against explicit host/port/service/CVE truth., Resolve suites plus explicit use-cases, preserving first-seen order., Require every IP/CIDR target to be fully allowed and not excluded., Return the conservative number of addresses represented by targets. (+11 more)

### Community 46 - "Community 46"
Cohesion: 0.15
Nodes (12): get_settings(), Settings, BaseSettings, AiGenerateRequest, AiGenerateResponse, AiMessage, AiProviderStatus, AiStatusResponse (+4 more)

### Community 47 - "Community 47"
Cohesion: 0.07
Nodes (13): bracket_host(), parse_ports(), scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h, Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., resolve(), Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG (+5 more)

### Community 48 - "Community 48"
Cohesion: 0.11
Nodes (9): EvidenceTier, IntEnum, _fact(), TestAsset, TestCorrelateSmbPatch, TestFactRef, TestNormalize, TestNormalizeBanner (+1 more)

### Community 49 - "Community 49"
Cohesion: 0.11
Nodes (24): _finalize_trace(), _gather_per_host(), _port_candidates(), workflow_engine.py — the async DAG executor. Loops through gates, checks precond, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Return TCP ports worth scanning for this profile and requested branch set., In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass (+16 more)

### Community 50 - "Community 50"
Cohesion: 0.13
Nodes (13): AttackAction, CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender, _parse_dt(), EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender, Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi (+5 more)

### Community 51 - "Community 51"
Cohesion: 0.09
Nodes (16): ToastContext, useToast(), ActivityItem, AssetRow, displayDate(), EDIT_STATUSES, Engagement, EngagementDetailPage() (+8 more)

### Community 52 - "Community 52"
Cohesion: 0.11
Nodes (21): GET, STATUS_TO_API, VALID_SEVERITIES, VALID_SORTS, DETECTION_TO_UI, ENG_STATUS_TO_API, ENG_STATUS_TO_UI, engStatusToApi() (+13 more)

### Community 53 - "Community 53"
Cohesion: 0.10
Nodes (22): Agent, AgentCapability, AGENTS, agentsStore, AgentStatus, ensureDataDir(), FIELD_AGENTS_FILE, FieldAgent (+14 more)

### Community 54 - "Community 54"
Cohesion: 0.10
Nodes (20): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+12 more)

### Community 55 - "Community 55"
Cohesion: 0.15
Nodes (23): AgentUnavailableError, Raised when the Anthropic SDK or API key is not configured., Base, AgentRecommendation, AttackTimeline, DetectionConfig, DetectionResult, AgentCredential (+15 more)

### Community 56 - "Community 56"
Cohesion: 0.13
Nodes (11): ElasticSIEM, _parse_dt(), SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi, Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_, Abstract SIEM connector., Splunk via the REST search endpoint (``/services/search/jobs/export``) with an, SentinelSIEM (+3 more)

### Community 57 - "Community 57"
Cohesion: 0.08
Nodes (15): apiFetch(), Cat, CATS, Engagement, EngineManifest, getToken(), Intensity, JobStatus (+7 more)

### Community 58 - "Community 58"
Cohesion: 0.11
Nodes (11): Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., TestEnqueueAgentJob, TestListAgents (+3 more)

### Community 59 - "Community 59"
Cohesion: 0.11
Nodes (24): assessment(), discovery(), EngagementMode, host_discovery(), includes_stage(), port_scan(), modes.py — engagement mode configurations. Each mode is a thin config that tunes, Discovery + ports + banner only — no deep dives, no credentials. (+16 more)

### Community 60 - "Community 60"
Cohesion: 0.09
Nodes (24): _flush_spool_over_http(), Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Persistent WebSocket push loop.      Returns False if WebSocket is unavailable ( (+16 more)

### Community 61 - "Community 61"
Cohesion: 0.12
Nodes (15): EMPTY_FORM, Engagement, EngagementsPage(), EngagementsResponse, EngagementStatus, FormState, hasValidDateRange(), splitEntries() (+7 more)

### Community 62 - "Community 62"
Cohesion: 0.09
Nodes (18): ADJ, ATTACK_PATHS, AttackPath, BlastRadiusResult, buildAttackPaths(), Chokepoint, CHOKEPOINTS, edgesForPath() (+10 more)

### Community 63 - "Community 63"
Cohesion: 0.08
Nodes (1): TestResultSpool

### Community 64 - "Community 64"
Cohesion: 0.10
Nodes (8): Asset, _parse_ts(), PortFact, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Dispatch a real ScanResult into the right sub-structure, keyed         on result, Dispatch a real ScanResult into the right sub-structure, keyed         on result, _utcnow()

### Community 65 - "Community 65"
Cohesion: 0.17
Nodes (14): AiMessage, ManagerAiResponse, POST(), validMessages(), cveRecordToFactCard(), detectFindingId(), isExploited(), plainWhyItMatters() (+6 more)

### Community 66 - "Community 66"
Cohesion: 0.11
Nodes (6): interpret_dns_recursion(), interpret_memcached_stats(), interpret_ntp_monlist(), _ntp_monlist_probe(), udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, UDPScanner

### Community 67 - "Community 67"
Cohesion: 0.09
Nodes (10): AiStatus, ConfigField, DEFAULT_RULES, DeploymentStatus, EMAIL_FIELDS, EnvSetting, INTEGRATIONS, JIRA_FIELDS (+2 more)

### Community 68 - "Community 68"
Cohesion: 0.11
Nodes (15): _Socket, test_collector_raises_when_no_listener_binds(), test_ot_udp_backend_never_joins_or_transmits(), test_subset_listener_failure_reports_degraded_coverage(), _Writer, classify_scanner_error(), engine_manifest(), ErrorDetail (+7 more)

### Community 69 - "Community 69"
Cohesion: 0.16
Nodes (21): A, banner(), findingDetail(), findingLine(), findingsTable(), hostLine(), info(), LINE (+13 more)

### Community 70 - "Community 70"
Cohesion: 0.16
Nodes (13): ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM, Read pKICertificateTemplate objects from the Configuration NC. (+5 more)

### Community 71 - "Community 71"
Cohesion: 0.15
Nodes (11): MetasploitRPCClient, MetasploitRPCError, Returns {status, output, uuid}., Returns True if job was successfully killed., Poll until job completes or max_wait exceeded., Authenticated RPC call — prepends token., Async Metasploit RPC client using msgpack-over-HTTPS., Authenticate with msfrpcd and store the session token. (+3 more)

### Community 72 - "Community 72"
Cohesion: 0.11
Nodes (6): _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_background_job_failed(), test_partial_nuclei_run_preserves_findings_and_diagnostics()

### Community 73 - "Community 73"
Cohesion: 0.16
Nodes (4): _asset(), TestAssetNeedsRecheckLive, TestGate5, TestGate6

### Community 74 - "Community 74"
Cohesion: 0.13
Nodes (11): _make_http_mock(), Unit tests for VulnEnrichmentService — all external HTTP calls mocked., Create a mock httpx.AsyncClient that returns different responses per URL., test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full(), test_fetch_epss_success() (+3 more)

### Community 75 - "Community 75"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 76 - "Community 76"
Cohesion: 0.14
Nodes (4): _scan_result(), TestCacheEntry, TestClassifyCertainty, TestWorkflowCache

### Community 77 - "Community 77"
Cohesion: 0.11
Nodes (17): JobResult, Structured result from running one scan job., Submit the result, with spool-and-retry if available., Structured result from running one scan job., Submit the result, with spool-and-retry if available., Submit the result, with spool-and-retry if available., Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Orchestrates one scan job's lifecycle.      The runner holds injected dependenci (+9 more)

### Community 78 - "Community 78"
Cohesion: 0.13
Nodes (13): metadata, AssistantDrawer(), AssistantFab(), AssistantCtx, AssistantProvider(), Ctx, useAssistant(), QueryProvider() (+5 more)

### Community 79 - "Community 79"
Cohesion: 0.20
Nodes (16): _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database(), _check_jwt_secret(), _check_redis(), _check_required_env_vars() (+8 more)

### Community 80 - "Community 80"
Cohesion: 0.16
Nodes (18): _char_order(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), has_ambiguous_epoch(), version_compare.py — per-scheme version comparators.  Spec calls this "the highe (+10 more)

### Community 81 - "Community 81"
Cohesion: 0.15
Nodes (10): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+2 more)

### Community 82 - "Community 82"
Cohesion: 0.17
Nodes (16): _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError, license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the (+8 more)

### Community 83 - "Community 83"
Cohesion: 0.12
Nodes (11): ActivityItem, DashboardCharts(), Engagement, Finding, FindingPage, FindingSummary, SEV, STATUS_STYLE (+3 more)

### Community 84 - "Community 84"
Cohesion: 0.15
Nodes (12): correlate_smb_patch(), dedup_findings(), _product_from_cpe(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Suppress a suspected/potential (inferred-source) finding when the     SAME host (+4 more)

### Community 85 - "Community 85"
Cohesion: 0.18
Nodes (16): match_candidate(), matcher.py — does this CPE candidate's version fall inside a vulnerable range, p, dpkg_compare, but None instead of a misleading answer when one side     has an e, Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A, All Findings this single CPE candidate produces against the snapshot.     Empty, _safe_compare(), _version_in_ranges(), FindingState (+8 more)

### Community 86 - "Community 86"
Cohesion: 0.13
Nodes (11): NucleiExploitRunner, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Parse nuclei JSONL output for a single CVE PoC result., Parse nuclei JSONL output for a single CVE PoC result., Run Nuclei CVE PoC templates against a single target.     Every template is safe, Run Nuclei CVE PoC templates against a single target.     Every template is safe, Parse template YAML and validate it contains no write/delete/DoS actions. (+3 more)

### Community 87 - "Community 87"
Cohesion: 0.16
Nodes (9): PathAnalyzer, _priority(), Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for, Assets that appear in more than ``threshold`` (default 50%) of all paths —, Assets reachable (and thus at risk) if ``compromised_asset_id`` is owned., Best (easiest) exploitable finding on an asset: {cvss, weight, finding}., Build (and cache) the Asset→Asset movement projection. Edge weight is the (+1 more)

### Community 88 - "Community 88"
Cohesion: 0.19
Nodes (8): FakeReader, FakeWriter, _probe(), Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol (, _run(), TestMysqlxVsOracle, _tns_packet(), _xproto_frame()

### Community 89 - "Community 89"
Cohesion: 0.21
Nodes (1): TestServiceIdentifier

### Community 90 - "Community 90"
Cohesion: 0.13
Nodes (7): BloodHoundCollector, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., Run bloodhound-python and return the list of produced JSON file paths.         R, TestBuildADFinding

### Community 91 - "Community 91"
Cohesion: 0.12
Nodes (17): _enroll_device(), _load_or_create_identity(), _load_or_create_signing_identity(), _obtain_identity(), Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64). (+9 more)

### Community 92 - "Community 92"
Cohesion: 0.14
Nodes (15): fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), scope_validator.py — defense-in-depth scope re-validation for the probe.  The pr, Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)., Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Parse one IP, CIDR, or inclusive IP range into covering networks.      ``None`` (+7 more)

### Community 93 - "Community 93"
Cohesion: 0.13
Nodes (13): GzipRequestMiddleware, Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., _service_root(), agent_jwt_path_allows(), _is_public_enrollment_request(), Extracts JWT from Authorization header and injects tenant_id + user     claims i, Extracts JWT from Authorization header and injects tenant_id + user     claims i (+5 more)

### Community 94 - "Community 94"
Cohesion: 0.18
Nodes (15): addComment(), Case, CaseActivity, CaseComment, CaseSeverity, CaseStatus, createCase(), DATA_FILE (+7 more)

### Community 95 - "Community 95"
Cohesion: 0.16
Nodes (10): _netbios_session(), parse_smb2_security_mode(), smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, Read signing posture from an SMB2 NEGOTIATE response.      The response carries, _smb1_negotiate(), _smb2_negotiate(), SMBScanner, _smb2_negotiate_response() (+2 more)

### Community 96 - "Community 96"
Cohesion: 0.24
Nodes (15): _detect_drift(), _hash(), _log(), log_error(), log_info(), log_warn(), main(), Warn if the tenant has multiple admins or a stale admin email. (+7 more)

### Community 97 - "Community 97"
Cohesion: 0.19
Nodes (2): _action(), TestDetectionCorrelator

### Community 98 - "Community 98"
Cohesion: 0.20
Nodes (5): AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()

### Community 99 - "Community 99"
Cohesion: 0.14
Nodes (10): PageShell(), PageShellProps, Theme, ThemeContext, ThemeContextValue, ThemeProvider(), useTheme(), EnrollmentRequest (+2 more)

### Community 100 - "Community 100"
Cohesion: 0.28
Nodes (8): asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder, is_internet_exposed(), service_node_id(), _to_float()

### Community 101 - "Community 101"
Cohesion: 0.14
Nodes (6): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only., WebScanner

### Community 102 - "Community 102"
Cohesion: 0.14
Nodes (6): NTLMRelayChecker, Build a Finding for hosts missing SMB signing. The attack_narrative         incl, Probe SMB/LDAP signing posture across a host list., For each IP, returns {signing_enabled, signing_required}.          A host is rel, Returns True if the DC *enforces* LDAP signing / channel binding.          We at, TestNTLMRelayChecker

### Community 103 - "Community 103"
Cohesion: 0.16
Nodes (15): _bounded_env_int(), _is_local_manager_url(), main(), _poll_jobs_or_empty(), Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Return an integer environment setting constrained to a safe range. (+7 more)

### Community 104 - "Community 104"
Cohesion: 0.17
Nodes (7): Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh a device token before expiry; legacy identities are unchanged., Refresh routing metadata using the cached agent identity.          Returns True

### Community 105 - "Community 105"
Cohesion: 0.17
Nodes (6): BaseScanner, DBScanner, _build_get(), _extract_sysdescr(), snmp_scanner.py — detect SNMP and read sysDescr via common community strings.  M, SNMPScanner

### Community 106 - "Community 106"
Cohesion: 0.13
Nodes (12): approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest, ExploitEvidence, ExploitJob, ExploitResult (+4 more)

### Community 107 - "Community 107"
Cohesion: 0.14
Nodes (4): interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act

### Community 108 - "Community 108"
Cohesion: 0.17
Nodes (10): looks_like_db(), looks_like_http(), looks_like_tls(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, True when this port's banner result is exactly the silent-on-garbage     signatu, For every open port with a banner fact, returns {port: {branches}}     that obse, True when a service banner carries a database greeting signature, so a DB     on (+2 more)

### Community 109 - "Community 109"
Cohesion: 0.13
Nodes (5): When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., TestRunnerScopeValidation

### Community 110 - "Community 110"
Cohesion: 0.18
Nodes (12): AgentDeps, AgentOpts, isBlocked(), requiresApproval(), runAutonomousEngagement(), Rung, RUNG_LABELS, AgentState (+4 more)

### Community 111 - "Community 111"
Cohesion: 0.22
Nodes (13): client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId, PhaseRecommendation, planExploit() (+5 more)

### Community 112 - "Community 112"
Cohesion: 0.23
Nodes (6): _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO, _host_matches(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale

### Community 113 - "Community 113"
Cohesion: 0.23
Nodes (13): _all_known_cve_ids(), main(), _query_osv(), update_snapshot.py — the ONLY module in this package that talks to the network., The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, EPSS scores for exactly the CVE IDs this detection run actually cares     about, Some macOS python.org installs ship expecting `Install Certificates.     command, All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n (+5 more)

### Community 114 - "Community 114"
Cohesion: 0.16
Nodes (9): _content_hash(), _default_products(), load_snapshot(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Derives the synced product list from cpe_normalizer.py's tables —     the single, Stable hash of the snapshot's actual vulnerability content — recorded     in eve, SnapshotMeta, TestFindingPostInit (+1 more)

### Community 115 - "Community 115"
Cohesion: 0.16
Nodes (7): AdversaError, AdversaErrorOpts, diagnoseSpawnError(), ErrorCode, Errors, VedhaError, VedhaErrorOpts

### Community 116 - "Community 116"
Cohesion: 0.27
Nodes (13): createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), Job, JOBS_FILE (+5 more)

### Community 117 - "Community 117"
Cohesion: 0.24
Nodes (13): isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest, OPENVAS_CONFIGS, OpenVASScanRequest, validateHost() (+5 more)

### Community 118 - "Community 118"
Cohesion: 0.16
Nodes (10): OSError, NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here., # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree (+2 more)

### Community 119 - "Community 119"
Cohesion: 0.20
Nodes (7): _clean(), _Collector, Make a per-host scanner instance share ONE rate limiter + semaphore with all, Make a raw banner safe and readable for the summary line.      Many services ans, _rollup(), _run_active(), _shared()

### Community 120 - "Community 120"
Cohesion: 0.19
Nodes (12): _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them., Excluded networks -> masscan --exclude specs, so they get ZERO packets., A CIDR spec is in scope only if it is fully contained in an allowed network., target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them. (+4 more)

### Community 121 - "Community 121"
Cohesion: 0.21
Nodes (9): _get_cert_der(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None., _scan_tls_sync(), _sni(), TLSScanner (+1 more)

### Community 122 - "Community 122"
Cohesion: 0.20
Nodes (4): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect(), WindowsCollector

### Community 123 - "Community 123"
Cohesion: 0.26
Nodes (5): _engagement(), _finding(), pytest_addoption(), Register --msf-host CLI option for integration tests., TestExploitOrchestrator

### Community 124 - "Community 124"
Cohesion: 0.16
Nodes (9): gate_0_is_passive_profile(), gate_2_host_discovery(), gate_3_port_scan(), gate_5_branch_eligible(), gates.py — precondition functions deciding whether each stage of the workflow ru, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, Does `branch` apply to this host?       - Must be in this profile's allowed deep (+1 more)

### Community 125 - "Community 125"
Cohesion: 0.14
Nodes (1): TestValidateTargetsInScope

### Community 126 - "Community 126"
Cohesion: 0.20
Nodes (5): CacheEntry, classify_certainty(), True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, WorkflowCache

### Community 127 - "Community 127"
Cohesion: 0.22
Nodes (3): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., True when execution produced errors and no usable or cached facts.

### Community 128 - "Community 128"
Cohesion: 0.18
Nodes (9): check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, Raised when the binary is running on an unauthorized machine., Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B, Tests for agent/hw_bind.py (+1 more)

### Community 129 - "Community 129"
Cohesion: 0.17
Nodes (10): Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed)., Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable). (+2 more)

### Community 130 - "Community 130"
Cohesion: 0.36
Nodes (12): _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius(), _build_analyzer(), _critical_asset_ids(), _explain_hop(), get_attack_path() (+4 more)

### Community 131 - "Community 131"
Cohesion: 0.26
Nodes (7): FakeProcess, _finding_line(), test_nonzero_exit_retains_and_marks_partial_findings(), test_nonzero_exit_without_findings_raises_with_stderr(), test_run_scan_streams_jsonl_and_separates_timeouts(), test_template_initialization_failure_cannot_be_clean_zero(), test_timeout_retains_findings_emitted_before_termination()

### Community 132 - "Community 132"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 133 - "Community 133"
Cohesion: 0.17
Nodes (12): _check_anti_debug(), Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block (+4 more)

### Community 134 - "Community 134"
Cohesion: 0.18
Nodes (3): decode_key(), Verify a Manager-signed policy and return its public key for TOFU pinning., verify_site_policy()

### Community 135 - "Community 135"
Cohesion: 0.23
Nodes (7): extract_features(), VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)., Build the model's feature vector from a Finding (+ optional Asset + extra     co, _to_float()

### Community 136 - "Community 136"
Cohesion: 0.24
Nodes (8): DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci, TestNeo4jClient

### Community 137 - "Community 137"
Cohesion: 0.26
Nodes (7): HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber(), isOptionalString(), normalizePort(), parseHttpxJsonLine()

### Community 138 - "Community 138"
Cohesion: 0.18
Nodes (9): CheckOpts, groupResults(), NativePortResult, nativePortScan(), NativeScanOpts, PORT_NAMES, PortRange, resolvePorts() (+1 more)

### Community 139 - "Community 139"
Cohesion: 0.27
Nodes (7): bulk_import_assets(), _compute_overview(), create_engagement(), engagements_overview(), _overview_cache_key(), _refresh_overview_cache(), update_engagement()

### Community 140 - "Community 140"
Cohesion: 0.29
Nodes (3): _enum_with_entries(), _FakeEntry, TestLDAPEnumeratorParsing

### Community 141 - "Community 141"
Cohesion: 0.17
Nodes (1): TestAgentJobCompatibility

### Community 142 - "Community 142"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 143 - "Community 143"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()

### Community 144 - "Community 144"
Cohesion: 0.17
Nodes (2): Tests that use the real engine but with no-op callbacks., TestRunnerHeadless

### Community 145 - "Community 145"
Cohesion: 0.22
Nodes (5): main(), _orchestrate(), # NOTE: credentialed collectors (ssh_collector, windows_collector) are run, service_banner.py — grab service banners and light version strings.  METHOD (col, ServiceBannerScanner

### Community 146 - "Community 146"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 147 - "Community 147"
Cohesion: 0.18
Nodes (7): Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., TestPromoteAssets

### Community 148 - "Community 148"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 149 - "Community 149"
Cohesion: 0.18
Nodes (1): TestNucleiExploitRunner

### Community 150 - "Community 150"
Cohesion: 0.18
Nodes (1): TestValidatePayload

### Community 151 - "Community 151"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 152 - "Community 152"
Cohesion: 0.20
Nodes (2): test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses(), _token()

### Community 153 - "Community 153"
Cohesion: 0.18
Nodes (1): TestNmapXMLParser

### Community 154 - "Community 154"
Cohesion: 0.20
Nodes (5): HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Transport

### Community 155 - "Community 155"
Cohesion: 0.33
Nodes (1): ExploitOrchestrator

### Community 156 - "Community 156"
Cohesion: 0.20
Nodes (9): Safety constants, exceptions, and validators for the exploitation engine.  All s, Raises SafetyViolationError if payload is not on allowlist     or violates per-p, Raises SafetyViolationError if module is on the block list., Raises OutOfScopeError if target_ip is not in scope or is excluded., True if this target requires human manager approval before exploit runs., requires_approval(), validate_module(), validate_payload() (+1 more)

### Community 157 - "Community 157"
Cohesion: 0.20
Nodes (8): ACTIVITY, Credential, Engagement, engagementsStore, EngagementStatus, FINDINGS_TIMELINE, now, STORE

### Community 158 - "Community 158"
Cohesion: 0.27
Nodes (7): NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), parseWhatWebOutput(), WhatWebParseResult, WhatWebResult

### Community 159 - "Community 159"
Cohesion: 0.27
Nodes (7): COMMON_RANGES, estimateHostCount(), isValidTarget(), ParseResult, parseTargets(), RFC1918, validOctets()

### Community 160 - "Community 160"
Cohesion: 0.20
Nodes (6): HttpProbeResult, NativeHttpOpts, nativeHttpProbe(), TECH_RULES, TechRule, WEB_PORT_PROTO

### Community 161 - "Community 161"
Cohesion: 0.27
Nodes (5): check(), _fact(), _free_port(), _Handler, main()

### Community 162 - "Community 162"
Cohesion: 0.20
Nodes (10): _agent_token_from_websocket(), agent_websocket_endpoint(), _claim_pushed_job(), Persistent WebSocket for probe → manager push communication.      Authentication, Persistent WebSocket for probe → manager push communication.      Authentication, Read an agent bearer token exclusively from the non-logged auth header., Read an agent bearer token exclusively from the non-logged auth header., Persistent WebSocket for probe → manager push communication.      Query params: (+2 more)

### Community 163 - "Community 163"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 166 - "Community 166"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 167 - "Community 167"
Cohesion: 0.20
Nodes (2): Each encryption uses a fresh ephemeral key, so blobs are different., TestEncryptDecryptRoundtrip

### Community 168 - "Community 168"
Cohesion: 0.20
Nodes (1): TestSubmitResult

### Community 169 - "Community 169"
Cohesion: 0.20
Nodes (7): Push a job to the first online connected agent.          Returns the agent_id th, Push a job to the first online agent in the requested tenant.          Returns t, Push a job to the first online agent in the requested tenant.          Returns t, Return idle connected agents belonging to exactly one tenant., Return idle connected agents belonging to exactly one tenant., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'.

### Community 170 - "Community 170"
Cohesion: 0.20
Nodes (6): AgentConnectionManager, Record transport features explicitly advertised by a connected probe., Record transport features explicitly advertised by a connected probe., Tracks WebSocket connections from probes/agents for direct job push.      Each c, Register an agent's WebSocket connection.          If the agent already has a co, Register an agent's WebSocket connection.          If the agent already has a co

### Community 171 - "Community 171"
Cohesion: 0.22
Nodes (9): Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation., Send periodic heartbeats over WebSocket., Acknowledge an offer without executing it before claim confirmation., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., _ws_heartbeat_sender() (+1 more)

### Community 172 - "Community 172"
Cohesion: 0.22
Nodes (7): Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active.

### Community 173 - "Community 173"
Cohesion: 0.22
Nodes (9): close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, FastAPI dependency that enforces role-based access.      Usage:         @router., require_role(), CurrentUser, Parsed from JWT claims — attached to request.state and injected as dependency. (+1 more)

### Community 174 - "Community 174"
Cohesion: 0.31
Nodes (5): Normalise naive datetimes to UTC so comparisons never raise., SigmaRuleGenerator — produces a Sigma detection rule (YAML) for a MITRE techniqu, Return a Sigma rule (YAML string) for the technique, customised with the, SigmaRuleGenerator, _stable_rule_id()

### Community 175 - "Community 175"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 176 - "Community 176"
Cohesion: 0.25
Nodes (4): HostDiscoveryScanner, host_discovery.py — determine which hosts are alive.  METHOD (collection only):, Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response).

### Community 177 - "Community 177"
Cohesion: 0.31
Nodes (7): compute(), SLA policy engine.  Turns a severity + "first seen" timestamp into a remediation, Aggregate SLA states across a set of findings.      Returns counts per state plu, Compute the SLA state for one finding. Never raises on missing data., SlaResult, summarize(), _windows()

### Community 178 - "Community 178"
Cohesion: 0.22
Nodes (1): TestUseCasesResolve

### Community 179 - "Community 179"
Cohesion: 0.22
Nodes (1): TestTargetsInExcludes

### Community 180 - "Community 180"
Cohesion: 0.22
Nodes (1): TestIdentity

### Community 181 - "Community 181"
Cohesion: 0.31
Nodes (8): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 182 - "Community 182"
Cohesion: 0.36
Nodes (6): create_access_token(), create_device_access_token(), create_refresh_token(), _now(), Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation.

### Community 183 - "Community 183"
Cohesion: 0.36
Nodes (7): extractScripts(), NmapHost, NmapScriptResult, NmapService, parseNmapXml(), parser, toArray()

### Community 184 - "Community 184"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, loadWordlist(), nativeDirBust(), NativeDirOpts, probe(), ProbeResp

### Community 185 - "Community 185"
Cohesion: 0.29
Nodes (8): MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, Run masscan over the given target specs and return its parsed JSON records., Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, _run_masscan()

### Community 186 - "Community 186"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 187 - "Community 187"
Cohesion: 0.29
Nodes (7): encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt scope payloads to a probe's X25519 publi, Encrypt scope JSON to a specific probe's X25519 public key.      Args:         s, Convenience: dict → JSON → encrypt → base64 string., Decode a base64-encoded X25519 public key to raw bytes.      Returns empty bytes

### Community 188 - "Community 188"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 189 - "Community 189"
Cohesion: 0.32
Nodes (3): _boundary_test_client(), test_agent_jwt_is_blocked_before_human_route_handler(), test_human_jwt_still_reaches_human_route_handler()

### Community 190 - "Community 190"
Cohesion: 0.25
Nodes (1): TestGraphVisualizer

### Community 191 - "Community 191"
Cohesion: 0.43
Nodes (1): TestMetasploitRPCClient

### Community 192 - "Community 192"
Cohesion: 0.25
Nodes (1): TestRequiresApproval

### Community 193 - "Community 193"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 194 - "Community 194"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 196 - "Community 196"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 197 - "Community 197"
Cohesion: 0.33
Nodes (6): ADError, build_ad_finding(), Shared building blocks for the Active Directory assessment module.  Every AD che, Assemble a Finding-compatible dict.      All findings carry — as required by the, Base class for Active Directory assessment errors., severity_from_str()

### Community 198 - "Community 198"
Cohesion: 0.48
Nodes (5): build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()

### Community 199 - "Community 199"
Cohesion: 0.67
Nodes (7): agents/greeting-introduction, main, 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit

### Community 200 - "Community 200"
Cohesion: 0.38
Nodes (6): base_score(), parse_vector(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network, CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r, Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin, _roundup()

### Community 201 - "Community 201"
Cohesion: 0.33
Nodes (4): _as_uuid(), AttackLogger, AttackLogger — records every attack action to the ``attack_timeline`` table.  Al, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 202 - "Community 202"
Cohesion: 0.33
Nodes (2): PortScanner, port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec

### Community 203 - "Community 203"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 204 - "Community 204"
Cohesion: 0.29
Nodes (1): TestIngestFile

### Community 205 - "Community 205"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 206 - "Community 206"
Cohesion: 0.29
Nodes (1): TestValidateModule

### Community 207 - "Community 207"
Cohesion: 0.29
Nodes (1): TestValidateScope

### Community 208 - "Community 208"
Cohesion: 0.38
Nodes (3): _dry_run(), test_installer_accepts_enroll_token_and_insecure_for_http_manager(), test_installer_without_token_still_shows_manual_approval()

### Community 209 - "Community 209"
Cohesion: 0.29
Nodes (1): TestMergeExclusions

### Community 210 - "Community 210"
Cohesion: 0.29
Nodes (5): Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., TestRunnerSubmission

### Community 212 - "Community 212"
Cohesion: 0.29
Nodes (5): Remove an agent's WebSocket registration., Remove the current registration, optionally only for one socket.          Return, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job

### Community 213 - "Community 213"
Cohesion: 0.33
Nodes (5): _atomic_write_private_state(), Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., _sync_directory()

### Community 214 - "Community 214"
Cohesion: 0.33
Nodes (3): Apply constraints + indexes (idempotent)., Run a Cypher statement and return records as dicts. [] if not connected., Run a parametrised write with UNWIND batching for bulk node/edge loads.

### Community 215 - "Community 215"
Cohesion: 0.33
Nodes (4): _deterministic_layout(), GraphVisualizer, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag

### Community 216 - "Community 216"
Cohesion: 0.47
Nodes (3): get_finding(), patch_finding(), _tenant_finding()

### Community 217 - "Community 217"
Cohesion: 0.40
Nodes (5): AttemptClaim, claim_job_attempt(), Atomically claim a pending job and create its fenced attempt ledger row., Renew only the currently installed running attempt/fence., renew_job_attempt()

### Community 218 - "Community 218"
Cohesion: 0.33
Nodes (6): _identity_ip(), Return network identities that could create assets or findings.      Scanner-lev, Parse a probe identity as an IP, tolerating common host:port notation., Return result identities outside the job's authoritative IP scope.      Fail clo, _result_network_identities(), validate_result_scope()

### Community 219 - "Community 219"
Cohesion: 0.33
Nodes (1): TestASREPRoastChecker

### Community 220 - "Community 220"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 221 - "Community 221"
Cohesion: 0.33
Nodes (1): TestCvss

### Community 222 - "Community 222"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 223 - "Community 223"
Cohesion: 0.60
Nodes (5): Unit tests for the dashboard list endpoints (jobs + assets)., _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user()

### Community 224 - "Community 224"
Cohesion: 0.33
Nodes (4): Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., TestTaskRunnerWithEncryptedScope

### Community 225 - "Community 225"
Cohesion: 0.33
Nodes (2): Phase 1: combined scope validation (validate + excludes)., TestScopeValidationPipeline

### Community 226 - "Community 226"
Cohesion: 0.33
Nodes (2): Phase 2: WebSocket message parsing., TestWebSocketMessageProtocol

### Community 227 - "Community 227"
Cohesion: 0.33
Nodes (4): Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup., TestStartupGauntlet

### Community 229 - "Community 229"
Cohesion: 0.33
Nodes (1): TestClamp

### Community 230 - "Community 230"
Cohesion: 0.33
Nodes (1): TestEngagementModes

### Community 231 - "Community 231"
Cohesion: 0.33
Nodes (1): TestFetchEngagementScope

### Community 232 - "Community 232"
Cohesion: 0.33
Nodes (1): TestValidateEnv

### Community 233 - "Community 233"
Cohesion: 0.33
Nodes (6): expire_attempt(), Expire one fenced attempt; return True when the job may be retried., Expire current attempts and requeue only jobs within their retry budget., Poll loop: requeue expired jobs every reaper_interval_seconds until stopped., reap_once(), run_reaper()

### Community 234 - "Community 234"
Cohesion: 0.33
Nodes (3): diff_assets(), report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d, re-scan mode's delta report: what changed between two engagements.

### Community 235 - "Community 235"
Cohesion: 0.40
Nodes (5): _load_env(), Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience.

### Community 236 - "Community 236"
Cohesion: 0.40
Nodes (4): True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls.

### Community 237 - "Community 237"
Cohesion: 0.40
Nodes (4): Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce

### Community 238 - "Community 238"
Cohesion: 0.40
Nodes (4): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of

### Community 239 - "Community 239"
Cohesion: 0.40
Nodes (4): Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons

### Community 240 - "Community 240"
Cohesion: 0.40
Nodes (4): Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used

### Community 241 - "Community 241"
Cohesion: 0.40
Nodes (4): Return the WebSocket connection URL with auth token.          The token is passe, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica

### Community 242 - "Community 242"
Cohesion: 0.40
Nodes (4): Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns

### Community 243 - "Community 243"
Cohesion: 0.40
Nodes (5): Raised when one or more fatal checks fail — aborts app startup., StartupAbortError, RuntimeError, Raised when a required configuration invariant is violated at boot., StartupValidationError

### Community 244 - "Community 244"
Cohesion: 0.70
Nodes (4): create_findings_from_probe_result(), _find_open_duplicate(), _map_severity(), _resolve_asset()

### Community 245 - "Community 245"
Cohesion: 0.40
Nodes (4): __dirname, frontendRoot, nextConfig, securityHeaders

### Community 246 - "Community 246"
Cohesion: 0.50
Nodes (2): _run_ad_assessment_and_save(), _set_job_status()

### Community 247 - "Community 247"
Cohesion: 0.60
Nodes (2): _claim_fixture(), TestAtomicWebSocketClaim

### Community 248 - "Community 248"
Cohesion: 0.40
Nodes (1): TestTenantWebSocketSelection

### Community 249 - "Community 249"
Cohesion: 0.40
Nodes (1): TestGetAgentJobs

### Community 250 - "Community 250"
Cohesion: 0.40
Nodes (1): TestEDRParsing

### Community 252 - "Community 252"
Cohesion: 0.40
Nodes (1): TestCheckHwBind

### Community 253 - "Community 253"
Cohesion: 0.40
Nodes (2): Phase 1: result spool with upload retry., TestResultSpoolWithRetry

### Community 254 - "Community 254"
Cohesion: 0.40
Nodes (3): Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine., TestTransportWithIdentity

### Community 256 - "Community 256"
Cohesion: 0.40
Nodes (1): TestEngineSummary

### Community 257 - "Community 257"
Cohesion: 0.40
Nodes (1): TestGate2

### Community 258 - "Community 258"
Cohesion: 0.40
Nodes (1): TestLooksLikeHttp

### Community 259 - "Community 259"
Cohesion: 0.40
Nodes (1): TestLooksLikeTls

### Community 260 - "Community 260"
Cohesion: 0.40
Nodes (1): TestResolveScanType

### Community 261 - "Community 261"
Cohesion: 0.40
Nodes (1): TestTargets

### Community 262 - "Community 262"
Cohesion: 0.40
Nodes (1): TestDeviceEnrollment

### Community 263 - "Community 263"
Cohesion: 0.40
Nodes (1): TestWebSocket

### Community 264 - "Community 264"
Cohesion: 0.40
Nodes (1): Cross-validates the pure-Python Debian version comparator against the real `dpkg

### Community 265 - "Community 265"
Cohesion: 0.70
Nodes (4): _b64(), issue(), keygen(), main()

### Community 266 - "Community 266"
Cohesion: 0.50
Nodes (4): Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., Release a staged job only after the manager confirms its claim., _ws_take_confirmed_job()

### Community 267 - "Community 267"
Cohesion: 0.50
Nodes (4): decrypt_scope(), decrypt_scope_b64(), decrypt_scope() accepting a base64 string from JSON transport., Decrypt a scope blob using the probe's private key.      Args:         blob: Wir

### Community 268 - "Community 268"
Cohesion: 0.50
Nodes (4): encrypt_scope(), encrypt_scope_b64(), encrypt_scope() returning a base64 string suitable for JSON transport., Encrypt scope JSON to a specific probe's public key.      Args:         scope_js

### Community 269 - "Community 269"
Cohesion: 0.50
Nodes (1): DiagnosticsReport

### Community 270 - "Community 270"
Cohesion: 0.83
Nodes (3): die(), load_facts(), main()

### Community 271 - "Community 271"
Cohesion: 0.67
Nodes (1): _ConnectSweep

### Community 272 - "Community 272"
Cohesion: 0.67
Nodes (3): compute_exposure(), Exposure analytics — protocol risk + zone health.  Derives two dashboard aggrega, _sev()

### Community 274 - "Community 274"
Cohesion: 0.50
Nodes (1): TestGate3

### Community 275 - "Community 275"
Cohesion: 0.50
Nodes (1): TestGate4

### Community 276 - "Community 276"
Cohesion: 0.50
Nodes (1): TestRouteBranches

### Community 277 - "Community 277"
Cohesion: 0.50
Nodes (1): TestScanResult

### Community 278 - "Community 278"
Cohesion: 0.83
Nodes (3): _objects(), test_expired_attempt_fails_job_when_retry_budget_is_exhausted(), test_expired_attempt_requeues_with_fence_history_preserved()

### Community 279 - "Community 279"
Cohesion: 0.50
Nodes (1): Product-boundary tests for the single-dashboard Manager API.

### Community 280 - "Community 280"
Cohesion: 0.50
Nodes (1): TestHashHelpers

### Community 281 - "Community 281"
Cohesion: 0.50
Nodes (1): TestHeartbeat

### Community 282 - "Community 282"
Cohesion: 0.50
Nodes (1): TestHttpGet

### Community 283 - "Community 283"
Cohesion: 0.50
Nodes (1): TestPollJobs

### Community 284 - "Community 284"
Cohesion: 0.50
Nodes (1): TestRefreshRegistration

### Community 285 - "Community 285"
Cohesion: 0.50
Nodes (1): TestRegister

### Community 286 - "Community 286"
Cohesion: 0.50
Nodes (1): Transactional outbox for durable background work (detection, etc.).  Producers i

### Community 287 - "Community 287"
Cohesion: 0.50
Nodes (1): Temporal detection: detection_runs table + finding provenance columns.  Records

### Community 288 - "Community 288"
Cohesion: 0.50
Nodes (1): Job leasing: scan_jobs.lease_expires_at for the dead-probe reaper.  A claimed (r

### Community 289 - "Community 289"
Cohesion: 0.50
Nodes (1): Agentic AI advisor: agent_recommendations (recommend-only, human-approved).  Sto

### Community 290 - "Community 290"
Cohesion: 0.50
Nodes (1): Add agents.public_key (Phase-4 X25519 identity for scope encryption).  The probe

### Community 291 - "Community 291"
Cohesion: 0.50
Nodes (1): Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises

### Community 292 - "Community 292"
Cohesion: 0.50
Nodes (1): Add is_active to users and tenants; add password_expires_at to users.  All exist

### Community 293 - "Community 293"
Cohesion: 0.50
Nodes (1): Add fenced execution attempts for agent-dispatched scan jobs.  Revision ID: 0017

### Community 294 - "Community 294"
Cohesion: 0.50
Nodes (1): Add Manager-approved device-key probe enrollment and Site policy.  Revision ID:

### Community 295 - "Community 295"
Cohesion: 0.50
Nodes (3): Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag

### Community 296 - "Community 296"
Cohesion: 0.50
Nodes (3): Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs.

### Community 297 - "Community 297"
Cohesion: 0.50
Nodes (3): Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.

### Community 298 - "Community 298"
Cohesion: 0.50
Nodes (3): Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy).

### Community 299 - "Community 299"
Cohesion: 0.50
Nodes (3): Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job).

### Community 300 - "Community 300"
Cohesion: 0.67
Nodes (3): get_read_db(), Read-only session (no commit) routed to the replica when configured.     For SEL, Read-only session (no commit) routed to the replica when configured.     For SEL

### Community 301 - "Community 301"
Cohesion: 0.67
Nodes (1): TestAgentWebSocketAuthentication

### Community 302 - "Community 302"
Cohesion: 0.67
Nodes (1): TestJobSecretBoundary

### Community 303 - "Community 303"
Cohesion: 0.67
Nodes (1): TestAgentExecutableTypes

### Community 304 - "Community 304"
Cohesion: 0.67
Nodes (1): TestAgentRegistrationRefresh

### Community 305 - "Community 305"
Cohesion: 0.67
Nodes (1): TestAssetMergeCredentialed

### Community 306 - "Community 306"
Cohesion: 0.67
Nodes (1): TestAssetMergeHostDiscovery

### Community 307 - "Community 307"
Cohesion: 0.67
Nodes (1): TestAssetMergePortScan

### Community 308 - "Community 308"
Cohesion: 0.67
Nodes (1): TestAssetOpenPortsForDeepScan

### Community 309 - "Community 309"
Cohesion: 0.67
Nodes (3): ResultSpool with tiny retry delay for fast tests., ResultSpool with tiny retry delay for fast tests., spool()

### Community 310 - "Community 310"
Cohesion: 0.67
Nodes (1): TestKeyGeneration

### Community 311 - "Community 311"
Cohesion: 0.67
Nodes (1): TestDriftDetection

### Community 312 - "Community 312"
Cohesion: 0.67
Nodes (1): TestPasswordRotation

### Community 313 - "Community 313"
Cohesion: 0.67
Nodes (1): TestRunnerScanTypes

### Community 314 - "Community 314"
Cohesion: 0.67
Nodes (3): Create a Transport with a real state file path but no actual HTTP calls., Create a Transport with a real state file path but no actual HTTP calls., transport()

### Community 315 - "Community 315"
Cohesion: 0.67
Nodes (1): TestFetchScope

### Community 316 - "Community 316"
Cohesion: 0.67
Nodes (2): Record a heartbeat from an agent., Record a heartbeat from an agent.

### Community 317 - "Community 317"
Cohesion: 1.00
Nodes (1): Open the driver and verify connectivity. Returns False on any failure.

### Community 318 - "Community 318"
Cohesion: 1.00
Nodes (1): TestAssetMergePassiveCollect

### Community 319 - "Community 319"
Cohesion: 1.00
Nodes (1): TestAssetMergeServiceBanner

### Community 320 - "Community 320"
Cohesion: 1.00
Nodes (1): TestAssetMergeSmbScan

### Community 321 - "Community 321"
Cohesion: 1.00
Nodes (1): TestAssetMergeTlsScan

### Community 322 - "Community 322"
Cohesion: 1.00
Nodes (1): TestAssetMergeUnknownScanner

### Community 323 - "Community 323"
Cohesion: 1.00
Nodes (1): TestAssetMergeWebScan

### Community 324 - "Community 324"
Cohesion: 1.00
Nodes (1): Fast port discovery with naabu. Feeds port list to Nmap.

### Community 325 - "Community 325"
Cohesion: 1.00
Nodes (1): Nmap service enumeration. Accepts port list from Naabu.

### Community 326 - "Community 326"
Cohesion: 1.00
Nodes (1): Nuclei vulnerability scan — production-ready.

### Community 327 - "Community 327"
Cohesion: 1.00
Nodes (1): Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.

### Community 328 - "Community 328"
Cohesion: 1.00
Nodes (1): NetExec SMB validation: signing, null sessions, SMBv1.

### Community 329 - "Community 329"
Cohesion: 1.00
Nodes (1): testssl.sh TLS/SSL analysis.

### Community 330 - "Community 330"
Cohesion: 1.00
Nodes (1): Extract HTTP/HTTPS URLs from nmap XML output.

### Community 331 - "Community 331"
Cohesion: 1.00
Nodes (1): EyeWitness screenshot evidence collection.

### Community 332 - "Community 332"
Cohesion: 1.00
Nodes (1): Safe lateral movement checks — no actual exploitation.

### Community 333 - "Community 333"
Cohesion: 1.00
Nodes (1): Cloud infrastructure scan (AWS/Azure/GCP).

### Community 334 - "Community 334"
Cohesion: 1.00
Nodes (1): Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.

### Community 335 - "Community 335"
Cohesion: 1.00
Nodes (1): Read a KV-v2 secret from Vault.

### Community 336 - "Community 336"
Cohesion: 1.00
Nodes (1): Verify the Python probe can open what the TypeScript manager sealed (T14 interop

### Community 337 - "Community 337"
Cohesion: 1.00
Nodes (1): Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO

### Community 338 - "Community 338"
Cohesion: 1.00
Nodes (1): Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).

### Community 339 - "Community 339"
Cohesion: 1.00
Nodes (1): End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.

### Community 340 - "Community 340"
Cohesion: 1.00
Nodes (1): Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 341 - "Community 341"
Cohesion: 1.00
Nodes (1): ThreadingHTTPServer

## Knowledge Gaps
- **1143 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+1138 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 63`** (1 nodes): `TestResultSpool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 125`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 132`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 141`** (1 nodes): `TestAgentJobCompatibility`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 142`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 144`** (2 nodes): `Tests that use the real engine but with no-op callbacks.`, `TestRunnerHeadless`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 148`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 149`** (1 nodes): `TestNucleiExploitRunner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 150`** (1 nodes): `TestValidatePayload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 151`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 152`** (2 nodes): `test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()`, `_token()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 153`** (1 nodes): `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 155`** (1 nodes): `ExploitOrchestrator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 163`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 166`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (2 nodes): `Each encryption uses a fresh ephemeral key, so blobs are different.`, `TestEncryptDecryptRoundtrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 178`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 179`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 180`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 186`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 188`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 190`** (1 nodes): `TestGraphVisualizer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 191`** (1 nodes): `TestMetasploitRPCClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 192`** (1 nodes): `TestRequiresApproval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 196`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 202`** (2 nodes): `PortScanner`, `port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 203`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 204`** (1 nodes): `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 205`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (1 nodes): `TestValidateModule`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (1 nodes): `TestValidateScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 209`** (1 nodes): `TestMergeExclusions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (1 nodes): `TestASREPRoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (1 nodes): `TestCvss`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (2 nodes): `Phase 1: combined scope validation (validate + excludes).`, `TestScopeValidationPipeline`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (2 nodes): `Phase 2: WebSocket message parsing.`, `TestWebSocketMessageProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (1 nodes): `TestClamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (1 nodes): `TestEngagementModes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (1 nodes): `TestFetchEngagementScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (1 nodes): `TestValidateEnv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (2 nodes): `_run_ad_assessment_and_save()`, `_set_job_status()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (2 nodes): `_claim_fixture()`, `TestAtomicWebSocketClaim`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 248`** (1 nodes): `TestTenantWebSocketSelection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (1 nodes): `TestGetAgentJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (1 nodes): `TestEDRParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (1 nodes): `TestCheckHwBind`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (2 nodes): `Phase 1: result spool with upload retry.`, `TestResultSpoolWithRetry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (1 nodes): `TestEngineSummary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (1 nodes): `TestGate2`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (1 nodes): `TestLooksLikeHttp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 259`** (1 nodes): `TestLooksLikeTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (1 nodes): `TestResolveScanType`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (1 nodes): `TestTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (1 nodes): `TestDeviceEnrollment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (1 nodes): `TestWebSocket`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (1 nodes): `Cross-validates the pure-Python Debian version comparator against the real `dpkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (1 nodes): `DiagnosticsReport`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (1 nodes): `_ConnectSweep`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (1 nodes): `TestGate3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (1 nodes): `TestGate4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (1 nodes): `TestRouteBranches`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (1 nodes): `TestScanResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (1 nodes): `Product-boundary tests for the single-dashboard Manager API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (1 nodes): `TestHashHelpers`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (1 nodes): `TestHeartbeat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (1 nodes): `TestHttpGet`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (1 nodes): `TestPollJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (1 nodes): `TestRefreshRegistration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 285`** (1 nodes): `TestRegister`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 286`** (1 nodes): `Transactional outbox for durable background work (detection, etc.).  Producers i`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 287`** (1 nodes): `Temporal detection: detection_runs table + finding provenance columns.  Records`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 288`** (1 nodes): `Job leasing: scan_jobs.lease_expires_at for the dead-probe reaper.  A claimed (r`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 289`** (1 nodes): `Agentic AI advisor: agent_recommendations (recommend-only, human-approved).  Sto`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 290`** (1 nodes): `Add agents.public_key (Phase-4 X25519 identity for scope encryption).  The probe`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 291`** (1 nodes): `Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 292`** (1 nodes): `Add is_active to users and tenants; add password_expires_at to users.  All exist`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (1 nodes): `Add fenced execution attempts for agent-dispatched scan jobs.  Revision ID: 0017`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 294`** (1 nodes): `Add Manager-approved device-key probe enrollment and Site policy.  Revision ID:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 301`** (1 nodes): `TestAgentWebSocketAuthentication`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 302`** (1 nodes): `TestJobSecretBoundary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 303`** (1 nodes): `TestAgentExecutableTypes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 304`** (1 nodes): `TestAgentRegistrationRefresh`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 305`** (1 nodes): `TestAssetMergeCredentialed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 306`** (1 nodes): `TestAssetMergeHostDiscovery`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 307`** (1 nodes): `TestAssetMergePortScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 308`** (1 nodes): `TestAssetOpenPortsForDeepScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 310`** (1 nodes): `TestKeyGeneration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 311`** (1 nodes): `TestDriftDetection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 312`** (1 nodes): `TestPasswordRotation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 313`** (1 nodes): `TestRunnerScanTypes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 315`** (1 nodes): `TestFetchScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 316`** (2 nodes): `Record a heartbeat from an agent.`, `Record a heartbeat from an agent.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 317`** (1 nodes): `Open the driver and verify connectivity. Returns False on any failure.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 318`** (1 nodes): `TestAssetMergePassiveCollect`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 319`** (1 nodes): `TestAssetMergeServiceBanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (1 nodes): `TestAssetMergeSmbScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 321`** (1 nodes): `TestAssetMergeTlsScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 322`** (1 nodes): `TestAssetMergeUnknownScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 323`** (1 nodes): `TestAssetMergeWebScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 324`** (1 nodes): `Fast port discovery with naabu. Feeds port list to Nmap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 325`** (1 nodes): `Nmap service enumeration. Accepts port list from Naabu.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 326`** (1 nodes): `Nuclei vulnerability scan — production-ready.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 327`** (1 nodes): `Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 328`** (1 nodes): `NetExec SMB validation: signing, null sessions, SMBv1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 329`** (1 nodes): `testssl.sh TLS/SSL analysis.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 330`** (1 nodes): `Extract HTTP/HTTPS URLs from nmap XML output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 331`** (1 nodes): `EyeWitness screenshot evidence collection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 332`** (1 nodes): `Safe lateral movement checks — no actual exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 333`** (1 nodes): `Cloud infrastructure scan (AWS/Azure/GCP).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 334`** (1 nodes): `Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 335`** (1 nodes): `Read a KV-v2 secret from Vault.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 336`** (1 nodes): `Verify the Python probe can open what the TypeScript manager sealed (T14 interop`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 337`** (1 nodes): `Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 338`** (1 nodes): `Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 339`** (1 nodes): `End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 340`** (1 nodes): `Deterministic stand-ins emitting realistic output for 127.0.0.1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 341`** (1 nodes): `ThreadingHTTPServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 25` to `Community 38`, `Community 70`, `Community 90`, `Community 0`, `Community 32`, `Community 197`, `Community 102`, `Community 12`, `Community 2`, `Community 3`, `Community 140`, `Community 146`, `Community 219`, `Community 203`, `Community 188`, `Community 71`, `Community 86`, `Community 123`, `Community 191`, `Community 149`, `Community 192`, `Community 206`, `Community 150`, `Community 207`, `Community 1`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `Transport` connect `Community 154` to `Community 1`, `Community 104`, `Community 129`, `Community 213`, `Community 242`, `Community 172`, `Community 237`, `Community 240`, `Community 236`, `Community 238`, `Community 239`, `Community 241`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `Finding` connect `Community 2` to `Community 1`, `Community 55`, `Community 98`, `Community 12`, `Community 155`, `Community 13`, `Community 100`, `Community 11`, `Community 25`, `Community 3`, `Community 5`, `Community 177`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 173 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 173 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R` to the rest of the system?**
  _1143 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.021788283658787256 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.028980322003577818 - nodes in this community are weakly interconnected._