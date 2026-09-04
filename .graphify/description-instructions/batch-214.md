# Node Description Batch 215 of 332

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

- "main_scripts_host_discovery_rationale_233": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=probe/main_scripts/host_discovery.py:L233 | neighbors=[read_neighbor()] | lang=en
- "main_scripts_host_discovery_rationale_240": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/main_scripts/host_discovery.py:L240 | neighbors=[device_hint()] | lang=en
- "main_scripts_host_discovery_rationale_261": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/main_scripts/host_discovery.py:L261 | neighbors=[read_arp_table()] | lang=en
- "main_scripts_host_discovery_rationale_264": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/main_scripts/host_discovery.py:L264 | neighbors=[read_arp_table()] | lang=en
- "main_scripts_host_discovery_rationale_295": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=probe/main_scripts/host_discovery.py:L295 | neighbors=[Neighbor] | lang=pt
- "main_scripts_host_discovery_rationale_302": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=probe/main_scripts/host_discovery.py:L302 | neighbors=[parse_neighbor_line()] | lang=pt
- "main_scripts_host_discovery_rationale_308": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/main_scripts/host_discovery.py:L308 | neighbors=[fuse_liveness()] | lang=pt
- "main_scripts_host_discovery_rationale_311": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/main_scripts/host_discovery.py:L311 | neighbors=[fuse_liveness()] | lang=pt
- "main_scripts_host_discovery_rationale_332": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=probe/main_scripts/host_discovery.py:L332 | neighbors=[read_neighbor()] | lang=en
- "main_scripts_host_discovery_rationale_363": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/main_scripts/host_discovery.py:L363 | neighbors=[read_arp_table()] | lang=en
- "main_scripts_host_discovery_rationale_396": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/main_scripts/host_discovery.py:L396 | neighbors=[._probe()] | lang=en
- "main_scripts_host_discovery_rationale_399": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/main_scripts/host_discovery.py:L399 | neighbors=[._probe()] | lang=en
- "main_scripts_host_discovery_rationale_411": "Combine TCP + UDP + neighbor signals into a confidence-scored verdict.      `udp" | kind=entity | source=probe/main_scripts/host_discovery.py:L411 | neighbors=[fuse_liveness()] | lang=pt
- "main_scripts_host_discovery_rationale_517": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/main_scripts/host_discovery.py:L517 | neighbors=[._probe()] | lang=en
- "main_scripts_host_discovery_rationale_536": "One UDP liveness probe -> structured signal, or None on silence." | kind=entity | source=probe/main_scripts/host_discovery.py:L536 | neighbors=[._udp_one()] | lang=en
- "main_scripts_host_discovery_rationale_561": "Run the UDP tier concurrently; return every positive signal." | kind=entity | source=probe/main_scripts/host_discovery.py:L561 | neighbors=[._udp_liveness()] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-214.json

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
