# Node Description Batch 42 of 131

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@6b6acb87b50e17f444fd6433cdaaf57cca5c2918": "6b6acb8 fix: update AWS compose command and set default MANAGER_PUBLIC_URL in d…" | kind=Commit | source=git | neighbors=[main, 2a36f8a fix: update docker compose comm…, d7329cf feat: enhance AWS deployment wi…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@879cdfa25f56102c23df1efdc671934f88d1b793": "879cdfa docs: probe fleet automation design spec (Phase 0 detailed)" | kind=Commit | source=git | neighbors=[41b692a Update project files, main, f3c3591 docs: Phase 0 queue-control imp…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@d7329cfe261cfa5fd29d0892344b94340cbe0b77": "d7329cf feat: enhance AWS deployment with new environment variables and scripts…" | kind=Commit | source=git | neighbors=[b5ffcb0 Refactor Vedha probe installer …, main, 6b6acb8 fix: update AWS compose command…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f1da96f64e70aef9d0275a6cdcdbf89b7334e948": "f1da96f fix: update environment variables and resource limits in docker-compose…" | kind=Commit | source=git | neighbors=[2a36f8a fix: update docker compose comm…, main, ca41cbf docs: pre-auth probe enrollment…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3c359163f16baf103a46a5170e40a9e95edda9d": "f3c3591 docs: Phase 0 queue-control implementation plan (8 TDD tasks)" | kind=Commit | source=git | neighbors=[879cdfa docs: probe fleet automation de…, main, c76b428 backend and login page error ha…]
- "dashboard_exposure_protocolriskcard": "ProtocolRiskCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/Exposure.tsx:L32 | neighbors=[page.tsx, Exposure.tsx, useExposure()]
- "dashboard_exposure_useexposure": "useExposure()" | kind=code-symbol | source=manager/frontend/components/dashboard/Exposure.tsx:L24 | neighbors=[Exposure.tsx, ProtocolRiskCard(), ZoneHealthCard()]
- "dashboard_exposure_zonehealthcard": "ZoneHealthCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/Exposure.tsx:L49 | neighbors=[page.tsx, Exposure.tsx, useExposure()]
- "dashboard_slarow_slarow": "SlaRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L31 | neighbors=[SlaRow.tsx, getSla(), page.tsx]
- "dashboard_slastatus_slarowview": "SlaRowView()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L77 | neighbors=[SlaStatus.tsx, pct(), timeLabel()]
- "dashboard_zonerow_zonerow": "ZoneRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/ZoneRow.tsx:L6 | neighbors=[Exposure.tsx, ZoneRow.tsx, page.tsx]
- "data_mock_dashboard_severity": "Severity" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L9 | neighbors=[SlaRow.tsx, mock-dashboard.ts, page.tsx]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-041.json

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
