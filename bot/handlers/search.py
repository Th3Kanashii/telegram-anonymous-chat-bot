from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from ..keyboards import builder_reply
from ..middlewares import SearchCompanionMiddleware

search_router: Final[Router] = Router(name=__name__)
search_router.message.middleware(SearchCompanionMiddleware())


@search_router.message(
    or_f(Command("search"), F.text == LazyProxy("search-btn")), flags={"throttling_key": "default"}
)
async def search_command(message: Message, i18n: I18nContext) -> Any:
    """
    Handle the /search command.
    Search for a companion.

    :param message: The message.
    :param i18n: The i18n context.
    :return: The response.
    """
    return message.answer(
        text=i18n.get("search-companion"),
        reply_markup=builder_reply(i18n.get("stop-btn")),
    )
