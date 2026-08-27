# Node Description Batch 61 of 92

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

- "scanner_findings_rationale_806": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=scanner/findings.py:L806 | neighbors=[_rule_rsync()] | lang=en
- "scanner_findings_rationale_810": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=scanner/findings.py:L810 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_820": "VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo" | kind=entity | source=scanner/findings.py:L820 | neighbors=[_rule_vnc()] | lang=en
- "scanner_findings_rationale_840": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=scanner/findings.py:L840 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_851": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=scanner/findings.py:L851 | neighbors=[_rule_ipmi()] | lang=pt
- "scanner_findings_rationale_860": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=scanner/findings.py:L860 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_863": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=scanner/findings.py:L863 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_875": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=scanner/findings.py:L875 | neighbors=[_rule_ipmi()] | lang=pt
- "scanner_findings_rationale_880": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=scanner/findings.py:L880 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_883": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=scanner/findings.py:L883 | neighbors=[_rule_smtp()] | lang=en
- "scanner_findings_rationale_907": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=scanner/findings.py:L907 | neighbors=[_rule_smtp()] | lang=en
- "scanner_findings_rationale_917": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=scanner/findings.py:L917 | neighbors=[_rule_msrpc()] | lang=en
- "scanner_findings_rationale_926": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=scanner/findings.py:L926 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_941": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=scanner/findings.py:L941 | neighbors=[_rule_msrpc()] | lang=en
- "scanner_findings_rationale_943": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=scanner/findings.py:L943 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_944": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=scanner/findings.py:L944 | neighbors=[_rule_printer()] | lang=en
- "scanner_findings_rationale_949": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=scanner/findings.py:L949 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_964": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=scanner/findings.py:L964 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_965": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=scanner/findings.py:L965 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_966": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=scanner/findings.py:L966 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_968": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=scanner/findings.py:L968 | neighbors=[_rule_printer()] | lang=en
- "scanner_findings_rationale_98": "Accept a raw JSONL dict or a ScanResult; return a plain dict view." | kind=entity | source=scanner/findings.py:L98 | neighbors=[_as_dict()] | lang=pt
- "scanner_findings_rationale_987": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=scanner/findings.py:L987 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_990": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=scanner/findings.py:L990 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=scanner/host_discovery.py:L394 | neighbors=[HostDiscoveryScanner] | lang=en
- "scanner_host_discovery_main": "main()" | kind=code-symbol | source=scanner/host_discovery.py:L495 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive, with graded confidence.  ME" | kind=entity | source=scanner/host_discovery.py:L1 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_112": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=scanner/host_discovery.py:L112 | neighbors=[normalize_mac()] | lang=en
- "scanner_host_discovery_rationale_126": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=scanner/host_discovery.py:L126 | neighbors=[is_locally_administered()] | lang=en
- "scanner_host_discovery_rationale_143": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=scanner/host_discovery.py:L143 | neighbors=[device_hint()] | lang=en
- "scanner_host_discovery_rationale_196": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=scanner/host_discovery.py:L196 | neighbors=[Neighbor] | lang=pt
- "scanner_host_discovery_rationale_203": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=scanner/host_discovery.py:L203 | neighbors=[parse_neighbor_line()] | lang=pt
- "scanner_host_discovery_rationale_233": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=scanner/host_discovery.py:L233 | neighbors=[read_neighbor()] | lang=en
- "scanner_host_discovery_rationale_264": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=scanner/host_discovery.py:L264 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_311": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=scanner/host_discovery.py:L311 | neighbors=[fuse_liveness()] | lang=pt
- "scanner_host_discovery_rationale_399": "Return 'open', 'refused', or None (no response)." | kind=entity | source=scanner/host_discovery.py:L399 | neighbors=[._probe()] | lang=en
- "scanner_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=scanner/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "scanner_iot_scanner_main": "main()" | kind=code-symbol | source=scanner/iot_scanner.py:L559 | neighbors=[iot_scanner.py] | lang=en
- "scanner_iot_scanner_rationale_1": "iot_scanner.py — IoT / embedded device fingerprint and exposure scanner.  Covers" | kind=entity | source=scanner/iot_scanner.py:L1 | neighbors=[iot_scanner.py] | lang=en
- "scanner_iot_scanner_rationale_131": "Decode a DNS wire-format name, following pointers.  Returns (name, end_offset)." | kind=entity | source=scanner/iot_scanner.py:L131 | neighbors=[_decode_mdns_name()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-060.json

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
