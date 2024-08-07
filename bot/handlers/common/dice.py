from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command


if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser, Repository, UoW

flags: Final[dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(Command("dice"), flags={"throttling_key": "dice"})
async def dice_command(
    message: Message,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
    uow: UoW,
) -> None:
    """
    Handle the /dice command.
    Send a dice and add its value to the user's balance.

    :param message: Received message.
    :param i18n: I18n context.
    :param user: User from the database.
    :param repository: The repository.
    :param uow: Unit of work.
    """
    dice: Message = await message.answer_dice(emoji=DiceEmoji.DICE)
    await asyncio.sleep(2)
    user.balance += dice.dice.value**3
    await uow.commit(user)
    position: int = await repository.user.position(balance=user.balance)
    await dice.reply(
        text=i18n.get("dice", number=dice.dice.value, balance=user.balance, position=position),
    )
