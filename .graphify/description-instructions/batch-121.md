# Node Description Batch 122 of 380

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

- "services_portal_metrics_status_timeline": "status_timeline()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L54 | neighbors=[portal_metrics.py, Per-month {period, opened, closed} for …, _period()] | lang=en
- "services_posture_clamp01": "_clamp01()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L43 | neighbors=[posture.py, aggregate(), _exploit_prob()] | lang=en
- "services_posture_exploit_prob": "_exploit_prob()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L67 | neighbors=[posture.py, compute_scores(), _clamp01()] | lang=en
- "services_posture_to_utc": "_to_utc()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L98 | neighbors=[posture.py, build_posture(), _present_in_run()] | lang=en
- "services_project_time_project_file_stamp": "project_file_stamp()" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L84 | neighbors=[project_time.py, project_now(), Compact project-local stamp for FILE an…] | lang=en
- "services_project_time_project_timestamp": "project_timestamp()" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L65 | neighbors=[project_time.py, project_now(), ISO-8601 instant in the project timezon…] | lang=en
- "services_reference_is_reference": "is_reference()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L111 | neighbors=[reference.py, normalize(), True when `text` looks like one of our …] | lang=en
- "services_reference_normalize": "normalize()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L101 | neighbors=[reference.py, is_reference(), Canonicalise a reference a human typed:…] | lang=en
- "services_remediation_kb_os_key": "os_key()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L26 | neighbors=[remediation_kb.py, Normalize an arbitrary OS/target string…, recipe_for_finding()] | lang=en
- "services_scheduler_advance": "advance()" | kind=code-symbol | source=manager/backend/app/services/scheduler.py:L33 | neighbors=[scheduler.py, Mark a schedule run and set its next du…, run_due()] | lang=en
- "services_scheduler_due_schedules": "due_schedules()" | kind=code-symbol | source=manager/backend/app/services/scheduler.py:L24 | neighbors=[scheduler.py, Schedules that should fire at `now`: en…, run_due()] | lang=en
- "services_scope_crypto_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L34 | neighbors=[scope_crypto.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…] | lang=en
- "services_scope_crypto_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L77 | neighbors=[scope_crypto.py, encrypt_scope(), Convenience: dict → JSON → encrypt → ba…] | lang=en
- "services_scope_targets_expand_requested": "_expand_requested()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L37 | neighbors=[scope_targets.py, Expand raw target tokens (IP / CIDR / `…, validate_targets_in_scope()] | lang=en
- "services_sla_default_windows": "default_windows()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L108 | neighbors=[sla.py, _windows(), The env-configured SLA windows — the fa…] | lang=en
- "services_sla_rationale_1": "SLA policy engine.  Turns a severity + \"first seen\" timestamp into a remediation" | kind=entity | source=manager/backend/app/services/sla.py:L1 | neighbors=[sla.py, FindingStatus, Finding] | lang=pt
- "services_sla_rationale_101": "Aggregate SLA states across a set of findings.      Returns counts per state plu" | kind=entity | source=manager/backend/app/services/sla.py:L101 | neighbors=[summarize(), FindingStatus, Finding] | lang=en
- "services_sla_rationale_61": "Compute the SLA state for one finding. Never raises on missing data." | kind=entity | source=manager/backend/app/services/sla.py:L61 | neighbors=[compute(), FindingStatus, Finding] | lang=en
- "services_sla_windows": "_windows()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L34 | neighbors=[sla.py, compute(), default_windows()] | lang=en
- "services_validation_ingest_apply_validation_outcome": "apply_validation_outcome()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L32 | neighbors=[validation_ingest.py, ingest_validation_result(), Apply a validation verdict to a finding…] | lang=en
- "services_validation_ingest_looks_like_validation_result": "looks_like_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L44 | neighbors=[validation_ingest.py, ingest_validation_result(), Cheap gate so normal scan submissions n…] | lang=en
- "services_verification_kb": "verification_kb.py" | kind=code-symbol | source=manager/backend/app/services/verification_kb.py:L1 | neighbors=[c6420a6 Add deterministic verification …, verification_for_finding(), verification_kb.py — deterministic rete…] | lang=en
- "supporting_research_evidence_store_assetverdict": "AssetVerdict" | kind=code-symbol | source=Supporting_research/evidence_store.py:L287 | neighbors=[evidence_store.py, retroactive_detect(), time_travel()] | lang=en
- "supporting_research_evidence_store_exposure_timeline": "exposure_timeline()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L388 | neighbors=[evidence_store.py, get_path(), (observed_at, answer) transitions -- th…] | lang=en
- "supporting_research_evidence_store_get_path": "get_path()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L99 | neighbors=[evidence_store.py, exposure_timeline(), _identity_keys()] | lang=en
- "supporting_research_evidence_store_identity_keys": "_identity_keys()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L163 | neighbors=[evidence_store.py, get_path(), resolve_identity()] | lang=en
- "supporting_research_evidence_store_iso": "_iso()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L85 | neighbors=[evidence_store.py, record_observation(), retroactive_detect()] | lang=en
- "supporting_research_evidence_store_unionfind_find": ".find()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L150 | neighbors=[resolve_identity(), _UnionFind, .union()] | lang=en
- "supporting_research_evidence_store_unionfind_union": ".union()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L157 | neighbors=[resolve_identity(), _UnionFind, .find()] | lang=en
- "supporting_research_test_evidence_store_demo": "demo()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L222 | neighbors=[test_evidence_store.py, build_fleet(), openssh_below()] | lang=en
- "supporting_research_test_evidence_store_testretroactivedetection_test_a_brand_new_rule_answers_against_stored_evidence": ".test_a_brand_new_rule_answers_against_stored_evidence()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L145 | neighbors=[No rescan. The whole point., TestRetroactiveDetection, openssh_below()] | lang=en
- "supporting_research_test_evidence_store_testretroactivedetection_test_current_state_comes_from_latest_evidence_not_a_union_over_history": ".test_current_state_comes_from_latest_evidence_not_a_union_over_history()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L168 | neighbors=[Regression guard. An OR over history me…, TestRetroactiveDetection, openssh_below()] | lang=en
- "tests_scanner_workspace_test": "scanner-workspace.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-workspace.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, scan-launch.ts, buildScanLaunchRequest()] | lang=en
- "tests_test_accuracy_gate_testcorpusvalidation_test_ground_truth_states_alone_is_a_valid_corpus": ".test_ground_truth_states_alone_is_a_valid_corpus()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L122 | neighbors=[TestCorpusValidation, _port_fact(), _write()] | lang=en
- "tests_test_accuracy_gate_testprovenance_test_gate_counts_the_two_kinds_separately": ".test_gate_counts_the_two_kinds_separately()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L136 | neighbors=[TestProvenance, _port_fact(), _write()] | lang=en
- "tests_test_accuracy_gate_testshippedcorpora_test_regression_only_directory_still_warns": ".test_regression_only_directory_still_warns()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L81 | neighbors=[TestShippedCorpora, _port_fact(), _write()] | lang=en
- "tests_test_accuracy_gate_testthresholds_test_matching_port_state_scores_perfectly": ".test_matching_port_state_scores_perfectly()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L197 | neighbors=[TestThresholds, _port_fact(), _write()] | lang=en
- "tests_test_accuracy_gate_testthresholds_test_thresholds_are_overridable": ".test_thresholds_are_overridable()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L186 | neighbors=[TestThresholds, _port_fact(), _write()] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_computers_flags_dc": ".test_get_computers_flags_dc()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L132 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_groups_marks_privileged": ".test_get_groups_marks_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L150 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-121.json

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
