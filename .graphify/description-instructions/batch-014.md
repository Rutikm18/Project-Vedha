# Node Description Batch 15 of 330

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@00c6648b4d38308e37ce245514b25f99cb5b3ae9": "00c6648 feat(settings): editable email/Slack/Jira integrations wired to backend…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@64e8290422a4d984a2428bb30ee728d3b5f8f2c4": "64e8290 feat(campaign): implement VA campaign progress endpoint and UI integrat…" | kind=Commit | source=git | neighbors=[26ea68c Add comprehensive tests for OS …, addcapabilities-fable, main, ui-ux-backend-updates0109, route.ts, 25c014d feat: enhance campaign progress…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bc08715ed9a3be7d600b4595a6872f649784fd00": "bc08715 feat(agent): risk-tier action classification (fail-closed)" | kind=Commit | source=git | neighbors=[3569103 docs(agent): research + design …, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@ecbb4adbc9733f25281faa5986dbcfdc1e7520ae": "ecbb4ad feat(agent): rules-of-engagement policy evaluation (verdict-vs-action, …" | kind=Commit | source=git | neighbors=[bc08715 feat(agent): risk-tier action c…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "components_toastprovider": "ToastProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L1 | neighbors=[layout.tsx, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, Toast]
- "cve_vulndb_vulndb": "VulnDB" | kind=code-symbol | source=probe/cve/vulndb.py:L62 | neighbors=[vulndb.py, .add_cpe_match(), .close(), .commit(), .counts(), .cves_for_cpe()]
- "discovery_finding_translator": "finding_translator.py" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_probe_result(), create_scan_health_finding()]
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, ManagerAiResponse, POST(), assistant.ts]
- "hooks_usetoast": "useToast.ts" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, EngagementStatusControl.tsx, page.tsx, page.tsx, page.tsx, page.tsx]
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), OtpEntry, otpStore, OtpVerifyResult]
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, counters, generateFindingId(), resetCounters()]
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, countBySeverity(), NucleiMatch, nucleiMatchToFinding()]
- "main_scripts_ipv6_discovery": "ipv6_discovery.py" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, discover_ipv6_hosts(), _is_ipv6(), main()]
- "main_scripts_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, _have_nmap(), main(), NmapExecutionError]
- "main_scripts_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, build_default_funnel(), _candidate_ports(), FunnelResult]
- "main_scripts_service_banner": "service_banner.py" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…]
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, str, Base, TimestampMixin, AgentRegisterRequest, AgentRegisterResponse]
- "native_http_probe": "http-probe.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractTitle(), fingerprint(), HttpProbeResult]
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L201 | neighbors=[agents.py, BaseModel, bootstrap_agent(), register_agent(), Asset, Engagement]
- "routers_agents_encrypt_scope_for_agent": "_encrypt_scope_for_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L536 | neighbors=[agents.py, enqueue_agent_job(), get_agent_jobs(), Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…]
- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L302 | neighbors=[agents.py, BaseModel, ._validate_intensity(), ._validate_uc(), Asset, Engagement]
- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L46 | neighbors=[ai_report.py, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath]
- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L56 | neighbors=[ai_report.py, ReviewRequest, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath]
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L86 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L69 | neighbors=[exploits.py, BaseModel, _result_out(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_remediation": "remediation.py" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, dependencies.py]
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[vuln_scans.py, Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "routers_vuln_scans_rationale_279": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L279 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_ipv6_discovery": "ipv6_discovery.py" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, discover_ipv6_hosts(), _is_ipv6(), main()]
- "scanner_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L353 | neighbors=[os_fingerprint.py, BaseScanner, ._apply_smb_build(), ._icmp_echo_ttl(), ._icmp_scan_target(), ._icmp_timestamp()]
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L315 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "scanner_ssh_scanner": "ssh_scanner.py" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _Cursor, _dedup(), evaluate_algorithms(), main()]
- "states_datastate_skeletonrows": "SkeletonRows()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L26 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx]
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, .__init__(), .__getitem__(), ADCSChecker, CertTemplate, ASREPRoastChecker]
- "tests_test_agent_policy_roe": "_roe()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L30 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…]
- "tests_test_agent_policy_testevaluateaction": "TestEvaluateAction" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L36 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…]
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, .setup_method(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_fallback_score_capped(), .test_higher_cvss_scores_higher()]
- "tests_test_customer_access": "test_customer_access.py" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, _added(), _mock_db(), _operator()]
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, .skip_without_flag(), .test_connect_and_list_modules(), .test_run_safe_scanner_smb(), MetasploitRPCClient]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-014.json

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
