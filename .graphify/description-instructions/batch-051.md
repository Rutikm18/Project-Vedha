# Node Description Batch 52 of 104

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

- "routers_agents_register_agent": "register_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L277 | neighbors=[agents.py, AgentRegisterResponse]
- "routers_agents_resolve_scan_type": "_resolve_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L57 | neighbors=[agents.py, enqueue_agent_job()]
- "routers_agents_submit_job_result": "submit_job_result()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L619 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_ai_report_approve_report": "approve_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L133 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_get_draft": "get_draft()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L116 | neighbors=[ai_report.py, _output_out()]
- "routers_ai_report_output_out": "_output_out()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L198 | neighbors=[ai_report.py, get_draft()]
- "routers_ai_report_reject_report": "reject_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L155 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L359 | neighbors=[ai_report.py, _run_generation()]
- "routers_attack_paths_explain_hop": "_explain_hop()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L246 | neighbors=[attack_paths.py, get_attack_path()]
- "routers_attack_paths_path_summary": "_path_summary()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L235 | neighbors=[attack_paths.py, list_attack_paths()]
- "routers_detection_get_results": "get_results()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L128 | neighbors=[detection.py, _result_out()]
- "routers_detection_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L217 | neighbors=[detection.py, get_results()]
- "routers_detection_runs_latest_run_delta": "latest_run_delta()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L73 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_runs_list_detection_runs": "list_detection_runs()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L56 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L322 | neighbors=[detection.py, _run_correlation()]
- "routers_engagements_bulk_import_assets": "bulk_import_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L529 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_create_engagement": "create_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L350 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_get_engagement_scope": "get_engagement_scope()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L640 | neighbors=[engagements.py, Probe-facing: the probe calls this inde…]
- "routers_engagements_re_detect": "re_detect()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L122 | neighbors=[engagements.py, Re-runs the detection pipeline against …]
- "routers_engagements_update_engagement": "update_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L495 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_exploits_approve_exploit": "approve_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L245 | neighbors=[exploits.py, _get_approval_or_404()]
- "routers_exploits_get_result_or_404": "_get_result_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L396 | neighbors=[exploits.py, get_exploit_result()]
- "routers_exploits_list_approvals": "list_approvals()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L218 | neighbors=[exploits.py, _approval_out()]
- "routers_exploits_list_exploit_results": "list_exploit_results()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L177 | neighbors=[exploits.py, _result_out()]
- "routers_exploits_load_finding_and_eng": "_load_finding_and_eng()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L369 | neighbors=[exploits.py, run_exploit()]
- "routers_exploits_reject_exploit": "reject_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L303 | neighbors=[exploits.py, _get_approval_or_404()]
- "routers_exploits_run_approved_exploit": "_run_approved_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L446 | neighbors=[exploits.py, Background task: run the exploit after …]
- "routers_exploits_run_exploit": "run_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L111 | neighbors=[exploits.py, _load_finding_and_eng()]
- "routers_findings_sla_summary": "sla_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L24 | neighbors=[findings.py, Compute SLA state across the tenant's t…]
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L264 | neighbors=[vuln_scans.py, Background task: run nuclei, persist fi…]
- "scan_page_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L115 | neighbors=[page.tsx, getToken()]
- "scan_page_gettoken": "getToken()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L110 | neighbors=[page.tsx, apiFetch()]
- "scanner_banner_grabbanner": "GrabBanner()" | kind=code-symbol | source=probe-go/scanner/banner.go:L24 | neighbors=[banner.go, guessService()]
- "scanner_banner_guessservice": "guessService()" | kind=code-symbol | source=probe-go/scanner/banner.go:L72 | neighbors=[banner.go, GrabBanner()]
- "scanner_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L237 | neighbors=[DBScanner, ._scan_port()]
- "scanner_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L271 | neighbors=[DBScanner, ._scan_port()]
- "scanner_discover_discoverhosts": "DiscoverHosts()" | kind=code-symbol | source=probe-go/scanner/discover.go:L17 | neighbors=[discover.go, probeAlive()]
- "scanner_discover_findstr": "findStr()" | kind=code-symbol | source=probe-go/scanner/discover.go:L83 | neighbors=[discover.go, containsStr()]
- "scanner_discover_intstr": "intStr()" | kind=code-symbol | source=probe-go/scanner/discover.go:L92 | neighbors=[discover.go, probeAlive()]
- "scanner_fingerprint_expandbackrefs": "expandBackrefs()" | kind=code-symbol | source=probe-go/scanner/fingerprint.go:L233 | neighbors=[fingerprint.go, Fingerprint()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-051.json

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
