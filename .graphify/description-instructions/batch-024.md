# Node Description Batch 25 of 209

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

- "agent_license_check_license": "check_license()" | kind=code-symbol | source=probe/agent/license.py:L84 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…]
- "agent_result_spool_resultspool_path": "._path()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .exists(), .flush_spool(), .load(), .quarantine(), .remove()]
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=probe/agent/result_spool.py:L68 | neighbors=[Atomically write a result payload to th…, ResultSpool, ._path(), ._sync_directory(), .submit_with_retry(), Atomically write a result payload to th…]
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L129 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .quarantine(), .remove(), .save(), Attempt to upload a result with retries…]
- "agent_task_runner_taskrunner_run_job": ".run_job()" | kind=code-symbol | source=probe/agent/task_runner.py:L88 | neighbors=[Execute a complete scan job lifecycle. …, TaskRunner, JobResult, ._submit_or_spool(), Execute a complete scan job lifecycle. …, Execute a complete scan job lifecycle. …]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L442 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L626 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError, Establish an authenticated WebSocket co…, Establish an authenticated WebSocket co…]
- "agent_transport_transport_load_state": ".load_state()" | kind=code-symbol | source=probe/agent/transport.py:L170 | neighbors=[Transport, .activate_enrollment(), .ensure_device_access(), .__init__(), .refresh_device_access(), .refresh_registration()]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L498 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L412 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError, Refresh routing metadata using the cach…]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L214 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …, Register the probe with the manager.   …]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L234 | neighbors=[use_cases.py, Return (scan_type, profile, intensity) …, normalize_intensity(), use_case_for_code(), Return (scan_type, profile, intensity) …, Return (scan_type, profile) for a job. …]
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L285 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()]
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L245 | neighbors=[main.py, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…]
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts]
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()]
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()]
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()]
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1963 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1697 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()]
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1622 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@6a1c958273a695fdfb8a8e43254742b6436b3b8e": "6a1c958 docs(plans): record execution status for active-validation + risk-rank …" | kind=Commit | source=git | neighbors=[50d6554 feat(active-validation): approv…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 8ebc053 feat(risk-rank-ui): surface ver…]
- "detection_edr_edrqueryengine": "EDRQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L62 | neighbors=[edr.py, CrowdStrikeFalcon, .__init__(), .query_detections(), ._request(), MicrosoftDefender]
- "detection_engine_ai_normalizer_ainormalizercache_get": ".get()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L152 | neighbors=[AINormalizerCache, ._key(), .propose_cpe(), extract_raw_text(), .propose_cpe(), propose_candidates()]
- "detection_engine_bridge_rationale_112": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L112 | neighbors=[_apply_regression_reopen(), create_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus]
- "detection_engine_correlate": "correlate.py" | kind=code-symbol | source=manager/detection_engine/correlate.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, correlate_smb_patch(), dedup_findings(), _product_from_cpe(), suppress_negated(), correlate.py — dedup, authoritative-sup…]
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L91 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()]
- "detection_engine_vuln_db_read_snapshot": "_read_snapshot()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L156 | neighbors=[vuln_db.py, load_snapshot(), The actual parse + integrity-verify + b…, _boundary_versions(), _content_hash(), SnapshotMeta]
- "detection_sigma": "sigma.py" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma d…, 2885afa Add comprehensive probe testing…]
- "detection_vantage_fusion": "vantage_fusion.py" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _collect(), fuse_exposure_results(), fused_service_exposure(), _is_external(), _verdict()]
- "discovery_finding_translator_create_findings_from_probe_result": "create_findings_from_probe_result()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L141 | neighbors=[finding_translator.py, _escalate_by_exposure(), _find_open_duplicate(), _map_severity(), _resolve_asset(), Convert a probe's self-assessed `findin…]
- "discovery_finding_translator_rationale_98": "Bump severity one rung when the finding's service is internet-reachable     (Ser" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L98 | neighbors=[_escalate_by_exposure(), create_findings_from_probe_result(), Asset, AssetType, FindingSeverity, FindingStatus]
- "discovery_worker": "worker.py" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …]
- "discovery_xml_parser": "xml_parser.py" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NmapXMLParser, ParsedHost, ParsedPort, Nmap XML output parser. Converts -oX ou…]
- "discovery_xml_parser_parsedport": "ParsedPort" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L12 | neighbors=[xml_parser.py, ._parse_port(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "engine_tool_runners_binname": "binName()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L77 | neighbors=[tool-runners.ts, bin(), isWindows(), runHostDiscovery(), runSshAudit(), runTestssl()]
- "engine_tool_runners_runnaabu": "runNaabu()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L146 | neighbors=[scanner.ts, tool-runners.ts, bin(), hasBinary(), spawnOpts(), streamProcess()]
- "engine_types_scancallbacks": "ScanCallbacks" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L109 | neighbors=[agent.py, tools.ts, interactive.ts, scan.ts, scanner.ts, tool-runners.ts]
- "engine_types_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[findings.ts, scanner.ts, types.ts, finding-id.ts, findings-store.ts, nuclei-parser.ts]
- "enrollment_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/fleet/enrollment/route.ts:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, GET, POST, backend.ts, backend(), with-backend.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-024.json

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
