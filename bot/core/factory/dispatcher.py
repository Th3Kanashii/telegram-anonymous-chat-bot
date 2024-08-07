from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .setup import setup_filters, setup_inner_middlewares, setup_outer_middlewares, setup_routers


if TYPE_CHECKING:
    from bot.config import Config


def create_dispatcher(config: Config) -> Dispatcher:
    """
    Creates and configures a Telegram bot dispatcher.

    :param config: A configuration object containing necessary settings.
    :return: An instance of the Dispatcher for the Telegram bot.
    """
    storage: MemoryStorage = MemoryStorage()
    dispatcher: Dispatcher = Dispatcher(name="main_dispatcher", config=config, storage=storage)
    setup_filters(dispatcher=dispatcher)
    setup_outer_middlewares(dispatcher=dispatcher, config=config)
    setup_inner_middlewares(dispatcher=dispatcher)
    setup_routers(dispatcher=dispatcher)
    return dispatcher
