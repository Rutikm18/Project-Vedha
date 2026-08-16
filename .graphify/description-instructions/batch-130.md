# Node Description Batch 131 of 209

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

- "detection_vantage_fusion_rationale_38": "(ip → {(proto,port): {vantage: status}}, ip → set(vantages))." | kind=entity | source=manager/backend/app/detection/vantage_fusion.py:L38 | neighbors=[_collect()] | lang=en
- "detection_vantage_fusion_rationale_81": "Fuse several probes' exposure_matrix results into one per-target matrix.      `r" | kind=entity | source=manager/backend/app/detection/vantage_fusion.py:L81 | neighbors=[fuse_exposure_results()] | lang=en
- "detection_verification_rationale_1": "verification.py — normalized, dashboard-facing verification verdict.  The determ" | kind=entity | source=manager/backend/app/detection/verification.py:L1 | neighbors=[verification.py] | lang=en
- "detection_verification_rationale_46": "Deterministic passive verdict from a detection finding's evidence dict." | kind=entity | source=manager/backend/app/detection/verification.py:L46 | neighbors=[compute_verdict()] | lang=en
- "detection_verification_rationale_76": "Only spend an LLM call where a rationale / FP-triage is worth it:     uncertain" | kind=entity | source=manager/backend/app/detection/verification.py:L76 | neighbors=[_qualifies_for_llm()] | lang=en
- "detection_verification_rationale_83": "Deterministic verdict, optionally enriched by an LLM rationale. The LLM     (duc" | kind=entity | source=manager/backend/app/detection/verification.py:L83 | neighbors=[verify_finding()] | lang=en
- "dev_hint_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/auth/dev-hint/route.ts:L17 | neighbors=[route.ts] | lang=en
- "discovery_device_profile_rationale_1": "device_profile.py — map a probe device_inventory result onto asset fields.  The" | kind=entity | source=manager/backend/app/discovery/device_profile.py:L1 | neighbors=[device_profile.py] | lang=en
- "discovery_device_profile_rationale_30": "The AssetType for a classifier device_type, or None to keep the existing." | kind=entity | source=manager/backend/app/discovery/device_profile.py:L30 | neighbors=[asset_type_for()] | lang=en
- "discovery_device_profile_rationale_37": "ip → {asset_type, device_role, role_detail, role_confidence} from a probe     de" | kind=entity | source=manager/backend/app/discovery/device_profile.py:L37 | neighbors=[device_profiles()] | lang=en
- "discovery_exposure_rationale_1": "exposure.py — reachability-aware risk from the probe's exposure_matrix use-case." | kind=entity | source=manager/backend/app/discovery/exposure.py:L1 | neighbors=[exposure.py] | lang=en
- "discovery_exposure_rationale_38": "(ip, proto, port) → exposure verdict, from a probe exposure_matrix result." | kind=entity | source=manager/backend/app/discovery/exposure.py:L38 | neighbors=[service_exposure()] | lang=en
- "discovery_exposure_rationale_69": "Bump a finding one severity rung when its service is internet-reachable.      On" | kind=entity | source=manager/backend/app/discovery/exposure.py:L69 | neighbors=[escalate_for_exposure()] | lang=en
- "discovery_finding_translator_rationale_124": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L124 | neighbors=[_find_open_duplicate()] | lang=en
- "discovery_finding_translator_rationale_144": "Convert a probe's self-assessed `findings` list into persisted Finding rows." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L144 | neighbors=[create_findings_from_probe_result()] | lang=pt
- "discovery_finding_translator_rationale_210": "Raise ONE engagement-level finding when the probe's own metrics say the     scan" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L210 | neighbors=[create_scan_health_finding()] | lang=en
- "discovery_finding_translator_rationale_55": "Find the Asset for a probe-reported target IP, creating a minimal one if needed." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L55 | neighbors=[_resolve_asset()] | lang=en
- "discovery_finding_translator_rationale_77": "Best-effort port for a probe finding: explicit `port`, else the ':NNN'     suffi" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L77 | neighbors=[_finding_port()] | lang=en
- "discovery_rate_limiter_ratelimiter_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L30 | neighbors=[RateLimiter] | lang=en
- "discovery_rate_limiter_rationale_1": "RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[rate_limiter.py] | lang=en
- "discovery_rate_limiter_rationale_44": "True if current time is inside the allowed scan window." | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L44 | neighbors=[.is_within_window()] | lang=en
- "discovery_rate_limiter_rationale_61": "Blocks until a token is available for the given target IP.         Raises Runtim" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L61 | neighbors=[.acquire()] | lang=en
- "discovery_scan_health_rationale_1": "scan_health.py — turn the probe's per-host scan completeness/health metrics into" | kind=entity | source=manager/backend/app/discovery/scan_health.py:L1 | neighbors=[scan_health.py] | lang=en
- "discovery_scan_health_rationale_18": "Aggregate result['scan_metrics'] into a coverage/health verdict.        degraded" | kind=entity | source=manager/backend/app/discovery/scan_health.py:L18 | neighbors=[scan_health_summary()] | lang=pt
- "discovery_service_id_rationale_1": "ServiceIdentifier — banner + port → structured service fingerprint. Handles: HTT" | kind=entity | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[service_id.py] | lang=en
- "discovery_worker_discoveryjobpayload_post_init": ".__post_init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L50 | neighbors=[DiscoveryJobPayload] | lang=en
- "discovery_worker_discoveryworker_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L61 | neighbors=[DiscoveryWorker] | lang=en
- "discovery_xml_parser_parsedhost_open_ports": ".open_ports()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L36 | neighbors=[ParsedHost] | lang=en
- "discovery_xml_parser_rationale_1": "Nmap XML output parser. Converts -oX output into structured ParsedHost / ParsedP" | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[xml_parser.py] | lang=en
- "discovery_xml_parser_rationale_41": "Parse nmap -oX XML into a list of ParsedHost objects." | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L41 | neighbors=[NmapXMLParser] | lang=en
- "discovery_xml_parser_rationale_42": "Parse nmap -oX XML into a list of ParsedHost objects." | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L42 | neighbors=[NmapXMLParser] | lang=en
- "draft_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L4 | neighbors=[route.ts] | lang=en
- "engagements_page_empty_form": "EMPTY_FORM" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L41 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L17 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagementsresponse": "EngagementsResponse" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L15 | neighbors=[page.tsx] | lang=en
- "engagements_page_formstate": "FormState" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L33 | neighbors=[page.tsx] | lang=en
- "engagements_page_rowskeleton": "RowSkeleton()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L71 | neighbors=[page.tsx] | lang=en
- "engagements_page_sevcolor": "sevColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L63 | neighbors=[page.tsx] | lang=en
- "engagements_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L55 | neighbors=[page.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-130.json

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
