from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def buy_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📸 Instagram",
                    callback_data="buy_instagram"
                ),

                InlineKeyboardButton(
                    text="📘 Facebook",
                    callback_data="buy_facebook"
                )
            ],

            [
                InlineKeyboardButton(
                    text="▶️ YouTube",
                    callback_data="buy_youtube"
                ),

                InlineKeyboardButton(
                    text="💬 Telegram",
                    callback_data="buy_telegram"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📱 WhatsApp",
                    callback_data="buy_whatsapp"
                ),

                InlineKeyboardButton(
                    text="👻 Snapchat",
                    callback_data="buy_snapchat"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎵 TikTok",
                    callback_data="buy_tiktok"
                ),

                InlineKeyboardButton(
                    text="🎮 Games",
                    callback_data="buy_games"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏠 Menu",
                    callback_data="menu"
                )
            ]
        ]
    )


def buy_social_menu(platform):

    if platform == "whatsapp":

        return InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="📱 Virtual Number",
                        callback_data="virtual_number_buy"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🛠 Service Provide",
                        callback_data="wa_service_buy"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data="buy"
                    )
                ]
            ]
        )

    elif platform == "games":

        return InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🎮 Game Accounts",
                        callback_data="game_details_buy"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data="buy"
                    )
                ]
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📱 Account Selling",
                    callback_data=f"{platform}_account_buy"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🛠 Service Provide",
                    callback_data=f"{platform}_service_buy"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="buy"
                )
            ]
        ]
    )