# Settings page — research and design

Date: 2026-10-03 · Status: proposal, not implemented (the owner will build it later)
Applies to: `manager/frontend/app/settings/page.tsx` (operator console) and `app/portal/settings` (customer portal), which share `SettingsWorkspace`.

## 1. What the owner asked for

"Do work on setting page — design like an expert and have meaning for each field. Take references from other companies. Document it after research; I'll implement it later."

This document has four parts:

1. An audit of today's page.
2. What leading security and SaaS products do.
3. A proposed structure.
4. A field-by-field specification: what each field means, its default, who may change it, when it takes effect, and whether the backend already supports it.

## 2. Today's page — audit

The operator page has 12 flat sections: Workspace, Team, API Keys, Probe Fleet, AI Runtime, Access & Security, Email, Slack, Jira, SLA Policy, Notifications, Audit Log. The portal shows Plan & Licence, Workspace, Probe Fleet, AI Runtime and Audit Log.

### Defects to fix first

These are wrong today, not just unpolished.

| # | Problem | Where | Why it matters |
| --- | --- | --- | --- |
| D1 | **Notifications "Save" does nothing.** It waits 600 ms and shows "Notification policy saved." Nothing is stored, and the rules reset on reload. | `NotificationsSection`, `save()` | It tells the operator something false. Alerts they think are on are not configured anywhere. |
| D2 | **API keys are always created with `read` + `write` and never expire.** There is no scope picker and no expiry field, although the model already has `scopes`, `expires_at`, `last_used_at` and `revoked_at`. | `ApiKeysSection` | Every automation token has full write access forever. The page's own advice says to grant only the scopes needed and set an expiry. |
| D3 | **AI Runtime describes an old setup.** It shows four static cards (Ollama, OpenRouter, Anthropic, Gemini) and calls Ollama the "recommended production default". Production now runs the automatic fallback chain (ADR-0004): premium → budget → free → local, with cooldowns, spend caps and answer reuse. | `AiRuntimeSection` | The operator cannot see which provider is answering, which ones are cooling down, or how much has been spent today. |
| D4 | **"Access & Security" is a status board, not settings.** It shows reachability, secure cookie and runtime mode, but nothing can be changed. | `AccessSection` | Session length, MFA requirement and IP restrictions are policies an admin expects to set here. |

### Structure problems

- **No split between "my account" and "the organisation".** Changing your own password or MFA has no home. GitHub, Linear, Vercel, Datadog and Snyk all separate personal settings from organisation settings, and settings-UX guidance treats that split as the first rule.
- **Email, Slack and Jira are three top-level sections.** They are the same kind of thing (integrations), and the list will grow (webhooks, Teams, ServiceNow).
- **Scanning has no settings at all.** There are no default intensity, rate limit, blackout windows or global exclusions. Tenable and Rapid7 put these at the centre of their admin areas.
- **Customer and portal defaults have no home.** The new plan locks (Critical + High locked on a POC) are set per customer. The default template for a new POC is a constant in code (`DEFAULT_POC_LOCKED_SEVERITIES`).
- **Fields do not explain themselves consistently.** The integration fields do this well: each has a label, a purpose and an example. The rest of the page does not.

## 3. What leading products do

