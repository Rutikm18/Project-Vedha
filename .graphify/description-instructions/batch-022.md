# Node Description Batch 23 of 209

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "commit:repo:github.com/Rutikm18/Project-Vedha@d2eb44c3d2c1f5ac6a3398dc1bf865c46447a9a8": "d2eb44c feat(posture): add dashboard PatchComparisonMatrix component" | kind=Commit | source=git | neighbors=[aa560a0 feat(posture): add dashboard Po…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 9347a9a feat(posture): surface posture …]
- "commit:repo:github.com/Rutikm18/Project-Vedha@d7329cfe261cfa5fd29d0892344b94340cbe0b77": "d7329cf feat: enhance AWS deployment with new environment variables and scripts…" | kind=Commit | source=git | neighbors=[b5ffcb0 Refactor Vedha probe installer …, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f1da96f64e70aef9d0275a6cdcdbf89b7334e948": "f1da96f fix: update environment variables and resource limits in docker-compose…" | kind=Commit | source=git | neighbors=[2a36f8a fix: update docker compose comm…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3c359163f16baf103a46a5170e40a9e95edda9d": "f3c3591 docs: Phase 0 queue-control implementation plan (8 TDD tasks)" | kind=Commit | source=git | neighbors=[879cdfa docs: probe fleet automation de…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd]
- "detection_engine_ai_normalizer_aiclient": "AIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L88 | neighbors=[ai_normalizer.py, .propose_cpe(), Protocol, CPECandidate, Fact, pipeline.py — Phase 1 + Phase 2 end to …]
- "detection_engine_consistency": "consistency.py" | kind=code-symbol | source=manager/detection_engine/consistency.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, aggregate(), ConsistencyReport, FindingConsistency, format_line(), wilson_ci()]
- "detection_siem_siemqueryengine": "SIEMQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L50 | neighbors=[siem.py, ElasticSIEM, Abstract SIEM connector., SentinelSIEM, .__init__(), .query_alerts()]
- "detection_verification": "verification.py" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, de2d1c9 feat(verification): optional fa…, compute_verdict(), _int_confidence(), _qualifies_for_llm(), VerificationVerdict]
- "discovery_xml_parser_parsedhost": "ParsedHost" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L24 | neighbors=[xml_parser.py, ._parse_host(), .open_ports(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …]
- "enum": "Enum" | kind=code-symbol | neighbors=[models.py, FindingState, SourceConfidence, verifier.py, agent.py, enums.py]
- "frontend_proxy": "proxy.ts" | kind=code-symbol | source=manager/frontend/proxy.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES]
- "lib_adapters_touifinding": "toUiFinding()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L112 | neighbors=[route.ts, route.ts, adapters.ts, evidenceToUi(), severityToPriority(), security-context.ts]
- "lib_job_store_readjobs": "readJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L25 | neighbors=[job-store.ts, createJob(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), markDispatched()]
- "lib_tenant": "tenant.ts" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, proxy.ts, RESERVED, resolveTenantSubdomain(), rootDomain(), subdomainFromHost()]
- "main_scripts_service_banner": "service_banner.py" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, _dec(), main(), match_service(), ServiceBannerScanner]
- "main_scripts_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()]
- "main_scripts_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L308 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()]
- "main_scripts_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L86 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()]
- "main_scripts_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "models_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/models/finding.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, ddb51f2 feat(resolution): add finding r…, Finding]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 58c2d10 feat(active-validation): Valida…, 81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …]
- "routers_attack_paths_rationale_1": "Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path" | kind=entity | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[attack_paths.py, PathAnalyzer, GraphBuilder, GraphVisualizer, Asset, AttackPath]
- "routers_detection_runs": "detection_runs.py" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, cac022c Everything is done and verified…, dependencies.py, latest_run_delta(), list_detection_runs(), _run_dict()]
- "routers_probe_enrollment_create_enrollment_request": "create_enrollment_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L361 | neighbors=[probe_enrollment.py, _decode_public_key(), enroll_token_is_usable(), _get_or_create_auto_enroll_site(), _keyed_hash(), _provision_agent_for_site()]
- "scanner_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()]
- "scanner_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/scanner/port_scanner.py:L251 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._scan_port()]
- "scanner_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L311 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…, One connect() and its classification. A…]
- "scanner_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L516 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…]
- "scanner_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()]
- "scanner_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L308 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()]
- "scanner_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L86 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()]
- "scanner_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/scanner/windows_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "scanner_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/scanner/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "services_job_result_service_promote_assets": "_promote_assets()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L374 | neighbors=[job_result_service.py, process_job_result(), _apply_device_profile(), Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…]
- "services_job_result_service_rationale_1": "job_result_service.py — shared job result processing. Single source of truth for" | kind=entity | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[job_result_service.py, Asset, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_140": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_145": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L145 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_35": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L35 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_llm_runtime": "Runtime" | kind=code-symbol | source=manager/backend/app/services/llm.py:L28 | neighbors=[llm.py, ._default_runtime(), ._fallback_candidates(), ._runtime(), Settings, AiGenerateRequest]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-022.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
