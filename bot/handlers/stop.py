from __future__ import annotations

from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from ..keyboards import builder_reply
from ..middlewares import StopCompanionMiddleware

router: Final[Router] = Router(name=__name__)
router.message.middleware(StopCompanionMiddleware())


@router.message(
    or_f(Command("stop"), F.text.in_([LazyProxy("stop-btn"), LazyProxy("cancel-btn")])),
    flags={"throttling_key": "default"},
)
async def stop_command(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handle the /stop command.
    Stop the companion search.

    :param message: The message.
    :param i18n: The i18n context.
    :return: The response.
    """
    return message.answer(
        text=i18n.get("stop-companion"), reply_markup=builder_reply(i18n.get("search-btn"))
    )
