# Node Description Batch 28 of 380

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

- "exploit_orchestrator_rationale_43": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L43 | neighbors=[ExploitOrchestrator, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_68": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L68 | neighbors=[.select_exploit(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "hooks_usetoast_usetoast": "useToast()" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L6 | neighbors=[EngagementStatusControl.tsx, page.tsx, page.tsx, page.tsx, page.tsx, useToast.ts]
- "lib_adapters_touiengagement": "toUiEngagement()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L37 | neighbors=[route.ts, route.ts, adapters.ts, engStatusToUi(), aibrain-workspace-api.ts, campaign-workspace-api.ts]
- "lib_campaign_workspace_api": "campaign-workspace-api.ts" | kind=code-symbol | source=manager/frontend/lib/campaign-workspace-api.ts:L1 | neighbors=[page.tsx, 198bae4 snapshot: uncommitted system/ui…, adapters.ts, toUiEngagement(), CampaignWorkspaceSurface, createCampaignWorkspaceApi()]
- "lib_httpx_parser": "httpx-parser.ts" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber()]
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw, NaabuResult]
- "lib_portal_client_useportalengagement": "usePortalEngagement()" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L161 | neighbors=[portal-client.ts, page.tsx, page.tsx, page.tsx, page.tsx, PortalShell.tsx]
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, getClientBySubdomain(), clientFromRequest(), currentClient(), readTenantSubdomain()]
- "main_scripts_accuracy": "accuracy.py" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "main_scripts_dns_scanner_dnsscanner": "DNSScanner" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L88 | neighbors=[dns_scanner.py, BaseScanner, ._axfr(), ._chaos_txt(), ._dnssec_present(), .__init__()]
- "main_scripts_nfs_scanner_nfsscanner": "NFSScanner" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L187 | neighbors=[nfs_scanner.py, BaseScanner, .__init__(), ._mount_export(), ._portmap_dump(), ._portmap_getport()]
- "main_scripts_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L224 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), match_stack_signature(), ._icmp_scan_target(), ._tcp_ttl_result()]
- "main_scripts_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 8f6bf49 Refactor code structure and rem…, build_connection_request(), main(), parse_connection_confirm()]
- "main_scripts_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1155 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()]
- "main_scripts_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L807 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()]
- "main_scripts_smb_scanner_ntlm_os_build": "ntlm_os_build()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L337 | neighbors=[smb_scanner.py, build_ntlmssp_negotiate(), _netbios_session(), parse_ntlm_challenge(), _recv_smb_frame(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[agent_recommendation.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, TimestampMixin, Per-engagement SIEM + EDR connection se…, Base, TimestampMixin]
- "models_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/models/finding.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 9e5f980 feat(findings): add assigned_to…, d1b4dd3 trim frontend to 7 core pages; …, ddb51f2 feat(resolution): add finding r…]
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()]
- "portal_timestamp_timestamp": "Timestamp()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L79 | neighbors=[Timestamp.tsx, formatCompact(), formatExact(), formatRelative(), isoUtc(), page.tsx]
- "remediation_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, backend.ts, backend(), BackendError]
- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig]
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus]
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus]
- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L256 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_detection_runs": "detection_runs.py" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 7dc9b08 feat(detection): surface NEW fi…, cac022c Everything is done and verified…, dependencies.py, latest_run_delta(), list_detection_runs()]
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L35 | neighbors=[findings.py, finding_timeline(), get_finding(), Fetch a finding scoped to the caller's …, patch_finding(), Fetch a finding scoped to the caller's …]
- "scanner_accuracy": "accuracy.py" | kind=code-symbol | source=probe/scanner/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "scanner_dns_scanner_dnsscanner": "DNSScanner" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L88 | neighbors=[dns_scanner.py, BaseScanner, ._axfr(), ._chaos_txt(), ._dnssec_present(), .__init__()]
- "scanner_nfs_scanner_nfsscanner": "NFSScanner" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L187 | neighbors=[nfs_scanner.py, BaseScanner, .__init__(), ._mount_export(), ._portmap_dump(), ._portmap_getport()]
- "scanner_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L224 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), match_stack_signature(), ._icmp_scan_target(), ._tcp_ttl_result()]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L544 | neighbors=[PortScanner, ._attempt(), ._note_probe_outcome(), One port's terminal result, gated by th…, One port's terminal result, gated by th…, One port's terminal result, gated by th…]
- "scanner_printer_scanner": "printer_scanner.py" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_ipp_get_printer_attributes(), _ipp_attr(), main(), parse_ipp_make_model(), parse_pjl_id()]
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1127 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…]
- "scanner_smb_scanner_ntlm_os_build": "ntlm_os_build()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L337 | neighbors=[smb_scanner.py, build_ntlmssp_negotiate(), _netbios_session(), parse_ntlm_challenge(), _recv_smb_frame(), _smb2_negotiate()]
- "services_job_result_service_process_job_result": "process_job_result()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L172 | neighbors=[job_result_service.py, _promote_assets(), result_checksum(), sanitize_jsonb(), validate_result_scope(), Process a scan job result.  Called from…]
- "services_notifications": "notifications.py" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, f300b2a feat(integrations): ServiceNow …, deliver(), enqueue_notification(), notify_tenant(), _send_email()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-027.json

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
