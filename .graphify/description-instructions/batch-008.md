# Node Description Batch 9 of 227

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_detection_core_testfindingpostinit": "TestFindingPostInit" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L113 | neighbors=[test_detection_core.py, .test_accepts_nonempty_evidence_refs(), .test_refuses_zero_evidence_refs(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testisip": "TestIsIp" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L212 | neighbors=[test_detection_core.py, .test_hostname(), .test_valid_ipv4(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testkevdb": "TestKevDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L838 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_is_kev(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testnormalize": "TestNormalize" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L960 | neighbors=[test_detection_core.py, .test_dispatches_banner(), .test_unknown_scanner_returns_empty(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testnormalizebanner": "TestNormalizeBanner" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L913 | neighbors=[test_detection_core.py, .test_empty_banner(), .test_ssh_banner(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_detection_core_testproductfromcpe": "TestProductFromCpe" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L552 | neighbors=[test_detection_core.py, .test_extracts_product(), .test_short_cpe_returns_cpe(), ConsistencyReport, FindingConsistency, CPECandidate] | lang=en
- "tests_test_exploit_engine_testmetasploitrpcclient": "TestMetasploitRPCClient" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L181 | neighbors=[test_exploit_engine.py, ._make_client(), .test_call_without_connect_raises(), .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit()] | lang=en
- "tests_test_exploit_engine_testrequiresapproval": "TestRequiresApproval" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L153 | neighbors=[test_exploit_engine.py, .test_adcs_server(), .test_critical_asset_needs_approval(), .test_dc02_pattern(), .test_dc_hostname_needs_approval(), .test_exchange_server()] | lang=en
- "tests_test_integration": "test_integration.py" | kind=code-symbol | source=probe/tests/test_integration.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, result_spool.py, scope_crypt.py, scope_validator.py, task_runner.py, transport.py] | lang=en
- "tests_test_new_scanners_testsnmpberutilities": "TestSNMPBerUtilities" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L24 | neighbors=[test_new_scanners.py, .test_ber_len_long_form_one_byte(), .test_ber_len_long_form_two_bytes(), .test_ber_len_short_form(), .test_ber_parse_empty(), .test_ber_parse_two_tlvs()] | lang=en
- "workflow_gates": "gates.py" | kind=code-symbol | source=probe/workflow/gates.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, cdee859 feat(probe): add container/clou…, d1b4dd3 trim frontend to 7 core pages; …, test_port_catalog.py, test_probe_core.py] | lang=en
- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L235 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _finalize_trace(), _gather_per_host(), _port_candidates(), _record()] | lang=en
- "agent_agent_say": "say()" | kind=code-symbol | source=probe/agent/agent.py:L76 | neighbors=[agent.py, _check_anti_debug(), _enroll_device(), _flush_spool_over_http(), _load_or_create_identity(), main()] | lang=en
- "app_layout": "layout.tsx" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L1 | neighbors=[metadata, RootLayout(), AssistantProvider.tsx, AssistantProvider(), QueryProvider.tsx, QueryProvider()] | lang=en
- "auth_exceptions": "exceptions.py" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L1 | neighbors=[AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@58c2d10f572ed4b7fce3da53bb9f95b696c4b94f": "58c2d10 feat(active-validation): ValidationRequest model + migration" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c140451c247068bc76251c851f7936cbeeb8a0ac": "c140451 fix(portal): clean 409 on duplicate-email provision + 7-day session ref…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive, integration/all-branches] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f00ce5fb2e9537f4630e4bf1ff0326b3f6422ffe": "f00ce5f fix(ui): session-timer persistence, hydration-safe count-up, security h…" | kind=Commit | source=git | neighbors=[88c9278 feat(ai): pin manager LLM pipel…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@fbe7450ad544cc4fced845b4b28720d54fe802b9": "fbe7450 Add comprehensive documentation for Playwright CLI features- Introduced…" | kind=Commit | source=git | neighbors=[llm_report.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/remediation-ai-plans, integration/all-branches] | lang=en
- "detection_siem_siemalert": "SIEMAlert" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L24 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response(), AttackAction, DetectionCorrelator] | lang=en
- "detection_sigma_sigmarulegenerator": "SigmaRuleGenerator" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L107 | neighbors=[sigma.py, ._customise_detection(), .generate_sigma_for_technique(), ._lookup_template(), AttackAction, DetectionCorrelator] | lang=en
- "discovery_service_id_servicefingerprint": "ServiceFingerprint" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L13 | neighbors=[service_id.py, .identify(), NucleiRunReport, NucleiScanError, NucleiScanner, NucleiScanner — async subprocess wrappe…] | lang=en
- "graph_analyzer_pathanalyzer": "PathAnalyzer" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L60 | neighbors=[analyzer.py, ._exploit_info(), .find_blast_radius(), .find_paths_to_target(), .identify_chokepoints(), .__init__()] | lang=en
- "lib_exploit_store": "exploit-store.ts" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest] | lang=en
- "main_scripts_findings_finding": "Finding" | kind=code-symbol | source=probe/main_scripts/findings.py:L63 | neighbors=[findings.py, _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay(), .to_dict(), One vulnerability finding, always backe…] | lang=en
- "main_scripts_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, 4d0377d Add unit tests for SMB scanner,…, device_hint(), fuse_liveness(), HostDiscoveryScanner, is_locally_administered()] | lang=en
- "models_attack_path_attackpath": "AttackPath" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L11 | neighbors=[attack_path.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…] | lang=en
- "models_detection_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/backend/app/models/detection.py:L12 | neighbors=[detection.py, Base, TimestampMixin, Base, TimestampMixin, DetectionStatus] | lang=en
- "native_port_scan": "port-scan.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, CheckOpts, checkPort(), expandTarget()] | lang=en
- "portal_portalshell": "PortalShell.tsx" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L1 | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, c52feb4 feat(portal): reskin User Porta…, f8ff229 feat(ui): remove decorative ses…, page.tsx, page.tsx, ThemeProvider.tsx] | lang=en
- "routers_engagements_engagementupdate": "EngagementUpdate" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L483 | neighbors=[engagements.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), Asset] | lang=en
- "scanner_findings_finding": "Finding" | kind=code-symbol | source=probe/scanner/findings.py:L63 | neighbors=[findings.py, _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay(), .to_dict(), One vulnerability finding, always backe…] | lang=en
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 95904f1 feat(probe): detect SMB signing…, d1b4dd3 trim frontend to 7 core pages; …, main()] | lang=en
- "schemas_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…, ClientEngagementOut, ClientFindingOut] | lang=en
- "tests_test_ai_engine_testhallucinationguard": "TestHallucinationGuard" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L104 | neighbors=[test_ai_engine.py, .setup_method(), .test_cve_all_known_valid(), .test_cve_invention_flagged(), .test_cvss_match_passes(), .test_cvss_mismatch_flagged()] | lang=en
- "tests_test_attack_paths_testgraphbuilder": "TestGraphBuilder" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L52 | neighbors=[test_attack_paths.py, .test_asset_node_attributes(), .test_connects_to_and_same_segment_edge…, .test_credential_reuse_edges(), .test_exploit_complexity_falls_back_to_…, .test_exploit_complexity_from_vector()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-008.json

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
