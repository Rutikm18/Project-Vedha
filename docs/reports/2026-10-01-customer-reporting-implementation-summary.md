# Customer Security Reporting Implementation Summary

- **Status:** Completed and deployed to `main`
- **Implementation commit:** `82492a72ea97d77ab22facfec4d228169937d7cf`
- **Completed:** 1 October 2026 (Asia/Kolkata)
**Scope:** Manager-side canonical customer security reports, finding evidence, closure/retest records, compliance context, and downloadable report formats

## Outcome

Vedha now produces a canonical customer security report from the complete tenant-scoped assessment record instead of relying on the truncated findings-list response. The standard report is the primary manager report and keeps missing information visible as an explicit readiness gap rather than inventing or silently omitting data.

## Work completed

### Complete finding records

Each report finding can include:

- title, description, severity, status, risk score, CVSS, EPSS, CVE, CWE and MITRE references;
- technical impact, business impact, exploitation details, prerequisites, root cause and reproduction steps;
- affected assets and initial/latest scan provenance, including detection tool and observation identifiers;
- evidence artifacts with collection metadata, timestamps, timezone information and integrity status;
- remediation instructions, recommendations, ownership, due dates, authoring/review provenance and update times;
- lifecycle history, SLA state, action tracking and report-readiness gaps.

The report endpoint loads the full engagement finding set and is not limited to the previous 100-finding page size.

### Closure and retest evidence

Finding closure now supports a structured resolution and retest record containing:

- before-and-after evidence;
- who performed and reviewed the retest;
- when and where it was performed;
- tool, configuration, scope, expected result and actual result;
- remediation/change reference, coverage and residual risk;
- cryptographic evidence integrity details;
- immutable lifecycle events for later audit.

Legacy closures remain readable, but reports explicitly flag missing closure proof instead of presenting them as fully verified.

### Compliance and framework mapping

The report separates evidence-backed recorded mappings from derived applicability guidance.

- Recorded mappings remain authoritative and contribute to the report's control rollups.
- Derived global context includes PCI DSS, ISO/IEC 27001, NIST SP 800-53, SOC 2 and HIPAA pointers.
- Derived regional context includes configured asset/sector applicability for RBI, CERT-In, SEBI and SWIFT-related obligations.
- Generic fallback mappings are visibly labelled.
- Derived mappings are explicitly marked as not assessed, not a certification, not an attestation and not legal advice.
- Asset tags are considered even when an asset currently has no findings.

### Standard report structure and exports

The customer report includes document control, engagement and assessment metadata, methodology/risk information, executive and technical summaries, detailed findings, compliance context, closure register and completeness warnings.

Supported outputs:

- browser/print report;
- PDF with Unicode font support;
- Word-compatible DOCX output;
- multi-sheet XLSX tracker;
- CSV finding tracker.

Export endpoints accept only an engagement identifier and format, then reload the canonical tenant-scoped record server-side. Browser-supplied report facts are not trusted.

## Security and data-boundary controls

- The canonical report endpoint is restricted to authenticated operator roles.
- Engagement, finding, event, remediation, scan, SLA and asset-tag queries are tenant scoped.
- The customer portal does not call the operator-only canonical endpoint.
- AI-generated report content stays review-gated and is not automatically approved.
- Trusted scan provenance is manager stamped; forged scanner provenance is discarded.
- Spreadsheet exports neutralize formula-injection values.
- Evidence and command content is masked before customer-facing rendering.

## Database and implementation changes

- Alembic `0050` records initial finding detection runs separately from later observations.
- Alembic `0051` records remediation provenance.
- The migration graph has one head: `0051`.
- Detection, discovery, workflow and outbox paths preserve trusted provenance and closure history.
- The responsive report UI introduced on `main` was retained during final integration.

## Verification completed

- Frontend test suite: **345 passed**.
- Final focused backend reporting/provenance/workflow suite: **79 passed**.
- Full backend suite before final rebase: **2,137 passed, 4 skipped**.
- TypeScript typecheck: passed.
- Next.js production build: passed.
- Alembic head check: passed (`0051`).
- Git whitespace/conflict checks: passed.
- Remote `main` was verified at implementation commit `82492a72ea97d77ab22facfec4d228169937d7cf` after deployment.

## Supporting design and research

- [Customer cybersecurity reporting standard research](../research/2026-09-26-customer-cybersecurity-reporting-standard.md)
- [Customer reporting standard design](../superpowers/specs/2026-09-26-customer-reporting-standard-design.md)

## Optional future enhancements

The requested reporting correction is complete. Future product enhancements may include persisted signed/final report versions, formal multi-party approval workflows, and continued maintenance of regulatory mappings as source requirements change.
