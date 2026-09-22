# Review Follow-ups Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix every defect the 2026-09-23 two-axis review found in commit `13f1170` — a CI break on `main`, tests that cannot fail or never run, a misleading result field, wrong UI copy, a hazard fix that did not work, and false claims in comments and the handoff doc.

**Architecture:** Twelve independent, small tasks. Task 1 is urgent and lands alone on its own branch because `main` is very likely red. Tasks 2–11 land together on `fix/review-followups`. Task 12 lands them through a pull request, because `agent-ci` runs **only** on pull requests.

**Tech Stack:** Python 3.12/3.13 + pytest 9 + pytest-asyncio (probe, manager backend); TypeScript + `tsx --test` + `tsc` (manager frontend); GitHub Actions.

## Global Constraints

- Repo root has spaces. In every new shell first run `REPO="/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"`, and always quote it: `cd "$REPO/probe"`.
- Probe Python: `cd "$REPO/probe" && ./.venv/bin/python -m pytest ...`. Manager Python: `cd "$REPO/manager/backend" && ./.venv/bin/python -m pytest ...`. Frontend: `cd "$REPO/manager/frontend" && npx tsx --test tests/<file>.test.ts`, `npm test`, `npx tsc --noEmit`.
- **Two-tree rule:** `probe/main_scripts/` is canonical; `probe/scanner/` must be byte-identical. After editing `probe/main_scripts/X.py` run `cp probe/main_scripts/X.py probe/scanner/X.py` and `./.venv/bin/python -m pytest tests/test_two_tree_parity.py -q`.
- **A test file runs in CI only if NAMED** in a workflow's pytest list (`.github/workflows/agent-ci.yml`, `.github/workflows/scanner-accuracy.yml`). The `paths:` trigger alone does not run it.
- `.githooks` bumps `VERSION` on every commit. Expected — commit it, do not revert it.
- Every commit message ends with the line: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
- Comment rule for this plan: keep the codebase's long-comment convention, but in every line you touch remove (a) false claims, (b) plan IDs (`A1`, `T2.4`, `P2/D1`), (c) before/after history wording ("used to", "previously", "now"), and (d) line-number citations such as `port_scanner.py:474` — cite a symbol instead ("the reprobe comment in `PortScanner.__init__`").
- Pushing, opening PRs and merging are shared-state actions: **ask the user before each one.**
- Baselines before starting: probe `2372 passed`, manager backend `1272 passed, 4 skipped`, frontend `221 passed`, `tsc` clean.

## Task Map

| # | Task | Why it matters | Branch |
|---|---|---|---|
| 1 | CI: install `pytest-asyncio` | `main` very likely red (15 failures in `scanner-accuracy`) | `fix/ci-async-plugin` |
| 2 | SYN: a bad-cookie test that can fail | The spoof filter is guarded by nothing | `fix/review-followups` |
| 3 | SYN: drain bound, dead code, honest buffer comment | Bound untested; comment overstates the buffer ~10× | same |
| 4 | Kernel gate: `gate_measured` | `measured` is always `True` in practice | same |
| 5 | `scan_metrics`: mirror the probe's default | A dataless summary survives the partition | same |
| 6 | `ScopeError`: remove the reload at its source | The `ValueError` base defused nothing | same |
| 7 | Probe comments: correct false and dated claims | "`light` never ran" is false | same |
| 8 | Frontend: intensity data module + honest copy | UI claims ~15 ports (65) and "hours per host" (30 min cap) | same |
| 9 | Manager: pin the UI alias chain | `aggressive → deep` is tested nowhere | same |
| 10 | CI: run the new tests + frontend workflow | 5 new probe tests and all frontend tests never run in CI | same |
| 11 | Handoff doc: correct the record | Doc repeats every false claim | same |
| 12 | Land via pull request | `agent-ci` only runs on PRs | — |

## File Structure

| File | Responsibility | Tasks |
|---|---|---|
| `.github/workflows/agent-ci.yml` | Agent-module CI (PR only, 3-OS matrix) | 1, 10 |
| `.github/workflows/scanner-accuracy.yml` | Scanner accuracy gate (push to main + PR) | 1, 10 |
| `.github/workflows/frontend-ci.yml` (new) | Frontend tests + type check | 10 |
| `probe/main_scripts/syn_scanner.py` (+ mirror) | Raw SYN scan loop | 2 (mutation only), 3 |
| `probe/tests/test_syn_recv_interleave.py` | SYN loop tests against a simulated kernel | 2, 3 |
| `probe/agent/kernel_limits.py` | Kernel ceiling checks + run_stats shape | 4 |
| `probe/agent/engine.py` | Job admission + run_stats | 4, 6 |
| `probe/tests/test_kernel_admission.py` | Kernel gate tests | 4 |
| `probe/docker-compose.yml` | Deployment + ceiling documentation | 4 |
| `manager/backend/app/services/job_result_service.py` | Scope partition of results | 5 |
| `manager/backend/tests/test_scan_metrics_partition.py` | Partition metrics tests | 5 |
| `probe/main_scripts/scanner_base.py` (+ mirror) | `ScopeError` | 6 |
| `probe/tests/test_scope_error_identity.py` | ScopeError + no-reload guard | 6 |
| `probe/tests/test_project_timezone.py` | Project timezone tests | 6 |
| `probe/tests/test_scope_parity.py` | Scope parity (comment only) | 6 |
| `probe/workflow/intensity.py` | Intensity presets | 7 |
| `probe/tests/test_intensity_envelope.py` | Preset envelope tests | 7 |
| `probe/workflow/workflow_engine.py` | Gate 6 comment only | 7 |
| `manager/frontend/lib/scan-intensity.ts` (new) | Dial display data | 8 |
| `manager/frontend/app/scan/page.tsx` | Scanner page | 8 |
| `manager/frontend/tests/scan-intensity.test.ts` | Launcher + dial parity tests | 8 |
| `manager/backend/tests/test_enqueue_intensity.py` | Enqueue intensity tests | 9 |
| `agressive-plan.md` | Handoff record | 11 |

---

### Task 1: CI — install `pytest-asyncio` in both probe workflows (URGENT)

**Why:** Both workflows install bare `pytest` (resolves to 9.x). Under pytest 9 an `async def` test with no async plugin **fails** ("async def functions are not natively supported"). `scanner-accuracy` runs on push to `main` and lists `test_reprobe_budget.py` and `test_rate_limiter_throughput.py`, both async — so `main` is very likely red now. `agent-ci`'s list has async files too and will fail on the next probe PR.

**Files:**
- Modify: `.github/workflows/agent-ci.yml:28`
- Modify: `.github/workflows/scanner-accuracy.yml:56`

**Interfaces:**
- Consumes: nothing.
- Produces: CI environments where `@pytest.mark.asyncio` tests run. Task 10 relies on this.

- [ ] **Step 1: Branch**

```bash
cd "$REPO" && git switch main && git pull --ff-only && git switch -c fix/ci-async-plugin
```

- [ ] **Step 2: Reproduce the CI failure locally (the failing test)**

`-p no:asyncio` disables the plugin, which is exactly what CI lacks.

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest -p no:asyncio -q \
  tests/test_accuracy_gate.py tests/test_main_scripts_accuracy.py tests/test_scanner_congestion.py \
  tests/test_dualstack_fallback.py tests/test_syn_scanner.py tests/test_tarpit.py \
  tests/test_two_tree_parity.py tests/test_scope_parity.py tests/test_reprobe_budget.py \
  tests/test_port_state_ranges.py tests/test_rate_limiter_throughput.py 2>&1 | tail -1
```

Expected: `15 failed, 272 passed`

- [ ] **Step 3: Add the plugin to `agent-ci.yml`**

Replace line 28:

```yaml
        run: python -m pip install -r requirements-runtime.txt pytest
```

with:

```yaml
        run: python -m pip install -r requirements-runtime.txt pytest 'pytest-asyncio>=1,<2'
```

(Single quotes are literal in bash and in the Windows runner's pwsh.)

- [ ] **Step 4: Add the plugin to `scanner-accuracy.yml`**

Replace line 56:

```yaml
          ./.venv/bin/pip install pytest
```

with:

```yaml
          ./.venv/bin/pip install pytest 'pytest-asyncio>=1,<2'
```

- [ ] **Step 5: Verify both files parse and the lists pass with the plugin**

```bash
cd "$REPO" && manager/backend/.venv/bin/python -c "import yaml; [yaml.safe_load(open(p)) for p in ('.github/workflows/agent-ci.yml','.github/workflows/scanner-accuracy.yml')]; print('yaml ok')"
cd "$REPO/probe" && ./.venv/bin/python -m pytest -q tests/test_reprobe_budget.py tests/test_rate_limiter_throughput.py tests/test_banner_pass_concurrency.py tests/test_stage_fanout_policy.py 2>&1 | tail -1
```

Expected: `yaml ok`, then `... passed` with 0 failed.

- [ ] **Step 6: Commit**

```bash
cd "$REPO" && git add .github/workflows/agent-ci.yml .github/workflows/scanner-accuracy.yml && git commit -F- <<'MSG'
ci: install pytest-asyncio so async probe tests can run

Under pytest 9 an async test with no async plugin fails outright. Both
workflows installed bare pytest, so scanner-accuracy (runs on push to main)
failed 15 tests and agent-ci would fail 27 on the next probe PR.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

- [ ] **Step 7: Land it alone — ASK THE USER FIRST**

`gh` is not installed. After the user approves:

```bash
cd "$REPO" && git push -u origin fix/ci-async-plugin
```

Open `https://github.com/Rutikm18/Project-Vedha/compare/main...fix/ci-async-plugin?expand=1`, create the PR, wait for `scanner-accuracy` to go green, merge. Then `git switch main && git pull --ff-only`.

---

### Task 2: SYN — a bad-cookie test that can actually fail

**Why:** `test_a_foreign_reply_is_ignored` can never fail, for two reasons. It writes bytes `[36:40]` (the TCP checksum and urgent pointer — the ack is at `[28:32]`), so the "forged" packet is a byte-identical valid reply. And it forges an RST, which has the same effect as the genuine RST it races. With the cookie check deleted from the scanner, all 159 SYN tests still pass.

**Files:**
- Modify: `probe/tests/test_syn_recv_interleave.py` (the `sendto` helper and `test_a_foreign_reply_is_ignored`)

**Interfaces:**
- Consumes: `_reply(port, *, flags)`, `fake_net`, `_scanner`, `_states`, `TARGET` — existing helpers in the same file.
- Produces: `test_a_reply_with_a_bad_cookie_is_ignored`.

- [ ] **Step 1: Branch (all of Tasks 2–11 use this branch)**

```bash
cd "$REPO" && git switch main && git pull --ff-only && git switch -c fix/review-followups
```

- [ ] **Step 2: Replace the vacuous test**

In `probe/tests/test_syn_recv_interleave.py`, replace the whole of `test_a_foreign_reply_is_ignored`:

```python
    def test_a_foreign_reply_is_ignored(self, fake_net):
        """Cross-host leakage: a reply whose cookie does not recompute must
        never resolve a port."""
        net = fake_net(capacity=100)
        bad = bytearray(_reply(9000, flags=ss.TCP_RST))
        bad[36:40] = (0).to_bytes(4, "big")           # wrong ack -> bad cookie
        net["kernel"].deliver(bytes(bad))
        states = _states(_scanner([9000, 9001])._syn_scan_blocking(TARGET))
        assert states[9000] in ("closed", "filtered")
```

with:

```python
    def test_a_reply_with_a_bad_cookie_is_ignored(self, fake_net):
        """A spoofed or cross-host SYN-ACK must never mark a port open.

        Port 9000 genuinely answers RST. A forged SYN-ACK with the wrong ack is
        queued BEFORE any send, so it is the first packet drained: without the
        cookie check it would win (`states.setdefault` keeps the first verdict)
        and 9000 would read `open`."""
        net = fake_net(capacity=100)
        forged = bytearray(_reply(9000, flags=ss.TCP_SYN | ss.TCP_ACK))
        forged[28:32] = (0).to_bytes(4, "big")        # the TCP ack field
        net["kernel"].deliver(bytes(forged))
        states = _states(_scanner([9000, 9001])._syn_scan_blocking(TARGET))
        assert states[9000] == "closed"
```

Also fix the odd index in `_SendSock.sendto`. Replace:

```python
        port = struct.unpack("!H", pkt[22:24])[1 - 1]   # TCP dst_port
```

with:

```python
        port = struct.unpack("!H", pkt[22:24])[0]       # TCP dst_port
```

