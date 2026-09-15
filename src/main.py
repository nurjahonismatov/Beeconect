import os
import asyncio
from aiohttp import web

# 1. Loyihangiz ichidagi haqiqiy bot va dp (dispatcher) o'zgaruvchilarini import qilamiz.
# (Agar sizda ular boshqa faylda bo'lsa, o'sha fayl nomini yozing, masalan: from src.bot_config import bot, dp)
from src.main import bot, dp  

# Render talab qiladigan soxta veb-sahifa funksiyasi
async def handle(request):
    return web.Response(text="Bot is running successfully!")

async def start_bot():
    # Soxta veb-serverni sozlash (Render xursand bo'lishi uchun)
    app = web.Application()
    app.router.add_get('/', handle)
    
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Fake server started on port {port}")

    # Telegram botni Polling rejimida ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
