# Node Description Batch 1 of 134

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@d1b4dd3ee73bfd2dd10b7d9b682b5e3cb4d2f7d5": "d1b4dd3 trim frontend to 7 core pages; add use-case library, scope re-validatio…" | kind=Commit | source=git | neighbors=[0510df3 going to build prompt and conne…, adcs.py, asreproast.py, bloodhound.py, findings.py, __init__.py]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@298a9d489c8ecbabc70d474cce518d1295aa66cd": "298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validatio…" | kind=Commit | source=git | neighbors=[0510df3 going to build prompt and conne…, adcs.py, asreproast.py, bloodhound.py, findings.py, __init__.py]
- "models_enums_findingseverity": "FindingSeverity" | kind=code-symbol | source=manager/backend/app/models/enums.py:L35 | neighbors=[enums.py, str, ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@10dfc80b4b96bacfbdc8a5d3116907e88c9e25ab": "10dfc80 Add comprehensive probe testing guide with step-by-step instructions- D…" | kind=Commit | source=git | neighbors=[route.ts, agent.py, cli.py, engine.py, hw_bind.py, __init__.py]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@2885afab48ed2cf48cc14de457e9730f9d14b08b": "2885afa Add comprehensive probe testing guide with step-by-step instructions- D…" | kind=Commit | source=git | neighbors=[0557559 scanner: real use-case library,…, route.ts, agent.py, cli.py, engine.py, hw_bind.py]
- "models_enums_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L43 | neighbors=[enums.py, str, ADConnectionError, ADError, DependencyMissingError, Shared building blocks for the Active D…]
- "models_engagement_engagement": "Engagement" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L12 | neighbors=[engagement.py, Base, TimestampMixin, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "models_finding_finding": "Finding" | kind=code-symbol | source=manager/backend/app/models/finding.py:L13 | neighbors=[finding.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "models_asset_asset": "Asset" | kind=code-symbol | source=manager/backend/app/models/asset.py:L12 | neighbors=[asset.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1fe16c8ae308d129d848d84656ca57d9ac472939": "1fe16c8 stable but some dead code, need to optimize" | kind=Commit | source=git | neighbors=[route.ts, agent.py, cli.py, engine.py, scope_validator.py, task_runner.py]
- "models_scan_job_scanjob": "ScanJob" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L12 | neighbors=[scan_job.py, Base, TimestampMixin, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …]
- "commands_interactive": "interactive.ts" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1 | neighbors=[agent.py, auth.ts, apiFetch(), clearSession(), loadSession(), requireAuth()]
- "engine_tool_runners": "tool-runners.ts" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, bin(), binName()]
- "models_service_service": "Service" | kind=code-symbol | source=manager/backend/app/models/service.py:L10 | neighbors=[service.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "models_enums_scanjobtype": "ScanJobType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L58 | neighbors=[enums.py, str, ScanJob, ADAssessRequest, Neo4jConfig, Active Directory assessment API.  POST …]
- "models_enums_scanjobstatus": "ScanJobStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L69 | neighbors=[enums.py, str, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "detection_engine_models_sourceconfidence": "SourceConfidence" | kind=code-symbol | source=manager/detection_engine/models.py:L24 | neighbors=[models.py, How was this fact obtained? Drives ever…, Enum, str, correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…]
- "findings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 41b692a Update project files, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, AssistantProvider.tsx, useAssistant()]
- "detection_engine_models_fact": "Fact" | kind=code-symbol | source=manager/detection_engine/models.py:L44 | neighbors=[models.py, .ref(), One ScanResult line, carried forward wi…, AIClient, AINormalizerCache, AnthropicAIClient]
- "detection_engine_cpe_normalizer_cpecandidate": "CPECandidate" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L42 | neighbors=[cpe_normalizer.py, .cpe23(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web()]
- "detection_engine_models_finding": "Finding" | kind=code-symbol | source=manager/detection_engine/models.py:L138 | neighbors=[models.py, .__post_init__(), .to_dict(), ConsistencyReport, FindingConsistency, consistency.py — Phase 5: N-run consist…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@b4b12a903b40303ffa76f097396cb121f1b9b16e": "b4b12a9 Rename project and update files" | kind=Commit | source=git | neighbors=[agent.py, engine.py, result_spool.py, scope_crypt.py, task_runner.py, transport.py]
- "models_enums_assettype": "AssetType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L19 | neighbors=[enums.py, str, Convert a probe's self-assessed `findin…, Find the Asset for a probe-reported tar…, A still-relevant Finding with the same …, Convert a probe's self-assessed `findin…]
- "agent_agent": "agent.py" | kind=code-symbol | source=probe/agent/agent.py:L1 | neighbors=[AgentDeps, AgentOpts, _bounded_env_int(), _check_anti_debug(), _enroll_device(), _flush_spool_over_http()]
- "ad_ldap_enum_ldapenumerator": "LDAPEnumerator" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L117 | neighbors=[ldap_enum.py, ._attr(), .check_anonymous_bind(), .connect(), .connection(), .get_aces()]
- "models_scan_result_scanresult": "ScanResult" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L10 | neighbors=[scan_result.py, Append-only raw probe facts (P3-#10).  …, Base, TimestampMixin, Base, TimestampMixin]
- "basemodel": "BaseModel" | kind=code-symbol | neighbors=[ActivityItem, ADAssessRequest, Neo4jConfig, AgentBootstrapRequest, AgentRefreshRequest, AgentRegisterRequest]
- "detection_engine_vuln_db_vulndb": "VulnDB" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L78 | neighbors=[vuln_db.py, load_snapshot(), In-memory index over a loaded snapshot:…, ._build_cve_index(), .covers(), .get_cvss_vector()]
- "tests_test_probe_core": "test_probe_core.py" | kind=code-symbol | source=probe/tests/test_probe_core.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, cac022c Everything is done and verified…, agent.py, engine.py]
- "detection_engine_models_asset": "Asset" | kind=code-symbol | source=manager/detection_engine/models.py:L70 | neighbors=[models.py, .add_alias(), .add_fact(), .as_of(), .facts_by_scanner(), .open_ports()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@b5ffcb044f83b971e79c066de279484edeed94ac": "b5ffcb0 Refactor Vedha probe installer and enhance device identity tests- Updat…" | kind=Commit | source=git | neighbors=[65f22a7 Add comprehensive tests for aut…, agent.py, device_identity.py, engine.py, result_spool.py, task_runner.py]
- "detection_engine_models_findingstate": "FindingState" | kind=code-symbol | source=manager/detection_engine/models.py:L119 | neighbors=[models.py, Enum, str, correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…, SMBv1 enabled + (credentialed hotfix li…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#main": "main" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…, 0f0097b feat(posture): mirror posture s…]
- "exploit_msf_client_metasploitrpcclient": "MetasploitRPCClient" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L27 | neighbors=[msf_client.py, ._call(), .connect(), .disconnect(), .get_job_status(), .__init__()]
- "tests_test_detection_core_finding": "_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L56 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), .test_authoritative_tier4()]
- "reports_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), fetcher.ts]
- "detection_engine_ingest_ingestresult": "IngestResult" | kind=code-symbol | source=manager/detection_engine/ingest.py:L42 | neighbors=[ingest.py, ingest_file(), ingest_files(), .get_or_create_asset(), .__init__(), Asset]
- "detection_engine_enrichment_db_epssdb": "EpssDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L23 | neighbors=[enrichment_db.py, .get(), .__init__(), load_epss(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "detection_engine_enrichment_db_kevdb": "KevDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L14 | neighbors=[enrichment_db.py, .__init__(), .is_kev(), load_kev(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "lib_ai_engine": "ai-engine.ts" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, types.ts, LiveFinding, aiReportStore]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-000.json

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
