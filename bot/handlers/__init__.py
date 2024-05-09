from aiogram import Dispatcher, F

from .callbacks import callbacks_router
from .chatting import chatting_router
from .menu import menu_router


def setup_routers(dispatcher: Dispatcher) -> None:
    """
    Include routers in the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.message.filter(F.chat.type == "private")
    dispatcher.include_routers(
        menu_router,
        chatting_router,
        callbacks_router,
    )


__all__ = [
    "setup_routers",
]
