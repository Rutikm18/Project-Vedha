# Node Description Batch 66 of 330

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

- "tests_test_vnc_scanner_testvncfindings": "TestVNCFindings" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L52 | neighbors=[test_vnc_scanner.py, ._fact(), .test_no_auth_is_critical(), .test_strong_auth_silent(), .test_weak_only_is_medium()]
- "tests_test_web_methods": "test_web_methods.py" | kind=code-symbol | source=probe/tests/test_web_methods.py:L1 | neighbors=[bce780a feat(probe): enumerate HTTP met…, web_scanner.py, test_dangerous_methods_flagged(), test_no_allow_header(), test_safe_methods_only()]
- "tests_test_wire_identity_testjittereddelay": "TestJitteredDelay" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L57 | neighbors=[test_wire_identity.py, Evasion: blur a fixed scan cadence with…, .test_never_negative_even_at_full_jitte…, .test_stays_within_jitter_band(), .test_zero_or_negative_base_is_zero()]
- "tools_installer_getinstalledrecord": "getInstalledRecord()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L63 | neighbors=[installer.ts, readInstalled(), installAll(), installTool(), tools.ts]
- "tools_installer_ismanaged": "isManaged()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L56 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), managedPath()]
- "tools_installer_readinstalled": "readInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L33 | neighbors=[installer.ts, getInstalledRecord(), installTool(), listStatus(), removeTool()]
- "tools_installer_removetool": "removeTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L243 | neighbors=[tools.ts, installer.ts, managedPath(), readInstalled(), writeInstalled()]
- "ui_output_rule": "rule()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L50 | neighbors=[output.ts, findingDetail(), ln(), scanHeader(), summary()]
- "versions_0002_services_agents": "0002_services_agents.py" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add services and agents tables  Revisio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0003_vuln_scan_fields": "0003_vuln_scan_fields.py" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add enrichment fields index + webhook c…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0004_exploit_tables": "0004_exploit_tables.py" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Exploit results, approvals, and audit l…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0005_detection_validation": "0005_detection_validation.py" | kind=code-symbol | source=manager/backend/alembic/versions/0005_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Detection validation: attack_timeline, …, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0006_llm_outputs": "0006_llm_outputs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), AI engine: llm_outputs table + reviewst…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0007_scale_indexes": "0007_scale_indexes.py" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3: composite indexes for the hot aggre…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0008_scan_results": "0008_scan_results.py" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3-#10: append-only scan_results table …, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0009_outbox_events": "0009_outbox_events.py" | kind=code-symbol | source=manager/backend/alembic/versions/0009_outbox_events.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Transactional outbox for durable backgr…, 2885afa Add comprehensive probe testing…]
- "versions_0010_detection_runs": "0010_detection_runs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Temporal detection: detection_runs tabl…, 2885afa Add comprehensive probe testing…]
- "versions_0011_job_lease": "0011_job_lease.py" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Job leasing: scan_jobs.lease_expires_at…, 2885afa Add comprehensive probe testing…]
- "versions_0012_agent_recommendations": "0012_agent_recommendations.py" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Agentic AI advisor: agent_recommendatio…, 2885afa Add comprehensive probe testing…]
- "versions_0013_agent_public_key": "0013_agent_public_key.py" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Add agents.public_key (Phase-4 X25519 i…, 2885afa Add comprehensive probe testing…]
- "versions_0024_device_role_inventory": "0024_device_role_inventory.py" | kind=code-symbol | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, downgrade(), upgrade(), Device-role inventory: persist the prob…, # NOTE: Postgres cannot DROP a single e…]
- "versions_0035_engagement_lifecycle_states": "0035_engagement_lifecycle_states.py" | kind=code-symbol | source=manager/backend/alembic/versions/0035_engagement_lifecycle_states.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, downgrade(), upgrade(), engagement lifecycle: add 'ongoing' and…]
- "vuln_enrichment_vulnenrichmentservice_enrich": ".enrich()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L105 | neighbors=[Add NVD CVSS, EPSS, KEV flag, MITRE tec…, VulnEnrichmentService, .get(), .compute_composite_risk(), ._fetch_all()]
- "vuln_enrichment_vulnenrichmentservice_fetch_mitre_techniques": ".fetch_mitre_techniques()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L270 | neighbors=[Returns MITRE ATT&CK technique IDs link…, VulnEnrichmentService, ._fetch_all(), .get(), .fetch_nvd()]
- "vuln_enrichment_vulnenrichmentservice_fetch_nvd": ".fetch_nvd()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L163 | neighbors=[Returns {cvss_v3, cvss_vector, descript…, VulnEnrichmentService, ._fetch_all(), .fetch_mitre_techniques(), .get()]
- "vuln_nessus_nessusscanner_create_scan": ".create_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L94 | neighbors=[NessusScanner, ._get_client(), ._get_template_uuid(), Returns nessus scan_id as string., Returns nessus scan_id as string.]
- "vuln_nessus_nessusscanner_get_results": ".get_results()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L166 | neighbors=[NessusScanner, ._get_client(), ._get_plugin_detail(), Returns list of raw finding dicts from …, Returns list of raw finding dicts from …]
- "websocket_manager_agentconnectionmanager_run_backplane": ".run_backplane()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L262 | neighbors=[AgentConnectionManager, .is_connected(), .push_job(), Subscribe to the push backplane and for…, Subscribe to the push backplane and for…]
- "workers_outbox_enqueue": "enqueue()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L98 | neighbors=[outbox.py, Add an outbox event to the caller's ses…, Add an outbox event to the caller's ses…, Add an outbox event to the caller's ses…, Add an outbox event to the caller's ses…]
- "workers_outbox_handle_facts_ready": "_handle_facts_ready()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L115 | neighbors=[outbox.py, Run the deterministic detection pipelin…, Run the deterministic detection pipelin…, Run the deterministic detection pipelin…, Run the deterministic detection pipelin…]
- "workers_outbox_register": "register()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L88 | neighbors=[outbox.py, Decorator: bind an async handler to a t…, Decorator: bind an async handler to a t…, Decorator: bind an async handler to a t…, Decorator: bind an async handler to a t…]
- "workers_reaper_reap_once": "reap_once()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L56 | neighbors=[reaper.py, Expire current attempts and requeue onl…, expire_attempt(), run_reaper(), Requeue every running job whose lease h…]
- "workflow_cache_workflowcache_should_recheck": ".should_recheck()" | kind=code-symbol | source=probe/workflow/cache.py:L141 | neighbors=[True if there's no cached entry, OR the…, WorkflowCache, .get(), True if there's no cached entry, OR the…, True if there's no cached entry, OR the…]
- "workflow_execution_classify_scanner_error": "classify_scanner_error()" | kind=code-symbol | source=probe/workflow/execution.py:L165 | neighbors=[execution.py, ErrorDetail, Map low-level failures into stable, ope…, scanner_failure_result(), Map low-level failures into stable, ope…]
- "workflow_execution_executiontrace_ensure": "._ensure()" | kind=code-symbol | source=probe/workflow/execution.py:L251 | neighbors=[ExecutionTrace, .__init__(), .record(), .skip(), .timing()]
- "workflow_gates_gate_5_branch_eligible": "gate_5_branch_eligible()" | kind=code-symbol | source=probe/workflow/gates.py:L133 | neighbors=[gates.py, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …]
- "workflow_host_health_hosthealthmonitor_confirm": ".confirm()" | kind=code-symbol | source=probe/workflow/host_health.py:L194 | neighbors=[HostHealthMonitor, ._mark_offline(), ._state(), .suspect(), Re-probe a suspected host and record th…]
- "workflow_router_looks_like_db": "looks_like_db()" | kind=code-symbol | source=probe/workflow/router.py:L101 | neighbors=[router.py, looks_like_http(), True when a service banner carries a da…, route_branches(), True when a service banner carries a da…]
- "workflow_router_looks_like_tls": "looks_like_tls()" | kind=code-symbol | source=probe/workflow/router.py:L71 | neighbors=[router.py, True when the port was OBSERVED speakin…, route_branches(), True when this port's banner result is …, True when this port's banner result is …]
- "ad_adcs_adcschecker_check_esc1": ".check_esc1()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L132 | neighbors=[ADCSChecker, ._has_low_priv(), .generate_findings(), ESC1: enrollee supplies subject + clien…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-065.json

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
