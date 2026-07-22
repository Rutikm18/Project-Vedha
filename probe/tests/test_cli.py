from __future__ import annotations

import json
import sys
import stat
import types
from argparse import Namespace

import pytest
from agent import cli


def test_config_store_writes_private_file(tmp_path):
    path = tmp_path / "probe-cli.json"
    store = cli.ConfigStore(path)
    store.set_profile(
        "default",
        {
            "manager_url": "https://manager.example.com",
            "token": "vpat_test",
            "verify_tls": True,
        },
    )

    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode == 0o600
    data = json.loads(path.read_text())
    assert data["profiles"]["default"]["token"] == "vpat_test"


def test_config_store_rejects_malformed_json(tmp_path):
    path = tmp_path / "probe-cli.json"
    path.write_text("{not-json")
    with pytest.raises(cli.CliError):
        cli.ConfigStore(path).load()


def test_config_store_rejects_non_object_profiles(tmp_path):
    path = tmp_path / "probe-cli.json"
    path.write_text(json.dumps({"profiles": []}))
    with pytest.raises(cli.CliError, match="profiles must be an object"):
        cli.ConfigStore(path).load()


def test_parse_param_pairs_supports_json_values():
    parsed = cli.parse_param_pairs([
        "rate=25",
        "dry_run=true",
        "ports=1-1024",
        'tags=["dmz","first-run"]',
    ])

    assert parsed["rate"] == 25
    assert parsed["dry_run"] is True
    assert parsed["ports"] == "1-1024"
    assert parsed["tags"] == ["dmz", "first-run"]


def test_parse_param_pairs_rejects_missing_equals():
    with pytest.raises(cli.CliError, match="expected key=value"):
        cli.parse_param_pairs(["rate"])


def test_split_values_accepts_repeated_and_csv_values():
    assert cli.split_values(["10.0.0.1,10.0.0.2", "10.0.0.3"]) == [
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.3",
    ]


def test_normalize_manager_url_trims_and_validates():
    assert cli.normalize_manager_url("https://manager.example.com///") == "https://manager.example.com"
    with pytest.raises(cli.CliError):
        cli.normalize_manager_url("manager.example.com")
    with pytest.raises(cli.CliError):
        cli.normalize_manager_url(" ")


def test_parser_accepts_json_after_concrete_commands():
    parser = cli.build_parser()

    args = parser.parse_args([
        "auth", "login",
        "--manager", "http://127.0.0.1:18080",
        "--pat", "vpat_test",
        "--json",
    ])
    assert args.json is True

    args = parser.parse_args(["whoami", "--json"])
    assert args.json is True

    args = parser.parse_args([
        "scan", "run",
        "--engagement-id", "eng-1",
        "--json",
    ])
    assert args.json is True

    args = parser.parse_args(["doctor", "--engagement-id", "eng-1", "--json"])
    assert args.json is True
    assert args.engagement_id == "eng-1"


def test_resolve_profile_env_overrides_config(tmp_path, monkeypatch):
    path = tmp_path / "probe-cli.json"
    cli.ConfigStore(path).set_profile(
        "default",
        {
            "manager_url": "https://stored.example.com",
            "token": "vpat_stored",
            "verify_tls": True,
            "ca_bundle": None,
        },
    )
    monkeypatch.setenv("PROBE_MANAGER_URL", "https://env.example.com")
    monkeypatch.setenv("PROBE_PAT", "vpat_env")

    profile = cli.resolve_profile(Namespace(
        config=str(path),
        profile="default",
        manager=None,
        pat=None,
        insecure=False,
        ca_bundle=None,
        timeout=1,
    ))

    assert profile["manager_url"] == "https://env.example.com"
    assert profile["token"] == "vpat_env"


def test_resolve_profile_reports_missing_manager_or_token(tmp_path):
    args = Namespace(
        config=str(tmp_path / "missing.json"),
        profile="default",
        manager=None,
        pat=None,
        insecure=False,
        ca_bundle=None,
        timeout=1,
    )
    with pytest.raises(cli.CliError, match="manager"):
        cli.resolve_profile(args)

    args.manager = "https://manager.example.com"
    with pytest.raises(cli.CliError, match="pat"):
        cli.resolve_profile(args)


class FakeClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, path, *, json_body=None, params=None):
        self.calls.append((method, path, json_body, params))
        if not self.responses:
            return {}
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def test_cmd_scan_run_builds_dispatch_payload(monkeypatch):
    fake = FakeClient([{"job_id": "job-1", "job_type": "discovery", "status": "pending"}])
    monkeypatch.setattr(cli, "client_from_args", lambda args: fake)
    monkeypatch.setattr(cli, "output", lambda *args, **kwargs: None)

    rc = cli.cmd_scan_run(Namespace(
        engagement_id="eng-1",
        job_type="discovery",
        use_case="uc_web_app_triage",
        target=["10.0.0.10,10.0.0.11"],
        ports="80,443",
        param=["rate=25", "dry_run=true"],
        wait=False,
        poll_interval=5,
        wait_timeout=60,
        json=False,
    ))

    assert rc == 0
    assert fake.calls == [(
        "POST",
        "/agents/jobs",
        {
            "engagement_id": "eng-1",
            "job_type": "discovery",
            "use_case_id": "uc_web_app_triage",
            "params": {
                "rate": 25,
                "dry_run": True,
                "targets": ["10.0.0.10", "10.0.0.11"],
                "ports": "80,443",
            },
        },
        None,
    )]


