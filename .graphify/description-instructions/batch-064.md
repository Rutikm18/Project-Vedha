# Node Description Batch 65 of 236

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

- "vuln_nuclei_nucleiscanner_template_selector": ".template_selector()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L444 | neighbors=[NucleiScanner, Given a list of service names on an ass…, Given a list of service names on an ass…, Given a list of service names on an ass…]
- "vuln_nuclei_rationale_1": "NucleiScanner — async subprocess wrapper around the Nuclei CLI.  Nuclei outputs" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[nuclei.py, FindingSeverity, FindingStatus, ServiceFingerprint]
- "vuln_nuclei_rationale_110": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L110 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_127": "Run Nuclei and stream JSONL findings from stdout.          ``request_timeout_sec" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L127 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_132": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L132 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_195": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L195 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_383": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L383 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_446": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L446 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_68": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L68 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_80": "Machine-readable state for the most recent scanner invocation." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L80 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiRunReport]
- "vuln_nuclei_rationale_81": "Runs nuclei as an async subprocess.         Returns a list of parsed finding dic" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L81 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_91": "Fatal Nuclei failure, optionally carrying findings emitted before failure." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L91 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanError]
- "vuln_tasks_run_post_scan_enrichment": "run_post_scan_enrichment()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L34 | neighbors=[tasks.py, Triggered by the vuln scan API after a …, _fire_critical_webhook(), Triggered by the vuln scan API after a …]
- "websocket_manager_agentconnectionmanager_run_backplane": ".run_backplane()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L260 | neighbors=[AgentConnectionManager, .is_connected(), .push_job(), Subscribe to the push backplane and for…]
- "workers_outbox_enqueue": "enqueue()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L86 | neighbors=[outbox.py, Add an outbox event to the caller's ses…, Add an outbox event to the caller's ses…, Add an outbox event to the caller's ses…]
- "workers_outbox_handle_facts_ready": "_handle_facts_ready()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L103 | neighbors=[outbox.py, Run the deterministic detection pipelin…, Run the deterministic detection pipelin…, Run the deterministic detection pipelin…]
- "workers_outbox_process": "_process()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L281 | neighbors=[outbox.py, _mark_done(), _mark_retry_or_dead(), run_worker()]
- "workers_outbox_rationale_186": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L186 | neighbors=[_requeue_stale_stmt(), OutboxEvent, ScanResult, run_worker()]
- "workers_outbox_register": "register()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L76 | neighbors=[outbox.py, Decorator: bind an async handler to a t…, Decorator: bind an async handler to a t…, Decorator: bind an async handler to a t…]
- "workers_reaper_run_reaper": "run_reaper()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L87 | neighbors=[reaper.py, Poll loop: requeue expired jobs every r…, reap_once(), Poll loop: requeue expired jobs every r…]
- "workflow_asset_parse_ts": "_parse_ts()" | kind=code-symbol | source=probe/workflow/asset.py:L31 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_asset_portfact": "PortFact" | kind=code-symbol | source=probe/workflow/asset.py:L36 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_cache_cacheentry": "CacheEntry" | kind=code-symbol | source=probe/workflow/cache.py:L55 | neighbors=[cache.py, .from_jsonl_dict(), .to_jsonl_dict(), .put()]
- "workflow_cache_workflowcache_should_recheck": ".should_recheck()" | kind=code-symbol | source=probe/workflow/cache.py:L120 | neighbors=[True if there's no cached entry, OR the…, WorkflowCache, .get(), True if there's no cached entry, OR the…]
- "workflow_cli_main": "_main()" | kind=code-symbol | source=probe/workflow/cli.py:L95 | neighbors=[cli.py, _build_creds(), _build_mode(), build_parser()]
- "workflow_execution_classify_scanner_error": "classify_scanner_error()" | kind=code-symbol | source=probe/workflow/execution.py:L153 | neighbors=[execution.py, ErrorDetail, Map low-level failures into stable, ope…, scanner_failure_result()]
- "workflow_execution_executiontrace_ensure": "._ensure()" | kind=code-symbol | source=probe/workflow/execution.py:L239 | neighbors=[ExecutionTrace, .__init__(), .record(), .skip()]
- "workflow_gates_gate_5_branch_eligible": "gate_5_branch_eligible()" | kind=code-symbol | source=probe/workflow/gates.py:L87 | neighbors=[gates.py, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …]
- "workflow_modes_assessment": "assessment()" | kind=code-symbol | source=probe/workflow/modes.py:L111 | neighbors=[modes.py, EngagementMode, Full funnel, every branch the profile a…, Full funnel, every branch the profile a…]
- "workflow_modes_re_scan": "re_scan()" | kind=code-symbol | source=probe/workflow/modes.py:L126 | neighbors=[modes.py, Loads a prior engagement's cache; only …, EngagementMode, Loads a prior engagement's cache; only …]
- "workflow_modes_triage": "triage()" | kind=code-symbol | source=probe/workflow/modes.py:L104 | neighbors=[modes.py, Discovery + ports + banner only — no de…, EngagementMode, Discovery + ports + banner only — no de…]
- "workflow_router_looks_like_db": "looks_like_db()" | kind=code-symbol | source=probe/workflow/router.py:L62 | neighbors=[router.py, looks_like_http(), True when a service banner carries a da…, route_branches()]
- "workflow_router_looks_like_tls": "looks_like_tls()" | kind=code-symbol | source=probe/workflow/router.py:L50 | neighbors=[router.py, True when this port's banner result is …, route_branches(), True when this port's banner result is …]
- "ad_adcs_adcschecker_check_esc4": ".check_esc4()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L147 | neighbors=[ADCSChecker, .generate_findings(), ESC4: a low-privilege principal holds a…]
- "ad_adcs_adcschecker_check_esc8": ".check_esc8()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L160 | neighbors=[ADCSChecker, .generate_findings(), ESC8: the CA exposes a web-enrollment (…]
- "ad_adcs_adcschecker_enrollment_principals": "._enrollment_principals()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L116 | neighbors=[ADCSChecker, .enumerate_templates(), Principals with an enrollment ExtendedR…]
- "ad_asreproast_asreproastchecker_format_asrep_hash": "._format_asrep_hash()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L90 | neighbors=[ASREPRoastChecker, .request_asrep(), Render an AS-REP as a hashcat $krb5asre…]
- "ad_asreproast_asreproastchecker_request_asrep": ".request_asrep()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L54 | neighbors=[ASREPRoastChecker, ._format_asrep_hash(), Request an AS-REP for ``username`` with…]
- "ad_asreproast_rationale_1": "ASREPRoastChecker — find accounts with Kerberos pre-authentication disabled and" | kind=entity | source=manager/backend/app/ad/asreproast.py:L1 | neighbors=[asreproast.py, LDAPEnumerator, FindingSeverity]
- "ad_asreproast_rationale_35": "Enumerate AS-REP roastable accounts and capture AS-REP evidence." | kind=entity | source=manager/backend/app/ad/asreproast.py:L35 | neighbors=[ASREPRoastChecker, LDAPEnumerator, FindingSeverity]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-064.json

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
