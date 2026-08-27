# Node Description Batch 60 of 92

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "scanner_findings_rationale_1188": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=scanner/findings.py:L1188 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_1196": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=scanner/findings.py:L1196 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_120": "A definitively open TCP port. `open|filtered` is NOT open — we never     raise a" | kind=entity | source=scanner/findings.py:L120 | neighbors=[_is_open()] | lang=pt
- "scanner_findings_rationale_1212": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=scanner/findings.py:L1212 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_154": "Map (target, port) -> confirmed-service info from service_banner facts.      Onl" | kind=entity | source=scanner/findings.py:L154 | neighbors=[build_service_index()] | lang=en
- "scanner_findings_rationale_444": "JA4X-based threat-intel match. Fires only when a certificate's structural     fi" | kind=entity | source=scanner/findings.py:L444 | neighbors=[_rule_tls_fingerprint()] | lang=pt
- "scanner_findings_rationale_466": "Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a" | kind=entity | source=scanner/findings.py:L466 | neighbors=[_rule_unauth_access()] | lang=en
- "scanner_findings_rationale_468": "JA4X-based threat-intel match. Fires only when a certificate's structural     fi" | kind=entity | source=scanner/findings.py:L468 | neighbors=[_rule_tls_fingerprint()] | lang=pt
- "scanner_findings_rationale_490": "Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a" | kind=entity | source=scanner/findings.py:L490 | neighbors=[_rule_unauth_access()] | lang=en
- "scanner_findings_rationale_492": "JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only" | kind=entity | source=scanner/findings.py:L492 | neighbors=[_rule_tls_server_fingerprint()] | lang=en
- "scanner_findings_rationale_512": "Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e" | kind=entity | source=scanner/findings.py:L512 | neighbors=[_rule_rdp()] | lang=en
- "scanner_findings_rationale_516": "JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only" | kind=entity | source=scanner/findings.py:L516 | neighbors=[_rule_tls_server_fingerprint()] | lang=en
- "scanner_findings_rationale_536": "Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e" | kind=entity | source=scanner/findings.py:L536 | neighbors=[_rule_rdp()] | lang=en
- "scanner_findings_rationale_577": "Anonymous SMB (null-session) information disclosure. The null session is a     m" | kind=entity | source=scanner/findings.py:L577 | neighbors=[_rule_smb_enum()] | lang=en
- "scanner_findings_rationale_593": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=scanner/findings.py:L593 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_601": "Anonymous SMB (null-session) information disclosure. The null session is a     m" | kind=entity | source=scanner/findings.py:L601 | neighbors=[_rule_smb_enum()] | lang=en
- "scanner_findings_rationale_616": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=scanner/findings.py:L616 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_628": "Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a" | kind=entity | source=scanner/findings.py:L628 | neighbors=[_rule_ldap()] | lang=en
- "scanner_findings_rationale_633": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=scanner/findings.py:L633 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_64": "One vulnerability finding, always backed by an observed fact." | kind=entity | source=scanner/findings.py:L64 | neighbors=[Finding] | lang=en
- "scanner_findings_rationale_652": "Anonymous LDAP exposure. An anonymous RootDSE bind is common (low), but an     a" | kind=entity | source=scanner/findings.py:L652 | neighbors=[_rule_ldap()] | lang=en
- "scanner_findings_rationale_656": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=scanner/findings.py:L656 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_666": "DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent" | kind=entity | source=scanner/findings.py:L666 | neighbors=[_rule_dns()] | lang=en
- "scanner_findings_rationale_685": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=scanner/findings.py:L685 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_690": "DNS server hygiene: a full AXFR zone transfer is the high-value finding     (ent" | kind=entity | source=scanner/findings.py:L690 | neighbors=[_rule_dns()] | lang=en
- "scanner_findings_rationale_702": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=scanner/findings.py:L702 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_708": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=scanner/findings.py:L708 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_716": "NFS anonymous export exposure. A world-readable export is the high-value     fin" | kind=entity | source=scanner/findings.py:L716 | neighbors=[_rule_nfs()] | lang=en
- "scanner_findings_rationale_718": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=scanner/findings.py:L718 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_725": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=scanner/findings.py:L725 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_735": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=scanner/findings.py:L735 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_740": "NFS anonymous export exposure. A world-readable export is the high-value     fin" | kind=entity | source=scanner/findings.py:L740 | neighbors=[_rule_nfs()] | lang=en
- "scanner_findings_rationale_748": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=scanner/findings.py:L748 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_753": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=scanner/findings.py:L753 | neighbors=[_rule_ftp()] | lang=en
- "scanner_findings_rationale_758": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=scanner/findings.py:L758 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_775": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=scanner/findings.py:L775 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_777": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=scanner/findings.py:L777 | neighbors=[_rule_ftp()] | lang=en
- "scanner_findings_rationale_782": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=scanner/findings.py:L782 | neighbors=[_rule_rsync()] | lang=en
- "scanner_findings_rationale_794": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=scanner/findings.py:L794 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_798": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=scanner/findings.py:L798 | neighbors=[run_findings()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-059.json

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
