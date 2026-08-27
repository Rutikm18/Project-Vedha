# Node Description Batch 175 of 236

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

- "scanner_device_classifier_rationale_202": "Convenience adapter: extract classifier inputs from a list of ScanResult     obj" | kind=entity | source=probe/scanner/device_classifier.py:L202 | neighbors=[classify_from_results()] | lang=en
- "scanner_findings_rationale_1013": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/scanner/findings.py:L1013 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_1030": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/scanner/findings.py:L1030 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_1057": "Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h" | kind=entity | source=probe/scanner/findings.py:L1057 | neighbors=[_corr_anon_data_exposure()] | lang=en
- "scanner_findings_rationale_1076": "A disclosed user list (SMB null session) plus a weak/exposed login surface on" | kind=entity | source=probe/scanner/findings.py:L1076 | neighbors=[_corr_user_enum_plus_weak_auth()] | lang=pt
- "scanner_findings_rationale_1099": "Out-of-band / console management surfaces reachable on one host — these grant" | kind=entity | source=probe/scanner/findings.py:L1099 | neighbors=[_corr_mgmt_plane_exposed()] | lang=en
- "scanner_findings_rationale_1126": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/scanner/findings.py:L1126 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_1172": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/scanner/findings.py:L1172 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_1188": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/scanner/findings.py:L1188 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_120": "A definitively open TCP port. `open|filtered` is NOT open — we never     raise a" | kind=entity | source=probe/scanner/findings.py:L120 | neighbors=[_is_open()] | lang=pt
- "scanner_findings_rationale_154": "Map (target, port) -> confirmed-service info from service_banner facts.      Onl" | kind=entity | source=probe/scanner/findings.py:L154 | neighbors=[build_service_index()] | lang=en
- "scanner_findings_rationale_444": "JA4X-based threat-intel match. Fires only when a certificate's structural     fi" | kind=entity | source=probe/scanner/findings.py:L444 | neighbors=[_rule_tls_fingerprint()] | lang=pt
- "scanner_findings_rationale_466": "Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a" | kind=entity | source=probe/scanner/findings.py:L466 | neighbors=[_rule_unauth_access()] | lang=en
- "scanner_findings_rationale_492": "JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only" | kind=entity | source=probe/scanner/findings.py:L492 | neighbors=[_rule_tls_server_fingerprint()] | lang=en
- "scanner_findings_rationale_512": "Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e" | kind=entity | source=probe/scanner/findings.py:L512 | neighbors=[_rule_rdp()] | lang=en
- "scanner_findings_rationale_560": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/scanner/findings.py:L560 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_577": "Anonymous SMB (null-session) information disclosure. The null session is a     m" | kind=entity | source=probe/scanner/findings.py:L577 | neighbors=[_rule_smb_enum()] | lang=en
- "scanner_findings_rationale_583": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/scanner/findings.py:L583 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_600": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/scanner/findings.py:L600 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_623": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/scanner/findings.py:L623 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_628": "Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a" | kind=entity | source=probe/scanner/findings.py:L628 | neighbors=[_rule_ldap()] | lang=en
- "scanner_findings_rationale_64": "One vulnerability finding, always backed by an observed fact." | kind=entity | source=probe/scanner/findings.py:L64 | neighbors=[Finding] | lang=en
- "scanner_findings_rationale_666": "DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent" | kind=entity | source=probe/scanner/findings.py:L666 | neighbors=[_rule_dns()] | lang=en
- "scanner_findings_rationale_669": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/scanner/findings.py:L669 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_685": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/scanner/findings.py:L685 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_716": "NFS anonymous export exposure. A world-readable export is the high-value     fin" | kind=entity | source=probe/scanner/findings.py:L716 | neighbors=[_rule_nfs()] | lang=en
- "scanner_findings_rationale_753": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=probe/scanner/findings.py:L753 | neighbors=[_rule_ftp()] | lang=en
- "scanner_findings_rationale_782": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=probe/scanner/findings.py:L782 | neighbors=[_rule_rsync()] | lang=en
- "scanner_findings_rationale_820": "VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo" | kind=entity | source=probe/scanner/findings.py:L820 | neighbors=[_rule_vnc()] | lang=en
- "scanner_findings_rationale_851": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=probe/scanner/findings.py:L851 | neighbors=[_rule_ipmi()] | lang=pt
- "scanner_findings_rationale_883": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=probe/scanner/findings.py:L883 | neighbors=[_rule_smtp()] | lang=en
- "scanner_findings_rationale_917": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=probe/scanner/findings.py:L917 | neighbors=[_rule_msrpc()] | lang=en
- "scanner_findings_rationale_944": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=probe/scanner/findings.py:L944 | neighbors=[_rule_printer()] | lang=en
- "scanner_findings_rationale_98": "Accept a raw JSONL dict or a ScanResult; return a plain dict view." | kind=entity | source=probe/scanner/findings.py:L98 | neighbors=[_as_dict()] | lang=pt
- "scanner_findings_rationale_990": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/scanner/findings.py:L990 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L394 | neighbors=[HostDiscoveryScanner] | lang=en
- "scanner_host_discovery_main": "main()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L495 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive, with graded confidence.  ME" | kind=entity | source=probe/scanner/host_discovery.py:L1 | neighbors=[host_discovery.py] | lang=en
- "scanner_host_discovery_rationale_101": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=probe/scanner/host_discovery.py:L101 | neighbors=[is_locally_administered()] | lang=en
- "scanner_host_discovery_rationale_112": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=probe/scanner/host_discovery.py:L112 | neighbors=[normalize_mac()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-174.json

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