- [ ] **Step 3: Run it against the real scanner**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_syn_recv_interleave.py -q
```

Expected: `7 passed`

- [ ] **Step 4: Prove it can fail — delete the cookie check, run, restore**

```bash
cd "$REPO/probe" && ORIG="${TMPDIR:-/tmp}/syn_scanner.orig" && cp main_scripts/syn_scanner.py "$ORIG" \
&& ./.venv/bin/python - <<'PY'
import pathlib
needle = "        if not verify_reply_cookie(parsed, src_port, self._key):\n            return False\n"
for p in ("main_scripts/syn_scanner.py", "scanner/syn_scanner.py"):
    f = pathlib.Path(p); s = f.read_text()
    assert s.count(needle) == 1, p
    f.write_text(s.replace(needle, "", 1))
PY
./.venv/bin/python -m pytest tests/test_syn_recv_interleave.py -q -k bad_cookie 2>&1 | tail -1
cp "$ORIG" main_scripts/syn_scanner.py && cp "$ORIG" scanner/syn_scanner.py && rm "$ORIG"
git -C "$REPO" status --short probe/main_scripts probe/scanner
```

Expected: `1 failed` (`assert 'open' == 'closed'`), then an **empty** `git status` (scanner restored).

- [ ] **Step 5: Commit**

```bash
cd "$REPO" && git add probe/tests/test_syn_recv_interleave.py && git commit -F- <<'MSG'
test(syn): make the bad-cookie test able to fail

It wrote the checksum field instead of the ack, so the "forged" packet was
valid, and it forged an RST that matched the genuine answer. Now a forged
SYN-ACK must be rejected; deleting the cookie check makes it fail.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 3: SYN — test the drain bound, remove dead code, correct the buffer comment

**Why:** The 64-packet drain cap is untested. `_accept_reply` returns a bool and `_drain_ready` returns a count that nothing reads, `max_packets` is never passed, and `except BlockingIOError` sits right before an `except OSError` that already catches it. The loop comment says the buffer is 4 MB and holds ~5,000 packets; plain `SO_RCVBUF` is clamped to `net.core.rmem_max` (~208 KB default, doubled by the kernel), so it holds a few hundred.

**Files:**
- Modify: `probe/main_scripts/syn_scanner.py` (then mirror to `probe/scanner/syn_scanner.py`)
- Modify: `probe/tests/test_syn_recv_interleave.py` (module docstring + new test class)

**Interfaces:**
- Consumes: `_scanner`, `TARGET`, `SRC_PORT` test helpers.
- Produces: module constant `ss._DRAIN_BATCH: int = 64`; `SynScanner._drain_ready(recv_sock, **ctx) -> None`; `SynScanner._accept_reply(...) -> None`.

- [ ] **Step 1: Write the failing test**

Append to `probe/tests/test_syn_recv_interleave.py`:

```python
class _Flood:
    """A socket that always has another packet queued."""

    def __init__(self):
        self.recv_calls = 0

    def recv(self, _n):
        self.recv_calls += 1
        return b"\x00" * 40            # unparseable, so ignored — but consumed


class TestTheDrainIsBounded:
    def test_one_call_consumes_at_most_one_batch(self):
        """Without the cap, a host answering faster than we send would hold
        the send loop forever."""
        sock = _Flood()
        _scanner([9000])._drain_ready(
            sock, dst_ip=TARGET, src_port=SRC_PORT, send_at={}, states={},
            pending_set=set(), meta={}, est=None)
        assert sock.recv_calls == ss._DRAIN_BATCH
```

- [ ] **Step 2: Run it to verify it fails**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_syn_recv_interleave.py -q -k one_batch 2>&1 | tail -3
```

Expected: FAIL with `AttributeError: module 'scanner.syn_scanner' has no attribute '_DRAIN_BATCH'`

- [ ] **Step 3: Add the constant**

In `probe/main_scripts/syn_scanner.py`, immediately after the line `TCP_ACK = 0x10`, add:

```python

# Replies consumed per drain call: bounds catch-up so a reply flood cannot
# starve the send loop.
_DRAIN_BATCH = 64
```

- [ ] **Step 4: Replace `_drain_ready`**

Replace the whole method:

```python
    def _drain_ready(self, recv_sock, *, max_packets: int = 64, **ctx) -> int:
        """Consume replies already queued, without blocking. Returns the count.

        `max_packets` bounds one call so a host answering faster than we send
        cannot hold the send loop indefinitely: the cap turns a starvation risk
        into a bounded amount of catch-up per packet sent.
        """
        harvested = 0
        while harvested < max_packets:
            try:
                raw = recv_sock.recv(65535)
            except BlockingIOError:
                break                       # nothing queued — the common case
            except OSError:
                break
            self._accept_reply(raw, **ctx)
            harvested += 1
        return harvested
```

with:

```python
    def _drain_ready(self, recv_sock, **ctx) -> None:
        """Consume up to _DRAIN_BATCH replies already queued, without blocking."""
        for _ in range(_DRAIN_BATCH):
            try:
                raw = recv_sock.recv(65535)
            except OSError:        # includes BlockingIOError: nothing queued
                return
            self._accept_reply(raw, **ctx)
```

- [ ] **Step 5: Drop `_accept_reply`'s unused return value**

In `_accept_reply`:
- change the signature's `meta: dict, est) -> bool:` to `meta: dict, est) -> None:`
- change each of its four `return False` lines to `return`
- delete its final line `        return True`

The body between those lines is unchanged. The four early exits become:

```python
        parsed = parse_packet(raw)
        if not parsed or parsed["ip_src"] != dst_ip:
            return
        if parsed["dst_port"] != src_port:
            return
        if not verify_reply_cookie(parsed, src_port, self._key):
            return
        verdict = classify(parsed["flags"])
        if not verdict:
            return
```

- [ ] **Step 6: Correct the loop comment**

In `_syn_scan_blocking`, replace:

```python
                    # DRAIN AS WE SEND. Every SYN provokes its reply about one
                    # RTT later, i.e. while this loop is still running, and the
                    # socket is the only thing holding them. SO_RCVBUF is 4 MB
                    # but Linux charges skb->truesize (~768 B for a 40-byte
                    # segment, not 40), so it holds on the order of 5,000
                    # packets — and a 65,535-port sweep of a mostly-closed host
                    # answers with 65,535 RSTs. The overflow is dropped with no
                    # error, and those ports end up reported `filtered`.
                    #
                    # Rate does NOT save this: the overflow is set by how many
                    # ports are in the round, not how fast they leave. Bounded
                    # per call so a reply flood cannot starve the send loop.
                    self._drain_ready(recv_sock, **ctx)
```

with:

```python
                    # Drain as we send: each SYN's reply arrives about one RTT
                    # later, while this loop is still running. Plain SO_RCVBUF
                    # is clamped to net.core.rmem_max (~208 KB by default, which
                    # the kernel doubles) and charged per skb->truesize, so a few
                    # hundred replies fill it. Overflow is dropped with no error
                    # and reads as `filtered`, however slowly we send.
                    self._drain_ready(recv_sock, **ctx)
```

- [ ] **Step 7: Correct the test module docstring**

Replace the module docstring of `probe/tests/test_syn_recv_interleave.py` (everything from the opening `"""` to the closing `"""` before `from __future__ import annotations`) with:

```python
"""
The SYN scanner must drain replies WHILE it is still sending.

A round that sends its whole cohort before reading the socket leaves every
reply waiting in the receive buffer. Plain SO_RCVBUF is clamped to
net.core.rmem_max (~208 KB by default, doubled by the kernel) and charged per
skb->truesize, so a few hundred replies fill it; the rest are dropped with no
error and the ports read as `filtered`. The overflow depends on how many ports
are in the round, not on the send rate.

These tests replace the KERNEL, not the scanner: a bounded receive queue that
drops silently, driving the real _syn_scan_blocking. They prove the loop
structure. The packet bytes still need Linux with NET_RAW to verify.
"""
```

- [ ] **Step 8: Mirror and run**

```bash
cd "$REPO/probe" && cp main_scripts/syn_scanner.py scanner/syn_scanner.py \
&& ./.venv/bin/python -m pytest tests/test_syn_recv_interleave.py tests/test_syn_scanner.py tests/test_two_tree_parity.py -q 2>&1 | tail -1
```

Expected: all passed, 0 failed.

- [ ] **Step 9: Commit**

```bash
cd "$REPO" && git add probe/main_scripts/syn_scanner.py probe/scanner/syn_scanner.py probe/tests/test_syn_recv_interleave.py && git commit -F- <<'MSG'
fix(syn): test the drain bound; drop dead returns; correct buffer size

The 64-packet cap was untested and its parameter never passed; the return
values were never read. SO_RCVBUF is clamped to rmem_max, so the buffer
holds a few hundred replies, not the ~5,000 the comment claimed.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 4: Kernel gate — `gate_measured` instead of an always-true `measured`

**Why:** `as_run_stats` sets `measured = bool(checks)`, but `assess()` always returns `fd` and `raw_socket` checks, so on a Mac — where conntrack, the only blocking check, cannot be read — it reports `measured: true`. That is the false confidence the field was meant to prevent. Also: a preflight exception is logged at DEBUG (invisible), `engine.py` imports one module under three names, and `docker-compose.yml` wrongly says host networking avoids conntrack.

**Files:**
- Modify: `probe/agent/kernel_limits.py` (`as_run_stats`)
- Modify: `probe/tests/test_kernel_admission.py`
- Modify: `probe/agent/engine.py:312-314,1018,1031-1032,1044,1071,1081`
- Modify: `probe/docker-compose.yml` (two comment sentences)

**Interfaces:**
- Consumes: `kl.KernelLimits(fd_soft, fd_hard, conntrack_max, conntrack_count, ephemeral_lo, ephemeral_hi, gc_thresh3, syn_capable)`, `kl.assess(limits, *, rate, concurrency, host_count, port_count) -> list[Check]`, `kl.BLOCKING_CHECKS`.
- Produces: `run_stats["kernel"]` keys `gate_measured: bool`, `warnings: int`, `blocking: list[str]`, `checks: list[dict]`. The key `measured` is removed. Task 11 documents `gate_measured`.

- [ ] **Step 1: Write the failing tests**

In `probe/tests/test_kernel_admission.py`, replace the test `test_unmeasurable_is_not_reported_as_clean` (the last method of `TestTheCeilingsReachTheResult`) with:

```python
    def test_a_host_that_cannot_read_conntrack_reports_a_blind_gate(self):
        """Realistic input. macOS or a container without /proc still yields
        fd and raw_socket checks, so a non-empty list proves nothing."""
        checks = kl.assess(_limits(conntrack_max=None, conntrack_count=None),
                           rate=150, concurrency=80, host_count=8, port_count=65535)
        assert checks, "assess() always returns something — that is the trap"
        assert kl.as_run_stats(checks)["gate_measured"] is False

    def test_a_readable_conntrack_table_measures_the_gate(self):
        checks = kl.assess(_limits(), rate=150, concurrency=80,
                           host_count=8, port_count=65535)
        assert kl.as_run_stats(checks)["gate_measured"] is True

    def test_a_skipped_preflight_is_a_blind_gate(self):
        """run_scan passes [] when the preflight itself raised."""
        assert kl.as_run_stats([])["gate_measured"] is False
```

and add this helper just above `class TestWhichChecksBlock:`:

```python
def _limits(**overrides):
    base = dict(fd_soft=1_048_576, fd_hard=1_048_576, conntrack_max=65_536,
                conntrack_count=0, ephemeral_lo=32_768, ephemeral_hi=60_999,
                gc_thresh3=1024, syn_capable=False)
    base.update(overrides)
    return kl.KernelLimits(**base)
```

- [ ] **Step 2: Run them to verify they fail**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_kernel_admission.py -q 2>&1 | tail -4
```

Expected: 3 failed with `KeyError: 'gate_measured'`

- [ ] **Step 3: Implement `gate_measured`**

In `probe/agent/kernel_limits.py`, replace the whole `as_run_stats` function with:

```python
def as_run_stats(checks: list[Check]) -> dict:
    """The ceilings this scan ran under, as JSON for the job result.

    `gate_measured` is False when a blocking ceiling could not be read (no /proc,
    no netfilter): the refusal gate then ran blind, which is a different
    statement from "the ceilings are fine".
    """
    present = {c.name for c in checks}
    return {
        "gate_measured": all(name in present for name in BLOCKING_CHECKS),
        "warnings": sum(1 for c in checks if c.status != "pass"),
        "blocking": [c.name for c in blocking_checks(checks)],
        "checks": [{"name": c.name, "status": c.status, "detail": c.detail}
                   for c in checks],
    }
```

- [ ] **Step 4: Run to verify they pass**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_kernel_admission.py -q 2>&1 | tail -1
```

Expected: all passed.

