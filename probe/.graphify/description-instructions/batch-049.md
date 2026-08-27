# Node Description Batch 50 of 92

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

- "tests_test_tls_posture_testgradetlsposture_test_grade_f_tls10": ".test_grade_f_tls10()" | kind=code-symbol | source=tests/test_tls_posture.py:L94 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_transport_transport": "transport()" | kind=code-symbol | source=tests/test_transport.py:L17 | neighbors=[test_transport.py, Create a Transport with a real state fi…]
- "tests_test_wire_identity_testevasionflags": "TestEvasionFlags" | kind=code-symbol | source=tests/test_wire_identity.py:L73 | neighbors=[test_wire_identity.py, .test_randomize_and_scan_delay_flags_pr…]
- "tests_test_workflow_execution_test_host_fanout_is_bounded": "test_host_fanout_is_bounded()" | kind=code-symbol | source=tests/test_workflow_execution.py:L76 | neighbors=[test_workflow_execution.py, _ConcurrencyScanner]
- "tests_test_workflow_execution_test_per_target_exception_preserves_other_results": "test_per_target_exception_preserves_other_results()" | kind=code-symbol | source=tests/test_workflow_execution.py:L61 | neighbors=[test_workflow_execution.py, _ExplodingScanner]
- "tools_issue_license_b64": "_b64()" | kind=code-symbol | source=tools/issue_license.py:L31 | neighbors=[issue_license.py, issue()]
- "tools_issue_license_keygen": "keygen()" | kind=code-symbol | source=tools/issue_license.py:L35 | neighbors=[issue_license.py, main()]
- "workflow_asset_utcnow": "_utcnow()" | kind=code-symbol | source=workflow/asset.py:L27 | neighbors=[asset.py, .needs_recheck_live()]
- "workflow_cache_cacheentry_from_jsonl_dict": ".from_jsonl_dict()" | kind=code-symbol | source=workflow/cache.py:L71 | neighbors=[CacheEntry, ._load()]
- "workflow_cache_cacheentry_to_jsonl_dict": ".to_jsonl_dict()" | kind=code-symbol | source=workflow/cache.py:L65 | neighbors=[CacheEntry, .save()]
- "workflow_cache_workflowcache_init": ".__init__()" | kind=code-symbol | source=workflow/cache.py:L83 | neighbors=[WorkflowCache, ._load()]
- "workflow_cache_workflowcache_save": ".save()" | kind=code-symbol | source=workflow/cache.py:L101 | neighbors=[WorkflowCache, .to_jsonl_dict()]
- "workflow_cli_build_creds": "_build_creds()" | kind=code-symbol | source=workflow/cli.py:L83 | neighbors=[cli.py, _main()]
- "workflow_cli_build_mode": "_build_mode()" | kind=code-symbol | source=workflow/cli.py:L71 | neighbors=[cli.py, _main()]
- "workflow_cli_build_parser": "build_parser()" | kind=code-symbol | source=workflow/cli.py:L43 | neighbors=[cli.py, _main()]
- "workflow_cli_parse_duration": "_parse_duration()" | kind=code-symbol | source=workflow/cli.py:L28 | neighbors=[cli.py, 7d' / '12h' / '30m' -> timedelta. Simpl…]
- "workflow_execution_engine_manifest": "engine_manifest()" | kind=code-symbol | source=workflow/execution.py:L58 | neighbors=[execution.py, Return the runtime engine inventory wit…]
- "workflow_execution_errordetail": "ErrorDetail" | kind=code-symbol | source=workflow/execution.py:L147 | neighbors=[execution.py, classify_scanner_error()]
- "workflow_execution_executiontrace_as_list": ".as_list()" | kind=code-symbol | source=workflow/execution.py:L364 | neighbors=[ExecutionTrace, ._has_active_coverage()]
- "workflow_execution_executiontrace_finalize": ".finalize()" | kind=code-symbol | source=workflow/execution.py:L333 | neighbors=[ExecutionTrace, .skip()]
- "workflow_execution_executiontrace_init": ".__init__()" | kind=code-symbol | source=workflow/execution.py:L234 | neighbors=[ExecutionTrace, ._ensure()]
- "workflow_execution_executiontrace_reused": ".reused()" | kind=code-symbol | source=workflow/execution.py:L319 | neighbors=[ExecutionTrace, .record()]
- "workflow_execution_planned_components": "planned_components()" | kind=code-symbol | source=workflow/execution.py:L96 | neighbors=[execution.py, Resolve the exact collector plan for on…]
- "workflow_gates_gate_2_host_discovery": "gate_2_host_discovery()" | kind=code-symbol | source=workflow/gates.py:L70 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_gates_gate_3_port_scan": "gate_3_port_scan()" | kind=code-symbol | source=workflow/gates.py:L77 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_init": "__init__.py" | kind=code-symbol | source=workflow/__init__.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, workflow — conditional, caching, depend…]
- "workflow_modes_includes_stage": "includes_stage()" | kind=code-symbol | source=workflow/modes.py:L45 | neighbors=[modes.py, Return whether a bounded plan includes …]
- "workflow_modes_resolve_stage_ceiling": "resolve_stage_ceiling()" | kind=code-symbol | source=workflow/modes.py:L25 | neighbors=[modes.py, Resolve the explicit ceiling while pres…]
- "workflow_modes_service_specific": "service_specific()" | kind=code-symbol | source=workflow/modes.py:L118 | neighbors=[modes.py, EngagementMode]
- "workflow_report_diff_assets": "diff_assets()" | kind=code-symbol | source=workflow/report.py:L42 | neighbors=[report.py, re-scan mode's delta report: what chang…]
- "workflow_workflow_engine_finalize_trace": "_finalize_trace()" | kind=code-symbol | source=workflow/workflow_engine.py:L264 | neighbors=[workflow_engine.py, run_engagement()]
- "workflow_workflow_engine_record": "_record()" | kind=code-symbol | source=workflow/workflow_engine.py:L238 | neighbors=[workflow_engine.py, run_engagement()]
- "workflow_workflow_engine_record_reused": "_record_reused()" | kind=code-symbol | source=workflow/workflow_engine.py:L255 | neighbors=[workflow_engine.py, run_engagement()]
- "workflow_workflow_engine_store_results": "_store_results()" | kind=code-symbol | source=workflow/workflow_engine.py:L223 | neighbors=[workflow_engine.py, run_engagement()]
- "agent_cli_configstore_init": ".__init__()" | kind=code-symbol | source=agent/cli.py:L56 | neighbors=[ConfigStore]
- "agent_cli_rationale_574": "Run a bounded capability suite and optionally score known ground truth." | kind=entity | source=agent/cli.py:L574 | neighbors=[cmd_validate()]
- "agent_device_identity_encode_key": "encode_key()" | kind=code-symbol | source=agent/device_identity.py:L26 | neighbors=[device_identity.py]
- "agent_device_identity_generate_signing_identity": "generate_signing_identity()" | kind=code-symbol | source=agent/device_identity.py:L12 | neighbors=[device_identity.py]
- "agent_device_identity_rationale_38": "Verify a Manager-signed policy and return its public key for TOFU pinning." | kind=entity | source=agent/device_identity.py:L38 | neighbors=[verify_site_policy()]
- "agent_device_identity_sign_b64": "sign_b64()" | kind=code-symbol | source=agent/device_identity.py:L21 | neighbors=[device_identity.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-049.json

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
