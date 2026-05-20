from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from config import VPLINK_URL


def sell_menu(unlocked=False):

    if unlocked:

        return InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="📸 Instagram",
                        callback_data="instagram"
                    ),

                    InlineKeyboardButton(
                        text="📘 Facebook",
                        callback_data="facebook"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="▶️ YouTube",
                        callback_data="youtube"
                    ),

                    InlineKeyboardButton(
                        text="💬 Telegram",
                        callback_data="telegram"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="📱 WhatsApp",
                        callback_data="whatsapp"
                    ),

                    InlineKeyboardButton(
                        text="👻 Snapchat",
                        callback_data="snapchat"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🎵 TikTok",
                        callback_data="tiktok"
                    ),

                    InlineKeyboardButton(
                        text="🎮 Games",
                        callback_data="games"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🏠 Main Menu",
                        callback_data="menu"
                    )
                ]
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🚀 Unlock Access",
                    url=VPLINK_URL
                )
            ],

            [
                InlineKeyboardButton(
                    text="📘 Tutorial",
                    url="https://t.me/snuffeEcrow"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="menu"
                )
            ]
        ]
    )


def social_menu(platform):

    if platform == "games":

        return InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🎮 Game Account Details",
                        callback_data="game_details"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data="sell"
                    ),

                    InlineKeyboardButton(
                        text="🏠 Menu",
                        callback_data="menu"
                    )
                ]
            ]
        )

    elif platform == "whatsapp":

        return InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="📱 Virtual Number",
                        callback_data="virtual_number"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🛠 Service Provide",
                        callback_data="wa_service"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data="sell"
                    ),

                    InlineKeyboardButton(
                        text="🏠 Menu",
                        callback_data="menu"
                    )
                ]
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📱 Account Selling",
                    callback_data=f"{platform}_account"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🛠 Service Provide",
                    callback_data=f"{platform}_service"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="sell"
                ),

                InlineKeyboardButton(
                    text="🏠 Menu",
                    callback_data="menu"
                )
            ]
        ]
    )