from __future__ import annotations

from enum import StrEnum, auto


class CallbackData(StrEnum):
    """
    Enumerate the callback data.
    """

    PROFILE = auto()
    OPEN_PROFILE = auto()
    CLOSE_PROFILE = auto()
    NOTHING = auto()
    TOP = auto()
