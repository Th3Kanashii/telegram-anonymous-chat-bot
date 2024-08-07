from typing import Final

from aiogram import Router

from . import chan, dialog, dice, language, profile, start, top


router: Final[Router] = Router(name=__name__)
router.include_routers(
    start.router,
    chan.router,
    dialog.router,
    language.router,
    profile.router,
    top.router,
    dice.router,
)
