# Node Description Batch 37 of 330

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

- "main_scripts_msrpc_scanner": "msrpc_scanner.py" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _extract_tcp_ports(), main(), MSRPCScanner, _summarize()] | lang=en
- "main_scripts_nfs_scanner_parse_mount_export": "parse_mount_export()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L96 | neighbors=[nfs_scanner.py, ._mount_export(), is_world_readable(), _XDR, .string(), .u32()] | lang=en
- "main_scripts_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L48 | neighbors=[nmap_wrapper.py, .__init__(), OSError, _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()] | lang=en
- "main_scripts_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L152 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), match_stack_signature(), os_family_from_ttl(), Round the observed TTL up to the neares…] | lang=en
- "main_scripts_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()] | lang=en
- "main_scripts_run_all_main": "main()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L110 | neighbors=[run_all.py, _advertised_dynamic_ports(), _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl()] | lang=en
- "main_scripts_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L162 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), reconcile_ports(), route_ports()] | lang=en
- "main_scripts_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L817 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…] | lang=en
- "main_scripts_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L429 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…, Simple async rate limiter: at most `rat…] | lang=en
- "main_scripts_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L266 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …] | lang=en
- "main_scripts_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L235 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…, Soft-match collected bytes to {service,…] | lang=en
- "main_scripts_service_enum_serviceenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L558 | neighbors=[ServiceEnumScanner, classify_roles(), Enrichment, guess_os(), resolve_hostnames(), ._probe_port()] | lang=en
- "main_scripts_smb_enum_scanner_smbenumscanner_enumerate": "._enumerate()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L227 | neighbors=[Blocking: attempt a null session and en…, SMBEnumScanner, _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _merge_users()] | lang=en
- "main_scripts_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L224 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie(), Keyed 32-bit ISN for (dst_ip, dst_port,…, Keyed 32-bit ISN for (dst_ip, dst_port,…] | lang=en
- "main_scripts_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L231 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie(), A genuine reply to our SYN acknowledges…, A genuine reply to our SYN acknowledges…] | lang=en
- "main_scripts_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L275 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…] | lang=en
- "main_scripts_va_campaign_build_campaign": "build_campaign()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L620 | neighbors=[va_campaign.py, CampaignContext, default_stages(), ProgressReporter, VACampaign, Wire a campaign with the real scanners …] | lang=en
- "main_scripts_va_campaign_cliprogressview": "CliProgressView" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L649 | neighbors=[va_campaign.py, .__call__(), ._format(), .__init__(), ._redraw(), ._transitions()] | lang=en
- "main_scripts_va_campaign_progressreporter_flush": "._flush()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L265 | neighbors=[ProgressReporter, .finish(), _atomic_write_json(), .snapshot(), .__init__(), .mark()] | lang=en
- "me_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, backend(), withBackend(), GET, 298a9d4 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "models_user": "user.py" | kind=code-symbol | source=manager/backend/app/models/user.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 65f22a7 Add comprehensive tests for aut…, c4386e4 feat(customers): operator Custo…, d1b4dd3 trim frontend to 7 core pages; …, e3958e7 feat(customers): reveal + copy …, User] | lang=en
- "models_user_user": "User" | kind=code-symbol | source=manager/backend/app/models/user.py:L13 | neighbors=[user.py, Base, TimestampMixin, Base, TimestampMixin, UserRole] | lang=en
- "native_tls_info": "tls-info.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, nativeTlsInfo(), TlsInfoResult, WEAK_PROTOCOLS, WEAK_SIGNATURES, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "pats_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/pats/route.ts:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, backend.ts, backend(), with-backend.ts, withBackend(), GET] | lang=en
- "portscan": "portscan.py" | kind=code-symbol | source=portscan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, classify_os_error(), family_of(), main(), parse_ports(), PortScanner] | lang=en
- "portscan_portscanner": "PortScanner" | kind=code-symbol | source=portscan.py:L112 | neighbors=[portscan.py, main(), ._attempt(), .__init__(), ._record(), .run()] | lang=en
- "probes_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, backend(), withBackend(), GET, 0557559 scanner: real use-case library,…, backend.ts] | lang=en
- "raw_facts_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/raw-facts/route.ts:L1 | neighbors=[25c014d feat: enhance campaign progress…, backend.ts, backend(), BackendError, bearerFrom(), fail()] | lang=en
- "routers_activity": "activity.py" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, dependencies.py, ActivityItem, recent_activity(), Recent activity feed.  A tenant-wide, r…] | lang=en
- "routers_agent_advisor": "agent_advisor.py" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dependencies.py, list_recommendations(), _rec_dict(), run_advisor(), agent_advisor.py — API for the agentic …] | lang=en
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L139 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…] | lang=en
- "routers_agents_list_intensities": "list_intensities()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L619 | neighbors=[agents.py, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…] | lang=en
- "routers_agents_rationale_103": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L103 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=pt
- "routers_agents_rationale_139": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L139 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_207": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L207 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_387": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L387 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_425": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L425 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_444": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L444 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_706": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L706 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en
- "routers_agents_rationale_90": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L90 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-036.json

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
