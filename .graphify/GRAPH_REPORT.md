# Graph Report - .  (2026-07-22)

## Corpus Check
- 353 files · ~242,226 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3037 nodes · 6414 edges · 174 communities detected
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 1611 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 1611 · contains: 1601 · calls: 973 · method: 618 · rationale_for: 487 · imports: 372 · MODIFIES: 310 · imports_from: 297 · inherits: 127 · ON_BRANCH: 12 · PARENT_OF: 6


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 353 · Candidates: 470
- Excluded: 571 untracked · 63552 ignored · 0 sensitive · 8 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `0557559`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `FindingSeverity` - 129 edges
2. `FindingStatus` - 87 edges
3. `Finding` - 73 edges
4. `Engagement` - 67 edges
5. `Asset` - 60 edges
6. `LDAPEnumerator` - 52 edges
7. `ScanJob` - 50 edges
8. `ScanJobType` - 45 edges
9. `MetasploitRPCClient` - 41 edges
10. `SafetyViolationError` - 39 edges

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

### Community 106 - "Community 106"
Cohesion: 0.22
Nodes (3): Settings, BaseSettings, get_settings()

### Community 165 - "Community 165"
Cohesion: 0.50
Nodes (1): Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19

### Community 166 - "Community 166"
Cohesion: 0.50
Nodes (1): Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202

### Community 167 - "Community 167"
Cohesion: 0.50
Nodes (1): Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R

### Community 168 - "Community 168"
Cohesion: 0.50
Nodes (1): Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000

### Community 169 - "Community 169"
Cohesion: 0.50
Nodes (1): Detection validation: attack_timeline, detection_configs, extend detection_resul

### Community 170 - "Community 170"
Cohesion: 0.50
Nodes (1): AI engine: llm_outputs table + reviewstatus enum  Revision ID: 0006 Revises: 000

### Community 171 - "Community 171"
Cohesion: 0.50
Nodes (1): P3: composite indexes for the hot aggregate + poll query paths.  The dashboard's

