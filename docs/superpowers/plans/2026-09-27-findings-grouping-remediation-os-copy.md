# Findings: auto-OS remediation, working copy buttons, grouped findings — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** (1) The remediation plan picks the target platform from what Vedha already knows about the asset — no OS dropdown in the common case. (2) Every copy button works, including on plain-HTTP deployments. (3) Findings that are the same issue are grouped so the operator can prioritise one fix instead of scrolling N near-identical rows.

**Branch:** `feat/findings-grouping-os-copy` (shared checkout — stage explicit paths only).

---

## Root causes (verified before planning)

### 1. "I have to select the OS"
- `RemediationPlanView` (`frontend/app/findings/page.tsx:827-918`) defaults the dropdown from `finding.assetContext.os` **only**. When that single column is empty it falls to `"generic"` and the operator must pick.
- The backend already has a better, evidence-backed detector: `app/intel/tagging.py::_os_family` reads the asset OS string (confidence 0.85) **and** service banners (e.g. `Microsoft-IIS`, `OpenSSH … Ubuntu`, confidence 0.6). The remediation route never used it — it trusts `?os=` blindly (default `generic`).
- Accuracy trap: the KB's `linux` commands are `apt`/`systemctl`. BSD and network OSes must map to **generic**, not linux.

### 2. "Copy button not working"
- All six copy sites call `navigator.clipboard.writeText` directly:
  `app/findings/page.tsx:353` (remediation/evidence), `app/settings/page.tsx:203`, `app/fleet/page.tsx:172`, `app/customers/page.tsx:151`, `components/assistant/AdvisorFlow.tsx:35`, `components/report/FindingReport.tsx:73`.
- `navigator.clipboard` **only exists in secure contexts** (HTTPS or localhost). The testing deploy (`make aws-up`, no TLS, `http://<ip>`) is not secure → `navigator.clipboard` is `undefined` → the click throws a `TypeError` and silently does nothing (three sites have no failure feedback at all).

### 3. "Lots of findings seem duplicate"
- Findings are deduped per `(engagement, asset, title)` — they are *not* literal duplicates, they are **one issue × many rows**:
  - CVE track: **one row per CVE per host** (`engine_bridge.py:708`, title `"CVE-… — openssh"`). One outdated OpenSSH on 10 hosts → hundreds of rows, all fixed by one upgrade.
  - Posture track: title is `"<rule title> (port N)"` (`engine_bridge.py:_posture_title`) → same rule × every port × every host.
  - Seed data shows the same shape: 3× "SMB signing not required", 3× "Weak TLS 1.0", 3× "Outdated OpenSSH 7.4" on different assets.
- The list is **paginated server-side** (20/page), so grouping must be computed server-side — client-side grouping of one page would report wrong counts.

---

## Architecture

- **Remediation OS**: new pure resolver `app/services/remediation_os.py` built on the existing tagging rule (single OS-detection source of truth). Remediation GET/POST (operator + portal) accept `os=auto` (new default); the response carries a `platform` block saying what was resolved and *why* (source + evidence). UI shows a platform chip; an override is available behind "Change", never required.
- **Copy**: one shared `lib/clipboard.ts::copyText()` — async Clipboard API when available in a secure context, otherwise a hidden-textarea `execCommand("copy")` fallback; returns `boolean` so every site can show honest success/failure.
- **Grouping**: pure `app/services/finding_groups.py` computes a deterministic group identity per finding (rule → vulnerable product → CVE set → normalised title) and aggregates. New `GET /findings/groups` (+ portal `/workspace/findings/groups`) applies **exactly the same filters** as `GET /findings` via an extracted shared filter helper. UI gets a "Grouped | All findings" view toggle; a group row expands to its member findings, each opening the existing detail panel.

**Tech stack:** FastAPI + SQLAlchemy 2 async (backend), Next.js App Router + TanStack Query (frontend), pytest, `tsx --test`.

## Global constraints

- Never guess: every auto-detected platform states its source; unknown → `generic` with "not detected" (no silent linux default).
- BSD / network OS → `generic` (Linux commands would be wrong).
- Group view must apply *identical* filters to the list (shared helper, not a copy).
- Portal parity: every new operator endpoint gets a portal delegate pinned to `assert_client(user)`.
- Existing explicit `?os=linux|windows|macos|generic` behaviour and existing tests stay unchanged.
- No DB migration.

