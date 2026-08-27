# Node Description Batch 157 of 236

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

- "main_scripts_findings_rationale_550": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/main_scripts/findings.py:L550 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_560": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/main_scripts/findings.py:L560 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_findings_rationale_573": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/main_scripts/findings.py:L573 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_577": "Anonymous SMB (null-session) information disclosure. The null session is a     m" | kind=entity | source=probe/main_scripts/findings.py:L577 | neighbors=[_rule_smb_enum()] | lang=en
- "main_scripts_findings_rationale_583": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/main_scripts/findings.py:L583 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_600": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/main_scripts/findings.py:L600 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_619": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/main_scripts/findings.py:L619 | neighbors=[load_facts_jsonl()] | lang=pt
- "main_scripts_findings_rationale_623": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/main_scripts/findings.py:L623 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_628": "Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a" | kind=entity | source=probe/main_scripts/findings.py:L628 | neighbors=[_rule_ldap()] | lang=en
- "main_scripts_findings_rationale_635": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/main_scripts/findings.py:L635 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_64": "One vulnerability finding, always backed by an observed fact." | kind=entity | source=probe/main_scripts/findings.py:L64 | neighbors=[Finding] | lang=en
- "main_scripts_findings_rationale_666": "DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent" | kind=entity | source=probe/main_scripts/findings.py:L666 | neighbors=[_rule_dns()] | lang=en
- "main_scripts_findings_rationale_669": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/main_scripts/findings.py:L669 | neighbors=[load_facts_jsonl()] | lang=pt
- "main_scripts_findings_rationale_685": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/main_scripts/findings.py:L685 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_716": "NFS anonymous export exposure. A world-readable export is the high-value     fin" | kind=entity | source=probe/main_scripts/findings.py:L716 | neighbors=[_rule_nfs()] | lang=en
- "main_scripts_findings_rationale_753": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=probe/main_scripts/findings.py:L753 | neighbors=[_rule_ftp()] | lang=en
- "main_scripts_findings_rationale_782": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=probe/main_scripts/findings.py:L782 | neighbors=[_rule_rsync()] | lang=en
- "main_scripts_findings_rationale_820": "VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo" | kind=entity | source=probe/main_scripts/findings.py:L820 | neighbors=[_rule_vnc()] | lang=en
- "main_scripts_findings_rationale_851": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=probe/main_scripts/findings.py:L851 | neighbors=[_rule_ipmi()] | lang=pt
- "main_scripts_findings_rationale_883": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=probe/main_scripts/findings.py:L883 | neighbors=[_rule_smtp()] | lang=en
- "main_scripts_findings_rationale_917": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=probe/main_scripts/findings.py:L917 | neighbors=[_rule_msrpc()] | lang=en
- "main_scripts_findings_rationale_944": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=probe/main_scripts/findings.py:L944 | neighbors=[_rule_printer()] | lang=en
- "main_scripts_findings_rationale_98": "Accept a raw JSONL dict or a ScanResult; return a plain dict view." | kind=entity | source=probe/main_scripts/findings.py:L98 | neighbors=[_as_dict()] | lang=pt
- "main_scripts_findings_rationale_990": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/main_scripts/findings.py:L990 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L394 | neighbors=[HostDiscoveryScanner] | lang=en
- "main_scripts_host_discovery_main": "main()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L495 | neighbors=[host_discovery.py] | lang=en
- "main_scripts_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive, with graded confidence.  ME" | kind=entity | source=probe/main_scripts/host_discovery.py:L1 | neighbors=[host_discovery.py] | lang=en
- "main_scripts_host_discovery_rationale_112": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=probe/main_scripts/host_discovery.py:L112 | neighbors=[normalize_mac()] | lang=en
- "main_scripts_host_discovery_rationale_126": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/main_scripts/host_discovery.py:L126 | neighbors=[is_locally_administered()] | lang=en
- "main_scripts_host_discovery_rationale_143": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=probe/main_scripts/host_discovery.py:L143 | neighbors=[device_hint()] | lang=en
- "main_scripts_host_discovery_rationale_196": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=probe/main_scripts/host_discovery.py:L196 | neighbors=[Neighbor] | lang=pt
- "main_scripts_host_discovery_rationale_203": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=probe/main_scripts/host_discovery.py:L203 | neighbors=[parse_neighbor_line()] | lang=pt
- "main_scripts_host_discovery_rationale_233": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=probe/main_scripts/host_discovery.py:L233 | neighbors=[read_neighbor()] | lang=en
- "main_scripts_host_discovery_rationale_261": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/main_scripts/host_discovery.py:L261 | neighbors=[read_arp_table()] | lang=en
- "main_scripts_host_discovery_rationale_264": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=probe/main_scripts/host_discovery.py:L264 | neighbors=[read_arp_table()] | lang=en
- "main_scripts_host_discovery_rationale_308": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/main_scripts/host_discovery.py:L308 | neighbors=[fuse_liveness()] | lang=pt
- "main_scripts_host_discovery_rationale_311": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=probe/main_scripts/host_discovery.py:L311 | neighbors=[fuse_liveness()] | lang=pt
- "main_scripts_host_discovery_rationale_396": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/main_scripts/host_discovery.py:L396 | neighbors=[._probe()] | lang=en
- "main_scripts_host_discovery_rationale_399": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/main_scripts/host_discovery.py:L399 | neighbors=[._probe()] | lang=en
- "main_scripts_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=probe/main_scripts/__init__.py:L1 | neighbors=[__init__.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-156.json

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
