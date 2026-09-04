# Node Description Batch 252 of 330

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

- "scanner_scanner_registry_rationale_98": "True only for a scanner explicitly on the verified (trusted) list. Unknown     s" | kind=entity | source=probe/scanner/scanner_registry.py:L98 | neighbors=[is_verified()]
- "scanner_scanner_registry_scannerinfo": "ScannerInfo" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L27 | neighbors=[scanner_registry.py]
- "scanner_service_banner_main": "main()" | kind=code-symbol | source=probe/scanner/service_banner.py:L530 | neighbors=[service_banner.py]
- "scanner_service_banner_rationale_1": "service_banner.py — grab service banners and identify the service behind a port." | kind=entity | source=probe/scanner/service_banner.py:L1 | neighbors=[service_banner.py]
- "scanner_service_banner_rationale_116": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/scanner/service_banner.py:L116 | neighbors=[._rung()]
- "scanner_service_banner_rationale_130": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/scanner/service_banner.py:L130 | neighbors=[._rung()]
- "scanner_service_banner_rationale_133": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/scanner/service_banner.py:L133 | neighbors=[._rung()]
- "scanner_service_banner_rationale_236": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/scanner/service_banner.py:L236 | neighbors=[match_service()]
- "scanner_service_banner_rationale_268": "Pull status code, the identifying headers and the <title> out of an     HTTP/RTS" | kind=entity | source=probe/scanner/service_banner.py:L268 | neighbors=[parse_http_head()]
- "scanner_service_banner_rationale_349": "Read up to read_bytes: wait `first_wait` for the first segment, then         onl" | kind=entity | source=probe/scanner/service_banner.py:L349 | neighbors=[._read_some()]
- "scanner_service_banner_rationale_368": "One probe-ladder rung on its own connection. Returns (banner, extra):         ba" | kind=entity | source=probe/scanner/service_banner.py:L368 | neighbors=[._rung()]
- "scanner_service_banner_rationale_51": "A permissive client context for FINGERPRINTING only: no verification, any     ve" | kind=entity | source=probe/scanner/service_banner.py:L51 | neighbors=[_tls_context()]
- "scanner_service_banner_rationale_82": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/scanner/service_banner.py:L82 | neighbors=[match_service()]
- "scanner_service_banner_rationale_89": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/scanner/service_banner.py:L89 | neighbors=[match_service()]
- "scanner_service_banner_rationale_92": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/scanner/service_banner.py:L92 | neighbors=[match_service()]
- "scanner_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/service_banner.py:L324 | neighbors=[ServiceBannerScanner]
- "scanner_service_enum_rationale_1": "service_enum.py — enrichment / enumeration layer that runs AFTER host_discovery." | kind=entity | source=probe/scanner/service_enum.py:L1 | neighbors=[service_enum.py]
- "scanner_service_enum_rationale_105": "Everything learned about one target beyond 'it is alive'." | kind=entity | source=probe/scanner/service_enum.py:L105 | neighbors=[Enrichment]
- "scanner_service_enum_rationale_127": "Decode a DNS name (with 0xC0 compression) -> (name, next_offset)." | kind=entity | source=probe/scanner/service_enum.py:L127 | neighbors=[_dns_read_name()]
- "scanner_service_enum_rationale_134": "Everything learned about one target beyond 'it is alive'." | kind=entity | source=probe/scanner/service_enum.py:L134 | neighbors=[Enrichment]
- "scanner_service_enum_rationale_148": "Ask the host over multicast DNS (5353) for the PTR of its own address." | kind=entity | source=probe/scanner/service_enum.py:L148 | neighbors=[mdns_hostname()]
- "scanner_service_enum_rationale_156": "Decode a DNS name (with 0xC0 compression) -> (name, next_offset)." | kind=entity | source=probe/scanner/service_enum.py:L156 | neighbors=[_dns_read_name()]
- "scanner_service_enum_rationale_175": "NetBIOS first-level name encoding (16-byte name -> 32 nibble bytes)." | kind=entity | source=probe/scanner/service_enum.py:L175 | neighbors=[_nb_encode()]
- "scanner_service_enum_rationale_177": "Ask the host over multicast DNS (5353) for the PTR of its own address." | kind=entity | source=probe/scanner/service_enum.py:L177 | neighbors=[mdns_hostname()]
- "scanner_service_enum_rationale_185": "NBNS node-status (NBSTAT) query to UDP/137; return the workstation name." | kind=entity | source=probe/scanner/service_enum.py:L185 | neighbors=[netbios_name()]
- "scanner_service_enum_rationale_204": "NetBIOS first-level name encoding (16-byte name -> 32 nibble bytes)." | kind=entity | source=probe/scanner/service_enum.py:L204 | neighbors=[_nb_encode()]
- "scanner_service_enum_rationale_214": "NBNS node-status (NBSTAT) query to UDP/137; return the workstation name." | kind=entity | source=probe/scanner/service_enum.py:L214 | neighbors=[netbios_name()]
- "scanner_service_enum_rationale_216": "Run the three name sources concurrently off the event loop." | kind=entity | source=probe/scanner/service_enum.py:L216 | neighbors=[resolve_hostnames()]
- "scanner_service_enum_rationale_236": "One permissive TLS handshake: negotiated version + cert subject/issuer." | kind=entity | source=probe/scanner/service_enum.py:L236 | neighbors=[tls_info()]
- "scanner_service_enum_rationale_245": "Run the three name sources concurrently off the event loop." | kind=entity | source=probe/scanner/service_enum.py:L245 | neighbors=[resolve_hostnames()]
- "scanner_service_enum_rationale_259": "Which deprecated TLS/SSL versions the server still accepts (weak-config)." | kind=entity | source=probe/scanner/service_enum.py:L259 | neighbors=[tls_accepts_old()]
- "scanner_service_enum_rationale_265": "One permissive TLS handshake: negotiated version + cert subject/issuer." | kind=entity | source=probe/scanner/service_enum.py:L265 | neighbors=[tls_info()]
- "scanner_service_enum_rationale_288": "Which deprecated TLS/SSL versions the server still accepts (weak-config)." | kind=entity | source=probe/scanner/service_enum.py:L288 | neighbors=[tls_accepts_old()]
- "scanner_service_enum_rationale_294": "Negotiate against 445; report whether SMBv1 is offered (defensive flag)." | kind=entity | source=probe/scanner/service_enum.py:L294 | neighbors=[smb_dialects()]
- "scanner_service_enum_rationale_313": "Best-effort OS guess from voluntary evidence. Returns (label, confidence)." | kind=entity | source=probe/scanner/service_enum.py:L313 | neighbors=[guess_os()]
- "scanner_service_enum_rationale_323": "Negotiate against 445; report whether SMBv1 is offered (defensive flag)." | kind=entity | source=probe/scanner/service_enum.py:L323 | neighbors=[smb_dialects()]
- "scanner_service_enum_rationale_342": "Best-effort OS guess from voluntary evidence. Returns (label, confidence)." | kind=entity | source=probe/scanner/service_enum.py:L342 | neighbors=[guess_os()]
- "scanner_service_enum_rationale_361": "Descriptive role tags from the open-port signature." | kind=entity | source=probe/scanner/service_enum.py:L361 | neighbors=[classify_roles()]
- "scanner_service_enum_rationale_390": "Descriptive role tags from the open-port signature." | kind=entity | source=probe/scanner/service_enum.py:L390 | neighbors=[classify_roles()]
- "scanner_service_enum_rationale_396": "Directly-connected subnets and default gateway(s) from the OS route table." | kind=entity | source=probe/scanner/service_enum.py:L396 | neighbors=[local_topology()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-251.json

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
