from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove

from bot.keyboards.reply import builder_reply


if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart(), flags={"throttling_key": "default"})
async def start_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /start command.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer_photo(
        photo="https://imgur.com/a/GwWoUQO",
        caption=i18n.get("welcome", name=user.mention),
        reply_markup=builder_reply(i18n.get("search-btn")),
    )


@router.message(Command("help"), flags={"throttling_key": "default"})
async def help_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /help command.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(i18n.get("help", name=user.mention), reply_markup=ReplyKeyboardRemove())
