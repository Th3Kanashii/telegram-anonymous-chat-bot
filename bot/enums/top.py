from enum import StrEnum, auto


class Top(StrEnum):
    """
    Enumeration representing the top of the list.
    """

    RATING = auto()
    PREV_USER = auto()
    NEXT_USER = auto()
    NOTHING = auto()
