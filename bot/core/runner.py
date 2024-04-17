from aiogram import Bot, Dispatcher


async def _polling_startup(bot: Bot) -> None:
    """
    Perform startup actions for the Telegram bot when using polling.

    :param bot: The instance of the Telegram bot.
    """
    await bot.delete_webhook(drop_pending_updates=True)


async def start_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    """
    Run the Telegram bot with long polling.

    :param dispatcher: The Dispatcher instance for the Telegram bot.
    :param bot: The instance of the Telegram bot.
    """
    dispatcher.startup.register(_polling_startup)
    await dispatcher.start_polling(bot)
