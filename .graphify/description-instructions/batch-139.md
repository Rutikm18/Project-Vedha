# Node Description Batch 140 of 186

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

- "scanner_db_scanner_probe_postgres": "_probe_postgres()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L67 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_rationale_1": "db_scanner.py — fingerprint database services.  WHY: databases are everywhere on" | kind=entity | source=probe/scanner/db_scanner.py:L1 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_rationale_102": "Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act" | kind=entity | source=probe/scanner/db_scanner.py:L102 | neighbors=[interpret_redis_info()] | lang=en
- "scanner_delta_scanner_rationale_1": "delta_scanner.py — scan-state comparison and continuous attack-surface monitorin" | kind=entity | source=probe/scanner/delta_scanner.py:L1 | neighbors=[delta_scanner.py] | lang=en
- "scanner_delta_scanner_rationale_122": "Best-effort service name from data dict or scanner name." | kind=entity | source=probe/scanner/delta_scanner.py:L122 | neighbors=[_extract_service()] | lang=en
- "scanner_delta_scanner_rationale_139": "Best-effort version string." | kind=entity | source=probe/scanner/delta_scanner.py:L139 | neighbors=[_extract_version()] | lang=en
- "scanner_delta_scanner_rationale_158": "Load JSONL scan snapshots and compute security-relevant diffs." | kind=entity | source=probe/scanner/delta_scanner.py:L158 | neighbors=[DeltaEngine] | lang=en
- "scanner_delta_scanner_rationale_161": "Parse a JSONL file of ScanResult records and return a SnapshotIndex.         Lin" | kind=entity | source=probe/scanner/delta_scanner.py:L161 | neighbors=[.load_jsonl()] | lang=en
- "scanner_delta_scanner_rationale_206": "Compute security-relevant deltas between baseline and current snapshots." | kind=entity | source=probe/scanner/delta_scanner.py:L206 | neighbors=[.diff()] | lang=en
- "scanner_delta_scanner_rationale_297": "Heuristic priority for a newly-detected service." | kind=entity | source=probe/scanner/delta_scanner.py:L297 | neighbors=[_new_service_severity()] | lang=en
- "scanner_delta_scanner_rationale_309": "True if version changed in a security-relevant way (not just whitespace)." | kind=entity | source=probe/scanner/delta_scanner.py:L309 | neighbors=[_significant_version_change()] | lang=en
- "scanner_delta_scanner_rationale_54": "Normalised representation of one ScanResult JSONL line." | kind=entity | source=probe/scanner/delta_scanner.py:L54 | neighbors=[ScanRecord] | lang=en
- "scanner_delta_scanner_rationale_70": "One security-relevant change between two scans." | kind=entity | source=probe/scanner/delta_scanner.py:L70 | neighbors=[Delta] | lang=en
- "scanner_delta_scanner_rationale_92": "Derive a stable host identity from a raw scan record in priority order:       1." | kind=entity | source=probe/scanner/delta_scanner.py:L92 | neighbors=[_stable_host_id()] | lang=en
- "scanner_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L391 | neighbors=[HostDiscoveryScanner] | lang=en
- "scanner_host_discovery_main": "main()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L492 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive, with graded confidence.  ME" | kind=entity | source=probe/scanner/host_discovery.py:L1 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_101": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/scanner/host_discovery.py:L101 | neighbors=[is_locally_administered()] | lang=en
- "scanner_host_discovery_rationale_112": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=probe/scanner/host_discovery.py:L112 | neighbors=[normalize_mac()] | lang=en
- "scanner_host_discovery_rationale_118": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/scanner/host_discovery.py:L118 | neighbors=[device_hint()] | lang=en
- "scanner_host_discovery_rationale_126": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/scanner/host_discovery.py:L126 | neighbors=[is_locally_administered()] | lang=en
- "scanner_host_discovery_rationale_134": "Return {ip: normalized_mac} from the OS neighbor cache.      Tries `ip neigh` (L" | kind=entity | source=probe/scanner/host_discovery.py:L134 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_143": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/scanner/host_discovery.py:L143 | neighbors=[device_hint()] | lang=en
- "scanner_host_discovery_rationale_185": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L185 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_196": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=probe/scanner/host_discovery.py:L196 | neighbors=[Neighbor] | lang=pt
- "scanner_host_discovery_rationale_203": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=probe/scanner/host_discovery.py:L203 | neighbors=[parse_neighbor_line()] | lang=pt
- "scanner_host_discovery_rationale_233": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=probe/scanner/host_discovery.py:L233 | neighbors=[read_neighbor()] | lang=en
- "scanner_host_discovery_rationale_261": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/scanner/host_discovery.py:L261 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_308": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/scanner/host_discovery.py:L308 | neighbors=[fuse_liveness()] | lang=pt
- "scanner_host_discovery_rationale_33": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L33 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_37": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L37 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_396": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L396 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_87": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=probe/scanner/host_discovery.py:L87 | neighbors=[normalize_mac()] | lang=en
- "scanner_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=probe/scanner/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "scanner_iot_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L557 | neighbors=[iot_scanner.py] | lang=en
- "scanner_iot_scanner_rationale_1": "iot_scanner.py — IoT / embedded device fingerprint and exposure scanner.  Covers" | kind=entity | source=probe/scanner/iot_scanner.py:L1 | neighbors=[iot_scanner.py] | lang=en
- "scanner_iot_scanner_rationale_130": "Decode a DNS wire-format name, following pointers.  Returns (name, end_offset)." | kind=entity | source=probe/scanner/iot_scanner.py:L130 | neighbors=[_decode_mdns_name()] | lang=pt
- "scanner_iot_scanner_rationale_156": "Extract PTR target names from mDNS response (services discovered)." | kind=entity | source=probe/scanner/iot_scanner.py:L156 | neighbors=[_parse_mdns_response()] | lang=en
- "scanner_iot_scanner_rationale_270": "MQTT variable-length encoding." | kind=entity | source=probe/scanner/iot_scanner.py:L270 | neighbors=[_mqtt_remaining_len()] | lang=en
- "scanner_iot_scanner_rationale_282": "MQTT SUBSCRIBE to '#' (all topics), QoS 0." | kind=entity | source=probe/scanner/iot_scanner.py:L282 | neighbors=[_mqtt_subscribe_all()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-139.json

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
