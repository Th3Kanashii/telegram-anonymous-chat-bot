from typing import Final

from aiogram import Router

from . import factories, process_data

router: Final[Router] = Router(name=__name__)
router.include_routers(factories.router, process_data.router)
