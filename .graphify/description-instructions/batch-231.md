# Node Description Batch 232 of 336

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

- "main_scripts_udp_scanner_ntp_probe": "_ntp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L46 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_rationale_1": "udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO" | kind=entity | source=probe/main_scripts/udp_scanner.py:L1 | neighbors=[udp_scanner.py] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-231.json

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
