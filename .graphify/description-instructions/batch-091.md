# Node Description Batch 92 of 332

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@2c38782317674ba6a0323a1ea1539a68587a356d": "2c38782 docs: spec CVE-breadth phase — snapshot must answer for every recognize…" | kind=Commit | source=git | neighbors=[main, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…]
- "components_dashboardcharts_dashboardcharts": "DashboardCharts()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L180 | neighbors=[page.tsx, DashboardCharts.tsx, page.tsx]
- "cve_cli_cmd_correlate": "cmd_correlate()" | kind=code-symbol | source=probe/cve/cli.py:L81 | neighbors=[cli.py, _merge_findings(), _read_facts()]
- "cve_cli_merge_findings": "_merge_findings()" | kind=code-symbol | source=probe/cve/cli.py:L65 | neighbors=[cli.py, cmd_correlate(), Merge CVE-finding lists, dedup by (cve_…]
- "cve_cli_read_facts": "_read_facts()" | kind=code-symbol | source=probe/cve/cli.py:L26 | neighbors=[cli.py, cmd_correlate(), Yield fact dicts from a JSONL file ('-'…]
- "cve_correlator_backport_marker": "_backport_marker()" | kind=code-symbol | source=probe/cve/correlator.py:L57 | neighbors=[correlator.py, correlate(), Return the distro-backport token found …]
- "cve_correlator_cvefinding": "CVEFinding" | kind=code-symbol | source=probe/cve/correlator.py:L84 | neighbors=[correlator.py, correlate(), .to_dict()]
- "cve_correlator_risk_score": "risk_score()" | kind=code-symbol | source=probe/cve/correlator.py:L63 | neighbors=[correlator.py, correlate(), 0–100 prioritization score. CVSS is hal…]
- "cve_ingest_cvss": "_cvss()" | kind=code-symbol | source=probe/cve/ingest.py:L88 | neighbors=[ingest.py, ingest_one_cve(), Best available CVSS: prefer v3.1 > v3.0…]
- "cve_ingest_ingest_epss": "ingest_epss()" | kind=code-symbol | source=probe/cve/ingest.py:L211 | neighbors=[ingest.py, ingest_all(), _get()]
- "cve_ingest_ingest_kev": "ingest_kev()" | kind=code-symbol | source=probe/cve/ingest.py:L193 | neighbors=[ingest.py, ingest_all(), _get()]
- "cve_ingest_parse_criteria": "_parse_criteria()" | kind=code-symbol | source=probe/cve/ingest.py:L109 | neighbors=[ingest.py, ingest_one_cve(), cpe:2.3:a:vendor:product:version:... ->…]
- "cve_online_lookup_vulners": "lookup_vulners()" | kind=code-symbol | source=probe/cve/online.py:L90 | neighbors=[online.py, enrich_findings(), Ask Vulners whether a public exploit is…]
- "cve_online_onlineresult": "OnlineResult" | kind=code-symbol | source=probe/cve/online.py:L51 | neighbors=[online.py, lookup_nvd(), What a live lookup could establish for …]
- "cve_online_was_exposed": "_was_exposed()" | kind=code-symbol | source=probe/cve/online.py:L214 | neighbors=[online.py, _apply(), Recover whether the exposure boost was …]
- "cve_version_in_range": "in_range()" | kind=code-symbol | source=probe/cve/version.py:L56 | neighbors=[version.py, compare(), Is `version` inside the NVD-style bound…]
- "cve_version_parse_version": "parse_version()" | kind=code-symbol | source=probe/cve/version.py:L28 | neighbors=[version.py, compare(), Normalize a version string into a compa…]
- "cve_weakness_map_finding_view": "_finding_view()" | kind=code-symbol | source=probe/cve/weakness_map.py:L120 | neighbors=[weakness_map.py, correlate_weaknesses(), Return the Finding dict from a fact, or…]
- "cve_weakness_map_mirror_cve": "_mirror_cve()" | kind=code-symbol | source=probe/cve/weakness_map.py:L141 | neighbors=[weakness_map.py, correlate_weaknesses(), Pull CVSS/KEV/EPSS for one CVE straight…]
- "dashboard_dashboardgrid_dashboardgrid": "DashboardGrid()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L138 | neighbors=[page.tsx, DashboardGrid.tsx, page.tsx]
- "dashboard_exposurecards_protocolriskcard": "ProtocolRiskCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L89 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, useExposure()]
- "dashboard_exposurecards_useexposure": "useExposure()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L30 | neighbors=[ExposureCards.tsx, ProtocolRiskCard(), ZoneHealthCard()]
- "dashboard_exposurecards_zonehealthcard": "ZoneHealthCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L123 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, useExposure()]
- "dashboard_posturescorecard_useposture": "usePosture()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L38 | neighbors=[PatchComparisonMatrix.tsx, PostureScorecard.tsx, PostureScorecard()]
- "dashboard_slastatus_slastatus": "SlaStatus()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L181 | neighbors=[DashboardGrid.tsx, SlaStatus.tsx, page.tsx]
- "detection_active_validation_interpret_validation": "interpret_validation()" | kind=code-symbol | source=manager/backend/app/detection/active_validation.py:L40 | neighbors=[active_validation.py, ValidationOutcome, Map a probe safe-check result to a verd…]
- "detection_attack_paths_attack_path_findings": "attack_path_findings()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L273 | neighbors=[attack_paths.py, _group(), Correlate composite attack paths from r…]
- "detection_attack_paths_hostsignals_finalize": ".finalize()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L124 | neighbors=[_group(), _HostSignals, Fold in a persisted device role (from a…]
- "detection_attack_paths_is_domain_controller": "_is_domain_controller()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L53 | neighbors=[attack_paths.py, _legacy_windows(), _ntlm_relay()]
- "detection_attack_paths_snmp_public_lateral": "_snmp_public_lateral()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L242 | neighbors=[attack_paths.py, B3: a default SNMP community on network…, _is_network_device()]
- "detection_correlator_detectioncorrelator_host_for": "._host_for()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L164 | neighbors=[DetectionCorrelator, .correlate(), _host_matches()]
- "detection_correlator_detectioncorrelator_in_window": "._in_window()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L157 | neighbors=[DetectionCorrelator, .correlate(), _aware()]
- "detection_correlator_detectioncorrelator_min_latency": "._min_latency()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L169 | neighbors=[DetectionCorrelator, .correlate(), _aware()]
- "detection_correlator_host_matches": "_host_matches()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L69 | neighbors=[correlator.py, ._host_for(), _host_identity()]
- "detection_edr_crowdstrikefalcon_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L118 | neighbors=[CrowdStrikeFalcon, EDRDetection, _parse_dt()]
- "detection_edr_microsoftdefender_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L158 | neighbors=[MicrosoftDefender, EDRDetection, _parse_dt()]
- "detection_edr_sentinelone_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L209 | neighbors=[SentinelOne, EDRDetection, _parse_dt()]
- "detection_engine_ai_normalizer_ainormalizercache_key": "._key()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L149 | neighbors=[AINormalizerCache, .get(), .put()]
- "detection_engine_ai_normalizer_ainormalizercache_put": ".put()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L155 | neighbors=[AINormalizerCache, ._key(), propose_candidates()]
- "detection_engine_ai_normalizer_extract_raw_text": "extract_raw_text()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L206 | neighbors=[ai_normalizer.py, .get(), The raw observable text worth sending t…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-091.json

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