| Product | Pattern | What Vedha should take from it |
| --- | --- | --- |
| **GitHub** (Primer design system) | Two settings trees: personal (`/settings`) and organisation (`/orgs/x/settings`). A left nav in groups. Destructive actions sit in a red **Danger zone** at the bottom. Fine-grained tokens pick a resource owner and per-permission access. Organisations can **enforce a maximum token lifetime**; the default policy for fine-grained tokens is 366 days. | Split personal and organisation settings. Add a Danger zone. Give tokens scopes, an expiry and an organisation-wide maximum lifetime. |
| **Vercel** | Settings → **Security & Privacy** holds SAML SSO. You can only **enforce** SAML while your own session is SAML-authenticated, so an admin cannot lock themselves out. Editing the SAML configuration turns enforcement off automatically. Token values are shown **once**, at creation. | Lock-out guards on every authentication policy. Show secrets once. |
| **Datadog** | Organisation Settings → **Login Methods** (password, Google, SAML), **maximum session duration** (up to 720 h) and an **IP allowlist** of CIDR ranges under Security. | An authentication-policy page with session lifetime and an IP allowlist. |
| **Stripe** | **Restricted keys**: each resource is None, Read or Write. Secret keys can be **restricted to IP addresses**. | Per-area token scopes, with an optional IP restriction for probe and CI tokens. |
| **Tenable Vulnerability Management** | Settings is a page of **tiles**. **Access Control** groups Users, User Groups, Roles, Permissions and API Access Security. Roles control functions; permissions control data (tags, assets, findings). **Exclusions** block targets by IP, hostname or tag, either always or on a recurring schedule. Scan settings say what each option does and give its default. | Scan exclusions with schedules. Field tables that show the default. Keep roles (what you can do) separate from data access (which engagements). |
| **Rapid7 InsightVM** | **Global scan blackouts**: scheduled scans do not start and running scans pause. A manual scan is blocked with a message, though a Global Administrator can override. **Data retention** is 12 months by default and can be adjusted for audit needs (e.g. PCI). | Blackout windows with an admin override. A data-retention setting. |
| **Snyk** | Admins set **organisation notification defaults** (issue alerts, weekly report, usage alerts). Each user can **override** their own. Changing a default does not change users who already customised theirs. | Two layers of notifications: organisation defaults, then personal overrides. |
| **Salesforce** | Session timeout is chosen from a fixed list; for **portal users** the range is 15 min – 24 h. A warning pop-up appears before timeout. | Separate session limits for customer-portal users and operators. Warn before signing someone out. |
| **Checkmarx One** | IP restrictions are a toggle that opens CIDR rows. The admin role is **exempt** so it cannot be locked out. | An IP allowlist with a lock-out exemption. |
| Settings-UX guides (Eleken, Setproduct) | Group related options under labelled sections. Plain-word labels with one line of helper text. Scope settings by role so people only see what applies to them. Make saves visible. Set risky actions apart. Settings pages keep growing, so revisit the structure. | The field specification in section 5 follows these rules. |

Sources:
- docs.github.com: PAT management; organisation PAT policy
- primer.style: layout
- vercel.com/docs/saml; vercel.com/docs/accounts/access-tokens
- docs.datadoghq.com/account_management/org_settings (and its IP allowlist page)
- docs.stripe.com/keys/restricted-api-keys; docs.stripe.com/keys-best-practices
- docs.tenable.com/vulnerability-management: Access Control, Permissions, Exclusions, Scans
- docs.rapid7.com/insightvm/scan-blackouts; Rapid7 InsightVM console best practices
- docs.snyk.io: manage notifications
- help.salesforce.com: session security settings
- docs.checkmarx.com: general settings
- eleken.co: settings page UI; setproduct.com: settings UI design

## 4. Design principles for Vedha's settings

1. **Three scopes, always labelled:**
   - **Your account**: only affects you.
   - **Organisation**: affects everyone in this Vedha tenant.
   - **System**: read-only facts about the deployment.

   Every page header says which scope it belongs to.
2. **Every field answers five questions** in its helper text or info popover:
   - What does it do, in plain words?
   - What is the default?
   - Who can change it?
   - When does a change take effect?
   - What is the risk of changing it?
3. **Say where a value comes from.** A setting stored in the database is editable. A setting from the server environment (`.env` or the secret store) shows a **"Set on the server"** badge, its current value (never a secret), and the variable name to change. Do not show a disabled input with no explanation.
4. **Secrets are write-only.** Show "Configured · last changed 12 Sep" and a Replace button. Never show the value again, except a token's value once, at creation.
5. **Save model:**
   - Each section has one **Save changes** bar that appears only when something has changed, with Discard next to it.
   - Toggles that take effect immediately say so ("Saved").
   - Never show "Saved" unless the server confirmed it (see D1).
6. **Lock-out guards:**
   - Requiring MFA, shortening sessions, or adding an IP allowlist checks that the person saving would still be allowed in. Otherwise the save is refused with the reason.
   - An admin account is always exempt from the IP allowlist (Checkmarx pattern), and the page says so.
