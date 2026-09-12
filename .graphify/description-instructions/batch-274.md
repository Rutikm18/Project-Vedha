# Node Description Batch 275 of 380

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

- "scan_page_scannerrun": "ScannerRun" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L66 | neighbors=[page.tsx] | lang=en
- "scan_page_scanpage": "ScanPage()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1220 | neighbors=[page.tsx] | lang=en
- "scan_page_sectionlabel": "SectionLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L161 | neighbors=[page.tsx] | lang=en
- "scan_page_uc_meta": "UC_META" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L113 | neighbors=[page.tsx] | lang=en
- "scan_page_usecase": "UseCase" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L23 | neighbors=[page.tsx] | lang=en
- "scan_page_usecasecard": "UseCaseCard()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L328 | neighbors=[page.tsx] | lang=en
- "scanner_accuracy_gate_rationale_101": "True when this corpus's labels can support an ACCURACY claim." | kind=entity | source=probe/scanner/accuracy_gate.py:L101 | neighbors=[is_independent()] | lang=en
- "scanner_accuracy_gate_rationale_106": "Threshold violations for one scored corpus (empty list = passed)." | kind=entity | source=probe/scanner/accuracy_gate.py:L106 | neighbors=[check_thresholds()] | lang=en
- "scanner_accuracy_gate_rationale_143": "Score every corpus in `directory` and collect threshold violations.      Returns" | kind=entity | source=probe/scanner/accuracy_gate.py:L143 | neighbors=[run_gate()] | lang=en
- "scanner_accuracy_gate_rationale_62": "A corpus is malformed or unlabeled — a gate failure, never a silent pass." | kind=entity | source=probe/scanner/accuracy_gate.py:L62 | neighbors=[CorpusError] | lang=pt
- "scanner_accuracy_gate_rationale_66": "Load and structurally validate one corpus file." | kind=entity | source=probe/scanner/accuracy_gate.py:L66 | neighbors=[load_corpus()] | lang=en
- "scanner_accuracy_gate_rationale_93": "Every *.json corpus in `directory`, sorted by name for stable reports." | kind=entity | source=probe/scanner/accuracy_gate.py:L93 | neighbors=[load_corpora()] | lang=en
- "scanner_accuracy_rationale_125": "Run the findings engine over a labeled corpus and score it.      corpus = {name," | kind=entity | source=probe/scanner/accuracy.py:L125 | neighbors=[evaluate_corpus()] | lang=en
- "scanner_accuracy_rationale_49": "Precision / recall / F1 of produced findings vs a labeled expected set.      Key" | kind=entity | source=probe/scanner/accuracy.py:L49 | neighbors=[score_findings()] | lang=en
- "scanner_accuracy_rationale_80": "(target, port) -> status, from port/syn/mass scan facts (last one wins)." | kind=entity | source=probe/scanner/accuracy.py:L80 | neighbors=[_observed_states()] | lang=en
- "scanner_accuracy_rationale_95": "OPEN precision/recall + overall state accuracy vs a remote-validated     ground" | kind=entity | source=probe/scanner/accuracy.py:L95 | neighbors=[score_port_states()] | lang=pt
- "scanner_adaptive_timeout_adaptivetimeout_init": ".__init__()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L21 | neighbors=[AdaptiveTimeout] | lang=en
- "scanner_adaptive_timeout_rationale_32": "Fold one round-trip sample (seconds) into the estimate. Ignores         missing/" | kind=entity | source=probe/scanner/adaptive_timeout.py:L32 | neighbors=[.observe()] | lang=en
- "scanner_adaptive_timeout_rationale_45": "Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp" | kind=entity | source=probe/scanner/adaptive_timeout.py:L45 | neighbors=[.timeout()] | lang=pt
- "scanner_adaptive_timeout_rationale_55": "Convenience: build an estimator and fold in a sequence of RTT samples." | kind=entity | source=probe/scanner/adaptive_timeout.py:L55 | neighbors=[from_rtts()] | lang=en
- "scanner_cpe_rationale_1": "cpe.py — derive a CPE 2.3 identity from an observed (service, product, version)." | kind=entity | source=probe/scanner/cpe.py:L1 | neighbors=[cpe.py] | lang=en
- "scanner_cpe_rationale_104": "Prefer an explicit version field; else pull a version-like token out of the" | kind=entity | source=probe/scanner/cpe.py:L104 | neighbors=[_extract_version()] | lang=en
- "scanner_cpe_rationale_117": "Return {vendor, product, version, cpe23} for a recognized product, else None." | kind=entity | source=probe/scanner/cpe.py:L117 | neighbors=[to_cpe()] | lang=en
- "scanner_db_scanner_dbscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L456 | neighbors=[DBScanner] | lang=en
- "scanner_db_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L504 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_mysqlx": "_probe_mysqlx()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L363 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_oracle": "_probe_oracle()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L392 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_postgres": "_probe_postgres()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L98 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_rationale_1": "db_scanner.py — fingerprint database services.  WHY: databases are everywhere on" | kind=entity | source=probe/scanner/db_scanner.py:L1 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_rationale_102": "Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act" | kind=entity | source=probe/scanner/db_scanner.py:L102 | neighbors=[interpret_redis_info()] | lang=en
- "scanner_db_scanner_rationale_131": "A well-formed PRELOGIN request (MS-TDS 2.2.6.5).      The previous request's opt" | kind=entity | source=probe/scanner/db_scanner.py:L131 | neighbors=[_build_tds_prelogin()] | lang=en
- "scanner_db_scanner_rationale_165": "Read server version and encryption posture out of a TDS PRELOGIN reply.      Pos" | kind=entity | source=probe/scanner/db_scanner.py:L165 | neighbors=[parse_tds_prelogin()] | lang=en
- "scanner_db_scanner_rationale_229": "Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act" | kind=entity | source=probe/scanner/db_scanner.py:L229 | neighbors=[interpret_redis_info()] | lang=en
- "scanner_db_scanner_rationale_259": "Frame a single-field admin command as OP_MSG (opcode 2013).      MongoDB 5.1 REM" | kind=entity | source=probe/scanner/db_scanner.py:L259 | neighbors=[build_op_msg_command()] | lang=pt
- "scanner_db_scanner_rationale_289": "Pull a MongoDB server version out of a wire reply, or None.      The isMaster ha" | kind=entity | source=probe/scanner/db_scanner.py:L289 | neighbors=[extract_mongo_version()] | lang=en
- "scanner_db_scanner_rationale_301": "Classify a serverStatus reply into auth posture.      Returns {} when the reply" | kind=entity | source=probe/scanner/db_scanner.py:L301 | neighbors=[interpret_mongodb_auth()] | lang=en
- "scanner_db_scanner_rationale_435": "Stamp the `db: True` discriminator onto every db_scan fact.      Every sibling d" | kind=entity | source=probe/scanner/db_scanner.py:L435 | neighbors=[stamp_db_fact()] | lang=en
- "scanner_db_scanner_rationale_54": "Parse a MySQL/MariaDB initial handshake packet.      Returns None when this is n" | kind=entity | source=probe/scanner/db_scanner.py:L54 | neighbors=[parse_mysql_greeting()] | lang=en
- "scanner_delta_scanner_rationale_1": "delta_scanner.py — scan-state comparison and continuous attack-surface monitorin" | kind=entity | source=probe/scanner/delta_scanner.py:L1 | neighbors=[delta_scanner.py] | lang=en
- "scanner_delta_scanner_rationale_122": "Best-effort service name from data dict or scanner name." | kind=entity | source=probe/scanner/delta_scanner.py:L122 | neighbors=[_extract_service()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-274.json

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
