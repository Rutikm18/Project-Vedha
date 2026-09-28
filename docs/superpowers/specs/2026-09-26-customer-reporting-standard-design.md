# Customer Security Reporting Standard Design

**Status:** Implementation baseline; customer policy decisions remain open  
**Date:** 2026-09-26  
**Research:** [`docs/research/2026-09-26-customer-cybersecurity-reporting-standard.md`](../../research/2026-09-26-customer-cybersecurity-reporting-standard.md)

## Problem

The current reports workspace combines a capped findings list, an active-tab-only
print view, and AI-authored narrative. It does not provide a single authoritative
record for evidence provenance, remediation, lifecycle history, closure proof, or
versioned compliance mappings. A status such as `remediated` can therefore appear
without showing what was tested, when it was tested, or which recorded evidence
supports the disposition.

The report must be useful to both security operators and customers without
overstating facts. Missing evidence must remain missing, a framework relationship
must not become a compliance claim, and model-generated prose must not become the
source of truth.

## Design principles

1. Generate every view from one canonical, versioned report contract.
2. Keep recorded facts, deterministic projections, and generated narrative
   visibly distinct.
3. Preserve source timestamps and provenance; never substitute render time for an
   observation, remediation, retest, or closure timestamp.
4. Treat closure, risk acceptance, false-positive disposition, and duplicate
   disposition as different outcomes with different evidence requirements.
5. Map only recorded framework relationships, pinned to a version with rationale
   and limitations. Never infer certification or whole-control effectiveness.
6. Expose completeness gaps instead of inventing customer policy, SLA, evidence,
   or mappings.

## Current implementation boundary

This phase provides an operator-only `live_read_model` snapshot. It also adds
validated write contracts for optional structured retest/closure proof and open
finding action tracking, but it does not enforce a customer-specific closure
gate. It is not a published report artifact and is not safe for direct customer
delivery until review, redaction, immutable versioning, export hashing, and
customer-safe authorization are implemented.

The snapshot includes:

- document generation time, schema version, timezone, and non-persisted status;
- engagement, scope, exclusions, customer/assessor metadata when recorded, and
  explicit metadata gaps;
- reconciled summary counts over every finding in the engagement;
- per-finding asset context, description, severity/risk data, identifiers,
  observation times, separate initial-discovery and latest-observation run/scan
  provenance, verification state, and lifecycle history;
- manager-stamped scanner provenance that records the real scan result, scan
  job, tool, source, and timestamp basis; asynchronous probe findings are linked
  only to the completed detection run for that exact scan result, while job-only
  scanners retain a truthful null detection-run ID;
- normalized evidence presentation plus the exact recorded evidence value and
  provenance/integrity gaps;
- recorded remediation, reviewed remediation plans, verification steps,
  recommendations, compensating controls, and timestamp gaps;
- terminal/reopen history, recorded closure evidence, retest gaps, and clearly
  labelled auto-resolution coverage that is not patch attestation;
- recorded framework mappings and a framework/control rollup; and
- report/finding readiness gaps that block a future publication workflow.

AI report generation is a separate manager-owned workflow. The browser selects
only an engagement and bounded generation options. The backend reloads tenant-
scoped records, stores drafts, and requires human review. Generated text is never
used to populate canonical evidence, timestamps, status, closure, or mappings.

## Components and data flow

```text
PostgreSQL findings/assets/events/reviewed plans/detection runs/SLA policy
                              |
                              v
              deterministic report-document service
                              |
                              v
       operator-only GET /engagements/{id}/report-document
                              |
                              v
               authenticated Next.js BFF endpoint
                              |
                              v
   one fully mounted report document -> screen view / complete print view

Optional AI draft:
browser options -> authenticated BFF -> tenant/RBAC-scoped manager job
                -> persisted draft sections -> human review queue
```

The report service performs bounded batched queries. It does not call an LLM,
mutate a finding, persist a snapshot, or infer a missing relationship.

## Canonical report contract

The first response schema is `1.0` and contains:

- `document`: schema version, exact UTC generation instant, snapshot kind, and
  persistence flag;
- `engagement`: identity, scope, assessment time, parties, report metadata, and
  metadata gaps;
- `summary`: totals by recorded severity/status and closure/reopen projections;
- `findings[]`: the complete technical records described above;
- `compliance_rollup`: recorded mappings grouped by framework version and
  control, plus unmapped findings; and
- `readiness`: machine-readable gap counts and affected finding IDs.

