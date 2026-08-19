# Node Description Batch 161 of 227

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

- "main_scripts_udp_scanner_rationale_114": "SIP OPTIONS request — safe fingerprint method." | kind=entity | source=probe/main_scripts/udp_scanner.py:L114 | neighbors=[_sip_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_133": "TFTP RRQ for a non-existent file.  Error reply confirms TFTP service." | kind=entity | source=probe/main_scripts/udp_scanner.py:L133 | neighbors=[_tftp_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_139": "RMCP Ping (ASF Presence Ping) to detect IPMI/BMC." | kind=entity | source=probe/main_scripts/udp_scanner.py:L139 | neighbors=[_ipmi_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_140": "RMCP Ping (ASF Presence Ping) to detect IPMI/BMC." | kind=entity | source=probe/main_scripts/udp_scanner.py:L140 | neighbors=[_ipmi_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_146": "UPnP/SSDP M-SEARCH — unicast to target:1900." | kind=entity | source=probe/main_scripts/udp_scanner.py:L146 | neighbors=[_ssdp_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_147": "UPnP/SSDP M-SEARCH — unicast to target:1900." | kind=entity | source=probe/main_scripts/udp_scanner.py:L147 | neighbors=[_ssdp_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_158": "mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)." | kind=entity | source=probe/main_scripts/udp_scanner.py:L158 | neighbors=[_mdns_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_159": "mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)." | kind=entity | source=probe/main_scripts/udp_scanner.py:L159 | neighbors=[_mdns_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_188": "Parse IKEv1 or IKEv2 response header." | kind=entity | source=probe/main_scripts/udp_scanner.py:L188 | neighbors=[interpret_ike()] | lang=en
- "main_scripts_udp_scanner_rationale_189": "Parse IKEv1 or IKEv2 response header." | kind=entity | source=probe/main_scripts/udp_scanner.py:L189 | neighbors=[interpret_ike()] | lang=en
- "main_scripts_udp_scanner_rationale_204": "Extract SIP version + server header from a SIP response." | kind=entity | source=probe/main_scripts/udp_scanner.py:L204 | neighbors=[interpret_sip()] | lang=en
- "main_scripts_udp_scanner_rationale_205": "Extract SIP version + server header from a SIP response." | kind=entity | source=probe/main_scripts/udp_scanner.py:L205 | neighbors=[interpret_sip()] | lang=en
- "main_scripts_udp_scanner_rationale_219": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=probe/main_scripts/udp_scanner.py:L219 | neighbors=[interpret_ipmi()] | lang=en
- "main_scripts_udp_scanner_rationale_220": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=probe/main_scripts/udp_scanner.py:L220 | neighbors=[interpret_ipmi()] | lang=en
- "main_scripts_udp_scanner_rationale_232": "Extract Location and Server from SSDP response." | kind=entity | source=probe/main_scripts/udp_scanner.py:L232 | neighbors=[interpret_ssdp()] | lang=en
- "main_scripts_udp_scanner_rationale_233": "Extract Location and Server from SSDP response." | kind=entity | source=probe/main_scripts/udp_scanner.py:L233 | neighbors=[interpret_ssdp()] | lang=en
- "main_scripts_udp_scanner_rationale_247": "Return byte count and check QR bit (1 = response)." | kind=entity | source=probe/main_scripts/udp_scanner.py:L247 | neighbors=[interpret_mdns()] | lang=en
- "main_scripts_udp_scanner_rationale_248": "Return byte count and check QR bit (1 = response)." | kind=entity | source=probe/main_scripts/udp_scanner.py:L248 | neighbors=[interpret_mdns()] | lang=en
- "main_scripts_udp_scanner_rationale_290": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/main_scripts/udp_scanner.py:L290 | neighbors=[._gated_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_291": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/main_scripts/udp_scanner.py:L291 | neighbors=[._gated_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_78": "Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-" | kind=entity | source=probe/main_scripts/udp_scanner.py:L78 | neighbors=[_ike_probe()] | lang=fr
- "main_scripts_udp_scanner_snmp_probe": "_snmp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L54 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_udpscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L280 | neighbors=[UDPScanner] | lang=en
- "main_scripts_unauth_access_is_rce_capable": "is_rce_capable()" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L68 | neighbors=[unauth_access.py] | lang=en
- "main_scripts_unauth_access_rationale_49": "Decide whether `banner` proves unauthenticated access for `service`.      True =" | kind=entity | source=probe/main_scripts/unauth_access.py:L49 | neighbors=[classify_unauth_access()] | lang=en
- "main_scripts_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "main_scripts_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=probe/main_scripts/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "main_scripts_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "main_scripts_web_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L166 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L56 | neighbors=[_NoRedirect] | lang=en
- "main_scripts_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en
- "main_scripts_web_scanner_rationale_46": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/main_scripts/web_scanner.py:L46 | neighbors=[parse_allow_header()] | lang=en
- "main_scripts_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L139 | neighbors=[WebScanner] | lang=en
- "main_scripts_windows_collector_main": "main()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "main_scripts_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "main_scripts_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=probe/main_scripts/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "main_scripts_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "main_scripts_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "me_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L10 | neighbors=[route.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-160.json

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
