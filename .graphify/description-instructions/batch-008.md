# Node Description Batch 9 of 104

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

- "routers_engagements_rationale_97": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_exploits_rationale_1": "Exploit validation API.  POST /exploits/run              — request exploit valid" | kind=entity | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_exploits_rationale_456": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L456 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_vuln_scans": "vuln_scans.py" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, dependencies.py, FindingImport, import_findings(), launch_nessus_scan(), launch_nuclei_scan()]
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "routers_vuln_scans_rationale_272": "Background task: run nuclei, persist findings, trigger enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L272 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_nmap": "nmap.go" | kind=code-symbol | source=probe-go/scanner/nmap.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, joinInts(), NmapAvailable(), parseNmapXML(), RunNmapVersion(), nmapAddr]
- "tests_test_ad_assessment": "test_ad_assessment.py" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _enum_with_entries(), _FakeAttr, _FakeEntry, TestADCSChecker, TestASREPRoastChecker]
- "tests_test_ad_assessment_rationale_1": "Unit tests for the Active Directory assessment module (Prompt 5).  All directory" | kind=entity | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker, ACE]
- "tests_test_agents": "test_agents.py" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, TestAccessTokenExpiry, TestAgentExecutableTypes, TestEnqueueAgentJob, TestGetAgentJobs]
- "tests_test_agents_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L22 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_rejects_server_side_type(), .test_success_creates_pending_job(), .test_lists_with_online_flag(), .test_allows_passive_discovery_on_ot_en…]
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=probe/tests/test_transport.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, transport.py, TestFetchScope, TestHeartbeat, TestHttpGet, TestIdentity]
- "tests_test_xml_parser_testnmapxmlparser": "TestNmapXMLParser" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L42 | neighbors=[test_xml_parser.py, NmapXMLParser, .setup_method(), .test_cpe_extraction(), .test_empty_scan(), .test_empty_string()]
- "tools_installer_installtool": "installTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L156 | neighbors=[tools.ts, installer.ts, installAll(), downloadFile(), extract(), getInstalledRecord()]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L224 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_output": "output()" | kind=code-symbol | source=probe/agent/cli.py:L175 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()]
- "agent_license": "license.py" | kind=code-symbol | source=probe/agent/license.py:L1 | neighbors=[agent.py, _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError]
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()]
- "auth_router": "router.py" | kind=code-symbol | source=manager/backend/app/auth/router.py:L1 | neighbors=[database.py, dependencies.py, ratelimit.py, create_personal_access_token(), list_personal_access_tokens(), login()]
- "basescanner": "BaseScanner" | kind=code-symbol | neighbors=[DBScanner, HostDiscoveryScanner, _ConnectSweep, MCPAIScanner, PortScanner, ServiceBannerScanner]
- "commands_interactive_divider": "divider()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L112 | neighbors=[interactive.ts, ln(), mainMenu(), wizardAdmin(), wizardAsk(), wizardEngagement()]
- "detection_edr_crowdstrikefalcon": "CrowdStrikeFalcon" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L91 | neighbors=[edr.py, .parse_response(), .query_detections(), EDRQueryEngine, Falcon: query detection IDs then fetch …, Unit tests for the detection validation…]
- "detection_edr_microsoftdefender": "MicrosoftDefender" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L140 | neighbors=[edr.py, EDRQueryEngine, .parse_response(), .query_detections(), Microsoft Defender via the Graph Securi…, Unit tests for the detection validation…]
- "detection_edr_sentinelone": "SentinelOne" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L186 | neighbors=[edr.py, SentinelOne via the REST ``/web/api/v2.…, EDRQueryEngine, .parse_response(), .query_detections(), Unit tests for the detection validation…]
- "detection_engine_ai_normalizer_ainormalizercache": "AINormalizerCache" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L139 | neighbors=[ai_normalizer.py, .get(), ._key(), .__post_init__(), .put(), CPECandidate]
- "detection_engine_ingest": "ingest.py" | kind=code-symbol | source=manager/detection_engine/ingest.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, _classify_confidence(), _extract_aliases(), ingest_file(), ingest_files()]
- "discovery_worker_rationale_1": "DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner" | kind=entity | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[RateLimiter, ServiceIdentifier, worker.py, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_worker_rationale_58": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L58 | neighbors=[RateLimiter, ServiceIdentifier, DiscoveryWorker, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L41 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, xml_parser.py, .parse()]
- "engine_tool_runners_runnmapnse": "runNmapNse()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L991 | neighbors=[tool-runners.ts, runLdapEnum(), runNetbiosEnum(), runNfsEnum(), bin(), collectProcess()]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, GET, POST(), VALID_SEVERITIES, adapters.ts]
- "launch_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L1 | neighbors=[0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, INTENSITY_PRESETS, LaunchBody, POST, SshCreds]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[index.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode]
- "models_detection_run_detectionrun": "DetectionRun" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L40 | neighbors=[engine_bridge.py — run the deterministi…, New raw-facts path: detect CVE findings…, Background entry point (P1: keep detect…, (content_hash, fetched_at) of the pinne…, facts (ScanResult dicts) -> detection_e…, detection_run.py]
- "routers_agents_rationale_1": "Agent registration, heartbeat, job polling, and result submission." | kind=entity | source=manager/backend/app/routers/agents.py:L1 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_208": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L208 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_246": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L246 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_265": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L265 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_459": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L459 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_detection_rationale_1": "Detection validation API (DetectionValidationAPI).  POST /engagements/{id}/detec" | kind=entity | source=manager/backend/app/routers/detection.py:L1 | neighbors=[AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult, Engagement]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-008.json

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