7. **Risky changes ask for confirmation in words**, e.g. "This signs out 14 people now." Destructive actions live in a **Danger zone** at the bottom of the page they affect.
8. **Every change is audited** with who, what, old value → new value, and when. The Audit log can filter to settings changes only.
9. **Test buttons** for anything that talks to the outside: send a test email, a test Slack message, a test Jira issue, a test AI call down the chain.
10. **Search** across settings (a ⌘K filter on field labels and helper text), because the page will keep growing.
11. **The portal sees only customer-relevant settings**, worded for a customer, not an operator.

## 5. Proposed structure and field specification

Columns in the tables below:
- **Who** is the minimum role that can change the field: admin, manager, or any user (self).
- **Effect** is when a change applies.
- **Backend today**:
  - ✅ editable now
  - ⚙️ server environment only (needs a database-backed setting to become editable)
  - 🧱 data model exists, no UI or API
  - ➕ new

### Navigation (operator console)

```
YOUR ACCOUNT
  Profile
  Sign-in & security
  My notifications
  My API tokens
ORGANISATION
  General
  Team & roles
  Authentication policy
  API tokens (all)
  Audit log
SCANNING
  Scan defaults
  Blackouts & exclusions
  Probe fleet
FINDINGS & REMEDIATION
  SLA policy
  Risk & verification
  Compliance
CUSTOMERS & PORTAL
  New-customer defaults
  Portal experience
AI
  Provider chain
  Spending & data handling
INTEGRATIONS
  Email · Slack · Jira · Webhooks
NOTIFICATIONS
  Organisation rules
SYSTEM
  Deployment health
  Version & licence
  Intel bundles
```

On a phone the left nav becomes a grouped list. Opening a page shows it with a Back link, the same pattern as iOS Settings and GitHub mobile.

### 5.1 Your account

**Profile**

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Email | Your sign-in name and where your notifications go. Changing it needs your current password. | from invite | self | next sign-in | 🧱 (`users.email`, no self-service API) |
| Display name | How your name appears in comments, audit entries and reports you approve. | email prefix | self | immediately | ➕ |
| Time zone | How times are shown to you. Stored times stay exact; only the display changes. | organisation time zone (IST) | self | immediately | ➕ (organisation-wide `VEDHA_TZ` exists) |

**Sign-in & security**

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Password | Change your password. Needs the current one. Shows when it expires, if the organisation sets expiry. | — | self | immediately; other sessions are signed out | 🧱 (`password_expires_at`) |
| Two-step verification (MFA) | A second check at sign-in with an authenticator app. Shows **Required by your organisation** when policy enforces it. | off | self | next sign-in | 🧱 (`users.mfa_enabled`; enrolment flow ➕) |
| Active sessions | Where you are signed in: device, IP, last active. **Sign out** any of them, or all others. | — | self | immediately | ➕ (refresh-token store exists, no listing) |

**My notifications.** This is your personal override of the organisation rules, the Snyk pattern. Each event row offers *Use organisation default*, *Email*, *Slack DM* or *Off*. ➕

**My API tokens.** The same table as section 5.2 "API tokens", filtered to tokens you own.

### 5.2 Organisation

**General**

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Organisation name | Shown in the console header, on reports and in emails to customers. | tenant name | admin | immediately | 🧱 (`tenants.name`) |
| Default time zone | Used for times in reports, emails and scan schedules, unless a user picks their own. | Asia/Kolkata (IST) | admin | immediately | ⚙️ `VEDHA_TZ` |
| Report logo & colour | Your brand on exported PDF, Word and Excel reports and the customer portal header. | Vedha | admin | next export | ➕ |
| Data retention | How long raw scan results are kept. Findings and their history are kept regardless. Shorter saves storage; longer helps audits (PCI asks for 12 months). | 12 months | admin | nightly clean-up | ➕ |

**Team & roles.** A table with columns user · role · MFA · last sign-in · status, plus Invite, Change role, Deactivate.

The page explains each role in one line:
- **Admin**: everything, including settings.
- **Manager**: engagements, customers and approvals.
- **Tester**: runs scans and validates findings.
- **Analyst**: triages findings.
- **Auditor**: read-only, including the audit log.
- **Client**: customer portal only.

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Role | What this person can do. Changing your own role is not allowed, and the last admin cannot be demoted. | — | admin | next request | 🧱 (role enum; role-change API ➕) |
| Active | Deactivated people cannot sign in, and their tokens stop working. History is kept. | on | admin | immediately | ✅ |

