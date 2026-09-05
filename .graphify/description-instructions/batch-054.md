# Node Description Batch 55 of 336

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

- "detection_correlator_rationale_1": "DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale" | kind=entity | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_correlator_rationale_210": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L210 | neighbors=[_aware(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_bridge_persist_attack_paths": "_persist_attack_paths()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L417 | neighbors=[engine_bridge.py, create_findings_from_facts(), _engagement_device_roles(), Correlate composite attack paths from t…, Correlate composite attack paths from t…] | lang=en
- "detection_engine_bridge_stamp_verification": "_stamp_verification()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L387 | neighbors=[engine_bridge.py, create_findings_from_facts(), Best-effort: compute + stamp each findi…, Best-effort: compute + stamp each findi…, Best-effort: compute + stamp each findi…] | lang=en
- "detection_engine_build_nvd_cpe_snapshot": "build_nvd_cpe_snapshot.py" | kind=code-symbol | source=manager/detection_engine/build_nvd_cpe_snapshot.py:L1 | neighbors=[d0d1931 feat(detection): NVD/CPE vuln f…, _content_hash(), main(), _rec(), build_nvd_cpe_snapshot.py — generate th…] | lang=en
- "detection_engine_correlate_product_from_cpe": "_product_from_cpe()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L157 | neighbors=[correlate.py, The CPE 'product' field — used as the j…, suppress_negated_with_audit(), The CPE 'product' field — used as the j…, suppress_negated()] | lang=en
- "detection_engine_correlate_suppress_negated": "suppress_negated()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L80 | neighbors=[correlate.py, Suppress a suspected/potential (inferre…, suppress_negated_with_audit(), Suppress a suspected/potential (inferre…, _product_from_cpe()] | lang=en
- "detection_engine_correlate_suppress_negated_with_audit": "suppress_negated_with_audit()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L101 | neighbors=[correlate.py, Apply authoritative-version suppression…, suppress_negated(), _product_from_cpe(), SuppressionRecord] | lang=en
- "detection_engine_cpe_normalizer_normalize_banner": "normalize_banner()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L250 | neighbors=[cpe_normalizer.py, CPECandidate, service_banner.py's parsed product/vers…, service_banner.py's parsed product/vers…, service_banner.py's first_line/banner t…] | lang=en
- "detection_engine_cpe_normalizer_normalize_db": "normalize_db()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L313 | neighbors=[cpe_normalizer.py, CPECandidate, db_scanner.py's real-protocol-handshake…, db_scanner.py's real-protocol-handshake…, db_scanner.py's real-protocol-handshake…] | lang=en
- "detection_engine_cpe_normalizer_normalize_web": "normalize_web()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L285 | neighbors=[cpe_normalizer.py, CPECandidate, web_scanner.py's Server header + tech_h…, web_scanner.py's Server header + tech_h…, web_scanner.py's Server header + tech_h…] | lang=en
- "detection_engine_cpe_normalizer_parse_package_lines": "_parse_package_lines()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L355 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), Yields (package_name, raw_version, upst…, Yields (package_name, raw_version, upst…, Yields (package_name, raw_version, upst…] | lang=en
- "detection_engine_enrichment": "enrichment.py" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _compute_priority(), enrich_finding(), enrichment.py — join CVSS + KEV + EPSS …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_enrichment_db_epssdb_get": ".get()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L29 | neighbors=[EpssDB, load_epss(), load_kev(), {'epss': float, 'percentile': float} or…, {'epss': float, 'percentile': float} or…] | lang=en
- "detection_engine_enrichment_rationale_1": "enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier." | kind=entity | source=manager/detection_engine/enrichment.py:L1 | neighbors=[enrichment.py, EpssDB, KevDB, Finding, VulnDB] | lang=pt
- "detection_engine_enrichment_rationale_33": "Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr" | kind=entity | source=manager/detection_engine/enrichment.py:L33 | neighbors=[enrich_finding(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_enrichment_rationale_53": "Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li" | kind=entity | source=manager/detection_engine/enrichment.py:L53 | neighbors=[_compute_priority(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_exploitability_assess": "assess()" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L130 | neighbors=[exploitability.py, apply_to_findings(), kev_links_for(), _tier(), Exploitability evidence for one posture…] | lang=en
- "detection_engine_ingest_quarantinedline": "QuarantinedLine" | kind=code-symbol | source=manager/detection_engine/ingest.py:L42 | neighbors=[ingest.py, ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_pipeline_run_pipeline": "run_pipeline()" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L45 | neighbors=[pipeline.py, ab_evaluate(), exposure: optional {asset_ip: {"interne…, run_full_detection(), exposure: optional {asset_ip: {"interne…] | lang=en
- "detection_engine_port_intel_classify_port": "classify_port()" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L211 | neighbors=[port_intel.py, _banner_confirms_backdoor(), contradicts_port_hypothesis(), PortRisk, Map an open TCP port (+ optional banner…] | lang=en
- "detection_engine_posture_confidence": "posture_confidence.py" | kind=code-symbol | source=manager/detection_engine/posture_confidence.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, assess_confidence(), calibrate_host_findings(), corroborating_chains(), posture_confidence.py — calibrated, aud…] | lang=en
- "detection_engine_posture_rules_posturefinding": "PostureFinding" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L169 | neighbors=[posture_rules.py, detect_exposed_services(), detect_posture_traced(), .__post_init__(), .to_dict()] | lang=en
- "detection_engine_posture_rules_tracerow": "TraceRow" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L111 | neighbors=[posture_rules.py, detect_posture_traced(), evaluate_rule(), One rule evaluation's outcome. Purely d…, .to_dict()] | lang=en
- "detection_engine_update_snapshot_sync_epss_snapshot": "sync_epss_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L141 | neighbors=[update_snapshot.py, EPSS scores for exactly the CVE IDs thi…, _ssl_context(), main(), EPSS scores for exactly the CVE IDs thi…] | lang=en
- "detection_engine_update_snapshot_sync_kev_snapshot": "sync_kev_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L120 | neighbors=[update_snapshot.py, main(), The full CISA Known Exploited Vulnerabi…, _ssl_context(), The full CISA Known Exploited Vulnerabi…] | lang=en
- "detection_engine_version_compare_dpkg_compare": "dpkg_compare()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L172 | neighbors=[version_compare.py, _dpkg_compare_pure_python(), -1 if a<b, 0 if a==b, 1 if a>b, per Deb…, _dpkg_compare_via_binary(), -1 if a<b, 0 if a==b, 1 if a>b, per Deb…] | lang=en
- "detection_engine_version_compare_dpkg_compare_pure_python": "_dpkg_compare_pure_python()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L161 | neighbors=[version_compare.py, dpkg_compare(), _compare_part(), _split_dpkg_version(), verify_pure_python_matches_dpkg()] | lang=en
- "detection_engine_version_compare_dpkg_compare_via_binary": "_dpkg_compare_via_binary()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L36 | neighbors=[version_compare.py, Real dpkg --compare-versions. None (not…, verify_pure_python_matches_dpkg(), dpkg_compare(), Real dpkg --compare-versions. None (not…] | lang=en
- "detection_engine_version_compare_split_dpkg_version": "_split_dpkg_version()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L110 | neighbors=[version_compare.py, _dpkg_compare_pure_python(), has_ambiguous_epoch(), 1:8.4p1-5+deb11u1' -> (epoch='1', upstr…, 1:8.4p1-5+deb11u1' -> (epoch='1', upstr…] | lang=en
- "detection_logger": "logger.py" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _as_uuid(), AttackLogger, AttackLogger — records every attack act…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_resolution_evaluate_resolutions": "evaluate_resolutions()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L100 | neighbors=[resolution.py, decide_resolution(), Apply decide_resolution to every engine…, Apply decide_resolution to every engine…, Apply decide_resolution to every engine…] | lang=en
- "detection_resolution_resolution_threshold": "resolution_threshold()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L67 | neighbors=[resolution.py, decide_resolution(), Consecutive coverage-proven clean runs …, Consecutive coverage-proven clean runs …, Consecutive coverage-proven clean runs …] | lang=en
- "detection_sigma_sigmarulegenerator_generate_sigma_for_technique": ".generate_sigma_for_technique()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L109 | neighbors=[Return a Sigma rule (YAML string) for t…, SigmaRuleGenerator, ._customise_detection(), ._lookup_template(), _stable_rule_id()] | lang=en
- "detection_verification_compute_verdict": "compute_verdict()" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L45 | neighbors=[verification.py, _int_confidence(), VerificationVerdict, Deterministic passive verdict from a de…, verify_finding()] | lang=en
- "detection_verification_verify_finding": "verify_finding()" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L82 | neighbors=[verification.py, Deterministic verdict, optionally enric…, compute_verdict(), _qualifies_for_llm(), VerificationVerdict] | lang=en
- "discovery_finding_translator_escalate_by_exposure": "_escalate_by_exposure()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L106 | neighbors=[finding_translator.py, create_findings_from_probe_result(), _finding_port(), Bump severity one rung when the finding…, Bump severity one rung when the finding…] | lang=en
- "discovery_finding_translator_resolve_asset": "_resolve_asset()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L54 | neighbors=[finding_translator.py, create_findings_from_probe_result(), Find the Asset for a probe-reported tar…, Find the Asset for a probe-reported tar…, Find the Asset for a probe-reported tar…] | lang=en
- "discovery_rate_limiter_ratelimiter_acquire": ".acquire()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L60 | neighbors=[RateLimiter, ._consume_token(), .is_within_window(), ._resolve_cidr(), Blocks until a token is available for t…] | lang=en
- "discovery_worker_discoveryworker_run": ".run()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L68 | neighbors=[DiscoveryWorker, ._banner_grab_all(), ._run_nmap(), ._save_assets(), ._set_status()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-054.json

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
