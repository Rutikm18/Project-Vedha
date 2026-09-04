# Node Description Batch 236 of 332

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

- "routers_customer_access_rationale_110": "Per-tenant-unique portal slug: <base>, else <base>-2, <base>-3, … Two     custom" | kind=entity | source=manager/backend/app/routers/customer_access.py:L110 | neighbors=[_unique_portal_slug()]
- "routers_customer_access_rationale_122": "Pure: turn an approved request into a pending ScanJob on the engagement's     as" | kind=entity | source=manager/backend/app/routers/customer_access.py:L122 | neighbors=[build_scan_job()]
- "routers_customer_access_rationale_123": "Pure: turn an approved request into a pending ScanJob on the engagement's     as" | kind=entity | source=manager/backend/app/routers/customer_access.py:L123 | neighbors=[build_scan_job()]
- "routers_customer_access_rationale_124": "Pure: turn an approved request into a pending ScanJob on the engagement's     as" | kind=entity | source=manager/backend/app/routers/customer_access.py:L124 | neighbors=[build_scan_job()]
- "routers_customer_access_rationale_385": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L385 | neighbors=[list_customers()]
- "routers_customer_access_rationale_394": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L394 | neighbors=[list_customers()]
- "routers_customer_access_rationale_398": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L398 | neighbors=[list_customers()]
- "routers_customer_access_rationale_400": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L400 | neighbors=[list_customers()]
- "routers_customer_access_rationale_430": "Decrypt and return a customer login's stored password. Tenant-scoped and     wri" | kind=entity | source=manager/backend/app/routers/customer_access.py:L430 | neighbors=[reveal_customer_password()]
- "routers_customer_access_rationale_432": "Decrypt and return a customer login's stored password. Tenant-scoped and     wri" | kind=entity | source=manager/backend/app/routers/customer_access.py:L432 | neighbors=[reveal_customer_password()]
- "routers_customer_access_rationale_96": "A URL-safe temporary password the operator hands to the customer once." | kind=entity | source=manager/backend/app/routers/customer_access.py:L96 | neighbors=[generate_password()]
- "routers_customer_access_rationale_97": "A URL-safe temporary password the operator hands to the customer once." | kind=entity | source=manager/backend/app/routers/customer_access.py:L97 | neighbors=[generate_password()]
- "routers_customer_access_rationale_98": "A URL-safe temporary password the operator hands to the customer once." | kind=entity | source=manager/backend/app/routers/customer_access.py:L98 | neighbors=[generate_password()]
- "routers_detection_configure_siem": "configure_siem()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L61 | neighbors=[detection.py]
- "routers_detection_get_coverage": "get_coverage()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L148 | neighbors=[detection.py]
- "routers_detection_get_gaps": "get_gaps()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L187 | neighbors=[detection.py]
- "routers_detection_run_validation": "run_validation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L96 | neighbors=[detection.py]
- "routers_engagements_engagementupdate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L523 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L539 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L533 | neighbors=[EngagementUpdate]
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L459 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1222 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L625 | neighbors=[engagements.py]
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L398 | neighbors=[engagements.py]
- "routers_engagements_rationale_1115": "The machine-readable answer to \"the scripts catch it but the manager doesn't\"." | kind=entity | source=manager/backend/app/routers/engagements.py:L1115 | neighbors=[detection_explain()]
- "routers_engagements_rationale_1171": "The raw ScanResult facts as the probe submitted them, straight from the     appe" | kind=entity | source=manager/backend/app/routers/engagements.py:L1171 | neighbors=[raw_facts()]
- "routers_engagements_rationale_125": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L125 | neighbors=[_refresh_overview_cache()]
- "routers_engagements_rationale_1264": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L1264 | neighbors=[get_engagement_scope()]
- "routers_engagements_rationale_130": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L130 | neighbors=[re_detect()]
- "routers_engagements_rationale_156": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L156 | neighbors=[re_detect()]
- "routers_engagements_rationale_163": "Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s" | kind=entity | source=manager/backend/app/routers/engagements.py:L163 | neighbors=[_read_capped()]
- "routers_engagements_rationale_181": "Parse a probe export into (facts, scan_type).      Accepts two shapes the probe" | kind=entity | source=manager/backend/app/routers/engagements.py:L181 | neighbors=[_parse_probe_file()]
- "routers_engagements_rationale_189": "Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s" | kind=entity | source=manager/backend/app/routers/engagements.py:L189 | neighbors=[_read_capped()]
- "routers_engagements_rationale_207": "Parse a probe export into (facts, scan_type).      Accepts two shapes the probe" | kind=entity | source=manager/backend/app/routers/engagements.py:L207 | neighbors=[_parse_probe_file()]
- "routers_engagements_rationale_228": "Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen" | kind=entity | source=manager/backend/app/routers/engagements.py:L228 | neighbors=[_promote_from_facts()]
- "routers_engagements_rationale_254": "Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen" | kind=entity | source=manager/backend/app/routers/engagements.py:L254 | neighbors=[_promote_from_facts()]
- "routers_engagements_rationale_302": "Offline ingest path: upload a probe's scan export and run it through the     SAM" | kind=entity | source=manager/backend/app/routers/engagements.py:L302 | neighbors=[import_facts()]
- "routers_engagements_rationale_328": "Offline ingest path: upload a probe's scan export and run it through the     SAM" | kind=entity | source=manager/backend/app/routers/engagements.py:L328 | neighbors=[import_facts()]
- "routers_engagements_rationale_400": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L400 | neighbors=[engagements_overview()]
- "routers_engagements_rationale_42": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L42 | neighbors=[_compute_overview()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-235.json

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
