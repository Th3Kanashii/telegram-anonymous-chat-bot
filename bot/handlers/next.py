from __future__ import annotations

from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from ..keyboards import builder_reply
from ..middlewares import NextCompanionMiddleware

router: Final[Router] = Router(name=__name__)
router.message.middleware(NextCompanionMiddleware())


@router.message(
    or_f(Command("next"), F.text == LazyProxy("next-btn")), flags={"throttling_key": "default"}
)
async def next_command(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handle the /next command.
    Next the companion.

    :param message: The message.
    :param i18n: The i18n context.
    :return: The response.
    """
    return message.answer(
        text=i18n.get("next-companion"), reply_markup=builder_reply(i18n.get("search-btn"))
    )