**Authentication policy.** Every change here runs the lock-out check in section 4, principle 6.

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Require MFA for operators | Operators without MFA must set it up at their next sign-in. | off (recommend on) | admin | next sign-in | ➕ |
| Require MFA for customers | The same, for portal users. | off | admin | next sign-in | ➕ |
| Operator session length | How long a sign-in lasts before you must sign in again. Shorter is safer on shared machines. | 7 days (refresh) / 15 min (access) | admin | new sessions | ⚙️ `REFRESH_TOKEN_EXPIRE_DAYS`, `ACCESS_TOKEN_EXPIRE_MINUTES` |
| Idle sign-out | Sign out after this long with no activity. Warns one minute before. | 8 hours | admin | immediately | ➕ |
| Customer session length | Separate limit for portal users (Salesforce allows 15 min – 24 h). | 12 hours | admin | new sessions | ➕ |
| Password expiry | Force a password change every N days. Current guidance (NIST SP 800-63B) is **not** to expire passwords without a reason; offer it for customers whose policy demands it. | never | admin | at next expiry | 🧱 (`password_expires_at`) |
| IP allowlist | Only these address ranges (CIDR) can reach the console. Admins are always exempt so they cannot be locked out. Portal users are not affected unless *Apply to portal* is on. | empty (off) | admin | immediately | ➕ |
| Trusted proxies | Which load balancers may pass on the client's real IP. Rate limits and the allowlist depend on it. | private ranges | admin | restart | ⚙️ `TRUSTED_PROXY_CIDRS` |

**API tokens (all).** A table with columns name · owner · scopes · created · expires · last used · status. It shows a warning chip for tokens unused for 90 days or more, and for tokens with no expiry.

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Name | What the token is for, e.g. "Probe – Pune DC" or "CI pipeline". Shown in the audit log. | — | owner | — | ✅ |
| Scopes | What the token can do, per area: Findings, Scans, Engagements, Reports, Probes. Each is None, Read or Write (the Stripe pattern). Probe tokens get only the probe scope. | Read (all areas) | owner | immediately | 🧱 (`scopes` column; UI sends read+write, see D2) |
| Expires | 7, 30, 90 or 365 days, or custom. "Never" only if the organisation policy allows it. | 90 days | owner | — | 🧱 (`expires_at`) |
| Maximum token lifetime (policy) | The longest expiry anyone may choose (GitHub enforces 366 days by default). | 365 days | admin | new tokens | ➕ |
| Revoke | Stops the token now. It cannot be undone; create a new one. | — | owner / admin | immediately | ✅ |

**Audit log.** Filters for person, action type (settings / access / scans / findings / AI), date and engagement. Export to CSV. A **Verify integrity** button calls `/audit/verify` (✅ exists).

### 5.3 Scanning

**Scan defaults**

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Default intensity | The preset used when someone starts a scan without choosing: Stealth, Normal, Aggressive or Deep. Explain each in one line: speed, noise and what each finds. | Normal | manager | next scan | ➕ (launcher sends intensity per scan) |
| Packets per second cap | The upper limit on the scan rate, whatever the preset. Protects fragile networks. | per preset | admin | next scan | ➕ |
| Concurrent scan jobs | How many jobs can run at once in this organisation. More is faster but loads the probes. | 3 | admin | next queue check | ⚙️ (hard-coded cap) |
| Fragile-asset protection | Hosts tagged fragile (OT, printers, legacy) are never scanned at Aggressive or Deep. | on | admin | next scan | 🧱 (guard exists) |
| Verification after scan | Re-check findings after a scan to mark them Verified or Unverified. Off makes every finding Unverified. | on | admin | next run | ⚙️ `VERIFICATION_ENABLED` |

**Blackouts & exclusions** (Tenable exclusions plus Rapid7 blackouts)

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Blackout windows | Times when no scan may start, e.g. month-end close or a change freeze. Running scans pause and resume afterwards. Each window has a name, time zone, start, duration and repeat (once, daily, weekly, monthly). | none | admin | immediately | ➕ |
| Admin override | Whether an admin can still start a manual scan during a blackout. The scan is marked "override" in the audit log. | on | admin | immediately | ➕ |
| Global exclusions | Addresses, ranges, hostnames or tags that are never scanned for any customer, e.g. your own management network. Always on, or on a schedule. | none | admin | next scan | ➕ (per-engagement scope exists) |

