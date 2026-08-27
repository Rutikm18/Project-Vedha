# Graph Report - .  (2026-08-26)

## Corpus Check
- Large corpus: 996 files · ~866,770 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 9402 nodes · 19075 edges · 493 communities detected
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 2776 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 4048 · calls: 3162 · uses: 2776 · rationale_for: 2470 · method: 2099 · MODIFIES: 1689 · ON_BRANCH: 1400 · imports: 541 · imports_from: 496 · inherits: 252 · PARENT_OF: 142


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 996 · Candidates: 2270
- Excluded: 441 untracked · 64467 ignored · 10 sensitive · 1 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `0236a60`
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

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (63): Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19, Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202, Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R, Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000, Detection validation: attack_timeline, detection_configs, extend detection_resul, AI engine: llm_outputs table + reviewstatus enum  Revision ID: 0006 Revises: 000, P3: composite indexes for the hot aggregate + poll query paths.  The dashboard's, P3-#10: append-only scan_results table (raw facts).  Decouples the (large) raw f (+55 more)

### Community 0 - "Community 0"
Cohesion: 0.01
Nodes (150): Transactional outbox for durable background work (detection, etc.).  Producers i, Temporal detection: detection_runs table + finding provenance columns.  Records, Job leasing: scan_jobs.lease_expires_at for the dead-probe reaper.  A claimed (r, Agentic AI advisor: agent_recommendations (recommend-only, human-approved).  Sto, Add agents.public_key (Phase-4 X25519 identity for scope encryption).  The probe, VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal, _authenticate(), login() (+142 more)

### Community 455 - "Community 455"
Cohesion: 0.50
Nodes (1): Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises

### Community 6 - "Community 6"
Cohesion: 0.02
Nodes (32): Add is_active to users and tenants; add password_expires_at to users.  All exist, Add fenced execution attempts for agent-dispatched scan jobs.  Revision ID: 0017, Add Manager-approved device-key probe enrollment and Site policy.  Revision ID:, Client portal slug — the customer's stable 'user as domain' handle.  Adds users., Single source of truth for the deployed application version.  The value is injec, Product-boundary tests for the single-dashboard Manager API., TestHashHelpers, TestFirstDeployment (+24 more)

### Community 456 - "Community 456"
Cohesion: 0.50
Nodes (1): Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision

### Community 457 - "Community 457"
Cohesion: 0.50
Nodes (1): Finding verification verdict columns (P2 passive verification).  Revision ID: 00

### Community 458 - "Community 458"
Cohesion: 0.50
Nodes (1): Approval-gated safe active-validation requests (P3).  Revision ID: 0022 Revises:

### Community 24 - "Community 24"
Cohesion: 0.04
Nodes (21): Customer portal foundation (Part 2, Phase 0): client role, engagement↔agent assi, Service exposure: persist the exposure_matrix reachability verdict.  Adds servic, scan_health_summary(), scan_health.py — turn the probe's per-host scan completeness/health metrics into, Aggregate result['scan_metrics'] into a coverage/health verdict.        degraded, scan_request.py — a customer-initiated, operator-approved request to run a scan, record_audit(), audit.py — the append-only audit-log writer, shared by the operator and portal r (+13 more)

### Community 440 - "Community 440"
Cohesion: 0.40
Nodes (2): Device-role inventory: persist the probe device_classifier's role on assets.  Ad, # NOTE: Postgres cannot DROP a single enum value; the added 'printer' /

### Community 459 - "Community 459"
Cohesion: 0.50
Nodes (1): Scan-request targets + intensity — the rich customer scan request.  Adds two nul

### Community 460 - "Community 460"
Cohesion: 0.50
Nodes (1): Remediation plans — cached, OS-specific, structured remediation for a finding.

### Community 461 - "Community 461"
Cohesion: 0.50
Nodes (1): SLA policies — per-tenant custom remediation windows (hours per severity).  One

### Community 462 - "Community 462"
Cohesion: 0.50
Nodes (1): Integrations — per-tenant notification config (email / Slack / Jira).  One row p

### Community 463 - "Community 463"
Cohesion: 0.50
Nodes (1): scan_requests.use_case_id — the capability use-case a customer requested.  The p

### Community 144 - "Community 144"
Cohesion: 0.19
Nodes (7): CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, _FakeAttr, _FakeEntry, _enum_with_entries(), TestLDAPEnumeratorParsing, Unit tests for the Active Directory assessment module (Prompt 5).  All directory

### Community 218 - "Community 218"
Cohesion: 0.22
Nodes (6): ADCSChecker, Read pKICertificateTemplate objects from the Configuration NC., Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM

### Community 138 - "Community 138"
Cohesion: 0.13
Nodes (10): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., ADAssessmentRunner, ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu (+2 more)

### Community 160 - "Community 160"
Cohesion: 0.13
Nodes (7): BloodHoundCollector, Run bloodhound-python and return the list of produced JSON file paths.         R, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., TestBuildADFinding

### Community 59 - "Community 59"
Cohesion: 0.12
Nodes (23): ADConnectionError, DependencyMissingError, severity_from_str(), build_ad_finding(), ADUser, ADComputer, ADGroup, ACE (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (94): ADError, Shared building blocks for the Active Directory assessment module.  Every AD che, Base class for Active Directory assessment errors., Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., Assemble a Finding-compatible dict.      All findings carry — as required by the, engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, ServiceFingerprint (+86 more)

### Community 114 - "Community 114"
Cohesion: 0.15
Nodes (11): Exception, MetasploitRPCError, MetasploitRPCClient, Async Metasploit RPC client using msgpack-over-HTTPS., Authenticate with msfrpcd and store the session token., module_type: exploit | auxiliary | payload | post | encoder         Returns list, Execute a Metasploit module.         Returns job_id as string., Returns {status, output, uuid}. (+3 more)

### Community 107 - "Community 107"
Cohesion: 0.14
Nodes (15): KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline, Enumerate kerberoastable accounts and capture TGS evidence., Returns user accounts that have a servicePrincipalName set (and are not, Request a TGS for ``spn`` and return the $krb5tgs$ hash string for offline, Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., One aggregate Finding for all kerberoastable accounts.         Severity is Criti, LDAPEnumerator (+7 more)

### Community 186 - "Community 186"
Cohesion: 0.14
Nodes (6): NTLMRelayChecker, Probe SMB/LDAP signing posture across a host list., For each IP, returns {signing_enabled, signing_required}.          A host is rel, Returns True if the DC *enforces* LDAP signing / channel binding.          We at, Build a Finding for hosts missing SMB signing. The attack_narrative         incl, TestASREPRoastChecker

### Community 128 - "Community 128"
Cohesion: 0.18
Nodes (8): AgentUnavailableError, AgentDecisionEngine, _tool_result(), _val(), _maybe_uuid(), _maybe_decimal(), Raised when the Anthropic SDK or API key is not configured., agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag

### Community 87 - "Community 87"
Cohesion: 0.09
Nodes (23): RuntimeError, StartupValidationError, Raised when a required configuration invariant is violated at boot., _printable_strings(), _device_hint(), PassiveListenerError, _open_listener(), _listener_error_code() (+15 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (103): agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Bump severity one rung when the finding's service is internet-reachable     (Ser, GraphBuilder — turns engagement assets/services/findings into an attack graph., Normalise a value that may be an Enum, str, or None to a lowercase str., Edge cost for an EXPLOITS edge. Derived from the CVSS Attack Complexity     comp, Build the full multi-type attack graph. Returns the populated DiGraph         (a, For each exploitable finding add an EXPLOITS edge Finding→Asset with         ``w (+95 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (54): HallucinationGuard, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide., Run all relevant checks and return a combined verdict:         ``{valid, issues,, LLMUnavailableError, LLMReportGenerator, _enum() (+46 more)

### Community 417 - "Community 417"
Cohesion: 0.40
Nodes (3): run_verification(), verification_graph.py — optional LangGraph orchestration for passive verificatio, Run passive verification. Uses the LangGraph StateGraph when available;     othe

### Community 77 - "Community 77"
Cohesion: 0.09
Nodes (29): VedhaAuthError, AuthenticationError, UserNotFoundError, PasswordMismatchError, DisabledUserError, DisabledTenantError, ExpiredPasswordError, BcryptFailureError (+21 more)

### Community 303 - "Community 303"
Cohesion: 0.31
Nodes (7): _now(), create_access_token(), create_device_access_token(), create_refresh_token(), Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation.

### Community 108 - "Community 108"
Cohesion: 0.09
Nodes (19): _is_public_enrollment_request(), agent_jwt_path_allows(), TenantIsolationMiddleware, BaseHTTPMiddleware, Least-privilege route allowlist for legacy probe access JWTs.      This is the i, Extracts JWT from Authorization header and injects tenant_id + user     claims i, GzipRequestMiddleware, _service_root() (+11 more)

### Community 349 - "Community 349"
Cohesion: 0.48
Nodes (5): new_pat_token(), hash_pat_token(), pat_display_prefix(), validate_pat_scopes(), build_personal_access_token()

### Community 163 - "Community 163"
Cohesion: 0.15
Nodes (16): assert_client(), resolve_scope(), client_scoped(), require_client(), scoped_engagement(), portal_scope.py — the customer-portal authorization boundary.  Every customer-po, Return the client's bound engagement id, or 403.      403 (never 404) is deliber, The safe engagement id to filter by.      A caller-supplied engagement_id is hon (+8 more)

### Community 78 - "Community 78"
Cohesion: 0.11
Nodes (24): CheckResult, DiagnosticsReport, StartupAbortError, _check_database(), _check_redis(), _check_jwt_secret(), _check_bcrypt(), _check_admin_account() (+16 more)

### Community 418 - "Community 418"
Cohesion: 0.40
Nodes (3): Settings, BaseSettings, get_settings()

### Community 348 - "Community 348"
Cohesion: 0.29
Nodes (7): close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, CurrentUser, Parsed from JWT claims — attached to request.state and injected as dependency., Parsed from JWT claims — attached to request.state and injected as dependency.

### Community 351 - "Community 351"
Cohesion: 0.33
Nodes (6): should_escalate(), ValidationOutcome, interpret_validation(), active_validation.py — manager-side decision core for safe active validation.  P, True iff this finding warrants an approval-gated active re-check.     Escalate o, Map a probe safe-check result to a verdict transition. Anything that isn't     a

### Community 122 - "Community 122"
Cohesion: 0.13
Nodes (15): _is_domain_controller(), _is_network_device(), _HostSignals, _group(), _ntlm_relay(), _legacy_windows(), _exposed_db_unauth(), _snmp_public_lateral() (+7 more)

### Community 141 - "Community 141"
Cohesion: 0.18
Nodes (9): DetectionResultDTO, _host_matches(), DetectionCorrelator, _aware(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale, Normalise naive datetimes to UTC so comparisons never raise., SigmaRuleGenerator, _stable_rule_id() (+1 more)

### Community 199 - "Community 199"
Cohesion: 0.19
Nodes (5): AttackAction, DetectionGap, TestEDRParsing, TestSplunkIntegration, Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc

### Community 113 - "Community 113"
Cohesion: 0.14
Nodes (10): EDRDetection, _parse_dt(), EDRQueryEngine, CrowdStrikeFalcon, MicrosoftDefender, SentinelOne, EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender, Falcon: query detection IDs then fetch their summaries.     config: {base_url, t (+2 more)

### Community 91 - "Community 91"
Cohesion: 0.08
Nodes (26): _vuln_db_meta(), _ensure_importable(), detect_findings_from_facts(), _apply_regression_reopen(), _find_remediated_match(), _stamp_verification(), _engagement_device_roles(), _persist_attack_paths() (+18 more)

### Community 380 - "Community 380"
Cohesion: 0.40
Nodes (5): _results_from_scan_rows(), recompute_fused_exposure(), exposure_fusion_service.py — apply multi-probe vantage fusion to Service rows., Reconstruct one {"exposure": [...]} dict per probe from persisted facts.      Ea, Fuse all probes' exposure_matrix observations for an engagement and stamp     th

### Community 352 - "Community 352"
Cohesion: 0.33
Nodes (4): AttackLogger, _as_uuid(), AttackLogger — records every attack action to the ``attack_timeline`` table.  Al, Persist a single attack action. Returns the AttackTimeline row.          ``times

### Community 276 - "Community 276"
Cohesion: 0.27
Nodes (9): composite_risk_score(), _strongest_exposure(), _load_offline_kev_epss(), prioritize_engagement_findings(), prioritization.py — the single risk-scoring engine for ALL findings.  WHY THIS E, The unified 0-1000 composite (see module docstring). Pure + deterministic., The most-exposed value among an asset's services (external beats internal)., (kev_db, epss_db) from the pinned snapshots, or (None, None) if the     detectio (+1 more)

### Community 187 - "Community 187"
Cohesion: 0.17
Nodes (14): host_of(), build_coverage(), resolution_threshold(), ResolutionOutcome, decide_resolution(), evaluate_resolutions(), apply_manual_reopen(), resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c (+6 more)

### Community 96 - "Community 96"
Cohesion: 0.13
Nodes (11): SIEMAlert, _parse_dt(), SIEMQueryEngine, SplunkSIEM, SentinelSIEM, ElasticSIEM, SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic, Abstract SIEM connector. (+3 more)

### Community 277 - "Community 277"
Cohesion: 0.31
Nodes (9): _is_external(), _collect(), _verdict(), fuse_exposure_results(), fused_service_exposure(), vantage_fusion.py — fuse the exposure_matrix results of MULTIPLE probes.  A sing, (ip → {(proto,port): {vantage: status}}, ip → set(vantages))., Fuse several probes' exposure_matrix results into one per-target matrix.      `r (+1 more)

### Community 278 - "Community 278"
Cohesion: 0.31
Nodes (9): VerificationVerdict, _int_confidence(), compute_verdict(), _qualifies_for_llm(), verify_finding(), verification.py — normalized, dashboard-facing verification verdict.  The determ, Deterministic passive verdict from a detection finding's evidence dict., Only spend an LLM call where a rationale / FP-triage is worth it:     uncertain (+1 more)

### Community 381 - "Community 381"
Cohesion: 0.40
Nodes (5): asset_type_for(), device_profiles(), device_profile.py — map a probe device_inventory result onto asset fields.  The, The AssetType for a classifier device_type, or None to keep the existing., ip → {asset_type, device_role, role_detail, role_confidence} from a probe     de

### Community 382 - "Community 382"
Cohesion: 0.33
Nodes (5): service_exposure(), escalate_for_exposure(), exposure.py — reachability-aware risk from the probe's exposure_matrix use-case., (ip, proto, port) → exposure verdict, from a probe exposure_matrix result., Bump a finding one severity rung when its service is internet-reachable.      On

### Community 221 - "Community 221"
Cohesion: 0.23
Nodes (12): _map_severity(), _resolve_asset(), _finding_port(), _escalate_by_exposure(), _find_open_duplicate(), create_findings_from_probe_result(), create_scan_health_finding(), Find the Asset for a probe-reported target IP, creating a minimal one if needed. (+4 more)

### Community 62 - "Community 62"
Cohesion: 0.11
Nodes (15): RateLimiter, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim, ServiceIdentifier, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner, Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr (+7 more)

### Community 279 - "Community 279"
Cohesion: 0.29
Nodes (9): _new_finding(), _ssh_rules(), _http_rules(), _cleartext_rule(), create_service_vuln_findings(), service_vuln.py — turn network-service banner facts into Finding rows.  WHY THIS, SSH hygiene findings the CVE engine does NOT cover.      Outdated-version → CVE, Findings for an HTTP service, from its Server header / banner. (+1 more)

### Community 74 - "Community 74"
Cohesion: 0.09
Nodes (24): NucleiExploitRunner, Run Nuclei CVE PoC templates against a single target.     Every template is safe, Parse template YAML and validate it contains no write/delete/DoS actions., Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc, Parse nuclei JSONL output for a single CVE PoC result., SafetyViolationError, validate_payload(), validate_module() (+16 more)

### Community 33 - "Community 33"
Cohesion: 0.19
Nodes (36): ExploitOrchestrator, ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is, Coordinates safe exploit validation runs:       1. Safety validation (payload al, Returns {module, payload, safe_check} for the given finding.         Priority: C, Raises SafetyViolationError if module or payload is not permitted., Raises OutOfScopeError if target_ip not in engagement scope., Full exploit execution pipeline with safety, scope, blast radius,         audit, Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo (+28 more)

### Community 147 - "Community 147"
Cohesion: 0.16
Nodes (9): PathAnalyzer, _safe_float(), _priority(), Best (easiest) exploitable finding on an asset: {cvss, weight, finding}., Build (and cache) the Asset→Asset movement projection. Edge weight is the, Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for, Assets that appear in more than ``threshold`` (default 50%) of all paths — (+1 more)

### Community 178 - "Community 178"
Cohesion: 0.28
Nodes (8): asset_node_id(), service_node_id(), finding_node_id(), _enum_value(), _to_float(), exploit_complexity(), is_internet_exposed(), GraphBuilder

### Community 129 - "Community 129"
Cohesion: 0.14
Nodes (9): DemoAsset, DemoService, DemoFinding, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, TestGraphVisualizer, TestNeo4jClient (+1 more)

### Community 383 - "Community 383"
Cohesion: 0.33
Nodes (3): Apply constraints + indexes (idempotent)., Run a Cypher statement and return records as dicts. [] if not connected., Run a parametrised write with UNWIND batching for bulk node/edge loads.

### Community 353 - "Community 353"
Cohesion: 0.29
Nodes (5): _deterministic_layout(), GraphVisualizer, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (80): test_portal_remediation.py — Section 6: the customer-facing remediation route., user_agent(), probe_payload(), choose_source_port(), jittered_delay(), assess_tarpit(), inet_checksum(), resolve() (+72 more)

### Community 75 - "Community 75"
Cohesion: 0.09
Nodes (16): str, UserRole, AssetCriticality, parse_csv_assets(), Parse CSV text into a list of AssetIn models and error strings., TTLCache, OrderedDict, LRU + TTL eviction. Expired keys are purged on access; when ``maxsize``     is e (+8 more)

### Community 21 - "Community 21"
Cohesion: 0.07
Nodes (45): Base, TimestampMixin, AgentRecommendation, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., AttackTimeline, Append-only ledger of every attack action performed during an engagement.      W, Base, DeclarativeBase (+37 more)

### Community 37 - "Community 37"
Cohesion: 0.07
Nodes (35): BaseModel, AssetIn, AssetOut, BulkAssetImportResult, LoginRequest, TokenResponse, PersonalAccessTokenCreate, PersonalAccessTokenCreated (+27 more)

### Community 285 - "Community 285"
Cohesion: 0.20
Nodes (10): _agent_token_from_websocket(), _claim_pushed_job(), agent_websocket_endpoint(), Read an agent bearer token exclusively from the non-logged auth header., Validate eligibility and atomically claim a WebSocket job offer., Persistent WebSocket for probe → manager push communication.      Authentication, Read an agent bearer token exclusively from the non-logged auth header., Validate eligibility and atomically claim a WebSocket job offer. (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.04
Nodes (66): _job_params_contain_secret(), _resolve_scan_type(), _required_scan_type(), _scope_is_reachable(), _job_reachability_scope(), _agent_can_execute_job(), _normalize_intensity_name(), _encrypt_scope_for_agent() (+58 more)

### Community 387 - "Community 387"
Cohesion: 0.33
Nodes (6): list_intensities(), The numeric scan-hardness scale: 1 light, 2 standard, 3 deep., The numeric scan-hardness scale: 1 light, 2 standard, 3 deep., The numeric scan-hardness scale: 1 light, 2 standard, 3 deep., The numeric scan-hardness scale: 1 light, 2 standard, 3 deep., The numeric scan-hardness scale: 1 light, 2 standard, 3 deep.

### Community 181 - "Community 181"
Cohesion: 0.18
Nodes (13): get_draft(), approve_report(), reject_report(), build_posture_report_section(), _pending_outputs(), _output_out(), _build_engagement_summary(), _run_generation() (+5 more)

### Community 356 - "Community 356"
Cohesion: 0.43
Nodes (5): _sev_str(), _finding_views(), _two_latest_completed_runs(), posture(), Map joined (Finding, Asset.criticality) rows to duck-typed views.

### Community 225 - "Community 225"
Cohesion: 0.36
Nodes (12): list_attack_paths(), get_attack_path(), list_chokepoints(), blast_radius(), attack_graph(), _build_analyzer(), _critical_asset_ids(), _all_paths_to_critical() (+4 more)

### Community 46 - "Community 46"
Cohesion: 0.06
Nodes (40): ClientUserCreate, ClientUserPatch, ClientUserOut, AssignAgentBody, ScanRequestOut, RejectBody, generate_password(), _slugify() (+32 more)

### Community 109 - "Community 109"
Cohesion: 0.13
Nodes (18): _overview_cache_key(), _compute_overview(), _refresh_overview_cache(), _parse_probe_file(), _promote_from_facts(), import_facts(), create_engagement(), engagements_overview() (+10 more)

### Community 191 - "Community 191"
Cohesion: 0.22
Nodes (13): ExploitResultOut, ApprovalOut, run_exploit(), list_exploit_results(), get_exploit_result(), list_approvals(), approve_exploit(), reject_exploit() (+5 more)

### Community 226 - "Community 226"
Cohesion: 0.22
Nodes (12): IntegrationIn, IntegrationOut, _out(), _row(), list_integrations(), put_integration(), delete_integration(), test_integrations() (+4 more)

### Community 131 - "Community 131"
Cohesion: 0.15
Nodes (15): _portal_use_cases(), _enum_val(), portal_engagement(), portal_finding_remediation(), portal_posture(), _metric_finding(), _posture_view(), portal_summary() (+7 more)

### Community 34 - "Community 34"
Cohesion: 0.07
Nodes (40): _secret_hash(), _keyed_hash(), _derive_refresh_secret(), generate_enroll_token(), enroll_token_is_usable(), _decode_public_key(), _verify_signature(), _rate_limit() (+32 more)

### Community 244 - "Community 244"
Cohesion: 0.29
Nodes (11): _tenant_finding(), _cached_plan(), _build_upsert_stmt(), _upsert_plan(), _serialize(), get_remediation(), generate_remediation(), remediation.py — per-finding remediation plans (operator-facing).  Two routes on (+3 more)

### Community 245 - "Community 245"
Cohesion: 0.29
Nodes (11): SlaPolicyOut, SlaPolicyIn, _row(), _windows_of(), resolve_windows(), _out(), _windows_of_named(), get_sla_policy() (+3 more)

### Community 182 - "Community 182"
Cohesion: 0.20
Nodes (15): ValidateRequest, RejectBody, ValidationRequestOut, _roe_allows_active_validation(), _default_check_kind(), _load_finding_and_eng(), _get_request_or_404(), _request_out() (+7 more)

### Community 70 - "Community 70"
Cohesion: 0.15
Nodes (13): AiMessage, AiGenerateRequest, AiProviderStatus, AiStatusResponse, AiGenerateResponse, _is_local_ollama_model(), AiRuntimeError, Runtime (+5 more)

### Community 250 - "Community 250"
Cohesion: 0.23
Nodes (11): classify_action(), RulesOfEngagement, UsageCounters, Decision, _deny(), evaluate_action(), agent_policy.py — the deterministic policy engine for the Autonomous Engagement, Map an action name to its risk tier; unknown actions fail closed. (+3 more)

### Community 390 - "Community 390"
Cohesion: 0.40
Nodes (5): AttemptClaim, claim_job_attempt(), renew_job_attempt(), Atomically claim a pending job and create its fenced attempt ledger row., Renew only the currently installed running attempt/fence.

### Community 206 - "Community 206"
Cohesion: 0.15
Nodes (14): sanitize_jsonb(), result_checksum(), process_job_result(), _apply_device_profile(), _promote_assets(), Recursively strip NUL (U+0000) from every string in a result payload.      Defen, Stable idempotency checksum for one attempt completion payload., Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu (+6 more)

### Community 308 - "Community 308"
Cohesion: 0.22
Nodes (9): _result_network_identities(), _identity_ip(), validate_result_scope(), Return network identities that could create assets or findings.      Scanner-lev, Parse a probe identity as an IP, tolerating common host:port notation., Return result identities outside the job's authoritative IP scope.      Fail clo, Return network identities that could create assets or findings.      Scanner-lev, Parse a probe identity as an IP, tolerating common host:port notation. (+1 more)

### Community 263 - "Community 263"
Cohesion: 0.20
Nodes (7): deliver(), notify_tenant(), enqueue_notification(), notifications.py — deliver a message to a tenant's configured integrations (emai, Send via one integration. True on success; False on any handled failure     (log, Deliver to every ENABLED integration for the tenant. Returns the count sent., Producer API: enqueue a durable notify event (commits with the caller's txn).

### Community 264 - "Community 264"
Cohesion: 0.24
Nodes (10): MetricFinding, _is_closed(), severity_breakdown(), open_closed_counts(), _period(), status_timeline(), portal_metrics.py — pure aggregations for the customer dashboard.  Kept pure (no, Count findings by severity (all five buckets always present, zero-filled).     o (+2 more)

### Community 133 - "Community 133"
Cohesion: 0.17
Nodes (19): FindingView, Scores, _clamp01(), aggregate(), grade_for(), _risk_prob(), _exploit_prob(), compute_scores() (+11 more)

### Community 251 - "Community 251"
Cohesion: 0.23
Nodes (11): os_key(), _text(), _cves(), classify_finding(), _step(), recipe_for_finding(), remediation_kb.py — the deterministic remediation knowledge base.  Pure (no DB,, Normalize an arbitrary OS/target string to a supported KB key.      Public becau (+3 more)

### Community 479 - "Community 479"
Cohesion: 0.67
Nodes (1): risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se

### Community 358 - "Community 358"
Cohesion: 0.38
Nodes (6): _parse_networks(), _expand_requested(), validate_targets_in_scope(), scope_targets.py — the single source of truth for "is this scan target inside th, Expand raw target tokens (IP / CIDR / ``a-b`` range) into networks.      Returns, Return the normalized list of authorized target networks, or ``None``.      * ``

### Community 228 - "Community 228"
Cohesion: 0.21
Nodes (11): _windows(), SlaResult, compute(), default_windows(), summarize(), SLA policy engine.  Turns a severity + "first seen" timestamp into a remediation, Compute the SLA state for one finding. Never raises on missing data.      `windo, The env-configured SLA windows — the fallback when a tenant has no policy. (+3 more)

### Community 326 - "Community 326"
Cohesion: 0.32
Nodes (7): apply_validation_outcome(), looks_like_validation_result(), ingest_validation_result(), validation_ingest.py — turn a probe's safe active-validation result into a findi, Apply a validation verdict to a finding object (pure — no DB/session)., Cheap gate so normal scan submissions never trigger a lookup: a probe     valida, If ``job_id`` belongs to a ValidationRequest, store the result, set its     outc

### Community 43 - "Community 43"
Cohesion: 0.06
Nodes (32): ConnectionManager, GraphWebSocketManager, Manages WebSocket connections with room-based broadcasting., Accept connection and add to room., Remove connection from room., Broadcast message to all connections in a room., Send message to a specific connection., Get number of connected clients in a room. (+24 more)

### Community 300 - "Community 300"
Cohesion: 0.20
Nodes (6): AgentConnectionManager, Tracks WebSocket connections from probes/agents for direct job push.      Each c, Register an agent's WebSocket connection.          If the agent already has a co, Record transport features explicitly advertised by a connected probe., Record transport features explicitly advertised by a connected probe., Register an agent's WebSocket connection.          If the agent already has a co

### Community 299 - "Community 299"
Cohesion: 0.22
Nodes (7): Remove the current registration, optionally only for one socket.          Return, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to the first online agent in the requested tenant.          Returns t, Push a job to a specific agent over WebSocket.          Returns True if the job, Remove an agent's WebSocket registration., Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to the first online connected agent.          Returns the agent_id th

### Community 484 - "Community 484"
Cohesion: 0.67
Nodes (2): Record a heartbeat from an agent., Record a heartbeat from an agent.

### Community 413 - "Community 413"
Cohesion: 0.33
Nodes (4): Deliver a job-push to an agent wherever its socket is connected.          Return, Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job).

### Community 377 - "Community 377"
Cohesion: 0.29
Nodes (5): Subscribe to the push backplane and forward any job whose target agent         i, Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.

### Community 444 - "Community 444"
Cohesion: 0.40
Nodes (4): Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy).

### Community 442 - "Community 442"
Cohesion: 0.40
Nodes (4): Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs.

### Community 464 - "Community 464"
Cohesion: 0.50
Nodes (3): Return idle connected agents belonging to exactly one tenant., Return idle connected agents belonging to exactly one tenant., Return idle connected agents belonging to exactly one tenant.

### Community 443 - "Community 443"
Cohesion: 0.40
Nodes (4): Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Push a job to the first online agent in the requested tenant.          Returns t, Return 'online', 'busy', or 'offline'.

### Community 441 - "Community 441"
Cohesion: 0.40
Nodes (4): Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag

### Community 415 - "Community 415"
Cohesion: 0.47
Nodes (5): Event, _mark_done(), _process(), main(), outbox.py (worker) — durable consumer for the transactional outbox.  Run as its

### Community 485 - "Community 485"
Cohesion: 0.67
Nodes (3): is_stale_processing(), Return whether a claimed event was stranded by a dead worker.      `_claim_batch, Return whether a claimed event was stranded by a dead worker.      `_claim_batch

### Community 469 - "Community 469"
Cohesion: 0.50
Nodes (4): register(), Decorator: bind an async handler to a topic., Decorator: bind an async handler to a topic., Decorator: bind an async handler to a topic.

### Community 466 - "Community 466"
Cohesion: 0.50
Nodes (4): enqueue(), Add an outbox event to the caller's session. Does NOT commit — it commits     at, Add an outbox event to the caller's session. Does NOT commit — it commits     at, Add an outbox event to the caller's session. Does NOT commit — it commits     at

### Community 467 - "Community 467"
Cohesion: 0.50
Nodes (4): _handle_facts_ready(), Run the deterministic detection pipeline on a submitted facts payload.     Re-re, Run the deterministic detection pipeline on a submitted facts payload.     Re-re, Run the deterministic detection pipeline on a submitted facts payload.     Re-re

### Community 340 - "Community 340"
Cohesion: 0.25
Nodes (8): _handle_notify(), _claim_batch(), Fan a notification out to the tenant's enabled email/Slack/Jira integrations., Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means, Fan a notification out to the tenant's enabled email/Slack/Jira integrations., Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means, Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means, Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means

### Community 468 - "Community 468"
Cohesion: 0.50
Nodes (4): _stale_cutoff(), The `locked_at` boundary before which a PROCESSING row is considered dead., The `locked_at` boundary before which a PROCESSING row is considered dead., The `locked_at` boundary before which a PROCESSING row is considered dead.

### Community 465 - "Community 465"
Cohesion: 0.50
Nodes (4): _dead_letter_stale_stmt(), Stranded events that already exhausted their retry budget → dead-letter.     Bou, Stranded events that already exhausted their retry budget → dead-letter.     Bou, Stranded events that already exhausted their retry budget → dead-letter.     Bou

### Community 341 - "Community 341"
Cohesion: 0.29
Nodes (8): _requeue_stale_stmt(), _reclaim_stale(), Stranded events with retry budget left → make due now so a live worker     re-cl, Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat, Stranded events with retry budget left → make due now so a live worker     re-cl, Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat, Stranded events with retry budget left → make due now so a live worker     re-cl, Requeue events a dead worker left in PROCESSING past the lease.      `attempts`

### Community 414 - "Community 414"
Cohesion: 0.33
Nodes (6): _mark_retry_or_dead(), Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus

### Community 445 - "Community 445"
Cohesion: 0.40
Nodes (5): run_worker(), Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so

### Community 173 - "Community 173"
Cohesion: 0.24
Nodes (15): _log(), log_info(), log_warn(), log_error(), _validate_env(), _hash(), _verify_hash(), _detect_drift() (+7 more)

### Community 58 - "Community 58"
Cohesion: 0.09
Nodes (23): CheckResult, ValidationReport, ConfigValidator, SecretsValidator, AppEnvironmentValidator, CorsValidator, CookieValidator, DatabaseURLValidator (+15 more)

### Community 327 - "Community 327"
Cohesion: 0.46
Nodes (7): _ev(), test_high_severity_suspected_escalates_when_roe_allows(), test_kev_escalates_even_if_medium(), test_confirmed_authoritative_does_not_escalate(), test_roe_forbids_blocks_escalation(), test_ot_profile_never_escalates(), test_low_severity_non_kev_does_not_escalate()

### Community 328 - "Community 328"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 391 - "Community 391"
Cohesion: 0.33
Nodes (1): TestNTLMRelayChecker

### Community 265 - "Community 265"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 359 - "Community 359"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 329 - "Community 329"
Cohesion: 0.32
Nodes (3): _boundary_test_client(), test_agent_jwt_is_blocked_before_human_route_handler(), test_human_jwt_still_reaches_human_route_handler()

### Community 480 - "Community 480"
Cohesion: 0.67
Nodes (1): TestAgentWebSocketAuthentication

### Community 481 - "Community 481"
Cohesion: 0.67
Nodes (1): TestJobSecretBoundary

### Community 423 - "Community 423"
Cohesion: 0.40
Nodes (1): TestTenantWebSocketSelection

### Community 422 - "Community 422"
Cohesion: 0.60
Nodes (2): _claim_fixture(), TestAtomicWebSocketClaim

### Community 134 - "Community 134"
Cohesion: 0.17
Nodes (4): TestClassifyAction, _roe(), TestEvaluateAction, test_agent_policy.py — the pure deterministic agent policy engine.

### Community 183 - "Community 183"
Cohesion: 0.21
Nodes (10): _Result, _FakeSession, _asset(), _svc(), test_list_assets_batches_services_no_n_plus_one(), test_list_assets_caps_services_at_30(), test_list_assets_empty_skips_service_query(), Regression tests for AgentDecisionEngine._list_assets service batching.  The rea (+2 more)

### Community 207 - "Community 207"
Cohesion: 0.14
Nodes (6): TestAgentExecutableTypes, TestAgentRegistrationRefresh, TestHeartbeat, TestLegacyBootstrap, TestAccessTokenExpiry, Unit tests for the agent/probe protocol changes:   * agent polling is restricted

### Community 230 - "Community 230"
Cohesion: 0.35
Nodes (4): _user(), _redis(), TestEnqueueAgentJob, TestOTProfileGate

### Community 424 - "Community 424"
Cohesion: 0.40
Nodes (1): TestGetAgentJobs

### Community 253 - "Community 253"
Cohesion: 0.17
Nodes (1): TestAgentJobCompatibility

### Community 482 - "Community 482"
Cohesion: 0.67
Nodes (1): TestListAgents

### Community 252 - "Community 252"
Cohesion: 0.17
Nodes (9): TestRegisterAgent, Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup. (+1 more)

### Community 229 - "Community 229"
Cohesion: 0.15
Nodes (9): TestPromoteAssets, Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate (+1 more)

### Community 153 - "Community 153"
Cohesion: 0.20
Nodes (15): _ids(), _get(), test_ntlm_relay_medium_when_only_signing_not_required(), test_ntlm_relay_high_when_smbv1_also_enabled(), test_no_relay_when_signing_required(), test_ntlm_relay_on_domain_controller_is_critical(), test_device_role_from_facts_also_amplifies(), test_legacy_windows_smbv1_plus_rdp() (+7 more)

### Community 287 - "Community 287"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 254 - "Community 254"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 48 - "Community 48"
Cohesion: 0.07
Nodes (16): _make_user(), _make_tenant(), _make_db(), TestAuthenticateUserNotFound, TestAuthenticatePasswordMismatch, TestAuthenticateDisabledUser, TestAuthenticateDisabledTenant, TestAuthenticateExpiredPassword (+8 more)

### Community 95 - "Community 95"
Cohesion: 0.15
Nodes (12): _operator(), _mock_db(), _added(), TestBuildScanJob, TestProvisionClientUser, _pending_request(), TestApproveScanRequest, TestRejectScanRequest (+4 more)

### Community 330 - "Community 330"
Cohesion: 0.54
Nodes (7): _operator(), _db(), _user(), test_reveal_returns_decrypted_password(), test_reveal_null_ciphertext_returns_none(), test_reveal_missing_user_is_404(), test_customer_reveal.py — operator reveal of a customer login password (item 1).

### Community 192 - "Community 192"
Cohesion: 0.22
Nodes (2): _action(), TestDetectionCorrelator

### Community 362 - "Community 362"
Cohesion: 0.29
Nodes (1): TestSigmaRuleGenerator

### Community 394 - "Community 394"
Cohesion: 0.33
Nodes (1): TestSIEMParsing

### Community 331 - "Community 331"
Cohesion: 0.25
Nodes (1): test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure

### Community 395 - "Community 395"
Cohesion: 0.60
Nodes (5): _user(), _scalars(), test_list_jobs_returns_results(), test_list_assets_groups_services(), Unit tests for the dashboard list endpoints (jobs + assets).

### Community 255 - "Community 255"
Cohesion: 0.17
Nodes (1): test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper

### Community 231 - "Community 231"
Cohesion: 0.29
Nodes (4): _finding(), _engagement(), TestExploitOrchestrator, pytest_addoption()

### Community 268 - "Community 268"
Cohesion: 0.18
Nodes (1): TestValidatePayload

### Community 363 - "Community 363"
Cohesion: 0.29
Nodes (1): TestValidateModule

### Community 364 - "Community 364"
Cohesion: 0.29
Nodes (1): TestValidateScope

### Community 333 - "Community 333"
Cohesion: 0.25
Nodes (1): TestRequiresApproval

### Community 332 - "Community 332"
Cohesion: 0.43
Nodes (1): TestMetasploitRPCClient

### Community 267 - "Community 267"
Cohesion: 0.18
Nodes (1): TestNucleiExploitRunner

### Community 365 - "Community 365"
Cohesion: 0.29
Nodes (1): test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.

### Community 366 - "Community 366"
Cohesion: 0.48
Nodes (6): _base(), test_risk_rank_is_computed_not_none(), test_confirmed_exploited_outranks_contradicted(), test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), FindingOut computes the explainable risk_rank at serialization (P4 Task 5 wiring

### Community 448 - "Community 448"
Cohesion: 0.83
Nodes (3): _db_with(), test_reopen_remediated_finding_sets_open_and_audits(), test_reopen_non_remediated_is_conflict()

### Community 289 - "Community 289"
Cohesion: 0.36
Nodes (5): _operator(), _db(), TestPutIntegration, TestListIntegrations, test_integrations.py — operator notification-integration config (item 3).

### Community 154 - "Community 154"
Cohesion: 0.15
Nodes (8): _cloud(), test_default_auto_detects_the_configured_cloud_provider(), test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter(), test_default_runtime_fails_closed_without_any_cloud_key(), test_generate_fails_closed_when_no_cloud_provider_configured(), test_fallback_never_includes_local_ollama(), test_status_fails_safe_without_cloud_key(), Settings with provider unset and all cloud keys pinned, so .env cannot     leak

### Community 256 - "Community 256"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_running(), test_poll_status_completed()

### Community 309 - "Community 309"
Cohesion: 0.22
Nodes (3): TestDeliver, TestNotifyTenant, test_notifications.py — integration delivery fan-out (item 3 delivery worker).

### Community 117 - "Community 117"
Cohesion: 0.11
Nodes (6): _ScalarResult, _NestedTransaction, _FakeSession, _SessionFactory, test_fatal_nuclei_error_marks_background_job_failed(), test_partial_nuclei_run_preserves_findings_and_diagnostics()

### Community 235 - "Community 235"
Cohesion: 0.26
Nodes (7): _finding_line(), FakeProcess, test_run_scan_streams_jsonl_and_separates_timeouts(), test_nonzero_exit_without_findings_raises_with_stderr(), test_nonzero_exit_retains_and_marks_partial_findings(), test_timeout_retains_findings_emitted_before_termination(), test_template_initialization_failure_cannot_be_clean_zero()

### Community 184 - "Community 184"
Cohesion: 0.25
Nodes (15): _sql(), _now(), test_fresh_processing_lock_is_not_reclaimed(), test_expired_processing_lock_is_reclaimed(), test_boundary_at_exactly_the_lease_is_reclaimed(), test_pending_and_done_rows_are_never_reclaimed(), test_missing_locked_at_is_not_reclaimed(), test_stale_cutoff_is_now_minus_lease() (+7 more)

### Community 236 - "Community 236"
Cohesion: 0.22
Nodes (5): _f(), TestSeverityBreakdown, TestOpenClosed, TestStatusTimeline, test_portal_metrics.py — pure dashboard aggregations.

### Community 42 - "Community 42"
Cohesion: 0.10
Nodes (22): _client(), _operator(), _db_list(), _db_scalar(), _finding_with_internal(), TestClientFindingWhitelist, TestPortalFindings, TestPortalReports (+14 more)

### Community 311 - "Community 311"
Cohesion: 0.44
Nodes (5): _client(), _finding(), _db_scalar(), TestPortalRemediation, Each db.execute(...) → result whose .scalar_one_or_none() is the next val.

### Community 143 - "Community 143"
Cohesion: 0.15
Nodes (7): _client(), _operator(), TestAssertClient, TestResolveScope, TestClientScoped, TestPortalTokenClaims, test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping au

### Community 175 - "Community 175"
Cohesion: 0.15
Nodes (7): _fv(), test_compute_scores_uses_risk_epss_exploit_and_asset_criticality(), test_build_posture_single_run_has_no_prev(), test_build_posture_buckets_resolved_new_persisting(), _Row, test_finding_views_maps_columns_and_asset_criticality(), test_finding_views_handles_null_asset_and_scores()

### Community 402 - "Community 402"
Cohesion: 0.33
Nodes (1): test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.  T

### Community 272 - "Community 272"
Cohesion: 0.20
Nodes (2): _token(), test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()

### Community 273 - "Community 273"
Cohesion: 0.24
Nodes (5): _db_names(), TestNextProbeName, TestSimpleApproveInput, test_probe_simple_approve.py — one-click probe approval helpers (item 5)., db.execute(...).scalars().all() → the given agent-name list.

### Community 451 - "Community 451"
Cohesion: 0.83
Nodes (3): _objects(), test_expired_attempt_requeues_with_fence_history_preserved(), test_expired_attempt_fails_job_when_retry_budget_is_exhausted()

### Community 100 - "Community 100"
Cohesion: 0.10
Nodes (6): _finding(), TestParseJsonResponse, TestSafeCommands, TestNormalizeAiPlan, TestGenerateRemediationPlan, test_remediation_generator.py — Section 3: the AI remediation-plan helpers.  Pur

### Community 176 - "Community 176"
Cohesion: 0.18
Nodes (5): _f(), TestClassify, TestRecipeShape, TestRecipeForFinding, test_remediation_kb.py — the pure deterministic remediation knowledge base.

### Community 66 - "Community 66"
Cohesion: 0.11
Nodes (16): _operator(), _finding(), _db_scalar(), _scalar_result(), _one_result(), _returning_row(), _FakeDB, _GenUnavailable (+8 more)

### Community 433 - "Community 433"
Cohesion: 0.60
Nodes (4): _stmt(), _run(), test_upsert_resets_gate_and_is_race_safe(), test_remediation_upsert_integration.py — real-Postgres verification of the remed

### Community 404 - "Community 404"
Cohesion: 0.73
Nodes (5): _finding(), _db_returning(), test_covered_clean_medium_finding_is_auto_resolved(), test_uncovered_finding_is_left_open(), test_db_version_change_blocks_resolution()

### Community 313 - "Community 313"
Cohesion: 0.39
Nodes (7): _rank(), test_bounds(), test_confirmed_exploitable_outranks_contradicted(), test_contradicted_sinks_below_inferred(), test_kev_raises_rank(), test_internet_facing_raises_and_auth_lowers(), test_low_confidence_lowers_rank()

### Community 339 - "Community 339"
Cohesion: 0.36
Nodes (5): _summary(), test_clean_scan_is_healthy_and_does_not_warn(), test_local_resource_errors_flag_degraded(), test_missing_ports_flag_incomplete(), test_scan_health.py — the probe scan-metrics → coverage/health verdict.  Guards

### Community 90 - "Community 90"
Cohesion: 0.07
Nodes (8): TestNoScopeAuthorizesNothing, TestTargetsWithinScope, TestOutOfScopeIsRejected, TestExclusions, TestIpVersionSafety, test_property_every_accepted_target_is_subnet_of_scope(), test_scope_targets.py — the pure scope-authorization core shared by the dispatch, Whatever the validator accepts must be provably inside the scope.

### Community 407 - "Community 407"
Cohesion: 0.33
Nodes (1): TestValidateEnv

### Community 158 - "Community 158"
Cohesion: 0.21
Nodes (1): TestServiceIdentifier

### Community 215 - "Community 215"
Cohesion: 0.26
Nodes (7): _finding(), TestPolicyAwareCompute, _operator(), _db(), _row(), TestSlaPolicyRoutes, test_sla_policy.py — per-tenant custom SLA windows (item 4).

### Community 298 - "Community 298"
Cohesion: 0.44
Nodes (9): _exec(), _mock_db(), _user(), test_create_request_is_pending_and_derives_tls_check(), test_create_rejected_when_roe_forbids(), test_approve_enqueues_safe_validate_job(), test_approve_conflict_when_not_pending(), test_reject_marks_rejected() (+1 more)

### Community 258 - "Community 258"
Cohesion: 0.27
Nodes (9): _finding(), test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_without_touching_status(), test_inconclusive_leaves_finding_unchanged(), test_confirmed_never_overrides_human_closed_finding(), _exec(), test_ingest_confirmed_updates_request_and_finding(), test_ingest_unknown_job_is_noop() (+1 more)

### Community 216 - "Community 216"
Cohesion: 0.23
Nodes (11): _probe(), test_external_vantage_open_makes_port_external(), test_internal_only_when_no_external_probe_sees_open(), test_internal_open_does_not_imply_external(), test_ambiguous_when_only_open_filtered(), test_not_exposed_when_closed_everywhere(), test_declared_external_vantage_without_hint_name(), test_single_probe_matches_its_own_verdict() (+3 more)

### Community 118 - "Community 118"
Cohesion: 0.13
Nodes (11): _make_http_mock(), test_fetch_nvd_success(), test_fetch_nvd_caches_result(), test_fetch_epss_success(), test_check_cisa_kev_present(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_fetch_mitre_from_nvd_references() (+3 more)

### Community 274 - "Community 274"
Cohesion: 0.18
Nodes (1): TestNmapXMLParser

### Community 72 - "Community 72"
Cohesion: 0.12
Nodes (20): AIClient, AnthropicAIClient, FakeAIClient, AINormalizerCache, validate_cpe_exists(), extract_raw_text(), propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look (+12 more)

### Community 170 - "Community 170"
Cohesion: 0.15
Nodes (13): Protocol, route_ports(), FunnelResult, _Scanner, _candidate_ports(), _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, Map a host's open ports onto the deep-scanner routes that handle them.     Retur (+5 more)

### Community 379 - "Community 379"
Cohesion: 0.40
Nodes (5): _rec(), _content_hash(), main(), build_nvd_cpe_snapshot.py — generate the NVD/CPE companion vuln snapshot.  WHY A, One OSV-shaped record: affected below `fixed` (NVD versionEndExcluding).

### Community 79 - "Community 79"
Cohesion: 0.08
Nodes (13): wilson_ci(), FindingConsistency, ConsistencyReport, aggregate(), format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen, run_findings: one list of Findings per run (N runs). Aggregated by     the deter (+5 more)

### Community 27 - "Community 27"
Cohesion: 0.09
Nodes (35): dedup_findings(), suppress_negated(), _product_from_cpe(), correlate_smb_patch(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Suppress a suspected/potential (inferred-source) finding when the     SAME host, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp (+27 more)

### Community 29 - "Community 29"
Cohesion: 0.06
Nodes (43): clean_debian_version(), clean_rpm_version(), osv_source_packages(), normalize_banner(), normalize_web(), normalize_db(), _parse_package_lines(), normalize_credentialed_packages() (+35 more)

### Community 80 - "Community 80"
Cohesion: 0.10
Nodes (18): enrich_finding(), _compute_priority(), enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier., Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr, Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li, KevDB, EpssDB, _clear_caches() (+10 more)

### Community 40 - "Community 40"
Cohesion: 0.07
Nodes (16): _fact(), TestExtractRawText, TestFakeAIClient, TestAINormalizerCache, TestProposeCandidates, Tests for ai_normalizer.py — 0% prior coverage.  Covers:   - extract_raw_text: p, ssh_inventory facts have no banner-style text for the AI to normalise., Any exception from the AI client yields [] — never raises, never         blocks (+8 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (10): _candidate(), _mock_vuln_db(), _mock_kev_db(), _mock_epss_db(), TestMatchCandidate, TestSuppressNegated, TestEnrichFinding, TestKevDb (+2 more)

### Community 86 - "Community 86"
Cohesion: 0.11
Nodes (9): _fact(), TestAsset, TestFactRef, TestCorrelateSmbPatch, TestNormalizeBanner, TestNormalizeDb, TestNormalize, EvidenceTier (+1 more)

### Community 36 - "Community 36"
Cohesion: 0.08
Nodes (7): _finding(), TestDedupFindings, TestClassifyTier, TestVerify, TestComputePriority, TestFindingConsistency, TestAggregate

### Community 361 - "Community 361"
Cohesion: 0.29
Nodes (1): TestIngestFile

### Community 393 - "Community 393"
Cohesion: 0.33
Nodes (1): TestCvss

### Community 266 - "Community 266"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 360 - "Community 360"
Cohesion: 0.29
Nodes (1): TestDeceptionScore

### Community 38 - "Community 38"
Cohesion: 0.06
Nodes (33): TestWilsonCi, _default_products(), _content_hash(), SnapshotMeta, VulnDB, _clear_caches(), _boundary_versions(), _read_snapshot() (+25 more)

### Community 71 - "Community 71"
Cohesion: 0.07
Nodes (15): _valid_snapshot(), _write_snapshot(), _valid_kev(), _valid_epss(), TestLoadSnapshotErrors, TestLoadKevErrors, TestLoadEpssErrors, Tests for loader error paths in vuln_db.py and enrichment_db.py.  These are the (+7 more)

### Community 155 - "Community 155"
Cohesion: 0.14
Nodes (14): test_dpkg_compare_does_not_call_the_binary(), clean_guard_cache(), test_guard_is_noop_without_dpkg(), test_guard_reports_divergence_and_warns(), _write_snapshot(), test_load_snapshot_memoized_returns_same_instance(), test_load_snapshot_reloads_after_file_change(), test_clear_caches_forces_reload() (+6 more)

### Community 41 - "Community 41"
Cohesion: 0.11
Nodes (28): _empty_kev(), _empty_epss(), _mock_vuln_db(), _openssh_vuln_db(), _ssh_inventory_jsonl(), _banner_jsonl(), _empty_jsonl(), TestRunPipelineEmptyInput (+20 more)

### Community 146 - "Community 146"
Cohesion: 0.18
Nodes (17): _ssl_context(), _query_osv(), sync_snapshot(), sync_kev_snapshot(), sync_epss_snapshot(), sync_epss_full(), _all_known_cve_ids(), main() (+9 more)

### Community 73 - "Community 73"
Cohesion: 0.09
Nodes (31): _dpkg_compare_via_binary(), _char_order(), _compare_non_digit(), _split_segments(), _compare_part(), _split_dpkg_version(), has_ambiguous_epoch(), _dpkg_compare_pure_python() (+23 more)

### Community 103 - "Community 103"
Cohesion: 0.09
Nodes (16): Message, AiStatus, Engagement, STARTER_PROMPTS, WELCOME, providerLabel(), AIBrainPage(), AssistantText() (+8 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (92): ApiActivity, GET, GET, GET(), Exposure, GET, ManagerAiResponse, ManagerAiResponse (+84 more)

### Community 50 - "Community 50"
Cohesion: 0.06
Nodes (32): DEMO_FINDINGS, DEMO_ASSETS, ReviewStatus, ReportSection, FindingInput, AssetInput, PriorityFeatures, ShapExplanation (+24 more)

### Community 82 - "Community 82"
Cohesion: 0.08
Nodes (15): DetectionOutcome, AttackAction, ATTACK_TIMELINE, SIEMAlert, EDRDetection, SIEM_ALERTS, EDR_DETECTIONS, DetectionResult (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.03
Nodes (43): Customer, Engagement, ClientUserResp, TabKey, Severity, Engagement, ActivityItem, AssetRow (+35 more)

### Community 419 - "Community 419"
Cohesion: 0.40
Nodes (2): ScanReq, ClientUser

### Community 16 - "Community 16"
Cohesion: 0.04
Nodes (50): Severity, FindingStatus, ExploitMaturity, DetectionCoverage, RemStep, ComplianceRef, RiskBreakdown, KillChainStep (+42 more)

### Community 130 - "Community 130"
Cohesion: 0.14
Nodes (11): DataStateProps, DataState(), center, btn, ApiError, clearAuth(), fetchJson(), isUnauthorized() (+3 more)

### Community 162 - "Community 162"
Cohesion: 0.13
Nodes (8): DashboardCharts(), DashboardGrid(), useMouseGradient(), AgentStatus, Agent, AGENT_STATUS, PATH_STATUS, SEV_LABEL

### Community 18 - "Community 18"
Cohesion: 0.04
Nodes (39): SEVS, SEV_ORDER, ReportContent, PortalReport, Tab, TABS, SEVS, SEV_ORDER (+31 more)

### Community 97 - "Community 97"
Cohesion: 0.09
Nodes (14): INTENSITIES, PHASES, JobMeta, relTime(), prettyType(), JobCard(), NAV, PortalShellProps (+6 more)

### Community 93 - "Community 93"
Cohesion: 0.08
Nodes (16): UseCase, Probe, Engagement, JobStatus, ScannerRun, EngineManifest, UC_META, RISK (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.04
Nodes (44): SESSION_DIR, SESSION_FILE, Session, loadSession(), saveSession(), clearSession(), requireAuth(), serverUrl() (+36 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (136): PROFILE_TOOLS, A, w(), ln(), SEV_COLOR, sevBadge(), LINE, rule() (+128 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (55): A, w(), ln(), ask(), askSecret(), confirm(), choose(), banner() (+47 more)

### Community 67 - "Community 67"
Cohesion: 0.12
Nodes (30): C, ln(), showSpinner(), buildToolsCommand(), InstalledRecord, InstalledManifest, readInstalled(), writeInstalled() (+22 more)

### Community 198 - "Community 198"
Cohesion: 0.22
Nodes (13): client(), commentOnStage(), explainFindings(), suggestAttackPath(), ValidationVerdict, validateFindings(), PhaseId, PhaseRecommendation (+5 more)

### Community 164 - "Community 164"
Cohesion: 0.13
Nodes (10): TimelinePoint, Engagement, ActivityItem, Finding, FindingPage, FindingSummary, SEV, STATUS_STYLE (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.07
Nodes (26): PATCH_PILL, AdvisorFlow(), Msg, Served, ExplainResponse, AssistantDrawer(), AssistantFab(), Ctx (+18 more)

### Community 25 - "Community 25"
Cohesion: 0.06
Nodes (34): Panel(), Meter(), Delta(), Readout(), AgentStatus, Agent, AGENT_STATUS, Exposure (+26 more)

### Community 165 - "Community 165"
Cohesion: 0.15
Nodes (14): SeverityChip(), SlaState, SlaItem, SlaSummary, STATE, timeLabel(), elapsedPct(), deadlineTitle() (+6 more)

### Community 197 - "Community 197"
Cohesion: 0.18
Nodes (12): Rung, RUNG_LABELS, AgentOpts, AgentDeps, requiresApproval(), isBlocked(), runAutonomousEngagement(), AgentState (+4 more)

### Community 92 - "Community 92"
Cohesion: 0.10
Nodes (22): AgentStatus, JobStatus, JobType, KafkaTopic, AgentCapability, Agent, ScanJob, KafkaTopicInfo (+14 more)

### Community 166 - "Community 166"
Cohesion: 0.18
Nodes (15): CaseSeverity, CaseStatus, CaseComment, CaseActivity, Case, DATA_FILE, SLA_HOURS, SEED_CASES (+7 more)

### Community 63 - "Community 63"
Cohesion: 0.09
Nodes (31): DATA_PATH, ClientStatus, ClientJiraConfig, ClientNotifyConfig, ClientSettings, Client, ClientsFile, SEED (+23 more)

### Community 280 - "Community 280"
Cohesion: 0.20
Nodes (8): EngagementStatus, Credential, Engagement, STORE, ACTIVITY, now, FINDINGS_TIMELINE, engagementsStore

### Community 321 - "Community 321"
Cohesion: 0.32
Nodes (7): BUILTIN_PATHS, DirBustResult, ProbeResp, probe(), NativeDirOpts, loadWordlist(), nativeDirBust()

### Community 322 - "Community 322"
Cohesion: 0.32
Nodes (7): DnsReconResult, PtrSweepResult, COMMON_SUBDOMAINS, safe(), nativeDnsRecon(), attemptZoneTransfer(), nativePtrSweep()

### Community 188 - "Community 188"
Cohesion: 0.13
Nodes (12): PayloadType, JobStatus, ApprovalStatus, ExploitEvidence, ExploitResult, ExploitJob, ExploitApprovalRequest, AuditEntry (+4 more)

### Community 81 - "Community 81"
Cohesion: 0.08
Nodes (20): FindingSeverity, NucleiMatch, OpenVASFinding, OpenVASTaskState, taskStore, setTask(), OpenVASHelperOutput, parseOpenVASHelperOutput() (+12 more)

### Community 104 - "Community 104"
Cohesion: 0.09
Nodes (18): NodeType, RelationType, Severity, PathStatus, GNode, GEdge, AttackPath, Chokepoint (+10 more)

### Community 240 - "Community 240"
Cohesion: 0.26
Nodes (7): HttpxJsonRecord, HttpxLineParseResult, isOptionalString(), normalizePort(), isOptionalNumber(), parseHttpxJsonLine(), HttpxJsonlDecoder

### Community 200 - "Community 200"
Cohesion: 0.27
Nodes (13): JOBS_FILE, JobStatus, Job, ensureDir(), readJobs(), writeJobs(), genJobId(), createJob() (+5 more)

### Community 105 - "Community 105"
Cohesion: 0.13
Nodes (20): NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), OPENVAS_CONFIGS, NETEXEC_CHECKS, ValidationResult, OpenVASScanRequest (+12 more)

### Community 319 - "Community 319"
Cohesion: 0.36
Nodes (7): NmapService, NmapScriptResult, NmapHost, parser, toArray(), extractScripts(), parseNmapXml()

### Community 167 - "Community 167"
Cohesion: 0.23
Nodes (16): DATA_PATH, UserRole, PermissionsFile, ensureDir(), read(), write(), getAllUsers(), getUser() (+8 more)

### Community 281 - "Community 281"
Cohesion: 0.27
Nodes (7): RFC1918, validOctets(), isValidTarget(), estimateHostCount(), ParseResult, parseTargets(), COMMON_RANGES

### Community 190 - "Community 190"
Cohesion: 0.23
Nodes (7): classify_os_error(), family_of(), RateLimiter, PortScanner, parse_ports(), main(), Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('

### Community 275 - "Community 275"
Cohesion: 0.20
Nodes (10): _bounded_env_int(), _run_polled_job_with_heartbeats(), Return an integer environment setting constrained to a safe range., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Return an integer environment setting constrained to a safe range., Run an HTTP-claimed job while renewing its manager lease. (+2 more)

### Community 76 - "Community 76"
Cohesion: 0.09
Nodes (31): _is_local_manager_url(), say(), _dbg(), _classify_connection_error(), _manager_reachable(), _wait_for_manager(), _poll_jobs_or_empty(), main() (+23 more)

### Community 416 - "Community 416"
Cohesion: 0.40
Nodes (5): _load_env(), Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience.

### Community 259 - "Community 259"
Cohesion: 0.18
Nodes (11): _job_intent(), _result_summary(), _ws_run_job(), Human label for what a job will actually run — the use-case (real intent),     n, One-line, transparent summary of what a scan actually found so the operator, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort. (+3 more)

### Community 119 - "Community 119"
Cohesion: 0.10
Nodes (21): _run_ws_push_loop(), _ws_stage_job_offer(), _ws_heartbeat_sender(), Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Acknowledge an offer without executing it before claim confirmation., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Persistent WebSocket push loop.      Returns False if WebSocket is unavailable ( (+13 more)

### Community 196 - "Community 196"
Cohesion: 0.14
Nodes (14): _ws_take_confirmed_job(), _load_or_create_identity(), Release a staged job only after the manager confirms its claim., Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Release a staged job only after the manager confirms its claim., Load the probe's X25519 identity from persistent state, or create one.      Retu, Release a staged job only after the manager confirms its claim. (+6 more)

### Community 260 - "Community 260"
Cohesion: 0.18
Nodes (11): _ws_http_poll_fallback(), Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, _ws_flush_spool(), Poll pending jobs even while WS is connected.      This makes result delivery re (+3 more)

### Community 342 - "Community 342"
Cohesion: 0.29
Nodes (7): _flush_spool_over_http(), Retry durable result files using the acknowledged HTTP result path., Retry durable result files using the acknowledged HTTP result path., Run one job while keeping WS status/result frames best-effort., Retry durable result files using the acknowledged HTTP result path., Retry durable result files using the acknowledged HTTP result path., Retry durable result files using the acknowledged HTTP result path.

### Community 219 - "Community 219"
Cohesion: 0.15
Nodes (13): _startup_gauntlet(), _load_or_create_signing_identity(), Run all startup security checks before any network I/O.      Order matters: HW b, Load or atomically create the probe's Ed25519 enrollment identity., Run all startup security checks before any network I/O.      Order matters: HW b, Load or atomically create the probe's Ed25519 enrollment identity., Run all startup security checks before any network I/O.      Order matters: HW b, Load or atomically create the probe's Ed25519 enrollment identity. (+5 more)

### Community 301 - "Community 301"
Cohesion: 0.22
Nodes (9): _check_anti_debug(), Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block (+1 more)

### Community 49 - "Community 49"
Cohesion: 0.14
Nodes (33): CliError, _env(), default_config_path(), normalize_manager_url(), ConfigStore, ManagerClient, split_values(), parse_param_pairs() (+25 more)

### Community 239 - "Community 239"
Cohesion: 0.18
Nodes (3): decode_key(), verify_site_policy(), Verify a Manager-signed policy and return its public key for TOFU pinning.

### Community 15 - "Community 15"
Cohesion: 0.04
Nodes (73): _env_number(), _runtime_manifest(), _error_result(), _scan_method_for(), _string_list(), _targets(), _clamp(), _job_runtime_seconds() (+65 more)

### Community 145 - "Community 145"
Cohesion: 0.17
Nodes (16): LicenseError, host_fingerprint(), short_id(), _b64d(), verify_license(), check_license(), gauntlet(), license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p (+8 more)

### Community 127 - "Community 127"
Cohesion: 0.15
Nodes (18): _scope_file(), _ports_from_env(), _clean(), _port_label(), summarize(), _usage_error(), _parse_args(), _main() (+10 more)

### Community 52 - "Community 52"
Cohesion: 0.07
Nodes (28): ResultSpool, Persists scan results locally and retries failed uploads., Atomically write a result payload to the spool directory.          Returns the s, Check if a spooled result exists for this job., Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result., Move a terminally rejected result out of the retry queue., Attempt to upload a result with retries and local spool as fallback.          Ar (+20 more)

### Community 120 - "Community 120"
Cohesion: 0.10
Nodes (18): JobResult, TaskRunner, Structured result from running one scan job., Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Args:             http_get:       Callback for authenticated GET (from Transport, Execute a complete scan job lifecycle.          Args:             job: Job dict, Submit the result, with spool-and-retry if available., Submit the result, with spool-and-retry if available. (+10 more)

### Community 302 - "Community 302"
Cohesion: 0.22
Nodes (8): _strip_nul(), Recursively remove NUL (U+0000) characters from every string in a payload., Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons

### Community 161 - "Community 161"
Cohesion: 0.13
Nodes (14): TransportError, Raised when a transport operation fails permanently (not retryable)., Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed)., Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed)., Register the probe with the manager.          Args:             name: Probe name, Register using a manager-side shared bootstrap key (no user login needed). (+6 more)

### Community 343 - "Community 343"
Cohesion: 0.29
Nodes (6): DeviceAlreadyEnrolledError, _enrollment_conflict_detail(), The probe's device signing key is already registered as an agent on the     mana, Best-effort extraction of the manager's 409 ``detail`` message., The probe's device signing key is already registered as an agent on the     mana, Best-effort extraction of the manager's 409 ``detail`` message.

### Community 318 - "Community 318"
Cohesion: 0.25
Nodes (7): _sync_directory(), _atomic_write_private_state(), Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets.

### Community 121 - "Community 121"
Cohesion: 0.13
Nodes (11): Transport, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Merge and atomically persist private state while preserving fields., HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Merge and atomically persist private state while preserving fields., HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Merge and atomically persist private state while preserving fields. (+3 more)

### Community 344 - "Community 344"
Cohesion: 0.29
Nodes (6): True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls.

### Community 177 - "Community 177"
Cohesion: 0.13
Nodes (13): Refresh a device token before expiry; legacy identities are unchanged., Generic authenticated GET, returns parsed JSON or None on failure.          Used, Establish an authenticated WebSocket connection to the manager.          Returns, Refresh a device token before expiry; legacy identities are unchanged., Generic authenticated GET, returns parsed JSON or None on failure.          Used, Establish an authenticated WebSocket connection to the manager.          Returns, Refresh a device token before expiry; legacy identities are unchanged., Generic authenticated GET, returns parsed JSON or None on failure.          Used (+5 more)

### Community 378 - "Community 378"
Cohesion: 0.33
Nodes (5): Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True

### Community 345 - "Community 345"
Cohesion: 0.29
Nodes (6): Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce

### Community 346 - "Community 346"
Cohesion: 0.29
Nodes (6): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of

### Community 220 - "Community 220"
Cohesion: 0.15
Nodes (11): Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active. (+3 more)

### Community 347 - "Community 347"
Cohesion: 0.29
Nodes (6): Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket connection URL with auth token.          The token is passe

### Community 10 - "Community 10"
Cohesion: 0.21
Nodes (95): use_cases.py — the finite, pre-defined library of scan scenarios the manager can, 01f4398 feat(probe): IoT survey reaches the banner stage (service_fingerprint), 02b6341 feat(active-validation): pure escalation decision core, 045c9ae fix(posture): normalize run_at in _present_in_run; drop dead scores_prev call; tidy test import, 0510df3 going to build prompt and connection, architecture almost done, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — self-register without admin login, 0d6be85 feat(risk-rank): explainable 0-1000 finding priority (+87 more)

### Community 139 - "Community 139"
Cohesion: 0.11
Nodes (19): _as_int(), use_case_for_code(), normalize_intensity(), resolve(), Coerce an int-or-numeric-string to int, else None (non-numeric)., Map a numeric use-case code → use_case_id (raises on an unknown code)., Accept an intensity as a number (1/2/3) OR a name; return the name.      None st, Return (scan_type, profile, intensity) for a job.      Resolution order:     1. (+11 more)

### Community 85 - "Community 85"
Cohesion: 0.10
Nodes (19): resolve_use_cases(), validate_targets(), target_address_count(), validate_ground_truth(), _metric(), _not_scored(), score_inventory(), Pure helpers for controlled Probe capability and accuracy validation. (+11 more)

### Community 23 - "Community 23"
Cohesion: 0.04
Nodes (23): VA scanner module — pure collection/scanning layer.  Each submodule is an indepe, resolve_profile(), port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD, Resolve a named scan profile to a concrete, de-duplicated port list.      'full', syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).  WH, syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).  WH, test_main_scripts_coverage.py — P0 coverage + self-health capabilities added to, test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model (+15 more)

### Community 201 - "Community 201"
Cohesion: 0.24
Nodes (13): _ratio(), _finding_key(), _expected_keys(), score_findings(), _observed_states(), score_port_states(), evaluate_corpus(), format_report() (+5 more)

### Community 148 - "Community 148"
Cohesion: 0.12
Nodes (6): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples., test_main_scripts_adaptive_timeout.py — Phase 7: per-host adaptive probe timeout

### Community 168 - "Community 168"
Cohesion: 0.14
Nodes (5): interpret_redis_info(), _probe_redis(), DBScanner, db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act

### Community 140 - "Community 140"
Cohesion: 0.13
Nodes (7): BaseScanner, TLSFingerprintScanner, TLSScanner, MobileScanner, Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO, TLSFingerprintScanner, TLSScanner

### Community 98 - "Community 98"
Cohesion: 0.12
Nodes (20): ScanRecord, Delta, _stable_host_id(), _extract_service(), _extract_version(), DeltaEngine, _new_service_severity(), _significant_version_change() (+12 more)

### Community 11 - "Community 11"
Cohesion: 0.05
Nodes (80): Finding, _as_dict(), _scanner(), _data(), _is_open(), build_service_index(), _rule_tls(), _rule_smb() (+72 more)

### Community 83 - "Community 83"
Cohesion: 0.09
Nodes (25): normalize_mac(), is_locally_administered(), vendor_for_mac(), device_hint(), Neighbor, parse_neighbor_line(), read_neighbor(), read_arp_table() (+17 more)

### Community 55 - "Community 55"
Cohesion: 0.07
Nodes (35): _parse_ssdp_headers(), _fetch_upnp_root_desc(), _probe_ssdp_sync(), _decode_mdns_name(), _parse_mdns_response(), _probe_mdns_sync(), _probe_rtsp(), _mqtt_connect() (+27 more)

### Community 169 - "Community 169"
Cohesion: 0.18
Nodes (15): _version_str(), _walk_extensions(), _ext_types(), _selected_alpn(), _alpn_code(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello() (+7 more)

### Community 241 - "Community 241"
Cohesion: 0.23
Nodes (11): oid_to_hex(), _hash_oids(), ja4x_from_oid_lists(), ja4x_from_cert(), ja4x_from_der(), match_suspicious(), DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040, Pure JA4X from the three ordered OID lists (dotted-decimal strings). (+3 more)

### Community 123 - "Community 123"
Cohesion: 0.14
Nodes (16): MasscanRun, _have_masscan(), _run_masscan(), _parse_masscan_json(), _parse_masscan_json_detailed(), _masscan_records_to_results(), _ConnectSweep, run_mass_scan() (+8 more)

### Community 115 - "Community 115"
Cohesion: 0.12
Nodes (13): _NoRedirect, _known_false_positive(), _mcp_oauth_signal(), _auth_shaped_json_body(), _model_count(), MCPAIScanner, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+5 more)

### Community 124 - "Community 124"
Cohesion: 0.13
Nodes (18): _adb_checksum(), _build_adb_cnxn(), _parse_adb_header(), _probe_adb(), _probe_lockdownd(), _build_mdns_query(), _parse_mdns_ptr_names(), _probe_mdns_mobile_sync() (+10 more)

### Community 222 - "Community 222"
Cohesion: 0.18
Nodes (9): NmapExecutionError, _validated_extra_args(), _run_nmap(), _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here., # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree (+1 more)

### Community 189 - "Community 189"
Cohesion: 0.15
Nodes (11): OSError, NmapExecutionError, _validated_extra_args(), _run_nmap(), _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, Actionable subprocess failure; never reinterpret it as zero findings., Allow tuning only; target, script, and output controls stay owned here. (+3 more)

### Community 39 - "Community 39"
Cohesion: 0.06
Nodes (38): _icmp(), build_icmp_echo(), build_icmp_timestamp(), build_icmp_addrmask(), _strip_ip_header(), parse_icmp_reply(), parse_icmp_timestamps(), remote_clock() (+30 more)

### Community 125 - "Community 125"
Cohesion: 0.13
Nodes (15): _printable_strings(), _device_hint(), PassiveListenerError, _open_listener(), _listener_error_code(), _coverage(), PassiveCollector, _is_readable() (+7 more)

### Community 60 - "Community 60"
Cohesion: 0.06
Nodes (24): _family_of(), ScanMetrics, PortScanner, Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Per-target scan accounting — the completeness + self-health record.      It lets, Tally exactly one terminal per-port observation., Requested ports that were never recorded — the silent-skip proof., Ports recorded more than once (a port must get exactly one verdict). (+16 more)

### Community 242 - "Community 242"
Cohesion: 0.23
Nodes (8): build_connection_request(), parse_connection_confirm(), probe_rdp(), RDPScanner, main(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure.

### Community 304 - "Community 304"
Cohesion: 0.39
Nodes (8): _log(), _run_stage(), _read_jsonl(), _open_tcp_ports(), _ports_arg(), main(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl.

### Community 179 - "Community 179"
Cohesion: 0.16
Nodes (12): route_ports(), FunnelResult, _Scanner, _candidate_ports(), _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, The full outcome of funnelling one host. (+4 more)

### Community 282 - "Community 282"
Cohesion: 0.20
Nodes (8): ScanFunnel, build_default_funnel(), Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun

### Community 386 - "Community 386"
Cohesion: 0.33
Nodes (6): classify_os_error(), describe_os_error(), Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc, Full, debuggable classification for attaching to a ScanResult: state,     reason, Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc, Full, debuggable classification for attaching to a ScanResult: state,     reason

### Community 283 - "Community 283"
Cohesion: 0.20
Nodes (6): ScanResult, main_entrypoint(), One observation about one target. Pure fact, no interpretation.      Network-sta, Run a scanner CLI's body with consistent, operator-friendly error handling., One observation about one target. Pure fact, no interpretation.      Network-sta, Run a scanner CLI's body with consistent, operator-friendly error handling.

### Community 180 - "Community 180"
Cohesion: 0.15
Nodes (8): ScopeError, ScopeGuard, Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude)., Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of excluded networks (to build masscan --exclude).

### Community 384 - "Community 384"
Cohesion: 0.33
Nodes (3): RateLimiter, Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second.

### Community 261 - "Community 261"
Cohesion: 0.22
Nodes (5): AdaptiveRateController, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window)., A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window).

### Community 284 - "Community 284"
Cohesion: 0.20
Nodes (9): expand_targets(), ResultWriter, run_cli(), Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Writes ScanResult objects as JSONL to a file and/or stdout., Wire argparse args into a scanner instance and execute it., Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Writes ScanResult objects as JSONL to a file and/or stdout. (+1 more)

### Community 355 - "Community 355"
Cohesion: 0.29
Nodes (3): _UDPProbeProtocol, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi

### Community 354 - "Community 354"
Cohesion: 0.29
Nodes (6): async_udp_probe(), async_udp_probe_retry(), Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de

### Community 385 - "Community 385"
Cohesion: 0.40
Nodes (3): BaseScanner, Subclasses implement `scan_target(self, target)` (async), returning a list     o, Subclasses implement `scan_target(self, target)` (async), returning a list     o

### Community 223 - "Community 223"
Cohesion: 0.18
Nodes (9): _dec(), match_service(), ServiceBannerScanner, Soft-match collected bytes to {service, product, version}; None if unknown., One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown. (+1 more)

### Community 64 - "Community 64"
Cohesion: 0.07
Nodes (29): Enrichment, _dns_read_name(), mdns_hostname(), _nb_encode(), netbios_name(), resolve_hostnames(), tls_info(), tls_accepts_old() (+21 more)

### Community 243 - "Community 243"
Cohesion: 0.23
Nodes (7): _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate(), SMBScanner, smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout

### Community 61 - "Community 61"
Cohesion: 0.11
Nodes (27): _ber_len(), _encode_oid(), _decode_oid(), _decode_value(), _ber_parse(), _parse_varbinds(), _oid_tlv(), _varbind() (+19 more)

### Community 320 - "Community 320"
Cohesion: 0.29
Nodes (2): SSHCollector, ssh_collector.py — credentialed (authenticated) inventory collection for Linux.

### Community 30 - "Community 30"
Cohesion: 0.05
Nodes (42): build_ip_header(), build_tcp_syn(), build_syn_packet(), _parse_mss(), parse_packet(), classify(), syn_cookie(), verify_reply_cookie() (+34 more)

### Community 68 - "Community 68"
Cohesion: 0.09
Nodes (31): _ext(), _sni_extension(), _supported_versions_ext(), _key_share_ext(), build_client_hello(), parse_server_hello(), version_code(), cipher_code() (+23 more)

### Community 202 - "Community 202"
Cohesion: 0.22
Nodes (12): classify_cipher(), grade_tls_posture(), _sni(), _try_version(), _get_cert_der(), _parse_cert_der(), _scan_tls_sync(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only): (+4 more)

### Community 28 - "Community 28"
Cohesion: 0.05
Nodes (38): _ntp_monlist_probe(), _ike_probe(), _sip_probe(), _tftp_probe(), _ipmi_probe(), _ssdp_probe(), _mdns_probe(), interpret_ntp_monlist() (+30 more)

### Community 149 - "Community 149"
Cohesion: 0.14
Nodes (8): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =, _run(), test_unauth_redis_is_critical_and_rce_flagged(), test_unauth_elasticsearch_is_high(), test_protected_redis_raises_no_unauth_finding(), test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive

### Community 150 - "Community 150"
Cohesion: 0.17
Nodes (9): _is_external(), _extract(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, _r(), TestReconcileVantages (+1 more)

### Community 224 - "Community 224"
Cohesion: 0.18
Nodes (7): parse_allow_header(), _NoRedirect, _fetch(), WebScanner, web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only., Read the Allow header from an OPTIONS response. Read-only.

### Community 203 - "Community 203"
Cohesion: 0.20
Nodes (4): _smb_registry_collect(), WindowsCollector, windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus

### Community 204 - "Community 204"
Cohesion: 0.24
Nodes (13): _ratio(), _finding_key(), _expected_keys(), score_findings(), _observed_states(), score_port_states(), evaluate_corpus(), format_report() (+5 more)

### Community 305 - "Community 305"
Cohesion: 0.28
Nodes (5): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples.

### Community 56 - "Community 56"
Cohesion: 0.07
Nodes (13): interpret_redis_info(), _probe_redis(), DBScanner, db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act, FakeReader, FakeWriter, _run() (+5 more)

### Community 99 - "Community 99"
Cohesion: 0.12
Nodes (20): ScanRecord, Delta, _stable_host_id(), _extract_service(), _extract_version(), DeltaEngine, _new_service_severity(), _significant_version_change() (+12 more)

### Community 388 - "Community 388"
Cohesion: 0.40
Nodes (5): classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj

### Community 14 - "Community 14"
Cohesion: 0.06
Nodes (74): Finding, _as_dict(), _scanner(), _data(), _is_open(), build_service_index(), _rule_tls(), _rule_smb() (+66 more)

### Community 323 - "Community 323"
Cohesion: 0.32
Nodes (6): _now(), _state_for_confidence(), fuse_liveness(), host_discovery.py — determine which hosts are alive, with graded confidence.  ME, Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a, Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a

### Community 306 - "Community 306"
Cohesion: 0.22
Nodes (9): normalize_mac(), Neighbor, parse_neighbor_line(), read_neighbor(), Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower., One OS neighbor-cache observation about a target, with graded freshness., Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo, Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads (+1 more)

### Community 389 - "Community 389"
Cohesion: 0.33
Nodes (6): is_locally_administered(), device_hint(), True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc, Best-effort device classification from the L2/L3 evidence., True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc, Best-effort device classification from the L2/L3 evidence.

### Community 262 - "Community 262"
Cohesion: 0.22
Nodes (7): vendor_for_mac(), HostDiscoveryScanner, Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response)., Return 'open', 'refused', or None (no response).

### Community 446 - "Community 446"
Cohesion: 0.50
Nodes (4): read_arp_table(), Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R, Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R, Return {ip: normalized_mac} from the OS neighbor cache.      Tries `ip neigh` (L

### Community 57 - "Community 57"
Cohesion: 0.07
Nodes (35): _parse_ssdp_headers(), _fetch_upnp_root_desc(), _probe_ssdp_sync(), _decode_mdns_name(), _parse_mdns_response(), _probe_mdns_sync(), _probe_rtsp(), _mqtt_connect() (+27 more)

### Community 171 - "Community 171"
Cohesion: 0.18
Nodes (15): _version_str(), _walk_extensions(), _ext_types(), _selected_alpn(), _alpn_code(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello() (+7 more)

### Community 246 - "Community 246"
Cohesion: 0.23
Nodes (11): oid_to_hex(), _hash_oids(), ja4x_from_oid_lists(), ja4x_from_cert(), ja4x_from_der(), match_suspicious(), DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040, Pure JA4X from the three ordered OID lists (dotted-decimal strings). (+3 more)

### Community 151 - "Community 151"
Cohesion: 0.15
Nodes (13): _have_masscan(), _masscan_records_to_results(), _ConnectSweep, run_mass_scan(), _masscan_excludes(), _spec_in_scope(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them. (+5 more)

### Community 324 - "Community 324"
Cohesion: 0.29
Nodes (8): MasscanRun, _run_masscan(), _parse_masscan_json(), _parse_masscan_json_detailed(), Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin

### Community 116 - "Community 116"
Cohesion: 0.12
Nodes (13): _NoRedirect, _known_false_positive(), _mcp_oauth_signal(), _auth_shaped_json_body(), _model_count(), MCPAIScanner, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+5 more)

### Community 142 - "Community 142"
Cohesion: 0.14
Nodes (16): _adb_checksum(), _build_adb_cnxn(), _parse_adb_header(), _probe_adb(), _probe_lockdownd(), _build_mdns_query(), _parse_mdns_ptr_names(), _probe_mdns_mobile_sync() (+8 more)

### Community 35 - "Community 35"
Cohesion: 0.06
Nodes (41): _icmp(), build_icmp_echo(), build_icmp_timestamp(), build_icmp_addrmask(), _strip_ip_header(), parse_icmp_reply(), parse_icmp_timestamps(), remote_clock() (+33 more)

### Community 94 - "Community 94"
Cohesion: 0.09
Nodes (13): resolve_profile(), port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD, Resolve a named scan profile to a concrete, de-duplicated port list.      'full', TestAssessTarpit, TestPortScannerTarpitFlag, test_tarpit.py — tarpit / honeypot detection (task C5).  A tarpit (LaBrea), hone, resolve_intensity(), intensity_port_override() (+5 more)

### Community 47 - "Community 47"
Cohesion: 0.06
Nodes (30): _family_of(), ScanMetrics, PortScanner, Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Per-target scan accounting — the completeness + self-health record.      It lets, Tally exactly one terminal per-port observation., Requested ports that were never recorded — the silent-skip proof., Ports recorded more than once (a port must get exactly one verdict). (+22 more)

### Community 247 - "Community 247"
Cohesion: 0.23
Nodes (8): build_connection_request(), parse_connection_confirm(), probe_rdp(), RDPScanner, main(), TPKT + X.224 Connection Request carrying an RDP Negotiation Request., Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the, One synchronous RDP handshake. Best-effort; None on any failure.

### Community 307 - "Community 307"
Cohesion: 0.39
Nodes (8): _log(), _run_stage(), _read_jsonl(), _open_tcp_ports(), _ports_arg(), main(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl.

### Community 286 - "Community 286"
Cohesion: 0.20
Nodes (8): ScanFunnel, build_default_funnel(), Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun

### Community 19 - "Community 19"
Cohesion: 0.04
Nodes (51): user_agent(), probe_payload(), choose_source_port(), jittered_delay(), assess_tarpit(), classify_os_error(), describe_os_error(), ScopeError (+43 more)

### Community 20 - "Community 20"
Cohesion: 0.04
Nodes (48): ScanResult, _UDPProbeProtocol, async_udp_probe(), async_udp_probe_retry(), ResultWriter, BaseScanner, main_entrypoint(), run_cli() (+40 more)

### Community 88 - "Community 88"
Cohesion: 0.07
Nodes (19): RateLimiter, AdaptiveRateController, expand_targets(), Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Simple async rate limiter: at most `rate` operations per second., A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window)., Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10 (+11 more)

### Community 227 - "Community 227"
Cohesion: 0.18
Nodes (9): _dec(), match_service(), ServiceBannerScanner, Soft-match collected bytes to {service, product, version}; None if unknown., One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown. (+1 more)

### Community 65 - "Community 65"
Cohesion: 0.07
Nodes (29): Enrichment, _dns_read_name(), mdns_hostname(), _nb_encode(), netbios_name(), resolve_hostnames(), tls_info(), tls_accepts_old() (+21 more)

### Community 248 - "Community 248"
Cohesion: 0.23
Nodes (7): _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate(), SMBScanner, smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection, Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout

### Community 152 - "Community 152"
Cohesion: 0.22
Nodes (16): _ber_len(), _decode_oid(), _ber_parse(), _parse_varbinds(), _oid_tlv(), _varbind(), _varbind_list(), _snmp_msg() (+8 more)

### Community 132 - "Community 132"
Cohesion: 0.13
Nodes (12): _encode_oid(), _decode_value(), _oid_in_subtree(), SNMPScanner, Dotted-notation OID string → BER-encoded bytes., Human-readable SNMP value for common ASN.1/SNMP types., Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli, Return (community, sysdescr) for the first responding community, or None. (+4 more)

### Community 447 - "Community 447"
Cohesion: 0.67
Nodes (1): SSHCollector

### Community 31 - "Community 31"
Cohesion: 0.05
Nodes (42): build_ip_header(), build_tcp_syn(), build_syn_packet(), _parse_mss(), parse_packet(), classify(), syn_cookie(), verify_reply_cookie() (+34 more)

### Community 69 - "Community 69"
Cohesion: 0.09
Nodes (31): _ext(), _sni_extension(), _supported_versions_ext(), _key_share_ext(), build_client_hello(), parse_server_hello(), version_code(), cipher_code() (+23 more)

### Community 26 - "Community 26"
Cohesion: 0.05
Nodes (27): classify_cipher(), grade_tls_posture(), _sni(), _try_version(), _get_cert_der(), _parse_cert_der(), _scan_tls_sync(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only): (+19 more)

### Community 249 - "Community 249"
Cohesion: 0.17
Nodes (5): _ike_probe(), _tftp_probe(), udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-, TFTP RRQ for a non-existent file.  Error reply confirms TFTP service.

### Community 205 - "Community 205"
Cohesion: 0.16
Nodes (9): _ntp_monlist_probe(), _sip_probe(), interpret_ntp_monlist(), interpret_dns_recursion(), interpret_memcached_stats(), UDPScanner, SIP OPTIONS request — safe fingerprint method., Acquire the concurrency gate (adaptive window or fixed semaphore),         run t (+1 more)

### Community 476 - "Community 476"
Cohesion: 0.67
Nodes (3): _ipmi_probe(), RMCP Ping (ASF Presence Ping) to detect IPMI/BMC., RMCP Ping (ASF Presence Ping) to detect IPMI/BMC.

### Community 478 - "Community 478"
Cohesion: 0.67
Nodes (3): _ssdp_probe(), UPnP/SSDP M-SEARCH — unicast to target:1900., UPnP/SSDP M-SEARCH — unicast to target:1900.

### Community 477 - "Community 477"
Cohesion: 0.67
Nodes (3): _mdns_probe(), mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)., mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353).

### Community 471 - "Community 471"
Cohesion: 0.67
Nodes (3): interpret_ike(), Parse IKEv1 or IKEv2 response header., Parse IKEv1 or IKEv2 response header.

### Community 474 - "Community 474"
Cohesion: 0.67
Nodes (3): interpret_sip(), Extract SIP version + server header from a SIP response., Extract SIP version + server header from a SIP response.

### Community 472 - "Community 472"
Cohesion: 0.67
Nodes (3): interpret_ipmi(), Parse RMCP Pong; extract supported entities and IPMI capabilities., Parse RMCP Pong; extract supported entities and IPMI capabilities.

### Community 475 - "Community 475"
Cohesion: 0.67
Nodes (3): interpret_ssdp(), Extract Location and Server from SSDP response., Extract Location and Server from SSDP response.

### Community 473 - "Community 473"
Cohesion: 0.67
Nodes (3): interpret_mdns(), Return byte count and check QR bit (1 = response)., Return byte count and check QR bit (1 = response).

### Community 420 - "Community 420"
Cohesion: 0.50
Nodes (3): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =

### Community 357 - "Community 357"
Cohesion: 0.38
Nodes (6): _is_external(), _extract(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta

### Community 172 - "Community 172"
Cohesion: 0.13
Nodes (7): parse_allow_header(), _NoRedirect, _fetch(), WebScanner, web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl, Read the Allow header from an OPTIONS response. Read-only., Read the Allow header from an OPTIONS response. Read-only.

### Community 325 - "Community 325"
Cohesion: 0.43
Nodes (1): WindowsCollector

### Community 89 - "Community 89"
Cohesion: 0.07
Nodes (6): TestWindowStateMachine, TestWindowGating, TestUdpRetransmit, _EchoProtocol, TestUdpScannerAdaptive, test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit.

### Community 392 - "Community 392"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 135 - "Community 135"
Cohesion: 0.10
Nodes (3): _EchoProtocol, _SinkProtocol, test_async_udp.py — tests for the true-async UDP probe helper in scanner_base.

### Community 126 - "Community 126"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_scan_run_builds_dispatch_payload(), test_cmd_doctor_success_with_online_agent(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 208 - "Community 208"
Cohesion: 0.22
Nodes (12): _plant(), _manager(), test_engagement_dispatch_reaches_probe_and_enforces_scope(), test_out_of_scope_target_is_refused_end_to_end(), test_real_scan_of_open_datastore_yields_manager_finding(), _vulnerable_host_facts(), test_manager_correlation_finds_all_three_attack_paths(), test_correlated_findings_cite_their_base_findings() (+4 more)

### Community 209 - "Community 209"
Cohesion: 0.14
Nodes (4): TestLocallyAdministered, TestVendorLookup, TestDeviceHint, Pure-logic tests for the ARP/MAC/mobile-detection helpers in host_discovery. No

### Community 367 - "Community 367"
Cohesion: 0.29
Nodes (1): TestNormalizeMac

### Community 426 - "Community 426"
Cohesion: 0.40
Nodes (1): TestCheckHwBind

### Community 368 - "Community 368"
Cohesion: 0.38
Nodes (3): _dry_run(), test_installer_accepts_enroll_token_and_insecure_for_http_manager(), test_installer_without_token_still_shows_manual_approval()

### Community 335 - "Community 335"
Cohesion: 0.25
Nodes (5): TestIdentityAndEncryption, Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe.

### Community 396 - "Community 396"
Cohesion: 0.33
Nodes (4): TestTaskRunnerWithEncryptedScope, Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope.

### Community 397 - "Community 397"
Cohesion: 0.33
Nodes (2): TestScopeValidationPipeline, Phase 1: combined scope validation (validate + excludes).

### Community 427 - "Community 427"
Cohesion: 0.40
Nodes (2): TestResultSpoolWithRetry, Phase 1: result spool with upload retry.

### Community 428 - "Community 428"
Cohesion: 0.40
Nodes (3): TestTransportWithIdentity, Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine.

### Community 398 - "Community 398"
Cohesion: 0.33
Nodes (2): TestWebSocketMessageProtocol, Phase 2: WebSocket message parsing.

### Community 334 - "Community 334"
Cohesion: 0.25
Nodes (5): TestFullJobLifecycle, End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly.

### Community 399 - "Community 399"
Cohesion: 0.33
Nodes (4): TestStartupGauntlet, Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup.

### Community 232 - "Community 232"
Cohesion: 0.15
Nodes (1): test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor

### Community 290 - "Community 290"
Cohesion: 0.44
Nodes (9): _metrics(), _rec(), test_full_scan_is_complete(), test_missing_port_is_detected(), test_duplicate_port_is_detected(), test_skip_plus_duplicate_is_not_falsely_complete(), test_summary_exposes_missing_and_duplicates(), test_fallback_count_based_when_no_requested_set() (+1 more)

### Community 210 - "Community 210"
Cohesion: 0.33
Nodes (13): _run(), _ids(), _get(), test_ntlm_relay_is_medium_when_only_signing_not_required(), test_ntlm_relay_is_high_when_smbv1_also_enabled(), test_no_relay_finding_when_signing_required(), test_legacy_windows_surface_smbv1_plus_rdp(), test_no_legacy_surface_with_only_smbv1() (+5 more)

### Community 211 - "Community 211"
Cohesion: 0.25
Nodes (5): _scope(), _mk_scanner(), _summary(), TestWorkerPoolAndMetrics, TestDefaultsAndAdaptiveTimeout

### Community 369 - "Community 369"
Cohesion: 0.29
Nodes (1): TestProfiles

### Community 336 - "Community 336"
Cohesion: 0.36
Nodes (5): _svc(), test_redis_info_and_noauth_identify_as_redis(), test_memcached_version_and_stat_identify_as_memcached(), test_elasticsearch_and_couchdb_win_over_generic_http(), test_main_scripts_datastore_probe.py — safe read-only datastore probes make the

### Community 291 - "Community 291"
Cohesion: 0.20
Nodes (1): TestClassifyDevice

### Community 400 - "Community 400"
Cohesion: 0.33
Nodes (1): test_main_scripts_device_ties.py — Phase 23: device classification never resolve

### Community 292 - "Community 292"
Cohesion: 0.29
Nodes (6): _oserr(), test_definitive_states(), test_scanner_side_errors_are_error_not_filtered(), test_unknown_errno_is_self_identifying_and_never_filtered(), test_describe_os_error_is_fully_debuggable(), test_main_scripts_errno.py — Phase 2: shared TCP/UDP errno classification.  Veri

### Community 54 - "Community 54"
Cohesion: 0.11
Nodes (37): _run(), _ids(), test_tls_obsolete_protocol_is_high(), test_tls_legacy_protocol_is_medium_and_not_double_reported_with_obsolete(), test_tls_modern_only_produces_no_crypto_finding(), test_tls_weak_cipher_is_high_with_reasons(), test_tls_expired_and_self_signed_cert(), test_smbv1_enabled_is_high() (+29 more)

### Community 110 - "Community 110"
Cohesion: 0.13
Nodes (11): _scope(), _run(), TestUdpStateModel, TestOsConfidence, _smb2_header(), make_smb2_success(), make_smb2_error(), TestSmbParsing (+3 more)

### Community 269 - "Community 269"
Cohesion: 0.22
Nodes (4): _ext(), _serverhello(), test_ja4s_from_serverhello_tls13(), test_main_scripts_ja4s.py — JA4S TLS ServerHello fingerprint (advanced capabilit

### Community 233 - "Community 233"
Cohesion: 0.17
Nodes (3): _fake_cert(), test_ja4x_from_cert_matches_pure_core(), test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced capa

### Community 193 - "Community 193"
Cohesion: 0.21
Nodes (12): _cc(), test_nla_when_hybrid_selected(), test_tls_only_is_not_nla(), test_standard_rdp_security_no_nla(), test_negotiation_failure(), test_cc_without_negotiation_is_standard_rdp(), _run(), test_confirmed_rdp_without_nla_is_high_finding() (+4 more)

### Community 213 - "Community 213"
Cohesion: 0.14
Nodes (3): TestStableHostId, TestVersionChange, test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te

### Community 174 - "Community 174"
Cohesion: 0.12
Nodes (1): TestSNMPBerUtilities

### Community 136 - "Community 136"
Cohesion: 0.10
Nodes (1): TestUDPProbeConstruction

### Community 293 - "Community 293"
Cohesion: 0.20
Nodes (1): TestIoTScanner

### Community 234 - "Community 234"
Cohesion: 0.36
Nodes (2): _make_scan_record(), TestDeltaEngine

### Community 212 - "Community 212"
Cohesion: 0.14
Nodes (1): TestMobileScanner

### Community 401 - "Community 401"
Cohesion: 0.33
Nodes (2): TestNmapEntityGuard, test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti

### Community 430 - "Community 430"
Cohesion: 0.40
Nodes (1): TestIcmpBuilders

### Community 431 - "Community 431"
Cohesion: 0.50
Nodes (1): TestIcmpParse

### Community 432 - "Community 432"
Cohesion: 0.60
Nodes (1): TestIcmpTimestamps

### Community 450 - "Community 450"
Cohesion: 0.83
Nodes (1): TestTimestampFallback

### Community 370 - "Community 370"
Cohesion: 0.48
Nodes (1): TestAcceptEchoReply

### Community 310 - "Community 310"
Cohesion: 0.22
Nodes (1): TestTtlInference

### Community 270 - "Community 270"
Cohesion: 0.18
Nodes (1): TestFingerprintOs

### Community 111 - "Community 111"
Cohesion: 0.11
Nodes (15): _Writer, _Socket, test_subset_listener_failure_reports_degraded_coverage(), test_ot_udp_backend_never_joins_or_transmits(), test_collector_raises_when_no_listener_binds(), engine_manifest(), planned_components(), ErrorDetail (+7 more)

### Community 185 - "Community 185"
Cohesion: 0.14
Nodes (11): gate_0_is_passive_profile(), gate_2_host_discovery(), gate_3_port_scan(), gate_5_branch_eligible(), gates.py — precondition functions deciding whether each stage of the workflow ru, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti, Does `branch` apply to this host?       - Must be in this profile's allowed deep, True means OT/ICS passive-only mode — a hard stop, never reached by     any acti (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.03
Nodes (25): _scan_result(), TestScanResult, TestRateLimiter, TestGate0, TestLooksLikeHttp, TestLooksLikeTls, TestEngagementModes, TestAssetMergeHostDiscovery (+17 more)

### Community 51 - "Community 51"
Cohesion: 0.08
Nodes (9): _asset(), TestGate2, TestGate3, TestGate4, TestGate5, TestGate6, TestRouteBranches, TestAssetNeedsRecheckLive (+1 more)

### Community 237 - "Community 237"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 271 - "Community 271"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 294 - "Community 294"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 338 - "Community 338"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 295 - "Community 295"
Cohesion: 0.20
Nodes (1): TestUseCasesResolve

### Community 403 - "Community 403"
Cohesion: 0.53
Nodes (5): _manifest(), test_manifest_is_clean_parseable_json(), test_manifest_surfaces_the_capability_contract(), test_manifest_is_deterministic(), test_probe_manifest.py — the `agent.agent manifest` command that the seal-parity

### Community 112 - "Community 112"
Cohesion: 0.11
Nodes (7): _cache_with(), test_device_inventory_post_stage_classifies_from_open_ports(), test_device_inventory_skips_hosts_without_evidence(), test_exposure_matrix_flags_internet_reachable_ports(), test_exposure_matrix_internal_only_from_lan_vantage(), test_no_post_stage_for_ordinary_scan_types(), test_probe_next_features.py — the probe_next plan: run the improved main_scripts

### Community 312 - "Community 312"
Cohesion: 0.31
Nodes (4): _infos(), TestResolveFamily, test_resolve.py — resolve() address-family selection (task A9)., Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr).

### Community 106 - "Community 106"
Cohesion: 0.08
Nodes (1): TestResultSpool

### Community 156 - "Community 156"
Cohesion: 0.14
Nodes (13): looks_like_http(), looks_like_tls(), looks_like_db(), looks_like_ssh(), route_branches(), router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content,, True when this port's banner result is exactly the silent-on-garbage     signatu, True when a service banner carries a database greeting signature, so a DB     on (+5 more)

### Community 157 - "Community 157"
Cohesion: 0.12
Nodes (7): FakeDiscovery, FakePortScanner, RecordingDeep, _scope(), TestBuildDefaultFunnel, TestScanFunnelRun, test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel

### Community 238 - "Community 238"
Cohesion: 0.27
Nodes (3): _make_funnel(), TestScanFunnel, Build a funnel with fakes; return (funnel, discovery, port_scanner, created).

### Community 434 - "Community 434"
Cohesion: 0.40
Nodes (1): TestRoutePorts

### Community 314 - "Community 314"
Cohesion: 0.28
Nodes (8): _py_files(), test_scanner_is_superset_of_no_missing_files(), test_no_extra_scanner_files(), test_scanner_module_matches_main_scripts(), test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1, Every scanner module authored in main_scripts must exist in scanner/., scanner/ must not carry modules that main_scripts/ does not — otherwise the, Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py.

### Community 296 - "Community 296"
Cohesion: 0.20
Nodes (2): TestEncryptDecryptRoundtrip, Each encryption uses a fresh ephemeral key, so blobs are different.

### Community 214 - "Community 214"
Cohesion: 0.14
Nodes (1): TestValidateTargetsInScope

### Community 315 - "Community 315"
Cohesion: 0.22
Nodes (1): TestTargetsInExcludes

### Community 371 - "Community 371"
Cohesion: 0.29
Nodes (1): TestMergeExclusions

### Community 406 - "Community 406"
Cohesion: 0.33
Nodes (1): TestFetchEngagementScope

### Community 101 - "Community 101"
Cohesion: 0.08
Nodes (7): TestSshMatch, TestHttpMatch, TestOtherServices, TestNoMatch, TestProbeLadder, TestScannerIntegration, test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi

### Community 194 - "Community 194"
Cohesion: 0.17
Nodes (13): _smb2_negotiate_response(), _smb2_error_response(), test_signing_required_smb311(), test_signing_not_required(), test_error_response_not_parsed_as_signing(), test_truncated_negotiate_body_not_parsed(), test_signing_supported_field_present(), test_request_omits_311_without_preauth_context() (+5 more)

### Community 436 - "Community 436"
Cohesion: 0.40
Nodes (1): TestSynCookie

### Community 435 - "Community 435"
Cohesion: 0.40
Nodes (1): TestPacketRoundTrip

### Community 437 - "Community 437"
Cohesion: 0.70
Nodes (1): TestVerifyReplyCookie

### Community 372 - "Community 372"
Cohesion: 0.43
Nodes (3): TestSynRetransmit, The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa

### Community 409 - "Community 409"
Cohesion: 0.33
Nodes (1): TestOptionParsing

### Community 408 - "Community 408"
Cohesion: 0.60
Nodes (1): TestBuildResultsEnrichment

### Community 257 - "Community 257"
Cohesion: 0.17
Nodes (2): TestRunnerHeadless, Tests that use the real engine but with no-op callbacks.

### Community 195 - "Community 195"
Cohesion: 0.13
Nodes (5): TestRunnerScopeValidation, When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced.

### Community 373 - "Community 373"
Cohesion: 0.29
Nodes (5): TestRunnerSubmission, Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit.

### Community 137 - "Community 137"
Cohesion: 0.11
Nodes (5): TestClientHello, _synthetic_server_hello(), TestParseServerHello, TestDigest, test_tls_fingerprint.py — Tier 2.3: active TLS fingerprint (JARM methodology).

### Community 316 - "Community 316"
Cohesion: 0.22
Nodes (1): TestIdentity

### Community 374 - "Community 374"
Cohesion: 0.29
Nodes (1): TestDeviceEnrollment

### Community 297 - "Community 297"
Cohesion: 0.20
Nodes (1): TestSubmitResult

### Community 438 - "Community 438"
Cohesion: 0.40
Nodes (1): TestWebSocket

### Community 412 - "Community 412"
Cohesion: 0.33
Nodes (2): TestChooseSourcePort, Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs.

### Community 439 - "Community 439"
Cohesion: 0.40
Nodes (2): TestJitteredDelay, Evasion: blur a fixed scan cadence with a bounded random per-probe delay.

### Community 454 - "Community 454"
Cohesion: 0.50
Nodes (2): TestModuleConstantsUnbranded, Import-time probe constants built from user_agent() must be signature-free.

### Community 84 - "Community 84"
Cohesion: 0.07
Nodes (4): _ExplodingScanner, _ConcurrencyScanner, test_per_target_exception_preserves_other_results(), test_host_fanout_is_bounded()

### Community 376 - "Community 376"
Cohesion: 0.48
Nodes (6): _b64(), keygen(), pubkey(), issue(), main(), Print the vendor PUBLIC key (hex) derived from the private key.      build/seal-

### Community 44 - "Community 44"
Cohesion: 0.05
Nodes (13): _utcnow(), _parse_ts(), PortFact, Asset, asset.py — per-host fact model the workflow engine reasons about.  This is an OR, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Dispatch a real ScanResult into the right sub-structure, keyed         on result, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep (+5 more)

### Community 159 - "Community 159"
Cohesion: 0.16
Nodes (8): classify_certainty(), CacheEntry, WorkflowCache, cache.py — (host, port, scanner) -> CacheEntry, so deterministic facts are colle, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, True if there's no cached entry, OR the entry is uncertain         (always worth

### Community 317 - "Community 317"
Cohesion: 0.31
Nodes (8): _parse_duration(), build_parser(), _build_mode(), _build_creds(), _main(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 217 - "Community 217"
Cohesion: 0.22
Nodes (3): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., True when execution produced errors and no usable or cached facts.

### Community 102 - "Community 102"
Cohesion: 0.11
Nodes (24): resolve_stage_ceiling(), includes_stage(), EngagementMode, discovery(), host_discovery(), port_scan(), service_fingerprint(), triage() (+16 more)

### Community 32 - "Community 32"
Cohesion: 0.05
Nodes (44): _scan_one(), _gather_per_host(), _split_cached(), _port_candidates(), _Sink, _run_passive(), _run_inventory(), _store_results() (+36 more)

### Community 513 - "Community 513"
Cohesion: 1.00
Nodes (1): Make a per-host scanner instance share ONE rate limiter + semaphore with all

### Community 514 - "Community 514"
Cohesion: 1.00
Nodes (1): Make a raw banner safe and readable for the summary line.      Many services ans

### Community 515 - "Community 515"
Cohesion: 1.00
Nodes (1): # NOTE: credentialed collectors (ssh_collector, windows_collector) are run

### Community 506 - "Community 506"
Cohesion: 1.00
Nodes (1): Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.

### Community 507 - "Community 507"
Cohesion: 1.00
Nodes (1): Read a KV-v2 secret from Vault.

### Community 496 - "Community 496"
Cohesion: 1.00
Nodes (1): Fast port discovery with naabu. Feeds port list to Nmap.

### Community 497 - "Community 497"
Cohesion: 1.00
Nodes (1): Nmap service enumeration. Accepts port list from Naabu.

### Community 498 - "Community 498"
Cohesion: 1.00
Nodes (1): Nuclei vulnerability scan — production-ready.

### Community 499 - "Community 499"
Cohesion: 1.00
Nodes (1): Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.

### Community 500 - "Community 500"
Cohesion: 1.00
Nodes (1): NetExec SMB validation: signing, null sessions, SMBv1.

### Community 501 - "Community 501"
Cohesion: 1.00
Nodes (1): testssl.sh TLS/SSL analysis.

### Community 502 - "Community 502"
Cohesion: 1.00
Nodes (1): Extract HTTP/HTTPS URLs from nmap XML output.

### Community 503 - "Community 503"
Cohesion: 1.00
Nodes (1): EyeWitness screenshot evidence collection.

### Community 504 - "Community 504"
Cohesion: 1.00
Nodes (1): Safe lateral movement checks — no actual exploitation.

### Community 505 - "Community 505"
Cohesion: 1.00
Nodes (1): Cloud infrastructure scan (AWS/Azure/GCP).

### Community 508 - "Community 508"
Cohesion: 1.00
Nodes (1): Verify the Python probe can open what the TypeScript manager sealed (T14 interop

### Community 516 - "Community 516"
Cohesion: 1.00
Nodes (1): ThreadingHTTPServer

### Community 509 - "Community 509"
Cohesion: 1.00
Nodes (1): Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO

### Community 510 - "Community 510"
Cohesion: 1.00
Nodes (1): Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).

### Community 511 - "Community 511"
Cohesion: 1.00
Nodes (1): End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.

### Community 512 - "Community 512"
Cohesion: 1.00
Nodes (1): Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 350 - "Community 350"
Cohesion: 0.67
Nodes (7): 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit, agents/greeting-introduction, main

## Knowledge Gaps
- **2584 isolated node(s):** `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R`, `Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000`, `Detection validation: attack_timeline, detection_configs, extend detection_resul` (+2579 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 455`** (1 nodes): `Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 456`** (1 nodes): `Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 457`** (1 nodes): `Finding verification verdict columns (P2 passive verification).  Revision ID: 00`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 458`** (1 nodes): `Approval-gated safe active-validation requests (P3).  Revision ID: 0022 Revises:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 440`** (2 nodes): `Device-role inventory: persist the probe device_classifier's role on assets.  Ad`, `# NOTE: Postgres cannot DROP a single enum value; the added 'printer' /`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 459`** (1 nodes): `Scan-request targets + intensity — the rich customer scan request.  Adds two nul`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 460`** (1 nodes): `Remediation plans — cached, OS-specific, structured remediation for a finding.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 461`** (1 nodes): `SLA policies — per-tenant custom remediation windows (hours per severity).  One`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 462`** (1 nodes): `Integrations — per-tenant notification config (email / Slack / Jira).  One row p`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 463`** (1 nodes): `scan_requests.use_case_id — the capability use-case a customer requested.  The p`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 479`** (1 nodes): `risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 484`** (2 nodes): `Record a heartbeat from an agent.`, `Record a heartbeat from an agent.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 328`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 391`** (1 nodes): `TestNTLMRelayChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 359`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 480`** (1 nodes): `TestAgentWebSocketAuthentication`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 481`** (1 nodes): `TestJobSecretBoundary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 423`** (1 nodes): `TestTenantWebSocketSelection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 422`** (2 nodes): `_claim_fixture()`, `TestAtomicWebSocketClaim`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 424`** (1 nodes): `TestGetAgentJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (1 nodes): `TestAgentJobCompatibility`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 482`** (1 nodes): `TestListAgents`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 287`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 254`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 192`** (2 nodes): `_action()`, `TestDetectionCorrelator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 362`** (1 nodes): `TestSigmaRuleGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 394`** (1 nodes): `TestSIEMParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 331`** (1 nodes): `test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 255`** (1 nodes): `test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (1 nodes): `TestValidatePayload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 363`** (1 nodes): `TestValidateModule`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 364`** (1 nodes): `TestValidateScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 333`** (1 nodes): `TestRequiresApproval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 332`** (1 nodes): `TestMetasploitRPCClient`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (1 nodes): `TestNucleiExploitRunner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 365`** (1 nodes): `test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 402`** (1 nodes): `test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.  T`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 272`** (2 nodes): `_token()`, `test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 407`** (1 nodes): `TestValidateEnv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 158`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (1 nodes): `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 361`** (1 nodes): `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 393`** (1 nodes): `TestCvss`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 360`** (1 nodes): `TestDeceptionScore`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 419`** (2 nodes): `ScanReq`, `ClientUser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (2 nodes): `SSHCollector`, `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 447`** (1 nodes): `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 325`** (1 nodes): `WindowsCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 367`** (1 nodes): `TestNormalizeMac`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 426`** (1 nodes): `TestCheckHwBind`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 397`** (2 nodes): `TestScopeValidationPipeline`, `Phase 1: combined scope validation (validate + excludes).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 427`** (2 nodes): `TestResultSpoolWithRetry`, `Phase 1: result spool with upload retry.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 398`** (2 nodes): `TestWebSocketMessageProtocol`, `Phase 2: WebSocket message parsing.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (1 nodes): `test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 369`** (1 nodes): `TestProfiles`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 291`** (1 nodes): `TestClassifyDevice`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 400`** (1 nodes): `test_main_scripts_device_ties.py — Phase 23: device classification never resolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 174`** (1 nodes): `TestSNMPBerUtilities`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 136`** (1 nodes): `TestUDPProbeConstruction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (1 nodes): `TestIoTScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (2 nodes): `_make_scan_record()`, `TestDeltaEngine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 212`** (1 nodes): `TestMobileScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 401`** (2 nodes): `TestNmapEntityGuard`, `test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 430`** (1 nodes): `TestIcmpBuilders`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 431`** (1 nodes): `TestIcmpParse`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 432`** (1 nodes): `TestIcmpTimestamps`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 450`** (1 nodes): `TestTimestampFallback`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 370`** (1 nodes): `TestAcceptEchoReply`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 310`** (1 nodes): `TestTtlInference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 270`** (1 nodes): `TestFingerprintOs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 294`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 338`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 295`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (1 nodes): `TestResultSpool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 434`** (1 nodes): `TestRoutePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 296`** (2 nodes): `TestEncryptDecryptRoundtrip`, `Each encryption uses a fresh ephemeral key, so blobs are different.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 315`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 371`** (1 nodes): `TestMergeExclusions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 406`** (1 nodes): `TestFetchEngagementScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 436`** (1 nodes): `TestSynCookie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 435`** (1 nodes): `TestPacketRoundTrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 437`** (1 nodes): `TestVerifyReplyCookie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 409`** (1 nodes): `TestOptionParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 408`** (1 nodes): `TestBuildResultsEnrichment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (2 nodes): `TestRunnerHeadless`, `Tests that use the real engine but with no-op callbacks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 316`** (1 nodes): `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 374`** (1 nodes): `TestDeviceEnrollment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 297`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 438`** (1 nodes): `TestWebSocket`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 412`** (2 nodes): `TestChooseSourcePort`, `Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 439`** (2 nodes): `TestJitteredDelay`, `Evasion: blur a fixed scan cadence with a bounded random per-probe delay.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 454`** (2 nodes): `TestModuleConstantsUnbranded`, `Import-time probe constants built from user_agent() must be signature-free.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 513`** (1 nodes): `Make a per-host scanner instance share ONE rate limiter + semaphore with all`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 514`** (1 nodes): `Make a raw banner safe and readable for the summary line.      Many services ans`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 515`** (1 nodes): `# NOTE: credentialed collectors (ssh_collector, windows_collector) are run`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 506`** (1 nodes): `Fetches credentials from HashiCorp Vault at runtime. Never caches to disk.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 507`** (1 nodes): `Read a KV-v2 secret from Vault.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 496`** (1 nodes): `Fast port discovery with naabu. Feeds port list to Nmap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 497`** (1 nodes): `Nmap service enumeration. Accepts port list from Naabu.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 498`** (1 nodes): `Nuclei vulnerability scan — production-ready.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 499`** (1 nodes): `Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 500`** (1 nodes): `NetExec SMB validation: signing, null sessions, SMBv1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 501`** (1 nodes): `testssl.sh TLS/SSL analysis.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 502`** (1 nodes): `Extract HTTP/HTTPS URLs from nmap XML output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 503`** (1 nodes): `EyeWitness screenshot evidence collection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 504`** (1 nodes): `Safe lateral movement checks — no actual exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 505`** (1 nodes): `Cloud infrastructure scan (AWS/Azure/GCP).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 508`** (1 nodes): `Verify the Python probe can open what the TypeScript manager sealed (T14 interop`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 516`** (1 nodes): `ThreadingHTTPServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 509`** (1 nodes): `Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 510`** (1 nodes): `Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 511`** (1 nodes): `End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 512`** (1 nodes): `Deterministic stand-ins emitting realistic output for 127.0.0.1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 4` to `Community 75`, `Community 218`, `Community 144`, `Community 138`, `Community 160`, `Community 2`, `Community 59`, `Community 107`, `Community 186`, `Community 5`, `Community 265`, `Community 359`, `Community 328`, `Community 391`, `Community 74`, `Community 231`, `Community 332`, `Community 267`, `Community 333`, `Community 363`, `Community 268`, `Community 364`, `Community 37`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `Transport` connect `Community 121` to `Community 6`, `Community 161`, `Community 318`, `Community 177`, `Community 343`, `Community 220`, `Community 345`, `Community 344`, `Community 346`, `Community 378`, `Community 302`, `Community 347`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `AgentConnectionManager` connect `Community 300` to `Community 0`, `Community 441`, `Community 442`, `Community 413`, `Community 443`, `Community 377`, `Community 444`, `Community 464`, `Community 299`, `Community 484`, `Community 480`, `Community 422`, `Community 481`, `Community 423`, `Community 5`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 173 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 173 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19`, `Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202`, `Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R` to the rest of the system?**
  _2584 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.017135862913096694 - nodes in this community are weakly interconnected._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.012039587797163555 - nodes in this community are weakly interconnected._