# Node Description Batch 96 of 131

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "lib_nuclei_parser_nucleirawline": "NucleiRawLine" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L82 | neighbors=[nuclei-parser.ts]
- "lib_openvas_client_cvsstoseverity": "cvssToSeverity()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L39 | neighbors=[openvas-client.ts]
- "lib_openvas_client_gettask": "getTask()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L31 | neighbors=[openvas-client.ts]
- "lib_openvas_client_isopenvasfinding": "isOpenVASFinding()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L54 | neighbors=[openvas-client.ts]
- "lib_openvas_client_openvashelperoutput": "OpenVASHelperOutput" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L47 | neighbors=[openvas-client.ts]
- "lib_openvas_client_openvastaskstate": "OpenVASTaskState" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L19 | neighbors=[openvas-client.ts]
- "lib_openvas_client_taskstore": "taskStore" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L29 | neighbors=[openvas-client.ts]
- "lib_permissions_store_data_path": "DATA_PATH" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L4 | neighbors=[permissions-store.ts]
- "lib_permissions_store_permissionsfile": "PermissionsFile" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L16 | neighbors=[permissions-store.ts]
- "lib_permissions_store_userrole": "UserRole" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L6 | neighbors=[permissions-store.ts]
- "lib_scan_events_broadcasttoscan": "broadcastToScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L20 | neighbors=[scan-events.ts]
- "lib_scan_events_callback": "Callback" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L3 | neighbors=[scan-events.ts]
- "lib_scan_events_scanlisteners": "scanListeners" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L5 | neighbors=[scan-events.ts]
- "lib_scan_events_subscribescan": "subscribeScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L7 | neighbors=[scan-events.ts]
- "lib_scan_pipeline_computeoverallprogress": "computeOverallProgress()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L114 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_createinitialpipelinestate": "createInitialPipelineState()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L84 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_drainscanevents": "drainScanEvents()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L78 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_eventqueues": "eventQueues" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L60 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_getpipeline": "getPipeline()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L62 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_pipelinecontext": "PipelineContext" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L14 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_pipelinestate": "PipelineState" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L26 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_pipelinestore": "pipelineStore" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L59 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_profile_tools": "PROFILE_TOOLS" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L53 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_pushscanevent": "pushScanEvent()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L71 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_scanprofile": "ScanProfile" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L4 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_scantool": "ScanTool" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L3 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_setpipeline": "setPipeline()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L66 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_stage_weights": "STAGE_WEIGHTS" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L42 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_stagestate": "StageState" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L6 | neighbors=[scan-pipeline.ts]
- "lib_scanner_request_validation_netexec_checks": "NETEXEC_CHECKS" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L10 | neighbors=[scanner-request-validation.ts]
- "lib_scanner_request_validation_netexecscanrequest": "NetExecScanRequest" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L25 | neighbors=[scanner-request-validation.ts]
- "lib_scanner_request_validation_openvas_configs": "OPENVAS_CONFIGS" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L4 | neighbors=[scanner-request-validation.ts]
- "lib_scanner_request_validation_openvasscanrequest": "OpenVASScanRequest" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L16 | neighbors=[scanner-request-validation.ts]
- "lib_scanner_request_validation_validationresult": "ValidationResult" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L12 | neighbors=[scanner-request-validation.ts]
- "lib_security_context_securitycontexterror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L11 | neighbors=[SecurityContextError]
- "lib_severity_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L17 | neighbors=[severity.ts]
- "lib_severity_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L16 | neighbors=[severity.ts]
- "lib_severity_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L14 | neighbors=[severity.ts]
- "lib_severity_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L13 | neighbors=[severity.ts]
- "lib_target_parser_common_ranges": "COMMON_RANGES" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L132 | neighbors=[target-parser.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-095.json

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
