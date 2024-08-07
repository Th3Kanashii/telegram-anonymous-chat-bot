from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault


if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram_i18n import I18nContext


async def _remove_commands(bot: Bot, chat_id: int | str | None = None) -> None:
    """
    Remove commands from the chat.

    :param bot: Bot instance.
    :param chat_id: Chat ID.
    """
    if not chat_id:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
        return

    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=chat_id))


async def set_default_commands(bot: Bot, i18n: I18nContext) -> None:
    """
    Set default commands for the bot.

    :param bot: Bot instance.
    :param i18n: I18nContext instance.
    """
    await _remove_commands(bot=bot)
    await bot.set_my_commands(
        commands=[
            BotCommand(command="language", description=i18n.get("command-language")),
            BotCommand(command="profile", description=i18n.get("command-profile")),
            BotCommand(command="link", description=i18n.get("command-link")),
            BotCommand(command="search", description=i18n.get("command-search")),
            BotCommand(command="next", description=i18n.get("command-next")),
            BotCommand(command="stop", description=i18n.get("command-stop")),
            BotCommand(command="chan", description=i18n.get("command-chan")),
            BotCommand(command="dice", description=i18n.get("command-dice")),
            BotCommand(command="top", description=i18n.get("command-top")),
        ],
        scope=BotCommandScopeDefault(),
    )


async def set_commands(bot: Bot, i18n: I18nContext, chat_id: int | str) -> None:
    """
    Set commands for chat

    :param bot: Bot instance
    :param i18n: I18nContext instance
    :param chat_id: Chat ID
    :return: True if the commands were set successfully
    """
    await _remove_commands(bot=bot, chat_id=chat_id)
    await bot.set_my_commands(
        commands=[
            BotCommand(command="language", description=i18n.get("command-language")),
            BotCommand(command="profile", description=i18n.get("command-profile")),
            BotCommand(command="link", description=i18n.get("command-link")),
            BotCommand(command="search", description=i18n.get("command-search")),
            BotCommand(command="next", description=i18n.get("command-next")),
            BotCommand(command="stop", description=i18n.get("command-stop")),
            BotCommand(command="chan", description=i18n.get("command-chan")),
            BotCommand(command="dice", description=i18n.get("command-dice")),
            BotCommand(command="top", description=i18n.get("command-top")),
        ],
        scope=BotCommandScopeChat(chat_id=chat_id),
    )
