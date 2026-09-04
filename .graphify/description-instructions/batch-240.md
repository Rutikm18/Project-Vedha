# Node Description Batch 241 of 330

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

- "scanner_findings_rationale_986": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=probe/scanner/findings.py:L986 | neighbors=[_rule_printer()] | lang=en
- "scanner_findings_rationale_990": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/scanner/findings.py:L990 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_ftp_scanner_ftpscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L65 | neighbors=[FTPScanner] | lang=en
- "scanner_ftp_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L176 | neighbors=[ftp_scanner.py] | lang=en
- "scanner_ftp_scanner_rationale_1": "ftp_scanner.py — FTP anonymous-access check (VA checklist: anonymous file exposu" | kind=entity | source=probe/scanner/ftp_scanner.py:L1 | neighbors=[ftp_scanner.py] | lang=en
- "scanner_ftp_scanner_rationale_129": "Confirm anonymous READ via PASV + LIST, reading a bounded amount." | kind=entity | source=probe/scanner/ftp_scanner.py:L129 | neighbors=[._list_bounded()] | lang=pt
- "scanner_ftp_scanner_rationale_45": "Extract the passive data PORT from a 227 reply. We connect to the TARGET     on" | kind=entity | source=probe/scanner/ftp_scanner.py:L45 | neighbors=[parse_pasv()] | lang=en
- "scanner_ftp_scanner_rationale_56": "Best-effort software token from the 220 greeting (e.g. 'vsFTPd 3.0.3')." | kind=entity | source=probe/scanner/ftp_scanner.py:L56 | neighbors=[banner_software()] | lang=en
- "scanner_ftp_scanner_rationale_70": "Read one (possibly multi-line) FTP reply; return (code, full_text)." | kind=entity | source=probe/scanner/ftp_scanner.py:L70 | neighbors=[._read_response()] | lang=en
- "scanner_ftp_scanner_rationale_96": "Blocking: greeting → anonymous login → bounded read confirmation.         Monkey" | kind=entity | source=probe/scanner/ftp_scanner.py:L96 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L501 | neighbors=[HostDiscoveryScanner] | lang=en
- "scanner_host_discovery_main": "main()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L696 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive, with graded confidence.  ME" | kind=entity | source=probe/scanner/host_discovery.py:L1 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_101": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/scanner/host_discovery.py:L101 | neighbors=[is_locally_administered()] | lang=en
- "scanner_host_discovery_rationale_104": "Parse a NetBIOS NBSTAT (node status) response (RFC 1002 §4.2.18).      Returns {" | kind=entity | source=probe/scanner/host_discovery.py:L104 | neighbors=[parse_nbstat()] | lang=pt
- "scanner_host_discovery_rationale_112": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=probe/scanner/host_discovery.py:L112 | neighbors=[normalize_mac()] | lang=en
- "scanner_host_discovery_rationale_118": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/scanner/host_discovery.py:L118 | neighbors=[device_hint()] | lang=en
- "scanner_host_discovery_rationale_126": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/scanner/host_discovery.py:L126 | neighbors=[is_locally_administered()] | lang=en
- "scanner_host_discovery_rationale_134": "Return {ip: normalized_mac} from the OS neighbor cache.      Tries `ip neigh` (L" | kind=entity | source=probe/scanner/host_discovery.py:L134 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_143": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/scanner/host_discovery.py:L143 | neighbors=[device_hint()] | lang=en
- "scanner_host_discovery_rationale_163": "PTR lookup; None on any failure. Runs in _RDNS_POOL, never on the loop." | kind=entity | source=probe/scanner/host_discovery.py:L163 | neighbors=[_reverse_dns()] | lang=en
- "scanner_host_discovery_rationale_185": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L185 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_196": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=probe/scanner/host_discovery.py:L196 | neighbors=[Neighbor] | lang=pt
- "scanner_host_discovery_rationale_203": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=probe/scanner/host_discovery.py:L203 | neighbors=[parse_neighbor_line()] | lang=pt
- "scanner_host_discovery_rationale_209": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=probe/scanner/host_discovery.py:L209 | neighbors=[normalize_mac()] | lang=en
- "scanner_host_discovery_rationale_223": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/scanner/host_discovery.py:L223 | neighbors=[is_locally_administered()] | lang=en
- "scanner_host_discovery_rationale_233": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=probe/scanner/host_discovery.py:L233 | neighbors=[read_neighbor()] | lang=en
- "scanner_host_discovery_rationale_240": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/scanner/host_discovery.py:L240 | neighbors=[device_hint()] | lang=en
- "scanner_host_discovery_rationale_261": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/scanner/host_discovery.py:L261 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_264": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/scanner/host_discovery.py:L264 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_295": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=probe/scanner/host_discovery.py:L295 | neighbors=[Neighbor] | lang=pt
- "scanner_host_discovery_rationale_302": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=probe/scanner/host_discovery.py:L302 | neighbors=[parse_neighbor_line()] | lang=pt
- "scanner_host_discovery_rationale_308": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/scanner/host_discovery.py:L308 | neighbors=[fuse_liveness()] | lang=pt
- "scanner_host_discovery_rationale_311": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/scanner/host_discovery.py:L311 | neighbors=[fuse_liveness()] | lang=pt
- "scanner_host_discovery_rationale_33": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L33 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_332": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=probe/scanner/host_discovery.py:L332 | neighbors=[read_neighbor()] | lang=en
- "scanner_host_discovery_rationale_363": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/scanner/host_discovery.py:L363 | neighbors=[read_arp_table()] | lang=en
- "scanner_host_discovery_rationale_37": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L37 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_396": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L396 | neighbors=[._probe()] | lang=en
- "scanner_host_discovery_rationale_399": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L399 | neighbors=[._probe()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-240.json

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
