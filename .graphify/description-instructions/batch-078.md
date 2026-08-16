# Node Description Batch 79 of 209

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

- "vuln_enrichment_vulnenrichmentservice_get_kev_catalog": "._get_kev_catalog()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L249 | neighbors=[VulnEnrichmentService, .check_cisa_kev(), .get()] | lang=en
- "vuln_nessus_nessusscanner_authenticate": ".authenticate()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L72 | neighbors=[NessusScanner, Prefer API key auth (stateless, no sess…, Prefer API key auth (stateless, no sess…] | lang=en
- "vuln_nessus_nessusscanner_map_finding": ".map_finding()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L205 | neighbors=[NessusScanner, Map a raw Nessus vulnerability dict → F…, Map a raw Nessus vulnerability dict → F…] | lang=en
- "vuln_nessus_rationale_1": "NessusScanner — wraps the Tenable Nessus REST API v6.  Endpoints used:   POST /s" | kind=entity | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[nessus.py, FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_101": "Returns nessus scan_id as string." | kind=entity | source=manager/backend/app/vuln/nessus.py:L101 | neighbors=[.create_scan(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_102": "Returns nessus scan_id as string." | kind=entity | source=manager/backend/app/vuln/nessus.py:L102 | neighbors=[FindingSeverity, FindingStatus, .create_scan()] | lang=en
- "vuln_nessus_rationale_140": "Returns scan_uuid (token for tracking)." | kind=entity | source=manager/backend/app/vuln/nessus.py:L140 | neighbors=[.launch_scan(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_141": "Returns scan_uuid (token for tracking)." | kind=entity | source=manager/backend/app/vuln/nessus.py:L141 | neighbors=[FindingSeverity, FindingStatus, .launch_scan()] | lang=en
- "vuln_nessus_rationale_151": "Returns {status, progress_percent, host_count}." | kind=entity | source=manager/backend/app/vuln/nessus.py:L151 | neighbors=[.poll_status(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_152": "Returns {status, progress_percent, host_count}." | kind=entity | source=manager/backend/app/vuln/nessus.py:L152 | neighbors=[FindingSeverity, FindingStatus, .poll_status()] | lang=en
- "vuln_nessus_rationale_167": "Returns list of raw finding dicts from all hosts." | kind=entity | source=manager/backend/app/vuln/nessus.py:L167 | neighbors=[.get_results(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_168": "Returns list of raw finding dicts from all hosts." | kind=entity | source=manager/backend/app/vuln/nessus.py:L168 | neighbors=[FindingSeverity, FindingStatus, .get_results()] | lang=en
- "vuln_nessus_rationale_206": "Map a raw Nessus vulnerability dict → Finding-compatible dict.         Returns a" | kind=entity | source=manager/backend/app/vuln/nessus.py:L206 | neighbors=[.map_finding(), FindingSeverity, FindingStatus] | lang=pt
- "vuln_nessus_rationale_207": "Map a raw Nessus vulnerability dict → Finding-compatible dict.         Returns a" | kind=entity | source=manager/backend/app/vuln/nessus.py:L207 | neighbors=[FindingSeverity, FindingStatus, .map_finding()] | lang=pt
- "vuln_nessus_rationale_257": "Request + poll + download .nessus XML for evidence storage." | kind=entity | source=manager/backend/app/vuln/nessus.py:L257 | neighbors=[.export_nessus_file(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_258": "Request + poll + download .nessus XML for evidence storage." | kind=entity | source=manager/backend/app/vuln/nessus.py:L258 | neighbors=[FindingSeverity, FindingStatus, .export_nessus_file()] | lang=en
- "vuln_nessus_rationale_38": "Async Nessus API client. One instance per engagement scan session." | kind=entity | source=manager/backend/app/vuln/nessus.py:L38 | neighbors=[NessusScanner, FindingSeverity, FindingStatus] | lang=it
- "vuln_nessus_rationale_39": "Async Nessus API client. One instance per engagement scan session." | kind=entity | source=manager/backend/app/vuln/nessus.py:L39 | neighbors=[FindingSeverity, FindingStatus, NessusScanner] | lang=it
- "vuln_nessus_rationale_73": "Prefer API key auth (stateless, no session expiry).         Falls back to userna" | kind=entity | source=manager/backend/app/vuln/nessus.py:L73 | neighbors=[.authenticate(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nessus_rationale_74": "Prefer API key auth (stateless, no session expiry).         Falls back to userna" | kind=entity | source=manager/backend/app/vuln/nessus.py:L74 | neighbors=[FindingSeverity, FindingStatus, .authenticate()] | lang=en
- "vuln_nuclei_nucleiscanner_consume_stdout": "._consume_stdout()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L287 | neighbors=[NucleiScanner, ._map_finding(), .run_scan()] | lang=en
- "vuln_nuclei_nucleiscanner_map_finding": "._map_finding()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L395 | neighbors=[NucleiScanner, ._consume_stdout(), .parse_output()] | lang=en
- "vuln_nuclei_rationale_109": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L109 | neighbors=[NucleiScanner, FindingSeverity, FindingStatus] | lang=en
- "vuln_nuclei_rationale_126": "Run Nuclei and stream JSONL findings from stdout.          ``request_timeout_sec" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L126 | neighbors=[.run_scan(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nuclei_rationale_382": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L382 | neighbors=[.parse_output(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nuclei_rationale_445": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L445 | neighbors=[.template_selector(), FindingSeverity, FindingStatus] | lang=en
- "vuln_nuclei_rationale_79": "Machine-readable state for the most recent scanner invocation." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L79 | neighbors=[NucleiRunReport, FindingSeverity, FindingStatus] | lang=en
- "vuln_nuclei_rationale_90": "Fatal Nuclei failure, optionally carrying findings emitted before failure." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L90 | neighbors=[NucleiScanError, FindingSeverity, FindingStatus] | lang=en
- "vuln_tasks_dedup_hash": "_dedup_hash()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L167 | neighbors=[tasks.py, Deprecated — use app.utils.hash.dedup_h…, Deprecated — use app.utils.hash.dedup_h…] | lang=en
- "websocket_manager_agentconnectionmanager_record_features": ".record_features()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L163 | neighbors=[AgentConnectionManager, Record transport features explicitly ad…, Record transport features explicitly ad…] | lang=en
- "websocket_manager_agentconnectionmanager_record_heartbeat": ".record_heartbeat()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L151 | neighbors=[AgentConnectionManager, Record a heartbeat from an agent., Record a heartbeat from an agent.] | lang=en
- "websocket_manager_agentconnectionmanager_register": ".register()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L97 | neighbors=[AgentConnectionManager, Register an agent's WebSocket connectio…, Register an agent's WebSocket connectio…] | lang=en
- "websocket_manager_connectionmanager_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L33 | neighbors=[ConnectionManager, .handle_client(), Accept connection and add to room.] | lang=en
- "workers_outbox_dead_letter_stale_stmt": "_dead_letter_stale_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L168 | neighbors=[outbox.py, Stranded events that already exhausted …, _reclaim_stale()] | lang=en
- "workers_outbox_is_stale_processing": "is_stale_processing()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L42 | neighbors=[outbox.py, Return whether a claimed event was stra…, Return whether a claimed event was stra…] | lang=en
- "workers_outbox_rationale_1": "outbox.py (worker) — durable consumer for the transactional outbox.  Run as its" | kind=entity | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[outbox.py, OutboxEvent, ScanResult] | lang=en
- "workers_outbox_rationale_110": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L110 | neighbors=[OutboxEvent, ScanResult, _claim_batch()] | lang=en
- "workers_outbox_rationale_152": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L152 | neighbors=[OutboxEvent, ScanResult, _mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_56": "Decorator: bind an async handler to a topic." | kind=entity | source=manager/backend/app/workers/outbox.py:L56 | neighbors=[OutboxEvent, ScanResult, register()] | lang=en
- "workers_outbox_rationale_67": "Add an outbox event to the caller's session. Does NOT commit — it commits     at" | kind=entity | source=manager/backend/app/workers/outbox.py:L67 | neighbors=[OutboxEvent, ScanResult, enqueue()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-078.json

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
