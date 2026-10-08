"""
Ground-truth validation of attack-path generation (P5c, FM-31).

Runs the analyzer over hand-written networks whose true paths are known
(tests/fixtures/attack_paths) and fails when the result is wrong in a way unit tests
cannot see: a missing path, a step that cannot happen, a path that crosses a hop the
attacker has no way to take. The harness itself is tested too, with a deliberately
wrong fixture, so "all fixtures pass" cannot silently mean "the checker checks nothing".
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from app.graph import validation as v

FIXTURES = Path(__file__).parent / "fixtures" / "attack_paths"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_every_fixture_passes():
    result = v.evaluate_directory(FIXTURES)
    failing = {r["name"]: r["failures"] for r in result["reports"] if not r["passed"]}
    assert result["fixtures"] >= 9
    assert not failing, failing
    assert result["mean_recall"] == 1.0
    assert result["mean_cascade_validity"] == 1.0


def test_fixtures_each_declare_what_they_check():
    """A fixture with no ground truth would pass vacuously."""
    for path in sorted(FIXTURES.glob("*.json")):
        fx = json.loads(path.read_text(encoding="utf-8"))
        truth = fx.get("truth") or {}
        assert truth, path.name
        assert fx.get("targets"), path.name
        assert any(k in truth for k in (
            "expected_paths", "unreachable_targets", "expected_freshness", "min_fix_set",
            "independent_routes", "top_choke", "forbidden_hops")), path.name


# ── cascade validity ─────────────────────────────────────────────────────────

VALID = {("a", "b"), ("b", "c"), ("c", "d")}


def test_cascade_validity_full_path():
    assert v.cascade_validity(["a", "b", "c", "d"], VALID) == 1.0


def test_cascade_validity_stops_at_the_first_bad_hop():
    # a>b valid, b>x invalid, x>d would "look" valid in isolation — it earns nothing
    assert v.cascade_validity(["a", "b", "x", "d"], VALID | {("x", "d")}) == pytest.approx(1 / 3)


def test_cascade_validity_first_hop_wrong_is_zero():
    assert v.cascade_validity(["a", "z", "c", "d"], VALID | {("c", "d")}) == 0.0


def test_cascade_validity_single_node_path_is_vacuously_valid():
    assert v.cascade_validity(["a"], VALID) == 1.0


# ── the harness detects wrong answers ────────────────────────────────────────

def test_harness_flags_a_path_that_should_not_exist():
    fx = _fixture("02_segmented_gateway.json")
    bad = copy.deepcopy(fx)
    bad["truth"]["unreachable_targets"] = list(bad["targets"])     # claim the target cannot be reached
    report = v.run_fixture(bad)
    assert not report["passed"]
    assert any("must be unreachable" in f for f in report["failures"])


def test_harness_flags_a_missing_expected_path():
    fx = _fixture("01_flat_internal.json")
    bad = copy.deepcopy(fx)
    bad["truth"]["expected_paths"] = [["entry", "mid", "mid2", "jewel"]]
    report = v.run_fixture(bad)
    assert not report["passed"]
    assert report["metrics"]["recall"] == 0.0
    assert any("missing expected path" in f for f in report["failures"])


def test_harness_flags_a_forbidden_hop():
    fx = _fixture("01_flat_internal.json")
    bad = copy.deepcopy(fx)
    bad["truth"]["forbidden_hops"] = [["entry", "jewel"]]
    report = v.run_fixture(bad)
    assert not report["passed"]
    assert any("forbidden hop appeared" in f for f in report["failures"])


def test_harness_flags_an_invalid_step_and_reports_it_as_cascade_failure():
    fx = _fixture("01_flat_internal.json")
    bad = copy.deepcopy(fx)
    bad["truth"]["valid_hops"] = [["entry", "mid"]]                # entry>jewel is not declared valid
    report = v.run_fixture(bad)
    assert not report["passed"]
    assert report["metrics"]["cascade_validity"] < 1.0
    assert report["metrics"]["fabricated_paths"] >= 1


def test_harness_flags_wrong_freshness():
    fx = _fixture("07_stale_target.json")
    key, want = next(iter(fx["truth"]["expected_freshness"].items()))
    bad = copy.deepcopy(fx)
    bad["truth"]["expected_freshness"] = {key: "fresh" if want != "fresh" else "stale"}
    report = v.run_fixture(bad)
    assert not report["passed"]
    assert any("expected" in f for f in report["failures"])


def test_harness_flags_a_wrong_minimum_fix_set_and_wrong_route_count():
    fx = _fixture("09_single_bottleneck_many_entries.json")
    bad = copy.deepcopy(fx)
    bad["truth"]["min_fix_set"] = ["not-a-real-host"]
    bad["truth"]["independent_routes"] = {t: 99 for t in bad["targets"]}
    bad["truth"]["top_choke"] = "not-a-real-host"
    report = v.run_fixture(bad)
    assert not report["passed"]
    text = " ".join(report["failures"])
    assert "minimum fix set" in text and "independent routes" in text and "top choke point" in text


def test_missing_path_in_freshness_check_is_a_failure_not_a_pass():
    fx = _fixture("07_stale_target.json")
    bad = copy.deepcopy(fx)
    bad["truth"]["expected_freshness"] = {"no>such>path": "fresh"}
    report = v.run_fixture(bad)
    assert not report["passed"]
    assert any("no path no>such>path" in f for f in report["failures"])


# ── the CLI ──────────────────────────────────────────────────────────────────

def test_cli_exit_code_reflects_the_result(tmp_path, capsys):
    assert v.main([str(FIXTURES)]) == 0
    assert "fixtures pass" in capsys.readouterr().out

    broken = _fixture("01_flat_internal.json")
    broken["truth"]["expected_paths"] = [["entry", "nowhere"]]
    (tmp_path / "broken.json").write_text(json.dumps(broken), encoding="utf-8")
    assert v.main([str(tmp_path)]) == 1
    assert "FAIL" in capsys.readouterr().out


def test_cli_rejects_wrong_usage(capsys):
    assert v.main([]) == 2
    assert v.main(["a", "b"]) == 2


def test_an_empty_directory_does_not_report_success(tmp_path):
    result = v.evaluate_directory(tmp_path)
    assert result["fixtures"] == 0 and result["passed"] == 0


def test_cli_treats_no_fixtures_as_failure(tmp_path, capsys):
    assert v.main([str(tmp_path)]) == 1
    assert "no fixtures" in capsys.readouterr().err
