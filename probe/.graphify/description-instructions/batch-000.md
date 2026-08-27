# Node Description Batch 1 of 92

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

- "main_scripts_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=main_scripts/scanner_base.py:L200 | neighbors=[LeaseLostError, engine.py — adapt a manager scan job to…, syn' for wide sweeps (deep intensity / …, Coerce val to float and clamp to [lo, h…, Return the effective whole-job deadline…, Translate operator-supplied job params …]
- "main_scripts_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=main_scripts/scanner_base.py:L251 | neighbors=[LeaseLostError, engine.py — adapt a manager scan job to…, syn' for wide sweeps (deep intensity / …, Coerce val to float and clamp to [lo, h…, Return the effective whole-job deadline…, Translate operator-supplied job params …]
- "main_scripts_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=main_scripts/scanner_base.py:L695 | neighbors=[DBScanner, db_scanner.py — fingerprint database se…, Classify a Redis INFO reply. `unauthent…, VA scanner module — pure collection/sca…, IoTScanner, iot_scanner.py — IoT / embedded device …]
- "main_scripts_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=main_scripts/scanner_base.py:L725 | neighbors=[DBScanner, db_scanner.py — fingerprint database se…, Classify a Redis INFO reply. `unauthent…, HostDiscoveryScanner, Neighbor, host_discovery.py — determine which hos…]
- "commit:repo:local/probe@20f2a9dc@a5483592553f665914a3d0a3c1bbd25340bd58f9": "a548359 feat(auto-enrollment): implement trust-on-first-use for probe enrollmen…" | kind=Commit | source=git | neighbors=[agent.py, engine.py, __init__.py, task_runner.py, use_cases.py, feat/wire-osfp-service-enum]
- "commit:repo:local/probe@20f2a9dc@ae7a30b64b32bc7ab66898946433fa786ca611e3": "ae7a30b feat: add Posture & Patch-Comparison Scorecard design spec- Introduced …" | kind=Commit | source=git | neighbors=[agent.py, cli.py, device_identity.py, engine.py, hw_bind.py, __init__.py]
- "main_scripts_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=main_scripts/syn_scanner.py:L245 | neighbors=[FunnelResult, scan_funnel.py — per-host scan orchestr…, Orchestrates discovery → port scan → ro…, Funnel many hosts with bounded concurre…, Wire the funnel with the package's real…, Map a host's open ports onto the deep-s…]
- "main_scripts_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L199 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()]
- "main_scripts_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=main_scripts/udp_scanner.py:L277 | neighbors=[FunnelResult, scan_funnel.py — per-host scan orchestr…, Orchestrates discovery → port scan → ro…, Funnel many hosts with bounded concurre…, Wire the funnel with the package's real…, Map a host's open ports onto the deep-s…]
- "main_scripts_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=main_scripts/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "main_scripts_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=main_scripts/smb_scanner.py:L142 | neighbors=[FunnelResult, scan_funnel.py — per-host scan orchestr…, Orchestrates discovery → port scan → ro…, Funnel many hosts with bounded concurre…, Wire the funnel with the package's real…, Map a host's open ports onto the deep-s…]
- "main_scripts_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=main_scripts/tls_scanner.py:L272 | neighbors=[FunnelResult, scan_funnel.py — per-host scan orchestr…, Orchestrates discovery → port scan → ro…, Funnel many hosts with bounded concurre…, Wire the funnel with the package's real…, Map a host's open ports onto the deep-s…]
- "main_scripts_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=main_scripts/web_scanner.py:L136 | neighbors=[FunnelResult, scan_funnel.py — per-host scan orchestr…, Orchestrates discovery → port scan → ro…, Funnel many hosts with bounded concurre…, Wire the funnel with the package's real…, Map a host's open ports onto the deep-s…]
- "main_scripts_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=main_scripts/host_discovery.py:L391 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target(), BaseScanner]
- "tests_test_probe_core": "test_probe_core.py" | kind=code-symbol | source=tests/test_probe_core.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, agent.py, engine.py, use_cases.py, scanner_base.py]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=agent/transport.py:L115 | neighbors=[Load or atomically create the probe's E…, Request UI approval, poll, prove key po…, One-line, transparent summary of what a…, Return (agent_id, token, fresh, identit…, Map a low-level connection exception to…, GET /health. Returns (ok, human-detail)…]
- "scanner_scanner_base": "scanner_base.py" | kind=code-symbol | source=scanner/scanner_base.py:L1 | neighbors=[engine.py, local_run.py, 56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, AdaptiveRateController]
- "tests_test_probe_core_asset": "_asset()" | kind=code-symbol | source=tests/test_probe_core.py:L71 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "tests_test_main_scripts_findings": "test_main_scripts_findings.py" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _ids(), _run(), test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…, test_build_service_index_extracts_confi…]
- "main_scripts_findings": "findings.py" | kind=code-symbol | source=main_scripts/findings.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _as_dict(), build_service_index(), _by_target(), _corr_anon_data_exposure(), _corr_cleartext_cluster()]
- "scanner_findings": "findings.py" | kind=code-symbol | source=scanner/findings.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _as_dict(), build_service_index(), _by_target(), _corr_anon_data_exposure(), _corr_cleartext_cluster()]
- "workflow_execution_executiontrace": "ExecutionTrace" | kind=code-symbol | source=workflow/execution.py:L231 | neighbors=[LeaseLostError, engine.py — adapt a manager scan job to…, syn' for wide sweeps (deep intensity / …, Coerce val to float and clamp to [lo, h…, Return the effective whole-job deadline…, Translate operator-supplied job params …]
- "agent_agent": "agent.py" | kind=code-symbol | source=agent/agent.py:L1 | neighbors=[_bounded_env_int(), _check_anti_debug(), _classify_connection_error(), _dbg(), _enroll_device(), _flush_spool_over_http()]
- "commit:repo:local/probe@20f2a9dc@56508b23300cfdb457d29fbeef24c49c73870199": "56508b2 Add unit tests for XML parsing, address-family selection, tarpit detect…" | kind=Commit | source=git | neighbors=[agent.py, transport.py, main, a1430fb Add local_run.py for direct pro…, host_discovery.py, iot_scanner.py]
- "tests_test_main_scripts_findings_run": "_run()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L15 | neighbors=[test_main_scripts_findings.py, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_dou…, test_confirmed_ftp_cleartext_is_high_co…, test_confirmed_redis_is_high_confidence…]
- "agent_result_spool_resultspool": "ResultSpool" | kind=code-symbol | source=agent/result_spool.py:L27 | neighbors=[Load or atomically create the probe's E…, Request UI approval, poll, prove key po…, One-line, transparent summary of what a…, Return (agent_id, token, fresh, identit…, Map a low-level connection exception to…, GET /health. Returns (ok, human-detail)…]
- "workflow_cache_workflowcache": "WorkflowCache" | kind=code-symbol | source=workflow/cache.py:L78 | neighbors=[LeaseLostError, engine.py — adapt a manager scan job to…, syn' for wide sweeps (deep intensity / …, Coerce val to float and clamp to [lo, h…, Return the effective whole-job deadline…, Translate operator-supplied job params …]
- "agent_engine": "engine.py" | kind=code-symbol | source=agent/engine.py:L1 | neighbors=[agent.py, _applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _derive_devices()]
- "basescanner": "BaseScanner" | kind=code-symbol | neighbors=[DBScanner, HostDiscoveryScanner, IoTScanner, _ConnectSweep, MCPAIScanner, MobileScanner]
- "main_scripts_scanner_base": "scanner_base.py" | kind=code-symbol | source=main_scripts/scanner_base.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, AdaptiveRateController, assess_tarpit(), async_udp_probe(), async_udp_probe_retry()]
- "workflow_workflow_engine": "workflow_engine.py" | kind=code-symbol | source=workflow/workflow_engine.py:L1 | neighbors=[engine.py, local_run.py, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, de583d8 feat(workflow): wire os_fingerp…, test_passive_collector.py]
- "tests_test_workflow_execution": "test_workflow_execution.py" | kind=code-symbol | source=tests/test_workflow_execution.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, port_scanner.py, scanner_base.py, _ConcurrencyScanner, _ExplodingScanner, test_agent_scan_types_have_distinct_sta…]
- "agent_cli": "cli.py" | kind=code-symbol | source=agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=agent/hw_bind.py:L19 | neighbors=[Load or atomically create the probe's E…, Request UI approval, poll, prove key po…, One-line, transparent summary of what a…, Return (agent_id, token, fresh, identit…, Map a low-level connection exception to…, GET /health. Returns (ok, human-detail)…]
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=agent/transport.py:L49 | neighbors=[Load or atomically create the probe's E…, Request UI approval, poll, prove key po…, One-line, transparent summary of what a…, Return (agent_id, token, fresh, identit…, Map a low-level connection exception to…, GET /health. Returns (ok, human-detail)…]
- "main_scripts_findings_finding": "Finding" | kind=code-symbol | source=main_scripts/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "scanner_findings_finding": "Finding" | kind=code-symbol | source=scanner/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=agent/license.py:L29 | neighbors=[Load or atomically create the probe's E…, Request UI approval, poll, prove key po…, One-line, transparent summary of what a…, Return (agent_id, token, fresh, identit…, Map a low-level connection exception to…, GET /health. Returns (ok, human-detail)…]
- "main_scripts_adaptive_timeout_adaptivetimeout": "AdaptiveTimeout" | kind=code-symbol | source=main_scripts/adaptive_timeout.py:L17 | neighbors=[adaptive_timeout.py, .__init__(), .observe(), .timeout(), from_rtts(), PortScanner]
- "workflow_asset_asset": "Asset" | kind=code-symbol | source=workflow/asset.py:L51 | neighbors=[asset.py, ._merge_db_scan(), ._merge_dns_scan(), ._merge_ftp_scan(), ._merge_host_discovery(), ._merge_ipmi_scan()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-000.json

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