- [ ] **Step 5: One import name in `engine.py`; make a skipped gate loud**

`engine.py` already has `from agent import kernel_limits as _kernel_limits` at line 50. Use it everywhere:

1. In `_refuse_if_kernel_unsafe`, delete the line `    from agent import kernel_limits` and the blank line after it, and change `kernel_limits.blocking_checks(checks or [])` to `_kernel_limits.blocking_checks(checks or [])`.
2. In the preflight `try:` block, delete the line `        from agent import kernel_limits` and the blank line after it, and change

```python
        _kernel_checks = kernel_limits.assess(
            kernel_limits.probe_limits(),
```

to

```python
        _kernel_checks = _kernel_limits.assess(
            _kernel_limits.probe_limits(),
```

3. Replace `        LOG.debug("job preflight skipped: %r", exc)` with:

```python
        LOG.warning("job preflight skipped; kernel gate not evaluated: %r", exc)
```

4. In the kernel refusal block, delete `        from agent import kernel_limits as _kl` and change `run_stats={"kernel": _kl.as_run_stats(_kernel_checks)},` to `run_stats={"kernel": _kernel_limits.as_run_stats(_kernel_checks)},`.

Verify nothing else refers to the removed names:

```bash
cd "$REPO/probe" && grep -nE "^\s+from agent import kernel_limits|\b_kl\b|[^_]kernel_limits\.(assess|probe_limits|blocking_checks|as_run_stats)" agent/engine.py || echo "clean"
```

Expected: `clean`

- [ ] **Step 6: Correct the test module docstring**

In `probe/tests/test_kernel_admission.py`, replace the first paragraph of the module docstring:

```python
"""
T2.4 — the kernel ceilings stop being advice nobody acts on.

A1 measures them and logs them. Nothing read the result, so a probe whose
conntrack table cannot hold the job's probe rate ran the job anyway, and the
kernel dropped the overflow with NO error to userspace. The scanner saw
silence, waited out its timeout, and recorded `filtered` — a claim about the
TARGET manufactured entirely by a limit on the SCANNER. The scan then looks
complete. That is the same deception `_refuse_if_infeasible` exists to prevent,
and it is invisible from inside the result.
```

with:

```python
"""
The probe host's kernel ceilings are enforced at admission and recorded.

A conntrack table that cannot hold the job's probe rate drops the overflow
with NO error to userspace. The scanner hears silence and records `filtered` —
a claim about the TARGET produced entirely by a limit on the SCANNER, which
the result cannot reveal on its own.
```

- [ ] **Step 7: Correct `docker-compose.yml`**

Replace:

```yaml
    # job param allow_degraded_kernel=true). `network_mode: host` without NAT
    # avoids conntrack entirely.
```

with:

```yaml
    # job param allow_degraded_kernel=true). `network_mode: host` removes the
    # NAT hop, but conntrack still tracks the probe's traffic whenever the
    # module is loaded (Docker loads it), so the same check applies there.
```

and replace `pool — min(32, cpu+4) — and Gate 6 now fans out across hosts, so a busy` with `pool — min(32, cpu+4) — and Gate 6 fans out across hosts, so a busy`.

- [ ] **Step 8: Run the admission suites and validate the compose file**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_kernel_admission.py tests/test_kernel_limits.py tests/test_infeasible_job_admission.py tests/test_run_timing.py -q 2>&1 | tail -1
cd "$REPO" && manager/backend/.venv/bin/python -c "import yaml; yaml.safe_load(open('probe/docker-compose.yml')); print('yaml ok')"
```

Expected: all passed; `yaml ok`.

- [ ] **Step 9: Commit**

```bash
cd "$REPO" && git add probe/agent/kernel_limits.py probe/agent/engine.py probe/tests/test_kernel_admission.py probe/docker-compose.yml && git commit -F- <<'MSG'
fix(kernel): report whether the refusal gate actually measured anything

`measured` was bool(checks), which is always true because assess() always
returns fd/raw_socket checks. `gate_measured` is true only when every
blocking ceiling was read. A skipped preflight now logs at WARNING, and
host networking does not avoid conntrack.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 5: `scan_metrics` — match the probe's default for a dataless summary

**Why:** The probe builds `scan_metrics` with `f.get("data", {})`, so a summary fact with no `data` key appears as `{}`. The manager removes `fact.get("data")` — i.e. `None` — which never matches, so that `{}` survives the partition. Two guards in the loop also check for cases that cannot occur: indices come from enumerating the same list, and the identity traversal only yields dicts.

**Files:**
- Modify: `manager/backend/app/services/job_result_service.py` (`_drop_orphaned_metrics`)
- Test: `manager/backend/tests/test_scan_metrics_partition.py`

**Interfaces:**
- Consumes: `partition_result_scope(result, scope_cidrs, excluded_cidrs=None) -> tuple[dict, list]`; test helpers `_summary()`, `SCOPE`.
- Produces: no signature change.

- [ ] **Step 1: Write the failing test**

Add to `class TestTheMetricsFollowTheFacts` in `manager/backend/tests/test_scan_metrics_partition.py`:

```python
    def test_a_summary_without_data_is_matched_as_the_probe_emitted_it(self):
        """The probe surfaces `f.get("data", {})`, so a summary fact with no
        `data` key appears in scan_metrics as {}. The partition must remove
        that same {}."""
        result = {
            "hosts": [{"ip": "10.0.0.5"}, {"ip": "192.168.99.9"}],
            "facts": [
                {"target": "10.0.0.5", "scanner": "port_scan",
                 "status": "scan_summary", "data": _summary()},
                {"target": "192.168.99.9", "scanner": "port_scan",
                 "status": "scan_summary"},
            ],
            "scan_metrics": [_summary(), {}],
        }
        filtered, _ = partition_result_scope(result, SCOPE)
        assert filtered["scan_metrics"] == [_summary()]
```

- [ ] **Step 2: Run it to verify it fails**

```bash
cd "$REPO/manager/backend" && ./.venv/bin/python -m pytest tests/test_scan_metrics_partition.py -q -k without_data 2>&1 | tail -3
```

Expected: FAIL — the right side of the comparison shows an extra `{}`.

- [ ] **Step 3: Implement**

In `_drop_orphaned_metrics`, replace the docstring sentence

```
    describes the sweep and carries `vantage`, not a target — so a host's
    metrics row used to survive the partition that discarded its evidence, and
    scan_health_summary() then aggregated a host absent from the result.
```

with

```
    describes the sweep and carries `vantage`, not a target — so without this
    a host's metrics row would outlive the evidence the partition discarded,
    and scan_health_summary() would aggregate a host absent from the result.
```

and replace the loop:

```python
    survivors = list(metrics)
    for index in sorted(dropped_facts):
        if not (0 <= index < len(facts)):
            continue
        fact = facts[index]
        if not isinstance(fact, dict) or fact.get("status") != "scan_summary":
            continue
        try:
            survivors.remove(fact.get("data"))
        except ValueError:      # this summary was never surfaced at top level
            continue
    filtered["scan_metrics"] = survivors
```

with:

```python
    survivors = list(metrics)
    for index in sorted(dropped_facts):
        fact = facts[index]
        if fact.get("status") != "scan_summary":
            continue
        try:
            # The same default the probe used when it built scan_metrics.
            survivors.remove(fact.get("data", {}))
        except ValueError:      # this summary was never surfaced at top level
            continue
    filtered["scan_metrics"] = survivors
```

- [ ] **Step 4: Run to verify**

```bash
cd "$REPO/manager/backend" && ./.venv/bin/python -m pytest tests/test_scan_metrics_partition.py tests/test_partial_scope_rejection.py tests/test_run_scoped_fact_scope.py -q 2>&1 | tail -1
```

Expected: all passed.

- [ ] **Step 5: Commit**

```bash
cd "$REPO" && git add manager/backend/app/services/job_result_service.py manager/backend/tests/test_scan_metrics_partition.py && git commit -F- <<'MSG'
fix(ingest): drop a dataless summary's metrics row with its fact

The probe emits f.get("data", {}); the manager removed f.get("data"),
i.e. None, so a {} row survived. Also drops two guards for cases the
identity traversal makes impossible.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 6: `ScopeError` — remove the reload hazard at its source

**Why:** Making `ScopeError` a `ValueError` did not defuse the hazard. A handler or `pytest.raises` holding a class bound before `importlib.reload()` misses the reloaded class whatever its base, because the fresh class is not a subclass of the stale one. The real fix is the spec's other option: stop reloading. `project_now()` reads the module global `PROJECT_TZ` at call time, so the timezone tests can patch that directly. `test_scope_error_identity.py` itself calls `reload`, so it gets rewritten too.

**Files:**
- Rewrite: `probe/tests/test_scope_error_identity.py`
- Modify: `probe/tests/test_project_timezone.py:17,78-90`
- Modify: `probe/tests/test_scope_parity.py:44-51` (comment)
- Modify: `probe/main_scripts/scanner_base.py` (`ScopeError` docstring; then mirror)
- Modify: `probe/agent/engine.py` (comment above `except _scanner_base.ScopeError`)

**Interfaces:**
- Consumes: `sb.PROJECT_TZ`, `sb._resolve_project_tz()`, `sb.project_now()`, `sb.ScopeGuard`, `sb.ScopeError`.
- Produces: guard test `TestNoReload.test_no_test_reloads_a_module`.

- [ ] **Step 1: Write the failing guard**

Replace the entire content of `probe/tests/test_scope_error_identity.py` with:

```python
"""
ScopeError is a ValueError, and nothing in the suite may reload a module.

`importlib.reload()` rebinds every class in a module to a NEW object. A handler
or `pytest.raises` holding a name bound before the reload then matches a class
nothing raises any more — the fresh class is not a subclass of the stale one,
so no choice of base class can fix it. The hazard is removed at its source:
the suite does not reload, and the guard below keeps it that way.

The ValueError base stays for what it says: a boundary that is not an IP or
CIDR is a bad value, as ipaddress itself reports. Every handler around a scope
call fails closed, so a wider catch changes which branch reports a refusal,
never whether a target gets scanned — TestTheGateStillRefuses pins that.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from scanner import scanner_base as sb

TESTS_DIR = Path(__file__).resolve().parent


class TestNoReload:
    def test_scope_error_is_a_value_error(self):
        assert issubclass(sb.ScopeError, ValueError)

    def test_no_test_reloads_a_module(self):
        offenders = []
        for path in sorted(TESTS_DIR.glob("test_*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                fn = node.func
                name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
                if name == "reload":
                    offenders.append(f"{path.name}:{node.lineno}")
        assert offenders == [], (
            "reload rebinds classes and breaks every name bound before it; "
            f"patch the module attribute instead: {offenders}")


class TestTheGateStillRefuses:
    """A widened catch must not widen the SCOPE. These assert the refusal
    itself, independent of which handler reports it."""

    def test_out_of_scope_target_is_still_refused(self):
        guard = sb.ScopeGuard.from_list(["10.0.0.0/24"])
        assert guard.in_scope("192.168.1.1") is False
        with pytest.raises(sb.ScopeError):
            guard.assert_in_scope("192.168.1.1")

    def test_strict_mode_still_rejects_a_malformed_boundary(self):
        with pytest.raises(sb.ScopeError, match="10.0.0.0/244"):
            sb.ScopeGuard.from_list(["10.0.0.0/244"], strict=True)

    def test_strict_mode_still_rejects_a_malformed_exclusion(self):
        """The dangerous direction: a dropped exclusion SCANS the host the
        operator carved out."""
        with pytest.raises(sb.ScopeError, match="10.0.0.5/33"):
            sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=["10.0.0.5/33"], strict=True)

    def test_an_excluded_host_is_still_out_of_scope(self):
        guard = sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=["10.0.0.5"])
        assert guard.in_scope("10.0.0.5") is False
        assert guard.in_scope("10.0.0.6") is True
```

- [ ] **Step 2: Run it to verify it fails on the real offender**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_scope_error_identity.py -q 2>&1 | grep -E "offenders|failed|passed" | tail -2
```

Expected: 1 failed, listing `test_project_timezone.py:81`, `:83`, `:88`, `:90`.

- [ ] **Step 3: Patch the timezone instead of reloading**

In `probe/tests/test_project_timezone.py`, delete the line `import importlib`, and replace the two reloading tests:

```python
    def test_vedha_tz_overrides_the_default(self, monkeypatch):
        monkeypatch.setenv("VEDHA_TZ", "UTC")
        assert importlib.reload(sb).project_now().utcoffset() == timedelta(0)
        monkeypatch.delenv("VEDHA_TZ")
        importlib.reload(sb)            # restore for the rest of the session

    def test_unknown_zone_falls_back_without_crashing(self, monkeypatch):
        """A bad VEDHA_TZ must never take a scan down mid-engagement."""
        monkeypatch.setenv("VEDHA_TZ", "Not/AZone")
        assert importlib.reload(sb).project_now().tzinfo is not None
        monkeypatch.delenv("VEDHA_TZ")
        importlib.reload(sb)
```

with:

```python
    def test_vedha_tz_overrides_the_default(self, monkeypatch):
        monkeypatch.setenv("VEDHA_TZ", "UTC")
        monkeypatch.setattr(sb, "PROJECT_TZ", sb._resolve_project_tz())
        assert sb.project_now().utcoffset() == timedelta(0)

    def test_unknown_zone_falls_back_without_crashing(self, monkeypatch):
        """A bad VEDHA_TZ must never take a scan down mid-engagement."""
        monkeypatch.setenv("VEDHA_TZ", "Not/AZone")
        monkeypatch.setattr(sb, "PROJECT_TZ", sb._resolve_project_tz())
        assert sb.project_now().tzinfo is not None
```

(`monkeypatch` restores both the env var and `PROJECT_TZ` after each test.)

- [ ] **Step 4: Run to verify the guard passes**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_scope_error_identity.py tests/test_project_timezone.py -q 2>&1 | tail -1
```

Expected: all passed.

- [ ] **Step 5: Correct the three comments that justify the old approach**

In `probe/main_scripts/scanner_base.py`, replace the `ScopeError` docstring (everything between `class ScopeError(ValueError):` and the class's closing `"""`) so the class reads:

```python
class ScopeError(ValueError):
    """A target or boundary outside the authorized scope. A ValueError because a
    boundary that is not an IP or CIDR is a bad value, as ipaddress reports."""