Current SLA information is labelled as a projection from the effective tenant
policy at render time. It is not represented as the policy that applied
historically unless that policy version was actually recorded.

## Closure semantics

This phase does not change lifecycle policy. It reports the stored terminal state
and separately reports whether the supporting record is complete. Operators may
now submit a validated closure packet containing comparable before/after evidence,
the retest method and scope, tester/verifier, exact timestamps, tool configuration,
expected and actual results, coverage comparison, change reference, residual risk,
and reviewer. Legacy reason-only transitions remain visible as incomplete rather
than being silently upgraded to verified closure.

The recommended target state is `closed_verified`, valid only after a comparable
passed retest links the original and after evidence, records exact scope and
method, verifier and timestamps, remediation/change references, coverage
differences, and residual risk. Scanner non-observation without adequate coverage
is inconclusive rather than proof of closure.

Risk acceptance and false-positive dispositions require their own authority and
evidence. They must not be rendered as verified remediation. Whether a manager
may override a missing or failed retest is an unresolved customer policy decision;
no override rule is hard-coded in this phase.

## Compliance semantics

A mapping is a scoped relationship, not a certification statement. The full
target mapping record includes framework and version, profile/release, control ID
and title, relationship, applicability, assessment status, rationale, evidence
and test references, scope, mapping provenance, reviewer, timestamps, and
limitations.

The initial read model normalizes only mappings already present in recorded
finding data. Missing fields remain visible. A later registry and reviewed
mapping workflow should support NIST CSF 2.0, NIST SP 800-53 Rev. 5, CIS Controls
v8.1, ISO/IEC 27001:2022, PCI DSS 4.0.1, OWASP ASVS 5.0.0/WSTG 4.2, and MITRE
ATT&CK with pinned versions and licensing controls.

## Security and privacy

- Scope every backend query to the authenticated tenant and engagement.
- Keep this endpoint operator-only; do not reuse it as a portal DTO because raw
  evidence may contain restricted data.
- Reject caller-supplied facts at the AI-generation edge.
- Include only human-reviewed remediation plans in the factual report.
- Do not expose secrets from rules of engagement as report metadata.
- Before customer publication, add explicit redaction, secret scanning,
  classification, audience, access logging, retention, and secure-delivery rules.
- Published versions must be immutable and include an artifact digest; evidence
  originals and redacted derivatives need separate identities and hashes.

## Reliability and observability

- Summary values are calculated from the same in-memory finding records rendered
  in detail, avoiding separate count/list drift.
- Report queries are batched rather than performed once per finding.
- A future persisted report job must record source-record version, generation and
  publication events, validation failures, reviewer/approver, and artifact hash.
- Monitor generation latency, query failures, readiness-gap rates, redaction
  failures, export digest failures, and rejected publication attempts. Never log
  raw sensitive evidence.

## Verification

Automated checks for this phase must cover:

- tenant-scoped engagement lookup and indistinguishable foreign/missing 404s;
- exact timestamp preservation and no fabricated evidence/retest time;
- exclusion of unreviewed remediation plans and rules-of-engagement secrets;
- terminal/reopen history, closure evidence gaps, and coverage disclaimer;
- recorded-only compliance rollup and explicit unmapped state;
- summary/detail reconciliation;
- authenticated BFF behavior and rejection of caller-supplied facts;
- full-document print mounting rather than active-tab-only output; and
- frontend type checking plus focused report rendering/adapter tests.

## Rollout

1. Ship the operator-only live snapshot and full report workspace.
2. Validate the contract against representative open, remediated, accepted,
   false-positive, reopened, and unmapped records.
3. Confirm customer risk, SLA, approval, retention, framework, and closure-override
   policy before enforcing the optional structured closure contract as a gate.
4. Add a dedicated mapping registry and enforce the selected closure gate.
5. Add review/redaction and immutable PDF/HTML/JSON publication with manifests,
   digests, version history, and customer-safe authorization.
6. Add optional OSCAL Assessment Results export after the internal schema is
   stable.

## Decisions that must not be assumed

- assessment types and report variants to support first;
- customer risk model and override authority;
- remediation SLA rules and policy versioning;
- who may accept risk, approve false positives, and verify or override closure;
- evidence retention, region, classification, and restricted-original access;
- selected framework profiles and licenses for proprietary content;
- whether formal compliance conclusions are allowed and by which qualified role;
- branding, languages, accessibility target, and mandatory customer sections.
