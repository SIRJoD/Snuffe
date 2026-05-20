from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

from keyboards.buyer import (
    buy_menu,
    buy_social_menu
)

import aiosqlite
from datetime import datetime
import re

router = Router()

user_pages = {}


@router.callback_query(
    lambda c: c.data == "buy"
)
async def buy_intro(
    callback: CallbackQuery
):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Continue",
                    callback_data="buy_continue"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👑 Middleman ID",
                    url="https://t.me/SnuffeMM"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🚫 Banning Course",
                    url="https://t.me/+VpTsiyC93M84NmY1"
                )
            ]
        ]
    )

    photo = FSInputFile(
        "images/buy.jpg"
    )

    await callback.message.delete()

    await callback.message.answer_photo(

        photo=photo,

        caption=
        "🔥 <b>WELCOME TO SNUFFe MARKETPLACE</b>\n\n"

        "💎 Biggest marketplace for digital products\n"
        "🚀 Buy and sell safely\n"
        "📈 Multiple categories available\n"
        "🤝 Trusted community marketplace\n\n"

        "⚠️ <b>IMPORTANT WARNING</b>\n\n"

        "❗ <b>DO NOT DEAL WITH ANYONE "
        "WITHOUT OUR MIDDLEMAN</b>\n\n"

        "❗ <b>ELSE IT IS NOT OUR "
        "RESPONSIBILITY</b>",

        reply_markup=keyboard
    )


@router.callback_query(
    lambda c: c.data == "buy_continue"
)
async def buy_section(
    callback: CallbackQuery
):

    await callback.message.edit_caption(

        caption=
        "🛒 <b>WELCOME TO BUY HUB</b>\n\n"

        "Choose your social media below.",

        reply_markup=buy_menu()
    )


@router.callback_query(
    lambda c: c.data.startswith("buy_")
    and not c.data.endswith("_buy")
)
async def buy_social(
    callback: CallbackQuery
):

    platform = callback.data.replace(
        "buy_",
        ""
    )

    await callback.message.edit_caption(

        caption=
        f"🛒 <b>{platform.upper()} BUY HUB</b>\n\n"

        "Choose option below",

        reply_markup=buy_social_menu(
            platform
        )
    )


@router.callback_query(
    lambda c: c.data.endswith("_buy")
)
async def show_ads(
    callback: CallbackQuery
):

    category = callback.data.replace(
        "_buy",
        ""
    )

    db = await aiosqlite.connect(
        "data/snuffe.db"
    )

    cursor = await db.execute(
        """
        SELECT
        id,
        ad_text,
        expires_at

        FROM ads

        WHERE category=?
        """,
        (category,)
    )

    ads = await cursor.fetchall()

    await db.close()

    active = []

    for ad in ads:

        expire = datetime.fromisoformat(
            ad[2]
        )

        if datetime.now() < expire:

            active.append(ad)

    if not active:

        await callback.message.edit_caption(

            caption=
            "❌ No active ads found"
        )

        return


    user_pages[
        callback.from_user.id
    ] = {

        "category": category,
        "index": 0,
        "ads": active
    }

    await display_ad(
        callback
    )


async def display_ad(
    callback
):

    data = user_pages[
        callback.from_user.id
    ]

    ad = data["ads"][
        data["index"]
    ]

    ad_text = ad[1]

    username = None

    match = re.search(
        r'@\w+',
        ad_text
    )

    if match:

        username = match.group()

        username = username.replace(
            "@",
            ""
        )


    buttons=[]


    if username:

        buttons.append(

            [

                InlineKeyboardButton(
                    text="📩 Contact Seller",
                    url=f"https://t.me/{username}"
                )
            ]
        )


    buttons.append(

        [

            InlineKeyboardButton(
                text="⬅ Previous",
                callback_data="prev_ad"
            ),

            InlineKeyboardButton(
                text="Next ➡",
                callback_data="next_ad"
            )
        ]
    )

    buttons.append(

        [

            InlineKeyboardButton(
                text="🏠 Menu",
                callback_data="menu"
            )
        ]
    )


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.edit_caption(

        caption=

        f"🛒 <b>ADVERTISEMENT "
        f"{data['index']+1}/"
        f"{len(data['ads'])}</b>\n\n"

        f"{ad_text}",

        reply_markup=keyboard
    )


@router.callback_query(
    lambda c: c.data == "next_ad"
)
async def next_ad(
    callback: CallbackQuery
):

    data=user_pages[
        callback.from_user.id
    ]

    if data["index"]<len(
        data["ads"]
    )-1:

        data["index"]+=1

    await display_ad(
        callback
    )


@router.callback_query(
    lambda c: c.data == "prev_ad"
)
async def prev_ad(
    callback: CallbackQuery
):

    data=user_pages[
        callback.from_user.id
    ]

    if data["index"]>0:

        data["index"]-=1

    await display_ad(
        callback
    )