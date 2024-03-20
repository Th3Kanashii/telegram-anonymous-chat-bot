from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, User
from aiogram_i18n import I18nContext

from ...enums import UserStatus
from ...keyboards import builder_reply, dialog
from ...services.database import DBUser

if TYPE_CHECKING:
    from ...services.database import Repository, UoW


class NextCompanionMiddleware(BaseMiddleware):
    """
    Middleware for finding a new companion.
    """

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        bot: Bot = data["bot"]
        repository: Repository = data["repository"]
        i18n: I18nContext = data["i18n"]
        user: Optional[DBUser] = await repository.user.get(user_id=aiogram_user.id)

        if user.status == UserStatus.ACTIVE:
            companion: Optional[DBUser] = await repository.user.get(user_id=user.companion)

            await i18n.set_locale(locale=companion.locale, companion=companion)
            await bot.send_message(
                chat_id=companion.id,
                text=i18n.get("companion-leave"),
                reply_markup=builder_reply(i18n.get("stop-btn")),
            )
            await repository.user.update_companions(
                user=user,
                companion=companion,
                user_status=UserStatus.WAITING,
                companion_status=UserStatus.WAITING,
                is_stop=True,
            )

            uow: UoW = data["uow"]
            new_companion: Optional[DBUser] = await repository.user.get_random_companion(
                user_id=user.id
            )
            if new_companion:
                await i18n.set_locale(locale=new_companion.locale, companion=new_companion)
                await repository.user.update_companions(
                    user=user,
                    companion=new_companion,
                    user_status=UserStatus.ACTIVE,
                    companion_status=UserStatus.ACTIVE,
                )
                await bot.send_message(
                    chat_id=new_companion.id,
                    text=i18n.get("found-companion"),
                    reply_markup=dialog(i18n=i18n),
                )
                await i18n.set_locale(locale=user.locale)
                await uow.commit(user)

                return event.answer(
                    text=i18n.get("found-companion"), reply_markup=dialog(i18n=i18n)
                )

            await uow.commit(user)
            return await handler(event, data)

        if user.status == UserStatus.WAITING:
            return event.answer(
                text=i18n.get("looking-for-a-companion"),
                reply_markup=builder_reply(i18n.get("stop-btn")),
            )

        return event.answer(
            text=i18n.get("search-not-started"),
            reply_markup=builder_reply(i18n.get("search-btn")),
        )
