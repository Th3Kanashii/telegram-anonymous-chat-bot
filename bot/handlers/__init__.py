from aiogram import Dispatcher, F

from .chatting import chatting_router
from .menu import menu_router
from .next import next_router
from .search import search_router
from .stop import stop_router


def _setup_routers(dispatcher: Dispatcher) -> None:
    """
    Include routers in the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.message.filter(F.chat.type == "private")
    dispatcher.include_routers(
        menu_router,
        search_router,
        next_router,
        stop_router,
        chatting_router,
    )


__all__ = [
    "_setup_routers",
]
