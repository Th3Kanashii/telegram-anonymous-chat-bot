from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware

from bot.services.database import SQLSessionContext


if TYPE_CHECKING:
    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DBSessionMiddleware(BaseMiddleware):
    """
    Middleware for handling database sessions.
    """

    session_pool: async_sessionmaker[AsyncSession]

    __slots__ = ("session_pool",)

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]) -> None:
        """
        :param session_pool: Pool of database sessions.
        """
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with SQLSessionContext(session_pool=self.session_pool) as (repository, uow):
            data["repository"] = repository
            data["uow"] = uow
            return await handler(event, data)
