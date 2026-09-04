# System Design & SWE Check

Date: 2026-07-15

## Verdict

The core architecture is directionally strong: a thin client-network probe collects raw facts, while the manager owns detection, vulnerability data, findings, attack paths, and reporting. That split is the right foundation for a VA product because it keeps customer-network deployment light and keeps the high-value detection logic centralized and auditable.

The codebase is not yet "clean product-grade" because source, runtime artifacts, generated files, and frontend quality debt are mixed together. Backend/probe/detection tests now pass, but frontend lint exposes existing React and TypeScript issues that should be fixed before treating CI as green.

## Architecture Checkmarks

- [x] Thin probe / fat manager responsibility split.
- [x] Probe returns raw facts rather than CVE verdicts.
- [x] Manager-side deterministic detection pipeline with pinned snapshots.
- [x] Durable outbox worker for facts-ready detection processing.
- [x] Probe job leasing and reaper for abandoned running jobs.
- [x] HTTP polling plus WebSocket push path for probes.
- [x] Scope guard exists in probe scanner base.
- [x] OT profile has passive-only manager-side gate.
- [x] Manager-issued probe jobs fail closed when neither fetched nor embedded scope is available.
- [ ] Frontend lint is not clean.
- [ ] Repo hygiene is not clean until tracked `.env`, `.pyc`, certs, scan outputs, and binaries are removed from git history/index.

## SWE Checkmarks

- [x] Backend tests: 233 passed, 3 skipped.
- [x] Probe Python tests: 268 passed.
- [x] Detection engine tests: 146 passed.
- [x] Go probe packages: `go test ./...` passes, but there are no Go test files.
- [x] Frontend production build passes.
- [ ] Frontend lint fails with 34 errors and 36 warnings.
- [ ] No root `.gitignore` existed before this pass; one has now been added.
- [ ] Optional ML dependency handling was brittle; `xgboost` native-load failure used to break backend test collection.
- [ ] Root README contained a pasted business-advisor prompt; removed.

## Highest-Priority Fixes

1. Clean tracked artifacts from git: `.env`, `.DS_Store`, `__pycache__`, `*.pyc`, generated scan outputs, local cert material, and compiled binaries.
2. Fix frontend lint errors instead of weakening lint rules: React purity issues, synchronous `setState` in effects, and explicit `any` in API adapters/routes.
3. Add real tests for `probe-go`; current Go verification only proves the packages compile.
4. Move large/raw scan facts fully out of job rows in every path and keep `scan_jobs.result` lean.
