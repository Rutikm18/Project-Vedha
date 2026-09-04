# Node Description Batch 229 of 332

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

- "main_scripts_udp_scanner_rationale_248": "Return byte count and check QR bit (1 = response)." | kind=entity | source=probe/main_scripts/udp_scanner.py:L248 | neighbors=[interpret_mdns()] | lang=en
- "main_scripts_udp_scanner_rationale_290": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/main_scripts/udp_scanner.py:L290 | neighbors=[._gated_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_291": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/main_scripts/udp_scanner.py:L291 | neighbors=[._gated_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_296": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/main_scripts/udp_scanner.py:L296 | neighbors=[._gated_probe()] | lang=en
- "main_scripts_udp_scanner_rationale_78": "Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-" | kind=entity | source=probe/main_scripts/udp_scanner.py:L78 | neighbors=[_ike_probe()] | lang=fr
- "main_scripts_udp_scanner_snmp_probe": "_snmp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L54 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_udpscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L285 | neighbors=[UDPScanner] | lang=en
- "main_scripts_unauth_access_is_rce_capable": "is_rce_capable()" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L68 | neighbors=[unauth_access.py] | lang=en
- "main_scripts_unauth_access_rationale_49": "Decide whether `banner` proves unauthenticated access for `service`.      True =" | kind=entity | source=probe/main_scripts/unauth_access.py:L49 | neighbors=[classify_unauth_access()] | lang=en
- "main_scripts_va_campaign_alive": "_alive()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L332 | neighbors=[va_campaign.py] | lang=en
- "main_scripts_va_campaign_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L336 | neighbors=[va_campaign.py] | lang=en
- "main_scripts_va_campaign_cliprogressview_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L657 | neighbors=[CliProgressView] | lang=en
- "main_scripts_va_campaign_main": "main()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L708 | neighbors=[va_campaign.py] | lang=en
- "main_scripts_va_campaign_rationale_1": "va_campaign.py — the sequential Network Vulnerability-Assessment campaign.  WHY" | kind=entity | source=probe/main_scripts/va_campaign.py:L1 | neighbors=[va_campaign.py] | lang=en
- "main_scripts_va_campaign_rationale_114": "What a stage produced. `count` is stage-specific (live hosts, open ports,     se" | kind=entity | source=probe/main_scripts/va_campaign.py:L114 | neighbors=[StageOutcome] | lang=en
- "main_scripts_va_campaign_rationale_139": "Mutable state threaded through the stages." | kind=entity | source=probe/main_scripts/va_campaign.py:L139 | neighbors=[CampaignContext] | lang=en
- "main_scripts_va_campaign_rationale_170": "Owns the live campaign record. Every transition recomputes percent + ETA,     wr" | kind=entity | source=probe/main_scripts/va_campaign.py:L170 | neighbors=[ProgressReporter] | lang=en
- "main_scripts_va_campaign_rationale_291": "Runs the ordered stages sequentially, emitting progress throughout.      The eng" | kind=entity | source=probe/main_scripts/va_campaign.py:L291 | neighbors=[VACampaign] | lang=en
- "main_scripts_va_campaign_rationale_344": "Best-effort IPv6 neighbor discovery (ND multicast, RFC 4861). Returns     {facts" | kind=entity | source=probe/main_scripts/va_campaign.py:L344 | neighbors=[_discover_ipv6()] | lang=en
- "main_scripts_va_campaign_rationale_375": "Run coro_factory(item) over items with bounded concurrency; return the     list" | kind=entity | source=probe/main_scripts/va_campaign.py:L375 | neighbors=[_bounded_gather()] | lang=en
- "main_scripts_va_campaign_rationale_391": "Build the real capability stages from a pre-wired ScanFunnel, reusing its     pr" | kind=entity | source=probe/main_scripts/va_campaign.py:L391 | neighbors=[default_stages()] | lang=en
- "main_scripts_va_campaign_rationale_624": "Wire a campaign with the real scanners (or injected stages for tests)." | kind=entity | source=probe/main_scripts/va_campaign.py:L624 | neighbors=[build_campaign()] | lang=en
- "main_scripts_va_campaign_rationale_650": "Renders campaign progress to a stream. On a TTY it re-draws one live block     i" | kind=entity | source=probe/main_scripts/va_campaign.py:L650 | neighbors=[CliProgressView] | lang=en
- "main_scripts_va_campaign_rationale_98": "Everything that changes WHAT the campaign does (not HOW it reports)." | kind=entity | source=probe/main_scripts/va_campaign.py:L98 | neighbors=[CampaignOptions] | lang=en
- "main_scripts_va_campaign_vacampaign_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L297 | neighbors=[VACampaign] | lang=en
- "main_scripts_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "main_scripts_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=probe/main_scripts/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "main_scripts_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "main_scripts_vnc_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L150 | neighbors=[vnc_scanner.py] | lang=en
- "main_scripts_vnc_scanner_rationale_1": "vnc_scanner.py — VNC/RFB authentication exposure (VA checklist: unauthenticated" | kind=entity | source=probe/main_scripts/vnc_scanner.py:L1 | neighbors=[vnc_scanner.py] | lang=en
- "main_scripts_vnc_scanner_rationale_109": "Blocking: RFB version handshake + read offered security types.         Monkeypat" | kind=entity | source=probe/main_scripts/vnc_scanner.py:L109 | neighbors=[._probe()] | lang=en
- "main_scripts_vnc_scanner_rationale_47": "Parse a 'RFB 003.008' banner into (major, minor), or None if not RFB." | kind=entity | source=probe/main_scripts/vnc_scanner.py:L47 | neighbors=[parse_rfb_version()] | lang=pt
- "main_scripts_vnc_scanner_rationale_61": "Turn a list of offered security-type ids into a verdict." | kind=entity | source=probe/main_scripts/vnc_scanner.py:L61 | neighbors=[classify_security_types()] | lang=pt
- "main_scripts_vnc_scanner_rationale_82": "Read the offered security types, handling the RFB 3.3 (single 4-byte type)     v" | kind=entity | source=probe/main_scripts/vnc_scanner.py:L82 | neighbors=[_read_security_types()] | lang=en
- "main_scripts_vnc_scanner_vncscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L104 | neighbors=[VNCScanner] | lang=en
- "main_scripts_web_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L182 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L56 | neighbors=[_NoRedirect] | lang=en
- "main_scripts_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_rationale_149": "Preferred scheme first, the other as a fallback: a scheme guess must         nev" | kind=entity | source=probe/main_scripts/web_scanner.py:L149 | neighbors=[._schemes_for()] | lang=pt
- "main_scripts_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-228.json

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
