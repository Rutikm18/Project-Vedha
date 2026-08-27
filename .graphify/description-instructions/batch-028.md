# Node Description Batch 29 of 236

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

- "main_scripts_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L199 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()] | lang=en
- "main_scripts_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L237 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()] | lang=en
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L298 | neighbors=[OSFingerprintScanner, accept_echo_reply(), build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…] | lang=en
- "main_scripts_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()] | lang=en
- "main_scripts_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L256 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._scan_port()] | lang=en
- "main_scripts_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L324 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…, One connect() and its classification. A…] | lang=en
- "main_scripts_run_all": "run_all.py" | kind=code-symbol | source=probe/main_scripts/run_all.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _log(), main(), _open_tcp_ports(), _ports_arg(), _read_jsonl()] | lang=en
- "main_scripts_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L109 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()] | lang=en
- "main_scripts_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L725 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…] | lang=en
- "main_scripts_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L695 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()] | lang=en
- "main_scripts_service_enum_serviceenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L529 | neighbors=[ServiceEnumScanner, classify_roles(), Enrichment, guess_os(), resolve_hostnames(), ._probe_port()] | lang=en
- "main_scripts_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L200 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…] | lang=en
- "main_scripts_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L261 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…] | lang=en
- "me_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, backend(), withBackend(), GET, 298a9d4 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "models_user": "user.py" | kind=code-symbol | source=manager/backend/app/models/user.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 65f22a7 Add comprehensive tests for aut…, c4386e4 feat(customers): operator Custo…, d1b4dd3 trim frontend to 7 core pages; …, e3958e7 feat(customers): reveal + copy …, User] | lang=en
- "models_user_user": "User" | kind=code-symbol | source=manager/backend/app/models/user.py:L13 | neighbors=[user.py, Base, TimestampMixin, Base, TimestampMixin, UserRole] | lang=en
- "native_tls_info": "tls-info.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, nativeTlsInfo(), TlsInfoResult, WEAK_PROTOCOLS, WEAK_SIGNATURES, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "portscan": "portscan.py" | kind=code-symbol | source=portscan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, classify_os_error(), family_of(), main(), parse_ports(), PortScanner] | lang=en
- "portscan_portscanner": "PortScanner" | kind=code-symbol | source=portscan.py:L112 | neighbors=[portscan.py, main(), ._attempt(), .__init__(), ._record(), .run()] | lang=en
- "probes_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, backend(), withBackend(), GET, 0557559 scanner: real use-case library,…, backend.ts] | lang=en
- "routers_activity": "activity.py" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, dependencies.py, ActivityItem, recent_activity(), Recent activity feed.  A tenant-wide, r…] | lang=en
- "routers_agent_advisor": "agent_advisor.py" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dependencies.py, list_recommendations(), _rec_dict(), run_advisor(), agent_advisor.py — API for the agentic …] | lang=en
- "routers_agents_enqueue_agent_job": "enqueue_agent_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1087 | neighbors=[agents.py, _agent_can_execute_job(), _encrypt_scope_for_agent(), _job_params_contain_secret(), _job_reachability_scope(), _normalize_intensity_name()] | lang=en
- "routers_agents_normalize_intensity_name": "_normalize_intensity_name()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L275 | neighbors=[agents.py, enqueue_agent_job(), ._validate_intensity(), Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…] | lang=en
- "routers_agents_rationale_103": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L103 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=pt
- "routers_agents_rationale_139": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L139 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_207": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L207 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_387": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L387 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_425": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L425 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_444": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L444 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_706": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L706 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_90": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L90 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_analytics_exposureanalytics": "ExposureAnalytics" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L40 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding] | lang=en
- "routers_analytics_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L30 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding] | lang=en
- "routers_analytics_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L35 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding] | lang=en
- "routers_findings_rationale_25": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L25 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_findings_rationale_26": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L26 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_findings_rationale_48": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L48 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_findings_rationale_49": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L49 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L26 | neighbors=[findings.py, get_finding(), patch_finding(), Fetch a finding scoped to the caller's …, reopen_finding(), Fetch a finding scoped to the caller's …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-028.json

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
