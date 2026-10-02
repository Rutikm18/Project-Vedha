# Portal plan locks — design

Date: 2026-10-02 · Status: proposed (awaiting owner approval)

## What the owner asked for

- A POC customer sees **Medium and Low findings in full**; **Critical and High are locked** by default.
- A locked finding shows as a **teaser**: its severity and a lock — "Available on a licensed plan". Its title, host, evidence and fix never reach the browser.
- Per customer, at any time, the operator can change which severities are locked and lock or unlock four features: **AI assistant, Reports, Remediation & fix bundles, Compliance briefs**.
- The same controls exist on **licensed** plans (e.g. a 14-day licensed trial with major features locked).
- Customers who already have access keep it until the operator changes their locks. New POC customers start with Critical + High locked.
- With Reports on, locked findings **stay locked inside reports** too.

## Settings (per customer, on the existing plan record)

| Setting | Type | Default for a new POC | Default for a new licensed plan | Existing customers |
| --- | --- | --- | --- | --- |
| `locked_severities` | list of `critical` / `high` / `medium` / `low` / `info` | `critical`, `high` | none | none (unchanged access) |
| `locked_features` | list of `ai_assistant` / `reports` / `remediation` / `compliance` | none | none | none |

One migration (`0052`) adds both as JSONB columns defaulting to `[]`. The operator edits them in the customer's Plan panel on the main dashboard; the change takes effect on the customer's next request.

## Enforcement — one guard, not twenty route patches

The portal has about 20 routes that return finding data, and the workspace routes reuse the operator's handlers. Patching each one invites a leak. Instead:

1. `require_client` (every portal request already passes through it) loads the customer's locks and sets a request-scoped context value.
2. A SQLAlchemy `do_orm_execute` hook adds `severity NOT IN locked` to every query that **loads finding rows or sensitive finding columns** while that context value is set. Delegated operator handlers, fix bundles, the AI assistant's context and data-driven reports all inherit it.
3. Aggregate queries that read only counts by severity stay unfiltered, so the customer still sees how many Critical and High findings exist.
4. A dedicated `GET /portal/findings/locked` returns only `{severity: count}` for the locked findings, which feeds the teaser rows.
5. A direct request for a locked finding (detail, events, remediation, compliance brief, status change) returns **403 "This finding is available on a licensed plan."**

Operator requests never set the context value, so nothing changes for operators.

## Features

| Feature | When locked | When open but severities are locked |
| --- | --- | --- |
| AI assistant | `POST /portal/assistant/chat` → 403 with the plan message; portal shows a lock panel | Answers only from open findings (the guard filters its context) |
| Reports | Report routes → 403; Reports section shows a lock panel | Data-driven report views show locked findings as teaser rows. Approved **written** reports are free text and cannot be redacted per finding, so they are withheld while any severity is locked ("Full written reports are available on a licensed plan") |
| Remediation & fix bundles | Remediation routes and the tracker export → 403; lock panel | Bundles and the export cover open findings only |
| Compliance briefs | Obligations and compliance-brief routes → 403; lock panel | Available for open findings only |

## Known gaps (owner's choice, recorded)

- **Raw scan evidence** (scan job results, raw facts) has no lock. Those results contain service banners for every host, so a technical customer could infer what a locked finding is about.
- **Posture and analytics** scores are computed from the findings the customer can see. The portal will say so ("Scores cover the findings available on your plan").

## Tests

- The guard: a locked Critical never appears in any portal finding list, group, asset view, compare, bundle, export or assistant context; operator queries are unaffected.
- A direct read of a locked finding → 403 on every per-finding route.
- Feature locks → 403 with the plan message on each route.
- Teaser counts are correct, and change as soon as the operator edits the locks.
- Defaults: new POC = Critical + High locked; new licensed = nothing; existing rows = nothing.
