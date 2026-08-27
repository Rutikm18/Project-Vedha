# Node Description Batch 53 of 92

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

- "agent_validation_rationale_60": "Require every IP/CIDR target to be fully allowed and not excluded." | kind=entity | source=agent/validation.py:L60 | neighbors=[validate_targets()] | lang=en
- "agent_validation_rationale_94": "Return the conservative number of addresses represented by targets." | kind=entity | source=agent/validation.py:L94 | neighbors=[target_address_count()] | lang=en
- "main_scripts_accuracy_rationale_125": "Run the findings engine over a labeled corpus and score it.      corpus = {name," | kind=entity | source=main_scripts/accuracy.py:L125 | neighbors=[evaluate_corpus()] | lang=en
- "main_scripts_accuracy_rationale_49": "Precision / recall / F1 of produced findings vs a labeled expected set.      Key" | kind=entity | source=main_scripts/accuracy.py:L49 | neighbors=[score_findings()] | lang=en
- "main_scripts_accuracy_rationale_80": "(target, port) -> status, from port/syn/mass scan facts (last one wins)." | kind=entity | source=main_scripts/accuracy.py:L80 | neighbors=[_observed_states()] | lang=en
- "main_scripts_accuracy_rationale_95": "OPEN precision/recall + overall state accuracy vs a remote-validated     ground" | kind=entity | source=main_scripts/accuracy.py:L95 | neighbors=[score_port_states()] | lang=pt
- "main_scripts_adaptive_timeout_adaptivetimeout_init": ".__init__()" | kind=code-symbol | source=main_scripts/adaptive_timeout.py:L21 | neighbors=[AdaptiveTimeout] | lang=en
- "main_scripts_adaptive_timeout_rationale_32": "Fold one round-trip sample (seconds) into the estimate. Ignores         missing/" | kind=entity | source=main_scripts/adaptive_timeout.py:L32 | neighbors=[.observe()] | lang=en
- "main_scripts_adaptive_timeout_rationale_45": "Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp" | kind=entity | source=main_scripts/adaptive_timeout.py:L45 | neighbors=[.timeout()] | lang=pt
- "main_scripts_adaptive_timeout_rationale_55": "Convenience: build an estimator and fold in a sequence of RTT samples." | kind=entity | source=main_scripts/adaptive_timeout.py:L55 | neighbors=[from_rtts()] | lang=en
- "main_scripts_db_scanner_dbscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/db_scanner.py:L240 | neighbors=[DBScanner] | lang=en
- "main_scripts_db_scanner_main": "main()" | kind=code-symbol | source=main_scripts/db_scanner.py:L287 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mongodb": "_probe_mongodb()" | kind=code-symbol | source=main_scripts/db_scanner.py:L131 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mssql": "_probe_mssql()" | kind=code-symbol | source=main_scripts/db_scanner.py:L82 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mysql": "_probe_mysql()" | kind=code-symbol | source=main_scripts/db_scanner.py:L47 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mysqlx": "_probe_mysqlx()" | kind=code-symbol | source=main_scripts/db_scanner.py:L166 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_oracle": "_probe_oracle()" | kind=code-symbol | source=main_scripts/db_scanner.py:L195 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_postgres": "_probe_postgres()" | kind=code-symbol | source=main_scripts/db_scanner.py:L67 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_delta_scanner_rationale_1": "delta_scanner.py — scan-state comparison and continuous attack-surface monitorin" | kind=entity | source=main_scripts/delta_scanner.py:L1 | neighbors=[delta_scanner.py] | lang=en
- "main_scripts_delta_scanner_rationale_122": "Best-effort service name from data dict or scanner name." | kind=entity | source=main_scripts/delta_scanner.py:L122 | neighbors=[_extract_service()] | lang=en
- "main_scripts_delta_scanner_rationale_139": "Best-effort version string." | kind=entity | source=main_scripts/delta_scanner.py:L139 | neighbors=[_extract_version()] | lang=en
- "main_scripts_delta_scanner_rationale_158": "Load JSONL scan snapshots and compute security-relevant diffs." | kind=entity | source=main_scripts/delta_scanner.py:L158 | neighbors=[DeltaEngine] | lang=en
- "main_scripts_delta_scanner_rationale_161": "Parse a JSONL file of ScanResult records and return a SnapshotIndex.         Lin" | kind=entity | source=main_scripts/delta_scanner.py:L161 | neighbors=[.load_jsonl()] | lang=en
- "main_scripts_delta_scanner_rationale_206": "Compute security-relevant deltas between baseline and current snapshots." | kind=entity | source=main_scripts/delta_scanner.py:L206 | neighbors=[.diff()] | lang=en
- "main_scripts_delta_scanner_rationale_297": "Heuristic priority for a newly-detected service." | kind=entity | source=main_scripts/delta_scanner.py:L297 | neighbors=[_new_service_severity()] | lang=en
- "main_scripts_delta_scanner_rationale_309": "True if version changed in a security-relevant way (not just whitespace)." | kind=entity | source=main_scripts/delta_scanner.py:L309 | neighbors=[_significant_version_change()] | lang=en
- "main_scripts_delta_scanner_rationale_54": "Normalised representation of one ScanResult JSONL line." | kind=entity | source=main_scripts/delta_scanner.py:L54 | neighbors=[ScanRecord] | lang=en
- "main_scripts_delta_scanner_rationale_70": "One security-relevant change between two scans." | kind=entity | source=main_scripts/delta_scanner.py:L70 | neighbors=[Delta] | lang=en
- "main_scripts_delta_scanner_rationale_92": "Derive a stable host identity from a raw scan record in priority order:       1." | kind=entity | source=main_scripts/delta_scanner.py:L92 | neighbors=[_stable_host_id()] | lang=en
- "main_scripts_device_classifier_rationale_1": "device_classifier.py — infer a device's ROLE from collection-layer facts.  This" | kind=entity | source=main_scripts/device_classifier.py:L1 | neighbors=[device_classifier.py] | lang=en
- "main_scripts_device_classifier_rationale_102": "Fuse OS family + open ports + service products into a device-role guess.      Re" | kind=entity | source=main_scripts/device_classifier.py:L102 | neighbors=[classify_device()] | lang=pt
- "main_scripts_device_classifier_rationale_202": "Convenience adapter: extract classifier inputs from a list of ScanResult     obj" | kind=entity | source=main_scripts/device_classifier.py:L202 | neighbors=[classify_from_results()] | lang=en
- "main_scripts_findings_rationale_1004": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=main_scripts/findings.py:L1004 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_1012": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=main_scripts/findings.py:L1012 | neighbors=[load_facts_jsonl()] | lang=pt
- "main_scripts_findings_rationale_1013": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=main_scripts/findings.py:L1013 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_1014": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=main_scripts/findings.py:L1014 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_findings_rationale_1027": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=main_scripts/findings.py:L1027 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_1028": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=main_scripts/findings.py:L1028 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_1030": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=main_scripts/findings.py:L1030 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_1037": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=main_scripts/findings.py:L1037 | neighbors=[_corr_legacy_windows()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-052.json

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
