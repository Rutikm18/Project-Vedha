"""Reading the audit trail: filters, keyset paging and the shapes returned.

Two readers share this: the operator audit log (a tenant's whole trail, administrators
only) and the customer view (only what concerns the customer's own engagement, with
operator identities and technical detail left out).
"""
from __future__ import annotations

import base64
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy import Select, String, and_, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.engagement import Engagement
from app.models.user import User
from app.services import audit_catalog

MAX_PAGE = 200
EXPORT_CAP = 100_000


@dataclass
class AuditFilters:
    start: datetime | None = None
    end: datetime | None = None
    actor: str | None = None
    actions: list[str] = field(default_factory=list)
    category: str | None = None
    outcome: str | None = None
    resource_type: str | None = None
    resource_id: uuid.UUID | None = None
    engagement_id: uuid.UUID | None = None
    ip: str | None = None
    q: str | None = None


def apply_filters(stmt: Select, f: AuditFilters) -> Select:
    if f.start:
        stmt = stmt.where(AuditLog.timestamp >= f.start)
    if f.end:
        stmt = stmt.where(AuditLog.timestamp <= f.end)
    if f.actor:
        stmt = stmt.where(or_(AuditLog.actor_id == f.actor,
                              AuditLog.actor_label.icontains(f.actor, autoescape=True)))
    if f.actions:
        stmt = stmt.where(AuditLog.action.in_(f.actions))
    if f.category:
        stmt = stmt.where(audit_catalog.category_clause(AuditLog.action, f.category))
    if f.outcome:
        stmt = stmt.where(AuditLog.outcome == f.outcome)
    if f.resource_type:
        stmt = stmt.where(AuditLog.resource_type == f.resource_type)
    if f.resource_id:
        stmt = stmt.where(AuditLog.resource_id == f.resource_id)
    if f.engagement_id:
        stmt = stmt.where(AuditLog.engagement_id == f.engagement_id)
    if f.ip:
        stmt = stmt.where(AuditLog.ip_address == f.ip)
    if f.q:
        stmt = stmt.where(or_(
            AuditLog.action.icontains(f.q, autoescape=True),
            AuditLog.actor_label.icontains(f.q, autoescape=True),
            AuditLog.resource_type.icontains(f.q, autoescape=True),
            AuditLog.request_id == f.q,
            cast(AuditLog.detail, String).icontains(f.q, autoescape=True),
        ))
    return stmt


# ── keyset paging (newest first) ──────────────────────────────────────────────

def encode_cursor(ts: datetime, entry_id: uuid.UUID) -> str:
    raw = f"{ts.astimezone(timezone.utc).isoformat()}|{entry_id}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def decode_cursor(cursor: str) -> tuple[datetime, uuid.UUID]:
    try:
        raw = base64.urlsafe_b64decode(cursor + "=" * (-len(cursor) % 4)).decode()
        ts, entry_id = raw.split("|", 1)
        return datetime.fromisoformat(ts), uuid.UUID(entry_id)
    except Exception as exc:  # noqa: BLE001 — any malformed cursor is the caller's error
        raise ValueError("invalid cursor") from exc


def page_after(stmt: Select, cursor: str | None) -> Select:
    if cursor:
        ts, entry_id = decode_cursor(cursor)
        stmt = stmt.where(or_(AuditLog.timestamp < ts,
                              and_(AuditLog.timestamp == ts, AuditLog.id < entry_id)))
    return stmt.order_by(AuditLog.timestamp.desc(), AuditLog.id.desc())


# ── shapes ────────────────────────────────────────────────────────────────────

class AuditActor(BaseModel):
    id: str
    type: str | None = None
    label: str | None = None


class AuditEntryOut(BaseModel):
    id: uuid.UUID
    timestamp: datetime
    action: str
    label: str
    category: str
    category_label: str
    outcome: str
    actor: AuditActor
    resource_type: str | None = None
    resource_id: uuid.UUID | None = None
    engagement_id: uuid.UUID | None = None
    engagement_name: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    request_id: str | None = None
    detail: dict | None = None
    changes: dict | None = None
    chain_position: int | None = None
    entry_hash: str | None = None


class AuditPage(BaseModel):
    items: list[AuditEntryOut]
    next_cursor: str | None = None


async def _people(db: AsyncSession, rows: list[AuditLog]) -> dict[str, str]:
    """Email for actors whose entry did not freeze a label (older entries)."""
    ids: set[uuid.UUID] = set()
    for r in rows:
        if not r.actor_label:
            try:
                ids.add(uuid.UUID(r.actor_id))
            except ValueError:
                pass
    if not ids:
        return {}
    found = (await db.execute(select(User.id, User.email).where(User.id.in_(ids)))).all()
    return {str(i): e for i, e in found}


