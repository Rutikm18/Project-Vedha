# Node Description Batch 83 of 186

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

- "main_scripts_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L375 | neighbors=[UDPScanner, ._probe()]
- "main_scripts_vantage_matrix_is_external": "_is_external()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L34 | neighbors=[vantage_matrix.py, reconcile_vantages()]
- "main_scripts_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L77 | neighbors=[web_scanner.py, parse_allow_header()]
- "main_scripts_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L54 | neighbors=[web_scanner.py, .redirect_request()]
- "main_scripts_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L142 | neighbors=[WebScanner, .scan_target()]
- "main_scripts_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L159 | neighbors=[WebScanner, ._scan_port()]
- "main_scripts_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "main_scripts_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "models_audit_log_rationale_12": "Immutable, append-only audit trail for all exploit actions.     No TimestampMixi" | kind=entity | source=manager/backend/app/models/audit_log.py:L12 | neighbors=[AuditLog, Base]
- "models_probe_site": "probe_site.py" | kind=code-symbol | source=manager/backend/app/models/probe_site.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, ProbeSite]
- "models_scan_job_attempt": "scan_job_attempt.py" | kind=code-symbol | source=manager/backend/app/models/scan_job_attempt.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, ScanJobAttempt]
- "native_dir_bust_loadwordlist": "loadWordlist()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L97 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dir_bust_probe": "probe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L71 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dns_recon_attemptzonetransfer": "attemptZoneTransfer()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L96 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_dns_recon_nativeptrsweep": "nativePtrSweep()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L147 | neighbors=[dns-recon.ts, tool-runners.ts]
- "native_dns_recon_safe": "safe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L49 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_http_probe_nativehttpprobe": "nativeHttpProbe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L248 | neighbors=[tool-runners.ts, http-probe.ts]
- "native_port_scan_groupresults": "groupResults()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L261 | neighbors=[tool-runners.ts, port-scan.ts]
- "native_port_scan_resolveports": "resolvePorts()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L131 | neighbors=[port-scan.ts, nativePortScan()]
- "native_tls_info_nativetlsinfo": "nativeTlsInfo()" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L38 | neighbors=[tls-info.ts, tool-runners.ts]
- "oserror": "OSError" | kind=code-symbol | neighbors=[NmapExecutionError, NmapExecutionError]
- "portscan_family_of": "family_of()" | kind=code-symbol | source=portscan.py:L83 | neighbors=[portscan.py, ._attempt()]
- "portscan_parse_ports": "parse_ports()" | kind=code-symbol | source=portscan.py:L199 | neighbors=[portscan.py, main()]
- "portscan_portscanner_init": ".__init__()" | kind=code-symbol | source=portscan.py:L113 | neighbors=[PortScanner, RateLimiter]
- "portscan_portscanner_record": "._record()" | kind=code-symbol | source=portscan.py:L124 | neighbors=[PortScanner, ._attempt()]
- "portscan_ratelimiter_wait": ".wait()" | kind=code-symbol | source=portscan.py:L101 | neighbors=[.scan_port(), RateLimiter]
- "probe_pipeline_collector_write": ".write()" | kind=code-symbol | source=probe/pipeline.py:L126 | neighbors=[_Collector, _run_active()]
- "probe_push_results_die": "die()" | kind=code-symbol | source=probe/push_results.py:L29 | neighbors=[push_results.py, main()]
- "probe_push_results_load_facts": "load_facts()" | kind=code-symbol | source=probe/push_results.py:L34 | neighbors=[push_results.py, main()]
- "probe_run_scan_main": "main()" | kind=code-symbol | source=probe/run_scan.py:L135 | neighbors=[run_scan.py, _orchestrate()]
- "probe_run_scan_orchestrate": "_orchestrate()" | kind=code-symbol | source=probe/run_scan.py:L62 | neighbors=[run_scan.py, main()]
- "probe_selftest_live_check": "check()" | kind=code-symbol | source=probe/selftest_live.py:L38 | neighbors=[selftest_live.py, main()]
- "probe_selftest_live_fact": "_fact()" | kind=code-symbol | source=probe/selftest_live.py:L81 | neighbors=[selftest_live.py, main()]
- "probe_selftest_live_free_port": "_free_port()" | kind=code-symbol | source=probe/selftest_live.py:L69 | neighbors=[selftest_live.py, main()]
- "probe_showcase_run_list_use_cases": "list_use_cases()" | kind=code-symbol | source=probe/showcase_run.py:L39 | neighbors=[showcase_run.py, main()]
- "probe_showcase_run_print_summary": "_print_summary()" | kind=code-symbol | source=probe/showcase_run.py:L49 | neighbors=[showcase_run.py, main()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-082.json

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
