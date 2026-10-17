"""The audit trail's tamper evidence, against a real Postgres.

The append-only rule and the hash chain live in database triggers (migration 0067), so
only a real database can prove them. Skipped (not failed) when DATABASE_URL is not a
reachable Postgres that has been migrated to 0067 or later.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import get_settings
from app.services import audit_integrity as integrity

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def session():
    url = get_settings().database_url
    if not url.startswith("postgresql"):
        pytest.skip("audit triggers are Postgres-only")
    engine = create_async_engine(url)
    try:
        async with engine.connect() as probe:
            has = (await probe.execute(text(
                "SELECT count(*) FROM information_schema.columns "
                "WHERE table_name = 'audit_logs' AND column_name = 'row_hash'"))).scalar_one()
    except Exception as exc:  # noqa: BLE001 — no reachable database in this run
        await engine.dispose()
        pytest.skip(f"no reachable Postgres: {exc}")
    if not has:
        await engine.dispose()
        pytest.skip("database is not migrated to 0067")
    async with AsyncSession(engine) as s:
        yield s
        await s.rollback()
    await engine.dispose()


_INSERT = text("""
    INSERT INTO audit_logs (actor_id, action, "timestamp", tenant_id, outcome, detail)
    VALUES (:actor, :action, :ts, :tenant, :outcome, CAST(:detail AS jsonb))
    RETURNING id
