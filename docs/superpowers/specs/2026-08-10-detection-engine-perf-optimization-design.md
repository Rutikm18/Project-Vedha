# Detection-engine performance optimization (P1 + P2)

**Date:** 2026-08-10
**Scope:** `manager/detection_engine/` only. Performance dimension only (P1, P2).
Deferred by explicit decision: test-coverage expansion (C1–C3), KEV/EPSS integrity
hardening (S1), CVSS memoization + cosmetic cleanups (P3/quality).

## Context

The detection engine turns probe facts into enriched CVE findings, fully offline
against a pinned OSV snapshot. Code quality is high (clear module boundaries, no
god files, 81% test coverage, 146 tests green in ~1.3s). Two measured performance
problems dominate real-scan runtime; both are fixed here without changing detection
output.

## Problem 1 — `dpkg` subprocess in the matcher hot loop

`version_compare.dpkg_compare()` shells out to the real `dpkg --compare-versions`
binary (1–2 `subprocess` spawns **per comparison**) whenever dpkg is installed —
true on any Debian/Linux manager. It is called from `matcher._version_in_ranges`
for every version boundary of every CVE range of every candidate.

**Measured:** 11.5 ms/comparison (binary) vs 4.2 µs (pure-Python) = **2,753× slower**.
The pure-Python comparator already exists as the fallback and is cross-validated
against dpkg in the test suite. A fresh check confirmed **0 divergences across 5,411
pairs**, including every tricky epoch/tilde case and all 1,047 boundary versions in
the current snapshot.

### Decision: pure-Python in the hot path + load-time dpkg guard

- Make `_dpkg_compare_pure_python` the implementation `dpkg_compare()` uses at
  runtime. Keep `_dpkg_compare_via_binary` (still lru-cached) for the guard and tests.
- Add `verify_pure_python_matches_dpkg(versions, cache_key)` in `version_compare.py`.
  When dpkg is present, it sorts the unique `versions` with the pure-Python
  comparator and confirms the binary agrees on every **adjacent** pair (sound: if
  dpkg agrees the pure-Python order is non-decreasing on all adjacent pairs, it
  agrees on the whole order by transitivity). On any divergence it logs a loud,
  structured warning naming the diverging pair; it does **not** raise (pure-Python
  remains the best available answer, and breaking detection is worse than a warning).
- Runs **once per snapshot content-hash**: results cached in-memory, and
  best-effort persisted to `snapshots/.dpkg_validation.json` (`{content_hash: ok}`)
  so it survives process restarts and never reruns for an already-validated snapshot.
  A no-dpkg environment is a silent no-op (pure-Python is all there is anyway).
- Wiring: `vuln_db.load_snapshot()` extracts boundary versions from the loaded
  records and calls the guard once, keyed by the snapshot's `content_hash`.
- **One-time cost & the marker file.** The validation runs `dpkg` once per unique
  adjacent boundary pair. On the current snapshot that is ~1,046 pairs ≈ 13 s on
  macOS (slow `subprocess` spawns) / an estimated ~1–3 s on a Linux manager. This
  is paid **once** and then cached. The `.dpkg_validation.json` marker is committed
  alongside the snapshot (same convention as the already-tracked
  `ai_normalizer_cache.json`), so fresh checkouts / CI / production deploys load
  with the guard as a no-op — the cost lands only on whoever generates a new
  snapshot. (A "skip purely-numeric pairs" bounding was measured and rejected: 99%
  of Debian boundary strings carry an epoch/tilde/suffix, so it saved nothing.)

**Effect:** matching phase drops from subprocess-bound to in-process; ~2,750× faster
per comparison, with a one-time (cached-forever) correctness check against dpkg for
the exact data being matched.

## Problem 2 — 7.6 MB snapshot loaded + re-hashed twice per run

`engine_bridge._vuln_db_meta()` calls `load_snapshot()` (full 7.6 MB parse +
canonical `json.dumps` + SHA-256 re-hash) purely to read metadata, then
`run_pipeline()` calls `load_snapshot()` **again**. KEV/EPSS reload similarly. No
caching across runs.

**Measured:** 75 ms/load (36 ms of it the content-hash), ~150 ms wasted per run on
the double load, repeated on every detection run.

### Decision: mtime-keyed memoization of the loaders

