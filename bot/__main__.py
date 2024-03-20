import asyncio

from aiogram import Bot, Dispatcher

from .config import Config
from .core import create_bot, create_dispatcher, run_polling


async def main() -> None:
    config: Config = Config()
    dispatcher: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    return await run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    asyncio.run(main())