""")


async def _write(s, tenant, action="finding.updated", *, ts=None, outcome="success", detail="{}"):
    return (await s.execute(_INSERT, {
        "actor": "u1", "action": action, "ts": ts or datetime.now(timezone.utc),
        "tenant": tenant, "outcome": outcome, "detail": detail})).scalar_one()


async def _purge(s, tenant):
    await s.execute(text("SELECT set_config('vedha.audit_purge', 'on', true)"))
    await s.execute(text("DELETE FROM audit_logs WHERE tenant_id = :t"), {"t": tenant})


async def test_each_entry_is_chained_to_the_one_before(session):
    tenant = uuid.uuid4()
    for i in range(3):
        await _write(session, tenant, f"a.{i}")
    rows = (await session.execute(text(
        "SELECT chain_pos, prev_hash, row_hash FROM audit_logs WHERE tenant_id = :t ORDER BY chain_pos"),
        {"t": tenant})).all()
    assert [r[0] for r in rows] == [1, 2, 3]
    assert rows[0][1] is None and rows[1][1] == rows[0][2] and rows[2][1] == rows[1][2]
    result = await integrity.verify_chain(session, tenant)
    assert result.ok and result.checked == 3
    await _purge(session, tenant)


async def test_two_tenants_have_separate_chains(session):
    a, b = uuid.uuid4(), uuid.uuid4()
    await _write(session, a)
    await _write(session, b)
    await _write(session, a)
    assert (await integrity.verify_chain(session, a)).checked == 2
    assert (await integrity.verify_chain(session, b)).checked == 1
    await _purge(session, a)
    await _purge(session, b)


async def test_an_entry_cannot_be_changed_deleted_or_truncated(session):
    tenant = uuid.uuid4()
    entry = await _write(session, tenant)
    for statement in (
        "UPDATE audit_logs SET action = 'tampered' WHERE id = :i",
        "DELETE FROM audit_logs WHERE id = :i",
    ):
        with pytest.raises(Exception, match="append-only"):
            async with session.begin_nested():
                await session.execute(text(statement), {"i": entry})
    with pytest.raises(Exception, match="append-only"):
        async with session.begin_nested():
            await session.execute(text("TRUNCATE audit_logs"))
    await _purge(session, tenant)


async def test_tampering_with_the_database_directly_is_detected(session):
    tenant = uuid.uuid4()
    first = await _write(session, tenant, "a.1")
    await _write(session, tenant, "a.2")
    await _write(session, tenant, "a.3")
    # A superuser can switch the trigger off; the chain still shows what they did.
    await session.execute(text("ALTER TABLE audit_logs DISABLE TRIGGER audit_logs_immutable_bud"))
    try:
        await session.execute(text("UPDATE audit_logs SET action = 'tampered' WHERE id = :i"), {"i": first})
    finally:
        await session.execute(text("ALTER TABLE audit_logs ENABLE TRIGGER audit_logs_immutable_bud"))
    result = await integrity.verify_chain(session, tenant)
    assert not result.ok and result.first_break_pos == 1 and result.reason == "an entry was changed"
    await session.execute(text("ALTER TABLE audit_logs DISABLE TRIGGER audit_logs_immutable_bud"))
    await session.execute(text("DELETE FROM audit_logs WHERE tenant_id = :t"), {"t": tenant})
    await session.execute(text("ALTER TABLE audit_logs ENABLE TRIGGER audit_logs_immutable_bud"))


async def test_a_removed_entry_is_detected(session):
    tenant = uuid.uuid4()
    await _write(session, tenant, "a.1")
    middle = await _write(session, tenant, "a.2")
    await _write(session, tenant, "a.3")
    await session.execute(text("ALTER TABLE audit_logs DISABLE TRIGGER audit_logs_immutable_bud"))
    await session.execute(text("DELETE FROM audit_logs WHERE id = :i"), {"i": middle})
    await session.execute(text("ALTER TABLE audit_logs ENABLE TRIGGER audit_logs_immutable_bud"))
    result = await integrity.verify_chain(session, tenant)
    assert not result.ok and result.reason == "an entry is missing" and result.first_break_pos == 3
    await _purge(session, tenant)


async def test_retention_removes_only_expired_entries_and_the_rest_still_verifies(session):
    tenant = uuid.uuid4()
    now = datetime.now(timezone.utc)
    await _write(session, tenant, "old.1", ts=now - timedelta(days=400))
    await _write(session, tenant, "old.2", ts=now - timedelta(days=380))
    await _write(session, tenant, "recent.1", ts=now - timedelta(days=10))
    await _write(session, tenant, "recent.2", ts=now)
    removed = await integrity.purge_expired(session, tenant, 365)
    assert removed == 2
    result = await integrity.verify_chain(session, tenant)
    assert result.ok and result.checked == 2
    # New entries keep chaining after a purge.
    await _write(session, tenant, "after.purge")
    assert (await integrity.verify_chain(session, tenant)).ok
    await _purge(session, tenant)


async def test_retention_never_goes_under_the_legal_floor(session):
    tenant = uuid.uuid4()
    now = datetime.now(timezone.utc)
    await _write(session, tenant, "year.old", ts=now - timedelta(days=200))
    await _write(session, tenant, "ninety.days.old", ts=now - timedelta(days=90))
    # Asking for 7 days still keeps everything inside the 180-day floor.
    assert await integrity.purge_expired(session, tenant, 7) == 1
    left = (await session.execute(text("SELECT action FROM audit_logs WHERE tenant_id = :t"), {"t": tenant})).scalars().all()
    assert "ninety.days.old" in left and "year.old" not in left
    await _purge(session, tenant)


async def test_the_platform_chain_for_entries_with_no_tenant_is_verifiable_and_purgeable(session):
    now = datetime.now(timezone.utc)
    await _write(session, None, "auth.login.failure", ts=now - timedelta(days=500), outcome="failure")
    await _write(session, None, "auth.login.failure", ts=now, outcome="failure")
    assert (await integrity.verify_chain(session, None)).ok
    before = (await integrity.verify_chain(session, None)).checked
    assert await integrity.purge_expired(session, None, 365) >= 1
    after = await integrity.verify_chain(session, None)
    assert after.ok and after.checked < before


# ── the readers, against real data ───────────────────────────────────────────

async def _world(s):
    """Two tenants; tenant A has an engagement, an admin, an operator and a customer user."""
    a, b = uuid.uuid4(), uuid.uuid4()
    eng, other_eng = uuid.uuid4(), uuid.uuid4()
    admin, op, client, other_client = (uuid.uuid4() for _ in range(4))
    for t in (a, b):
        await s.execute(text("INSERT INTO tenants (id, name) VALUES (:i, 'T')"), {"i": t})
    for e, t in ((eng, a), (other_eng, a)):
        await s.execute(text("INSERT INTO engagements (id, tenant_id, name) VALUES (:i, :t, 'Perimeter review')"),
                        {"i": e, "t": t})
    for uid, role, eng_id, email in (
        (admin, "admin", None, "admin@a.test"), (op, "analyst", None, "ana@a.test"),
        (client, "client", eng, "ciso@c.test"), (other_client, "client", other_eng, "other@c.test"),
    ):
        await s.execute(text(
            "INSERT INTO users (id, tenant_id, email, hashed_password, role, client_engagement_id) "
            "VALUES (:i, :t, :e, 'x', CAST(:r AS userrole), :c)"),
            {"i": uid, "t": a, "e": email, "r": role, "c": eng_id})
    return SimpleNamespace(a=a, b=b, eng=eng, other_eng=other_eng, admin=admin, op=op,
                           client=client, other_client=other_client)


from types import SimpleNamespace  # noqa: E402

_FULL = text("""
    INSERT INTO audit_logs (actor_id, actor_type, actor_label, action, "timestamp", tenant_id,
                            engagement_id, outcome, ip_address, detail)
    VALUES (:actor, :atype, :label, :action, :ts, :tenant, :eng, :outcome, :ip, CAST(:detail AS jsonb))
