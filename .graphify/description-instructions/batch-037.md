# Node Description Batch 38 of 336

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
- "routers_engagements_compute_overview": "_compute_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L67 | neighbors=[engagements.py, engagements_overview(), Shared aggregation — used by both the c…, _refresh_overview_cache(), Shared aggregation — used by both the c…, Shared aggregation — used by both the c…] | lang=en
- "routers_engagements_engagements_overview": "engagements_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L425 | neighbors=[engagements.py, _compute_overview(), _overview_cache_key(), P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…] | lang=en
- "routers_findings_rationale_25": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L25 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_findings_rationale_26": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L26 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_findings_rationale_48": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L48 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_findings_rationale_49": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L49 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding] | lang=en
- "routers_probe_enrollment_activate_enrollment": "activate_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L684 | neighbors=[probe_enrollment.py, _authenticated_request(), _derive_refresh_secret(), _policy(), _rate_limit(), _secret_hash()] | lang=en
- "scanner_cpe": "cpe.py" | kind=code-symbol | source=probe/scanner/cpe.py:L1 | neighbors=[6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _extract_version(), to_cpe(), cpe.py — derive a CPE 2.3 identity from…] | lang=en
- "scanner_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L159 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…] | lang=en
- "scanner_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L206 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…] | lang=en
- "scanner_dns_scanner": "dns_scanner.py" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, derive_zones(), DNSScanner, _is_ip(), main(), dns_scanner.py — DNS server hygiene: zo…] | lang=en
- "scanner_dns_scanner_dnsscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L178 | neighbors=[DNSScanner, derive_zones(), ._axfr(), ._chaos_txt(), ._dnssec_present(), ._ptr_self()] | lang=en
- "scanner_findings_by_target": "_by_target()" | kind=code-symbol | source=probe/scanner/findings.py:L1082 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()] | lang=en
- "scanner_ftp_scanner": "ftp_scanner.py" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, banner_software(), FTPScanner, main(), parse_pasv(), ftp_scanner.py — FTP anonymous-access c…] | lang=en
- "scanner_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L406 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + UDP + neighbor signals in…, Combine TCP + neighbor signals into a c…] | lang=en
- "scanner_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L301 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()] | lang=en
- "scanner_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L362 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line(), Bulk {ip: normalized_mac} snapshot of t…, Bulk {ip: normalized_mac} snapshot of t…, ._arp_table()] | lang=en
- "scanner_ipmi_scanner": "ipmi_scanner.py" | kind=code-symbol | source=probe/scanner/ipmi_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_open_session_request(), IPMIScanner, main(), parse_open_session_response(), ipmi_scanner.py — IPMI 2.0 cipher-zero …] | lang=en
- "scanner_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=probe/scanner/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-037.json

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
