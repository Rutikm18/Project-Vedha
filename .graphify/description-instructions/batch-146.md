# Node Description Batch 147 of 209

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

- "main_scripts_scanner_base_rationale_778": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/main_scripts/scanner_base.py:L778 | neighbors=[run_cli()] | lang=en
- "main_scripts_scanner_base_rationale_99": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/main_scripts/scanner_base.py:L99 | neighbors=[classify_os_error()] | lang=en
- "main_scripts_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L618 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L160 | neighbors=[ScanResult] | lang=en
- "main_scripts_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L228 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L192 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L741 | neighbors=[scanner_base.py] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L511 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L497 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L501 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L494 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_service_banner_main": "main()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L219 | neighbors=[service_banner.py] | lang=en
- "main_scripts_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=probe/main_scripts/service_banner.py:L1 | neighbors=[service_banner.py] | lang=en
- "main_scripts_service_banner_rationale_116": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/main_scripts/service_banner.py:L116 | neighbors=[._rung()] | lang=en
- "main_scripts_service_banner_rationale_130": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/main_scripts/service_banner.py:L130 | neighbors=[._rung()] | lang=en
- "main_scripts_service_banner_rationale_82": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/main_scripts/service_banner.py:L82 | neighbors=[match_service()] | lang=en
- "main_scripts_service_banner_rationale_89": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/main_scripts/service_banner.py:L89 | neighbors=[match_service()] | lang=en
- "main_scripts_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L123 | neighbors=[ServiceBannerScanner] | lang=en
- "main_scripts_smb_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L197 | neighbors=[smb_scanner.py] | lang=en
- "main_scripts_smb_scanner_rationale_1": "smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection" | kind=entity | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[smb_scanner.py] | lang=en
- "main_scripts_smb_scanner_rationale_37": "Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout" | kind=entity | source=probe/main_scripts/smb_scanner.py:L37 | neighbors=[parse_smb2_security_mode()] | lang=en
- "main_scripts_smb_scanner_smbscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L145 | neighbors=[SMBScanner] | lang=en
- "main_scripts_snmp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L401 | neighbors=[snmp_scanner.py] | lang=en
- "main_scripts_snmp_scanner_rationale_1": "snmp_scanner.py — full SNMP enumeration: community discovery, targeted MIB walk," | kind=entity | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[snmp_scanner.py] | lang=en
- "main_scripts_snmp_scanner_rationale_105": "Shallow parse of BER TLVs starting at offset. Returns [(tag, value), ...]." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L105 | neighbors=[_ber_parse()] | lang=en
- "main_scripts_snmp_scanner_rationale_127": "Extract (oid_dotted, value_tag, value_bytes) from a GET/GETNEXT/GETBULK response" | kind=entity | source=probe/main_scripts/snmp_scanner.py:L127 | neighbors=[_parse_varbinds()] | lang=en
- "main_scripts_snmp_scanner_rationale_246": "Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli" | kind=entity | source=probe/main_scripts/snmp_scanner.py:L246 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_snmp_scanner_rationale_278": "Return (community, sysdescr) for the first responding community, or None." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L278 | neighbors=[._discover_community()] | lang=en
- "main_scripts_snmp_scanner_rationale_292": "GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L292 | neighbors=[._walk_subtree()] | lang=en
- "main_scripts_snmp_scanner_rationale_315": "One GETBULK request — measure response/request size ratio." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L315 | neighbors=[._amplification_factor()] | lang=en
- "main_scripts_snmp_scanner_rationale_325": "Send a SNMPv3 Discover. Any reply = v3 agent present." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L325 | neighbors=[._snmpv3_present()] | lang=pt
- "main_scripts_snmp_scanner_rationale_46": "Dotted-notation OID string → BER-encoded bytes." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L46 | neighbors=[_encode_oid()] | lang=en
- "main_scripts_snmp_scanner_rationale_64": "BER-encoded OID bytes → dotted-notation string." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L64 | neighbors=[_decode_oid()] | lang=en
- "main_scripts_snmp_scanner_rationale_79": "Human-readable SNMP value for common ASN.1/SNMP types." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L79 | neighbors=[_decode_value()] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L252 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L329 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_ssh_collector_collect_over_ssh": "_collect_over_ssh()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L52 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_main": "main()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L125 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_rationale_1": "ssh_collector.py — credentialed (authenticated) inventory collection for Linux." | kind=entity | source=probe/main_scripts/ssh_collector.py:L1 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_sshcollector_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L83 | neighbors=[SSHCollector] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-146.json

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
