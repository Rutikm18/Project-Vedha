# Node Description Batch 191 of 330

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

- "detection_edr_rationale_187": "SentinelOne via the REST ``/web/api/v2.1/threats`` endpoint.     config: {base_u" | kind=entity | source=manager/backend/app/detection/edr.py:L187 | neighbors=[SentinelOne] | lang=en
- "detection_edr_rationale_92": "Falcon: query detection IDs then fetch their summaries.     config: {base_url, t" | kind=entity | source=manager/backend/app/detection/edr.py:L92 | neighbors=[CrowdStrikeFalcon] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache_post_init": ".__post_init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L142 | neighbors=[AINormalizerCache] | lang=en
- "detection_engine_ai_normalizer_anthropicaiclient_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L103 | neighbors=[AnthropicAIClient] | lang=en
- "detection_engine_ai_normalizer_fakeaiclient_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L131 | neighbors=[FakeAIClient] | lang=en
- "detection_engine_bridge_rationale_105": "(census, rejected_line_numbers) from the engine's IngestResult.      The census" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L105 | neighbors=[_ingest_census()] | lang=en
- "detection_engine_bridge_rationale_114": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L114 | neighbors=[_apply_regression_reopen()] | lang=en
- "detection_engine_bridge_rationale_128": "A remediated finding with the same (engagement, asset, title) — the     regressi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L128 | neighbors=[_find_remediated_match()] | lang=en
- "detection_engine_bridge_rationale_130": "A remediated finding with the same (engagement, asset, title) — the     regressi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L130 | neighbors=[_find_remediated_match()] | lang=en
- "detection_engine_bridge_rationale_139": "The subset of `facts` ingest accepted. We wrote one fact per line in order," | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L139 | neighbors=[_accepted()] | lang=en
- "detection_engine_bridge_rationale_140": "Best-effort: compute + stamp each finding's verification verdict. A failure" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L140 | neighbors=[_stamp_verification()] | lang=pt
- "detection_engine_bridge_rationale_142": "Best-effort: compute + stamp each finding's verification verdict. A failure" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L142 | neighbors=[_stamp_verification()] | lang=pt
- "detection_engine_bridge_rationale_149": "Escalate by severity of loss. A TOTAL wipeout with facts submitted is the     ag" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L149 | neighbors=[_log_ingest_health()] | lang=en
- "detection_engine_bridge_rationale_157": "ip → {device_role, role_detail} from already-promoted assets, so a prior     dev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L157 | neighbors=[_engagement_device_roles()] | lang=en
- "detection_engine_bridge_rationale_158": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L158 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_171": "Raw scanner facts -> (cve_finding_dicts, posture_finding_dicts, meta), running" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L171 | neighbors=[detect_all_from_facts_traced()] | lang=en
- "detection_engine_bridge_rationale_174": "Correlate composite attack paths from the run's facts and persist them as     Fi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L174 | neighbors=[_persist_attack_paths()] | lang=en
- "detection_engine_bridge_rationale_223": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L223 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_252": "Backward-compatible (cve, posture) view — drops the trace meta." | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L252 | neighbors=[detect_all_from_facts()] | lang=en
- "detection_engine_bridge_rationale_258": "CVE finding dicts only — backward-compatible wrapper over the full run." | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L258 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_272": "Stable, human title for a posture finding — the same string across runs so     d" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L272 | neighbors=[_posture_title()] | lang=en
- "detection_engine_bridge_rationale_279": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L279 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_281": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L281 | neighbors=[_apply_regression_reopen()] | lang=en
- "detection_engine_bridge_rationale_292": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L292 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_297": "A remediated finding with the same (engagement, asset, title) — the     regressi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L297 | neighbors=[_find_remediated_match()] | lang=en
- "detection_engine_bridge_rationale_324": "Translate posture/config-exposure findings (from the VERIFIED scanners) into" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L324 | neighbors=[_persist_posture_findings()] | lang=en
- "detection_engine_bridge_rationale_368": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L368 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_388": "Best-effort: compute + stamp each finding's verification verdict. A failure" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L388 | neighbors=[_stamp_verification()] | lang=pt
- "detection_engine_bridge_rationale_403": "ip → {device_role, role_detail} from already-promoted assets, so a prior     dev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L403 | neighbors=[_engagement_device_roles()] | lang=en
- "detection_engine_bridge_rationale_421": "Correlate composite attack paths from the run's facts and persist them as     Fi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L421 | neighbors=[_persist_attack_paths()] | lang=en
- "detection_engine_bridge_rationale_48": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L48 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_493": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L493 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_50": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L50 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_56": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L56 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_678": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L678 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_86": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L86 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_88": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L88 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_build_nvd_cpe_snapshot_rationale_1": "build_nvd_cpe_snapshot.py — generate the NVD/CPE companion vuln snapshot.  WHY A" | kind=entity | source=manager/detection_engine/build_nvd_cpe_snapshot.py:L1 | neighbors=[build_nvd_cpe_snapshot.py] | lang=en
- "detection_engine_build_nvd_cpe_snapshot_rationale_33": "One OSV-shaped record: affected below `fixed` (NVD versionEndExcluding)." | kind=entity | source=manager/detection_engine/build_nvd_cpe_snapshot.py:L33 | neighbors=[_rec()] | lang=en
- "detection_engine_consistency_consistencyreport_intermittent": ".intermittent()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L96 | neighbors=[ConsistencyReport] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-190.json

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
