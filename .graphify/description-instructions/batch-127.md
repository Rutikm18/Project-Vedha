# Node Description Batch 128 of 209

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

- "detection_attack_paths_rationale_63": "The weaknesses observed on ONE host, distilled from its facts." | kind=entity | source=manager/backend/app/detection/attack_paths.py:L63 | neighbors=[_HostSignals] | lang=en
- "detection_correlator_detectioncorrelator_compute_coverage": ".compute_coverage()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L159 | neighbors=[DetectionCorrelator] | lang=en
- "detection_correlator_detectioncorrelator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L76 | neighbors=[DetectionCorrelator] | lang=en
- "detection_edr_build_edr_engine": "build_edr_engine()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L235 | neighbors=[edr.py] | lang=en
- "detection_edr_edrdetection_is_prevented": ".is_prevented()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L43 | neighbors=[EDRDetection] | lang=en
- "detection_edr_edrqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L65 | neighbors=[EDRQueryEngine] | lang=en
- "detection_edr_edrqueryengine_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L70 | neighbors=[EDRQueryEngine] | lang=en
- "detection_edr_rationale_1": "EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender" | kind=entity | source=manager/backend/app/detection/edr.py:L1 | neighbors=[edr.py] | lang=en
- "detection_edr_rationale_141": "Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi" | kind=entity | source=manager/backend/app/detection/edr.py:L141 | neighbors=[MicrosoftDefender] | lang=en
- "detection_edr_rationale_187": "SentinelOne via the REST ``/web/api/v2.1/threats`` endpoint.     config: {base_u" | kind=entity | source=manager/backend/app/detection/edr.py:L187 | neighbors=[SentinelOne] | lang=en
- "detection_edr_rationale_92": "Falcon: query detection IDs then fetch their summaries.     config: {base_url, t" | kind=entity | source=manager/backend/app/detection/edr.py:L92 | neighbors=[CrowdStrikeFalcon] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache_post_init": ".__post_init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L142 | neighbors=[AINormalizerCache] | lang=en
- "detection_engine_ai_normalizer_anthropicaiclient_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L103 | neighbors=[AnthropicAIClient] | lang=en
- "detection_engine_ai_normalizer_fakeaiclient_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L131 | neighbors=[FakeAIClient] | lang=en
- "detection_engine_bridge_rationale_114": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L114 | neighbors=[_apply_regression_reopen()] | lang=en
- "detection_engine_bridge_rationale_128": "A remediated finding with the same (engagement, asset, title) — the     regressi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L128 | neighbors=[_find_remediated_match()] | lang=en
- "detection_engine_bridge_rationale_130": "A remediated finding with the same (engagement, asset, title) — the     regressi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L130 | neighbors=[_find_remediated_match()] | lang=en
- "detection_engine_bridge_rationale_140": "Best-effort: compute + stamp each finding's verification verdict. A failure" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L140 | neighbors=[_stamp_verification()] | lang=pt
- "detection_engine_bridge_rationale_142": "Best-effort: compute + stamp each finding's verification verdict. A failure" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L142 | neighbors=[_stamp_verification()] | lang=pt
- "detection_engine_bridge_rationale_157": "ip → {device_role, role_detail} from already-promoted assets, so a prior     dev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L157 | neighbors=[_engagement_device_roles()] | lang=en
- "detection_engine_bridge_rationale_158": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L158 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_174": "Correlate composite attack paths from the run's facts and persist them as     Fi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L174 | neighbors=[_persist_attack_paths()] | lang=en
- "detection_engine_bridge_rationale_223": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L223 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_279": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L279 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_292": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L292 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_368": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L368 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_48": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L48 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_50": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L50 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_86": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L86 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_88": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L88 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_consistency_consistencyreport_intermittent": ".intermittent()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L96 | neighbors=[ConsistencyReport] | lang=en
- "detection_engine_consistency_consistencyreport_stable": ".stable()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L92 | neighbors=[ConsistencyReport] | lang=en
- "detection_engine_consistency_findingconsistency_classification": ".classification()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L67 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_consistency_findingconsistency_rate": ".rate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L59 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_cpe_normalizer_cpecandidate_cpe23": ".cpe23()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L72 | neighbors=[CPECandidate] | lang=en
- "detection_engine_cvss_rationale_1": "cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network" | kind=entity | source=manager/detection_engine/cvss.py:L1 | neighbors=[cvss.py] | lang=en
- "detection_engine_cvss_rationale_23": "CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r" | kind=entity | source=manager/detection_engine/cvss.py:L23 | neighbors=[_roundup()] | lang=en
- "detection_engine_cvss_rationale_44": "Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin" | kind=entity | source=manager/detection_engine/cvss.py:L44 | neighbors=[base_score()] | lang=en
- "detection_engine_enrichment_db_epssdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L25 | neighbors=[EpssDB] | lang=en
- "detection_engine_enrichment_db_kevdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L16 | neighbors=[KevDB] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-127.json

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
