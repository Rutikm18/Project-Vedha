# Node Description Batch 36 of 92

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

- "tests_test_syn_scanner_testsyndefaults": "TestSynDefaults" | kind=code-symbol | source=tests/test_syn_scanner.py:L287 | neighbors=[test_syn_scanner.py, .test_default_ports_are_nmap_top100(), .test_default_retries_is_two()]
- "tests_test_tarpit_testportscannertarpitflag_scanner": "._scanner()" | kind=code-symbol | source=tests/test_tarpit.py:L43 | neighbors=[TestPortScannerTarpitFlag, .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tarpit_testportscannertarpitflag_summary": "._summary()" | kind=code-symbol | source=tests/test_tarpit.py:L48 | neighbors=[TestPortScannerTarpitFlag, .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tarpit_testportscannertarpitflag_test_all_open_host_flagged_as_tarpit": ".test_all_open_host_flagged_as_tarpit()" | kind=code-symbol | source=tests/test_tarpit.py:L51 | neighbors=[TestPortScannerTarpitFlag, ._scanner(), ._summary()]
- "tests_test_tarpit_testportscannertarpitflag_test_mostly_closed_host_not_flagged": ".test_mostly_closed_host_not_flagged()" | kind=code-symbol | source=tests/test_tarpit.py:L63 | neighbors=[TestPortScannerTarpitFlag, ._scanner(), ._summary()]
- "tests_test_task_runner_testrunnerscantypes": "TestRunnerScanTypes" | kind=code-symbol | source=tests/test_task_runner.py:L447 | neighbors=[test_task_runner.py, .test_ot_passive_profile(), .test_web_triage_scan_type()]
- "tests_test_task_runner_testrunnersubmission": "TestRunnerSubmission" | kind=code-symbol | source=tests/test_task_runner.py:L389 | neighbors=[test_task_runner.py, .test_calls_submit_with_result(), .test_uses_spool_when_available()]
- "tests_test_tls_fingerprint_synthetic_server_hello": "_synthetic_server_hello()" | kind=code-symbol | source=tests/test_tls_fingerprint.py:L45 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_integration_self_signed": "_self_signed()" | kind=code-symbol | source=tests/test_tls_integration.py:L29 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_integration_test_tls_fingerprint_is_nonzero_and_stable": "test_tls_fingerprint_is_nonzero_and_stable()" | kind=code-symbol | source=tests/test_tls_integration.py:L111 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_tls_integration_test_tls_scanner_reports_posture_grade": "test_tls_scanner_reports_posture_grade()" | kind=code-symbol | source=tests/test_tls_integration.py:L87 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_transport_testfetchscope": "TestFetchScope" | kind=code-symbol | source=tests/test_transport.py:L405 | neighbors=[test_transport.py, .test_http_error_returns_none(), .test_returns_scope()]
- "tests_test_wire_identity_testprobepayload": "TestProbePayload" | kind=code-symbol | source=tests/test_wire_identity.py:L28 | neighbors=[test_wire_identity.py, .test_default_carries_no_brand(), .test_env_override()]
- "tests_test_wire_identity_testuseragent": "TestUserAgent" | kind=code-symbol | source=tests/test_wire_identity.py:L17 | neighbors=[test_wire_identity.py, .test_default_is_generic_browser_no_bra…, .test_env_override()]
- "tests_test_workflow_execution_explodingscanner": "_ExplodingScanner" | kind=code-symbol | source=tests/test_workflow_execution.py:L29 | neighbors=[test_workflow_execution.py, .scan_target(), test_per_target_exception_preserves_oth…]
- "tools_issue_license_issue": "issue()" | kind=code-symbol | source=tools/issue_license.py:L62 | neighbors=[issue_license.py, _b64(), main()]
- "tools_issue_license_pubkey": "pubkey()" | kind=code-symbol | source=tools/issue_license.py:L48 | neighbors=[issue_license.py, main(), Print the vendor PUBLIC key (hex) deriv…]
- "tools_probe_local_run": "probe_local_run.py" | kind=code-symbol | source=tools/probe_local_run.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a1430fb Add local_run.py for direct pro…, local_run.py]
- "workflow_asset_asset_merge_host_discovery": "._merge_host_discovery()" | kind=code-symbol | source=workflow/asset.py:L111 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_asset_asset_merge_port_scan": "._merge_port_scan()" | kind=code-symbol | source=workflow/asset.py:L121 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_asset_asset_merge_udp_scan": "._merge_udp_scan()" | kind=code-symbol | source=workflow/asset.py:L207 | neighbors=[Asset, _parse_ts(), PortFact]
- "workflow_cache_classify_certainty": "classify_certainty()" | kind=code-symbol | source=workflow/cache.py:L46 | neighbors=[cache.py, .get(), .put()]
- "workflow_cache_workflowcache_get": ".get()" | kind=code-symbol | source=workflow/cache.py:L109 | neighbors=[classify_certainty(), WorkflowCache, .should_recheck()]
- "workflow_cache_workflowcache_load": "._load()" | kind=code-symbol | source=workflow/cache.py:L89 | neighbors=[WorkflowCache, .__init__(), .from_jsonl_dict()]
- "workflow_cache_workflowcache_put": ".put()" | kind=code-symbol | source=workflow/cache.py:L112 | neighbors=[WorkflowCache, CacheEntry, classify_certainty()]
- "workflow_cache_workflowcache_should_recheck": ".should_recheck()" | kind=code-symbol | source=workflow/cache.py:L120 | neighbors=[True if there's no cached entry, OR the…, WorkflowCache, .get()]
- "workflow_execution_executiontrace_failed": ".failed()" | kind=code-symbol | source=workflow/execution.py:L350 | neighbors=[ExecutionTrace, ._has_active_coverage(), True when execution produced errors and…]
- "workflow_execution_executiontrace_has_active_coverage": "._has_active_coverage()" | kind=code-symbol | source=workflow/execution.py:L360 | neighbors=[ExecutionTrace, .as_list(), .failed()]
- "workflow_execution_executiontrace_record": ".record()" | kind=code-symbol | source=workflow/execution.py:L259 | neighbors=[ExecutionTrace, ._ensure(), .reused()]
- "workflow_execution_executiontrace_skip": ".skip()" | kind=code-symbol | source=workflow/execution.py:L328 | neighbors=[ExecutionTrace, .finalize(), ._ensure()]
- "workflow_execution_scanner_failure_result": "scanner_failure_result()" | kind=code-symbol | source=workflow/execution.py:L209 | neighbors=[execution.py, Represent an unexpected component excep…, classify_scanner_error()]
- "workflow_intensity_intensity_port_override": "intensity_port_override()" | kind=code-symbol | source=workflow/intensity.py:L79 | neighbors=[intensity.py, resolve_intensity(), Concrete TCP port list for this intensi…]
- "workflow_intensity_resolve_intensity": "resolve_intensity()" | kind=code-symbol | source=workflow/intensity.py:L64 | neighbors=[intensity.py, intensity_port_override(), Return a COPY of the preset for `name` …]
- "workflow_modes_assessment": "assessment()" | kind=code-symbol | source=workflow/modes.py:L111 | neighbors=[modes.py, EngagementMode, Full funnel, every branch the profile a…]
- "workflow_modes_discovery": "discovery()" | kind=code-symbol | source=workflow/modes.py:L60 | neighbors=[modes.py, EngagementMode, Host discovery plus the profile's TCP p…]
- "workflow_modes_host_discovery": "host_discovery()" | kind=code-symbol | source=workflow/modes.py:L71 | neighbors=[modes.py, EngagementMode, Liveness checks only.]
- "workflow_modes_port_scan": "port_scan()" | kind=code-symbol | source=workflow/modes.py:L82 | neighbors=[modes.py, EngagementMode, Liveness checks plus the profile's TCP …]
- "workflow_modes_re_scan": "re_scan()" | kind=code-symbol | source=workflow/modes.py:L126 | neighbors=[modes.py, Loads a prior engagement's cache; only …, EngagementMode]
- "workflow_modes_service_fingerprint": "service_fingerprint()" | kind=code-symbol | source=workflow/modes.py:L93 | neighbors=[modes.py, Liveness, TCP ports, and service banner…, EngagementMode]
- "workflow_modes_triage": "triage()" | kind=code-symbol | source=workflow/modes.py:L104 | neighbors=[modes.py, Discovery + ports + banner only — no de…, EngagementMode]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-035.json

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
