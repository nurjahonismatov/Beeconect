import os
from aiohttp import web

# Render talab qiladigan soxta veb-sahifa funksiyasi
async def handle(request):
    return web.Response(text="Bot is running successfully!")

async def start_bot():
    # 1. Soxta veb-serverni sozlash (Render tinchlanishi uchun)
    app = web.Application()
    app.router.add_get('/', handle)
    
    # Render avtomat beradigan portni oladi (yoki defolt 10000)
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Fake server started on port {port}")

    # 2. Telegram botni odatdagidek Polling rejimida ishga tushirish
    # O'zingizning dp va bot o'zgaruvchilaringiz nomini tekshirib oling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
