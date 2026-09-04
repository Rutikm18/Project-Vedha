# Node Description Batch 214 of 330

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

- "main_scripts_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=probe/main_scripts/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "main_scripts_iot_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L559 | neighbors=[iot_scanner.py] | lang=en
- "main_scripts_iot_scanner_rationale_1": "iot_scanner.py — IoT / embedded device fingerprint and exposure scanner.  Covers" | kind=entity | source=probe/main_scripts/iot_scanner.py:L1 | neighbors=[iot_scanner.py] | lang=en
- "main_scripts_iot_scanner_rationale_130": "Decode a DNS wire-format name, following pointers.  Returns (name, end_offset)." | kind=entity | source=probe/main_scripts/iot_scanner.py:L130 | neighbors=[_decode_mdns_name()] | lang=pt
- "main_scripts_iot_scanner_rationale_131": "Decode a DNS wire-format name, following pointers.  Returns (name, end_offset)." | kind=entity | source=probe/main_scripts/iot_scanner.py:L131 | neighbors=[_decode_mdns_name()] | lang=pt
- "main_scripts_iot_scanner_rationale_156": "Extract PTR target names from mDNS response (services discovered)." | kind=entity | source=probe/main_scripts/iot_scanner.py:L156 | neighbors=[_parse_mdns_response()] | lang=en
- "main_scripts_iot_scanner_rationale_157": "Extract PTR target names from mDNS response (services discovered)." | kind=entity | source=probe/main_scripts/iot_scanner.py:L157 | neighbors=[_parse_mdns_response()] | lang=en
- "main_scripts_iot_scanner_rationale_270": "MQTT variable-length encoding." | kind=entity | source=probe/main_scripts/iot_scanner.py:L270 | neighbors=[_mqtt_remaining_len()] | lang=en
- "main_scripts_iot_scanner_rationale_272": "MQTT variable-length encoding." | kind=entity | source=probe/main_scripts/iot_scanner.py:L272 | neighbors=[_mqtt_remaining_len()] | lang=en
- "main_scripts_iot_scanner_rationale_282": "MQTT SUBSCRIBE to '#' (all topics), QoS 0." | kind=entity | source=probe/main_scripts/iot_scanner.py:L282 | neighbors=[_mqtt_subscribe_all()] | lang=en
- "main_scripts_iot_scanner_rationale_284": "MQTT SUBSCRIBE to '#' (all topics), QoS 0." | kind=entity | source=probe/main_scripts/iot_scanner.py:L284 | neighbors=[_mqtt_subscribe_all()] | lang=en
- "main_scripts_iot_scanner_rationale_347": "CoAP Confirmable GET for /.well-known/core — resource discovery." | kind=entity | source=probe/main_scripts/iot_scanner.py:L347 | neighbors=[_coap_get_wellknown_core()] | lang=en
- "main_scripts_iot_scanner_rationale_349": "CoAP Confirmable GET for /.well-known/core — resource discovery." | kind=entity | source=probe/main_scripts/iot_scanner.py:L349 | neighbors=[_coap_get_wellknown_core()] | lang=en
- "main_scripts_iot_scanner_rationale_360": "Extract CoAP response code and content." | kind=entity | source=probe/main_scripts/iot_scanner.py:L360 | neighbors=[_parse_coap_response()] | lang=en
- "main_scripts_iot_scanner_rationale_362": "Extract CoAP response code and content." | kind=entity | source=probe/main_scripts/iot_scanner.py:L362 | neighbors=[_parse_coap_response()] | lang=en
- "main_scripts_iot_scanner_rationale_404": "HTTP GET to CWMP port — detect ACS or CPE management interface." | kind=entity | source=probe/main_scripts/iot_scanner.py:L404 | neighbors=[_probe_cwmp()] | lang=en
- "main_scripts_iot_scanner_rationale_406": "HTTP GET to CWMP port — detect ACS or CPE management interface." | kind=entity | source=probe/main_scripts/iot_scanner.py:L406 | neighbors=[_probe_cwmp()] | lang=en
- "main_scripts_iot_scanner_rationale_444": "Surveys a target for IoT/embedded device exposure across 6 protocol families." | kind=entity | source=probe/main_scripts/iot_scanner.py:L444 | neighbors=[IoTScanner] | lang=en
- "main_scripts_iot_scanner_rationale_446": "Surveys a target for IoT/embedded device exposure across 6 protocol families." | kind=entity | source=probe/main_scripts/iot_scanner.py:L446 | neighbors=[IoTScanner] | lang=en
- "main_scripts_iot_scanner_rationale_58": "HTTP GET the UPnP rootDesc.xml and extract device info." | kind=entity | source=probe/main_scripts/iot_scanner.py:L58 | neighbors=[_fetch_upnp_root_desc()] | lang=en
- "main_scripts_iot_scanner_rationale_59": "HTTP GET the UPnP rootDesc.xml and extract device info." | kind=entity | source=probe/main_scripts/iot_scanner.py:L59 | neighbors=[_fetch_upnp_root_desc()] | lang=en
- "main_scripts_ipmi_scanner_ipmiscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L68 | neighbors=[IPMIScanner] | lang=en
- "main_scripts_ipmi_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L113 | neighbors=[ipmi_scanner.py] | lang=en
- "main_scripts_ipmi_scanner_rationale_1": "ipmi_scanner.py — IPMI 2.0 cipher-zero authentication-bypass detection (VA check" | kind=entity | source=probe/main_scripts/ipmi_scanner.py:L1 | neighbors=[ipmi_scanner.py] | lang=en
- "main_scripts_ipmi_scanner_rationale_37": "A fixed RMCP+ Open Session Request offering cipher suite 0 (auth=0,     integrit" | kind=entity | source=probe/main_scripts/ipmi_scanner.py:L37 | neighbors=[build_open_session_request()] | lang=pt
- "main_scripts_ipmi_scanner_rationale_53": "Parse an RMCP+ Open Session Response; None if it isn't one.     resp[0]=RMCP ver" | kind=entity | source=probe/main_scripts/ipmi_scanner.py:L53 | neighbors=[parse_open_session_response()] | lang=en
- "main_scripts_ipmi_scanner_rationale_73": "Blocking: one RMCP+ Open Session Request, parse the response.         Monkeypatc" | kind=entity | source=probe/main_scripts/ipmi_scanner.py:L73 | neighbors=[._probe()] | lang=en
- "main_scripts_ipv6_discovery_rationale_1": "ipv6_discovery.py — link-local IPv6 host discovery via Neighbor Discovery (RFC 4" | kind=entity | source=probe/main_scripts/ipv6_discovery.py:L1 | neighbors=[ipv6_discovery.py] | lang=en
- "main_scripts_ipv6_discovery_rationale_103": "Fire an ICMPv6 echo at ff02::1 (scoped to `iface`) to make live hosts reply," | kind=entity | source=probe/main_scripts/ipv6_discovery.py:L103 | neighbors=[_ping_all_nodes()] | lang=en
- "main_scripts_ipv6_discovery_rationale_121": "Discover live IPv6 neighbors on the segment via ND multicast + neighbor     cach" | kind=entity | source=probe/main_scripts/ipv6_discovery.py:L121 | neighbors=[discover_ipv6_hosts()] | lang=en
- "main_scripts_ipv6_discovery_rationale_43": "Parse Linux `ip -6 neigh show` into [(address, state)]. Lines look like:" | kind=entity | source=probe/main_scripts/ipv6_discovery.py:L43 | neighbors=[parse_ip_neigh6()] | lang=en
- "main_scripts_ipv6_discovery_rationale_60": "Parse macOS/BSD `ndp -an` into [(address, state)]. Columns:         Neighbor  Li" | kind=entity | source=probe/main_scripts/ipv6_discovery.py:L60 | neighbors=[parse_ndp()] | lang=en
- "main_scripts_ipv6_discovery_rationale_81": "Best-effort set of this host's own IPv6 addresses, to exclude from results     (" | kind=entity | source=probe/main_scripts/ipv6_discovery.py:L81 | neighbors=[_own_ipv6_addresses()] | lang=en
- "main_scripts_ja4s_match_suspicious": "match_suspicious()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L131 | neighbors=[ja4s.py] | lang=en
- "main_scripts_ja4s_rationale_100": "JA4S from `parse_server_hello`'s output ({version, cipher, extensions})." | kind=entity | source=probe/main_scripts/ja4s.py:L100 | neighbors=[ja4s_from_parsed()] | lang=en
- "main_scripts_ja4s_rationale_110": "JA4S from raw ServerHello record bytes (reuses the JARM parser)." | kind=entity | source=probe/main_scripts/ja4s.py:L110 | neighbors=[ja4s_from_serverhello()] | lang=en
- "main_scripts_ja4s_rationale_117": "Do one standard TLS handshake and compute the server's JA4S. Reuses the     JARM" | kind=entity | source=probe/main_scripts/ja4s.py:L117 | neighbors=[compute_ja4s()] | lang=en
- "main_scripts_ja4s_rationale_57": "Yield (type, value) for each extension in a ServerHello extensions blob." | kind=entity | source=probe/main_scripts/ja4s.py:L57 | neighbors=[_walk_extensions()] | lang=en
- "main_scripts_ja4s_rationale_70": "The single ALPN protocol the server chose (b'' if none)." | kind=entity | source=probe/main_scripts/ja4s.py:L70 | neighbors=[_selected_alpn()] | lang=en
- "main_scripts_ja4s_rationale_87": "Pure JA4S from already-extracted ServerHello fields." | kind=entity | source=probe/main_scripts/ja4s.py:L87 | neighbors=[ja4s_from_fields()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-213.json

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
