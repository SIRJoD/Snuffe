from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)

from keyboards.menu import (
    start_buttons,
    main_menu
)

from config import CHANNEL_ID
from database import add_user

import aiosqlite


router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message,
    command: CommandObject
):

    await add_user(
        message.from_user.id
    )

    # Reward system
    if command.args == "reward_24hr":

        db = await aiosqlite.connect(
            "data/snuffe.db"
        )

        await db.execute(
            """
            UPDATE users
            SET remaining_slots=
            remaining_slots+1
            WHERE user_id=?
            """,
            (
                message.from_user.id,
            )
        )

        cursor = await db.execute(
            """
            SELECT remaining_slots
            FROM users
            WHERE user_id=?
            """,
            (
                message.from_user.id,
            )
        )

        user = await cursor.fetchone()

        await db.commit()
        await db.close()

        slots = user[0]

        await message.answer(

            "🎉 <b>CONGRATULATIONS!</b>\n\n"

            "✅ Advertisement slot added\n\n"

            f"📦 Total Slots: {slots}\n\n"

            "🚀 You can now post advertisements."
        )


    await message.answer_photo(

        photo=FSInputFile(
            "images/snuffe.jpg"
        ),

        caption=
        "🔥 <b>Welcome to SNUFFe Marketplace</b>\n\n"

        "📢 Biggest marketplace for digital goods.\n\n"

        "🚀 Buy • Sell • Grow\n\n"

        "Join channel to continue.",

        reply_markup=start_buttons()
    )


@router.callback_query(
    lambda c:c.data=="joined"
)
async def joined_check(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    try:

        member = await callback.bot.get_chat_member(
            CHANNEL_ID,
            user_id
        )

        if member.status in [

            "member",
            "administrator",
            "creator"

        ]:

            await callback.message.edit_caption(

                caption=
                "✅ <b>Thanks for joining!</b>\n\n"

                "Select your option below.",

                reply_markup=main_menu()
            )

        else:

            await callback.answer(
                "❌ Join channel first",
                show_alert=True
            )

    except:

        await callback.answer(
            "❌ Join channel first",
            show_alert=True
        )


@router.callback_query(
    lambda c:c.data=="menu"
)
async def menu_button(
    callback: CallbackQuery
):

    await callback.message.edit_caption(

        caption=
        "🏠 <b>SNUFFe MAIN MENU</b>\n\n"

        "Choose an option below.",

        reply_markup=main_menu()
    )