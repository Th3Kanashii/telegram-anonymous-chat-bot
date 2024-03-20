from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Bot, Router
from aiogram.methods import TelegramMethod
from aiogram.types import BotCommandScopeChat, CallbackQuery, ReplyKeyboardRemove
from aiogram_i18n import I18nContext

from ..commands import set_commands
from ..keyboards import Language

if TYPE_CHECKING:
    from ..services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.callback_query(Language.filter())
async def language_changed(
    callback: CallbackQuery, callback_data: Language, bot: Bot, i18n: I18nContext, user: DBUser
) -> TelegramMethod[Any]:
    """
    Handle the language selection callback.
    Change the user's language.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    await i18n.set_locale(locale=callback_data.language)
    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=user.id))
    await set_commands(bot=bot, i18n=i18n, chat_id=user.id)
    await callback.message.delete()

    return callback.message.answer(
        text=i18n.get("help", name=user.mention), reply_markup=ReplyKeyboardRemove()
    )
