# Node Description Batch 304 of 380

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

- "tests_campaign_store_test_tmp_dir": "TMP_DIR" | kind=code-symbol | source=manager/frontend/tests/campaign-store.test.ts:L8 | neighbors=[campaign-store.test.ts]
- "tests_campaign_workspace_test": "campaign-workspace.test.ts" | kind=code-symbol | source=manager/frontend/tests/campaign-workspace.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…]
- "tests_conftest_pytest_configure": "pytest_configure()" | kind=code-symbol | source=probe/tests/conftest.py:L25 | neighbors=[conftest.py]
- "tests_conftest_rationale_11": "Keep the local result archive out of the checkout.      TaskRunner writes every" | kind=entity | source=probe/tests/conftest.py:L11 | neighbors=[_isolate_result_archive()]
- "tests_engagement_workspace_test": "engagement-workspace.test.ts" | kind=code-symbol | source=manager/frontend/tests/engagement-workspace.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…]
- "tests_findings_detail_layout_test_findingspage": "findingsPage" | kind=code-symbol | source=manager/frontend/tests/findings-detail-layout.test.ts:L5 | neighbors=[findings-detail-layout.test.ts]
- "tests_findings_detail_layout_test_portalfindingspage": "portalFindingsPage" | kind=code-symbol | source=manager/frontend/tests/findings-detail-layout.test.ts:L9 | neighbors=[findings-detail-layout.test.ts]
- "tests_findings_store_test_makefinding": "makeFinding()" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L25 | neighbors=[findings-store.test.ts]
- "tests_findings_store_test_tmp_dir": "TMP_DIR" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L8 | neighbors=[findings-store.test.ts]
- "tests_findings_store_test_tmp_file": "TMP_FILE" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L9 | neighbors=[findings-store.test.ts]
- "tests_fleet_workspace_test": "fleet-workspace.test.ts" | kind=code-symbol | source=manager/frontend/tests/fleet-workspace.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…]
- "tests_parsers_test_naabu_line": "NAABU_LINE" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L81 | neighbors=[parsers.test.ts]
- "tests_parsers_test_nuclei_valid": "NUCLEI_VALID" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L56 | neighbors=[parsers.test.ts]
- "tests_parsers_test_testssl_valid": "TESTSSL_VALID" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L73 | neighbors=[parsers.test.ts]
- "tests_portal_auth_gate_test": "portal-auth-gate.test.ts" | kind=code-symbol | source=manager/frontend/tests/portal-auth-gate.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…]
- "tests_report_adapt_test_u": "U()" | kind=code-symbol | source=manager/frontend/tests/report-adapt.test.ts:L18 | neighbors=[report-adapt.test.ts]
- "tests_report_adapt_test_uibase": "uiBase" | kind=code-symbol | source=manager/frontend/tests/report-adapt.test.ts:L7 | neighbors=[report-adapt.test.ts]
- "tests_report_finding_model_test_a": "a" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L150 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_bare": "bare" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L146 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_base": "base" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L17 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_dirty": "dirty" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L107 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_f": "F()" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L27 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_group": "group()" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L15 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_lowkev": "lowKev" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L47 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_now": "NOW" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L26 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_ok": "ok()" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L11 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_p0sla": "p0sla" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L59 | neighbors=[report-finding-model.test.ts]
- "tests_report_finding_model_test_r": "r" | kind=code-symbol | source=manager/frontend/tests/report-finding-model.test.ts:L117 | neighbors=[report-finding-model.test.ts]
- "tests_report_portal_adapt_test_pf": "pf()" | kind=code-symbol | source=manager/frontend/tests/report-portal-adapt.test.ts:L7 | neighbors=[report-portal-adapt.test.ts]
- "tests_reports_workspace_test": "reports-workspace.test.ts" | kind=code-symbol | source=manager/frontend/tests/reports-workspace.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…]
- "tests_settings_workspace_test": "settings-workspace.test.ts" | kind=code-symbol | source=manager/frontend/tests/settings-workspace.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…]
- "tests_shared_shell_test": "shared-shell.test.ts" | kind=code-symbol | source=manager/frontend/tests/shared-shell.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…]
- "tests_test_accuracy_gate_rationale_1": "test_accuracy_gate.py — the accuracy MERGE GATE (roadmap #4 / Tier 1.3).  `accur" | kind=entity | source=probe/tests/test_accuracy_gate.py:L1 | neighbors=[test_accuracy_gate.py]
- "tests_test_accuracy_gate_rationale_44": "CI's actual assertion: the engine still matches every labeled corpus." | kind=entity | source=probe/tests/test_accuracy_gate.py:L44 | neighbors=[.test_gate_passes_on_the_committed_corp…]
- "tests_test_accuracy_gate_rationale_58": "Without one of these the gate proves only non-drift, never accuracy." | kind=entity | source=probe/tests/test_accuracy_gate.py:L58 | neighbors=[.test_an_independently_labeled_corpus_i…]
- "tests_test_accuracy_gate_rationale_64": "Locks in the measured results: every port state agrees with nmap on         both" | kind=entity | source=probe/tests/test_accuracy_gate.py:L64 | neighbors=[.test_every_independent_corpus_scores_p…]
- "tests_test_accuracy_gate_testcli_test_cli_exits_two_on_a_corpus_error": ".test_cli_exits_two_on_a_corpus_error()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L209 | neighbors=[TestCli]
- "tests_test_accuracy_gate_testcli_test_cli_exits_zero_on_passing_corpora": ".test_cli_exits_zero_on_passing_corpora()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L206 | neighbors=[TestCli]
- "tests_test_accuracy_gate_testcli_test_cli_json_mode_is_machine_readable": ".test_cli_json_mode_is_machine_readable()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L212 | neighbors=[TestCli]
- "tests_test_accuracy_gate_testcorpusvalidation_test_malformed_json_is_a_gate_error_not_a_crash": ".test_malformed_json_is_a_gate_error_not_a_crash()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L113 | neighbors=[TestCorpusValidation]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-303.json

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
