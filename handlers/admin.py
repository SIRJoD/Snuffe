from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
import aiosqlite

router = Router()


class BroadcastState(
    StatesGroup
):
    waiting_message = State()


class BanState(
    StatesGroup
):
    waiting_ban = State()

    waiting_unban = State()


@router.message(
    Command("admin")
)
async def admin_panel(
    message: Message
):

    if message.from_user.id != ADMIN_ID:

        await message.answer(
            "❌ You are not authorized."
        )

        return


    db = await aiosqlite.connect(
        "data/snuffe.db"
    )

    users_cursor = await db.execute(
        "SELECT COUNT(*) FROM users"
    )

    ads_cursor = await db.execute(
        "SELECT COUNT(*) FROM ads"
    )

    total_users = (
        await users_cursor.fetchone()
    )[0]

    total_ads = (
        await ads_cursor.fetchone()
    )[0]

    await db.close()


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📢 Broadcast",
                    callback_data="broadcast"
                )
            ],

            [

                InlineKeyboardButton(
                    text="🚫 Ban User",
                    callback_data="ban_user"
                ),

                InlineKeyboardButton(
                    text="✅ Unban",
                    callback_data="unban_user"
                )
            ]
        ]
    )

    await message.answer(

        "👑 <b>SNUFFe ADMIN PANEL</b>\n\n"

        f"👥 Total Users: {total_users}\n"
        f"📦 Active Ads: {total_ads}\n\n"

        "Choose option below.",

        reply_markup=keyboard
    )


@router.callback_query(
    lambda c:c.data=="broadcast"
)
async def start_broadcast(
    callback:CallbackQuery,
    state:FSMContext
):

    await state.set_state(
        BroadcastState.waiting_message
    )

    await callback.message.answer(
        "📢 Send broadcast message"
    )


@router.message(
BroadcastState.waiting_message
)
async def send_broadcast(
message:Message,
state:FSMContext
):

    db=await aiosqlite.connect(
        "data/snuffe.db"
    )

    cursor=await db.execute(
        "SELECT user_id FROM users"
    )

    users=await cursor.fetchall()

    await db.close()

    success=0

    for user in users:

        try:

            await message.bot.send_message(
                user[0],
                message.text
            )

            success+=1

        except:
            pass


    await message.answer(

        f"✅ Sent to {success} users"
    )

    await state.clear()


@router.callback_query(
lambda c:c.data=="ban_user"
)
async def ban_start(
callback:CallbackQuery,
state:FSMContext
):

    await state.set_state(
        BanState.waiting_ban
    )

    await callback.message.answer(

        "🚫 Send user ID to ban"
    )


@router.message(
BanState.waiting_ban
)
async def ban_user(
message:Message,
state:FSMContext
):

    user_id=int(
        message.text
    )

    db=await aiosqlite.connect(
        "data/snuffe.db"
    )

    await db.execute(

        """
        ALTER TABLE users
        ADD COLUMN banned INTEGER DEFAULT 0
        """

    )

    try:
        pass
    except:
        pass


    await db.execute(

        """
        UPDATE users
        SET banned=1
        WHERE user_id=?
        """,

        (user_id,)
    )

    await db.commit()
    await db.close()

    await message.answer(
        f"🚫 User {user_id} banned"
    )

    await state.clear()


@router.callback_query(
lambda c:c.data=="unban_user"
)
async def unban_start(
callback:CallbackQuery,
state:FSMContext
):

    await state.set_state(
        BanState.waiting_unban
    )

    await callback.message.answer(

        "✅ Send user ID to unban"
    )


@router.message(
BanState.waiting_unban
)
async def unban_user(
message:Message,
state:FSMContext
):

    user_id=int(
        message.text
    )

    db=await aiosqlite.connect(
        "data/snuffe.db"
    )

    await db.execute(

        """
        UPDATE users
        SET banned=0
        WHERE user_id=?
        """,

        (user_id,)
    )

    await db.commit()
    await db.close()

    await message.answer(
        f"✅ User {user_id} unbanned"
    )

    await state.clear()