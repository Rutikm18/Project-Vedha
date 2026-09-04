# Node Description Batch 36 of 332

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

- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L369 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…, ssh_inventory's dpkg_packages/rpm_packa…]
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L91 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()]
- "detection_explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L1 | neighbors=[6bb51ab feat: add detection-explain end…, fail(), GET(), backend.ts, backend(), BackendError]
- "detection_sigma": "sigma.py" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma d…, 2885afa Add comprehensive probe testing…]
- "detection_vantage_fusion": "vantage_fusion.py" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _collect(), fuse_exposure_results(), fused_service_exposure(), _is_external(), _verdict()]
- "discovery_finding_translator_rationale_98": "Bump severity one rung when the finding's service is internet-reachable     (Ser" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L98 | neighbors=[_escalate_by_exposure(), create_findings_from_probe_result(), Asset, AssetType, FindingSeverity, FindingStatus]
- "discovery_service_vuln": "service_vuln.py" | kind=code-symbol | source=manager/backend/app/discovery/service_vuln.py:L1 | neighbors=[3565ada fix(ingest): NUL-safe result su…, _cleartext_rule(), create_service_vuln_findings(), _http_rules(), _new_finding(), _ssh_rules()]
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
- "id_rawfacts": "RawFacts.tsx" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/RawFacts.tsx:L1 | neighbors=[25c014d feat: enhance campaign progress…, CampaignProgress.tsx, Chip(), fetchJson(), RawFacts(), RawFactsResp]
- "kind_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/integrations/[kind]/route.ts:L1 | neighbors=[00c6648 feat(settings): editable email/…, DELETE(), PUT(), backend.ts, backend(), BackendError]
- "lib_campaign_store_getcampaign": "getCampaign()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L153 | neighbors=[route.ts, campaign-store.ts, fileFor(), isSafeCampaignId(), validateSnapshot(), listCampaigns()]
- "lib_findings_store_savefindings": "saveFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L51 | neighbors=[tools.ts, findings-store.ts, createFinding(), ensureDir(), getAllFindings(), slaDeadline()]
- "lib_httpx_parser_httpxjsonldecoder": "HttpxJsonlDecoder" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L93 | neighbors=[tool-runners.ts, httpx-parser.ts, .decode(), .finish(), .malformedLines(), .push()]
- "lib_security_context_securitycontexterror": "SecurityContextError" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L9 | neighbors=[route.ts, route.ts, route.ts, security-context.ts, publicCveRecord(), resolveSecurityReference()]
- "main_scripts_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L159 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "main_scripts_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L206 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "main_scripts_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…]
- "main_scripts_dns_scanner_dnsscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L178 | neighbors=[DNSScanner, derive_zones(), ._axfr(), ._chaos_txt(), ._dnssec_present(), ._ptr_self()]
- "main_scripts_findings_by_target": "_by_target()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1082 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "main_scripts_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1129 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "main_scripts_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1112 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "main_scripts_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1089 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "main_scripts_findings_run_findings": "run_findings()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1225 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…, Derive findings from collected facts. P…]
- "main_scripts_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L406 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + UDP + neighbor signals in…, Combine TCP + neighbor signals into a c…]
- "main_scripts_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L498 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._udp_liveness()]
- "main_scripts_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L569 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), ._udp_liveness(), is_locally_administered()]
- "main_scripts_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L301 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "main_scripts_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()]

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
