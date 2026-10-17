"""Port 9100 relabel: an open finding from the old 'admin UI' label takes the
printer title; the printer class has its own fix plan."""
from __future__ import annotations

from types import SimpleNamespace

from app.detection.engine_bridge import _is_catalog_relabel
from app.remediation import plan as P
from app.remediation.context import build_context
from app.remediation.recipes import RECIPES


def test_old_admin_ui_9100_finding_is_a_relabel():
    prev = {"rule_id": "POSTURE-EXPOSED-ADMIN_UI", "port": 9100}
    assert _is_catalog_relabel(prev, {"rule_id": "POSTURE-EXPOSED-PRINTER", "port": 9100})


def test_other_ports_and_other_producers_are_not_relabels():
    assert not _is_catalog_relabel({"rule_id": "POSTURE-EXPOSED-ADMIN_UI", "port": 8080},
                                   {"rule_id": "POSTURE-EXPOSED-PRINTER", "port": 8080})
    # A different producer of the same condition stays a merged signal.
    assert not _is_catalog_relabel({"rule_id": "PROBE-PRINTER-OPEN", "port": 9100},
                                   {"rule_id": "POSTURE-EXPOSED-PRINTER", "port": 9100})
    assert not _is_catalog_relabel({"rule_id": "POSTURE-EXPOSED-ADMIN_UI", "port": "x"},
                                   {"rule_id": "POSTURE-EXPOSED-PRINTER", "port": "x"})
    assert not _is_catalog_relabel({"rule_id": "POSTURE-EXPOSED-PRINTER", "port": 9100},
                                   {"rule_id": "POSTURE-EXPOSED-PRINTER", "port": 9100})


def test_printer_finding_gets_the_print_port_plan():
    f = SimpleNamespace(id="f", title="Printer raw-print port open on 9100", description="",
                        remediation="", cve_ids=[], severity=SimpleNamespace(value="low"),
                        epss_score=None, exploit_validated=False,
                        evidence={"rule_id": "POSTURE-EXPOSED-PRINTER", "port": 9100,
                                  "category": "printer"})
    plan = P.build_plan(f, build_context(f, None, None))
    assert plan["recipe_id"] == "POSTURE-EXPOSED-PRINTER" in RECIPES
    assert any("PJL" in s["title"] or "PJL" in s["description"] for s in plan["steps"])
