from __future__ import annotations

from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from ..keyboards import builder_reply
from ..middlewares import SearchCompanionMiddleware

router: Final[Router] = Router(name=__name__)
router.message.middleware(SearchCompanionMiddleware())


@router.message(
    or_f(Command("search"), F.text == LazyProxy("search-btn")), flags={"throttling_key": "default"}
)
async def search_command(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
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