async def _engagement_names(db: AsyncSession, rows: list[AuditLog]) -> dict[uuid.UUID, str]:
    ids = {r.engagement_id for r in rows if r.engagement_id}
    if not ids:
        return {}
    found = (await db.execute(select(Engagement.id, Engagement.name).where(Engagement.id.in_(ids)))).all()
    return dict(found)


async def to_entries(db: AsyncSession, rows: list[AuditLog]) -> list[AuditEntryOut]:
    people = await _people(db, rows)
    names = await _engagement_names(db, rows)
    out: list[AuditEntryOut] = []
    for r in rows:
        info = audit_catalog.describe(r.action)
        out.append(AuditEntryOut(
            id=r.id, timestamp=r.timestamp, action=r.action, label=info.label,
            category=info.category, category_label=audit_catalog.CATEGORIES[info.category],
            outcome=r.outcome,
            actor=AuditActor(id=r.actor_id, type=r.actor_type,
                             label=r.actor_label or people.get(r.actor_id)),
            resource_type=r.resource_type, resource_id=r.resource_id,
            engagement_id=r.engagement_id, engagement_name=names.get(r.engagement_id),
            ip_address=r.ip_address, user_agent=r.user_agent, request_id=r.request_id,
            detail=r.detail, changes=r.changes, chain_position=r.chain_pos,
            entry_hash=r.row_hash.hex() if r.row_hash else None,
        ))
    return out


async def read_page(
    db: AsyncSession, base: Select, filters: AuditFilters, cursor: str | None, limit: int,
) -> AuditPage:
    limit = max(1, min(limit, MAX_PAGE))
    stmt = page_after(apply_filters(base, filters), cursor).limit(limit + 1)
    rows = list((await db.execute(stmt)).scalars().all())
    more = len(rows) > limit
    rows = rows[:limit]
    return AuditPage(
        items=await to_entries(db, rows),
        next_cursor=encode_cursor(rows[-1].timestamp, rows[-1].id) if more and rows else None)


async def facets(db: AsyncSession, base_where, filters: AuditFilters) -> dict:
    """Counts by category and by outcome over the same window, for the filter chips.
    The category/outcome the caller is filtering by is left out of its own counts so the
    chips keep showing the alternatives."""
    from dataclasses import replace

    def counted(column, f: AuditFilters):
        return apply_filters(select(column, func.count()).where(base_where).group_by(column), f)

    by_action = (await db.execute(
        apply_filters(select(AuditLog.action, func.count()).where(base_where).group_by(AuditLog.action),
                      replace(filters, category=None, actions=[])))).all()
    categories: dict[str, int] = {}
    for action, n in by_action:
        cat = audit_catalog.describe(action).category
        categories[cat] = categories.get(cat, 0) + int(n)
    outcomes = {o: int(n) for o, n in (await db.execute(counted(AuditLog.outcome, replace(filters, outcome=None)))).all()}
    return {
        "categories": [{"key": k, "label": v, "count": categories.get(k, 0)}
                       for k, v in audit_catalog.CATEGORIES.items()],
        "outcomes": [{"key": k, "count": outcomes.get(k, 0)} for k in ("success", "failure", "denied")],
    }


# ── the customer's view ───────────────────────────────────────────────────────

class CustomerAuditEntry(BaseModel):
    id: uuid.UUID
    timestamp: datetime
    label: str
    category: str
    category_label: str
    outcome: str
    who: str                      # "You", a colleague's email, or "Vedha analyst"
    who_is_vedha: bool
    ip_address: str | None = None  # the customer's own people only


def customer_scope(engagement_id: uuid.UUID):
    """Entries a customer may see: customer-visible actions in their engagement, plus
    the sign-in and account events of the customer users bound to it."""
    visible = audit_catalog.customer_visible_actions()
    own_users = select(cast(User.id, String)).where(User.client_engagement_id == engagement_id)
    return and_(
        AuditLog.action.in_(visible),
        or_(AuditLog.engagement_id == engagement_id,
            and_(AuditLog.actor_type == "client", AuditLog.actor_id.in_(own_users))),
    )


async def to_customer_entries(
    db: AsyncSession, rows: list[AuditLog], *, me: uuid.UUID,
) -> list[CustomerAuditEntry]:
    people = await _people(db, rows)
    out: list[CustomerAuditEntry] = []
    for r in rows:
        info = audit_catalog.describe(r.action)
        own = r.actor_type == "client"
        if own and r.actor_id == str(me):
            who = "You"
        elif own:
            who = r.actor_label or people.get(r.actor_id) or "A colleague"
        else:
            who = "Vedha analyst"
        out.append(CustomerAuditEntry(
            id=r.id, timestamp=r.timestamp, label=info.label, category=info.category,
            category_label=audit_catalog.CATEGORIES[info.category], outcome=r.outcome,
            who=who, who_is_vedha=not own, ip_address=r.ip_address if own else None))
    return out


class CustomerAuditPage(BaseModel):
    items: list[CustomerAuditEntry]
    next_cursor: str | None = None
