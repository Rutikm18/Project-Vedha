"""The advisor's output is untrusted: only real objects of the engagement survive."""
from __future__ import annotations

import asyncio
import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.ai import agent as ag
from app.ai.agent import AgentDecisionEngine

EID = uuid.uuid4()
F1, F2, A1, P1 = (uuid.uuid4() for _ in range(4))
OTHER = uuid.uuid4()          # exists, but in someone else's engagement


class FakeDB:
    """execute() answers the three membership queries from per-model id sets."""

    def __init__(self, findings=(), assets=(), paths=()):
        self.members = {"findings": set(findings), "assets": set(assets), "attack_paths": set(paths)}
        self.added: list = []
        self.queries = 0

    async def execute(self, stmt):
        self.queries += 1
        table = stmt.get_final_froms()[0].name
        out = MagicMock()
        # The query asks "which of these ids belong to the engagement": answer from members.
        ids = list(stmt.compile().params.values())
        flat = [i for v in ids for i in (v if isinstance(v, (list, tuple, set)) else [v])]
        out.scalars = MagicMock(return_value=MagicMock(all=MagicMock(
            return_value=[i for i in flat if i in self.members.get(table, set())])))
        return out

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        pass


def _engine(db):
    e = AgentDecisionEngine(db, client=MagicMock())
    return e


def run(coro):
    return asyncio.run(coro)


def _rec(**kw):
    base = {"category": "triage", "title": "Check it", "target_type": "finding", "target_id": str(F1)}
    base.update(kw)
    return base


def persist(recs, **members):
    db = FakeDB(**members)
    n = run(_engine(db)._persist(EID, uuid.uuid4(), {"recommendations": recs}))
    return n, db


def test_a_real_target_of_the_engagement_is_kept():
    n, db = persist([_rec()], findings={F1})
    assert n == 1 and db.added[0].target_id == F1 and db.added[0].target_type == "finding"
    assert db.added[0].status == "pending"


def test_a_target_from_another_engagement_or_tenant_is_dropped():
    n, db = persist([_rec(target_id=str(OTHER))], findings={F1})
    assert n == 0 and db.added == []


def test_an_unknown_target_type_is_dropped():
    n, _ = persist([_rec(target_type="user")], findings={F1})
    assert n == 0


def test_a_target_type_that_does_not_match_the_id_is_dropped():
    # F1 is a finding, not an asset
    n, _ = persist([_rec(target_type="asset", target_id=str(F1))], findings={F1}, assets={A1})
    assert n == 0


def test_a_malformed_target_id_is_dropped_not_silently_cleared():
    n, _ = persist([_rec(target_id="not-a-uuid")], findings={F1})
    assert n == 0


def test_the_engagement_itself_is_a_valid_target_only_for_this_engagement():
    n, _ = persist([_rec(target_type="engagement", target_id=str(EID), category="next_action", action="run_discovery_scan")])
    assert n == 1
    n, _ = persist([_rec(target_type="engagement", target_id=str(OTHER), category="next_action", action="run_discovery_scan")])
    assert n == 0


def test_a_recommendation_with_no_target_is_allowed_when_it_does_not_need_one():
    n, db = persist([{"category": "next_action", "title": "Discover more", "action": "run_discovery_scan"}])
    assert n == 1 and db.added[0].target_id is None


def test_targeted_actions_need_a_finding_or_asset():
    # no target at all
    n, _ = persist([{"category": "next_action", "title": "Scan it", "action": "run_targeted_scan"}])
    assert n == 0
    # an attack path is not a scan target
    n, _ = persist([{"category": "next_action", "title": "Scan it", "action": "run_targeted_scan",
                     "target_type": "attack_path", "target_id": str(P1)}], paths={P1})
    assert n == 0
    # a real asset is
    n, _ = persist([{"category": "next_action", "title": "Scan it", "action": "run_targeted_scan",
                     "target_type": "asset", "target_id": str(A1)}], assets={A1})
    assert n == 1


def test_actions_off_the_allowlist_are_still_dropped():
    n, _ = persist([{"category": "next_action", "title": "x", "action": "delete_everything"}])
    assert n == 0


def test_one_membership_query_per_type_however_many_recommendations():
    db = FakeDB(findings={F1, F2})
    recs = [_rec(target_id=str(F1)), _rec(target_id=str(F2)), _rec(target_id=str(F1), title="again")]
    n = run(_engine(db)._persist(EID, uuid.uuid4(), {"recommendations": recs}))
    assert n == 3 and db.queries == 1


def test_a_flood_of_recommendations_is_capped():
    recs = [{"category": "triage", "title": f"t{i}"} for i in range(ag.MAX_RECOMMENDATIONS_PER_RUN + 25)]
    n, _ = persist(recs)
    assert n == ag.MAX_RECOMMENDATIONS_PER_RUN


def test_text_is_single_line_control_free_and_bounded():
    n, db = persist([{"category": "triage", "title": "Line1\nLine2\x00\x1b[31m" + "x" * 900,
                      "rationale": "a\r\nb" + "y" * 9000, "priority": "high\nINJECT" + "z" * 50}])
    rec = db.added[0]
    assert n == 1
    assert "\n" not in rec.title and "\x00" not in rec.title and len(rec.title) <= 500
    assert "\n" not in rec.rationale and len(rec.rationale) <= 4000
    assert "\n" not in rec.priority and len(rec.priority) <= 16


def test_evidence_is_capped_but_small_payloads_are_kept_whole():
    n, db = persist([{"category": "triage", "title": "ok", "extra": {"k": 1}}])
    assert db.added[0].evidence["extra"] == {"k": 1}
    n, db = persist([{"category": "triage", "title": "big", "blob": {"x": "q" * 20000}, "note": "keep"}])
    assert db.added[0].evidence == {"category": "triage", "title": "big", "blob": None, "note": "keep"}


def test_confidence_is_clamped_and_never_aborts_the_flush():
    ok = ag._maybe_decimal
    assert ok(87.46) == Decimal("87.5") and ok("55") == Decimal("55.0")
    assert ok(1e9) == Decimal("100.0") and ok(-5) == Decimal("0.0")
    for bad in (float("inf"), float("nan"), "abc", None, True):
        assert ok(bad) is None


def test_a_non_list_submission_stores_nothing():
    db = FakeDB()
    assert run(_engine(db)._persist(EID, uuid.uuid4(), {"recommendations": "drop table"})) == 0
