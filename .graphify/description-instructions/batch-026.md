# Node Description Batch 27 of 76

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

- "detection_logger_attacklogger_log_action": ".log_action()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L27 | neighbors=[AttackLogger, _as_uuid(), Persist a single attack action. Returns…]
- "detection_siem_elasticsiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L219 | neighbors=[ElasticSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_elasticsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L204 | neighbors=[ElasticSIEM, .build_query(), ._request()]
- "detection_siem_sentinelsiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L163 | neighbors=[SentinelSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_sentinelsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L152 | neighbors=[SentinelSIEM, .build_kql(), ._request()]
- "detection_siem_splunksiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L107 | neighbors=[SplunkSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_splunksiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L96 | neighbors=[SplunkSIEM, ._request(), .build_spl()]
- "discovery_finding_translator_find_open_duplicate": "_find_open_duplicate()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L75 | neighbors=[finding_translator.py, create_findings_from_probe_result(), A still-relevant Finding with the same …]
- "discovery_finding_translator_resolve_asset": "_resolve_asset()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L53 | neighbors=[finding_translator.py, create_findings_from_probe_result(), Find the Asset for a probe-reported tar…]
- "discovery_rate_limiter": "rate_limiter.py" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, RateLimiter, RateLimiter — enforces PPS limits per C…]
- "discovery_rate_limiter_ratelimiter_is_within_window": ".is_within_window()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L43 | neighbors=[RateLimiter, .acquire(), True if current time is inside the allo…]
- "discovery_worker_discoveryworker_banner_grab_all": "._banner_grab_all()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L151 | neighbors=[DiscoveryWorker, ._grab_one(), .run()]
- "discovery_xml_parser_nmapxmlparser_parse_port": "._parse_port()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L115 | neighbors=[NmapXMLParser, ._parse_host(), ParsedPort]
- "e2e_mock_manager_managerstate_next_job_for": ".next_job_for()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L98 | neighbors=[ManagerState, ._mint_scope_token(), ._seal_plan()]
- "e2e_mock_manager_managerstate_seal_plan": "._seal_plan()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L84 | neighbors=[ManagerState, .next_job_for(), b64e()]
- "e2e_mock_manager_spki_pin": "spki_pin()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L213 | neighbors=[mock_manager.py, b64e(), start()]
- "e2e_run_make_fake_tools": "make_fake_tools()" | kind=code-symbol | source=manager/frontend/tests/e2e/run.py:L29 | neighbors=[run.py, main(), Deterministic stand-ins emitting realis…]
- "engine_tool_runners_hassystembinary": "hasSystemBinary()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L33 | neighbors=[tool-runners.ts, isWindows(), resolveBinPath()]
- "engine_tool_runners_nativebannergrab": "nativeBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L303 | neighbors=[tool-runners.ts, httpBannerGrab(), tcpBannerGrab()]
- "engine_tool_runners_resolvebinpath": "resolveBinPath()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L52 | neighbors=[tool-runners.ts, hasBinary(), hasSystemBinary()]
- "engine_tool_runners_runldapenum": "runLdapEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1159 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runnetbiosenum": "runNetbiosEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1096 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runnfsenum": "runNfsEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1212 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runnmap": "runNmap()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L202 | neighbors=[tools.ts, scanner.ts, tool-runners.ts]
- "engine_tool_runners_runrdpfingerprint": "runRdpFingerprint()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1238 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runrpcenum": "runRpcEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1187 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runsmbenum": "runSmbEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1028 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runsnmpenum": "runSnmpEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1118 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_streamprocess": "streamProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L98 | neighbors=[tool-runners.ts, runNaabu(), runNuclei()]
- "engine_types_scantool": "ScanTool" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L5 | neighbors=[interactive.ts, scan-modules.ts, types.ts]
- "exploit_msf_client_metasploitrpcclient_list_modules": ".list_modules()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L65 | neighbors=[MetasploitRPCClient, ._call(), module_type: exploit | auxiliary | payl…]
- "exploit_nuclei_exploit": "nuclei_exploit.py" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, NucleiExploitRunner, NucleiExploitRunner — CVE PoC validatio…]
- "exploit_nuclei_exploit_nucleiexploitrunner_run_cve_poc": ".run_cve_poc()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L118 | neighbors=[NucleiExploitRunner, ._parse_poc_output(), Run Nuclei CVE PoC template against tar…]
- "exploit_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "exploit_orchestrator_exploitorchestrator_check_approval_required": "._check_approval_required()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L290 | neighbors=[ExploitOrchestrator, .execute(), Creates and returns an ExploitApprovalR…]
- "exploit_orchestrator_exploitorchestrator_check_blast_radius": "._check_blast_radius()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L268 | neighbors=[ExploitOrchestrator, .execute(), Count running exploit jobs for this eng…]
- "exploit_orchestrator_exploitorchestrator_select_exploit": ".select_exploit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L70 | neighbors=[ExploitOrchestrator, .execute(), Returns {module, payload, safe_check} f…]
- "exploit_orchestrator_exploitorchestrator_validate_safety": ".validate_safety()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L106 | neighbors=[ExploitOrchestrator, .execute(), Raises SafetyViolationError if module o…]
- "exploit_orchestrator_exploitorchestrator_validate_scope": ".validate_scope()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L113 | neighbors=[ExploitOrchestrator, .execute(), Raises OutOfScopeError if target_ip not…]
- "exploit_safety_validate_module": "validate_module()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L202 | neighbors=[safety.py, Raises SafetyViolationError if module i…, SafetyViolationError]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-026.json

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