---

## File map

| File | Change | Responsibility |
|---|---|---|
| `backend/app/intel/tagging.py` | modify | expose `os_family_tag(facts)` (public wrapper of `_os_family`) |
| `backend/app/services/remediation_os.py` | create | pure `resolve_platform(asset, services)` + async `resolve_finding_platform(db, finding)` |
| `backend/app/schemas/remediation.py` | modify | `RemediationPlatformOut`, optional `platform` on `RemediationPlanOut` |
| `backend/app/routers/remediation.py` | modify | `os=auto` default on GET/POST, platform in response |
| `backend/app/routers/portal.py` | modify | same for portal remediation; `/workspace/findings/groups` delegate |
| `backend/app/services/finding_groups.py` | create | pure group identity + aggregation + priority order |
| `backend/app/routers/findings.py` | modify | extract `_filtered_findings(...)`; add `GET /findings/groups` |
| `backend/app/schemas/finding_groups.py` | create | response models |
| `backend/tests/test_remediation_os.py` | create | resolver tests |
| `backend/tests/test_finding_groups.py` | create | grouping tests |
| `backend/tests/test_findings_groups_route.py` | create | route/filter-parity tests |
| `frontend/lib/clipboard.ts` | create | `copyText()` with fallback |
| 6 copy call sites | modify | use `copyText` + failure feedback |
| `frontend/app/api/findings/[id]/remediation/route.ts` | modify | allow + default `auto` |
| `frontend/lib/findings-query.ts` | create | shared BFF filter → backend query mapping |
| `frontend/app/api/findings/route.ts` | modify | use shared mapping (behaviour-preserving) |
| `frontend/app/api/findings/groups/route.ts` | create | BFF proxy for groups |
| `frontend/lib/adapters.ts` | modify | `mapFindingGroupPage` |
| `frontend/lib/findings-workspace-api.ts` | modify | `groups()` on both surfaces |
| `frontend/app/findings/page.tsx` | modify | auto-platform chip; view toggle; `FindingGroupRow` |
| `frontend/tests/clipboard.test.ts`, `frontend/tests/finding-groups.test.ts` | create | unit tests |

---

### Task 1: Shared clipboard helper + fix all copy buttons

**Files:** Create `frontend/lib/clipboard.ts`, `frontend/tests/clipboard.test.ts`; modify the six call sites listed above.

**Produces:** `copyText(text: string): Promise<boolean>`

- [ ] **Step 1: failing test** `frontend/tests/clipboard.test.ts` — installs fake `window`/`navigator`/`document` globals and asserts:
  1. secure context + working `navigator.clipboard` → uses it, returns `true`, no textarea created;
  2. **insecure context (`isSecureContext=false`, `navigator.clipboard` undefined)** → textarea fallback runs `execCommand("copy")`, returns `true`, textarea removed afterwards;
  3. Clipboard API rejects (permission denied) → falls back, returns fallback result;
  4. both paths fail → returns `false` (never throws).
- [ ] **Step 2:** `cd manager/frontend && npx tsx --test tests/clipboard.test.ts` → FAIL (module missing).
- [ ] **Step 3: implement** `lib/clipboard.ts`:

