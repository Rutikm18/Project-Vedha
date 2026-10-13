from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.db_rls import mark_session_tenant

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
    pool_recycle=settings.db_pool_recycle,
    pool_timeout=settings.db_pool_timeout,
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# P3: read-replica routing. A separate engine bound to the replica DSN when
# configured; otherwise it IS the primary engine (zero-cost no-op until a
# replica exists). Read-only endpoints use get_read_db so the dashboard's
# aggregate reads can be offloaded from the primary just by setting
# DATABASE_READ_URL — no code change needed when the replica appears.
read_engine = (
    create_async_engine(
        settings.database_read_url,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_pre_ping=True,
        pool_recycle=settings.db_pool_recycle,
        pool_timeout=settings.db_pool_timeout,
        echo=settings.debug,
    )
    if settings.database_read_url
    else engine
)
ReadSessionLocal = async_sessionmaker(
    read_engine, class_=AsyncSession, expire_on_commit=False,
    autocommit=False, autoflush=False,
)


# Whether each engine speaks Postgres (RLS and the tenant GUC are Postgres-only;
# SQLite unit tests are a no-op). Computed once at import.
_PRIMARY_IS_PG = engine.dialect.name == "postgresql"
_READ_IS_PG = read_engine.dialect.name == "postgresql"


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            # F1: opt this request's session into the tenant RLS GUC (dormant
            # unless DB_RLS_ENABLED and a tenant is present). No-op otherwise.
            mark_session_tenant(session, getattr(request.state, "tenant_id", None),
                                enabled=settings.db_rls_enabled, is_postgres=_PRIMARY_IS_PG)
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_read_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Read-only session (no commit) routed to the replica when configured.
    For SELECT-only endpoints; never write through this."""
    async with ReadSessionLocal() as session:
        try:
            mark_session_tenant(session, getattr(request.state, "tenant_id", None),
                                enabled=settings.db_rls_enabled, is_postgres=_READ_IS_PG)
            yield session
        finally:
            await session.close()
