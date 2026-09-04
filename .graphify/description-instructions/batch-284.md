# Node Description Batch 285 of 332

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

- "tests_test_ipv6_wiring_testinterfacescoping_test_globals_are_kept_they_are_not_interface_bound": ".test_globals_are_kept_they_are_not_interface_bound()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L56 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_iface_filters_out_other_segments": ".test_iface_filters_out_other_segments()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L47 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_iface_keeps_its_own_neighbours": ".test_iface_keeps_its_own_neighbours()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L52 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_link_local_keeps_its_zone_so_connect_can_route": ".test_link_local_keeps_its_zone_so_connect_can_route()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L66 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_no_iface_keeps_everything": ".test_no_iface_keeps_everything()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L62 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_unresolved_neighbours_are_never_returned": ".test_unresolved_neighbours_are_never_returned()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L59 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_job_attempt_service_test_claim_creates_immutable_attempt_with_returned_fence": "test_claim_creates_immutable_attempt_with_returned_fence()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L13 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_attempt_service_test_current_fence_renews_attempt_and_logical_job": "test_current_fence_renews_attempt_and_logical_job()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L75 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_attempt_service_test_lost_claim_does_not_create_attempt": "test_lost_claim_does_not_create_attempt()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L40 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_attempt_service_test_stale_fence_cannot_renew_attempt": "test_stale_fence_cannot_renew_attempt()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L58 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_cancel_probe_rationale_1": "Probe-side operator job control + polling-noise suppression.  Two independent be" | kind=entity | source=probe/tests/test_job_cancel_probe.py:L1 | neighbors=[test_job_cancel_probe.py] | lang=en
- "tests_test_job_cancel_probe_rationale_54": "These may be transient/refreshable, so they must NOT read as a cancel         —" | kind=entity | source=probe/tests/test_job_cancel_probe.py:L54 | neighbors=[.test_other_rejections_are_plain_failur…] | lang=pt
- "tests_test_job_cancel_probe_rationale_74": "The probe polls forever; routine transport chatter must stay out of the     term" | kind=entity | source=probe/tests/test_job_cancel_probe.py:L74 | neighbors=[TestPollingNoiseIsSuppressed] | lang=en
- "tests_test_job_cancel_probe_rationale_92": "The actual regression: one INFO line per poll, every POLL_INTERVAL." | kind=entity | source=probe/tests/test_job_cancel_probe.py:L92 | neighbors=[.test_per_request_info_lines_are_suppre…] | lang=en
- "tests_test_job_cancel_probe_rationale_97": "Quieting must not hide a genuinely unreachable manager." | kind=entity | source=probe/tests/test_job_cancel_probe.py:L97 | neighbors=[.test_transport_errors_still_surface()] | lang=pt
- "tests_test_job_cancel_probe_testheartbeatoutcomes_test_200_is_ok": ".test_200_is_ok()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L48 | neighbors=[TestHeartbeatOutcomes] | lang=en
- "tests_test_job_cancel_probe_testheartbeatoutcomes_test_409_is_reported_as_a_revoked_lease": ".test_409_is_reported_as_a_revoked_lease()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L44 | neighbors=[TestHeartbeatOutcomes] | lang=en
- "tests_test_job_cancel_probe_testheartbeatoutcomes_test_bool_heartbeat_contract_is_unchanged": ".test_bool_heartbeat_contract_is_unchanged()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L64 | neighbors=[TestHeartbeatOutcomes] | lang=en
- "tests_test_job_cancel_probe_testheartbeatoutcomes_test_network_error_is_a_plain_failure": ".test_network_error_is_a_plain_failure()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L59 | neighbors=[TestHeartbeatOutcomes] | lang=en
- "tests_test_job_cancel_probe_testheartbeatoutcomes_test_revoked_lease_is_distinct_from_failure": ".test_revoked_lease_is_distinct_from_failure()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L69 | neighbors=[TestHeartbeatOutcomes] | lang=en
- "tests_test_job_cancel_probe_transport": "transport()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L35 | neighbors=[test_job_cancel_probe.py] | lang=en
- "tests_test_job_cancel_rationale_1": "Operator job control: stop a running job, remove a queued one, and cap the queue" | kind=entity | source=manager/backend/tests/test_job_cancel.py:L1 | neighbors=[test_job_cancel.py] | lang=en
- "tests_test_job_cancel_rationale_176": "An operator stop must never be mistaken for a system fault." | kind=entity | source=manager/backend/tests/test_job_cancel.py:L176 | neighbors=[test_cancelled_is_distinct_from_failed()] | lang=en
- "tests_test_job_cancel_rationale_208": "Two queued jobs must leave room for a third — an off-by-one here         would s" | kind=entity | source=manager/backend/tests/test_job_cancel.py:L208 | neighbors=[.test_third_queued_job_is_still_accepte…] | lang=en
- "tests_test_job_cancel_rationale_225": "Pins the reason this endpoint may not reference `.email`.      If CurrentUser ev" | kind=entity | source=manager/backend/tests/test_job_cancel.py:L225 | neighbors=[test_current_user_has_no_email_field()] | lang=en
- "tests_test_job_cancel_rationale_30": "The REAL CurrentUser, not a SimpleNamespace.      A hand-rolled stand-in is what" | kind=entity | source=manager/backend/tests/test_job_cancel.py:L30 | neighbors=[_user()] | lang=en
- "tests_test_job_cancel_rationale_61": "A db.execute() result whose scalar_one_or_none() yields `value`." | kind=entity | source=manager/backend/tests/test_job_cancel.py:L61 | neighbors=[_one()] | lang=pt
- "tests_test_job_cancel_rationale_91": "Attribution must come from a field the JWT actually carries." | kind=entity | source=manager/backend/tests/test_job_cancel.py:L91 | neighbors=[test_cancel_records_who_did_it()] | lang=en
- "tests_test_job_cancel_testqueuelimit_test_limit_is_three": ".test_limit_is_three()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L183 | neighbors=[TestQueueLimit] | lang=en
- "tests_test_job_result_service_test_out_of_scope_result_is_rejected_before_database_mutation": "test_out_of_scope_result_is_rejected_before_database_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L98 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_result_scope_accepts_authorized_targets_and_control_records": "test_result_scope_accepts_authorized_targets_and_control_records()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L13 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_result_scope_fails_closed": "test_result_scope_fails_closed()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L36 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_stale_attempt_gets_terminal_receipt_without_mutation": "test_stale_attempt_gets_terminal_receipt_without_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L136 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_terminal_result_retry_is_idempotent": "test_terminal_result_retry_is_idempotent()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L51 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_loaders_rationale_1": "Tests for loader error paths in vuln_db.py and enrichment_db.py.  These are the" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L1 | neighbors=[test_loaders.py] | lang=en
- "tests_test_loaders_rationale_102": "The FileNotFoundError message should mention re-syncing, so         operators kn" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L102 | neighbors=[.test_error_message_mentions_re_sync()] | lang=en
- "tests_test_loaders_rationale_108": "The ValueError for a hash mismatch must include truncated hashes         in the" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L108 | neighbors=[.test_hash_mismatch_message_truncates_h…] | lang=en
- "tests_test_loaders_rationale_60": "A path that doesn't exist must raise FileNotFoundError with a         helpful me" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L60 | neighbors=[.test_missing_file_raises_file_not_foun…] | lang=en
- "tests_test_loaders_rationale_66": "A snapshot whose records don't match the stored content_hash must         raise" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L66 | neighbors=[.test_content_hash_mismatch_raises_valu…] | lang=en
- "tests_test_loaders_rationale_78": "Completely broken JSON must propagate as an exception — never         silently y" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L78 | neighbors=[.test_malformed_json_raises()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-284.json

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
