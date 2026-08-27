# Node Description Batch 69 of 236

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

- "commands_interactive_runphaseenumeration": "runPhaseEnumeration()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1044 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()] | lang=en
- "commands_interactive_runphasehostdiscovery": "runPhaseHostDiscovery()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1023 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, f5ce592 first commit] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0236a6011fa2a49e65e7f5cad6b04f643f83c6f7": "0236a60 fix(detection): full EPSS catalog so exploit-probability isn't blind" | kind=Commit | source=git | neighbors=[feat/nvd-vuln-detection-and-ingest-hard…, update_snapshot.py, 21ebc46 feat(detection): unified priori…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@bf61dbc3d12b9690e3e603f4adbf0e341f656c0c": "bf61dbc docs: probe run/test guide; gitignore nohup.out" | kind=Commit | source=git | neighbors=[bd85323 feat(probe): self-heal re-enrol…, feat/nvd-vuln-detection-and-ingest-hard…, 21ebc46 feat(detection): unified priori…] | lang=en
- "dashboard_exposurecards_protocolriskcard": "ProtocolRiskCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L92 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, useExposure()] | lang=en
- "dashboard_exposurecards_useexposure": "useExposure()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L31 | neighbors=[ExposureCards.tsx, ProtocolRiskCard(), ZoneHealthCard()] | lang=en
- "dashboard_exposurecards_zonehealthcard": "ZoneHealthCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L121 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, useExposure()] | lang=en
- "dashboard_posturescorecard_useposture": "usePosture()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L39 | neighbors=[PatchComparisonMatrix.tsx, PostureScorecard.tsx, PostureScorecard()] | lang=en
- "dashboard_slastatus_slastatus": "SlaStatus()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L169 | neighbors=[DashboardGrid.tsx, SlaStatus.tsx, page.tsx] | lang=en
- "detection_active_validation_interpret_validation": "interpret_validation()" | kind=code-symbol | source=manager/backend/app/detection/active_validation.py:L40 | neighbors=[active_validation.py, ValidationOutcome, Map a probe safe-check result to a verd…] | lang=en
- "detection_attack_paths_attack_path_findings": "attack_path_findings()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L273 | neighbors=[attack_paths.py, _group(), Correlate composite attack paths from r…] | lang=en
- "detection_attack_paths_hostsignals_finalize": ".finalize()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L124 | neighbors=[_group(), _HostSignals, Fold in a persisted device role (from a…] | lang=en
- "detection_attack_paths_is_domain_controller": "_is_domain_controller()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L53 | neighbors=[attack_paths.py, _legacy_windows(), _ntlm_relay()] | lang=en
- "detection_attack_paths_snmp_public_lateral": "_snmp_public_lateral()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L242 | neighbors=[attack_paths.py, B3: a default SNMP community on network…, _is_network_device()] | lang=en
- "detection_correlator_detectioncorrelator_host_for": "._host_for()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L142 | neighbors=[DetectionCorrelator, .correlate(), _host_matches()] | lang=en
- "detection_correlator_detectioncorrelator_in_window": "._in_window()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L135 | neighbors=[DetectionCorrelator, .correlate(), _aware()] | lang=en
- "detection_correlator_detectioncorrelator_min_latency": "._min_latency()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L147 | neighbors=[DetectionCorrelator, .correlate(), _aware()] | lang=en
- "detection_edr_crowdstrikefalcon_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L118 | neighbors=[CrowdStrikeFalcon, EDRDetection, _parse_dt()] | lang=en
- "detection_edr_microsoftdefender_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L158 | neighbors=[MicrosoftDefender, EDRDetection, _parse_dt()] | lang=en
- "detection_edr_sentinelone_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L209 | neighbors=[SentinelOne, EDRDetection, _parse_dt()] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache_key": "._key()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L149 | neighbors=[AINormalizerCache, .get(), .put()] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache_put": ".put()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L155 | neighbors=[AINormalizerCache, ._key(), propose_candidates()] | lang=en
- "detection_engine_ai_normalizer_extract_raw_text": "extract_raw_text()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L206 | neighbors=[ai_normalizer.py, .get(), The raw observable text worth sending t…] | lang=en
- "detection_engine_ai_normalizer_rationale_1": "ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[ai_normalizer.py, CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_rationale_124": "Test double — a fixed lookup table, no network. Used to validate the     surroun" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L124 | neighbors=[FakeAIClient, CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_rationale_170": "True iff the real NVD CPE dictionary has at least one entry for this     vendor:" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L170 | neighbors=[validate_cpe_exists(), CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_rationale_207": "The raw observable text worth sending to the AI normalizer for this     Fact's s" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L207 | neighbors=[extract_raw_text(), CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_rationale_233": "The Phase 2 entry point. raw_text is whatever observed string the     rule-based" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L233 | neighbors=[propose_candidates(), CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_rationale_90": "Returns a list of {\"vendor\", \"product\", \"version\"} dicts —         exactly the v" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L90 | neighbors=[.propose_cpe(), CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_rationale_97": "Real implementation, gated behind the anthropic SDK + an API key.     Forces the" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L97 | neighbors=[AnthropicAIClient, CPECandidate, Fact] | lang=en
- "detection_engine_bridge_engagement_device_roles": "_engagement_device_roles()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L156 | neighbors=[engine_bridge.py, _persist_attack_paths(), ip → {device_role, role_detail} from al…] | lang=en
- "detection_engine_bridge_ensure_importable": "_ensure_importable()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L70 | neighbors=[engine_bridge.py, detect_findings_from_facts(), _vuln_db_meta()] | lang=en
- "detection_engine_consistency_wilson_ci": "wilson_ci()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L32 | neighbors=[consistency.py, .ci(), Wilson score interval for a binomial pr…] | lang=en
- "detection_engine_correlate_product_from_cpe": "_product_from_cpe()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L114 | neighbors=[correlate.py, The CPE 'product' field — used as the j…, suppress_negated()] | lang=en
- "detection_engine_correlate_suppress_negated": "suppress_negated()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L61 | neighbors=[correlate.py, Suppress a suspected/potential (inferre…, _product_from_cpe()] | lang=en
- "detection_engine_cpe_normalizer_all_osv_source_packages": "all_osv_source_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L382 | neighbors=[cpe_normalizer.py, Every distinct OSV source-package name …, Every distinct OSV source-package name …] | lang=en
- "detection_engine_cpe_normalizer_clean_debian_version": "clean_debian_version()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L77 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), dpkg version syntax: [epoch:]upstream_v…] | lang=en
- "detection_engine_cpe_normalizer_normalize": "normalize()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L373 | neighbors=[cpe_normalizer.py, Dispatch a single Fact to the right par…, Dispatch a single Fact to the right par…] | lang=en
- "detection_engine_cpe_normalizer_rationale_1": "cpe_normalizer.py — observed strings -> CPE 2.3 candidates, deterministically." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[cpe_normalizer.py, Fact, SourceConfidence] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-068.json

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
