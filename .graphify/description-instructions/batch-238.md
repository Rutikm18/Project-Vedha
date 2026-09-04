# Node Description Batch 239 of 330

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

- "scanner_delta_scanner_rationale_299": "Heuristic priority for a newly-detected service." | kind=entity | source=probe/scanner/delta_scanner.py:L299 | neighbors=[_new_service_severity()] | lang=en
- "scanner_delta_scanner_rationale_309": "True if version changed in a security-relevant way (not just whitespace)." | kind=entity | source=probe/scanner/delta_scanner.py:L309 | neighbors=[_significant_version_change()] | lang=en
- "scanner_delta_scanner_rationale_311": "True if version changed in a security-relevant way (not just whitespace)." | kind=entity | source=probe/scanner/delta_scanner.py:L311 | neighbors=[_significant_version_change()] | lang=en
- "scanner_delta_scanner_rationale_54": "Normalised representation of one ScanResult JSONL line." | kind=entity | source=probe/scanner/delta_scanner.py:L54 | neighbors=[ScanRecord] | lang=en
- "scanner_delta_scanner_rationale_56": "Normalised representation of one ScanResult JSONL line." | kind=entity | source=probe/scanner/delta_scanner.py:L56 | neighbors=[ScanRecord] | lang=en
- "scanner_delta_scanner_rationale_70": "One security-relevant change between two scans." | kind=entity | source=probe/scanner/delta_scanner.py:L70 | neighbors=[Delta] | lang=en
- "scanner_delta_scanner_rationale_72": "One security-relevant change between two scans." | kind=entity | source=probe/scanner/delta_scanner.py:L72 | neighbors=[Delta] | lang=en
- "scanner_delta_scanner_rationale_92": "Derive a stable host identity from a raw scan record in priority order:       1." | kind=entity | source=probe/scanner/delta_scanner.py:L92 | neighbors=[_stable_host_id()] | lang=en
- "scanner_delta_scanner_rationale_94": "Derive a stable host identity from a raw scan record in priority order:       1." | kind=entity | source=probe/scanner/delta_scanner.py:L94 | neighbors=[_stable_host_id()] | lang=en
- "scanner_device_classifier_rationale_1": "device_classifier.py — infer a device's ROLE from collection-layer facts.  This" | kind=entity | source=probe/scanner/device_classifier.py:L1 | neighbors=[device_classifier.py] | lang=en
- "scanner_device_classifier_rationale_102": "Fuse OS family + open ports + service products into a device-role guess.      Re" | kind=entity | source=probe/scanner/device_classifier.py:L102 | neighbors=[classify_device()] | lang=pt
- "scanner_device_classifier_rationale_116": "Fuse OS family + open ports + service products into a device-role guess.      Re" | kind=entity | source=probe/scanner/device_classifier.py:L116 | neighbors=[classify_device()] | lang=pt
- "scanner_device_classifier_rationale_202": "Convenience adapter: extract classifier inputs from a list of ScanResult     obj" | kind=entity | source=probe/scanner/device_classifier.py:L202 | neighbors=[classify_from_results()] | lang=en
- "scanner_device_classifier_rationale_238": "Convenience adapter: extract classifier inputs from a list of ScanResult     obj" | kind=entity | source=probe/scanner/device_classifier.py:L238 | neighbors=[classify_from_results()] | lang=en
- "scanner_dns_scanner_dnsscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L91 | neighbors=[DNSScanner] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-238.json

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
