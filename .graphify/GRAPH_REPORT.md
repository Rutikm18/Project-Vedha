# Graph Report - .  (2026-07-22)

## Corpus Check
- Large corpus: 521 files · ~374,807 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 4137 nodes · 8774 edges · 243 communities detected
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 2239 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 2239 · contains: 2019 · calls: 1403 · method: 1111 · rationale_for: 609 · MODIFIES: 489 · imports: 395 · imports_from: 348 · inherits: 141 · ON_BRANCH: 13 · PARENT_OF: 7


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 521 · Candidates: 1042
- Excluded: 0 untracked · 63553 ignored · 2 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `2885afa`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `FindingSeverity` - 129 edges
2. `FindingStatus` - 96 edges
3. `Finding` - 88 edges
4. `Engagement` - 78 edges
5. `SourceConfidence` - 72 edges
6. `Asset` - 71 edges
7. `Fact` - 68 edges
8. `CPECandidate` - 67 edges
9. `Finding` - 65 edges
10. `ScanJob` - 60 edges

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
Nodes (26): agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit, HallucinationGuard — post-generation validation of LLM report text against the g, 298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence, Verify the Python probe can open what the TypeScript manager sealed (T14 interop, eslintConfig, __dirname, frontendRoot, nextConfig (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (42): ServiceFingerprint, AssetCriticality, OrderedDict, FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment., Background task: run nuclei, persist findings, trigger enrichment. (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (33): apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl(), Session, SESSION_DIR (+25 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (32): aggregate(), ConsistencyReport, FindingConsistency, format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, run_findings: one list of Findings per run (N runs). Aggregated by     the deter, The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen (+24 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (56): AgentUnavailableError, agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Raised when the Anthropic SDK or API key is not configured., Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Convert a probe's self-assessed `findings` list into persisted Finding rows., GraphBuilder — turns engagement assets/services/findings into an attack graph. (+48 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (49): AuthContext, Handler, withAuth(), generateOtp(), OtpEntry, otpStore, OtpVerifyResult, SessionPayload (+41 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (40): HallucinationGuard, Run all relevant checks and return a combined verdict:         ``{valid, issues,, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide., _collect_cves_scores(), _enum(), _finding_scores() (+32 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (55): A, ask(), askSecret(), banner(), buildInteractiveCommand(), choose(), chooseNextPhase(), confirm() (+47 more)

### Community 8 - "Community 8"
Cohesion: 0.07
Nodes (30): buildScanCommand(), PROFILE_TOOLS, ModuleCategory, ModuleInput, ModuleOutput, modulesForPorts(), ScanModule, bySeverityCount() (+22 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (33): DEMO_ASSET, DEMO_ENGAGEMENT, DEMO_FINDING, aiReportStore, AssetInput, chat(), CRITICALITY_SCORE, DESTRUCTIVE_PATTERNS (+25 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (46): bin(), binName(), collectProcess(), hasBinary(), hasSystemBinary(), httpBannerGrab(), HttpxLine, isWindows() (+38 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (43): all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), normalize(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web() (+35 more)

### Community 12 - "Community 12"
Cohesion: 0.07
Nodes (8): _finding(), TestAggregate, TestClassifyTier, TestComputePriority, TestDedupFindings, TestFindingConsistency, TestSuppressNegated, TestVerify

### Community 13 - "Community 13"
Cohesion: 0.05
Nodes (25): JobResult, task_runner.py — orchestrates the full lifecycle of a single scan job.  Given a, Submit the result, with spool-and-retry if available., Structured result from running one scan job., Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Args:             http_get:       Callback for authenticated GET (from Transport, Execute a complete scan job lifecycle.          Args:             job: Job dict, TaskRunner (+17 more)

### Community 14 - "Community 14"
Cohesion: 0.07
Nodes (32): Agent, AGENT_STATUS, AgentStatus, PATH_STATUS, SEV_LABEL, Exposure, ProtocolRiskCard(), useExposure() (+24 more)

### Community 15 - "Community 15"
Cohesion: 0.08
Nodes (29): Evidence, createFinding(), DEFAULT_DATA_PATH, deleteFinding(), ensureDir(), FindingSeverity, getAllFindings(), getFindingById() (+21 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (41): Exception, ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is, Raises SafetyViolationError if module or payload is not permitted., Raises OutOfScopeError if target_ip not in engagement scope., Full exploit execution pipeline with safety, scope, blast radius,         audit, Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo, Count running exploit jobs for this engagement; raise if over limit., Creates and returns an ExploitApprovalRequest if approval is needed. (+33 more)

### Community 17 - "Community 17"
Cohesion: 0.07
Nodes (10): _asset(), TestAssetMergePortScan, TestAssetNeedsRecheckLive, TestAssetOpenPortsForDeepScan, TestGate2, TestGate3, TestGate4, TestGate5 (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (25): AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient, propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Test double — a fixed lookup table, no network. Used to validate the     surroun (+17 more)

### Community 19 - "Community 19"
Cohesion: 0.08
Nodes (34): countBySeverity(), NucleiMatch, nucleiMatchToFinding(), NucleiRaw, NucleiRawLine, nucleiSeverityToSeverity(), parseNucleiLine(), broadcastToScan() (+26 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (36): Agent, AgentStatus, ScanJobStatus, ScanJobType, ScanJob, ScanResult, ADAssessRequest, Neo4jConfig (+28 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (21): ADConnectionError, DependencyMissingError, Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., ADComputer, ADGroup, ADUser, _as_list() (+13 more)

### Community 22 - "Community 22"
Cohesion: 0.16
Nodes (28): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+20 more)

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (10): _candidate(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db(), TestCPECandidateCpe23, TestEnrichFinding, TestEpssDb, TestKevDb (+2 more)

### Community 24 - "Community 24"
Cohesion: 0.09
Nodes (9): Fit an XGBoost regressor on historical findings. ``historical_findings_df``, VulnPrioritizer, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard, TestLLMReportGenerator (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.06
Nodes (19): Agent, criticalChain, defaultAgents, Finding, findings, graphStats, initialMessage, Message (+11 more)

### Community 26 - "Community 26"
Cohesion: 0.07
Nodes (19): ADJ, ATTACK_PATHS, AttackPath, BlastRadiusResult, buildAttackPaths(), Chokepoint, CHOKEPOINTS, edgesForPath() (+11 more)

### Community 27 - "Community 27"
Cohesion: 0.09
Nodes (31): config, isPublic(), middleware(), PUBLIC_PATHS, PUBLIC_PREFIXES, Client, ClientJiraConfig, ClientNotifyConfig (+23 more)

### Community 28 - "Community 28"
Cohesion: 0.08
Nodes (14): Unit tests for the agent/probe protocol changes:   * agent polling is restricted, Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., TestAccessTokenExpiry, TestAgentExecutableTypes, TestEnqueueAgentJob (+6 more)

### Community 29 - "Community 29"
Cohesion: 0.12
Nodes (30): buildToolsCommand(), C, ln(), showSpinner(), downloadFile(), extract(), getInstalledRecord(), installAll() (+22 more)

### Community 30 - "Community 30"
Cohesion: 0.10
Nodes (20): ADError, build_ad_finding(), Shared building blocks for the Active Directory assessment module.  Every AD che, Assemble a Finding-compatible dict.      All findings carry — as required by the, Base class for Active Directory assessment errors., severity_from_str(), KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline (+12 more)

### Community 31 - "Community 31"
Cohesion: 0.07
Nodes (22): ComplianceRef, COVERAGE_COLOR, DetectionCoverage, ExploitMaturity, Finding, FindingDetail(), FindingsPage(), FindingStatus (+14 more)

### Community 32 - "Community 32"
Cohesion: 0.08
Nodes (27): AgentDeps, AgentOpts, execute_ad_enum(), execute_cloud_scan(), execute_discovery(), execute_lateral_movement(), execute_naabu(), firstStr() (+19 more)

### Community 33 - "Community 33"
Cohesion: 0.07
Nodes (19): bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity(), pubkey_to_bytes(), scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.  T (+11 more)

### Community 34 - "Community 34"
Cohesion: 0.08
Nodes (15): PageShell(), ToastContext, useToast(), AssetRow, EDIT_STATUSES, Engagement, EngagementDetailPage(), statusColor() (+7 more)

### Community 35 - "Community 35"
Cohesion: 0.08
Nodes (15): ATTACK_TIMELINE, AttackAction, correlationRuns, CoverageStats, DetectionOutcome, DetectionResult, detectionStore, EDR_DETECTIONS (+7 more)

### Community 36 - "Community 36"
Cohesion: 0.10
Nodes (16): Engagement, Finding, LiveOverview(), Sev, ApiError, clearAuth(), errorMessage(), fetchJson() (+8 more)

### Community 37 - "Community 37"
Cohesion: 0.11
Nodes (9): EvidenceTier, IntEnum, _fact(), TestAsset, TestCorrelateSmbPatch, TestNormalize, TestNormalizeBanner, TestNormalizeDb (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.11
Nodes (22): BaseModel, ActivityItem, Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant, recent_activity(), LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated, PersonalAccessTokenOut (+14 more)

### Community 39 - "Community 39"
Cohesion: 0.14
Nodes (11): ServiceIdentifier — banner + port → structured service fingerprint. Handles: HTT, ServiceIdentifier, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner, Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr, NmapXMLParser, ParsedHost (+3 more)

### Community 40 - "Community 40"
Cohesion: 0.10
Nodes (22): Agent, AgentCapability, AGENTS, agentsStore, AgentStatus, ensureDataDir(), FIELD_AGENTS_FILE, FieldAgent (+14 more)

### Community 41 - "Community 41"
Cohesion: 0.08
Nodes (10): True if we have both an agent_id and a token for API calls., Register the probe with the manager.          Args:             name: Probe name, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Fetch the engagement's authoritative scope.          Returns the response dict i, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Return the WebSocket connection URL with auth token.          The token is passe, True if the WebSocket connection is active. (+2 more)

### Community 42 - "Community 42"
Cohesion: 0.13
Nodes (11): CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender, _parse_dt(), EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender, Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi, SentinelOne via the REST ``/web/api/v2.1/threats`` endpoint.     config: {base_u (+3 more)

### Community 43 - "Community 43"
Cohesion: 0.13
Nodes (11): ElasticSIEM, _parse_dt(), SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi, Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_, Abstract SIEM connector., Splunk via the REST search endpoint (``/services/search/jobs/export``) with an, SentinelSIEM (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.13
Nodes (13): MetasploitRPCClient, MetasploitRPCError, MetasploitRPCClient — async client for msfrpcd.  Protocol: MessagePack RPC over, Returns {status, output, uuid}., Returns True if job was successfully killed., Poll until job completes or max_wait exceeded., Authenticated RPC call — prepends token., Async Metasploit RPC client using msgpack-over-HTTPS. (+5 more)

### Community 45 - "Community 45"
Cohesion: 0.12
Nodes (5): _scan_result(), TestAssetMergeCredentialed, TestAssetMergeHostDiscovery, TestClassifyCertainty, TestWorkflowCache

### Community 46 - "Community 46"
Cohesion: 0.19
Nodes (16): AttackAction, _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO, _host_matches(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale, Normalise naive datetimes to UTC so comparisons never raise. (+8 more)

### Community 47 - "Community 47"
Cohesion: 0.11
Nodes (7): Asset, _parse_ts(), PortFact, asset.py — per-host fact model the workflow engine reasons about.  This is an OR, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Dispatch a real ScanResult into the right sub-structure, keyed         on result, _utcnow()

### Community 48 - "Community 48"
Cohesion: 0.14
Nodes (19): GET, POST, fail(), GET, PUT(), DETECTION_TO_UI, ENG_STATUS_TO_API, ENG_STATUS_TO_UI (+11 more)

### Community 49 - "Community 49"
Cohesion: 0.09
Nodes (13): apiFetch(), Cat, CATS, Engagement, getToken(), Intensity, JobStatus, PHASES (+5 more)

### Community 50 - "Community 50"
Cohesion: 0.16
Nodes (21): A, banner(), findingDetail(), findingLine(), findingsTable(), hostLine(), info(), LINE (+13 more)

### Community 51 - "Community 51"
Cohesion: 0.13
Nodes (11): _make_http_mock(), Unit tests for VulnEnrichmentService — all external HTTP calls mocked., Create a mock httpx.AsyncClient that returns different responses per URL., test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full(), test_fetch_epss_success() (+3 more)

### Community 52 - "Community 52"
Cohesion: 0.18
Nodes (12): ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM, Read pKICertificateTemplate objects from the Configuration NC. (+4 more)

### Community 53 - "Community 53"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 54 - "Community 54"
Cohesion: 0.10
Nodes (10): Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG, TestAssetMergePassiveCollect, TestAssetMergeServiceBanner, TestAssetMergeSmbScan, TestAssetMergeTlsScan, TestAssetMergeUnknownScanner, TestAssetMergeWebScan, TestCacheEntry (+2 more)

### Community 55 - "Community 55"
Cohesion: 0.10
Nodes (4): Tests for agent/result_spool.py, ResultSpool with tiny retry delay for fast tests., spool(), TestResultSpool

### Community 56 - "Community 56"
Cohesion: 0.12
Nodes (13): metadata, PageShellProps, QueryProvider(), Theme, ThemeContext, ThemeContextValue, ThemeProvider(), useTheme() (+5 more)

### Community 57 - "Community 57"
Cohesion: 0.15
Nodes (10): b64e(), _make_handler(), ManagerState, _QuietServer, Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO, Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64)., _self_signed(), spki_pin() (+2 more)

### Community 58 - "Community 58"
Cohesion: 0.15
Nodes (10): PathAnalyzer, _priority(), PathAnalyzer — attack-path discovery, scoring, chokepoint and blast-radius analy, Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for, Assets that appear in more than ``threshold`` (default 50%) of all paths —, Assets reachable (and thus at risk) if ``compromised_asset_id`` is owned., Best (easiest) exploitable finding on an asset: {cvss, weight, finding}. (+2 more)

### Community 59 - "Community 59"
Cohesion: 0.17
Nodes (18): OutboxEvent, _claim_batch(), enqueue(), Event, _handle_facts_ready(), main(), _mark_done(), _mark_retry_or_dead() (+10 more)

### Community 60 - "Community 60"
Cohesion: 0.18
Nodes (2): Unit tests for ServiceIdentifier., TestServiceIdentifier

### Community 61 - "Community 61"
Cohesion: 0.10
Nodes (10): AgentConnectionManager, Record a heartbeat from an agent., Check if a specific agent is connected., Check if a specific agent is online (connected + not busy)., Return a snapshot of all connected agent IDs., Return agent IDs whose status is 'online' (idle, ready for job)., Return 'online', 'busy', or 'offline'., Return agent_ids whose last heartbeat is older than `seconds`.          These ag (+2 more)

### Community 62 - "Community 62"
Cohesion: 0.11
Nodes (8): BloodHoundCollector, BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., Run bloodhound-python and return the list of produced JSON file paths.         R, TestBuildADFinding

### Community 63 - "Community 63"
Cohesion: 0.12
Nodes (11): check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, Raised when the binary is running on an unauthorized machine., Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B, RuntimeError (+3 more)

### Community 64 - "Community 64"
Cohesion: 0.13
Nodes (10): result_spool.py — local result persistence with upload retry.  When the probe co, Re-attempt upload of all previously spooled results.          Called once at pro, Number of pending (unsubmitted) results in the spool., Persists scan results locally and retries failed uploads., Atomically write a result payload to the spool directory.          Returns the s, Check if a spooled result exists for this job., Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result. (+2 more)

### Community 65 - "Community 65"
Cohesion: 0.13
Nodes (10): get_settings(), Settings, get_read_db(), Read-only session (no commit) routed to the replica when configured.     For SEL, BaseSettings, agent_websocket_endpoint(), agent_ws.py — WebSocket endpoint for probe push connectivity.  Probes connect vi, Persistent WebSocket for probe → manager push communication.      Query params: (+2 more)

### Community 66 - "Community 66"
Cohesion: 0.16
Nodes (18): _char_order(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), has_ambiguous_epoch(), version_compare.py — per-scheme version comparators.  Spec calls this "the highe (+10 more)

### Community 67 - "Community 67"
Cohesion: 0.12
Nodes (9): _content_hash(), _default_products(), load_snapshot(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Derives the synced product list from cpe_normalizer.py's tables —     the single, Stable hash of the snapshot's actual vulnerability content — recorded     in eve, SnapshotMeta, TestDeceptionScore (+1 more)

### Community 68 - "Community 68"
Cohesion: 0.19
Nodes (18): Fact, Job, assemble(), assembleError(), buildHostsMap(), clamp(), clampInt(), countOpenPorts() (+10 more)

### Community 69 - "Community 69"
Cohesion: 0.15
Nodes (14): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), _parse_masscan_json(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them., Excluded networks -> masscan --exclude specs, so they get ZERO packets. (+6 more)

### Community 70 - "Community 70"
Cohesion: 0.15
Nodes (10): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+2 more)

### Community 71 - "Community 71"
Cohesion: 0.16
Nodes (8): build_ssl_context(), check_tool_availability(), JobType, Fetches credentials from HashiCorp Vault at runtime. Never caches to disk., Read a KV-v2 secret from Vault., ScanJob, ScanningAgent, VaultCredentialFetcher

### Community 72 - "Community 72"
Cohesion: 0.13
Nodes (11): close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, FastAPI dependency that enforces role-based access.      Usage:         @router., require_role(), list_recommendations(), _rec_dict() (+3 more)

### Community 73 - "Community 73"
Cohesion: 0.15
Nodes (12): correlate_smb_patch(), dedup_findings(), _product_from_cpe(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Suppress a suspected/potential (inferred-source) finding when the     SAME host (+4 more)

### Community 74 - "Community 74"
Cohesion: 0.18
Nodes (16): match_candidate(), matcher.py — does this CPE candidate's version fall inside a vulnerable range, p, dpkg_compare, but None instead of a misleading answer when one side     has an e, Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A, All Findings this single CPE candidate produces against the snapshot.     Empty, _safe_compare(), _version_in_ranges(), FindingState (+8 more)

### Community 75 - "Community 75"
Cohesion: 0.15
Nodes (15): resetCounters(), groupNaabuResults(), NaabuRaw, NaabuResult, parseNaabuLine(), extractScripts(), NmapHost, NmapScriptResult (+7 more)

### Community 76 - "Community 76"
Cohesion: 0.18
Nodes (13): bulk_import_assets(), _compute_overview(), create_engagement(), engagements_overview(), get_engagement_scope(), import_facts(), _overview_cache_key(), _parse_probe_file() (+5 more)

### Community 77 - "Community 77"
Cohesion: 0.13
Nodes (13): bracket_host(), expand_targets(), parse_ports(), scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h, Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535). (+5 more)

### Community 78 - "Community 78"
Cohesion: 0.19
Nodes (8): FakeReader, FakeWriter, _probe(), Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol (, _run(), TestMysqlxVsOracle, _tns_packet(), _xproto_frame()

### Community 79 - "Community 79"
Cohesion: 0.16
Nodes (11): ApiActivity, GET, 0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner UI, Exposure, GET, BackendCtx, Handler, withBackend() (+3 more)

### Community 80 - "Community 80"
Cohesion: 0.13
Nodes (7): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., TestASREPRoastChecker

### Community 81 - "Community 81"
Cohesion: 0.21
Nodes (5): AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()

### Community 82 - "Community 82"
Cohesion: 0.14
Nodes (8): buildDoctorCommand(), C, CheckResult, checkTool(), ln(), render(), symbol(), which()

### Community 83 - "Community 83"
Cohesion: 0.18
Nodes (15): addComment(), Case, CaseActivity, CaseComment, CaseSeverity, CaseStatus, createCase(), DATA_FILE (+7 more)

### Community 84 - "Community 84"
Cohesion: 0.21
Nodes (15): Finding, checkDB(), checkService(), checkTLS(), checkUDP(), checkWeb(), Correlate(), dedupAndRank() (+7 more)

### Community 85 - "Community 85"
Cohesion: 0.19
Nodes (2): _action(), TestDetectionCorrelator

### Community 86 - "Community 86"
Cohesion: 0.19
Nodes (7): BASE, backend(), BackendError, BackendOpts, BASE, bearerFrom(), safeJson()

### Community 87 - "Community 87"
Cohesion: 0.13
Nodes (9): ActivityItem, DashboardCharts(), Engagement, Finding, SEV, STATUS_STYLE, TimelinePoint, TOP_FINDINGS (+1 more)

### Community 88 - "Community 88"
Cohesion: 0.15
Nodes (8): NucleiExploitRunner, NucleiExploitRunner — CVE PoC validation using Nuclei templates.  Enforces templ, Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Parse nuclei JSONL output for a single CVE PoC result., Run Nuclei CVE PoC templates against a single target.     Every template is safe, Parse template YAML and validate it contains no write/delete/DoS actions., Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me, TestMetasploitIntegration

### Community 89 - "Community 89"
Cohesion: 0.28
Nodes (8): asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder, is_internet_exposed(), service_node_id(), _to_float()

### Community 90 - "Community 90"
Cohesion: 0.17
Nodes (11): _device_hint(), _is_readable(), _open_listener(), PassiveCollector, _printable_strings(), passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)., Listen-only discovery. No active probing. Reports in-scope hosts that     announ, Await readability on any listener without blocking the event loop. (+3 more)

### Community 91 - "Community 91"
Cohesion: 0.15
Nodes (8): BaseScanner, main_entrypoint(), RateLimiter, Simple async rate limiter: at most `rate` operations per second., Subclasses implement `scan_target(self, target)` (async), returning a list     o, One observation about one target. Pure fact, no interpretation., Run a scanner CLI's body with consistent, operator-friendly error handling., ScanResult

### Community 92 - "Community 92"
Cohesion: 0.18
Nodes (6): CacheEntry, classify_certainty(), cache.py — (host, port, scanner) -> CacheEntry, so deterministic facts are colle, True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, WorkflowCache

### Community 93 - "Community 93"
Cohesion: 0.17
Nodes (12): _gather_per_host(), _port_candidates(), workflow_engine.py — the async DAG executor. Loops through gates, checks precond, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs scanner.scan_target(host) across hosts concurrently; the     scanner's own, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Return TCP ports worth scanning for this profile and requested branch set. (+4 more)

### Community 94 - "Community 94"
Cohesion: 0.15
Nodes (15): Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket. (+7 more)

### Community 95 - "Community 95"
Cohesion: 0.17
Nodes (6): BaseScanner, DBScanner, _build_get(), _extract_sysdescr(), snmp_scanner.py — detect SNMP and read sysDescr via common community strings.  M, SNMPScanner

### Community 96 - "Community 96"
Cohesion: 0.19
Nodes (8): DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci, TestNeo4jClient

### Community 97 - "Community 97"
Cohesion: 0.13
Nodes (12): approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest, ExploitEvidence, ExploitJob, ExploitResult (+4 more)

### Community 98 - "Community 98"
Cohesion: 0.16
Nodes (6): CircuitBreaker, RetryConfig, backoff(), DialContext(), IsTransient(), Retry()

### Community 99 - "Community 99"
Cohesion: 0.13
Nodes (7): _fake_run_scan(), Integration tests — full probe lifecycles exercised through the public APIs of a, Phase 1: combined scope validation (validate + excludes)., Phase 1: result spool with upload retry., Return a minimal valid scan result (no real network I/O)., TestResultSpoolWithRetry, TestScopeValidationPipeline

### Community 100 - "Community 100"
Cohesion: 0.13
Nodes (3): Tests for agent/scope_validator.py, TestFetchEngagementScope, TestMergeExclusions

### Community 101 - "Community 101"
Cohesion: 0.24
Nodes (7): _check_anti_debug(), Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, say(), _startup_gauntlet()

### Community 102 - "Community 102"
Cohesion: 0.20
Nodes (12): _clamp(), _count_open_port_facts(), _error_result(), engine.py — adapt a manager scan job to scanner_module's workflow engine and ret, Count concrete open services, not generic host-liveness observations., Execute a scan and return the enriched result bundle.      Args:         scan_ty, Single factory for error result dicts — no copy-paste., Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def (+4 more)

### Community 103 - "Community 103"
Cohesion: 0.24
Nodes (12): _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError, license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Stable per-machine ID, derived from hw_bind's hardware fingerprint. (+4 more)

### Community 104 - "Community 104"
Cohesion: 0.15
Nodes (7): client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the exi, Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a     prox, FastAPI dependency factory. Keys the window by (scope, client-IP)., create_personal_access_token(), refresh()

### Community 105 - "Community 105"
Cohesion: 0.22
Nodes (13): client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId, PhaseRecommendation, planExploit() (+5 more)

### Community 106 - "Community 106"
Cohesion: 0.23
Nodes (13): DeclarativeBase, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., Append-only ledger of every attack action performed during an engagement.      W, Immutable, append-only audit trail for all exploit actions.     No TimestampMixi, Base, TimestampMixin, UUIDMixin, Per-engagement SIEM + EDR connection settings used by the detection     validati (+5 more)

### Community 107 - "Community 107"
Cohesion: 0.23
Nodes (13): _all_known_cve_ids(), main(), _query_osv(), update_snapshot.py — the ONLY module in this package that talks to the network., The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, EPSS scores for exactly the CVE IDs this detection run actually cares     about, Some macOS python.org installs ship expecting `Install Certificates.     command, All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n (+5 more)

### Community 108 - "Community 108"
Cohesion: 0.16
Nodes (7): AdversaError, AdversaErrorOpts, diagnoseSpawnError(), ErrorCode, Errors, VedhaError, VedhaErrorOpts

### Community 109 - "Community 109"
Cohesion: 0.20
Nodes (7): _clean(), _Collector, Make a per-host scanner instance share ONE rate limiter + semaphore with all, Make a raw banner safe and readable for the summary line.      Many services ans, _rollup(), _run_active(), _shared()

### Community 110 - "Community 110"
Cohesion: 0.21
Nodes (9): _get_cert_der(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None., _scan_tls_sync(), _sni(), TLSScanner (+1 more)

### Community 111 - "Community 111"
Cohesion: 0.20
Nodes (4): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect(), WindowsCollector

### Community 112 - "Community 112"
Cohesion: 0.18
Nodes (11): pct(), Sev, SEV_STYLE, SlaItem, SlaRowView(), SlaState, SlaStatus(), SlaSummary (+3 more)

### Community 113 - "Community 113"
Cohesion: 0.17
Nodes (6): _deterministic_layout(), GraphVisualizer, GraphVisualizer — serialise the attack graph into D3-compatible JSON for the fro, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag, TestGraphVisualizer

### Community 114 - "Community 114"
Cohesion: 0.36
Nodes (12): _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius(), _build_analyzer(), _critical_asset_ids(), _explain_hop(), get_attack_path() (+4 more)

### Community 115 - "Community 115"
Cohesion: 0.19
Nodes (5): Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, ScopeError, ScopeGuard

### Community 116 - "Community 116"
Cohesion: 0.29
Nodes (4): _engagement(), _finding(), Unit tests for the exploitation engine.  All external connections (Metasploit RP, TestExploitOrchestrator

### Community 117 - "Community 117"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 118 - "Community 118"
Cohesion: 0.15
Nodes (2): Unit tests for NmapXMLParser., TestNmapXMLParser

### Community 119 - "Community 119"
Cohesion: 0.26
Nodes (1): transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap

### Community 120 - "Community 120"
Cohesion: 0.23
Nodes (7): extract_features(), VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)., Build the model's feature vector from a Finding (+ optional Asset + extra     co, _to_float()

### Community 121 - "Community 121"
Cohesion: 0.18
Nodes (9): POST, ACTIVITY, Credential, Engagement, engagementsStore, EngagementStatus, FINDINGS_TIMELINE, now (+1 more)

### Community 122 - "Community 122"
Cohesion: 0.30
Nodes (11): create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, New raw-facts path: detect CVE findings from result['facts'] and persist     the, Background entry point (P1: keep detection OFF the probe-result request     path, (content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev, facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur (+3 more)

### Community 123 - "Community 123"
Cohesion: 0.18
Nodes (9): CheckOpts, groupResults(), NativePortResult, nativePortScan(), NativeScanOpts, PORT_NAMES, PortRange, resolvePorts() (+1 more)

### Community 124 - "Community 124"
Cohesion: 0.18
Nodes (10): NSE_VULN_MAP, NseScript, parseNmapXml(), POST(), SCAN_PROFILES, ScanHost, ScanPort, ScanResult (+2 more)

### Community 125 - "Community 125"
Cohesion: 0.21
Nodes (11): joinInts(), NmapAvailable(), parseNmapXML(), RunNmapVersion(), nmapAddr, nmapHost, nmapPort, NmapResult (+3 more)

### Community 126 - "Community 126"
Cohesion: 0.18
Nodes (2): udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, UDPScanner

### Community 127 - "Community 127"
Cohesion: 0.29
Nodes (3): _enum_with_entries(), _FakeEntry, TestLDAPEnumeratorParsing

### Community 128 - "Community 128"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 129 - "Community 129"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()

### Community 130 - "Community 130"
Cohesion: 0.18
Nodes (6): EMPTY_FORM, Engagement, EngagementsResponse, EngagementStatus, FormState, STEPS

### Community 131 - "Community 131"
Cohesion: 0.29
Nodes (1): ExploitOrchestrator

### Community 132 - "Community 132"
Cohesion: 0.22
Nodes (5): main(), _orchestrate(), # NOTE: credentialed collectors (ssh_collector, windows_collector) are run, service_banner.py — grab service banners and light version strings.  METHOD (col, ServiceBannerScanner

### Community 133 - "Community 133"
Cohesion: 0.33
Nodes (10): buildSNMPGetRequest(), dnsVersionQuery(), extractSNMPCommunity(), netbiosNameQuery(), ntpRequest(), ProbeAllSNMPCommunities(), ProbeUDP(), probeUDPPort() (+2 more)

### Community 134 - "Community 134"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 135 - "Community 135"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 136 - "Community 136"
Cohesion: 0.18
Nodes (1): TestNucleiExploitRunner

### Community 137 - "Community 137"
Cohesion: 0.18
Nodes (1): TestValidatePayload

### Community 138 - "Community 138"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 139 - "Community 139"
Cohesion: 0.18
Nodes (5): Tests for agent/transport.py, Create a Transport with a real state file path but no actual HTTP calls., TestFetchScope, TestHeartbeat, transport()

### Community 140 - "Community 140"
Cohesion: 0.22
Nodes (6): GraphWebSocketManager, High-level manager for graph-specific WebSocket operations., Broadcast graph data update to all subscribers., Broadcast a single node update., Broadcast layout change to all subscribers., Broadcast message to all connections in a room.

### Community 141 - "Community 141"
Cohesion: 0.20
Nodes (9): fetch_engagement_scope(), merge_exclusions(), scope_validator.py — defense-in-depth scope re-validation for the probe.  The pr, Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl, Fetch the engagement's authoritative scope from the manager.      Args:, Check targets against the authoritative scope CIDRs.      Returns (allowed, reje, Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)., targets_in_excludes() (+1 more)

### Community 142 - "Community 142"
Cohesion: 0.27
Nodes (4): RateLimiter, RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim

### Community 143 - "Community 143"
Cohesion: 0.20
Nodes (9): Safety constants, exceptions, and validators for the exploitation engine.  All s, Raises SafetyViolationError if payload is not on allowlist     or violates per-p, Raises SafetyViolationError if module is on the block list., Raises OutOfScopeError if target_ip is not in scope or is excluded., True if this target requires human manager approval before exploit runs., requires_approval(), validate_module(), validate_payload() (+1 more)

### Community 144 - "Community 144"
Cohesion: 0.20
Nodes (6): HttpProbeResult, NativeHttpOpts, nativeHttpProbe(), TECH_RULES, TechRule, WEB_PORT_PROTO

### Community 145 - "Community 145"
Cohesion: 0.40
Nodes (9): envFilePath(), findServiceLabel(), isDirWritable(), localScan(), main(), protoOr(), renderReport(), run() (+1 more)

### Community 146 - "Community 146"
Cohesion: 0.20
Nodes (1): db_scanner.py — fingerprint database services.  WHY: databases are everywhere on

### Community 147 - "Community 147"
Cohesion: 0.31
Nodes (8): expandBackrefs(), Fingerprint(), firstLine(), matchSignature(), sanitize(), sendProbe(), probe, signature

### Community 148 - "Community 148"
Cohesion: 0.27
Nodes (5): _netbios_session(), smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, _smb1_negotiate(), _smb2_negotiate(), SMBScanner

### Community 149 - "Community 149"
Cohesion: 0.22
Nodes (3): _NoRedirect, web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, WebScanner

### Community 150 - "Community 150"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 151 - "Community 151"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 152 - "Community 152"
Cohesion: 0.24
Nodes (7): gate_0_is_passive_profile(), gate_2_host_discovery(), gate_3_port_scan(), gate_5_branch_eligible(), gates.py — precondition functions deciding whether each stage of the workflow ru, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, Does `branch` apply to this host?       - Must be in this profile's allowed deep

### Community 153 - "Community 153"
Cohesion: 0.29
Nodes (9): assessment(), EngagementMode, modes.py — engagement mode configurations. Each mode is a thin config that tunes, Discovery + ports + banner only — no deep dives, no credentials., Full funnel, every branch the profile allows., Loads a prior engagement's cache; only facts older than     recheck_older_than g, re_scan(), service_specific() (+1 more)

### Community 154 - "Community 154"
Cohesion: 0.22
Nodes (9): _load_env(), _load_or_create_identity(), main(), _obtain_identity(), Load key=value lines from probe.env for dev convenience., Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64). (+1 more)

### Community 155 - "Community 155"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 156 - "Community 156"
Cohesion: 0.22
Nodes (1): TestUseCasesResolve

### Community 157 - "Community 157"
Cohesion: 0.22
Nodes (5): ConnectionManager, WebSocket manager for real-time graph updates, agent push, and live collaboratio, Manages WebSocket connections with room-based broadcasting., Accept connection and add to room., Get number of connected clients in a room.

### Community 158 - "Community 158"
Cohesion: 0.50
Nodes (7): env(), envBool(), envDuration(), envInt(), hostname(), Load(), loadFile()

### Community 159 - "Community 159"
Cohesion: 0.36
Nodes (4): SigmaRuleGenerator — produces a Sigma detection rule (YAML) for a MITRE techniqu, Return a Sigma rule (YAML string) for the technique, customised with the, SigmaRuleGenerator, _stable_rule_id()

### Community 160 - "Community 160"
Cohesion: 0.39
Nodes (7): main(), make_fake_tools(), probe_env(), End-to-end probe test: real probe process ↔ reference mock manager over HTTPS., Deterministic stand-ins emitting realistic output for 127.0.0.1., run_probe(), scan_plan()

### Community 161 - "Community 161"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, loadWordlist(), nativeDirBust(), NativeDirOpts, probe(), ProbeResp

### Community 162 - "Community 162"
Cohesion: 0.61
Nodes (7): dial(), ProbeDB(), probeMongo(), probeMSSQL(), probeMysql(), probePostgres(), probeRedis()

### Community 163 - "Community 163"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 164 - "Community 164"
Cohesion: 0.29
Nodes (7): encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt scope payloads to a probe's X25519 publi, Encrypt scope JSON to a specific probe's X25519 public key.      Args:         s, Convenience: dict → JSON → encrypt → base64 string., Decode a base64-encoded X25519 public key to raw bytes.      Returns empty bytes

### Community 165 - "Community 165"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 166 - "Community 166"
Cohesion: 0.43
Nodes (1): TestMetasploitRPCClient

### Community 167 - "Community 167"
Cohesion: 0.25
Nodes (1): TestRequiresApproval

### Community 168 - "Community 168"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 169 - "Community 169"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 171 - "Community 171"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 172 - "Community 172"
Cohesion: 0.25
Nodes (1): TestValidateTargetsInScope

### Community 173 - "Community 173"
Cohesion: 0.25
Nodes (1): TestSubmitResult

### Community 174 - "Community 174"
Cohesion: 0.32
Nodes (4): Handle a new WebSocket client connection., Handle incoming WebSocket messages., Remove connection from room., Send message to a specific connection.

### Community 175 - "Community 175"
Cohesion: 0.36
Nodes (7): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 176 - "Community 176"
Cohesion: 0.29
Nodes (7): count_by_severity(), execute_smb_validation(), execute_tls_scan(), execute_vuln_scan(), Nuclei vulnerability scan — production-ready., NetExec SMB validation: signing, null sessions, SMBv1., testssl.sh TLS/SSL analysis.

### Community 177 - "Community 177"
Cohesion: 0.29
Nodes (1): GzipRequestMiddleware

### Community 178 - "Community 178"
Cohesion: 0.33
Nodes (4): Extracts JWT from Authorization header and injects tenant_id + user     claims i, Extracts JWT from Authorization header and injects tenant_id + user     claims i, TenantIsolationMiddleware, BaseHTTPMiddleware

### Community 179 - "Community 179"
Cohesion: 0.48
Nodes (5): build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()

### Community 180 - "Community 180"
Cohesion: 0.67
Nodes (7): agents/greeting-introduction, main, 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit

### Community 181 - "Community 181"
Cohesion: 0.38
Nodes (6): base_score(), parse_vector(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network, CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r, Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin, _roundup()

### Community 182 - "Community 182"
Cohesion: 0.33
Nodes (4): _as_uuid(), AttackLogger, AttackLogger — records every attack action to the ``attack_timeline`` table.  Al, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 183 - "Community 183"
Cohesion: 0.52
Nodes (6): containsStr(), DiscoverHosts(), findStr(), intStr(), isRefused(), probeAlive()

### Community 184 - "Community 184"
Cohesion: 0.33
Nodes (3): HostDiscoveryScanner, host_discovery.py — determine which hosts are alive.  METHOD (collection only):, Return 'open', 'refused', or None (no response).

### Community 185 - "Community 185"
Cohesion: 0.29
Nodes (2): nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree

### Community 186 - "Community 186"
Cohesion: 0.33
Nodes (2): PortScanner, port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec

### Community 187 - "Community 187"
Cohesion: 0.43
Nodes (5): compute(), SLA policy engine.  Turns a severity + "first seen" timestamp into a remediation, SlaResult, summarize(), _windows()

### Community 188 - "Community 188"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 189 - "Community 189"
Cohesion: 0.29
Nodes (1): TestIngestFile

### Community 190 - "Community 190"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 191 - "Community 191"
Cohesion: 0.29
Nodes (1): TestValidateModule

### Community 192 - "Community 192"
Cohesion: 0.29
Nodes (1): TestValidateScope

### Community 193 - "Community 193"
Cohesion: 0.29
Nodes (1): TestTargetsInExcludes

### Community 194 - "Community 194"
Cohesion: 0.38
Nodes (6): looks_like_http(), looks_like_tls(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, For every open port with a banner fact, returns {port: {branches}}     that obse, route_branches()

### Community 195 - "Community 195"
Cohesion: 0.33
Nodes (4): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Raised when a transport operation fails permanently (not retryable)., Establish an authenticated WebSocket connection to the manager.          Returns, TransportError

### Community 196 - "Community 196"
Cohesion: 0.47
Nodes (4): create_access_token(), create_refresh_token(), _now(), Returns (token, jti) — jti is stored in Redis for revocation.

### Community 197 - "Community 197"
Cohesion: 0.33
Nodes (3): Apply constraints + indexes (idempotent)., Run a Cypher statement and return records as dicts. [] if not connected., Run a parametrised write with UNWIND batching for bulk node/edge loads.

### Community 198 - "Community 198"
Cohesion: 0.53
Nodes (4): copyFile(), Install(), installLaunchd(), installSystemd()

### Community 199 - "Community 199"
Cohesion: 0.33
Nodes (5): INTENSITY_PRESETS, LaunchBody, POST, SshCreds, WinCreds

### Community 200 - "Community 200"
Cohesion: 0.33
Nodes (3): HostResult, PortResult, Result

### Community 201 - "Community 201"
Cohesion: 0.40
Nodes (3): NewScopeGuard(), ScopeFromFile(), ScopeGuard

### Community 202 - "Community 202"
Cohesion: 0.33
Nodes (1): TestNTLMRelayChecker

### Community 203 - "Community 203"
Cohesion: 0.33
Nodes (1): TestCvss

### Community 204 - "Community 204"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 205 - "Community 205"
Cohesion: 0.60
Nodes (5): Unit tests for the dashboard list endpoints (jobs + assets)., _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user()

### Community 206 - "Community 206"
Cohesion: 0.33
Nodes (4): Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., TestTaskRunnerWithEncryptedScope

### Community 207 - "Community 207"
Cohesion: 0.33
Nodes (2): Phase 2: WebSocket message parsing., TestWebSocketMessageProtocol

### Community 208 - "Community 208"
Cohesion: 0.33
Nodes (4): Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup., TestStartupGauntlet

### Community 209 - "Community 209"
Cohesion: 0.33
Nodes (1): TestClamp

### Community 210 - "Community 210"
Cohesion: 0.33
Nodes (1): TestEngagementModes

### Community 211 - "Community 211"
Cohesion: 0.33
Nodes (3): Remove an agent's WebSocket registration., Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to the first online connected agent.          Returns the agent_id th

### Community 212 - "Community 212"
Cohesion: 0.33
Nodes (3): diff_assets(), report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d, re-scan mode's delta report: what changed between two engagements.

### Community 214 - "Community 214"
Cohesion: 0.70
Nodes (4): create_findings_from_probe_result(), _find_open_duplicate(), _map_severity(), _resolve_asset()

### Community 215 - "Community 215"
Cohesion: 0.40
Nodes (1): sla_summary()

### Community 216 - "Community 216"
Cohesion: 0.40
Nodes (4): ApiSlaItem, ApiSlaSummary, GET, SEV_TO_UI

### Community 217 - "Community 217"
Cohesion: 0.40
Nodes (1): TestEDRParsing

### Community 218 - "Community 218"
Cohesion: 0.40
Nodes (3): Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine., TestTransportWithIdentity

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
Nodes (1): TestIdentity

### Community 224 - "Community 224"
Cohesion: 0.40
Nodes (1): TestWebSocket

### Community 225 - "Community 225"
Cohesion: 0.40
Nodes (1): Cross-validates the pure-Python Debian version comparator against the real `dpkg

### Community 226 - "Community 226"
Cohesion: 0.70
Nodes (4): _b64(), issue(), keygen(), main()

### Community 227 - "Community 227"
Cohesion: 0.50
Nodes (4): execute_eyewitness(), extract_web_urls_from_nmap(), Extract HTTP/HTTPS URLs from nmap XML output., EyeWitness screenshot evidence collection.

### Community 229 - "Community 229"
Cohesion: 0.50
Nodes (2): GET, VALID_SEVERITIES

### Community 230 - "Community 230"
Cohesion: 0.83
Nodes (3): latest_run_delta(), list_detection_runs(), _run_dict()

### Community 231 - "Community 231"
Cohesion: 0.67
Nodes (2): GrabBanner(), guessService()

### Community 232 - "Community 232"
Cohesion: 0.83
Nodes (3): enumerateWeakCiphers(), parseCert(), ProbeTLS()

### Community 233 - "Community 233"
Cohesion: 0.67
Nodes (3): compute_exposure(), Exposure analytics — protocol risk + zone health.  Derives two dashboard aggrega, _sev()

### Community 234 - "Community 234"
Cohesion: 0.50
Nodes (1): TestGate0

### Community 235 - "Community 235"
Cohesion: 0.50
Nodes (1): TestRateLimiter

### Community 236 - "Community 236"
Cohesion: 0.50
Nodes (1): TestScanResult

### Community 237 - "Community 237"
Cohesion: 0.50
Nodes (1): TestHttpGet

### Community 238 - "Community 238"
Cohesion: 0.50
Nodes (1): TestPollJobs

### Community 239 - "Community 239"
Cohesion: 0.50
Nodes (1): TestRegister

### Community 240 - "Community 240"
Cohesion: 0.50
Nodes (3): get_or_404(), Shared database helpers — single source of truth for patterns duplicated across, Fetch a row by primary key, optionally scoped to a tenant.     Raises 404 if mis

### Community 241 - "Community 241"
Cohesion: 0.50
Nodes (3): dedup_hash(), Shared hashing utilities — deduplication keys, fingerprinting., SHA-256 of (asset_id, cve_id, plugin_id) for finding deduplication.      Used by

### Community 242 - "Community 242"
Cohesion: 0.50
Nodes (1): Agentic AI advisor: agent_recommendations (recommend-only, human-approved).  Sto

### Community 243 - "Community 243"
Cohesion: 0.50
Nodes (1): Add agents.public_key (Phase-4 X25519 identity for scope encryption).  The probe

### Community 244 - "Community 244"
Cohesion: 0.67
Nodes (3): _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment()

### Community 245 - "Community 245"
Cohesion: 0.67
Nodes (2): toUiAgent(), GET

## Knowledge Gaps
- **752 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+747 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 60`** (2 nodes): `Unit tests for ServiceIdentifier.`, `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 117`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 118`** (2 nodes): `Unit tests for NmapXMLParser.`, `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 119`** (1 nodes): `transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 126`** (2 nodes): `udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO`, `UDPScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 128`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 131`** (1 nodes): `ExploitOrchestrator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 134`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 135`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 136`** (1 nodes): `TestNucleiExploitRunner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 137`** (1 nodes): `TestValidatePayload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 138`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (1 nodes): `db_scanner.py — fingerprint database services.  WHY: databases are everywhere on`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 150`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 151`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 156`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 163`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 165`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 166`** (1 nodes): `TestMetasploitRPCClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (1 nodes): `TestRequiresApproval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 171`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 172`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 173`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 177`** (1 nodes): `GzipRequestMiddleware`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 185`** (2 nodes): `nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:`, `# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 186`** (2 nodes): `PortScanner`, `port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 188`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 189`** (1 nodes): `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 190`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 191`** (1 nodes): `TestValidateModule`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 192`** (1 nodes): `TestValidateScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 193`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 202`** (1 nodes): `TestNTLMRelayChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 203`** (1 nodes): `TestCvss`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 204`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (2 nodes): `Phase 2: WebSocket message parsing.`, `TestWebSocketMessageProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 209`** (1 nodes): `TestClamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 210`** (1 nodes): `TestEngagementModes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (1 nodes): `sla_summary()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (1 nodes): `TestEDRParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (1 nodes): `TestLooksLikeHttp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (1 nodes): `TestLooksLikeTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (1 nodes): `TestResolveScanType`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (1 nodes): `TestTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (1 nodes): `TestWebSocket`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (1 nodes): `Cross-validates the pure-Python Debian version comparator against the real `dpkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (2 nodes): `GET`, `VALID_SEVERITIES`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (2 nodes): `GrabBanner()`, `guessService()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (1 nodes): `TestGate0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (1 nodes): `TestRateLimiter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (1 nodes): `TestScanResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (1 nodes): `TestHttpGet`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (1 nodes): `TestPollJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (1 nodes): `TestRegister`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 242`** (1 nodes): `Agentic AI advisor: agent_recommendations (recommend-only, human-approved).  Sto`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (1 nodes): `Add agents.public_key (Phase-4 X25519 identity for scope encryption).  The probe`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (2 nodes): `toUiAgent()`, `GET`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 30` to `Community 52`, `Community 80`, `Community 62`, `Community 21`, `Community 122`, `Community 4`, `Community 20`, `Community 1`, `Community 38`, `Community 127`, `Community 134`, `Community 188`, `Community 165`, `Community 202`, `Community 116`, `Community 88`, `Community 44`, `Community 166`, `Community 136`, `Community 167`, `Community 191`, `Community 137`, `Community 192`, `Community 0`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `Finding` connect `Community 4` to `Community 81`, `Community 122`, `Community 131`, `Community 16`, `Community 89`, `Community 2`, `Community 6`, `Community 106`, `Community 46`, `Community 30`, `Community 38`, `Community 20`, `Community 1`, `Community 187`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `SourceConfidence` connect `Community 11` to `Community 73`, `Community 18`, `Community 74`, `Community 20`, `Community 37`, `Community 12`, `Community 3`, `Community 23`, `Community 203`, `Community 67`, `Community 189`, `Community 135`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 127 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 127 INFERRED edges - model-reasoned connections that need verification._
- **Are the 94 inferred relationships involving `FindingStatus` (e.g. with `ADConnectionError` and `ADError`) actually correct?**
  _`FindingStatus` has 94 INFERRED edges - model-reasoned connections that need verification._
- **Are the 85 inferred relationships involving `Finding` (e.g. with `AgentDecisionEngine` and `AgentUnavailableError`) actually correct?**
  _`Finding` has 85 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R` to the rest of the system?**
  _752 weakly-connected nodes found - possible documentation gaps or missing edges._