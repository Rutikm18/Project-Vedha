# Node Description Batch 95 of 119

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

- "scanner_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L454 | neighbors=[scanner_base.py] | lang=en
- "scanner_service_banner_main": "main()" | kind=code-symbol | source=probe/scanner/service_banner.py:L103 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=probe/scanner/service_banner.py:L1 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/service_banner.py:L37 | neighbors=[ServiceBannerScanner] | lang=en
- "scanner_smb_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L159 | neighbors=[smb_scanner.py] | lang=en
- "scanner_smb_scanner_rationale_1": "smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection" | kind=entity | source=probe/scanner/smb_scanner.py:L1 | neighbors=[smb_scanner.py] | lang=en
- "scanner_smb_scanner_rationale_37": "Read signing posture from an SMB2 NEGOTIATE response.      The response carries" | kind=entity | source=probe/scanner/smb_scanner.py:L37 | neighbors=[parse_smb2_security_mode()] | lang=en
- "scanner_smb_scanner_smbscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L107 | neighbors=[SMBScanner] | lang=en
- "scanner_snmp_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L124 | neighbors=[snmp_scanner.py] | lang=en
- "scanner_snmp_scanner_rationale_1": "snmp_scanner.py — detect SNMP and read sysDescr via common community strings.  M" | kind=entity | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[snmp_scanner.py] | lang=en
- "scanner_snmp_scanner_snmpscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L78 | neighbors=[SNMPScanner] | lang=en
- "scanner_ssh_collector_collect_over_ssh": "_collect_over_ssh()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L52 | neighbors=[ssh_collector.py] | lang=en
- "scanner_ssh_collector_main": "main()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L125 | neighbors=[ssh_collector.py] | lang=en
- "scanner_ssh_collector_rationale_1": "ssh_collector.py — credentialed (authenticated) inventory collection for Linux." | kind=entity | source=probe/scanner/ssh_collector.py:L1 | neighbors=[ssh_collector.py] | lang=en
- "scanner_ssh_collector_sshcollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L83 | neighbors=[SSHCollector] | lang=en
- "scanner_tls_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L186 | neighbors=[tls_scanner.py] | lang=en
- "scanner_tls_scanner_rationale_1": "tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):" | kind=entity | source=probe/scanner/tls_scanner.py:L1 | neighbors=[tls_scanner.py] | lang=en
- "scanner_tls_scanner_rationale_57": "Never send an IP literal as SNI — non-conformant; some servers reject it." | kind=entity | source=probe/scanner/tls_scanner.py:L57 | neighbors=[_sni()] | lang=en
- "scanner_tls_scanner_rationale_66": "Attempt a handshake forcing one protocol version. Returns cipher dict or None." | kind=entity | source=probe/scanner/tls_scanner.py:L66 | neighbors=[_try_version()] | lang=pt
- "scanner_tls_scanner_tlsscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L158 | neighbors=[TLSScanner] | lang=en
- "scanner_udp_scanner_dns_probe": "_dns_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L29 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L181 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_memcached_stats_probe": "_memcached_stats_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L78 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_netbios_probe": "_netbios_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L62 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_ntp_probe": "_ntp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L40 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_rationale_1": "udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO" | kind=entity | source=probe/scanner/udp_scanner.py:L1 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_snmp_probe": "_snmp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L45 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_udpscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L115 | neighbors=[UDPScanner] | lang=en
- "scanner_udp_scanner_udpscanner_send_recv": "._send_recv()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L157 | neighbors=[UDPScanner] | lang=en
- "scanner_web_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L165 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L55 | neighbors=[_NoRedirect] | lang=en
- "scanner_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/scanner/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/scanner/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en
- "scanner_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L138 | neighbors=[WebScanner] | lang=en
- "scanner_windows_collector_main": "main()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=probe/scanner/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=probe/scanner/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "scanner_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "scanner_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "schemas_ai_aigeneraterequest_validate_bounded_input": ".validate_bounded_input()" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L27 | neighbors=[AiGenerateRequest] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-094.json

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
