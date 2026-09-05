# Node Description Batch 215 of 336

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

- "main_scripts_adaptive_timeout_rationale_55": "Convenience: build an estimator and fold in a sequence of RTT samples." | kind=entity | source=probe/main_scripts/adaptive_timeout.py:L55 | neighbors=[from_rtts()] | lang=en
- "main_scripts_cpe_rationale_1": "cpe.py — derive a CPE 2.3 identity from an observed (service, product, version)." | kind=entity | source=probe/main_scripts/cpe.py:L1 | neighbors=[cpe.py] | lang=en
- "main_scripts_cpe_rationale_104": "Prefer an explicit version field; else pull a version-like token out of the" | kind=entity | source=probe/main_scripts/cpe.py:L104 | neighbors=[_extract_version()] | lang=en
- "main_scripts_cpe_rationale_117": "Return {vendor, product, version, cpe23} for a recognized product, else None." | kind=entity | source=probe/main_scripts/cpe.py:L117 | neighbors=[to_cpe()] | lang=en
- "main_scripts_db_scanner_dbscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L240 | neighbors=[DBScanner] | lang=en
- "main_scripts_db_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L287 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mongodb": "_probe_mongodb()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L131 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mssql": "_probe_mssql()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L82 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mysql": "_probe_mysql()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L47 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_mysqlx": "_probe_mysqlx()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L166 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_oracle": "_probe_oracle()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L195 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_probe_postgres": "_probe_postgres()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L67 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_rationale_1": "db_scanner.py — fingerprint database services.  WHY: databases are everywhere on" | kind=entity | source=probe/main_scripts/db_scanner.py:L1 | neighbors=[db_scanner.py] | lang=en
- "main_scripts_db_scanner_rationale_102": "Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act" | kind=entity | source=probe/main_scripts/db_scanner.py:L102 | neighbors=[interpret_redis_info()] | lang=en
- "main_scripts_delta_scanner_rationale_1": "delta_scanner.py — scan-state comparison and continuous attack-surface monitorin" | kind=entity | source=probe/main_scripts/delta_scanner.py:L1 | neighbors=[delta_scanner.py] | lang=en
- "main_scripts_delta_scanner_rationale_122": "Best-effort service name from data dict or scanner name." | kind=entity | source=probe/main_scripts/delta_scanner.py:L122 | neighbors=[_extract_service()] | lang=en
- "main_scripts_delta_scanner_rationale_124": "Best-effort service name from data dict or scanner name." | kind=entity | source=probe/main_scripts/delta_scanner.py:L124 | neighbors=[_extract_service()] | lang=en
- "main_scripts_delta_scanner_rationale_139": "Best-effort version string." | kind=entity | source=probe/main_scripts/delta_scanner.py:L139 | neighbors=[_extract_version()] | lang=en
- "main_scripts_delta_scanner_rationale_141": "Best-effort version string." | kind=entity | source=probe/main_scripts/delta_scanner.py:L141 | neighbors=[_extract_version()] | lang=en
- "main_scripts_delta_scanner_rationale_158": "Load JSONL scan snapshots and compute security-relevant diffs." | kind=entity | source=probe/main_scripts/delta_scanner.py:L158 | neighbors=[DeltaEngine] | lang=en
- "main_scripts_delta_scanner_rationale_160": "Load JSONL scan snapshots and compute security-relevant diffs." | kind=entity | source=probe/main_scripts/delta_scanner.py:L160 | neighbors=[DeltaEngine] | lang=en
- "main_scripts_delta_scanner_rationale_161": "Parse a JSONL file of ScanResult records and return a SnapshotIndex.         Lin" | kind=entity | source=probe/main_scripts/delta_scanner.py:L161 | neighbors=[.load_jsonl()] | lang=en
- "main_scripts_delta_scanner_rationale_163": "Parse a JSONL file of ScanResult records and return a SnapshotIndex.         Lin" | kind=entity | source=probe/main_scripts/delta_scanner.py:L163 | neighbors=[.load_jsonl()] | lang=en
- "main_scripts_delta_scanner_rationale_206": "Compute security-relevant deltas between baseline and current snapshots." | kind=entity | source=probe/main_scripts/delta_scanner.py:L206 | neighbors=[.diff()] | lang=en
- "main_scripts_delta_scanner_rationale_208": "Compute security-relevant deltas between baseline and current snapshots." | kind=entity | source=probe/main_scripts/delta_scanner.py:L208 | neighbors=[.diff()] | lang=en
- "main_scripts_delta_scanner_rationale_297": "Heuristic priority for a newly-detected service." | kind=entity | source=probe/main_scripts/delta_scanner.py:L297 | neighbors=[_new_service_severity()] | lang=en
- "main_scripts_delta_scanner_rationale_299": "Heuristic priority for a newly-detected service." | kind=entity | source=probe/main_scripts/delta_scanner.py:L299 | neighbors=[_new_service_severity()] | lang=en
- "main_scripts_delta_scanner_rationale_309": "True if version changed in a security-relevant way (not just whitespace)." | kind=entity | source=probe/main_scripts/delta_scanner.py:L309 | neighbors=[_significant_version_change()] | lang=en
- "main_scripts_delta_scanner_rationale_311": "True if version changed in a security-relevant way (not just whitespace)." | kind=entity | source=probe/main_scripts/delta_scanner.py:L311 | neighbors=[_significant_version_change()] | lang=en
- "main_scripts_delta_scanner_rationale_54": "Normalised representation of one ScanResult JSONL line." | kind=entity | source=probe/main_scripts/delta_scanner.py:L54 | neighbors=[ScanRecord] | lang=en
- "main_scripts_delta_scanner_rationale_56": "Normalised representation of one ScanResult JSONL line." | kind=entity | source=probe/main_scripts/delta_scanner.py:L56 | neighbors=[ScanRecord] | lang=en
- "main_scripts_delta_scanner_rationale_70": "One security-relevant change between two scans." | kind=entity | source=probe/main_scripts/delta_scanner.py:L70 | neighbors=[Delta] | lang=en
- "main_scripts_delta_scanner_rationale_72": "One security-relevant change between two scans." | kind=entity | source=probe/main_scripts/delta_scanner.py:L72 | neighbors=[Delta] | lang=en
- "main_scripts_delta_scanner_rationale_92": "Derive a stable host identity from a raw scan record in priority order:       1." | kind=entity | source=probe/main_scripts/delta_scanner.py:L92 | neighbors=[_stable_host_id()] | lang=en
- "main_scripts_delta_scanner_rationale_94": "Derive a stable host identity from a raw scan record in priority order:       1." | kind=entity | source=probe/main_scripts/delta_scanner.py:L94 | neighbors=[_stable_host_id()] | lang=en
- "main_scripts_device_classifier_rationale_1": "device_classifier.py — infer a device's ROLE from collection-layer facts.  This" | kind=entity | source=probe/main_scripts/device_classifier.py:L1 | neighbors=[device_classifier.py] | lang=en
- "main_scripts_device_classifier_rationale_102": "Fuse OS family + open ports + service products into a device-role guess.      Re" | kind=entity | source=probe/main_scripts/device_classifier.py:L102 | neighbors=[classify_device()] | lang=pt
- "main_scripts_device_classifier_rationale_116": "Fuse OS family + open ports + service products into a device-role guess.      Re" | kind=entity | source=probe/main_scripts/device_classifier.py:L116 | neighbors=[classify_device()] | lang=pt
- "main_scripts_device_classifier_rationale_182": "Convenience adapter: extract classifier inputs from a list of ScanResult     obj" | kind=entity | source=probe/main_scripts/device_classifier.py:L182 | neighbors=[classify_from_results()] | lang=en
- "main_scripts_device_classifier_rationale_202": "Convenience adapter: extract classifier inputs from a list of ScanResult     obj" | kind=entity | source=probe/main_scripts/device_classifier.py:L202 | neighbors=[classify_from_results()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-214.json

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
