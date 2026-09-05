# Graph Report - .  (2026-09-05)

## Corpus Check
- Large corpus: 1391 files · ~1,334,052 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 13434 nodes · 25836 edges · 743 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 2776 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 5463 · calls: 4670 · rationale_for: 3860 · method: 3187 · uses: 2776 · MODIFIES: 2374 · ON_BRANCH: 1722 · imports: 674 · imports_from: 655 · inherits: 294 · PARENT_OF: 161


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 1391 · Candidates: 3350
- Excluded: 20 untracked · 66095 ignored · 11 sensitive · 1 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `9c54022`
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
Cohesion: 0.01
Nodes (181): check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina, Raised when the binary is running on an unauthorized machine., Deterministic per-machine fingerprint built from stable hardware IDs.      Combi, Verify the binary is running on the machine it was compiled for.      Reads HW_B, agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit (+173 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (146): engine.py — adapt a manager scan job to scanner_module's workflow engine and ret, main(), _print_table(), explain_plan.py — "which scanners will run against this host, and WHY?"      pyt, Recreate this branch's decision and say, in one line, what drove it., _why(), CampaignSummary, EngagementSummary (+138 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (95): BloodHoundCollector — wrapper around the BloodHound.py collector + a Neo4j inges, NTLMRelayChecker — detect missing SMB/LDAP signing that enables NTLM relay.  NTL, HallucinationGuard — post-generation validation of LLM report text against the g, metadata, AssistantProvider(), FastAPI dependency that enforces role-based access.      Usage:         @router., require_role(), 298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validation, result persistence (+87 more)

### Community 3 - "Community 3"
Cohesion: 0.02
Nodes (152): requireAuth(), client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId, PhaseRecommendation (+144 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (94): Exception, MetasploitRPCClient, MetasploitRPCError, Returns {status, output, uuid}., Returns True if job was successfully killed., Poll until job completes or max_wait exceeded., Authenticated RPC call — prepends token., Async Metasploit RPC client using msgpack-over-HTTPS. (+86 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (138): AgentUnavailableError, agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to, Raised when the Anthropic SDK or API key is not configured., Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI, Find the Asset for a probe-reported target IP, creating a minimal one if needed., A still-relevant Finding with the same (engagement, asset, title), if any., Bump severity one rung when the finding's service is internet-reachable     (Ser, ServiceIdentifier (+130 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (95): ApiActivity, GET, AiMessage, ManagerAiResponse, POST(), validMessages(), fail(), GET() (+87 more)

### Community 7 - "Community 7"
Cohesion: 0.02
Nodes (90): AssistantReply, STARTERS, Turn, PortalConsoleProvider(), GRADE_STYLE, GRADE_VAR, portalApi(), PortalEngagement (+82 more)

### Community 8 - "Community 8"
Cohesion: 0.03
Nodes (90): Agent, AGENT_STATUS, AgentStatus, PATH_STATUS, SEV_LABEL, 07ba102 feat: enhance UI UX and detection pipeline, 3c9062a refactor: Update dashboard components for improved styling and functionality, DashboardCharts() (+82 more)

### Community 9 - "Community 9"
Cohesion: 0.04
Nodes (87): ADError, Shared building blocks for the Active Directory assessment module.  Every AD che, Assemble a Finding-compatible dict.      All findings carry — as required by the, Base class for Active Directory assessment errors., Raised when an LDAP/Kerberos/SMB connection to the DC fails., Raised when an optional offensive dependency (ldap3/impacket) is absent., engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS, A previously-remediated finding whose issue reappeared this run: reopen     the (+79 more)

### Community 10 - "Community 10"
Cohesion: 0.02
Nodes (68): assess_tarpit(), get_fd_limit(), inet_checksum(), jittered_delay(), probe_payload(), project_file_stamp(), project_now(), project_timestamp() (+60 more)

### Community 11 - "Community 11"
Cohesion: 0.04
Nodes (41): AttackAction, _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO, _host_identity(), _host_matches(), DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale (+33 more)

### Community 12 - "Community 12"
Cohesion: 0.02
Nodes (72): ComplianceRef, COVERAGE_COLOR, CVSS_AGGRAVATING, CVSS_METRIC, CvssMetric, decisionDrivers(), decodeCvssVector(), DetailTab (+64 more)

### Community 13 - "Community 13"
Cohesion: 0.02
Nodes (100): _agent_can_execute_job(), _agent_ownership_check(), AgentBootstrapRequest, bootstrap_agent(), cancel_agent_job(), _encrypt_scope_for_agent(), enqueue_agent_job(), get_agent_job_history() (+92 more)

### Community 14 - "Community 14"
Cohesion: 0.03
Nodes (88): addcapabilities-fable, ui-ux-backend-updates0109, 0236a60 fix(detection): full EPSS catalog so exploit-probability isn't blind, 185e648 docs: pending-work inventory (buckets A-G), 21ebc46 feat(detection): unified prioritization engine (risk_score for every finding), 22e4f8d chore: update version, 2534404 scanner(service_enum): commit owner's in-progress changes as-is + re-sync scanner/, 2be040c improve(probe/install): portability, supply-chain, ops hardening (+80 more)

### Community 15 - "Community 15"
Cohesion: 0.22
Nodes (96): feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hardening, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive, feat/user-portal-reskin-scan-request (+88 more)

### Community 16 - "Community 16"
Cohesion: 0.03
Nodes (70): 9c54022 Refactor code structure and remove redundant sections for improved readability and maintainability, DEMO_ASSET, DEMO_ENGAGEMENT, DEMO_FINDING, AssetInput, chat(), countSeverities(), CRITICALITY_SCORE (+62 more)

### Community 17 - "Community 17"
Cohesion: 0.03
Nodes (62): AssistantFab(), AssistantCtx, Ctx, useAssistant(), 42f4e28 feat: enhance security operations UX and risk workflows, 7d8d3f3 merge: resolve conflicts with origin/ui-ux-backend-updates0109, ActivityItem, Engagement (+54 more)

### Community 18 - "Community 18"
Cohesion: 0.04
Nodes (53): HallucinationGuard, Run all relevant checks and return a combined verdict:         ``{valid, issues,, Flag any CVE ID mentioned in ``text`` that isn't in the real finding set., Flag CVSS scores in the text that don't match any real score.          ``actual_, Flag destructive-looking commands that shouldn't appear in a fix guide., _collect_cves_scores(), _enum(), _finding_scores() (+45 more)

### Community 19 - "Community 19"
Cohesion: 0.03
Nodes (50): 2c38782 docs: spec CVE-breadth phase — snapshot must answer for every recognized product, 6b41065 probe fixed, 8f6bf49 Refactor code structure and remove redundant sections for improved readability and maintainability, fuse_liveness(), _now(), host_discovery.py — determine which hosts are alive, with graded confidence.  ME, PTR lookup; None on any failure. Runs in _RDNS_POOL, never on the loop., Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a (+42 more)

### Community 20 - "Community 20"
Cohesion: 0.04
Nodes (58): 25c014d feat: enhance campaign progress tracking and add raw facts inspection- Update campaign progress tests to reflect changes in job statuses and overall completion logic.- Introduce new tests for fleet jobs to validate job listing with probe and engagement name resolution.- Implement raw facts endpoint to expose collected scanner data for inspection.- Create frontend components for displaying raw facts and fleet jobs, including filtering options.- Ensure proper integration of new features into the existing campaign and fleet pages., 26ea68c Add comprehensive tests for OS identification, reconciliation, and validation gate- Introduced tests for OS identification based on SMB2 and TTL signals in .- Added tests for the reconciliation of open TCP ports and dynamic ports in .- Implemented tests for the  function in .- Created tests for SMB NTLM build parsing in .- Enhanced SMB scanner tests to ensure proper negotiation context handling in .- Updated SSH scanner tests to differentiate between open and filtered statuses in .- Added tests for TCP option parsing in .- Implemented IPv6 discovery tests to ensure proper scope handling in .- Established validation gate tests to prevent unconfirmed observations from being flagged as exposed in ., 64e8290 feat(campaign): implement VA campaign progress endpoint and UI integration- Added backend endpoint for retrieving VA campaign progress, including job statuses and findings.- Created frontend component for displaying campaign progress with polling for real-time updates.- Enhanced asset and workflow management to include RDP scanning and results handling.- Updated tests to ensure coverage for new campaign progress functionality., 6bb51ab feat: add detection-explain endpoint and enhance campaign progress UI- Implemented a new API endpoint for detection explanations at   /engagements/{id}/detection-explain to provide per-rule verdicts.- Updated CampaignProgress component to include coverage details,   reasons for findings, and improved handling of empty findings states.- Introduced new Coverage interface to track assessment metrics.- Enhanced polling logic to back off on stalled queues.- Added visual indicators for gaps in coverage and reasons for detection status.- Improved findings display with confidence levels and corroboration details., Coverage, Finding, Job, JobSummary (+50 more)

### Community 21 - "Community 21"
Cohesion: 0.03
Nodes (27): 4d0377d Add unit tests for SMB scanner, SYN scanner, and TLS functionality- Implemented unit tests for SMB scanner to validate security mode parsing and error handling.- Added a new SYN scanner test suite to cover packet crafting, checksum validation, and SYN cookie functionality.- Introduced tests for TLS fingerprinting and posture grading, ensuring accurate classification of cipher suites and TLS versions.- Created integration tests for the TLS scanner against a loopback server to verify posture grading and cipher analysis., ae08d19 feat(scanner): adaptive timeout, SYN retransmit, top-100 default (accuracy roadmap 1-3), VA scanner module — pure collection/scanning layer.  Each submodule is an indepe, port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD, Resolve a named scan profile to a concrete, de-duplicated port list.      'full', Resolve a named scan profile to a concrete, de-duplicated port list.      'full', Resolve a named scan profile to a concrete, de-duplicated port list.      'full', Resolve a named scan profile to a concrete, de-duplicated port list.      'full' (+19 more)

### Community 22 - "Community 22"
Cohesion: 0.03
Nodes (21): transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap, 63d9c9a fix(probe): recover from 409 when device key already enrolled, b5ffcb0 Refactor Vedha probe installer and enhance device identity tests- Updated the installer script to require only the manager endpoint in dry run mode, removing unnecessary prompts for credentials.- Changed the default behavior of LICENSE_ENFORCED to false.- Improved error handling for unknown arguments and missing required parameters in the installer.- Added tests for device identity generation, signing, and verification, ensuring robust handling of key encoding and site policy enforcement.- Enhanced HTTP lease tests to cover edge cases for lease renewal and cancellation.- Introduced tests for installer contract to ensure no human credentials are present in the source.- Updated result spool tests to handle permanent rejections and ensure proper quarantine behavior.- Improved transport tests to validate device enrollment and access token rotation.- Enhanced WebSocket claim protocol tests to verify job claiming with additional parameters., An operator cancel (409) is DEFINITIVE, unlike a flaky network.      The grace b, test_revoked_lease_cancels_the_attempt_immediately(), _dry_run(), test_installer_accepts_enroll_token_and_insecure_for_http_manager(), test_installer_without_token_still_shows_manual_approval() (+13 more)

### Community 23 - "Community 23"
Cohesion: 0.04
Nodes (38): apiFetch(), clearSession(), loadSession(), saveSession(), serverUrl(), Session, SESSION_DIR, SESSION_FILE (+30 more)

### Community 24 - "Community 24"
Cohesion: 0.04
Nodes (43): Agent, AIBrainPage(), AiStatus, criticalChain, defaultAgents, Engagement, Finding, findings (+35 more)

### Community 25 - "Community 25"
Cohesion: 0.05
Nodes (53): AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient, propose_candidates(), ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look, Test double — a fixed lookup table, no network. Used to validate the     surroun (+45 more)

### Community 26 - "Community 26"
Cohesion: 0.07
Nodes (43): _banner_jsonl(), _empty_epss(), _empty_jsonl(), _empty_kev(), _mock_vuln_db(), _openssh_upstream_vuln_db(), _openssh_vuln_db(), Tests for pipeline.py — the orchestrator with 0% prior coverage.  Covers the cri (+35 more)

### Community 27 - "Community 27"
Cohesion: 0.04
Nodes (24): 22701ea Add tests for scanner parity and enhance use case resolution- Introduced  to ensure that the scanner directory is in sync with the main_scripts directory, preventing silent code drift.- Updated  to include additional assertions for use case resolution, intensity handling, and validation of unique use case codes.- Enhanced  to clarify the build process for sealed probes.- Added  command to  for printing the vendor public key derived from the private key.- Implemented  to introduce a new intensity knob for scanning, allowing operators to specify scan depth and breadth.- Modified  to support port overrides based on intensity settings and introduced a SYN scanning method for efficiency.- Created  script to verify that the sealed binary matches the source manifest, ensuring build integrity., scan_health.py — turn the probe's per-host scan completeness/health metrics into, Aggregate result['scan_metrics'] into a coverage/health verdict.        degraded, scan_health_summary(), classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re (+16 more)

### Community 28 - "Community 28"
Cohesion: 0.12
Nodes (55): A, ask(), askSecret(), banner(), buildInteractiveCommand(), choose(), chooseNextPhase(), confirm() (+47 more)

### Community 29 - "Community 29"
Cohesion: 0.05
Nodes (48): accept_echo_reply(), build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), fingerprint_os(), hop_estimate(), _icmp(), icmp_supported() (+40 more)

### Community 30 - "Community 30"
Cohesion: 0.04
Nodes (46): classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology(), main(), mdns_hostname(), _nb_encode() (+38 more)

### Community 31 - "Community 31"
Cohesion: 0.05
Nodes (44): BaseModel, AiGenerateResponse, AiMessage, LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated, PersonalAccessTokenOut, TokenResponse (+36 more)

### Community 32 - "Community 32"
Cohesion: 0.10
Nodes (41): correlate_smb_patch(), dedup_findings(), correlate.py — dedup, authoritative-suppression, and cross-fact composite correl, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the, Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the (+33 more)

### Community 33 - "Community 33"
Cohesion: 0.08
Nodes (43): Base, DeclarativeBase, AgentRecommendation, agent_recommendation.py — decisions/actions proposed by the agentic AI advisor., AttackTimeline, Append-only ledger of every attack action performed during an engagement.      W, Base, TimestampMixin (+35 more)

### Community 34 - "Community 34"
Cohesion: 0.06
Nodes (51): _accepted(), _apply_regression_reopen(), create_findings_from_facts(), detect_all_from_facts(), detect_all_from_facts_traced(), detect_findings_from_facts(), _engagement_device_roles(), _ensure_importable() (+43 more)

### Community 35 - "Community 35"
Cohesion: 0.06
Nodes (18): FakeDiscovery, _FakeMSRPC, FakePortScanner, _make_funnel(), _OpenSetPortFactory, test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel, Port-scanner factory whose scanners report a port open iff it is in     `actuall, A deep scanner on 135 that returns EPM-advertised dynamic ports. (+10 more)

### Community 36 - "Community 36"
Cohesion: 0.07
Nodes (27): _atomic_write_json(), _bounded_gather(), build_campaign(), CampaignContext, CampaignOptions, CliProgressView, default_stages(), _discover_ipv6() (+19 more)

### Community 37 - "Community 37"
Cohesion: 0.05
Nodes (42): classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology(), main(), mdns_hostname(), _nb_encode() (+34 more)

### Community 38 - "Community 38"
Cohesion: 0.07
Nodes (40): activate_enrollment(), approve_enrollment(), approve_request_simple(), _authenticated_request(), auto_enroll_cidrs(), create_enroll_token(), create_enrollment_request(), _decode_public_key() (+32 more)

### Community 39 - "Community 39"
Cohesion: 0.07
Nodes (19): _monitor(), _r(), One false alarm must not disable the check for the rest of the scan., The whole point: 'we stopped early' must never read as 'nothing found'., Regression: "open|filtered" is the UDP no-reply verdict, not an open port.     R, The primary detector. Branch-failure evidence covers only the milliseconds     t, An offline host must reach the operator's screen, not just the fact list.     Ex, A host that is merely filtered is not a problem with the run. (+11 more)

### Community 40 - "Community 40"
Cohesion: 0.05
Nodes (12): _kexinit(), _nl(), Encode an SSH name-list: uint32 length + comma-joined ASCII., TestEvaluate, TestFullDBCoverage, TestMainScriptsParity, TestNoFalsePositives, TestParseKexinit (+4 more)

### Community 41 - "Community 41"
Cohesion: 0.07
Nodes (7): _finding(), TestAggregate, TestClassifyTier, TestComputePriority, TestDedupFindings, TestFindingConsistency, TestVerify

### Community 42 - "Community 42"
Cohesion: 0.06
Nodes (33): _boundary_versions(), _clear_caches(), _content_hash(), _default_products(), load_snapshot(), _merge_companion(), vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN, Raw OSV vulnerability records for this product, or [] if the         snapshot do (+25 more)

### Community 43 - "Community 43"
Cohesion: 0.05
Nodes (24): ActivityEvent, Agent, AiStatus, ApiKeysSection(), AuditLogSection(), ConfigField, DEFAULT_RULES, DeploymentStatus (+16 more)

### Community 44 - "Community 44"
Cohesion: 0.05
Nodes (14): Asset, _parse_ts(), PortFact, Dispatch a real ScanResult into the right sub-structure, keyed         on result, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep, Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep (+6 more)

### Community 45 - "Community 45"
Cohesion: 0.05
Nodes (38): device_hint(), HostDiscoveryScanner, is_locally_administered(), Neighbor, normalize_mac(), parse_nbstat(), parse_neighbor_line(), True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc (+30 more)

### Community 46 - "Community 46"
Cohesion: 0.07
Nodes (16): _fact(), Tests for ai_normalizer.py — 0% prior coverage.  Covers:   - extract_raw_text: p, Any exception from the AI client yields [] — never raises, never         blocks, When the cache already has an answer, the client must not be called., A candidate dict without a 'product' key must be silently skipped., If the client returns something that isn't a list, return []., Every candidate produced by propose_candidates must be tagged         ai_assiste, source_confidence on the resulting CPECandidate must match the         originati (+8 more)

### Community 47 - "Community 47"
Cohesion: 0.10
Nodes (42): _ids(), test_main_scripts_findings.py — the findings interpretation layer.  Pure-logic,, _run(), test_accepts_scanresult_objects_not_just_dicts(), test_all_security_headers_present_no_finding(), test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_double_report(), test_confirmed_ftp_cleartext_is_high_confidence() (+34 more)

### Community 48 - "Community 48"
Cohesion: 0.10
Nodes (22): _added(), _client(), _db_first(), _db_for_create(), _db_list(), _db_scalar(), _engagement(), _finding() (+14 more)

### Community 49 - "Community 49"
Cohesion: 0.14
Nodes (34): build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout(), cmd_auth_status(), cmd_daemon_run() (+26 more)

### Community 50 - "Community 50"
Cohesion: 0.10
Nodes (21): get_settings(), Settings, BaseSettings, RuntimeError, AiGenerateRequest, AiProviderStatus, AiStatusResponse, Raised when a required configuration invariant is violated at boot. (+13 more)

### Community 51 - "Community 51"
Cohesion: 0.06
Nodes (40): approve_scan_request(), AssignAgentBody, build_scan_job(), ClientUserCreate, ClientUserOut, ClientUserPatch, CustomerListItem, _existing_client_user() (+32 more)

### Community 52 - "Community 52"
Cohesion: 0.07
Nodes (16): _make_db(), _make_tenant(), _make_user(), Tests for authentication login flow.  Covers:   - login success   - user_not_fou, Ensure every exception class has the expected reason_code attribute.     These c, AsyncSession mock that returns user on first execute, tenant on second., TestAuthenticateBcryptFailure, TestAuthenticateDatabaseFailure (+8 more)

### Community 53 - "Community 53"
Cohesion: 0.08
Nodes (25): _asset(), _corpus(), _fact(), _fire(), test_service_posture_rules.py — the service-layer rule pack.  These 14 rules cov, no-auth is strictly worse and is reported instead., The live-host case: negotiation returned RDP_NEG_FAILURE so no `nla`         key, The regression this fixes: `nla` was declared in `requires` even though (+17 more)

### Community 54 - "Community 54"
Cohesion: 0.05
Nodes (27): scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, test_network_va_accuracy.py — end-to-end accuracy of the network_va use case.  E, The regression this guards: these ports were outside the 40-port catalog,     so, Positive protocol evidence turns the botnet-C2 port guess into an     observatio, 4444 says nothing. The scanner must record that, not invent a service., Every deep branch that ran must have produced facts or have had a port to     ju, service_banner now proves non-TLS by attempting a handshake, so silent     binar, network_va composes device classification and the exposure matrix. (+19 more)

### Community 55 - "Community 55"
Cohesion: 0.07
Nodes (28): Load a previously spooled result, returning None if missing/corrupt., Remove the spool file for a successfully uploaded result., Remove the spool file for a successfully uploaded result., Attempt to upload a result with retries and local spool as fallback.          Ar, Move a terminally rejected result out of the retry queue., Re-attempt upload of all previously spooled results.          Called once at pro, Attempt to upload a result with retries and local spool as fallback.          Ar, Number of pending (unsubmitted) results in the spool. (+20 more)

### Community 56 - "Community 56"
Cohesion: 0.07
Nodes (39): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+31 more)

### Community 57 - "Community 57"
Cohesion: 0.06
Nodes (21): fuse_liveness(), _now(), host_discovery.py — determine which hosts are alive, with graded confidence.  ME, PTR lookup; None on any failure. Runs in _RDNS_POOL, never on the loop., Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a, Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a, Combine TCP + UDP + neighbor signals into a confidence-scored verdict.      `udp, _reverse_dns() (+13 more)

### Community 58 - "Community 58"
Cohesion: 0.07
Nodes (39): build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest(), _key_share_ext(), _one_probe(), parse_server_hello() (+31 more)

### Community 59 - "Community 59"
Cohesion: 0.10
Nodes (10): _candidate(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db(), TestEnrichFinding, TestEpssDb, TestKevDb, TestMatchCandidate (+2 more)

### Community 60 - "Community 60"
Cohesion: 0.07
Nodes (29): test_ipv6_wiring.py — IPv6 neighbour discovery inside the engagement.  An IPv4 /, The core restraint: discovery must not widen authorization., Only the scan types that opt in pay for the multicast ping., _run(), test_disabled_by_default(), test_discovery_failure_does_not_abort_the_engagement(), test_in_scope_neighbour_is_added_and_scanned(), test_out_of_scope_neighbour_is_reported_but_never_probed() (+21 more)

### Community 61 - "Community 61"
Cohesion: 0.07
Nodes (31): test_os_stage_wiring.py — the OS-identification stage in the agent workflow.  Be, test_cached_os_fact_is_reused_not_reprobed(), test_os_stage_runs_for_a_port_stage_job(), test_rescan_mode_reprobes_a_stale_os_fact(), test_stack_hints_from_syn_scan_reach_the_os_scanner(), TestPlan, _wire(), assessment() (+23 more)

### Community 62 - "Community 62"
Cohesion: 0.07
Nodes (26): manager_fingerprint(), Stable identity for the manager a credential belongs to.      Device credentials, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent, Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields., Merge and atomically persist private state while preserving fields. (+18 more)

### Community 63 - "Community 63"
Cohesion: 0.07
Nodes (11): _port_fact(), test_accuracy_gate.py — the accuracy MERGE GATE (roadmap #4 / Tier 1.3).  `accur, CI's actual assertion: the engine still matches every labeled corpus., Without one of these the gate proves only non-drift, never accuracy., Locks in the measured results: every port state agrees with nmap on         both, TestCli, TestCorpusValidation, TestProvenance (+3 more)

### Community 64 - "Community 64"
Cohesion: 0.07
Nodes (35): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response() (+27 more)

### Community 65 - "Community 65"
Cohesion: 0.08
Nodes (32): _align8(), build_ntlmssp_negotiate(), _der(), _der_len(), _encryption_context(), _netbios_session(), ntlm_os_build(), parse_ntlm_challenge() (+24 more)

### Community 66 - "Community 66"
Cohesion: 0.07
Nodes (13): DBScanner, interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act, FakeReader, FakeWriter, _probe() (+5 more)

### Community 67 - "Community 67"
Cohesion: 0.07
Nodes (35): _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, _mqtt_connect(), _mqtt_remaining_len(), _mqtt_subscribe_all(), _parse_coap_response() (+27 more)

### Community 68 - "Community 68"
Cohesion: 0.08
Nodes (32): _align8(), build_ntlmssp_negotiate(), _der(), _der_len(), _encryption_context(), _netbios_session(), ntlm_os_build(), parse_ntlm_challenge() (+24 more)

### Community 69 - "Community 69"
Cohesion: 0.09
Nodes (23): AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator, DatabaseConnectivityValidator, DatabaseURLValidator, DetectionEngineValidator (+15 more)

### Community 70 - "Community 70"
Cohesion: 0.10
Nodes (19): _db_scalar(), _FakeDB, _finding(), _GenAI, _GenUnavailable, _one_result(), _operator(), test_remediation_routes.py — Section 5: operator remediation endpoints + wiring. (+11 more)

### Community 71 - "Community 71"
Cohesion: 0.09
Nodes (14): A host that rate-limits its RSTs answers only when probed gently. The     fast s, Silent for the first `answer_after` probes per port, then a real RST., Corrected ports must be recorded ONCE, with their final state., A converged estimator can be tuned to a path that was dropping us., Congestion control must react to a CHANGE in delivery, not to a steady     rate, ~97% definitive (the measured RST-suppressing host) must NOT throttle., A genuinely lossy path (verified separately with 60% netem loss) must         st, Never throttle on a handful of early probes. (+6 more)

### Community 72 - "Community 72"
Cohesion: 0.08
Nodes (25): _compute_priority(), _cache_key(), _clear_caches(), EpssDB, KevDB, load_epss(), load_kev(), enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as vuln_d (+17 more)

### Community 73 - "Community 73"
Cohesion: 0.12
Nodes (23): ADConnectionError, build_ad_finding(), DependencyMissingError, severity_from_str(), ACE, ADComputer, ADGroup, ADUser (+15 more)

### Community 74 - "Community 74"
Cohesion: 0.06
Nodes (31): device_hint(), HostDiscoveryScanner, is_locally_administered(), Neighbor, normalize_mac(), parse_nbstat(), parse_neighbor_line(), Parse a NetBIOS NBSTAT (node status) response (RFC 1002 §4.2.18).      Returns { (+23 more)

### Community 75 - "Community 75"
Cohesion: 0.11
Nodes (27): _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _decode_oid(), _decode_value(), _encode_oid() (+19 more)

### Community 76 - "Community 76"
Cohesion: 0.09
Nodes (31): config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES, Client, ClientJiraConfig, ClientNotifyConfig (+23 more)

### Community 77 - "Community 77"
Cohesion: 0.08
Nodes (30): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+22 more)

### Community 78 - "Community 78"
Cohesion: 0.08
Nodes (30): Delta, DeltaEngine, _extract_service(), _extract_version(), main(), _new_service_severity(), delta_scanner.py — scan-state comparison and continuous attack-surface monitorin, Best-effort service name from data dict or scanner name. (+22 more)

### Community 79 - "Community 79"
Cohesion: 0.12
Nodes (30): buildToolsCommand(), C, ln(), showSpinner(), downloadFile(), extract(), getInstalledRecord(), installAll() (+22 more)

### Community 80 - "Community 80"
Cohesion: 0.09
Nodes (17): AssetCriticality, OrderedDict, AssetIn, AssetOut, BulkAssetImportResult, parse_csv_assets(), Parse CSV text into a list of AssetIn models and error strings., Add NVD CVSS, EPSS, KEV flag, MITRE techniques, and composite risk.         Muta (+9 more)

### Community 81 - "Community 81"
Cohesion: 0.06
Nodes (7): test_cve_correlation.py — the offline CVE-correlation layer (cve/ package).  Thi, TestCli, TestCorrelate, TestCpe, TestIngestFeeds, TestIngestPagination, TestRiskScore

### Community 82 - "Community 82"
Cohesion: 0.13
Nodes (15): _epss(), _fact(), _finding(), _kev(), test_exploitability.py — CISA KEV + FIRST EPSS on the POSTURE track.  The CVE tr, Severity is the rule's judgement of the weakness. Exploitation         evidence, A re-rank here must never disagree with the original scoring, so the         two, The pipeline may enrich the same finding twice (a re-run, or a caller         th (+7 more)

### Community 83 - "Community 83"
Cohesion: 0.09
Nodes (10): test_weakness_map.py — the weakness -> canonical-CVE bridge (cve/weakness_map.py, A detect-stage fact: ScanResult('findings', ..., data=Finding.to_dict())., A bare Finding dict (findings.py --json output)., _raw(), TestCliCorrelateMerges, TestCliStatus, TestCorrelateWeaknesses, TestFindingView (+2 more)

### Community 84 - "Community 84"
Cohesion: 0.11
Nodes (33): _data(), Finding, Fuse OS signals across scanners into ONE identification with calibrated     conf, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only (+25 more)

### Community 85 - "Community 85"
Cohesion: 0.07
Nodes (15): Tests for loader error paths in vuln_db.py and enrichment_db.py.  These are the, The FileNotFoundError message should mention re-syncing, so         operators kn, The ValueError for a hash mismatch must include truncated hashes         in the, A path that doesn't exist must raise FileNotFoundError with a         helpful me, A snapshot whose records don't match the stored content_hash must         raise, Completely broken JSON must propagate as an exception — never         silently y, A JSON file that is valid JSON but missing the 'records' key         must raise, A well-formed snapshot must load without error and return a VulnDB         that (+7 more)

### Community 86 - "Community 86"
Cohesion: 0.08
Nodes (13): _client(), _operator(), test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping au, `jwt.py` states the portal audience exists "so it can be rejected on     operato, `/portal` must not authorize `/portalsomething` or a crafted path., `/auth/refresh` must re-mint the SAME credential class the login issued.      Lo, Same rule as login: never mint an unscoped client token., TestAssertClient (+5 more)

### Community 87 - "Community 87"
Cohesion: 0.12
Nodes (10): _asset(), _fact(), test_posture_rules.py — the manager posture/config detection engine.  Covers: th, The live tls_scanner labels its probe list "TLSv1_0"/"TLSv1_1" (from         ssl, TestHardenedGroundTruth, TestInvariants, TestRiskModel, TestTrustTier (+2 more)

### Community 88 - "Community 88"
Cohesion: 0.19
Nodes (21): use_cases.py — the finite, pre-defined library of scan scenarios the manager can, backup-before-secret-removal, feat/probe-usecase-alignment, spike/probe-go, worktree-fleet-already-downloaded-cmd, 01f4398 feat(probe): IoT survey reaches the banner stage (service_fingerprint), 0510df3 going to build prompt and connection, architecture almost done, 5c8e696 docs(probe): correct overclaiming use-case descriptions to match current behavior (+13 more)

### Community 89 - "Community 89"
Cohesion: 0.09
Nodes (31): _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part(), dpkg_compare(), _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), has_ambiguous_epoch() (+23 more)

### Community 90 - "Community 90"
Cohesion: 0.10
Nodes (18): is_world_readable(), NFSScanner, parse_mount_export(), parse_portmap_dump(), _parse_rpc_reply(), nfs_scanner.py — NFS export exposure over ONC RPC (VA checklist: anonymous netwo, An export with no client restriction, or one shared to a wildcard group,     is, Send one ONC-RPC CALL (AUTH_NULL) over a TCP record-marked stream and     return (+10 more)

### Community 91 - "Community 91"
Cohesion: 0.10
Nodes (18): is_world_readable(), NFSScanner, parse_mount_export(), parse_portmap_dump(), _parse_rpc_reply(), nfs_scanner.py — NFS export exposure over ONC RPC (VA checklist: anonymous netwo, An export with no client restriction, or one shared to a wildcard group,     is, Send one ONC-RPC CALL (AUTH_NULL) over a TCP record-marked stream and     return (+10 more)

### Community 92 - "Community 92"
Cohesion: 0.09
Nodes (29): AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError, ExpiredPasswordError, JWTFailureError (+21 more)

### Community 93 - "Community 93"
Cohesion: 0.11
Nodes (24): _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database(), _check_jwt_secret(), _check_redis(), _check_required_env_vars() (+16 more)

### Community 94 - "Community 94"
Cohesion: 0.08
Nodes (20): FindingSeverity, NucleiMatch, boundedEnvMs(), OpenVASFinding, OpenVASHelperOutput, OpenVASTaskState, parseOpenVASHelperOutput(), runOpenVASScanBackground() (+12 more)

### Community 95 - "Community 95"
Cohesion: 0.10
Nodes (29): check_thresholds(), CorpusError, format_gate_report(), is_independent(), load_corpora(), load_corpus(), _main(), True when this corpus's labels can support an ACCURACY claim. (+21 more)

### Community 96 - "Community 96"
Cohesion: 0.09
Nodes (22): _assistant_finding_view(), create_scan_request(), _enum_val(), _metric_finding(), portal_agents(), portal_assistant_chat(), portal_engagement(), portal_finding_remediation() (+14 more)

### Community 97 - "Community 97"
Cohesion: 0.16
Nodes (23): _ask(), _client(), _db(), _engagement(), _finding(), _llm(), test_portal_assistant.py — the customer-facing AI assistant.  Free-form chat was, The schema has no context field, so a client cannot inject its own     'evidence (+15 more)

### Community 98 - "Community 98"
Cohesion: 0.07
Nodes (26): JobResult, prepare_result_dir(), Orchestrates one scan job's lifecycle.      The runner holds injected dependenci, Args:             http_get:       Callback for authenticated GET (from Transport, Execute a complete scan job lifecycle.          Args:             job: Job dict, Structured result from running one scan job., Submit the result, with spool-and-retry if available., Structured result from running one scan job. (+18 more)

### Community 99 - "Community 99"
Cohesion: 0.10
Nodes (19): _classify_confidence(), _extract_aliases(), ingest_file(), ingest_files(), IngestResult, _is_ip(), QuarantinedLine, ingest.py — stream-read scanner_module JSONL output, validate, assemble per-host (+11 more)

### Community 100 - "Community 100"
Cohesion: 0.09
Nodes (25): bulk_import_assets(), campaign_progress(), _compute_overview(), create_engagement(), detection_explain(), engagements_overview(), _job_phase(), _overview_cache_key() (+17 more)

### Community 101 - "Community 101"
Cohesion: 0.11
Nodes (16): Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup., Re-registering the same-named probe must reuse the row, not create a dup., Agent token must outlive the 15-min access default so it doesn't churn., Re-registering the same-named probe must reuse the row, not create a dup. (+8 more)

### Community 102 - "Community 102"
Cohesion: 0.08
Nodes (13): _at(), test_reference.py — the human-readable reference scheme.  A scan job could only, Migration 0036 backfills in SQL so it needs no application layer. If the     two, A backfilled reference must match what the row would have been given         whe, The whole point of the scheme: a human relays it., The prefix and date are literal — folding them would corrupt a date., It is quoted in tickets — it must not move., test_the_migration_backfill_agrees_with_the_application() (+5 more)

### Community 103 - "Community 103"
Cohesion: 0.07
Nodes (4): _ConcurrencyScanner, _ExplodingScanner, test_host_fanout_is_bounded(), test_per_target_exception_preserves_other_results()

### Community 104 - "Community 104"
Cohesion: 0.10
Nodes (19): _metric(), _not_scored(), Pure helpers for controlled Probe capability and accuracy validation., Validate the small, explicit inventory used for accuracy scoring., Score promoted inventory against explicit host/port/service/CVE truth., Resolve suites plus explicit use-cases, preserving first-seen order., Require every IP/CIDR target to be fully allowed and not excluded., Return the conservative number of addresses represented by targets. (+11 more)

### Community 105 - "Community 105"
Cohesion: 0.07
Nodes (18): apiFetch(), Cat, CATS, Engagement, EngineManifest, getToken(), Intensity, JobStatus (+10 more)

### Community 106 - "Community 106"
Cohesion: 0.10
Nodes (21): AssetVerdict, coverage_summary(), exposure_timeline(), get_path(), _identity_keys(), IdentityResult, _iso(), naive_ip_identity() (+13 more)

### Community 107 - "Community 107"
Cohesion: 0.08
Nodes (12): _cache_with(), test_probe_next_features.py — the probe_next plan: run the improved main_scripts, test_device_inventory_post_stage_classifies_from_open_ports(), test_device_inventory_skips_hosts_without_evidence(), test_exposure_matrix_flags_internet_reachable_ports(), test_exposure_matrix_internal_only_from_lan_vantage(), test_no_post_stage_for_ordinary_scan_types(), intensity_port_override() (+4 more)

### Community 108 - "Community 108"
Cohesion: 0.12
Nodes (14): _job(), _ok_result(), test_result_archive.py — the local result archive written before submission.  Th, A read-only filesystem must cost a warning, never a scan result., Unset env => alongside agent/ scanner/ workflow/ (in the image, /app/result)., The agent creates the archive directory at boot so the operator sees the     pat, The Linux bind-mount case: Docker creates the source as root, so the         dir, The disable latch is module state; keep tests independent. (+6 more)

### Community 109 - "Community 109"
Cohesion: 0.09
Nodes (12): aggregate(), ConsistencyReport, FindingConsistency, format_line(), consistency.py — Phase 5: N-run consistency & reporting.  "A single scan is an a, run_findings: one list of Findings per run (N runs). Aggregated by     the deter, The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru, Wilson score interval for a binomial proportion k/n, as percentages.     Chosen (+4 more)

### Community 110 - "Community 110"
Cohesion: 0.13
Nodes (8): _finding(), test_finding_events.py — the finding lifecycle audit trail.  The synthesis half, TestEventTypeForStatus, TestMerge, TestPatchAudits, TestSynthesize, TestTimelineEndpoint, _types()

### Community 111 - "Community 111"
Cohesion: 0.20
Nodes (23): _count(), _db(), _job(), _one(), Operator job control: stop a running job, remove a queued one, and cap the queue, An operator stop must never be mistaken for a system fault., Two queued jobs must leave room for a third — an off-by-one here         would s, Pins the reason this endpoint may not reference `.email`.      If CurrentUser ev (+15 more)

### Community 112 - "Community 112"
Cohesion: 0.08
Nodes (23): GzipRequestMiddleware, Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard., Identify the Manager API without exposing a second dashboard. (+15 more)

### Community 113 - "Community 113"
Cohesion: 0.11
Nodes (13): build_fleet(), demo(), openssh_below(), Tests for the evidence store, and a demo that puts numbers on the strategic clai, Not merely coarse -- wrong. It splits one machine and merges two., No rescan. The whole point., Regression guard. An OR over history means a patched host stays vulnerable, Drifted payload: the probe ran, the field moved. (+5 more)

### Community 114 - "Community 114"
Cohesion: 0.07
Nodes (6): _EchoProtocol, test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit., TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating, TestWindowStateMachine

### Community 115 - "Community 115"
Cohesion: 0.13
Nodes (9): _asset(), _by_port(), _fact(), A catalog entry is a guess about what a port means. When service_banner     posi, A shell answering on a benign-listed port is still a backdoor: the         contr, test_exposed_findings_flow_through_detect_posture(), TestDetect, TestObservedServiceSignals (+1 more)

### Community 116 - "Community 116"
Cohesion: 0.14
Nodes (12): _finding(), _get_raising(), _get_returning(), _nvd_bytes(), _nvd_empty(), test_online.py — the OPT-IN live enrichment layer (cve/online.py).  Every test i, A fake transport that ignores its args and returns fixed bytes., A CVEFinding as the offline pass would emit it — CVSS None models a mirror gap. (+4 more)

### Community 117 - "Community 117"
Cohesion: 0.07
Nodes (8): test_scope_targets.py — the pure scope-authorization core shared by the dispatch, Whatever the validator accepts must be provably inside the scope., test_property_every_accepted_target_is_subnet_of_scope(), TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected, TestTargetsWithinScope

### Community 118 - "Community 118"
Cohesion: 0.08
Nodes (23): GraphWebSocketManager, High-level manager for graph-specific WebSocket operations., Broadcast graph data update to all subscribers., Broadcast a single node update., High-level manager for graph-specific WebSocket operations., High-level manager for graph-specific WebSocket operations., Broadcast layout change to all subscribers., Broadcast graph data update to all subscribers. (+15 more)

### Community 119 - "Community 119"
Cohesion: 0.10
Nodes (10): BaseScanner, TLSFingerprintScanner, Preferred scheme first, the other as a fallback: a scheme guess must         nev, WebScanner, MobileScanner, Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO, main(), RDPScanner (+2 more)

### Community 120 - "Community 120"
Cohesion: 0.10
Nodes (22): Agent, AgentCapability, AGENTS, agentsStore, AgentStatus, ensureDataDir(), FIELD_AGENTS_FILE, FieldAgent (+14 more)

### Community 121 - "Community 121"
Cohesion: 0.10
Nodes (20): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+12 more)

### Community 122 - "Community 122"
Cohesion: 0.15
Nodes (12): _added(), _mock_db(), _operator(), _pending_request(), test_customer_access.py — Phase 1: operator provisioning + scan-request inbox. H, An email already used elsewhere in the tenant (the operator's own login,, db.execute yields the given scalar_one_or_none values in order., TestApproveScanRequest (+4 more)

### Community 123 - "Community 123"
Cohesion: 0.11
Nodes (6): _fact(), TestAsset, TestCorrelateSmbPatch, TestNormalize, TestNormalizeBanner, TestNormalizeDb

### Community 124 - "Community 124"
Cohesion: 0.15
Nodes (24): _d(), _dns_zone_transfer(), _ftp_anonymous(), _ipmi_cipher_zero(), _ldap_anonymous_bind(), _msrpc_exposed(), _nfs_world_readable(), PostureRule (+16 more)

### Community 125 - "Community 125"
Cohesion: 0.09
Nodes (24): apply_manual_reopen(), build_coverage(), decide_resolution(), evaluate_resolutions(), host_of(), resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c, Apply decide_resolution to every engine-managed open/confirmed finding     NOT t, Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r (+16 more)

### Community 126 - "Community 126"
Cohesion: 0.12
Nodes (16): _Cursor, _dedup(), evaluate_algorithms(), parse_kexinit(), parse_ssh_banner(), ssh_scanner.py — SSH configuration / algorithm audit (VA checklist §6).  METHOD, Parse a SSH_MSG_KEXINIT body into its name-lists.      Accepts the payload with, Grade a server's offered algorithms against the vendored weakness table.      Re (+8 more)

### Community 127 - "Community 127"
Cohesion: 0.12
Nodes (16): _Cursor, _dedup(), evaluate_algorithms(), parse_kexinit(), parse_ssh_banner(), ssh_scanner.py — SSH configuration / algorithm audit (VA checklist §6).  METHOD, Parse a SSH_MSG_KEXINIT body into its name-lists.      Accepts the payload with, Grade a server's offered algorithms against the vendored weakness table.      Re (+8 more)

### Community 128 - "Community 128"
Cohesion: 0.10
Nodes (20): _atomic_write_json(), _bounded_gather(), build_campaign(), CampaignContext, CampaignOptions, default_stages(), _discover_ipv6(), va_campaign.py — the sequential Network Vulnerability-Assessment campaign.  WHY (+12 more)

### Community 129 - "Community 129"
Cohesion: 0.08
Nodes (11): Project timestamps render in IST, and stay timezone-AWARE while doing it.  Opera, Rendering moved; the instant did not., The ordering guarantee that makes this change safe., A `Z` on a local-time stamp is an outright lie., The timestamp that ends up inside every result file., A bad VEDHA_TZ must never take a scan down mid-engagement., Sealed/slim images may ship no tzdata. IST has no DST, so the fixed         +05:, TestFileStamps (+3 more)

### Community 130 - "Community 130"
Cohesion: 0.10
Nodes (6): _finding(), test_remediation_generator.py — Section 3: the AI remediation-plan helpers.  Pur, TestGenerateRemediationPlan, TestNormalizeAiPlan, TestParseJsonResponse, TestSafeCommands

### Community 131 - "Community 131"
Cohesion: 0.11
Nodes (12): _fact(), Run-scoped facts must not be scope-checked as if they were hosts.  THE BUG THIS, Authorization is IP/CIDR-only; a hostname must not pass., The pre-existing <nmap-run> exemption this fix is modelled on., The exact payload that caused the 422., Same record, but an interface actually resolved — still not a host., The damage was collateral: one non-host descriptor discarded every         legit, The exemption must be narrow. These are the security assertions. (+4 more)

### Community 132 - "Community 132"
Cohesion: 0.08
Nodes (7): test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi, TestHttpMatch, TestNoMatch, TestOtherServices, TestProbeLadder, TestScannerIntegration, TestSshMatch

### Community 133 - "Community 133"
Cohesion: 0.13
Nodes (20): NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS (+12 more)

### Community 134 - "Community 134"
Cohesion: 0.10
Nodes (24): _by_target(), _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay(), _corr_user_enum_plus_weak_auth(), Finding (+16 more)

### Community 135 - "Community 135"
Cohesion: 0.12
Nodes (11): make_smb2_error(), make_smb2_success(), test_main_scripts_hardening.py — verifies the Phase-1 correctness fixes applied, A 64-byte SMB2 header. Caller prepends a 4-byte NBT transport prefix, so     Pro, STATUS_INVALID_PARAMETER error response: same header, body StructureSize 9,, _run(), _scope(), _smb2_header() (+3 more)

### Community 136 - "Community 136"
Cohesion: 0.08
Nodes (1): TestResultSpool

### Community 137 - "Community 137"
Cohesion: 0.14
Nodes (15): KerberoastChecker, KerberoastChecker — find SPN-bearing accounts and capture TGS hashes as *offline, Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., Render the TGS as a hashcat $krb5tgs$ string (etype 23/RC4 layout)., One aggregate Finding for all kerberoastable accounts.         Severity is Criti, One aggregate Finding for all kerberoastable accounts.         Severity is Criti, Enumerate kerberoastable accounts and capture TGS evidence., Enumerate kerberoastable accounts and capture TGS evidence. (+7 more)

### Community 138 - "Community 138"
Cohesion: 0.09
Nodes (23): Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Poll pending jobs even while WS is connected.      This makes result delivery re, Release a staged job only after the manager confirms its claim., Re-submit previously spooled results over WebSocket., Release a staged job only after the manager confirms its claim., Re-submit previously spooled results over WebSocket., Poll pending jobs even while WS is connected.      This makes result delivery re (+15 more)

### Community 139 - "Community 139"
Cohesion: 0.16
Nodes (16): CampaignSnapshot, CampaignStatus, CampaignSummary, CampaignTotals, DEFAULT_DIR, ensureDir(), fileFor(), getCampaign() (+8 more)

### Community 140 - "Community 140"
Cohesion: 0.11
Nodes (11): _cloud(), The advisor_flow rules instruct the model to use lifecycle facts, and the     re, Settings with provider unset and all cloud keys pinned, so .env cannot     leak, Settings with provider unset and all cloud keys pinned, so .env cannot     leak, test_advisor_flow_prompt_grounds_lifecycle_facts(), test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter(), test_default_auto_detects_the_configured_cloud_provider(), test_default_runtime_fails_closed_without_any_cloud_key() (+3 more)

### Community 141 - "Community 141"
Cohesion: 0.20
Nodes (10): _asset(), _fact(), _outcome(), test_posture_trace.py — the detection trace: every rule evaluation records an OU, I10 structurally: for EVERY rule with a declared contract, feeding a fact, TestAbsentVersusClean, TestBehaviourPreserved, TestNoEvidence (+2 more)

### Community 142 - "Community 142"
Cohesion: 0.12
Nodes (8): _challenge(), test_smb_ntlm_build.py — Card 5: exact Windows build from the SMB2 pre-auth NTLM, Synthesize an NTLMSSP CHALLENGE (Type-2). TargetName payload sits right after, Regression: _recv_smb_frame STRIPS the 4-byte NBT prefix, so the SMB2 header, TestBuildMap, TestNtlmFingerprintFraming, TestParseChallenge, TestType1AndSpnego

### Community 143 - "Community 143"
Cohesion: 0.21
Nodes (16): _CM, _hb(), _job(), Stage 2 — reconciled campaign completion + worker liveness.  Proves the correctn, _rows(), _run(), _scalars(), test_dead_lettered_facts_event_is_error() (+8 more)

### Community 144 - "Community 144"
Cohesion: 0.15
Nodes (16): _detect_stage(), test_va_campaign.py — the VA-campaign orchestrator (scanner/va_campaign.py).  Th, _reporter(), _run(), _scope(), test_catalog_ids_are_unique_and_match_default_stages(), test_detect_stage_skipped_when_nothing_was_collected(), test_detect_stage_turns_facts_into_weakness_findings() (+8 more)

### Community 145 - "Community 145"
Cohesion: 0.11
Nodes (22): _dbg(), _detect_primary_ipv4(), _is_local_manager_url(), main(), _poll_jobs_or_empty(), _preflight_scope_check(), Bounded reachability preflight. Proceeds the moment the Manager answers     /hea, Bounded reachability preflight. Proceeds the moment the Manager answers     /hea (+14 more)

### Community 146 - "Community 146"
Cohesion: 0.13
Nodes (17): discover_ipv6_hosts(), _is_ipv6(), main(), _own_ipv6_addresses(), parse_ip_neigh6(), parse_ndp(), _ping_all_nodes(), ipv6_discovery.py — link-local IPv6 host discovery via Neighbor Discovery (RFC 4 (+9 more)

### Community 147 - "Community 147"
Cohesion: 0.12
Nodes (13): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), _NoRedirect, mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH, Server/body fingerprint match against known non-AI squatters, or None. (+5 more)

### Community 148 - "Community 148"
Cohesion: 0.09
Nodes (3): _EchoProtocol, test_async_udp.py — tests for the true-async UDP probe helper in scanner_base., _SinkProtocol

### Community 149 - "Community 149"
Cohesion: 0.13
Nodes (15): _cc(), test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detec, A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU., A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU., _run(), test_cc_without_negotiation_is_standard_rdp(), test_confirmed_rdp_wins_dedup_over_port_hint(), test_confirmed_rdp_with_nla_has_no_nla_finding() (+7 more)

### Community 150 - "Community 150"
Cohesion: 0.11
Nodes (6): _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_background_job_failed(), test_partial_nuclei_run_preserves_findings_and_diagnostics()

### Community 151 - "Community 151"
Cohesion: 0.16
Nodes (4): _asset(), TestAssetNeedsRecheckLive, TestGate5, TestGate6

### Community 152 - "Community 152"
Cohesion: 0.09
Nodes (9): Manager-side project time: render in IST, stay timezone-AWARE.  The manager stor, The property that makes this safe next to existing UTC data., Every naive datetime in this codebase's history came from utcnow().         Assu, Guards the actual bug: utcnow() strings carried no offset., test_websocket_no_longer_emits_naive_timestamps(), TestFileStamp, TestOverrideAndFallback, TestRendering (+1 more)

### Community 153 - "Community 153"
Cohesion: 0.09
Nodes (7): test_smb_ldap_scanners.py — SMB null-session + LDAP anonymous-bind enumeration., ldap3 packs receive_timeout into a struct for SO_RCVTIMEO, so it must be an, TestLDAPScanner, TestLDAPTimeoutTypes, TestMainScriptsParity, TestMergeUsers, TestRidRanges

### Community 154 - "Community 154"
Cohesion: 0.13
Nodes (11): _make_http_mock(), Unit tests for VulnEnrichmentService — all external HTTP calls mocked., Create a mock httpx.AsyncClient that returns different responses per URL., test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full(), test_fetch_epss_success() (+3 more)

### Community 155 - "Community 155"
Cohesion: 0.10
Nodes (21): _check_anti_debug(), Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Detect common debugging/tracing tools.  Informational only — does     NOT block, Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation., Acknowledge an offer without executing it before claim confirmation., Persistent WebSocket push loop.      Returns False if WebSocket is unavailable ( (+13 more)

### Community 156 - "Community 156"
Cohesion: 0.10
Nodes (21): _flush_spool_over_http(), Retry durable result files using the acknowledged HTTP result path., Retry durable result files using the acknowledged HTTP result path., Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (, Persistent WebSocket push loop.      Returns False if WebSocket is unavailable ( (+13 more)

### Community 157 - "Community 157"
Cohesion: 0.10
Nodes (21): _load_or_create_signing_identity(), Load or atomically create the probe's Ed25519 enrollment identity., Load or atomically create the probe's Ed25519 enrollment identity., Run all startup security checks before any network I/O.      Order matters: HW b, Run all startup security checks before any network I/O.      Order matters: HW b, Load or atomically create the probe's Ed25519 enrollment identity., Load or atomically create the probe's Ed25519 enrollment identity., Load or atomically create the probe's Ed25519 enrollment identity. (+13 more)

### Community 158 - "Community 158"
Cohesion: 0.10
Nodes (18): Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Refresh a device token before expiry; legacy identities are unchanged., Refresh a device token before expiry; legacy identities are unchanged., Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Send a heartbeat to the manager.          Returns True if the heartbeat was acce, Refresh a device token before expiry; legacy identities are unchanged. (+10 more)

### Community 159 - "Community 159"
Cohesion: 0.13
Nodes (15): attack_path_findings(), _exposed_db_unauth(), _group(), _HostSignals, _is_domain_controller(), _is_network_device(), _legacy_windows(), _ntlm_relay() (+7 more)

### Community 160 - "Community 160"
Cohesion: 0.14
Nodes (16): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con (+8 more)

### Community 161 - "Community 161"
Cohesion: 0.13
Nodes (18): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), MobileScanner, _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd() (+10 more)

### Community 162 - "Community 162"
Cohesion: 0.13
Nodes (15): _coverage(), _device_hint(), _is_readable(), _listener_error_code(), _open_listener(), PassiveCollector, PassiveListenerError, _printable_strings() (+7 more)

### Community 163 - "Community 163"
Cohesion: 0.12
Nodes (14): _dec(), match_service(), parse_http_head(), One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., Pull status code, the identifying headers and the <title> out of an     HTTP/RTS (+6 more)

### Community 164 - "Community 164"
Cohesion: 0.15
Nodes (15): _decode(), _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _merge_users(), parse_rid_ranges(), smb_enum_scanner.py — SMB null-session enumeration (VA checklist: anonymous info, Enumerate domain/local users via the SAMR named pipe, reusing the null     sessi (+7 more)

### Community 165 - "Community 165"
Cohesion: 0.12
Nodes (14): _dec(), match_service(), parse_http_head(), One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, One probe-ladder rung on its own connection. Returns banner bytes, b""         (, Soft-match collected bytes to {service, product, version}; None if unknown., Pull status code, the identifying headers and the <title> out of an     HTTP/RTS (+6 more)

### Community 166 - "Community 166"
Cohesion: 0.15
Nodes (15): _decode(), _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _merge_users(), parse_rid_ranges(), smb_enum_scanner.py — SMB null-session enumeration (VA checklist: anonymous info, Enumerate domain/local users via the SAMR named pipe, reusing the null     sessi (+7 more)

### Community 167 - "Community 167"
Cohesion: 0.13
Nodes (19): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it. (+11 more)

### Community 168 - "Community 168"
Cohesion: 0.14
Nodes (9): A campaign whose jobs all ended without producing results must reach a TERMINAL, The normal path must be untouched: a completed job with no run yet is         ge, Precedence: work in flight is reported before any terminal verdict., One good job is enough to expect a detection run., Regression guard: the happy path and its known edge cases still hold., Callers that don't pass the new inputs must behave as before., _status(), TestNormalPipelineUnaffected (+1 more)

### Community 169 - "Community 169"
Cohesion: 0.12
Nodes (6): FakeClient, test_cmd_doctor_success_with_online_agent(), test_cmd_scan_run_builds_dispatch_payload(), test_poll_job_rejects_invalid_timing(), test_poll_job_returns_terminal_status(), test_poll_job_times_out()

### Community 170 - "Community 170"
Cohesion: 0.13
Nodes (17): _ctx, _fact(), test_detection_pipeline_gaps.py — four ways facts reached the manager and then f, An older probe reports none. Coverage stays empty and nothing auto-resolves —, Facts are persisted whenever they are present, but the outbox enqueue used to, Minimal async-context-manager wrapper around a mock session., `data` is read with .get() by every rule. A string there used to raise mid-run, attack_path_findings runs on meta['accepted_facts']. If that still contained (+9 more)

### Community 171 - "Community 171"
Cohesion: 0.10
Nodes (5): Pure-logic tests for the ARP/MAC/mobile-detection helpers in host_discovery. No, TestDeviceHint, TestLocallyAdministered, TestNormalizeMac, TestVendorLookup

### Community 172 - "Community 172"
Cohesion: 0.12
Nodes (7): Probe-side operator job control + polling-noise suppression.  Two independent be, These may be transient/refreshable, so they must NOT read as a cancel         —, The probe polls forever; routine transport chatter must stay out of the     term, The actual regression: one INFO line per poll, every POLL_INTERVAL., Quieting must not hide a genuinely unreachable manager., TestHeartbeatOutcomes, TestPollingNoiseIsSuppressed

### Community 173 - "Community 173"
Cohesion: 0.14
Nodes (8): _mount_export_reply(), _portmap_dump_reply(), test_nfs_scanner.py — NFS export enumeration over ONC RPC.  The live RPC path ne, TestNFSFindings, TestNFSScanner, TestParity, TestXdrParsers, _xstr()

### Community 174 - "Community 174"
Cohesion: 0.10
Nodes (6): test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe +, TestIcmpBuilders, TestIcmpCapability, TestInetChecksum, TestRemoteClock, TestSmbBuildEnrichment

### Community 175 - "Community 175"
Cohesion: 0.14
Nodes (4): _scan_result(), TestCacheEntry, TestClassifyCertainty, TestWorkflowCache

### Community 176 - "Community 176"
Cohesion: 0.15
Nodes (10): _heartbeat_interval(), HostHealthMonitor, _HostState, Tracks per-host reachability across the deep-scan stages.      `liveness_probe`, True when a component ran and got nothing back that proves life.          An emp, Feed one component's results in.          Only pass components that had POSITIVE, Re-probe a suspected host and record the verdict.          Returns VERDICT_OFFLI, Heartbeat a host for as long as it is being scanned.          This, not the stri (+2 more)

### Community 177 - "Community 177"
Cohesion: 0.15
Nodes (18): _clean(), _main(), _parse_args(), _port_label(), _ports_from_env(), local_run.py — run the probe's REAL pipeline (workflow.run_engagement) directly, Actionable input error on stderr → exit code 2. No traceback: this is     operat, Validate positional args (args[0]=target, [1]=profile, [2]=stage, [3]=filter) (+10 more)

### Community 178 - "Community 178"
Cohesion: 0.10
Nodes (18): Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active., True if the WebSocket connection is active., Fetch the engagement's authoritative scope.          Returns the response dict i, Fetch the engagement's authoritative scope.          Returns the response dict i, True if the WebSocket connection is active. (+10 more)

### Community 179 - "Community 179"
Cohesion: 0.14
Nodes (9): DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-path engine.  Produces a small but realist, Returns {engagement_id, assets, services, findings, credentials,     network_top, Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci, TestGraphVisualizer (+1 more)

### Community 180 - "Community 180"
Cohesion: 0.10
Nodes (20): _by_target(), _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay(), _corr_user_enum_plus_weak_auth(), Two or more cleartext services on one host — any sniffing position harvests, Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h (+12 more)

### Community 181 - "Community 181"
Cohesion: 0.13
Nodes (12): _decode_value(), _encode_oid(), _extract_sysdescr(), _oid_in_subtree(), Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli, Return (community, sysdescr) for the first responding community, or None., GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]., One GETBULK request — measure response/request size ratio. (+4 more)

### Community 182 - "Community 182"
Cohesion: 0.15
Nodes (19): build_timeline(), _decorate(), _detected_actor(), _detected_detail(), _ev(), event_type_for_status(), merge_timeline(), finding_events.py — the finding lifecycle audit trail.  Two sources feed one tim (+11 more)

### Community 183 - "Community 183"
Cohesion: 0.17
Nodes (19): aggregate(), build_posture(), _clamp01(), compare(), compute_scores(), _exploit_prob(), FindingView, grade_for() (+11 more)

### Community 184 - "Community 184"
Cohesion: 0.17
Nodes (4): test_agent_policy.py — the pure deterministic agent policy engine., _roe(), TestClassifyAction, TestEvaluateAction

### Community 185 - "Community 185"
Cohesion: 0.10
Nodes (1): TestUDPProbeConstruction

### Community 186 - "Community 186"
Cohesion: 0.15
Nodes (17): _port_intel(), test_risk_port_coverage.py — the collection half of the exposed-service rules., A connect scan is one socket per port per host, so this list is a cost as     we, The sweep is profile catalog UNION the TCP branch tables; a regression that, The complement of the rule above, pinned so a future edit cannot quietly     add, Exactly what a default network_va puts on the wire: the profile catalog     plus, Called out separately: these carry the highest severity and were 100%     unscan, Reverse direction: VA_RISK_PORTS must not accumulate ports the manager has     n (+9 more)

### Community 187 - "Community 187"
Cohesion: 0.11
Nodes (5): test_tls_fingerprint.py — Tier 2.3: active TLS fingerprint (JARM methodology)., _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello

### Community 188 - "Community 188"
Cohesion: 0.12
Nodes (4): _modern(), test_tls_posture.py — Tier 2.4: cipher-suite classification + TLS posture gradin, TestClassifyCipher, TestGradeTlsPosture

### Community 189 - "Community 189"
Cohesion: 0.13
Nodes (10): ASREPRoastChecker, ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and, Enumerate AS-REP roastable accounts and capture AS-REP evidence., Usernames of enabled accounts with pre-authentication not required., Request an AS-REP for ``username`` with no credentials and return the         $k, Render an AS-REP as a hashcat $krb5asrep$ string (no decryption)., ADAssessmentRunner, ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu (+2 more)

### Community 190 - "Community 190"
Cohesion: 0.11
Nodes (19): _job_intent(), Human label for what a job will actually run — the use-case (real intent),     n, Human label for what a job will actually run — the use-case (real intent),     n, One-line, transparent summary of what a scan actually found so the operator, One-line, transparent summary of what a scan actually found so the operator, One-line, transparent summary of what a scan actually found so the operator, Run one job while keeping WS status/result frames best-effort., Run one job while keeping WS status/result frames best-effort. (+11 more)

### Community 191 - "Community 191"
Cohesion: 0.11
Nodes (16): DeviceAlreadyEnrolledError, _enrollment_conflict_detail(), EnrollmentRequestNotFound, Best-effort extraction of the manager's 409 ``detail`` message., Best-effort extraction of the manager's 409 ``detail`` message., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls., True if we have both an agent_id and a token for API calls. (+8 more)

### Community 192 - "Community 192"
Cohesion: 0.11
Nodes (17): Generic authenticated GET, returns parsed JSON or None on failure.          Used, Refresh a device token before expiry; legacy identities are unchanged., Generic authenticated GET, returns parsed JSON or None on failure.          Used, Establish an authenticated WebSocket connection to the manager.          Returns, Establish an authenticated WebSocket connection to the manager.          Returns, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Generic authenticated GET, returns parsed JSON or None on failure.          Used, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of (+9 more)

### Community 193 - "Community 193"
Cohesion: 0.11
Nodes (19): _as_int(), normalize_intensity(), Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id, Return (scan_type, profile, intensity) for a job.      Resolution order:     1., Coerce an int-or-numeric-string to int, else None (non-numeric)., Map a numeric use-case code → use_case_id (raises on an unknown code)., Accept an intensity as a number (1/2/3) OR a name; return the name.      None st (+11 more)

### Community 194 - "Community 194"
Cohesion: 0.18
Nodes (18): _cvss(), _get(), ingest_all(), ingest_epss(), ingest_kev(), ingest_nvd(), ingest_one_cve(), _iter_cpe_matches() (+10 more)

### Community 195 - "Community 195"
Cohesion: 0.13
Nodes (17): _calibrate_host_findings(), compute_risk(), detect_all_traced(), detect_exposed_services(), detect_posture_traced(), _evidence_ref(), _exposed_title(), is_validated() (+9 more)

### Community 196 - "Community 196"
Cohesion: 0.14
Nodes (18): create_findings_from_probe_result(), create_scan_health_finding(), _escalate_by_exposure(), _find_open_duplicate(), _finding_port(), _map_severity(), Bump severity one rung when the finding's service is internet-reachable     (Ser, A still-relevant Finding with the same (engagement, asset, title), if any. (+10 more)

### Community 197 - "Community 197"
Cohesion: 0.12
Nodes (6): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples., test_main_scripts_adaptive_timeout.py — Phase 7: per-host adaptive probe timeout

### Community 198 - "Community 198"
Cohesion: 0.14
Nodes (15): build_connection_request(), main(), parse_connection_confirm(), _posture_from_selected(), probe_rdp(), probe_rdp_posture(), Two-probe RDP posture (MS-RDPBCGR 2.2.1.1.1 / 2.2.1.2.1).      Probe A offers SS, TPKT + X.224 Connection Request carrying an RDP Negotiation Request. (+7 more)

### Community 199 - "Community 199"
Cohesion: 0.15
Nodes (14): classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):, Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl, Never send an IP literal as SNI — non-conformant; some servers reject it., Attempt a handshake forcing one protocol version. Returns cipher dict or None. (+6 more)

### Community 200 - "Community 200"
Cohesion: 0.16
Nodes (19): _data(), Fuse OS signals across scanners into ONE identification with calibrated     conf, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4X-based threat-intel match. Fires only when a certificate's structural     fi, Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a, JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only, JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only (+11 more)

### Community 201 - "Community 201"
Cohesion: 0.14
Nodes (16): _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), _parse_adb_header(), _parse_mdns_ptr_names(), _probe_adb(), _probe_lockdownd(), _probe_mdns_mobile_sync() (+8 more)

### Community 202 - "Community 202"
Cohesion: 0.14
Nodes (18): _db_with(), _event(), test_pipeline_concurrency.py — the two correctness fixes from ADR-0001.  R1: the, The guard must not swallow real work., Pre-existing behaviour: a vanished scan_result logs and returns rather     than, The lock must be taken BEFORE the first read, or the race it prevents can     st, pg_advisory_lock (session) would leak on any path that forgets to unlock.     Th, Two concurrent handlers must contend, so the key has to be a pure function     o (+10 more)

### Community 203 - "Community 203"
Cohesion: 0.17
Nodes (7): _asset(), _by_rule(), _fact(), test_posture_confidence.py — calibrated, auditable posture confidence with cross, TestAssessor, TestChains, TestEndToEnd

### Community 204 - "Community 204"
Cohesion: 0.19
Nodes (7): CertTemplate, ADCSChecker — Active Directory Certificate Services template misconfiguration an, _enum_with_entries(), _FakeAttr, _FakeEntry, Unit tests for the Active Directory assessment module (Prompt 5).  All directory, TestLDAPEnumeratorParsing

### Community 205 - "Community 205"
Cohesion: 0.13
Nodes (16): AgentDeps, AgentOpts, configure_logging(), isBlocked(), Install a root log handler for the daemon.      Nothing on the daemon path calle, Install a root log handler for the daemon.      Nothing on the daemon path calle, Install a root log handler for the daemon.      Nothing on the daemon path calle, requiresApproval() (+8 more)

### Community 206 - "Community 206"
Cohesion: 0.17
Nodes (16): _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError, license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the, Combined startup gauntlet: HW bind → license check. Fails fast.      This is the (+8 more)

### Community 207 - "Community 207"
Cohesion: 0.12
Nodes (16): Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Refresh routing metadata using the cached agent identity.          Returns True, Merge and atomically persist private state while preserving fields., Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Submit a scan result to the manager.          Returns True ONLY on a 2xx respons, Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True, Refresh routing metadata using the cached agent identity.          Returns True (+8 more)

### Community 208 - "Community 208"
Cohesion: 0.14
Nodes (4): _norm(), vulndb.py — the offline vulnerability mirror (SQLite) and its query surface.  Ho, All vulnerable CVEs whose CPE applicability covers (vendor, product,         ver, VulnDB

### Community 209 - "Community 209"
Cohesion: 0.18
Nodes (17): _all_known_cve_ids(), main(), _query_osv(), update_snapshot.py — the ONLY module in this package that talks to the network., The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, The full CISA Known Exploited Vulnerabilities catalog — a single flat     list,, EPSS scores for exactly the CVE IDs this detection run actually cares     about, EPSS scores for exactly the CVE IDs this detection run actually cares     about (+9 more)

### Community 210 - "Community 210"
Cohesion: 0.16
Nodes (9): PathAnalyzer, _priority(), Return scored attack paths from every source asset to the target.         Each p, Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for, Assets that appear in more than ``threshold`` (default 50%) of all paths —, Assets reachable (and thus at risk) if ``compromised_asset_id`` is owned., Best (easiest) exploitable finding on an asset: {cvss, weight, finding}., Build (and cache) the Asset→Asset movement projection. Edge weight is the (+1 more)

### Community 211 - "Community 211"
Cohesion: 0.16
Nodes (8): derive_zones(), DNSScanner, _is_ip(), dns_scanner.py — DNS server hygiene: zone transfer (AXFR), DNSSEC presence, and, Ask the target (as a resolver) for the PTR of its own IP — a common way, Attempt a zone transfer, reading incrementally and stopping at         MAX_AXFR_, Blocking orchestration of the DNS checks. Monkeypatchable for tests., Candidate zone names to try AXFR / DNSSEC against, most-confident first.      Ex

### Community 212 - "Community 212"
Cohesion: 0.17
Nodes (9): banner_software(), FTPScanner, parse_pasv(), ftp_scanner.py — FTP anonymous-access check (VA checklist: anonymous file exposu, Confirm anonymous READ via PASV + LIST, reading a bounded amount., Extract the passive data PORT from a 227 reply. We connect to the TARGET     on, Best-effort software token from the 220 greeting (e.g. 'vsFTPd 3.0.3')., Read one (possibly multi-line) FTP reply; return (code, full_text). (+1 more)

### Community 213 - "Community 213"
Cohesion: 0.17
Nodes (10): build_ipp_get_printer_attributes(), _ipp_attr(), parse_ipp_make_model(), parse_pjl_id(), PrinterScanner, printer_scanner.py — network printer exposure (VA checklist: exposed print servi, Extract the model string from a PJL INFO ID response., A minimal IPP/1.1 Get-Printer-Attributes request body (RFC 8010). (+2 more)

### Community 214 - "Community 214"
Cohesion: 0.14
Nodes (8): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =, test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive, _run(), test_protected_redis_raises_no_unauth_finding(), test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_flagged()

### Community 215 - "Community 215"
Cohesion: 0.17
Nodes (9): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages(), _r(), test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ "Multi-vantag (+1 more)

### Community 216 - "Community 216"
Cohesion: 0.12
Nodes (14): OSError, NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings. (+6 more)

### Community 217 - "Community 217"
Cohesion: 0.16
Nodes (8): derive_zones(), DNSScanner, _is_ip(), dns_scanner.py — DNS server hygiene: zone transfer (AXFR), DNSSEC presence, and, Ask the target (as a resolver) for the PTR of its own IP — a common way, Attempt a zone transfer, reading incrementally and stopping at         MAX_AXFR_, Blocking orchestration of the DNS checks. Monkeypatchable for tests., Candidate zone names to try AXFR / DNSSEC against, most-confident first.      Ex

### Community 218 - "Community 218"
Cohesion: 0.17
Nodes (9): banner_software(), FTPScanner, parse_pasv(), ftp_scanner.py — FTP anonymous-access check (VA checklist: anonymous file exposu, Confirm anonymous READ via PASV + LIST, reading a bounded amount., Extract the passive data PORT from a 227 reply. We connect to the TARGET     on, Best-effort software token from the 220 greeting (e.g. 'vsFTPd 3.0.3')., Read one (possibly multi-line) FTP reply; return (code, full_text). (+1 more)

### Community 219 - "Community 219"
Cohesion: 0.15
Nodes (13): _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results(), mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con, target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them., Excluded networks -> masscan --exclude specs, so they get ZERO packets., A CIDR spec is in scope only if it is fully contained in an allowed network. (+5 more)

### Community 220 - "Community 220"
Cohesion: 0.17
Nodes (10): build_ipp_get_printer_attributes(), _ipp_attr(), parse_ipp_make_model(), parse_pjl_id(), PrinterScanner, printer_scanner.py — network printer exposure (VA checklist: exposed print servi, Extract the model string from a PJL INFO ID response., A minimal IPP/1.1 Get-Printer-Attributes request body (RFC 8010). (+2 more)

### Community 221 - "Community 221"
Cohesion: 0.12
Nodes (12): BaseScanner, One observation about one target. Pure fact, no interpretation.      Network-sta, One observation about one target. Pure fact, no interpretation.      Network-sta, One observation about one target. Pure fact, no interpretation.      Network-sta, Subclasses implement `scan_target(self, target)` (async), returning a list     o, One observation about one target. Pure fact, no interpretation., One observation about one target. Pure fact, no interpretation., Subclasses implement `scan_target(self, target)` (async), returning a list     o (+4 more)

### Community 222 - "Community 222"
Cohesion: 0.22
Nodes (16): _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext(), _decode_oid(), _oid_tlv(), _parse_varbinds() (+8 more)

### Community 223 - "Community 223"
Cohesion: 0.20
Nodes (15): _get(), _ids(), test_attack_path_correlation.py — manager-native composite correlation over prob, test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_device_role_from_facts_also_amplifies(), test_exposed_db_with_unauth_is_critical(), test_exposed_db_without_unauth_does_not_fire() (+7 more)

### Community 224 - "Community 224"
Cohesion: 0.14
Nodes (14): clean_guard_cache(), Tests for the P1+P2 performance optimization of the detection engine.  P1 — vers, dpkg_compare must use the pure-Python comparator in the hot path.     Shelling o, Isolate the guard's in-memory + on-disk validation cache per test., No dpkg binary → nothing to cross-check against; return [] and never     attempt, When the binary disagrees with pure-Python on an adjacent pair, that pair     is, test_clear_caches_forces_reload(), test_dpkg_compare_does_not_call_the_binary() (+6 more)

### Community 225 - "Community 225"
Cohesion: 0.11
Nodes (7): Tests for seed_admin.py.  Covers:   - first deployment: creates tenant + admin,, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset, TestFirstDeployment, TestHashHelpers, TestPasswordRotation

### Community 226 - "Community 226"
Cohesion: 0.21
Nodes (1): TestServiceIdentifier

### Community 227 - "Community 227"
Cohesion: 0.12
Nodes (13): AgentConnectionManager, Record transport features explicitly advertised by a connected probe., Record transport features explicitly advertised by a connected probe., Record transport features explicitly advertised by a connected probe., Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected., Subscribe to the push backplane and forward any job whose target agent         i (+5 more)

### Community 228 - "Community 228"
Cohesion: 0.14
Nodes (9): CacheEntry, classify_certainty(), In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, True if there's no cached entry, OR the entry is uncertain         (always worth, True if there's no cached entry, OR the entry is uncertain         (always worth, True if there's no cached entry, OR the entry is uncertain         (always worth, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c, In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c (+1 more)

### Community 229 - "Community 229"
Cohesion: 0.16
Nodes (6): ExecutionTrace, Mutable per-run component accounting, serialized only after completion., Mutable per-run component accounting, serialized only after completion., Accumulate wall time for one component.          Without this, `scanner_runs` sa, True when execution produced errors and no usable or cached facts., True when execution produced errors and no usable or cached facts.

### Community 230 - "Community 230"
Cohesion: 0.13
Nodes (7): BloodHoundCollector, Load nodes (users/computers/groups) and MemberOf edges into Neo4j.          Retu, Ingest one BloodHound collector file. Returns (#nodes, #rels)., Return shortest attack paths from any non-DA principal to a Domain Admins, Build a Finding summarising the shortest paths to Domain Admins., Run bloodhound-python and return the list of produced JSON file paths.         R, TestBuildADFinding

### Community 231 - "Community 231"
Cohesion: 0.12
Nodes (17): _classify_connection_error(), _enroll_device(), _manager_reachable(), Request UI approval, poll, prove key possession, and activate., Request UI approval, poll, prove key possession, and activate., Request UI approval, poll, prove key possession, and activate., Request UI approval, poll, prove key possession, and activate.      `_recreate_b, Request UI approval, poll, prove key possession, and activate.      `_recreate_b (+9 more)

### Community 232 - "Community 232"
Cohesion: 0.12
Nodes (16): _atomic_write_private_state(), Durably replace one private JSON state file without exposing secrets., Durably replace one private JSON state file without exposing secrets., Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name, Register the probe with the manager.          Args:             name: Probe name (+8 more)

### Community 233 - "Community 233"
Cohesion: 0.21
Nodes (5): AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()

### Community 234 - "Community 234"
Cohesion: 0.15
Nodes (16): assert_client(), client_scoped(), portal_scope.py — the customer-portal authorization boundary.  Every customer-po, Return the client's bound engagement id, or 403.      403 (never 404) is deliber, Return the client's bound engagement id, or 403.      403 (never 404) is deliber, The safe engagement id to filter by.      A caller-supplied engagement_id is hon, The safe engagement id to filter by.      A caller-supplied engagement_id is hon, The single choke point every portal SELECT must pass through: restricts the (+8 more)

### Community 235 - "Community 235"
Cohesion: 0.18
Nodes (15): addComment(), Case, CaseActivity, CaseComment, CaseSeverity, CaseStatus, createCase(), DATA_FILE (+7 more)

### Community 236 - "Community 236"
Cohesion: 0.23
Nodes (16): addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser(), ipToInt(), isAdmin(), isEmailAllowed() (+8 more)

### Community 237 - "Community 237"
Cohesion: 0.14
Nodes (5): DBScanner, interpret_redis_info(), _probe_redis(), db_scanner.py — fingerprint database services.  WHY: databases are everywhere on, Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act

### Community 238 - "Community 238"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 239 - "Community 239"
Cohesion: 0.18
Nodes (9): _handshake(), parse_modules(), rsync_scanner.py — rsync daemon anonymous-module exposure (VA checklist: anonymo, Select a module without a secret: OK => anonymous, AUTHREQD => auth., Blocking: list modules, then anon-test each. Monkeypatchable for tests., Parse the daemon's module listing into [{name, comment}]. Lines are     'name<wh, Read the @RSYNCD greeting and echo it back VERBATIM. Returns the negotiated, _recv_until() (+1 more)

### Community 240 - "Community 240"
Cohesion: 0.16
Nodes (14): _candidate_ports(), FunnelResult, _is_alive(), scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 0, The full outcome of funnelling one host., The port set worth scanning = union of every route's ports (deduped)., Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur (+6 more)

### Community 241 - "Community 241"
Cohesion: 0.18
Nodes (15): _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed(), ja4s_from_serverhello(), JA4S from `parse_server_hello`'s output ({version, cipher, extensions})., JA4S from raw ServerHello record bytes (reuses the JARM parser). (+7 more)

### Community 242 - "Community 242"
Cohesion: 0.23
Nodes (5): _monotonic(), _now(), ProgressReporter, Owns the live campaign record. Every transition recomputes percent + ETA,     wr, StageState

### Community 243 - "Community 243"
Cohesion: 0.24
Nodes (15): _detect_drift(), _hash(), _log(), log_error(), log_info(), log_warn(), main(), Warn if the tenant has multiple admins or a stale admin email. (+7 more)

### Community 244 - "Community 244"
Cohesion: 0.14
Nodes (16): _identity_ip(), Return result identities outside the job's authoritative IP scope.      Fail clo, Parse a probe identity as an IP, tolerating common host:port notation., Return result identities outside the job's authoritative IP scope.      Fail clo, Recursively strip NUL (U+0000) from every string in a result payload.      Defen, Return network identities that could create assets or findings.      Scanner-lev, Stable idempotency checksum for one attempt completion payload., Return network identities that could create assets or findings.      Scanner-lev (+8 more)

### Community 245 - "Community 245"
Cohesion: 0.12
Nodes (1): TestSNMPBerUtilities

### Community 246 - "Community 246"
Cohesion: 0.15
Nodes (7): _fv(), _Row, test_build_posture_buckets_resolved_new_persisting(), test_build_posture_single_run_has_no_prev(), test_compute_scores_uses_risk_epss_exploit_and_asset_criticality(), test_finding_views_handles_null_asset_and_scores(), test_finding_views_maps_columns_and_asset_criticality()

### Community 247 - "Community 247"
Cohesion: 0.18
Nodes (5): _f(), test_remediation_kb.py — the pure deterministic remediation knowledge base., TestClassify, TestRecipeForFinding, TestRecipeShape

### Community 248 - "Community 248"
Cohesion: 0.17
Nodes (7): _FakeSock, A synthetic Linux `struct tcp_info`: 8 u8 flag bytes then 20 u32 fields., TCP_MAXSEG on an ESTABLISHED socket is the post-options effective         segmen, End-to-end form of the same guarantee, through os_fingerprint., THE accuracy guarantee for #6b.          os_fingerprint scores `tcp_window` agai, _tcp_info_buf(), TestHarvestTcpStack

### Community 249 - "Community 249"
Cohesion: 0.15
Nodes (11): _LegacyTLSServer, test_tls_legacy_versions.py — the deprecated-TLS detection must measure the SERV, A version the probe cannot OFFER is 'not tested', not 'server refused'., When the probe genuinely cannot test a version, the result must say so     inste, A loopback server pinned to exactly one (legacy) TLS version., Skip rather than fail on a build with the legacy protocol compiled out., _self_signed(), _server_supports() (+3 more)

### Community 250 - "Community 250"
Cohesion: 0.13
Nodes (13): Remove an agent's WebSocket registration., Remove the current registration, optionally only for one socket.          Return, Remove the current registration, optionally only for one socket.          Return, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to the first online connected agent.          Returns the agent_id th, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job, Push a job to a specific agent over WebSocket.          Returns True if the job (+5 more)

### Community 251 - "Community 251"
Cohesion: 0.13
Nodes (13): Handle a new WebSocket client connection., Handle incoming WebSocket messages., Handle a new WebSocket client connection., Handle incoming WebSocket messages., Handle incoming WebSocket messages., Handle a new WebSocket client connection., Handle a new WebSocket client connection., Handle incoming WebSocket messages. (+5 more)

### Community 252 - "Community 252"
Cohesion: 0.28
Nodes (8): asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder, is_internet_exposed(), service_node_id(), _to_float()

### Community 253 - "Community 253"
Cohesion: 0.14
Nodes (12): NmapExecutionError, _parse_nmap_xml(), nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree, Actionable subprocess failure; never reinterpret it as zero findings., Actionable subprocess failure; never reinterpret it as zero findings. (+4 more)

### Community 254 - "Community 254"
Cohesion: 0.17
Nodes (10): classify_security_types(), parse_rfb_version(), vnc_scanner.py — VNC/RFB authentication exposure (VA checklist: unauthenticated, Blocking: RFB version handshake + read offered security types.         Monkeypat, Parse a 'RFB 003.008' banner into (major, minor), or None if not RFB., Turn a list of offered security-type ids into a verdict., Read the offered security types, handling the RFB 3.3 (single 4-byte type)     v, _read_security_types() (+2 more)

### Community 255 - "Community 255"
Cohesion: 0.20
Nodes (15): approve_validation(), create_validation_request(), _default_check_kind(), _get_request_or_404(), list_validation_requests(), _load_finding_and_eng(), Approval-gated safe active-validation API (P3).  POST /engagements/{id}/findings, RoE gate: active validation is allowed unless the engagement's RoE     explicitl (+7 more)

### Community 256 - "Community 256"
Cohesion: 0.21
Nodes (15): discover_ipv6_hosts(), _is_ipv6(), main(), _own_ipv6_addresses(), parse_ip_neigh6(), parse_ndp(), _ping_all_nodes(), ipv6_discovery.py — link-local IPv6 host discovery via Neighbor Discovery (RFC 4 (+7 more)

### Community 257 - "Community 257"
Cohesion: 0.15
Nodes (11): _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), MCPAIScanner, _model_count(), Server/body fingerprint match against known non-AI squatters, or None., Server/body fingerprint match against known non-AI squatters, or None., The strongest possible evidence for a real MCP server: a WWW-Authenticate     he (+3 more)

### Community 258 - "Community 258"
Cohesion: 0.17
Nodes (10): classify_security_types(), parse_rfb_version(), vnc_scanner.py — VNC/RFB authentication exposure (VA checklist: unauthenticated, Blocking: RFB version handshake + read offered security types.         Monkeypat, Parse a 'RFB 003.008' banner into (major, minor), or None if not RFB., Turn a list of offered security-type ids into a verdict., Read the offered security types, handling the RFB 3.3 (single 4-byte type)     v, _read_security_types() (+2 more)

### Community 259 - "Community 259"
Cohesion: 0.21
Nodes (10): _asset(), _FakeSession, Regression tests for AgentDecisionEngine._list_assets service batching.  The rea, Mimics the subset of a SQLAlchemy Result the read tools use., Returns queued results in call order and counts execute() calls., _Result, _svc(), test_list_assets_batches_services_no_n_plus_one() (+2 more)

### Community 260 - "Community 260"
Cohesion: 0.25
Nodes (15): _mock_session(), _now(), _sql(), test_boundary_at_exactly_the_lease_is_reclaimed(), test_dead_letter_and_requeue_are_mutually_exclusive(), test_dead_letter_stmt_targets_exhausted_stranded_rows(), test_expired_processing_lock_is_reclaimed(), test_fresh_processing_lock_is_not_reclaimed() (+7 more)

### Community 261 - "Community 261"
Cohesion: 0.17
Nodes (14): An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this, The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was     rea, A response with the wrong body StructureSize is not a valid NEGOTIATE., Step 13: expose signing_supported (protocol-precise), not only the     ambiguous, FIX 4: 3.1.1 IS now advertised, together with the mandatory preauth-integrity, _smb2_error_response(), _smb2_negotiate_response(), test_error_response_not_parsed_as_signing() (+6 more)

### Community 262 - "Community 262"
Cohesion: 0.14
Nodes (6): NTLMRelayChecker, Build a Finding for hosts missing SMB signing. The attack_narrative         incl, Probe SMB/LDAP signing posture across a host list., For each IP, returns {signing_enabled, signing_required}.          A host is rel, Returns True if the DC *enforces* LDAP signing / channel binding.          We at, TestASREPRoastChecker

### Community 263 - "Community 263"
Cohesion: 0.13
Nodes (15): _bounded_env_int(), Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Run an HTTP-claimed job while renewing its manager lease., Return an integer environment setting constrained to a safe range., Return an integer environment setting constrained to a safe range., Return an integer environment setting constrained to a safe range. (+7 more)

### Community 264 - "Community 264"
Cohesion: 0.13
Nodes (15): _obtain_identity(), Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)., Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64). (+7 more)

### Community 265 - "Community 265"
Cohesion: 0.15
Nodes (15): _derive_devices(), _derive_exposure(), _derive_post_stage(), Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur, Classify each target's device role from its collected facts (no I/O).     Return (+7 more)

### Community 266 - "Community 266"
Cohesion: 0.19
Nodes (8): extract_features(), Fit an XGBoost regressor on historical findings. ``historical_findings_df``, Return a 0–1000 priority score. Uses the model if trained, else the formula., Per-feature contribution to this prediction. Uses SHAP when available;         o, Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)., Build the model's feature vector from a Finding (+ optional Asset + extra     co, _to_float(), VulnPrioritizer

### Community 267 - "Community 267"
Cohesion: 0.18
Nodes (12): _as_dict(), _backport_marker(), correlate(), CVEFinding, mirror_age_note(), correlator.py — map probe facts to prioritized CVE findings.  Consumes the CPE i, Correlate facts carrying a CPE identity against the vuln DB. Deduped by     (cve, Human-readable note on how old the mirror is (from meta.last_ingest_utc),     pr (+4 more)

### Community 268 - "Community 268"
Cohesion: 0.13
Nodes (12): approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest, ExploitEvidence, ExploitJob, ExploitResult (+4 more)

### Community 269 - "Community 269"
Cohesion: 0.19
Nodes (7): parse_ehlo_capabilities(), smtp_scanner.py — SMTP hygiene: user enumeration + transport encryption (VA chec, Extract EHLO capability tokens from a multi-line 250 response., VRFY leaks usernames when it gives DIFFERENT definitive answers for an     exist, Blocking: greeting → EHLO → STARTTLS/VRFY/EXPN checks. Monkeypatchable., SMTPScanner, vrfy_leaks()

### Community 270 - "Community 270"
Cohesion: 0.23
Nodes (7): classify_os_error(), family_of(), main(), parse_ports(), PortScanner, RateLimiter, Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('

### Community 271 - "Community 271"
Cohesion: 0.21
Nodes (14): _build_upsert_stmt(), _cached_plan(), generate_remediation(), get_remediation(), remediation.py — per-finding remediation plans (operator-facing).  Two routes on, Fetch a finding scoped to the caller's tenant via its engagement., Fetch a finding scoped to the caller's tenant via its engagement., Build the atomic INSERT … ON CONFLICT DO UPDATE for a cached plan.      Pure (no (+6 more)

### Community 272 - "Community 272"
Cohesion: 0.13
Nodes (15): expand_targets(), Wire argparse args into a scanner instance and execute it., A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Wire argparse args into a scanner instance and execute it. (+7 more)

### Community 273 - "Community 273"
Cohesion: 0.19
Nodes (7): parse_ehlo_capabilities(), smtp_scanner.py — SMTP hygiene: user enumeration + transport encryption (VA chec, Extract EHLO capability tokens from a multi-line 250 response., VRFY leaks usernames when it gives DIFFERENT definitive answers for an     exist, Blocking: greeting → EHLO → STARTTLS/VRFY/EXPN checks. Monkeypatchable., SMTPScanner, vrfy_leaks()

### Community 274 - "Community 274"
Cohesion: 0.13
Nodes (11): Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., Discovery results → assets/services promotion (makes the Attack Surface populate, Discovery results → assets/services promotion (makes the Attack Surface populate, A single web scan can emit multiple facts for the same host:port., A single web scan can emit multiple facts for the same host:port. (+3 more)

### Community 275 - "Community 275"
Cohesion: 0.13
Nodes (5): A spec the profile tables don't know about could never run., gate_5 intersects open ports with its own table; the engine uses the         spe, A fact whose scanner name has no merge handler is collected, cached,         shi, An unlisted scanner falls back to 'uncertain' (re-probed every pass).         Th, TestRegistryConsistency

### Community 276 - "Community 276"
Cohesion: 0.18
Nodes (3): test_finding_section.py — the scanner-module trust view + the finding section., TestFindingSection, TestScannerRegistry

### Community 277 - "Community 277"
Cohesion: 0.13
Nodes (5): When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., When scope is fetched and targets are outside it., When scope fetch fails, manager-embedded scope is still enforced., TestRunnerScopeValidation

### Community 278 - "Community 278"
Cohesion: 0.15
Nodes (15): looks_like_db(), looks_like_http(), looks_like_ssh(), looks_like_tls(), True when a service banner carries a database greeting signature, so a DB     on, True when a service banner is an SSH identification string, so an SSH     server, For every open port with a banner fact, returns {port: {branches}}     that obse, True when this port's banner result is exactly the silent-on-garbage     signatu (+7 more)

### Community 279 - "Community 279"
Cohesion: 0.14
Nodes (14): _build_run_stats(), _hosts_from_facts(), Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port., Build promotion-ready hosts without duplicating scanner facts per port. (+6 more)

### Community 280 - "Community 280"
Cohesion: 0.14
Nodes (13): Register using a manager-side shared bootstrap key (no user login needed)., Register using a manager-side shared bootstrap key (no user login needed)., Raised when a transport operation fails permanently (not retryable)., Register using a manager-side shared bootstrap key (no user login needed)., Recursively remove NUL (U+0000) characters from every string in a payload., Raised when a transport operation fails permanently (not retryable)., Raised when a transport operation fails permanently (not retryable)., Register using a manager-side shared bootstrap key (no user login needed). (+5 more)

### Community 281 - "Community 281"
Cohesion: 0.20
Nodes (13): _apply(), enrich_findings(), lookup_nvd(), lookup_vulners(), OnlineResult, online.py — OPT-IN live enrichment for CVE findings.  The offline mirror (vulndb, Enrich CVE findings in place from live sources and return the same list.      `o, Fold one CVE's live result into a finding. FILLS a missing CVSS (and     recompu (+5 more)

### Community 282 - "Community 282"
Cohesion: 0.16
Nodes (12): _Assoc, correlate_weaknesses(), _finding_view(), _mirror_cve(), missing_from_mirror(), weakness_map.py — bridge the probe's deterministic weakness findings to canonica, Return the Finding dict from a fact, or None if the fact is not a finding., Pull CVSS/KEV/EPSS for one CVE straight from the mirror tables. Degrades to (+4 more)

### Community 283 - "Community 283"
Cohesion: 0.27
Nodes (13): createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), Job, JOBS_FILE (+5 more)

### Community 284 - "Community 284"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 285 - "Community 285"
Cohesion: 0.15
Nodes (12): async_udp_probe(), Wire argparse args into a scanner instance and execute it., Send one UDP datagram and await the first reply — fully on the event loop., Send one UDP datagram and await the first reply — fully on the event loop., Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., Wire argparse args into a scanner instance and execute it., Send one UDP datagram and await the first reply — fully on the event loop. (+4 more)

### Community 286 - "Community 286"
Cohesion: 0.18
Nodes (7): Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of allowed networks (for CIDR-level engines)., ScopeError, ScopeGuard

### Community 287 - "Community 287"
Cohesion: 0.20
Nodes (4): windows_collector.py — credentialed (authenticated) inventory for Windows hosts., Connect to RemoteRegistry over SMB and enumerate installed-software keys plus, _smb_registry_collect(), WindowsCollector

### Community 288 - "Community 288"
Cohesion: 0.24
Nodes (13): evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main(), _observed_states(), _ratio(), Run the findings engine over a labeled corpus and score it.      corpus = {name, (+5 more)

### Community 289 - "Community 289"
Cohesion: 0.21
Nodes (8): _handshake(), parse_modules(), Select a module without a secret: OK => anonymous, AUTHREQD => auth., Blocking: list modules, then anon-test each. Monkeypatchable for tests., Parse the daemon's module listing into [{name, comment}]. Lines are     'name<wh, Read the @RSYNCD greeting and echo it back VERBATIM. Returns the negotiated, _recv_until(), RsyncScanner

### Community 290 - "Community 290"
Cohesion: 0.16
Nodes (13): _candidate_ports(), FunnelResult, _is_alive(), The full outcome of funnelling one host., The port set worth scanning = union of every route's ports (deduped)., Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Map a host's open ports onto the deep-scanner routes that handle them.     Retur, Canonical open-TCP set for a host = deduped, sorted union of every source. (+5 more)

### Community 291 - "Community 291"
Cohesion: 0.14
Nodes (13): async_udp_probe(), async_udp_probe_retry(), Send one UDP datagram and await the first reply — fully on the event loop., Send one UDP datagram and await the first reply — fully on the event loop., Send one UDP datagram and await the first reply — fully on the event loop., `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, Send one UDP datagram and await the first reply — fully on the event loop. (+5 more)

### Community 292 - "Community 292"
Cohesion: 0.18
Nodes (8): choose_source_port(), The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p, Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p, Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i, ScopeError, ScopeGuard

### Community 293 - "Community 293"
Cohesion: 0.14
Nodes (2): The diagnostic that turns a silent stuck-pending job into a fixable         one:, TestAgentJobCompatibility

### Community 294 - "Community 294"
Cohesion: 0.22
Nodes (12): _manager(), _plant(), test_e2e_engagement_to_findings.py — the whole pipeline in one place.      manag, Exactly what the probe's smb/port scanners emit for a vulnerable host., Return (http_get, submit_result, captured) simulating the manager side., test_correlated_findings_cite_their_base_findings(), test_engagement_dispatch_reaches_probe_and_enforces_scope(), test_manager_correlation_finds_all_three_attack_paths() (+4 more)

### Community 295 - "Community 295"
Cohesion: 0.22
Nodes (13): _emitted_paths_by_scanner(), _ingest_corpus(), _load_corpus(), test_fact_contract.py — the machine-checkable contract between the probe's emitt, Reverse direction, informational: data the probe collects that NO rule reads., Map scanner -> set of top-level data keys it has been observed to emit., Run the corpus through the REAL ingester, exactly as engine_bridge does:     one, The gate the name-level check above cannot provide: a corpus whose field NAMES (+5 more)

### Community 296 - "Community 296"
Cohesion: 0.33
Nodes (13): _get(), _ids(), test_main_scripts_correlation.py — Epic 2: correlation findings.  Composite, hig, _run(), test_cleartext_cluster_fires_on_two_cleartext_services(), test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_rdp() (+5 more)

### Community 297 - "Community 297"
Cohesion: 0.25
Nodes (5): _mk_scanner(), _scope(), _summary(), TestDefaultsAndAdaptiveTimeout, TestWorkerPoolAndMetrics

### Community 298 - "Community 298"
Cohesion: 0.14
Nodes (1): TestMobileScanner

### Community 299 - "Community 299"
Cohesion: 0.14
Nodes (3): test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te, TestStableHostId, TestVersionChange

### Community 300 - "Community 300"
Cohesion: 0.14
Nodes (1): TestFingerprintOs

### Community 301 - "Community 301"
Cohesion: 0.14
Nodes (1): TestValidateTargetsInScope

### Community 302 - "Community 302"
Cohesion: 0.26
Nodes (7): _db(), _finding(), _operator(), test_sla_policy.py — per-tenant custom SLA windows (item 4)., _row(), TestPolicyAwareCompute, TestSlaPolicyRoutes

### Community 303 - "Community 303"
Cohesion: 0.23
Nodes (11): _probe(), test_vantage_fusion.py — fleet-level reconciliation of exposure_matrix across pr, Build a one-target probe exposure result. `ports` maps 'proto/port' →     {vanta, test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_hint_name(), test_external_vantage_open_makes_port_external(), test_fused_service_exposure_is_keyed_for_service_rows(), test_internal_only_when_no_external_probe_sees_open() (+3 more)

### Community 304 - "Community 304"
Cohesion: 0.22
Nodes (6): ADCSChecker, Principals with an enrollment ExtendedRight or broad write on the template., ESC1: enrollee supplies subject + client-auth EKU + low-priv can enrol +, ESC4: a low-privilege principal holds a dangerous write right on the template., ESC8: the CA exposes a web-enrollment (HTTP) endpoint that accepts NTLM, Read pKICertificateTemplate objects from the Configuration NC.

### Community 305 - "Community 305"
Cohesion: 0.17
Nodes (13): _clamp(), _job_runtime_seconds(), Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Return the effective whole-job deadline; callers can only reduce it., Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def, Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def (+5 more)

### Community 306 - "Community 306"
Cohesion: 0.22
Nodes (12): _as_dict(), build_service_index(), _finding_row(), _is_open(), A definitively open TCP port. `open|filtered` is NOT open — we never     raise a, One finding as the finding-section shows it — the ACTUAL vulnerability, with, Roll up findings for the finding section.      Beyond counts, this returns the A, Map (target, port) -> confirmed-service info from service_banner facts.      Onl (+4 more)

### Community 307 - "Community 307"
Cohesion: 0.19
Nodes (7): build_open_session_request(), IPMIScanner, parse_open_session_response(), ipmi_scanner.py — IPMI 2.0 cipher-zero authentication-bypass detection (VA check, A fixed RMCP+ Open Session Request offering cipher suite 0 (auth=0,     integrit, Parse an RMCP+ Open Session Response; None if it isn't one.     resp[0]=RMCP ver, Blocking: one RMCP+ Open Session Request, parse the response.         Monkeypatc

### Community 308 - "Community 308"
Cohesion: 0.19
Nodes (7): _extract_tcp_ports(), MSRPCScanner, msrpc_scanner.py — MSRPC endpoint-mapper (EPM) enumeration over port 135 (VA che, Parse ncacn_ip_tcp bindings → (all_tcp_ports, dynamic_tcp_ports).      Pure and, Reduce the raw endpoint list to distinct interfaces and dynamic ports., Blocking: EPM ept_lookup via impacket. Monkeypatchable for tests., _summarize()

### Community 309 - "Community 309"
Cohesion: 0.15
Nodes (11): build_default_funnel(), Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun, Funnel many hosts with bounded concurrency, writing every result. (+3 more)

### Community 310 - "Community 310"
Cohesion: 0.18
Nodes (7): AdaptiveRateController, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window)., A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window)., A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, Current integer window (>= min_window).

### Community 311 - "Community 311"
Cohesion: 0.36
Nodes (12): _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius(), _build_analyzer(), _critical_asset_ids(), _explain_hop(), get_attack_path() (+4 more)

### Community 312 - "Community 312"
Cohesion: 0.22
Nodes (12): delete_integration(), integration_secret(), IntegrationIn, IntegrationOut, list_integrations(), _out(), put_integration(), integrations.py — operator management of notification integrations (email/Slack/ (+4 more)

### Community 313 - "Community 313"
Cohesion: 0.15
Nodes (12): load_facts_jsonl(), _main(), Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., CLI: derive findings from one or more scanner JSONL files.          python -m ma, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., CLI: derive findings from one or more scanner JSONL files.          python -m ma (+4 more)

### Community 314 - "Community 314"
Cohesion: 0.22
Nodes (12): _as_dict(), build_service_index(), _finding_row(), _is_open(), A definitively open TCP port. `open|filtered` is NOT open — we never     raise a, One finding as the finding-section shows it — the ACTUAL vulnerability, with, Roll up findings for the finding section.      Beyond counts, this returns the A, Map (target, port) -> confirmed-service info from service_banner facts.      Onl (+4 more)

### Community 315 - "Community 315"
Cohesion: 0.19
Nodes (7): build_open_session_request(), IPMIScanner, parse_open_session_response(), ipmi_scanner.py — IPMI 2.0 cipher-zero authentication-bypass detection (VA check, A fixed RMCP+ Open Session Request offering cipher suite 0 (auth=0,     integrit, Parse an RMCP+ Open Session Response; None if it isn't one.     resp[0]=RMCP ver, Blocking: one RMCP+ Open Session Request, parse the response.         Monkeypatc

### Community 316 - "Community 316"
Cohesion: 0.21
Nodes (11): build_icmp_addrmask(), build_icmp_echo(), hop_estimate(), _icmp(), infer_initial_ttl(), os_family_from_ttl(), os_fingerprint.py — OS/stack fingerprinting via ICMP + TTL (Tier 2.1 + 2.2).  TW, Round the observed TTL up to the nearest standard initial TTL. (+3 more)

### Community 317 - "Community 317"
Cohesion: 0.15
Nodes (11): build_default_funnel(), Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Orchestrates discovery → port scan → routed deep scanners for each host.      Pa, Funnel many hosts with bounded concurrency, writing every result., Funnel many hosts with bounded concurrency, writing every result., Wire the funnel with the package's real scanners. Imported lazily so the     fun, Wire the funnel with the package's real scanners. Imported lazily so the     fun, Funnel many hosts with bounded concurrency, writing every result. (+3 more)

### Community 318 - "Community 318"
Cohesion: 0.15
Nodes (12): classify_os_error(), describe_os_error(), Full, debuggable classification for attaching to a ScanResult: state,     reason, Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc, Full, debuggable classification for attaching to a ScanResult: state,     reason, Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc, Current integer window (>= min_window)., Full, debuggable classification for attaching to a ScanResult: state,     reason (+4 more)

### Community 319 - "Community 319"
Cohesion: 0.15
Nodes (13): _apply_device_profile(), process_job_result(), _promote_assets(), Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu, Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu, Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu, Upsert discovered hosts/services into the asset inventory.      Keyed by (engage, Stamp the probe's evidence-based device role onto an Asset (create/update). (+5 more)

### Community 320 - "Community 320"
Cohesion: 0.21
Nodes (11): compute(), default_windows(), SLA policy engine.  Turns a severity + "first seen" timestamp into a remediation, Aggregate SLA states across a set of findings.      Returns counts per state plu, The env-configured SLA windows — the fallback when a tenant has no policy., Aggregate SLA states across a set of findings.      Returns counts per state plu, Compute the SLA state for one finding. Never raises on missing data., Compute the SLA state for one finding. Never raises on missing data.      `windo (+3 more)

### Community 321 - "Community 321"
Cohesion: 0.40
Nodes (12): _job(), Detection-trace coverage surfaced in the API: complete_with_gaps + explain.  Gua, _rows(), _run(), _scalars(), test_aggregating_reason_names_the_outbox_worker(), test_completed_no_blind_is_plain_complete(), test_completed_with_blind_rules_is_complete_with_gaps() (+4 more)

### Community 322 - "Community 322"
Cohesion: 0.15
Nodes (1): test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor

### Community 323 - "Community 323"
Cohesion: 0.17
Nodes (3): _fake_cert(), test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced capa, test_ja4x_from_cert_matches_pure_core()

### Community 324 - "Community 324"
Cohesion: 0.36
Nodes (2): _make_scan_record(), TestDeltaEngine

### Community 325 - "Community 325"
Cohesion: 0.26
Nodes (7): FakeProcess, _finding_line(), test_nonzero_exit_retains_and_marks_partial_findings(), test_nonzero_exit_without_findings_raises_with_stderr(), test_run_scan_streams_jsonl_and_separates_timeouts(), test_template_initialization_failure_cannot_be_clean_zero(), test_timeout_retains_findings_emitted_before_termination()

### Community 326 - "Community 326"
Cohesion: 0.22
Nodes (5): _f(), test_portal_metrics.py — pure dashboard aggregations., TestOpenClosed, TestSeverityBreakdown, TestStatusTimeline

### Community 327 - "Community 327"
Cohesion: 0.15
Nodes (1): TestScopeGuard

### Community 328 - "Community 328"
Cohesion: 0.17
Nodes (13): _gather_per_host(), _port_candidates(), Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Run per-host probes with bounded fan-out and failure isolation., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set., Return TCP ports worth scanning for this profile and requested branch set. (+5 more)

### Community 329 - "Community 329"
Cohesion: 0.15
Nodes (10): In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl, _run_inventory() (+2 more)

### Community 330 - "Community 330"
Cohesion: 0.17
Nodes (12): _load_or_create_identity(), Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu, Load the probe's X25519 identity from persistent state, or create one.      Retu (+4 more)

### Community 331 - "Community 331"
Cohesion: 0.17
Nodes (12): Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket. (+4 more)

### Community 332 - "Community 332"
Cohesion: 0.18
Nodes (3): decode_key(), Verify a Manager-signed policy and return its public key for TOFU pinning., verify_site_policy()

### Community 333 - "Community 333"
Cohesion: 0.18
Nodes (12): _facts_from_cache(), Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty, Execute a scan and return the enriched result bundle.      Args:         scan_ty (+4 more)

### Community 334 - "Community 334"
Cohesion: 0.21
Nodes (10): build_parser(), cmd_correlate(), cmd_status(), main(), _merge_findings(), cli.py — the two operator verbs for the offline CVE layer.      python -m cve.cl, Verify the offline mirror: feed counts, freshness, and — critically — whether, Yield fact dicts from a JSONL file ('-' = stdin). Blank/comment/bad lines     ar (+2 more)

### Community 335 - "Community 335"
Cohesion: 0.23
Nodes (11): apply_to_findings(), assess(), kev_links_for(), KevLink, priority_for(), exploitability.py — join real-world exploitation evidence (CISA KEV + FIRST EPSS, Exploitability evidence for one posture rule.      Returns {kev_refs, epss_max,, Enrich posture findings in place with exploitation evidence and re-rank.      Th (+3 more)

### Community 336 - "Community 336"
Cohesion: 0.26
Nodes (7): HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber(), isOptionalString(), normalizePort(), parseHttpxJsonLine()

### Community 337 - "Community 337"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 338 - "Community 338"
Cohesion: 0.27
Nodes (11): _advertised_dynamic_ports(), _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl. (+3 more)

### Community 339 - "Community 339"
Cohesion: 0.17
Nodes (8): main_entrypoint(), Run a scanner CLI's body with consistent, operator-friendly error handling., One observation about one target. Pure fact, no interpretation.      Network-sta, One observation about one target. Pure fact, no interpretation.      Network-sta, One observation about one target. Pure fact, no interpretation.      Network-sta, Run a scanner CLI's body with consistent, operator-friendly error handling., Run a scanner CLI's body with consistent, operator-friendly error handling., ScanResult

### Community 340 - "Community 340"
Cohesion: 0.18
Nodes (11): _local_source_ip(), A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)., A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)., A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, Block until `sock` has a packet waiting, or `timeout` seconds elapse.     Return (+3 more)

### Community 341 - "Community 341"
Cohesion: 0.17
Nodes (5): _ike_probe(), udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, TFTP RRQ for a non-existent file.  Error reply confirms TFTP service., Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-, _tftp_probe()

### Community 342 - "Community 342"
Cohesion: 0.17
Nodes (12): import_facts(), _parse_probe_file(), _promote_from_facts(), Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s, Parse a probe export into (facts, scan_type).      Accepts two shapes the probe, Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s, Parse a probe export into (facts, scan_type).      Accepts two shapes the probe, Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen (+4 more)

### Community 343 - "Community 343"
Cohesion: 0.29
Nodes (11): get_sla_policy(), _out(), put_sla_policy(), sla_policy.py — operator management of the tenant's custom SLA remediation windo, The tenant's custom SLA windows if set, else the env defaults. Shared by any, resolve_windows(), _row(), SlaPolicyIn (+3 more)

### Community 344 - "Community 344"
Cohesion: 0.23
Nodes (11): _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious(), oid_to_hex(), Return a threat-intel label if this JA4X is a known-suspicious fingerprint,, DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040 (+3 more)

### Community 345 - "Community 345"
Cohesion: 0.17
Nodes (11): classify_os_error(), _harvest_tcp_stack(), Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier, One connect() and its classification. Always returns a ScanResult         (open, One connect() and its classification. Always returns a ScanResult         (open, One connect() and its classification. Always returns a ScanResult         (open, One connect() and its classification. Always returns a ScanResult         (open (+3 more)

### Community 346 - "Community 346"
Cohesion: 0.27
Nodes (11): _advertised_dynamic_ports(), _log(), main(), _open_tcp_ports(), _ports_arg(), Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl., Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl. (+3 more)

### Community 347 - "Community 347"
Cohesion: 0.17
Nodes (11): bracket_host(), Read-only view of allowed networks (for CIDR-level engines)., Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h, Read-only view of allowed networks (for CIDR-level engines)., Read-only view of allowed networks (for CIDR-level engines)., Read-only view of allowed networks (for CIDR-level engines)., Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h, Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h (+3 more)

### Community 348 - "Community 348"
Cohesion: 0.18
Nodes (11): _local_source_ip(), A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)., A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)., A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr, Block until `sock` has a packet waiting, or `timeout` seconds elapse.     Return (+3 more)

### Community 349 - "Community 349"
Cohesion: 0.17
Nodes (5): _ike_probe(), udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO, TFTP RRQ for a non-existent file.  Error reply confirms TFTP service., Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-, _tftp_probe()

### Community 350 - "Community 350"
Cohesion: 0.23
Nodes (11): classify_action(), Decision, _deny(), evaluate_action(), agent_policy.py — the deterministic policy engine for the Autonomous Engagement, Map an action name to its risk tier; unknown actions fail closed., The deterministic authorization envelope for one engagement's agent., Running engagement usage, checked against the blast-radius caps. (+3 more)

### Community 351 - "Community 351"
Cohesion: 0.20
Nodes (11): project_file_stamp(), project_now(), project_timestamp(), project_time — one place that decides what "now" looks like to a human.  The man, The project timezone, degrading safely when tzdata is unavailable., Current time as an AWARE datetime in the project timezone., ISO-8601 instant in the project timezone: 2026-09-03T23:15:05+05:30., Re-render an existing datetime in the project timezone.      The instant is pres (+3 more)

### Community 352 - "Community 352"
Cohesion: 0.23
Nodes (11): _encode(), is_reference(), make_reference(), normalize(), reference.py — human-readable references for things a customer has to talk about, Canonicalise a reference a human typed: trim, upper-case, and apply     Crockfor, True when `text` looks like one of our references rather than a UUID, so a     l, The stable code for one row. Deterministic, so a backfill and a fresh     insert (+3 more)

### Community 353 - "Community 353"
Cohesion: 0.23
Nodes (11): classify_finding(), _cves(), os_key(), remediation_kb.py — the deterministic remediation knowledge base.  Pure (no DB,, Normalize an arbitrary OS/target string to a supported KB key.      Public becau, Return a structured, OS-filtered remediation plan for `finding`.      Always ret, Map a finding to a KB category key using title/description/CVE hints.      Deter, One remediation step. `generic` is REQUIRED (the vendor-neutral fallback);     p (+3 more)

### Community 354 - "Community 354"
Cohesion: 0.17
Nodes (1): TestPathAnalyzer

### Community 355 - "Community 355"
Cohesion: 0.17
Nodes (1): test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper

### Community 356 - "Community 356"
Cohesion: 0.24
Nodes (6): _mock_response(), test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()

### Community 357 - "Community 357"
Cohesion: 0.26
Nodes (3): _asset(), TestAssetMerge, TestGate

### Community 358 - "Community 358"
Cohesion: 0.23
Nodes (5): _db_names(), test_probe_simple_approve.py — one-click probe approval helpers (item 5)., db.execute(...).scalars().all() → the given agent-name list., TestNextProbeName, TestSimpleApproveInput

### Community 359 - "Community 359"
Cohesion: 0.17
Nodes (2): Tests that use the real engine but with no-op callbacks., TestRunnerHeadless

### Community 360 - "Community 360"
Cohesion: 0.27
Nodes (9): _exec(), _finding(), Unit tests for P3 Task 7: validation-result ingestion → finding verdict.  Pure t, test_confirmed_never_overrides_human_closed_finding(), test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_without_touching_status(), test_inconclusive_leaves_finding_unchanged(), test_ingest_confirmed_updates_request_and_finding() (+1 more)

### Community 361 - "Community 361"
Cohesion: 0.18
Nodes (11): _applied_tuning(), syn' for wide sweeps (deep intensity / full-port audit), else 'connect'., syn' for wide sweeps (deep intensity / full-port audit), else 'connect'., syn' for wide sweeps (deep intensity / full-port audit), else 'connect'., Serialize effective limits without ever echoing credential values., Serialize effective limits without ever echoing credential values., Serialize effective limits without ever echoing credential values., Serialize effective limits without ever echoing credential values. (+3 more)

### Community 362 - "Community 362"
Cohesion: 0.18
Nodes (10): Return the WebSocket connection URL with auth token.          The token is passe, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica, Return the WebSocket endpoint without embedding credentials.          Authentica (+2 more)

### Community 363 - "Community 363"
Cohesion: 0.18
Nodes (10): _main(), Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, CLI: derive findings from one or more scanner JSONL files.          python -m ma, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, CLI: derive findings from one or more scanner JSONL files.          python -m ma, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc, CLI: derive findings from one or more scanner JSONL files.          python -m ma (+2 more)

### Community 364 - "Community 364"
Cohesion: 0.18
Nodes (11): build_ip_header(), build_syn_packet(), build_tcp_syn(), Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)., Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)., Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)., Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma, Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma (+3 more)

### Community 365 - "Community 365"
Cohesion: 0.20
Nodes (11): _parse_mss(), parse_packet(), parse_tcp_options(), Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket)., Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked, Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked, Walk a TCP options field into a p0f-style profile.      Returns {mss, wscale, sa, Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also (+3 more)

### Community 366 - "Community 366"
Cohesion: 0.18
Nodes (7): One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, _UDPProbeProtocol

### Community 367 - "Community 367"
Cohesion: 0.18
Nodes (11): build_ip_header(), build_syn_packet(), build_tcp_syn(), Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)., Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)., Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)., Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma, Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma (+3 more)

### Community 368 - "Community 368"
Cohesion: 0.20
Nodes (11): _parse_mss(), parse_packet(), parse_tcp_options(), Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket)., Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked, Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked, Walk a TCP options field into a p0f-style profile.      Returns {mss, wscale, sa, Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also (+3 more)

### Community 369 - "Community 369"
Cohesion: 0.20
Nodes (7): deliver(), enqueue_notification(), notify_tenant(), notifications.py — deliver a message to a tenant's configured integrations (emai, Producer API: enqueue a durable notify event (commits with the caller's txn)., Send via one integration. True on success; False on any handled failure     (log, Deliver to every ENABLED integration for the tenant. Returns the count sent.

### Community 370 - "Community 370"
Cohesion: 0.24
Nodes (10): _is_closed(), MetricFinding, open_closed_counts(), _period(), portal_metrics.py — pure aggregations for the customer dashboard.  Kept pure (no, Count findings by severity (all five buckets always present, zero-filled).     o, (open, closed) totals over the given findings., Per-month {period, opened, closed} for the last `months` months.      opened = f (+2 more)

### Community 371 - "Community 371"
Cohesion: 0.18
Nodes (1): TestADCSChecker

### Community 372 - "Community 372"
Cohesion: 0.18
Nodes (1): TestVersionInRanges

### Community 373 - "Community 373"
Cohesion: 0.22
Nodes (4): _ext(), test_main_scripts_ja4s.py — JA4S TLS ServerHello fingerprint (advanced capabilit, _serverhello(), test_ja4s_from_serverhello_tls13()

### Community 374 - "Community 374"
Cohesion: 0.38
Nodes (6): _client(), _db_scalar(), _finding(), test_portal_remediation.py — Section 6: the customer-facing remediation route., Each db.execute(...) → result whose .scalar_one_or_none() is the next val., TestPortalRemediation

### Community 375 - "Community 375"
Cohesion: 0.18
Nodes (1): TestExpandTargets

### Community 376 - "Community 376"
Cohesion: 0.20
Nodes (2): test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses(), _token()

### Community 377 - "Community 377"
Cohesion: 0.31
Nodes (8): _rank(), test_bounds(), test_confirmed_exploitable_outranks_contradicted(), test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lowers(), test_kev_raises_rank(), test_low_confidence_lowers_rank(), test_severity_remains_an_impact_signal_without_cvss()

### Community 378 - "Community 378"
Cohesion: 0.24
Nodes (4): _FakeSock, Minimal socket stand-in: replays the daemon greeting, records what the     scann, Protocol >= 32 daemons append their digest-name list to the greeting and     rej, TestHandshake

### Community 379 - "Community 379"
Cohesion: 0.18
Nodes (1): TestSendPacer

### Community 380 - "Community 380"
Cohesion: 0.18
Nodes (2): Re-pointing to a different manager must forget the OLD manager's         pinned, TestIdentity

### Community 381 - "Community 381"
Cohesion: 0.27
Nodes (5): _ids(), test_validation_gate.py — the "validation gate" (build spec Card 7) as detection, TestNoFabricatedIcmpLiveness, TestRdpNlaGate, TestUdpNoReplyRejected

### Community 382 - "Community 382"
Cohesion: 0.18
Nodes (1): TestNmapXMLParser

### Community 383 - "Community 383"
Cohesion: 0.18
Nodes (7): ConnectionManager, Manages WebSocket connections with room-based broadcasting., Manages WebSocket connections with room-based broadcasting., Accept connection and add to room., Accept connection and add to room., Get number of connected clients in a room., Get number of connected clients in a room.

### Community 384 - "Community 384"
Cohesion: 0.18
Nodes (11): _default_host_concurrency(), _finalize_trace(), Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass, Hosts scanned in parallel during the deep-branch stage.      Env override: PROBE (+3 more)

### Community 385 - "Community 385"
Cohesion: 0.29
Nodes (8): _product_from_cpe(), Apply authoritative-version suppression and preserve every decision.      The ac, The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp, Why a candidate finding was omitted from the active result set., Suppress a suspected/potential (inferred-source) finding when the     SAME host, suppress_negated(), suppress_negated_with_audit(), SuppressionRecord

### Community 386 - "Community 386"
Cohesion: 0.29
Nodes (8): _banner_confirms_backdoor(), classify_port(), contradicts_port_hypothesis(), _normalized(), PortRisk, port_intel.py — port-intelligence catalog for the exposed-service detector.  The, True when an identified product proves the catalog's port guess wrong., Map an open TCP port (+ optional banner, the probe's soft-matched service     la

### Community 387 - "Community 387"
Cohesion: 0.31
Nodes (9): _collect(), fuse_exposure_results(), fused_service_exposure(), _is_external(), vantage_fusion.py — fuse the exposure_matrix results of MULTIPLE probes.  A sing, (ip, proto, port) → fused exposure verdict, ready to stamp onto Service rows., (ip → {(proto,port): {vantage: status}}, ip → set(vantages))., Fuse several probes' exposure_matrix results into one per-target matrix.      `r (+1 more)

### Community 388 - "Community 388"
Cohesion: 0.31
Nodes (9): compute_verdict(), _int_confidence(), _qualifies_for_llm(), verification.py — normalized, dashboard-facing verification verdict.  The determ, Deterministic passive verdict from a detection finding's evidence dict., Only spend an LLM call where a rationale / FP-triage is worth it:     uncertain, Deterministic verdict, optionally enriched by an LLM rationale. The LLM     (duc, VerificationVerdict (+1 more)

### Community 389 - "Community 389"
Cohesion: 0.29
Nodes (9): _cleartext_rule(), create_service_vuln_findings(), _http_rules(), _new_finding(), service_vuln.py — turn network-service banner facts into Finding rows.  WHY THIS, Scan the result's `facts` for weak/outdated network services and persist     Fin, SSH hygiene findings the CVE engine does NOT cover.      Outdated-version → CVE, Findings for an HTTP service, from its Server header / banner. (+1 more)

### Community 390 - "Community 390"
Cohesion: 0.27
Nodes (7): COMMON_RANGES, estimateHostCount(), isValidTarget(), ParseResult, parseTargets(), RFC1918, validOctets()

### Community 391 - "Community 391"
Cohesion: 0.24
Nodes (4): _first(), LDAPScanner, ldap_scanner.py — LDAP anonymous-bind enumeration (VA checklist: anonymous direc, Blocking: anonymous bind + RootDSE read + bounded tree-read probe.         Retur

### Community 392 - "Community 392"
Cohesion: 0.20
Nodes (7): Bounded worker-pool scan of every requested port.          A fixed pool of `conc, Bounded worker-pool scan of every requested port.          A fixed pool of `conc, Bounded worker-pool scan of every requested port.          A fixed pool of `conc, True for the one state a retry can legitimately change: silence., Bounded worker-pool scan of every requested port.          A fixed pool of `conc, True for the one state a retry can legitimately change: silence., Bounded worker-pool scan of every requested port.          A fixed pool of `conc

### Community 393 - "Community 393"
Cohesion: 0.20
Nodes (10): _agent_token_from_websocket(), agent_websocket_endpoint(), _claim_pushed_job(), Persistent WebSocket for probe → manager push communication.      Authentication, Persistent WebSocket for probe → manager push communication.      Authentication, Read an agent bearer token exclusively from the non-logged auth header., Read an agent bearer token exclusively from the non-logged auth header., Persistent WebSocket for probe → manager push communication.      Query params: (+2 more)

### Community 394 - "Community 394"
Cohesion: 0.22
Nodes (6): _extract_tcp_ports(), MSRPCScanner, Parse ncacn_ip_tcp bindings → (all_tcp_ports, dynamic_tcp_ports).      Pure and, Reduce the raw endpoint list to distinct interfaces and dynamic ports., Blocking: EPM ept_lookup via impacket. Monkeypatchable for tests., _summarize()

### Community 395 - "Community 395"
Cohesion: 0.27
Nodes (7): fingerprint_os(), Interpret a timestamp reply's transmit value. Per RFC 792 a *standard* value, Combine available stack signals into a best-guess OS family with a calibrated, Combine available stack signals into a best-guess OS family with a calibrated, Combine available stack signals into a best-guess OS family with a calibrated, FIX 3b: aliveness/TTL came from a TCP SYN-ACK, not ICMP. Label the TTL         s, remote_clock()

### Community 396 - "Community 396"
Cohesion: 0.20
Nodes (7): Bounded worker-pool scan of every requested port.          A fixed pool of `conc, Bounded worker-pool scan of every requested port.          A fixed pool of `conc, Bounded worker-pool scan of every requested port.          A fixed pool of `conc, True for the one state a retry can legitimately change: silence., Bounded worker-pool scan of every requested port.          A fixed pool of `conc, True for the one state a retry can legitimately change: silence., Bounded worker-pool scan of every requested port.          A fixed pool of `conc

### Community 397 - "Community 397"
Cohesion: 0.29
Nodes (5): PortScanner, Emit a non-open result only when report_closed is on., One port's terminal result, gated by the rate limiter and (when         enabled), One port's terminal result, gated by the rate limiter and (when         enabled), Record one probe and answer: is the PATH still delivering?          WHY THIS EXI

### Community 398 - "Community 398"
Cohesion: 0.20
Nodes (6): RateLimiter, Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second.

### Community 399 - "Community 399"
Cohesion: 0.24
Nodes (5): AdaptiveRateController, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),, A self-tuning concurrency window, modelled on TCP congestion control (AIMD),

### Community 400 - "Community 400"
Cohesion: 0.20
Nodes (1): TestGraphBuilder

### Community 401 - "Community 401"
Cohesion: 0.20
Nodes (1): TestVersion

### Community 402 - "Community 402"
Cohesion: 0.20
Nodes (2): ipv6_discovery reports on the RUN, not a host: its target is the local         i, TestIngestFile

### Community 403 - "Community 403"
Cohesion: 0.20
Nodes (9): test_engine_bridge_ingest_health.py — a zero-finding run must never be able to L, Baseline: the shape the agent actually sends survives ingest and fires rules., The regression. Drop the one field an agent rename could plausibly drop and, A partly-bad batch must keep its good findings AND still admit what it lost., The census is best-effort by contract: an older engine returning no     IngestRe, test_census_survives_an_engine_that_returns_no_ingest_result(), test_healthy_facts_ingest_completely_and_detect(), test_partial_drift_still_detects_but_reports_the_loss() (+1 more)

### Community 405 - "Community 405"
Cohesion: 0.36
Nodes (5): _db(), _operator(), test_integrations.py — operator notification-integration config (item 3)., TestListIntegrations, TestPutIntegration

### Community 406 - "Community 406"
Cohesion: 0.44
Nodes (9): _metrics(), test_main_scripts_completeness.py — Epic 4: set-based scan-completeness invarian, _rec(), test_duplicate_port_is_detected(), test_fallback_count_based_when_no_requested_set(), test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely_complete() (+1 more)

### Community 407 - "Community 407"
Cohesion: 0.20
Nodes (1): TestClassifyDevice

### Community 408 - "Community 408"
Cohesion: 0.29
Nodes (6): _oserr(), test_main_scripts_errno.py — Phase 2: shared TCP/UDP errno classification.  Veri, test_definitive_states(), test_describe_os_error_is_fully_debuggable(), test_scanner_side_errors_are_error_not_filtered(), test_unknown_errno_is_self_identifying_and_never_filtered()

### Community 409 - "Community 409"
Cohesion: 0.20
Nodes (1): TestIoTScanner

### Community 410 - "Community 410"
Cohesion: 0.20
Nodes (1): TestStackSignature

### Community 411 - "Community 411"
Cohesion: 0.20
Nodes (1): TestParsePorts

### Community 412 - "Community 412"
Cohesion: 0.20
Nodes (1): TestUseCasesResolve

### Community 413 - "Community 413"
Cohesion: 0.27
Nodes (3): _fake_gai(), The false negative #9 exists to kill: a dual-stack host whose IPv6         path, TestResolveCandidates

### Community 414 - "Community 414"
Cohesion: 0.20
Nodes (2): Each encryption uses a fresh ephemeral key, so blobs are different., TestEncryptDecryptRoundtrip

### Community 415 - "Community 415"
Cohesion: 0.20
Nodes (3): test_ssh_scanner.py — SSH configuration audit (Tier 2.x, §6 of the VA checklist), TestParseBanner, TestVendoredDB

### Community 416 - "Community 416"
Cohesion: 0.29
Nodes (5): test_tls_integration.py — Tier 2.4 live check: run the real TLSScanner against a, _self_signed(), test_tls_fingerprint_is_nonzero_and_stable(), test_tls_scanner_reports_posture_grade(), _TLSServer

### Community 417 - "Community 417"
Cohesion: 0.20
Nodes (1): TestSubmitResult

### Community 418 - "Community 418"
Cohesion: 0.44
Nodes (9): _exec(), _mock_db(), Mocked-session unit tests for the P3 active-validation endpoints (Task 4).  No D, test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job(), test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_derives_tls_check(), test_reject_marks_rejected() (+1 more)

### Community 419 - "Community 419"
Cohesion: 0.20
Nodes (10): _claim_batch(), _handle_notify(), Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means, Fan a notification out to the tenant's enabled email/Slack/Jira integrations., Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means, Fan a notification out to the tenant's enabled email/Slack/Jira integrations., Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means, Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means (+2 more)

### Community 420 - "Community 420"
Cohesion: 0.22
Nodes (10): Requeue events a dead worker left in PROCESSING past the lease.      `attempts`, Stranded events with retry budget left → make due now so a live worker     re-cl, Stranded events with retry budget left → make due now so a live worker     re-cl, Stranded events with retry budget left → make due now so a live worker     re-cl, Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat, Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat, Stranded events with retry budget left → make due now so a live worker     re-cl, Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat (+2 more)

### Community 421 - "Community 421"
Cohesion: 0.27
Nodes (9): Event, main(), _mark_done(), _process(), outbox.py (worker) — durable consumer for the transactional outbox.  Run as its, DetectionRuns stuck RUNNING → mark FAILED. Prefer the per-run LEASE     (`lease_, Fail DetectionRuns a crashed worker left RUNNING. Without this a campaign whose, _reap_runs_stmt() (+1 more)

### Community 422 - "Community 422"
Cohesion: 0.22
Nodes (8): Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of, Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of

### Community 423 - "Community 423"
Cohesion: 0.31
Nodes (7): create_access_token(), create_device_access_token(), create_refresh_token(), _now(), Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation., Returns (token, jti) — jti is stored in Redis for revocation.

### Community 424 - "Community 424"
Cohesion: 0.22
Nodes (8): evaluate_rule(), _fact_indicates_no_service(), get_path(), One rule evaluation's outcome. Purely diagnostic — never gates a finding., Resolve `a.b.c` inside a Fact.data dict. Returns `_MISSING` (never None)     whe, True when the scanner ran but the service did NOT answer — so a rule's     decla, Evaluate ONE rule against ONE fact and record the outcome. NEVER raises —     a, TraceRow

### Community 425 - "Community 425"
Cohesion: 0.22
Nodes (5): Blocking packets-per-second pacer with AIMD rate adaptation, for raw-socket, Block just long enough to hold `rate` packets/sec. No-op at rate <= 0., Fold one send/collect round's reply ratio into the rate (AIMD).          Returns, Pacing telemetry for the scan summary (so a throttled scan is visible)., SendPacer

### Community 426 - "Community 426"
Cohesion: 0.28
Nodes (4): get_results(), _result_out(), _run_correlation(), _set_job()

### Community 427 - "Community 427"
Cohesion: 0.28
Nodes (5): AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) into the estimate. Ignores         missing/, Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp, Convenience: build an estimator and fold in a sequence of RTT samples.

### Community 428 - "Community 428"
Cohesion: 0.25
Nodes (6): OSFingerprintScanner, ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP, ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP, ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP, Best-effort exact Windows build via SMB2 NTLM (shared impl). {} on any         f, Fuse an SMB2 NTLM build into an OS result: authoritative release + build,

### Community 429 - "Community 429"
Cohesion: 0.22
Nodes (8): Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., Writes ScanResult objects as JSONL to a file and/or stdout., ResultWriter

### Community 430 - "Community 430"
Cohesion: 0.22
Nodes (5): Blocking packets-per-second pacer with AIMD rate adaptation, for raw-socket, Block just long enough to hold `rate` packets/sec. No-op at rate <= 0., Fold one send/collect round's reply ratio into the rate (AIMD).          Returns, Pacing telemetry for the scan summary (so a throttled scan is visible)., SendPacer

### Community 431 - "Community 431"
Cohesion: 0.22
Nodes (1): TestClassify

### Community 432 - "Community 432"
Cohesion: 0.39
Nodes (8): _base(), FindingOut computes the explainable risk_rank at serialization (P4 Task 5 wiring, test_confirmed_exploited_outranks_contradicted(), test_detail_asset_context_round_trips_without_changing_list_contract(), test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_nested_enrichment_kev_is_part_of_the_rank(), test_risk_rank_is_computed_not_none()

### Community 433 - "Community 433"
Cohesion: 0.22
Nodes (2): The neighbour cache is system-wide. Pinging en0 and then harvesting every     in, TestInterfaceScoping

### Community 434 - "Community 434"
Cohesion: 0.31
Nodes (4): _Listener, A real TCP listener that optionally speaks first., One real network_va against loopback with risk-catalog services listening., va_scan()

### Community 435 - "Community 435"
Cohesion: 0.22
Nodes (3): test_notifications.py — integration delivery fan-out (item 3 delivery worker)., TestDeliver, TestNotifyTenant

### Community 436 - "Community 436"
Cohesion: 0.22
Nodes (1): TestTtlInference

### Community 437 - "Community 437"
Cohesion: 0.31
Nodes (4): _infos(), test_resolve.py — resolve() address-family selection (task A9)., Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr)., TestResolveFamily

### Community 438 - "Community 438"
Cohesion: 0.28
Nodes (8): _py_files(), test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1, Every scanner module authored in main_scripts must exist in scanner/., scanner/ must not carry modules that main_scripts/ does not — otherwise the, Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py., test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_files(), test_scanner_module_matches_main_scripts()

### Community 439 - "Community 439"
Cohesion: 0.22
Nodes (1): TestTargetsInExcludes

### Community 440 - "Community 440"
Cohesion: 0.28
Nodes (5): The banner and the match must come from the SAME rung (an earlier, longer     bu, _scanner(), test_matched_rung_banner_is_the_one_reported(), test_prefers_decrypted_tls_reply_over_plaintext_noise(), TestLadder

### Community 441 - "Community 441"
Cohesion: 0.22
Nodes (2): The freshness check reads the STATE FILE but requests authenticate with, TestDeviceEnrollment

### Community 442 - "Community 442"
Cohesion: 0.31
Nodes (8): _build_creds(), _build_mode(), build_parser(), _main(), _parse_duration(), cli.py — entrypoint for the conditional workflow engine. Flag conventions follow, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar, 7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar

### Community 443 - "Community 443"
Cohesion: 0.25
Nodes (8): _count_open_port_facts(), Count concrete open services, not generic host-liveness observations., Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact., Count unique open network endpoints, not every confirming scanner fact.

### Community 444 - "Community 444"
Cohesion: 0.25
Nodes (8): LeaseLostError, Raised when Manager fencing revokes the running attempt., Raised when Manager fencing revokes the running attempt., Raised when Manager fencing revokes the running attempt., Raised when Manager fencing revokes the running attempt., Raised when Manager fencing revokes the running attempt., Raised when Manager fencing revokes the running attempt., _run_with_cancellation()

### Community 445 - "Community 445"
Cohesion: 0.25
Nodes (8): syn' for wide sweeps (deep intensity / full-port audit), else 'connect'., Return the effective whole-job deadline; callers can only reduce it., Translate operator-supplied job params into run_engagement() kwargs.      This i, Translate operator-supplied job params into run_engagement() kwargs.      This i, Translate operator-supplied job params into run_engagement() kwargs.      This i, Translate operator-supplied job params into run_engagement() kwargs.      This i, Translate operator-supplied job params into run_engagement() kwargs.      This i, _tuning_from_params()

### Community 446 - "Community 446"
Cohesion: 0.32
Nodes (7): compare(), in_range(), parse_version(), version.py — loose version comparison for CVE range matching.  Real service bann, Normalize a version string into a comparable tuple of ints., Return -1/0/1 for version a vs b (zero-padded tuple comparison)., Is `version` inside the NVD-style bound set? An `exact` match (no range     boun

### Community 447 - "Community 447"
Cohesion: 0.32
Nodes (7): assess_confidence(), calibrate_host_findings(), corroborating_chains(), posture_confidence.py — calibrated, auditable confidence for posture findings., Second pass over ONE host's posture findings: now that every rule that fired on, Chains this rule belongs to where ≥1 OTHER member also fired on the host.     A, Return (confidence 0-100, precision_factors). Pure and deterministic:     same i

### Community 448 - "Community 448"
Cohesion: 0.36
Nodes (3): RateLimiter, True if current time is inside the allowed scan window., Blocks until a token is available for the given target IP.         Raises Runtim

### Community 449 - "Community 449"
Cohesion: 0.36
Nodes (7): extractScripts(), NmapHost, NmapScriptResult, NmapService, parseNmapXml(), parser, toArray()

### Community 450 - "Community 450"
Cohesion: 0.25
Nodes (7): _harvest_tcp_stack(), One connect() and its classification. Always returns a ScanResult         (open, One connect() and its classification. Always returns a ScanResult         (open, One connect() and its classification. Always returns a ScanResult         (open, One connect() and its classification. Always returns a ScanResult         (open, One connect() and its classification. Always returns a ScanResult         (open, Peer TCP-stack signals readable from a COMPLETED connect(), for OS/link     fing

### Community 451 - "Community 451"
Cohesion: 0.29
Nodes (4): PortScanner, One port's terminal result, gated by the rate limiter and (when         enabled), One port's terminal result, gated by the rate limiter and (when         enabled), Record one probe and answer: is the PATH still delivering?          WHY THIS EXI

### Community 452 - "Community 452"
Cohesion: 0.25
Nodes (5): Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, ScanMetrics

### Community 453 - "Community 453"
Cohesion: 0.25
Nodes (8): classify_os_error(), describe_os_error(), Full, debuggable classification for attaching to a ScanResult: state,     reason, Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc, Full, debuggable classification for attaching to a ScanResult: state,     reason, Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc, Full, debuggable classification for attaching to a ScanResult: state,     reason, Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc

### Community 454 - "Community 454"
Cohesion: 0.25
Nodes (4): One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi, _UDPProbeProtocol

### Community 455 - "Community 455"
Cohesion: 0.25
Nodes (6): is_verified(), scanner_registry.py — the single source of truth for WHICH scanners are trusted., The scanner-module trust view: which scanners are verified vs experimental,, True only for a scanner explicitly on the verified (trusted) list. Unknown     s, ScannerInfo, verification_report()

### Community 456 - "Community 456"
Cohesion: 0.29
Nodes (2): ssh_collector.py — credentialed (authenticated) inventory collection for Linux., SSHCollector

### Community 457 - "Community 457"
Cohesion: 0.32
Nodes (5): SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SynScanner

### Community 458 - "Community 458"
Cohesion: 0.32
Nodes (7): attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon(), nativePtrSweep(), PtrSweepResult, safe()

### Community 459 - "Community 459"
Cohesion: 0.36
Nodes (5): get_user(), list_users(), _out(), Tenant user management — list and deactivate operator accounts.  Exposed endpoin, UserOut

### Community 460 - "Community 460"
Cohesion: 0.29
Nodes (7): classify_device(), classify_from_results(), device_classifier.py — infer a device's ROLE from collection-layer facts.  This, Fuse OS family + open ports + service products into a device-role guess.      Re, Fuse OS family + open ports + service products into a device-role guess.      Re, Convenience adapter: extract classifier inputs from a list of ScanResult     obj, Convenience adapter: extract classifier inputs from a list of ScanResult     obj

### Community 461 - "Community 461"
Cohesion: 0.29
Nodes (8): MasscanRun, _parse_masscan_json(), _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, Run masscan over the given target specs and return its parsed JSON records., Run masscan over the given target specs and return its parsed JSON records., Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin, _run_masscan()

### Community 462 - "Community 462"
Cohesion: 0.25
Nodes (5): Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, Per-target scan accounting — the completeness + self-health record.      It lets, ScanMetrics

### Community 463 - "Community 463"
Cohesion: 0.25
Nodes (8): main_entrypoint(), Run a scanner CLI's body with consistent, operator-friendly error handling., Run a scanner CLI's body with consistent, operator-friendly error handling., Subclasses implement `scan_target(self, target)` (async), returning a list     o, Run a scanner CLI's body with consistent, operator-friendly error handling., Run a scanner CLI's body with consistent, operator-friendly error handling., Run a scanner CLI's body with consistent, operator-friendly error handling., Run a scanner CLI's body with consistent, operator-friendly error handling.

### Community 464 - "Community 464"
Cohesion: 0.25
Nodes (8): parse_ports(), Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)., Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535).

### Community 465 - "Community 465"
Cohesion: 0.25
Nodes (6): is_verified(), scanner_registry.py — the single source of truth for WHICH scanners are trusted., The scanner-module trust view: which scanners are verified vs experimental,, True only for a scanner explicitly on the verified (trusted) list. Unknown     s, ScannerInfo, verification_report()

### Community 466 - "Community 466"
Cohesion: 0.32
Nodes (5): SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SYN scan on privileged Linux; transparent connect-scan fallback elsewhere., SynScanner

### Community 467 - "Community 467"
Cohesion: 0.25
Nodes (4): Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, UDPScanner

### Community 468 - "Community 468"
Cohesion: 0.43
Nodes (1): WindowsCollector

### Community 469 - "Community 469"
Cohesion: 0.32
Nodes (7): apply_validation_outcome(), ingest_validation_result(), looks_like_validation_result(), validation_ingest.py — turn a probe's safe active-validation result into a findi, Apply a validation verdict to a finding object (pure — no DB/session)., Cheap gate so normal scan submissions never trigger a lookup: a probe     valida, If ``job_id`` belongs to a ValidationRequest, store the result, set its     outc

### Community 470 - "Community 470"
Cohesion: 0.46
Nodes (7): _ev(), test_confirmed_authoritative_does_not_escalate(), test_high_severity_suspected_escalates_when_roe_allows(), test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_escalate(), test_ot_profile_never_escalates(), test_roe_forbids_blocks_escalation()

### Community 471 - "Community 471"
Cohesion: 0.29
Nodes (1): TestKerberoastChecker

### Community 472 - "Community 472"
Cohesion: 0.32
Nodes (3): _boundary_test_client(), test_agent_jwt_is_blocked_before_human_route_handler(), test_human_jwt_still_reaches_human_route_handler()

### Community 473 - "Community 473"
Cohesion: 0.54
Nodes (7): _db(), _operator(), test_customer_reveal.py — operator reveal of a customer login password (item 1)., test_reveal_missing_user_is_404(), test_reveal_null_ciphertext_returns_none(), test_reveal_returns_decrypted_password(), _user()

### Community 474 - "Community 474"
Cohesion: 0.25
Nodes (1): test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure

### Community 475 - "Community 475"
Cohesion: 0.25
Nodes (5): End-to-end: identity → register → job → decrypt → validate → scan → submit., Simulate the full probe lifecycle from identity to result submission., All targets outside scope → job is rejected cleanly., OT passive profile resolves correctly., TestFullJobLifecycle

### Community 476 - "Community 476"
Cohesion: 0.25
Nodes (5): Phase 4: identity generation + scope encryption roundtrip., Generate identity → encrypt scope → decrypt scope., Manager encrypts → probe decrypts., A different probe cannot decrypt scope meant for another probe., TestIdentityAndEncryption

### Community 477 - "Community 477"
Cohesion: 0.36
Nodes (5): test_main_scripts_datastore_probe.py — safe read-only datastore probes make the, _svc(), test_elasticsearch_and_couchdb_win_over_generic_http(), test_memcached_version_and_stat_identify_as_memcached(), test_redis_info_and_noauth_identify_as_redis()

### Community 478 - "Community 478"
Cohesion: 0.25
Nodes (1): TestProvenance

### Community 479 - "Community 479"
Cohesion: 0.43
Nodes (7): _os(), test_os_fusion.py — FIX 3(a): cross-scanner OS identification with calibrated, m, test_build_only_is_strong_but_not_certain(), test_build_smb2_hostname_is_high_confidence(), test_no_os_signal_yields_no_finding(), test_smb2_plus_p0f_stack_is_medium(), test_ttl_only_stays_a_hint()

### Community 480 - "Community 480"
Cohesion: 0.25
Nodes (2): ipv6_discovery reports on the RUN (its target is an interface name, or         t, TestEngineSummary

### Community 481 - "Community 481"
Cohesion: 0.25
Nodes (1): TestTuningFromParams

### Community 482 - "Community 482"
Cohesion: 0.54
Nodes (7): Raw scanner facts endpoint — inspect exactly what the vedha-agent collected., _scalars(), _sr(), test_raw_facts_bounds_and_no_results(), test_raw_facts_filter_by_scanner(), test_raw_facts_grouped_by_scanner(), _user()

### Community 483 - "Community 483"
Cohesion: 0.25
Nodes (4): A scanner that stood down because the service isn't on the host is NOT     degra, Splitting the label must NOT loosen auto-resolution. A skipped scanner is     st, test_skipped_scanner_is_not_reported_as_degraded(), test_skipped_scanner_still_proves_nothing_about_coverage()

### Community 484 - "Community 484"
Cohesion: 0.25
Nodes (4): _open(), service_banner now ATTEMPTS a TLS handshake on every unidentified port and     r, test_https_on_odd_port_routes_tls_and_web(), TestTlsProbedNegative

### Community 485 - "Community 485"
Cohesion: 0.25
Nodes (1): test_run_all_reconcile.py — cross-cutting: run_all and scan_funnel must derive t

### Community 486 - "Community 486"
Cohesion: 0.36
Nodes (5): test_scan_health.py — the probe scan-metrics → coverage/health verdict.  Guards, _summary(), test_clean_scan_is_healthy_and_does_not_warn(), test_local_resource_errors_flag_degraded(), test_missing_ports_flag_incomplete()

### Community 487 - "Community 487"
Cohesion: 0.46
Nodes (1): TestBuildResultsEnrichment

### Community 488 - "Community 488"
Cohesion: 0.43
Nodes (7): test_tier1_correlations.py — enterprise attack-path correlations built from the, _run(), test_anon_data_exposure_cluster(), test_mgmt_plane_exposed_on_cipher_zero_alone(), test_mgmt_plane_needs_two_when_no_cipher_zero(), test_single_anon_finding_does_not_correlate(), test_user_enum_plus_weak_auth()

### Community 489 - "Community 489"
Cohesion: 0.25
Nodes (5): Excluded on purpose — a bare ClientHello is the WRONG packet here., 3389 reaches TLS only after the X.224 rdpNegReq. rdp_scanner already         obs, 5986 is WinRM's TLS listener and IS included; these two are plaintext., STARTTLS negotiates in-band; implicit TLS would fail., TestDeliberateExclusions

### Community 490 - "Community 490"
Cohesion: 0.29
Nodes (6): _mirrored_py_files(), test_two_tree_parity.py — the guard the architecture review (#4) demanded.  `sca, Every .py present in BOTH trees (the mirrored set), excluding caches., A scanner that exists in only one tree is a wiring bug: one orchestrator     fam, test_mirrored_set_is_nonempty(), test_no_unmirrored_scanner_files()

### Community 491 - "Community 491"
Cohesion: 0.25
Nodes (8): Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, Upsert this worker's heartbeat. A stale row tells campaign-progress the     dete, Main loop: claim → process → repeat. Sleeps only when the queue is idle,     so, run_worker(), _write_heartbeat()

### Community 492 - "Community 492"
Cohesion: 0.29
Nodes (7): _load_env(), Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience., Load key=value lines from probe.env for dev convenience.

### Community 493 - "Community 493"
Cohesion: 0.29
Nodes (7): _error_result(), Single factory for error result dicts — no copy-paste., Single factory for error result dicts — no copy-paste., Single factory for error result dicts — no copy-paste., Single factory for error result dicts — no copy-paste., Single factory for error result dicts — no copy-paste., _runtime_manifest()

### Community 494 - "Community 494"
Cohesion: 0.29
Nodes (7): close_redis(), get_current_user(), Close the global Redis connection pool. Call during app shutdown., Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl, CurrentUser, Parsed from JWT claims — attached to request.state and injected as dependency., Parsed from JWT claims — attached to request.state and injected as dependency.

### Community 495 - "Community 495"
Cohesion: 0.48
Nodes (5): build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()

### Community 496 - "Community 496"
Cohesion: 0.67
Nodes (7): agents/greeting-introduction, main, 0510df3 going to build prompt and connection, architecture almost done, 8d65c92 first commit, a388bb3 script updated, architecture design and integration with adversa repo, bd7383f scanner fine ..now integrations, f5ce592 first commit

### Community 497 - "Community 497"
Cohesion: 0.33
Nodes (6): interpret_validation(), active_validation.py — manager-side decision core for safe active validation.  P, True iff this finding warrants an approval-gated active re-check.     Escalate o, Map a probe safe-check result to a verdict transition. Anything that isn't     a, should_escalate(), ValidationOutcome

### Community 498 - "Community 498"
Cohesion: 0.38
Nodes (6): base_score(), parse_vector(), cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network, CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r, Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin, _roundup()

### Community 499 - "Community 499"
Cohesion: 0.29
Nodes (5): _deterministic_layout(), GraphVisualizer, Numpy-free seed layout: place nodes on concentric rings by type so the     front, Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag, Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path

### Community 500 - "Community 500"
Cohesion: 0.29
Nodes (7): load_facts_jsonl(), Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., Anonymous SMB (null-session) information disclosure. The null session is a     m, Anonymous SMB (null-session) information disclosure. The null session is a     m, Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)., _rule_smb_enum()

### Community 501 - "Community 501"
Cohesion: 0.29
Nodes (4): RateLimiter, Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second., Simple async rate limiter: at most `rate` operations per second.

### Community 502 - "Community 502"
Cohesion: 0.33
Nodes (4): BaseScanner, Subclasses implement `scan_target(self, target)` (async), returning a list     o, Subclasses implement `scan_target(self, target)` (async), returning a list     o, Subclasses implement `scan_target(self, target)` (async), returning a list     o

### Community 503 - "Community 503"
Cohesion: 0.29
Nodes (6): interpret_dns_recursion(), interpret_memcached_stats(), interpret_ntp_monlist(), _ntp_monlist_probe(), SIP OPTIONS request — safe fingerprint method., _sip_probe()

### Community 504 - "Community 504"
Cohesion: 0.29
Nodes (4): Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, Acquire the concurrency gate (adaptive window or fixed semaphore),         run t, UDPScanner

### Community 505 - "Community 505"
Cohesion: 0.33
Nodes (3): _first(), LDAPScanner, Blocking: anonymous bind + RootDSE read + bounded tree-read probe.         Retur

### Community 506 - "Community 506"
Cohesion: 0.29
Nodes (6): accept_echo_reply(), True only for an ICMP ECHO reply that actually came FROM the probed host.      A, Send one ICMP echo; return observed TTL, None (no TTL), or "down"., Send one ICMP echo; return observed TTL, None (no TTL), or "down"., Send one ICMP echo; return observed TTL, None (no TTL), or "down"., Send one ICMP echo; return observed TTL, None (no TTL), or "down".

### Community 507 - "Community 507"
Cohesion: 0.29
Nodes (7): Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h, resolve()

### Community 508 - "Community 508"
Cohesion: 0.29
Nodes (6): interpret_dns_recursion(), interpret_memcached_stats(), interpret_ntp_monlist(), _ntp_monlist_probe(), SIP OPTIONS request — safe fingerprint method., _sip_probe()

### Community 509 - "Community 509"
Cohesion: 0.43
Nodes (2): CliProgressView, Renders campaign progress to a stream. On a TTY it re-draws one live block     i

### Community 510 - "Community 510"
Cohesion: 0.38
Nodes (6): _extract(), _is_external(), vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E, (proto, port, status) from a ScanResult or a plain dict., Compare per-vantage observations of one target.      `observations` maps a vanta, reconcile_vantages()

### Community 511 - "Community 511"
Cohesion: 0.38
Nodes (6): _expand_requested(), _parse_networks(), scope_targets.py — the single source of truth for "is this scan target inside th, Expand raw target tokens (IP / CIDR / ``a-b`` range) into networks.      Returns, Return the normalized list of authorized target networks, or ``None``.      * ``, validate_targets_in_scope()

### Community 512 - "Community 512"
Cohesion: 0.29
Nodes (1): TestBloodHoundCollector

### Community 513 - "Community 513"
Cohesion: 0.29
Nodes (1): TestDeceptionScore

### Community 514 - "Community 514"
Cohesion: 0.29
Nodes (1): test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.

### Community 515 - "Community 515"
Cohesion: 0.57
Nodes (6): Fleet: tenant-wide job feed with probe + engagement name resolution and filters., _scalars(), test_filter_by_probe_and_engagement_run_without_error(), test_lists_jobs_with_probe_and_engagement_names(), test_running_filter_is_accepted(), _user()

### Community 516 - "Community 516"
Cohesion: 0.52
Nodes (1): TestDiscoverFiltering

### Community 517 - "Community 517"
Cohesion: 0.29
Nodes (1): TestProfiles

### Community 518 - "Community 518"
Cohesion: 0.29
Nodes (2): FIX 5(b): don't tie an obvious workstation; require role ports/DomainRole     fo, TestWorkstationVsServer

### Community 519 - "Community 519"
Cohesion: 0.48
Nodes (1): TestAcceptEchoReply

### Community 520 - "Community 520"
Cohesion: 0.38
Nodes (6): _declared(), test_runtime_requirements_coverage.py — the probe IMAGE must be able to run ever, Package names declared in a requirements file, normalised and lowercased., A package shipped in the image but absent from requirements.txt is a     depende, test_runtime_image_installs_every_wired_branch_dependency(), test_runtime_is_a_subset_of_the_development_set()

### Community 521 - "Community 521"
Cohesion: 0.29
Nodes (1): TestMergeExclusions

### Community 522 - "Community 522"
Cohesion: 0.43
Nodes (3): The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa, TestSynRetransmit

### Community 523 - "Community 523"
Cohesion: 0.29
Nodes (5): Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., Verify the submit callback is called with the correct payload., When spool_submit is provided, it's used instead of direct submit., TestRunnerSubmission

### Community 524 - "Community 524"
Cohesion: 0.29
Nodes (3): _Buf, test_cli_view_deduplicates_unchanged_status(), test_cli_view_emits_one_line_per_transition()

### Community 526 - "Community 526"
Cohesion: 0.48
Nodes (6): _b64(), issue(), keygen(), main(), pubkey(), Print the vendor PUBLIC key (hex) derived from the private key.      build/seal-

### Community 527 - "Community 527"
Cohesion: 0.33
Nodes (5): Return agent IDs whose status is 'online' (idle, ready for job)., Deliver a job-push to an agent wherever its socket is connected.          Return, Deliver a job-push to an agent wherever its socket is connected.          Return, Return agent IDs whose status is 'online' (idle, ready for job)., Return agent IDs whose status is 'online' (idle, ready for job).

### Community 528 - "Community 528"
Cohesion: 0.29
Nodes (7): _mark_retry_or_dead(), Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus, Reschedule with exponential backoff, or dead-letter once attempts are     exhaus

### Community 529 - "Community 529"
Cohesion: 0.29
Nodes (7): Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Run one component without allowing a target-specific bug to abort peers., Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes, _split_cached()

### Community 530 - "Community 530"
Cohesion: 0.29
Nodes (7): Accumulate wall time for a stage. No-op when tracing is off., Run ONE deep-scan branch for one host: the gate -> split-cache -> scan ->     re, _record(), _record_reused(), _run_branch(), _store_results(), _timed()

### Community 531 - "Community 531"
Cohesion: 0.40
Nodes (5): _content_hash(), main(), build_nvd_cpe_snapshot.py — generate the NVD/CPE companion vuln snapshot.  WHY A, One OSV-shaped record: affected below `fixed` (NVD versionEndExcluding)., _rec()

### Community 532 - "Community 532"
Cohesion: 0.40
Nodes (5): exposure_fusion_service.py — apply multi-probe vantage fusion to Service rows., Reconstruct one {"exposure": [...]} dict per probe from persisted facts.      Ea, Fuse all probes' exposure_matrix observations for an engagement and stamp     th, recompute_fused_exposure(), _results_from_scan_rows()

### Community 533 - "Community 533"
Cohesion: 0.40
Nodes (5): asset_type_for(), device_profiles(), device_profile.py — map a probe device_inventory result onto asset fields.  The, The AssetType for a classifier device_type, or None to keep the existing., ip → {asset_type, device_role, role_detail, role_confidence} from a probe     de

### Community 534 - "Community 534"
Cohesion: 0.33
Nodes (5): escalate_for_exposure(), exposure.py — reachability-aware risk from the probe's exposure_matrix use-case., (ip, proto, port) → exposure verdict, from a probe exposure_matrix result., Bump a finding one severity rung when its service is internet-reachable.      On, service_exposure()

### Community 535 - "Community 535"
Cohesion: 0.33
Nodes (3): Apply constraints + indexes (idempotent)., Run a Cypher statement and return records as dicts. [] if not connected., Run a parametrised write with UNWIND batching for bulk node/edge loads.

### Community 536 - "Community 536"
Cohesion: 0.33
Nodes (5): True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, syn_scan_supported()

### Community 537 - "Community 537"
Cohesion: 0.33
Nodes (5): build_icmp_timestamp(), parse_icmp_timestamps(), Parse an ICMP timestamp reply (type 14): id/seq/ttl plus the three 32-bit     ti, Send an ICMP timestamp request (type 13); return {ttl, transmit} from a, Send an ICMP timestamp request (type 13); return {ttl, transmit} from a

### Community 538 - "Community 538"
Cohesion: 0.33
Nodes (6): match_stack_signature(), _open_icmp_socket(), Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw., p0f-style match on (initial TTL, option layout, window scale) → a specific     s, Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw., Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw.

### Community 539 - "Community 539"
Cohesion: 0.33
Nodes (6): _family_of(), Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname).

### Community 540 - "Community 540"
Cohesion: 0.33
Nodes (5): Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude).

### Community 541 - "Community 541"
Cohesion: 0.33
Nodes (5): True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't, syn_scan_supported()

### Community 542 - "Community 542"
Cohesion: 0.47
Nodes (2): Preferred scheme first, the other as a fallback: a scheme guess must         nev, WebScanner

### Community 543 - "Community 543"
Cohesion: 0.40
Nodes (5): AttemptClaim, claim_job_attempt(), Atomically claim a pending job and create its fenced attempt ledger row., Renew only the currently installed running attempt/fence., renew_job_attempt()

### Community 544 - "Community 544"
Cohesion: 0.33
Nodes (1): TestNTLMRelayChecker

### Community 545 - "Community 545"
Cohesion: 0.53
Nodes (4): _cached_transport(), test_cached_identity_refreshes_current_capabilities(), test_cached_identity_retries_transient_refresh_failure(), test_rejected_cached_token_falls_back_to_idempotent_registration()

### Community 546 - "Community 546"
Cohesion: 0.33
Nodes (1): TestVulnDB

### Community 547 - "Community 547"
Cohesion: 0.33
Nodes (1): TestDeriveZones

### Community 548 - "Community 548"
Cohesion: 0.53
Nodes (2): A socket whose connect() fails for `dead_family`, succeeds otherwise., TestSmbNegotiateFallback

### Community 549 - "Community 549"
Cohesion: 0.60
Nodes (5): Unit tests for the dashboard list endpoints (jobs + assets)., _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user()

### Community 550 - "Community 550"
Cohesion: 0.33
Nodes (4): Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it., Job carries encrypted_scope → TaskRunner decrypts → uses it., Wrong key → decryption fails → graceful fallback to params scope., TestTaskRunnerWithEncryptedScope

### Community 551 - "Community 551"
Cohesion: 0.33
Nodes (2): Phase 1: combined scope validation (validate + excludes)., TestScopeValidationPipeline

### Community 552 - "Community 552"
Cohesion: 0.33
Nodes (2): Phase 2: WebSocket message parsing., TestWebSocketMessageProtocol

### Community 553 - "Community 553"
Cohesion: 0.33
Nodes (4): Phase 5: startup gauntlet checks., With LICENSE_ENFORCED=false, gauntlet returns None., Wrong HW fingerprint blocks startup., TestStartupGauntlet

### Community 554 - "Community 554"
Cohesion: 0.33
Nodes (1): test_main_scripts_device_ties.py — Phase 23: device classification never resolve

### Community 555 - "Community 555"
Cohesion: 0.33
Nodes (2): test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti, TestNmapEntityGuard

### Community 556 - "Community 556"
Cohesion: 0.33
Nodes (1): test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.  T

### Community 557 - "Community 557"
Cohesion: 0.33
Nodes (1): TestClamp

### Community 558 - "Community 558"
Cohesion: 0.33
Nodes (1): TestEngagementModes

### Community 559 - "Community 559"
Cohesion: 0.53
Nodes (5): _manifest(), test_probe_manifest.py — the `agent.agent manifest` command that the seal-parity, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_contract()

### Community 560 - "Community 560"
Cohesion: 0.73
Nodes (5): _db_returning(), _finding(), test_covered_clean_medium_finding_is_auto_resolved(), test_db_version_change_blocks_resolution(), test_uncovered_finding_is_left_open()

### Community 562 - "Community 562"
Cohesion: 0.33
Nodes (1): TestFetchEngagementScope

### Community 563 - "Community 563"
Cohesion: 0.33
Nodes (1): TestValidateEnv

### Community 564 - "Community 564"
Cohesion: 0.33
Nodes (1): TestParseHttpHead

### Community 565 - "Community 565"
Cohesion: 0.33
Nodes (1): TestSMBEnumScanner

### Community 566 - "Community 566"
Cohesion: 0.33
Nodes (1): TestSMBLDAPFindings

### Community 567 - "Community 567"
Cohesion: 0.33
Nodes (1): TestOptionParsing

### Community 568 - "Community 568"
Cohesion: 0.33
Nodes (1): TestAssessTarpit

### Community 571 - "Community 571"
Cohesion: 0.33
Nodes (2): Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs., TestChooseSourcePort

### Community 572 - "Community 572"
Cohesion: 0.33
Nodes (5): Push a job to the first online agent in the requested tenant.          Returns t, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag, Return agent_ids whose last heartbeat is older than `seconds`.          These ag

### Community 573 - "Community 573"
Cohesion: 0.33
Nodes (5): Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs., Return a snapshot of all connected agent IDs.

### Community 574 - "Community 574"
Cohesion: 0.33
Nodes (5): Push a job to the first online agent in the requested tenant.          Returns t, Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'.

### Community 575 - "Community 575"
Cohesion: 0.33
Nodes (5): Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy)., Check if a specific agent is online (connected + not busy).

### Community 576 - "Community 576"
Cohesion: 0.40
Nodes (5): _env_number(), Read a bounded numeric safety setting without trusting the environment., Read a bounded numeric safety setting without trusting the environment., Read a bounded numeric safety setting without trusting the environment., Read a bounded numeric safety setting without trusting the environment.

### Community 577 - "Community 577"
Cohesion: 0.40
Nodes (3): verification_graph.py — optional LangGraph orchestration for passive verificatio, Run passive verification. Uses the LangGraph StateGraph when available;     othe, run_verification()

### Community 578 - "Community 578"
Cohesion: 0.40
Nodes (5): _corr_legacy_windows(), SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas, SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas

### Community 579 - "Community 579"
Cohesion: 0.40
Nodes (5): _family_of(), Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)., Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname).

### Community 580 - "Community 580"
Cohesion: 0.40
Nodes (4): Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation.

### Community 581 - "Community 581"
Cohesion: 0.40
Nodes (4): Requested ports that were never recorded — the silent-skip proof., Requested ports that were never recorded — the silent-skip proof., Requested ports that were never recorded — the silent-skip proof., Requested ports that were never recorded — the silent-skip proof.

### Community 582 - "Community 582"
Cohesion: 0.40
Nodes (4): Ports recorded more than once (a port must get exactly one verdict)., Ports recorded more than once (a port must get exactly one verdict)., Ports recorded more than once (a port must get exactly one verdict)., Ports recorded more than once (a port must get exactly one verdict).

### Community 583 - "Community 583"
Cohesion: 0.40
Nodes (3): _Scanner, Protocol, _Scanner

### Community 584 - "Community 584"
Cohesion: 0.40
Nodes (5): classify(), SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)., SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)., SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)., SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate).

### Community 585 - "Community 585"
Cohesion: 0.40
Nodes (5): Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., syn_cookie()

### Community 586 - "Community 586"
Cohesion: 0.40
Nodes (5): icmp_supported(), True if we can open an ICMP socket (datagram-ICMP or raw)., True if we can open an ICMP socket (datagram-ICMP or raw)., True if we can open an ICMP socket (datagram-ICMP or raw)., True if we can open an ICMP socket (datagram-ICMP or raw).

### Community 587 - "Community 587"
Cohesion: 0.40
Nodes (5): parse_icmp_reply(), Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres, Return (ttl, icmp_bytes). Raw-socket delivery prepends the full IPv4 header, Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres, _strip_ip_header()

### Community 588 - "Community 588"
Cohesion: 0.40
Nodes (4): Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation., Tally exactly one terminal per-port observation.

### Community 589 - "Community 589"
Cohesion: 0.40
Nodes (4): Requested ports that were never recorded — the silent-skip proof., Requested ports that were never recorded — the silent-skip proof., Requested ports that were never recorded — the silent-skip proof., Requested ports that were never recorded — the silent-skip proof.

### Community 590 - "Community 590"
Cohesion: 0.40
Nodes (4): Ports recorded more than once (a port must get exactly one verdict)., Ports recorded more than once (a port must get exactly one verdict)., Ports recorded more than once (a port must get exactly one verdict)., Ports recorded more than once (a port must get exactly one verdict).

### Community 591 - "Community 591"
Cohesion: 0.40
Nodes (5): classify(), SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)., SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)., SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)., SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate).

### Community 592 - "Community 592"
Cohesion: 0.40
Nodes (5): Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1., syn_cookie()

### Community 593 - "Community 593"
Cohesion: 0.50
Nodes (3): _as_text(), classify_unauth_access(), Decide whether `banner` proves unauthenticated access for `service`.      True =

### Community 595 - "Community 595"
Cohesion: 0.60
Nodes (2): _claim_fixture(), TestAtomicWebSocketClaim

### Community 596 - "Community 596"
Cohesion: 0.40
Nodes (1): TestTenantWebSocketSelection

### Community 597 - "Community 597"
Cohesion: 0.40
Nodes (1): TestGetAgentJobs

### Community 598 - "Community 598"
Cohesion: 0.40
Nodes (1): TestIngestParse

### Community 599 - "Community 599"
Cohesion: 0.40
Nodes (1): TestMirrorAge

### Community 600 - "Community 600"
Cohesion: 0.70
Nodes (1): TestDNSFindings

### Community 601 - "Community 601"
Cohesion: 0.70
Nodes (1): TestDNSScanner

### Community 603 - "Community 603"
Cohesion: 0.70
Nodes (1): TestFTPFindings

### Community 604 - "Community 604"
Cohesion: 0.70
Nodes (1): TestFTPScanner

### Community 605 - "Community 605"
Cohesion: 0.40
Nodes (1): TestCheckHwBind

### Community 606 - "Community 606"
Cohesion: 0.40
Nodes (2): Phase 1: result spool with upload retry., TestResultSpoolWithRetry

### Community 607 - "Community 607"
Cohesion: 0.40
Nodes (3): Phase 4 + Phase 1: Transport sends public_key during registration., Backward compat: registration without public_key is fine., TestTransportWithIdentity

### Community 608 - "Community 608"
Cohesion: 0.70
Nodes (1): TestMSRPCScanner

### Community 609 - "Community 609"
Cohesion: 0.40
Nodes (1): test_nmap_wrapper.py — the "nmap returned 0 while native scanners saw ports" bug

### Community 610 - "Community 610"
Cohesion: 0.80
Nodes (1): TestCliOnlineFlag

### Community 611 - "Community 611"
Cohesion: 0.50
Nodes (1): TestIcmpParse

### Community 612 - "Community 612"
Cohesion: 0.60
Nodes (1): TestIcmpTimestamps

### Community 613 - "Community 613"
Cohesion: 0.40
Nodes (1): TestGate2

### Community 614 - "Community 614"
Cohesion: 0.40
Nodes (1): TestLooksLikeHttp

### Community 615 - "Community 615"
Cohesion: 0.40
Nodes (1): TestLooksLikeTls

### Community 616 - "Community 616"
Cohesion: 0.40
Nodes (1): TestResolveScanType

### Community 617 - "Community 617"
Cohesion: 0.40
Nodes (1): TestTargets

### Community 618 - "Community 618"
Cohesion: 0.60
Nodes (4): test_remediation_upsert_integration.py — real-Postgres verification of the remed, _run(), _stmt(), test_upsert_resets_gate_and_is_race_safe()

### Community 619 - "Community 619"
Cohesion: 0.70
Nodes (1): TestRsyncFindings

### Community 620 - "Community 620"
Cohesion: 0.70
Nodes (1): TestSMTPFindings

### Community 621 - "Community 621"
Cohesion: 0.70
Nodes (1): TestSSHFindings

### Community 622 - "Community 622"
Cohesion: 0.70
Nodes (1): TestVerifyReplyCookie

### Community 623 - "Community 623"
Cohesion: 0.80
Nodes (1): TestPortScannerTarpitFlag

### Community 624 - "Community 624"
Cohesion: 0.40
Nodes (2): The drift that used to exist: spec allows a port the gate refuses., TestSingleSourceOfTruth

### Community 625 - "Community 625"
Cohesion: 0.70
Nodes (1): TestVNCFindings

### Community 626 - "Community 626"
Cohesion: 0.40
Nodes (2): Evasion: blur a fixed scan cadence with a bounded random per-probe delay., TestJitteredDelay

### Community 627 - "Community 627"
Cohesion: 0.40
Nodes (5): _dead_letter_stale_stmt(), Stranded events that already exhausted their retry budget → dead-letter.     Bou, Stranded events that already exhausted their retry budget → dead-letter.     Bou, Stranded events that already exhausted their retry budget → dead-letter.     Bou, Stranded events that already exhausted their retry budget → dead-letter.     Bou

### Community 628 - "Community 628"
Cohesion: 0.40
Nodes (5): enqueue(), Add an outbox event to the caller's session. Does NOT commit — it commits     at, Add an outbox event to the caller's session. Does NOT commit — it commits     at, Add an outbox event to the caller's session. Does NOT commit — it commits     at, Add an outbox event to the caller's session. Does NOT commit — it commits     at

### Community 629 - "Community 629"
Cohesion: 0.40
Nodes (5): _handle_facts_ready(), Run the deterministic detection pipeline on a submitted facts payload.     Re-re, Run the deterministic detection pipeline on a submitted facts payload.     Re-re, Run the deterministic detection pipeline on a submitted facts payload.     Re-re, Run the deterministic detection pipeline on a submitted facts payload.     Re-re

### Community 630 - "Community 630"
Cohesion: 0.40
Nodes (5): The `locked_at` boundary before which a PROCESSING row is considered dead., The `locked_at` boundary before which a PROCESSING row is considered dead., The `locked_at` boundary before which a PROCESSING row is considered dead., The `locked_at` boundary before which a PROCESSING row is considered dead., _stale_cutoff()

### Community 631 - "Community 631"
Cohesion: 0.40
Nodes (5): Decorator: bind an async handler to a topic., Decorator: bind an async handler to a topic., Decorator: bind an async handler to a topic., Decorator: bind an async handler to a topic., register()

### Community 632 - "Community 632"
Cohesion: 0.40
Nodes (5): gate_5_branch_eligible(), Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep, Does `branch` apply to this host?       - Must be in this profile's allowed deep

### Community 633 - "Community 633"
Cohesion: 0.40
Nodes (5): Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., Run one component without allowing a target-specific bug to abort peers., _scan_one()

### Community 634 - "Community 634"
Cohesion: 0.50
Nodes (4): detect_all(), detect_posture(), Run posture detection across every asset. Accepts an IngestResult (uses its, Apply every posture rule to one asset's facts. Deduplicates by     (rule_id, por

### Community 635 - "Community 635"
Cohesion: 0.50
Nodes (4): async_udp_probe_retry(), `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de, `async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de

### Community 636 - "Community 636"
Cohesion: 0.50
Nodes (4): expand_targets(), Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10, Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10

### Community 637 - "Community 637"
Cohesion: 0.50
Nodes (3): Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude)., Read-only view of excluded networks (to build masscan --exclude).

### Community 638 - "Community 638"
Cohesion: 0.50
Nodes (3): lookup(), ssh_kexdb.py — vendored SSH algorithm weakness database (the "content" half of t, Return (failures, warnings, infos) for one offered algorithm, or None if     the

### Community 639 - "Community 639"
Cohesion: 0.50
Nodes (3): Turn resolved port states + harvested intel into ScanResults. Pure —         no, Turn resolved port states + harvested intel into ScanResults. Pure —         no, Turn resolved port states + harvested intel into ScanResults. Pure —         no

### Community 640 - "Community 640"
Cohesion: 0.67
Nodes (1): SSHCollector

### Community 641 - "Community 641"
Cohesion: 0.50
Nodes (3): lookup(), ssh_kexdb.py — vendored SSH algorithm weakness database (the "content" half of t, Return (failures, warnings, infos) for one offered algorithm, or None if     the

### Community 642 - "Community 642"
Cohesion: 0.50
Nodes (3): Turn resolved port states + harvested intel into ScanResults. Pure —         no, Turn resolved port states + harvested intel into ScanResults. Pure —         no, Turn resolved port states + harvested intel into ScanResults. Pure —         no

### Community 643 - "Community 643"
Cohesion: 0.83
Nodes (1): TestIPMIFindings

### Community 644 - "Community 644"
Cohesion: 0.83
Nodes (1): TestIPMIScanner

### Community 645 - "Community 645"
Cohesion: 0.83
Nodes (1): TestMSRPCFindings

### Community 646 - "Community 646"
Cohesion: 0.83
Nodes (1): TestTimestampFallback

### Community 647 - "Community 647"
Cohesion: 0.83
Nodes (1): TestPrinterScanner

### Community 648 - "Community 648"
Cohesion: 0.50
Nodes (1): TestGate0

### Community 649 - "Community 649"
Cohesion: 0.50
Nodes (1): TestGate3

### Community 650 - "Community 650"
Cohesion: 0.50
Nodes (1): TestGate4

### Community 651 - "Community 651"
Cohesion: 0.50
Nodes (1): TestRateLimiter

### Community 652 - "Community 652"
Cohesion: 0.50
Nodes (1): TestRouteBranches

### Community 653 - "Community 653"
Cohesion: 0.50
Nodes (1): TestScanResult

### Community 654 - "Community 654"
Cohesion: 0.83
Nodes (3): _objects(), test_expired_attempt_fails_job_when_retry_budget_is_exhausted(), test_expired_attempt_requeues_with_fence_history_preserved()

### Community 655 - "Community 655"
Cohesion: 0.50
Nodes (1): TestPositiveTls

### Community 656 - "Community 656"
Cohesion: 0.50
Nodes (1): TestStructuredService

### Community 657 - "Community 657"
Cohesion: 0.83
Nodes (1): TestRsyncScanner

### Community 658 - "Community 658"
Cohesion: 0.50
Nodes (1): Product-boundary tests for the single-dashboard Manager API.

### Community 659 - "Community 659"
Cohesion: 0.83
Nodes (1): TestSMTPScanner

### Community 661 - "Community 661"
Cohesion: 0.83
Nodes (1): TestVNCScanner

### Community 662 - "Community 662"
Cohesion: 0.50
Nodes (1): Add is_active to users and tenants; add password_expires_at to users.  All exist

### Community 663 - "Community 663"
Cohesion: 0.50
Nodes (1): Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision

### Community 664 - "Community 664"
Cohesion: 0.50
Nodes (1): Finding verification verdict columns (P2 passive verification).  Revision ID: 00

### Community 665 - "Community 665"
Cohesion: 0.50
Nodes (1): Approval-gated safe active-validation requests (P3).  Revision ID: 0022 Revises:

### Community 666 - "Community 666"
Cohesion: 0.50
Nodes (1): Client portal slug — the customer's stable 'user as domain' handle.  Adds users.

### Community 667 - "Community 667"
Cohesion: 0.50
Nodes (1): Scan-request targets + intensity — the rich customer scan request.  Adds two nul

### Community 668 - "Community 668"
Cohesion: 0.50
Nodes (1): Remediation plans — cached, OS-specific, structured remediation for a finding.

### Community 669 - "Community 669"
Cohesion: 0.50
Nodes (1): SLA policies — per-tenant custom remediation windows (hours per severity).  One

### Community 670 - "Community 670"
Cohesion: 0.50
Nodes (1): Integrations — per-tenant notification config (email / Slack / Jira).  One row p

### Community 671 - "Community 671"
Cohesion: 0.50
Nodes (1): Finding lifecycle audit trail — append-only per-finding event log.  One row per

### Community 672 - "Community 672"
Cohesion: 0.50
Nodes (3): Record a heartbeat from an agent., Record a heartbeat from an agent., Record a heartbeat from an agent.

### Community 673 - "Community 673"
Cohesion: 0.50
Nodes (3): Register an agent's WebSocket connection.          If the agent already has a co, Register an agent's WebSocket connection.          If the agent already has a co, Register an agent's WebSocket connection.          If the agent already has a co

### Community 674 - "Community 674"
Cohesion: 0.50
Nodes (4): is_stale_processing(), Return whether a claimed event was stranded by a dead worker.      `_claim_batch, Return whether a claimed event was stranded by a dead worker.      `_claim_batch, Return whether a claimed event was stranded by a dead worker.      `_claim_batch

### Community 675 - "Community 675"
Cohesion: 0.50
Nodes (3): BranchSpec, True when the fact describes the host rather than one port — it is         cache, One deep-scan branch. `branch` is the gate key (gates.PROFILE_DEEP_BRANCHES

### Community 676 - "Community 676"
Cohesion: 0.67
Nodes (3): _cert(), _tls_expired(), _tls_self_signed()

### Community 677 - "Community 677"
Cohesion: 0.67
Nodes (3): Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, _rule_ftp()

### Community 678 - "Community 678"
Cohesion: 0.67
Nodes (3): rsync daemon exposure. Anonymously-selectable modules are the high finding     (, rsync daemon exposure. Anonymously-selectable modules are the high finding     (, _rule_rsync()

### Community 679 - "Community 679"
Cohesion: 0.67
Nodes (3): VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo, VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo, _rule_vnc()

### Community 680 - "Community 680"
Cohesion: 0.67
Nodes (3): IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, _rule_ipmi()

### Community 681 - "Community 681"
Cohesion: 0.67
Nodes (3): SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., _rule_smtp()

### Community 682 - "Community 682"
Cohesion: 0.67
Nodes (3): Windows RPC endpoint-mapper disclosure — the internal RPC service map., Windows RPC endpoint-mapper disclosure — the internal RPC service map., _rule_msrpc()

### Community 683 - "Community 683"
Cohesion: 0.67
Nodes (3): Exposed network printer — an information leak and an attack surface., Exposed network printer — an information leak and an attack surface., _rule_printer()

### Community 684 - "Community 684"
Cohesion: 0.67
Nodes (2): Gentle second look at ports that stayed silent through the main sweep., Gentle second look at ports that stayed silent through the main sweep.

### Community 685 - "Community 685"
Cohesion: 0.67
Nodes (3): interpret_ike(), Parse IKEv1 or IKEv2 response header., Parse IKEv1 or IKEv2 response header.

### Community 686 - "Community 686"
Cohesion: 0.67
Nodes (3): interpret_ipmi(), Parse RMCP Pong; extract supported entities and IPMI capabilities., Parse RMCP Pong; extract supported entities and IPMI capabilities.

### Community 687 - "Community 687"
Cohesion: 0.67
Nodes (3): interpret_mdns(), Return byte count and check QR bit (1 = response)., Return byte count and check QR bit (1 = response).

### Community 688 - "Community 688"
Cohesion: 0.67
Nodes (3): interpret_sip(), Extract SIP version + server header from a SIP response., Extract SIP version + server header from a SIP response.

### Community 689 - "Community 689"
Cohesion: 0.67
Nodes (3): interpret_ssdp(), Extract Location and Server from SSDP response., Extract Location and Server from SSDP response.

### Community 690 - "Community 690"
Cohesion: 0.67
Nodes (3): _ipmi_probe(), RMCP Ping (ASF Presence Ping) to detect IPMI/BMC., RMCP Ping (ASF Presence Ping) to detect IPMI/BMC.

### Community 691 - "Community 691"
Cohesion: 0.67
Nodes (3): _mdns_probe(), mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)., mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353).

### Community 692 - "Community 692"
Cohesion: 0.67
Nodes (3): UPnP/SSDP M-SEARCH — unicast to target:1900., UPnP/SSDP M-SEARCH — unicast to target:1900., _ssdp_probe()

### Community 693 - "Community 693"
Cohesion: 0.67
Nodes (3): Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e, Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e, _rule_rdp()

### Community 694 - "Community 694"
Cohesion: 0.67
Nodes (3): Anonymous SMB (null-session) information disclosure. The null session is a     m, Anonymous SMB (null-session) information disclosure. The null session is a     m, _rule_smb_enum()

### Community 695 - "Community 695"
Cohesion: 0.67
Nodes (3): Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a, Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a, _rule_ldap()

### Community 696 - "Community 696"
Cohesion: 0.67
Nodes (3): DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent, DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent, _rule_dns()

### Community 697 - "Community 697"
Cohesion: 0.67
Nodes (3): NFS anonymous export exposure. A world-readable export is the high-value     fin, NFS anonymous export exposure. A world-readable export is the high-value     fin, _rule_nfs()

### Community 698 - "Community 698"
Cohesion: 0.67
Nodes (3): Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig, _rule_ftp()

### Community 699 - "Community 699"
Cohesion: 0.67
Nodes (3): rsync daemon exposure. Anonymously-selectable modules are the high finding     (, rsync daemon exposure. Anonymously-selectable modules are the high finding     (, _rule_rsync()

### Community 700 - "Community 700"
Cohesion: 0.67
Nodes (3): VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo, VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo, _rule_vnc()

### Community 701 - "Community 701"
Cohesion: 0.67
Nodes (3): IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable, _rule_ipmi()

### Community 702 - "Community 702"
Cohesion: 0.67
Nodes (3): SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)., _rule_smtp()

### Community 703 - "Community 703"
Cohesion: 0.67
Nodes (3): Windows RPC endpoint-mapper disclosure — the internal RPC service map., Windows RPC endpoint-mapper disclosure — the internal RPC service map., _rule_msrpc()

### Community 704 - "Community 704"
Cohesion: 0.67
Nodes (3): Exposed network printer — an information leak and an attack surface., Exposed network printer — an information leak and an attack surface., _rule_printer()

### Community 705 - "Community 705"
Cohesion: 0.67
Nodes (2): Gentle second look at ports that stayed silent through the main sweep., Gentle second look at ports that stayed silent through the main sweep.

### Community 706 - "Community 706"
Cohesion: 0.67
Nodes (3): interpret_ike(), Parse IKEv1 or IKEv2 response header., Parse IKEv1 or IKEv2 response header.

### Community 707 - "Community 707"
Cohesion: 0.67
Nodes (3): interpret_ipmi(), Parse RMCP Pong; extract supported entities and IPMI capabilities., Parse RMCP Pong; extract supported entities and IPMI capabilities.

### Community 708 - "Community 708"
Cohesion: 0.67
Nodes (3): interpret_mdns(), Return byte count and check QR bit (1 = response)., Return byte count and check QR bit (1 = response).

### Community 709 - "Community 709"
Cohesion: 0.67
Nodes (3): interpret_sip(), Extract SIP version + server header from a SIP response., Extract SIP version + server header from a SIP response.

### Community 710 - "Community 710"
Cohesion: 0.67
Nodes (3): interpret_ssdp(), Extract Location and Server from SSDP response., Extract Location and Server from SSDP response.

### Community 711 - "Community 711"
Cohesion: 0.67
Nodes (3): _ipmi_probe(), RMCP Ping (ASF Presence Ping) to detect IPMI/BMC., RMCP Ping (ASF Presence Ping) to detect IPMI/BMC.

### Community 712 - "Community 712"
Cohesion: 0.67
Nodes (3): _mdns_probe(), mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)., mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353).

### Community 713 - "Community 713"
Cohesion: 0.67
Nodes (3): UPnP/SSDP M-SEARCH — unicast to target:1900., UPnP/SSDP M-SEARCH — unicast to target:1900., _ssdp_probe()

### Community 714 - "Community 714"
Cohesion: 0.67
Nodes (1): TestJobSecretBoundary

### Community 715 - "Community 715"
Cohesion: 0.67
Nodes (1): TestAssetMergeCredentialed

### Community 716 - "Community 716"
Cohesion: 0.67
Nodes (1): TestAssetMergeHostDiscovery

### Community 717 - "Community 717"
Cohesion: 0.67
Nodes (1): TestAssetMergePortScan

### Community 718 - "Community 718"
Cohesion: 0.67
Nodes (1): TestAssetOpenPortsForDeepScan

### Community 720 - "Community 720"
Cohesion: 1.00
Nodes (2): build(), main()

### Community 721 - "Community 721"
Cohesion: 1.00
Nodes (2): Collapse every trace for one rule into a single verdict + reason strings.     Pr, verdict_for_rule()

### Community 722 - "Community 722"
Cohesion: 1.00
Nodes (2): Engagement-level coverage roll-up over a set of traces. `rules_blind > 0`     is, summarize_traces()

### Community 723 - "Community 723"
Cohesion: 1.00
Nodes (2): Fires on EITHER of the rdp_scanner's two independent probes.      The scanner pr, _rdp_no_nla()

### Community 724 - "Community 724"
Cohesion: 1.00
Nodes (2): The server REFUSED a TLS-capable negotiation, so the session falls back to     l, _rdp_no_tls()

### Community 725 - "Community 725"
Cohesion: 1.00
Nodes (2): VNC type 2 is the legacy DES-based challenge with an 8-character password     ce, _vnc_weak_auth()

### Community 734 - "Community 734"
Cohesion: 1.00
Nodes (1): TestAssetMergePassiveCollect

### Community 735 - "Community 735"
Cohesion: 1.00
Nodes (1): TestAssetMergeServiceBanner

### Community 736 - "Community 736"
Cohesion: 1.00
Nodes (1): TestAssetMergeSmbScan

### Community 737 - "Community 737"
Cohesion: 1.00
Nodes (1): TestAssetMergeTlsScan

### Community 738 - "Community 738"
Cohesion: 1.00
Nodes (1): TestAssetMergeUnknownScanner

### Community 739 - "Community 739"
Cohesion: 1.00
Nodes (1): TestAssetMergeWebScan

### Community 741 - "Community 741"
Cohesion: 1.00
Nodes (1): Fast port discovery with naabu. Feeds port list to Nmap.

### Community 742 - "Community 742"
Cohesion: 1.00
Nodes (1): Nmap service enumeration. Accepts port list from Naabu.

### Community 743 - "Community 743"
Cohesion: 1.00
Nodes (1): Nuclei vulnerability scan — production-ready.

### Community 744 - "Community 744"
Cohesion: 1.00
Nodes (1): Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.

### Community 745 - "Community 745"
Cohesion: 1.00
Nodes (1): NetExec SMB validation: signing, null sessions, SMBv1.

### Community 746 - "Community 746"
Cohesion: 1.00
Nodes (1): testssl.sh TLS/SSL analysis.

### Community 747 - "Community 747"
Cohesion: 1.00
Nodes (1): Extract HTTP/HTTPS URLs from nmap XML output.

### Community 748 - "Community 748"
Cohesion: 1.00
Nodes (1): EyeWitness screenshot evidence collection.

### Community 749 - "Community 749"
Cohesion: 1.00
Nodes (1): Safe lateral movement checks — no actual exploitation.

### Community 750 - "Community 750"
Cohesion: 1.00
Nodes (1): Cloud infrastructure scan (AWS/Azure/GCP).

### Community 751 - "Community 751"
Cohesion: 1.00
Nodes (1): Read a KV-v2 secret from Vault.

### Community 752 - "Community 752"
Cohesion: 1.00
Nodes (1): Verify the Python probe can open what the TypeScript manager sealed (T14 interop

### Community 753 - "Community 753"
Cohesion: 1.00
Nodes (1): Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO

### Community 754 - "Community 754"
Cohesion: 1.00
Nodes (1): Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).

### Community 755 - "Community 755"
Cohesion: 1.00
Nodes (1): End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.

### Community 756 - "Community 756"
Cohesion: 1.00
Nodes (1): Deterministic stand-ins emitting realistic output for 127.0.0.1.

### Community 757 - "Community 757"
Cohesion: 1.00
Nodes (1): Make a per-host scanner instance share ONE rate limiter + semaphore with all

### Community 758 - "Community 758"
Cohesion: 1.00
Nodes (1): Make a raw banner safe and readable for the summary line.      Many services ans

### Community 759 - "Community 759"
Cohesion: 1.00
Nodes (1): # NOTE: credentialed collectors (ssh_collector, windows_collector) are run

### Community 760 - "Community 760"
Cohesion: 1.00
Nodes (1): ThreadingHTTPServer

## Knowledge Gaps
- **3995 isolated node(s):** `Rule`, `vedha_ref.evidence_store -- the layer the whole strategy rests on.  Thesis under`, `Cluster observations into assets using fingerprint keys.      Strong keys merge`, `The industry default, for comparison. Included so the cost is measurable.`, `Answer a brand-new rule against evidence already on disk.      No network traffi` (+3990 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 136`** (1 nodes): `TestResultSpool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 185`** (1 nodes): `TestUDPProbeConstruction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (1 nodes): `TestServiceIdentifier`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (1 nodes): `TestSNMPBerUtilities`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (2 nodes): `The diagnostic that turns a silent stuck-pending job into a fixable         one:`, `TestAgentJobCompatibility`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 298`** (1 nodes): `TestMobileScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 300`** (1 nodes): `TestFingerprintOs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 301`** (1 nodes): `TestValidateTargetsInScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 322`** (1 nodes): `test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 324`** (2 nodes): `_make_scan_record()`, `TestDeltaEngine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 327`** (1 nodes): `TestScopeGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 354`** (1 nodes): `TestPathAnalyzer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 355`** (1 nodes): `test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 359`** (2 nodes): `Tests that use the real engine but with no-op callbacks.`, `TestRunnerHeadless`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 371`** (1 nodes): `TestADCSChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 372`** (1 nodes): `TestVersionInRanges`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 375`** (1 nodes): `TestExpandTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 376`** (2 nodes): `test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()`, `_token()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 379`** (1 nodes): `TestSendPacer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 380`** (2 nodes): `Re-pointing to a different manager must forget the OLD manager's         pinned`, `TestIdentity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 382`** (1 nodes): `TestNmapXMLParser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 400`** (1 nodes): `TestGraphBuilder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 401`** (1 nodes): `TestVersion`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 402`** (2 nodes): `ipv6_discovery reports on the RUN, not a host: its target is the local         i`, `TestIngestFile`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 407`** (1 nodes): `TestClassifyDevice`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 409`** (1 nodes): `TestIoTScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 410`** (1 nodes): `TestStackSignature`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 411`** (1 nodes): `TestParsePorts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 412`** (1 nodes): `TestUseCasesResolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 414`** (2 nodes): `Each encryption uses a fresh ephemeral key, so blobs are different.`, `TestEncryptDecryptRoundtrip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 417`** (1 nodes): `TestSubmitResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 431`** (1 nodes): `TestClassify`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 433`** (2 nodes): `The neighbour cache is system-wide. Pinging en0 and then harvesting every     in`, `TestInterfaceScoping`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 436`** (1 nodes): `TestTtlInference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 439`** (1 nodes): `TestTargetsInExcludes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 441`** (2 nodes): `The freshness check reads the STATE FILE but requests authenticate with`, `TestDeviceEnrollment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 456`** (2 nodes): `ssh_collector.py — credentialed (authenticated) inventory collection for Linux.`, `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 468`** (1 nodes): `WindowsCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 471`** (1 nodes): `TestKerberoastChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 474`** (1 nodes): `test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 478`** (1 nodes): `TestProvenance`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 480`** (2 nodes): `ipv6_discovery reports on the RUN (its target is an interface name, or         t`, `TestEngineSummary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 481`** (1 nodes): `TestTuningFromParams`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 485`** (1 nodes): `test_run_all_reconcile.py — cross-cutting: run_all and scan_funnel must derive t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 487`** (1 nodes): `TestBuildResultsEnrichment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 509`** (2 nodes): `CliProgressView`, `Renders campaign progress to a stream. On a TTY it re-draws one live block     i`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 512`** (1 nodes): `TestBloodHoundCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 513`** (1 nodes): `TestDeceptionScore`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 514`** (1 nodes): `test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 516`** (1 nodes): `TestDiscoverFiltering`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 517`** (1 nodes): `TestProfiles`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 518`** (2 nodes): `FIX 5(b): don't tie an obvious workstation; require role ports/DomainRole     fo`, `TestWorkstationVsServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 519`** (1 nodes): `TestAcceptEchoReply`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 521`** (1 nodes): `TestMergeExclusions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 542`** (2 nodes): `Preferred scheme first, the other as a fallback: a scheme guess must         nev`, `WebScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 544`** (1 nodes): `TestNTLMRelayChecker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 546`** (1 nodes): `TestVulnDB`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 547`** (1 nodes): `TestDeriveZones`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 548`** (2 nodes): `A socket whose connect() fails for `dead_family`, succeeds otherwise.`, `TestSmbNegotiateFallback`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 551`** (2 nodes): `Phase 1: combined scope validation (validate + excludes).`, `TestScopeValidationPipeline`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 552`** (2 nodes): `Phase 2: WebSocket message parsing.`, `TestWebSocketMessageProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 554`** (1 nodes): `test_main_scripts_device_ties.py — Phase 23: device classification never resolve`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 555`** (2 nodes): `test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti`, `TestNmapEntityGuard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 556`** (1 nodes): `test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.  T`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 557`** (1 nodes): `TestClamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 558`** (1 nodes): `TestEngagementModes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 562`** (1 nodes): `TestFetchEngagementScope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 563`** (1 nodes): `TestValidateEnv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 564`** (1 nodes): `TestParseHttpHead`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 565`** (1 nodes): `TestSMBEnumScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 566`** (1 nodes): `TestSMBLDAPFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 567`** (1 nodes): `TestOptionParsing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 568`** (1 nodes): `TestAssessTarpit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 571`** (2 nodes): `Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs.`, `TestChooseSourcePort`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 595`** (2 nodes): `_claim_fixture()`, `TestAtomicWebSocketClaim`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 596`** (1 nodes): `TestTenantWebSocketSelection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 597`** (1 nodes): `TestGetAgentJobs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 598`** (1 nodes): `TestIngestParse`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 599`** (1 nodes): `TestMirrorAge`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 600`** (1 nodes): `TestDNSFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 601`** (1 nodes): `TestDNSScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 603`** (1 nodes): `TestFTPFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 604`** (1 nodes): `TestFTPScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 605`** (1 nodes): `TestCheckHwBind`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 606`** (2 nodes): `Phase 1: result spool with upload retry.`, `TestResultSpoolWithRetry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 608`** (1 nodes): `TestMSRPCScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 609`** (1 nodes): `test_nmap_wrapper.py — the "nmap returned 0 while native scanners saw ports" bug`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 610`** (1 nodes): `TestCliOnlineFlag`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 611`** (1 nodes): `TestIcmpParse`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 612`** (1 nodes): `TestIcmpTimestamps`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 613`** (1 nodes): `TestGate2`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 614`** (1 nodes): `TestLooksLikeHttp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 615`** (1 nodes): `TestLooksLikeTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 616`** (1 nodes): `TestResolveScanType`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 617`** (1 nodes): `TestTargets`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 619`** (1 nodes): `TestRsyncFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 620`** (1 nodes): `TestSMTPFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 621`** (1 nodes): `TestSSHFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 622`** (1 nodes): `TestVerifyReplyCookie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 623`** (1 nodes): `TestPortScannerTarpitFlag`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 624`** (2 nodes): `The drift that used to exist: spec allows a port the gate refuses.`, `TestSingleSourceOfTruth`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 625`** (1 nodes): `TestVNCFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 626`** (2 nodes): `Evasion: blur a fixed scan cadence with a bounded random per-probe delay.`, `TestJitteredDelay`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 640`** (1 nodes): `SSHCollector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 643`** (1 nodes): `TestIPMIFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 644`** (1 nodes): `TestIPMIScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 645`** (1 nodes): `TestMSRPCFindings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 646`** (1 nodes): `TestTimestampFallback`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 647`** (1 nodes): `TestPrinterScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 648`** (1 nodes): `TestGate0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 649`** (1 nodes): `TestGate3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 650`** (1 nodes): `TestGate4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 651`** (1 nodes): `TestRateLimiter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 652`** (1 nodes): `TestRouteBranches`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 653`** (1 nodes): `TestScanResult`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 655`** (1 nodes): `TestPositiveTls`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 656`** (1 nodes): `TestStructuredService`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 657`** (1 nodes): `TestRsyncScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 658`** (1 nodes): `Product-boundary tests for the single-dashboard Manager API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 659`** (1 nodes): `TestSMTPScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 661`** (1 nodes): `TestVNCScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 662`** (1 nodes): `Add is_active to users and tenants; add password_expires_at to users.  All exist`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 663`** (1 nodes): `Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 664`** (1 nodes): `Finding verification verdict columns (P2 passive verification).  Revision ID: 00`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 665`** (1 nodes): `Approval-gated safe active-validation requests (P3).  Revision ID: 0022 Revises:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 666`** (1 nodes): `Client portal slug — the customer's stable 'user as domain' handle.  Adds users.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 667`** (1 nodes): `Scan-request targets + intensity — the rich customer scan request.  Adds two nul`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 668`** (1 nodes): `Remediation plans — cached, OS-specific, structured remediation for a finding.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 669`** (1 nodes): `SLA policies — per-tenant custom remediation windows (hours per severity).  One`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 670`** (1 nodes): `Integrations — per-tenant notification config (email / Slack / Jira).  One row p`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 671`** (1 nodes): `Finding lifecycle audit trail — append-only per-finding event log.  One row per`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 684`** (2 nodes): `Gentle second look at ports that stayed silent through the main sweep.`, `Gentle second look at ports that stayed silent through the main sweep.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 705`** (2 nodes): `Gentle second look at ports that stayed silent through the main sweep.`, `Gentle second look at ports that stayed silent through the main sweep.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 714`** (1 nodes): `TestJobSecretBoundary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 715`** (1 nodes): `TestAssetMergeCredentialed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 716`** (1 nodes): `TestAssetMergeHostDiscovery`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 717`** (1 nodes): `TestAssetMergePortScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 718`** (1 nodes): `TestAssetOpenPortsForDeepScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 720`** (2 nodes): `build()`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 721`** (2 nodes): `Collapse every trace for one rule into a single verdict + reason strings.     Pr`, `verdict_for_rule()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 722`** (2 nodes): `Engagement-level coverage roll-up over a set of traces. `rules_blind > 0`     is`, `summarize_traces()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 723`** (2 nodes): `Fires on EITHER of the rdp_scanner's two independent probes.      The scanner pr`, `_rdp_no_nla()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 724`** (2 nodes): `The server REFUSED a TLS-capable negotiation, so the session falls back to     l`, `_rdp_no_tls()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 725`** (2 nodes): `VNC type 2 is the legacy DES-based challenge with an 8-character password     ce`, `_vnc_weak_auth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 734`** (1 nodes): `TestAssetMergePassiveCollect`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 735`** (1 nodes): `TestAssetMergeServiceBanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 736`** (1 nodes): `TestAssetMergeSmbScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 737`** (1 nodes): `TestAssetMergeTlsScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 738`** (1 nodes): `TestAssetMergeUnknownScanner`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 739`** (1 nodes): `TestAssetMergeWebScan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 741`** (1 nodes): `Fast port discovery with naabu. Feeds port list to Nmap.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 742`** (1 nodes): `Nmap service enumeration. Accepts port list from Naabu.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 743`** (1 nodes): `Nuclei vulnerability scan — production-ready.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 744`** (1 nodes): `Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 745`** (1 nodes): `NetExec SMB validation: signing, null sessions, SMBv1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 746`** (1 nodes): `testssl.sh TLS/SSL analysis.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 747`** (1 nodes): `Extract HTTP/HTTPS URLs from nmap XML output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 748`** (1 nodes): `EyeWitness screenshot evidence collection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 749`** (1 nodes): `Safe lateral movement checks — no actual exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 750`** (1 nodes): `Cloud infrastructure scan (AWS/Azure/GCP).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 751`** (1 nodes): `Read a KV-v2 secret from Vault.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 752`** (1 nodes): `Verify the Python probe can open what the TypeScript manager sealed (T14 interop`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 753`** (1 nodes): `Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 754`** (1 nodes): `Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 755`** (1 nodes): `End-to-end probe test: real probe process ↔ reference mock manager over HTTPS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 756`** (1 nodes): `Deterministic stand-ins emitting realistic output for 127.0.0.1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 757`** (1 nodes): `Make a per-host scanner instance share ONE rate limiter + semaphore with all`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 758`** (1 nodes): `Make a raw banner safe and readable for the summary line.      Many services ans`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 759`** (1 nodes): `# NOTE: credentialed collectors (ssh_collector, windows_collector) are run`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 760`** (1 nodes): `ThreadingHTTPServer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FindingSeverity` connect `Community 9` to `Community 5`, `Community 304`, `Community 204`, `Community 189`, `Community 230`, `Community 2`, `Community 73`, `Community 137`, `Community 262`, `Community 371`, `Community 512`, `Community 471`, `Community 544`, `Community 4`, `Community 31`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `Transport` connect `Community 62` to `Community 22`, `Community 280`, `Community 192`, `Community 191`, `Community 158`, `Community 178`, `Community 422`, `Community 207`, `Community 232`, `Community 362`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `FindingStatus` connect `Community 9` to `Community 5`, `Community 73`, `Community 320`, `Community 204`, `Community 371`, `Community 262`, `Community 512`, `Community 230`, `Community 471`, `Community 544`, `Community 4`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 173 inferred relationships involving `FindingSeverity` (e.g. with `ADCSChecker` and `CertTemplate`) actually correct?**
  _`FindingSeverity` has 173 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Rule`, `vedha_ref.evidence_store -- the layer the whole strategy rests on.  Thesis under`, `Cluster observations into assets using fingerprint keys.      Strong keys merge` to the rest of the system?**
  _3995 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.009650237725368356 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.012141618202224263 - nodes in this community are weakly interconnected._