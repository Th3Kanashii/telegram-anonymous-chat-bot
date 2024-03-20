from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Optional

from aiogram import Bot, Router
from aiogram.methods import TelegramMethod
from aiogram.types import Message, MessageReactionUpdated
from aiogram_i18n import I18nContext

from ..keyboards import dialog

if TYPE_CHECKING:
    from ..services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(flags={"throttling_key": "chatting"})
async def chatting(message: Message, i18n: I18nContext, user: DBUser) -> TelegramMethod[Any]:
    """
    Process the chatting.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    if user.companion:
        return message.copy_to(chat_id=user.companion, reply_markup=dialog(i18n=i18n))
    return message.delete()


@router.message_reaction()
async def chatting_reaction(
    message: MessageReactionUpdated, bot: Bot, user: DBUser
) -> Optional[bool]:
    """
    Process the reaction to the chatting message.

    :parammessage: The message.
    :param bot: The bot.
    :param user: The user.
    :return: The response.
    """
    if user.companion:
        return await bot.set_message_reaction(
            chat_id=user.companion,
            message_id=message.message_id - 1,
            reaction=message.new_reaction,
        )
    return None
