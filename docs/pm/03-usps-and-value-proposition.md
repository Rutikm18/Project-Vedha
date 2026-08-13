# 03 · USPs & Value Proposition

> A USP earns the name only if it (a) maps to a pain a buyer will pay to remove, (b) is **hard for
> incumbents to copy**, and (c) is **true in the shipping product**. Each USP below is graded on
> those three. "Sell this" lines are ready for a deck / homepage / cold email.

## Positioning statement (the canonical form)

> **For** MSSPs, security consultancies, and data-sovereign / OT security teams
> **who** must run vulnerability assessment inside networks they don't fully control,
> **Vedha** is an agentic network VA platform
> **that** keeps the vulnerability database out of the client network, makes every finding
> anti-false-positive by construction, and re-detects new CVEs without re-scanning —
> **unlike** Nessus/Qualys/Rapid7, whose scanner *is* the database and whose findings you have to
> re-scan to refresh and hand-triage to trust.

## Messaging pillars (the 3 things to repeat everywhere)

1. **Trust the deployment.** The intelligence never enters the client's network.
2. **Trust the findings.** Anti-false-positive by construction; prove it with a number.
3. **Trust the answer, fast.** Re-detect and re-prioritize without touching the network again.

---

## The USP portfolio

### USP-1 — The vulnerability DB never enters the client network
- **Pain killed:** can't/won't place a scanning appliance + CVE database inside a client, OT, or
  regulated segment.
- **Why hard to copy:** incumbents' scanners *carry* the DB; changing that is a re-architecture.
- **True today?** ✅ Probe is dial-out-only, no inbound ports, holds no vuln DB (`ARCHITECTURE.md`).
- **Sell this:** *"Deploy a probe that dials out only — no inbound ports, no database, nothing in
  your client's network worth stealing. The brains stay in your cloud."*

### USP-2 — Re-detect against today's CVEs without re-scanning
- **Pain killed:** a new critical CVE means re-scanning every network, tonight.
- **Why hard to copy:** requires storing *raw facts* and separating collection from detection —
  Vedha's core split.
- **True today?** ✅ Probe ships raw facts; detection re-runs against the pinned DB. *(Note: the
  append-only `scan_results` store is scoped but partly deferred — see doc 04 #6; land it to make
  this bulletproof at scale.)*
- **Sell this:** *"New CVE at 9am? Re-run detection across every past scan by 9:15 — zero new
  packets, every client answered before lunch."*

### USP-3 — Findings are anti-false-positive *by construction*
- **Pain killed:** scanners cry wolf; analysts stop trusting them; triage eats the week.
- **Why hard to copy:** it's a *pipeline philosophy* (calibrated confidence + evidence tier + audit
  of checks + N-run Wilson-CI consistency; the verifier only ever *lowers* certainty), not a toggle.
- **True today?** ✅ Detection P3 verifier + P5 consistency; recent `verification`/`active-validation`
  commits add verdicts + FP-triage.
- **Sell this:** *"Every finding carries a calibrated confidence, its evidence, and a cross-run
  stability score. We never inflate certainty — only lower it. Fewer apologies, more fixes."*
- **⚠️ Do this:** back it with a published precision/recall number (doc 04 #5). A claim becomes a
  weapon the moment it's a metric.

### USP-4 — Explainable 0–1000 risk rank, KEV/EPSS-aware
- **Pain killed:** "which of my thousands of findings actually matter?"
- **Why hard to copy:** partly (everyone has a risk score) — differentiator is **explainability**.
- **True today?** ✅ `risk_rank` 0–1000, explainable, on the findings API (recent commits).
- **Sell this:** *"Not a black-box severity — a 0–1000 rank that shows its work: exploited-in-the-wild
  (KEV), exploit probability (EPSS), and evidence. Fix what's actually exploitable first."*

### USP-5 — Posture & patch-comparison scorecard (board-ready)
- **Pain killed:** "are we getting better?" has no clean answer; board reporting is manual.
- **True today?** ✅ `GET /analytics/posture`; Risk Index / Exploitable Score / Posture grade;
  patch-comparison matrix; mirrored into generated reports.
- **Sell this:** *"Show the board a grade that moves. See exactly which vulns got patched between
  runs — proof the program works, generated, not hand-built."*

### USP-6 — Structurally passive OT profile
- **Pain killed:** active scanning crashing industrial devices.
- **Why hard to copy:** it's enforced at both probe and manager, not a checkbox.
- **True today?** ✅ `ot` profile is passive-only on both ends.
- **Sell this:** *"OT mode can't fire an active packet — it's passive by construction, enforced at
  the probe and the manager. Visibility without touching the plant floor."*

### USP-7 — Local-first, self-hostable, data-sovereign AI
- **Pain killed:** "I won't send my asset+vuln inventory — or my findings — to a vendor's cloud/LLM."
- **True today?** ✅ Self-hostable manager; AI inference local-first (Ollama) with OpenRouter/Anthropic
  optional; keys never touch the frontend.
- **Sell this:** *"Run it in your cloud, on your model. Your vulnerabilities never leave your
  perimeter — not even to the AI."*

### USP-8 — Built multi-tenant for delivery, not retrofitted
- **Pain killed:** serving many clients on a single-tenant tool doesn't scale.
- **True today?** ✅ Multi-tenant, engagement model, per-engagement customer portal (WIP).
- **Sell this:** *"One platform, every client isolated, each with their own portal, report, and SLA.
  Onboard a client in an afternoon."*

---

## Objection handling (say the quiet part first)

| Objection | Honest, disarming response |
|---|---|
| *"You don't do authenticated scanning."* | "Correct today — and by design we won't store target credentials in a job. Authenticated collection ships via an ephemeral secret broker (no secret ever persisted). Roadmap item #1." *(Don't hide it — the design is the credibility.)* |
| *"Nobody's heard of Vedha."* | "Right — so we bring receipts: a published precision/recall benchmark and a probe you can deploy and kill in ten minutes. Judge the tool, not the logo." |
| *"Why not just Nessus?"* | "If you're one enterprise scanning your own network, Nessus is fine. If you're placing scanners in networks you don't own, refreshing against new CVEs constantly, and drowning in false positives — that's the architecture we built for and they didn't." |
| *"Is 'agentic' just a buzzword here?"* | "The probe is a real autonomous agent: register → poll → scope-check → scan → durably submit, with dynamic routing and per-target failure isolation. The word earns its keep." |
| *"Coverage — web apps? cloud?"* | "We're network/infra VA done right, not a do-everything suite. We integrate rather than pretend. If unified web+cloud is your #1 need, we're honest that we're not it — yet." |

## The elevator pitch (30 seconds)

> "Vedha is network vulnerability assessment built for the people who scan networks they don't own —
> MSSPs, consultants, OT teams. The probe dials out only and carries no database, so the intelligence
> never enters the client's network. Every finding is anti-false-positive by construction — calibrated
> confidence, evidence, cross-run stability — so your analysts stop triaging noise. And because we
> store the raw facts, a new CVE means *re-detect*, not *re-scan*. It's the VA engine an MSSP can run
> across a hundred clients."

## What NOT to lead with (positioning discipline)

- ❌ "Agentic AI platform" — vague; earns skepticism, not a demo.
- ❌ "13 scanners" — feature-listing; incumbents have more. Lead with the *architecture outcome*.
- ❌ Competing on coverage breadth — you lose that comparison today. Compete on **trust boundary,
  false-positive discipline, and re-detection** — the three things they *can't* easily match.
