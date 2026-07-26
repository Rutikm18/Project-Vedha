from __future__ import annotations

import asyncio

from agent import engine
from scanner.scanner_base import ScanResult
from scanner.scanner_base import ScopeGuard
from scanner.port_scanner import PortScanner
from workflow.asset import Asset
from workflow.execution import (
    ExecutionTrace,
    engine_manifest,
    planned_components,
    scanner_failure_result,
)
from workflow.gates import DB_PORTS, TLS_PORTS, WEB_PORTS
from workflow.modes import (
    STAGE_HOST_DISCOVERY,
    STAGE_PORT_SCAN,
    STAGE_SERVICE_BANNER,
)
from workflow.workflow_engine import (
    _gather_per_host,
    _port_candidates,
    run_engagement,
)


class _ExplodingScanner:
    name = "web_scan"

    async def scan_target(self, host: str) -> list[ScanResult]:
        if host.endswith(".2"):
            raise TimeoutError("component exceeded its operation deadline")
        return [
            ScanResult(
                scanner=self.name,
                target=host,
                port=80,
                status="observed",
                data={"service": "http"},
            )
        ]


class _ConcurrencyScanner:
    name = "port_scan"

    def __init__(self) -> None:
        self.active = 0
        self.maximum = 0

    async def scan_target(self, host: str) -> list[ScanResult]:
        self.active += 1
        self.maximum = max(self.maximum, self.active)
        await asyncio.sleep(0.005)
        self.active -= 1
        return [ScanResult(scanner=self.name, target=host)]


def test_per_target_exception_preserves_other_results() -> None:
    results = asyncio.run(_gather_per_host(
        _ExplodingScanner(),
        ["10.0.0.1", "10.0.0.2"],
        max_in_flight=2,
    ))

    assert len(results) == 2
    assert any(result.target == "10.0.0.1" and not result.error for result in results)
    failure = next(result for result in results if result.target == "10.0.0.2")
    assert failure.status == "error"
    assert failure.data["error_code"] == "scanner_timeout"
    assert failure.data["retryable"] is True


def test_host_fanout_is_bounded() -> None:
    scanner = _ConcurrencyScanner()
    asyncio.run(_gather_per_host(
        scanner,
        [f"10.0.0.{index}" for index in range(1, 13)],
        max_in_flight=3,
    ))

    assert scanner.maximum == 3


def test_error_result_does_not_mutate_asset_state() -> None:
    asset = Asset(host="10.0.0.1")
    asset.merge_result(scanner_failure_result(
        "ssh_inventory",
        asset.host,
        PermissionError("credential rejected"),
    ))

    assert asset.cred_collected is False
    assert asset.credential_inventory is None


def test_execution_trace_reports_partial_component() -> None:
    trace = ExecutionTrace(["web_scan", "tls_scan"])
    trace.record(
        "web_scan",
        target_count=2,
        results=[
            ScanResult(scanner="web_scan", target="10.0.0.1"),
            scanner_failure_result("web_scan", "10.0.0.2", TimeoutError()),
        ],
    )
    trace.finalize()

    runs = {run["id"]: run for run in trace.as_list()}
    assert runs["web_scan"]["status"] == "degraded"
    assert runs["web_scan"]["error_count"] == 1
    assert runs["tls_scan"]["status"] == "skipped"
    assert trace.degraded is True
    assert trace.failed is False


def test_manifest_does_not_claim_external_engine_executed(monkeypatch) -> None:
    monkeypatch.setattr(
        "workflow.execution.shutil.which",
        lambda name: f"/usr/bin/{name}" if name == "nmap" else None,
    )

    manifest = engine_manifest(build_version="test")
    external = {item["id"]: item for item in manifest["external_engines"]}
    assert external["nmap"]["available"] is True
    assert external["nmap"]["execution"] == "standalone_validation"
    assert external["masscan"]["available"] is False


def test_database_gate_uses_scanner_port_catalog() -> None:
    assert 33060 in DB_PORTS


def test_filtered_jobs_use_only_requested_tcp_catalogs() -> None:
    assert set(_port_candidates("it", {"web"})) == WEB_PORTS
    assert set(_port_candidates("it", {"tls"})) == TLS_PORTS
    assert _port_candidates("it", {"snmp"}) == []
    assert _port_candidates("it", {"udp"}) == []


def test_explicit_empty_port_catalog_never_falls_back_to_top_ports() -> None:
    scanner = PortScanner(ScopeGuard.from_list(["10.0.0.1"]), ports=[])
    assert scanner.ports == []


