"""
The probe's half of the per-host buffer.

A job's evidence left the probe exactly once, at the end, so a process that died
mid-scan (OOM on a deep sweep, container evicted) lost every host it had already
finished. Committing each host as it completes means the manager holds that work
even if this process never returns — and a retry can ask which hosts to skip
instead of rescanning them.

Best-effort by construction: the buffer is an optimisation, so a manager that is
unreachable, slow or refusing chunks must never take the scan down with it.
"""
from __future__ import annotations

import asyncio
import inspect
from unittest.mock import MagicMock

import pytest

from scanner.scanner_base import ScanResult, ScopeGuard
from workflow.workflow_engine import run_engagement

HOSTS = ["10.0.0.1", "10.0.0.2"]
SCOPE = ScopeGuard.from_list(["10.0.0.0/24"])


def _wire(monkeypatch):
    from workflow.branches import BRANCHES

    def _stub(component, *, port=None, data=None, status="open"):
        class Scanner:
            name = component

            def __init__(self, *a, **kw):
                pass

            async def scan_target(self, host):
                return [ScanResult(scanner=component, target=host, port=port,
                                   proto="tcp" if port else None,
                                   status=status, data=data or {})]
        return Scanner

    def _inert(component):
        class Inert:
            name = component

            def __init__(self, *a, **kw):
                pass

            async def scan_target(self, host):
                return []
        return Inert

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                        _stub("host_discovery", data={"alive": True}))
    monkeypatch.setattr("workflow.workflow_engine.PortScanner",
                        _stub("port_scan", port=445))
    monkeypatch.setattr("workflow.workflow_engine.SynScanner",
                        _stub("syn_scan", port=445))
    monkeypatch.setattr("workflow.workflow_engine.ServiceBannerScanner",
                        _stub("service_banner", port=445))
    monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                        _stub("os_fingerprint"))
    monkeypatch.setattr("workflow.workflow_engine.UDPScanner", _inert("udp_scan"))
    for spec in BRANCHES:
        monkeypatch.setattr(f"workflow.workflow_engine.{spec.scanner}",
                            _inert(spec.component))


def _run(**kwargs):
    return asyncio.run(run_engagement(HOSTS, SCOPE, port_override=[445],
                                      stage_ceiling="deep_scan",
                                      host_concurrency=2, **kwargs))


class TestPerHostCommit:
    def test_each_finished_host_is_handed_over_with_its_own_facts(self, monkeypatch):
        _wire(monkeypatch)
        seen: list[tuple[str, list]] = []

        _run(on_host_complete=lambda host, facts: seen.append((host, facts)))

        assert sorted(h for h, _ in seen) == HOSTS
        for host, facts in seen:
            assert facts, f"{host} was committed with no evidence"
            assert {f["target"] for f in facts} == {host}, (
                "a host's chunk must carry only that host's facts")

    def test_an_async_hook_is_awaited(self, monkeypatch):
        """The real sink does network I/O; it must not block the event loop."""
        _wire(monkeypatch)
        seen: list[str] = []

        async def _sink(host, facts):
            await asyncio.sleep(0)
            seen.append(host)

        _run(on_host_complete=_sink)

        assert sorted(seen) == HOSTS

    def test_a_failing_hook_does_not_take_the_scan_down(self, monkeypatch):
        """The buffer is an optimisation. An unreachable manager must not turn a
        working scan into a failed one."""
        _wire(monkeypatch)

        def _boom(host, facts):
            raise RuntimeError("manager unreachable")

        assets = _run(on_host_complete=_boom)

        for host in HOSTS:
            assert 445 in assets[host].open_ports_for_deep_scan()


class TestResume:
    def test_hosts_the_manager_already_has_are_not_rescanned(self, monkeypatch):
        _wire(monkeypatch)
        seen: list[str] = []

        assets = _run(skip_hosts={"10.0.0.1"},
                      on_host_complete=lambda h, f: seen.append(h))

        assert seen == ["10.0.0.2"]
        assert "10.0.0.1" not in assets or not assets["10.0.0.1"].open_ports_for_deep_scan()

    def test_skipping_every_host_is_not_an_error(self, monkeypatch):
        """A retry after the last host was committed has nothing left to do."""
        _wire(monkeypatch)

        assets = _run(skip_hosts=set(HOSTS))

        assert assets is not None


class TestTransport:
    def test_a_chunk_is_posted_to_the_job_chunk_endpoint(self, tmp_path):
        from agent.transport import Transport

        t = Transport("http://localhost:8000", verify_tls=False,
                      state_file=tmp_path / "state.json",
                      agent_id="agent-1", agent_token="tok")
        t._client = MagicMock()
        t._client.post.return_value = MagicMock(status_code=200)
        t.ensure_device_access = lambda: True

        ok = t.submit_chunk("job-1", attempt_id="att-1", fence=3,
                            host="10.0.0.5", facts=[{"target": "10.0.0.5"}],
                            scan_type="network_va")

        assert ok is True
        path = t._client.post.call_args[0][0]
        assert path == "/agents/agent-1/jobs/job-1/chunks"
        body = t._client.post.call_args[1]["json"]
        assert body["host"] == "10.0.0.5" and body["fence"] == 3

    def test_a_refused_chunk_is_reported_not_raised(self, tmp_path):
        from agent.transport import Transport

        t = Transport("http://localhost:8000", verify_tls=False,
                      state_file=tmp_path / "state.json",
                      agent_id="agent-1", agent_token="tok")
        t._client = MagicMock()
        t._client.post.return_value = MagicMock(status_code=422)
        t.ensure_device_access = lambda: True

        assert t.submit_chunk("job-1", attempt_id="a", fence=1, host="8.8.8.8",
                              facts=[]) is False

    def test_committed_hosts_reads_the_resume_list(self, tmp_path):
        from agent.transport import Transport

        t = Transport("http://localhost:8000", verify_tls=False,
                      state_file=tmp_path / "state.json",
                      agent_id="agent-1", agent_token="tok")
        t._client = MagicMock()
        t._client.get.return_value = MagicMock(
            status_code=200, json=lambda: {"hosts": ["10.0.0.1"], "count": 1})
        t.ensure_device_access = lambda: True

        assert t.committed_hosts("job-1") == ["10.0.0.1"]

    def test_an_unreachable_manager_yields_no_resume_list(self, tmp_path):
        """Resume is an optimisation: failing to read it must mean 'scan
        everything', never 'skip everything'."""
        import httpx

        from agent.transport import Transport

        t = Transport("http://localhost:8000", verify_tls=False,
                      state_file=tmp_path / "state.json",
                      agent_id="agent-1", agent_token="tok")
        t._client = MagicMock()
        t._client.get.side_effect = httpx.ConnectError("down")
        t.ensure_device_access = lambda: True

        assert t.committed_hosts("job-1") == []


class TestEngineSeam:
    def test_run_engagement_accepts_the_hooks(self):
        params = inspect.signature(run_engagement).parameters
        assert "on_host_complete" in params
        assert "skip_hosts" in params

    def test_run_scan_passes_them_through(self):
        from agent.engine import run_scan
        src = inspect.getsource(run_scan)
        assert "on_host_complete=" in src
        assert "skip_hosts=" in src

    def test_the_task_runner_commits_and_resumes(self):
        from agent.task_runner import TaskRunner
        src = inspect.getsource(TaskRunner)
        assert "submit_chunk" in src
        assert "committed_hosts" in src
