# Node Description Batch 58 of 92

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

- "main_scripts_snmp_scanner_snmpscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L252 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L329 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_ssh_collector_collect_over_ssh": "_collect_over_ssh()" | kind=code-symbol | source=main_scripts/ssh_collector.py:L52 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_main": "main()" | kind=code-symbol | source=main_scripts/ssh_collector.py:L125 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_sshcollector_init": ".__init__()" | kind=code-symbol | source=main_scripts/ssh_collector.py:L83 | neighbors=[SSHCollector] | lang=en
- "main_scripts_syn_scanner_main": "main()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L465 | neighbors=[syn_scanner.py] | lang=en
- "main_scripts_tls_fingerprint_main": "main()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L320 | neighbors=[tls_fingerprint.py] | lang=en
- "main_scripts_tls_fingerprint_tlsfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L285 | neighbors=[TLSFingerprintScanner] | lang=en
- "main_scripts_tls_scanner_main": "main()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L304 | neighbors=[tls_scanner.py] | lang=en
- "main_scripts_tls_scanner_tlsscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L275 | neighbors=[TLSScanner] | lang=en
- "main_scripts_udp_scanner_dns_probe": "_dns_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L39 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_main": "main()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L382 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_memcached_stats_probe": "_memcached_stats_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L73 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_netbios_probe": "_netbios_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L65 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_ntp_probe": "_ntp_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L46 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_snmp_probe": "_snmp_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L54 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_udpscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L280 | neighbors=[UDPScanner] | lang=en
- "main_scripts_unauth_access_is_rce_capable": "is_rce_capable()" | kind=code-symbol | source=main_scripts/unauth_access.py:L68 | neighbors=[unauth_access.py] | lang=en
- "main_scripts_unauth_access_rationale_49": "Decide whether `banner` proves unauthenticated access for `service`.      True =" | kind=entity | source=main_scripts/unauth_access.py:L49 | neighbors=[classify_unauth_access()] | lang=en
- "main_scripts_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=main_scripts/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "main_scripts_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=main_scripts/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "main_scripts_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=main_scripts/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "main_scripts_web_scanner_main": "main()" | kind=code-symbol | source=main_scripts/web_scanner.py:L166 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=main_scripts/web_scanner.py:L56 | neighbors=[_NoRedirect] | lang=en
- "main_scripts_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/web_scanner.py:L139 | neighbors=[WebScanner] | lang=en
- "main_scripts_windows_collector_main": "main()" | kind=code-symbol | source=main_scripts/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "main_scripts_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=main_scripts/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "main_scripts_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=main_scripts/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "scanner_accuracy_rationale_125": "Run the findings engine over a labeled corpus and score it.      corpus = {name," | kind=entity | source=scanner/accuracy.py:L125 | neighbors=[evaluate_corpus()] | lang=en
- "scanner_accuracy_rationale_49": "Precision / recall / F1 of produced findings vs a labeled expected set.      Key" | kind=entity | source=scanner/accuracy.py:L49 | neighbors=[score_findings()] | lang=en
- "scanner_accuracy_rationale_80": "(target, port) -> status, from port/syn/mass scan facts (last one wins)." | kind=entity | source=scanner/accuracy.py:L80 | neighbors=[_observed_states()] | lang=en
- "scanner_accuracy_rationale_95": "OPEN precision/recall + overall state accuracy vs a remote-validated     ground" | kind=entity | source=scanner/accuracy.py:L95 | neighbors=[score_port_states()] | lang=pt
- "scanner_adaptive_timeout_adaptivetimeout_init": ".__init__()" | kind=code-symbol | source=scanner/adaptive_timeout.py:L21 | neighbors=[AdaptiveTimeout] | lang=en
- "scanner_adaptive_timeout_rationale_32": "Fold one round-trip sample (seconds) into the estimate. Ignores         missing/" | kind=entity | source=scanner/adaptive_timeout.py:L32 | neighbors=[.observe()] | lang=en
- "scanner_adaptive_timeout_rationale_45": "Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp" | kind=entity | source=scanner/adaptive_timeout.py:L45 | neighbors=[.timeout()] | lang=pt
- "scanner_adaptive_timeout_rationale_55": "Convenience: build an estimator and fold in a sequence of RTT samples." | kind=entity | source=scanner/adaptive_timeout.py:L55 | neighbors=[from_rtts()] | lang=en
- "scanner_db_scanner_dbscanner_init": ".__init__()" | kind=code-symbol | source=scanner/db_scanner.py:L240 | neighbors=[DBScanner] | lang=en
- "scanner_db_scanner_main": "main()" | kind=code-symbol | source=scanner/db_scanner.py:L287 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_mongodb": "_probe_mongodb()" | kind=code-symbol | source=scanner/db_scanner.py:L131 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_mssql": "_probe_mssql()" | kind=code-symbol | source=scanner/db_scanner.py:L82 | neighbors=[db_scanner.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-057.json

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
