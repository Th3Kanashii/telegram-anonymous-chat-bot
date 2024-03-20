from aiogram import Dispatcher, F


def _setup_routers(dispatcher: Dispatcher) -> None:
    """
    Include routers in the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    from . import callbacks, chatting, menu, next, search, stop

    dispatcher.message.filter(F.chat.type == "private")
    dispatcher.include_routers(
        menu.router,
        stop.router,
        search.router,
        next.router,
        callbacks.router,
        chatting.router,
    )


__all__ = [
    "_setup_routers",
]
