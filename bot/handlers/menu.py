from __future__ import annotations

import asyncio
import secrets
from typing import TYPE_CHECKING, Any, Dict, Final, List, Optional

from aiogram import Bot, Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext

from ..keyboards import builder_reply, dialog, link_profile, select_language, top_users
from ..ui_commands import set_commands

if TYPE_CHECKING:
    from ..services.database import DBUser, Repository, UoW

flags: Final[Dict[str, str]] = {"throttling_key": "default"}
menu_router: Final[Router] = Router(name=__name__)


@menu_router.message(CommandStart(), flags=flags)
async def start_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, commands: Optional[bool] = False
) -> Any:
    """
    Handle the /start command.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param commands: Whether to set the commands.
    :return: The response.
    """
    if commands:
        await set_commands(bot=bot, i18n=i18n, chat_id=user.id)

    return message.answer_photo(
        photo="https://imgur.com/a/GwWoUQO",
        caption=i18n.get("welcome", name=user.mention),
        reply_markup=builder_reply(i18n.get("search-btn")),
    )


@menu_router.message(Command("language"), flags=flags)
async def language_command(message: Message, i18n: I18nContext, user: DBUser) -> Any:
    """
    Handle the /language command.
    Show the language selection keyboard.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    return message.answer(i18n.get("language", name=user.mention), reply_markup=select_language())


@menu_router.message(Command("help"), flags=flags)
async def help_command(message: Message, i18n: I18nContext, user: DBUser) -> Any:
    """
    Handle the /help command.
    Show the help message.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    return message.answer(
        text=i18n.get("help", name=user.mention), reply_markup=ReplyKeyboardRemove()
    )


@menu_router.message(Command("link"), flags=flags)
async def link_command(message: Message, bot: Bot, i18n: I18nContext, user: DBUser) -> Any:
    """
    Handle the /link command.
    Send link to the companion.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    if user.companion:
        await bot.send_message(
            chat_id=user.companion,
            text=i18n.get("send-link"),
            reply_markup=link_profile(i18n=i18n, url=user.url),
        )
        return message.answer(text=i18n.get("companion-linked"), reply_markup=dialog(i18n=i18n))
    return message.answer(text=user.mention)


@menu_router.message(Command("chan"), flags=flags)
async def chan_command(message: Message, i18n: I18nContext, user: DBUser, uow: UoW) -> Any:
    """
    Handle the /chan command.
    Send a random 4chan image.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    :return: The response.
    """
    if user.balance <= 999:
        return message.answer(
            i18n.get("not-enough-balance", name=user.mention, balance=user.balance)
        )

    user.balance -= 999
    chans: List[str] = [
        "https://imgur.com/a/suN3hTv",
        "https://imgur.com/a/lSwCP2O",
        "https://imgur.com/a/dNWN9Gq",
    ]
    chan_index: int = secrets.randbelow(len(chans))
    await uow.commit()
    return message.answer_photo(
        photo=chans[chan_index], caption=i18n.get("chans-info", chan=chan_index)
    )


@menu_router.message(Command("profile"), flags=flags)
async def profile_command(message: Message, i18n: I18nContext, user: DBUser) -> Any:
    """
    Handle the /profile command.
    Show the user's profile.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :return: The response.
    """
    return message.answer_photo(
        photo="https://imgur.com/nipmCQe",
        caption=i18n.get(
            "profile", name=user.mention, id=user.id, balance=user.balance, date=user.created_at
        ),
    )


@menu_router.message(Command("top"), flags=flags)
async def top_command(
    message: Message, i18n: I18nContext, user: DBUser, repository: Repository
) -> Any:
    """
    Handle the /top command.
    Show the top users.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :return: The response.
    """
    position: int = await repository.user.position(balance=user.balance)
    users: List[tuple[str, bool, int]] = await repository.user.top()
    top: str = "".join(
        [
            f"❯❯ {index + 1}. {name if profile else '🕶'} ⇏ {balance} 🍪\n"
            for index, (name, profile, balance) in enumerate(users[0:15])
        ]
    )
    return message.answer(
        text=i18n.get("top", tops=top, name=user.name, position=position, users=len(users)),
        reply_markup=top_users(i18n=i18n, profile=user.profile),
    )


@menu_router.message(Command("dice"), flags={"throttling_key": "dice"})
async def dice_command(
    message: Message, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> Any:
    """
    Handle the /dice command.
    Send a dice and add its value to the user's balance.

    :param message: Received message.
    :param i18n: I18n context.
    :param user: User from the database.
    :param repository: The repository.
    :param uow: Unit of work.
    :return: The responce.
    """
    dice: Message = await message.answer_dice(emoji=DiceEmoji.DICE)
    await asyncio.sleep(2)

    user.balance += dice.dice.value**3
    await uow.commit()
    position: int = await repository.user.position(balance=user.balance)
    return dice.reply(
        text=i18n.get("dice", number=dice.dice.value, balance=user.balance, position=position)
    )
