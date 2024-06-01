from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from aiogram import Bot
from aiogram_i18n import I18nContext

from ..enums import UserStatus
from ..keyboards import dialog

if TYPE_CHECKING:
    from ..services.database import DBUser, Repository, UoW


async def find_companion(
    bot: Bot, i18n: I18nContext, user: DBUser, repository: Repository, uow: UoW
) -> bool:
    """
    Find and notify a companion.

    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param repository: The repository.
    :param uow: The unit of work.
    :return: True if a companion was found, False otherwise.
    """
    found_companion: Optional[DBUser] = await repository.user.get_random_companion(user_id=user.id)
    if found_companion:
        await repository.user.update_companions(
            user=user,
            companion=found_companion,
            user_status=UserStatus.ACTIVE,
            companion_status=UserStatus.ACTIVE,
        )
        await uow.commit(user, found_companion)
        await bot.send_message(
            chat_id=found_companion.companion,
            text=i18n.get("found-companion"),
            reply_markup=dialog(i18n=i18n),
        )
        await i18n.set_locale(locale=found_companion.locale, companion=found_companion)
        await bot.send_message(
            chat_id=found_companion.id,
            text=i18n.get("found-companion"),
            reply_markup=dialog(i18n=i18n),
        )
        return True
    return False
