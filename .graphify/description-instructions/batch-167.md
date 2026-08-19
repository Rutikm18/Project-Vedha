# Node Description Batch 168 of 227

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

- "scan_page_enginemanifest": "EngineManifest" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L72 | neighbors=[page.tsx] | lang=en
- "scan_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L166 | neighbors=[page.tsx] | lang=en
- "scan_page_fleetstrip": "FleetStrip()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L190 | neighbors=[page.tsx] | lang=en
- "scan_page_hudframe": "HudFrame()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L175 | neighbors=[page.tsx] | lang=en
- "scan_page_intensity": "Intensity" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L125 | neighbors=[page.tsx] | lang=en
- "scan_page_intensitydial": "IntensityDial()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L287 | neighbors=[page.tsx] | lang=en
- "scan_page_jobpanel": "JobPanel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L335 | neighbors=[page.tsx] | lang=en
- "scan_page_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L47 | neighbors=[page.tsx] | lang=en
- "scan_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L333 | neighbors=[page.tsx] | lang=en
- "scan_page_probe": "Probe" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L27 | neighbors=[page.tsx] | lang=en
- "scan_page_profile_badge": "PROFILE_BADGE" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L114 | neighbors=[page.tsx] | lang=en
- "scan_page_risk": "RISK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L107 | neighbors=[page.tsx] | lang=en
- "scan_page_scannerrun": "ScannerRun" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L60 | neighbors=[page.tsx] | lang=en
- "scan_page_scanpage": "ScanPage()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L554 | neighbors=[page.tsx] | lang=en
- "scan_page_sectionlabel": "SectionLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L155 | neighbors=[page.tsx] | lang=en
- "scan_page_uc_meta": "UC_META" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L92 | neighbors=[page.tsx] | lang=en
- "scan_page_usecase": "UseCase" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L18 | neighbors=[page.tsx] | lang=en
- "scan_page_usecasecard": "UseCaseCard()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L257 | neighbors=[page.tsx] | lang=en
- "scanner_accuracy_rationale_125": "Run the findings engine over a labeled corpus and score it.      corpus = {name," | kind=entity | source=probe/scanner/accuracy.py:L125 | neighbors=[evaluate_corpus()] | lang=en
- "scanner_accuracy_rationale_49": "Precision / recall / F1 of produced findings vs a labeled expected set.      Key" | kind=entity | source=probe/scanner/accuracy.py:L49 | neighbors=[score_findings()] | lang=en
- "scanner_accuracy_rationale_80": "(target, port) -> status, from port/syn/mass scan facts (last one wins)." | kind=entity | source=probe/scanner/accuracy.py:L80 | neighbors=[_observed_states()] | lang=en
- "scanner_accuracy_rationale_95": "OPEN precision/recall + overall state accuracy vs a remote-validated     ground" | kind=entity | source=probe/scanner/accuracy.py:L95 | neighbors=[score_port_states()] | lang=pt
- "scanner_adaptive_timeout_adaptivetimeout_init": ".__init__()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L21 | neighbors=[AdaptiveTimeout] | lang=en
- "scanner_adaptive_timeout_rationale_32": "Fold one round-trip sample (seconds) into the estimate. Ignores         missing/" | kind=entity | source=probe/scanner/adaptive_timeout.py:L32 | neighbors=[.observe()] | lang=en
- "scanner_adaptive_timeout_rationale_45": "Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp" | kind=entity | source=probe/scanner/adaptive_timeout.py:L45 | neighbors=[.timeout()] | lang=pt
- "scanner_adaptive_timeout_rationale_55": "Convenience: build an estimator and fold in a sequence of RTT samples." | kind=entity | source=probe/scanner/adaptive_timeout.py:L55 | neighbors=[from_rtts()] | lang=en
- "scanner_db_scanner_dbscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L240 | neighbors=[DBScanner] | lang=en
- "scanner_db_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L287 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_mongodb": "_probe_mongodb()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L131 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_mssql": "_probe_mssql()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L82 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_mysql": "_probe_mysql()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L47 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_mysqlx": "_probe_mysqlx()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L166 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_oracle": "_probe_oracle()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L195 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_probe_postgres": "_probe_postgres()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L67 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_rationale_1": "db_scanner.py — fingerprint database services.  WHY: databases are everywhere on" | kind=entity | source=probe/scanner/db_scanner.py:L1 | neighbors=[db_scanner.py] | lang=en
- "scanner_db_scanner_rationale_102": "Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act" | kind=entity | source=probe/scanner/db_scanner.py:L102 | neighbors=[interpret_redis_info()] | lang=en
- "scanner_delta_scanner_rationale_1": "delta_scanner.py — scan-state comparison and continuous attack-surface monitorin" | kind=entity | source=probe/scanner/delta_scanner.py:L1 | neighbors=[delta_scanner.py] | lang=en
- "scanner_delta_scanner_rationale_122": "Best-effort service name from data dict or scanner name." | kind=entity | source=probe/scanner/delta_scanner.py:L122 | neighbors=[_extract_service()] | lang=en
- "scanner_delta_scanner_rationale_139": "Best-effort version string." | kind=entity | source=probe/scanner/delta_scanner.py:L139 | neighbors=[_extract_version()] | lang=en
- "scanner_delta_scanner_rationale_158": "Load JSONL scan snapshots and compute security-relevant diffs." | kind=entity | source=probe/scanner/delta_scanner.py:L158 | neighbors=[DeltaEngine] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-167.json

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
