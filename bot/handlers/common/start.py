from __future__ import annotations

from typing import TYPE_CHECKING, Final, Optional

from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from ...keyboards import builder_reply
from ...ui_commands import set_commands

if TYPE_CHECKING:
    from ...services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart(), flags={"throttling_key": "default"})
async def start_command(
    message: Message, bot: Bot, i18n: I18nContext, user: DBUser, commands: Optional[bool] = False
) -> None:
    """
    Handle the /start command.

    :param message: The message.
    :param bot: The bot.
    :param i18n: The i18n context.
    :param user: The user.
    :param commands: Whether to set the commands.
    """
    if commands:
        await set_commands(bot=bot, i18n=i18n, chat_id=user.id)

    await message.answer_photo(
        photo="https://imgur.com/a/GwWoUQO",
        caption=i18n.get("welcome", name=user.mention),
        reply_markup=builder_reply(i18n.get("search-btn")),
    )
