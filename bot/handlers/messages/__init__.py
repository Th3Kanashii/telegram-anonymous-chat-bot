from typing import Final

from aiogram import Router

from . import chatting


router: Final[Router] = Router(name=__name__)
router.include_routers(chatting.router)
