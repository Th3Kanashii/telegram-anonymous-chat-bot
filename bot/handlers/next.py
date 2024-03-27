from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from ..keyboards import builder_reply
from ..middlewares import NextCompanionMiddleware

next_router: Final[Router] = Router(name=__name__)
next_router.message.middleware(NextCompanionMiddleware())


@next_router.message(
    or_f(Command("next"), F.text == LazyProxy("next-btn")), flags={"throttling_key": "default"}
)
async def next_command(message: Message, i18n: I18nContext) -> Any:
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
