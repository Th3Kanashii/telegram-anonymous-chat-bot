from __future__ import annotations

from typing import TYPE_CHECKING, Final, Optional

from aiogram import Bot, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message, MessageReactionUpdated
from aiogram_i18n import I18nContext

from ...enums import UserStatus
from ...keyboards import builder_reply, dialog
from ...utils import find_companion

if TYPE_CHECKING:
    from ...services.database import DBUser, Repository, UoW

router: Final[Router] = Router(name=__name__)


@router.message(flags={"throttling_key": "chatting"})
async def chatting(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> None:
    """
    Process the chatting.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    """
    if not user.companion:
        await message.delete()
        return

    companion: Optional[DBUser] = await repository.user.get(user_id=user.companion)
    await i18n.set_locale(locale=companion.locale, companion=companion)

    try:
        await message.copy_to(chat_id=user.companion, reply_markup=dialog(i18n=i18n))
    except TelegramForbiddenError:
        await repository.user.update_companions(
            user=user,
            companion=companion,
            user_status=UserStatus.WAITING,
            companion_status=UserStatus.OFFLINE,
            is_stop=True,
        )
        await uow.commit(user, companion)
        await i18n.set_locale(locale=user.locale, user=user)
        await message.answer(text=i18n.get("block-companion"))
        await message.answer(
            text=i18n.get("next-companion"), reply_markup=builder_reply(i18n.get("stop-btn"))
        )
        await find_companion(bot, i18n, user, repository, uow)


@router.message_reaction()
async def chatting_reaction(message: MessageReactionUpdated, bot: Bot, user: DBUser) -> None:
    """
    Process the reaction to the chatting message.

    :param message: The message.
    :param bot: The bot.
    :param user: The user.
    """
    if not user.companion:
        return

    await bot.set_message_reaction(
        chat_id=user.companion,
        message_id=message.message_id - 1,
        reaction=message.new_reaction,
    )
