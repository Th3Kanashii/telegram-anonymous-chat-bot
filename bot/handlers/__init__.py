from aiogram import Dispatcher, F
from aiogram.enums.chat_type import ChatType

from . import callbacks, common, messages


def setup_routers(dispatcher: Dispatcher) -> None:
    """
    Include routers in the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.message.filter(F.chat.type == ChatType.PRIVATE)
    dispatcher.include_routers(
        common.router,
        callbacks.router,
        messages.router,
    )


__all__ = [
    "setup_routers",
]
