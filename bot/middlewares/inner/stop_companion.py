from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, User
from aiogram_i18n import I18nContext

from ...enums import UserStatus
from ...keyboards import builder_reply
from ...services.database import DBUser

if TYPE_CHECKING:
    from ...services.database import Repository, UoW


class StopCompanionMiddleware(BaseMiddleware):
    """
    The middleware for stopping the companion search.
    """

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        repository: Repository = data["repository"]
        i18n: I18nContext = data["i18n"]
        uow: UoW = data["uow"]
        user: Optional[DBUser] = await repository.user.get(user_id=aiogram_user.id)

        if user.status == UserStatus.ACTIVE:
            bot: Bot = data["bot"]
            companion: Optional[DBUser] = await repository.user.get(user_id=user.companion)
            await event.answer(
                text=i18n.get("you-leave"), reply_markup=builder_reply(i18n.get("search-btn"))
            )
            await i18n.set_locale(locale=companion.locale, companion=companion)
            await repository.user.update_companions(
                user=user,
                companion=companion,
                user_status=UserStatus.OFFLINE,
                companion_status=UserStatus.WAITING,
                is_stop=True,
            )
            await uow.commit(user)

            return await bot.send_message(
                chat_id=companion.id,
                text=i18n.get("companion-leave"),
                reply_markup=builder_reply(i18n.get("stop-btn")),
            )

        if user.status == UserStatus.OFFLINE:
            return event.answer(
                text=i18n.get("search-not-started"),
                reply_markup=builder_reply(i18n.get("search-btn")),
            )

        user.status = UserStatus.OFFLINE
        await uow.commit(user)
        return await handler(event, data)
