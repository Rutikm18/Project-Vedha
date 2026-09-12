# Node Description Batch 2 of 380

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

- "engine_tool_runners": "tool-runners.ts" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, bin(), binName()]
- "lib_ai_engine": "ai-engine.ts" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c59db1 Implement instance locking mech…, 9c54022 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, route.ts]
- "agent_agent": "agent.py" | kind=code-symbol | source=probe/agent/agent.py:L1 | neighbors=[AgentDeps, AgentOpts, _bounded_env_int(), _check_anti_debug(), _classify_connection_error(), configure_logging()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@7a637ebe0685305ffefa921a6d3663c60b62878d": "7a637eb feat: network VA accuracy, KEV exploitability, and console parity" | kind=Commit | source=git | neighbors=[engine.py, explain_plan.py, page.tsx, page.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable]
- "settings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L1 | neighbors=[00c6648 feat(settings): editable email/…, 07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 3c9062a refactor: Update dashboard comp…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@198bae473612272d48586c2211dcfc881ed75ff2": "198bae4 snapshot: uncommitted system/ui/backend WIP for the 1209 integration" | kind=Commit | source=git | neighbors=[page.tsx, page.tsx, page.tsx, 1209_system_ui_backend_level_changes, page.tsx, 06b825d merge: hardened-agent architect…]
- "models_service_service": "Service" | kind=code-symbol | source=manager/backend/app/models/service.py:L10 | neighbors=[service.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@b4b12a903b40303ffa76f097396cb121f1b9b16e": "b4b12a9 Rename project and update files" | kind=Commit | source=git | neighbors=[agent.py, engine.py, result_spool.py, scope_crypt.py, task_runner.py, transport.py]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/coverage-gated-auto-resolution": "feat/coverage-gated-auto-resolution" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@26ea68c0a5b57ca977c28a93b7634862d8567e75": "26ea68c Add comprehensive tests for OS identification, reconciliation, and vali…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps]
- "models_enums_scanjobtype": "ScanJobType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L91 | neighbors=[enums.py, str, ScanJob, ADAssessRequest, Neo4jConfig, Active Directory assessment API.  POST …]
- "models_enums_scanjobstatus": "ScanJobStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L102 | neighbors=[enums.py, str, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "workflow_workflow_engine": "workflow_engine.py" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L1 | neighbors=[engine.py, explain_plan.py, local_run.py, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 22701ea Add tests for scanner parity an…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@b5ffcb044f83b971e79c066de279484edeed94ac": "b5ffcb0 Refactor Vedha probe installer and enhance device identity tests- Updat…" | kind=Commit | source=git | neighbors=[65f22a7 Add comprehensive tests for aut…, agent.py, device_identity.py, engine.py, result_spool.py, task_runner.py]
- "detection_engine_models_sourceconfidence": "SourceConfidence" | kind=code-symbol | source=manager/detection_engine/models.py:L24 | neighbors=[models.py, How was this fact obtained? Drives ever…, Enum, str, correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…]
- "detection_engine_models_fact": "Fact" | kind=code-symbol | source=manager/detection_engine/models.py:L44 | neighbors=[models.py, .ref(), One ScanResult line, carried forward wi…, AIClient, AINormalizerCache, AnthropicAIClient]
- "commit:repo:github.com/Rutikm18/Project-Vedha@7d8d3f3b50ca9f1d4c76921b8e656f345023b616": "7d8d3f3 merge: resolve conflicts with origin/ui-ux-backend-updates0109" | kind=Commit | source=git | neighbors=[42f4e28 feat: enhance security operatio…, page.tsx, layout.tsx, AssistantProvider.tsx, route.ts, 1209_system_ui_backend_level_changes]
- "detection_engine_cpe_normalizer_cpecandidate": "CPECandidate" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L42 | neighbors=[cpe_normalizer.py, .cpe23(), normalize_banner(), normalize_credentialed_packages(), normalize_db(), normalize_web()]
- "detection_engine_posture_rules": "posture_rules.py" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 198bae4 snapshot: uncommitted system/ui…, 26ea68c Add comprehensive tests for OS …, 3c9062a refactor: Update dashboard comp…, 6136a6e feat(detection): stable group_k…, 6bb51ab feat: add detection-explain end…]
- "id_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 5c59db1 Implement instance locking mech…, 7a637eb feat: network VA accuracy, KEV …]
- "detection_engine_models_finding": "Finding" | kind=code-symbol | source=manager/detection_engine/models.py:L138 | neighbors=[models.py, .__post_init__(), .to_dict(), ConsistencyReport, FindingConsistency, consistency.py — Phase 5: N-run consist…]
- "routers_agents": "agents.py" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1 | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, 0e22dbf feat(probe): bounded auto-troub…, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…]
- "lib_backend": "backend.ts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L1 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "scan_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 42f4e28 feat: enhance security operatio…]
- "basescanner": "BaseScanner" | kind=code-symbol | neighbors=[DBScanner, DNSScanner, FTPScanner, HostDiscoveryScanner, IoTScanner, IPMIScanner]
- "models_enums_assettype": "AssetType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L29 | neighbors=[enums.py, str, Convert a probe's self-assessed `findin…, Find the Asset for a probe-reported tar…, A still-relevant Finding with the same …, Bump severity one rung when the finding…]
- "detection_engine_vuln_db_vulndb": "VulnDB" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L85 | neighbors=[vuln_db.py, _merge_companion(), In-memory index over a loaded snapshot:…, _read_snapshot(), ._build_cve_index(), .covers()]
- "routers_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, 3ddc104 feat: unify customer and manage…, 3e6b187 feat: unify customer and manage…, 7a637eb feat: network VA accuracy, KEV …]
- "ad_ldap_enum_ldapenumerator": "LDAPEnumerator" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L117 | neighbors=[ldap_enum.py, ._attr(), .check_anonymous_bind(), .connect(), .connection(), .get_aces()]
- "models_scan_result_scanresult": "ScanResult" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L10 | neighbors=[scan_result.py, Append-only raw probe facts (P3-#10).  …, Base, TimestampMixin, Base, TimestampMixin]
- "tests_test_probe_core": "test_probe_core.py" | kind=code-symbol | source=probe/tests/test_probe_core.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files]
- "report_finding_model": "finding-model.ts" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 315cf9c feat(frontend): refine reports …, 3618365 Vendor finding-model + port its…, 76240ac UI UX Update, evidence-presentation.ts, adapt.ts]
- "app_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/page.tsx:L1 | neighbors=[Dashboard(), DashboardWorkspace.tsx, DashboardWorkspace(), console-source.tsx, OperatorConsoleProvider(), 07ba102 feat: enhance UI UX and detecti…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cac022c40e254cd92ba6e8c73c79c0987b8650d2": "cac022c Everything is done and verified. Here's the wrap-up.What I did (as an a…" | kind=Commit | source=git | neighbors=[c5e2d0e chore: retire probe-go to spike…, kerberoast.py, ldap_enum.py, agent.py, license.py, task_runner.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@07ba102eb502f501c148d70f07182fc9f0548511": "07ba102 feat: enhance UI UX and detection pipeline" | kind=Commit | source=git | neighbors=[page.tsx, layout.tsx, page.tsx, route.ts, 1209_system_ui_backend_level_changes, addcapabilities-fable]
- "detection_engine_models_asset": "Asset" | kind=code-symbol | source=manager/detection_engine/models.py:L70 | neighbors=[models.py, .add_alias(), .add_fact(), .as_of(), .facts_by_scanner(), .open_ports()]
- "detection_engine_models_findingstate": "FindingState" | kind=code-symbol | source=manager/detection_engine/models.py:L119 | neighbors=[models.py, Enum, str, correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…, SMBv1 enabled + (credentialed hotfix li…]
- "lib_adapters": "adapters.ts" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 315cf9c feat(frontend): refine reports …, 42f4e28 feat: enhance security operatio…, 76240ac UI UX Update]
- "main_scripts_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 37376de hardening(scanner): OPSEC de-si…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 5c59db1 Implement instance locking mech…]
- "agent_engine": "engine.py" | kind=code-symbol | source=probe/agent/engine.py:L1 | neighbors=[agent.py, _applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _derive_devices()]

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
