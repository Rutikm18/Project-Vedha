# Node Description Batch 241 of 332

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

- "scanner_dns_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L242 | neighbors=[dns_scanner.py] | lang=en
- "scanner_dns_scanner_rationale_1": "dns_scanner.py — DNS server hygiene: zone transfer (AXFR), DNSSEC presence, and" | kind=entity | source=probe/scanner/dns_scanner.py:L1 | neighbors=[dns_scanner.py] | lang=en
- "scanner_dns_scanner_rationale_120": "Ask the target (as a resolver) for the PTR of its own IP — a common way" | kind=entity | source=probe/scanner/dns_scanner.py:L120 | neighbors=[._ptr_self()] | lang=en
- "scanner_dns_scanner_rationale_140": "Attempt a zone transfer, reading incrementally and stopping at         MAX_AXFR_" | kind=entity | source=probe/scanner/dns_scanner.py:L140 | neighbors=[._axfr()] | lang=en
- "scanner_dns_scanner_rationale_179": "Blocking orchestration of the DNS checks. Monkeypatchable for tests." | kind=entity | source=probe/scanner/dns_scanner.py:L179 | neighbors=[._probe()] | lang=en
- "scanner_dns_scanner_rationale_56": "Candidate zone names to try AXFR / DNSSEC against, most-confident first.      Ex" | kind=entity | source=probe/scanner/dns_scanner.py:L56 | neighbors=[derive_zones()] | lang=en
- "scanner_findings_rationale_1011": "Fuse OS signals across scanners into ONE identification with calibrated     conf" | kind=entity | source=probe/scanner/findings.py:L1011 | neighbors=[_rule_os_identification()] | lang=en
- "scanner_findings_rationale_1013": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/scanner/findings.py:L1013 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_1030": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/scanner/findings.py:L1030 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_1057": "Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h" | kind=entity | source=probe/scanner/findings.py:L1057 | neighbors=[_corr_anon_data_exposure()] | lang=en
- "scanner_findings_rationale_1076": "A disclosed user list (SMB null session) plus a weak/exposed login surface on" | kind=entity | source=probe/scanner/findings.py:L1076 | neighbors=[_corr_user_enum_plus_weak_auth()] | lang=pt
- "scanner_findings_rationale_1090": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/scanner/findings.py:L1090 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_1099": "Out-of-band / console management surfaces reachable on one host — these grant" | kind=entity | source=probe/scanner/findings.py:L1099 | neighbors=[_corr_mgmt_plane_exposed()] | lang=en
- "scanner_findings_rationale_1113": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/scanner/findings.py:L1113 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_1126": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/scanner/findings.py:L1126 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_1130": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/scanner/findings.py:L1130 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "scanner_findings_rationale_1157": "Two or more INDEPENDENT anonymous data-exposure channels on one host — the     h" | kind=entity | source=probe/scanner/findings.py:L1157 | neighbors=[_corr_anon_data_exposure()] | lang=en
- "scanner_findings_rationale_1172": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/scanner/findings.py:L1172 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_1176": "A disclosed user list (SMB null session) plus a weak/exposed login surface on" | kind=entity | source=probe/scanner/findings.py:L1176 | neighbors=[_corr_user_enum_plus_weak_auth()] | lang=pt
- "scanner_findings_rationale_1188": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/scanner/findings.py:L1188 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_1199": "Out-of-band / console management surfaces reachable on one host — these grant" | kind=entity | source=probe/scanner/findings.py:L1199 | neighbors=[_corr_mgmt_plane_exposed()] | lang=en
- "scanner_findings_rationale_120": "A definitively open TCP port. `open|filtered` is NOT open — we never     raise a" | kind=entity | source=probe/scanner/findings.py:L120 | neighbors=[_is_open()] | lang=pt
- "scanner_findings_rationale_1226": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=probe/scanner/findings.py:L1226 | neighbors=[run_findings()] | lang=en
- "scanner_findings_rationale_1258": "One finding as the finding-section shows it — the ACTUAL vulnerability, with" | kind=entity | source=probe/scanner/findings.py:L1258 | neighbors=[_finding_row()] | lang=en
- "scanner_findings_rationale_1280": "Roll up findings for the finding section.      Beyond counts, this returns the A" | kind=entity | source=probe/scanner/findings.py:L1280 | neighbors=[summarize()] | lang=en
- "scanner_findings_rationale_1320": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=probe/scanner/findings.py:L1320 | neighbors=[load_facts_jsonl()] | lang=pt
- "scanner_findings_rationale_1336": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=probe/scanner/findings.py:L1336 | neighbors=[_main()] | lang=en
- "scanner_findings_rationale_154": "Map (target, port) -> confirmed-service info from service_banner facts.      Onl" | kind=entity | source=probe/scanner/findings.py:L154 | neighbors=[build_service_index()] | lang=en
- "scanner_findings_rationale_444": "JA4X-based threat-intel match. Fires only when a certificate's structural     fi" | kind=entity | source=probe/scanner/findings.py:L444 | neighbors=[_rule_tls_fingerprint()] | lang=pt
- "scanner_findings_rationale_466": "Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a" | kind=entity | source=probe/scanner/findings.py:L466 | neighbors=[_rule_unauth_access()] | lang=en
- "scanner_findings_rationale_468": "JA4X-based threat-intel match. Fires only when a certificate's structural     fi" | kind=entity | source=probe/scanner/findings.py:L468 | neighbors=[_rule_tls_fingerprint()] | lang=pt
- "scanner_findings_rationale_490": "Proven UNAUTHENTICATED access to a datastore (from the collected banner) —     a" | kind=entity | source=probe/scanner/findings.py:L490 | neighbors=[_rule_unauth_access()] | lang=en
- "scanner_findings_rationale_492": "JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only" | kind=entity | source=probe/scanner/findings.py:L492 | neighbors=[_rule_tls_server_fingerprint()] | lang=en
- "scanner_findings_rationale_512": "Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e" | kind=entity | source=probe/scanner/findings.py:L512 | neighbors=[_rule_rdp()] | lang=en
- "scanner_findings_rationale_516": "JA4S-based threat-intel match on the TLS ServerHello fingerprint. Fires only" | kind=entity | source=probe/scanner/findings.py:L516 | neighbors=[_rule_tls_server_fingerprint()] | lang=en
- "scanner_findings_rationale_536": "Confirmed RDP (X.224 handshake) + NLA detection. Runs before the port-hint     e" | kind=entity | source=probe/scanner/findings.py:L536 | neighbors=[_rule_rdp()] | lang=en
- "scanner_findings_rationale_560": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=probe/scanner/findings.py:L560 | neighbors=[_corr_ntlm_relay()] | lang=en
- "scanner_findings_rationale_577": "Anonymous SMB (null-session) information disclosure. The null session is a     m" | kind=entity | source=probe/scanner/findings.py:L577 | neighbors=[_rule_smb_enum()] | lang=en
- "scanner_findings_rationale_583": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=probe/scanner/findings.py:L583 | neighbors=[_corr_legacy_windows()] | lang=en
- "scanner_findings_rationale_600": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=probe/scanner/findings.py:L600 | neighbors=[_corr_cleartext_cluster()] | lang=en

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
