"""
attack_path_fm_probe.py — reproduce the attack-path failure modes measured in
manager/docs/ATTACK_PATH_PLAN.md §9 against the REAL app/graph/analyzer.py.

Read-only diagnostic: builds small in-memory graphs, touches no DB or network.
  FM-17  scoring inversion (long chains outrank a one-step critical)
  FM-19  misconfig-only paths score 0 (posture findings carry no CVSS)
  FM-21  all_simple_paths explosion on a flat subnet mesh vs Yen k-shortest
  FM-05  pass-through pivot from a never-compromised host

After P0 the scoring and pass-through cases show the FIXED behaviour; the
all_simple_paths explosion is kept as a reference measurement (the analyzer no
longer uses it).

Run from manager/backend:  python scripts/attack_path_fm_probe.py
Pass --full to include the 11-host mesh case (~7s on a laptop-class CPU).
"""
from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.graph.analyzer import PathAnalyzer  # noqa: E402


def scoring() -> None:
    pa = PathAnalyzer(nx.MultiDiGraph())
    short = {"hops": 1, "edges": [{"cvss": 9.8, "technique": "CONNECTS_TO"}]}
    long_ = {"hops": 4, "edges": [{"cvss": 7.0, "technique": "SAME_SEGMENT"}] * 4}
    misconf = {"hops": 2, "edges": [{"cvss": 0.0, "technique": "SAME_SEGMENT"}] * 2}
    print("FM-17 score 1-hop CVSS 9.8       :", pa.score_path(short))
    print("FM-17 score 4-hop CVSS 7.0 x4    :", pa.score_path(long_))
    print("FM-19 score 2-hop misconfig-only :", pa.score_path(misconf))
    print("      product likelihood (p=cvss/10) 1-hop: 0.98   4-hop:", round(0.7 ** 4, 3))


def explosion(full: bool) -> None:
    sizes = (8, 9, 10, 11) if full else (8, 9, 10)
    for n in sizes:
        g = nx.complete_graph(n, create_using=nx.DiGraph)
        t = time.time()
        count = sum(1 for _ in nx.all_simple_paths(g, 0, n - 1, cutoff=10))
        print(f"FM-21 flat mesh n={n:>2} edges={g.number_of_edges():>3} "
              f"simple paths: {count:>9,}  ({time.time() - t:.2f}s)")
    g = nx.complete_graph(60, create_using=nx.DiGraph)
    t = time.time()
    k = list(itertools.islice(nx.shortest_simple_paths(g, 0, 59), 5))
    print(f"      Yen k-shortest k=5 on 60-node mesh: {len(k)} paths in {time.time() - t:.3f}s")


def pass_through() -> None:
    g = nx.MultiDiGraph()
    for name in ("A", "B", "C"):
        g.add_node(f"asset:{name}", type="Asset", entity_id=name, internet_exposed=(name == "A"))
    g.add_node("finding:c", type="Finding", entity_id="fc", exploitable=True, cvss=9.0)
    g.add_edge("asset:C", "finding:c", type="HAS_FINDING")
    g.add_edge("finding:c", "asset:C", type="EXPLOITS", weight=1.0)
    g.add_edge("asset:A", "asset:B", type="CONNECTS_TO", weight=1.0)
    g.add_edge("asset:B", "asset:C", type="CONNECTS_TO", weight=1.0)
    paths = PathAnalyzer(g).find_paths_to_target("C")
    if not paths:
        print("FM-05 no path A->B->C: B cannot be compromised, so the attacker cannot pivot from it (fixed in P0)")
    for p in paths:
        print("FM-05 path:", p["nodes"], "| A->B dest_compromisable:",
              p["edges"][0]["exploited"], "-> pivots FROM B without compromising it")


if __name__ == "__main__":
    scoring()
    explosion(full="--full" in sys.argv)
    pass_through()
