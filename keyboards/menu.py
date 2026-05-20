from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_buttons():

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📢 Join Channel",
                    url="https://t.me/SnuffeUpdate"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✅ I've Joined",
                    callback_data="joined"
                )
            ]
        ]
    )

    return keyboard


def main_menu():

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🛒 Buy",
                    callback_data="buy"
                ),

                InlineKeyboardButton(
                    text="💰 Sell",
                    callback_data="sell"
                )
            ]
        ]
    )

    return keyboard