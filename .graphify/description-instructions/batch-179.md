# Node Description Batch 180 of 227

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

- "scanner_udp_scanner_rationale_219": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=probe/scanner/udp_scanner.py:L219 | neighbors=[interpret_ipmi()] | lang=en
- "scanner_udp_scanner_rationale_220": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=probe/scanner/udp_scanner.py:L220 | neighbors=[interpret_ipmi()] | lang=en
- "scanner_udp_scanner_rationale_232": "Extract Location and Server from SSDP response." | kind=entity | source=probe/scanner/udp_scanner.py:L232 | neighbors=[interpret_ssdp()] | lang=en
- "scanner_udp_scanner_rationale_233": "Extract Location and Server from SSDP response." | kind=entity | source=probe/scanner/udp_scanner.py:L233 | neighbors=[interpret_ssdp()] | lang=en
- "scanner_udp_scanner_rationale_247": "Return byte count and check QR bit (1 = response)." | kind=entity | source=probe/scanner/udp_scanner.py:L247 | neighbors=[interpret_mdns()] | lang=en
- "scanner_udp_scanner_rationale_248": "Return byte count and check QR bit (1 = response)." | kind=entity | source=probe/scanner/udp_scanner.py:L248 | neighbors=[interpret_mdns()] | lang=en
- "scanner_udp_scanner_rationale_290": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/scanner/udp_scanner.py:L290 | neighbors=[._gated_probe()] | lang=en
- "scanner_udp_scanner_rationale_291": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/scanner/udp_scanner.py:L291 | neighbors=[._gated_probe()] | lang=en
- "scanner_udp_scanner_rationale_78": "Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-" | kind=entity | source=probe/scanner/udp_scanner.py:L78 | neighbors=[_ike_probe()] | lang=fr
- "scanner_udp_scanner_snmp_probe": "_snmp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L54 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_udpscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L280 | neighbors=[UDPScanner] | lang=en
- "scanner_udp_scanner_udpscanner_send_recv": "._send_recv()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L157 | neighbors=[UDPScanner] | lang=en
- "scanner_unauth_access_is_rce_capable": "is_rce_capable()" | kind=code-symbol | source=probe/scanner/unauth_access.py:L68 | neighbors=[unauth_access.py] | lang=en
- "scanner_unauth_access_rationale_49": "Decide whether `banner` proves unauthenticated access for `service`.      True =" | kind=entity | source=probe/scanner/unauth_access.py:L49 | neighbors=[classify_unauth_access()] | lang=en
- "scanner_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=probe/scanner/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "scanner_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=probe/scanner/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "scanner_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=probe/scanner/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "scanner_web_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L166 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L56 | neighbors=[_NoRedirect] | lang=en
- "scanner_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/scanner/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/scanner/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en
- "scanner_web_scanner_rationale_46": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/scanner/web_scanner.py:L46 | neighbors=[parse_allow_header()] | lang=en
- "scanner_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L139 | neighbors=[WebScanner] | lang=en
- "scanner_windows_collector_main": "main()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=probe/scanner/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=probe/scanner/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "scanner_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "scanner_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "scans_page_field": "Field()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L125 | neighbors=[page.tsx] | lang=en
- "scans_page_group": "Group()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L183 | neighbors=[page.tsx] | lang=en
- "scans_page_intensities": "INTENSITIES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L17 | neighbors=[page.tsx] | lang=en
- "scans_page_jobmeta": "JobMeta" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L37 | neighbors=[page.tsx] | lang=en
- "scans_page_looksliketarget": "looksLikeTarget()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "scans_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L35 | neighbors=[page.tsx] | lang=en
- "scans_page_phaseticker": "PhaseTicker()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L96 | neighbors=[page.tsx] | lang=en
- "scans_page_portalscans": "PortalScans()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L195 | neighbors=[page.tsx] | lang=en
- "scans_page_scan_types": "SCAN_TYPES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L11 | neighbors=[page.tsx] | lang=en
- "scans_page_status_style": "STATUS_STYLE" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L8 | neighbors=[page.tsx] | lang=en
- "scans_page_status_var": "STATUS_VAR" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L28 | neighbors=[page.tsx] | lang=en
- "scans_page_statusicon": "StatusIcon()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L88 | neighbors=[page.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-179.json

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
