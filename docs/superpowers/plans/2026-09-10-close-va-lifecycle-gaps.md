# Closing the VA Lifecycle Gaps — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the seven capability gaps verified against the codebase on 2026-09-10, so Vedha covers the full VA lifecycle (detect → prioritise → validate → mobilise) rather than stopping at detection.

**Architecture:** Vedha is a two-halves product and every task here respects that boundary: **the probe emits FACTS only; the manager DETECTS.** New detection logic therefore lands as data-driven `PostureRule` entries in `manager/detection_engine/posture_rules.py`, never as findings in the probe. New *observations* (credential probes, checkpoints) land as probe scanners emitting facts. Platform features (scheduling, ownership, MTTR, ServiceNow) land in `manager/backend`.

**Tech Stack:** Python 3.12/3.13, FastAPI, SQLAlchemy 2.x async, Alembic, Postgres 16, pytest. Probe: stdlib-only asyncio scanners under `probe/main_scripts/` mirrored byte-identically to `probe/scanner/`.

---

## Global Constraints

Copied verbatim from the codebase's established rules. **Every task's requirements implicitly include this section.**

- **Two-tree parity is mandatory.** `probe/main_scripts/*.py` is canonical. After ANY change, run `cp probe/main_scripts/<file>.py probe/scanner/<file>.py`. `tests/test_two_tree_parity.py` fails the build on drift. All 53 mirrored modules must stay byte-identical.
- **The probe never emits findings.** `finding_count` staying 0 in `result.json` is correct. Detection belongs to the manager. Do not add a findings pass to the probe.
- **Alembic head is `0038`.** New migrations chain from it, in order, one per task that needs schema.
- **A running probe holds its code in memory.** After any probe change, the probe must be restarted; an in-flight job keeps the old behaviour until it ends. Verify with `ps -p <pid> -o lstart=` against the file mtime.
- **Manager/frontend code is BAKED into images** (`vedha-backend:local`, `vedha-frontend:local`), not mounted. Verification via `docker cp` + `docker restart` is fine; a real deploy needs an image rebuild.
- **Timestamps are IST-aware** (`+05:30`), never naive. Use `project_timestamp()` (probe: `scanner_base`) / `app/services/project_time.py` (manager). Filenames carry no `Z`.
- **No credential material in job params.** `_JOB_SECRET_KEYS` in `agents.py` rejects it at the API boundary; Postgres would store it in plaintext.
- **Scope is IP/CIDR only.** Hostnames are rejected — manager and probe DNS can disagree.
- **Every new PostureRule must declare `requires=(...)`** — the machine-checkable fact contract. Omitting it turns a missing input into a silent false-negative instead of a `MISSING_INPUT` drift record.

---

## Sequencing rationale, and what I am NOT doing

Ordered by **security value per unit of risk**, not by the order the gap list presented them.

| # | Workstream | Value | Risk | Ship independently? |
|---|---|---|---|---|
| A | Default-credential checks (IoT/printer/camera) | **Highest** — biggest real-world IoT risk | **Highest** — active auth attempts | Yes |
| B | EOL/EOS detection | High — Win10/11 22H2 unflagged today | Very low — pure data lookup | Yes |
| C | MTTR + trend metrics | Medium — inputs already exist | Very low — read-only | Yes |
| D | Finding ownership | Medium — mobilisation gap | Low — additive schema | Yes |
| E | ServiceNow integration | Low — Jira already covers the need | Low — mirrors `_send_jira` | Yes |
| F | Checkpointing / partial results | High — a 21-min/host scan streams nothing | **High** — touches the scan loop | Yes |
| G | Continuous scheduling | High — makes it a monitoring product | Medium — new worker | Needs C+F first |

**Deliberately excluded from this plan:**
- **Rewriting the probe to emit findings.** The gap list's "finding_count is 0" is a misreading of the architecture, not a defect. Doing this would create two sources of detection truth and guarantee drift.
- **Attack-path / correlation work.** Already exists (`detection/attack_paths.py`, five `CORR-*` rules).
- **CVE/CVSS/EPSS/KEV.** Already exists (`enrichment.py`, `cvss.py`, `vuln_db.py`).

---

## Points of failure — read before writing any code

These are the specific ways each workstream can go wrong. They are why the tasks are shaped the way they are.

### A. Default-credential checks — the dangerous one

1. **Account lockout.** Trying 3 passwords against a camera can lock an operator out of their own NVR, or worse, a domain account. **Mitigation:** hard cap of 