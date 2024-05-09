from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Final, Optional

from aiogram import Bot, F, Router
from aiogram.filters import Command, or_f
from aiogram.types import Message, MessageReactionUpdated
from aiogram_i18n import I18nContext, LazyProxy

from ..enums import UserStatus
from ..keyboards import builder_reply, dialog

if TYPE_CHECKING:
    from ..services.database import DBUser, Repository, UoW

flags: Final[Dict[str, str]] = {"throttling_key": "default"}
chatting_router: Final[Router] = Router(name=__name__)


@chatting_router.message(or_f(Command("search"), F.text == LazyProxy("search-btn")), flags=flags)
async def search_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> Any:
    """
    Handle the /search command.
    Search for a companion.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    :return: The response.
    """
    if user.status == UserStatus.ACTIVE:
        return message.answer(text=i18n.get("chat-with-companion"), reply_markup=dialog(i18n=i18n))
    if user.status == UserStatus.WAITING:
        return message.answer(
            text=i18n.get("looking-for-a-companion"),
            reply_markup=builder_reply(i18n.get("stop-btn")),
        )
    companion: Optional[DBUser] = await repository.user.get_random_companion(user_id=user.id)
    if companion:
        await repository.user.update_companions(
            user=user,
            companion=companion,
            user_status=UserStatus.ACTIVE,
            companion_status=UserStatus.ACTIVE,
        )
        await message.answer(text=i18n.get("found-companion"), reply_markup=dialog(i18n=i18n))
        await i18n.set_locale(locale=companion.locale, companion=companion)
        await uow.commit(user)

        return await bot.send_message(
            chat_id=companion.id,
            text=i18n.get("found-companion"),
            reply_markup=dialog(i18n=i18n),
        )

    user.status = UserStatus.WAITING
    await uow.commit(user)
    await message.answer_sticker(
        sticker="CAACAgQAAxkBAAEL8KhmIDlSgGRsYYZdHgeYeCa9WRmeHgACeg8AAiD2UgyxLSQwkJOmejQE"
    )
    return message.answer(
        text=i18n.get("search-companion"),
        reply_markup=builder_reply(i18n.get("stop-btn")),
    )


@chatting_router.message(
    or_f(Command("stop"), F.text.in_([LazyProxy("stop-btn"), LazyProxy("cancel-btn")])),
    flags=flags,
)
async def stop_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> Any:
    """
    Handle the /stop command.
    Stop the companion search.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    :return: The response.
    """
    if user.status == UserStatus.ACTIVE:
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
        await i18n.set_locale(locale=companion.locale, companion=companion)
        await uow.commit(user)

        return await bot.send_message(
            chat_id=companion.id,
            text=i18n.get("companion-leave"),
            reply_markup=builder_reply(i18n.get("stop-btn")),
        )

    if user.status == UserStatus.OFFLINE:
        return message.answer(
            text=i18n.get("search-not-started"),
            reply_markup=builder_reply(i18n.get("search-btn")),
        )

    user.status = UserStatus.OFFLINE
    await uow.commit(user)
    return message.answer(
        text=i18n.get("stop-companion"), reply_markup=builder_reply(i18n.get("search-btn"))
    )


@chatting_router.message(or_f(Command("next"), F.text == LazyProxy("next-btn")), flags=flags)
async def next_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> Any:
    """
    Handle the /next command.
    Next the companion.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    :return: The response.
    """
    if user.status == UserStatus.ACTIVE:
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
        await i18n.set_locale(locale=companion.locale, companion=companion)
        await uow.commit(user)

        return await bot.send_message(
            chat_id=companion.id,
            text=i18n.get("companion-leave"),
            reply_markup=builder_reply(i18n.get("stop-btn")),
        )

    if user.status == UserStatus.WAITING:
        return message.answer(
            text=i18n.get("looking-for-a-companion"),
            reply_markup=builder_reply(i18n.get("stop-btn")),
        )

    return message.answer(
        text=i18n.get("search-not-started"),
        reply_markup=builder_reply(i18n.get("search-btn")),
    )


@chatting_router.message(flags={"throttling_key": "chatting"})
async def chatting(
    message: Message, i18n: I18nContext, user: DBUser, repository: Repository
) -> Any:
    """
    Process the chatting.

    :param message: The message.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :return: The response.
    """
    if user.companion:
        companion: Optional[DBUser] = await repository.user.get(user_id=user.companion)
        await i18n.set_locale(locale=companion.locale, companion=companion)
        return message.copy_to(chat_id=user.companion, reply_markup=dialog(i18n=i18n))
    return message.delete()


@chatting_router.message_reaction()
async def chatting_reaction(message: MessageReactionUpdated, bot: Bot, user: DBUser) -> Any:
    """
    Process the reaction to the chatting message.

    :param message: The message.
    :param bot: The bot.
    :param user: The user.
    :return: The response.
    """
    if user.companion:
        return await bot.set_message_reaction(
            chat_id=user.companion,
            message_id=message.message_id - 1,
            reaction=message.new_reaction,
        )
    return None
