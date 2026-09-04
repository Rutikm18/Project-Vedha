# Node Description Batch 283 of 330

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

- "tests_test_ipmi_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L77 | neighbors=[TestParity] | lang=en
- "tests_test_ipmi_scanner_testwireformat_test_open_session_request_offers_cipher_zero": ".test_open_session_request_offers_cipher_zero()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L24 | neighbors=[TestWireFormat] | lang=en
- "tests_test_ipmi_scanner_testwireformat_test_parse_rejects_non_response": ".test_parse_rejects_non_response()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L39 | neighbors=[TestWireFormat] | lang=en
- "tests_test_ipv6_discovery_rationale_1": "test_ipv6_discovery.py — FIX 3: IPv6 neighbor discovery (RFC 4861 ND multicast)." | kind=entity | source=probe/tests/test_ipv6_discovery.py:L1 | neighbors=[test_ipv6_discovery.py] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_ignores_non_ipv6_lines": ".test_ignores_non_ipv6_lines()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L33 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_parse_ip_neigh_linux": ".test_parse_ip_neigh_linux()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L24 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_parse_ndp_macos": ".test_parse_ndp_macos()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L14 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_wiring_rationale_1": "test_ipv6_wiring.py — IPv6 neighbour discovery inside the engagement.  An IPv4 /" | kind=entity | source=probe/tests/test_ipv6_wiring.py:L1 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_rationale_111": "The core restraint: discovery must not widen authorization." | kind=entity | source=probe/tests/test_ipv6_wiring.py:L111 | neighbors=[test_out_of_scope_neighbour_is_reported…] | lang=en
- "tests_test_ipv6_wiring_rationale_137": "Only the scan types that opt in pay for the multicast ping." | kind=entity | source=probe/tests/test_ipv6_wiring.py:L137 | neighbors=[test_disabled_by_default()] | lang=en
- "tests_test_ipv6_wiring_rationale_28": "The neighbour cache is system-wide. Pinging en0 and then harvesting every     in" | kind=entity | source=probe/tests/test_ipv6_wiring.py:L28 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_test_component_is_in_the_catalog": "test_component_is_in_the_catalog()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L160 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_test_network_va_opts_in": "test_network_va_opts_in()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L172 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_test_planned_only_when_enabled": "test_planned_only_when_enabled()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L164 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_stub": "._stub()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L42 | neighbors=[TestInterfaceScoping] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-282.json

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
