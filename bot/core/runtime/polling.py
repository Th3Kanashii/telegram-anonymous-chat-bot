from __future__ import annotations

from typing import TYPE_CHECKING

from bot.utils.commands import set_default_commands


if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher
    from aiogram_i18n import I18nMiddleware
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def polling_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    """
    Starts the bot in the polling mode.

    :param bot: An instance of the Telegram bot.
    :param config: An instance of the bot configuration.
    """
    i18n: I18nMiddleware = dispatcher["i18n_middleware"]
    with i18n.use_context() as _i18n:
        await set_default_commands(bot=bot, i18n=_i18n)

    await bot.delete_webhook(drop_pending_updates=True)


async def polling_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    """
    Stops the bot in the polling mode.

    :param bot: An instance of the Telegram bot.
    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    session_pool: async_sessionmaker[AsyncSession] = dispatcher["session_pool"]
    async with session_pool() as session:
        await session.close_all()
        await session.bind.dispose()

    await dispatcher.storage.close()
    await bot.session.close()