```ts
/**
 * copyText — clipboard write that works on every origin Vedha is served from.
 * navigator.clipboard only exists in secure contexts (HTTPS / localhost); the
 * plain-HTTP deploy has none, so every button that called it directly threw and
 * did nothing. Falls back to a hidden textarea + execCommand("copy").
 * Resolves true only when a copy actually happened; never throws.
 */
export async function copyText(text: string): Promise<boolean> {
  if (typeof window === "undefined" || typeof document === "undefined") return false;
  const clip = typeof navigator !== "undefined" ? navigator.clipboard : undefined;
  if (window.isSecureContext && clip?.writeText) {
    try {
      await clip.writeText(text);
      return true;
    } catch {
      // Permission denied / document not focused — try the legacy path.
    }
  }
  return legacyCopy(text);
}

function legacyCopy(text: string): boolean {
  const active = document.activeElement as HTMLElement | null;
  // Inside a modal with a focus trap the textarea must live in the dialog or
  // focus() is stolen back and nothing is selected.
  const host = (active?.closest?.("[role='dialog']") as HTMLElement | null) ?? document.body;
  const area = document.createElement("textarea");
  area.value = text;
  area.setAttribute("readonly", "");
  area.setAttribute("aria-hidden", "true");
  Object.assign(area.style, { position: "fixed", top: "0", left: "0", opacity: "0", pointerEvents: "none" });
  host.appendChild(area);
  let ok = false;
  try {
    area.focus();
    area.select();
    area.setSelectionRange(0, text.length);
    ok = document.execCommand("copy");
  } catch {
    ok = false;
  } finally {
    host.removeChild(area);
    active?.focus?.();
  }
  return ok;
}
```

