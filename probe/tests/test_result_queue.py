"""Phase 4 — durable result queue: crash-safe, idempotent, bounded, backpressure,
encrypted-at-rest. Queue logic tested with an injected null cipher + fake clock;
the real Fernet cipher is tested separately (skipped if cryptography absent)."""
from __future__ import annotations

import pytest

from agent import result_queue as rq


class Clock:
    def __init__(self): self.t = 1000.0
    def __call__(self): return self.t


def _q(tmp_path, **kw):
    clock = kw.pop("clock", Clock())
    return rq.ResultQueue(str(tmp_path), cipher=rq.NullCipher(), now=clock, **kw), clock


def test_enqueue_then_pending_roundtrips_payload(tmp_path):
    q, _ = _q(tmp_path)
    q.enqueue("job-1", {"finding": "open-445"})
    pend = q.pending()
    assert len(pend) == 1
    assert pend[0].job_id == "job-1"
    assert pend[0].payload == {"finding": "open-445"}


def test_enqueue_is_idempotent_by_job_id(tmp_path):
    q, _ = _q(tmp_path)
    q.enqueue("job-1", {"a": 1})
    q.enqueue("job-1", {"a": 2})     # same job_id → no duplicate
    assert len(q.pending()) == 1


def test_ack_removes_the_record(tmp_path):
    q, _ = _q(tmp_path)
    q.enqueue("job-1", {"a": 1})
    q.ack("job-1")
    assert q.pending() == []


def test_pending_is_oldest_first(tmp_path):
    q, _ = _q(tmp_path)
    for i in range(3):
        q.enqueue(f"job-{i}", {"i": i})
    assert [r.job_id for r in q.pending()] == ["job-0", "job-1", "job-2"]


def test_overflow_drops_oldest(tmp_path):
    q, _ = _q(tmp_path, max_records=2)
    for i in range(3):
        q.enqueue(f"job-{i}", {"i": i})
    ids = [r.job_id for r in q.pending()]
    assert ids == ["job-1", "job-2"]   # job-0 dropped (oldest)


def test_age_prune_drops_stale_records(tmp_path):
    clock = Clock()
    q, _ = _q(tmp_path, max_age_s=100, clock=clock)
    q.enqueue("old", {"x": 1})
    clock.t += 500                      # advance well past max_age
    q.enqueue("new", {"x": 2})
    dropped = q.prune()
    assert dropped == 1
    assert [r.job_id for r in q.pending()] == ["new"]


def test_backpressure_at_high_water(tmp_path):
    q, _ = _q(tmp_path, high_water_records=2, max_records=10)
    q.enqueue("a", {})
    assert not q.should_backpressure()
    q.enqueue("b", {})
    assert q.should_backpressure()


def test_records_survive_a_reopen_until_acked(tmp_path):
    q, _ = _q(tmp_path)
    q.enqueue("job-1", {"a": 1})
    q2 = rq.ResultQueue(str(tmp_path), cipher=rq.NullCipher())   # simulate restart
    assert [r.job_id for r in q2.pending()] == ["job-1"]


def test_host_sealed_cipher_encrypts_at_rest(tmp_path):
    pytest.importorskip("cryptography")
    cipher = rq.host_sealed_cipher(str(tmp_path))
    q = rq.ResultQueue(str(tmp_path), cipher=cipher)
    q.enqueue("job-secret", {"banner": "root:x:0:0"})
    # the raw bytes on disk must not contain the plaintext
    rec = q.pending()[0]
    with open(rec.path, "rb") as fh:
        raw = fh.read()
    assert b"root:x:0:0" not in raw
    assert q.pending()[0].payload == {"banner": "root:x:0:0"}   # decrypts back
