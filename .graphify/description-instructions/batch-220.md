# Node Description Batch 221 of 380

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

- "detection_engine_bridge_rationale_223": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L223 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_252": "Backward-compatible (cve, posture) view — drops the trace meta." | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L252 | neighbors=[detect_all_from_facts()] | lang=en
- "detection_engine_bridge_rationale_258": "CVE finding dicts only — backward-compatible wrapper over the full run." | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L258 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_268": "Backward-compatible (cve, posture) view — drops the trace meta." | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L268 | neighbors=[detect_all_from_facts()] | lang=en
- "detection_engine_bridge_rationale_272": "Stable, human title for a posture finding — the same string across runs so     d" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L272 | neighbors=[_posture_title()] | lang=en
- "detection_engine_bridge_rationale_274": "CVE finding dicts only — backward-compatible wrapper over the full run." | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L274 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_279": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L279 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_281": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L281 | neighbors=[_apply_regression_reopen()] | lang=en
- "detection_engine_bridge_rationale_288": "Stable, human title for a posture finding — the same string across runs so     d" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L288 | neighbors=[_posture_title()] | lang=en
- "detection_engine_bridge_rationale_292": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L292 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_313": "The regression candidates, in ONE query. See load_finding_index." | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L313 | neighbors=[_load_remediated_index()] | lang=en
- "detection_engine_bridge_rationale_321": "A remediated finding with the same (engagement, asset, title) — the     regressi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L321 | neighbors=[_find_remediated_match()] | lang=en
- "detection_engine_bridge_rationale_324": "Translate posture/config-exposure findings (from the VERIFIED scanners) into" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L324 | neighbors=[_persist_posture_findings()] | lang=en
- "detection_engine_bridge_rationale_358": "Translate posture/config-exposure findings (from the VERIFIED scanners) into" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L358 | neighbors=[_persist_posture_findings()] | lang=en
- "detection_engine_bridge_rationale_368": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L368 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_388": "Best-effort: compute + stamp each finding's verification verdict. A failure" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L388 | neighbors=[_stamp_verification()] | lang=pt
- "detection_engine_bridge_rationale_403": "ip → {device_role, role_detail} from already-promoted assets, so a prior     dev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L403 | neighbors=[_engagement_device_roles()] | lang=en
- "detection_engine_bridge_rationale_421": "Correlate composite attack paths from the run's facts and persist them as     Fi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L421 | neighbors=[_persist_attack_paths()] | lang=en
- "detection_engine_bridge_rationale_436": "Best-effort: compute + stamp each finding's verification verdict. A failure" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L436 | neighbors=[_stamp_verification()] | lang=pt
- "detection_engine_bridge_rationale_451": "ip → {device_role, role_detail} from already-promoted assets, so a prior     dev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L451 | neighbors=[_engagement_device_roles()] | lang=en
- "detection_engine_bridge_rationale_469": "Correlate composite attack paths from the run's facts and persist them as     Fi" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L469 | neighbors=[_persist_attack_paths()] | lang=en
- "detection_engine_bridge_rationale_48": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L48 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_493": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L493 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_50": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L50 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_545": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L545 | neighbors=[create_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_56": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L56 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_57": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L57 | neighbors=[_vuln_db_meta()] | lang=en
- "detection_engine_bridge_rationale_678": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L678 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_750": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L750 | neighbors=[run_detection_job()] | lang=en
- "detection_engine_bridge_rationale_86": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L86 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_bridge_rationale_88": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L88 | neighbors=[detect_findings_from_facts()] | lang=en
- "detection_engine_build_nvd_cpe_snapshot_rationale_1": "build_nvd_cpe_snapshot.py — generate the NVD/CPE companion vuln snapshot.  WHY A" | kind=entity | source=manager/detection_engine/build_nvd_cpe_snapshot.py:L1 | neighbors=[build_nvd_cpe_snapshot.py] | lang=en
- "detection_engine_build_nvd_cpe_snapshot_rationale_33": "One OSV-shaped record: affected below `fixed` (NVD versionEndExcluding)." | kind=entity | source=manager/detection_engine/build_nvd_cpe_snapshot.py:L33 | neighbors=[_rec()] | lang=en
- "detection_engine_consistency_consistencyreport_intermittent": ".intermittent()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L96 | neighbors=[ConsistencyReport] | lang=en
- "detection_engine_consistency_consistencyreport_stable": ".stable()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L92 | neighbors=[ConsistencyReport] | lang=en
- "detection_engine_consistency_findingconsistency_classification": ".classification()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L67 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_consistency_findingconsistency_rate": ".rate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L59 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_correlate_rationale_105": "Apply authoritative-version suppression and preserve every decision.      The ac" | kind=entity | source=manager/detection_engine/correlate.py:L105 | neighbors=[suppress_negated_with_audit()] | lang=en
- "detection_engine_correlate_rationale_158": "The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp" | kind=entity | source=manager/detection_engine/correlate.py:L158 | neighbors=[_product_from_cpe()] | lang=en
- "detection_engine_correlate_rationale_178": "SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS" | kind=entity | source=manager/detection_engine/correlate.py:L178 | neighbors=[correlate_smb_patch()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-220.json

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
