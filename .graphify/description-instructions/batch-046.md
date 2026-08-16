# Node Description Batch 47 of 209

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

- "detection_engine_ingest_rationale_1": "ingest.py — stream-read scanner_module JSONL output, validate, assemble per-host" | kind=entity | source=manager/detection_engine/ingest.py:L1 | neighbors=[ingest.py, Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_100": "Stream-read one JSONL file, validating and assembling Assets as it goes.      Pa" | kind=entity | source=manager/detection_engine/ingest.py:L100 | neighbors=[ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_60": "Returns an error reason string if invalid, else None." | kind=entity | source=manager/detection_engine/ingest.py:L60 | neighbors=[_validate(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_83": "Real, verified hostname-alias sources in scanner_module's output —     deliberat" | kind=entity | source=manager/detection_engine/ingest.py:L83 | neighbors=[_extract_aliases(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_matcher_version_in_ranges": "_version_in_ranges()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L44 | neighbors=[matcher.py, match_candidate(), Returns (matched, matched_interval_desc…, _safe_compare()] | lang=en
- "detection_engine_update_snapshot_query_osv": "_query_osv()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L54 | neighbors=[update_snapshot.py, _ssl_context(), All known vulnerabilities OSV has for t…, sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_sync_epss_snapshot": "sync_epss_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L138 | neighbors=[update_snapshot.py, main(), EPSS scores for exactly the CVE IDs thi…, _ssl_context()] | lang=en
- "detection_engine_update_snapshot_sync_kev_snapshot": "sync_kev_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L117 | neighbors=[update_snapshot.py, main(), The full CISA Known Exploited Vulnerabi…, _ssl_context()] | lang=en
- "detection_engine_update_snapshot_sync_snapshot": "sync_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L76 | neighbors=[update_snapshot.py, main(), Fetch real OSV records for every produc…, _query_osv()] | lang=en
- "detection_engine_verifier_rationale_1": "verifier.py — Phase 3: the generalized verifier, the anti-false-positive backbon" | kind=entity | source=manager/detection_engine/verifier.py:L1 | neighbors=[verifier.py, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_verifier_rationale_52": "The scanner names behind this finding's evidence refs. A ref looks     like 'fil" | kind=entity | source=manager/detection_engine/verifier.py:L52 | neighbors=[_evidence_scanners(), Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_verifier_rationale_76": "A starter honeypot/deception heuristic (0.0-1.0). Real hosts run a     handful o" | kind=entity | source=manager/detection_engine/verifier.py:L76 | neighbors=[deception_score(), Finding, FindingState, SourceConfidence] | lang=pt
- "detection_engine_verifier_rationale_96": "Calibrate and stamp a Finding. Mutates and returns it.      reachability: \"open\"" | kind=entity | source=manager/detection_engine/verifier.py:L96 | neighbors=[verify(), Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_version_compare_char_order": "_char_order()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L58 | neighbors=[version_compare.py, _compare_non_digit(), dpkg's non-digit character ordering: '~…, dpkg's non-digit character ordering: '~…] | lang=en
- "detection_engine_version_compare_has_ambiguous_epoch": "has_ambiguous_epoch()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L129 | neighbors=[version_compare.py, _split_dpkg_version(), True when exactly one of the two versio…, True when exactly one of the two versio…] | lang=en
- "detection_engine_version_compare_semver_compare": "semver_compare()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L189 | neighbors=[version_compare.py, Plain dotted-numeric comparison for non…, _compare_part(), Plain dotted-numeric comparison for non…] | lang=en
- "detection_exposure_fusion_service": "exposure_fusion_service.py" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, recompute_fused_exposure(), _results_from_scan_rows(), exposure_fusion_service.py — apply mult…] | lang=en
- "detection_logger_attacklogger": "AttackLogger" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L23 | neighbors=[logger.py, .__init__(), .log_action(), AttackTimeline] | lang=en
- "detection_siem_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L35 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_siem_siemqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L68 | neighbors=[.query_alerts(), .query_alerts(), SIEMQueryEngine, .query_alerts()] | lang=en
- "discovery_device_profile": "device_profile.py" | kind=code-symbol | source=manager/backend/app/discovery/device_profile.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, asset_type_for(), device_profiles(), device_profile.py — map a probe device_…] | lang=en
- "discovery_exposure": "exposure.py" | kind=code-symbol | source=manager/backend/app/discovery/exposure.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, escalate_for_exposure(), service_exposure(), exposure.py — reachability-aware risk f…] | lang=en
- "discovery_finding_translator_escalate_by_exposure": "_escalate_by_exposure()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L95 | neighbors=[finding_translator.py, create_findings_from_probe_result(), _finding_port(), Bump severity one rung when the finding…] | lang=en
- "discovery_finding_translator_resolve_asset": "_resolve_asset()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L54 | neighbors=[finding_translator.py, create_findings_from_probe_result(), Find the Asset for a probe-reported tar…, Find the Asset for a probe-reported tar…] | lang=en
- "discovery_rate_limiter": "rate_limiter.py" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, RateLimiter, RateLimiter — enforces PPS limits per C…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "discovery_xml_parser_nmapxmlparser_parse_host": "._parse_host()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L52 | neighbors=[NmapXMLParser, .parse(), ._parse_port(), ParsedHost] | lang=en
- "engine_tool_runners_iswindows": "isWindows()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L30 | neighbors=[tool-runners.ts, binName(), hasSystemBinary(), spawnOpts()] | lang=en
- "engine_types_scansummary": "ScanSummary" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L119 | neighbors=[llm.ts, scanner.ts, types.ts, output.ts] | lang=en
- "exploit_msf_client_metasploitrpcclient_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L38 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, Authenticate with msfrpcd and store the…] | lang=en
- "exploit_msf_client_metasploitrpcclient_get_job_status": ".get_job_status()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L102 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns {status, output, uuid}.] | lang=en
- "exploit_msf_client_metasploitrpcclient_kill_job": ".kill_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L118 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns True if job was successfully ki…] | lang=en
- "exploit_msf_client_metasploitrpcclient_raw_call": "._raw_call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L157 | neighbors=[MetasploitRPCClient, ._call(), .connect(), MetasploitRPCError] | lang=en
- "exploit_msf_client_metasploitrpcclient_run_module": ".run_module()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L83 | neighbors=[MetasploitRPCClient, ._call(), MetasploitRPCError, Execute a Metasploit module.         Re…] | lang=en
- "exploit_msf_client_metasploitrpcclient_wait_for_job": ".wait_for_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L132 | neighbors=[MetasploitRPCClient, .get_job_status(), .kill_job(), Poll until job completes or max_wait ex…] | lang=en
- "exploit_nuclei_exploit_nucleiexploitrunner_run_cve_poc": ".run_cve_poc()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L117 | neighbors=[NucleiExploitRunner, ._parse_poc_output(), Run Nuclei CVE PoC template against tar…, Run Nuclei CVE PoC template against tar…] | lang=en
- "exploit_orchestrator_exploitorchestrator_check_approval_required": "._check_approval_required()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L287 | neighbors=[ExploitOrchestrator, .execute(), Creates and returns an ExploitApprovalR…, Creates and returns an ExploitApprovalR…] | lang=en
- "exploit_orchestrator_exploitorchestrator_check_blast_radius": "._check_blast_radius()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L265 | neighbors=[ExploitOrchestrator, .execute(), Count running exploit jobs for this eng…, Count running exploit jobs for this eng…] | lang=en
- "exploit_orchestrator_exploitorchestrator_select_exploit": ".select_exploit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L67 | neighbors=[ExploitOrchestrator, .execute(), Returns {module, payload, safe_check} f…, Returns {module, payload, safe_check} f…] | lang=en
- "exploit_orchestrator_exploitorchestrator_validate_safety": ".validate_safety()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L103 | neighbors=[ExploitOrchestrator, .execute(), Raises SafetyViolationError if module o…, Raises SafetyViolationError if module o…] | lang=en
- "exploit_orchestrator_exploitorchestrator_validate_scope": ".validate_scope()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L110 | neighbors=[ExploitOrchestrator, .execute(), Raises OutOfScopeError if target_ip not…, Raises OutOfScopeError if target_ip not…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-046.json

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
