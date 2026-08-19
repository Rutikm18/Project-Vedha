# Node Description Batch 169 of 227

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

- "scanner_delta_scanner_rationale_161": "Parse a JSONL file of ScanResult records and return a SnapshotIndex.         Lin" | kind=entity | source=probe/scanner/delta_scanner.py:L161 | neighbors=[.load_jsonl()] | lang=en
- "scanner_delta_scanner_rationale_206": "Compute security-relevant deltas between baseline and current snapshots." | kind=entity | source=probe/scanner/delta_scanner.py:L206 | neighbors=[.diff()] | lang=en
- "scanner_delta_scanner_rationale_297": "Heuristic priority for a newly-detected service." | kind=entity | source=probe/scanner/delta_scanner.py:L297 | neighbors=[_new_service_severity()] | lang=en
- "scanner_delta_scanner_rationale_309": "True if version changed in a security-relevant way (not just whitespace)." | kind=entity | source=probe/scanner/delta_scanner.py:L309 | neighbors=[_significant_version_change()] | lang=en
- "scanner_delta_scanner_rationale_54": "Normalised representation of one ScanResult JSONL line." | kind=entity | source=probe/scanner/delta_scanner.py:L54 | neighbors=[ScanRecord] | lang=en
- "scanner_delta_scanner_rationale_70": "One security-relevant change between two scans." | kind=entity | source=probe/scanner/delta_scanner.py:L70 | neighbors=[Delta] | lang=en
- "scanner_delta_scanner_rationale_92": "Derive a stable host identity from a raw scan record in priority order:       1." | kind=entity | source=probe/scanner/delta_scanner.py:L92 | neighbors=[_stable_host_id()] | lang=en
- "scanner_device_classifier_rationale_1": "device_classifier.py — infer a device's ROLE from collection-layer facts.  This" | kind=entity | source=probe/scanner/device_classifier.py:L1 | neighbors=[device_classifier.py] | lang=en
- "scanner_device_classifier_rationale_102": "Fuse OS family + open ports + service products into a device-role guess.      Re" | kind=entity | source=probe/scanner/device_classifier.py:L102 | neighbors=[classify_device()] | lang=pt
- "scanner_device_classifier_rationale_202": "Convenience adapter: extract classifier inputs from a list of ScanResult     obj" | kind=entity | source=probe/scanner/device_classifier.py:L202 | neighbors=[classify_from_results()] | lang=en
- "scanner_findings_rationale_120": "A definitively open TCP port. `open|filtered` is NOT open — we never     raise a" | kind=entity | source=probe/scanner/findings.py:L120 | neighbors=[_is_open()] | lang=pt
- "scanner_findings_rationale_154": "Map (target, port) -> confirmed-service info from service_banner facts.      Onl" | kind=entity | source=probe/scanner/findings.py:L154 | neighbors=[build_service_index()] | lang=en
- "scanner_findings_rationale_444": "JA4X-based threat-intel match. Fires only when a certificate's structural     fi" | kind=entity | source=probe/scanner/findings.py:L444 | neighbors=[_rule_tls_fingerprint()] | lang=pt
- "scanner_findings_rationale_466": "Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a" | kind=entity | source=probe/scanner/findings.py:L466 | neighbors=[_rule_unauth_access()] | lang=en
- "scanner_findings_rationale_492": "JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only" | kind=entity | source=probe/scanner/findings.py:L492 | neighbors=[_rule_tls_server_fingerprint()] | lang=en
- "scanner_findings_rationale_512": "Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e" | kind=entity | source=probe/scanner/findings.py:L512 | neighbors=[_rule_rdp()] | lang=en
- "scanner_findings_rationale_560": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/scanner/findings.py:L560 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_583": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/scanner/findings.py:L583 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_600": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/scanner/findings.py:L600 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_623": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/scanner/findings.py:L623 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_64": "One vulnerability finding, always backed by an observed fact." | kind=entity | source=probe/scanner/findings.py:L64 | neighbors=[Finding] | lang=en
- "scanner_findings_rationale_669": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/scanner/findings.py:L669 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_685": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/scanner/findings.py:L685 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_98": "Accept a raw JSONL dict or a ScanResult; return a plain dict view." | kind=entity | source=probe/scanner/findings.py:L98 | neighbors=[_as_dict()] | lang=pt
- "scanner_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L394 | neighbors=[HostDiscoveryScanner] | lang=en
- "scanner_host_discovery_main": "main()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L495 | neighbors=[host_discovery.py] | lang=en
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
- "scanner_host_discovery_rationale_264": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/scanner/host_discovery.py:L264 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_308": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/scanner/host_discovery.py:L308 | neighbors=[fuse_liveness()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-168.json

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
