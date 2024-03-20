from __future__ import annotations

from enum import StrEnum, auto


class UserStatus(StrEnum):
    """
    Enumeration representing user statuses.
    """

    ACTIVE = auto()
    WAITING = auto()
    OFFLINE = auto()

    DEFAULT = OFFLINE
