# Node Description Batch 144 of 236

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

- "detection_prioritization_rationale_116": "(Re)compute risk_score for every still-relevant finding in the engagement." | kind=entity | source=manager/backend/app/detection/prioritization.py:L116 | neighbors=[prioritize_engagement_findings()] | lang=en
- "detection_prioritization_rationale_74": "The unified 0-1000 composite (see module docstring). Pure + deterministic." | kind=entity | source=manager/backend/app/detection/prioritization.py:L74 | neighbors=[composite_risk_score()] | lang=en
- "detection_prioritization_rationale_93": "The most-exposed value among an asset's services (external beats internal)." | kind=entity | source=manager/backend/app/detection/prioritization.py:L93 | neighbors=[_strongest_exposure()] | lang=en
- "detection_prioritization_rationale_99": "(kev_db, epss_db) from the pinned snapshots, or (None, None) if the     detectio" | kind=entity | source=manager/backend/app/detection/prioritization.py:L99 | neighbors=[_load_offline_kev_epss()] | lang=en
- "detection_resolution_rationale_1": "resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c" | kind=entity | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[resolution.py] | lang=en
- "detection_resolution_rationale_132": "Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r" | kind=entity | source=manager/backend/app/detection/resolution.py:L132 | neighbors=[apply_manual_reopen()] | lang=en
- "detection_resolution_rationale_28": "IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin" | kind=entity | source=manager/backend/app/detection/resolution.py:L28 | neighbors=[host_of()] | lang=en
- "detection_resolution_rationale_36": "What this run PROVABLY re-observed. An asset is covered only if a     completed" | kind=entity | source=manager/backend/app/detection/resolution.py:L36 | neighbors=[build_coverage()] | lang=en
- "detection_resolution_rationale_58": "Consecutive coverage-proven clean runs required before auto-close.     critical/" | kind=entity | source=manager/backend/app/detection/resolution.py:L58 | neighbors=[resolution_threshold()] | lang=en
- "detection_resolution_rationale_73": "Pure heart of auto-resolution. Given whether the finding's asset was     re-obse" | kind=entity | source=manager/backend/app/detection/resolution.py:L73 | neighbors=[decide_resolution()] | lang=en
- "detection_resolution_rationale_93": "Apply decide_resolution to every engine-managed open/confirmed finding     NOT t" | kind=entity | source=manager/backend/app/detection/resolution.py:L93 | neighbors=[evaluate_resolutions()] | lang=en
- "detection_siem_build_siem_engine": "build_siem_engine()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L249 | neighbors=[siem.py] | lang=en
- "detection_siem_rationale_1": "SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic" | kind=entity | source=manager/backend/app/detection/siem.py:L1 | neighbors=[siem.py] | lang=en
- "detection_siem_rationale_135": "Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi" | kind=entity | source=manager/backend/app/detection/siem.py:L135 | neighbors=[SentinelSIEM] | lang=en
- "detection_siem_rationale_185": "Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_" | kind=entity | source=manager/backend/app/detection/siem.py:L185 | neighbors=[ElasticSIEM] | lang=en
- "detection_siem_rationale_51": "Abstract SIEM connector." | kind=entity | source=manager/backend/app/detection/siem.py:L51 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_siem_rationale_82": "Splunk via the REST search endpoint (``/services/search/jobs/export``) with an" | kind=entity | source=manager/backend/app/detection/siem.py:L82 | neighbors=[SplunkSIEM] | lang=en
- "detection_siem_siemqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L55 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_siem_siemqueryengine_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L60 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_sigma_rationale_1": "SigmaRuleGenerator — produces a Sigma detection rule (YAML) for a MITRE techniqu" | kind=entity | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[sigma.py] | lang=pt
- "detection_sigma_rationale_114": "Return a Sigma rule (YAML string) for the technique, customised with the" | kind=entity | source=manager/backend/app/detection/sigma.py:L114 | neighbors=[.generate_sigma_for_technique()] | lang=en
- "detection_vantage_fusion_rationale_1": "vantage_fusion.py — fuse the exposure_matrix results of MULTIPLE probes.  A sing" | kind=entity | source=manager/backend/app/detection/vantage_fusion.py:L1 | neighbors=[vantage_fusion.py] | lang=en
- "detection_vantage_fusion_rationale_119": "(ip, proto, port) → fused exposure verdict, ready to stamp onto Service rows." | kind=entity | source=manager/backend/app/detection/vantage_fusion.py:L119 | neighbors=[fused_service_exposure()] | lang=en
- "detection_vantage_fusion_rationale_38": "(ip → {(proto,port): {vantage: status}}, ip → set(vantages))." | kind=entity | source=manager/backend/app/detection/vantage_fusion.py:L38 | neighbors=[_collect()] | lang=en
- "detection_vantage_fusion_rationale_81": "Fuse several probes' exposure_matrix results into one per-target matrix.      `r" | kind=entity | source=manager/backend/app/detection/vantage_fusion.py:L81 | neighbors=[fuse_exposure_results()] | lang=en
- "detection_verification_rationale_1": "verification.py — normalized, dashboard-facing verification verdict.  The determ" | kind=entity | source=manager/backend/app/detection/verification.py:L1 | neighbors=[verification.py] | lang=en
- "detection_verification_rationale_46": "Deterministic passive verdict from a detection finding's evidence dict." | kind=entity | source=manager/backend/app/detection/verification.py:L46 | neighbors=[compute_verdict()] | lang=en
- "detection_verification_rationale_76": "Only spend an LLM call where a rationale / FP-triage is worth it:     uncertain" | kind=entity | source=manager/backend/app/detection/verification.py:L76 | neighbors=[_qualifies_for_llm()] | lang=en
- "detection_verification_rationale_83": "Deterministic verdict, optionally enriched by an LLM rationale. The LLM     (duc" | kind=entity | source=manager/backend/app/detection/verification.py:L83 | neighbors=[verify_finding()] | lang=en
- "dev_hint_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/auth/dev-hint/route.ts:L17 | neighbors=[route.ts] | lang=en
- "discovery_device_profile_rationale_1": "device_profile.py — map a probe device_inventory result onto asset fields.  The" | kind=entity | source=manager/backend/app/discovery/device_profile.py:L1 | neighbors=[device_profile.py] | lang=en
- "discovery_device_profile_rationale_30": "The AssetType for a classifier device_type, or None to keep the existing." | kind=entity | source=manager/backend/app/discovery/device_profile.py:L30 | neighbors=[asset_type_for()] | lang=en
- "discovery_device_profile_rationale_37": "ip → {asset_type, device_role, role_detail, role_confidence} from a probe     de" | kind=entity | source=manager/backend/app/discovery/device_profile.py:L37 | neighbors=[device_profiles()] | lang=en
- "discovery_exposure_rationale_1": "exposure.py — reachability-aware risk from the probe's exposure_matrix use-case." | kind=entity | source=manager/backend/app/discovery/exposure.py:L1 | neighbors=[exposure.py] | lang=en
- "discovery_exposure_rationale_38": "(ip, proto, port) → exposure verdict, from a probe exposure_matrix result." | kind=entity | source=manager/backend/app/discovery/exposure.py:L38 | neighbors=[service_exposure()] | lang=en
- "discovery_exposure_rationale_69": "Bump a finding one severity rung when its service is internet-reachable.      On" | kind=entity | source=manager/backend/app/discovery/exposure.py:L69 | neighbors=[escalate_for_exposure()] | lang=en
- "discovery_finding_translator_rationale_124": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L124 | neighbors=[_find_open_duplicate()] | lang=en
- "discovery_finding_translator_rationale_144": "Convert a probe's self-assessed `findings` list into persisted Finding rows." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L144 | neighbors=[create_findings_from_probe_result()] | lang=pt
- "discovery_finding_translator_rationale_210": "Raise ONE engagement-level finding when the probe's own metrics say the     scan" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L210 | neighbors=[create_scan_health_finding()] | lang=en
- "discovery_finding_translator_rationale_55": "Find the Asset for a probe-reported target IP, creating a minimal one if needed." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L55 | neighbors=[_resolve_asset()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-143.json

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
