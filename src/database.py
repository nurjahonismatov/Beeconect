import aiosqlite
from pathlib import Path

# Ma'lumotlar bazasi fayli yo'li
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "database.db"

async def init_db():
    """Ma'lumotlar bazasi va foydalanuvchilar jadvalini yaratish"""
    # data papkasi mavjudligini tekshirish va yaratish
    DB_PATH.parent.mkdir(exist_ok=True)
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def add_user(telegram_id: int, username: str):
    """Yangi foydalanuvchini bazaga qo'shish"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)",
            (telegram_id, username)
        )
        await db.commit()

async def get_all_users():
    """Barcha foydalanuvchilar ID-larini olish (reklama uchun)"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT telegram_id FROM users") as cursor:
            rows = await cursor.fetchall()
            # aiosqlite tuple qaytargani uchun faqat birinchi elementni (id) olamiz
            return [row[0] for row in rows]
