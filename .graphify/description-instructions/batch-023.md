# Node Description Batch 24 of 119

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

- "cli_auth_serverurl": "serverUrl()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L42 | neighbors=[auth.ts, apiFetch(), doctor.ts, interactive.ts, login.ts] | lang=en
- "commands_interactive_runinteractive": "runInteractive()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2102 | neighbors=[index.ts, interactive.ts, banner(), ensureAuthenticated(), mainMenu()] | lang=en
- "commands_interactive_runphaseexploitation": "runPhaseExploitation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1070 | neighbors=[interactive.ts, runIterativeEngagement(), choose(), confirm(), ln()] | lang=en
- "commands_interactive_runphaseportscan": "runPhasePortScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1028 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()] | lang=en
- "commands_interactive_runphaseservicedetect": "runPhaseServiceDetect()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1037 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()] | lang=en
- "commands_interactive_runphasevulnassess": "runPhaseVulnAssess()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1051 | neighbors=[interactive.ts, runIterativeEngagement(), confirm(), ln(), runPhaseWithTools()] | lang=en
- "commands_interactive_runvulnassessmentflow": "runVulnAssessmentFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1184 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow(), wizardScan()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/probe-usecase-alignment, main, spike/probe-go, f5ce592 first commit] | lang=en
- "dashboard_slasummarycell": "SlaSummaryCell.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaSummaryCell.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, SlaSummaryCell(), SlaSummaryMetric, 298a9d4 trim frontend to 7 core pages; …, page.tsx] | lang=en
- "detection_correlator_detectioncorrelator_correlate": ".correlate()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L82 | neighbors=[DetectionCorrelator, ._host_for(), ._in_window(), ._min_latency(), DetectionResultDTO] | lang=en
- "detection_correlator_rationale_1": "DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale" | kind=entity | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_correlator_rationale_210": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L210 | neighbors=[_aware(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_bridge_create_findings_from_facts": "create_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L108 | neighbors=[engine_bridge.py, detect_findings_from_facts(), _vuln_db_meta(), New raw-facts path: detect CVE findings…, run_detection_job()] | lang=en
- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L315 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…] | lang=en
- "detection_engine_enrichment": "enrichment.py" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _compute_priority(), enrich_finding(), enrichment.py — join CVSS + KEV + EPSS …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_enrichment_rationale_1": "enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier." | kind=entity | source=manager/detection_engine/enrichment.py:L1 | neighbors=[enrichment.py, EpssDB, KevDB, Finding, VulnDB] | lang=pt
- "detection_engine_enrichment_rationale_33": "Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr" | kind=entity | source=manager/detection_engine/enrichment.py:L33 | neighbors=[EpssDB, KevDB, enrich_finding(), Finding, VulnDB] | lang=en
- "detection_engine_enrichment_rationale_53": "Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li" | kind=entity | source=manager/detection_engine/enrichment.py:L53 | neighbors=[_compute_priority(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_ingest_quarantinedline": "QuarantinedLine" | kind=code-symbol | source=manager/detection_engine/ingest.py:L35 | neighbors=[ingest.py, ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_pipeline": "pipeline.py" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ab_evaluate(), run_pipeline(), pipeline.py — Phase 1 + Phase 2 end to …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_update_snapshot_main": "main()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L184 | neighbors=[update_snapshot.py, _all_known_cve_ids(), sync_epss_snapshot(), sync_kev_snapshot(), sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_ssl_context": "_ssl_context()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L37 | neighbors=[update_snapshot.py, _query_osv(), Some macOS python.org installs ship exp…, sync_epss_snapshot(), sync_kev_snapshot()] | lang=en
- "detection_logger": "logger.py" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _as_uuid(), AttackLogger, AttackLogger — records every attack act…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_sigma_sigmarulegenerator_generate_sigma_for_technique": ".generate_sigma_for_technique()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L109 | neighbors=[Return a Sigma rule (YAML string) for t…, SigmaRuleGenerator, ._customise_detection(), ._lookup_template(), _stable_rule_id()] | lang=en
- "discovery_finding_translator_create_findings_from_probe_result": "create_findings_from_probe_result()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L95 | neighbors=[finding_translator.py, _find_open_duplicate(), _map_severity(), _resolve_asset(), Convert a probe's self-assessed `findin…] | lang=en
- "discovery_rate_limiter_ratelimiter_acquire": ".acquire()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L60 | neighbors=[RateLimiter, ._consume_token(), .is_within_window(), ._resolve_cidr(), Blocks until a token is available for t…] | lang=en
- "discovery_service_id": "service_id.py" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ServiceFingerprint, ServiceIdentifier, ServiceIdentifier — banner + port → str…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
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
- "exploit_nuclei_exploit_nucleiexploitrunner_parse_poc_output": "._parse_poc_output()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L159 | neighbors=[NucleiExploitRunner, ._extract_evidence(), .run_cve_poc(), Parse nuclei JSONL output for a single …, Parse nuclei JSONL output for a single …] | lang=en
- "gaps_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/gaps/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET(), detectionStore, 298a9d4 trim frontend to 7 core pages; …, detection-store.ts] | lang=en
- "graph_analyzer_pathanalyzer_find_paths_to_target": ".find_paths_to_target()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L140 | neighbors=[PathAnalyzer, ._materialise_path(), .movement_graph(), ._source_assets(), Return scored attack paths from every s…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-023.json

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
