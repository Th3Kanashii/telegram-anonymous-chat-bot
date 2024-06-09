from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Final

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from ...enums import CallbackData
from ...keyboards import pagination_users, profile

if TYPE_CHECKING:
    from ...services.database import DBUser, Repository

router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == CallbackData.TOP)
async def tops(
    callback: CallbackQuery, i18n: I18nContext, user: DBUser, repository: Repository
) -> None:
    """
    Handle the top callback.
    Show the top users.

    :param callback: The callback.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    """
    users_stats: Dict[str, str | int] = await repository.user.stats(user=user)
    await callback.message.edit_text(
        text=i18n.get("top", **users_stats),
        reply_markup=pagination_users(),
    )


@router.callback_query(F.data == CallbackData.PROFILE)
async def get_profile(callback: CallbackQuery, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the profile callback.
    Change the profile status.

    :param callback: The callback.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await callback.message.edit_text(
        text=i18n.get(
            "profile",
            name=user.mention,
            id=str(user.id),
            open="❌" if user.profile else "☑️",
            balance=user.balance,
            date=user.created_at,
        ),
        reply_markup=profile(i18n=i18n, profile=user.profile),
    )


@router.callback_query(F.data == CallbackData.NOTHING)
async def nothing(callback: CallbackQuery, i18n: I18nContext) -> None:
    """
    Handle the nothing callback.

    :param callback: The callback.
    :param i18n: The i18n context.
    """
    await callback.answer(text=i18n.get("nothing"), cache_time=60)
