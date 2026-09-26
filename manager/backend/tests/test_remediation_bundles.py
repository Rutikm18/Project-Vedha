"""test_remediation_bundles.py — deterministic fix bundles (pure)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.remediation import bundles as B
from app.remediation.context import build_context

NOW = datetime(2026, 9, 27, tzinfo=timezone.utc)


def _asset(ip, host, os_version="Windows Server 2019"):
    return SimpleNamespace(ip_address=ip, hostname=host, fqdn=None, os="Windows" if "Windows" in os_version
                           else "Linux", os_version=os_version, asset_type=SimpleNamespace(value="server"),
                           criticality=SimpleNamespace(value="medium"), environment=None, tags=None)


def _svc(port, product, banner=None):
    return SimpleNamespace(port=port, protocol="tcp", service_name="svc", product=product, version=None,
                           cpe=None, banner=banner, exposure=None)


_n = 0


def _f(ev, status="open", severity="high", cve_ids=None, resolved_at=None):
    global _n
    _n += 1
    return SimpleNamespace(id=f"f{_n}", title=f"finding {_n}", description="", remediation="",
                           evidence=ev, cve_ids=cve_ids or [], severity=SimpleNamespace(value=severity),
                           status=SimpleNamespace(value=status), epss_score=None, exploit_validated=False,
                           resolved_at=resolved_at)


def _item(finding, asset, svc=None, due_days=None, source="tenant"):
    ctx = build_context(finding, asset, svc)
    due = {"at": NOW + timedelta(days=due_days), "source": source} if due_days is not None else None
    return finding, ctx, due


def _smb(ip, host, **kw):
    return _item(_f({"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445}, **{k: v for k, v in kw.items()
                                                                        if k in ("status", "severity")}),
                 _asset(ip, host), _svc(445, "SMB"), due_days=kw.get("due_days", 7))


class TestKey:
    def test_same_inputs_same_key(self):
        a = B.fix_key_for("POSTURE-TLS-DEPRECATED-VERSION", "nginx", "TLS 1.2+")
        assert a == B.fix_key_for("POSTURE-TLS-DEPRECATED-VERSION", "nginx", "TLS 1.2+")
        assert len(a) == 12
        assert B.fix_ref(a) == "FIX-" + a[:6].upper()

    def test_banner_casing_does_not_split(self):
        i1 = _item(_f({"rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "port": 443}),
                   _asset("10.0.0.1", "w1"), _svc(443, "nginx"))
        i2 = _item(_f({"rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "port": 443}),
                   _asset("10.0.0.2", "w2"), _svc(443, "  NGINX "))
        assert len(B.build_bundles([i1, i2], now=NOW)) == 1

    def test_product_splits(self):
        i1 = _item(_f({"rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "port": 443}),
                   _asset("10.0.0.1", "w1"), _svc(443, "nginx"))
        i2 = _item(_f({"rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "port": 443}),
                   _asset("10.0.0.2", "w2"), _svc(443, "Microsoft IIS"))
        assert len(B.build_bundles([i1, i2], now=NOW)) == 2


class TestBundle:
    def test_fleet_bundle_with_checklist_and_earliest_due(self):
        items = [_smb("10.0.0.1", "a", due_days=10), _smb("10.0.0.2", "b", due_days=3),
                 _smb("10.0.0.3", "c", due_days=5)]
        [b] = B.build_bundles(items, now=NOW)
        assert b["recipe_id"] == "POSTURE-SMB-V1-ENABLED"
        assert len(b["hosts"]) == 3
        assert len(b["resolves"]) == 3
        assert b["due_at"] == NOW + timedelta(days=3)
        assert b["progress"] == {"closed": 0, "total": 3}
        assert b["status"] == "open"
        assert "windows" in b["steps_by_os"]
        assert "3 hosts" in b["title"]

    def test_closed_and_excluded(self):
        items = [_smb("10.0.0.1", "a"), _smb("10.0.0.2", "b", status="remediated"),
                 _smb("10.0.0.3", "c", status="accepted"), _smb("10.0.0.4", "d", status="fp")]
        [b] = B.build_bundles(items, now=NOW)
        assert b["open_count"] == 1 and b["closed_count"] == 1
        assert {e["reason"] for e in b["excluded"]} == {"risk accepted", "false positive"}
        assert b["progress"] == {"closed": 1, "total": 2}
        statuses = {h["ip"]: h["status"] for h in b["hosts"]}
        assert statuses["10.0.0.2"] == "closed" and statuses["10.0.0.3"] == "excluded"

    def test_done_when_all_closed(self):
        [b] = B.build_bundles([_smb("10.0.0.1", "a", status="remediated")], now=NOW)
        assert b["status"] == "done" and b["due_at"] is None

    def test_extension_status(self):
        f = _f({"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445})
        it = _item(f, _asset("10.0.0.9", "z"), _svc(445, "SMB"), due_days=40, source="extension")
        [b] = B.build_bundles([it], now=NOW)
        assert b["hosts"][0]["status"] == "extension_approved"
        assert b["due_source"] == "extension"

    def test_generic_single_member(self):
        it = _item(_f({}), _asset("10.0.0.1", "a"))
        it[0].title = "Interesting behaviour observed"
        [b] = B.build_bundles([it], now=NOW)
        assert b["recipe_id"] == "GENERIC" and len(b["resolves"]) == 1

    def test_generic_findings_never_merge(self):
        a = _item(_f({}), _asset("10.0.0.1", "a"))
        b = _item(_f({}), _asset("10.0.0.2", "b"))
        a[0].title = b[0].title = "Interesting behaviour observed"
        assert len(B.build_bundles([a, b], now=NOW)) == 2

    def test_cve_upgrades_bundle_by_product_with_highest_fixed(self):
        a = _item(_f({"product": "openssh", "fixed_version": "8.8p1"}, cve_ids=["CVE-2021-41617"]),
                  _asset("10.0.0.1", "a", "Ubuntu 20.04"))
        b = _item(_f({"product": "openssh", "fixed_version": "9.8p1"}, cve_ids=["CVE-2024-6387"]),
                  _asset("10.0.0.1", "a", "Ubuntu 20.04"))
        [bundle] = B.build_bundles([a, b], now=NOW)
        assert bundle["target_state"] == "openssh ≥ 9.8p1"
        assert len(bundle["hosts"]) == 1 and len(bundle["hosts"][0]["finding_ids"]) == 2

    def test_order_by_due_then_size(self):
        fleet = [_smb("10.0.0.1", "a", due_days=5), _smb("10.0.0.2", "b", due_days=5)]
        tls = _item(_f({"rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "port": 443}),
                    _asset("10.0.0.5", "w"), _svc(443, "nginx"), due_days=1)
        out = B.build_bundles(fleet + [tls], now=NOW)
        assert out[0]["recipe_id"] == "POSTURE-TLS-DEPRECATED-VERSION"

    def test_urgency_is_max(self):
        hot = _item(_f({"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445, "kev": True,
                        "internet_facing": True}, severity="critical"),
                    _asset("10.0.0.1", "a"), _svc(445, "SMB"))
        cold = _smb("10.0.0.2", "b")
        [b] = B.build_bundles([hot, cold], now=NOW)
        assert b["urgency"] == "act"


class TestByHost:
    def test_pivot(self):
        items = [_smb("10.0.0.1", "a", due_days=4),
                 _item(_f({"rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "port": 443}),
                       _asset("10.0.0.1", "a"), _svc(443, "nginx"), due_days=2)]
        hosts = B.by_host(B.build_bundles(items, now=NOW))
        assert len(hosts) == 1
        assert [x["recipe_id"] for x in hosts[0]["bundles"]] == [
            "POSTURE-TLS-DEPRECATED-VERSION", "POSTURE-SMB-V1-ENABLED"]


def test_bundle_carries_max_open_severity_and_kev():
    hot = _item(_f({"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445, "kev": True}, severity="medium"),
                _asset("10.0.0.1", "a"), _svc(445, "SMB"))
    cold = _smb("10.0.0.2", "b", severity="high")
    [b] = B.build_bundles([hot, cold], now=NOW)
    assert b["max_severity"] == "high" and b["kev"] is True