```

In `probe/agent/engine.py`, replace:

```python
    # Named through the MODULE so the lookup is live. ScopeError subclasses
    # ValueError precisely so a reload of scanner_base cannot make this stop
    # catching, but resolving it late costs nothing and keeps the handler
    # specific — this branch reports invalid_scope, and no other ValueError
    # from that call should borrow the label.
```

with:

```python
    # Specific on purpose: this branch reports invalid_scope, and no other
    # ValueError from that call should borrow the label.
```

In `probe/tests/test_scope_parity.py`, replace the comment block directly above `from scanner import scanner_base as sb` (it begins `# Referenced through the MODULE, never bound at import time.` and ends `# lookups always resolve to the live classes.`) with the single line:

```python
# Referenced through the module, like every scope test.
```

- [ ] **Step 6: Mirror, then run everything that touches scope or time**

```bash
cd "$REPO/probe" && cp main_scripts/scanner_base.py scanner/scanner_base.py \
&& ./.venv/bin/python -m pytest tests/test_scope_error_identity.py tests/test_project_timezone.py tests/test_scope_parity.py tests/test_probe_core.py tests/test_two_tree_parity.py -q 2>&1 | tail -1
```

Expected: all passed.

- [ ] **Step 7: Commit**

```bash
cd "$REPO" && git add probe/tests/test_scope_error_identity.py probe/tests/test_project_timezone.py probe/tests/test_scope_parity.py probe/main_scripts/scanner_base.py probe/scanner/scanner_base.py probe/agent/engine.py && git commit -F- <<'MSG'
fix(tests): stop reloading scanner_base instead of working around it

A ValueError base cannot help a handler bound before a reload: the fresh
class is never a subclass of the stale one. The timezone tests now patch
PROJECT_TZ, and a guard fails if any test calls reload again.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 7: Probe comments — correct false and dated claims

**Why:** `intensity.py` and `test_intensity_envelope.py` say `light`'s 800 pps envelope "never ran". False: approved portal scan requests (`customer_access.build_scan_job`) and API intensity code 1 dispatch `light` with no rate, so those jobs ran at 800 pps. Both cite `port_scanner.py:474` by line number, and one test's name says the opposite of its assertion. The Gate 6 comment uses dated wording.

**Files:**
- Modify: `probe/workflow/intensity.py` (the `light` preset comment)
- Modify: `probe/tests/test_intensity_envelope.py` (module docstring, one docstring, one test name)
- Modify: `probe/workflow/workflow_engine.py` (first sentence of the Gate 6 comment)

**Interfaces:** none (comments and a test name).

- [ ] **Step 1: Correct the `light` preset comment**

In `probe/workflow/intensity.py`, replace:

```python
        # Light TOUCH, not light latency. This preset is what an operator picks
        # for a monitored, production or fragile segment, so it is the quietest
        # envelope in the table, not the fastest.
        #
        # It previously declared 800 pps / concurrency 200 / timeout 1.0. That
        # envelope never actually ran: the launcher overrode all four values on
        # every job, and nothing else selects `light`. It was also the least
        # accurate setting here — port_scanner.py:474 measured rate 300 /
        # concurrency 200 reporting 69 FALSE `filtered` on a real LAN host, all
        # 69 of which resolved `closed` when re-probed at 40 / 10. These are the
        # numbers the launcher had been forcing, i.e. the ones with field use
        # behind them.
```

with:

```python
        # Light TOUCH, not light latency: the preset an operator picks for a
        # monitored, production or fragile segment, so the quietest envelope in
        # the table. It stays well below the point where the reprobe comment in
        # PortScanner.__init__ records a fast sweep (300 pps / concurrency 200)
        # reporting closed ports as `filtered`.
```

- [ ] **Step 2: Correct the test file**

In `probe/tests/test_intensity_envelope.py`, replace the module docstring (from the opening `"""` to the closing `"""` before `from __future__ import annotations`) with:

```python
"""
The intensity preset is the ONLY source of a scan's probe envelope.

The launcher sends nothing but the intensity name, so each preset's rate,
concurrency and timeouts are what actually reach the scanner. Breadth and rate
move in opposite directions: a wide sweep at a quick-sweep rate reports closed
ports as `filtered`, as the reprobe comment in PortScanner.__init__ records.
"""
```

Replace the docstring of `test_no_preset_exceeds_the_measured_false_filtered_threshold`:

```python
        """rate 300 / concurrency 200 measured 69 false `filtered`
        (port_scanner.py:474). No preset may ship at or above that point."""
```

with:

```python
        """rate 300 / concurrency 200 measured 69 false `filtered` (the reprobe
        comment in PortScanner.__init__). No preset may ship at or above it."""
```

Rename `def test_breadth_and_rate_move_together(self):` to `def test_wider_sweeps_probe_more_gently(self):` (body unchanged).

- [ ] **Step 3: Correct the Gate 6 comment**

In `probe/workflow/workflow_engine.py`, replace:

```python
    # Hosts run CONCURRENTLY — the last stage in the pipeline that did not, and
    # the one where it cost the most. A credentialed collection is a key
```

with:

```python
    # Hosts run CONCURRENTLY. A credentialed collection is a key
```

- [ ] **Step 4: Run to verify nothing broke and no false phrase remains**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_intensity_envelope.py tests/test_intensity_budget.py tests/test_gate6_concurrency.py tests/test_stage_fanout_policy.py -q 2>&1 | tail -1
grep -nE "never (once |actually )?ran|port_scanner\.py:474|previously declared" workflow/intensity.py tests/test_intensity_envelope.py || echo "clean"
```

Expected: all passed; `clean`.

- [ ] **Step 5: Commit**

```bash
cd "$REPO" && git add probe/workflow/intensity.py probe/tests/test_intensity_envelope.py probe/workflow/workflow_engine.py && git commit -F- <<'MSG'
docs(probe): correct the claim that light's 800pps envelope never ran

Approved portal scan requests and API intensity code 1 dispatch light
with no rate override, so those jobs did run at 800 pps. Also replaces
line-number citations and a test name that contradicted its assertion.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 8: Frontend — intensity data module, numeric rate, honest copy

**Why:**
- Stealth's copy says "~15 ports", but the probe sweeps 65.
- Aggressive's says "Expect hours per host", but `deep` caps each host at 30 minutes.
- The parity test regex-parses TSX, because `pps` is a display string living inside a React page.
- The test hardcodes its own copy of the manager's alias table, which can drift silently.

**Files:**
- Create: `manager/frontend/lib/scan-intensity.ts`
- Modify: `manager/frontend/app/scan/page.tsx` (remove lines 144–157, add an import, lines 426 and 1130)
- Rewrite: `manager/frontend/tests/scan-intensity.test.ts`

**Interfaces:**
- Consumes: `buildScanLaunchRequest` from `lib/scan-launch.ts`; `_INTENSITY_ALIASES` in `manager/backend/app/routers/agents.py`; presets in `probe/workflow/intensity.py`.
- Produces: `export type Intensity = "stealth" | "normal" | "aggressive"`, `export interface IntensityOption { id; label; rate: number; why; color; angle; sweep }`, `export const INTENSITY: IntensityOption[]`.

- [ ] **Step 1: Write the failing test**

Replace the whole of `manager/frontend/tests/scan-intensity.test.ts` with:

```ts
/* The launcher ships no probe envelope, and the dial describes the envelope
 * the probe actually uses. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { INTENSITY } from "../lib/scan-intensity";
import { buildScanLaunchRequest } from "../lib/scan-launch";

const ENVELOPE = ["rate", "concurrency", "timeout", "disc_timeout"] as const;

function readRepoFile(relative: string): string | null {
  try {
    return readFileSync(join(process.cwd(), "../..", relative), "utf8");
  } catch {
    return null;
  }
}

for (const intensity of ["stealth", "normal", "aggressive"] as const) {
  test(`${intensity} sends intensity only, letting the probe preset supply the envelope`, () => {
    const { params } = buildScanLaunchRequest({
      engagement_id: "eng-1",
      use_case_id: "uc_network_va",
      intensity,
      targets: ["10.0.0.1"],
    });

    assert.equal(params.intensity, intensity);
    for (const knob of ENVELOPE) {
      assert.ok(!(knob in params), `${intensity} must not pin ${knob}`);
    }
  });
}

test("the dial's rate matches the probe preset each UI name maps to", (t) => {
  const agents = readRepoFile("manager/backend/app/routers/agents.py");
  const presets = readRepoFile("probe/workflow/intensity.py");
  if (agents === null || presets === null) return t.skip("manager or probe tree not present");

  const aliasBody = /_INTENSITY_ALIASES\s*=\s*\{([^}]*)\}/.exec(agents)?.[1];
  assert.ok(aliasBody, "_INTENSITY_ALIASES not found in agents.py");
  const alias: Record<string, string> = Object.fromEntries(
    [...aliasBody.matchAll(/"(\w+)":\s*"(\w+)"/g)].map((m) => [m[1], m[2]]),
  );

  for (const option of INTENSITY) {
    const presetName = alias[option.id];
    assert.ok(presetName, `manager has no alias for ${option.id}`);
    const block = presets.split(`"${presetName}": {`)[1]?.split("},")[0];
    assert.ok(block, `no ${presetName} preset in intensity.py`);
    const rate = Number(/"rate":\s*([\d.]+)/.exec(block)?.[1]);
    assert.equal(
      option.rate, rate,
      `dial shows ${option.rate} pps for ${option.id} but ${presetName} probes at ${rate}`,
    );
  }
});

test("dial copy carries no number a test cannot check", () => {
  for (const option of INTENSITY) {
    for (const n of option.why.match(/\d[\d,]*/g) ?? []) {
      assert.equal(n, "65,535", `${option.id} copy claims "${n}", which nothing verifies`);
    }
  }
});

test("an explicit operator override survives the named preset", () => {
  const { params } = buildScanLaunchRequest({
    engagement_id: "eng-1",
    use_case_id: "uc_network_va",
    intensity: "aggressive",
    targets: ["10.0.0.1"],
    params: { rate: 40, concurrency: 10 },
  });

  assert.equal(params.rate, 40);
  assert.equal(params.concurrency, 10);
  assert.equal(params.intensity, "aggressive");
});
```

- [ ] **Step 2: Run it to verify it fails**

```bash
cd "$REPO/manager/frontend" && npx tsx --test tests/scan-intensity.test.ts 2>&1 | grep -iE "cannot find|ERR_MODULE|fail" | head -3
```

Expected: fails — the module `../lib/scan-intensity` cannot be found.

- [ ] **Step 3: Create the data module**

Create `manager/frontend/lib/scan-intensity.ts`:

```ts
/* Display data for the scan-intensity dial. The probe owns the real envelope
   (probe/workflow/intensity.py) and the launcher sends only the name, so
   `rate` must equal the preset's rate — a test enforces it. The dial measures
   HARDNESS, not speed: the widest sweep probes the most gently. */
export type Intensity = "stealth" | "normal" | "aggressive";

