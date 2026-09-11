"""Phase 5 — self-scan: own-IP-only, manager-less. Decision logic is pure;
execute() is tested with an injected engine + fake queue + a temp scope file."""
from __future__ import annotations

from agent import self_scan as ss


# ── plan_self_scan (pure) ────────────────────────────────────────────────────
def test_plan_allows_normal_own_ip_scoped_to_self():
    plan, reason = ss.plan_self_scan("192.168.1.42", container=None)
    assert reason == ""
    assert plan.target == "192.168.1.42"
    assert plan.scope_file_line == "192.168.1.42"
    assert len(plan.scope) == 1
    seg = plan.scope[0]
    assert seg.cidr == "192.168.1.42/32" and seg.type == "IT" and seg.site == "self"


def test_plan_refuses_inside_container():
    plan, reason = ss.plan_self_scan("172.17.0.3", container="docker")
    assert plan is None and "not possible" in reason


def test_plan_refuses_without_an_ip():
    plan, reason = ss.plan_self_scan(None, container=None)
    assert plan is None and reason


def test_plan_refuses_denylisted_own_ip():
    plan, reason = ss.plan_self_scan("127.0.0.1", container=None)
    assert plan is None and "denylist" in reason


# ── execute (injected engine + queue) ────────────────────────────────────────
class FakeQueue:
    def __init__(self): self.enqueued = []
    def enqueue(self, job_id, payload): self.enqueued.append((job_id, payload))


def test_execute_writes_scope_runs_engine_and_archives(tmp_path):
    scope_file = tmp_path / "scope.txt"
    calls = {}
    def engine(argv): calls["argv"] = argv; return 0
    q = FakeQueue()
    plan, _ = ss.plan_self_scan("10.0.0.5", container=None, profile="it", stage="deep_scan")

    rc = ss.execute(plan, str(scope_file), engine_run=engine, queue=q, now=lambda: 1700.0)

    assert rc == 0
    assert scope_file.read_text().strip() == "10.0.0.5"        # scope = own IP only
    assert calls["argv"] == ["10.0.0.5", "it", "deep_scan"]    # engine invoked on self
    assert len(q.enqueued) == 1                                 # result archived durably
    jid, payload = q.enqueued[0]
    assert payload["target"] == "10.0.0.5" and payload["rc"] == 0


def test_execute_refusal_returns_fatal_config_and_skips_engine():
    called = {"engine": False}
    def engine(argv): called["engine"] = True; return 0
    rc = ss.run_from(primary_ip=None, container=None, scope_file_path="/tmp/x",
                     engine_run=engine, queue=None, now=lambda: 1.0)
    assert rc == 20 and called["engine"] is False   # fatal-config, engine never runs
