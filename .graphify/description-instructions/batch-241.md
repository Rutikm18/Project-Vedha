# Node Description Batch 242 of 332

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

- "scanner_findings_rationale_619": "Anonymous SMB (null-session) information disclosure. The null session is a     m" | kind=entity | source=probe/scanner/findings.py:L619 | neighbors=[_rule_smb_enum()] | lang=en
- "scanner_findings_rationale_623": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/scanner/findings.py:L623 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_628": "Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a" | kind=entity | source=probe/scanner/findings.py:L628 | neighbors=[_rule_ldap()] | lang=en
- "scanner_findings_rationale_64": "One vulnerability finding, always backed by an observed fact." | kind=entity | source=probe/scanner/findings.py:L64 | neighbors=[Finding] | lang=en
- "scanner_findings_rationale_666": "DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent" | kind=entity | source=probe/scanner/findings.py:L666 | neighbors=[_rule_dns()] | lang=en
- "scanner_findings_rationale_669": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/scanner/findings.py:L669 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_670": "Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a" | kind=entity | source=probe/scanner/findings.py:L670 | neighbors=[_rule_ldap()] | lang=en
- "scanner_findings_rationale_685": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/scanner/findings.py:L685 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_708": "DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent" | kind=entity | source=probe/scanner/findings.py:L708 | neighbors=[_rule_dns()] | lang=en
- "scanner_findings_rationale_716": "NFS anonymous export exposure. A world-readable export is the high-value     fin" | kind=entity | source=probe/scanner/findings.py:L716 | neighbors=[_rule_nfs()] | lang=en
- "scanner_findings_rationale_753": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=probe/scanner/findings.py:L753 | neighbors=[_rule_ftp()] | lang=en
- "scanner_findings_rationale_758": "NFS anonymous export exposure. A world-readable export is the high-value     fin" | kind=entity | source=probe/scanner/findings.py:L758 | neighbors=[_rule_nfs()] | lang=en
- "scanner_findings_rationale_782": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=probe/scanner/findings.py:L782 | neighbors=[_rule_rsync()] | lang=en
- "scanner_findings_rationale_795": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=probe/scanner/findings.py:L795 | neighbors=[_rule_ftp()] | lang=en
- "scanner_findings_rationale_820": "VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo" | kind=entity | source=probe/scanner/findings.py:L820 | neighbors=[_rule_vnc()] | lang=en
- "scanner_findings_rationale_824": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=probe/scanner/findings.py:L824 | neighbors=[_rule_rsync()] | lang=en
- "scanner_findings_rationale_851": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=probe/scanner/findings.py:L851 | neighbors=[_rule_ipmi()] | lang=pt
- "scanner_findings_rationale_862": "VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo" | kind=entity | source=probe/scanner/findings.py:L862 | neighbors=[_rule_vnc()] | lang=en
- "scanner_findings_rationale_883": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=probe/scanner/findings.py:L883 | neighbors=[_rule_smtp()] | lang=en
- "scanner_findings_rationale_893": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=probe/scanner/findings.py:L893 | neighbors=[_rule_ipmi()] | lang=pt
- "scanner_findings_rationale_917": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=probe/scanner/findings.py:L917 | neighbors=[_rule_msrpc()] | lang=en
- "scanner_findings_rationale_925": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=probe/scanner/findings.py:L925 | neighbors=[_rule_smtp()] | lang=en
- "scanner_findings_rationale_944": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=probe/scanner/findings.py:L944 | neighbors=[_rule_printer()] | lang=en
- "scanner_findings_rationale_959": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=probe/scanner/findings.py:L959 | neighbors=[_rule_msrpc()] | lang=en
- "scanner_findings_rationale_98": "Accept a raw JSONL dict or a ScanResult; return a plain dict view." | kind=entity | source=probe/scanner/findings.py:L98 | neighbors=[_as_dict()] | lang=pt
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-241.json

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
