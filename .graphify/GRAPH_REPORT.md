# Graph Report - .  (2026-08-01)

## Corpus Check
- Large corpus: 571 files · ~433,362 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 4729 nodes · 10697 edges · 295 communities detected
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 2776 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 2776 · contains: 2204 · calls: 1486 · method: 1209 · MODIFIES: 1059 · rationale_for: 864 · imports: 446 · imports_from: 401 · inherits: 149 · ON_BRANCH: 77 · PARENT_OF: 26


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 571 · Candidates: 1303
- Excluded: 56 untracked · 63429 ignored · 2 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `c5e2d0e`
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
Cohesion: 0.03
Nodes (40): agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit, get_read_db(), Read-only session (no commit) routed to the replica when configured.     For SEL, client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the exi, Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a     prox, FastAPI dependency factory. Keys the window by (scope, client-IP). (+32 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (85): agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Convert a probe's self-assessed `findings` list into persisted Finding rows., GraphBuilder — turns engagement assets/services/findings into an attack graph., Build the full multi-type attack graph. Returns the populated DiGraph         (a, For each exploitable finding add an EXPLOITS edge Finding→Asset with         ``w (+77 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (42): HallucinationGuard, Run all relevant checks and return a combined verdict:         ``{valid, issues,, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide., _collect_cves_scores(), _enum(), _finding_scores() (+34 more)

### Community 3 - "Community 3"
Cohesion: 0.04
Nodes (23): BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL, HallucinationGuard — post-generation validation of LLM report text against the g, FastAPI dependency that enforces role-based access.      Usage:         @router., require_role(), 298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, d1b4dd3 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (46): ApiActivity, GET, ManagerAiResponse, 0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner UI, 1fe16c8 stable but some dead code, need to optimize, GET, POST, ManagerAiResponse (+38 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (52): ServiceFingerprint, FindingStatus, FindingImport, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), NessusScanRequest, _nuclei_finding(), _nuclei_terminal_result() (+44 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (29): aggregate(), ConsistencyReport, FindingConsistency, run_findings: one list of Findings per run (N runs). Aggregated by     the deter, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen, wilson_ci(), _compute_priority(), EpssDB (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (50): Agent, AgentStatus, ScanJobStatus, ScanJobType, UserRole, ADAssessRequest, Neo4jConfig, Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun (+42 more)

### Community 8 - "Community 8"
Cohesion: 0.07
Nodes (51): Base, BaseModel, create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, New raw-facts path: detect CVE findings from result['facts'] and persist     the, Background entry point (P1: keep detection OFF the probe-result request     path (+43 more)

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (34): apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl(), Session, SESSION_DIR (+26 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (51): A, ask(), askSecret(), banner(), choose(), chooseNextPhase(), confirm(), detectLocalSubnet() (+43 more)

### Community 11 - "Community 11"
Cohesion: 0.05
Nodes (39): ComplianceRef, COVERAGE_COLOR, DetectionCoverage, ExploitMaturity, Finding, FindingDetail(), FindingPage, FindingsPage() (+31 more)

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (43): all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), normalize(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web() (+35 more)

### Community 13 - "Community 13"
Cohesion: 0.07
Nodes (8): _finding(), TestAggregate, TestClassifyTier, TestComputePriority, TestDedupFindings, TestFindingConsistency, TestSuppressNegated, TestVerify

### Community 14 - "Community 14"
Cohesion: 0.07
Nodes (32): Agent, AGENT_STATUS, AgentStatus, PATH_STATUS, SEV_LABEL, Exposure, ProtocolRiskCard(), useExposure() (+24 more)

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (44): ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is, Raises SafetyViolationError if module or payload is not permitted., Raises SafetyViolationError if module or payload is not permitted., Raises OutOfScopeError if target_ip not in engagement scope., Raises OutOfScopeError if target_ip not in engagement scope., Full exploit execution pipeline with safety, scope, blast radius,         audit, Full exploit execution pipeline with safety, scope, blast radius,         audit, Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo (+36 more)

### Community 16 - "Community 16"
Cohesion: 0.10
Nodes (33): task_runner.py — orchestrates the full lifecycle of a single scan job.  Given a, use_cases.py — the finite, pre-defined library of scan scenarios the manager can, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, resolve(), backup-before-secret-removal, feat/probe-usecase-alignment, main (+25 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (30): buildAskCommand(), ConvMessage, buildScanCommand(), PROFILE_TOOLS, bySeverityCount(), runScan(), AgentJob, AgentJobResult (+22 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (25): AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient, propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Test double — a fixed lookup table, no network. Used to validate the     surroun (+17 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (33): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+25 more)

### Community 20 - "Community 20"
Cohesion: 0.13
Nodes (37): bin(), binName(), collectProcess(), hasBinary(), hasSystemBinary(), httpBannerGrab(), HttpxLine, isWindows() (+29 more)

### Community 21 - "Community 21"
Cohesion: 0.07
Nodes (32): DEMO_ASSET, DEMO_ENGAGEMENT, DEMO_FINDING, AssetInput, chat(), CRITICALITY_SCORE, DESTRUCTIVE_PATTERNS, EPSS_MOCK (+24 more)

### Community 22 - "Community 22"
Cohesion: 0.10
Nodes (26): ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, Shared building blocks for the Active Directory assessment module.  Every AD che, Assemble a Finding-compatible dict.      All findings carry — as required by the, Base class for Active Directory assessment errors., Raised when an LDAP/Kerberos/SMB connection to the DC fails. (+18 more)

### Community 23 - "Community 23"
Cohesion: 0.07
Nodes (26): Agent, AIBrainPage(), AiStatus, criticalChain, defaultAgents, Engagement, Finding, findings (+18 more)

### Community 24 - "Community 24"
Cohesion: 0.08
Nodes (32): Severity, counters, generateFindingId(), resetCounters(), SEV_PREFIX, groupNaabuResults(), NaabuRaw, NaabuResult (+24 more)

### Community 25 - "Community 25"
Cohesion: 0.08
Nodes (34): _applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _env_number(), _error_result(), _facts_from_cache(), _hosts_from_facts() (+26 more)

### Community 26 - "Community 26"
Cohesion: 0.07
Nodes (19): BaseScanner, expand_targets(), main_entrypoint(), RateLimiter, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Simple async rate limiter: at most `rate` operations per second., Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10 (+11 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (10): _candidate(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db(), TestCPECandidateCpe23, TestEnrichFinding, TestEpssDb, TestKevDb (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.07
Nodes (19): ADJ, ATTACK_PATHS, AttackPath, BlastRadiusResult, buildAttackPaths(), Chokepoint, CHOKEPOINTS, edgesForPath() (+11 more)

### Community 29 - "Community 29"
Cohesion: 0.11
Nodes (15): RateLimiter, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim, ServiceIdentifier, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner, Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr (+7 more)

### Community 30 - "Community 30"
Cohesion: 0.09
Nodes (31): config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES, Client, ClientJiraConfig, ClientNotifyConfig (+23 more)

### Community 31 - "Community 31"
Cohesion: 0.06
Nodes (26): result_spool.py — local result persistence with upload retry.  When the probe co, bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity(), pubkey_to_bytes() (+18 more)

### Community 32 - "Community 32"
Cohesion: 0.12
Nodes (30): buildToolsCommand(), C, ln(), showSpinner(), downloadFile(), extract(), getInstalledRecord(), installAll() (+22 more)

### Community 33 - "Community 33"
Cohesion: 0.06
Nodes (19): NAV_SECTIONS, NavItem, Sidebar(), SidebarProps, ActivityItem, ComplianceControl, ComplianceFramework, ComplianceFrameworkData (+11 more)

### Community 34 - "Community 34"
Cohesion: 0.10
Nodes (26): AuthContext, Handler, generateOtp(), OtpEntry, otpStore, OtpVerifyResult, SessionPayload, verifyOtp() (+18 more)

### Community 35 - "Community 35"
Cohesion: 0.09
Nodes (17): AssetCriticality, OrderedDict, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path, AssetIn, AssetOut, BulkAssetImportResult, Parse CSV text into a list of AssetIn models and error strings., Add NVD CVSS, EPSS, KEV flag, MITRE techniques, and composite risk.         Muta (+9 more)

### Community 36 - "Community 36"
Cohesion: 0.09
Nodes (24): NucleiExploitRunner, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Parse nuclei JSONL output for a single CVE PoC result., Parse nuclei JSONL output for a single CVE PoC result., Run Nuclei CVE PoC templates against a single target.     Every template is safe, Run Nuclei CVE PoC templates against a single target.     Every template is safe, Parse template YAML and validate it contains no write/delete/DoS actions. (+16 more)

### Community 37 - "Community 37"
Cohesion: 0.08
Nodes (20): ConnectionManager, GraphWebSocketManager, High-level manager for graph-specific WebSocket operations., Handle a new WebSocket client connection., Handle incoming WebSocket messages., Manages WebSocket connections with room-based broadcasting., Broadcast graph data update to all subscribers., Broadcast a single node update. (+12 more)

### Community 38 - "Community 38"
Cohesion: 0.08
Nodes (22): Engagement, Finding, FindingSummary, LiveOverview(), Sev, pct(), Sev, SEV_STYLE (+14 more)

### Community 39 - "Community 39"
Cohesion: 0.08
Nodes (20): FindingSeverity, NucleiMatch, boundedEnvMs(), OpenVASFinding, OpenVASHelperOutput, OpenVASTaskState, parseOpenVASHelperOutput(), runOpenVASScanBackground() (+12 more)

### Community 40 - "Community 40"
Cohesion: 0.08
Nodes (15): ATTACK_TIMELINE, AttackAction, correlationRuns, CoverageStats, DetectionOutcome, DetectionResult, detectionStore, EDR_DETECTIONS (+7 more)

### Community 41 - "Community 41"
Cohesion: 0.07
Nodes (4): _ConcurrencyScanner, _ExplodingScanner, test_host_fanout_is_bounded(), test_per_target_exception_preserves_other_results()

### Community 42 - "Community 42"
Cohesion: 0.10
Nodes (19): _metric(), _not_scored(), Pure helpers for controlled Probe capability and accuracy validation., Validate the small, explicit inventory used for accuracy scoring., Score promoted inventory against explicit host/port/service/CVE truth., Resolve suites plus explicit use-cases, preserving first-seen order., Require every IP/CIDR target to be fully allowed and not excluded., Return the conservative number of addresses represented by targets. (+11 more)

### Community 43 - "Community 43"
Cohesion: 0.15
Nodes (12): get_settings(), Settings, BaseSettings, AiGenerateRequest, AiGenerateResponse, AiMessage, AiProviderStatus, AiStatusResponse (+4 more)

### Community 44 - "Community 44"
Cohesion: 0.09
Nodes (11): BaseScanner, DBScanner, HostDiscoveryScanner, Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., PortScanner, ServiceBannerScanner, _build_get() (+3 more)

### Community 45 - "Community 45"
Cohesion: 0.07
Nodes (13): bracket_host(), parse_ports(), scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h, Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., resolve(), Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG (+5 more)

### Community 46 - "Community 46"
Cohesion: 0.11
Nodes (9): EvidenceTier, IntEnum, _fact(), TestAsset, TestCorrelateSmbPatch, TestFactRef, TestNormalize, TestNormalizeBanner (+1 more)

### Community 47 - "Community 47"
Cohesion: 0.07
Nodes (10): Tests for agent/transport.py, Create a Transport with a real state file path but no actual HTTP calls., Create a Transport with a real state file path but no actual HTTP calls., TestFetchScope, TestHeartbeat, TestHttpGet, TestPollJobs, TestRefreshRegistration (+2 more)

### Community 48 - "Community 48"
Cohesion: 0.11
Nodes (24): _finalize_trace(), _gather_per_host(), _port_candidates(), workflow_engine.py — the async DAG executor. Loops through gates, checks precond, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Return TCP ports worth scanning for this profile and requested branch set., In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass (+16 more)

### Community 49 - "Community 49"
Cohesion: 0.11
Nodes (17): Remove the spool file for a successfully uploaded result., Attempt to upload a result with retries and local spool as fallback.          Ar, Re-attempt upload of all previously spooled results.          Called once at pro, Number of pending (unsubmitted) results in the spool., Re-attempt upload of all previously spooled results.          Called once at pro, Number of pending (unsubmitted) results in the spool., Persists scan results locally and retries failed uploads., Persists scan results locally and retries failed uploads. (+9 more)

### Community 50 - "Community 50"
Cohesion: 0.13
Nodes (13): AttackAction, CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender, _parse_dt(), EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender, Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi (+5 more)

### Community 51 - "Community 51"
Cohesion: 0.11
Nodes (16): PageShell(), PageShellProps, EMPTY_FORM, Engagement, EngagementsPage(), EngagementsResponse, EngagementStatus, FormState (+8 more)

### Community 52 - "Community 52"
Cohesion: 0.09
Nodes (16): ToastContext, useToast(), ActivityItem, AssetRow, displayDate(), EDIT_STATUSES, Engagement, EngagementDetailPage() (+8 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (21): GET, STATUS_TO_API, VALID_SEVERITIES, VALID_SORTS, DETECTION_TO_UI, ENG_STATUS_TO_API, ENG_STATUS_TO_UI, engStatusToApi() (+13 more)

### Community 54 - "Community 54"
Cohesion: 0.10
Nodes (22): Agent, AgentCapability, AGENTS, agentsStore, AgentStatus, ensureDataDir(), FIELD_AGENTS_FILE, FieldAgent (+14 more)

### Community 55 - "Community 55"
Cohesion: 0.10
Nodes (20): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+12 more)

### Community 56 - "Community 56"
Cohesion: 0.11
Nodes (25): _flush_spool_over_http(), Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Poll pending jobs even while WS is connected.      This makes result delivery re (+17 more)

### Community 57 - "Community 57"
Cohesion: 0.13
Nodes (11): ElasticSIEM, _parse_dt(), SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi, Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_, Abstract SIEM connector., Splunk via the REST search endpoint (``/services/search/jobs/export``) with an, SentinelSIEM (+3 more)

### Community 58 - "Community 58"
Cohesion: 0.08
Nodes (15): apiFetch(), Cat, CATS, Engagement, EngineManifest, getToken(), Intensity, JobStatus (+7 more)

### Community 59 - "Community 59"
Cohesion: 0.11
Nodes (24): assessment(), discovery(), EngagementMode, host_discovery(), includes_stage(), port_scan(), modes.py — engagement mode configurations. Each mode is a thin config that tunes, Discovery + ports + banner only — no deep dives, no credentials. (+16 more)

### Community 60 - "Community 60"
Cohesion: 0.15
Nodes (22): ScanSummary, A, banner(), findingDetail(), findingLine(), findingsTable(), hostLine(), info() (+14 more)

### Community 61 - "Community 61"
Cohesion: 0.10
Nodes (8): Asset, _parse_ts(), PortFact, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Dispatch a real ScanResult into the right sub-structure, keyed         on result, Dispatch a real ScanResult into the right sub-structure, keyed         on result, _utcnow()

### Community 62 - "Community 62"
Cohesion: 0.11
Nodes (6): interpret_dns_recursion(), interpret_memcached_stats(), interpret_ntp_monlist(), _ntp_monlist_probe(), udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, UDPScanner

### Community 63 - "Community 63"
Cohesion: 0.09
Nodes (10): AiStatus, ConfigField, DEFAULT_RULES, DeploymentStatus, EMAIL_FIELDS, EnvSetting, INTEGRATIONS, JIRA_FIELDS (+2 more)

### Community 64 - "Community 64"
Cohesion: 0.13
Nodes (9): Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., TestEnqueueAgentJob, TestListAgents, TestOTProfileGate, TestRegisterAgent (+1 more)

### Community 65 - "Community 65"
Cohesion: 0.11
Nodes (15): _Socket, test_collector_raises_when_no_listener_binds(), test_ot_udp_backend_never_joins_or_transmits(), test_subset_listener_failure_reports_degraded_coverage(), _Writer, classify_scanner_error(), engine_manifest(), ErrorDetail (+7 more)

### Community 66 - "Community 66"
Cohesion: 0.16
Nodes (13): ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM, Read pKICertificateTemplate objects from the Configuration NC. (+5 more)

### Community 67 - "Community 67"
Cohesion: 0.13
Nodes (13): ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline, FindingSeverity, Returns nessus scan_id as string., Returns nessus scan_id as string., Returns scan_uuid (token for tracking)., Returns scan_uuid (token for tracking)., Returns {status, progress_percent, host_count}. (+5 more)

### Community 68 - "Community 68"
Cohesion: 0.15
Nodes (15): KerberoastChecker, Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., One aggregate Finding for all kerberoastable accounts.         Severity is Criti, One aggregate Finding for all kerberoastable accounts.         Severity is Criti, Enumerate kerberoastable accounts and capture TGS evidence., Enumerate kerberoastable accounts and capture TGS evidence., Returns user accounts that have a servicePrincipalName set (and are not (+7 more)

### Community 69 - "Community 69"
Cohesion: 0.15
Nodes (11): Exception, MetasploitRPCClient, MetasploitRPCError, Returns {status, output, uuid}., Returns True if job was successfully killed., Poll until job completes or max_wait exceeded., Authenticated RPC call — prepends token., Async Metasploit RPC client using msgpack-over-HTTPS. (+3 more)

### Community 70 - "Community 70"
Cohesion: 0.11
Nodes (6): _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_background_job_failed(), test_partial_nuclei_run_preserves_findings_and_diagnostics()

### Community 71 - "Community 71"
Cohesion: 0.16
Nodes (4): _asset(), TestAssetNeedsRecheckLive, TestGate5, TestGate6

### Community 72 - "Community 72"
Cohesion: 0.13
Nodes (11): _make_http_mock(), Unit tests for VulnEnrichmentService — all external HTTP calls mocked., Create a mock httpx.AsyncClient that returns different responses per URL., test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full(), test_fetch_epss_success() (+3 more)

### Community 73 - "Community 73"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 74 - "Community 74"
Cohesion: 0.14
Nodes (4): _scan_result(), TestCacheEntry, TestClassifyCertainty, TestWorkflowCache

### Community 75 - "Community 75"
Cohesion: 0.11
Nodes (7): BloodHoundCollector, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., Run bloodhound-python and return the list of produced JSON file paths.         R, TestBloodHoundCollector

### Community 76 - "Community 76"
Cohesion: 0.12
Nodes (13): metadata, AssistantProvider(), QueryProvider(), Theme, ThemeContext, ThemeContextValue, ThemeProvider(), useTheme() (+5 more)

### Community 77 - "Community 77"
Cohesion: 0.21
Nodes (14): AiMessage, ManagerAiResponse, POST(), validMessages(), cveRecordToFactCard(), detectFindingId(), isExploited(), plainWhyItMatters() (+6 more)

### Community 78 - "Community 78"
Cohesion: 0.15
Nodes (19): DeclarativeBase, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., Append-only ledger of every attack action performed during an engagement.      W, Immutable, append-only audit trail for all exploit actions.     No TimestampMixi, Base, TimestampMixin, Per-engagement SIEM + EDR connection settings used by the detection     validati, detection_run.py — one execution of the deterministic detection engine over a fa (+11 more)

### Community 79 - "Community 79"
Cohesion: 0.16
Nodes (18): _char_order(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), has_ambiguous_epoch(), version_compare.py — per-scheme version comparators.  Spec calls this "the highe (+10 more)

### Community 80 - "Community 80"
Cohesion: 0.15
Nodes (10): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+2 more)

### Community 81 - "Community 81"
Cohesion: 0.11
Nodes (1): TestResultSpool

### Community 82 - "Community 82"
Cohesion: 0.17
Nodes (16): _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError, license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the (+8 more)

### Community 83 - "Community 83"
Cohesion: 0.12
Nodes (15): JobResult, Structured result from running one scan job., Submit the result, with spool-and-retry if available., Structured result from running one scan job., Submit the result, with spool-and-retry if available., Submit the result, with spool-and-retry if available., Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Orchestrates one scan job's lifecycle.      The runner holds injected dependenci (+7 more)

### Community 84 - "Community 84"
Cohesion: 0.12
Nodes (11): ActivityItem, DashboardCharts(), Engagement, Finding, FindingPage, FindingSummary, SEV, STATUS_STYLE (+3 more)

### Community 85 - "Community 85"
Cohesion: 0.15
Nodes (12): correlate_smb_patch(), dedup_findings(), _product_from_cpe(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Suppress a suspected/potential (inferred-source) finding when the     SAME host (+4 more)

### Community 86 - "Community 86"
Cohesion: 0.18
Nodes (16): match_candidate(), matcher.py — does this CPE candidate's version fall inside a vulnerable range, p, dpkg_compare, but None instead of a misleading answer when one side     has an e, Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A, All Findings this single CPE candidate produces against the snapshot.     Empty, _safe_compare(), _version_in_ranges(), FindingState (+8 more)

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
Cohesion: 0.14
Nodes (15): fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), scope_validator.py — defense-in-depth scope re-validation for the probe.  The pr, Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)., Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Parse one IP, CIDR, or inclusive IP range into covering networks.      ``None`` (+7 more)

### Community 91 - "Community 91"
Cohesion: 0.18
Nodes (15): addComment(), Case, CaseActivity, CaseComment, CaseSeverity, CaseStatus, createCase(), DATA_FILE (+7 more)

### Community 92 - "Community 92"
Cohesion: 0.16
Nodes (10): _netbios_session(), parse_smb2_security_mode(), smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, Read signing posture from an SMB2 NEGOTIATE response.      The response carries, _smb1_negotiate(), _smb2_negotiate(), SMBScanner, _smb2_negotiate_response() (+2 more)

### Community 93 - "Community 93"
Cohesion: 0.19
Nodes (2): _action(), TestDetectionCorrelator

### Community 94 - "Community 94"
Cohesion: 0.15
Nodes (12): AgentDeps, AgentOpts, isBlocked(), requiresApproval(), runAutonomousEngagement(), Rung, RUNG_LABELS, AgentState (+4 more)

### Community 95 - "Community 95"
Cohesion: 0.13
Nodes (8): check_hw_bind(), get_hw_id(), hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B, Tests for agent/hw_bind.py, TestCheckHwBind, TestGetHwId

### Community 96 - "Community 96"
Cohesion: 0.20
Nodes (5): AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()

### Community 97 - "Community 97"
Cohesion: 0.28
Nodes (8): asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder, is_internet_exposed(), service_node_id(), _to_float()

### Community 98 - "Community 98"
Cohesion: 0.14
Nodes (6): _fetch(), _NoRedirect, parse_allow_header(), web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only., WebScanner

### Community 99 - "Community 99"
Cohesion: 0.17
Nodes (8): ASREPRoastChecker, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., ADAssessmentRunner, Coordinates all AD checkers for a single engagement., Returns {findings: [...], stats: {...}, errors: [...]}.         Never raises for

### Community 100 - "Community 100"
Cohesion: 0.13
Nodes (12): approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest, ExploitEvidence, ExploitJob, ExploitResult (+4 more)

### Community 101 - "Community 101"
Cohesion: 0.14
Nodes (4): interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act

### Community 102 - "Community 102"
Cohesion: 0.17
Nodes (10): looks_like_db(), looks_like_http(), looks_like_tls(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, True when this port's banner result is exactly the silent-on-garbage     signatu, For every open port with a banner fact, returns {port: {branches}}     that obse, True when a service banner carries a database greeting signature, so a DB     on (+2 more)

### Community 103 - "Community 103"
Cohesion: 0.13
Nodes (5): When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., TestRunnerScopeValidation

### Community 104 - "Community 104"
Cohesion: 0.22
Nodes (13): client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId, PhaseRecommendation, planExploit() (+5 more)

### Community 105 - "Community 105"
Cohesion: 0.23
Nodes (6): _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO, _host_matches(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale

### Community 106 - "Community 106"
Cohesion: 0.23
Nodes (13): _all_known_cve_ids(), main(), _query_osv(), update_snapshot.py — the ONLY module in this package that talks to the network., The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, EPSS scores for exactly the CVE IDs this detection run actually cares     about, Some macOS python.org installs ship expecting `Install Certificates.     command, All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n (+5 more)

### Community 107 - "Community 107"
Cohesion: 0.16
Nodes (9): _content_hash(), _default_products(), load_snapshot(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Derives the synced product list from cpe_normalizer.py's tables —     the single, Stable hash of the snapshot's actual vulnerability content — recorded     in eve, SnapshotMeta, TestFindingPostInit (+1 more)

### Community 108 - "Community 108"
Cohesion: 0.16
Nodes (7): AdversaError, AdversaErrorOpts, diagnoseSpawnError(), ErrorCode, Errors, VedhaError, VedhaErrorOpts

### Community 109 - "Community 109"
Cohesion: 0.27
Nodes (13): createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), Job, JOBS_FILE (+5 more)

### Community 110 - "Community 110"
Cohesion: 0.24
Nodes (13): isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest, OPENVAS_CONFIGS, OpenVASScanRequest, validateHost() (+5 more)

### Community 111 - "Community 111"
Cohesion: 0.16
Nodes (10): OSError, NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here., # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree (+2 more)

### Community 112 - "Community 112"
Cohesion: 0.20
Nodes (7): _clean(), _Collector, Make a per-host scanner instance share ONE rate limiter + semaphore with all, Make a raw banner safe and readable for the summary line.      Many services ans, _rollup(), _run_active(), _shared()

### Community 113 - "Community 113"
Cohesion: 0.19
Nodes (12): _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them., Excluded networks -> masscan --exclude specs, so they get ZERO packets., A CIDR spec is in scope only if it is fully contained in an allowed network., target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them. (+4 more)

### Community 114 - "Community 114"
Cohesion: 0.21
Nodes (9): _get_cert_der(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None., _scan_tls_sync(), _sni(), TLSScanner (+1 more)

### Community 115 - "Community 115"
Cohesion: 0.16
Nodes (9): gate_0_is_passive_profile(), gate_2_host_discovery(), gate_3_port_scan(), gate_5_branch_eligible(), gates.py — precondition functions deciding whether each stage of the workflow ru, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, Does `branch` apply to this host?       - Must be in this profile's allowed deep (+1 more)

### Community 116 - "Community 116"
Cohesion: 0.14
Nodes (1): TestValidateTargetsInScope

### Community 117 - "Community 117"
Cohesion: 0.20
Nodes (5): CacheEntry, classify_certainty(), True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, WorkflowCache

### Community 118 - "Community 118"
Cohesion: 0.22
Nodes (3): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., True when execution produced errors and no usable or cached facts.

### Community 119 - "Community 119"
Cohesion: 0.17
Nodes (6): NTLMRelayChecker, Build a Finding for hosts missing SMB signing. The attack_narrative         incl, Probe SMB/LDAP signing posture across a host list., For each IP, returns {signing_enabled, signing_required}.          A host is rel, Returns True if the DC *enforces* LDAP signing / channel binding.          We at, TestBuildADFinding

### Community 120 - "Community 120"
Cohesion: 0.15
Nodes (13): _bounded_env_int(), _is_local_manager_url(), _load_env(), main(), Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Load key=value lines from probe.env for dev convenience., Return an integer environment setting constrained to a safe range. (+5 more)

### Community 121 - "Community 121"
Cohesion: 0.15
Nodes (9): ModuleCategory, ModuleInput, ModuleOutput, MODULES, modulesByCategory(), modulesForPorts(), profileModules(), ScanModule (+1 more)

### Community 122 - "Community 122"
Cohesion: 0.17
Nodes (6): main(), _orchestrate(), # NOTE: credentialed collectors (ssh_collector, windows_collector) are run, host_discovery.py — determine which hosts are alive.  METHOD (collection only):, port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec, service_banner.py — grab service banners and light version strings.  METHOD (col

### Community 123 - "Community 123"
Cohesion: 0.36
Nodes (12): _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius(), _build_analyzer(), _critical_asset_ids(), _explain_hop(), get_attack_path() (+4 more)

### Community 124 - "Community 124"
Cohesion: 0.29
Nodes (4): _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator

### Community 125 - "Community 125"
Cohesion: 0.26
Nodes (7): FakeProcess, _finding_line(), test_nonzero_exit_retains_and_marks_partial_findings(), test_nonzero_exit_without_findings_raises_with_stderr(), test_run_scan_streams_jsonl_and_separates_timeouts(), test_template_initialization_failure_cannot_be_clean_zero(), test_timeout_retains_findings_emitted_before_termination()

### Community 126 - "Community 126"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 127 - "Community 127"
Cohesion: 0.17
Nodes (8): Remove an agent's WebSocket registration., Remove the current registration, optionally only for one socket.          Return, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to the first online connected agent.          Returns the agent_id th, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to the first online agent in the requested tenant.          Returns t, Return idle connected agents belonging to exactly one tenant., Return 'online', 'busy', or 'offline'.

### Community 128 - "Community 128"
Cohesion: 0.23
Nodes (7): extract_features(), VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)., Build the model's feature vector from a Finding (+ optional Asset + extra     co, _to_float()

### Community 129 - "Community 129"
Cohesion: 0.18
Nodes (8): GzipRequestMiddleware, Identify the Manager API without exposing a second dashboard., _service_root(), Extracts JWT from Authorization header and injects tenant_id + user     claims i, Extracts JWT from Authorization header and injects tenant_id + user     claims i, Extracts JWT from Authorization header and injects tenant_id + user     claims i, TenantIsolationMiddleware, BaseHTTPMiddleware

### Community 130 - "Community 130"
Cohesion: 0.24
Nodes (8): DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci, TestNeo4jClient

### Community 131 - "Community 131"
Cohesion: 0.26
Nodes (7): HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber(), isOptionalString(), normalizePort(), parseHttpxJsonLine()

### Community 132 - "Community 132"
Cohesion: 0.18
Nodes (9): CheckOpts, groupResults(), NativePortResult, nativePortScan(), NativeScanOpts, PORT_NAMES, PortRange, resolvePorts() (+1 more)

### Community 133 - "Community 133"
Cohesion: 0.27
Nodes (7): bulk_import_assets(), _compute_overview(), create_engagement(), engagements_overview(), _overview_cache_key(), _refresh_overview_cache(), update_engagement()

### Community 134 - "Community 134"
Cohesion: 0.29
Nodes (3): _enum_with_entries(), _FakeEntry, TestLDAPEnumeratorParsing

### Community 135 - "Community 135"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 136 - "Community 136"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()

### Community 137 - "Community 137"
Cohesion: 0.17
Nodes (2): Tests that use the real engine but with no-op callbacks., TestRunnerHeadless

### Community 138 - "Community 138"
Cohesion: 0.27
Nodes (11): _claim_batch(), Event, main(), _mark_done(), _mark_retry_or_dead(), _process(), outbox.py (worker) — durable consumer for the transactional outbox.  Run as its, Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means (+3 more)

### Community 139 - "Community 139"
Cohesion: 0.18
Nodes (9): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable)., Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Raised when a transport operation fails permanently (not retryable). (+1 more)

### Community 140 - "Community 140"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 141 - "Community 141"
Cohesion: 0.18
Nodes (1): TestAgentJobCompatibility

### Community 142 - "Community 142"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 143 - "Community 143"
Cohesion: 0.18
Nodes (1): TestNucleiExploitRunner

### Community 144 - "Community 144"
Cohesion: 0.18
Nodes (1): TestValidatePayload

### Community 145 - "Community 145"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 146 - "Community 146"
Cohesion: 0.18
Nodes (1): TestNmapXMLParser

### Community 147 - "Community 147"
Cohesion: 0.20
Nodes (10): _check_anti_debug(), Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block (+2 more)

### Community 148 - "Community 148"
Cohesion: 0.20
Nodes (10): _load_or_create_identity(), _obtain_identity(), Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu (+2 more)

### Community 149 - "Community 149"
Cohesion: 0.33
Nodes (1): ExploitOrchestrator

### Community 150 - "Community 150"
Cohesion: 0.20
Nodes (8): ACTIVITY, Credential, Engagement, engagementsStore, EngagementStatus, FINDINGS_TIMELINE, now, STORE

### Community 151 - "Community 151"
Cohesion: 0.27
Nodes (7): NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), parseWhatWebOutput(), WhatWebParseResult, WhatWebResult

### Community 152 - "Community 152"
Cohesion: 0.27
Nodes (7): COMMON_RANGES, estimateHostCount(), isValidTarget(), ParseResult, parseTargets(), RFC1918, validOctets()

### Community 153 - "Community 153"
Cohesion: 0.20
Nodes (6): HttpProbeResult, NativeHttpOpts, nativeHttpProbe(), TECH_RULES, TechRule, WEB_PORT_PROTO

### Community 154 - "Community 154"
Cohesion: 0.27
Nodes (5): check(), _fact(), _free_port(), _Handler, main()

### Community 155 - "Community 155"
Cohesion: 0.20
Nodes (4): Unit tests for the agent/probe protocol changes:   * agent polling is restricted, TestAccessTokenExpiry, TestAgentExecutableTypes, TestAgentRegistrationRefresh

### Community 156 - "Community 156"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 159 - "Community 159"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 160 - "Community 160"
Cohesion: 0.20
Nodes (2): Each encryption uses a fresh ephemeral key, so blobs are different., TestEncryptDecryptRoundtrip

### Community 161 - "Community 161"
Cohesion: 0.25
Nodes (6): _atomic_write_private_state(), Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., _sync_directory()

### Community 162 - "Community 162"
Cohesion: 0.25
Nodes (4): HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Transport

### Community 163 - "Community 163"
Cohesion: 0.31
Nodes (5): Normalise naive datetimes to UTC so comparisons never raise., SigmaRuleGenerator — produces a Sigma detection rule (YAML) for a MITRE techniqu, Return a Sigma rule (YAML string) for the technique, customised with the, SigmaRuleGenerator, _stable_rule_id()

### Community 164 - "Community 164"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 165 - "Community 165"
Cohesion: 0.31
Nodes (7): compute(), SLA policy engine.  Turns a severity + "first seen" timestamp into a remediation, Aggregate SLA states across a set of findings.      Returns counts per state plu, Compute the SLA state for one finding. Never raises on missing data., SlaResult, summarize(), _windows()

### Community 166 - "Community 166"
Cohesion: 0.31
Nodes (3): _claim_fixture(), TestAtomicWebSocketClaim, TestJobSecretBoundary

### Community 167 - "Community 167"
Cohesion: 0.22
Nodes (1): TestUseCasesResolve

### Community 168 - "Community 168"
Cohesion: 0.22
Nodes (1): TestTargetsInExcludes

### Community 169 - "Community 169"
Cohesion: 0.22
Nodes (1): TestIdentity

### Community 170 - "Community 170"
Cohesion: 0.22
Nodes (5): AgentConnectionManager, Record transport features explicitly advertised by a connected probe., Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Tracks WebSocket connections from probes/agents for direct job push.      Each c

### Community 171 - "Community 171"
Cohesion: 0.31
Nodes (8): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 172 - "Community 172"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, loadWordlist(), nativeDirBust(), NativeDirOpts, probe(), ProbeResp

### Community 173 - "Community 173"
Cohesion: 0.32
Nodes (7): attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon(), nativePtrSweep(), PtrSweepResult, safe()

### Community 174 - "Community 174"
Cohesion: 0.29
Nodes (8): MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, Run masscan over the given target specs and return its parsed JSON records., Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, _run_masscan()

### Community 175 - "Community 175"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 176 - "Community 176"
Cohesion: 0.43
Nodes (1): WindowsCollector

### Community 177 - "Community 177"
Cohesion: 0.29
Nodes (7): encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt scope payloads to a probe's X25519 publi, Encrypt scope JSON to a specific probe's X25519 public key.      Args:         s, Convenience: dict → JSON → encrypt → base64 string., Decode a base64-encoded X25519 public key to raw bytes.      Returns empty bytes

### Community 178 - "Community 178"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 179 - "Community 179"
Cohesion: 0.25
Nodes (1): TestGraphVisualizer

### Community 180 - "Community 180"
Cohesion: 0.43
Nodes (1): TestMetasploitRPCClient

### Community 181 - "Community 181"
Cohesion: 0.25
Nodes (1): TestRequiresApproval

### Community 182 - "Community 182"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 183 - "Community 183"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 185 - "Community 185"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 186 - "Community 186"
Cohesion: 0.25
Nodes (1): TestSubmitResult

### Community 187 - "Community 187"
Cohesion: 0.29
Nodes (7): Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., _ws_heartbeat_sender(), _ws_stage_job_offer()

### Community 188 - "Community 188"
Cohesion: 0.38
Nodes (7): HWBindError, Raised when the binary is running on an unauthorized machine., AgentUnavailableError, Raised when the Anthropic SDK or API key is not configured., AgentRecommendation, agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag, RuntimeError

### Community 189 - "Community 189"
Cohesion: 0.29
Nodes (5): Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., True if the WebSocket connection is active.

### Community 190 - "Community 190"
Cohesion: 0.29
Nodes (7): close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, CurrentUser, Parsed from JWT claims — attached to request.state and injected as dependency., Parsed from JWT claims — attached to request.state and injected as dependency.

### Community 191 - "Community 191"
Cohesion: 0.48
Nodes (5): build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()

### Community 192 - "Community 192"
Cohesion: 0.67
Nodes (7): agents/greeting-introduction, main, 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit

### Community 193 - "Community 193"
Cohesion: 0.38
Nodes (6): base_score(), parse_vector(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network, CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r, Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin, _roundup()

### Community 194 - "Community 194"
Cohesion: 0.33
Nodes (4): _as_uuid(), AttackLogger, AttackLogger — records every attack action to the ``attack_timeline`` table.  Al, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 195 - "Community 195"
Cohesion: 0.29
Nodes (7): _agent_token_from_websocket(), agent_websocket_endpoint(), _claim_pushed_job(), Persistent WebSocket for probe → manager push communication.      Authentication, Read an agent bearer token exclusively from the non-logged auth header., Persistent WebSocket for probe → manager push communication.      Query params:, Validate eligibility and atomically claim a WebSocket job offer.

### Community 196 - "Community 196"
Cohesion: 0.29
Nodes (1): TestIngestFile

### Community 197 - "Community 197"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 198 - "Community 198"
Cohesion: 0.29
Nodes (1): TestValidateModule

### Community 199 - "Community 199"
Cohesion: 0.29
Nodes (1): TestValidateScope

### Community 200 - "Community 200"
Cohesion: 0.29
Nodes (1): TestMergeExclusions

### Community 201 - "Community 201"
Cohesion: 0.29
Nodes (5): Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., TestRunnerSubmission

### Community 203 - "Community 203"
Cohesion: 0.47
Nodes (4): create_access_token(), create_refresh_token(), _now(), Returns (token, jti) — jti is stored in Redis for revocation.

### Community 204 - "Community 204"
Cohesion: 0.33
Nodes (3): Apply constraints + indexes (idempotent)., Run a Cypher statement and return records as dicts. [] if not connected., Run a parametrised write with UNWIND batching for bulk node/edge loads.

### Community 205 - "Community 205"
Cohesion: 0.33
Nodes (4): _deterministic_layout(), GraphVisualizer, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag

### Community 206 - "Community 206"
Cohesion: 0.33
Nodes (3): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect()

### Community 207 - "Community 207"
Cohesion: 0.33
Nodes (1): TestASREPRoastChecker

### Community 208 - "Community 208"
Cohesion: 0.33
Nodes (1): TestNTLMRelayChecker

### Community 209 - "Community 209"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 210 - "Community 210"
Cohesion: 0.33
Nodes (1): TestCvss

### Community 211 - "Community 211"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 212 - "Community 212"
Cohesion: 0.60
Nodes (5): Unit tests for the dashboard list endpoints (jobs + assets)., _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user()

### Community 213 - "Community 213"
Cohesion: 0.33
Nodes (4): Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., TestTaskRunnerWithEncryptedScope

### Community 214 - "Community 214"
Cohesion: 0.33
Nodes (2): Phase 1: combined scope validation (validate + excludes)., TestScopeValidationPipeline

### Community 215 - "Community 215"
Cohesion: 0.33
Nodes (2): Phase 2: WebSocket message parsing., TestWebSocketMessageProtocol

### Community 216 - "Community 216"
Cohesion: 0.33
Nodes (4): Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup., TestStartupGauntlet

### Community 217 - "Community 217"
Cohesion: 0.33
Nodes (1): TestClamp

### Community 218 - "Community 218"
Cohesion: 0.33
Nodes (1): TestEngagementModes

### Community 219 - "Community 219"
Cohesion: 0.33
Nodes (1): TestFetchEngagementScope

### Community 220 - "Community 220"
Cohesion: 0.33
Nodes (3): diff_assets(), report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d, re-scan mode's delta report: what changed between two engagements.

### Community 221 - "Community 221"
Cohesion: 0.40
Nodes (3): Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name

### Community 222 - "Community 222"
Cohesion: 0.70
Nodes (4): create_findings_from_probe_result(), _find_open_duplicate(), _map_severity(), _resolve_asset()

### Community 223 - "Community 223"
Cohesion: 0.40
Nodes (2): Callback, scanListeners

### Community 224 - "Community 224"
Cohesion: 0.40
Nodes (4): nativeTlsInfo(), TlsInfoResult, WEAK_PROTOCOLS, WEAK_SIGNATURES

### Community 225 - "Community 225"
Cohesion: 0.40
Nodes (1): TestGetAgentJobs

### Community 226 - "Community 226"
Cohesion: 0.40
Nodes (1): TestEDRParsing

### Community 228 - "Community 228"
Cohesion: 0.40
Nodes (3): Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine., TestTransportWithIdentity

### Community 229 - "Community 229"
Cohesion: 0.40
Nodes (1): TestEngineSummary

### Community 230 - "Community 230"
Cohesion: 0.40
Nodes (1): TestGate2

### Community 231 - "Community 231"
Cohesion: 0.40
Nodes (1): TestLooksLikeHttp

### Community 232 - "Community 232"
Cohesion: 0.40
Nodes (1): TestLooksLikeTls

### Community 233 - "Community 233"
Cohesion: 0.40
Nodes (1): TestResolveScanType

### Community 234 - "Community 234"
Cohesion: 0.40
Nodes (1): TestTargets

### Community 235 - "Community 235"
Cohesion: 0.40
Nodes (1): TestWebSocket

### Community 236 - "Community 236"
Cohesion: 0.40
Nodes (1): Cross-validates the pure-Python Debian version comparator against the real `dpkg

### Community 237 - "Community 237"
Cohesion: 0.70
Nodes (4): _b64(), issue(), keygen(), main()

### Community 238 - "Community 238"
Cohesion: 0.50
Nodes (3): True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls.

### Community 239 - "Community 239"
Cohesion: 0.50
Nodes (3): Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce

### Community 240 - "Community 240"
Cohesion: 0.50
Nodes (3): Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons

### Community 241 - "Community 241"
Cohesion: 0.50
Nodes (3): Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used

### Community 242 - "Community 242"
Cohesion: 0.50
Nodes (3): Return the WebSocket connection URL with auth token.          The token is passe, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica

### Community 243 - "Community 243"
Cohesion: 0.50
Nodes (3): Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns

### Community 245 - "Community 245"
Cohesion: 0.50
Nodes (3): format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru

### Community 246 - "Community 246"
Cohesion: 0.67
Nodes (1): _ConnectSweep

### Community 247 - "Community 247"
Cohesion: 0.50
Nodes (1): TestTenantWebSocketSelection

### Community 249 - "Community 249"
Cohesion: 0.50
Nodes (1): TestGate3

### Community 250 - "Community 250"
Cohesion: 0.50
Nodes (1): TestGate4

### Community 251 - "Community 251"
Cohesion: 0.50
Nodes (1): TestRouteBranches

### Community 252 - "Community 252"
Cohesion: 0.50
Nodes (1): TestScanResult

### Community 253 - "Community 253"
Cohesion: 0.50
Nodes (1): Product-boundary tests for the single-dashboard Manager API.

### Community 254 - "Community 254"
Cohesion: 0.50
Nodes (3): get_or_404(), Shared database helpers — single source of truth for patterns duplicated across, Fetch a row by primary key, optionally scoped to a tenant.     Raises 404 if mis

### Community 255 - "Community 255"
Cohesion: 0.50
Nodes (3): dedup_hash(), Shared hashing utilities — deduplication keys, fingerprinting., SHA-256 of (asset_id, cve_id, plugin_id) for finding deduplication.      Used by

### Community 256 - "Community 256"
Cohesion: 0.50
Nodes (1): Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19

### Community 257 - "Community 257"
Cohesion: 0.50
Nodes (1): Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202

### Community 258 - "Community 258"
Cohesion: 0.50
Nodes (1): Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R

### Community 259 - "Community 259"
Cohesion: 0.50
Nodes (1): Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000

### Community 260 - "Community 260"
Cohesion: 0.50
Nodes (1): Detection validation: attack_timeline, detection_configs, extend detection_resul

### Community 261 - "Community 261"
Cohesion: 0.50
Nodes (1): AI engine: llm_outputs table + reviewstatus enum  Revision ID: 0006 Revises: 000

### Community 262 - "Community 262"
Cohesion: 0.50
Nodes (1): P3: composite indexes for the hot aggregate + poll query paths.  The dashboard's

### Community 263 - "Community 263"
Cohesion: 0.50
Nodes (1): P3-#10: append-only scan_results table (raw facts).  Decouples the (large) raw f

### Community 264 - "Community 264"
Cohesion: 0.50
Nodes (1): Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises

### Community 265 - "Community 265"
Cohesion: 0.67
Nodes (3): approve_exploit(), _get_approval_or_404(), reject_exploit()

### Community 266 - "Community 266"
Cohesion: 0.67
Nodes (1): TestAgentWebSocketAuthentication

### Community 267 - "Community 267"
Cohesion: 0.67
Nodes (1): TestAssetMergeCredentialed

### Community 268 - "Community 268"
Cohesion: 0.67
Nodes (1): TestAssetMergeHostDiscovery

### Community 269 - "Community 269"
Cohesion: 0.67
Nodes (1): TestAssetMergePortScan

### Community 270 - "Community 270"
Cohesion: 0.67
Nodes (1): TestAssetOpenPortsForDeepScan

### Community 271 - "Community 271"
Cohesion: 0.67
Nodes (2): paginate_query(), Returns (items, total). Applies OFFSET/LIMIT to `query`.

### Community 272 - "Community 272"
Cohesion: 0.67
Nodes (2): Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs.

### Community 273 - "Community 273"
Cohesion: 0.67
Nodes (2): Check if a specific agent is connected., Check if a specific agent is connected.

### Community 274 - "Community 274"
Cohesion: 0.67
Nodes (2): Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy).

### Community 275 - "Community 275"
Cohesion: 0.67
Nodes (2): Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job).

### Community 276 - "Community 276"
Cohesion: 0.67
Nodes (2): Record a heartbeat from an agent., Record a heartbeat from an agent.

### Community 277 - "Community 277"
Cohesion: 0.67
Nodes (2): Register an agent's WebSocket connection.          If the agent already has a co, Register an agent's WebSocket connection.          If the agent already has a co

### Community 278 - "Community 278"
Cohesion: 1.00
Nodes (1): TestAssetMergePassiveCollect

### Community 279 - "Community 279"
Cohesion: 1.00
Nodes (1): TestAssetMergeServiceBanner

### Community 280 - "Community 280"
Cohesion: 1.00
Nodes (1): TestAssetMergeSmbScan

### Community 281 - "Community 281"
Cohesion: 1.00
Nodes (1): TestAssetMergeTlsScan

### Community 282 - "Community 282"
Cohesion: 1.00
Nodes (1): TestAssetMergeUnknownScanner

### Community 283 - "Community 283"
Cohesion: 1.00
Nodes (1): TestAssetMergeWebScan

### Community 284 - "Community 284"
Cohesion: 1.00
Nodes (1): Fast port discovery with naabu. Feeds port list to Nmap.

### Community 285 - "Community 285"
Cohesion: 1.00
Nodes (1): Nmap service enumeration. Accepts port list from Naabu.

### Community 286 - "Community 286"
Cohesion: 1.00
Nodes (1): Nuclei vulnerability scan — production-ready.

### Community 287 - "Community 287"
Cohesion: 1.00
Nodes (1): Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.

### Community 288 - "Community 288"
Cohesion: 1.00
Nodes (1): NetExec SMB validation: signing, null sessions, SMBv1.

### Community 289 - "Community 289"
Cohesion: 1.00
Nodes (1): testssl.sh TLS/SSL analysis.

### Community 290 - "Community 290"
Cohesion: 1.00
Nodes (1): Extract HTTP/HTTPS URLs from nmap XML output.

### Community 291 - "Community 291"
Cohesion: 1.00
Nodes (1): EyeWitness screenshot evidence collection.

### Community 292 - "Community 292"
Cohesion: 1.00
Nodes (1): Safe lateral movement checks — no actual exploitation.

### Community 293 - "Community 293"
Cohesion: 1.00
Nodes (1): Cloud infrastructure scan (AWS/Azure/GCP).

### Community 294 - "Community 294"
Cohesion: 1.00
Nodes (1): Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.

### Community 295 - "Community 295"
Cohesion: 1.00
Nodes (1): Read a KV-v2 secret from Vault.

### Community 296 - "Community 296"
Cohesion: 1.00
Nodes (1): Verify the Python probe can open what the TypeScript manager sealed (T14 interop

### Community 297 - "Community 297"
Cohesion: 1.00
Nodes (1): Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO

### Community 298 - "Community 298"
Cohesion: 1.00
Nodes (1): Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).

### Community 299 - "Community 299"
Cohesion: 1.00
Nodes (1): End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.

### Community 300 - "Community 300"
Cohesion: 1.00
Nodes (1): Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 301 - "Community 301"
Cohesion: 1.00
Nodes (1): ThreadingHTTPServer

## Knowledge Gaps
- **967 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+962 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 81`** (1 nodes): `TestResultSpool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 116`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 126`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 135`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 137`** (2 nodes): `Tests that use the real engine but with no-op callbacks.`, `TestRunnerHeadless`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 140`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 141`** (1 nodes): `TestAgentJobCompatibility`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 142`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 143`** (1 nodes): `TestNucleiExploitRunner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 144`** (1 nodes): `TestValidatePayload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 145`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (1 nodes): `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 149`** (1 nodes): `ExploitOrchestrator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 156`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 159`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 160`** (2 nodes): `Each encryption uses a fresh ephemeral key, so blobs are different.`, `TestEncryptDecryptRoundtrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 169`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 175`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 176`** (1 nodes): `WindowsCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 178`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 179`** (1 nodes): `TestGraphVisualizer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 180`** (1 nodes): `TestMetasploitRPCClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 181`** (1 nodes): `TestRequiresApproval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 185`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 186`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 196`** (1 nodes): `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 197`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 198`** (1 nodes): `TestValidateModule`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 199`** (1 nodes): `TestValidateScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 200`** (1 nodes): `TestMergeExclusions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (1 nodes): `TestASREPRoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (1 nodes): `TestNTLMRelayChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 210`** (1 nodes): `TestCvss`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 211`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (2 nodes): `Phase 1: combined scope validation (validate + excludes).`, `TestScopeValidationPipeline`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (2 nodes): `Phase 2: WebSocket message parsing.`, `TestWebSocketMessageProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (1 nodes): `TestClamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (1 nodes): `TestEngagementModes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (1 nodes): `TestFetchEngagementScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (2 nodes): `Callback`, `scanListeners`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (1 nodes): `TestGetAgentJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (1 nodes): `TestEDRParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (1 nodes): `TestEngineSummary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (1 nodes): `TestGate2`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (1 nodes): `TestLooksLikeHttp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (1 nodes): `TestLooksLikeTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 233`** (1 nodes): `TestResolveScanType`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (1 nodes): `TestTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (1 nodes): `TestWebSocket`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (1 nodes): `Cross-validates the pure-Python Debian version comparator against the real `dpkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (1 nodes): `_ConnectSweep`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (1 nodes): `TestTenantWebSocketSelection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (1 nodes): `TestGate3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (1 nodes): `TestGate4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 251`** (1 nodes): `TestRouteBranches`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (1 nodes): `TestScanResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (1 nodes): `Product-boundary tests for the single-dashboard Manager API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (1 nodes): `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (1 nodes): `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (1 nodes): `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 259`** (1 nodes): `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (1 nodes): `Detection validation: attack_timeline, detection_configs, extend detection_resul`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (1 nodes): `AI engine: llm_outputs table + reviewstatus enum  Revision ID: 0006 Revises: 000`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (1 nodes): `P3: composite indexes for the hot aggregate + poll query paths.  The dashboard's`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (1 nodes): `P3-#10: append-only scan_results table (raw facts).  Decouples the (large) raw f`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (1 nodes): `Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (1 nodes): `TestAgentWebSocketAuthentication`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (1 nodes): `TestAssetMergeCredentialed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (1 nodes): `TestAssetMergeHostDiscovery`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (1 nodes): `TestAssetMergePortScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 270`** (1 nodes): `TestAssetOpenPortsForDeepScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (2 nodes): `paginate_query()`, `Returns (items, total). Applies OFFSET/LIMIT to `query`.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 272`** (2 nodes): `Return a snapshot of all connected agent IDs.`, `Return a snapshot of all connected agent IDs.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 273`** (2 nodes): `Check if a specific agent is connected.`, `Check if a specific agent is connected.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (2 nodes): `Check if a specific agent is online (connected + not busy).`, `Check if a specific agent is online (connected + not busy).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (2 nodes): `Return agent IDs whose status is 'online' (idle, ready for job).`, `Return agent IDs whose status is 'online' (idle, ready for job).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (2 nodes): `Record a heartbeat from an agent.`, `Record a heartbeat from an agent.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (2 nodes): `Register an agent's WebSocket connection.          If the agent already has a co`, `Register an agent's WebSocket connection.          If the agent already has a co`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 278`** (1 nodes): `TestAssetMergePassiveCollect`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (1 nodes): `TestAssetMergeServiceBanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (1 nodes): `TestAssetMergeSmbScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (1 nodes): `TestAssetMergeTlsScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (1 nodes): `TestAssetMergeUnknownScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (1 nodes): `TestAssetMergeWebScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (1 nodes): `Fast port discovery with naabu. Feeds port list to Nmap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 285`** (1 nodes): `Nmap service enumeration. Accepts port list from Naabu.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 286`** (1 nodes): `Nuclei vulnerability scan — production-ready.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 287`** (1 nodes): `Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 288`** (1 nodes): `NetExec SMB validation: signing, null sessions, SMBv1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 289`** (1 nodes): `testssl.sh TLS/SSL analysis.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 290`** (1 nodes): `Extract HTTP/HTTPS URLs from nmap XML output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 291`** (1 nodes): `EyeWitness screenshot evidence collection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 292`** (1 nodes): `Safe lateral movement checks — no actual exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (1 nodes): `Cloud infrastructure scan (AWS/Azure/GCP).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 294`** (1 nodes): `Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 295`** (1 nodes): `Read a KV-v2 secret from Vault.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 296`** (1 nodes): `Verify the Python probe can open what the TypeScript manager sealed (T14 interop`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 297`** (1 nodes): `Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 298`** (1 nodes): `Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 299`** (1 nodes): `End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 300`** (1 nodes): `Deterministic stand-ins emitting realistic output for 127.0.0.1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 301`** (1 nodes): `ThreadingHTTPServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 67` to `Community 66`, `Community 99`, `Community 75`, `Community 3`, `Community 22`, `Community 68`, `Community 119`, `Community 8`, `Community 1`, `Community 7`, `Community 5`, `Community 134`, `Community 140`, `Community 207`, `Community 178`, `Community 208`, `Community 36`, `Community 124`, `Community 180`, `Community 143`, `Community 181`, `Community 198`, `Community 144`, `Community 199`, `Community 0`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Finding` connect `Community 1` to `Community 96`, `Community 188`, `Community 8`, `Community 149`, `Community 15`, `Community 97`, `Community 0`, `Community 78`, `Community 67`, `Community 5`, `Community 7`, `Community 2`, `Community 165`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `FindingStatus` connect `Community 5` to `Community 22`, `Community 8`, `Community 1`, `Community 7`, `Community 165`, `Community 66`, `Community 134`, `Community 140`, `Community 207`, `Community 75`, `Community 119`, `Community 178`, `Community 208`, `Community 36`, `Community 124`, `Community 180`, `Community 143`, `Community 181`, `Community 198`, `Community 144`, `Community 199`, `Community 0`, `Community 67`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 173 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 173 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R` to the rest of the system?**
  _967 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.029853479853479855 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09137737961926092 - nodes in this community are weakly interconnected._