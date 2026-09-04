# Node Description Batch 145 of 330

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

- "services_job_result_service_rationale_30": "Recursively strip NUL (U+0000) from every string in a result payload.      Defen" | kind=entity | source=manager/backend/app/services/job_result_service.py:L30 | neighbors=[sanitize_jsonb(), result_checksum()]
- "services_notifications_enqueue_notification": "enqueue_notification()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L101 | neighbors=[notifications.py, Producer API: enqueue a durable notify …]
- "services_portal_metrics_period": "_period()" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L50 | neighbors=[portal_metrics.py, status_timeline()]
- "services_posture_findingview": "FindingView" | kind=code-symbol | source=manager/backend/app/services/posture.py:L22 | neighbors=[posture.py, Duck-typed projection of a Finding + it…]
- "services_posture_grade_for": "grade_for()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L55 | neighbors=[posture.py, compute_scores()]
- "services_posture_risk_prob": "_risk_prob()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L62 | neighbors=[posture.py, compute_scores()]
- "services_posture_scores": "Scores" | kind=code-symbol | source=manager/backend/app/services/posture.py:L36 | neighbors=[posture.py, compute_scores()]
- "services_posture_severity": "_severity()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L116 | neighbors=[posture.py, compare()]
- "services_project_time_resolve_project_tz": "_resolve_project_tz()" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L41 | neighbors=[project_time.py, The project timezone, degrading safely …]
- "services_project_time_to_project_tz": "to_project_tz()" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L70 | neighbors=[project_time.py, Re-render an existing datetime in the p…]
- "services_reference_encode": "_encode()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L64 | neighbors=[reference.py, suffix_for()]
- "services_reference_scan_job_reference": "scan_job_reference()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L96 | neighbors=[reference.py, make_reference()]
- "services_remediation_kb_cves": "_cves()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L54 | neighbors=[remediation_kb.py, classify_finding()]
- "services_remediation_kb_step": "_step()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L94 | neighbors=[remediation_kb.py, One remediation step. `generic` is REQU…]
- "services_remediation_kb_text": "_text()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L45 | neighbors=[remediation_kb.py, classify_finding()]
- "services_risk_rank_bounded": "_bounded()" | kind=code-symbol | source=manager/backend/app/services/risk_rank.py:L35 | neighbors=[risk_rank.py, compute_risk_rank()]
- "services_risk_rank_compute_risk_rank": "compute_risk_rank()" | kind=code-symbol | source=manager/backend/app/services/risk_rank.py:L39 | neighbors=[risk_rank.py, _bounded()]
- "services_scope_crypto_public_key_from_b64": "public_key_from_b64()" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L85 | neighbors=[scope_crypto.py, Decode a base64-encoded X25519 public k…]
- "services_scope_targets_parse_networks": "_parse_networks()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L28 | neighbors=[scope_targets.py, validate_targets_in_scope()]
- "settings_page_apikeyssection": "ApiKeysSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L287 | neighbors=[page.tsx, inlineInput()]
- "settings_page_auditlogsection": "AuditLogSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L795 | neighbors=[page.tsx, inlineInput()]
- "settings_page_integrationsection": "IntegrationSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L570 | neighbors=[page.tsx, inlineInput()]
- "status_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L15 | neighbors=[route.ts, readiness()]
- "status_route_readiness": "readiness()" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L10 | neighbors=[route.ts, GET()]
- "supporting_research_evidence_store_coverage_summary": "coverage_summary()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L362 | neighbors=[evidence_store.py, What a customer should actually be show…]
- "supporting_research_evidence_store_naive_ip_identity": "naive_ip_identity()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L257 | neighbors=[evidence_store.py, The industry default, for comparison. I…]
- "supporting_research_evidence_store_record_observation": "record_observation()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L113 | neighbors=[evidence_store.py, _iso()]
- "supporting_research_test_evidence_store_smb_obs": "smb_obs()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L45 | neighbors=[test_evidence_store.py, build_fleet()]
- "supporting_research_test_evidence_store_testidentity_setup": ".setUp()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L96 | neighbors=[TestIdentity, build_fleet()]
- "supporting_research_test_evidence_store_testidentity_test_hostname_never_overrides_a_fingerprint": ".test_hostname_never_overrides_a_fingerprint()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L119 | neighbors=[TestIdentity, ssh_obs()]
- "supporting_research_test_evidence_store_testidentity_test_ip_identity_is_wrong_in_both_directions": ".test_ip_identity_is_wrong_in_both_directions()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L104 | neighbors=[Not merely coarse -- wrong. It splits o…, TestIdentity]
- "supporting_research_test_evidence_store_testretroactivedetection_setup": ".setUp()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L141 | neighbors=[TestRetroactiveDetection, build_fleet()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_collected_but_unusable_evidence_is_distinguished_from_absent": ".test_collected_but_unusable_evidence_is_distinguished_from_absent()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L194 | neighbors=[Drifted payload: the probe ran, the fie…, TestRetroactiveDetection]
- "supporting_research_test_evidence_store_testretroactivedetection_test_remediation_is_verified_by_evidence_not_by_a_ticket": ".test_remediation_is_verified_by_evidence_not_by_a_ticket()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L162 | neighbors=[TestRetroactiveDetection, openssh_below()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_third_party_conclusions_are_kept_separate_from_first_party_evidence": ".test_third_party_conclusions_are_kept_separate_from_first_party_evidence()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L206 | neighbors=[TestRetroactiveDetection, ssh_obs()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_time_travel_recovers_the_historical_answer": ".test_time_travel_recovers_the_historical_answer()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L151 | neighbors=[TestRetroactiveDetection, openssh_below()]
- "tests_conftest_isolate_result_archive": "_isolate_result_archive()" | kind=code-symbol | source=probe/tests/conftest.py:L10 | neighbors=[conftest.py, Keep the local result archive out of th…]
- "tests_init": "__init__.py" | kind=code-symbol | source=manager/backend/tests/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_accuracy_gate_testcorpusvalidation_test_corpus_without_any_labels_is_rejected": ".test_corpus_without_any_labels_is_rejected()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L101 | neighbors=[TestCorpusValidation, _write()]
- "tests_test_accuracy_gate_testcorpusvalidation_test_corpus_without_facts_is_rejected": ".test_corpus_without_facts_is_rejected()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L107 | neighbors=[TestCorpusValidation, _write()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-144.json

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
