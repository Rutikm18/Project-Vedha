# Node Description Batch 28 of 332

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

- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L72 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…] | lang=en
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L72 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()] | lang=en
- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L132 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()] | lang=en
- "events_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/events/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fail(), GET(), backend.ts] | lang=en
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L120 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()] | lang=en
- "exposure_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 5d5c158 refactor: remove unused dashboa…, Exposure, GET, backend.ts, backend()] | lang=en
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder] | lang=en
- "lib_adapters_touifinding": "toUiFinding()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L116 | neighbors=[route.ts, route.ts, adapters.ts, evidenceToUi(), severityToPriority(), security-context.ts] | lang=en
- "lib_clients_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L52 | neighbors=[clients-store.ts, createClient(), getClient(), getClientBySubdomain(), listClients(), ensureDir()] | lang=en
- "lib_permissions_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L25 | neighbors=[permissions-store.ts, addUser(), getAllUsers(), getUser(), isEmailAllowed(), isScopeAllowed()] | lang=en
- "main_scripts_accuracy_gate": "accuracy_gate.py" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, check_thresholds(), CorpusError, format_gate_report(), is_independent(), load_corpora()] | lang=en
- "main_scripts_findings_main": "_main()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1335 | neighbors=[findings.py, .to_dict(), load_facts_jsonl(), run_findings(), summarize(), CLI: derive findings from one or more s…] | lang=en
- "main_scripts_ftp_scanner_ftpscanner": "FTPScanner" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L62 | neighbors=[ftp_scanner.py, BaseScanner, ._cmd(), .__init__(), ._list_bounded(), ._probe()] | lang=en
- "main_scripts_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L339 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._is_ambiguous()] | lang=en
- "main_scripts_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L448 | neighbors=[PortScanner, _family_of(), _harvest_tcp_stack(), ._build(), ._scan_port(), One connect() and its classification. A…] | lang=en
- "main_scripts_printer_scanner": "printer_scanner.py" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_ipp_get_printer_attributes(), _ipp_attr(), main(), parse_ipp_make_model(), parse_pjl_id()] | lang=en
- "main_scripts_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1133 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L785 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()] | lang=en
- "main_scripts_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L321 | neighbors=[service_banner.py, BaseScanner, ._connect(), ._grab(), .__init__(), ._ladder_for()] | lang=en
- "main_scripts_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L384 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()] | lang=en
- "main_scripts_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L87 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()] | lang=en
- "models_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/models/agent.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Enum, Agent] | lang=en
- "portal_portalshell_portalshell": "PortalShell()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L163 | neighbors=[page.tsx, page.tsx, page.tsx, page.tsx, PortalShell.tsx, page.tsx] | lang=en
- "posture_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/posture/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, backend.ts, backend(), with-backend.ts] | lang=en
- "register_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, toUiAgent(), backend(), withBackend(), GET, 2885afa Add comprehensive probe testing…] | lang=en
- "request_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), isEmailAllowed(), POST(), 2885afa Add comprehensive probe testing…] | lang=en
- "routers_ad_rationale_1": "Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun" | kind=entity | source=manager/backend/app/routers/ad.py:L1 | neighbors=[ad.py, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_ad_rationale_135": "Background task: run the AD assessment and persist findings + job result." | kind=entity | source=manager/backend/app/routers/ad.py:L135 | neighbors=[_run_ad_assessment_and_save(), ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_agents_rationale_106": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L106 | neighbors=[_scope_is_reachable(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=pt
- "routers_agents_rationale_142": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L142 | neighbors=[_job_reachability_scope(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_agents_rationale_210": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L210 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_709": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L709 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_93": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L93 | neighbors=[_required_scan_type(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_engagements_import_facts": "import_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L321 | neighbors=[engagements.py, _parse_probe_file(), _promote_from_facts(), _read_capped(), _refresh_overview_cache(), Offline ingest path: upload a probe's s…] | lang=en
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L31 | neighbors=[findings.py, finding_timeline(), get_finding(), patch_finding(), Fetch a finding scoped to the caller's …, reopen_finding()] | lang=en
- "routers_users": "users.py" | kind=code-symbol | source=manager/backend/app/routers/users.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, dependencies.py, activate_user(), deactivate_user(), get_user(), list_users()] | lang=en
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L270 | neighbors=[vuln_scans.py, Run Nuclei and always leave its job in …, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-027.json

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
