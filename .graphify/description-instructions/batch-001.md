# Node Description Batch 2 of 336

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

- "models_enums_scanjobtype": "ScanJobType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L91 | neighbors=[enums.py, str, ScanJob, ADAssessRequest, Neo4jConfig, Active Directory assessment API.  POST …]
- "models_enums_scanjobstatus": "ScanJobStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L102 | neighbors=[enums.py, str, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "settings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L1 | neighbors=[00c6648 feat(settings): editable email/…, 07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 3c9062a refactor: Update dashboard comp…, 5c6aa54 feat(portal-ui): portal shell/p…]
- "detection_engine_models_sourceconfidence": "SourceConfidence" | kind=code-symbol | source=manager/detection_engine/models.py:L24 | neighbors=[models.py, How was this fact obtained? Drives ever…, Enum, str, correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@b4b12a903b40303ffa76f097396cb121f1b9b16e": "b4b12a9 Rename project and update files" | kind=Commit | source=git | neighbors=[agent.py, engine.py, result_spool.py, scope_crypt.py, task_runner.py, transport.py]
- "workflow_workflow_engine": "workflow_engine.py" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L1 | neighbors=[engine.py, explain_plan.py, local_run.py, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 3ad95f4 feat: Optimize asset service fe…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@26ea68c0a5b57ca977c28a93b7634862d8567e75": "26ea68c Add comprehensive tests for OS identification, reconciliation, and vali…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, main, ui-ux-backend-updates0109, 64e8290 feat(campaign): implement VA ca…, engine_bridge.py, pipeline.py]
- "detection_engine_models_fact": "Fact" | kind=code-symbol | source=manager/detection_engine/models.py:L44 | neighbors=[models.py, .ref(), One ScanResult line, carried forward wi…, AIClient, AINormalizerCache, AnthropicAIClient]
- "detection_engine_cpe_normalizer_cpecandidate": "CPECandidate" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L42 | neighbors=[cpe_normalizer.py, .cpe23(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@b5ffcb044f83b971e79c066de279484edeed94ac": "b5ffcb0 Refactor Vedha probe installer and enhance device identity tests- Updat…" | kind=Commit | source=git | neighbors=[65f22a7 Add comprehensive tests for aut…, agent.py, device_identity.py, engine.py, result_spool.py, task_runner.py]
- "detection_engine_models_finding": "Finding" | kind=code-symbol | source=manager/detection_engine/models.py:L138 | neighbors=[models.py, .__post_init__(), .to_dict(), ConsistencyReport, FindingConsistency, consistency.py — Phase 5: N-run consist…]
- "basescanner": "BaseScanner" | kind=code-symbol | neighbors=[DBScanner, DNSScanner, FTPScanner, HostDiscoveryScanner, IoTScanner, IPMIScanner]
- "commit:repo:github.com/Rutikm18/Project-Vedha@7d8d3f3b50ca9f1d4c76921b8e656f345023b616": "7d8d3f3 merge: resolve conflicts with origin/ui-ux-backend-updates0109" | kind=Commit | source=git | neighbors=[42f4e28 feat: enhance security operatio…, page.tsx, layout.tsx, AssistantProvider.tsx, route.ts, addcapabilities-fable]
- "models_enums_assettype": "AssetType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L29 | neighbors=[enums.py, str, Convert a probe's self-assessed `findin…, Find the Asset for a probe-reported tar…, A still-relevant Finding with the same …, Bump severity one rung when the finding…]
- "detection_engine_vuln_db_vulndb": "VulnDB" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L85 | neighbors=[vuln_db.py, _merge_companion(), In-memory index over a loaded snapshot:…, _read_snapshot(), ._build_cve_index(), .covers()]
- "lib_backend": "backend.ts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L1 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "ad_ldap_enum_ldapenumerator": "LDAPEnumerator" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L117 | neighbors=[ldap_enum.py, ._attr(), .check_anonymous_bind(), .connect(), .connection(), .get_aces()]
- "models_scan_result_scanresult": "ScanResult" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L10 | neighbors=[scan_result.py, Append-only raw probe facts (P3-#10).  …, Base, TimestampMixin, Base, TimestampMixin]
- "tests_test_probe_core": "test_probe_core.py" | kind=code-symbol | source=probe/tests/test_probe_core.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files]
- "id_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7a637eb feat: network VA accuracy, KEV …, 7d8d3f3 merge: resolve conflicts with o…, 8f6bf49 Refactor code structure and rem…]
- "routers_agents": "agents.py" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1 | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, 0e22dbf feat(probe): bounded auto-troub…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 25c014d feat: enhance campaign progress…]
- "detection_engine_posture_rules": "posture_rules.py" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 26ea68c Add comprehensive tests for OS …, 3c9062a refactor: Update dashboard comp…, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…]
- "detection_engine_models_asset": "Asset" | kind=code-symbol | source=manager/detection_engine/models.py:L70 | neighbors=[models.py, .add_alias(), .add_fact(), .as_of(), .facts_by_scanner(), .open_ports()]
- "detection_engine_models_findingstate": "FindingState" | kind=code-symbol | source=manager/detection_engine/models.py:L119 | neighbors=[models.py, Enum, str, correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…, SMBv1 enabled + (credentialed hotfix li…]
- "main_scripts_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 37376de hardening(scanner): OPSEC de-si…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…]
- "scan_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 42f4e28 feat: enhance security operatio…, 64e8290 feat(campaign): implement VA ca…]
- "tests_test_detection_core_finding": "_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L62 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), .test_authoritative_tier4()]
- "app_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/page.tsx:L1 | neighbors=[Dashboard(), DashboardCharts.tsx, DashboardCharts(), PageShell.tsx, PageShell(), DashboardGrid.tsx]
- "exploit_msf_client_metasploitrpcclient": "MetasploitRPCClient" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L27 | neighbors=[msf_client.py, ._call(), .connect(), .disconnect(), .get_job_status(), .__init__()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cac022c40e254cd92ba6e8c73c79c0987b8650d2": "cac022c Everything is done and verified. Here's the wrap-up.What I did (as an a…" | kind=Commit | source=git | neighbors=[c5e2d0e chore: retire probe-go to spike…, kerberoast.py, ldap_enum.py, agent.py, license.py, task_runner.py]
- "agent_engine": "engine.py" | kind=code-symbol | source=probe/agent/engine.py:L1 | neighbors=[agent.py, _applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _derive_devices()]
- "main_scripts_findings": "findings.py" | kind=code-symbol | source=probe/main_scripts/findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 6c1f014 feat(correlation): implement co…, 6e2818f Add support for additional serv…, _as_dict()]
- "tests_test_detection_core": "test_detection_core.py" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 7d8d3f3 merge: resolve conflicts with o…, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, _candidate()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@07ba102eb502f501c148d70f07182fc9f0548511": "07ba102 feat: enhance UI UX and detection pipeline" | kind=Commit | source=git | neighbors=[page.tsx, layout.tsx, page.tsx, route.ts, addcapabilities-fable, main]
- "detection_engine_ingest_ingestresult": "IngestResult" | kind=code-symbol | source=manager/detection_engine/ingest.py:L49 | neighbors=[ingest.py, ingest_file(), ingest_files(), .get_or_create_asset(), .__init__(), Asset]
- "detection_engine_enrichment_db_epssdb": "EpssDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L24 | neighbors=[enrichment_db.py, .get(), .__init__(), load_epss(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "detection_engine_enrichment_db_kevdb": "KevDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L15 | neighbors=[enrichment_db.py, .__init__(), .is_kev(), load_kev(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "lib_backend_backend": "backend()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L33 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "tests_test_probe_core_asset": "_asset()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L71 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "scanner_findings": "findings.py" | kind=code-symbol | source=probe/scanner/findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _as_dict(), build_service_index(), _by_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-001.json

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
