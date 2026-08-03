# Node Description Batch 101 of 131

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "scan_page_jobpanel": "JobPanel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L335 | neighbors=[page.tsx]
- "scan_page_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L47 | neighbors=[page.tsx]
- "scan_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L333 | neighbors=[page.tsx]
- "scan_page_probe": "Probe" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L27 | neighbors=[page.tsx]
- "scan_page_profile_badge": "PROFILE_BADGE" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L114 | neighbors=[page.tsx]
- "scan_page_risk": "RISK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L107 | neighbors=[page.tsx]
- "scan_page_scannerrun": "ScannerRun" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L60 | neighbors=[page.tsx]
- "scan_page_scanpage": "ScanPage()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L554 | neighbors=[page.tsx]
- "scan_page_sectionlabel": "SectionLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L155 | neighbors=[page.tsx]
- "scan_page_uc_meta": "UC_META" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L92 | neighbors=[page.tsx]
- "scan_page_usecase": "UseCase" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L18 | neighbors=[page.tsx]
- "scan_page_usecasecard": "UseCaseCard()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L257 | neighbors=[page.tsx]
- "scanner_db_scanner_dbscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L240 | neighbors=[DBScanner]
- "scanner_db_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L287 | neighbors=[db_scanner.py]
- "scanner_db_scanner_probe_mongodb": "_probe_mongodb()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L131 | neighbors=[db_scanner.py]
- "scanner_db_scanner_probe_mssql": "_probe_mssql()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L82 | neighbors=[db_scanner.py]
- "scanner_db_scanner_probe_mysql": "_probe_mysql()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L47 | neighbors=[db_scanner.py]
- "scanner_db_scanner_probe_mysqlx": "_probe_mysqlx()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L166 | neighbors=[db_scanner.py]
- "scanner_db_scanner_probe_oracle": "_probe_oracle()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L195 | neighbors=[db_scanner.py]
- "scanner_db_scanner_probe_postgres": "_probe_postgres()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L67 | neighbors=[db_scanner.py]
- "scanner_db_scanner_rationale_1": "db_scanner.py — fingerprint database services.  WHY: databases are everywhere on" | kind=entity | source=probe/scanner/db_scanner.py:L1 | neighbors=[db_scanner.py]
- "scanner_db_scanner_rationale_102": "Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act" | kind=entity | source=probe/scanner/db_scanner.py:L102 | neighbors=[interpret_redis_info()]
- "scanner_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L32 | neighbors=[HostDiscoveryScanner]
- "scanner_host_discovery_main": "main()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L84 | neighbors=[host_discovery.py]
- "scanner_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive.  METHOD (collection only):" | kind=entity | source=probe/scanner/host_discovery.py:L1 | neighbors=[host_discovery.py]
- "scanner_host_discovery_rationale_33": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L33 | neighbors=[._probe()]
- "scanner_host_discovery_rationale_37": "Return 'open', 'refused', or None (no response)." | kind=entity | source=probe/scanner/host_discovery.py:L37 | neighbors=[._probe()]
- "scanner_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=probe/scanner/__init__.py:L1 | neighbors=[__init__.py]
- "scanner_mass_scan_connectsweep_init": ".__init__()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L209 | neighbors=[_ConnectSweep]
- "scanner_mass_scan_main": "main()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L341 | neighbors=[mass_scan.py]
- "scanner_mass_scan_rationale_1": "mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con" | kind=entity | source=probe/scanner/mass_scan.py:L1 | neighbors=[mass_scan.py]
- "scanner_mass_scan_rationale_148": "Parse masscan -oJ output robustly: handles trailing comma, 'finished'     sentin" | kind=entity | source=probe/scanner/mass_scan.py:L148 | neighbors=[_parse_masscan_json()]
- "scanner_mass_scan_rationale_176": "target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them." | kind=entity | source=probe/scanner/mass_scan.py:L176 | neighbors=[run_mass_scan()]
- "scanner_mass_scan_rationale_216": "Excluded networks -> masscan --exclude specs, so they get ZERO packets." | kind=entity | source=probe/scanner/mass_scan.py:L216 | neighbors=[_masscan_excludes()]
- "scanner_mass_scan_rationale_221": "A CIDR spec is in scope only if it is fully contained in an allowed network." | kind=entity | source=probe/scanner/mass_scan.py:L221 | neighbors=[_spec_in_scope()]
- "scanner_mass_scan_rationale_243": "target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them." | kind=entity | source=probe/scanner/mass_scan.py:L243 | neighbors=[run_mass_scan()]
- "scanner_mass_scan_rationale_308": "Excluded networks -> masscan --exclude specs, so they get ZERO packets." | kind=entity | source=probe/scanner/mass_scan.py:L308 | neighbors=[_masscan_excludes()]
- "scanner_mass_scan_rationale_313": "A CIDR spec is in scope only if it is fully contained in an allowed network." | kind=entity | source=probe/scanner/mass_scan.py:L313 | neighbors=[_spec_in_scope()]
- "scanner_mass_scan_rationale_55": "Run masscan over the given target specs and return its parsed JSON records." | kind=entity | source=probe/scanner/mass_scan.py:L55 | neighbors=[_run_masscan()]
- "scanner_mass_scan_rationale_66": "Run masscan over the given target specs and return its parsed JSON records." | kind=entity | source=probe/scanner/mass_scan.py:L66 | neighbors=[_run_masscan()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-100.json

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
