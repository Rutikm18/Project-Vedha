# Customer-facing cybersecurity finding and closure reporting standard

**Date:** 2026-09-26

**Status:** primary-source research and product/data-contract recommendation; no product code is changed by this document

**Scope:** customer-facing vulnerability assessment, penetration-test, application-security, and retest reports produced by Vedha

**Source policy:** official standards bodies, official framework owners, and first-party specifications only

## Executive decision

Vedha should adopt a versioned **Reporting Profile 1.0** with one canonical,
machine-readable assessment record and human PDF/HTML views generated from that
record. The profile should combine:

- NIST SP 800-115's assessment-report, activity-log, data-handling, finding, and
  mitigation guidance;
- NIST OSCAL's separation of observations/evidence, risks, findings, and
  remediation information;
- OWASP's customer-oriented report structure and application verification
  coverage records;
- FIRST CVSS for technical severity, without treating CVSS as business risk;
- explicit, versioned, evidence-backed mappings to each customer's applicable
  frameworks; and
- an append-only status and retest history that makes a verified closure
  auditable.

There is no single universal report layout mandated across these sources. NIST
SP 800-115 expressly anticipates different report formats for different
audiences, while OWASP WSTG calls its report structure suggestions rather than
strict rules ([NIST SP 800-115, section 8.2](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf),
[OWASP WSTG 4.2 Reporting](https://wstg.owasp.org/v4.2/5-Reporting/)). The
standardization opportunity is therefore a stable data contract and quality
gate, not one rigid visual template.

The essential product rule is:

> A finding is never erased or silently rewritten. Every status change is a
> dated event. `closed_verified` is allowed only after a scoped retest links
> before-and-after evidence to the same finding occurrence and records who
> verified it, how, when, from where, with which tools and coverage, and what
> residual risk remains.

## 1. How to interpret “required”

This research uses three requirement classes so the product does not confuse a
best practice with a legal or certification obligation.

| Class | Meaning in this document |
|---|---|
| **External requirement** | Binding only when the customer's contract, regulated scope, chosen assurance standard, or assessment program makes it applicable. Example: PCI DSS external scans used for PCI validation have PCI-specific assessor and report conditions. |
| **Framework guidance** | An authoritative practice or reporting recommendation, but not automatically mandatory for every customer. Examples include NIST SP 800-115 and OWASP WSTG. |
| **Vedha profile MUST/SHOULD** | A product data-contract decision recommended here. `MUST` is necessary for a trustworthy standard report; `SHOULD` is expected unless the assessment type makes it inapplicable. It is not a claim that every cited framework uses that exact normative word. |

The report must label the applicable assessment basis and must not claim
“compliant,” “certified,” “audit passed,” or equivalent merely because findings
were mapped to controls. An individual technical finding can support or
contradict evidence for a control objective, but cannot by itself establish the
organization-wide design and operating effectiveness of that control.

## 2. What the primary sources actually establish

### 2.1 NIST assessment reporting and records

NIST SP 800-115 says an assessment report should identify vulnerabilities and
recommended mitigation, and that the internal report should include the
methodology, results, analysis, and a plan of action and milestones. It also
says mitigation recommendations, including root-cause analysis, should be
developed for each finding. Different audiences may need different formats
([NIST SP 800-115, sections 8.1-8.2](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)).

The same publication gives a useful minimum activity log: date/time, assessor,
assessment-system identifier, target-system identifier, tool, command, and
comments. It calls for secure storage of plans/rules of engagement, tool
configurations, raw output, findings, reports, and remediation plans, plus
secure transmission and handling defined before the test
([NIST SP 800-115, sections 7.4.1-7.4.3](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)).
These records are the basis for Vedha's evidence-provenance fields.

The report is sensitive assessment data. NIST recommends securing assessment
artifacts, and OWASP recommends encrypting a report for its receiving party
([NIST SP 800-115, section 7.4](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf),
[OWASP WSTG 4.2 Reporting](https://wstg.owasp.org/v4.2/5-Reporting/)). Access
classification, authorized recipients, export encryption, and retention are
therefore report metadata, not deployment afterthoughts.

### 2.2 OSCAL as the machine-readable model

NIST's OSCAL Assessment Results model already separates:

- assessment metadata and the linked assessment plan;
- reviewed controls, subjects, team, tools, and rules of engagement;
- an assessment log with start/end timestamps;
- observations and their evidence;
- risks, recommendations, false-positive/risk adjustments, operationally
  required risks, and expiry information;
- findings that link observations and risks; and
- back-matter resources/attachments.

That model is described by NIST at
[OSCAL Assessment Results](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-results/)
and the wider [OSCAL assessment layer](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/).
OSCAL supports XML, JSON, and YAML; an OSCAL export can be added later without
forcing the customer-facing report to expose raw OSCAL terminology.

OSCAL also requires document identity/version discipline: when an OSCAL
document changes, its root UUID and `last-modified` value change, while a pure
format conversion retains them
([NIST OSCAL Assessment Results](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-results/)).
Vedha should apply the same principle to published report revisions: immutable
published versions linked by `supersedes_report_id`, never mutation in place.

### 2.3 OWASP report usability and application verification

OWASP WSTG 4.2 recommends a report with version control, team, scope,
limitations, timeline, executive summary, finding summary, detailed findings,
methodology, severity method, cleaned tool output, and a test checklist. Its
suggested finding detail includes a stable reference, title, likelihood or
exploitability, impact, risk, technical description, exploitation/damage,
masked sensitive data, detailed remediation, and references
([OWASP WSTG 4.2 Reporting](https://wstg.owasp.org/v4.2/5-Reporting/)). It also
recommends that a retest summarize prior findings, updated status, and
cross-references rather than presenting the retest as an unrelated report.

For ASVS-based assessments, OWASP says the report should include the scope, a
summary of all requirements checked, exceptions, non-applicable requirements,
and guidance for resolving issues. Verification methods should be disclosed
and ideally repeatable, with robust evidence such as work papers, screenshots,
scripts, and test logs; automated tooling alone is not adequate assurance
([OWASP ASVS 5.0 Assessment and Certification](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x04-Assessment_and_Certification.md)).
OWASP does not certify vendors or applications, so the report must not present
an “OWASP certification” or implied OWASP endorsement.

ASVS references should include the released version and full requirement ID,
for example `ASVS 5.0.0 / Vx.y.z`. WSTG references should likewise use a
released, versioned scenario identifier such as `WSTG-v42-...`, not a moving
`latest` or development URL
([OWASP ASVS repository](https://github.com/OWASP/ASVS),
[OWASP WSTG 4.2](https://wstg.owasp.org/v4.2/)).

### 2.4 Current NIST control expectations relevant to vulnerability reports

As of this research date, NIST publishes SP 800-53 Rev. 5 as Release 5.2.0
([NIST SP 800-53 Rev. 5 current release](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)).
The especially relevant controls are:

- `RA-5 Vulnerability Monitoring and Scanning`: scan at organization-defined
  frequencies and when new relevant vulnerabilities are identified; use
  interoperable standards where possible; analyze reports; remediate legitimate
  vulnerabilities in organization-defined, risk-based response times; and
  share relevant vulnerability information. Enhancements cover breadth/depth,
  trend analysis, historical results, and multi-hop correlation.
- `CA-5 Plan of Action and Milestones`: document planned remediation actions
  and update them based on assessments, audits, and continuous monitoring.
- `SI-2 Flaw Remediation`: identify, report, correct, test, and install security
  updates within organization-defined risk-based periods; enhancement `SI-2(3)`
  addresses measuring time to remediate against benchmarks.
- `AU-3 Content of Audit Records`: capture event type, when, where, source,
  outcome, and associated identities.
- `AU-8 Time Stamps`: use timestamps traceable to an authoritative source and
  record UTC or a fixed/local offset.
- `AU-9 Protection of Audit Information`: protect audit records, including
  cryptographic protection where the selected enhancement applies.

The control text and discussion are in the official
[NIST SP 800-53 Rev. 5 publication](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf).
These controls support the data fields recommended here, but their frequencies
and remediation deadlines remain customer-defined unless another applicable
regime sets them.

## 3. Reporting Profile 1.0

### 3.1 Delivery package and views

Each published assessment SHOULD produce the following from the same canonical
record:

1. A customer-readable PDF and accessible HTML report.
2. A machine-readable JSON export conforming to a versioned schema.
3. A protected evidence manifest containing metadata and hashes; evidence
   binaries are separate protected objects or explicitly embedded attachments.
4. When relevant, a delta/retest view comparing the original and latest state.
5. Optional exports for OSCAL Assessment Results and customer ticketing systems.

The PDF/HTML is a view, not the source of truth. All counts, status summaries,
control mappings, and closure statements must be computed from the canonical
record so the executive and technical sections cannot disagree.

### 3.2 Standard human-readable section order

| Order | Section | Required customer information |
|---:|---|---|
| 1 | Cover and handling | Customer, report/engagement ID, assessment type, classification, version, final/draft status, issue date, authorized recipients. |
| 2 | Document control | Authors/reviewers/approvers, full version/change history, predecessor/superseding report, distribution, artifact hash/signature. |
| 3 | Executive summary | Business objective, scope and dates, overall posture, count by customer risk/status, highest business risks, material trends, strategic recommendations, closure/retest summary, and limitations. Avoid raw tool jargon. |
| 4 | Engagement context | Authorization/rules of engagement, in-scope and excluded assets, assessment window, locations/vantage points, credentials/privileges, sampling, methodology, tools/versions, coverage achieved, unassessed areas, assumptions, and constraints. |
| 5 | Risk methodology | Customer risk model and version, severity scale, CVSS use, threat/context enrichments, confidence, SLA/due-date policy, and exception rules. |
| 6 | Findings summary | Finding ID, title, affected occurrence count/assets, severity, customer risk, status, owner, due date, age, retest state, and applicable framework references. Counts must reconcile to detail. |
| 7 | Detailed findings | The complete per-finding profile in section 4, including evidence, remediation, and lifecycle/retest history. |
| 8 | Remediation roadmap / POA&M | Prioritized actions, owners, milestones, dependencies, due dates, acceptance/exception expiry, validation plan, and residual risks. |
| 9 | Retest and closure register | Every original finding, current disposition, before/after evidence references, test coverage, verification outcome, verifier, date, residual risk, and reopening history. |
| 10 | Compliance/control mapping | Framework and version, profile/scope, control ID/title, relationship and rationale, evidence/test status, exceptions, mapping provenance, and explicit non-certification disclaimer. |
| 11 | Appendices | Asset and coverage matrix, test checklist including pass/fail/not-tested/not-applicable, sanitized tool output, glossary, references, and evidence manifest. |

This structure combines the audience split in NIST SP 800-115 with the
executive/technical and version-control structure suggested by
[OWASP WSTG 4.2](https://wstg.owasp.org/v4.2/5-Reporting/). It also satisfies the
ASVS need to show the checks performed rather than reporting failures only
([OWASP ASVS 5.0 reporting guidance](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x04-Assessment_and_Certification.md)).

## 4. Canonical data contract

The names below are recommendations for the schema, not a claim that any cited
framework prescribes these exact property names.

### 4.1 Report and engagement metadata

| Field group | Reporting Profile 1.0 requirement |
|---|---|
| Identity | `report_id` (UUID), `schema_version`, `report_version`, `report_status` (`draft`, `final`, `superseded`), `supersedes_report_id`, `engagement_id`, `assessment_id`, `customer_id`, title, assessment type. Published identity is immutable. |
| Ownership and approval | Provider organization, customer organization, authors, assessors, reviewers, approver, business/system owners, role and organization for each person, approval timestamp. Avoid exposing unnecessary personal data in broad exports. |
| Scope | Objectives; authorized scope; asset identifiers and environments; exclusions; assessment period; locations/vantage points; authenticated/unauthenticated status and privilege; sampling strategy; authorization and rules-of-engagement references. |
| Execution | Methodology and versions; tool names, versions/builds, plugin/signature/catalog/feed versions; scan/run IDs; relevant sanitized configurations; limitations, interruptions, errors, and unassessed areas; achieved coverage. |
| Risk method | Risk-method ID/version, severity scale, customer context inputs, likelihood/impact method, CVSS versions accepted, threat-enrichment sources and retrieval dates, remediation-SLA policy/version. |
| Handling | Classification, authorized audiences, distribution list, retention/deletion policy, evidence location, export protection, redaction policy, legal/contract references where applicable. |
| Time | `assessment_started_at`, `assessment_ended_at`, `generated_at`, `published_at`, `last_modified_at`, and `superseded_at`, all timezone-aware. |
| Integrity | Generated artifact MIME type/size/SHA-256, optional digital-signature metadata, evidence-manifest hash, source record UUID/version. |
| Change history | Append-only entries containing report version, prior version, changed fields/sections, change reason, author, reviewer/approver, and timestamp. |

NIST SP 800-115 makes scope, logistics, roles, systems, testing locations,
schedule, authorized activities, data handling, and incident handling part of
planning and rules of engagement
([NIST SP 800-115, chapters 5-6](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)).
Those inputs must survive into the final record so customers can understand what
the report does and does not prove.

### 4.2 Finding and affected-occurrence fields

One finding may affect many assets. Use a stable finding record for the common
condition plus a stable `occurrence_id` for each affected asset/component. This
allows an occurrence to close while another remains open without cloning or
losing the common remediation guidance.

| Field group | Required fields |
|---|---|
| Identity | Immutable `finding_id`, immutable `occurrence_id`, human reference, fingerprint/dedup key and version, source detector/test ID and version, title, finding type/category. |
| Condition | Clear description, observed condition, expected condition/control objective, root cause or `unknown`, preconditions, affected component/version/configuration, and reproducible steps or safe validation procedure. Distinguish observed fact from analyst inference. |
| Asset context | Canonical asset ID plus relevant hostname/FQDN/IP/URL, cloud/resource ID, environment, application/service/component, port/protocol/path/parameter, package identity (CPE/PURL where reliable), business owner, business criticality, data sensitivity, and exposure. Do not rely on mutable IP address alone. |
| Evidence | One or more `evidence_id` links for confirmation; confidence and rationale; evidence visible to the customer or an explicit access restriction/reason. |
| Impact and likelihood | Technical CIA/safety/privacy impact, business impact, attack preconditions, privileges/user interaction, reachability/exposure, exploit maturity, active exploitation context, likelihood rationale, and uncertainty. |
| Severity and risk | All CVSS objects; separate customer risk rating/score; risk model/version; rationale; analyst override with prior value, reason, author, and timestamp. |
| External identifiers | CVE(s), CWE(s), vendor advisory IDs, package/product identifiers, and authoritative references. Values are nullable; never invent a CVE/CWE match. |
| Threat relevance | CISA KEV record/date, EPSS probability/percentile/model/retrieved-at, exploit references, and optional ATT&CK relationships with rationale. Dynamic enrichments retain the value used for the report rather than silently changing later. |
| Remediation | Desired outcome, concrete fix, alternatives/compensating controls, prerequisites, dependencies, operational risk, validation steps, rollback notes, owner, milestones, due date and basis, authoritative vendor references. |
| Workflow | Current status, current disposition, owner, SLA policy/version, due date, overdue state, exception/risk acceptance, lifecycle events, retest records, closure record, and reopen count. |
| Mapping | Zero or more versioned framework/control mapping objects as defined in section 8. |
| Time | `detected_at`, `first_observed_at`, `last_observed_at`, `confirmed_at`, `assigned_at`, `remediation_submitted_at`, `due_at`, `retest_requested_at`, `verified_at`, `closed_at`, and `reopened_at` as applicable. Missing events remain null, not copied from another date. |

The field set implements the finding content recommended by
[OWASP WSTG 4.2](https://wstg.owasp.org/v4.2/5-Reporting/), the per-finding
mitigation/root-cause expectation in
[NIST SP 800-115](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf),
and the finding/observation/risk separation in
[NIST OSCAL](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-results/).

### 4.3 Evidence object and provenance

| Field group | Required evidence metadata |
|---|---|
| Identity | Immutable `evidence_id`, evidence kind, short description, related finding/occurrence/asset/test/run IDs. |
| Observation | Precisely what was observed, expected result, actual result, and any analyst interpretation in a separate field. |
| Source | `manual`, `tool`, `imported`, or `customer_provided`; collector identity/role; tool name/version/build; plugin/rule/signature/feed version; collection method and sanitized command/configuration. |
| Context | Subject asset/component, location/vantage point, authentication and privilege level, request/response or test-step reference, assessment/run/scan IDs, environmental preconditions. |
| Time | `observed_at`, `collected_at`, and ingestion time, each RFC 3339 with a known UTC relationship. Preserve source clock offset and clock-synchronization/uncertainty notes when material. |
| Artifact | Protected object URI or attachment ID, file name, MIME type, byte size, SHA-256 digest, encoding/compression, capture format/version, and optional digital-signature metadata. |
| Handling | Classification, access policy, contains-secrets/PII/payment-data flags, redaction state/method, redacted derivative ID, and restricted original ID. The original is retained under stricter access when policy permits. |
| Custody | For forensic, disciplinary, or legal use: every custodian/transfer, action, purpose, timestamp, integrity check, and storage location. Otherwise explicitly mark chain of custody `not_required`. |
| Reproducibility | Prerequisites, sanitized reproduction steps, required credentials/role, expected result, cleanup, and known limitations. |

NIST SP 800-115's activity log is the baseline provenance record. When artifacts
may become legal or disciplinary evidence, NIST SP 800-86 additionally calls for
documenting every custodian and action, securing originals, analyzing copies,
and verifying original/copy integrity with message digests
([NIST SP 800-86](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-86.pdf)).
That full chain of custody is conditional; it should not be falsely implied for
ordinary scanner output.

Use SHA-256 or a stronger approved SHA-2/SHA-3 digest for stored artifacts. The
Secure Hash Standard defines digests used to detect changed messages/files
([NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)). A digest
proves that bytes match a previously hashed object; it does **not** prove that
the capture was truthful, complete, or associated with the correct asset. That
is why provenance and assessor attestation remain separate fields.

Sensitive values must be masked in customer-readable detail, as OWASP WSTG
recommends, without breaking traceability to a restricted original
([OWASP WSTG 4.2 Reporting](https://wstg.owasp.org/v4.2/5-Reporting/)). Never put
passwords, session tokens, private keys, full payment-account data, or unrelated
personal data into the broad report.

### 4.4 Remediation and recommendation object

Every confirmed finding MUST include an actionable remediation object, even
when the current state is “no vendor fix.” It contains:

- the security outcome to achieve;
- root cause addressed, or why the root cause is unknown;
- primary fix with exact affected component/configuration scope;
- vendor patch/release/advisory references and minimum safe version when known;
- prerequisites, dependencies, rollout risk, service-impact notes, and rollback;
- compensating controls and their limitations when a direct fix is unavailable;
- responsible owner, milestones, target date, and the policy/risk basis for that
  date;
- a customer-verifiable validation procedure and expected secure result;
- residual risk after the proposed action; and
- recommendation author/reviewer, creation time, revision history, and
  superseded guidance.

“Update software,” “patch immediately,” and “follow best practices” are not
sufficient remediation instructions unless the report also identifies the
affected component, target state, authoritative reference, operational caveats,
and a verification procedure. NIST SP 800-115 calls for mitigation and root
cause per finding, while NIST 800-53 `CA-5` and `SI-2` support planned,
risk-based, testable remediation tracking
([NIST SP 800-115](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf),
[NIST SP 800-53 Rev. 5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf)).

Vedha MUST NOT invent a universal remediation deadline. Store a due date, but
derive it from the customer's chosen policy/regime and retain `due_date_basis`
and `sla_policy_version`. Framework-specific periods apply only within their
scope; section 8.5 describes the PCI case.

### 4.5 Timestamp representation

Machine timestamps MUST use RFC 3339 with a UTC designator or numeric offset,
for example `2026-09-26T09:42:31Z` or `2026-09-26T15:12:31+05:30`. RFC 3339 is a
focused ISO 8601 profile designed for interoperable Internet timestamps and
requires a stated relationship to UTC
([RFC 3339](https://www.rfc-editor.org/info/rfc3339/)). If the display needs the
named civil-time zone, store it separately (for example `Asia/Kolkata`);
[RFC 9557](https://www.rfc-editor.org/info/rfc9557/) standardizes additional
time-zone information.

Do not overload one `date` field. At minimum distinguish:

- observed/detected/confirmed;
- assigned and due;
- remediation submitted;
- retest requested/started/completed;
- verified and closed;
- reopened;
- report generated/published/superseded; and
- evidence collected/ingested.

Dates without times are allowed only for deliberately day-granular business
deadlines. UI display may be localized, but exports retain the original instant
and offset.

## 5. Severity, likelihood, and customer risk

### 5.1 CVSS is severity, not the final risk decision

FIRST explicitly defines CVSS as a measure of vulnerability severity, not risk.
CVSS v4.0 has Base, Threat, Environmental, and Supplemental metric groups; the
Supplemental metrics do not change the score
([FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document),
[FIRST CVSS v4.0 user guide](https://www.first.org/cvss/v4.0/user-guide)). CVSS
v3.1 remains common in vendor and legacy records and likewise should not be used
alone as an organization's risk score
([FIRST CVSS v3.1 user guide](https://www.first.org/cvss/v3.1/user-guide)).

Each CVSS object MUST store:

- `version` (`4.0` or `3.1`);
- score and complete vector;
- nomenclature/metric group represented (for example Base versus a combined
  Threat/Environmental score);
- scoring source and scorer;
- `scored_at`;
- authoritative source reference, when imported; and
- any customer environmental inputs separately from vendor/NVD inputs.

If CVSS information is published, FIRST requires both the score and vector and
attribution to FIRST, with values conforming to the specification
([FIRST CVSS data representations](https://www.first.org/cvss/data-representations)).
Never silently convert or compare v3.1 and v4.0 as if their vectors were the
same. For display, v4.0 qualitative bands are None `0.0`, Low `0.1-3.9`, Medium
`4.0-6.9`, High `7.0-8.9`, and Critical `9.0-10.0`
([FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document)).

### 5.2 Separate customer risk object

Vedha SHOULD compute or record a separate `customer_risk` using versioned,
explainable inputs:

- technical severity;
- exploitability/likelihood and attack prerequisites;
- internet or trust-zone exposure;
- asset/business criticality and data sensitivity;
- credible business, safety, privacy, and operational impact;
- available/observed exploit activity;
- compensating controls and detectability;
- confidence and evidence quality; and
- customer risk appetite and policy.

The object includes the input values, rule/model version, output score/band,
rationale, author, time, and override audit trail. A CVSS Base 9.8 may have a
different customer risk in an isolated lab and on an internet-facing payment
system; the report must explain that difference rather than modifying the
source CVSS silently.

CISA's Known Exploited Vulnerabilities catalog is evidence of known active
exploitation and is an important prioritization input; CISA urges organizations
to prioritize cataloged vulnerabilities, while the federal deadlines in BOD
22-01 are binding specifically on U.S. Federal Civilian Executive Branch
agencies
([CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog),
[CISA KEV notice and BOD scope](https://www.cisa.gov/news-events/alerts/2025/08/12/cisa-adds-three-known-exploited-vulnerabilities-catalog)).

FIRST EPSS is a daily probability from `0` to `1` estimating whether exploitation
of a CVE will be observed in the next 30 days. It is not severity or complete
risk because it lacks asset impact, local exposure, and compensating-control
context
([FIRST EPSS](https://www.first.org/epss/),
[FIRST EPSS FAQ](https://www.first.org/epss/faq)). Store probability, percentile,
model version, score date, and retrieval time because scores change. KEV/EPSS
must enrich risk reasoning; neither is a replacement for the customer's impact
analysis.

## 6. Finding status, disposition, and append-only history

### 6.1 Recommended lifecycle

Use a controlled lifecycle rather than free-text status:

```text
unverified
  -> confirmed_open
  -> acknowledged_assigned
  -> in_progress
  -> remediation_submitted
  -> retest_pending
  -> closed_verified

retest failed or recurrence: any remediated/closed state -> reopened -> in_progress
```

`unverified` findings remain clearly separated from customer-confirmed findings.
An “open” finding can skip operational states when the customer does not use
Vedha workflow, but the transition event must still state why.

Disposition is separate from lifecycle status:

| Disposition | Required evidence/authority |
|---|---|
| `risk_accepted` | Named accountable authority, scope, rationale, residual risk, compensating controls, accepted-at, review/expiry date, and policy reference. Expiry returns the item to review/open; it is not `closed_verified`. |
| `false_positive` | Technical validation evidence disproving the condition, method/tool/context, analyst and approver, decided-at, review date if inputs can change. Preserve the original detection. |
| `duplicate` | Canonical finding/occurrence ID and explanation that identity/scope match. Workflow continues on the canonical record. |
| `out_of_scope` | Scope basis, approver, and decision time. This says it was not assessed, not that it is safe. |
| `deferred` | Accountable owner, business reason, residual risk, next review and expiry, and any compensating control. |
| `cannot_reproduce` | Retest details and limitations. This is not verified closure unless evidence demonstrates the insecure condition is absent with adequate coverage. |
| `not_retested` | Explicitly open/unverified state; never rendered as closed. |

### 6.2 Lifecycle event record

Every transition MUST append an event containing:

- `event_id`, finding and occurrence IDs;
- prior and new status/disposition;
- event timestamp;
- actor identity, role, and organization;
- reason/comment and policy rule;
- linked evidence, remediation, exception, ticket/change, and retest IDs;
- source (`human`, `scanner`, `integration`, `policy_engine`);
- approval identity/time when required; and
- source-record version/hash where events cross trust boundaries.

Current state is a projection of these events. Events cannot be edited or
deleted through normal product workflows; corrections are later events. This
supports historical and trend analysis expected by NIST `RA-5` and preserves
the assessment history called for by NIST SP 800-115
([NIST SP 800-53 Rev. 5, RA-5 enhancements](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf),
[NIST SP 800-115, section 7.4.2](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)).

## 7. Verified closure and retest evidence

### 7.1 Closure gate

`closed_verified` MUST fail validation unless the occurrence has a completed
retest record with all of the following:

1. The immutable original finding/occurrence and affected asset/component.
2. Linked original (“before”) evidence.
3. The claimed remediation and change/ticket/commit/patch/configuration
   references, without requiring secrets in the report.
4. Retest request, start, completion, and verification timestamps.
5. Tester/verifier identity, organization, and independence where the applicable
   program requires it.
6. Retest scope, asset inventory/snapshot, location/vantage point,
   authenticated/unauthenticated state, privilege, preconditions, method,
   tool/build, rule/plugin/feed version, and sanitized configuration.
7. The expected secure condition and the actual result.
8. Linked “after” evidence sufficient to demonstrate the original condition is
   removed, blocked, or otherwise resolved.
9. Coverage comparison with the original test and any gaps or changed scope.
10. Outcome: `passed`, `failed`, `partial`, or `inconclusive`.
11. Residual risk, compensating controls, new side effects/findings, and
    follow-up actions.
12. Verifier approval, `verified_at`, closure reason, and `closed_at`.

`closed_at` cannot precede `verified_at`; `verified_at` cannot precede retest
completion. A finding with some open occurrences remains open at aggregate
level, even if other occurrences are verified closed.

### 7.2 What counts as closure evidence

Good closure evidence is method-specific. Examples include:

- package/version and configuration evidence plus an authenticated rescan;
- the original request/test replay showing the secure response, with secrets
  masked;
- a configuration-state query plus an external behavior test;
- code/change references plus a repeatable security test in the deployed
  environment; or
- evidence that a compensating control prevents the original attack path,
  together with explicit residual risk and approval.

The absence of a scanner result is not automatically proof of remediation. CIS
Controls Assessment Specification 8.1 uses absence from the current
asset-vulnerability scan as an assumption for its `7.7` metric, but that metric
also depends on current/previous comparable scans
([CIS CAS Control 7.7](https://cas.docs.cisecurity.org/en/latest/source/Controls7/)).
Vedha should exceed that metric-level assumption: if asset coverage, credentials,
scanner health, signatures, or test equivalence are unknown, record
`not_observed` or `inconclusive`, not `closed_verified`.

PCI DSS provides a concrete regime-specific precedent: applicable internal and
external vulnerability scans are followed by remediation and rescans that show
the identified vulnerabilities were addressed across in-scope systems
([PCI SSC FAQ 1152](https://www.pcisecuritystandards.org/faqs/1152/)). This does
not make PCI's exact thresholds universal, but it supports the general need to
retain the original scan, corrective work, and confirming rescan together.

### 7.3 Reopening

A new observation matching a verified-closed occurrence creates a `reopened`
event and links both the old closure record and new evidence. Preserve the
original `closed_at`, record `reopened_at`, increment `reopen_count`, and explain
whether the cause is regression, incomplete remediation, changed exposure,
product reintroduction, or a new detection method. Trend reports should expose
reopened findings rather than counting them as unrelated new items.

## 8. Compliance and framework mapping

### 8.1 Mapping object

Every mapping MUST contain:

```text
mapping_id
framework_id, framework_name, framework_version, release/profile
control_id, control_title
relationship: supports | implicates | tests_part_of | contradicts | contextual
applicability: applicable | not_applicable | unknown
assessment_status: passed | failed | partial | not_tested | not_applicable
rationale
evidence_ids and test_ids
scope/asset/profile context
source_url and mapping_source/version
mapped_by, reviewed_by, mapped_at, reviewed_at
limitations and customer_statement
```

The report should display `assessment_status` only when the assessment actually
tested a defined objective with documented coverage. A vulnerability's
relationship to a control normally means `implicates` or `tests_part_of`, not
that the entire control “failed.”

NIST calls cross-framework relationships **Informative References**. Its 2026
quick-start guide says they identify relationships/crosswalks that help users
work toward CSF outcomes; they are not a substitute for reading or assessing
the source document
([NIST SP 1347](https://csrc.nist.gov/pubs/sp/1347/final)). NIST's catalog also
states that non-NIST mappings receive limited conformance review, not a NIST
endorsement of correctness. Vedha should therefore store mapping provenance and
review status and never describe a crosswalk as equivalence
([NIST OLIR program](https://csrc.nist.gov/projects/olir)).

### 8.2 NIST Cybersecurity Framework 2.0

Pin mappings to `NIST CSF 2.0`. The most directly relevant outcomes for
vulnerability reporting are:

| CSF 2.0 outcome | Reporting relationship |
|---|---|
| `ID.RA-01` | Identified, validated, and recorded asset vulnerabilities: finding identity, evidence, asset and validation state. |
| `ID.RA-03` | Recorded internal/external threats: relevant threat sources and ATT&CK/KEV context. |
| `ID.RA-04` | Recorded likelihood and impact: explainable likelihood/impact fields and uncertainty. |
| `ID.RA-05` | Risk prioritization: customer risk rationale, asset/business context, and ordered remediation. |
| `ID.RA-06` | Chosen, prioritized, planned, tracked, and communicated risk responses: remediation, ownership, due dates, events, and closure. |
| `ID.RA-07` | Managed changes/exceptions: risk acceptance, deferral, exception history and expiry. |
| `ID.IM-01` / `ID.IM-02` | Improvements from evaluations and security tests: trends, repeated findings, and roadmap. |
| `PR.PS-02` | Risk-based software maintenance/replacement/removal: patch/remediation findings where evidence supports the relationship. |

The authoritative outcome definitions and machine-readable Core are available
from the [NIST CSF 2.0 Reference Tool](https://csrc.nist.gov/projects/cybersecurity-framework/filters)
and the final framework publication is
[NIST CSWP 29](https://doi.org/10.6028/NIST.CSWP.29). Do not map every finding to
all risk-assessment outcomes; choose only evidence-supported relationships.

### 8.3 NIST SP 800-53 Rev. 5, Release 5.2.0

| Control | Use in customer mapping |
|---|---|
| `RA-5` and selected enhancements | Vulnerability identification, scan coverage/frequency, analysis, trend/history, risk-based remediation, and information sharing. Usually the primary vulnerability-assessment relationship. |
| `CA-2` | Control-assessment procedure and evidence where the engagement actually assesses selected controls. |
| `CA-5` | Remediation/POA&M fields, owners, milestones, and update history. |
| `CA-7` | Continuous-monitoring source, cadence, metrics, and reporting where applicable. |
| `RA-3` / `RA-7` | Customer risk assessment and selected risk response. |
| `SI-2` and selected enhancements | Flaw-remediation action, update testing, risk-based timeframes, and remediation-time metrics. |
| `AU-3`, `AU-8`, `AU-9` | Evidence/lifecycle event content, time-source/offset, and protection/integrity. |
| `CM-8` | Asset/inventory coverage linkage and gaps. |

Control IDs, enhancement IDs, baseline applicability, and organization-defined
parameters must be stored separately. Do not insert a customer-specific value
into an organization-defined parameter without the customer's policy. Use the
official [current release page](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
and [Rev. 5 publication](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf).

### 8.4 CIS Controls v8.1

CIS Controls v8.1 describes a prioritized set of safeguards, not a universal
legal mandate
([CIS Controls v8.1](https://www.cisecurity.org/controls/v8-1)). Relevant mapping
targets include:

| Safeguard | Relevant evidence/customer information |
|---|---|
| `7.1` | Documented vulnerability-management process and last review/update; CIS specifies annual review or when significant changes occur. |
| `7.2` | Documented risk-based remediation strategy and monthly-or-more-frequent review. |
| `7.5` | Internal asset coverage, scanner inventory/config, authenticated and unauthenticated coverage, and at-least-quarterly cadence for the applicable implementation groups. |
| `7.6` | Externally exposed asset coverage and monthly-or-more-frequent cadence. |
| `7.7` | Current versus previous asset-vulnerability results, remediation measure, scan dates, and remaining occurrences. |

The official assessment specification provides the required inputs, operations,
measures, and metrics for these safeguards
([CIS Controls Assessment Specification 8.1, Control 7](https://cas.docs.cisecurity.org/en/latest/source/Controls7/)).
A report mapping should expose actual asset coverage and scan equivalence, not
just say “mapped to CIS 7.”

### 8.5 ISO/IEC 27001:2022

ISO/IEC 27001:2022 defines requirements for an information security management
system; the current official page also lists Amendment 1:2024
([ISO/IEC 27001:2022](https://www.iso.org/standard/27001)). A vulnerability report
does not establish certification or an ISMS-wide nonconformity.

Potentially relevant references, to be selected only after considering the
customer's risk treatment and Statement of Applicability, include:

- clause `6.1.3` for information-security risk treatment and the Statement of
  Applicability context;
- Annex A `5.7` threat intelligence;
- Annex A `5.36` compliance with information-security policies, rules, and
  standards;
- Annex A `8.8` management of technical vulnerabilities;
- Annex A `8.9` configuration management;
- Annex A `8.15` logging;
- Annex A `8.16` monitoring activities; and
- Annex A `8.29` security testing in development and acceptance.

The mapping object must include the customer's SoA status and rationale when
provided. Annex A is a reference set used in the risk-treatment process; it is
not correct to declare every Annex A control universally applicable. Official
ISO audit guidance explains the relationship between necessary controls, Annex
A, and the SoA
([ISO/IEC 27001 Auditing Practices Group — SoA](https://committee.iso.org/files/live/sites/jtc1sc27/files/resources/ISO-IECJTC1-SC27-WG1_N3298_Auditing%20Practices%20Note%20-%20SoA.pdf)).
NIST's OLIR catalog contains a final 2026 `ISO/IEC-27001:2022-to-CSFv2.0`
mapping, which may seed a reviewed crosswalk but is not proof of equivalent
control effectiveness
([NIST OLIR](https://csrc.nist.gov/projects/olir)).

### 8.6 PCI DSS v4.0.1

PCI DSS v4.0.1 is the current limited revision; PCI SSC says it clarified and
corrected v4.0 without adding or deleting requirements
([PCI SSC v4.0.1 announcement](https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1),
[PCI SSC Document Library](https://www.pcisecuritystandards.org/document_library/)).
Relevant mapping targets include:

| PCI DSS area | Report data needed when in PCI scope |
|---|---|
| `6.3.1` | Industry-recognized vulnerability sources, customer/environment-specific risk ranking, and identification of at least high/critical items. The customer's ranking may differ from an external source if documented. |
| `6.3.3` | Patch/update release date, applicability, customer risk rank, installed/target version, and deadline evidence. PCI SSC clarifies that the one-month requirement applies to critical security patches/updates; other timelines are risk-determined. |
| `11.3.1` family | Internal scan date, complete in-scope coverage, scanner currency/configuration, authenticated coverage where applicable, high/critical remediation, responsible/independent tester context, and confirming rescan evidence. |
| `11.3.2` family | External in-scope scan and rescan details, ASV identity where an ASV scan is required, passing-scan context, and significant-change scan evidence where applicable. |

PCI SSC's current FAQ explains the risk-ranking and remediation expectations
([PCI SSC FAQ 1597](https://www.pcisecuritystandards.org/faqs/1597/)); its scan
FAQ explains that all in-scope systems must be covered and rescans must show the
initial vulnerabilities were remediated
([PCI SSC FAQ 1152](https://www.pcisecuritystandards.org/faqs/1152/)). The
quarterly phrase means at least once every three months and scanning is also
required after significant changes in applicable scope
([PCI SSC FAQ 1087](https://www.pcisecuritystandards.org/faqs/1087/)).

A Vedha report must not call itself a PCI ROC, AOC, SAQ, or official ASV report
unless produced under the corresponding PCI program and official form. PCI SSC
states that an ASV scan does not prove overall PCI DSS compliance and that its
official ASV templates cannot be replaced by supplemental documentation
([PCI SSC FAQ 1234](https://www.pcisecuritystandards.org/faqs/1234/)).

### 8.7 OWASP ASVS 5.0.0 and WSTG 4.2

For an application finding, mapping and coverage are different records:

- A `finding_mapping` links a demonstrated issue to one or more ASVS
  requirements and/or WSTG scenarios, with rationale and evidence.
- A `test_result` records every selected requirement/scenario as `passed`,
  `failed`, `partial`, `not_tested`, or `not_applicable`, with method, evidence,
  tester, time, and rationale.

For ASVS, store release `5.0.0`, verification level/profile, full requirement
ID, requirement result, method (manual/dynamic/source review/etc.), and N/A or
exception rationale. For WSTG, store stable version `4.2`, full `WSTG-v42-...`
scenario ID, test coverage, result, and evidence. This implements OWASP's demand
for explicit scope and checked requirements rather than a failure-only claim
([OWASP ASVS 5.0 reporting guidance](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x04-Assessment_and_Certification.md),
[OWASP WSTG 4.2 Reporting](https://wstg.owasp.org/v4.2/5-Reporting/)).

### 8.8 MITRE ATT&CK v19.2

As of 2026-09-26, MITRE lists ATT&CK v19.2 as current
([MITRE ATT&CK version history](https://attack.mitre.org/resources/versions/)).
ATT&CK models adversary behavior; a technique describes how an adversary may
achieve a tactical goal. It is not a vulnerability-control or compliance
catalog.

Only add an ATT&CK relationship when the evidence supports it. Store:

- ATT&CK version and domain (`enterprise`, `mobile`, or `ics`);
- technique/sub-technique ID and title;
- relationship `observed`, `enables`, `could_enable`, or `mitigates`;
- evidence/rationale and confidence;
- analyst and review time; and
- source permalink.

For example, a demonstrably exploitable internet-facing application weakness
may `enable` `T1190 Exploit Public-Facing Application`; a CVE match alone does
not prove exploitation. Never render an `enables` mapping as “ATT&CK technique
observed.” Use the official [ATT&CK techniques catalog](https://attack.mitre.org/techniques/)
and pin the current release.

## 9. Version, integrity, privacy, and publication controls

### 9.1 Version/change history

Every published report version MUST be immutable and include:

- semantic/document version;
- report UUID and source-record version;
- predecessor/superseding report IDs;
- generated/published time;
- author, reviewer, approver;
- reason and a structured list of changed findings/sections;
- status/count deltas;
- artifact hash/signature; and
- correction versus retest distinction.

An editorial correction does not change finding lifecycle history. A retest is
a new assessment/retest record and normally a new report version. OWASP WSTG
specifically recommends version, change description, date, and author in report
version control
([OWASP WSTG 4.2 Reporting](https://wstg.owasp.org/v4.2/5-Reporting/)).

### 9.2 Integrity and access

- Hash each evidence object and final export; verify hashes on read/export.
- Keep immutable originals and separately hashed redacted derivatives.
- Record access classification and authorized audience on report and evidence.
- Encrypt reports in transit and at rest; use a separate secure delivery channel
  for decryption material.
- Audit evidence/report reads, exports, redactions, state changes, approvals, and
  deletions.
- Retention and legal-hold behavior must come from customer/contract policy.
- A generated report must fail publication if it contains detected credentials,
  secrets, private keys, or prohibited full payment-account data.

These implement the secure storage/transmission expectations in
[NIST SP 800-115](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)
and OWASP's report-security guidance
([OWASP WSTG 4.2](https://wstg.owasp.org/v4.2/5-Reporting/)).

## 10. Licensing, attribution, and representation limits

This is product-risk guidance, not legal advice. Legal review is needed before
shipping copyrighted control text or third-party marks.

| Source | Product implication |
|---|---|
| NIST publications/frameworks | NIST works are generally public-domain U.S. government works, but use official version identifiers and attribution. NIST mappings do not imply endorsement. See each publication's notices, including [SP 800-53](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf). |
| FIRST CVSS | FIRST permits public use subject to its conditions. When publishing CVSS, provide score **and** vector and attribute FIRST; do not alter metric meaning. See [FIRST CVSS data representations](https://www.first.org/cvss/data-representations). |
| ISO/IEC 27001/27002 | ISO standards are copyrighted and the complete text is sold/licensed. Store identifiers, customer-authored summaries, applicability, and links; do not bundle or reproduce control text without appropriate permission. See the official [ISO/IEC 27001 page](https://www.iso.org/standard/27001). |
| PCI DSS | PCI SSC standards/forms are copyrighted and official validation documents have program-specific uses. Use requirement IDs, short original product descriptions, and official links; do not reproduce or modify official forms or imply PCI SSC endorsement. See [PCI SSC policies](https://www.pcisecuritystandards.org/about_us/policies/) and [FAQ 1234](https://www.pcisecuritystandards.org/faqs/1234/). |
| CIS Controls/CAS | The official CAS v8.1 terms use CC BY-NC-ND 4.0: copying/redistribution is authorized for non-commercial purposes with credit and a license link, distributed modifications are prohibited, and commercial use requires prior CIS approval. A commercial Vedha product therefore needs license review/permission before bundling CIS content. Prefer IDs, minimal original summaries, licensed data where needed, and official links. See [CAS 8.1 terms](https://cas.docs.cisecurity.org/en/latest/source/terms-of-use/) and [CIS Controls v8.1](https://www.cisecurity.org/controls/v8-1). |
| OWASP ASVS/WSTG | Both repositories publish CC BY-SA 4.0 licenses. Attribution is required and distributing adapted licensed material can trigger ShareAlike; use stable IDs/links and original Vedha prose unless the product deliberately complies with the license. See [ASVS license](https://github.com/OWASP/ASVS/blob/master/LICENSE.md) and [WSTG license](https://github.com/OWASP/wstg/blob/master/LICENSE). |
| MITRE ATT&CK | MITRE grants a non-exclusive, royalty-free license for research, development, and commercial use. Copies must reproduce MITRE's copyright designation and license; branding must not imply endorsement. Preserve stable IDs/version and the required notice if ATT&CK content is copied. See [MITRE ATT&CK terms](https://attack.mitre.org/resources/terms-of-use/) and [legal/branding guidance](https://attack.mitre.org/resources/legal-and-branding/). |

The lowest-risk default is to store framework owner, version, identifier,
official URL, relationship, and an original Vedha/customer rationale. Avoid
shipping bulk proprietary control text in the product database.

## 11. Validation and acceptance checklist

### 11.1 Per-report publication gate

- [ ] Report/engagement/customer IDs, schema/report versions, status,
      classification, scope, dates, authors/reviewers/approver, and handling
      rules are present.
- [ ] Authorization/rules of engagement, included/excluded assets, vantage,
      credential level, methods, tools/versions, feed/signature versions,
      limitations, and actual coverage are present.
- [ ] Executive totals reconcile exactly with detailed occurrences by severity,
      customer risk, status, and disposition.
- [ ] Every published version has a predecessor/change record and artifact
      SHA-256; published versions are immutable.
- [ ] Every time value is RFC 3339 with `Z`/numeric offset, or is explicitly a
      day-granular deadline.
- [ ] Secrets and prohibited sensitive data scans pass; redactions link to
      restricted originals where retention is allowed.
- [ ] Framework versions and mapping provenance are explicit; the report has a
      non-certification/non-equivalence disclaimer.

### 11.2 Per-finding gate

- [ ] Immutable finding and occurrence IDs, asset identity, description,
      observed/expected condition, affected component, and root cause or
      `unknown` are present.
- [ ] At least one confirmation evidence record has provenance, time, context,
      collector/tool/version, artifact hash, handling/redaction, and reproducible
      validation information.
- [ ] Technical impact, business impact, likelihood/exposure, confidence, and
      customer risk rationale are present.
- [ ] Every displayed CVSS score includes version and vector, source and time;
      CVSS is not mislabeled as customer risk.
- [ ] Remediation gives a target state, actionable steps, dependencies/caveats,
      authoritative reference where available, validation procedure, owner, and
      risk/policy-based due date.
- [ ] Current status is derived from append-only lifecycle events.
- [ ] Risk acceptance/deferral has authority, rationale, residual risk, and
      expiry; false positive has validation evidence and approval; duplicate has
      a canonical reference.
- [ ] Each framework mapping has version, control ID, relationship, rationale,
      evidence/test status, source, mapper, and reviewer.

### 11.3 Closure gate

- [ ] Original finding and before evidence remain visible and immutable.
- [ ] Claimed remediation/change reference is linked.
- [ ] Retest records tester, times, scope, asset, vantage, authentication,
      method, tool/build/feed/configuration, and coverage comparison.
- [ ] After evidence demonstrates the original condition is resolved; simple
      absence from an incomplete or incomparable scan is not accepted.
- [ ] Outcome and residual risk are explicit; partial/inconclusive/failed is not
      rendered as closed.
- [ ] Verifier and verification time are present; close time is not earlier.
- [ ] Any still-open occurrence keeps the aggregate finding open.
- [ ] A later recurrence creates a reopen event rather than deleting closure
      history.

### 11.4 Automated consistency checks

The implementation should reject publication when:

- a summary count differs from its underlying query;
- evidence, mapping, retest, asset, or canonical-duplicate references are
  orphaned;
- `closed_verified` lacks a passed retest and before/after evidence;
- `risk_accepted` or `deferred` lacks authority/expiry;
- a status timestamp violates event order;
- CVSS has a score without vector/version or a vector/score mismatch;
- a framework mapping has no pinned version/rationale/source;
- a test marked `passed`/`failed` lacks defined scope and evidence;
- a report asserts compliance/certification without an authorized assessment
  type, official program/template, and qualified approver; or
- an export's manifest/artifact digest does not verify.

## 12. Customer decisions required before implementation

Research cannot safely choose the following business rules. They should be
confirmed with the user/customer rather than embedded as assumptions:

1. Which assessment types ship first: infrastructure vulnerability assessment,
   web/API penetration test, ASVS verification, PCI support, or all of them.
2. The customer risk matrix/model, acceptable labels, and whether analyst
   override is allowed.
3. Remediation SLA/due-date rules by risk, asset class, environment, and
   applicable regime.
4. Who may accept risk, approve false positives, verify closure, and whether
   independent verification is required above a chosen risk threshold.
5. Evidence retention, deletion, regional storage, classification, and who may
   access restricted originals.
6. Which framework profiles/versions customers can select and whether the
   product will license/import proprietary control catalogs.
7. Whether reports may state formal compliance conclusions, and under which
   assessor qualifications and official templates.
8. Required branding, languages, accessibility level, and customer-specific
   report sections.

Until these are answered, implement the neutral data model and use configurable
policy references; do not hard-code universal SLAs or compliance conclusions.

## 13. Recommended implementation sequence

1. Define versioned JSON schemas for report, finding occurrence, evidence,
   remediation, event, retest, and mapping objects, including validation rules.
2. Make evidence and lifecycle events append-only; migrate current findings
   without inventing missing metadata.
3. Implement the verified-closure gate and retest comparison before adding a
   “Closed” customer badge.
4. Generate executive, technical, retest, and mapping views from the same
   canonical queries; add reconciliation tests.
5. Add framework registry/versioning and reviewed mapping workflow. Start with
   identifiers and official links, not copied proprietary text.
6. Add PDF/HTML/JSON manifests, hashing, redaction, access logging, and secure
   delivery.
7. Add optional OSCAL Assessment Results export and ticketing integrations after
   the internal schema is stable.

## 14. Primary-source register

All substantive recommendations above are traced inline. The core source set is:

- [NIST SP 800-115, Technical Guide to Information Security Testing and Assessment](https://csrc.nist.gov/pubs/sp/800/115/final)
- [NIST OSCAL Assessment Results](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-results/)
- [NIST SP 800-53 Rev. 5, current release](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [NIST Cybersecurity Framework 2.0](https://doi.org/10.6028/NIST.CSWP.29)
- [NIST SP 1347, CSF 2.0 Informative References Quick-Start Guide](https://csrc.nist.gov/pubs/sp/1347/final)
- [FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document)
- [FIRST CVSS v3.1 specification](https://www.first.org/cvss/v3.1/specification-document)
- [CIS Controls v8.1](https://www.cisecurity.org/controls/v8-1)
- [CIS Controls Assessment Specification v8.1, Control 7](https://cas.docs.cisecurity.org/en/latest/source/Controls7/)
- [ISO/IEC 27001:2022 official page](https://www.iso.org/standard/27001)
- [PCI DSS official page and Document Library](https://www.pcisecuritystandards.org/standards/pci-dss/)
- [OWASP ASVS 5.0.0](https://github.com/OWASP/ASVS)
- [OWASP WSTG 4.2 Reporting](https://wstg.owasp.org/v4.2/5-Reporting/)
- [MITRE ATT&CK version history](https://attack.mitre.org/resources/versions/)
- [RFC 3339, Internet timestamps](https://www.rfc-editor.org/info/rfc3339/)

## 15. India and securities-market reporting addendum

**Verification date:** 2026-09-27

This addendum verifies the India-specific claims supplied with the reporting
request. It does not turn a regulator- or program-specific form into a universal
Vedha report requirement. An engagement must carry an explicit, reviewed
applicability profile before Vedha renders a regulatory annexure or applies its
deadlines.

### 15.1 Applicability boundary

| Instrument | Verified scope | Requirement class |
|---|---|---|
| CERT-In *Comprehensive Cyber Security Audit Policy Guidelines*, version 1.0, 25 July 2025 | Guidance for auditee organizations and auditing organizations, including CERT-In-empanelled audit practice. The document uses a mixture of `must`, `required`, `shall`, and `should`; Vedha must preserve that distinction instead of presenting every recommendation as a statutory duty for every Indian customer. | Program/regulatory guidance when the customer's audit basis, contract, or regulator makes it applicable; also a strong source for Vedha's general report profile. |
| SEBI CSCRF, circular `SEBI/HO/ITD-1/ITD_CSC_EXT/P/CIR/2024/113`, 20 August 2024, as clarified | Applies to the categories of SEBI Regulated Entities specified by CSCRF, with category-specific periodicity, reporting authority, audit, and closure rules. | External requirement only for the applicable SEBI-regulated scope. |
| NSE circular `NSE/INSP/74021`, 30 April 2026 | Addressed **to all Application Service Providers (ASPs)** and expressly concerns periodic System, Cyber, and VAPT audits of empaneled ASP vendors. Its Annexures D/E are therefore not a generic form for every SEBI entity. | Exchange/program-specific requirement for the covered NSE ASP population. |

Sources: [CERT-In publication notice](https://www.cert-in.org.in/s2cMainServlet?CACODE=CICA-2025-3411&pageid=PUBADV01),
[CERT-In guidelines PDF](https://www.cert-in.org.in/PDF/Comprehensive_Cyber_Security_Audit_Policy_Guidelines.pdf),
[SEBI CSCRF circular](https://www.sebi.gov.in/legal/circulars/aug-2024/cybersecurity-and-cyber-resilience-framework-cscrf-for-sebi-regulated-entities-res-_85964.html),
and [NSE/INSP/74021](https://nsearchives.nseindia.com/content/circulars/INSP74021.pdf).

Consequently, `India`, `RBI`, `SEBI`, `CERT-In`, and `NSE ASP` cannot be
interchangeable profile names. RBI applicability must be researched against the
customer's precise regulated-entity type and governing RBI instrument before an
RBI pack is implemented; no RBI requirement was inferred in this addendum.

### 15.2 CERT-In July 2025 claim check

| Supplied claim | Verification against the official guideline | Product-safe interpretation |
|---|---|---|
| Use CVSS severity and EPSS likelihood, and map observations to CWE and CVE. | **Confirmed as written.** Sections 16.2 and the definitions require CVSS categorization, EPSS supplementation, and state that every reported observation/vulnerability is mapped to CWE and CVE. | Store CVSS version/vector/source and EPSS score/model date/source. Store CWE/CVE IDs plus mapping status. If no defensible CVE or CWE exists, expose a validation gap or an explicitly reviewed not-applicable reason; never manufacture an identifier merely to satisfy the report. |
| Attach evidence and include evidence for compliant and non-compliant results. | **Confirmed with scope qualification.** Section 18 calls for audit evidence as an appendix to the final report and objective evidence for observations. Its explicit requirement to capture both compliant and non-compliant control evidence is stated for system or compliance audits. | A vulnerability-only report needs finding evidence; a control-assessment report additionally needs positive and negative test results for the assessed control set. Do not infer a passed control from absence of findings. |
| Maintain draft/final versions and each issue date. | **Confirmed.** Section 16.1 requires report versions such as draft/final and each version's issue date to be captured. | Persist immutable report versions and issue history; a live, non-persisted screen is not a final report. |
| Revalidate closure and mark unresolved prior issues as repeat observations. | **Confirmed.** Sections 15.1/15.2 require tracking revalidation, revalidating previous-cycle observations, and carrying unresolved issues as repeat observations. Section 16.3 calls for follow-up audits after remediation. | Add a retest record linked to the prior finding/occurrence and a `repeat_observation_of` relationship; do not clone recurrence as an unrelated finding. |
| Sign-off by the auditors, an independent mid-management reviewer, and the audit-firm head. | **Confirmed.** Sections 9.5 and 16.1 specify signing by declared audit personnel, review/signature by a reviewer outside the audit team from mid-management, authorization/signature by the head of the auditing organization, and an audit certificate signed by the lead auditor and organization head. | Model each signature as a separate role-bound approval with signer identity, organization, independence declaration, time, signature method, and artifact digest. One free-text `approved_by` field is insufficient. |
| Issue the final report only after closure and a production follow-up audit. | **Confirmed with environment qualification.** Section 16.3 says the final audit report follows vulnerability closure and follow-up audit of the application hosted in production; when testing is limited to staging, the report must say production was not tested. | Record the tested environment and production-equivalence limits. A staging-only retest cannot silently become production-verified closure. |
| Notify critical/high findings as they are found. | **Confirmed.** Section 16.3 requires critical/high items to be notified during the audit as found, and section 16.4 requires immediate reporting of defined high-risk conditions. | Add immutable notification/escalation events with recipient, time, severity at notification, channel, acknowledgement, and linked finding; a final-report timestamp cannot prove timely notification. |

The same guideline also requires a comprehensive statement of scope, duration,
methods/standards, tools and manual work, prioritization, sampling, personnel,
exemptions, limitations, and constraints; it calls for artifact hashes, versions,
and timestamps to appear prominently. Those fields belong in document control
and methodology, not only inside finding evidence
([CERT-In guidelines, sections 16 and 18](https://www.cert-in.org.in/PDF/Comprehensive_Cyber_Security_Audit_Policy_Guidelines.pdf)).

### 15.3 SEBI CSCRF and NSE ASP claim check

The supplied Annexure D/E claim is **substantively correct but too broad in
scope**. In [NSE/INSP/74021](https://nsearchives.nseindia.com/content/circulars/INSP74021.pdf):

- Annexure D records the auditing organization, CERT-In empanelment start/end,
  ASP and audit period, assessment-area scope and assets, yes/no compliance,
  auditor comments, not-applicable justification, no-conflict confirmation,
  signatory/contact, place, and date.
- Annexure E records ASP and preferably CISO contact details, VAPT completion
  and management-approval dates, auditor/firm/contact and empanelment-expiry
  details, closed and open counts by `critical`, `high`, `medium`, and `low`, a
  reason for non-closure for each severity, planned closure date, remarks, and
  digital signatures from the ASP and auditor.
- The Annexure E note requires the ATR/compliance report for closure within
  three months after the VAPT report and requires the target date to reflect
  that period. The circular's terms of reference also ask whether time-bound
  VAPT revalidation after closure confirmed that open vulnerabilities were
  fixed.

The wider SEBI CSCRF adds separate cyber-audit rules: the final cyber-audit
report is approved by the relevant IT Committee and submitted within one month
of audit completion; findings are closed within three months using a graded
criticality approach; and the follow-on audit is completed within five months
of audit completion. It also requires 100% critical-system coverage and a
stated sampling method/rationale for 25% of non-critical systems in the cyber
audit. These are not universal vulnerability-SLA defaults
([SEBI CSCRF, sections 4.4 and Annexure D](https://www.sebi.gov.in/sebi_data/attachdocs/aug-2024/1724326790365.pdf)).

A regulatory submission view must be different from the detailed customer
technical report. SEBI's 28 August 2025 clarification says REs submit the VAPT
and cyber-audit **summary** in the prescribed format and do not submit explicit
vulnerabilities unless SEBI asks for them
([SEBI circular `2025/119`, section 6.7](https://www.sebi.gov.in/legal/circulars/aug-2025/technical-clarifications-to-cybersecurity-and-cyber-resilience-framework-cscrf-for-sebi-regulated-entities-res-_96329.html)).
The product must therefore never reuse a detailed evidence-bearing report as
the default SEBI submission artifact.

### 15.4 Exact data-contract changes needed

The core report schema from sections 3-9 remains valid. India-specific support
requires the following typed additions; free-text tags are not enough.

1. `RegulatoryProfile`
   - `profile_id`, regulator/exchange, instrument title, circular/reference
     number, version, issue/effective dates, official source URL;
   - jurisdiction, regulated-entity type/category, exchange/member/ASP status,
     applicability decision, basis, decided by/at, reviewer, and expiry;
   - required annexure/template IDs and data-residency/handling rules.
2. `AuditReportVersion` and `ReportApproval`
   - immutable draft/final version, issue date/time, predecessor, change reason,
     artifact digest, and status;
   - lead auditor, audit-team signers, independent mid-management reviewer,
     organization head, customer IT-committee/management approval where
     applicable, signer role/organization, independence, signed-at, signature
     method, and signed artifact digest.
3. `AssessmentCoverage`
   - environment (`development`, `test`, `UAT`, `pre_production`,
     `production`), assessment areas, assets and criticality, included/excluded
     population, sample size/method/rationale, coverage percentage, manual/tool
     method, tool license/version, personnel, exemptions, constraints, and
     production-equivalence statement.
4. `FindingClassification`
   - CVSS object and EPSS observation with their versions/sources/effective
     dates;
   - CWE and CVE mapping objects with `mapped`, `not_applicable`, or
     `unresolved` state, rationale, mapper/reviewer, and date;
   - regulator risk band separately from customer risk, required notification
     state, closure timeline/basis, prior finding/cycle reference, and
     `repeat_observation` flag.
5. `RegulatoryNotificationEvent`
   - finding, trigger/severity, recipient/authority, sent/acknowledged times,
     channel, sender, content/artifact reference, and delivery status.
6. `ControlTestResult`
   - framework/instrument/version, control or CSCRF standard ID, mandatory or
     non-mandatory status, test procedure, scope, `compliant`, `non_compliant`,
     or `not_applicable`, N/A rationale, evidence IDs, assessor/reviewer, and
     time. This is distinct from a finding-to-control mapping.
7. `NseAspVaptDeclaration` and `NseAspVaptSummary`
   - encode the Annexure D and E fields listed above, including the four-severity
     open/closed matrix, per-severity non-closure reason, planned date, audit
     period, empanelment dates, approval, and digital signatures;
   - link the summary to its detailed report and ATR while excluding technical
     vulnerability details from the regulator submission by default.
8. `ActionTakenReport`
   - original report/finding, initial state, current state, customer and auditor
     comments, remediation action, target and actual closure dates, retest
     result/evidence, validated by, submission due date, submitted-at, and the
     exact policy/circular basis used to calculate the deadline.

### 15.5 Exact report/UI changes needed

- Add a reviewed **Regulatory applicability** step to engagement setup. Show the
  instrument/version, entity category, decision basis, reviewer, and warnings;
  never activate a pack from geography or customer name alone.
- Keep one complete customer report, then generate conditional annexures from
  the same canonical record: CERT-In audit control, SEBI CSCRF, and NSE ASP
  Annexures D/E. Each annexure must display its source instrument and scope.
- Add a **document versions and signatures** page showing every issue and the
  full role-separated sign-off chain. Disable `final` when the selected profile's
  mandatory approvals or closure/retest conditions are unmet.
- Add a **coverage matrix** with environment, assessment area, assets,
  critical/non-critical population, tested sample, method, rationale, and gap.
- On every finding, show CVSS and EPSS provenance, CWE/CVE mapping state,
  required-notification history, target closure basis, prior-cycle link, and a
  visible `Repeat observation` marker.
- Add a **control-test evidence** table for compliant, non-compliant, and N/A
  controls. Keep it separate from the existing finding mapping table.
- Add a dedicated **closure/revalidation register** with before/after evidence,
  production/staging environment, coverage comparison, outcome, verifier,
  time, residual risk, and repeat-observation history.
- For NSE ASP scope, render the exact Annexure E severity matrix and Annexure D
  declaration, plus ATR due/submission status. Offer a regulator-summary export
  that omits explicit findings and evidence; require an explicit authorized
  action to export technical details.
- Show India handling constraints and block a non-conforming delivery route
  when the applicable profile requires audit data/report storage within India.

### 15.6 Current-checkout audit

The regional implementation described in the supplied note is **not present in
this checkout**:

- `manager/backend/app/compliance/packs/` does not exist;
- `manager/backend/app/services/finding_compliance.py` does not exist;
- no backend or frontend `/findings/{id}/obligations` route or obligation model
  is present; and
- those paths also do not appear in the current `HEAD` tree or reachable local
  history checked on 2026-09-27.

The current in-progress canonical report service only reads mapping-like values
already embedded under finding `evidence` keys (`compliance_mappings`,
`framework_mappings`, or `compliance`). It deliberately does not infer missing
controls, which is the safe behavior, but this is not a versioned compliance
registry, reviewed mapping service, obligation engine, or regional pack.
`regulatory_profiles` is currently only a list of strings in engagement rules
of engagement, and the UI renders a generic recorded-mapping roll-up rather
than CERT-In/SEBI/NSE applicability, control tests, signatures, or annexures.

Accordingly, the regional work must begin with the typed applicability and
registry model above. Adding hard-coded strings to the generic compliance array
would reproduce the current reporting weakness and could falsely present a
customer as subject to a regulator or form that does not apply.

### 15.7 India-profile acceptance tests

- With no approved regional profile, no India regulator badge, deadline,
  conclusion, or annexure is emitted.
- A CERT-In-profile report identifies guideline version `1.0 / 25.07.2025`,
  exposes missing CVSS/EPSS/CWE/CVE/signature/retest fields as blockers, and
  never invents an identifier.
- A staging-only retest is visibly staging-only and cannot be labelled as a
  production-verified final report.
- Critical/high notification records retain exact sent and acknowledged times;
  report generation time is not accepted as notification evidence.
- An applicable SEBI CSCRF deadline is derived from the selected instrument and
  entity/audit context, with its policy basis retained; it never becomes the
  default SLA for non-SEBI customers.
- NSE ASP Annexure D/E totals reconcile exactly to the canonical findings and
  ATR, including separate critical/high/medium/low open/closed counts and
  non-closure reasons.
- The default SEBI/NSE regulatory summary contains no explicit vulnerability,
  exploit, request/response, credential, or evidence content.
- Signatures bind to the immutable artifact digest and satisfy the role and
  independence rules of the selected profile.
