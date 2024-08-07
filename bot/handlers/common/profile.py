from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import F, Router
from aiogram.filters import Command

from bot.enums import UserProfile
from bot.keyboards.inline import Profile, profile


if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser, UoW

flags: Final[dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(Command("profile"), flags=flags)
async def profile_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /profile command.
    Show the user's profile.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(
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


@router.callback_query(F.data == UserProfile.HOME)
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


@router.callback_query(Profile.filter())
async def update_profile(
    callback: CallbackQuery,
    callback_data: Profile,
    i18n: I18nContext,
    user: DBUser,
    uow: UoW,
) -> None:
    """
    Handle the profile callback.
    Open or close the user's profile.

    :param callback: The callback.
    :param callback_data: The callback data.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    """
    if callback_data.action == UserProfile.OPEN:
        user.open_profile()
    else:
        user.close_profile()

    await uow.commit(user)
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
