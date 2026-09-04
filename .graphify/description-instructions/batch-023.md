# Node Description Batch 24 of 330

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

- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[buildFindingsCommand(), Severity, getAllFindings(), getFindingById(), d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1275 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@32feef6ad967e9b67c9439acb1b2eba507d8b4df": "32feef6 feat(engagement): enhance engagement metrics styling for better readabi…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@63d9c9a1c0afc8ba6edd5701b9603fba06b657a3": "63d9c9a fix(probe): recover from 409 when device key already enrolled" | kind=Commit | source=git | neighbors=[agent.py, transport.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@78d51c5a8c9d6aaa3dabfd5ae21632e736865ea3": "78d51c5 opsec(scanner): de-sign service_enum UA — completes the sweep (task C6)" | kind=Commit | source=git | neighbors=[185e648 docs: pending-work inventory (b…, addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9b61c190ebbb02cde565390ea54bf2a5c806df8e": "9b61c19 feat(ui): improve engagement toolbar and metric card animations for enh…" | kind=Commit | source=git | neighbors=[32feef6 feat(engagement): enhance engag…, addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "customer_access_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, 7a637eb feat: network VA accuracy, KEV …, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…, RefreshButton.tsx, RefreshButton()]
- "cve_weakness_map": "weakness_map.py" | kind=code-symbol | source=probe/cve/weakness_map.py:L1 | neighbors=[6e2818f Add support for additional serv…, _Assoc, correlate_weaknesses(), _finding_view(), _has_version(), _mirror_cve()]
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender]
- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient]
- "detection_engine_enrichment_db": "enrichment_db.py" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _cache_key(), _clear_caches(), EpssDB, KevDB]
- "detection_engine_ingest_ingest_file": "ingest_file()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L125 | neighbors=[ingest.py, _classify_confidence(), _extract_aliases(), IngestResult, .get_or_create_asset(), QuarantinedLine]
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()]
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert]
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()]
- "exploit_orchestrator_rationale_104": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L104 | neighbors=[.validate_safety(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_111": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L111 | neighbors=[.validate_scope(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_131": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L131 | neighbors=[.execute(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_253": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L253 | neighbors=[.generate_dns_callback_token(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_266": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L266 | neighbors=[._check_blast_radius(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_297": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L297 | neighbors=[._check_approval_required(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_43": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L43 | neighbors=[ExploitOrchestrator, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_68": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L68 | neighbors=[.select_exploit(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "fleet_fleetjobs": "FleetJobs.tsx" | kind=code-symbol | source=manager/frontend/app/fleet/FleetJobs.tsx:L1 | neighbors=[page.tsx, 07ba102 feat: enhance UI UX and detecti…, 25c014d feat: enhance campaign progress…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fetchJson()]
- "hooks_usetoast_usetoast": "useToast()" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L6 | neighbors=[EngagementStatusControl.tsx, page.tsx, page.tsx, page.tsx, page.tsx, useToast.ts]
- "lib_httpx_parser": "httpx-parser.ts" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber()]
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw, NaabuResult]
- "lib_portal_client_portalapi": "portalApi()" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L8 | neighbors=[page.tsx, page.tsx, page.tsx, console-source.tsx, portal-client.ts, page.tsx]
- "lib_portal_client_useportalengagement": "usePortalEngagement()" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L148 | neighbors=[page.tsx, page.tsx, page.tsx, portal-client.ts, page.tsx, PortalShell.tsx]
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, getClientBySubdomain(), clientFromRequest(), currentClient(), readTenantSubdomain()]
- "main_scripts_accuracy": "accuracy.py" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "main_scripts_dns_scanner_dnsscanner": "DNSScanner" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L88 | neighbors=[dns_scanner.py, BaseScanner, ._axfr(), ._chaos_txt(), ._dnssec_present(), .__init__()]
- "main_scripts_nfs_scanner_nfsscanner": "NFSScanner" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L187 | neighbors=[nfs_scanner.py, BaseScanner, .__init__(), ._mount_export(), ._portmap_dump(), ._portmap_getport()]
- "main_scripts_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L224 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), match_stack_signature(), ._icmp_scan_target(), ._tcp_ttl_result()]
- "main_scripts_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L602 | neighbors=[PortScanner, ._is_ambiguous(), ._reprobe_ambiguous(), ScanMetrics, .record(), .summary()]
- "main_scripts_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 8f6bf49 Refactor code structure and rem…, build_connection_request(), main(), parse_connection_confirm()]
- "main_scripts_smb_scanner_ntlm_os_build": "ntlm_os_build()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L337 | neighbors=[smb_scanner.py, build_ntlmssp_negotiate(), _netbios_session(), parse_ntlm_challenge(), _recv_smb_frame(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "main_scripts_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _fetch(), main()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-023.json

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
