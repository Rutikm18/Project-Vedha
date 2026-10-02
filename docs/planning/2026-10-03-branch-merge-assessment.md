# Branch merge assessment — what is on the integration branch, what is not, and why

Date: 2026-10-03 · Integration branch: `integrate/agent-install-to-main` (based on `origin/main`)

## 1. What `origin/main` was missing, and where it went

| Source | Commits | Result |
|---|---|---|
| `origin/main` (other sessions' deploy / install / responsive fixes) | base | the base of the integration branch |
| local `main` (STATUS doc, single-asset Deep scan, ws-ssl) | 4 | merged; the ws-ssl fix is the same fix `origin/main` already had under a different hash |
| `feat/agent-install` (P0-3: distribution, tokens, expiry, closure-only build, docs) | 27 | merged |
| `docs/agent-install-approach` | 3 | already inside `feat/agent-install` |
| `feat/technical-finding-report` (standalone Technical Findings report page, 14 files, 3 test files) | 5 | **merged**: additive, frontend only, only `VERSION` conflicted; tsc, lint and its tests pass |
| `feat/reporting-boardroom-redesign` (spec + plan, 2 docs files) | 3 | **merged**: docs only; `STATUS.md` / `VERSION` conflicts resolved to ours |

Conflicts resolved: `VERSION` (kept the highest), `Makefile` (union of `.PHONY`), and
`probe/agent/transport.py`, where `origin/main` and `feat/agent-install` had each fixed the
WebSocket TLS context. Merged into one helper: certifi on top of the system store by default
(the macOS fix), only the CA bundle when one is given (matches httpx), verify-off mirrored,
mTLS client certificate loaded.

Tests on the integrated code: backend 2,234 · probe 2,512 · frontend 366 of 368 (the 2 failures are
the `pdfkit` package that is not installed, unrelated to any branch).

## 2. Branches that are NOT merged

### 2.1 `origin/codex/customer-portal-engagement-parity` — not merged, on purpose

One commit, `f1cbdd4 "AI architecture enhancement"` (27 Sep), 228 commits behind `main`.

**A literal merge is unsafe.** A trial merge conflicts in **52 files**, and about half are
"both added": `main` already carries independently ported copies of the report-document code
(`report_document.py`, `CanonicalReportDocument.tsx`, `report-document.ts`, the renderer tests...)
and the finding-provenance work. Resolving by hand would mostly mean choosing between a newer ported
version and an older original, with nothing to tell which is right.

**Already in `main` from this commit** (do not port again):

- Migrations 0038 / 0039 → ported as **0050 / 0051** (the Codex ids collide with `main`'s own 0038 / 0039).
- The canonical report document, report export and scan provenance.

**Genuinely missing (about 18 new files, plus edits):**

| Piece | What it is | Files |
|---|---|---|
| Remediation workspace | Deterministic, **non-executing** generator of reviewed fix scripts (bash / PowerShell) for batches of findings, grouped by asset and platform, from a small versioned operation catalog; every artifact is hashed; an optional AI "advisory" is attached afterwards and can never change an artifact byte | `app/ai/remediation_workspace.py` (1,013 lines), `app/services/remediation_workspace_context.py`, route `POST /findings/remediation-workspaces/preview`, schemas, `RemediationWorkspaceDialog.tsx`, `lib/remediation-workspace.ts`, BFF preview route, 3 backend + 4 frontend test files |
| AI recommendation agent hardening | A bounded-context builder and an allow-list of target pairs for AI recommendations (`app/ai/agent.py`, 489 → 788 lines) | `agent.py`, `test_agent_ai.py`, `test_ai_route_rbac.py` |
| Model picker | Browser-side provider / model selection | `lib/ai-model-selection.ts` and its test. **You already decided against this** |

**Is it important to merge? My assessment: not now.**

- `main` already ships remediation guidance per rule, OS-aware recipes, fix bundles, AI refine and
  publish. The workspace is an *additional* capability (ready-to-review fix scripts), not a gap in
  the core assessment-to-remediation flow.
- It generates executable content for customers' production systems. That is exactly where an
  unreviewed port is most dangerous: the safety comes from the operation catalog and its tests
  (the module rejects any command string that is not from the catalog). A hurried merge of a
  conflicted 1,000-line module is the wrong way to adopt it.
- The agent-hardening part (target allow-list) is worthwhile security hygiene, but it only matters if
  AI output drives scan targets; check that first.
- It touches the AI router, remediation router and finding schemas, all of which changed a lot on
  `main` since (AI fallback chain, contextual remediation).

**If you do it from Codex, do it this way** (smallest safe path):

1. Branch from `integrate/agent-install-to-main` (or `main` once it lands), not from the Codex branch.
2. Port the **new files** only; take no changes to `main.py`, models or existing routers except the
   one new route and its schema.
3. Migrations: `main`'s head is **0053**. Number anything new from **0054**. Do not bring 0038 / 0039.
4. Skip `ai-model-selection.ts` (declined) and the model parameters in the routes.
5. Adapt the optional advisory to `main`'s AI gateway and fallback chain (ADR-0004), not Codex's
   provider wiring.
6. Bring its tests with it and run the whole backend suite. The catalog's rejection tests are the
   safety net.
7. Port the agent hardening as a separate, second change.

### 2.2 Other branches

| Branch | State | Action |
|---|---|---|
| `probe-standalone` | unrelated history | **never merge** (recorded earlier) |
| `fix/probe-ws-ssl`, `docs/aws-*`, `fix/install-*`, `fix/caddy-frontend-health`, `fix/build-image-race`, `feat/make-admin-creds` | already on `origin/main` (their commits are the 10 on `origin/main`) | nothing to merge |
| `integration/all-branches`, `testing/all-features`, `feat/aggressive-enterprise`, `fix/*` older, `spike/probe-go`, `cross-os-*`, `codex/customer-portal-parity` and the rest | 0 commits ahead of `main`: already merged or superseded | can be deleted when you tidy (needs your approval; deleting branches is blocked for me) |

## 3. Landing it

The primary checkout (`main`) has uncommitted changes in `.gitignore`, `VERSION`,
`docs/deployment/aws-deployment.md` and a deleted `probe copy`, all of which this merge also
touches, so nothing was merged into that checkout. Publish the branch directly:

```
git push origin integrate/agent-install-to-main:main
```

Afterwards, in the primary checkout: commit or stash your changes, then `git pull`.
Local `main` itself is left alone (it is a strict subset of the integration branch).
