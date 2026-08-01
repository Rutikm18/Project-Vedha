from __future__ import annotations

import json
import stat
from argparse import Namespace

import pytest

from agent import cli
from agent.validation import (
    resolve_use_cases,
    score_inventory,
    target_address_count,
    validate_ground_truth,
    validate_targets,
)


def test_resolve_use_cases_deduplicates_combined_suites():
    assert resolve_use_cases(
        ["web", "infrastructure"],
        ["uc_external_web_triage"],
    ) == [
        "uc_discovery_only",
        "uc_external_web_triage",
        "uc_web_app_triage",
        "uc_db_exposure",
        "uc_windows_estate",
    ]


def test_validate_targets_enforces_scope_and_exclusions():
    validate_targets(["10.0.0.10", "10.0.0.16/30"], ["10.0.0.0/24"], [])

    with pytest.raises(ValueError, match="outside"):
        validate_targets(["10.0.1.10"], ["10.0.0.0/24"], [])
    with pytest.raises(ValueError, match="overlaps"):
        validate_targets(
            ["10.0.0.16/30"],
            ["10.0.0.0/24"],
            ["10.0.0.18/32"],
        )
    with pytest.raises(ValueError, match="IP address or CIDR"):
        validate_targets(["host.example"], ["10.0.0.0/24"], [])


def test_target_address_count_is_conservative():
    assert target_address_count(["10.0.0.1", "10.0.1.0/24"]) == 257


def test_validate_ground_truth_rejects_invalid_ports_and_duplicate_hosts():
    with pytest.raises(ValueError, match="outside"):
        validate_ground_truth({
            "hosts": [{"ip": "10.0.0.1", "ports": [{"port": 70000}]}],
        })
    with pytest.raises(ValueError, match="duplicate"):
        validate_ground_truth({
            "hosts": [{"ip": "10.0.0.1"}, {"ip": "10.0.0.1"}],
        })


def test_score_inventory_reports_precision_recall_and_unscored_dimensions():
    truth = {
        "hosts": [
            {
                "ip": "10.0.0.10",
                "ports": [
                    {"port": 22, "protocol": "tcp", "service": "ssh"},
                    {"port": 443, "protocol": "tcp"},
                ],
                "cves": ["CVE-2026-0001"],
            },
            {"ip": "10.0.0.20"},
        ],
    }
    assets = [
        {
            "id": "asset-1",
            "ip_address": "10.0.0.10",
            "services": [
                {"port": 22, "protocol": "tcp", "service": "ssh"},
                {"port": 80, "protocol": "tcp", "service": "http"},
            ],
        },
        {"id": "asset-3", "ip_address": "10.0.0.30", "services": []},
    ]
    findings = [{"asset_id": "asset-1", "cve_ids": ["CVE-2026-0001"]}]

    scored = score_inventory(truth, assets, findings)

    assert scored["hosts"]["true_positive"] == 1
    assert scored["hosts"]["false_positive"] == 1
    assert scored["hosts"]["false_negative"] == 1
    assert scored["ports"]["true_positive"] == 1
    assert scored["ports"]["false_positive"] == 1
    assert scored["ports"]["false_negative"] == 1
    assert scored["services"]["true_positive"] == 1
    assert scored["cves"]["recall"] == 1.0

    host_only = score_inventory(
        {"hosts": [{"ip": "10.0.0.10"}]},
        assets,
        findings,
    )
    assert host_only["ports"]["scored"] is False
    assert host_only["services"]["scored"] is False
    assert host_only["cves"]["scored"] is False


class FakeClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, path, *, json_body=None, params=None):
        self.calls.append((method, path, json_body, params))
        return self.responses.pop(0)


