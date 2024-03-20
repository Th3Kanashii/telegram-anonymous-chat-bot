from __future__ import annotations

from enum import IntEnum


class Throttle(IntEnum):
    """
    Throttle enum
    """

    THROTTLE_MENU = 1
    THROTTLE_DICE = 2
    THROTTLE_CHATTING = 0.5

    DEFAULT = THROTTLE_MENU
