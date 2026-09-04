# Node Description Batch 43 of 330

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

- "ai_agent_agentdecisionengine_run": ".run()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L183 | neighbors=[AgentDecisionEngine, ._create(), ._exec_read_tool(), ._persist(), AgentUnavailableError, _tool_result()]
- "ai_agent_rationale_1": "agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to" | kind=entity | source=manager/backend/app/ai/agent.py:L1 | neighbors=[agent.py, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_agent_rationale_59": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/agent.py:L59 | neighbors=[AgentUnavailableError, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_prioritizer_vulnprioritizer_explain_prediction": ".explain_prediction()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L158 | neighbors=[Per-feature contribution to this predic…, VulnPrioritizer, extract_features(), .fallback_score(), ._formula_contributions(), .predict_priority()]
- "alembic_env": "env.py" | kind=code-symbol | source=manager/backend/alembic/env.py:L1 | neighbors=[do_run_migrations(), run_migrations_offline(), run_migrations_online(), config.py, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "auth_portal_scope_assert_client": "assert_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L31 | neighbors=[portal_scope.py, client_scoped(), Return the client's bound engagement id…, require_client(), resolve_scope(), Return the client's bound engagement id…]
- "campaigns_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/campaigns/route.ts:L1 | neighbors=[GET(), POST(), campaign-store.ts, listCampaigns(), saveCampaign(), d98f654 feat(manager): network-VA campa…]
- "cancel_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/fleet/jobs/[jobId]/cancel/route.ts:L1 | neighbors=[POST, backend.ts, backend(), with-backend.ts, withBackend(), 8f6bf49 Refactor code structure and rem…]
- "cli_auth_loadsession": "loadSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L15 | neighbors=[auth.ts, requireAuth(), doctor.ts, interactive.ts, login.ts, logout.ts]
- "commands_interactive_ensureauthenticated": "ensureAuthenticated()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L117 | neighbors=[interactive.ts, ask(), askSecret(), ln(), mainMenu(), runInteractive()]
- "commands_interactive_runhostdiscoveryonly": "runHostDiscoveryOnly()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L595 | neighbors=[interactive.ts, choose(), confirm(), ln(), runIterativeEngagement(), wizardScan()]
- "commands_interactive_runphasewithtools": "runPhaseWithTools()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L963 | neighbors=[interactive.ts, runPhaseEnumeration(), runPhaseHostDiscovery(), runPhasePortScan(), runPhaseServiceDetect(), runPhaseVulnAssess()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bf61dbc3d12b9690e3e603f4adbf0e341f656c0c": "bf61dbc docs: probe run/test guide; gitignore nohup.out" | kind=Commit | source=git | neighbors=[bd85323 feat(probe): self-heal re-enrol…, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, 21ebc46 feat(detection): unified priori…]
- "console_freshness": "Freshness.tsx" | kind=code-symbol | source=manager/frontend/components/console/Freshness.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, Freshness(), DashboardGrid.tsx]
- "customers_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/route.ts:L1 | neighbors=[c4386e4 feat(customers): operator Custo…, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "cve_ingest_get": "_get()" | kind=code-symbol | source=probe/cve/ingest.py:L55 | neighbors=[ingest.py, _ssl_context(), ingest_epss(), ingest_kev(), ingest_nvd(), GET with backoff on the transient failu…]
- "cve_ingest_ingest_nvd": "ingest_nvd()" | kind=code-symbol | source=probe/cve/ingest.py:L150 | neighbors=[ingest.py, ingest_all(), _get(), ingest_one_cve(), _ssl_context(), Pull the NVD CVE corpus into the mirror…]
- "cve_ingest_ingest_one_cve": "ingest_one_cve()" | kind=code-symbol | source=probe/cve/ingest.py:L117 | neighbors=[ingest.py, ingest_nvd(), _cvss(), _iter_cpe_matches(), _parse_criteria(), Upsert one NVD `cve` object + its CPE-a…]
- "cve_vulndb": "vulndb.py" | kind=code-symbol | source=probe/cve/vulndb.py:L1 | neighbors=[6e2818f Add support for additional serv…, _norm(), VulnDB, vulndb.py — the offline vulnerability m…, test_cve_correlation.py, test_weakness_map.py]
- "detection_active_validation": "active_validation.py" | kind=code-symbol | source=manager/backend/app/detection/active_validation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, 7bd104a feat(active-validation): pure r…, interpret_validation(), should_escalate(), ValidationOutcome, active_validation.py — manager-side dec…]
- "detection_attack_paths_hostsignals": "_HostSignals" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L62 | neighbors=[attack_paths.py, _group(), .finalize(), .__init__(), .observe(), The weaknesses observed on ONE host, di…]
- "detection_correlator_detectionresultdto": "DetectionResultDTO" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L47 | neighbors=[correlator.py, .correlate(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_engine_ai_normalizer_anthropicaiclient": "AnthropicAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L96 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Real implementation, gated behind the a…, CPECandidate, Fact]
- "detection_engine_ai_normalizer_fakeaiclient": "FakeAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L123 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Test double — a fixed lookup table, no …, CPECandidate, Fact]
- "detection_engine_ai_normalizer_propose_candidates": "propose_candidates()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L230 | neighbors=[ai_normalizer.py, AINormalizerCache, .get(), .put(), validate_cpe_exists(), The Phase 2 entry point. raw_text is wh…]
- "detection_engine_bridge_apply_regression_reopen": "_apply_regression_reopen()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L280 | neighbors=[engine_bridge.py, create_findings_from_facts(), _persist_posture_findings(), A previously-remediated finding whose i…, A previously-remediated finding whose i…, A previously-remediated finding whose i…]
- "detection_engine_bridge_find_remediated_match": "_find_remediated_match()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L296 | neighbors=[engine_bridge.py, create_findings_from_facts(), _persist_posture_findings(), A remediated finding with the same (eng…, A remediated finding with the same (eng…, A remediated finding with the same (eng…]
- "detection_engine_bridge_rationale_1": "engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[engine_bridge.py, DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_209": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L209 | neighbors=[run_detection_job(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_45": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L45 | neighbors=[_vuln_db_meta(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_83": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L83 | neighbors=[detect_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_correlate_rationale_1": "correlate.py — dedup, authoritative-suppression, and cross-fact composite correl" | kind=entity | source=manager/detection_engine/correlate.py:L1 | neighbors=[correlate.py, CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_115": "The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp" | kind=entity | source=manager/detection_engine/correlate.py:L115 | neighbors=[_product_from_cpe(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_135": "SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS" | kind=entity | source=manager/detection_engine/correlate.py:L135 | neighbors=[correlate_smb_patch(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_36": "Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the" | kind=entity | source=manager/detection_engine/correlate.py:L36 | neighbors=[dedup_findings(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_63": "Suppress a suspected/potential (inferred-source) finding when the     SAME host" | kind=entity | source=manager/detection_engine/correlate.py:L63 | neighbors=[suppress_negated(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_cvss": "cvss.py" | kind=code-symbol | source=manager/detection_engine/cvss.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, base_score(), parse_vector(), _roundup(), cvss.py — CVSS v3.1 base score from a v…, 298a9d4 trim frontend to 7 core pages; …]
- "detection_engine_matcher": "matcher.py" | kind=code-symbol | source=manager/detection_engine/matcher.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, match_candidate(), _safe_compare(), _version_in_ranges(), matcher.py — does this CPE candidate's …, 298a9d4 trim frontend to 7 core pages; …]
- "detection_engine_matcher_rationale_1": "matcher.py — does this CPE candidate's version fall inside a vulnerable range, p" | kind=entity | source=manager/detection_engine/matcher.py:L1 | neighbors=[matcher.py, CPECandidate, Finding, FindingState, SourceConfidence, VulnDB]
- "detection_engine_matcher_rationale_34": "dpkg_compare, but None instead of a misleading answer when one side     has an e" | kind=entity | source=manager/detection_engine/matcher.py:L34 | neighbors=[_safe_compare(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-042.json

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
