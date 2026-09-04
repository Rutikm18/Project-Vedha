# Node Description Batch 135 of 332

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

- "main_scripts_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L106 | neighbors=[run_all.py, main()]
- "main_scripts_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L78 | neighbors=[run_all.py, main()]
- "main_scripts_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L125 | neighbors=[scan_funnel.py, .run_host()]
- "main_scripts_scan_funnel_rationale_73": "Canonical open-TCP set for a host = deduped, sorted union of every source." | kind=entity | source=probe/main_scripts/scan_funnel.py:L73 | neighbors=[reconcile_ports(), FunnelResult]
- "main_scripts_scan_funnel_rationale_87": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=probe/main_scripts/scan_funnel.py:L87 | neighbors=[route_ports(), _candidate_ports()]
- "main_scripts_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L114 | neighbors=[.run_host(), _Scanner]
- "main_scripts_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L512 | neighbors=[AdaptiveRateController, .wait()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L508 | neighbors=[AdaptiveRateController, .report_loss()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L501 | neighbors=[AdaptiveRateController, .report_success()]
- "main_scripts_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L524 | neighbors=[AdaptiveRateController, ._on_loss()]
- "main_scripts_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L518 | neighbors=[AdaptiveRateController, ._on_success()]
- "main_scripts_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L966 | neighbors=[BaseScanner, RateLimiter]
- "main_scripts_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L974 | neighbors=[BaseScanner, ._guarded()]
- "main_scripts_scanner_base_rationale_252": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=probe/main_scripts/scanner_base.py:L252 | neighbors=[describe_os_error(), ScopeGuard]
- "main_scripts_scanner_base_resolve_project_tz": "_resolve_project_tz()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L66 | neighbors=[scanner_base.py, The project timezone, degrading safely …]
- "main_scripts_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L304 | neighbors=[.write(), ScanResult]
- "main_scripts_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L408 | neighbors=[ScopeGuard, .in_scope()]
- "main_scripts_scanner_base_sendpacer_observe_round": ".observe_round()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L590 | neighbors=[Fold one send/collect round's reply rat…, SendPacer]
- "main_scripts_scanner_base_sendpacer_pace": ".pace()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L577 | neighbors=[Block just long enough to hold `rate` p…, SendPacer]
- "main_scripts_scanner_base_sendpacer_stats": ".stats()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L606 | neighbors=[Pacing telemetry for the scan summary (…, SendPacer]
- "main_scripts_scanner_registry_is_verified": "is_verified()" | kind=code-symbol | source=probe/main_scripts/scanner_registry.py:L97 | neighbors=[scanner_registry.py, True only for a scanner explicitly on t…]
- "main_scripts_scanner_registry_verification_report": "verification_report()" | kind=code-symbol | source=probe/main_scripts/scanner_registry.py:L107 | neighbors=[scanner_registry.py, The scanner-module trust view: which sc…]
- "main_scripts_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L229 | neighbors=[service_banner.py, match_service()]
- "main_scripts_service_banner_servicebannerscanner_connect": "._connect()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L339 | neighbors=[ServiceBannerScanner, ._rung()]
- "main_scripts_service_banner_servicebannerscanner_ladder_for": "._ladder_for()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L416 | neighbors=[ServiceBannerScanner, ._grab()]
- "main_scripts_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L524 | neighbors=[ServiceBannerScanner, ._grab()]
- "main_scripts_service_banner_tls_context": "_tls_context()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L50 | neighbors=[service_banner.py, A permissive client context for FINGERP…]
- "main_scripts_service_enum_main": "main()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L630 | neighbors=[service_enum.py, local_topology()]
- "main_scripts_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L485 | neighbors=[ServiceEnumScanner, ._probe_port()]
- "main_scripts_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L417 | neighbors=[service_enum.py, .scan_target()]
- "main_scripts_smb_enum_scanner_smbenumscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L221 | neighbors=[SMBEnumScanner, parse_rid_ranges()]
- "main_scripts_smb_enum_scanner_smbenumscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L274 | neighbors=[SMBEnumScanner, .scan_target()]
- "main_scripts_smb_enum_scanner_smbenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L295 | neighbors=[SMBEnumScanner, ._scan_port()]
- "main_scripts_smb_scanner_der_len": "_der_len()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L104 | neighbors=[smb_scanner.py, _der()]
- "main_scripts_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L229 | neighbors=[smb_scanner.py, .scan_target()]
- "main_scripts_smtp_scanner_smtpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L124 | neighbors=[SMTPScanner, .scan_target()]
- "main_scripts_smtp_scanner_smtpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L142 | neighbors=[SMTPScanner, ._scan_port()]
- "main_scripts_snmp_scanner_oid_in_subtree": "_oid_in_subtree()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L240 | neighbors=[snmp_scanner.py, ._walk_subtree()]
- "main_scripts_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()]
- "main_scripts_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-134.json

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
