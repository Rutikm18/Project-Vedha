# Node Description Batch 43 of 134

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

- "commands_interactive_mergehosts": "mergeHosts()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1165 | neighbors=[interactive.ts, runPhasePortScan(), runPhaseServiceDetect()]
- "commands_interactive_printhostdiscoverydiagnostic": "printHostDiscoveryDiagnostic()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L917 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_printhostsummary": "printHostSummary()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L905 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_printstatesummary": "printStateSummary()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L895 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_runphaseenumeration": "runPhaseEnumeration()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1044 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()]
- "commands_interactive_runphasehostdiscovery": "runPhaseHostDiscovery()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1023 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, f5ce592 first commit]
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L61 | neighbors=[LiveOverview.tsx, verdict(), page.tsx]
- "dashboard_patchcomparisonmatrix_patchcomparisonmatrix": "PatchComparisonMatrix()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L70 | neighbors=[PatchComparisonMatrix.tsx, n(), page.tsx]
- "dashboard_posturescorecard_posturescorecard": "PostureScorecard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L105 | neighbors=[PostureScorecard.tsx, usePosture(), page.tsx]
- "dashboard_posturescorecard_useposture": "usePosture()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L39 | neighbors=[PatchComparisonMatrix.tsx, PostureScorecard.tsx, PostureScorecard()]
- "detection_correlator_detectioncorrelator_host_for": "._host_for()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L142 | neighbors=[DetectionCorrelator, .correlate(), _host_matches()]
- "detection_correlator_detectioncorrelator_in_window": "._in_window()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L135 | neighbors=[DetectionCorrelator, .correlate(), _aware()]
- "detection_correlator_detectioncorrelator_min_latency": "._min_latency()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L147 | neighbors=[DetectionCorrelator, .correlate(), _aware()]
- "detection_edr_crowdstrikefalcon_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L118 | neighbors=[CrowdStrikeFalcon, EDRDetection, _parse_dt()]
- "detection_edr_microsoftdefender_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L158 | neighbors=[MicrosoftDefender, EDRDetection, _parse_dt()]
- "detection_edr_sentinelone_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L209 | neighbors=[SentinelOne, EDRDetection, _parse_dt()]
- "detection_engine_ai_normalizer_ainormalizercache_key": "._key()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L149 | neighbors=[AINormalizerCache, .get(), .put()]
- "detection_engine_ai_normalizer_ainormalizercache_put": ".put()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L155 | neighbors=[AINormalizerCache, ._key(), propose_candidates()]
- "detection_engine_ai_normalizer_extract_raw_text": "extract_raw_text()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L206 | neighbors=[ai_normalizer.py, .get(), The raw observable text worth sending t…]
- "detection_engine_ai_normalizer_rationale_1": "ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[ai_normalizer.py, CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_124": "Test double — a fixed lookup table, no network. Used to validate the     surroun" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L124 | neighbors=[FakeAIClient, CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_170": "True iff the real NVD CPE dictionary has at least one entry for this     vendor:" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L170 | neighbors=[validate_cpe_exists(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_207": "The raw observable text worth sending to the AI normalizer for this     Fact's s" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L207 | neighbors=[extract_raw_text(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_233": "The Phase 2 entry point. raw_text is whatever observed string the     rule-based" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L233 | neighbors=[propose_candidates(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_90": "Returns a list of {\"vendor\", \"product\", \"version\"} dicts —         exactly the v" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L90 | neighbors=[.propose_cpe(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_97": "Real implementation, gated behind the anthropic SDK + an API key.     Forces the" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L97 | neighbors=[AnthropicAIClient, CPECandidate, Fact]
- "detection_engine_bridge_ensure_importable": "_ensure_importable()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L65 | neighbors=[engine_bridge.py, detect_findings_from_facts(), _vuln_db_meta()]
- "detection_engine_bridge_run_detection_job": "run_detection_job()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L208 | neighbors=[engine_bridge.py, Background entry point (P1: keep detect…, create_findings_from_facts()]
- "detection_engine_consistency_wilson_ci": "wilson_ci()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L32 | neighbors=[consistency.py, .ci(), Wilson score interval for a binomial pr…]
- "detection_engine_correlate_product_from_cpe": "_product_from_cpe()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L114 | neighbors=[correlate.py, The CPE 'product' field — used as the j…, suppress_negated()]
- "detection_engine_correlate_suppress_negated": "suppress_negated()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L61 | neighbors=[correlate.py, Suppress a suspected/potential (inferre…, _product_from_cpe()]
- "detection_engine_cpe_normalizer_clean_debian_version": "clean_debian_version()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L77 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), dpkg version syntax: [epoch:]upstream_v…]
- "detection_engine_cpe_normalizer_normalize_banner": "normalize_banner()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L213 | neighbors=[cpe_normalizer.py, CPECandidate, service_banner.py's first_line/banner t…]
- "detection_engine_cpe_normalizer_normalize_db": "normalize_db()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L259 | neighbors=[cpe_normalizer.py, CPECandidate, db_scanner.py's real-protocol-handshake…]
- "detection_engine_cpe_normalizer_normalize_web": "normalize_web()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L231 | neighbors=[cpe_normalizer.py, CPECandidate, web_scanner.py's Server header + tech_h…]
- "detection_engine_cpe_normalizer_parse_package_lines": "_parse_package_lines()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L301 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), Yields (package_name, raw_version, upst…]
- "detection_engine_cpe_normalizer_rationale_1": "cpe_normalizer.py — observed strings -> CPE 2.3 candidates, deterministically." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[cpe_normalizer.py, Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_150": "Every distinct OSV source-package name _PACKAGE_TO_CPE covers." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L150 | neighbors=[osv_source_packages(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_214": "service_banner.py's first_line/banner text -> CPE. SSH only for now —     generi" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L214 | neighbors=[normalize_banner(), Fact, SourceConfidence]

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
