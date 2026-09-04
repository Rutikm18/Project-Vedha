# Node Description Batch 211 of 332

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

- "lib_target_parser_toapitargets": "toApiTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L127 | neighbors=[target-parser.ts] | lang=en
- "lib_tenant_reserved": "RESERVED" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L15 | neighbors=[tenant.ts] | lang=en
- "lib_testssl_parser_skip_severity": "SKIP_SEVERITY" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L12 | neighbors=[testssl-parser.ts] | lang=en
- "lib_testssl_parser_testsslissue": "TestsslIssue" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L4 | neighbors=[testssl-parser.ts] | lang=en
- "lib_testssl_parser_testssloutput": "TestsslOutput" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L26 | neighbors=[testssl-parser.ts] | lang=en
- "lib_testssl_parser_testsslparseresult": "TestsslParseResult" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L28 | neighbors=[testssl-parser.ts] | lang=en
- "lib_whatweb_parser_whatwebparseresult": "WhatWebParseResult" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L6 | neighbors=[whatweb-parser.ts] | lang=en
- "lib_whatweb_parser_whatwebresult": "WhatWebResult" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L1 | neighbors=[whatweb-parser.ts] | lang=en
- "lib_with_backend_backendctx": "BackendCtx" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L12 | neighbors=[with-backend.ts] | lang=en
- "lib_with_backend_handler": "Handler" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L16 | neighbors=[with-backend.ts] | lang=en
- "login_page_loginform": "LoginForm()" | kind=code-symbol | source=manager/frontend/app/login/page.tsx:L18 | neighbors=[page.tsx] | lang=en
- "login_page_loginpage": "LoginPage()" | kind=code-symbol | source=manager/frontend/app/login/page.tsx:L10 | neighbors=[page.tsx] | lang=en
- "login_page_portalloginpage": "PortalLoginPage()" | kind=code-symbol | source=manager/frontend/app/portal/login/page.tsx:L7 | neighbors=[page.tsx] | lang=en
- "logout_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/portal/logout/route.ts:L6 | neighbors=[route.ts] | lang=en
- "main_scripts_accuracy_gate_rationale_101": "True when this corpus's labels can support an ACCURACY claim." | kind=entity | source=probe/main_scripts/accuracy_gate.py:L101 | neighbors=[is_independent()] | lang=en
- "main_scripts_accuracy_gate_rationale_106": "Threshold violations for one scored corpus (empty list = passed)." | kind=entity | source=probe/main_scripts/accuracy_gate.py:L106 | neighbors=[check_thresholds()] | lang=en
- "main_scripts_accuracy_gate_rationale_143": "Score every corpus in `directory` and collect threshold violations.      Returns" | kind=entity | source=probe/main_scripts/accuracy_gate.py:L143 | neighbors=[run_gate()] | lang=en
- "main_scripts_accuracy_gate_rationale_62": "A corpus is malformed or unlabeled — a gate failure, never a silent pass." | kind=entity | source=probe/main_scripts/accuracy_gate.py:L62 | neighbors=[CorpusError] | lang=pt
- "main_scripts_accuracy_gate_rationale_66": "Load and structurally validate one corpus file." | kind=entity | source=probe/main_scripts/accuracy_gate.py:L66 | neighbors=[load_corpus()] | lang=en
- "main_scripts_accuracy_gate_rationale_93": "Every *.json corpus in `directory`, sorted by name for stable reports." | kind=entity | source=probe/main_scripts/accuracy_gate.py:L93 | neighbors=[load_corpora()] | lang=en
- "main_scripts_accuracy_rationale_125": "Run the findings engine over a labeled corpus and score it.      corpus = {name," | kind=entity | source=probe/main_scripts/accuracy.py:L125 | neighbors=[evaluate_corpus()] | lang=en
- "main_scripts_accuracy_rationale_49": "Precision / recall / F1 of produced findings vs a labeled expected set.      Key" | kind=entity | source=probe/main_scripts/accuracy.py:L49 | neighbors=[score_findings()] | lang=en
- "main_scripts_accuracy_rationale_80": "(target, port) -> status, from port/syn/mass scan facts (last one wins)." | kind=entity | source=probe/main_scripts/accuracy.py:L80 | neighbors=[_observed_states()] | lang=en
- "main_scripts_accuracy_rationale_95": "OPEN precision/recall + overall state accuracy vs a remote-validated     ground" | kind=entity | source=probe/main_scripts/accuracy.py:L95 | neighbors=[score_port_states()] | lang=pt
- "main_scripts_adaptive_timeout_adaptivetimeout_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L21 | neighbors=[AdaptiveTimeout] | lang=en
- "main_scripts_adaptive_timeout_rationale_32": "Fold one round-trip sample (seconds) into the estimate. Ignores         missing/" | kind=entity | source=probe/main_scripts/adaptive_timeout.py:L32 | neighbors=[.observe()] | lang=en
- "main_scripts_adaptive_timeout_rationale_45": "Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp" | kind=entity | source=probe/main_scripts/adaptive_timeout.py:L45 | neighbors=[.timeout()] | lang=pt
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-210.json

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
