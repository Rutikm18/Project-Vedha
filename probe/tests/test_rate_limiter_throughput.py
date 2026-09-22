"""
RateLimiter slept while holding its own lock.

    async with self._lock:
        now = time.monotonic()
        if now < self._next:
            await asyncio.sleep(self._next - now)   # <- inside the lock
            now = time.monotonic()
        self._next = now + self.min_interval

Only ONE coroutine could be pacing at a time; every other probe was blocked on
the mutex rather than on its own timer. So the achievable rate was bounded by
how fast the event loop could hand the lock around — not by the configured
rate — and the port stage runs thousands of coroutines through this one object
(one scanner instance serves every host in the stage).

The fix keeps the contract and moves the sleep out: claim a slot under the
lock (a few microseconds, no await), release, then sleep until that slot.
Waiters then wait CONCURRENTLY on their own deadlines.

It also removes a drift the old version had. Recomputing `now` AFTER sleeping
means every slot is scheduled from a moment already past its target, so the
error accumulates and the real rate is always below the configured one.
Claiming `max(now, self._next)` schedules on a fixed grid instead.
"""
from __future__ import annotations

import asyncio
import time

import pytest

from scanner.scanner_base import RateLimiter


async def _drain(limiter: RateLimiter, n: int, concurrency: int) -> float:
    """Run `n` paced operations across `concurrency` coroutines; return seconds."""
    remaining = list(range(n))
    started = time.monotonic()

    async def _worker() -> None:
        while True:
            try:
                remaining.pop()
            except IndexError:
                return
            await limiter.wait()

    await asyncio.gather(*(_worker() for _ in range(concurrency)))
    return time.monotonic() - started


# ── the contract is unchanged ───────────────────────────────────────────────

class TestPacing:
    @pytest.mark.asyncio
    async def test_a_zero_rate_disables_pacing(self):
        limiter = RateLimiter(0)
        assert await _drain(limiter, 500, 10) < 0.5

    @pytest.mark.asyncio
    async def test_operations_are_not_faster_than_the_configured_rate(self):
        """The safety property: pacing must still pace."""
        limiter = RateLimiter(200)
        elapsed = await _drain(limiter, 100, 20)
        # 100 ops at 200/s cannot legitimately finish in under ~0.5 s.
        assert elapsed > 0.35, f"paced 100 ops at 200/s in {elapsed:.3f}s"

    @pytest.mark.asyncio
    async def test_a_single_waiter_is_paced_correctly(self):
        limiter = RateLimiter(100)
        elapsed = await _drain(limiter, 20, 1)
        assert 0.15 < elapsed < 0.45, elapsed


# ── the defect: concurrent waiters must not serialize on the mutex ──────────

class TestConcurrentThroughput:
    @pytest.mark.asyncio
    async def test_many_waiters_still_reach_the_configured_rate(self):
        """The port stage puts thousands of coroutines through one limiter.

        With the sleep inside the lock, added concurrency made throughput
        WORSE — each probe paid a lock handoff on top of its own pacing.
        """
        limiter = RateLimiter(500)
        elapsed = await _drain(limiter, 500, 400)
        achieved = 500 / elapsed
        # Measured before the fix: 435/s (87%). After: 500/s. 92% discriminates
        # between them with room for a loaded CI box.
        assert achieved > 460, (
            f"500 waiters achieved only {achieved:.0f}/s against a "
            f"configured 500/s — the limiter is under-delivering"
        )

    @pytest.mark.asyncio
    async def test_throughput_does_not_collapse_as_waiters_are_added(self):
        """Same work, 40x the coroutines. A lock-bound limiter degrades; a
        slot-based one is flat."""
        few = await _drain(RateLimiter(500), 300, 10)
        many = await _drain(RateLimiter(500), 300, 400)
        assert many < few * 2.5, (
            f"{few:.2f}s with 10 waiters vs {many:.2f}s with 400 — "
            f"throughput collapses under concurrency"
        )

    @pytest.mark.asyncio
    async def test_the_lock_is_never_held_across_an_await(self):
        """Source-level, because this is the whole defect and a future edit
        could reintroduce it without changing any timing test's verdict."""
        import inspect
        import re

        src = inspect.getsource(RateLimiter.wait)
        body = src.split("async with self._lock:", 1)[1]
        # Everything up to the dedent back out of the `async with` block.
        held = []
        for line in body.splitlines()[1:]:
            if line.strip() and not line.startswith(" " * 12):
                break
            # Comments are stripped: the block explains that it must not await,
            # and matching the word in that explanation would fail forever.
            held.append(line.split("#", 1)[0])
        assert not re.search(r"\bawait\b", "\n".join(held)), (
            "RateLimiter.wait() awaits while holding its lock:\n"
            + "\n".join(held)
        )


# ── scheduling on a grid, not drifting off one ──────────────────────────────

class TestNoDrift:
    @pytest.mark.asyncio
    async def test_slots_do_not_accumulate_error(self):
        """Recomputing `now` after each sleep pushed every later slot further
        past its target, so the real rate drifted below the configured one."""
        limiter = RateLimiter(200)
        elapsed = await _drain(limiter, 200, 50)
        achieved = 200 / elapsed
        # Drift made this undershoot by 13-21%, growing with the rate. On a
        # fixed grid the achieved rate tracks the configured one closely.
        assert 185 < achieved < 215, f"achieved {achieved:.0f}/s against 200/s"
