import asyncio
import os
from bot.handlers import router
from aiogram import Bot, Dispatcher
import logging
from dotenv import load_dotenv


load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
