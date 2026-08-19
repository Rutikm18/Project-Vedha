# Node Description Batch 27 of 227

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

- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L286 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()]
- "ai_llm_report_llmreportgenerator_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L245 | neighbors=[LLMReportGenerator, ._complete(), _normalize_ai_plan(), _parse_json_response(), _remediation_plan_prompt(), Generate a STRUCTURED, OS-specific reme…]
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts]
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()]
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()]
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()]
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1963 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1697 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()]
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1622 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2de251b6a34cad99831e042cf014ca1bcfa6aed2": "2de251b feat(scanner): ICMP timestamp fallback — echo-filter bypass + clock har…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, main, 9c973dd feat(scanner): tarpit/honeypot …, os_fingerprint.py, os_fingerprint.py, test_os_fingerprint.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@daf3de2734a3efdd04df485c8544d56209bd5554": "daf3de2 feat(scanner): add service enumeration and enrichment layer" | kind=Commit | source=git | neighbors=[6be8259 feat(integrations): outbox deli…, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, 37376de hardening(scanner): OPSEC de-si…]
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
- "exploit_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, 2885afa Add comprehensive probe testing…]
- "graph_builder_graphbuilder_add_exploit_edges": ".add_exploit_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L183 | neighbors=[GraphBuilder, asset_node_id(), exploit_complexity(), finding_node_id(), _to_float(), .build_asset_graph()]
- "graph_demo": "demo.py" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-p…]
- "graph_demo_demoasset": "DemoAsset" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L27 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "graph_demo_demofinding": "DemoFinding" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L45 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "kind_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/integrations/[kind]/route.ts:L1 | neighbors=[00c6648 feat(settings): editable email/…, DELETE(), PUT(), backend.ts, backend(), BackendError]
- "lib_findings_store_savefindings": "saveFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L51 | neighbors=[tools.ts, findings-store.ts, createFinding(), ensureDir(), getAllFindings(), slaDeadline()]
- "lib_httpx_parser_httpxjsonldecoder": "HttpxJsonlDecoder" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L93 | neighbors=[tool-runners.ts, httpx-parser.ts, .decode(), .finish(), .malformedLines(), .push()]
- "lib_security_context_securitycontexterror": "SecurityContextError" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L9 | neighbors=[route.ts, route.ts, route.ts, security-context.ts, publicCveRecord(), resolveSecurityReference()]
- "main_scripts_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L160 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()]
- "main_scripts_findings_main": "_main()" | kind=code-symbol | source=probe/main_scripts/findings.py:L684 | neighbors=[findings.py, .to_dict(), load_facts_jsonl(), run_findings(), summarize(), CLI: derive findings from one or more s…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-026.json

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
