import aiosqlite


async def create_db():

    db = await aiosqlite.connect(
        "data/snuffe.db"
    )

    await db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        ad_access_until TEXT,
        remaining_slots INTEGER DEFAULT 0,
        banned INTEGER DEFAULT 0
    )
    """)

    await db.execute("""
    CREATE TABLE IF NOT EXISTS ads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        ad_text TEXT,
        expires_at TEXT
    )
    """)

    await db.commit()
    await db.close()


async def get_user(user_id):

    db = await aiosqlite.connect(
        "data/snuffe.db"
    )

    cursor = await db.execute(
        """
        SELECT *
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    user = await cursor.fetchone()

    await db.close()

    return user


async def add_user(user_id):

    db = await aiosqlite.connect(
        "data/snuffe.db"
    )

    await db.execute(
        """
        INSERT OR IGNORE INTO users
        (
            user_id,
            remaining_slots,
            banned
        )
        VALUES
        (?,0,0)
        """,
        (user_id,)
    )

    await db.commit()
    await db.close()