""")


async def _log(s, w, *, actor, atype, action, eng=None, tenant=None, outcome="success", ip="203.0.113.7",
               label=None, ts=None, detail='{"secret_internal": "x"}'):
    await s.execute(_FULL, {"actor": str(actor), "atype": atype, "label": label, "action": action,
                            "ts": ts or datetime.now(timezone.utc), "tenant": tenant or w.a, "eng": eng,
                            "outcome": outcome, "ip": ip, "detail": detail})


async def test_the_operator_log_is_tenant_scoped_filterable_and_paged(session):
    from app.routers import audit_logs as router
    from app.schemas.auth import CurrentUser
    w = await _world(session)
    now = datetime.now(timezone.utc)
    for i in range(5):
        await _log(session, w, actor=w.admin, atype="user", action="finding.updated", ts=now - timedelta(minutes=10 - i))
    await _log(session, w, actor="anonymous", atype="anonymous", action="auth.login.failure",
               outcome="failure", label="ghost@x.io", tenant=w.a, ts=now)
    await _log(session, w, actor=w.admin, atype="user", action="finding.updated", tenant=w.b)   # someone else's
    user = CurrentUser(user_id=w.admin, tenant_id=w.a, role="admin")

    page = await router.list_entries(session, user, router.audit_query.AuditFilters(), None, 4)
    assert len(page.items) == 4 and page.next_cursor
    assert page.items[0].action == "auth.login.failure" and page.items[0].actor.label == "ghost@x.io"
    nxt = await router.list_entries(session, user, router.audit_query.AuditFilters(), page.next_cursor, 4)
    assert len(nxt.items) == 2 and nxt.next_cursor is None
    ids = [e.id for e in page.items + nxt.items]
    assert len(set(ids)) == 6                                        # no overlap, none missing, none of tenant B
    assert all(e.category_label for e in page.items)

    failures = await router.list_entries(
        session, user, router.audit_query.AuditFilters(outcome="failure"), None, 50)
    assert [e.action for e in failures.items] == ["auth.login.failure"]
    by_category = await router.list_entries(
        session, user, router.audit_query.AuditFilters(category="authentication"), None, 50)
    assert {e.action for e in by_category.items} == {"auth.login.failure"}
    by_actor = await router.list_entries(
        session, user, router.audit_query.AuditFilters(actor="GHOST"), None, 50)
    assert len(by_actor.items) == 1
    # An actor with no frozen label is named from the users table.
    named = await router.list_entries(
        session, user, router.audit_query.AuditFilters(actions=["finding.updated"]), None, 1)
    assert named.items[0].actor.label == "admin@a.test"

    facets = await router.entry_facets(session, user, router.audit_query.AuditFilters())
    counts = {c["key"]: c["count"] for c in facets["categories"]}
    assert counts["findings"] == 5 and counts["authentication"] == 1
    assert {o["key"]: o["count"] for o in facets["outcomes"]} == {"success": 5, "failure": 1, "denied": 0}


async def test_a_customer_sees_only_their_engagement_without_operator_identity_or_detail(session):
    from app.routers import portal
    from app.schemas.auth import CurrentUser
    w = await _world(session)
    now = datetime.now(timezone.utc)
    await _log(session, w, actor=w.op, atype="user", action="finding.updated", eng=w.eng, ip="198.51.100.9", ts=now)
    await _log(session, w, actor=w.client, atype="client", action="scan_request.created", eng=w.eng, ts=now)
    await _log(session, w, actor=w.client, atype="client", action="auth.login.success", ts=now, label="ciso@c.test")
    await _log(session, w, actor=w.other_client, atype="client", action="auth.login.success", ts=now)   # another customer
    await _log(session, w, actor=w.op, atype="user", action="finding.updated", eng=w.other_eng, ts=now)  # another engagement
    await _log(session, w, actor=w.op, atype="user", action="integration.updated", eng=w.eng, ts=now)    # operator-only action
    me = CurrentUser(user_id=w.client, tenant_id=w.a, role="client", client_engagement_id=w.eng)

    page = await portal.portal_audit_log(me, session, None, None, None, None, None, 50)
    assert sorted(i.label for i in page.items) == ["Finding changed", "Scan requested", "Signed in"]
    by_label = {i.label: i for i in page.items}
    assert by_label["Finding changed"].who == "Vedha analyst" and by_label["Finding changed"].ip_address is None
    assert by_label["Scan requested"].who == "You" and by_label["Scan requested"].ip_address == "203.0.113.7"
    dumped = page.model_dump_json()
    assert "secret_internal" not in dumped and "198.51.100.9" not in dumped and "ana@a.test" not in dumped


async def test_export_is_complete_safe_for_spreadsheets_and_itself_recorded(session):
    import csv, io, json
    from app.routers import audit_logs as router
    from app.schemas.auth import CurrentUser
    w = await _world(session)
    await _log(session, w, actor="anonymous", atype="anonymous", action="auth.login.failure",
               outcome="failure", label="=cmd|' /C calc'!A0")
    for i in range(3):
        await _log(session, w, actor=w.admin, atype="user", action="finding.updated")
    user = CurrentUser(user_id=w.admin, tenant_id=w.a, role="admin")
    filters = router.audit_query.AuditFilters()

    resp = await router.export_entries(session, user, filters, "csv")
    assert resp.headers["content-disposition"].startswith('attachment; filename="audit-log-')
    rows = list(csv.reader(io.StringIO(resp.body.decode("utf-8-sig"))))
    assert rows[0][:4] == ["timestamp_utc", "entry_id", "action", "description"] and len(rows) == 5
    actor_col = rows[0].index("actor")
    assert any(r[actor_col].startswith("'=") for r in rows[1:])          # a formula never survives as one

    resp = await router.export_entries(session, user, router.audit_query.AuditFilters(outcome="failure"), "json")
    body = json.loads(resp.body)
    assert body["count"] == 1 and body["integrity"]["ok"] is True and body["truncated"] is False
    assert body["entries"][0]["actor"]["label"].startswith("=")          # JSON keeps the value; CSV is what is guarded

    # Both exports are in the trail, who took them and with which filters.
    trail = await router.list_entries(session, user, router.audit_query.AuditFilters(actions=["audit.exported"]), None, 10)
    assert len(trail.items) == 2
    assert {e.detail["format"] for e in trail.items} == {"csv", "json"}
    assert all(e.actor.id == str(w.admin) for e in trail.items)
    assert any(e.detail["filters"].get("outcome") == "failure" for e in trail.items)


async def test_the_integrity_endpoint_reports_the_chain_and_the_retention_in_force(session):
    from app.routers import audit_logs as router
    from app.schemas.auth import CurrentUser
    w = await _world(session)
    await _log(session, w, actor=w.admin, atype="user", action="finding.updated")
    await _log(session, w, actor=w.admin, atype="user", action="finding.updated")
    user = CurrentUser(user_id=w.admin, tenant_id=w.a, role="admin")
    out = await router.integrity(session, user)
    assert out["ok"] and out["entries_checked"] == 2 and out["first_problem"] is None
    assert out["retention_days"] == 365 and out["minimum_retention_days"] == 180
