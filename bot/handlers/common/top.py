from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import F, Router
from aiogram.filters import Command

from bot.enums import Top
from bot.keyboards.inline import Pagination, pagination_users


if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser, Repository

flags: Final[dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(Command("top"), flags=flags)
async def top_command(
    message: Message,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
) -> None:
    """
    Handle the /top command.
    Show the top users.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    """
    users_stats: dict[str, str | int] = await repository.user.stats(user=user)
    await message.answer(
        text=i18n.get("top", **users_stats),
        reply_markup=pagination_users(),
    )


@router.callback_query(F.data == Top.RATING)
async def tops(
    callback: CallbackQuery,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
) -> None:
    """
    Handle the top callback.
    Show the top users.

    :param callback: The callback.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    """
    users_stats: dict[str, str | int] = await repository.user.stats(user=user)
    await callback.message.edit_text(
        text=i18n.get("top", **users_stats),
        reply_markup=pagination_users(),
    )


@router.callback_query(Pagination.filter())
async def pagination(
    callback: CallbackQuery,
    callback_data: Pagination,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
) -> None:
    """
    Handle the pagination callback.
    Change the page.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    """
    page_num: int = int(callback_data.page)
    page: int = page_num - 1 if page_num > 0 else 0

    position: int = await repository.user.position(balance=user.balance)
    users: list[tuple[str, bool, int]] = await repository.user.top()

    if callback_data.action == Top.PREV_USER:
        page = page_num + 1 if page_num < len(users) - 1 else page_num

    start_index: int = page * 15
    end_index: int = min((page + 1) * 15, len(users))
    current_users: list[tuple[str, bool, int]] = users[start_index:end_index]

    top: str = "".join([
        f"❯❯ {index + start_index + 1}. {name if profile else '🕶'} ⇏ {balance} 🍪\n"
        for index, (name, profile, balance) in enumerate(current_users)
    ])
    end_page: bool = end_index == len(users)

    await callback.message.edit_text(
        text=i18n.get("top", tops=top, name=user.name, position=position, users=len(users)),
        reply_markup=pagination_users(end_page=end_page, page=page),
    )


@router.callback_query(F.data == Top.NOTHING)
async def nothing(callback: CallbackQuery, i18n: I18nContext) -> None:
    """
    Handle the nothing callback.

    :param callback: The callback.
    :param i18n: The i18n context.
    """
    await callback.answer(text=i18n.get("nothing"), cache_time=60)
