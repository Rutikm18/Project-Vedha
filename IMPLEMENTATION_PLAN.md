# Implementation Plan — for the follow-up (cheaper-model) session

Three parts: **(A) new theme**, **(B) probe-file import → findings + attack graph**,
**(C) backend verification**. Decisions are made; steps are mechanical. Reuse
existing code wherever noted — most of B already exists.

> Stack is healthy now: api `:18080` 200, frontend `:3000` 200. Skill installed at
> `~/.claude/skills/ui-ux-pro-max-skill` (remote = the GitHub repo, pulled latest).

---

## PART A — New theme: "crazy, modern, very simple but good"

### The design decision (color theory)
The current theme is blue-cyan "Adversa Ops". The new look uses the **60-30-10 rule**:
60% warm near-black, 30% elevated zinc surfaces, **10% ONE electric-violet accent**.
That single saturated hue against restrained neutrals is what reads "modern + premium +
striking" (the Linear/Vercel/Raycast formula) while staying *simple*. Bold via
**contrast + one accent + strong type**, NOT via clutter or many colors.

**Rules:** keep semantic severity colors (red/amber — accessibility, never recolor them).
All changes are TOKENS in one file → every component inherits, so this is low-risk.

### Files
1. `manager/frontend/app/globals.css` — replace the token VALUES below (keep names).
2. Font import (top of globals.css or layout) — add **Space Grotesk** (display).

### Token changes (old → new) in `:root[data-theme="dark"]`
```css
/* Backgrounds — warm near-black (was blue-black). Premium OLED feel. */
--bg-root:    #08080A;
--bg-app:     #0B0B0E;
--bg-panel:   #131316;
--bg-sidebar: #0E0E11;
--bg-surface: #1A1A1F;
--bg-hover:   #222228;
--bg-active:  #2A2A32;

/* Accent — electric indigo-violet (the 10% hero). Replaces cyan. */
--accent:        #7C6CFF;
--accent-hover:  #9D8CFF;
--accent-ghost:  rgba(124,108,255,0.12);
--accent-glow:   rgba(124,108,255,0.45);

/* Text — zinc scale (clean, modern, high-contrast) */
--text-primary:   #FAFAFA;
--text-secondary: #A1A1AA;
--text-muted:     #71717A;

/* Borders — very subtle */
--border-subtle:  #1C1C20;
--border-default: #27272A;
--border-strong:  #3F3F46;
--border-accent:  #7C6CFF;

/* KEEP severity colors as-is (accessibility): --sev-critical-* red,
   --sev-high-* amber, --sev-medium-* etc. Do NOT change these. */
```

### Fonts
```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
```
Use Space Grotesk for big numbers/section titles (`--font-display`), Inter for body,
JetBrains Mono for data/metrics (already used). Add a `--font-display: 'Space Grotesk'`
token and apply to KPI numbers + PageShell title.

### Steps
1. Edit the token values above in `globals.css`. Add the font import + `--font-display`.
2. In `components/dashboard/LiveOverview.tsx` and `PageShell`, set big numbers to
   `fontFamily: "var(--font-display)"` (optional polish).
3. Rebuild: `docker compose build frontend && docker compose up -d --no-build frontend`.
4. Verify `:3000` → 200, eyeball contrast (text ≥ 4.5:1 — the zinc scale satisfies this).

### Pre-delivery checks (from the skill)
No emoji icons (use lucide — already), focus rings visible, hover transitions 150–300ms
(tokens already define `--dur-*`), reduced-motion respected, test at 375/768/1024/1440.

---

## PART B — Import a probe-output file → findings + attack graph

### The big insight (minimal new code)
This **reuses P3-#10 + the existing graph builder**:
- `ScanResult` model + `run_detection_job` (facts→findings) already exist.
- `_promote_assets` (hosts→assets) already exists in `routers/agents.py`.
- `GET /engagements/{id}/attack-graph` already builds the graph from the findings/assets
  in the DB (`app/graph/builder.py` `build_asset_graph`). **No graph code needed** — once
  findings/assets exist, the graph endpoint just works.

So the only NEW code is: an upload endpoint that parses the file and feeds the existing pipeline.

### File format DECISION
**Primary: `.json` bundle** (self-describing, one file, easy to validate):
```json
{
  "engine": "scanner_module",
  "scan_type": "assessment",
  "generated_at": "2026-06-26T00:00:00Z",
  "facts": [ { "scanner":"ssh_inventory","target":"10.0.0.7","port":22,"proto":"tcp",
               "status":"observed","data":{...},"timestamp":"...","evidence":"...","error":null } ]
}
```
**Also accept `.jsonl`** (one ScanResult fact per line — the probe's native streaming format,
better for huge scans). The endpoint detects: if the body parses as a JSON object with a
`facts` array → bundle; else treat each line as a fact.

> Why `.json` over CSV/XML: the facts are already JSON (ScanResult), detection_engine
> ingests JSON natively, and a bundle carries provenance (engine, scan_type, time). Zero
> lossy conversion.

