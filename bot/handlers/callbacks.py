from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommandScopeChat, CallbackQuery, ReplyKeyboardRemove
from aiogram_i18n import I18nContext

from ..keyboards import Language, Pagination, top_users
from ..ui_commands import set_commands

if TYPE_CHECKING:
    from ..services.database import DBUser, Repository

callbacks_router: Final[Router] = Router(name=__name__)


@callbacks_router.callback_query(Language.filter())
async def language_changed(
    callback: CallbackQuery, callback_data: Language, bot: Bot, i18n: I18nContext, user: DBUser
) -> Any:
    """
    Handle the language selection callback.
    Change the user's language.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param bot: The bot.
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


@callbacks_router.callback_query(Pagination.filter())
async def pagination(
    callback: CallbackQuery,
    callback_data: Pagination,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
) -> Any:
    """
    Handle the pagination callback.
    Change the page.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :return: The response.
    """
    page_num: int = int(callback_data.page)
    page: int = page_num - 1 if page_num > 0 else 0

    position: int = await repository.user.position(balance=user.balance)
    users: List[tuple[str, int]] = await repository.user.top()

    if callback_data.action == "next":
        page = page_num + 1 if page_num < len(users) - 1 else page_num

    start_index: int = page * 15
    end_index: int = min((page + 1) * 15, len(users))
    current_users: List[tuple[str, int]] = users[start_index:end_index]

    top: str = "".join(
        [
            f"❯❯ {index + start_index + 1}. 🕶 ⇏ {balance} 🍪\n"
            for index, (name, balance) in enumerate(current_users)
        ]
    )
    end_page: bool = end_index == len(users)

    with suppress(TelegramBadRequest):
        return callback.message.edit_text(
            text=i18n.get("top", tops=top, name=user.mention, position=position, users=len(users)),
            reply_markup=top_users(end_page=end_page, page=page),
        )
