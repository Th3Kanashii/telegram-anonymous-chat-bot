from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from ...enums import CallbackData, Locale
from .factories import Language, Pagination, Profile


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


def pagination_users(end_page: bool = False, page: int = 0) -> InlineKeyboardMarkup:
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
                    Pagination(action="prev", page=page).pack() if page else CallbackData.NOTHING
                ),
            ),
            InlineKeyboardButton(text="👤", callback_data=CallbackData.PROFILE),
            InlineKeyboardButton(
                text="▶️" if not end_page else "🍑",
                callback_data=(
                    Pagination(action="next", page=page).pack() if not end_page else CallbackData.NOTHING
                ),
            ),
        ],
        width=3,
    )
    return keyboard.as_markup()


def profile(i18n: I18nContext, profile: bool) -> InlineKeyboardMarkup:
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
                callback_data=Profile(action=CallbackData.CLOSE_PROFILE).pack(),
            )
        )
    else:
        keyboard.add(
            InlineKeyboardButton(
                text=i18n.get("profile-btn"),
                callback_data=Profile(action=CallbackData.OPEN_PROFILE).pack(),
            )
        )
    keyboard.add(InlineKeyboardButton(text=i18n.get("top-btn"), callback_data=CallbackData.TOP))
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
