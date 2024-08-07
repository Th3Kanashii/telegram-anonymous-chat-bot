from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


if TYPE_CHECKING:
    from aiogram.types import ReplyKeyboardMarkup
    from aiogram_i18n import I18nContext


def builder_reply(
    *texts: str,
    is_persistent: bool | None = None,
    resize_keyboard: bool | None = True,
    one_time_keyboard: bool | None = None,
    input_field_placeholder: bool | None = None,
    selective: bool | None = None,
    width: int = 2,
) -> ReplyKeyboardMarkup:
    """
    Constructs a ReplyKeyboardMarkup using the provided text buttons.

    :param texts: Variable number of strings representing the text for each button.
    :param is_persistent: If True, the keyboard is persistent. Default is None.
    :param resize_keyboard: If True, the keyboard is resized. Default is True.
    :param one_time_keyboard: If True, the keyboard is displayed only once. Default is None.
    :param input_field_placeholder: Placeholder text for the input field. Default is None.
    :param selective: (Optional) If True, the keyboard is selective. Default is None.
    :param width: (Optional) Number of buttons in each row. Default is 2.

    :return: ReplyKeyboardMarkup object representing the constructed keyboard.
    """
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=text) for text in texts], width=width)
    return builder.as_markup(
        is_persistent=is_persistent,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )


def dialog(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """
    Constructs a ReplyKeyboardMarkup for a dialog.

    :param i18n: I18nContext instance.
    :return ReplyKeyboardMarkup object representing the constructed keyboard.
    """
    return builder_reply(*[i18n.get("next-btn"), i18n.get("cancel-btn")])
