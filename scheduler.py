import aiosqlite
from datetime import datetime
import asyncio


async def check_expired_ads(bot):

    while True:

        db = await aiosqlite.connect(
            "data/snuffe.db"
        )

        cursor = await db.execute(
            """
            SELECT
            id,
            user_id,
            expires_at

            FROM ads
            """
        )

        ads = await cursor.fetchall()

        for ad in ads:

            ad_id = ad[0]
            user_id = ad[1]

            expire = datetime.fromisoformat(
                ad[2]
            )

            if datetime.now() >= expire:

                await db.execute(
                    """
                    DELETE FROM ads
                    WHERE id=?
                    """,
                    (ad_id,)
                )

                try:

                    await bot.send_message(

                        chat_id=user_id,

                        text=
                        "⏰ <b>SNUFFe Notification</b>\n\n"
                        "❌ Your advertisement has expired.\n\n"
                        "🚀 Complete task again to unlock another advertisement slot.",

                        parse_mode="HTML"
                    )

                    print(
                        f"Notification sent to {user_id}"
                    )

                except Exception as e:

                    print(
                        f"Notification error: {e}"
                    )

        await db.commit()

        await db.close()

        await asyncio.sleep(
            60
        )