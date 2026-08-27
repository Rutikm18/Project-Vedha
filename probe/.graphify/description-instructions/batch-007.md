# Node Description Batch 8 of 92

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

- "agent_agent_rationale_1025": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=agent/agent.py:L1025 | neighbors=[_load_or_create_signing_identity(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_1058": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=agent/agent.py:L1058 | neighbors=[_enroll_device(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_107": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=agent/agent.py:L107 | neighbors=[_result_summary(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_1231": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=agent/agent.py:L1231 | neighbors=[_obtain_identity(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_131": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=agent/agent.py:L131 | neighbors=[_classify_connection_error(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_157": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=agent/agent.py:L157 | neighbors=[_manager_reachable(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_172": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=agent/agent.py:L172 | neighbors=[_wait_for_manager(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_199": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=agent/agent.py:L199 | neighbors=[_poll_jobs_or_empty(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_48": "Return an integer environment setting constrained to a safe range." | kind=entity | source=agent/agent.py:L48 | neighbors=[_bounded_env_int(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_508": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=agent/agent.py:L508 | neighbors=[_run_polled_job_with_heartbeats(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_557": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=agent/agent.py:L557 | neighbors=[_run_ws_push_loop(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_57": "Recognize only explicit single-host development/Compose manager names." | kind=entity | source=agent/agent.py:L57 | neighbors=[_is_local_manager_url(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_65": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=agent/agent.py:L65 | neighbors=[_load_env(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_692": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=agent/agent.py:L692 | neighbors=[_ws_stage_job_offer(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_710": "Release a staged job only after the manager confirms its claim." | kind=entity | source=agent/agent.py:L710 | neighbors=[_ws_take_confirmed_job(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_744": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=agent/agent.py:L744 | neighbors=[_ws_run_job(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_814": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=agent/agent.py:L814 | neighbors=[_ws_http_poll_fallback(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_851": "Send periodic heartbeats over WebSocket." | kind=entity | source=agent/agent.py:L851 | neighbors=[_ws_heartbeat_sender(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_868": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=agent/agent.py:L868 | neighbors=[_flush_spool_over_http(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_881": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=agent/agent.py:L881 | neighbors=[_startup_gauntlet(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=pt
- "agent_agent_rationale_928": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=agent/agent.py:L928 | neighbors=[_check_anti_debug(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_93": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=agent/agent.py:L93 | neighbors=[_job_intent(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_rationale_976": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=agent/agent.py:L976 | neighbors=[_load_or_create_identity(), HWBindError, LicenseError, ResultSpool, TaskRunner, DeviceAlreadyEnrolledError] | lang=en
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=agent/agent.py:L733 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), _dbg(), _job_intent()] | lang=en
- "agent_device_identity": "device_identity.py" | kind=code-symbol | source=agent/device_identity.py:L1 | neighbors=[decode_key(), encode_key(), generate_signing_identity(), sign_b64(), signing_public_from_private(), verify_site_policy()] | lang=en
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=agent/result_spool.py:L95 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_bytes()] | lang=en
- "agent_transport_transport_ensure_device_access": ".ensure_device_access()" | kind=code-symbol | source=agent/transport.py:L438 | neighbors=[Refresh a device token before expiry; l…, Transport, .connect_ws(), .load_state(), .refresh_device_access(), .heartbeat()] | lang=en
- "main_scripts_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=main_scripts/iot_scanner.py:L445 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), BaseScanner, ResultWriter, ScanResult] | lang=en
- "main_scripts_mobile_scanner_mobilescanner": "MobileScanner" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L278 | neighbors=[mobile_scanner.py, BaseScanner, .scan_target(), BaseScanner, ResultWriter, ScanResult] | lang=en
- "main_scripts_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=main_scripts/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), ResultWriter, ScanResult] | lang=en
- "main_scripts_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=main_scripts/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), .__init__(), ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L191 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…] | lang=en
- "main_scripts_service_banner": "service_banner.py" | kind=code-symbol | source=main_scripts/service_banner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _dec(), main(), match_service(), ServiceBannerScanner] | lang=en
- "main_scripts_service_enum_serviceenumscanner": "ServiceEnumScanner" | kind=code-symbol | source=main_scripts/service_enum.py:L449 | neighbors=[service_enum.py, BaseScanner, BaseScanner, ScanResult, .__init__(), ._open()] | lang=en
- "main_scripts_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=main_scripts/smb_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, main(), _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()] | lang=en
- "main_scripts_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=main_scripts/ssh_collector.py:L80 | neighbors=[ssh_collector.py, RateLimiter, ResultWriter, ScanResult, ScopeGuard, ._collect()] | lang=en
- "main_scripts_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L312 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()] | lang=en
- "main_scripts_web_scanner": "web_scanner.py" | kind=code-symbol | source=main_scripts/web_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _fetch(), main(), _NoRedirect, parse_allow_header()] | lang=en
- "scanner_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=scanner/scan_funnel.py:L191 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-007.json

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
