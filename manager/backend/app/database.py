from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings

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


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_read_db() -> AsyncGenerator[AsyncSession, None]:
    """Read-only session (no commit) routed to the replica when configured.
    For SELECT-only endpoints; never write through this."""
    async with ReadSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
