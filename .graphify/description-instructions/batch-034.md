# Node Description Batch 35 of 186

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

- "graph_builder_rationale_53": "Normalise a value that may be an Enum, str, or None to a lowercase str." | kind=entity | source=manager/backend/app/graph/builder.py:L53 | neighbors=[_enum_value(), Neo4jClient, Asset, Finding, Service]
- "graph_builder_rationale_71": "Edge cost for an EXPLOITS edge. Derived from the CVSS Attack Complexity     comp" | kind=entity | source=manager/backend/app/graph/builder.py:L71 | neighbors=[exploit_complexity(), Neo4jClient, Asset, Finding, Service]
- "graph_demo_generate_demo_dataset": "generate_demo_dataset()" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L57 | neighbors=[demo.py, DemoAsset, DemoFinding, DemoService, Returns {engagement_id, assets, service…]
- "graph_visualizer": "visualizer.py" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _deterministic_layout(), GraphVisualizer, GraphVisualizer — serialise the attack …, 298a9d4 trim frontend to 7 core pages; …]
- "hooks_usecountup": "useCountUp.ts" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, DashboardCharts.tsx, useCountUp(), 298a9d4 trim frontend to 7 core pages; …]
- "lib_adapters_toapiengagementpatch": "toApiEngagementPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L224 | neighbors=[route.ts, adapters.ts, engStatusToApi(), normalizeList(), engagement-adapters.test.ts]
- "lib_assistant_cverecordtofactcard": "cveRecordToFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L147 | neighbors=[assistant.ts, preferredText(), publicSeverity(), security-context.ts, assistant.test.ts]
- "lib_assistant_detectfindingid": "detectFindingId()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L66 | neighbors=[AssistantDrawer.tsx, route.ts, assistant.ts, security-context.ts, assistant.test.ts]
- "lib_assistant_tofactcard": "toFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L89 | neighbors=[assistant.ts, isExploited(), plainWhyItMatters(), security-context.ts, assistant.test.ts]
- "lib_cases_store_writecases": "writeCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L226 | neighbors=[cases-store.ts, addComment(), createCase(), updateCase(), ensureDataDir()]
- "lib_detection_store_detectionstore": "detectionStore" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L421 | neighbors=[route.ts, detection-store.ts, route.ts, route.ts, route.ts]
- "lib_fetcher_errormessage": "errorMessage()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L84 | neighbors=[AssistantDrawer.tsx, page.tsx, page.tsx, fetcher.ts, DataState.tsx]
- "lib_fetcher_isunauthorized": "isUnauthorized()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L80 | neighbors=[page.tsx, page.tsx, fetcher.ts, page.tsx, DataState.tsx]
- "lib_finding_id_generatefindingid": "generateFindingId()" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L13 | neighbors=[scanner.ts, tool-runners.ts, finding-id.ts, findings-store.ts, testssl-parser.ts]
- "lib_findings_store_getfindingbyid": "getFindingById()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L75 | neighbors=[findings.ts, interactive.ts, findings-store.ts, getAllFindings(), findings-store.test.ts]
- "lib_findings_store_updatefinding": "updateFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L132 | neighbors=[interactive.ts, findings-store.ts, ensureDir(), getAllFindings(), tools.ts]
- "lib_findings_store_updatefindingstatus": "updateFindingStatus()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L79 | neighbors=[interactive.ts, findings-store.ts, ensureDir(), getAllFindings(), findings-store.test.ts]
- "lib_job_store_writejobs": "writeJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L32 | neighbors=[job-store.ts, createJob(), markDispatched(), updateJobStatus(), ensureDir()]
- "lib_nmap_parser_parsenmapxml": "parseNmapXml()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L48 | neighbors=[tool-runners.ts, nmap-parser.ts, extractScripts(), toArray(), parsers.test.ts]
- "lib_openvas_client_runopenvasscanbackground": "runOpenVASScanBackground()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L133 | neighbors=[openvas-client.ts, boundedEnvMs(), parseOpenVASHelperOutput(), setTask(), startOpenVASScan()]
- "lib_permissions_store_getuser": "getUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L44 | neighbors=[permissions-store.ts, read(), isAdmin(), isScopeAllowed(), route.ts]
- "lib_permissions_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L35 | neighbors=[permissions-store.ts, addUser(), removeUser(), updateScopes(), ensureDir()]
- "lib_scanner_request_validation_validatenetexecscanrequest": "validateNetExecScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L192 | neighbors=[scanner-request-validation.ts, isRecord(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts]
- "lib_severity_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L13 | neighbors=[Primitives.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx, severity.ts]
- "lib_testssl_parser_parsetestssljsonchecked": "parseTestsslJsonChecked()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L56 | neighbors=[tool-runners.ts, testssl-parser.ts, parseTestsslJson(), mapSeverity(), parsers.test.ts]
- "main_scripts_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…, test_main_scripts_device.py]
- "main_scripts_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/main_scripts/findings.py:L599 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "main_scripts_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/main_scripts/findings.py:L582 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "main_scripts_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/main_scripts/findings.py:L559 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "main_scripts_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=probe/main_scripts/findings.py:L316 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()]
- "main_scripts_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L511 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L443 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L491 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=probe/main_scripts/findings.py:L465 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner()]
- "main_scripts_findings_run_findings": "run_findings()" | kind=code-symbol | source=probe/main_scripts/findings.py:L622 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…]
- "main_scripts_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L304 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + neighbor signals into a c…]
- "main_scripts_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L388 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target()]
- "main_scripts_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "main_scripts_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L127 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), .scan_target(), Combine available stack signals into a …]
- "main_scripts_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L57 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-034.json

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
