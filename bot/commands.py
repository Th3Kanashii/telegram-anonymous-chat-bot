from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram_i18n import I18nContext


async def set_commands(bot: Bot, i18n: I18nContext, chat_id: int) -> bool:
    """
    Set commands for chat

    :param bot: Bot instance
    :param i18n: I18nContext instance
    :param chat_id: Chat ID
    :return: True if the commands were set successfully
    """
    return await bot.set_my_commands(
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
