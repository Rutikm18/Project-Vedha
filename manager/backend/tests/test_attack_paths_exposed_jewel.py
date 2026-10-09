"""
A crown jewel that is itself an exploitable, internet-exposed host.

It is its own entry point: no route leads to it, it scores the maximum, and the
minimum fix set (which protects targets, and so leaves them out) says nothing about it.
The analyzer now says so per jewel, so no reader has to guess from a likelihood of 1.0.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from app.graph.analyzer import PathAnalyzer
from app.graph.validation import build_graph

FIXTURES = sorted((Path(__file__).parent / "fixtures" / "attack_paths").glob("*.json"))


def _choke(fx: dict) -> dict:
    return PathAnalyzer(build_graph(fx)).choke_analysis(list(fx["targets"]))


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_no_validation_fixture_has_an_exposed_crown_jewel(path):
    for target in _choke(json.loads(path.read_text()))["targets"]:
        assert target["exposed_directly"] is False


def _with_exposed_jewel(only: bool) -> dict:
    fx = json.loads((FIXTURES[-1]).read_text())                       # 09: eight exposed hosts, one gateway
    assert fx["name"].startswith("eight exposed hosts")
    fx = copy.deepcopy(fx)
    entries = [a for a in fx["assets"] if a.get("environment") == "dmz"]
    jewel = next(a for a in fx["assets"] if a["id"] == "jewel")
    jewel["environment"] = "dmz"
    if only:
        for a in entries:
            a.pop("environment")
    fx["exploitable"] = sorted(set(fx["exploitable"]) | {"jewel"})
    return fx


def test_an_exposed_jewel_is_flagged_and_scores_the_maximum():
    target = _choke(_with_exposed_jewel(only=False))["targets"][0]
    assert target["exposed_directly"] is True
    assert target["best_likelihood"] == 1.0 and target["risk"] == 100.0


def test_an_exposed_jewel_stays_flagged_when_it_is_the_only_way_in():
    choke = _choke(_with_exposed_jewel(only=True))
    assert choke["targets"][0]["exposed_directly"] is True
    assert choke["min_fix_set"]["size"] == 0 and choke["ranked"] == []      # nothing on the way in to fix
