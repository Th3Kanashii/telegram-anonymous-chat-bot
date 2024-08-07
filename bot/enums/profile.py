from enum import StrEnum, auto


class UserProfile(StrEnum):
    """
    Enumerate the different states of the profile.
    """

    HOME = auto()
    OPEN = auto()
    CLOSE = auto()
