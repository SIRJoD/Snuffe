from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from keyboards.sell import sell_menu, social_menu
from states import SellForm

import aiosqlite
from datetime import datetime, timedelta

router = Router()


PLATFORMS = {

    "instagram_account":
    "📸 <b>INSTAGRAM ACCOUNT SELLING</b>\n\n"
    "📝 <b>SEND DETAILS OF YOUR ADVERTISEMENT:</b>\n\n"
    "• Type of account\n"
    "• Username\n"
    "• Price\n"
    "• Old deal vouchers\n"
    "• Contact username",

    "instagram_service":
    "📸 <b>INSTAGRAM SERVICE</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Service detail\n"
    "• Price\n"
    "• Vouches\n"
    "• Contact username",

    "facebook_account":
    "📘 <b>FACEBOOK ACCOUNT SELLING</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Type\n"
    "• Username\n"
    "• Price\n"
    "• Vouches\n"
    "• Contact",

    "facebook_service":
    "📘 <b>FACEBOOK SERVICE</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Service\n"
    "• Price\n"
    "• Contact",

    "youtube_account":
    "▶️ <b>YOUTUBE ACCOUNT SELLING</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Channel name\n"
    "• Subscribers\n"
    "• Price\n"
    "• Contact",

    "youtube_service":
    "▶️ <b>YOUTUBE SERVICE</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Service\n"
    "• Price\n"
    "• Contact",

    "telegram_account":
    "💬 <b>TELEGRAM ACCOUNT</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Username\n"
    "• Price\n"
    "• Contact",

    "telegram_service":
    "💬 <b>TELEGRAM SERVICE</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Service\n"
    "• Price\n"
    "• Contact",

    "tiktok_account":
    "🎵 <b>TIKTOK ACCOUNT</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Username\n"
    "• Followers\n"
    "• Price\n"
    "• Contact",

    "tiktok_service":
    "🎵 <b>TIKTOK SERVICE</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Service\n"
    "• Price\n"
    "• Contact",

    "snapchat_account":
    "👻 <b>SNAPCHAT ACCOUNT</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Username\n"
    "• Price\n"
    "• Contact",

    "snapchat_service":
    "👻 <b>SNAPCHAT SERVICE</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Service\n"
    "• Price\n"
    "• Contact",

    "virtual_number":
    "📱 <b>WHATSAPP VIRTUAL NUMBER</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Country\n"
    "• Price\n"
    "• Contact",

    "wa_service":
    "📱 <b>WHATSAPP SERVICE</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Service\n"
    "• Price\n"
    "• Contact",

    "game_details":
    "🎮 <b>GAME ACCOUNT</b>\n\n"
    "📝 <b>SEND DETAILS:</b>\n\n"
    "• Game\n"
    "• Account details\n"
    "• Price\n"
    "• Contact"
}


@router.callback_query(
    lambda c:c.data=="sell"
)
async def sell_section(
    callback: CallbackQuery
):

    db = await aiosqlite.connect(
        "data/snuffe.db"
    )

    cursor = await db.execute(
        """
        SELECT remaining_slots
        FROM users
        WHERE user_id=?
        """,
        (callback.from_user.id,)
    )

    user = await cursor.fetchone()

    await db.close()

    slots = 0

    if user:
        slots = user[0]

    if slots <= 0:

        await callback.message.edit_caption(

            caption=
            "🚫 <b>No Advertisement Slots</b>\n\n"
            "Complete task again to unlock another advertisement slot.",

            reply_markup=sell_menu(
                unlocked=False
            )
        )

        return

    await callback.message.edit_caption(

        caption=
        f"🚀 <b>SNUFFe SELL HUB</b>\n\n"
        f"📦 Available Slots: {slots}\n\n"
        "Choose category below",

        reply_markup=sell_menu(
            unlocked=True
        )
    )


@router.callback_query(
lambda c:c.data in [
"instagram","facebook",
"youtube","telegram",
"whatsapp","snapchat",
"tiktok","games"
])
async def social_section(
callback:CallbackQuery
):

    await callback.message.edit_caption(
        caption=
        f"🚀 <b>{callback.data.upper()} HUB</b>",

        reply_markup=social_menu(
            callback.data
        )
    )


@router.callback_query(
lambda c:c.data in PLATFORMS
)
async def ad_form(
callback:CallbackQuery,
state:FSMContext
):

    await state.set_state(
        SellForm.waiting_for_details
    )

    await state.update_data(
        category=callback.data
    )

    await callback.message.edit_caption(
        caption=PLATFORMS[
            callback.data
        ]
    )


@router.message(
SellForm.waiting_for_details
)
async def get_details(
message:Message,
state:FSMContext
):

    await state.update_data(
        ad_text=message.text
    )

    data=await state.get_data()

    keyboard=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Confirm",
                    callback_data="confirm_ad"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data="cancel_ad"
                )
            ]
        ]
    )

    await message.answer(
        "📋 <b>ADVERTISEMENT PREVIEW</b>\n\n"
        f"{data['ad_text']}\n\n"
        "Post this advertisement?",
        reply_markup=keyboard
    )


@router.callback_query(
lambda c:c.data=="confirm_ad"
)
async def confirm_ad(
callback:CallbackQuery,
state:FSMContext
):

    data = await state.get_data()

    expire = (
        datetime.now() +
        timedelta(hours=24)
    )

    db = await aiosqlite.connect(
        "data/snuffe.db"
    )

    await db.execute(
        """
        INSERT INTO ads
        (
        user_id,
        category,
        ad_text,
        expires_at
        )
        VALUES
        (?,?,?,?)
        """,
        (
            callback.from_user.id,
            data["category"],
            data["ad_text"],
            str(expire)
        )
    )

    await db.execute(
        """
        UPDATE users
        SET remaining_slots=
        remaining_slots-1
        WHERE user_id=?
        """,
        (callback.from_user.id,)
    )

    await db.commit()
    await db.close()

    await callback.message.edit_text(
        "🎉 <b>ADVERTISEMENT POSTED</b>\n\n"
        "✅ Advertisement live\n"
        "📦 Slot consumed: -1\n"
        "⏰ Valid for 24h"
    )

    await state.clear()


@router.callback_query(
lambda c:c.data=="cancel_ad"
)
async def cancel_ad(
callback:CallbackQuery,
state:FSMContext
):

    await state.clear()

    await callback.message.edit_text(
        "❌ Advertisement cancelled"
    )