def test_planned_components_respect_stage_ceiling_and_udp_only_branches() -> None:
    common = {
        "profile": "it",
        "service_filter": None,
        "stop_after_banner": False,
        "ssh_enabled": False,
        "windows_enabled": False,
    }
    assert planned_components(
        **common,
        stage_ceiling=STAGE_HOST_DISCOVERY,
    ) == ["host_discovery"]
    assert planned_components(
        **common,
        stage_ceiling=STAGE_PORT_SCAN,
    ) == ["host_discovery", "port_scan"]
    assert planned_components(
        **common,
        stage_ceiling=STAGE_SERVICE_BANNER,
    ) == ["host_discovery", "port_scan", "service_banner"]
    assert planned_components(
        "it",
        service_filter={"snmp"},
        stop_after_banner=False,
        ssh_enabled=False,
        windows_enabled=False,
    ) == ["snmp_scan"]


def test_workflow_stops_at_port_stage_before_banner(monkeypatch) -> None:
    calls: list[str] = []

    class Discovery:
        name = "host_discovery"

        def __init__(self, *args, **kwargs):
            pass

        async def scan_target(self, host):
            calls.append(self.name)
            return [
                ScanResult(
                    scanner=self.name,
                    target=host,
                    data={"alive": True},
                )
            ]

    class Ports:
        name = "port_scan"

        def __init__(self, *args, **kwargs):
            pass

        async def scan_target(self, host):
            calls.append(self.name)
            return [
                ScanResult(
                    scanner=self.name,
                    target=host,
                    port=80,
                    proto="tcp",
                    status="open",
                )
            ]

    class Banner:
        name = "service_banner"

        def __init__(self, *args, **kwargs):
            pass

        async def scan_target(self, host):
            calls.append(self.name)
            return []

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner", Discovery)
    monkeypatch.setattr("workflow.workflow_engine.PortScanner", Ports)
    monkeypatch.setattr("workflow.workflow_engine.ServiceBannerScanner", Banner)

    scope = ScopeGuard.from_list(["10.0.0.1"])
    asyncio.run(run_engagement(
        ["10.0.0.1"],
        scope,
        stage_ceiling=STAGE_PORT_SCAN,
    ))

    assert calls == ["host_discovery", "port_scan"]


def test_udp_only_workflow_never_falls_back_to_tcp_or_banner(monkeypatch) -> None:
    calls: list[str] = []

    class UnexpectedTCP:
        def __init__(self, *args, **kwargs):
            raise AssertionError("UDP-only plan must not initialize a TCP scanner")

    class UDP:
        name = "udp_scan"

        def __init__(self, *args, **kwargs):
            pass

        async def scan_target(self, host):
            calls.append(self.name)
            return []

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner", UnexpectedTCP)
    monkeypatch.setattr("workflow.workflow_engine.PortScanner", UnexpectedTCP)
    monkeypatch.setattr("workflow.workflow_engine.ServiceBannerScanner", UnexpectedTCP)
    monkeypatch.setattr("workflow.workflow_engine.UDPScanner", UDP)

    scope = ScopeGuard.from_list(["10.0.0.1"])
    asyncio.run(run_engagement(
        ["10.0.0.1"],
        scope,
        service_filter={"udp"},
    ))

    assert calls == ["udp_scan"]


def test_snmp_only_workflow_never_falls_back_to_tcp(monkeypatch) -> None:
    calls: list[str] = []

    class UnexpectedTCP:
        def __init__(self, *args, **kwargs):
            raise AssertionError("SNMP-only plan must not initialize a TCP scanner")

    class SNMP:
        name = "snmp_scan"

        def __init__(self, *args, **kwargs):
            pass

        async def scan_target(self, host):
            calls.append(self.name)
            return []

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner", UnexpectedTCP)
    monkeypatch.setattr("workflow.workflow_engine.PortScanner", UnexpectedTCP)
    monkeypatch.setattr("workflow.workflow_engine.ServiceBannerScanner", UnexpectedTCP)
    monkeypatch.setattr("workflow.workflow_engine.SNMPScanner", SNMP)

    scope = ScopeGuard.from_list(["10.0.0.1"])
    asyncio.run(run_engagement(
        ["10.0.0.1"],
        scope,
        service_filter={"snmp"},
    ))

    assert calls == ["snmp_scan"]


