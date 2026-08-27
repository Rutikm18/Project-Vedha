# Node Description Batch 41 of 236

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

- "dashboard_slastatus_slarowview": "SlaRowView()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L122 | neighbors=[SlaStatus.tsx, deadlineTitle(), elapsedPct(), timeLabel(), pct()] | lang=en
- "detection_attack_paths_group": "_group()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L130 | neighbors=[attack_paths.py, attack_path_findings(), _HostSignals, .finalize(), .observe()] | lang=en
- "detection_correlator_detectioncorrelator_correlate": ".correlate()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L82 | neighbors=[DetectionCorrelator, ._host_for(), ._in_window(), ._min_latency(), DetectionResultDTO] | lang=en
- "detection_correlator_rationale_1": "DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale" | kind=entity | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_correlator_rationale_210": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L210 | neighbors=[_aware(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_build_nvd_cpe_snapshot": "build_nvd_cpe_snapshot.py" | kind=code-symbol | source=manager/detection_engine/build_nvd_cpe_snapshot.py:L1 | neighbors=[d0d1931 feat(detection): NVD/CPE vuln f…, _content_hash(), main(), _rec(), build_nvd_cpe_snapshot.py — generate th…] | lang=en
- "detection_engine_enrichment": "enrichment.py" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _compute_priority(), enrich_finding(), enrichment.py — join CVSS + KEV + EPSS …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_enrichment_db_epssdb_get": ".get()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L29 | neighbors=[EpssDB, load_epss(), load_kev(), {'epss': float, 'percentile': float} or…, {'epss': float, 'percentile': float} or…] | lang=en
- "detection_engine_enrichment_rationale_1": "enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier." | kind=entity | source=manager/detection_engine/enrichment.py:L1 | neighbors=[enrichment.py, EpssDB, KevDB, Finding, VulnDB] | lang=pt
- "detection_engine_enrichment_rationale_33": "Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr" | kind=entity | source=manager/detection_engine/enrichment.py:L33 | neighbors=[enrich_finding(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_enrichment_rationale_53": "Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li" | kind=entity | source=manager/detection_engine/enrichment.py:L53 | neighbors=[_compute_priority(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_ingest_quarantinedline": "QuarantinedLine" | kind=code-symbol | source=manager/detection_engine/ingest.py:L35 | neighbors=[ingest.py, ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_pipeline": "pipeline.py" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ab_evaluate(), run_pipeline(), pipeline.py — Phase 1 + Phase 2 end to …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_update_snapshot_sync_epss_snapshot": "sync_epss_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L141 | neighbors=[update_snapshot.py, EPSS scores for exactly the CVE IDs thi…, _ssl_context(), main(), EPSS scores for exactly the CVE IDs thi…] | lang=en
- "detection_engine_update_snapshot_sync_kev_snapshot": "sync_kev_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L120 | neighbors=[update_snapshot.py, main(), The full CISA Known Exploited Vulnerabi…, _ssl_context(), The full CISA Known Exploited Vulnerabi…] | lang=en
- "detection_engine_version_compare_dpkg_compare": "dpkg_compare()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L172 | neighbors=[version_compare.py, _dpkg_compare_pure_python(), -1 if a<b, 0 if a==b, 1 if a>b, per Deb…, _dpkg_compare_via_binary(), -1 if a<b, 0 if a==b, 1 if a>b, per Deb…] | lang=en
- "detection_engine_version_compare_dpkg_compare_pure_python": "_dpkg_compare_pure_python()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L161 | neighbors=[version_compare.py, dpkg_compare(), _compare_part(), _split_dpkg_version(), verify_pure_python_matches_dpkg()] | lang=en
- "detection_engine_version_compare_dpkg_compare_via_binary": "_dpkg_compare_via_binary()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L36 | neighbors=[version_compare.py, Real dpkg --compare-versions. None (not…, verify_pure_python_matches_dpkg(), dpkg_compare(), Real dpkg --compare-versions. None (not…] | lang=en
- "detection_engine_version_compare_split_dpkg_version": "_split_dpkg_version()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L110 | neighbors=[version_compare.py, _dpkg_compare_pure_python(), has_ambiguous_epoch(), 1:8.4p1-5+deb11u1' -> (epoch='1', upstr…, 1:8.4p1-5+deb11u1' -> (epoch='1', upstr…] | lang=en
- "detection_logger": "logger.py" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _as_uuid(), AttackLogger, AttackLogger — records every attack act…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_prioritization_prioritize_engagement_findings": "prioritize_engagement_findings()" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L113 | neighbors=[prioritization.py, composite_risk_score(), _load_offline_kev_epss(), _strongest_exposure(), (Re)compute risk_score for every still-…] | lang=en
- "detection_resolution_decide_resolution": "decide_resolution()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L71 | neighbors=[resolution.py, resolution_threshold(), ResolutionOutcome, evaluate_resolutions(), Pure heart of auto-resolution. Given wh…] | lang=en
- "detection_sigma_sigmarulegenerator_generate_sigma_for_technique": ".generate_sigma_for_technique()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L109 | neighbors=[Return a Sigma rule (YAML string) for t…, SigmaRuleGenerator, ._customise_detection(), ._lookup_template(), _stable_rule_id()] | lang=en
- "detection_verification_compute_verdict": "compute_verdict()" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L45 | neighbors=[verification.py, _int_confidence(), VerificationVerdict, Deterministic passive verdict from a de…, verify_finding()] | lang=en
- "detection_verification_verify_finding": "verify_finding()" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L82 | neighbors=[verification.py, Deterministic verdict, optionally enric…, compute_verdict(), _qualifies_for_llm(), VerificationVerdict] | lang=en
- "discovery_finding_translator_find_open_duplicate": "_find_open_duplicate()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L121 | neighbors=[finding_translator.py, create_findings_from_probe_result(), create_scan_health_finding(), A still-relevant Finding with the same …, A still-relevant Finding with the same …] | lang=en
- "discovery_rate_limiter_ratelimiter_acquire": ".acquire()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L60 | neighbors=[RateLimiter, ._consume_token(), .is_within_window(), ._resolve_cidr(), Blocks until a token is available for t…] | lang=en
- "discovery_worker_discoveryworker_run": ".run()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L68 | neighbors=[DiscoveryWorker, ._banner_grab_all(), ._run_nmap(), ._save_assets(), ._set_status()] | lang=en
- "engine_scanner_runscan": "runScan()" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L17 | neighbors=[tools.ts, interactive.ts, scan.ts, scanner.ts, bySeverityCount()] | lang=en
- "engine_tool_runners_rundbenum": "runDbEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1327 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), spawnOpts()] | lang=en
- "engine_tool_runners_runhttpx": "runHttpx()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L689 | neighbors=[scanner.ts, tool-runners.ts, bin(), hasBinary(), spawnOpts()] | lang=en
- "engine_tool_runners_runnuclei": "runNuclei()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L407 | neighbors=[scanner.ts, tool-runners.ts, bin(), spawnOpts(), streamProcess()] | lang=en
- "engine_tool_runners_runsshaudit": "runSshAudit()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L962 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts()] | lang=en
- "engine_tool_runners_runsubfinder": "runSubfinder()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L666 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), spawnOpts()] | lang=en
- "engine_tool_runners_runtestssl": "runTestssl()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L506 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts()] | lang=en
- "engine_types_scanoptions": "ScanOptions" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L36 | neighbors=[tools.ts, interactive.ts, scan.ts, scanner.ts, types.ts] | lang=en
- "exploit_msf_client": "msf_client.py" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, MetasploitRPCClient, MetasploitRPCError, MetasploitRPCClient — async client for …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "exploit_nuclei_exploit": "nuclei_exploit.py" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NucleiExploitRunner, NucleiExploitRunner — CVE PoC validatio…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "exploit_nuclei_exploit_nucleiexploitrunner_parse_poc_output": "._parse_poc_output()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L159 | neighbors=[NucleiExploitRunner, ._extract_evidence(), .run_cve_poc(), Parse nuclei JSONL output for a single …, Parse nuclei JSONL output for a single …] | lang=en
- "gaps_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/gaps/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET(), detectionStore, 298a9d4 trim frontend to 7 core pages; …, detection-store.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-040.json

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
