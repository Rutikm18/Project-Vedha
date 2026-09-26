"""test_remediation_plan.py — contextual plan assembly (pure)."""
from __future__ import annotations

from types import SimpleNamespace

from app.remediation import plan as P
from app.remediation.context import build_context


def _finding(evidence=None, cve_ids=None, severity="high", title="t", epss=None, validated=False):
    return SimpleNamespace(id="f1", title=title, description="", remediation="",
                           evidence=evidence or {}, cve_ids=cve_ids or [],
                           severity=SimpleNamespace(value=severity), epss_score=epss,
                           exploit_validated=validated)


def _asset(os="Windows", os_version="Windows Server 2012 R2", criticality="high", tags=None,
           environment=None):
    return SimpleNamespace(ip_address="10.0.0.5", hostname="FS01", fqdn=None, os=os,
                           os_version=os_version, asset_type=SimpleNamespace(value="server"),
                           criticality=SimpleNamespace(value=criticality), environment=environment,
                           tags=tags)


def _svc(port=445, product="Microsoft Windows SMB", version=None, exposure=None):
    return SimpleNamespace(port=port, protocol="tcp", service_name="microsoft-ds", product=product,
                           version=version, cpe=None, banner=None, exposure=exposure)


def _smb_plan(**kw):
    f = _finding({"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445}, severity="critical")
    ctx = build_context(f, _asset(), _svc())
    return P.build_plan(f, ctx, **kw)


class TestSmbV1Example:
    def test_recipe_and_context(self):
        plan = _smb_plan()
        assert plan["recipe_id"] == "POSTURE-SMB-V1-ENABLED"
        assert plan["context"]["host"]["value"] == "FS01"
        assert plan["context"]["port"]["value"] == 445

    def test_os_auto_selected_from_scan(self):
        plan = _smb_plan()
        assert plan["os_auto"] == "windows" and plan["os"] == "windows"
        fix = next(s for s in plan["steps"] if s["tier"] == "fix")
        assert any("EnableSMB1Protocol" in c for c in fix["commands_for_os"])

    def test_explicit_os_overrides(self):
        plan = _smb_plan(os="linux")
        fix = next(s for s in plan["steps"] if s["tier"] == "fix")
        assert any("smb.conf" in c for c in fix["commands_for_os"])

    def test_facts_filled_into_text(self):
        plan = _smb_plan()
        assert "FS01" in plan["summary"]
        fix = next(s for s in plan["steps"] if s["tier"] == "fix")
        assert "Windows" in fix["description"]
        assert "10.0.0.5" in plan["verification_check"]["check"]

    def test_standard_vocabulary(self):
        plan = _smb_plan()
        assert plan["remediation_type"] == "mitigation"
        assert plan["risk_response"] == "mitigate"
        assert plan["target_state"].startswith("SMBv1 disabled")

    def test_back_compat_keys(self):
        plan = _smb_plan()
        for key in ("category", "os", "source", "summary", "effort", "remediation_risk", "steps",
                    "verification", "long_term_recommendations", "compensating_controls"):
            assert key in plan
        assert plan["source"] == "deterministic_kb"
        s = plan["steps"][0]
        for key in ("step", "title", "description", "commands_for_os", "verification", "risk"):
            assert key in s
        assert [s["step"] for s in plan["steps"]] == list(range(1, len(plan["steps"]) + 1))

    def test_remediation_risk_is_worst_step(self):
        assert _smb_plan()["remediation_risk"] == "medium"

    def test_provenance(self):
        plan = _smb_plan()
        assert plan["provenance"]["source"] == "kb"
        assert "host" in plan["provenance"]["facts_used"]
        assert plan["provenance"]["recipe_version"] == 1

    def test_due_passthrough(self):
        due = {"at": "2026-10-01T00:00:00+05:30", "source": "engagement"}
        assert _smb_plan(due=due)["due"] == due
        assert _smb_plan()["due"] == {"at": None, "source": None}


class TestTargetState:
    def test_cve_with_fixed_version(self):
        f = _finding({"fixed_version": "9.8p1", "product": "openssh", "matched_version": "8.2p1"},
                     cve_ids=["CVE-2024-6387"])
        plan = P.build_plan(f, build_context(f, _asset(os="Linux", os_version="Ubuntu 20.04"), None))
        assert plan["recipe_id"] == "CVE-PATCH"
        assert plan["target_state"] == "openssh ≥ 9.8p1"
        fix = next(s for s in plan["steps"] if s["tier"] == "fix")
        assert "9.8p1" in fix["description"]
        assert any("--only-upgrade openssh-server" in c for c in fix["commands_for_os"])

    def test_unknown_product_keeps_explicit_placeholder(self):
        assert P.package_for("WidgetOS") == "<package that ships WidgetOS>"
        assert P.package_for("OpenSSH") == "openssh-server" and P.package_for("nginx 1.18") == "nginx"

    def test_cve_without_fixed_version(self):
        f = _finding({"product": "openssh"}, cve_ids=["CVE-2024-6387"])
        plan = P.build_plan(f, build_context(f, _asset(), None))
        assert "confirm the fixed version" in plan["target_state"]


class TestMissingFacts:
    def test_not_recorded_rendered(self):
        f = _finding({"rule_id": "POSTURE-TLS-DEPRECATED-VERSION"})
        plan = P.build_plan(f, build_context(f, None, None))
        fix = next(s for s in plan["steps"] if s["tier"] == "fix")
        assert "not recorded" in fix["description"]
        assert plan["os_auto"] == "generic"


class TestFragile:
    def test_fragile_guard_prefixes_steps(self):
        f = _finding({"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445})
        a = _asset(tags={"auto": [{"key": "sector_fn", "value": "swift"}], "manual": []})
        plan = P.build_plan(f, build_context(f, a, _svc()))
        assert plan["fragile_guard"]["active"] is True
        assert all(s["description"].startswith("Coordinate with the asset owner") for s in plan["steps"])


class TestUrgency:
    def test_kev_internet_critical_is_act(self):
        f = _finding({"kev": True, "internet_facing": True}, severity="critical")
        u = P.urgency_for(build_context(f, _asset(criticality="critical"), None), "critical")
        assert u["label"] == "act"
        assert any("known exploited" in d.lower() for d in u["drivers"])

    def test_kev_internal_is_attend(self):
        f = _finding({"kev": True, "internet_facing": False}, severity="high")
        assert P.urgency_for(build_context(f, _asset(criticality="low"), None), "high")["label"] == "attend"

    def test_quiet_is_track(self):
        f = _finding({}, severity="medium")
        assert P.urgency_for(build_context(f, _asset(criticality="low"), None), "medium")["label"] == "track"

    def test_poc_high_mission_is_attend(self):
        f = _finding({}, severity="high", epss=0.8)
        assert P.urgency_for(build_context(f, _asset(criticality="critical"), None), "high")["label"] == "attend"

    def test_poc_total_automatable_is_track_star(self):
        f = _finding({"internet_facing": True}, severity="critical", validated=True)
        assert P.urgency_for(build_context(f, _asset(criticality="low"), None), "critical")["label"] == "track_star"