- `vuln_db.load_snapshot(path)`: module-level cache keyed by
  `(resolved_path, st_mtime_ns, st_size)`, guarded by a `threading.Lock`. Cache hit
  returns the already-built `VulnDB` (integrity hash verified once, on the real
  load). File change (mtime/size differ) triggers a genuine reload — pinning
  semantics preserved.
- `enrichment_db.load_kev` / `load_epss`: same mtime-keyed memoization.
- No API changes. The `_vuln_db_meta()` + `run_pipeline()` double-load collapses to
  one real load + one cache hit automatically; repeated runs reuse the loaded DBs.
- `_clear_caches()` helpers exposed for tests.

**Effect:** ~150 ms/run → ~75 ms first run, ~0 ms subsequent; content-hash
re-serialization runs once per snapshot version instead of once per call.

## Non-goals / preserved invariants

- **Detection output is unchanged.** Same snapshot in → same findings out. Verified
  by keeping all 146 existing tests green and diffing pipeline output before/after.
- No network calls added to the detection path. The guard uses only the local dpkg
  binary; absence is a no-op.
- `_dpkg_compare_via_binary` and `_HAVE_DPKG` stay public (test suite depends on them).
- `VulnDB` direct construction path (used by `test_detection_core.py`) untouched.

## Implementation plan (TDD, phased)

**Phase 1 — P1 hot path (`version_compare.py`)**
1. RED: test that `dpkg_compare` returns correct orderings without spawning a
   subprocess (monkeypatch `_dpkg_compare_via_binary` to raise/count; assert not
   called by `dpkg_compare`).
2. GREEN: point `dpkg_compare` at `_dpkg_compare_pure_python`; keep `a == b`
   short-circuit.
3. Confirm existing `test_version_compare.py` (incl. binary cross-validation) stays green.

**Phase 2 — P1 guard (`version_compare.py` + `vuln_db.py`)**
4. RED: test `verify_pure_python_matches_dpkg` — passes on agreeing versions,
   warns + records divergence on a stubbed disagreeing binary, no-ops when dpkg
   absent, and reruns only on a new cache_key.
5. GREEN: implement guard with in-memory + best-effort file cache.
6. Wire into `load_snapshot`; test it runs once per content-hash.

**Phase 3 — P2 caching (`vuln_db.py`, `enrichment_db.py`)**
7. RED: test `load_snapshot` returns the same instance on repeat calls, reloads
   after mtime change, and `_clear_caches()` resets it; same for KEV/EPSS.
8. GREEN: implement mtime-keyed memoization + lock + clear helpers.

**Phase 4 — verification**
9. Full `detection_engine` suite green (146 + new).
10. Benchmark harness: end-to-end `run_pipeline` on a representative fixture,
    before vs after, reporting wall-clock + subprocess count. Capture numbers.
11. Output-equivalence check: findings identical pre/post.

## Results (measured, after implementation)

End-to-end `run_pipeline` on a 40-host × 13-package fixture (28,000 findings):

| | Before | After |
|---|---|---|
| **P1** matcher version compare (per run) | 17,284 ms (400k binary-path comparisons) | 2,325 ms (0 subprocess spawns) — **7× faster** |
| **P2** snapshot load (7.6 MB parse + hash) | 85 ms cold, ×2 per run via engine_bridge | 0.04 ms warm — **2,122×**; double-load eliminated |
| Findings output | 28,000 | 28,000, **identical `finding_id` set** |

Tests: 146 existing detection-engine tests + 10 new = **156 green** (suite runtime
also dropped 1.26 s → 0.49 s, since the tests themselves no longer spawn `dpkg`).
Full backend suite: **427 passed, 3 skipped** — no regression. On real
multi-hundred-host scans the pre-optimization matcher ran into minutes; this is the
change that makes background detection complete promptly.

## Risks

- **Pure-Python diverges from dpkg on some future snapshot string.** Mitigated by
  the load-time guard (loud warning on the exact snapshot in use) and existing
  cross-validation tests.
- **Stale cache after an out-of-band snapshot swap.** Mitigated by mtime+size key;
  an atomic replace changes mtime and invalidates.
- **Concurrent first-load race.** Mitigated by the lock; worst case is a benign
  double-load, never a corrupt cache.
