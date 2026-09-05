# Node Description Batch 92 of 336

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

- "auth_exceptions_usernotfounderror": "UserNotFoundError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L33 | neighbors=[exceptions.py, No user record for the supplied email., AuthenticationError]
- "auth_jwt_create_access_token": "create_access_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L27 | neighbors=[jwt.py, _now(), create_device_access_token()]
- "auth_jwt_now": "_now()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L23 | neighbors=[jwt.py, create_access_token(), create_refresh_token()]
- "auth_middleware_portal_jwt_path_allows": "portal_jwt_path_allows()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L37 | neighbors=[middleware.py, Routes a customer-portal token (aud=ved…, .dispatch()]
- "auth_router_login": "login()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L153 | neighbors=[router.py, access_claims_for(), _authenticate()]
- "auth_router_refresh": "refresh()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L247 | neighbors=[router.py, create_personal_access_token(), access_claims_for()]
- "auth_startup_check_cookie_config": "_check_cookie_config()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L228 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_cors": "_check_cors()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L243 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_database": "_check_database()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L96 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_jwt_secret": "_check_jwt_secret()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L128 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_redis": "_check_redis()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L115 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_required_env_vars": "_check_required_env_vars()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L257 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "brain_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L48 | neighbors=[route.ts, validMessages(), assistant.test.ts]
- "cli_auth_clearsession": "clearSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L29 | neighbors=[auth.ts, interactive.ts, logout.ts]
- "cli_auth_savesession": "saveSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L24 | neighbors=[auth.ts, interactive.ts, login.ts]
- "cli_llm_streamask": "streamAsk()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L340 | neighbors=[llm.ts, client(), ask.ts]
- "commands_doctor_render": "render()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L41 | neighbors=[doctor.ts, ln(), symbol()]
- "commands_interactive_fetchengagements": "fetchEngagements()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1746 | neighbors=[interactive.ts, pickEngagementId(), wizardEngagement()]
- "commands_interactive_inferhostsfromfindings": "inferHostsFromFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1418 | neighbors=[interactive.ts, pickTargets(), wizardScan()]
- "commands_interactive_mergehosts": "mergeHosts()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1165 | neighbors=[interactive.ts, runPhasePortScan(), runPhaseServiceDetect()]
- "commands_interactive_printhostdiscoverydiagnostic": "printHostDiscoveryDiagnostic()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L917 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_printhostsummary": "printHostSummary()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L905 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_printstatesummary": "printStateSummary()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L895 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_runphaseenumeration": "runPhaseEnumeration()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1044 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()]
- "commands_interactive_runphasehostdiscovery": "runPhaseHostDiscovery()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1023 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, f5ce592 first commit]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2c38782317674ba6a0323a1ea1539a68587a356d": "2c38782 docs: spec CVE-breadth phase — snapshot must answer for every recognize…" | kind=Commit | source=git | neighbors=[main, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…]
- "components_dashboardcharts_dashboardcharts": "DashboardCharts()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L180 | neighbors=[page.tsx, DashboardCharts.tsx, page.tsx]
- "cve_cli_cmd_correlate": "cmd_correlate()" | kind=code-symbol | source=probe/cve/cli.py:L81 | neighbors=[cli.py, _merge_findings(), _read_facts()]
- "cve_cli_merge_findings": "_merge_findings()" | kind=code-symbol | source=probe/cve/cli.py:L65 | neighbors=[cli.py, cmd_correlate(), Merge CVE-finding lists, dedup by (cve_…]
- "cve_cli_read_facts": "_read_facts()" | kind=code-symbol | source=probe/cve/cli.py:L26 | neighbors=[cli.py, cmd_correlate(), Yield fact dicts from a JSONL file ('-'…]
- "cve_correlator_backport_marker": "_backport_marker()" | kind=code-symbol | source=probe/cve/correlator.py:L57 | neighbors=[correlator.py, correlate(), Return the distro-backport token found …]
- "cve_correlator_cvefinding": "CVEFinding" | kind=code-symbol | source=probe/cve/correlator.py:L84 | neighbors=[correlator.py, correlate(), .to_dict()]
- "cve_correlator_risk_score": "risk_score()" | kind=code-symbol | source=probe/cve/correlator.py:L63 | neighbors=[correlator.py, correlate(), 0–100 prioritization score. CVSS is hal…]
- "cve_ingest_cvss": "_cvss()" | kind=code-symbol | source=probe/cve/ingest.py:L88 | neighbors=[ingest.py, ingest_one_cve(), Best available CVSS: prefer v3.1 > v3.0…]
- "cve_ingest_ingest_epss": "ingest_epss()" | kind=code-symbol | source=probe/cve/ingest.py:L211 | neighbors=[ingest.py, ingest_all(), _get()]
- "cve_ingest_ingest_kev": "ingest_kev()" | kind=code-symbol | source=probe/cve/ingest.py:L193 | neighbors=[ingest.py, ingest_all(), _get()]
- "cve_ingest_parse_criteria": "_parse_criteria()" | kind=code-symbol | source=probe/cve/ingest.py:L109 | neighbors=[ingest.py, ingest_one_cve(), cpe:2.3:a:vendor:product:version:... ->…]
- "cve_online_lookup_vulners": "lookup_vulners()" | kind=code-symbol | source=probe/cve/online.py:L90 | neighbors=[online.py, enrich_findings(), Ask Vulners whether a public exploit is…]
- "cve_online_onlineresult": "OnlineResult" | kind=code-symbol | source=probe/cve/online.py:L51 | neighbors=[online.py, lookup_nvd(), What a live lookup could establish for …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-091.json

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
