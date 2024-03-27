from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from aiogram_i18n import I18nContext

from ...enums import UserStatus
from ...keyboards import builder_reply, dialog
from ...services.database import DBUser

if TYPE_CHECKING:
    from ...services.database import Repository, UoW


class SearchCompanionMiddleware(BaseMiddleware):
    """
    The middleware for the companion search.
    """

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Optional[Any]:
        i18n: I18nContext = data["i18n"]
        repository: Repository = data["repository"]
        user: DBUser = data["user"]

        if user.status == UserStatus.ACTIVE:
            return event.answer(
                text=i18n.get("chat-with-companion"), reply_markup=dialog(i18n=i18n)
            )
        if user.status == UserStatus.WAITING:
            return event.answer(
                text=i18n.get("looking-for-a-companion"),
                reply_markup=builder_reply(i18n.get("stop-btn")),
            )

        uow: UoW = data["uow"]
        companion: Optional[DBUser] = await repository.user.get_random_companion(user_id=user.id)
        if companion:
            bot: Bot = data["bot"]
            await repository.user.update_companions(
                user=user,
                companion=companion,
                user_status=UserStatus.ACTIVE,
                companion_status=UserStatus.ACTIVE,
            )
            await event.answer(text=i18n.get("found-companion"), reply_markup=dialog(i18n=i18n))
            await i18n.set_locale(locale=companion.locale, companion=companion)
            await uow.commit(user)

            return await bot.send_message(
                chat_id=companion.id,
                text=i18n.get("found-companion"),
                reply_markup=dialog(i18n=i18n),
            )

        user.status = UserStatus.WAITING
        await uow.commit(user)
        return await handler(event, data)
