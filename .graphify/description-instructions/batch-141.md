# Node Description Batch 142 of 330

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

- "scanner_scanner_base_rationale_353": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L353 | neighbors=[.networks(), bracket_host()] | lang=en
- "scanner_scanner_base_rationale_359": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L359 | neighbors=[_UDPProbeProtocol, BaseScanner] | lang=en
- "scanner_scanner_base_rationale_535": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L535 | neighbors=[BaseScanner, main_entrypoint()] | lang=pt
- "scanner_scanner_base_rationale_69": "The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p" | kind=entity | source=probe/scanner/scanner_base.py:L69 | neighbors=[choose_source_port(), ScopeGuard] | lang=en
- "scanner_scanner_base_resolve_project_tz": "_resolve_project_tz()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L66 | neighbors=[scanner_base.py, The project timezone, degrading safely …] | lang=en
- "scanner_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L304 | neighbors=[.write(), ScanResult] | lang=en
- "scanner_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L408 | neighbors=[ScopeGuard, .in_scope()] | lang=en
- "scanner_scanner_base_sendpacer_observe_round": ".observe_round()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L590 | neighbors=[Fold one send/collect round's reply rat…, SendPacer] | lang=en
- "scanner_scanner_base_sendpacer_pace": ".pace()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L577 | neighbors=[Block just long enough to hold `rate` p…, SendPacer] | lang=en
- "scanner_scanner_base_sendpacer_stats": ".stats()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L606 | neighbors=[Pacing telemetry for the scan summary (…, SendPacer] | lang=en
- "scanner_scanner_registry_is_verified": "is_verified()" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L97 | neighbors=[scanner_registry.py, True only for a scanner explicitly on t…] | lang=en
- "scanner_scanner_registry_verification_report": "verification_report()" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L107 | neighbors=[scanner_registry.py, The scanner-module trust view: which sc…] | lang=en
- "scanner_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/scanner/service_banner.py:L229 | neighbors=[service_banner.py, match_service()] | lang=en
- "scanner_service_banner_servicebannerscanner_connect": "._connect()" | kind=code-symbol | source=probe/scanner/service_banner.py:L339 | neighbors=[ServiceBannerScanner, ._rung()] | lang=en
- "scanner_service_banner_servicebannerscanner_ladder_for": "._ladder_for()" | kind=code-symbol | source=probe/scanner/service_banner.py:L416 | neighbors=[ServiceBannerScanner, ._grab()] | lang=en
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L524 | neighbors=[ServiceBannerScanner, ._grab()] | lang=en
- "scanner_service_banner_tls_context": "_tls_context()" | kind=code-symbol | source=probe/scanner/service_banner.py:L50 | neighbors=[service_banner.py, A permissive client context for FINGERP…] | lang=en
- "scanner_service_enum_main": "main()" | kind=code-symbol | source=probe/scanner/service_enum.py:L630 | neighbors=[service_enum.py, local_topology()] | lang=en
- "scanner_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=probe/scanner/service_enum.py:L485 | neighbors=[ServiceEnumScanner, ._probe_port()] | lang=en
- "scanner_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=probe/scanner/service_enum.py:L417 | neighbors=[service_enum.py, .scan_target()] | lang=en
- "scanner_smb_enum_scanner_smbenumscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L221 | neighbors=[SMBEnumScanner, parse_rid_ranges()] | lang=en
- "scanner_smb_enum_scanner_smbenumscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L274 | neighbors=[SMBEnumScanner, .scan_target()] | lang=en
- "scanner_smb_enum_scanner_smbenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L295 | neighbors=[SMBEnumScanner, ._scan_port()] | lang=en
- "scanner_smb_scanner_der_len": "_der_len()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L104 | neighbors=[smb_scanner.py, _der()] | lang=en
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L229 | neighbors=[smb_scanner.py, .scan_target()] | lang=en
- "scanner_smtp_scanner_smtpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L124 | neighbors=[SMTPScanner, .scan_target()] | lang=en
- "scanner_smtp_scanner_smtpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L142 | neighbors=[SMTPScanner, ._scan_port()] | lang=en
- "scanner_snmp_scanner_extract_sysdescr": "_extract_sysdescr()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L44 | neighbors=[snmp_scanner.py, .scan_target()] | lang=en
- "scanner_snmp_scanner_oid_in_subtree": "_oid_in_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L240 | neighbors=[snmp_scanner.py, ._walk_subtree()] | lang=en
- "scanner_snmp_scanner_snmpscanner_query": "._query()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L84 | neighbors=[SNMPScanner, _build_get()] | lang=en
- "scanner_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L329 | neighbors=[SNMPScanner, _extract_sysdescr()] | lang=en
- "scanner_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()] | lang=en
- "scanner_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()] | lang=en
- "scanner_ssh_kexdb_lookup": "lookup()" | kind=code-symbol | source=probe/scanner/ssh_kexdb.py:L477 | neighbors=[ssh_kexdb.py, Return (failures, warnings, infos) for …] | lang=en
- "scanner_ssh_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L215 | neighbors=[ssh_scanner.py, _read_packet()] | lang=en
- "scanner_ssh_scanner_sshscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L331 | neighbors=[SSHScanner, ._scan_port()] | lang=en
- "scanner_syn_scanner_rationale_232": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/scanner/syn_scanner.py:L232 | neighbors=[verify_reply_cookie(), _local_source_ip()] | lang=en
- "scanner_syn_scanner_synscanner_fallback_scan": "._fallback_scan()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L371 | neighbors=[SynScanner, .scan_target()] | lang=en
- "scanner_syn_scanner_synscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L315 | neighbors=[SynScanner, syn_scan_supported()] | lang=en
- "scanner_syn_scanner_synscanner_syn_scan_target": "._syn_scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L379 | neighbors=[SynScanner, .scan_target()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-141.json

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
