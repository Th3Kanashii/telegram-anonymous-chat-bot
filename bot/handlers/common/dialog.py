from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Final

from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram_i18n import LazyProxy

from bot.enums import UserStatus
from bot.keyboards.inline import link_profile
from bot.keyboards.reply import builder_reply, dialog
from bot.utils import find_companion


if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser, Repository, UoW

flags: Final[dict[str, str]] = {"throttling_key": "default"}
router: Final[Router] = Router(name=__name__)


@router.message(or_f(Command("search"), F.text == LazyProxy("search-btn")), flags=flags)
async def search_command(
    message: Message,
    bot: Bot,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
    uow: UoW,
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
        sticker="CAACAgQAAxkBAAEL8KhmIDlSgGRsYYZdHgeYeCa9WRmeHgACeg8AAiD2UgyxLSQwkJOmejQE",
    )
    await message.answer(
        text=i18n.get("search-companion"),
        reply_markup=builder_reply(i18n.get("stop-btn")),
    )


@router.message(
    or_f(Command("stop"), F.text.in_([LazyProxy("stop-btn"), LazyProxy("cancel-btn")])),
    flags=flags,
)
async def stop_command(
    message: Message,
    bot: Bot,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
    uow: UoW,
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
            text=i18n.get("stop-companion"),
            reply_markup=builder_reply(i18n.get("search-btn")),
        )
        return

    companion: DBUser | None = await repository.user.get(user_id=user.companion)
    await message.answer(
        text=i18n.get("you-leave"),
        reply_markup=builder_reply(i18n.get("search-btn")),
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
    message: Message,
    bot: Bot,
    i18n: I18nContext,
    user: DBUser,
    repository: Repository,
    uow: UoW,
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

    companion: DBUser | None = await repository.user.get(user_id=user.companion)
    await message.answer(
        text=i18n.get("next-companion"),
        reply_markup=builder_reply(i18n.get("stop-btn")),
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
