import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Qolgan importlar shundan keyin davom etadi...
import asyncio
from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN
...



import asyncio
import sys
from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN
from src.database import init_db
from src.handlers import commands, downloader

async def main():
    # Ma'lumotlar bazasini yaratish va tekshirish
    print("🗄 Ma'lumotlar bazasi ishga tushirilmoqda...")
    await init_db()

    # Bot va Dispatcher-ni sozlash
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni (handlers) ro'yxatdan o'tkazish
    dp.include_router(commands.router)
    dp.include_router(downloader.router)

    print("🚀 Bot muvaffaqiyatli ishga tushdi!")
    
    # Botni yangi xabarlarni eshitish rejimiga o'tkazish
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Windows-da asinxron yuklashlar xato bermasligi uchun
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())

