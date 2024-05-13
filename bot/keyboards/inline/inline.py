from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from ...enums import Locale
from .factory import Language, Pagination


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


def top_users(
    i18n: I18nContext, profile: bool, end_page: bool = False, page: int = 0
) -> InlineKeyboardMarkup:
    """
    Top users keyboard

    :param i18n: I18nContext object.
    :param profile: Is the profile.
    :param end_page: Is the last page.
    :param page: Page number.
    :return: InlineKeyboardMarkup with the top users.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if profile:
        keyboard.add(
            InlineKeyboardButton(text=i18n.get("close-profile-btn"), callback_data="close-profile")
        )
    else:
        keyboard.add(
            InlineKeyboardButton(text=i18n.get("profile-btn"), callback_data="open-profile")
        )

    keyboard.row(
        *[
            InlineKeyboardButton(
                text="◀️" if page else "⏹️",
                callback_data=Pagination(action="prev", page=page).pack(),
            ),
            InlineKeyboardButton(
                text="▶️" if not end_page else "⏹️",
                callback_data=Pagination(action="next", page=page).pack() if not end_page else "_",
            ),
        ],
        width=2,
    )
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
