# Node Description Batch 8 of 380

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@c5e2d0ed7a2fe2e171616a98cebb2295cf557314": "c5e2d0e chore: retire probe-go to spike/probe-go branch" | kind=Commit | source=git | neighbors=[1fe16c8 stable but some dead code, need…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@caf1e5d0a9e53f79a5c9e541a083b332aa127fdd": "caf1e5d feat(verification): deterministic passive verdict core" | kind=Commit | source=git | neighbors=[0fbec7d feat(verification): add finding…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@cbf5d6cb96915e7c031de705eb116568a081940b": "cbf5d6c feat(resolution): pure decision core (coverage + confirm window + db gu…" | kind=Commit | source=git | neighbors=[9a36729 feat(resolution): coverage buil…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@de2d1c9825984fa315f761df4bb2da6139d7ff36": "de2d1c9 feat(verification): optional fail-closed LLM rationale + FP-triage" | kind=Commit | source=git | neighbors=[caf1e5d feat(verification): determinist…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=nl
- "commit:repo:github.com/Rutikm18/Project-Vedha@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@fadb4f53f6fecb205c9da67b084b4f8ad43ea578": "fadb4f5 fix(posture): hoist report-section test import; flush before section co…" | kind=Commit | source=git | neighbors=[0f0097b feat(posture): mirror posture s…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[neo4j_client.py, .available(), .close(), .connect(), .ensure_schema(), .__init__()] | lang=en
- "lib_assistant": "assistant.ts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L1 | neighbors=[page.tsx, AdvisorFlow.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, 1fe16c8 stable but some dead code, need…] | lang=en
- "main_scripts_findings_data": "_data()" | kind=code-symbol | source=probe/main_scripts/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()] | lang=en
- "reportsection_findingreport": "FindingReport.tsx" | kind=code-symbol | source=reportsection/FindingReport.tsx:L1 | neighbors=[ef14810 Implement instance locking mech…, Severity, SEVERITY_ORDER, assess(), AssessedFinding, provenanceOf()] | lang=en
- "scanner_findings_data": "_data()" | kind=code-symbol | source=probe/scanner/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()] | lang=en
- "scanner_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…] | lang=en
- "scanner_va_campaign": "va_campaign.py" | kind=code-symbol | source=probe/scanner/va_campaign.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _alive(), _atomic_write_json(), _bounded_gather()] | lang=en
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 6cf7e16 Expose report enrichment on Fin…, 72f68af feat(verification): expose veri…] | lang=en
- "tests_report_finding_model_test": "report-finding-model.test.ts" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 315cf9c feat(frontend): refine reports …, 3618365 Vendor finding-model + port its…, 76240ac UI UX Update, finding-model.ts, assess()] | lang=en
- "tests_test_agents": "test_agents.py" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 9c54022 Refactor code structure and rem…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L795 | neighbors=[test_detection_core.py, .test_cvss_critical(), .test_cvss_high(), .test_cvss_low(), .test_cvss_medium(), .test_elevated_epss_high()] | lang=en
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=probe/tests/test_result_spool.py:L18 | neighbors=[test_result_spool.py, .test_byte_high_water_mark_pauses_new_w…, .test_custom_retry_config(), .test_exists(), .test_file_high_water_mark_pauses_new_w…, .test_flush_quarantines_permanent_rejec…] | lang=en
- "tests_test_service_posture_rules_fire": "_fire()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L50 | neighbors=[test_service_posture_rules.py, _fact(), test_rule_fires_on_captured_shape(), test_smb_null_session_fires_when_permit…, test_smb_null_session_is_silent_on_the_…, test_ssh_rules_against_live_capture()] | lang=en
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L108 | neighbors=[nuclei.py, ._consume_stdout(), .__init__(), ._map_finding(), .parse_output(), ._partial_or_raise()] | lang=en
- "workflow_asset": "asset.py" | kind=code-symbol | source=probe/workflow/asset.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3ad95f4 feat: Optimize asset service fe…, 3c9062a refactor: Update dashboard comp…, 64e8290 feat(campaign): implement VA ca…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …] | lang=en
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()] | lang=en
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=probe/agent/engine.py:L588 | neighbors=[engine.py, Execute a scan and return the enriched …, _build_run_stats(), _derive_post_stage(), _error_result(), _facts_from_cache()] | lang=en
- "ai_llm_report_llmreportgenerator": "LLMReportGenerator" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L83 | neighbors=[llm_report.py, .available(), ._complete(), ._generate_and_store(), .generate_detection_rule_explanation(), .generate_executive_summary()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@027f4e4a2d8ac673df4346462728ac22849b0cf0": "027f4e4 feat(integrations): per-tenant email/Slack/Jira config store + CRUD (it…" | kind=Commit | source=git | neighbors=[main.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@08e0594c53bb049b1860e796d7c8315f1a5afd7e": "08e0594 deployement ready" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@25c014d75e19e4bf82d8f4033426ad02425be6f8": "25c014d feat: enhance campaign progress tracking and add raw facts inspection- …" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2a36f8a328c12c4fd1f8d9d7a61f80bddc044304": "2a36f8a fix: update docker compose commands to use .env file for environment va…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@315cf9c740d58ce76a8411d236ebfeedadfdf0dd": "315cf9c feat(frontend): refine reports and findings evidence" | kind=Commit | source=git | neighbors=[page.tsx, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3ad95f45b1a7fcabc284bdb92a99e96a7ed33d57": "3ad95f4 feat: Optimize asset service fetching and enhance password handling- Re…" | kind=Commit | source=git | neighbors=[agent.py, router.py, startup.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@54503ae3d26d1926e1232f1dc9803e8cfd20faec": "54503ae feat(scanner): SYN path harvests OS-fingerprint intel + RTT-adaptive ti…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b6acb87b50e17f444fd6433cdaaf57cca5c2918": "6b6acb8 fix: update AWS compose command and set default MANAGER_PUBLIC_URL in d…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@879cdfa25f56102c23df1efdc671934f88d1b793": "879cdfa docs: probe fleet automation design spec (Phase 0 detailed)" | kind=Commit | source=git | neighbors=[41b692a Update project files, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent, feat/complete-pending-work] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9347a9a16f87a98cc882c39ad050f50544b65e0b": "9347a9a feat(posture): surface posture scorecard + patch matrix on dashboard" | kind=Commit | source=git | neighbors=[page.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0791783d160c85c688ea511dc20396a7ac4e2e2": "a079178 fix(posture): full-width posture section; avoid blank grid column on de…" | kind=Commit | source=git | neighbors=[9347a9a feat(posture): surface posture …, page.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@aa560a0292202728647e1f6cde4e0ca942782cd6": "aa560a0 feat(posture): add dashboard PostureScorecard component" | kind=Commit | source=git | neighbors=[2cddd52 fix(posture): tenant-scope run …, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@ca41cbf25bddbb70f2808dcfbb236405c24bfc69": "ca41cbf docs: pre-auth probe enrollment token design spec" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d2eb44c3d2c1f5ac6a3398dc1bf865c46447a9a8": "d2eb44c feat(posture): add dashboard PatchComparisonMatrix component" | kind=Commit | source=git | neighbors=[aa560a0 feat(posture): add dashboard Po…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d7329cfe261cfa5fd29d0892344b94340cbe0b77": "d7329cf feat: enhance AWS deployment with new environment variables and scripts…" | kind=Commit | source=git | neighbors=[b5ffcb0 Refactor Vedha probe installer …, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-007.json

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
