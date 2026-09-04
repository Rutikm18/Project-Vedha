# Node Description Batch 126 of 332

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "commands_interactive_w": "w()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L31 | neighbors=[interactive.ts, wizardAsk()]
- "commands_login_buildlogincommand": "buildLoginCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L46 | neighbors=[index.ts, login.ts]
- "commands_logout_buildlogoutcommand": "buildLogoutCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L4 | neighbors=[index.ts, logout.ts]
- "commands_report_buildreportcommand": "buildReportCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L85 | neighbors=[index.ts, report.ts]
- "commands_scan_buildscancommand": "buildScanCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L143 | neighbors=[index.ts, scan.ts]
- "commands_status_buildstatuscommand": "buildStatusCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L21 | neighbors=[index.ts, status.ts]
- "commands_tools_buildtoolscommand": "buildToolsCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L29 | neighbors=[index.ts, tools.ts]
- "commands_tools_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L14 | neighbors=[tools.ts, showSpinner()]
- "commands_tools_showspinner": "showSpinner()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L16 | neighbors=[tools.ts, ln()]
- "commands_whoami_buildwhoamicommand": "buildWhoamiCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L4 | neighbors=[index.ts, whoami.ts]
- "components_engagementstatuscontrol_engagementstatuscontrol": "EngagementStatusControl()" | kind=code-symbol | source=manager/frontend/components/EngagementStatusControl.tsx:L59 | neighbors=[EngagementStatusControl.tsx, page.tsx]
- "components_engagementstatuscontrol_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/components/EngagementStatusControl.tsx:L39 | neighbors=[EngagementStatusControl.tsx, page.tsx]
- "components_queryprovider_queryprovider": "QueryProvider()" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L6 | neighbors=[layout.tsx, QueryProvider.tsx]
- "components_themeprovider_themeprovider": "ThemeProvider()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L30 | neighbors=[layout.tsx, ThemeProvider.tsx]
- "components_toastprovider_toastcontext": "ToastContext" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L26 | neighbors=[ToastProvider.tsx, useToast.ts]
- "components_toastprovider_toastprovider": "ToastProvider()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L158 | neighbors=[layout.tsx, ToastProvider.tsx]
- "console_freshness_freshness": "Freshness()" | kind=code-symbol | source=manager/frontend/components/console/Freshness.tsx:L6 | neighbors=[Freshness.tsx, DashboardGrid.tsx]
- "console_primitives_delta": "Delta()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L123 | neighbors=[Primitives.tsx, PostureScorecard.tsx]
- "console_primitives_panel": "Panel()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L15 | neighbors=[Primitives.tsx, DashboardGrid.tsx]
- "console_primitives_readout": "Readout()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L161 | neighbors=[Primitives.tsx, LiveOverview.tsx]
- "console_primitives_severitychip": "SeverityChip()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L78 | neighbors=[Primitives.tsx, SlaStatus.tsx]
- "cve_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/cve/cli.py:L151 | neighbors=[cli.py, main()]
- "cve_cli_cmd_status": "cmd_status()" | kind=code-symbol | source=probe/cve/cli.py:L119 | neighbors=[cli.py, Verify the offline mirror: feed counts,…]
- "cve_cli_main": "main()" | kind=code-symbol | source=probe/cve/cli.py:L192 | neighbors=[cli.py, build_parser()]
- "cve_correlator_as_dict": "_as_dict()" | kind=code-symbol | source=probe/cve/correlator.py:L114 | neighbors=[correlator.py, correlate()]
- "cve_correlator_mirror_age_note": "mirror_age_note()" | kind=code-symbol | source=probe/cve/correlator.py:L30 | neighbors=[correlator.py, Human-readable note on how old the mirr…]
- "cve_correlator_risk_band": "risk_band()" | kind=code-symbol | source=probe/cve/correlator.py:L73 | neighbors=[correlator.py, correlate()]
- "cve_ingest_iter_cpe_matches": "_iter_cpe_matches()" | kind=code-symbol | source=probe/cve/ingest.py:L102 | neighbors=[ingest.py, ingest_one_cve()]
- "cve_init": "__init__.py" | kind=code-symbol | source=probe/cve/__init__.py:L1 | neighbors=[6e2818f Add support for additional serv…, cve — vulnerability (CVE) correlation l…]
- "cve_vulndb_vulndb_add_cpe_match": ".add_cpe_match()" | kind=code-symbol | source=probe/cve/vulndb.py:L79 | neighbors=[VulnDB, _norm()]
- "cve_vulndb_vulndb_commit": ".commit()" | kind=code-symbol | source=probe/cve/vulndb.py:L107 | neighbors=[VulnDB, .__init__()]
- "cve_vulndb_vulndb_enrich": "._enrich()" | kind=code-symbol | source=probe/cve/vulndb.py:L141 | neighbors=[VulnDB, .cves_for_cpe()]
- "cve_vulndb_vulndb_init": ".__init__()" | kind=code-symbol | source=probe/cve/vulndb.py:L63 | neighbors=[VulnDB, .commit()]
- "cve_vulndb_vulndb_upsert_kev": ".upsert_kev()" | kind=code-symbol | source=probe/cve/vulndb.py:L92 | neighbors=[VulnDB, _norm()]
- "cve_weakness_map_assoc": "_Assoc" | kind=code-symbol | source=probe/cve/weakness_map.py:L37 | neighbors=[weakness_map.py, One canonical CVE a weakness can map to…]
- "cve_weakness_map_missing_from_mirror": "missing_from_mirror()" | kind=code-symbol | source=probe/cve/weakness_map.py:L216 | neighbors=[weakness_map.py, Every canonical CVE referenced by the w…]
- "dashboard_liveoverview_verdict": "verdict()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L46 | neighbors=[LiveOverview.tsx, LiveOverview()]
- "dashboard_patchcomparisonmatrix_n": "n()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L45 | neighbors=[PatchComparisonMatrix.tsx, PatchComparisonMatrix()]
- "dashboard_posturescorecard_matrixrow": "MatrixRow" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L26 | neighbors=[PatchComparisonMatrix.tsx, PostureScorecard.tsx]
- "dashboard_slastatus_deadlinetitle": "deadlineTitle()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L75 | neighbors=[SlaStatus.tsx, SlaRowView()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-125.json

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
