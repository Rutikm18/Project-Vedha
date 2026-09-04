# Node Description Batch 87 of 332

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

- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser., 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "tools_issue_license_main": "main()" | kind=code-symbol | source=probe/tools/issue_license.py:L75 | neighbors=[issue_license.py, issue(), keygen(), pubkey()]
- "utils_db": "db.py" | kind=code-symbol | source=manager/backend/app/utils/db.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, get_or_404(), Shared database helpers — single source…, 298a9d4 trim frontend to 7 core pages; …]
- "utils_hash": "hash.py" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dedup_hash(), Shared hashing utilities — deduplicatio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0015_finding_risk_score_scale": "0015_finding_risk_score_scale.py" | kind=code-symbol | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, downgrade(), upgrade(), Allow the documented 0-1000 finding ris…]
- "versions_0016_user_tenant_is_active": "0016_user_tenant_is_active.py" | kind=code-symbol | source=manager/backend/alembic/versions/0016_user_tenant_is_active.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, downgrade(), upgrade(), Add is_active to users and tenants; add…]
- "versions_0017_scan_job_attempts": "0017_scan_job_attempts.py" | kind=code-symbol | source=manager/backend/alembic/versions/0017_scan_job_attempts.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add fenced execution attempts for agent…]
- "versions_0018_probe_enrollment": "0018_probe_enrollment.py" | kind=code-symbol | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add Manager-approved device-key probe e…]
- "versions_0020_finding_resolution_lifecycle": "0020_finding_resolution_lifecycle.py" | kind=code-symbol | source=manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, downgrade(), upgrade(), Finding resolution lifecycle: coverage-…]
- "versions_0021_finding_verification": "0021_finding_verification.py" | kind=code-symbol | source=manager/backend/alembic/versions/0021_finding_verification.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, downgrade(), upgrade(), Finding verification verdict columns (P…]
- "versions_0022_validation_requests": "0022_validation_requests.py" | kind=code-symbol | source=manager/backend/alembic/versions/0022_validation_requests.py:L1 | neighbors=[58c2d10 feat(active-validation): Valida…, downgrade(), upgrade(), Approval-gated safe active-validation r…]
- "versions_0023_customer_portal_foundation": "0023_customer_portal_foundation.py" | kind=code-symbol | source=manager/backend/alembic/versions/0023_customer_portal_foundation.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, downgrade(), upgrade(), Customer portal foundation (Part 2, Pha…]
- "versions_0025_service_exposure": "0025_service_exposure.py" | kind=code-symbol | source=manager/backend/alembic/versions/0025_service_exposure.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, downgrade(), upgrade(), Service exposure: persist the exposure_…]
- "versions_0026_client_portal_slug": "0026_client_portal_slug.py" | kind=code-symbol | source=manager/backend/alembic/versions/0026_client_portal_slug.py:L1 | neighbors=[c4386e4 feat(customers): operator Custo…, downgrade(), upgrade(), Client portal slug — the customer's sta…]
- "versions_0027_scan_request_targets_intensity": "0027_scan_request_targets_intensity.py" | kind=code-symbol | source=manager/backend/alembic/versions/0027_scan_request_targets_intensity.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, downgrade(), upgrade(), Scan-request targets + intensity — the …]
- "versions_0028_remediation_plans": "0028_remediation_plans.py" | kind=code-symbol | source=manager/backend/alembic/versions/0028_remediation_plans.py:L1 | neighbors=[fd5dc96 feat(remediation): AI + determi…, downgrade(), upgrade(), Remediation plans — cached, OS-specific…]
- "versions_0030_sla_policies": "0030_sla_policies.py" | kind=code-symbol | source=manager/backend/alembic/versions/0030_sla_policies.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, downgrade(), upgrade(), SLA policies — per-tenant custom remedi…]
- "versions_0031_integrations": "0031_integrations.py" | kind=code-symbol | source=manager/backend/alembic/versions/0031_integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, downgrade(), upgrade(), Integrations — per-tenant notification …]
- "versions_0032_scan_request_use_case": "0032_scan_request_use_case.py" | kind=code-symbol | source=manager/backend/alembic/versions/0032_scan_request_use_case.py:L1 | neighbors=[c7f226f chore: bundle pending working-t…, downgrade(), upgrade(), scan_requests.use_case_id — the capabil…]
- "versions_0033_finding_events": "0033_finding_events.py" | kind=code-symbol | source=manager/backend/alembic/versions/0033_finding_events.py:L1 | neighbors=[d98f654 feat(manager): network-VA campa…, downgrade(), upgrade(), Finding lifecycle audit trail — append-…]
- "versions_0034_run_lease_worker_heartbeat": "0034_run_lease_worker_heartbeat.py" | kind=code-symbol | source=manager/backend/alembic/versions/0034_run_lease_worker_heartbeat.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, downgrade(), upgrade(), Stage 2b: DetectionRun lease + worker h…]
- "versions_0036_scan_job_reference": "0036_scan_job_reference.py" | kind=code-symbol | source=manager/backend/alembic/versions/0036_scan_job_reference.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, downgrade(), upgrade(), scan jobs get a human-readable referenc…]
- "versions_0037_scan_job_cancelled_status": "0037_scan_job_cancelled_status.py" | kind=code-symbol | source=manager/backend/alembic/versions/0037_scan_job_cancelled_status.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, downgrade(), upgrade(), scan jobs gain a terminal `cancelled` s…]
- "vuln_enrichment_vulnenrichmentservice_check_cisa_kev": ".check_cisa_kev()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L244 | neighbors=[True if CVE is in the CISA Known Exploi…, VulnEnrichmentService, ._get_kev_catalog(), ._fetch_all()]
- "vuln_enrichment_vulnenrichmentservice_compute_composite_risk": ".compute_composite_risk()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L297 | neighbors=[Returns composite risk score on 0-1000 …, VulnEnrichmentService, .get(), .enrich()]
- "vuln_enrichment_vulnenrichmentservice_fetch_epss": ".fetch_epss()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L215 | neighbors=[Returns {epss_score: float, percentile:…, VulnEnrichmentService, ._fetch_all(), .get()]
- "vuln_nessus_nessusscanner_export_nessus_file": ".export_nessus_file()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L256 | neighbors=[NessusScanner, ._get_client(), Request + poll + download .nessus XML f…, Request + poll + download .nessus XML f…]
- "vuln_nessus_nessusscanner_launch_scan": ".launch_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L139 | neighbors=[NessusScanner, ._get_client(), Returns scan_uuid (token for tracking)., Returns scan_uuid (token for tracking).]
- "vuln_nessus_nessusscanner_poll_status": ".poll_status()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L150 | neighbors=[NessusScanner, ._get_client(), Returns {status, progress_percent, host…, Returns {status, progress_percent, host…]
- "vuln_nuclei_nucleiscanner_partial_or_raise": "._partial_or_raise()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L337 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, .run_scan()]
- "vuln_nuclei_nucleiscanner_template_selector": ".template_selector()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L444 | neighbors=[NucleiScanner, Given a list of service names on an ass…, Given a list of service names on an ass…, Given a list of service names on an ass…]
- "vuln_nuclei_rationale_1": "NucleiScanner — async subprocess wrapper around the Nuclei CLI.  Nuclei outputs" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[nuclei.py, FindingSeverity, FindingStatus, ServiceFingerprint]
- "vuln_nuclei_rationale_110": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L110 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_127": "Run Nuclei and stream JSONL findings from stdout.          ``request_timeout_sec" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L127 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_132": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L132 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_195": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L195 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_383": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L383 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_446": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L446 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_68": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L68 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-086.json

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
