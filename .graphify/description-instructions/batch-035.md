# Node Description Batch 36 of 336

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

- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1697 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()] | lang=en
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1622 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0236a6011fa2a49e65e7f5cad6b04f643f83c6f7": "0236a60 fix(detection): full EPSS catalog so exploit-probability isn't blind" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, d98f654 feat(manager): network-VA campa…, update_snapshot.py] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd853230be2d89a28a641677bd8900d3071b1186": "bd85323 feat(probe): self-heal re-enroll, local-run driver, WS send resilience" | kind=Commit | source=git | neighbors=[agent.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, bf61dbc docs: probe run/test guide; git…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@dbcff7fc782d1da19c2bf749b8ac45146179b864": "dbcff7f feat: Update UseCaseCard component for improved description handling an…" | kind=Commit | source=git | neighbors=[b393dbe feat: Enhance Sidebar UI and in…, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, d0d1931 feat(detection): NVD/CPE vuln f…] | lang=en
- "components_refreshbutton": "RefreshButton.tsx" | kind=code-symbol | source=manager/frontend/components/RefreshButton.tsx:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, PageShell.tsx, RefreshButton(), RefreshButtonProps, page.tsx] | lang=en
- "cve_correlator_correlate": "correlate()" | kind=code-symbol | source=probe/cve/correlator.py:L122 | neighbors=[correlator.py, _as_dict(), _backport_marker(), CVEFinding, risk_band(), risk_score()] | lang=en
- "detection_edr_edrqueryengine": "EDRQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L62 | neighbors=[edr.py, CrowdStrikeFalcon, .__init__(), .query_detections(), ._request(), MicrosoftDefender] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache_get": ".get()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L152 | neighbors=[AINormalizerCache, ._key(), .propose_cpe(), extract_raw_text(), .propose_cpe(), propose_candidates()] | lang=en
- "detection_engine_bridge_persist_posture_findings": "_persist_posture_findings()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L321 | neighbors=[engine_bridge.py, create_findings_from_facts(), _apply_regression_reopen(), _find_remediated_match(), _posture_description(), _posture_title()] | lang=en
- "detection_engine_bridge_rationale_112": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L112 | neighbors=[_apply_regression_reopen(), create_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus] | lang=en
- "detection_engine_bridge_run_detection_job": "run_detection_job()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L677 | neighbors=[engine_bridge.py, Background entry point (P1: keep detect…, create_findings_from_facts(), Background entry point (P1: keep detect…, Background entry point (P1: keep detect…, Background entry point (P1: keep detect…] | lang=en
- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L55 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable(), (content_hash, fetched_at) of the pinne…, (content_hash, fetched_at) of the pinne…] | lang=en
- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L369 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…, ssh_inventory's dpkg_packages/rpm_packa…] | lang=en
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L91 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()] | lang=en
- "detection_explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L1 | neighbors=[6bb51ab feat: add detection-explain end…, fail(), GET(), backend.ts, backend(), BackendError] | lang=en
- "detection_resolution_decide_resolution": "decide_resolution()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L81 | neighbors=[resolution.py, resolution_threshold(), ResolutionOutcome, evaluate_resolutions(), Pure heart of auto-resolution. Given wh…, Pure heart of auto-resolution. Given wh…] | lang=en
- "detection_sigma": "sigma.py" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma d…, 2885afa Add comprehensive probe testing…] | lang=en
- "detection_vantage_fusion": "vantage_fusion.py" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _collect(), fuse_exposure_results(), fused_service_exposure(), _is_external(), _verdict()] | lang=en
- "discovery_finding_translator_rationale_98": "Bump severity one rung when the finding's service is internet-reachable     (Ser" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L98 | neighbors=[_escalate_by_exposure(), create_findings_from_probe_result(), Asset, AssetType, FindingSeverity, FindingStatus] | lang=en
- "discovery_service_vuln": "service_vuln.py" | kind=code-symbol | source=manager/backend/app/discovery/service_vuln.py:L1 | neighbors=[3565ada fix(ingest): NUL-safe result su…, _cleartext_rule(), create_service_vuln_findings(), _http_rules(), _new_finding(), _ssh_rules()] | lang=en
- "discovery_worker": "worker.py" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …] | lang=en
- "discovery_xml_parser": "xml_parser.py" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NmapXMLParser, ParsedHost, ParsedPort, Nmap XML output parser. Converts -oX ou…] | lang=en
- "discovery_xml_parser_parsedport": "ParsedPort" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L12 | neighbors=[xml_parser.py, ._parse_port(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…] | lang=en
- "engine_tool_runners_binname": "binName()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L77 | neighbors=[tool-runners.ts, bin(), isWindows(), runHostDiscovery(), runSshAudit(), runTestssl()] | lang=en
- "engine_tool_runners_runnaabu": "runNaabu()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L146 | neighbors=[scanner.ts, tool-runners.ts, bin(), hasBinary(), spawnOpts(), streamProcess()] | lang=en
- "engine_types_scancallbacks": "ScanCallbacks" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L114 | neighbors=[agent.py, tools.ts, interactive.ts, scan.ts, scanner.ts, tool-runners.ts] | lang=en
- "engine_types_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[findings.ts, scanner.ts, types.ts, finding-id.ts, findings-store.ts, nuclei-parser.ts] | lang=en
- "enrollment_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/fleet/enrollment/route.ts:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, GET, POST, backend.ts, backend(), with-backend.ts] | lang=en
- "exploit_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, 2885afa Add comprehensive probe testing…] | lang=en
- "graph_builder_graphbuilder_add_exploit_edges": ".add_exploit_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L183 | neighbors=[GraphBuilder, asset_node_id(), exploit_complexity(), finding_node_id(), _to_float(), .build_asset_graph()] | lang=en
- "graph_demo": "demo.py" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-p…] | lang=en
- "graph_demo_demoasset": "DemoAsset" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L27 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "graph_demo_demofinding": "DemoFinding" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L45 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "id_rawfacts": "RawFacts.tsx" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/RawFacts.tsx:L1 | neighbors=[25c014d feat: enhance campaign progress…, CampaignProgress.tsx, Chip(), fetchJson(), RawFacts(), RawFactsResp] | lang=en
- "kind_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/integrations/[kind]/route.ts:L1 | neighbors=[00c6648 feat(settings): editable email/…, DELETE(), PUT(), backend.ts, backend(), BackendError] | lang=en
- "lib_ai_engine_generatereport": "generateReport()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L809 | neighbors=[ai-engine.ts, generateReportSectioned(), generateReportSingleCall(), getClient(), stripFences(), toModelFindings()] | lang=en
- "lib_ai_engine_generatereportsectioned": "generateReportSectioned()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L690 | neighbors=[ai-engine.ts, generateReport(), countSeverities(), getClient(), runSection(), toModelFindings()] | lang=en
- "lib_campaign_store_getcampaign": "getCampaign()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L153 | neighbors=[route.ts, campaign-store.ts, fileFor(), isSafeCampaignId(), validateSnapshot(), listCampaigns()] | lang=en
- "lib_findings_store_savefindings": "saveFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L51 | neighbors=[tools.ts, findings-store.ts, createFinding(), ensureDir(), getAllFindings(), slaDeadline()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-035.json

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
