"""
test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ "Multi-vantage
scanning" + "Reachability validation") in main_scripts/vantage_matrix.py.
"""
from __future__ import annotations

from main_scripts import vantage_matrix as vm
from main_scripts.vantage_matrix import reconcile_vantages
from main_scripts.scanner_base import ScanResult


def _r(port, status, proto="tcp"):
    return ScanResult("port_scan", "192.168.1.68", port=port, proto=proto, status=status)


class TestReconcileVantages:
    def test_external_exposure_is_flagged(self):
        obs = {
            "internet": [_r(443, "open")],
            "corp_lan": [_r(443, "open")],
        }
        out = reconcile_vantages(obs)
        assert out["ports"]["tcp/443"]["exposure"] == vm.EXTERNAL
        assert out["externally_exposed"] == [443]

    def test_internal_only_not_called_external(self):
        # The headline case: Internet ❌, Corp LAN ✅, Guest Wi-Fi ❌
        obs = {
            "internet": [_r(445, "filtered")],
            "corp_lan": [_r(445, "open")],
            "guest_wifi": [_r(445, "filtered")],
        }
        out = reconcile_vantages(obs)
        assert out["ports"]["tcp/445"]["exposure"] == vm.INTERNAL_ONLY
        assert out["externally_exposed"] == []
        assert out["internal_only"] == [445]
        assert out["ports"]["tcp/445"]["open_from"] == ["corp_lan"]

    def test_not_exposed_everywhere(self):
        obs = {"internet": [_r(3389, "filtered")], "corp_lan": [_r(3389, "closed")]}
        out = reconcile_vantages(obs)
        assert out["ports"]["tcp/3389"]["exposure"] == vm.NOT_EXPOSED

    def test_ambiguous_when_only_open_filtered(self):
        obs = {"corp_lan": [_r(161, "open|filtered", proto="udp")]}
        out = reconcile_vantages(obs)
        assert out["ports"]["udp/161"]["exposure"] == vm.AMBIGUOUS

    def test_vantages_are_not_collapsed(self):
        obs = {"internet": [_r(22, "open")], "corp_lan": [_r(22, "closed")]}
        out = reconcile_vantages(obs)
        by_v = out["ports"]["tcp/22"]["by_vantage"]
        assert by_v == {"internet": "open", "corp_lan": "closed"}   # both preserved
        assert out["ports"]["tcp/22"]["exposure"] == vm.EXTERNAL

    def test_explicit_external_vantage_by_name_override(self):
        # A vantage whose name doesn't hint "external" can be declared so.
        obs = {"dmz_probe": [_r(80, "open")]}
        out = reconcile_vantages(obs, external_vantages={"dmz_probe"})
        assert out["ports"]["tcp/80"]["exposure"] == vm.EXTERNAL
        assert out["externally_exposed"] == [80]

    def test_auto_detects_external_by_name(self):
        obs = {"corp_lan": [_r(8080, "open")]}
        out = reconcile_vantages(obs)
        assert out["external_vantages"] == []          # corp_lan is internal
        assert out["ports"]["tcp/8080"]["exposure"] == vm.INTERNAL_ONLY
