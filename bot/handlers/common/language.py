from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

from bot.keyboards.inline import Language, select_language
from bot.utils import set_commands


if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import CallbackQuery, Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser

flags: Final[dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(Command("language"), flags=flags)
async def language_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /language command.
    Show the language selection keyboard.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(i18n.get("language", name=user.mention), reply_markup=select_language())


@router.callback_query(Language.filter())
async def language_changed(
    callback: CallbackQuery,
    callback_data: Language,
    bot: Bot,
    i18n: I18nContext,
    user: DBUser,
) -> None:
    """
    Handle the language selection callback.
    Change the user's language.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await i18n.set_locale(locale=callback_data.language)
    await set_commands(bot=bot, i18n=i18n, chat_id=user.id)
    await callback.message.delete()
    await callback.message.answer(
        text=i18n.get("help", name=user.mention),
        reply_markup=ReplyKeyboardRemove(),
    )
