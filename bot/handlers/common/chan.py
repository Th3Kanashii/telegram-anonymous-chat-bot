from __future__ import annotations

import secrets
from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command


if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser, UoW

CHAN_PRICE: Final[int] = 999

flags: Final[dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(Command("chan"), flags=flags)
async def chan_command(message: Message, i18n: I18nContext, user: DBUser, uow: UoW) -> None:
    """
    Handle the /chan command.
    Send a random 4chan image.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    """
    if user.balance <= CHAN_PRICE:
        await message.answer(
            i18n.get("not-enough-balance", name=user.mention, balance=user.balance),
        )
        return

    user.balance -= CHAN_PRICE
    chans: list[str] = [
        "https://imgur.com/a/suN3hTv",
        "https://imgur.com/a/lSwCP2O",
        "https://imgur.com/a/dNWN9Gq",
    ]
    chan_index: int = secrets.randbelow(len(chans))
    await uow.commit(user)
    await message.answer_photo(
        photo=chans[chan_index],
        caption=i18n.get("chans-info", chan=chan_index),
    )