**Probe fleet.** The current list (host, version, status, last seen, capabilities), plus:
- Auto-enrol (⚙️ `PROBE_AUTO_ENROLL`, off), with the meaning: "New probes from these networks join without approval".
- Auto-enrol networks (⚙️ `PROBE_AUTO_ENROLL_CIDRS`).
- Retire probe, in the Danger zone.

### 5.4 Findings & remediation

**SLA policy** (✅ exists)

Keep the current page, which shows hours per severity and a "custom" badge. Add:
- each value in days as well as hours ("72 h · 3 days")
- the sentence "Due dates are counted from when a finding is first seen. Changing this recalculates open findings' due dates."
- the defaults: Critical 24 h, High 72 h, Medium 7 days, Low 30 days, Info no SLA

**Risk & verification**

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Raise known-exploited (KEV) findings | Findings on CISA's Known Exploited Vulnerabilities list move up one priority level. | on | admin | next detection run | 🧱 (KEV join exists) |
| EPSS threshold | Findings whose exploit-prediction score is above this are treated as urgent. | 0.5 | admin | next detection run | ➕ |
| Auto-close after clean re-scan | A finding not seen in N consecutive scans of the same scope is marked Remediated. See ADR-0002: this must stay off until scope matching is proven. | off | admin | next run | ➕ (deliberately) |

**Compliance.** Regional packs (India, EU, UK, US, Middle East, APAC), with the explanation "which regulations' obligations are mapped onto findings". The default region applies to new engagements. 🧱

### 5.5 Customers & portal

**New-customer defaults.** This is the template for a new customer's plan. Each customer can still be changed at any time in their Plan panel.

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| POC length | How long a new proof-of-concept lasts. | 14 days | manager | new customers | ➕ |
| POC scan allowances | Scans of each type a POC may run: Stealth, Normal, Aggressive, Deep. | as today | manager | new customers | ➕ (per customer ✅) |
| Locked severities on a POC | Findings of these severities show only as "N locked findings". Their details stay hidden until a licence is granted. | Critical, High | manager | new customers | ➕ (constant `DEFAULT_POC_LOCKED_SEVERITIES`; per customer ✅) |
| Locked features on a POC | Which of AI assistant, Reports, Remediation & fix bundles and Compliance briefs a POC cannot open. | none | manager | new customers | ➕ (per customer ✅) |

**Portal experience**

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Customer AI assistant | Lets customers ask security questions about their own findings. Answers are labelled "AI, not reviewed". | on | admin | immediately | ✅ (per customer via plan locks) |
| Portal sign-in address | The customer-specific sign-in link (`/p/<slug>`). | generated | manager | immediately | 🧱 (`portal_slug`) |
| Support contact | The name and email shown on lock panels ("Contact your security team…"). | organisation email | manager | immediately | ➕ |

### 5.6 AI

**Provider chain.** Mostly read-only status, because the chain is set on the server. It replaces the four static cards (D3).

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Chain order | The order providers are tried: premium, then budget, then free, then local. Each row shows provider · model · tier · state (healthy / cooling down until 14:20 / blocked: key invalid / probing) · today's calls. | auto-detected | — (server) | — | ⚙️ `LLM_CHAIN` |
| Test the chain | Sends one small request and shows which provider answered and how long it took. | — | admin | — | ➕ (status endpoint ✅) |
| Strict quality floor | When on, tasks that need a premium model fail rather than fall back to a weaker one. When off, they fall back and the answer is labelled. | off | — (server) | — | ⚙️ `AI_STRICT_QUALITY_FLOOR` |

**Spending & data handling**