- [ ] **Step 4:** test passes.
- [ ] **Step 5: replace every call site** (keep each component's existing UI; add failure feedback where missing):
  - `app/findings/page.tsx` `CopyBtn`: `setState((await copyText(text)) ? "copied" : "failed")`.
  - `app/settings/page.tsx` `CopyBtn`: `void copyText(text).then((ok) => { if (ok) {setDone(true); …} else toast/feedback })` — settings has no toast in scope → add `failed` state showing "Copy failed" title.
  - `app/fleet/page.tsx`: `void copyText(cmd).then((ok) => ok ? toast.success("Command copied") : toast.error("Copy failed — select the command and copy it manually"))`.
  - `app/customers/page.tsx`: same pattern with its toasts.
  - `components/assistant/AdvisorFlow.tsx`, `components/report/FindingReport.tsx`: set done only on `ok`; aria-label "Copy failed" otherwise.
- [ ] **Step 6:** `grep -rn "navigator.clipboard" app components lib` → only `lib/clipboard.ts`. Add that grep as an assertion in `clipboard.test.ts` (source-scan, repo convention like `findings-detail-layout.test.ts`) so a future direct call fails CI.
- [ ] **Step 7:** `npx tsc --noEmit -p .` and `npm test` green. Commit `fix(ui): copy buttons work on non-HTTPS origins (shared copyText fallback)`.

---

### Task 2: Backend platform resolver

**Files:** modify `backend/app/intel/tagging.py`; create `backend/app/services/remediation_os.py`, `backend/tests/test_remediation_os.py`.

**Produces:**
```python
@dataclass(frozen=True)
class PlatformResolution:
    os: str            # KB key: linux | windows | macos | generic
    family: str | None # windows | linux | macos | bsd | network_os | None
    source: str        # manual_tag | asset_os | service_banner | not_detected | no_asset | requested
    evidence: str | None
    confidence: float | None
    def to_dict(self) -> dict: ...

def resolve_platform(asset, services) -> PlatformResolution            # pure
async def resolve_finding_platform(db, finding) -> PlatformResolution  # loads asset + services
```

Resolution order (first hit wins):
1. **Manual `os_family` tag** on `asset.tags["manual"]` (operator said so) → confidence 1.0, source `manual_tag`.
2. **`os_family_tag(facts_from_records(asset, services))`** — asset OS string (`asset_os`, 0.85) else service banner (`service_banner`, 0.6).
3. Nothing → `generic`, source `not_detected`. No asset on the finding → `no_asset`.

Family → KB key: `windows→windows`, `linux→linux`, `macos→macos`, `bsd→generic`, `network_os→generic`.

- [ ] **Step 1: failing tests** covering: `os="Windows Server 2019"` → windows/asset_os/0.85; `os="Ubuntu 22.04"` → linux; `os="Mac OS X 13"` → macos; `os=None` + banner `Microsoft-IIS/10.0` → windows/service_banner/0.6 with evidence naming the port; `os=None` + `OpenSSH_8.2p1 Ubuntu-4ubuntu0.5` → linux; `os="FreeBSD 13"` → os `generic`, family `bsd`; `os="Cisco IOS XE"` → generic/network_os; manual tag `{"key":"os_family","value":"linux"}` beats `os="Windows"`; nothing → generic/not_detected; asset `None` → generic/no_asset; async `resolve_finding_platform` with `finding.asset_id=None` makes **zero** DB calls.
- [ ] **Step 2:** `cd manager/backend && .venv/bin/python -m pytest tests/test_remediation_os.py -q` → FAIL.
- [ ] **Step 3:** add to `tagging.py`:

```python
def os_family_tag(facts: AssetFacts) -> Tag | None:
    """The single os_family tag the evidence supports, or None. Public so the
    remediation planner resolves platforms with the SAME rule the tags use."""
    return next(iter(_os_family(facts)), None)
```

and implement `remediation_os.py` (pure resolver + async loader that selects `Asset` scoped by `engagement_id` and its `Service` rows).
- [ ] **Step 4:** tests pass. Commit `feat(remediation): evidence-based platform resolver`.

---

### Task 3: Remediation routes use `os=auto`

**Files:** modify `backend/app/schemas/remediation.py`, `backend/app/routers/remediation.py`, `backend/app/routers/portal.py`; extend `backend/tests/test_remediation_routes.py`, `backend/tests/test_portal_remediation.py`.

**Consumes:** Task 2. **Produces:** response field `platform: {requested, os, family, source, evidence, confidence}`.

```python
class RemediationPlatformOut(BaseModel):
    requested: str            # "auto" or the explicit os the caller asked for
    os: str                   # KB key actually served
    family: str | None = None
    source: str
    evidence: str | None = None
    confidence: float | None = None
```

Route change (operator GET, POST and portal GET), shared helper in `remediation_os.py`:

```python
async def platform_for_request(db, finding, requested: str | None) -> PlatformResolution:
    if (requested or "auto").strip().lower() == "auto":
        return await resolve_finding_platform(db, finding)
    key = os_key(requested)
    return PlatformResolution(os=key, family=None, source="requested", evidence=None, confidence=None)
```

`Query(default="auto")`; cache lookup / generation keyed by `platform.os` (unchanged cache semantics — the cache key is still a KB OS).

- [ ] **Step 1: failing tests**: GET with `os="auto"` on a finding whose asset has `os="Windows 10"` serves `os == "windows"`, `platform.source == "asset_os"`; explicit `os="linux"` still issues exactly the queries it did before (existing tests untouched) and returns `platform.source == "requested"`; portal GET with `auto` resolves the same way.
- [ ] **Step 2–4:** run → fail → implement → pass: `pytest tests/test_remediation_routes.py tests/test_portal_remediation.py tests/test_remediation_os.py -q`.
- [ ] **Step 5:** BFF `frontend/app/api/findings/[id]/remediation/route.ts`: `SUPPORTED_OS` gains `"auto"`, default `"auto"`.
- [ ] **Step 6:** Commit `feat(remediation): auto-detect target platform from asset evidence`.

---

### Task 4: Remediation UI — platform chip, no required dropdown

**Files:** modify `frontend/app/findings/page.tsx` (`RemediationPlanView`, types, CSS).

- Delete `remediationOsFor` (the backend is now the single resolver).
- `const [override, setOverride] = useState<RemediationOs | null>(null); const requested = override ?? "auto";` query key `[…, finding.id, requested]`.
- Header shows, instead of the `<select>`:
  - detected: **"Windows"** chip + "Detected from asset OS “Windows Server 2019”" / "…from tcp/443 banner" / "Set by an operator tag".
  - not detected: "Platform not detected — showing platform-neutral steps".
  - `family` bsd/network_os: "FreeBSD/network device — vendor-neutral steps (Linux commands would not apply)".
  - A small "Change" button reveals the select (options: Auto-detect, Linux, Windows, macOS, Generic). Choosing Auto-detect clears the override.
- Types: `RemediationPlanResponse.platform?: {requested; os; family; source; evidence; confidence}`.
- [ ] Update `tests/findings-detail-layout.test.ts` source assertions if they referenced the old select; add assertion that the remediation request uses `"auto"` by default.
- [ ] `npx tsc --noEmit`, `npm test`. Commit `feat(findings): remediation plan auto-selects the asset's platform`.

---

### Task 5: Pure grouping engine

**Files:** create `backend/app/services/finding_groups.py`, `backend/tests/test_finding_groups.py`.

**Produces:**
```python
@dataclass(frozen=True)
class GroupRow:  # one finding, lean columns only
    id: uuid.UUID; title: str; severity: str; status: str
    cvss: float | None; risk: float; epss: float | None
    cve_ids: tuple[str, ...]; asset_id: uuid.UUID | None
    asset_ip: str | None; asset_hostname: str | None
    port: int | None; rule_id: str | None; cpe: str | None
    kev: bool; exploit_validated: bool
    first_seen: datetime | None; last_seen: datetime | None

def group_identity(row: GroupRow) -> tuple[str, str, str]   # (key, kind, label)
def build_groups(rows: Iterable[GroupRow], *, member_cap: int = 100) -> list[dict]
```

Identity (first applicable, deterministic):
1. `rule_id` present → kind `rule`, key `rule:<rule_id lower>`, label = title with trailing `(port N)` removed. *Same posture rule, any port, any host.*
2. `cve_ids` and a parseable CPE 2.3 → kind `product`, key `product:<vendor>:<product>:<version>` (version omitted when `*`/`-`/empty), label `"<Product> <version> — known vulnerabilities"`. *Same vulnerable product/version = same upgrade fixes all its CVE rows.* Different versions stay separate groups (different CVE sets — accuracy over compression).
3. `cve_ids` without CPE → kind `cve`, key `cve:` + sorted upper-case CVE list.
4. Otherwise → kind `title`, key `title:` + normalised title (port suffix stripped, lower-cased, whitespace collapsed).

Aggregate per group: `finding_count`, `open_count` (open|confirmed), `severity` (max), `severity_counts`, `host_count` (distinct asset ids; findings without an asset counted once as "unassigned"), `hosts` (≤8 `{ip, hostname}`), `ports` (sorted, ≤12), `cve_count` + `cves` (≤8, sorted), `max_risk`, `max_cvss`, `max_epss`, `kev`, `exploit_validated`, `first_seen` (min), `last_seen` (max), `status_counts`, `members` (sorted severity→risk desc, capped at `member_cap`, `members_truncated`).

Priority order (mirrors the list's "critical always on top"): groups with open findings first → severity tier → KEV → exploit validated → max risk → open count → host count → label.

- [ ] **Step 1: failing tests**: the seed shape (3 hosts × "SMB signing not required", no evidence) → 1 group, `host_count == 3`; posture rule on ports 139 and 445 of one host + another host → 1 group, `ports == [139, 445]`, `host_count == 2`; 3 CVEs × 2 hosts on `cpe:2.3:a:openbsd:openssh:7.4:*…` → 1 `product` group, `cve_count == 3`, `finding_count == 6`; OpenSSH 7.4 vs 8.2 → 2 groups; CVE rows without CPE group by CVE; ordering: an all-remediated critical group sorts after an open medium group; a critical sorts above a KEV high; member cap truncation flag; titles differing only by case/whitespace/port suffix share a group.
- [ ] **Step 2–4:** fail → implement → pass (`pytest tests/test_finding_groups.py -q`).
- [ ] **Step 5:** Commit `feat(findings): deterministic similar-finding grouping engine`.

---

### Task 6: `GET /findings/groups` with identical filters (+ portal)

**Files:** modify `backend/app/routers/findings.py`, `backend/app/routers/portal.py`; create `backend/app/schemas/finding_groups.py`, `backend/tests/test_findings_groups_route.py`.

- Extract from `list_findings` the whole filter block into
  `async def _filtered_findings(q, db, current_user, *, severity, status_filter, active_only, asset_id, asset_ip, mitre_technique, engagement_id, agent_id, scan, search, detection_status, exploit_validated, verification_state, needs_review, sla_breached) -> tuple[Select | None, set[uuid.UUID] | None]`
  (returns `None` query when a scan filter matched no run → caller returns empty). `list_findings` calls it with `select(Finding)` — **pure refactor, existing tests prove no behaviour change**.
- `GET /findings/groups` (declared before `/{finding_id}`): same filter params + `page`, `page_size (≤100)`. Selects lean columns only (`Finding.evidence["rule_id"].astext`, `["port"]`, `["cpe"]`, `["kev"]`, `["enrichment"]["kev"]`), capped at 25 000 rows with `truncated` flag; asset ip/hostname loaded in one follow-up query for the distinct asset ids (no join → no clash with the `asset_ip` filter's join). Returns `{items, total, page, page_size, pages, finding_total, truncated}`.
- Portal `GET /workspace/findings/groups` delegates with `engagement_id=assert_client(user)`.
- [ ] **Tests:** compiled-SQL capture (pattern from `test_findings_scan_filter.py`) proves the groups query carries the tenant scope, severity/status/search/scan filters exactly as `list_findings`; unknown scan → empty page without a findings query; route registered before `/{finding_id}` (GET `/findings/groups` is not parsed as a UUID); portal delegate passes the pinned engagement.
- [ ] Full `pytest tests/ -q -k "finding or remediation or portal"` green. Commit `feat(findings): /findings/groups endpoint with list-parity filters`.

---

### Task 7: Frontend grouped view

**Files:** create `frontend/lib/findings-query.ts`, `frontend/app/api/findings/groups/route.ts`, `frontend/tests/finding-groups.test.ts`; modify `frontend/app/api/findings/route.ts`, `frontend/lib/adapters.ts`, `frontend/lib/findings-workspace-api.ts`, `frontend/app/findings/page.tsx`.

- `findings-query.ts::backendFindingFilters(url: URL)` — the sanitisation currently inline in the list route (severity enum, status map, IP regex, scan, flags, verification). List route switches to it unchanged; groups route reuses it (+ page/page_size).
- `adapters.ts::mapFindingGroupPage(api)` → camelCase `FindingGroup` with severity via `SEV_TO_UI`, members as `{id, title, severity, status, assetIp, assetHostname, port, cveIds, risk}`.
- `findings-workspace-api.ts`: `groups: (query) => …` for manager (`/api/findings/groups?…`) and portal (`/workspace/findings/groups?…` then `mapFindingGroupPage`).
- `page.tsx`:
  - View toggle "Grouped | All findings" beside the filters (`aria-pressed`), default **Grouped**, remembered per browser in `localStorage` (wrapped in try/catch).
  - Grouped view runs the groups query with the **same `queryString` filters** (own page counter), renders `FindingGroupRow`: severity badge, label, kind chip ("Same check" / "Same vulnerable product" / "Same CVE" / "Same title"), "N findings · M hosts · ports …", CVE count, KEV / exploit chips, max CVSS, open-vs-total, a one-line "One fix closes N findings on M hosts". Expand → member list; clicking a member opens the existing detail panel (`toggleFinding(id)`; `detailQuery` already loads findings not on the current page).
  - "+K more — switch to All findings filtered to this group" when `membersTruncated`.
- [ ] **Tests:** adapter mapping (snake→camel, severity mapping, truncation flag); source assertions that the grouped view passes the shared filter query string.
- [ ] `npx tsc --noEmit`, `npm run lint`, `npm test`. Commit `feat(findings): grouped view — similar findings collapse into prioritised groups`.

---

### Task 8: End-to-end verification

- [ ] Backend: `pytest tests/ -q` full suite green.
- [ ] Frontend: typecheck, lint, tests green.
- [ ] Live check against a running stack: groups endpoint on seed data returns 4 groups for the 10 seed findings (OpenSSH ×3, SMB ×3, TLS ×3, RDP ×1) in priority order; remediation `?os=auto` on a Windows-OS asset returns `windows`; copy works when the page is served over plain `http://<LAN-IP>` (non-secure context).
- [ ] `graphify update .`; update memory.

## Self-review

- Spec coverage: OS auto (Tasks 2–4), copy everywhere (Task 1, grep guard), grouping for prioritisation (Tasks 5–7), accuracy (verification Task 8, BSD/network → generic, versions kept separate, identical filters via shared helper).
- Names consistent: `copyText`, `PlatformResolution`, `resolve_platform`, `resolve_finding_platform`, `platform_for_request`, `os_family_tag`, `GroupRow`, `group_identity`, `build_groups`, `_filtered_findings`, `backendFindingFilters`, `mapFindingGroupPage`, `FindingGroupRow`.