def test_web_job_constrains_discovery_and_port_scan_to_web_catalog(
    monkeypatch,
) -> None:
    observed_ports: dict[str, set[int]] = {}

    class Discovery:
        name = "host_discovery"

        def __init__(self, *args, ports, **kwargs):
            observed_ports[self.name] = set(ports)

        async def scan_target(self, host):
            return [
                ScanResult(
                    scanner=self.name,
                    target=host,
                    data={"alive": True},
                )
            ]

    class Ports:
        name = "port_scan"

        def __init__(self, *args, ports, **kwargs):
            observed_ports[self.name] = set(ports)

        async def scan_target(self, host):
            return []

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner", Discovery)
    monkeypatch.setattr("workflow.workflow_engine.PortScanner", Ports)

    scope = ScopeGuard.from_list(["10.0.0.1"])
    asyncio.run(run_engagement(
        ["10.0.0.1"],
        scope,
        service_filter={"web"},
        stage_ceiling=STAGE_PORT_SCAN,
    ))

    assert observed_ports == {
        "host_discovery": WEB_PORTS,
        "port_scan": WEB_PORTS,
    }


def test_agent_scan_types_have_distinct_stage_ceilings() -> None:
    expected = {
        "discovery": STAGE_PORT_SCAN,
        "host_discovery": STAGE_HOST_DISCOVERY,
        "port_scan": STAGE_PORT_SCAN,
        "service_fingerprint": STAGE_SERVICE_BANNER,
    }
    for scan_type, ceiling in expected.items():
        _profile, factory, _services = engine._SCAN_MAP[scan_type]
        assert factory().stage_ceiling == ceiling


def test_engine_rejects_non_string_targets() -> None:
    result = engine.run_scan("discovery", {"targets": ["10.0.0.1", 7]})

    assert result["ok"] is False
    assert result["error_code"] == "invalid_targets"


def test_engine_rejects_oversized_cidr_instead_of_false_success() -> None:
    result = engine.run_scan("discovery", {"targets": ["10.0.0.0/8"]})

    assert result["ok"] is False
    assert result["error_code"] == "target_expansion_limit"
    assert result["facts"] == []


def test_empty_authoritative_scope_never_falls_back_to_job_targets() -> None:
    result = engine.run_scan(
        "discovery",
        {"targets": ["10.0.0.1"]},
        validated_scope=[],
    )

    assert result["ok"] is False
    assert result["error_code"] == "scope_empty"


def test_engine_exposes_component_manifest_and_run_states(monkeypatch) -> None:
    async def fake_run_engagement(
        targets,
        scope,
        *,
        cache,
        trace,
        **kwargs,
    ):
        result = ScanResult(
            scanner="tls_scan",
            target=targets[0],
            port=443,
            status="observed",
            data={"service": "https"},
        )
        cache.put(result)
        trace.record("tls_scan", target_count=1, results=[result])
        trace.finalize()
        return {}

    monkeypatch.setattr(engine, "run_engagement", fake_run_engagement)
    result = engine.run_scan(
        "tls_scan",
        {"target": "10.0.0.1"},
        validated_scope=["10.0.0.0/24"],
    )

    runs = {run["id"]: run for run in result["scanner_runs"]}
    assert result["ok"] is True
    assert result["engine"] == "scanner_module"
    assert result["engine_manifest"]["orchestrator"]["label"] == "Vedha Probe Collector"
    assert runs["tls_scan"]["status"] == "completed"
    assert runs["host_discovery"]["status"] == "skipped"


def test_engine_fails_when_every_observation_is_an_error(monkeypatch) -> None:
    async def fake_run_engagement(
        targets,
        scope,
        *,
        cache,
        trace,
        **kwargs,
    ):
        failure = scanner_failure_result(
            "host_discovery",
            targets[0],
            TimeoutError("deadline"),
        )
        cache.put(failure)
        trace.record("host_discovery", target_count=1, results=[failure])
        trace.finalize()
        return {}

    monkeypatch.setattr(engine, "run_engagement", fake_run_engagement)
    result = engine.run_scan(
        "discovery",
        {"target": "10.0.0.1"},
        validated_scope=["10.0.0.0/24"],
    )

    assert result["ok"] is False
    assert result["outcome"] == "failed"
    assert result["run_stats"]["fact_count"] == 0
    assert result["run_stats"]["error_count"] == 1
    assert result["scanner_runs"][0]["status"] == "failed"
