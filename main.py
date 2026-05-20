from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

from config import BOT_TOKEN
from database import create_db
from scheduler import check_expired_ads

from handlers.start import router as start_router
from handlers.sell import router as sell_router
from handlers.buy import router as buy_router
from handlers.admin import router as admin_router


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


async def startup():

    await create_db()

    asyncio.create_task(
        check_expired_ads(bot)
    )

    print("Database connected")
    print("Scheduler started")
    print("Bot started")


async def main():

    await startup()

    dp.include_router(start_router)
    dp.include_router(sell_router)
    dp.include_router(buy_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())