### B1. Probe side — export the bundle
`agent.engine.run_scan(...)` already RETURNS `{engine, scan_type, facts, host_count, ...}`
— that IS the bundle. Just write it to a file.
- Add to `probe/dev.sh`: `./dev.sh export <ip> <out.json>` → runs `run_scan` and
  `json.dump`s the result to `out.json`.
- (Optional) a `probe/agent/export.py` CLI: `python3 -m agent.export -t <ip> -s scope.txt -o scan.json`.

### B2. Backend — new import endpoint (the only real new code)
New: `POST /engagements/{engagement_id}/scans/import-facts` in `routers/engagements.py`
(or a small new router). Skeleton:
```python
@router.post("/{engagement_id}/scans/import-facts", status_code=202,
             summary="Import a probe scan file (.json bundle or .jsonl) → detection + graph")
async def import_facts(engagement_id, db: DB,
                       current_user: Annotated[AuthUser, require_role(["admin","manager","tester"])],
                       background_tasks: BackgroundTasks,
                       file: UploadFile = File(...)):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    raw = (await file.read()).decode("utf-8", "replace")
    facts, scan_type = _parse_probe_file(raw)        # bundle OR jsonl  (write this helper)
    if not facts:
        raise HTTPException(400, "No facts found in file.")
    # store durably (P3-#10) + feed the SAME pipeline the live probe path uses
    db.add(ScanResult(engagement_id=engagement_id, job_id=None,
                      scan_type=scan_type, fact_count=len(facts), facts=facts))
    await db.flush()
    result = {"facts": facts, "scan_type": scan_type, "engine": "scanner_module"}
    # promote hosts → assets (so the graph has nodes), then detect (facts → findings)
    background_tasks.add_task(run_detection_job, engagement_id, result)
    # NOTE: _promote_assets needs result['hosts']; facts use ScanResult shape, so also
    # derive assets from facts (host = fact['target']). Add a tiny _promote_from_facts(db, eng, facts).
    return {"imported": True, "fact_count": len(facts),
            "next": f"/engagements/{engagement_id}/attack-graph"}
```
Helpers to write:
- `_parse_probe_file(raw) -> (facts, scan_type)`: `json.loads`; if dict with `facts` → bundle;
  else split lines, `json.loads` each.
- `_promote_from_facts(db, engagement_id, facts)`: for each distinct `fact['target']`, upsert
  an `Asset` (mirror `_promote_assets` but from the ScanResult shape). Needed so the attack
  graph has asset nodes. (Findings already link by `asset_ip`.)

### B3. Frontend — upload UI
- On the engagement detail page (`app/engagements/[id]/`), add an "Import scan file" button →
  `<input type=file accept=".json,.jsonl">` → POST multipart to a BFF route.
- New BFF route `app/api/engagements/[id]/import-facts/route.ts` → `backend(... multipart ...)`.
- After upload: toast "Imported N facts — detection running", then poll
  `/api/findings?engagement_id=` + the attack-graph view refreshes.

### B4. Validation
1. `./dev.sh export 127.0.0.1 /tmp/scan.json` (or craft a bundle with a vulnerable apache fact).
2. `curl -F file=@/tmp/scan.json -H "Authorization: Bearer $TOKEN" .../engagements/$EID/scans/import-facts`
3. Findings appear (`/findings?engagement_id=$EID` > 0), assets created.
4. `GET /engagements/$EID/attack-graph` returns nodes/edges (graph built from imported data).

---

## PART C — Backend verification (confirm "works proper")

Current state is GOOD (validated this session): P1/P2/P3 done, api+frontend 200,
21 live integration tests + detection accuracy pass. To re-verify after A/B:
1. `docker compose ps` → all healthy.
2. `make test` → backend unit suite (222 tests; needs `manager/backend/.venv`; pytest is
   NOT in the prod image by design).
3. Re-run the connectivity/auth/function battery (see this session's test block) → expect all green.
4. New for Part B: the B4 validation above (import → findings → graph).
5. `/metrics` (P2) exposes request histograms; `/health` green.

---

## Execution order (token-efficient for the cheaper model)
1. **Part A** first (isolated to globals.css + one rebuild — fast, visual win, low risk).
2. **Part B2/B1** (backend endpoint + helpers + probe export) — one backend rebuild + migration not needed (scan_results table already exists from P3-#10).
3. **Part B3** (frontend upload UI) — one frontend rebuild.
4. **Part C** verification.

### Token-saving notes
- A and B are independent — do A fully, validate, then B. Don't interleave rebuilds.
- Reuse: `ScanResult`, `run_detection_job`, `_promote_assets`, `GraphBuilder`,
  `DataState`/`SkeletonRows`, the 139 existing design tokens. Write as little new code as possible.
- Only ONE genuinely new backend file is needed (the import endpoint + 2 helpers); everything
  else is edits. Part A is value-edits in one CSS file.
- Don't rebuild the sealed probe image for this; the probe export is a dev/CLI convenience.
