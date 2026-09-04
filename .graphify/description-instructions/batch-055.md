# Node Description Batch 56 of 332

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

- "graph_builder_rationale_295": "Mirror the current in-memory graph into Neo4j via batched writes." | kind=entity | source=manager/backend/app/graph/builder.py:L295 | neighbors=[.sync_to_neo4j(), Neo4jClient, Asset, Finding, Service]
- "graph_builder_rationale_53": "Normalise a value that may be an Enum, str, or None to a lowercase str." | kind=entity | source=manager/backend/app/graph/builder.py:L53 | neighbors=[_enum_value(), Neo4jClient, Asset, Finding, Service]
- "graph_builder_rationale_71": "Edge cost for an EXPLOITS edge. Derived from the CVSS Attack Complexity     comp" | kind=entity | source=manager/backend/app/graph/builder.py:L71 | neighbors=[exploit_complexity(), Neo4jClient, Asset, Finding, Service]
- "graph_demo_generate_demo_dataset": "generate_demo_dataset()" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L57 | neighbors=[demo.py, DemoAsset, DemoFinding, DemoService, Returns {engagement_id, assets, service…]
- "graph_visualizer": "visualizer.py" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _deterministic_layout(), GraphVisualizer, GraphVisualizer — serialise the attack …, 298a9d4 trim frontend to 7 core pages; …]
- "hooks_usecountup": "useCountUp.ts" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, DashboardCharts.tsx, useCountUp(), 298a9d4 trim frontend to 7 core pages; …]
- "lib_adapters_toapiengagementpatch": "toApiEngagementPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L249 | neighbors=[route.ts, adapters.ts, engStatusToApi(), normalizeList(), engagement-adapters.test.ts]
- "lib_ai_engine_generatereport": "generateReport()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L571 | neighbors=[ai-engine.ts, getClient(), stripFences(), toModelFindings(), toScorecardInput()]
- "lib_assistant_cverecordtofactcard": "cveRecordToFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L186 | neighbors=[assistant.ts, preferredText(), publicSeverity(), security-context.ts, assistant.test.ts]
- "lib_assistant_detectfindingid": "detectFindingId()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L81 | neighbors=[AssistantDrawer.tsx, route.ts, assistant.ts, security-context.ts, assistant.test.ts]
- "lib_backend_cookiefrom": "cookieFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L76 | neighbors=[backend.ts, bearerFrom(), route.ts, route.ts, backend-auth.test.ts]
- "lib_campaign_store_listcampaigns": "listCampaigns()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L165 | neighbors=[route.ts, campaign-store.ts, ensureDir(), getCampaign(), campaign-store.test.ts]
- "lib_campaign_store_validatesnapshot": "validateSnapshot()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L100 | neighbors=[campaign-store.ts, getCampaign(), saveCampaign(), isSafeCampaignId(), campaign-store.test.ts]
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
- "lib_portal_client_portalengagement": "PortalEngagement" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L43 | neighbors=[portal-client.ts, page.tsx, page.tsx, page.tsx, page.tsx]
- "lib_portal_client_portalfinding": "PortalFinding" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L58 | neighbors=[page.tsx, page.tsx, portal-client.ts, page.tsx, page.tsx]
- "lib_scanner_request_validation_validatenetexecscanrequest": "validateNetExecScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L192 | neighbors=[scanner-request-validation.ts, isRecord(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts]
- "lib_severity_toseverity": "toSeverity()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L118 | neighbors=[PatchComparisonMatrix.tsx, SlaStatus.tsx, severity.ts, sev(), page.tsx]
- "lib_testssl_parser_parsetestssljsonchecked": "parseTestsslJsonChecked()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L56 | neighbors=[tool-runners.ts, testssl-parser.ts, parseTestsslJson(), mapSeverity(), parsers.test.ts]
- "main_scripts_accuracy_evaluate_corpus": "evaluate_corpus()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L124 | neighbors=[accuracy.py, score_findings(), score_port_states(), _main(), Run the findings engine over a labeled …]
- "main_scripts_accuracy_gate_corpuserror": "CorpusError" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L61 | neighbors=[accuracy_gate.py, ValueError, load_corpora(), load_corpus(), A corpus is malformed or unlabeled — a …]
- "main_scripts_accuracy_gate_load_corpora": "load_corpora()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L92 | neighbors=[accuracy_gate.py, CorpusError, load_corpus(), Every *.json corpus in `directory`, sor…, run_gate()]
- "main_scripts_accuracy_score_port_states": "score_port_states()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L94 | neighbors=[accuracy.py, evaluate_corpus(), OPEN precision/recall + overall state a…, _observed_states(), _ratio()]
- "main_scripts_adaptive_timeout_adaptivetimeout": "AdaptiveTimeout" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L17 | neighbors=[adaptive_timeout.py, .__init__(), .observe(), .timeout(), from_rtts()]
- "main_scripts_delta_scanner_delta": "Delta" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L71 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…, One security-relevant change between tw…]
- "main_scripts_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L237 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…, Convenience adapter: extract classifier…, Convenience adapter: extract classifier…]
- "main_scripts_findings_corr_anon_data_exposure": "_corr_anon_data_exposure()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1156 | neighbors=[findings.py, _by_target(), Finding, Two or more INDEPENDENT anonymous data-…, Two or more INDEPENDENT anonymous data-…]
- "main_scripts_findings_corr_mgmt_plane_exposed": "_corr_mgmt_plane_exposed()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1198 | neighbors=[findings.py, _by_target(), Finding, Out-of-band / console management surfac…, Out-of-band / console management surfac…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-055.json

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
