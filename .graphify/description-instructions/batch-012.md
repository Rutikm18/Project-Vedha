# Node Description Batch 13 of 330

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@3ad95f45b1a7fcabc284bdb92a99e96a7ed33d57": "3ad95f4 feat: Optimize asset service fetching and enhance password handling- Re…" | kind=Commit | source=git | neighbors=[agent.py, router.py, startup.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65e568441bfb43e313c743db52bd2f65fb7e86fe": "65e5684 feat(probe): transparent job logging (real use-case + result summary)" | kind=Commit | source=git | neighbors=[1af3404 feat(deploy): probe-free manage…, agent.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@6a1c958273a695fdfb8a8e43254742b6436b3b8e": "6a1c958 docs(plans): record execution status for active-validation + risk-rank …" | kind=Commit | source=git | neighbors=[50d6554 feat(active-validation): approv…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@88c92781d5435f80d9b62fb0869cca708fc4920b": "88c9278 feat(ai): pin manager LLM pipeline to Claude Sonnet 4.6" | kind=Commit | source=git | neighbors=[1d5ae94 feat(fleet): live "Connected pr…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@e3958e7d0893279d1784154afd4ac1719633063f": "e3958e7 feat(customers): reveal + copy customer login password from dashboard (…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "detection_engine_ingest": "ingest.py" | kind=code-symbol | source=manager/detection_engine/ingest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, _classify_confidence()]
- "detection_engine_vuln_db": "vuln_db.py" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 4d0377d Add unit tests for SMB scanner,…, d0d1931 feat(detection): NVD/CPE vuln f…, d1b4dd3 trim frontend to 7 core pages; …, _boundary_versions(), _clear_caches()]
- "detection_siem_siemalert": "SIEMAlert" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L24 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response(), AttackAction, DetectionCorrelator]
- "detection_sigma_sigmarulegenerator": "SigmaRuleGenerator" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L107 | neighbors=[sigma.py, ._customise_detection(), .generate_sigma_for_technique(), ._lookup_template(), AttackAction, DetectionCorrelator]
- "discovery_service_id_servicefingerprint": "ServiceFingerprint" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L13 | neighbors=[service_id.py, .identify(), NucleiRunReport, NucleiScanError, NucleiScanner, NucleiScanner — async subprocess wrappe…]
- "graph_analyzer_pathanalyzer": "PathAnalyzer" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L60 | neighbors=[analyzer.py, ._exploit_info(), .find_blast_radius(), .find_paths_to_target(), .identify_chokepoints(), .__init__()]
- "lib_exploit_store": "exploit-store.ts" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest]
- "models_attack_path_attackpath": "AttackPath" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L11 | neighbors=[attack_path.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "models_detection_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/backend/app/models/detection.py:L12 | neighbors=[detection.py, Base, TimestampMixin, Base, TimestampMixin, DetectionStatus]
- "native_port_scan": "port-scan.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, CheckOpts, checkPort(), expandTarget()]
- "routers_agents_agent_ownership_check": "_agent_ownership_check()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L574 | neighbors=[agents.py, get_agent_jobs(), heartbeat(), Verify that the JWT token bearer IS the…, refresh_agent_registration(), submit_job_result()]
- "routers_engagements_engagementupdate": "EngagementUpdate" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L510 | neighbors=[engagements.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), Asset]
- "services_llm": "llm.py" | kind=code-symbol | source=manager/backend/app/services/llm.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, 7a637eb feat: network VA accuracy, KEV …]
- "tests_test_ai_engine_testhallucinationguard": "TestHallucinationGuard" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L104 | neighbors=[test_ai_engine.py, .setup_method(), .test_cve_all_known_valid(), .test_cve_invention_flagged(), .test_cvss_match_passes(), .test_cvss_mismatch_flagged()]
- "tests_test_attack_paths_testgraphbuilder": "TestGraphBuilder" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L52 | neighbors=[test_attack_paths.py, .test_asset_node_attributes(), .test_connects_to_and_same_segment_edge…, .test_credential_reuse_edges(), .test_exploit_complexity_falls_back_to_…, .test_exploit_complexity_from_vector()]
- "tests_test_auth_login": "test_auth_login.py" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, _make_db(), _make_tenant(), _make_user(), TestAuthenticateBcryptFailure]
- "tests_test_detection_core_testcleanrpmversion": "TestCleanRpmVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1057 | neighbors=[test_detection_core.py, .test_strips_release(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testcpecandidatecpe23": "TestCPECandidateCpe23" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L976 | neighbors=[test_detection_core.py, .test_cpe23_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testfactref": "TestFactRef" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L180 | neighbors=[test_detection_core.py, .test_ref_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testfindingtodict": "TestFindingToDict" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L172 | neighbors=[test_detection_core.py, .test_enums_serialized_to_values(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testnormalizeweb": "TestNormalizeWeb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L994 | neighbors=[test_detection_core.py, .test_server_header(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_validation_testsplunkintegration": "TestSplunkIntegration" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L323 | neighbors=[test_detection_validation.py, .skip_without_flag(), .test_live_query(), AttackAction, DetectionCorrelator, DetectionGap]
- "tests_test_exploit_engine": "test_exploit_engine.py" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator]
- "tests_test_exploit_engine_testvalidatemodule": "TestValidateModule" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L103 | neighbors=[test_exploit_engine.py, .test_dos_blocked(), .test_encoder_blocked(), .test_exploit_module_allowed(), .test_fuzzer_blocked(), .test_scanner_module_allowed()]
- "tests_test_exploit_engine_testvalidatescope": "TestValidateScope" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L128 | neighbors=[test_exploit_engine.py, .test_excluded_cidr_takes_priority(), .test_invalid_ip_fails(), .test_ip_in_excluded_fails(), .test_ip_in_scope_passes(), .test_ip_out_of_scope_fails()]
- "tests_test_exploitability_epss": "_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L28 | neighbors=[test_exploitability.py, .test_declared_severity_is_never_rewrit…, .test_idempotent_across_repeated_applic…, .test_kev_raises_the_score_and_priority…, .test_reason_is_recorded_in_notes(), .test_score_is_capped_at_100()]
- "tests_test_exploitability_kev": "_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L24 | neighbors=[test_exploitability.py, .test_declared_severity_is_never_rewrit…, .test_idempotent_across_repeated_applic…, .test_kev_raises_the_score_and_priority…, .test_reason_is_recorded_in_notes(), .test_score_is_capped_at_100()]
- "tests_test_host_health_monitor": "_monitor()" | kind=code-symbol | source=probe/tests/test_host_health.py:L28 | neighbors=[test_host_health.py, .test_cancellation_is_clean(), .test_declares_offline_after_consecutiv…, .test_healthy_host_is_never_marked(), .test_flaky_note_is_not_an_error(), .test_offline_fact_carries_an_error_so_…]
- "tests_test_outbox_reclaim": "test_outbox_reclaim.py" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, _mock_session(), _now(), _sql(), test_boundary_at_exactly_the_lease_is_r…, test_dead_letter_and_requeue_are_mutual…]
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()]
- "workflow_router": "router.py" | kind=code-symbol | source=probe/workflow/router.py:L1 | neighbors=[explain_plan.py, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …, bb0ef3d feat(probe): route DB services …, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…]
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr]
- "agent_agent_main": "main()" | kind=code-symbol | source=probe/agent/agent.py:L273 | neighbors=[agent.py, _bounded_env_int(), _classify_connection_error(), configure_logging(), _dbg(), _is_local_manager_url()]
- "agent_agent_ws_http_poll_fallback": "_ws_http_poll_fallback()" | kind=code-symbol | source=probe/agent/agent.py:L896 | neighbors=[agent.py, Poll pending jobs even while WS is conn…, _run_ws_push_loop(), _flush_spool_over_http(), say(), _ws_run_job()]
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=probe/agent/agent.py:L825 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), _dbg(), _job_intent()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-012.json

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
