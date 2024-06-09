from __future__ import annotations

import asyncio
import secrets
from typing import TYPE_CHECKING, Dict, Final, List, Optional

from aiogram import Bot, F, Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command, or_f
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext, LazyProxy

from ...enums import UserStatus
from ...keyboards import (
    builder_reply,
    dialog,
    link_profile,
    pagination_users,
    profile,
    select_language,
)
from ...utils import find_companion

if TYPE_CHECKING:
    from ...services.database import DBUser, Repository, UoW

flags: Final[Dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(or_f(Command("search"), F.text == LazyProxy("search-btn")), flags=flags)
async def search_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> None:
    """
    Handle the /search command.
    Search for a companion.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    """
    if user.status == UserStatus.ACTIVE:
        await message.answer(text=i18n.get("chat-with-companion"), reply_markup=dialog(i18n=i18n))
        return
    if user.status == UserStatus.WAITING:
        await message.answer(
            text=i18n.get("looking-for-a-companion"),
            reply_markup=builder_reply(i18n.get("stop-btn")),
        )
        return

    if await find_companion(bot, i18n, user, repository, uow):
        return

    user.status = UserStatus.WAITING
    await uow.commit(user)
    await message.answer_sticker(
        sticker="CAACAgQAAxkBAAEL8KhmIDlSgGRsYYZdHgeYeCa9WRmeHgACeg8AAiD2UgyxLSQwkJOmejQE"
    )
    await message.answer(
        text=i18n.get("search-companion"),
        reply_markup=builder_reply(i18n.get("stop-btn")),
    )


@router.message(
    or_f(Command("stop"), F.text.in_([LazyProxy("stop-btn"), LazyProxy("cancel-btn")])), flags=flags
)
async def stop_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> None:
    """
    Handle the /stop command.
    Stop the companion search.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    """
    if user.status == UserStatus.OFFLINE:
        await message.answer(
            text=i18n.get("search-not-started"),
            reply_markup=builder_reply(i18n.get("search-btn")),
        )
        return
    if user.status == UserStatus.WAITING:
        user.status = UserStatus.OFFLINE
        await uow.commit(user)
        await message.answer(
            text=i18n.get("stop-companion"), reply_markup=builder_reply(i18n.get("search-btn"))
        )
        return

    companion: Optional[DBUser] = await repository.user.get(user_id=user.companion)
    await message.answer(
        text=i18n.get("you-leave"), reply_markup=builder_reply(i18n.get("search-btn"))
    )
    await repository.user.update_companions(
        user=user,
        companion=companion,
        user_status=UserStatus.OFFLINE,
        companion_status=UserStatus.WAITING,
        is_stop=True,
    )
    await uow.commit(user, companion)
    await i18n.set_locale(locale=companion.locale, companion=companion)
    await bot.send_message(
        chat_id=companion.id,
        text=i18n.get("companion-leave"),
        reply_markup=builder_reply(i18n.get("stop-btn")),
    )
    await find_companion(bot, i18n, companion, repository, uow)


@router.message(or_f(Command("next"), F.text == LazyProxy("next-btn")), flags=flags)
async def next_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> None:
    """
    Handle the /next command.
    Next the companion.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    """
    if user.status == UserStatus.WAITING:
        await message.answer(
            text=i18n.get("looking-for-a-companion"),
            reply_markup=builder_reply(i18n.get("stop-btn")),
        )
        return
    if user.status == UserStatus.OFFLINE:
        await message.answer(
            text=i18n.get("search-not-started"),
            reply_markup=builder_reply(i18n.get("search-btn")),
        )
        return

    companion: Optional[DBUser] = await repository.user.get(user_id=user.companion)
    await message.answer(
        text=i18n.get("next-companion"), reply_markup=builder_reply(i18n.get("stop-btn"))
    )
    await repository.user.update_companions(
        user=user,
        companion=companion,
        user_status=UserStatus.WAITING,
        companion_status=UserStatus.WAITING,
        is_stop=True,
    )
    await uow.commit(user, companion)
    await i18n.set_locale(locale=companion.locale, companion=companion)
    await bot.send_message(
        chat_id=companion.id,
        text=i18n.get("companion-leave"),
        reply_markup=builder_reply(i18n.get("stop-btn")),
    )
    await i18n.set_locale(locale=user.locale, user=user)
    await asyncio.sleep(1)
    await find_companion(bot, i18n, user, repository, uow)


@router.message(Command("language"), flags=flags)
async def language_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /language command.
    Show the language selection keyboard.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(i18n.get("language", name=user.mention), reply_markup=select_language())


@router.message(Command("help"), flags=flags)
async def help_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /help command.
    Show the help message.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(
        text=i18n.get("help", name=user.mention), reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("link"), flags=flags)
async def link_command(message: Message, bot: Bot, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /link command.
    Send link to the companion.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    """
    if not user.companion:
        await message.answer(text=user.mention)
        return

    await bot.send_message(
        chat_id=user.companion,
        text=i18n.get("send-link"),
        reply_markup=link_profile(i18n=i18n, url=user.url),
    )
    await message.answer(text=i18n.get("companion-linked"), reply_markup=dialog(i18n=i18n))


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
    if user.balance <= 999:
        await message.answer(
            i18n.get("not-enough-balance", name=user.mention, balance=user.balance)
        )
        return

    user.balance -= 999
    chans: List[str] = [
        "https://imgur.com/a/suN3hTv",
        "https://imgur.com/a/lSwCP2O",
        "https://imgur.com/a/dNWN9Gq",
    ]
    chan_index: int = secrets.randbelow(len(chans))
    await uow.commit(user)
    await message.answer_photo(
        photo=chans[chan_index], caption=i18n.get("chans-info", chan=chan_index)
    )


@router.message(Command("profile"), flags=flags)
async def profile_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /profile command.
    Show the user's profile.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(
        text=i18n.get(
            "profile",
            name=user.mention,
            id=str(user.id),
            open="❌" if user.profile else "☑️",
            balance=user.balance,
            date=user.created_at,
        ),
        reply_markup=profile(i18n=i18n, profile=user.profile),
    )


@router.message(Command("top"), flags=flags)
async def top_command(
    message: Message, i18n: I18nContext, user: DBUser, repository: Repository
) -> None:
    """
    Handle the /top command.
    Show the top users.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    """
    users_stats: Dict[str, str | int] = await repository.user.stats(user=user)
    await message.answer(
        text=i18n.get("top", **users_stats),
        reply_markup=pagination_users(),
    )


@router.message(Command("dice"), flags={"throttling_key": "dice"})
async def dice_command(
    message: Message, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
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
        text=i18n.get("dice", number=dice.dice.value, balance=user.balance, position=position)
    )