### Community 172 - "Community 172"
Cohesion: 0.50
Nodes (1): P3-#10: append-only scan_results table (raw facts).  Decouples the (large) raw f

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (10): HallucinationGuard — post-generation validation of LLM report text against the g, Neo4jClient — thin, optional wrapper around the neo4j Python driver.  Neo4j is *, parse_csv_assets(), eslintConfig, config, Verify the Python probe can open what the TypeScript manager sealed (T14 interop, agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit, VA scanner module — pure collection/scanning layer.  Each submodule is an indepe (+2 more)

### Community 42 - "Community 42"
Cohesion: 0.18
Nodes (12): CertTemplate, ADCSChecker, ADCSChecker — Active Directory Certificate Services template misconfiguration an, Read pKICertificateTemplate objects from the Configuration NC., Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM (+4 more)

### Community 57 - "Community 57"
Cohesion: 0.13
Nodes (7): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., TestASREPRoastChecker

### Community 49 - "Community 49"
Cohesion: 0.11
Nodes (8): BloodHoundCollector, BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, Run bloodhound-python and return the list of produced JSON file paths.         R, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., TestBuildADFinding

### Community 23 - "Community 23"
Cohesion: 0.10
Nodes (20): ADError, severity_from_str(), build_ad_finding(), Shared building blocks for the Active Directory assessment module.  Every AD che, Base class for Active Directory assessment errors., Assemble a Finding-compatible dict.      All findings carry — as required by the, KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline (+12 more)

### Community 24 - "Community 24"
Cohesion: 0.28
Nodes (30): Exception, ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is, Coordinates safe exploit validation runs:       1. Safety validation (payload al, Returns {module, payload, safe_check} for the given finding.         Priority: C, Raises SafetyViolationError if module or payload is not permitted., Raises OutOfScopeError if target_ip not in engagement scope., Full exploit execution pipeline with safety, scope, blast radius,         audit, Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo (+22 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (21): ADConnectionError, DependencyMissingError, Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., ADUser, ADComputer, ADGroup, _domain_to_base_dn() (+13 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (35): HallucinationGuard, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide., Run all relevant checks and return a combined verdict:         ``{valid, issues,, LLMUnavailableError, RuntimeError, LLMReportGenerator (+27 more)

### Community 92 - "Community 92"
Cohesion: 0.23
Nodes (7): _to_float(), extract_features(), VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal, Build the model's feature vector from a Finding (+ optional Asset + extra     co, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula).

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (9): VulnPrioritizer, Fit an XGBoost regressor on historical findings. ``historical_findings_df``, _finding(), _asset(), TestVulnPrioritizer, TestHallucinationGuard, _resp(), _mock_db() (+1 more)

### Community 149 - "Community 149"
Cohesion: 0.47
Nodes (4): _now(), create_access_token(), create_refresh_token(), Returns (token, jti) — jti is stored in Redis for revocation.

### Community 50 - "Community 50"
Cohesion: 0.12
Nodes (9): TenantIsolationMiddleware, BaseHTTPMiddleware, Extracts JWT from Authorization header and injects tenant_id + user     claims i, get_read_db(), Read-only session (no commit) routed to the replica when configured.     For SEL, run_post_scan_enrichment(), _fire_critical_webhook(), _dedup_hash() (+1 more)

### Community 58 - "Community 58"
Cohesion: 0.13
Nodes (10): require_role(), FastAPI dependency that enforces role-based access.      Usage:         @router., close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, sla_summary(), CurrentUser (+2 more)

### Community 137 - "Community 137"
Cohesion: 0.33
Nodes (2): refresh(), create_personal_access_token()

### Community 80 - "Community 80"
Cohesion: 0.23
Nodes (6): DetectionResultDTO, DetectionGap, _host_matches(), DetectionCorrelator, _aware(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale

### Community 32 - "Community 32"
Cohesion: 0.13
Nodes (13): AttackAction, EDRDetection, _parse_dt(), EDRQueryEngine, CrowdStrikeFalcon, MicrosoftDefender, SentinelOne, EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender (+5 more)

### Community 117 - "Community 117"
Cohesion: 0.31
Nodes (5): Normalise naive datetimes to UTC so comparisons never raise., SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma detection rule (YAML) for a MITRE techniqu, Return a Sigma rule (YAML string) for the technique, customised with the

### Community 34 - "Community 34"
Cohesion: 0.17
Nodes (22): _vuln_db_meta(), _ensure_importable(), detect_findings_from_facts(), create_findings_from_facts(), run_detection_job(), engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, (content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev, facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur (+14 more)

### Community 139 - "Community 139"
Cohesion: 0.33
Nodes (4): AttackLogger, _as_uuid(), AttackLogger — records every attack action to the ``attack_timeline`` table.  Al, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 36 - "Community 36"
Cohesion: 0.13
Nodes (11): SIEMAlert, _parse_dt(), SIEMQueryEngine, SplunkSIEM, SentinelSIEM, ElasticSIEM, SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Abstract SIEM connector. (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (44): _map_severity(), _resolve_asset(), _find_open_duplicate(), create_findings_from_probe_result(), Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Convert a probe's self-assessed `findings` list into persisted Finding rows. (+36 more)

### Community 107 - "Community 107"
Cohesion: 0.27
Nodes (4): RateLimiter, RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim

### Community 140 - "Community 140"
Cohesion: 0.33
Nodes (4): ServiceFingerprint, ServiceIdentifier, ServiceIdentifier — banner + port → structured service fingerprint. Handles: HTT, Unit tests for ServiceIdentifier.

### Community 76 - "Community 76"
Cohesion: 0.24
Nodes (8): DiscoveryJobPayload, DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner, Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr, ParsedPort, ParsedHost, NmapXMLParser, Nmap XML output parser. Converts -oX output into structured ParsedHost / ParsedP, Parse nmap -oX XML into a list of ParsedHost objects.

### Community 122 - "Community 122"
Cohesion: 0.43
Nodes (1): DiscoveryWorker

### Community 37 - "Community 37"
Cohesion: 0.13
Nodes (13): MetasploitRPCError, MetasploitRPCClient, MetasploitRPCClient — async client for msfrpcd.  Protocol: MessagePack RPC over, Async Metasploit RPC client using msgpack-over-HTTPS., Authenticate with msfrpcd and store the session token., module_type: exploit | auxiliary | payload | post | encoder         Returns list, Execute a Metasploit module.         Returns job_id as string., Returns {status, output, uuid}. (+5 more)

### Community 67 - "Community 67"
Cohesion: 0.15
Nodes (8): NucleiExploitRunner, NucleiExploitRunner — CVE PoC validation using Nuclei templates.  Enforces templ, Run Nuclei CVE PoC templates against a single target.     Every template is safe, Parse template YAML and validate it contains no write/delete/DoS actions., Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Parse nuclei JSONL output for a single CVE PoC result., TestMetasploitIntegration, Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me

### Community 99 - "Community 99"
Cohesion: 0.29
Nodes (1): ExploitOrchestrator

### Community 108 - "Community 108"
Cohesion: 0.20
Nodes (9): validate_payload(), validate_module(), validate_scope(), requires_approval(), Safety constants, exceptions, and validators for the exploitation engine.  All s, Raises SafetyViolationError if payload is not on allowlist     or violates per-p, Raises SafetyViolationError if module is on the block list., Raises OutOfScopeError if target_ip is not in scope or is excluded. (+1 more)

### Community 47 - "Community 47"
Cohesion: 0.15
Nodes (10): PathAnalyzer, _safe_float(), _priority(), PathAnalyzer — attack-path discovery, scoring, chokepoint and blast-radius analy, Best (easiest) exploitable finding on an asset: {cvss, weight, finding}., Build (and cache) the Asset→Asset movement projection. Edge weight is the, Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for (+2 more)

### Community 68 - "Community 68"
Cohesion: 0.28
Nodes (8): asset_node_id(), service_node_id(), finding_node_id(), _enum_value(), _to_float(), exploit_complexity(), is_internet_exposed(), GraphBuilder

### Community 77 - "Community 77"
Cohesion: 0.19
Nodes (8): DemoAsset, DemoService, DemoFinding, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, TestNeo4jClient, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci

### Community 87 - "Community 87"
Cohesion: 0.17
Nodes (6): _deterministic_layout(), GraphVisualizer, GraphVisualizer — serialise the attack graph into D3-compatible JSON for the fro, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag, TestGraphVisualizer

### Community 135 - "Community 135"
Cohesion: 0.29
Nodes (1): GzipRequestMiddleware

### Community 16 - "Community 16"
Cohesion: 0.19
Nodes (34): AgentStatus, Agent, Engagement, ScanJobType, ScanJobStatus, ScanJob, Neo4jConfig, ADAssessRequest (+26 more)

### Community 59 - "Community 59"
Cohesion: 0.24
Nodes (16): Base, TimestampMixin, AttackTimeline, Append-only ledger of every attack action performed during an engagement.      W, Base, DeclarativeBase, TimestampMixin, UUIDMixin (+8 more)

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (40): AssetCriticality, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path, NessusScanRequest, NucleiScanRequest, FindingImport, _run_nuclei_and_save(), Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment., Background task: run nuclei, persist findings, trigger enrichment. (+32 more)

### Community 136 - "Community 136"
Cohesion: 0.29
Nodes (5): client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the exi, Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a     prox, FastAPI dependency factory. Keys the window by (scope, client-IP).

### Community 156 - "Community 156"
Cohesion: 0.50
Nodes (2): _run_ad_assessment_and_save(), _set_job_status()

### Community 43 - "Community 43"
Cohesion: 0.14
Nodes (16): BaseModel, AssetIn, AssetOut, BulkAssetImportResult, LoginRequest, TokenResponse, PersonalAccessTokenCreate, PersonalAccessTokenCreated (+8 more)

### Community 88 - "Community 88"
Cohesion: 0.36
Nodes (12): list_attack_paths(), get_attack_path(), list_chokepoints(), blast_radius(), attack_graph(), _build_analyzer(), _critical_asset_ids(), _all_paths_to_critical() (+4 more)

### Community 119 - "Community 119"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 55 - "Community 55"
Cohesion: 0.18
Nodes (13): _overview_cache_key(), _compute_overview(), _refresh_overview_cache(), re_detect(), _read_capped(), _parse_probe_file(), _promote_from_facts(), import_facts() (+5 more)

### Community 84 - "Community 84"
Cohesion: 0.22
Nodes (12): run_exploit(), list_exploit_results(), get_exploit_result(), list_approvals(), approve_exploit(), reject_exploit(), _load_finding_and_eng(), _get_result_or_404() (+4 more)

### Community 163 - "Community 163"
Cohesion: 0.50
Nodes (3): get_or_404(), Shared database helpers — single source of truth for patterns duplicated across, Fetch a row by primary key, optionally scoped to a tenant.     Raises 404 if mis

### Community 164 - "Community 164"
Cohesion: 0.50
Nodes (3): dedup_hash(), Shared hashing utilities — deduplication keys, fingerprinting., SHA-256 of (asset_id, cve_id, plugin_id) for finding deduplication.      Used by

### Community 173 - "Community 173"
Cohesion: 0.67
Nodes (2): paginate_query(), Returns (items, total). Applies OFFSET/LIMIT to `query`.

### Community 120 - "Community 120"
Cohesion: 0.22
Nodes (5): ConnectionManager, WebSocket manager for real-time graph updates, agent push, and live collaboratio, Manages WebSocket connections with room-based broadcasting., Accept connection and add to room., Get number of connected clients in a room.

### Community 131 - "Community 131"
Cohesion: 0.32
Nodes (4): Remove connection from room., Send message to a specific connection., Handle a new WebSocket client connection., Handle incoming WebSocket messages.

### Community 104 - "Community 104"
Cohesion: 0.22
Nodes (6): GraphWebSocketManager, Broadcast message to all connections in a room., High-level manager for graph-specific WebSocket operations., Broadcast graph data update to all subscribers., Broadcast a single node update., Broadcast layout change to all subscribers.

### Community 48 - "Community 48"
Cohesion: 0.10
Nodes (10): AgentConnectionManager, Tracks WebSocket connections from probes/agents for direct job push.      Each c, Register an agent's WebSocket connection.          If the agent already has a co, Record a heartbeat from an agent., Check if a specific agent is connected., Check if a specific agent is online (connected + not busy)., Return a snapshot of all connected agent IDs., Return agent IDs whose status is 'online' (idle, ready for job). (+2 more)

### Community 153 - "Community 153"
Cohesion: 0.33
Nodes (3): Remove an agent's WebSocket registration., Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to the first online connected agent.          Returns the agent_id th

### Community 95 - "Community 95"
Cohesion: 0.29
Nodes (3): _FakeEntry, _enum_with_entries(), TestLDAPEnumeratorParsing

### Community 128 - "Community 128"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 150 - "Community 150"
Cohesion: 0.33
Nodes (1): TestNTLMRelayChecker

### Community 101 - "Community 101"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 144 - "Community 144"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 21 - "Community 21"
Cohesion: 0.08
Nodes (14): _user(), TestAgentExecutableTypes, TestEnqueueAgentJob, TestOTProfileGate, TestGetAgentJobs, TestListAgents, TestRegisterAgent, TestPromoteAssets (+6 more)

### Community 115 - "Community 115"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 96 - "Community 96"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 63 - "Community 63"
Cohesion: 0.19
Nodes (2): _action(), TestDetectionCorrelator

### Community 145 - "Community 145"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 151 - "Community 151"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 157 - "Community 157"
Cohesion: 0.40
Nodes (1): TestEDRParsing

### Community 152 - "Community 152"
Cohesion: 0.60
Nodes (5): _user(), _scalars(), test_list_jobs_returns_results(), test_list_assets_groups_services(), Unit tests for the dashboard list endpoints (jobs + assets).

### Community 90 - "Community 90"
Cohesion: 0.29
Nodes (4): _finding(), _engagement(), TestExploitOrchestrator, Unit tests for the exploitation engine.  All external connections (Metasploit RP

### Community 103 - "Community 103"
Cohesion: 0.18
Nodes (1): TestValidatePayload

### Community 146 - "Community 146"
Cohesion: 0.29
Nodes (1): TestValidateModule

### Community 147 - "Community 147"
Cohesion: 0.29
Nodes (1): TestValidateScope

### Community 130 - "Community 130"
Cohesion: 0.25
Nodes (1): TestRequiresApproval

### Community 129 - "Community 129"
Cohesion: 0.43
Nodes (1): TestMetasploitRPCClient

### Community 102 - "Community 102"
Cohesion: 0.18
Nodes (1): TestNucleiExploitRunner

### Community 97 - "Community 97"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_running(), test_poll_status_completed()

### Community 56 - "Community 56"
Cohesion: 0.21
Nodes (1): TestServiceIdentifier

### Community 41 - "Community 41"
Cohesion: 0.13
Nodes (11): _make_http_mock(), test_fetch_nvd_success(), test_fetch_nvd_caches_result(), test_fetch_epss_success(), test_check_cisa_kev_present(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_fetch_mitre_from_nvd_references() (+3 more)

### Community 91 - "Community 91"
Cohesion: 0.15
Nodes (2): TestNmapXMLParser, Unit tests for NmapXMLParser.

### Community 26 - "Community 26"
Cohesion: 0.13
Nodes (19): AnthropicAIClient, FakeAIClient, AINormalizerCache, validate_cpe_exists(), extract_raw_text(), propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Returns a list of {"vendor", "product", "version"} dicts —         exactly the v (+11 more)

### Community 19 - "Community 19"
Cohesion: 0.09
Nodes (22): AIClient, Protocol, enrich_finding(), _compute_priority(), enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier., Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr, Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li, KevDB (+14 more)

### Community 74 - "Community 74"
Cohesion: 0.16
Nodes (9): wilson_ci(), FindingConsistency, ConsistencyReport, aggregate(), format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen, run_findings: one list of Findings per run (N runs). Aggregated by     the deter (+1 more)

### Community 61 - "Community 61"
Cohesion: 0.15
Nodes (11): dedup_findings(), suppress_negated(), _product_from_cpe(), correlate_smb_patch(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, Suppress a suspected/potential (inferred-source) finding when the     SAME host, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS (+3 more)

### Community 29 - "Community 29"
Cohesion: 0.14
Nodes (25): Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, _safe_compare(), _version_in_ranges(), match_candidate(), matcher.py — does this CPE candidate's version fall inside a vulnerable range, p, dpkg_compare, but None instead of a misleading answer when one side     has an e, Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A, All Findings this single CPE candidate produces against the snapshot.     Empty (+17 more)

### Community 45 - "Community 45"
Cohesion: 0.11
Nodes (19): clean_debian_version(), clean_rpm_version(), osv_source_packages(), normalize_banner(), normalize_web(), _parse_package_lines(), normalize_credentialed_packages(), normalize() (+11 more)

### Community 138 - "Community 138"
Cohesion: 0.38
Nodes (6): _roundup(), parse_vector(), base_score(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network, CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r, Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin

### Community 75 - "Community 75"
Cohesion: 0.22
Nodes (12): QuarantinedLine, IngestResult, _classify_confidence(), _validate(), _is_ip(), _extract_aliases(), ingest_file(), ingest_files() (+4 more)

### Community 158 - "Community 158"
Cohesion: 0.40
Nodes (1): Cross-validates the pure-Python Debian version comparator against the real `dpkg

### Community 81 - "Community 81"
Cohesion: 0.23
Nodes (13): _ssl_context(), _query_osv(), sync_snapshot(), sync_kev_snapshot(), sync_epss_snapshot(), _all_known_cve_ids(), main(), update_snapshot.py — the ONLY module in this package that talks to the network. (+5 more)

### Community 52 - "Community 52"
Cohesion: 0.16
Nodes (18): _dpkg_compare_via_binary(), _char_order(), _compare_non_digit(), _split_segments(), _compare_part(), _split_dpkg_version(), has_ambiguous_epoch(), _dpkg_compare_pure_python() (+10 more)

### Community 121 - "Community 121"
Cohesion: 0.32
Nodes (7): _default_products(), _content_hash(), SnapshotMeta, load_snapshot(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Derives the synced product list from cpe_normalizer.py's tables —     the single, Stable hash of the snapshot's actual vulnerability content — recorded     in eve

### Community 65 - "Community 65"
Cohesion: 0.13
Nodes (9): Message, Agent, Finding, quickPrompts, initialMessage, defaultAgents, findings, graphStats (+1 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (50): GET, BASE, fail(), GET, PUT(), GET, POST, VALID_SEVERITIES (+42 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (49): GET, POST, AuthContext, Handler, withAuth(), OtpEntry, otpStore, SessionPayload (+41 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (26): POST, Severity, FindingSeverity, DEFAULT_DATA_PATH, setDataPath(), SLA_HOURS, ensureDir(), slaDeadline() (+18 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (33): DEMO_ENGAGEMENT, DEMO_FINDING, DEMO_ASSET, DEMO_FINDINGS, DEMO_ASSETS, ReviewStatus, ReportSection, FindingInput (+25 more)

### Community 18 - "Community 18"
Cohesion: 0.07
Nodes (19): NodeType, RelationType, Severity, PathStatus, GNode, GEdge, AttackPath, Chokepoint (+11 more)

### Community 30 - "Community 30"
Cohesion: 0.08
Nodes (15): DetectionOutcome, AttackAction, ATTACK_TIMELINE, SIEMAlert, EDRDetection, SIEM_ALERTS, EDR_DETECTIONS, DetectionResult (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (30): ConvMessage, buildAskCommand(), PROFILE_TOOLS, buildScanCommand(), client(), commentOnStage(), explainFindings(), suggestAttackPath() (+22 more)

### Community 162 - "Community 162"
Cohesion: 0.67
Nodes (2): validateTargets(), POST()

### Community 155 - "Community 155"
Cohesion: 0.60
Nodes (4): NxcHost, parseNxcOutput(), runNxc(), POST()

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (44): NseScript, VulnRef, ScanPort, ScanHost, ScanResult, validateTarget(), SCAN_PROFILES, NSE_VULN_MAP (+36 more)

### Community 27 - "Community 27"
Cohesion: 0.09
Nodes (24): SEV_PREFIX, counters, generateFindingId(), resetCounters(), NaabuResult, NaabuRaw, parseNaabuLine(), groupNaabuResults() (+16 more)

### Community 28 - "Community 28"
Cohesion: 0.08
Nodes (15): TabKey, Engagement, statusColor(), AssetRow, EDIT_STATUSES, EngagementDetailPage(), EnvSetting, EMAIL_FIELDS (+7 more)

### Community 98 - "Community 98"
Cohesion: 0.18
Nodes (6): EngagementStatus, Engagement, EngagementsResponse, FormState, EMPTY_FORM, STEPS

### Community 25 - "Community 25"
Cohesion: 0.07
Nodes (22): Severity, FindingStatus, ExploitMaturity, DetectionCoverage, RemStep, ComplianceRef, RiskBreakdown, KillChainStep (+14 more)

### Community 44 - "Community 44"
Cohesion: 0.12
Nodes (13): metadata, PageShellProps, QueryProvider(), Theme, ThemeContextValue, ThemeContext, useTheme(), ThemeProvider() (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (27): AgentStatus, Agent, AGENT_STATUS, riskColor(), ProtocolRow(), getSla(), SEV_BG, SEV_COLOR (+19 more)

### Community 51 - "Community 51"
Cohesion: 0.11
Nodes (10): ReportType, ComplianceFramework, ComplianceControl, ComplianceFrameworkData, evidenceStats, frameworks, NavItem, NAV_SECTIONS (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.09
Nodes (13): UseCase, Probe, Engagement, JobStatus, UC_META, RISK, PROFILE_BADGE, CATS (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (25): SESSION_DIR, SESSION_FILE, Session, loadSession(), saveSession(), clearSession(), requireAuth(), serverUrl() (+17 more)

### Community 60 - "Community 60"
Cohesion: 0.14
Nodes (8): CheckResult, C, ln(), symbol(), render(), which(), checkTool(), buildDoctorCommand()

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (55): A, w(), ln(), ask(), askSecret(), confirm(), choose(), banner() (+47 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (30): C, ln(), showSpinner(), buildToolsCommand(), InstalledRecord, InstalledManifest, readInstalled(), writeInstalled() (+22 more)

### Community 38 - "Community 38"
Cohesion: 0.15
Nodes (22): A, w(), ln(), SEV_COLOR, sevBadge(), LINE, rule(), banner() (+14 more)

### Community 66 - "Community 66"
Cohesion: 0.13
Nodes (9): TimelinePoint, Engagement, ActivityItem, Finding, SEV, STATUS_STYLE, DashboardCharts(), useCountUp() (+1 more)

### Community 31 - "Community 31"
Cohesion: 0.10
Nodes (18): Sev, Finding, Engagement, LiveOverview(), SkeletonRows(), EmptyState(), ErrorState(), DataStateProps (+10 more)

### Community 35 - "Community 35"
Cohesion: 0.09
Nodes (23): execute_naabu(), execute_discovery(), parse_spn_output(), execute_ad_enum(), execute_lateral_movement(), execute_cloud_scan(), Fast port discovery with naabu. Feeds port list to Nmap., Nmap service enumeration. Accepts port list from Naabu. (+15 more)

### Community 105 - "Community 105"
Cohesion: 0.36
Nodes (3): ScanJob, check_tool_availability(), ScanningAgent

### Community 133 - "Community 133"
Cohesion: 0.29
Nodes (4): VaultCredentialFetcher, build_ssl_context(), Fetches credentials from HashiCorp Vault at runtime. Never caches to disk., Read a KV-v2 secret from Vault.

### Community 134 - "Community 134"
Cohesion: 0.29
Nodes (7): count_by_severity(), execute_vuln_scan(), execute_smb_validation(), execute_tls_scan(), Nuclei vulnerability scan — production-ready., NetExec SMB validation: signing, null sessions, SMBv1., testssl.sh TLS/SSL analysis.

### Community 160 - "Community 160"
Cohesion: 0.50
Nodes (4): extract_web_urls_from_nmap(), execute_eyewitness(), Extract HTTP/HTTPS URLs from nmap XML output., EyeWitness screenshot evidence collection.

### Community 33 - "Community 33"
Cohesion: 0.10
Nodes (22): AgentStatus, JobStatus, JobType, KafkaTopic, AgentCapability, Agent, ScanJob, KafkaTopicInfo (+14 more)

### Community 62 - "Community 62"
Cohesion: 0.18
Nodes (15): CaseSeverity, CaseStatus, CaseComment, CaseActivity, Case, DATA_FILE, SLA_HOURS, SEED_CASES (+7 more)

### Community 20 - "Community 20"
Cohesion: 0.09
Nodes (31): DATA_PATH, ClientStatus, ClientJiraConfig, ClientNotifyConfig, ClientSettings, Client, ClientsFile, SEED (+23 more)

### Community 109 - "Community 109"
Cohesion: 0.20
Nodes (8): EngagementStatus, Credential, Engagement, STORE, ACTIVITY, now, FINDINGS_TIMELINE, engagementsStore

### Community 124 - "Community 124"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, ProbeResp, probe(), NativeDirOpts, loadWordlist(), nativeDirBust()

### Community 125 - "Community 125"
Cohesion: 0.32
Nodes (7): DnsReconResult, PtrSweepResult, COMMON_SUBDOMAINS, safe(), nativeDnsRecon(), attemptZoneTransfer(), nativePtrSweep()

### Community 110 - "Community 110"
Cohesion: 0.20
Nodes (6): WEB_PORT_PROTO, TechRule, TECH_RULES, HttpProbeResult, NativeHttpOpts, nativeHttpProbe()

### Community 93 - "Community 93"
Cohesion: 0.18
Nodes (9): TOP_1000_TCP, PORT_NAMES, NativePortResult, PortRange, resolvePorts(), CheckOpts, NativeScanOpts, nativePortScan() (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (39): TlsInfoResult, WEAK_SIGNATURES, WEAK_PROTOCOLS, nativeTlsInfo(), NAABU_RATE, NMAP_TIMING, isWindows(), hasSystemBinary() (+31 more)

### Community 118 - "Community 118"
Cohesion: 0.22
Nodes (5): ModuleCategory, ModuleInput, ModuleOutput, ScanModule, modulesForPorts()

### Community 82 - "Community 82"
Cohesion: 0.16
Nodes (7): ErrorCode, VedhaErrorOpts, VedhaError, Errors, diagnoseSpawnError(), AdversaErrorOpts, AdversaError

### Community 78 - "Community 78"
Cohesion: 0.13
Nodes (12): PayloadType, JobStatus, ApprovalStatus, ExploitEvidence, ExploitResult, ExploitJob, ExploitApprovalRequest, AuditEntry (+4 more)

### Community 161 - "Community 161"
Cohesion: 0.50
Nodes (3): __dirname, frontendRoot, nextConfig

### Community 46 - "Community 46"
Cohesion: 0.15
Nodes (10): b64e(), ManagerState, _make_handler(), _self_signed(), spki_pin(), _QuietServer, ThreadingHTTPServer, start() (+2 more)

### Community 123 - "Community 123"
Cohesion: 0.39
Nodes (7): make_fake_tools(), scan_plan(), probe_env(), run_probe(), main(), End-to-end probe test: real probe process ↔ reference mock manager over HTTPS., Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 64 - "Community 64"
Cohesion: 0.16
Nodes (16): _load_env(), say(), main(), _startup_gauntlet(), _check_anti_debug(), _load_or_create_identity(), _obtain_identity(), Load key=value lines from probe.env for dev convenience. (+8 more)

### Community 72 - "Community 72"
Cohesion: 0.15
Nodes (15): _run_ws_push_loop(), _ws_run_job(), _ws_http_poll_fallback(), _ws_heartbeat_sender(), _ws_flush_spool(), Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Run one job while keeping WS status/result frames best-effort., Poll pending jobs even while WS is connected.      This makes result delivery re (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.07
Nodes (27): _error_result(), _targets(), _clamp(), _tuning_from_params(), _count_open_port_facts(), run_scan(), engine.py — adapt a manager scan job to scanner_module's workflow engine and ret, Single factory for error result dicts — no copy-paste. (+19 more)

### Community 79 - "Community 79"
Cohesion: 0.24
Nodes (12): LicenseError, host_fingerprint(), short_id(), _b64d(), verify_license(), check_license(), gauntlet(), license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p (+4 more)

### Community 83 - "Community 83"
Cohesion: 0.20
Nodes (7): _Collector, _shared(), _run_active(), _clean(), _rollup(), Make a per-host scanner instance share ONE rate limiter + semaphore with all, Make a raw banner safe and readable for the summary line.      Many services ans

### Community 100 - "Community 100"
Cohesion: 0.22
Nodes (5): _orchestrate(), main(), # NOTE: credentialed collectors (ssh_collector, windows_collector) are run, ServiceBannerScanner, service_banner.py — grab service banners and light version strings.  METHOD (col

### Community 111 - "Community 111"
Cohesion: 0.20
Nodes (1): db_scanner.py — fingerprint database services.  WHY: databases are everywhere on

### Community 73 - "Community 73"
Cohesion: 0.17
Nodes (6): DBScanner, BaseScanner, _build_get(), _extract_sysdescr(), SNMPScanner, snmp_scanner.py — detect SNMP and read sysDescr via common community strings.  M

### Community 141 - "Community 141"
Cohesion: 0.33
Nodes (3): HostDiscoveryScanner, host_discovery.py — determine which hosts are alive.  METHOD (collection only):, Return 'open', 'refused', or None (no response).

### Community 53 - "Community 53"
Cohesion: 0.15
Nodes (14): _have_masscan(), _run_masscan(), _parse_masscan_json(), _masscan_records_to_results(), _ConnectSweep, run_mass_scan(), _masscan_excludes(), _spec_in_scope() (+6 more)

### Community 54 - "Community 54"
Cohesion: 0.15
Nodes (10): _NoRedirect, _known_false_positive(), _mcp_oauth_signal(), _auth_shaped_json_body(), _model_count(), MCPAIScanner, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+2 more)

### Community 142 - "Community 142"
Cohesion: 0.29
Nodes (2): nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree

### Community 69 - "Community 69"
Cohesion: 0.17
Nodes (11): _printable_strings(), _device_hint(), _open_listener(), PassiveCollector, _is_readable(), passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)., Pull short printable ASCII runs from a payload, for human-readable evidence., Best-effort device label from an announcement payload (recv-only parsing). (+3 more)

### Community 143 - "Community 143"
Cohesion: 0.33
Nodes (2): PortScanner, port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec

### Community 112 - "Community 112"
Cohesion: 0.20
Nodes (7): resolve(), bracket_host(), parse_ports(), scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h, Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535).

### Community 70 - "Community 70"
Cohesion: 0.15
Nodes (8): ScanResult, RateLimiter, BaseScanner, main_entrypoint(), One observation about one target. Pure fact, no interpretation., Simple async rate limiter: at most `rate` operations per second., Subclasses implement `scan_target(self, target)` (async), returning a list     o, Run a scanner CLI's body with consistent, operator-friendly error handling.

### Community 89 - "Community 89"
Cohesion: 0.19
Nodes (5): ScopeError, ScopeGuard, Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude).

### Community 126 - "Community 126"
Cohesion: 0.29
Nodes (6): expand_targets(), ResultWriter, run_cli(), Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Writes ScanResult objects as JSONL to a file and/or stdout., Wire argparse args into a scanner instance and execute it.

### Community 113 - "Community 113"
Cohesion: 0.27
Nodes (5): _netbios_session(), _smb1_negotiate(), _smb2_negotiate(), SMBScanner, smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection

### Community 127 - "Community 127"
Cohesion: 0.29
Nodes (2): SSHCollector, ssh_collector.py — credentialed (authenticated) inventory collection for Linux.

### Community 85 - "Community 85"
Cohesion: 0.21
Nodes (9): _sni(), _try_version(), _get_cert_der(), _parse_cert_der(), _scan_tls_sync(), TLSScanner, tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Never send an IP literal as SNI — non-conformant; some servers reject it. (+1 more)

### Community 94 - "Community 94"
Cohesion: 0.18
Nodes (2): UDPScanner, udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO

### Community 114 - "Community 114"
Cohesion: 0.22
Nodes (3): _NoRedirect, WebScanner, web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl

### Community 86 - "Community 86"
Cohesion: 0.20
Nodes (4): _smb_registry_collect(), WindowsCollector, windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus

### Community 159 - "Community 159"
Cohesion: 0.70
Nodes (4): _b64(), keygen(), issue(), main()

### Community 39 - "Community 39"
Cohesion: 0.11
Nodes (7): _utcnow(), _parse_ts(), PortFact, Asset, asset.py — per-host fact model the workflow engine reasons about.  This is an OR, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Dispatch a real ScanResult into the right sub-structure, keyed         on result

### Community 132 - "Community 132"
Cohesion: 0.36
Nodes (7): _parse_duration(), build_parser(), _build_mode(), _build_creds(), _main(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 116 - "Community 116"
Cohesion: 0.24
Nodes (7): gate_0_is_passive_profile(), gate_2_host_discovery(), gate_3_port_scan(), gate_5_branch_eligible(), gates.py — precondition functions deciding whether each stage of the workflow ru, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, Does `branch` apply to this host?       - Must be in this profile's allowed deep

### Community 154 - "Community 154"
Cohesion: 0.33
Nodes (3): diff_assets(), report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d, re-scan mode's delta report: what changed between two engagements.

### Community 148 - "Community 148"
Cohesion: 0.38
Nodes (6): looks_like_http(), looks_like_tls(), route_branches(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, For every open port with a banner fact, returns {port: {branches}}     that obse

### Community 71 - "Community 71"
Cohesion: 0.17
Nodes (12): _gather_per_host(), _split_cached(), _port_candidates(), _Sink, _run_passive(), run_engagement(), workflow_engine.py — the async DAG executor. Loops through gates, checks precond, Runs scanner.scan_target(host) across hosts concurrently; the     scanner's own (+4 more)

## Knowledge Gaps
- **624 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+619 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 165`** (1 nodes): `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 166`** (1 nodes): `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (1 nodes): `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (1 nodes): `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 169`** (1 nodes): `Detection validation: attack_timeline, detection_configs, extend detection_resul`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 170`** (1 nodes): `AI engine: llm_outputs table + reviewstatus enum  Revision ID: 0006 Revises: 000`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 171`** (1 nodes): `P3: composite indexes for the hot aggregate + poll query paths.  The dashboard's`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 172`** (1 nodes): `P3-#10: append-only scan_results table (raw facts).  Decouples the (large) raw f`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 137`** (2 nodes): `refresh()`, `create_personal_access_token()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 122`** (1 nodes): `DiscoveryWorker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (1 nodes): `ExploitOrchestrator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 135`** (1 nodes): `GzipRequestMiddleware`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 156`** (2 nodes): `_run_ad_assessment_and_save()`, `_set_job_status()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 173`** (2 nodes): `paginate_query()`, `Returns (items, total). Applies OFFSET/LIMIT to `query`.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 128`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 150`** (1 nodes): `TestNTLMRelayChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 144`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 145`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 151`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 157`** (1 nodes): `TestEDRParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (1 nodes): `TestValidatePayload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (1 nodes): `TestValidateModule`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 147`** (1 nodes): `TestValidateScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 130`** (1 nodes): `TestRequiresApproval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 129`** (1 nodes): `TestMetasploitRPCClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (1 nodes): `TestNucleiExploitRunner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (2 nodes): `TestNmapXMLParser`, `Unit tests for NmapXMLParser.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 158`** (1 nodes): `Cross-validates the pure-Python Debian version comparator against the real `dpkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 162`** (2 nodes): `validateTargets()`, `POST()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (1 nodes): `db_scanner.py — fingerprint database services.  WHY: databases are everywhere on`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 142`** (2 nodes): `nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:`, `# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 143`** (2 nodes): `PortScanner`, `port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 127`** (2 nodes): `SSHCollector`, `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (2 nodes): `UDPScanner`, `udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 23` to `Community 42`, `Community 57`, `Community 49`, `Community 14`, `Community 34`, `Community 6`, `Community 16`, `Community 0`, `Community 43`, `Community 95`, `Community 101`, `Community 144`, `Community 128`, `Community 150`, `Community 90`, `Community 67`, `Community 37`, `Community 129`, `Community 102`, `Community 130`, `Community 146`, `Community 103`, `Community 147`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Finding` connect `Community 6` to `Community 34`, `Community 99`, `Community 24`, `Community 68`, `Community 8`, `Community 59`, `Community 23`, `Community 16`, `Community 5`, `Community 0`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `FindingStatus` connect `Community 34` to `Community 14`, `Community 23`, `Community 6`, `Community 16`, `Community 0`, `Community 42`, `Community 95`, `Community 101`, `Community 57`, `Community 144`, `Community 49`, `Community 128`, `Community 150`, `Community 90`, `Community 67`, `Community 37`, `Community 129`, `Community 102`, `Community 130`, `Community 146`, `Community 103`, `Community 147`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 127 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 127 INFERRED edges - model-reasoned connections that need verification._
- **Are the 85 inferred relationships involving `FindingStatus` (e.g. with `ADConnectionError` and `ADError`) actually correct?**
  _`FindingStatus` has 85 INFERRED edges - model-reasoned connections that need verification._
- **Are the 70 inferred relationships involving `Finding` (e.g. with `engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS` and `New raw-facts path: detect CVE findings from result['facts'] and persist     the`) actually correct?**
  _`Finding` has 70 INFERRED edges - model-reasoned connections that need verification._
- **Are the 64 inferred relationships involving `Engagement` (e.g. with `ExploitOrchestrator` and `ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is`) actually correct?**
  _`Engagement` has 64 INFERRED edges - model-reasoned connections that need verification._