export interface IntensityOption {
  id: Intensity;
  label: string;
  rate: number;
  why: string;
  color: string;
  angle: number;
  sweep: string;
}

export const INTENSITY: IntensityOption[] = [
  { id: "stealth",    label: "Stealth",    rate: 50,  color: "#6ee7b7",             angle: -60, sweep: "6.2s",
    why: "Low and slow over a small high-signal port set. Minimizes IDS/IPS triggers and link load — for monitored, production, or fragile segments." },
  { id: "normal",     label: "Normal",     rate: 200, color: "var(--accent)",        angle: 0,   sweep: "3.4s",
    why: "Balanced default. Right for most internal engagements with no special constraints." },
  { id: "aggressive", label: "Aggressive", rate: 150, color: "var(--sev-high-color)", angle: 60,  sweep: "4.2s",
    why: "Exhaustive, not fast: all 65,535 ports, probed patiently so silence means a firewall rather than a rushed probe. Each host runs on a time budget; a large estate takes hours." },
];
```

- [ ] **Step 4: Use it from the page**

In `manager/frontend/app/scan/page.tsx`:

1. Delete the block that starts `/* Scan-intensity presets — the one offensive-security knob operators reason about.` and ends with the `];` closing `const INTENSITY` (currently lines 144–157, including the `type Intensity = ...` line).
2. After the line `import type { ScanLaunchBody } from "../../lib/scan-launch";`, add:

```tsx
import { INTENSITY, type Intensity } from "../../lib/scan-intensity";
```

3. Replace `{active.pps}</span>` with `{active.rate} pps</span>`.
4. Replace `` `${intensityObj.label} · ${intensityObj.pps}` `` with `` `${intensityObj.label} · ${intensityObj.rate} pps` ``.

- [ ] **Step 5: Run the tests and the type check**

```bash
cd "$REPO/manager/frontend" && npx tsx --test tests/scan-intensity.test.ts 2>&1 | grep -E "^ℹ (pass|fail)" && npm test 2>&1 | grep -E "^ℹ (tests|pass|fail)" && npx tsc --noEmit 2>&1 | tail -2
```

Expected: `pass 6`, `fail 0`; full suite `fail 0`; `TypeScript: No errors found` (or no output).

- [ ] **Step 6: Commit**

```bash
cd "$REPO" && git add manager/frontend/lib/scan-intensity.ts manager/frontend/app/scan/page.tsx manager/frontend/tests/scan-intensity.test.ts && git commit -F- <<'MSG'
fix(scan-ui): honest intensity copy; test the dial against real data

Stealth claimed ~15 ports (the probe sweeps 65) and Aggressive claimed
hours per host (deep caps a host at 30 min). The dial data moves to a
module with a numeric rate, and the parity test reads the manager's
alias table instead of copying it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

- [ ] **Step 7: Note the verification gap in the task report**

`/scan` requires login, so the page cannot be rendered in a browser without credentials. Report that it was verified by tests and `tsc` only — do not enter credentials.

---

### Task 9: Manager — pin the UI intensity alias chain

**Why:** The whole P4 fix depends on the manager mapping `aggressive → deep → 3`, `stealth → light → 1`, `normal → standard → 2`. No manager test mentions `aggressive`, so changing `_INTENSITY_ALIASES` would pass every test.

**Files:**
- Modify: `manager/backend/tests/test_enqueue_intensity.py`

**Interfaces:**
- Consumes: `_normalize_intensity_name(value) -> str | None` and `_INTENSITY_NAME_TO_CODE: dict[str, int]` from `app.routers.agents`.
- Produces: `test_ui_intensity_names_reach_the_probe_as_the_right_preset_code`.

- [ ] **Step 1: Write the test**

In the import block at the top of `manager/backend/tests/test_enqueue_intensity.py`, add `_INTENSITY_NAME_TO_CODE,` to the names imported from `app.routers.agents`. Then append:

```python
@pytest.mark.parametrize("ui_name, preset, code", [
    ("stealth", "light", 1),
    ("normal", "standard", 2),
    ("aggressive", "deep", 3),
])
def test_ui_intensity_names_reach_the_probe_as_the_right_preset_code(ui_name, preset, code):
    """The Scanner UI sends stealth/normal/aggressive and no envelope, so this
    mapping alone decides which probe envelope runs."""
    assert _normalize_intensity_name(ui_name) == preset
    assert _INTENSITY_NAME_TO_CODE[preset] == code
```

- [ ] **Step 2: Run it**

```bash
cd "$REPO/manager/backend" && ./.venv/bin/python -m pytest tests/test_enqueue_intensity.py -q 2>&1 | tail -1
```

Expected: all passed. (It pins existing behaviour that was untested.)

- [ ] **Step 3: Prove it can fail — mis-map aggressive, run, restore**

```bash
cd "$REPO/manager/backend" && ./.venv/bin/python - <<'PY'
import pathlib
p = pathlib.Path("app/routers/agents.py"); s = p.read_text()
assert s.count('"aggressive": "deep"') == 1
p.write_text(s.replace('"aggressive": "deep"', '"aggressive": "standard"'))
PY
./.venv/bin/python -m pytest tests/test_enqueue_intensity.py -q -k ui_intensity 2>&1 | tail -1
./.venv/bin/python - <<'PY'
import pathlib
p = pathlib.Path("app/routers/agents.py"); s = p.read_text()
p.write_text(s.replace('"aggressive": "standard"', '"aggressive": "deep"'))
PY
git -C "$REPO" status --short manager/backend/app
```

Expected: `1 failed, 2 passed`, then an **empty** `git status`.

- [ ] **Step 4: Commit**

```bash
cd "$REPO" && git add manager/backend/tests/test_enqueue_intensity.py && git commit -F- <<'MSG'
test(enqueue): pin the UI intensity aliases to their probe preset codes

The launcher sends only the intensity name now, so this mapping alone
decides which envelope runs, and nothing tested it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 10: CI — run the new tests, and add a frontend workflow

**Why:** Five new probe test files exist but no workflow names them. The frontend suite — including the dial parity test — runs in no workflow at all. Tests go to the workflow whose `paths:` cover the code they exercise.

**Files:**
- Modify: `.github/workflows/agent-ci.yml` (test list)
- Modify: `.github/workflows/scanner-accuracy.yml` (test list)
- Create: `.github/workflows/frontend-ci.yml`

**Interfaces:**
- Consumes: Task 1 (`pytest-asyncio` installed); test files from Tasks 2–9.
- Produces: CI coverage for all tests added in `13f1170` and this plan.

- [ ] **Step 1: Show what is unwired (the failing check)**

```bash
cd "$REPO" && for t in test_intensity_envelope test_scope_error_identity test_kernel_admission test_gate6_concurrency test_syn_recv_interleave; do grep -q "$t" .github/workflows/*.yml && echo "wired:   $t" || echo "MISSING: $t"; done
```

Expected: five `MISSING:` lines.

- [ ] **Step 2: Add the agent test to `agent-ci.yml`**

Replace:

```yaml
          tests/test_infeasible_job_admission.py
```

with:

```yaml
          tests/test_infeasible_job_admission.py tests/test_kernel_admission.py
```

- [ ] **Step 3: Add the scanner/workflow tests to `scanner-accuracy.yml`**

Replace the last line of the pytest list:

```yaml
            tests/test_rate_limiter_throughput.py
```

with:

```yaml
            tests/test_rate_limiter_throughput.py \
            tests/test_syn_recv_interleave.py \
            tests/test_scope_error_identity.py \
            tests/test_intensity_envelope.py \
            tests/test_gate6_concurrency.py
```

- [ ] **Step 4: Create `frontend-ci.yml`**

Create `.github/workflows/frontend-ci.yml`:

```yaml
name: frontend-ci

# The dial parity test reads probe/workflow/intensity.py and the manager's
# alias table, so changes to either also run it.
on:
  push:
    branches: [main]
    paths:
      - 'manager/frontend/**'
      - 'probe/workflow/intensity.py'
      - 'manager/backend/app/routers/agents.py'
      - '.github/workflows/frontend-ci.yml'
  pull_request:
    paths:
      - 'manager/frontend/**'
      - 'probe/workflow/intensity.py'
      - 'manager/backend/app/routers/agents.py'
      - '.github/workflows/frontend-ci.yml'
  workflow_dispatch: {}

concurrency:
  group: frontend-ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    defaults:
      run:
        working-directory: manager/frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          cache: npm
          cache-dependency-path: manager/frontend/package-lock.json
      - run: npm ci
      - run: npm test
      - run: npx tsc --noEmit
```

- [ ] **Step 5: Verify**

GitHub Actions cannot run locally, so check what can be checked: YAML parses, every name resolves, and each list passes exactly as CI will run it.

```bash
cd "$REPO" && manager/backend/.venv/bin/python -c "import yaml; [yaml.safe_load(open(f'.github/workflows/{n}.yml')) for n in ('agent-ci','scanner-accuracy','frontend-ci')]; print('yaml ok')"
for t in test_intensity_envelope test_scope_error_identity test_kernel_admission test_gate6_concurrency test_syn_recv_interleave; do grep -q "$t" .github/workflows/*.yml && echo "wired:   $t" || echo "MISSING: $t"; done
cd "$REPO/probe" && ./.venv/bin/python -m pytest -q tests/test_syn_recv_interleave.py tests/test_scope_error_identity.py tests/test_intensity_envelope.py tests/test_gate6_concurrency.py tests/test_kernel_admission.py 2>&1 | tail -1
cd "$REPO/manager/frontend" && npm test 2>&1 | grep -E "^ℹ fail" && npx tsc --noEmit 2>&1 | tail -1
```

Expected: `yaml ok`; five `wired:` lines; `... passed`; `ℹ fail 0`; no type errors.

- [ ] **Step 6: Commit**

```bash
cd "$REPO" && git add .github/workflows/agent-ci.yml .github/workflows/scanner-accuracy.yml .github/workflows/frontend-ci.yml && git commit -F- <<'MSG'
ci: run the new probe tests and add a frontend workflow

Five probe test files were never named in a workflow, so CI never ran
them, and the frontend suite ran nowhere. frontend-ci also triggers on
the probe preset and manager alias files its parity test reads.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 11: Handoff doc — correct the record

**Why:** `agressive-plan.md` repeats every false claim the review found. The pushed commit message of `13f1170` repeats some of them too, but rewriting published `main` history is not worth it — this document is the corrected record.

**Files:**
- Modify: `agressive-plan.md`

**Interfaces:**
- Consumes: facts established by Tasks 1–10 (`gate_measured`, `pytest-asyncio`, no-reload guard).
- Produces: nothing code-facing.

- [ ] **Step 1: Apply exact replacements (each asserted unique)**

```bash
cd "$REPO" && ./manager/backend/.venv/bin/python - <<'PY'
import pathlib
p = pathlib.Path("agressive-plan.md"); s = p.read_text()

PAIRS = [
("Nothing committed — all work is uncommitted on `main`.",
 "Committed to `main` as 13f1170 (2026-09-22). A review on 2026-09-23 found\nerrors in this document — see §6 \"Review corrections (2026-09-23)\"."),

("2. **D1 (the SYN scanner's serialized send/recv) is real, was measured at ~92%\n   reply loss on a wide sweep, and is fixed.** It alone explains *\"aggressive\n   returns no results.\"* It also turned out to be verifiable after all — by\n   faking the kernel rather than the scanner. See §7 P2.",
 "2. **D1 (the SYN scanner's serialized send/recv) is real and fixed**, proven\n   against a simulated kernel but not yet on Linux. It is **not** established\n   as the cause of *\"aggressive returns no results\"*: both Docker deployments\n   ship `cap_drop: ALL`, so the SYN scanner is unused by default. P1's\n   `SYN scan: yes|no` answer decides that. See §7 P2."),

("> and the collision ran in **both** directions — `light` never once ran its\n> declared 800 pps either.",
 "> and the collision ran in **both** directions — Stealth's copy promised\n> 50 pps while `light` declared 800."),

("> **Still open.** This collision is NOT fixed. See pending task **P4**.\n\n", ""),

("| \"`light` is the fast triage preset\" | Its envelope **never ran once.** The UI, its only caller, always overrode all four values |",
 "| \"`light` is the fast triage preset\" | The UI always overrode it, but approved portal scan requests and API intensity code 1 ran it at 800 pps — the retune slowed those jobs 16× |"),

("| \"`SO_RCVBUF` 4 MB ≈ 40,000 packets\" | **~5,000.** Linux charges `skb->truesize` (~768 B/segment), not payload bytes |",
 "| \"`SO_RCVBUF` 4 MB ≈ 40,000 packets\" | **A few hundred.** Plain `SO_RCVBUF` is clamped to `net.core.rmem_max` (~208 KB default, doubled), and the kernel charges `skb->truesize` per packet |"),

("**D1 — fixed, and it is almost certainly the reported symptom.**",
 "**D1 — fixed. Whether it is the reported symptom is unknown until P1.**"),

("The original estimate of the ceiling was too generous. `SO_RCVBUF` is 4 MB, but\nLinux charges **`skb->truesize`** — roughly 768 B for a 40-byte TCP segment,\nnot 40 — so the buffer holds on the order of **5,000 packets, not 40,000**. A\n65,535-port sweep of a mostly-closed host answers with 65,535 RSTs. About 92%\nof them are discarded by the kernel **with no error**, leaving ports that\nanswered reported as `filtered`.",
 "The buffer is far smaller than the 4 MB the code requests: plain `SO_RCVBUF`\nis clamped to `net.core.rmem_max` (~208 KB by default, which the kernel\ndoubles), and the kernel charges **`skb->truesize`** per packet rather than\npayload bytes, so it holds a few hundred replies. A 65,535-port sweep of a\nmostly-closed host answers with 65,535 RSTs; nearly all would be discarded\n**with no error**, leaving ports that answered reported as `filtered`. (This is\narithmetic, not a measurement.)"),

("helps. And `deep` is exactly the configuration that routes the port stage here\n(65,535 ports > the 1,024 connect/SYN threshold). *\"Aggressive returns no\nresults\"* is fully explained by this alone.",
 "helps. `deep` routes the port stage here when SYN is available (65,535 ports >\nthe 4,096 `_SYN_PORT_THRESHOLD` in `engine.py`). But both Docker deployments\nship `cap_drop: ALL`, so by default the SYN scanner is not used at all and this\ndefect cannot be the reported symptom there."),

("**It IS verified, contrary to the earlier assessment.** What was blocked was\nnever the loop — it was the packet bytes.",
 "**The loop is verified; the packets are not.** What was blocked was never the\nloop — it was the packet bytes."),

("Rather than add a fourth preset, `light` was retuned to the envelope its only\ncaller had always forced (50 / 20 / 4.0 / 2.0). The evidence for that:",
 "Rather than add a fourth preset, `light` was retuned to the envelope the UI had\nalways forced (50 / 20 / 4.0 / 2.0). The evidence for that:"),

("- `light`'s declared 800 pps / concurrency 200 / timeout 1.0 / `retries: 0`\n  **never ran a single scan.** The launcher overrode all four on every job,\n  nothing in `use_cases.py` defaults to `light`, and no test pinned its\n  envelope — only its breadth, budget and first-pass profile.",
 "- **Correction (review, 2026-09-23):** an earlier version said `light`'s 800 pps\n  envelope had no callers. Wrong: approved portal scan requests\n  (`customer_access.build_scan_job`) and API intensity code 1 dispatch `light`\n  with no rate, so those jobs ran at 800 pps and are now 16× slower in the port\n  stage. A behaviour change, not a no-op."),

("and `TestTheGateStillRefuses` pins exactly that. The \"always reference it\nthrough the module\" convention is no longer load-bearing.",
 "and `TestTheGateStillRefuses` pins exactly that. **Correction (review):** the\n`ValueError` base did not defuse the reload hazard — a fresh class is never a\nsubclass of the stale one. The fix was removing `importlib.reload` from the\nsuite, now enforced by a guard test."),

("All 21 new test files are wired into one of the two.",
 "A test file runs in CI only if **named** in a workflow's pytest list — the\n`paths:` trigger alone does not run it. Both workflows install\n`pytest-asyncio`; without it every `@pytest.mark.asyncio` test fails under\npytest 9. `frontend-ci.yml` runs the frontend suite and `tsc`."),

("## 7. Pending work",
 "### Review corrections (2026-09-23)\n\nA two-axis review of 13f1170 found, and follow-up commits fixed:\n\n- **CI:** neither probe workflow installed `pytest-asyncio`, so `scanner-accuracy`\n  (push to main) failed 15 tests and `agent-ci` would fail 27. Five new test files\n  were never named in a workflow. The frontend suite ran nowhere.\n- **Tests that could not fail:** the SYN bad-cookie test wrote the checksum field\n  instead of the ack and forged an RST equal to the genuine answer.\n- **`run_stats.kernel.measured`** was always true; replaced by `gate_measured`,\n  true only when every blocking ceiling was read.\n- **UI copy:** Stealth claimed ~15 ports (65 swept); Aggressive claimed hours per\n  host (30 min cap).\n- **Kernel gate behaviour worth knowing:** it compares demand to *live* free\n  conntrack headroom, so a refusal can come and go with host load, and `standard`\n  (200 pps) is refused before `deep` (150 pps).\n- **Still unverified:** D1 on real packets, and whether any probe reporting the\n  symptom had `NET_RAW` at all — both P1.\n\n## 7. Pending work"),
]

for old, new in PAIRS:
    n = s.count(old)
    assert n == 1, f"expected exactly 1 match, found {n}: {old[:70]!r}"
    s = s.replace(old, new)
p.write_text(s)
print(f"applied {len(PAIRS)} corrections")
PY
```

Expected: `applied 15 corrections`. If an assertion fires, the doc changed since this plan was written — read the named passage and adapt the pair; do not loosen the assertion.

- [ ] **Step 2: Verify no false claim survives**

```bash
cd "$REPO" && grep -nE "never (once |actually )?ran|never ran a single|measured at ~92|alone explains|fully explained by this alone|1,024 connect|holds on the order of|IS verified|no longer load-bearing|Nothing committed|All 21 new test files" agressive-plan.md || echo "clean"
```

Expected: `clean`

- [ ] **Step 3: Commit**

```bash
cd "$REPO" && git add agressive-plan.md && git commit -F- <<'MSG'
docs: correct the aggressive-scan handoff after review

Removes claims the review disproved: light's envelope never running, D1
explaining the symptom, a measured 92% loss, a 4 MB/5,000-packet buffer,
the 1,024 threshold, and the ScopeError fix defusing the reload hazard.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 12: Land Tasks 2–11 through a pull request

**Why:** `agent-ci` triggers only on `pull_request`, so a direct push to `main` skips it entirely — that is how `13f1170` shipped without it running.

- [ ] **Step 1: Rebase on the merged Task 1 and run all three suites**

```bash
cd "$REPO" && git fetch origin && git rebase origin/main
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/ -q 2>&1 | tail -1
cd "$REPO/manager/backend" && ./.venv/bin/python -m pytest -q 2>&1 | tail -1
cd "$REPO/manager/frontend" && npm test 2>&1 | grep -E "^ℹ (tests|fail)" && npx tsc --noEmit 2>&1 | tail -1
```

Expected: probe ≥ 2372 passed, 0 failed; manager ≥ 1272 passed, 0 failed; frontend `fail 0`; no type errors.

- [ ] **Step 2: Secret scan the diff**

```bash
cd "$REPO" && git diff origin/main...HEAD | grep -nE "BEGIN [A-Z ]*PRIVATE KEY|eyJ[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}" || echo "no secrets"
```

Expected: `no secrets`

- [ ] **Step 3: Push and open the PR — ASK THE USER FIRST**

```bash
cd "$REPO" && git push -u origin fix/review-followups
```

Open `https://github.com/Rutikm18/Project-Vedha/compare/main...fix/review-followups?expand=1`. End the PR description with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

- [ ] **Step 4: Merge only when `agent-ci` (all three OSes), `scanner-accuracy`, `frontend-ci` and `secret-scan` are green — ASK THE USER FIRST**

---

## Added during execution (2026-09-23): user-reported issues

Two issues reported mid-execution, both root-caused from last night's run (jobs `7a3af813` A, `4f70f4c1` B, `b1db9b08` C on probe `scanner-probe-01`):

- **"Scans launched together run at the same time."** A (pushed over the WebSocket) and B (claimed by the HTTP poll) executed concurrently on one probe. Root cause: `_run_ws_push_loop` created the busy-state, lock, heartbeat task and poll task **per connection**, and cancelled the tasks only when the connection ended normally. The API restart at 01:03:23 killed the socket with an exception, so the old poll task survived with state nothing updated. It claimed and ran B while the new connection ran A. Reproduced: `repro_reconnect_orphan.py` gives peak concurrency 2, and the unmodified flow gives 1. The manager's poll endpoint also hands a job to a probe that already holds a running one (the push path is correctly gated).
- **"Aggressive scan throws an error."** `job cannot finish: 254 host(s) x 65535 port(s) ... 30.8h, against a 2.0h ceiling`. Root cause: `_refuse_if_infeasible` sizes `deep` by its full 65,535 ports, but `deep` is two-phase — only the first pass (1,145 ports on `it`) must finish, and the tail is budgeted per host and truncates to `not_scanned` by design. For a /24 the first pass takes 32 minutes and fits. Restoring `deep`'s real 150 pps in P4 cut the aggressive host limit from 65 to 16.

**Execution order from here:** 8 → 9 → 13 → 14 → 15 → 10 → 11 → 12. Task 10 must also wire the new test files; Task 11 must also record these root causes.

### Task 13: Probe — a dropped WebSocket must not leave a second job-claiming loop

**Files:**
- Modify: `probe/agent/agent.py` (`_run_ws_push_loop`, `_ws_http_poll_fallback`; add `_end_ws_session`)
- Create: `probe/tests/test_ws_reconnect_serialization.py`

**Interfaces:**
- Consumes: `_ws_heartbeat_sender`, `_ws_run_job`, `_ws_stage_job_offer`, `_ws_probe_is_free` (unchanged).
- Produces: `_ws_http_poll_fallback(ws, transport, runner, agent_id, spool, interval, job_lock, job_state, stop: asyncio.Event | None = None)` (new optional kwarg, positional args unchanged); `_end_ws_session(hb_task, stop_polling) -> None`; `_ws_connection_loop(...)` (the old body of `_run_ws_push_loop`, plus a `pollers` parameter). The `_run_ws_push_loop` signature is unchanged.

- [ ] **Step 1: Write the failing tests**

Create `probe/tests/test_ws_reconnect_serialization.py`:

```python
"""
A dropped WebSocket must not leave a second job-claiming loop behind.

The probe runs one job at a time. The push loop kept that promise per
CONNECTION: each connection had its own busy-state, lock, heartbeat task and
HTTP poll task, and the tasks were cleaned up only when the connection ended
normally. A connection that died with an exception — an API restart does
exactly that — left its poll task running with state nothing updated. That
task kept polling, believed the probe was idle, and ran the next job alongside
whatever the new connection was running.

A poll task that is mid-job must be told to stop, not cancelled: cancelling
the coroutine awaiting the scan's worker thread would mark the probe idle
while the scan kept going.
"""
from __future__ import annotations

import asyncio
import json
import threading
import time

import websockets.exceptions

from agent import agent as ag

JOB_SECONDS = 1.2


class _Clock:
    def __init__(self):
        self.t0 = time.monotonic()
        self.events: list[tuple[float, str]] = []

    def log(self, msg):
        self.events.append((round(time.monotonic() - self.t0, 2), msg))


class _WS:
    """A fake connection. With `die_after`, iterating it raises the error a
    server that went away produces."""

    def __init__(self, *, die_after=None):
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.acks: list[dict] = []
        self.die_after = die_after

    async def send(self, raw):
        msg = json.loads(raw)
        if msg.get("type") == "job_ack":
            self.acks.append(msg)
            if msg["accepted"]:
                await self.inbox.put(json.dumps({
                    "type": "job_claim", "job_id": msg["job_id"], "claimed": True,
                    "attempt_id": "att-" + msg["job_id"], "fence": 1}))

    async def recv(self):
        return await self.inbox.get()

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.die_after is not None:
            await asyncio.sleep(self.die_after)
            raise websockets.exceptions.ConnectionClosedError(None, None)
        return await self.inbox.get()

    async def close(self):
        pass


class _Spool:
    spool_count = 0
    at_capacity = False


class _Transport:
    agent_token = "t"

    def __init__(self, connections):
        self.connections = list(connections)
        self.pollable: list[dict] = []
        self.poll_times: list[float] = []

    async def connect_ws(self):
        ws = self.connections.pop(0)
        await ws.inbox.put(json.dumps(
            {"type": "hello_ok", "features": ["atomic_job_claim_v1"]}))
        return ws

    def poll_jobs(self, limit=1):
        self.poll_times.append(time.monotonic())
        return [self.pollable.pop(0)] if self.pollable else []

    def heartbeat_ex(self, *a, **k):
        return ag.HEARTBEAT_OK

    def submit_result(self, *a, **k):
        return True


class _Runner:
    def __init__(self, clock):
        self.clock = clock
        self.live = 0
        self.peak = 0
        self._lock = threading.Lock()

    def run_job(self, job, agent_id, cancellation_event=None):
        with self._lock:
            self.live += 1
            self.peak = max(self.peak, self.live)
        self.clock.log(f"start {job['job_id']}")
        time.sleep(JOB_SECONDS)
        with self._lock:
            self.live -= 1
        self.clock.log(f"end {job['job_id']}")

        class _Result:
            error = None
        return _Result()


def _quiet(monkeypatch):
    monkeypatch.setattr(ag, "say", lambda *a, **k: None)
    monkeypatch.setattr(ag, "_result_summary", lambda r: "ok")
    monkeypatch.setattr(ag, "WS_RECONNECT_BACKOFF_MIN", 0.1)


async def _stop(loop_task):
    loop_task.cancel()
    try:
        await loop_task
    except asyncio.CancelledError:
        pass


def test_a_reconnect_does_not_leave_a_second_claimer(monkeypatch):
    """The field sequence: the socket drops, the probe reconnects, job A is
    pushed, and job B becomes pollable while A runs. B must wait for A."""
    _quiet(monkeypatch)
    clock = _Clock()
    runner = _Runner(clock)
    live_ws = _WS()
    transport = _Transport([_WS(die_after=0.05), live_ws])

    async def scenario():
        loop = asyncio.create_task(ag._run_ws_push_loop(
            transport, runner, "agent-1", _Spool(), 30, 1))
        await asyncio.sleep(1.5)
        await live_ws.inbox.put(json.dumps(
            {"type": "job_push", "job": {"job_id": "A", "params": {}}}))
        await asyncio.sleep(0.3)
        transport.pollable.append({"job_id": "B", "params": {}})
        await asyncio.sleep(JOB_SECONDS * 2 + 2.5)
        await _stop(loop)

    asyncio.run(scenario())
    assert runner.peak == 1, clock.events
    starts = {m.split()[1]: t for t, m in clock.events if m.startswith("start")}
    ends = {m.split()[1]: t for t, m in clock.events if m.startswith("end")}
    assert set(starts) == {"A", "B"}, clock.events
    assert starts["B"] >= ends["A"], clock.events


def test_a_job_running_when_the_socket_drops_still_makes_the_probe_busy(monkeypatch):
    """The poll fallback is running B when the socket dies. The next
    connection must see a busy probe and decline a push for A."""
    _quiet(monkeypatch)
    clock = _Clock()
    runner = _Runner(clock)
    live_ws = _WS()
    transport = _Transport([_WS(die_after=1.6), live_ws])
    transport.pollable.append({"job_id": "B", "params": {}})

    async def scenario():
        loop = asyncio.create_task(ag._run_ws_push_loop(
            transport, runner, "agent-1", _Spool(), 30, 1))
        await asyncio.sleep(2.0)       # B taken at ~1s, socket died at ~1.6s
        await live_ws.inbox.put(json.dumps(
            {"type": "job_push", "job": {"job_id": "A", "params": {}}}))
        await asyncio.sleep(JOB_SECONDS + 1.5)
        await _stop(loop)

    asyncio.run(scenario())
    assert runner.peak == 1, clock.events
    assert live_ws.acks, "the push for A was never answered"
    assert live_ws.acks[0]["job_id"] == "A"
    assert live_ws.acks[0]["accepted"] is False, live_ws.acks


def test_reconnects_do_not_multiply_the_pollers(monkeypatch):
    """Every leaked poll task added another claimer — and another request
    against the manager every interval."""
    _quiet(monkeypatch)
    clock = _Clock()
    transport = _Transport([_WS(die_after=0.05) for _ in range(3)] + [_WS()])

    async def scenario():
        loop = asyncio.create_task(ag._run_ws_push_loop(
            transport, _Runner(clock), "agent-1", _Spool(), 30, 1))
        await asyncio.sleep(1.5)
        before = len(transport.poll_times)
        await asyncio.sleep(3.0)
        window = len(transport.poll_times) - before
        await _stop(loop)
        return window

    window = asyncio.run(scenario())
    assert window <= 4, f"{window} polls in 3s at a 1s interval — pollers are piling up"
```

- [ ] **Step 2: Run them to verify they fail**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_ws_reconnect_serialization.py -q 2>&1 | tail -6
```

Expected: 3 failed. The first shows `peak == 2`, the second `accepted` is `True`, and the third reports roughly 12 polls in 3s.

- [ ] **Step 3: Split `_run_ws_push_loop` so leftover pollers are awaited before falling back**

Rename the existing `async def _run_ws_push_loop(` definition line to `async def _ws_connection_loop(` and give it one more parameter, so its signature reads:

```python
async def _ws_connection_loop(
    transport: "Transport",
    runner,
    agent_id: str,
    spool,
    heartbeat_interval: int,
    poll_interval: int,
    pollers: set,
) -> bool:
```

Keep its docstring. Then insert this new function immediately **above** it:

```python
async def _run_ws_push_loop(
    transport: "Transport",
    runner,
    agent_id: str,
    spool,
    heartbeat_interval: int,
    poll_interval: int,
) -> bool:
    """Persistent WebSocket push loop.

    Returns False if WebSocket is unavailable (caller should fall back to
    HTTP polling). Returns True only on clean shutdown or unrecoverable error
    (caller should exit).
    """
    pollers: set = set()
    result = await _ws_connection_loop(
        transport, runner, agent_id, spool,
        heartbeat_interval, poll_interval, pollers,
    )
    # A poll task may still be finishing a job it claimed. Handing the caller
    # (the HTTP poll loop) a probe that looks idle mid-scan would start a
    # second job beside it.
    await asyncio.gather(*pollers, return_exceptions=True)
    return result
```

- [ ] **Step 4: Make the busy-state process-wide and stop tasks on every exit path**

Inside `_ws_connection_loop`, replace:

```python
    backoff = WS_RECONNECT_BACKOFF_MIN
    auth_failures = 0

    while True:
        try:
            say("Connecting via WebSocket (push mode)...")
```

with:

```python
    backoff = WS_RECONNECT_BACKOFF_MIN
    auth_failures = 0
    # The probe's one-job-at-a-time state belongs to the PROCESS, not to a
    # connection: a poll task outliving its socket must still see — and
    # update — the same busy flag and lock as every later connection.
    #   current_job_id — a job is RUNNING
    #   pending_job    — an offer is acked, awaiting the manager's claim
    #   pending_since  — when it was staged, so it can expire
    #   claiming       — the fallback is mid-claim and must not be raced
    job_state = {"current_job_id": None, "pending_job": None,
                 "pending_since": None, "claiming": False}
    job_lock = asyncio.Lock()

    while True:
        hb_task = None
        stop_polling = asyncio.Event()
        try:
            say("Connecting via WebSocket (push mode)...")
```

Replace:

```python
            # ── Start heartbeat + HTTP poll fallback tasks ────────────────
            # WebSocket pushes are process-local on the manager. With multiple
            # API workers a launch request can land on a different worker than
            # the probe's WS connection, so keep polling as a safety net.
            # The probe's one-job-at-a-time state, shared by the receive loop
            # and the poll fallback:
            #   current_job_id — a job is RUNNING
            #   pending_job    — an offer is acked, awaiting the manager's claim
            #   pending_since  — when it was staged, so it can expire
            #   claiming       — the fallback is mid-claim and must not be raced
            job_state = {"current_job_id": None, "pending_job": None,
                         "pending_since": None, "claiming": False}
            job_lock = asyncio.Lock()
            hb_task = asyncio.create_task(
                _ws_heartbeat_sender(ws, agent_id, heartbeat_interval,
                                     job_state, spool),
            )
            poll_task = asyncio.create_task(
                _ws_http_poll_fallback(
                    ws, transport, runner, agent_id, spool,
                    poll_interval, job_lock, job_state,
                ),
            )
```

with:

```python
            # ── Start heartbeat + HTTP poll fallback tasks ────────────────
            # WebSocket pushes are process-local on the manager. With multiple
            # API workers a launch request can land on a different worker than
            # the probe's WS connection, so keep polling as a safety net.
            #
            # An offer staged on an earlier connection can never be confirmed:
            # its claim frame would have arrived on the socket that died.
            job_state["pending_job"] = None
            job_state["pending_since"] = None
            hb_task = asyncio.create_task(
                _ws_heartbeat_sender(ws, agent_id, heartbeat_interval,
                                     job_state, spool),
            )
            poller = asyncio.create_task(
                _ws_http_poll_fallback(
                    ws, transport, runner, agent_id, spool,
                    poll_interval, job_lock, job_state, stop=stop_polling,
                ),
            )
            pollers.add(poller)
            poller.add_done_callback(pollers.discard)
```

Delete the normal-exit cleanup block (the `finally` below replaces it on every path):

```python
            # Loop exited (ws closed by manager)
            for task in (hb_task, poll_task):
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
```

Then add a `finally:` to the same `try`. It goes directly after the last `except` branch's final line and before `# Exponential backoff`, at the `try`'s indentation:

```python
            say(f"WebSocket error: {type(exc).__name__}: {exc} — reconnecting in {backoff:.0f}s...", 1)
        finally:
            await _end_ws_session(hb_task, stop_polling)

        # Exponential backoff
```

- [ ] **Step 5: Add `_end_ws_session` and make the poll loop stoppable**

Add this function directly above `def _ws_expire_stale_offer`:

```python
async def _end_ws_session(hb_task, stop_polling: asyncio.Event) -> None:
    """Stop one connection's background work, on every exit path.

    The heartbeat sender only writes to this connection, so it is cancelled.
    The poll fallback is only told to stop: it may be running a job in a
    worker thread, and cancelling the coroutine that awaits that thread would
    clear current_job_id while the scan kept going. It exits once any job it
    holds has finished.
    """
    stop_polling.set()
    if hb_task is None:
        return
    hb_task.cancel()
    try:
        await hb_task
    except asyncio.CancelledError:
        pass
```

In `_ws_http_poll_fallback`, add the parameter `stop: asyncio.Event | None = None,` after `job_state: dict,`. Then replace:

```python
    while True:
        await asyncio.sleep(max(1, interval))
        # An offer the manager never confirmed must not strand this loop.
```

with:

```python
    stop = stop or asyncio.Event()
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=max(1, interval))
            return                  # the connection ended while this was idle
        except asyncio.TimeoutError:
            pass
        # An offer the manager never confirmed must not strand this loop.
```

- [ ] **Step 6: Run the new tests and every test that drives these loops**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_ws_reconnect_serialization.py tests/test_ws_claim_race.py tests/test_spool_backpressure.py tests/test_lease_patience.py -q 2>&1 | tail -2
```

Expected: all passed.

- [ ] **Step 7: Run the full probe suite once**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/ -q 2>&1 | tail -1
```

Expected: 0 failed.

- [ ] **Step 8: Commit**

```bash
cd "$REPO" && git add probe/agent/agent.py probe/tests/test_ws_reconnect_serialization.py && git commit -F- <<'MSG'
fix(probe): a dropped WebSocket no longer leaves a second job claimer

The busy-state, lock and poll task were per connection and cleaned up
only on a normal close. An API restart killed the socket with an
exception, so the old poll task kept claiming work against a lock nobody
else held and ran a second scan beside the first. The state is now
process-wide, and every exit path stops the connection's tasks; a poll
task mid-job is told to stop instead of cancelled, so the probe cannot
look idle while a scan is still running.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 14: Manager — never hand a second job to a probe that holds a running one

**Why:** The queue should hold even when a probe misbehaves: a leaked poller like Task 13's, a probe build that predates that fix, or two processes sharing one identity. The push path already skips busy probes. The poll endpoint claims any pending job for whoever asks. The authority here is the job's lease, not the probe's self-reported status, because the status can be wrong: in the field, the new connection reported "online" while the leaked poller was scanning.

**Files:**
- Modify: `manager/backend/app/routers/agents.py` (`get_agent_jobs`)
- Modify: `manager/backend/tests/test_agents.py` (`TestGetAgentJobs`)

**Interfaces:**
- Consumes: `ScanJob.agent_id` (String column, so compare with `str(agent_id)`), `ScanJob.status`, `ScanJob.lease_expires_at`, `ScanJobStatus.running`, `func` (already imported from sqlalchemy).
- Produces: `get_agent_jobs` returns `[]` for an agent holding a running job with an unexpired lease. It issues one extra query, immediately after the agent lookup.

- [ ] **Step 1: Write the failing test**

Add to `class TestGetAgentJobs` in `manager/backend/tests/test_agents.py`:

```python
    @pytest.mark.asyncio
    async def test_a_probe_holding_a_live_job_is_handed_nothing(self):
        """One scan per probe, enforced at the queue: a probe that still holds
        a running job with an unexpired lease gets no second job, whatever it
        believes about itself."""
        agent = SimpleNamespace(
            id=uuid.uuid4(),
            tenant_id=uuid.uuid4(),
            capabilities=["discovery"],
            network_segments=["10.0.0.0/16"],
        )
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(first=lambda: (uuid.uuid4(),)),     # a running job it holds
        ])

        assert await ag.get_agent_jobs(agent.id, db, limit=1) == []
        assert db.execute.await_count == 2, "went on to look for pending work"
        busy_query = str(db.execute.await_args_list[1].args[0])
        assert "scan_jobs.agent_id" in busy_query
        assert "scan_jobs.status" in busy_query
        assert "scan_jobs.lease_expires_at >" in busy_query
```

- [ ] **Step 2: Run it to verify it fails**

```bash
cd "$REPO/manager/backend" && ./.venv/bin/python -m pytest tests/test_agents.py -q -k live_job 2>&1 | tail -3
```

Expected: FAIL. The second mocked result is consumed as the candidate query, so the function fails or returns the wrong shape.

- [ ] **Step 3: Implement**

In `get_agent_jobs`, directly after:

```python
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(404, "Agent not found")
```

insert:

```python
    # One job per probe, enforced where the queue lives. A probe keeps its own
    # one-at-a-time state, but one that loses track of it — a poller left over
    # from a dropped connection, an older build, two processes sharing one
    # identity — must still be handed nothing while it holds a live lease.
    # The lease, not the probe's reported status, is the authority: a probe
    # that has lost track of a running scan reports itself idle.
    busy = await db.execute(
        select(ScanJob.id)
        .where(
            ScanJob.agent_id == str(agent_id),
            ScanJob.status == ScanJobStatus.running,
            ScanJob.lease_expires_at > func.now(),
        )
        .limit(1)
    )
    if busy.first() is not None:
        logger.info("agent.job.poll_while_busy", agent_id=str(agent_id))
        return []
```

- [ ] **Step 4: Update the existing tests for the extra query**

Every other test in `TestGetAgentJobs` that calls `get_agent_jobs` feeds `db.execute` an ordered `side_effect` list. In each one, insert `MagicMock(first=lambda: None),` as the **second** element (directly after the `scalar_one_or_none=lambda: agent` entry), meaning "holds no running job". In the same tests, shift every positional index into `db.execute.await_args_list` by +1 (for example `await_args_list[1]` → `[2]`, `[2]` → `[3]`), and increase every `await_count == N` assertion by 1. Find them all with:

```bash
cd "$REPO/manager/backend" && grep -n "get_agent_jobs\|await_args_list\|await_count" tests/test_agents.py
```

- [ ] **Step 5: Run the agent tests, then the full manager suite**

```bash
cd "$REPO/manager/backend" && ./.venv/bin/python -m pytest tests/test_agents.py -q 2>&1 | tail -1 && ./.venv/bin/python -m pytest -q 2>&1 | tail -1
```

Expected: all passed, then the full suite with 0 failed.

- [ ] **Step 6: Commit**

```bash
cd "$REPO" && git add manager/backend/app/routers/agents.py manager/backend/tests/test_agents.py && git commit -F- <<'MSG'
fix(manager): do not hand a second job to a probe holding a live lease

The push path skipped busy probes, but the poll endpoint claimed pending
work for any caller. A probe that lost track of a running scan was
handed another and ran both at once. The lease is the authority, since
such a probe reports itself idle.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

### Task 15: Probe — size the infeasibility refusal by what a two-phase sweep must finish

**Why:** `deep` sweeps all 65,535 ports in two phases. The first pass covers the high-signal ports, and everything after the port stage runs on it. The rest is a tail, budgeted per host, that truncates to `not_scanned` by design. The admission gate sizes the job by the full breadth, so it refuses any aggressive scan wider than about 16 hosts at 150 pps. Your /24 needed 30.8 h by that measure, yet its first pass finishes in about 32 minutes.

**Files:**
- Modify: `probe/agent/feasibility.py` (add `admission_port_count`)
- Modify: `probe/agent/engine.py` (preflight sizing; `workflow.modes` import)
- Create: `probe/tests/test_phased_admission.py`

**Interfaces:**
- Consumes: `workflow.workflow_engine._port_candidates(profile, service_filter, port_override=...)`, `workflow.modes.includes_stage`, `workflow.modes.STAGE_DEEP_SCAN`, `first_pass_ports` (already computed in `run_scan` before the preflight).
- Produces: `feasibility.admission_port_count(profile, service_filter, port_override, first_pass_ports, *, phased: bool) -> int`.

- [ ] **Step 1: Write the failing tests**

Create `probe/tests/test_phased_admission.py`:

```python
"""
Admission must size a two-phase sweep by the part that has to finish.

`deep` intensity sweeps all 65,535 ports in two phases: a first pass over the
high-signal ports, with every later stage running on it, then the rest as a
tail budgeted per host that truncates to not_scanned by design. Sizing the
refusal by the full breadth refuses any aggressive scan wider than about 16
hosts at 150 pps, though a /24's first pass finishes in about half an hour.
"""
from __future__ import annotations

from agent import engine
from agent import feasibility as fz
from workflow.intensity import INTENSITY_PRESETS, intensity_first_pass, intensity_port_override
from workflow.workflow_engine import _port_candidates

FULL = intensity_port_override("deep")
FIRST = intensity_first_pass("deep")


class TestAdmissionPortCount:
    def test_a_phased_deep_sweep_is_sized_by_its_first_pass(self):
        """Mirrors run_engagement's own split, so admission and execution
        agree on the port set."""
        expected = len(set(_port_candidates("it", None, port_override=FIRST))
                       & set(_port_candidates("it", None, port_override=FULL)))
        n = fz.admission_port_count("it", None, FULL, FIRST, phased=True)
        assert n == expected
        assert n < 65535

    def test_an_unphased_sweep_is_sized_by_everything_it_sweeps(self):
        """A full-port audit stops at the port stage: nothing to bring
        forward, so every port must finish."""
        assert fz.admission_port_count("it", None, FULL, FIRST, phased=False) == 65535

    def test_a_job_without_a_first_pass_is_unchanged(self):
        assert fz.admission_port_count("it", None, None, None, phased=True) \
            == fz.port_count_for("it", None, None)


class TestTheReportedCase:
    def test_an_aggressive_slash_24_is_admitted(self):
        preset = INTENSITY_PRESETS["deep"]
        estimate = fz.estimate(
            hosts=254,
            ports=fz.admission_port_count("it", None, FULL, FIRST, phased=True),
            rate=preset["rate"], ceiling_seconds=7200, retries=preset["retries"])
        assert estimate.verdict != "cannot_finish"


class TestTheGateStillRefuses:
    def test_a_first_pass_that_cannot_finish_is_still_refused(self):
        """One host, but a 1 s ceiling: the ~1,145-port first pass at 150 pps
        needs ~7.6 s. Refused before a packet leaves, and the message states
        the first-pass arithmetic, not 65,535."""
        result = engine.run_scan("network_va", {
            "targets": ["10.77.0.1"],
            "scope_cidrs": ["10.77.0.0/24"],
            "intensity": "deep",
            "max_runtime_seconds": 1,
        })
        assert result["error_code"] == "job_cannot_finish"
        assert "65535" not in result["error"].replace(",", "")
        assert result["facts"] == []
```

- [ ] **Step 2: Run them to verify they fail**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_phased_admission.py -q 2>&1 | tail -4
```

Expected: FAIL with `AttributeError: module 'agent.feasibility' has no attribute 'admission_port_count'`.

- [ ] **Step 3: Add `admission_port_count`**

In `probe/agent/feasibility.py`, directly after `port_count_for`, add:

```python
def admission_port_count(
    profile: str,
    service_filter: set[str] | None,
    port_override: list[int] | None,
    first_pass_ports: list[int] | None,
    *,
    phased: bool,
) -> int:
    """Ports a job MUST sweep to finish — what admission sizes it by.

    A phased sweep (a first pass exists and stages run after the port scan)
    must finish only that first pass; the remaining ports are a tail budgeted
    per host that truncates to not_scanned by design. Computes the same split
    run_engagement makes, so admission and execution agree on the port set.
    """
    from workflow.workflow_engine import _port_candidates
    ports = set(_port_candidates(profile, service_filter, port_override=port_override))
    if not (phased and first_pass_ports):
        return len(ports)
    first = set(_port_candidates(profile, service_filter,
                                 port_override=list(first_pass_ports))) & ports
    return len(first) if first and len(first) < len(ports) else len(ports)
```

- [ ] **Step 4: Use it in the preflight**

In `probe/agent/engine.py`, add two names to the `from workflow.modes import (` block, so it reads:

```python
from workflow.modes import (
    STAGE_DEEP_SCAN,
    assessment,
    discovery as discovery_mode,
    host_discovery as host_discovery_mode,
    includes_stage,
    port_scan as port_scan_mode,
    service_fingerprint as service_fingerprint_mode,
    service_specific,
    triage,
)
```

Then in the preflight, replace:

```python
        _estimate = feasibility.estimate(
            hosts=len(targets),
            ports=_sweep_ports,
```

with:

```python
        # Admission sizes a two-phase sweep by its first pass: the tail is
        # budgeted and truncates to not_scanned by design, so measuring the
        # full breadth would refuse a /24 aggressive scan whose assessment
        # finishes in half an hour. The kernel checks below still see the
        # full sweep.
        _must_finish = feasibility.admission_port_count(
            profile, mode.service_filter, port_override, first_pass_ports,
            phased=includes_stage(mode.stage_ceiling, STAGE_DEEP_SCAN),
        )
        if _must_finish < _sweep_ports:
            LOG.info("two-phase sweep: admission sized by the %d-port first "
                     "pass; %d further ports are a budgeted tail",
                     _must_finish, _sweep_ports - _must_finish)
        _estimate = feasibility.estimate(
            hosts=len(targets),
            ports=_must_finish,
```

Leave `port_count=_sweep_ports` in the `kernel_limits.assess(...)` call unchanged.

- [ ] **Step 5: Run the admission tests and the feasibility/timing suites**

```bash
cd "$REPO/probe" && ./.venv/bin/python -m pytest tests/test_phased_admission.py tests/test_infeasible_job_admission.py tests/test_feasibility.py tests/test_run_timing.py tests/test_kernel_admission.py -q 2>&1 | tail -1
```

Expected: all passed. If a test in `test_run_timing.py` or `test_feasibility.py` asserts that a `deep` network_va estimate covers 65,535 ports, it was pinning the old sizing. Report it as a concern with the assertion quoted; do not change its expectation without saying so.

- [ ] **Step 6: Commit**

```bash
cd "$REPO" && git add probe/agent/feasibility.py probe/agent/engine.py probe/tests/test_phased_admission.py && git commit -F- <<'MSG'
fix(probe): size admission by what a two-phase sweep must finish

deep is two-phase: a first pass the assessment runs on, then a budgeted
tail that truncates to not_scanned. Admission sized it by all 65,535
ports, so any aggressive scan wider than ~16 hosts was refused; a /24
was rejected as needing 30.8 h though its first pass takes ~32 min.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
```

---

## Deliberately not in this plan

| Finding | Why not now |
|---|---|
| Raise the SYN receive buffer with `SO_RCVBUFFORCE`, add an `rmem_max` preflight check | The interleaved drain makes buffer size secondary, and it needs Linux + `NET_RAW` to verify |
| Skip ports already resolved by a late reply when re-sending | Minor: a wasted SYN and slight AIMD noise, and not a regression |
| Extract a helper for the two near-identical refusal blocks in `engine.py` | Cosmetic duplication |
| A shared helper for the five semaphore-plus-gather fan-outs in `workflow_engine.py` | Refactors code this plan does not otherwise touch |
| Replace the 7-value `**ctx` dict in the SYN loop with a small type | Cosmetic |
| Rewrite long comment blocks as one-liners | Fights the codebase's established convention; false and dated claims are removed instead |
| Run the full probe suite in CI instead of allowlists | Ends the "forgot to wire it" class for good, but costs CI time and flakiness risk — a separate decision |
| Manager backend CI workflow | Separate decision (does it need a database service?) |
| `test_gate_6_is_not_the_exception` finds code by comment text | Matches the file's existing pattern for the other stages |
| SSH host-key verification + auth-failure breaker in Gate 6 | Already a separate task (the chip from the review) |
| Rewrite commit `13f1170`'s message | It is on published `main`; Task 11's doc is the corrected record |
| Validate D1 on real packets; confirm whether reporters had `NET_RAW` | Needs hardware — this is P1 |