| Field | What it means | Default | Who | Effect | Backend today |
| --- | --- | --- | --- | --- | --- |
| Daily spend cap | Once paid providers have cost this much today, Vedha uses free and local models until midnight. Shows today's spend against the cap. | none | — (server) | immediately | ⚙️ `AI_DAILY_CAP_USD` |
| Pseudonymise for free models | Replaces hostnames, IPs and customer names with placeholders before sending to free (non-contracted) providers. | off (recommend on) | — (server) | next call | ⚙️ `AI_PSEUDONYMIZE` |
| Deployment profile | Cloud, hybrid or sovereign. Sovereign never sends data outside your network: local models only. | cloud | — (server) | restart | ⚙️ `DEPLOYMENT_PROFILE` |
| Answer reuse | How long an identical question reuses a saved answer instead of calling a model again. | 7 days | — (server) | — | ⚙️ `AI_ANSWER_CACHE_TTL_SECONDS` |

### 5.7 Integrations

Use one page with a card per integration: Email, Slack, Jira and, later, Webhooks. Each card shows a status (Not set up / Working / Last test failed: reason), a **Send test** button and the fields.

Keep today's field definitions; they already explain purpose and give an example. Add:
- "Last delivered" on each card
- an **Enabled** switch with the meaning "Turning this off keeps the settings but stops all messages"

Backend: ✅ (`/integrations`, `/integrations/test`).

### 5.8 Notifications — organisation rules

Fixes D1. Use a matrix: rows are events, columns are channels, plus a **Recipients** field per event.

| Event | Default channels | Meaning |
| --- | --- | --- |
| New Critical or High finding | Email, Slack | Sent once per finding when it first appears. |
| SLA breach | Email | A finding has passed its due date without being fixed. |
| SLA due in 24 h | Email | A daily digest of findings about to breach. |
| Scan finished / failed | Slack | Includes the scan reference (SCN-…) and a link. |
| Report approved | Email | Goes to the engagement's customer contacts as well. |
| Probe offline > 15 min | Email, Slack | A probe stopped checking in. |
| New probe enrolled | Slack | Security-relevant: confirm it was expected. |
| Customer requested a scan | Email | Portal scan requests waiting for approval. |
| AI spend cap reached | Email | Paid models are paused until midnight. |

Each user can override these in *My notifications*. Changing an organisation default does not overwrite a user who already chose their own (the Snyk rule). Backend: ➕ (store rules plus an event dispatcher; the outbox model exists).

### 5.9 System (read-only)

- **Deployment health**: what Access & Security shows today (API, secure cookie, environment), plus database, Redis, worker heartbeat and last migration.
- **Version & licence**: the `VERSION` file and the licence holder and expiry.
- **Intel bundles**: last KEV/EPSS update and its signature status.

### 5.10 Customer portal settings

Customers see four pages:
1. **Plan & licence**: today's page.
2. **Sign-in & security**: password, MFA, sessions.
3. **My notifications**: which emails I get.
4. **Activity**: their own audit trail.

Probe Fleet and AI Runtime are operator topics. Replace them with:
- a one-line "Your probe: online · last seen 2 min ago" on Plan & licence
- nothing about AI providers

## 6. Field anatomy (component spec)

Each setting row has this anatomy:

```
Label                                         [control]
One sentence: what it does, in plain words.
Default: 72 hours · Changes apply to new findings and recalculate open ones.
[Set on the server: ACCESS_TOKEN_EXPIRE_MINUTES]   ← only for env-backed values
```

- The label uses sentence case and nouns ("Idle sign-out", not "Enable idle sign-out?").
- Helper text is at most about 20 words. Longer detail goes in an ⓘ popover.
- Errors appear under the field and say how to fix the problem ("Enter a range like 10.0.0.0/8").
- Each section has a sticky save bar showing "2 unsaved changes · Discard · Save changes".
- Risky saves open a confirm dialog that names the effect.

## 7. Suggested build order (when the owner implements)

1. Fix **D1** (persist notification rules, or remove the fake save) and **D2** (scopes and expiry on tokens). Small changes, real risk today.
2. Split **Your account** from **Organisation**. Move Email, Slack and Jira into **Integrations**.
3. Replace AI Runtime with the live **Provider chain** status (D3).
4. **Authentication policy** (MFA requirement, session lengths, IP allowlist) with lock-out guards.
5. **Scanning**: defaults, blackouts and exclusions.
6. **New-customer defaults**, which moves the POC lock template out of code.
7. Make server-only settings editable where it is safe (database-backed with the environment value as the fallback). Keep secrets and `DEPLOYMENT_PROFILE` server-only.
