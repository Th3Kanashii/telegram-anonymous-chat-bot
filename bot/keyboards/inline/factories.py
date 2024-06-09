from aiogram.filters.callback_data import CallbackData


class Language(CallbackData, prefix="language"):
    """
    Language callback data
    """

    language: str


class Profile(CallbackData, prefix="profile"):
    """
    Profile callback data
    """

    action: str


class Pagination(CallbackData, prefix="pagination"):
    """
    Pagination callback data
    """

    page: int
    action: str
