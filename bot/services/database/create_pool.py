from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


if TYPE_CHECKING:
    from sqlalchemy import URL
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


def create_pool(dsn: str | URL) -> async_sessionmaker[AsyncSession]:
    """
    Create a new database pool.

    :param dsn: The database URL.
    :return: The database pool.
    """
    engine: AsyncEngine = create_async_engine(url=dsn, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)
