# Node Description Batch 129 of 186

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

- "main_scripts_findings_rationale_533": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/main_scripts/findings.py:L533 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_550": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/main_scripts/findings.py:L550 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_560": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/main_scripts/findings.py:L560 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_findings_rationale_573": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/main_scripts/findings.py:L573 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_583": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/main_scripts/findings.py:L583 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_600": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/main_scripts/findings.py:L600 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_619": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/main_scripts/findings.py:L619 | neighbors=[load_facts_jsonl()] | lang=pt
- "main_scripts_findings_rationale_623": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/main_scripts/findings.py:L623 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_635": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/main_scripts/findings.py:L635 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_64": "One vulnerability finding, always backed by an observed fact." | kind=entity | source=probe/main_scripts/findings.py:L64 | neighbors=[Finding] | lang=en
- "main_scripts_findings_rationale_669": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/main_scripts/findings.py:L669 | neighbors=[load_facts_jsonl()] | lang=pt
- "main_scripts_findings_rationale_685": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/main_scripts/findings.py:L685 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_98": "Accept a raw JSONL dict or a ScanResult; return a plain dict view." | kind=entity | source=probe/main_scripts/findings.py:L98 | neighbors=[_as_dict()] | lang=pt
- "main_scripts_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L391 | neighbors=[HostDiscoveryScanner] | lang=en
- "main_scripts_host_discovery_main": "main()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L492 | neighbors=[host_discovery.py] | lang=en
- "main_scripts_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive, with graded confidence.  ME" | kind=entity | source=probe/main_scripts/host_discovery.py:L1 | neighbors=[host_discovery.py] | lang=en
- "main_scripts_host_discovery_rationale_112": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=probe/main_scripts/host_discovery.py:L112 | neighbors=[normalize_mac()] | lang=en
- "main_scripts_host_discovery_rationale_126": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/main_scripts/host_discovery.py:L126 | neighbors=[is_locally_administered()] | lang=en
- "main_scripts_host_discovery_rationale_143": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/main_scripts/host_discovery.py:L143 | neighbors=[device_hint()] | lang=en
- "main_scripts_host_discovery_rationale_196": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=probe/main_scripts/host_discovery.py:L196 | neighbors=[Neighbor] | lang=pt
- "main_scripts_host_discovery_rationale_203": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=probe/main_scripts/host_discovery.py:L203 | neighbors=[parse_neighbor_line()] | lang=pt
- "main_scripts_host_discovery_rationale_233": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=probe/main_scripts/host_discovery.py:L233 | neighbors=[read_neighbor()] | lang=en
- "main_scripts_host_discovery_rationale_261": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/main_scripts/host_discovery.py:L261 | neighbors=[read_arp_table()] | lang=en
- "main_scripts_host_discovery_rationale_308": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/main_scripts/host_discovery.py:L308 | neighbors=[fuse_liveness()] | lang=pt
- "main_scripts_host_discovery_rationale_396": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/main_scripts/host_discovery.py:L396 | neighbors=[._probe()] | lang=en
- "main_scripts_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=probe/main_scripts/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "main_scripts_iot_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L557 | neighbors=[iot_scanner.py] | lang=en
- "main_scripts_iot_scanner_rationale_1": "iot_scanner.py — IoT / embedded device fingerprint and exposure scanner.  Covers" | kind=entity | source=probe/main_scripts/iot_scanner.py:L1 | neighbors=[iot_scanner.py] | lang=en
- "main_scripts_iot_scanner_rationale_130": "Decode a DNS wire-format name, following pointers.  Returns (name, end_offset)." | kind=entity | source=probe/main_scripts/iot_scanner.py:L130 | neighbors=[_decode_mdns_name()] | lang=pt
- "main_scripts_iot_scanner_rationale_156": "Extract PTR target names from mDNS response (services discovered)." | kind=entity | source=probe/main_scripts/iot_scanner.py:L156 | neighbors=[_parse_mdns_response()] | lang=en
- "main_scripts_iot_scanner_rationale_270": "MQTT variable-length encoding." | kind=entity | source=probe/main_scripts/iot_scanner.py:L270 | neighbors=[_mqtt_remaining_len()] | lang=en
- "main_scripts_iot_scanner_rationale_282": "MQTT SUBSCRIBE to '#' (all topics), QoS 0." | kind=entity | source=probe/main_scripts/iot_scanner.py:L282 | neighbors=[_mqtt_subscribe_all()] | lang=en
- "main_scripts_iot_scanner_rationale_347": "CoAP Confirmable GET for /.well-known/core — resource discovery." | kind=entity | source=probe/main_scripts/iot_scanner.py:L347 | neighbors=[_coap_get_wellknown_core()] | lang=en
- "main_scripts_iot_scanner_rationale_360": "Extract CoAP response code and content." | kind=entity | source=probe/main_scripts/iot_scanner.py:L360 | neighbors=[_parse_coap_response()] | lang=en
- "main_scripts_iot_scanner_rationale_404": "HTTP GET to CWMP port — detect ACS or CPE management interface." | kind=entity | source=probe/main_scripts/iot_scanner.py:L404 | neighbors=[_probe_cwmp()] | lang=en
- "main_scripts_iot_scanner_rationale_444": "Surveys a target for IoT/embedded device exposure across 6 protocol families." | kind=entity | source=probe/main_scripts/iot_scanner.py:L444 | neighbors=[IoTScanner] | lang=en
- "main_scripts_iot_scanner_rationale_58": "HTTP GET the UPnP rootDesc.xml and extract device info." | kind=entity | source=probe/main_scripts/iot_scanner.py:L58 | neighbors=[_fetch_upnp_root_desc()] | lang=en
- "main_scripts_ja4x_rationale_118": "Return a threat-intel label if this JA4X is a known-suspicious fingerprint," | kind=entity | source=probe/main_scripts/ja4x.py:L118 | neighbors=[match_suspicious()] | lang=en
- "main_scripts_ja4x_rationale_40": "DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040" | kind=entity | source=probe/main_scripts/ja4x.py:L40 | neighbors=[oid_to_hex()] | lang=en
- "main_scripts_ja4x_rationale_77": "Pure JA4X from the three ordered OID lists (dotted-decimal strings)." | kind=entity | source=probe/main_scripts/ja4x.py:L77 | neighbors=[ja4x_from_oid_lists()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-128.json

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
