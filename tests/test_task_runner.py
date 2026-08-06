"""Tests for agent/task_runner.py"""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from agent.task_runner import TaskRunner


def _fake_run_scan(scan_type, params, **kwargs):
    """Return a minimal successful result without doing any real I/O."""
    return {
        "result_schema_version": "1.1",
        "probe_id": "test",
        "engagement_uuid": kwargs.get("engagement_uuid"),
        "use_case_id": kwargs.get("use_case_id"),
        "scan_type": scan_type,
        "profile": params.get("profile", "it"),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "ok": True,
        "engine": "test_fake",
        "facts": [],
        "run_stats": {"host_count": 0, "open_ports": 0, "fact_count": 0, "scanners_run": []},
        "errors": [],
        "host_count": 0,
        "service_count": 0,
        "open_ports": 0,
        "finding_count": 0,
        "params": params,  # echo params for test assertions
    }


@pytest.fixture
def runner():
    """TaskRunner with no-op dependencies (no real scanning)."""
    return TaskRunner(
        http_get=lambda path: None,
        submit_result=lambda jid, p: True,
        run_scan_fn=_fake_run_scan,
    )


class TestRunnerHeadless:
    """Tests that use the real engine but with no-op callbacks."""

    def test_rejects_unknown_use_case(self, runner):
        job = {
            "job_id": "job-001",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {"use_case_id": "uc_nonexistent"},
        }
        result = runner.run_job(job, "agent-1")
        assert result.success is False
        assert "Unknown use_case_id" in (result.error or "")

    def test_rejects_empty_targets(self, runner):
        job = {
            "job_id": "job-002",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {},
        }
        result = runner.run_job(job, "agent-1")
        assert result.success is False
        assert "No targets" in (result.error or "")

    def test_explicit_empty_targets_never_expand_to_engagement_scope(self, runner):
        runner._http_get = lambda path: {
            "scope_cidrs": ["10.0.0.0/24"],
            "excluded_cidrs": [],
        }
        result = runner.run_job({
            "job_id": "job-empty-explicit",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {
                "targets": [],
                "scope_cidrs": ["10.0.0.0/24"],
            },
        }, "agent-1")

        assert result.success is False
        assert "No targets" in (result.error or "")

    def test_resolves_use_case_correctly(self, runner):
        job = {
            "job_id": "job-003",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {"use_case_id": "uc_discovery_only", "targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.scan_type == "discovery"
        assert result.profile == "it"

    def test_resolves_full_assessment(self, runner):
        job = {
            "job_id": "job-004",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {"use_case_id": "uc_full_assessment", "targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.scan_type == "assessment"

    def test_uses_job_type_when_no_use_case(self, runner):
        job = {
            "job_id": "job-005",
            "engagement_id": "",
            "job_type": "tls_scan",
            "params": {"targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.scan_type == "tls_scan"

    def test_rejects_non_object_params(self, runner):
        result = runner.run_job(
            {
                "job_id": "job-invalid-params",
                "params": ["not", "an", "object"],
            },
            "agent-1",
        )

        assert result.success is False
        assert result.error == "job params must be an object"

    def test_rejects_non_string_target(self, runner):
        result = runner.run_job(
            {
                "job_id": "job-invalid-target",
                "params": {"targets": ["10.0.0.1", 7]},
            },
            "agent-1",
        )

        assert result.success is False
        assert result.error == "targets must be a string or list of strings"

    @pytest.mark.parametrize(
        ("params", "expected"),
        [
            (
                {
                    "targets": ["10.0.0.1"],
                    "target": "10.0.0.2",
                    "scope_cidrs": ["10.0.0.0/24"],
                },
                ["10.0.0.1"],
            ),
            (
                {
                    "target": "10.0.0.2",
                    "scope_cidrs": ["10.0.0.0/24"],
                },
                ["10.0.0.2"],
            ),
            (
                {"scope_cidrs": ["10.0.0.0/24"]},
                ["10.0.0.0/24"],
            ),
        ],
    )
    def test_target_precedence(self, runner, params, expected):
        result = runner.run_job(
            {
                "job_id": "job-target-precedence",
                "params": params,
            },
            "agent-1",
        )

        assert result.success is True
        assert result.result["params"]["targets"] == expected

    def test_scan_engine_exception_becomes_submittable_failure(self):
        submitted = []

        def explode(*args, **kwargs):
            raise RuntimeError("collector initialization failed")

        runner = TaskRunner(
            http_get=lambda path: None,
            submit_result=lambda job_id, payload: submitted.append(payload) or True,
            run_scan_fn=explode,
        )
        result = runner.run_job(
            {
                "job_id": "job-engine-error",
                "params": {"targets": ["10.0.0.1"]},
            },
            "agent-1",
        )

        assert result.success is False
        assert result.result["error_code"] == "scan_engine_exception"
        assert submitted[0]["result"]["outcome"] == "failed"


class TestRunnerScopeValidation:
    def test_rejects_out_of_scope_target(self, runner):
        """When scope is fetched and targets are outside it."""
        runner._http_get = lambda path: {
            "scope_cidrs": ["10.0.0.0/24"],
            "excluded_cidrs": [],
        }
        job = {
            "job_id": "job-010",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["192.168.1.1"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.success is False
        assert "outside" in (result.error or "")

    def test_allows_in_scope_target(self, runner):
        runner._http_get = lambda path: {
            "scope_cidrs": ["10.0.0.0/24"],
            "excluded_cidrs": [],
        }
        job = {
            "job_id": "job-011",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")
        # Should proceed (no scope rejection). Result may fail for other reasons
        # (e.g. no actual network targets), but should NOT be a scope error.
        assert "outside" not in (result.error or "")

    def test_explicit_empty_local_ceiling_fails_closed(self):
        local_runner = TaskRunner(
            http_get=lambda path: {
                "scope_cidrs": ["10.0.0.0/24"],
                "excluded_cidrs": [],
            },
            submit_result=lambda jid, payload: True,
            run_scan_fn=_fake_run_scan,
            local_allowed_networks=[],
        )
        result = local_runner.run_job({
            "job_id": "job-local-empty",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.1"]},
        }, "agent-1")

        assert result.success is False
        assert "local network ceiling" in (result.error or "")

    def test_local_ceiling_filters_manager_authorized_targets(self):
        local_runner = TaskRunner(
            http_get=lambda path: {
                "scope_cidrs": ["10.0.0.0/16"],
                "excluded_cidrs": [],
            },
            submit_result=lambda jid, payload: True,
            run_scan_fn=_fake_run_scan,
            local_allowed_networks=["10.0.8.0/24"],
        )
        result = local_runner.run_job({
            "job_id": "job-local-filter",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["10.0.8.10", "10.0.9.10"]},
        }, "agent-1")

        assert result.success is True
        assert result.result["params"]["targets"] == ["10.0.8.10"]

    def test_local_ceiling_is_forwarded_to_engine(self):
        captured = {}

        def capture(scan_type, params, **kwargs):
            captured.update(kwargs)
            return _fake_run_scan(scan_type, params, **kwargs)

        local_runner = TaskRunner(
            http_get=lambda path: {
                "scope_cidrs": ["10.0.0.0/24"],
                "excluded_cidrs": [],
            },
            submit_result=lambda jid, payload: True,
            run_scan_fn=capture,
            local_allowed_networks=["10.0.0.0/24"],
        )
        result = local_runner.run_job({
            "job_id": "job-local-forward",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.10"]},
        }, "agent-1")

        assert result.success is True
        assert captured["local_allowed_scope"] == ["10.0.0.0/24"]

    def test_rejects_excluded_target(self, runner):
        runner._http_get = lambda path: {
            "scope_cidrs": ["10.0.0.0/24"],
            "excluded_cidrs": ["10.0.0.5/32"],
        }
        job = {
            "job_id": "job-012",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.5"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.success is False
        assert "excluded" in (result.error or "").lower()

    def test_scope_fallback_when_fetch_fails(self, runner):
        """When scope fetch fails, manager-embedded scope is still enforced."""
        runner._http_get = lambda path: None
        job = {
            "job_id": "job-013",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.1"], "scope_cidrs": ["10.0.0.0/24"]},
        }
        result = runner.run_job(job, "agent-1")
        # Should proceed using params-based scope. No scope rejection.
        assert "outside" not in (result.error or "")

    def test_scope_fallback_preserves_manager_and_job_exclusions(self, runner):
        runner._http_get = lambda path: None
        job = {
            "job_id": "job-013a",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {
                "targets": ["10.0.0.5", "10.0.0.10", "10.0.0.20"],
                "scope_cidrs": ["10.0.0.0/24"],
                "_excluded_cidrs": ["10.0.0.5/32"],
                "excluded_cidrs": ["10.0.0.20/32"],
            },
        }

        result = runner.run_job(job, "agent-1")

        assert result.success is True
        assert result.result["params"]["targets"] == ["10.0.0.10"]
        assert result.result["params"]["excluded_cidrs"] == [
            "10.0.0.5/32",
            "10.0.0.20/32",
        ]

    def test_manager_job_without_scope_fails_closed(self, runner):
        runner._http_get = lambda path: None
        job = {
            "job_id": "job-013b",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.success is False
        assert "No authoritative scope" in (result.error or "")

    def test_merge_engagement_and_job_excludes(self, runner):
        runner._http_get = lambda path: {
            "scope_cidrs": ["10.0.0.0/24"],
            "excluded_cidrs": ["10.0.0.5/32"],
        }
        job = {
            "job_id": "job-014",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "params": {
                "targets": ["10.0.0.5", "10.0.0.10", "10.0.0.20"],
                "excluded_cidrs": ["10.0.0.20/32"],
            },
        }
        result = runner.run_job(job, "agent-1")
        # Non-excluded target 10.0.0.10 should remain and scan succeeds
        assert result.success is True
        # Both 10.0.0.5 and 10.0.0.20 should be excluded
        assert "10.0.0.10" in result.result.get("params", {}).get("targets", [])
        assert "10.0.0.5" not in result.result.get("params", {}).get("targets", [])
        assert "10.0.0.20" not in result.result.get("params", {}).get("targets", [])


class TestRunnerSubmission:
    def test_calls_submit_with_result(self):
        """Verify the submit callback is called with the correct payload."""
        submitted = []

        def submit(jid, payload):
            submitted.append((jid, payload))
            return True

        runner = TaskRunner(
            http_get=lambda path: None,
            submit_result=submit,
            run_scan_fn=_fake_run_scan,
        )
        job = {
            "job_id": "job-020",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.1"]},
        }
        runner.run_job(job, "agent-1")
        assert len(submitted) == 1
        assert submitted[0][0] == "job-020"
        assert "success" in submitted[0][1]
        assert "result" in submitted[0][1]

    def test_uses_spool_when_available(self):
        """When spool_submit is provided, it's used instead of direct submit."""
        direct_calls = []
        spool_calls = []

        def direct(jid, payload):
            direct_calls.append(jid)
            return True

        def spool(jid, payload, upload_fn):
            spool_calls.append(jid)
            return True

        runner = TaskRunner(
            http_get=lambda path: None,
            submit_result=direct,
            spool_submit=spool,
            run_scan_fn=_fake_run_scan,
        )
        job = {
            "job_id": "job-030",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {"targets": ["10.0.0.1"]},
        }
        runner.run_job(job, "agent-1")
        # The spool callback should have been called
        assert len(spool_calls) == 1
        # Direct should NOT have been called (spool wraps direct)
        assert len(direct_calls) == 0


class TestRunnerScanTypes:
    def test_ot_passive_profile(self, runner):
        job = {
            "job_id": "job-040",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {"use_case_id": "uc_ot_passive", "targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.scan_type == "passive_discovery"
        assert result.profile == "ot"

    def test_web_triage_scan_type(self, runner):
        job = {
            "job_id": "job-041",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {"use_case_id": "uc_external_web_triage", "targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")
        assert result.scan_type == "web_tls_scan"
