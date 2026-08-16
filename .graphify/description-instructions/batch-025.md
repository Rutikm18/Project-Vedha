# Node Description Batch 26 of 209

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

- "exploit_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, 2885afa Add comprehensive probe testing…] | lang=en
- "graph_builder_graphbuilder_add_exploit_edges": ".add_exploit_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L183 | neighbors=[GraphBuilder, asset_node_id(), exploit_complexity(), finding_node_id(), _to_float(), .build_asset_graph()] | lang=en
- "graph_demo": "demo.py" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-p…] | lang=en
- "graph_demo_demoasset": "DemoAsset" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L27 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "graph_demo_demofinding": "DemoFinding" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L45 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "lib_findings_store_savefindings": "saveFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L51 | neighbors=[tools.ts, findings-store.ts, createFinding(), ensureDir(), getAllFindings(), slaDeadline()] | lang=en
- "lib_httpx_parser_httpxjsonldecoder": "HttpxJsonlDecoder" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L93 | neighbors=[tool-runners.ts, httpx-parser.ts, .decode(), .finish(), .malformedLines(), .push()] | lang=en
- "lib_security_context_securitycontexterror": "SecurityContextError" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L9 | neighbors=[route.ts, route.ts, route.ts, security-context.ts, publicCveRecord(), resolveSecurityReference()] | lang=en
- "main_scripts_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L160 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()] | lang=en
- "main_scripts_findings_main": "_main()" | kind=code-symbol | source=probe/main_scripts/findings.py:L684 | neighbors=[findings.py, .to_dict(), load_facts_jsonl(), run_findings(), summarize(), CLI: derive findings from one or more s…] | lang=en
- "main_scripts_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()] | lang=en
- "main_scripts_ja4x": "ja4x.py" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious()] | lang=en
- "main_scripts_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()] | lang=en
- "main_scripts_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L198 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()] | lang=en
- "main_scripts_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L236 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()] | lang=en
- "main_scripts_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()] | lang=en
- "main_scripts_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L251 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._scan_port()] | lang=en
- "main_scripts_run_all": "run_all.py" | kind=code-symbol | source=probe/main_scripts/run_all.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _log(), main(), _open_tcp_ports(), _ports_arg(), _read_jsonl()] | lang=en
- "main_scripts_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L777 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L484 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()] | lang=en
- "main_scripts_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L200 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…] | lang=en
- "main_scripts_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L261 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…] | lang=en
- "main_scripts_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _fetch(), main(), _NoRedirect, parse_allow_header(), WebScanner] | lang=en
- "me_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, backend(), withBackend(), GET, 298a9d4 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "models_user_user": "User" | kind=code-symbol | source=manager/backend/app/models/user.py:L13 | neighbors=[user.py, Base, TimestampMixin, Base, TimestampMixin, UserRole] | lang=en
- "native_tls_info": "tls-info.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, nativeTlsInfo(), TlsInfoResult, WEAK_PROTOCOLS, WEAK_SIGNATURES, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "portscan": "portscan.py" | kind=code-symbol | source=portscan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, classify_os_error(), family_of(), main(), parse_ports(), PortScanner] | lang=en
- "portscan_portscanner": "PortScanner" | kind=code-symbol | source=portscan.py:L112 | neighbors=[portscan.py, main(), ._attempt(), .__init__(), ._record(), .run()] | lang=en
- "probes_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, backend(), withBackend(), GET, 0557559 scanner: real use-case library,…, backend.ts] | lang=en
- "routers_activity": "activity.py" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, dependencies.py, ActivityItem, recent_activity(), Recent activity feed.  A tenant-wide, r…] | lang=en
- "routers_agent_advisor": "agent_advisor.py" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dependencies.py, list_recommendations(), _rec_dict(), run_advisor(), agent_advisor.py — API for the agentic …] | lang=en
- "routers_agents_bootstrap_agent": "bootstrap_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L570 | neighbors=[agents.py, AgentRegisterResponse, Allows a probe to register without an a…, Allows a probe to register without an a…, Allows a probe to register without an a…, Returns the finite library of scan use-…] | lang=en
- "routers_agents_enqueue_agent_job": "enqueue_agent_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L988 | neighbors=[agents.py, _agent_can_execute_job(), _encrypt_scope_for_agent(), _job_params_contain_secret(), _job_reachability_scope(), _normalize_intensity_name()] | lang=en
- "routers_agents_rationale_103": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L103 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=pt
- "routers_agents_rationale_139": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L139 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_207": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L207 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_387": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L387 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_425": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L425 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_444": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L444 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_706": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L706 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-025.json

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
