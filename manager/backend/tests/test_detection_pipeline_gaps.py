"""
test_detection_pipeline_gaps.py — four ways facts reached the manager and then
failed to become findings. Each of these was live; none of them logged an error.

R2  a submission with success=false stored its facts and never enqueued detection
R3  scanner_runs never reached build_coverage, so nothing could ever auto-resolve
R4  attack-path correlation read raw facts, including ones ingest had rejected
R5  one fact whose `data` was not an object aborted the CVE track for the batch

The unifying defect is that several consumers disagreed about which facts are
real. These tests pin the agreement.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge as EB
from app.detection.resolution import build_coverage
from app.workers import outbox as OB

_TS = "2026-09-02T11:03:50.208953+00:00"


def _fact(scanner="smb_scan", target="10.0.0.10", port=445, data=None, **kw):
    f = {"scanner": scanner, "target": target, "timestamp": _TS, "port": port,
         "proto": "tcp", "status": "open",
         "data": {"smbv1_enabled": True, "signing_required": False}
                 if data is None else data}
    f.update(kw)
    return f


pytestmark = pytest.mark.skipif(
    not EB._ensure_importable(),
    reason="detection_engine not importable in this environment",
)


# ── R5: one hostile fact must not sink the batch ─────────────────────────────

def test_a_non_dict_data_payload_is_quarantined_not_fatal():
    """`data` is read with .get() by every rule. A string there used to raise mid-run
    and take the CVE findings for every OTHER host down with it. It must be stopped
    at the same gate as any other malformed fact, and counted."""
    facts = [
        _fact(target="10.0.0.1", data="not-a-dict"),
        _fact(scanner="service_banner", target="10.0.0.2", port=22,
              data={"service": "ssh", "product": "OpenSSH", "version": "7.2",
                    "banner": "SSH-2.0-OpenSSH_7.2"}),
    ]
    cve, _posture, meta = EB.detect_all_from_facts_traced(facts)
    census = meta["ingest"]
    assert census["quarantined"] == 1
    assert any("data must be an object" in r for r in census["reasons"]), census["reasons"]
    assert cve, "the well-formed fact's CVEs must survive the hostile one"


# ── R4: every consumer agrees on which facts are real ────────────────────────

def test_accepted_facts_excludes_what_ingest_rejected():
    """attack_path_findings runs on meta['accepted_facts']. If that still contained
    rejected facts, a submission ingest refused wholesale could still emit an
    'NTLM relay attack path' — a finding built on evidence nothing else trusted."""
    good_a = _fact(target="10.0.0.1")
    bad = {k: v for k, v in _fact(target="10.0.0.2").items() if k != "timestamp"}
    good_b = _fact(target="10.0.0.3")
    _cve, _p, meta = EB.detect_all_from_facts_traced([good_a, bad, good_b])

    accepted = meta["accepted_facts"]
    assert [f["target"] for f in accepted] == ["10.0.0.1", "10.0.0.3"]
    assert len(accepted) == meta["ingest"]["ingested"]


def test_total_rejection_leaves_no_facts_for_correlation():
    drifted = [{k: v for k, v in _fact().items() if k != "timestamp"}]
    _cve, _p, meta = EB.detect_all_from_facts_traced(drifted)
    assert meta["accepted_facts"] == []


def test_accepted_facts_falls_back_to_raw_when_there_is_no_verdict():
    """No engine means no ingest verdict. Without a verdict we cannot call any fact
    bad, so correlation keeps its previous input rather than silently going dark."""
    facts = [_fact()]
    with patch.object(EB, "_ensure_importable", return_value=False):
        _cve, _p, meta = EB.detect_all_from_facts_traced(facts)
    assert meta["accepted_facts"] == facts


# ── R3: coverage needs scanner_runs, which live on the job ───────────────────

@pytest.mark.asyncio
async def test_facts_ready_reads_scanner_runs_from_the_job():
    """scan_results has no scanner_runs column; the job's result blob does. Passing
    only {"facts": ...} made build_coverage fail-closed on every run, so a host
    proven clean never auto-resolved its old finding."""
    sr_id, job_id, eng_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    runs = [{"id": "smb_scan", "status": "completed", "fact_count": 1}]
    sr = SimpleNamespace(id=sr_id, engagement_id=eng_id, job_id=job_id,
                         facts=[_fact()])
    job = SimpleNamespace(id=job_id, result={"scanner_runs": runs})

    db = MagicMock()
    db.get = AsyncMock(side_effect=lambda model, ident: sr if ident == sr_id else job)
    db.execute = AsyncMock(return_value=MagicMock(first=lambda: None))
    db.commit = AsyncMock()
    create = AsyncMock(return_value=0)

    with patch.object(OB, "AsyncSessionLocal", return_value=_ctx(db)), \
         patch("app.detection.engine_bridge.create_findings_from_facts", create):
        await OB._handle_facts_ready(
            SimpleNamespace(id="e1", topic="facts.ready", engagement_id=str(eng_id),
                            scan_result_id=str(sr_id), payload={}, attempts=1))

    passed = create.await_args.args[2]
    assert passed["scanner_runs"] == runs, "the job's scanner_runs must reach detection"
    assert build_coverage(passed["scanner_runs"], passed["facts"])["assets"] == ["10.0.0.10"], \
        "coverage must now name the asset, which is what lets it auto-resolve"


@pytest.mark.asyncio
async def test_missing_scanner_runs_degrades_to_empty_coverage():
    """An older probe reports none. Coverage stays empty and nothing auto-resolves —
    the safe direction, since absence of a finding only counts if we proved we looked."""
    sr_id, eng_id = uuid.uuid4(), uuid.uuid4()
    sr = SimpleNamespace(id=sr_id, engagement_id=eng_id, job_id=None, facts=[_fact()])
    db = MagicMock()
    db.get = AsyncMock(return_value=sr)
    db.execute = AsyncMock(return_value=MagicMock(first=lambda: None))
    db.commit = AsyncMock()
    create = AsyncMock(return_value=0)

    with patch.object(OB, "AsyncSessionLocal", return_value=_ctx(db)), \
         patch("app.detection.engine_bridge.create_findings_from_facts", create):
        await OB._handle_facts_ready(
            SimpleNamespace(id="e2", topic="facts.ready", engagement_id=str(eng_id),
                            scan_result_id=str(sr_id), payload={}, attempts=1))

    passed = create.await_args.args[2]
    assert passed["scanner_runs"] is None
    assert build_coverage(passed["scanner_runs"], passed["facts"])["assets"] == []


# ── R2: storing facts and detecting on them are one decision ─────────────────

def test_enqueue_is_not_gated_on_success():
    """Facts are persisted whenever they are present, but the outbox enqueue used to
    sit inside `if success:`. A submission reporting ok=false then stored real facts
    that detection never saw, and the orphan scan_results row also blocked the
    campaign's evidence_covered check forever.

    Read structurally: the enqueue must not be nested under the success branch."""
    import inspect
    from app.services import job_result_service as J

    src = inspect.getsource(J.process_job_result)
    lines = src.splitlines()
    gate = next(i for i, ln in enumerate(lines) if "if success and isinstance" in ln)
    enqueue = next(i for i, ln in enumerate(lines) if "TOPIC_FACTS_READY," in ln)
    assert enqueue < gate, (
        "the facts.ready enqueue must happen before/outside the `if success:` gate — "
        "if the facts were worth storing they are worth detecting on")


class _ctx:
    """Minimal async-context-manager wrapper around a mock session."""
    def __init__(self, db): self._db = db
    async def __aenter__(self): return self._db
    async def __aexit__(self, *a): return False
