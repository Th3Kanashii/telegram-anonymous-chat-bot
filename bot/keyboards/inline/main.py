from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.enums import Locale, Top, UserProfile

from .factory import Language, Pagination, Profile


if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup
    from aiogram_i18n import I18nContext


def select_language() -> InlineKeyboardMarkup:
    """
    Select language keyboard

    :return: InlineKeyboardMarkup with language selection
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.row(
        *[
            InlineKeyboardButton(text="🇬🇧", callback_data=Language(language=Locale.EN).pack()),
            InlineKeyboardButton(text="🇺🇦", callback_data=Language(language=Locale.UK).pack()),
            InlineKeyboardButton(text="🇯🇵", callback_data=Language(language=Locale.JA).pack()),
        ],
        width=2,
    )
    return keyboard.as_markup()


def pagination_users(*, end_page: bool = False, page: int = 0) -> InlineKeyboardMarkup:
    """
    Pagination keyboard for top users

    :param end_page: Is the last page.
    :param page: Page number.
    :return: InlineKeyboardMarkup with the top users.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.row(
        *[
            InlineKeyboardButton(
                text="◀️" if page else "🍓",
                callback_data=(
                    Pagination(action=Top.PREV_USER, page=page).pack() if page else Top.NOTHING
                ),
            ),
            InlineKeyboardButton(text="👤", callback_data=UserProfile.HOME),
            InlineKeyboardButton(
                text="▶️" if not end_page else "🍑",
                callback_data=(
                    Pagination(action=Top.NEXT_USER, page=page).pack()
                    if not end_page
                    else Top.NOTHING
                ),
            ),
        ],
        width=3,
    )
    return keyboard.as_markup()


def profile(i18n: I18nContext, *, profile: bool) -> InlineKeyboardMarkup:
    """
    Open profile keyboard

    :param i18n: I18nContext object.
    :param profile: Is the profile opened.
    :return: InlineKeyboardMarkup with the open profile button.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if profile:
        keyboard.add(
            InlineKeyboardButton(
                text=i18n.get("close-profile-btn"),
                callback_data=Profile(action=UserProfile.CLOSE).pack(),
            ),
        )
    else:
        keyboard.add(
            InlineKeyboardButton(
                text=i18n.get("profile-btn"),
                callback_data=Profile(action=UserProfile.OPEN).pack(),
            ),
        )
    keyboard.add(InlineKeyboardButton(text=i18n.get("top-btn"), callback_data=Top.RATING))
    keyboard.adjust(1)
    return keyboard.as_markup()


def link_profile(i18n: I18nContext, url: str) -> InlineKeyboardMarkup:
    """
    Link profile keyboard

    :param i18n: I18nContext object.
    :param url: URL of the profile.
    :return: InlineKeyboardMarkup with the link to the profile.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=i18n.get("profile-btn"), url=url))
    return keyboard.as_markup()
