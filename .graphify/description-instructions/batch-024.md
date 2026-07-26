# Node Description Batch 25 of 104

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

- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L44 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable()] | lang=en
- "detection_engine_consistency_aggregate": "aggregate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L100 | neighbors=[consistency.py, ConsistencyReport, FindingConsistency, run_findings: one list of Findings per …] | lang=en
- "detection_engine_cvss_base_score": "base_score()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L43 | neighbors=[cvss.py, parse_vector(), _roundup(), Returns the CVSS v3.1 base score (0.0-1…] | lang=en
- "detection_engine_enrichment": "enrichment.py" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _compute_priority(), enrich_finding(), enrichment.py — join CVSS + KEV + EPSS …] | lang=en
- "detection_engine_ingest_rationale_1": "ingest.py — stream-read scanner_module JSONL output, validate, assemble per-host" | kind=entity | source=manager/detection_engine/ingest.py:L1 | neighbors=[ingest.py, Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_100": "Stream-read one JSONL file, validating and assembling Assets as it goes.      Pa" | kind=entity | source=manager/detection_engine/ingest.py:L100 | neighbors=[ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_60": "Returns an error reason string if invalid, else None." | kind=entity | source=manager/detection_engine/ingest.py:L60 | neighbors=[_validate(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_83": "Real, verified hostname-alias sources in scanner_module's output —     deliberat" | kind=entity | source=manager/detection_engine/ingest.py:L83 | neighbors=[_extract_aliases(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_matcher_version_in_ranges": "_version_in_ranges()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L44 | neighbors=[matcher.py, match_candidate(), Returns (matched, matched_interval_desc…, _safe_compare()] | lang=en
- "detection_engine_pipeline": "pipeline.py" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ab_evaluate(), run_pipeline(), pipeline.py — Phase 1 + Phase 2 end to …] | lang=en
- "detection_engine_update_snapshot_query_osv": "_query_osv()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L54 | neighbors=[update_snapshot.py, _ssl_context(), All known vulnerabilities OSV has for t…, sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_sync_epss_snapshot": "sync_epss_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L138 | neighbors=[update_snapshot.py, main(), EPSS scores for exactly the CVE IDs thi…, _ssl_context()] | lang=en
- "detection_engine_update_snapshot_sync_kev_snapshot": "sync_kev_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L117 | neighbors=[update_snapshot.py, main(), The full CISA Known Exploited Vulnerabi…, _ssl_context()] | lang=en
- "detection_engine_update_snapshot_sync_snapshot": "sync_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L76 | neighbors=[update_snapshot.py, main(), Fetch real OSV records for every produc…, _query_osv()] | lang=en
- "detection_engine_verifier_rationale_1": "verifier.py — Phase 3: the generalized verifier, the anti-false-positive backbon" | kind=entity | source=manager/detection_engine/verifier.py:L1 | neighbors=[Finding, FindingState, SourceConfidence, verifier.py] | lang=en
- "detection_engine_verifier_rationale_52": "The scanner names behind this finding's evidence refs. A ref looks     like 'fil" | kind=entity | source=manager/detection_engine/verifier.py:L52 | neighbors=[Finding, FindingState, SourceConfidence, _evidence_scanners()] | lang=en
- "detection_engine_verifier_rationale_76": "A starter honeypot/deception heuristic (0.0-1.0). Real hosts run a     handful o" | kind=entity | source=manager/detection_engine/verifier.py:L76 | neighbors=[Finding, FindingState, SourceConfidence, deception_score()] | lang=pt
- "detection_engine_verifier_rationale_96": "Calibrate and stamp a Finding. Mutates and returns it.      reachability: \"open\"" | kind=entity | source=manager/detection_engine/verifier.py:L96 | neighbors=[Finding, FindingState, SourceConfidence, verify()] | lang=en
- "detection_engine_version_compare_dpkg_compare": "dpkg_compare()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L166 | neighbors=[version_compare.py, _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), -1 if a<b, 0 if a==b, 1 if a>b, per Deb…] | lang=en
- "detection_engine_version_compare_dpkg_compare_pure_python": "_dpkg_compare_pure_python()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L155 | neighbors=[version_compare.py, dpkg_compare(), _compare_part(), _split_dpkg_version()] | lang=en
- "detection_engine_version_compare_split_dpkg_version": "_split_dpkg_version()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L104 | neighbors=[version_compare.py, _dpkg_compare_pure_python(), has_ambiguous_epoch(), 1:8.4p1-5+deb11u1' -> (epoch='1', upstr…] | lang=en
- "detection_engine_vuln_db_load_snapshot": "load_snapshot()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L119 | neighbors=[vuln_db.py, _content_hash(), SnapshotMeta, VulnDB] | lang=en
- "detection_logger": "logger.py" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _as_uuid(), AttackLogger, AttackLogger — records every attack act…] | lang=en
- "detection_logger_attacklogger": "AttackLogger" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L23 | neighbors=[logger.py, .__init__(), .log_action(), AttackTimeline] | lang=en
- "detection_siem_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L35 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_siem_siemqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L68 | neighbors=[.query_alerts(), .query_alerts(), SIEMQueryEngine, .query_alerts()] | lang=en
- "discovery_service_id": "service_id.py" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ServiceFingerprint, ServiceIdentifier, ServiceIdentifier — banner + port → str…] | lang=en
- "discovery_xml_parser_nmapxmlparser_parse_host": "._parse_host()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L53 | neighbors=[NmapXMLParser, .parse(), ._parse_port(), ParsedHost] | lang=en
- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, GET(), ai-engine.ts, aiReportStore] | lang=en
- "e2e_mock_manager_quietserver": "_QuietServer" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L221 | neighbors=[mock_manager.py, .handle_error(), ThreadingHTTPServer, start()] | lang=en
- "engine_tool_runners_iswindows": "isWindows()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L28 | neighbors=[tool-runners.ts, binName(), hasSystemBinary(), spawnOpts()] | lang=en
- "engine_types_scansummary": "ScanSummary" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L119 | neighbors=[llm.ts, scanner.ts, types.ts, output.ts] | lang=en
- "exploit_msf_client": "msf_client.py" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, MetasploitRPCClient, MetasploitRPCError, MetasploitRPCClient — async client for …] | lang=en
- "exploit_msf_client_metasploitrpcclient_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L38 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, Authenticate with msfrpcd and store the…] | lang=en
- "exploit_msf_client_metasploitrpcclient_get_job_status": ".get_job_status()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L102 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns {status, output, uuid}.] | lang=en
- "exploit_msf_client_metasploitrpcclient_kill_job": ".kill_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L118 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns True if job was successfully ki…] | lang=en
- "exploit_msf_client_metasploitrpcclient_raw_call": "._raw_call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L157 | neighbors=[MetasploitRPCClient, ._call(), .connect(), MetasploitRPCError] | lang=en
- "exploit_msf_client_metasploitrpcclient_run_module": ".run_module()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L83 | neighbors=[MetasploitRPCClient, ._call(), MetasploitRPCError, Execute a Metasploit module.         Re…] | lang=en
- "exploit_msf_client_metasploitrpcclient_wait_for_job": ".wait_for_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L132 | neighbors=[MetasploitRPCClient, .get_job_status(), .kill_job(), Poll until job completes or max_wait ex…] | lang=en
- "exploit_nuclei_exploit_nucleiexploitrunner_parse_poc_output": "._parse_poc_output()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L160 | neighbors=[NucleiExploitRunner, ._extract_evidence(), .run_cve_poc(), Parse nuclei JSONL output for a single …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-024.json

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