def test_cmd_doctor_success_with_online_agent(tmp_path, monkeypatch):
    path = tmp_path / "probe-cli.json"
    cli.ConfigStore(path).set_profile(
        "default",
        {
            "manager_url": "http://127.0.0.1:18080",
            "token": "vpat_profile",
            "verify_tls": True,
            "ca_bundle": None,
        },
    )
    fake = FakeClient([
        {"status": "healthy"},
        {"auth_type": "pat", "role": "manager", "scopes": ["probe:read", "probe:write"]},
        [{"use_case_id": "uc_discovery_only"}],
        [{"id": "agent-1", "online": True}],
        {"engagement_id": "eng-1", "scope_cidrs": ["10.0.0.0/24"]},
    ])
    monkeypatch.setattr(cli, "ManagerClient", lambda *args, **kwargs: fake)
    monkeypatch.setattr(cli, "output", lambda *args, **kwargs: None)

    rc = cli.cmd_doctor(Namespace(
        config=str(path),
        profile="default",
        manager=None,
        pat=None,
        insecure=False,
        ca_bundle=None,
        timeout=1,
        engagement_id="eng-1",
        allow_no_agent=False,
        json=True,
    ))

    assert rc == 0
    assert [call[1] for call in fake.calls] == [
        "/health",
        "/auth/me",
        "/agents/use-cases",
        "/agents",
        "/engagements/eng-1/scope",
    ]


def test_cmd_doctor_fails_when_no_agent_unless_allowed(tmp_path, monkeypatch):
    path = tmp_path / "probe-cli.json"
    cli.ConfigStore(path).set_profile(
        "default",
        {
            "manager_url": "https://manager.example.com",
            "token": "vpat_profile",
            "verify_tls": True,
            "ca_bundle": None,
        },
    )

    def fake_client():
        return FakeClient([
            {"status": "healthy"},
            {"auth_type": "pat", "role": "manager", "scopes": ["probe:read"]},
            [{"use_case_id": "uc_discovery_only"}],
            [{"id": "agent-1", "online": False}],
        ])

    current = fake_client()
    monkeypatch.setattr(cli, "ManagerClient", lambda *args, **kwargs: current)
    monkeypatch.setattr(cli, "output", lambda *args, **kwargs: None)
    args = Namespace(
        config=str(path),
        profile="default",
        manager=None,
        pat=None,
        insecure=False,
        ca_bundle=None,
        timeout=1,
        engagement_id=None,
        allow_no_agent=False,
        json=True,
    )

    assert cli.cmd_doctor(args) == 1

    current = fake_client()
    args.allow_no_agent = True
    assert cli.cmd_doctor(args) == 0


def test_poll_job_rejects_invalid_timing():
    with pytest.raises(cli.CliError, match="poll-interval"):
        cli._poll_job(FakeClient([]), "job-1", 0, 10)
    with pytest.raises(cli.CliError, match="wait-timeout"):
        cli._poll_job(FakeClient([]), "job-1", 1, -1)


def test_poll_job_returns_terminal_status():
    fake = FakeClient([
        {"job_id": "job-1", "status": "running"},
        {"job_id": "job-1", "status": "completed"},
    ])
    out = cli._poll_job(fake, "job-1", interval=0.01, timeout=5)
    assert out["status"] == "completed"
    assert [call[1] for call in fake.calls] == ["/agents/jobs/job-1", "/agents/jobs/job-1"]


def test_poll_job_times_out(monkeypatch):
    fake = FakeClient([{"job_id": "job-1", "status": "running"}])
    times = iter([0.0, 2.0])
    monkeypatch.setattr(cli.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(cli.time, "sleep", lambda _interval: None)

    with pytest.raises(cli.CliError, match="timed out"):
        cli._poll_job(fake, "job-1", interval=1, timeout=1)


def test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity(tmp_path, monkeypatch):
    path = tmp_path / "probe-cli.json"
    cli.ConfigStore(path).set_profile(
        "default",
        {
            "manager_url": "https://manager.example.com",
            "token": "vpat_profile",
            "verify_tls": False,
            "ca_bundle": "/tmp/ca.pem",
        },
    )
    monkeypatch.setenv("PLATFORM_URL", "https://stale.example.com")
    monkeypatch.setenv("OPERATOR_TOKEN", "vpat_stale")
    called = {"main": False}
    fake_agent = types.ModuleType("agent.agent")
    fake_agent.main = lambda: called.update(main=True)
    monkeypatch.setitem(sys.modules, "agent.agent", fake_agent)

    rc = cli.cmd_daemon_run(Namespace(
        config=str(path),
        profile="default",
        manager="https://manager.example.com",
        pat="vpat_arg",
        insecure=False,
        ca_bundle=None,
        timeout=1,
        name="dmz-probe",
        location="DMZ",
        segment=["10.0.0.0/24,10.0.1.0/24"],
    ))

    assert rc == 0
    assert called["main"] is True
    assert cli.os.environ["PLATFORM_URL"] == "https://manager.example.com"
    assert cli.os.environ["OPERATOR_TOKEN"] == "vpat_arg"
    assert cli.os.environ["VERIFY_TLS"] == "false"
    assert cli.os.environ["PROBE_CA_BUNDLE"] == "/tmp/ca.pem"
    assert cli.os.environ["PROBE_NAME"] == "dmz-probe"
    assert cli.os.environ["PROBE_LOCATION"] == "DMZ"
    assert cli.os.environ["PROBE_NETWORK_SEGMENTS"] == "10.0.0.0/24,10.0.1.0/24"
