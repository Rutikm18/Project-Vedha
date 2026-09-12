# Node Description Batch 271 of 380

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

- "routers_detection_get_gaps": "get_gaps()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L187 | neighbors=[detection.py]
- "routers_detection_run_validation": "run_validation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L96 | neighbors=[detection.py]
- "routers_detection_runs_rationale_37": "Findings FIRST produced by this run — the \"what appeared\" half of a delta." | kind=entity | source=manager/backend/app/routers/detection_runs.py:L37 | neighbors=[_select_new_since()]
- "routers_engagements_engagementupdate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L523 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L539 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L533 | neighbors=[EngagementUpdate]
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L459 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1250 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L625 | neighbors=[engagements.py]
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L398 | neighbors=[engagements.py]
- "routers_engagements_rationale_1115": "The machine-readable answer to \"the scripts catch it but the manager doesn't\"." | kind=entity | source=manager/backend/app/routers/engagements.py:L1115 | neighbors=[detection_explain()]
- "routers_engagements_rationale_1171": "The raw ScanResult facts as the probe submitted them, straight from the     appe" | kind=entity | source=manager/backend/app/routers/engagements.py:L1171 | neighbors=[raw_facts()]
- "routers_engagements_rationale_125": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L125 | neighbors=[_refresh_overview_cache()]
- "routers_engagements_rationale_1264": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L1264 | neighbors=[get_engagement_scope()]
- "routers_engagements_rationale_1292": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L1292 | neighbors=[get_engagement_scope()]
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
- "routers_engagements_rationale_426": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L426 | neighbors=[engagements_overview()]
- "routers_engagements_rationale_68": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L68 | neighbors=[_compute_overview()]
- "routers_engagements_rationale_682": "Map a ScanJob status to the operator-facing scan phase shown on the card." | kind=entity | source=manager/backend/app/routers/engagements.py:L682 | neighbors=[_job_phase()]
- "routers_engagements_rationale_685": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L685 | neighbors=[get_engagement_scope()]
- "routers_engagements_rationale_699": "Derive ONE authoritative campaign phase from reconciled evidence, not from a" | kind=entity | source=manager/backend/app/routers/engagements.py:L699 | neighbors=[_reconcile_status()]
- "routers_engagements_rationale_745": "A SAFE, bounded view of a job's raw result — the counts an operator needs to" | kind=entity | source=manager/backend/app/routers/engagements.py:L745 | neighbors=[_result_summary()]
- "routers_engagements_rationale_767": "One call powers the VA Campaigns page: every probe's job (status + a safe raw" | kind=entity | source=manager/backend/app/routers/engagements.py:L767 | neighbors=[campaign_progress()]
- "routers_engagements_rationale_99": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L99 | neighbors=[_refresh_overview_cache()]
- "routers_exploits_list_audit_logs": "list_audit_logs()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L337 | neighbors=[exploits.py]
- "routers_findings_finding_summary": "finding_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L284 | neighbors=[findings.py]
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L184 | neighbors=[findings.py]
- "routers_findings_rationale_118": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L118 | neighbors=[sla_summary()]
- "routers_findings_rationale_144": "Mobilization metrics: how fast findings actually close, and who owns the     ope" | kind=entity | source=manager/backend/app/routers/findings.py:L144 | neighbors=[finding_metrics()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-270.json

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