def _validation_args(tmp_path, **overrides):
    path = tmp_path / "probe-cli.json"
    cli.ConfigStore(path).set_profile(
        "validation",
        {
            "manager_url": "https://manager.example.com",
            "token": "vpat_test",
            "verify_tls": True,
            "ca_bundle": None,
        },
    )
    values = {
        "config": str(path),
        "profile": "validation",
        "manager": None,
        "pat": None,
        "insecure": False,
        "ca_bundle": None,
        "timeout": 1,
        "engagement_id": None,
        "engagement_name": "Validation",
        "scope": ["10.0.0.10/32"],
        "exclude": None,
        "target": ["10.0.0.10"],
        "scan_profile": "it",
        "suite": ["baseline"],
        "use_case": None,
        "ports": "22,443",
        "repeat": 3,
        "ground_truth": None,
        "strict_ground_truth": False,
        "output_dir": str(tmp_path / "results"),
        "poll_interval": 1,
        "wait_timeout": 30,
        "settle_seconds": 0,
        "allow_multiple_agents": False,
        "allow_large_targets": False,
        "confirm_authorized": False,
        "dry_run": True,
        "json": True,
    }
    values.update(overrides)
    return Namespace(**values)


def _preflight_responses(agent_count=1):
    return [
        {
            "auth_type": "pat",
            "role": "manager",
            "scopes": [
                "probe:read",
                "probe:write",
                "engagement:read",
                "engagement:write",
            ],
        },
        [{"use_case_id": "uc_discovery_only", "scan_type": "discovery"}],
        [
            {
                "id": f"agent-{index}",
                "name": f"probe-{index}",
                "online": True,
                "capabilities": ["discovery"],
            }
            for index in range(agent_count)
        ],
    ]


def test_cmd_validate_dry_run_performs_no_mutating_requests(tmp_path, monkeypatch):
    fake = FakeClient(_preflight_responses())
    monkeypatch.setattr(cli, "ManagerClient", lambda *args, **kwargs: fake)
    captured = []
    monkeypatch.setattr(
        cli,
        "output",
        lambda data, **kwargs: captured.append(data),
    )

    assert cli.cmd_validate(_validation_args(tmp_path)) == 0
    assert all(method == "GET" for method, *_ in fake.calls)
    assert captured[0]["dry_run"] is True
    assert captured[0]["plan"]["targets"] == ["10.0.0.10"]


def test_cmd_validate_refuses_ambiguous_multi_probe_scheduling(tmp_path, monkeypatch):
    fake = FakeClient(_preflight_responses(agent_count=2))
    monkeypatch.setattr(cli, "ManagerClient", lambda *args, **kwargs: fake)

    with pytest.raises(cli.CliError, match="multiple Probes can reach"):
        cli.cmd_validate(_validation_args(tmp_path))


def test_cmd_validate_executes_one_bounded_job_and_protects_results(
    tmp_path, monkeypatch,
):
    responses = _preflight_responses() + [
        {"id": "eng-1"},
        {"job_id": "job-1", "status": "pending"},
        {
            "job_id": "job-1",
            "status": "completed",
            "result": {"fact_count": 2},
        },
        [
            {
                "id": "asset-1",
                "ip_address": "10.0.0.10",
                "services": [{"port": 22, "protocol": "tcp", "service": "ssh"}],
            },
        ],
        {"items": [], "total": 0},
    ]
    fake = FakeClient(responses)
    monkeypatch.setattr(cli, "ManagerClient", lambda *args, **kwargs: fake)
    monkeypatch.setattr(cli, "output", lambda *args, **kwargs: None)
    args = _validation_args(
        tmp_path,
        repeat=1,
        dry_run=False,
        confirm_authorized=True,
    )

    assert cli.cmd_validate(args) == 0
    assert [method for method, *_ in fake.calls].count("POST") == 2
    summary_path = tmp_path / "results" / "summary.json"
    summary = json.loads(summary_path.read_text())
    assert summary["jobs_total"] == 1
    assert summary["jobs_failed"] == 0
    assert stat.S_IMODE(summary_path.stat().st_mode) == 0o600
    assert stat.S_IMODE(summary_path.parent.stat().st_mode) == 0o700


def test_parser_accepts_validate_command():
    args = cli.build_parser().parse_args([
        "validate",
        "--scope", "10.0.0.10/32",
        "--target", "10.0.0.10",
        "--suite", "web",
        "--repeat", "2",
        "--dry-run",
        "--json",
    ])

    assert args.command == "validate"
    assert args.suite == ["web"]
    assert args.repeat == 2
    assert args.dry_run is True
    assert args.json is True
