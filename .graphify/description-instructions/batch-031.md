# Node Description Batch 32 of 227

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

- "cli_auth_loadsession": "loadSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L15 | neighbors=[auth.ts, requireAuth(), doctor.ts, interactive.ts, login.ts, logout.ts] | lang=en
- "commands_interactive_ensureauthenticated": "ensureAuthenticated()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L117 | neighbors=[interactive.ts, ask(), askSecret(), ln(), mainMenu(), runInteractive()] | lang=en
- "commands_interactive_runhostdiscoveryonly": "runHostDiscoveryOnly()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L595 | neighbors=[interactive.ts, choose(), confirm(), ln(), runIterativeEngagement(), wizardScan()] | lang=en
- "commands_interactive_runphasewithtools": "runPhaseWithTools()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L963 | neighbors=[interactive.ts, runPhaseEnumeration(), runPhaseHostDiscovery(), runPhasePortScan(), runPhaseServiceDetect(), runPhaseVulnAssess()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@32feef6ad967e9b67c9439acb1b2eba507d8b4df": "32feef6 feat(engagement): enhance engagement metrics styling for better readabi…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, 9b61c19 feat(ui): improve engagement to…, 4733f24 evasion(scanner): --source-port…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@78d51c5a8c9d6aaa3dabfd5ae21632e736865ea3": "78d51c5 opsec(scanner): de-sign service_enum UA — completes the sweep (task C6)" | kind=Commit | source=git | neighbors=[185e648 docs: pending-work inventory (b…, feat/complete-pending-work, main, dec1e7c fix(scanner): resolve() family …, service_enum.py, service_enum.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9b61c190ebbb02cde565390ea54bf2a5c806df8e": "9b61c19 feat(ui): improve engagement toolbar and metric card animations for enh…" | kind=Commit | source=git | neighbors=[32feef6 feat(engagement): enhance engag…, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, 22e4f8d chore: update version] | lang=en
- "customers_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/route.ts:L1 | neighbors=[c4386e4 feat(customers): operator Custo…, GET, backend.ts, backend(), with-backend.ts, withBackend()] | lang=en
- "detection_active_validation": "active_validation.py" | kind=code-symbol | source=manager/backend/app/detection/active_validation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, 7bd104a feat(active-validation): pure r…, interpret_validation(), should_escalate(), ValidationOutcome, active_validation.py — manager-side dec…] | lang=en
- "detection_attack_paths_hostsignals": "_HostSignals" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L62 | neighbors=[attack_paths.py, _group(), .finalize(), .__init__(), .observe(), The weaknesses observed on ONE host, di…] | lang=en
- "detection_correlator_detectionresultdto": "DetectionResultDTO" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L46 | neighbors=[correlator.py, .correlate(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_ai_normalizer_anthropicaiclient": "AnthropicAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L96 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Real implementation, gated behind the a…, CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_fakeaiclient": "FakeAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L123 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Test double — a fixed lookup table, no …, CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_propose_candidates": "propose_candidates()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L230 | neighbors=[ai_normalizer.py, AINormalizerCache, .get(), .put(), validate_cpe_exists(), The Phase 2 entry point. raw_text is wh…] | lang=en
- "detection_engine_bridge_detect_findings_from_facts": "detect_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L87 | neighbors=[engine_bridge.py, create_findings_from_facts(), _ensure_importable(), facts (ScanResult dicts) -> detection_e…, facts (ScanResult dicts) -> detection_e…, facts (ScanResult dicts) -> detection_e…] | lang=en
- "detection_engine_bridge_rationale_1": "engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[engine_bridge.py, DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_rationale_209": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L209 | neighbors=[run_detection_job(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_rationale_45": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L45 | neighbors=[_vuln_db_meta(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_rationale_83": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L83 | neighbors=[detect_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_run_detection_job": "run_detection_job()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L367 | neighbors=[engine_bridge.py, Background entry point (P1: keep detect…, create_findings_from_facts(), Background entry point (P1: keep detect…, Background entry point (P1: keep detect…, Background entry point (P1: keep detect…] | lang=en
- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L49 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable(), (content_hash, fetched_at) of the pinne…, (content_hash, fetched_at) of the pinne…] | lang=en
- "detection_engine_correlate_rationale_1": "correlate.py — dedup, authoritative-suppression, and cross-fact composite correl" | kind=entity | source=manager/detection_engine/correlate.py:L1 | neighbors=[correlate.py, CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_115": "The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp" | kind=entity | source=manager/detection_engine/correlate.py:L115 | neighbors=[_product_from_cpe(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_135": "SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS" | kind=entity | source=manager/detection_engine/correlate.py:L135 | neighbors=[correlate_smb_patch(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_36": "Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the" | kind=entity | source=manager/detection_engine/correlate.py:L36 | neighbors=[dedup_findings(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_63": "Suppress a suspected/potential (inferred-source) finding when the     SAME host" | kind=entity | source=manager/detection_engine/correlate.py:L63 | neighbors=[suppress_negated(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_cvss": "cvss.py" | kind=code-symbol | source=manager/detection_engine/cvss.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, base_score(), parse_vector(), _roundup(), cvss.py — CVSS v3.1 base score from a v…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_matcher": "matcher.py" | kind=code-symbol | source=manager/detection_engine/matcher.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, match_candidate(), _safe_compare(), _version_in_ranges(), matcher.py — does this CPE candidate's …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_matcher_rationale_1": "matcher.py — does this CPE candidate's version fall inside a vulnerable range, p" | kind=entity | source=manager/detection_engine/matcher.py:L1 | neighbors=[matcher.py, CPECandidate, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_34": "dpkg_compare, but None instead of a misleading answer when one side     has an e" | kind=entity | source=manager/detection_engine/matcher.py:L34 | neighbors=[_safe_compare(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_45": "Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A" | kind=entity | source=manager/detection_engine/matcher.py:L45 | neighbors=[_version_in_ranges(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_81": "All Findings this single CPE candidate produces against the snapshot.     Empty" | kind=entity | source=manager/detection_engine/matcher.py:L81 | neighbors=[match_candidate(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_version_compare_verify_pure_python_matches_dpkg": "verify_pure_python_matches_dpkg()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L243 | neighbors=[version_compare.py, Confirm pure-Python agrees with the rea…, _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), _load_validation_markers(), _save_validation_marker()] | lang=en
- "detection_vantage_fusion_fuse_exposure_results": "fuse_exposure_results()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L80 | neighbors=[vantage_fusion.py, _collect(), _is_external(), _verdict(), fused_service_exposure(), Fuse several probes' exposure_matrix re…] | lang=en
- "discovery_finding_translator_rationale_1": "Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[finding_translator.py, Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_finding_translator_rationale_54": "Find the Asset for a probe-reported target IP, creating a minimal one if needed." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L54 | neighbors=[_resolve_asset(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_78": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L78 | neighbors=[_find_open_duplicate(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_service_id": "service_id.py" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ServiceFingerprint, ServiceIdentifier, ServiceIdentifier — banner + port → str…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "engine_tool_runners_hasbinary": "hasBinary()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L63 | neighbors=[tool-runners.ts, resolveBinPath(), runFfuf(), runHttpx(), runNaabu(), runWhatweb()] | lang=en
- "engine_tool_runners_runffuf": "runFfuf()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L881 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), hasBinary(), spawnOpts()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-031.json

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
