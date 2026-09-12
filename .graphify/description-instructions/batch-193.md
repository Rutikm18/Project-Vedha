# Node Description Batch 194 of 380

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

- "workflow_host_health_hosthealthmonitor_finalize": ".finalize()" | kind=code-symbol | source=probe/workflow/host_health.py:L301 | neighbors=[HostHealthMonitor, Emit one fact per offline host, plus an…] | lang=en
- "workflow_host_health_hosthealthmonitor_init": ".__init__()" | kind=code-symbol | source=probe/workflow/host_health.py:L121 | neighbors=[HostHealthMonitor, _strike_threshold()] | lang=en
- "workflow_host_health_hosthealthmonitor_note_skipped": ".note_skipped()" | kind=code-symbol | source=probe/workflow/host_health.py:L189 | neighbors=[HostHealthMonitor, ._state()] | lang=en
- "workflow_host_health_hoststate": "_HostState" | kind=code-symbol | source=probe/workflow/host_health.py:L101 | neighbors=[host_health.py, ._state()] | lang=en
- "workflow_modes_includes_stage": "includes_stage()" | kind=code-symbol | source=probe/workflow/modes.py:L45 | neighbors=[modes.py, Return whether a bounded plan includes …] | lang=en
- "workflow_modes_resolve_stage_ceiling": "resolve_stage_ceiling()" | kind=code-symbol | source=probe/workflow/modes.py:L25 | neighbors=[modes.py, Resolve the explicit ceiling while pres…] | lang=en
- "workflow_modes_service_specific": "service_specific()" | kind=code-symbol | source=probe/workflow/modes.py:L118 | neighbors=[modes.py, EngagementMode] | lang=en
- "workflow_report_diff_assets": "diff_assets()" | kind=code-symbol | source=probe/workflow/report.py:L42 | neighbors=[report.py, re-scan mode's delta report: what chang…] | lang=en
- "workflow_router_rationale_72": "True when the port was OBSERVED speaking TLS (a completed handshake, or a     TL" | kind=entity | source=probe/workflow/router.py:L72 | neighbors=[looks_like_tls(), looks_like_ssh()] | lang=en
- "workflow_workflow_engine_finalize_trace": "_finalize_trace()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L305 | neighbors=[workflow_engine.py, run_engagement()] | lang=en
- "workflow_workflow_engine_rationale_112": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L112 | neighbors=[_gather_per_host(), _port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_145": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L145 | neighbors=[_split_cached(), _Sink] | lang=en
- "workflow_workflow_engine_rationale_147": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L147 | neighbors=[_split_cached(), _Sink] | lang=en
- "workflow_workflow_engine_rationale_270": "Hosts scanned in parallel during the deep-branch stage.      Env override: PROBE" | kind=entity | source=probe/workflow/workflow_engine.py:L270 | neighbors=[_default_host_concurrency(), _timed()] | lang=en
- "workflow_workflow_engine_rationale_80": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L80 | neighbors=[_gather_per_host(), _port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_94": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L94 | neighbors=[_scan_one(), _split_cached()] | lang=en
- "activity_route_apiactivity": "ApiActivity" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L9 | neighbors=[route.ts] | lang=en
- "activity_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L14 | neighbors=[route.ts] | lang=en
- "ad_asreproast_asreproastchecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L106 | neighbors=[ASREPRoastChecker] | lang=en
- "ad_bloodhound_bloodhoundcollector_close": ".close()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L267 | neighbors=[BloodHoundCollector] | lang=en
- "ad_bloodhound_bloodhoundcollector_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L46 | neighbors=[BloodHoundCollector] | lang=en
- "ad_ldap_enum_ldapenumerator_connection": ".connection()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L185 | neighbors=[LDAPEnumerator] | lang=en
- "ad_ldap_enum_ldapenumerator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L120 | neighbors=[LDAPEnumerator] | lang=en
- "ad_orchestrator_adassessmentrunner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L42 | neighbors=[ADAssessmentRunner] | lang=en
- "agent_agent_agentdeps": "AgentDeps" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L39 | neighbors=[agent.py] | lang=en
- "agent_agent_agentopts": "AgentOpts" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L26 | neighbors=[agent.py] | lang=en
- "agent_agent_rationale_1010": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L1010 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_1015": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L1015 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_1016": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1016 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_1020": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L1020 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_1025": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1025 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_103": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=probe/agent/agent.py:L103 | neighbors=[_job_intent()] | lang=en
- "agent_agent_rationale_104": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=probe/agent/agent.py:L104 | neighbors=[_job_intent()] | lang=en
- "agent_agent_rationale_1043": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L1043 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_1045": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L1045 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_1047": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L1047 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_1058": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1058 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_1064": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L1064 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_1068": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L1068 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_107": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L107 | neighbors=[_result_summary()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-193.json

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
