# Node Description Batch 22 of 131

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, main, spike/probe-go, d1b4dd3 trim frontend to 7 core pages; …, a388bb3 script updated, architecture de…, feat/probe-usecase-alignment] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, main, spike/probe-go, 0510df3 going to build prompt and conne…, bd7383f scanner fine ..now integrations, feat/probe-usecase-alignment] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, main, spike/probe-go, a388bb3 script updated, architecture de…, f5ce592 first commit, feat/probe-usecase-alignment] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, backup-before-secret-removal, main, spike/probe-go, bd7383f scanner fine ..now integrations, feat/probe-usecase-alignment] | lang=fr
- "detection_correlator_detectionresultdto": "DetectionResultDTO" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L46 | neighbors=[correlator.py, .correlate(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_ai_normalizer_anthropicaiclient": "AnthropicAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L96 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Real implementation, gated behind the a…, CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_fakeaiclient": "FakeAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L123 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Test double — a fixed lookup table, no …, CPECandidate, Fact] | lang=en
- "detection_engine_ai_normalizer_propose_candidates": "propose_candidates()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L230 | neighbors=[ai_normalizer.py, AINormalizerCache, .get(), .put(), validate_cpe_exists(), The Phase 2 entry point. raw_text is wh…] | lang=en
- "detection_engine_bridge_rationale_1": "engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[engine_bridge.py, DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_rationale_112": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L112 | neighbors=[create_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_rationale_209": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L209 | neighbors=[run_detection_job(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_rationale_45": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L45 | neighbors=[_vuln_db_meta(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "detection_engine_bridge_rationale_83": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L83 | neighbors=[detect_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
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
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L85 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()] | lang=en
- "discovery_finding_translator_rationale_1": "Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[finding_translator.py, Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_finding_translator_rationale_54": "Find the Asset for a probe-reported target IP, creating a minimal one if needed." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L54 | neighbors=[_resolve_asset(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_78": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L78 | neighbors=[_find_open_duplicate(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_98": "Convert a probe's self-assessed `findings` list into persisted Finding rows." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L98 | neighbors=[create_findings_from_probe_result(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_service_id": "service_id.py" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ServiceFingerprint, ServiceIdentifier, ServiceIdentifier — banner + port → str…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "engine_tool_runners_hasbinary": "hasBinary()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L63 | neighbors=[tool-runners.ts, resolveBinPath(), runFfuf(), runHttpx(), runNaabu(), runWhatweb()] | lang=en
- "engine_tool_runners_runffuf": "runFfuf()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L881 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "engine_tool_runners_runhostdiscovery": "runHostDiscovery()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L564 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts(), tools.ts] | lang=en
- "engine_tool_runners_runwhatweb": "runWhatweb()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L798 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "graph_analyzer": "analyzer.py" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, PathAnalyzer, _priority(), _safe_float(), PathAnalyzer — attack-path discovery, s…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "graph_analyzer_pathanalyzer_movement_graph": ".movement_graph()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L87 | neighbors=[PathAnalyzer, .find_blast_radius(), .find_paths_to_target(), ._exploit_info(), ._source_assets(), Build (and cache) the Asset→Asset movem…] | lang=en
- "import_facts_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/import-facts/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, BASE, POST(), bearerFrom(), 298a9d4 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "lib_agents_store_readfieldagents": "readFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L343 | neighbors=[agents-store.ts, getAgent(), getAllAgents(), ensureDataDir(), registerAgent(), updateAgentLastSeen()] | lang=en
- "lib_ai_engine_aireportstore": "aiReportStore" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L342 | neighbors=[ai-engine.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "lib_assistant_factcardvm": "FactCardVM" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L4 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, assistant.ts, security-context.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
