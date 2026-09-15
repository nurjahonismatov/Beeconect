import os
import sys
import asyncio
from aiohttp import web

# Loyihaning asosiy papkasini Python qidiruv yo'liga qo'shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from src.database import add_user  # Bazaga qo'shish funksiyasi
import os
import sys
import asyncio
from aiohttp import web
from dotenv import load_dotenv  # <-- 1. BU QATORNI QO'SHING

# .env fayli ichidagi o'zgaruvchilarni tizim xotirasiga yuklaydi
load_dotenv()  # <-- 2. BU QATORNI HAM QO'SHING

# Loyihaning asosiy papkasini Python qidiruv yo'liga qo'shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from src.database import add_user 

# 3. Endi bu qator ham kompyuteringizda, ham Renderda 100% xatosiz ishlaydi:
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# 1. Bot va Dispatcher-ni yaratish
# Tokenni Render xavfsiz xotirasidan (Environment Variables) o'qiydi
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Foydalanuvchilar tilini vaqtinchalik saqlash
user_languages = {}

# 🌍 3 tildagi barcha matnlar lug'ati
TEXTS = {
    'uz': {
        'settings_menu': "⚙️ <b>Sozlamalar bo'limi</b>\n\nBot tilini o'zgartirish uchun quyidagi tugmalardan birini tanlang:",
        'lang_changed': "✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>\nEndi bot sizga o'zbek tilida xizmat ko'rsatadi.",
        'need_lang': "⚠️ Iltimos, oldin pastdagi tugmalardan tilni tanlang!",
        'help': """🤖 <b>Botdan qanday foydalanish kerak?</b>\nMenga Instagram’dan biron bir video, rasm yoki Reels ssilkasini yuboring. Men uni sizga yuklab beraman.\n\n📌 <b>Imkoniyatlar:</b>\n• Reels, Post, Stories va Carousel yuklash.\n\n⚙️ <b>Buyruqlar:</b>\n/start — Qayta ishga tushirish\n/help — Yordam oynasi\n/settings — Tilni o'zgartirish\n/restart — Yangilash""",
        'start': """👑 <b>Assalomu alaykum, {name}!</b>\n\nInstagram’dan media fayllarni reklamasiz va kutishlarsiz yuklab beruvchi botga xush kelibsiz! ✨\n\n📥 <b>Qanday ishlatiladi?</b>\nInstagram ilovasidan olingan havolani (linkni) ushbu chatga yuboring, xolos."""
    },
    'ru': {
        'settings_menu': "⚙️ <b>Раздел настроек</b>\n\nЧтобы изменить язык бота, выберите один из вариантов ниже:",
        'lang_changed': "✅ <b>Язык успешно изменен!</b>\nТеперь бот будет отвечать вам на русском языке.",
        'need_lang': "⚠️ Пожалуйста, сначала выберите язык, нажав на кнопку ниже!",
        'help': """🤖 <b>Как пользоваться ботом?</b>\nОтправьте мне ссылку на любое видео, фото или Reels из Instagram. Я скачаю и отправлю его вам.\n\n📌 <b>Возможности:</b>\n• Скачивание Reels, Постов, Историй и Каруселей.\n\n⚙️ <b>Команды:</b>\n/start — Перезапустить\n/help — Помощь\n/settings — Изменить язык\n/restart — Обновить модули""",
        'start': """👑 <b>Здравствуйте, {name}!</b>\n\nДобро пожаловать в бот, который скачивает медиафайлы из Instagram без рекламы и ожиданий! ✨\n\n📥 <b>Как использовать?</b>\nПросто отправьте ссылку, скопированную из приложения Instagram, в этот чат."""
    },
    'en': {
        'settings_menu': "⚙️ <b>Settings Menu</b>\n\nTo change the bot language, please select one of the options below:",
        'lang_changed': "✅ <b>Language successfully changed!</b>\nNow the bot will serve you in English.",
        'need_lang': "⚠️ Please select a language from the buttons below first!",
        'help': """🤖 <b>How to use the bot?</b>\nSend me any video, photo, or Reels link from Instagram. I will download and send it to you.\n\n📌 <b>Features:</b>\n• Download Reels, Posts, Stories, and Carousels.\n\n⚙️ <b>Commands:</b>\n/start — Restart\n/help — Help menu\n/settings — Change language\n/restart — Refresh functions""",
        'start': """👑 <b>Hello, {name}!</b>\n\nWelcome to the bot that downloads media files from Instagram without ads or waiting! ✨\n\n📥 <b>How to use?</b>\nJust send the link copied from the Instagram app to this chat."""
    }
}

def get_lang_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data="lang_uz")],
            [InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru")],
            [InlineKeyboardButton(text="English 🇬🇧", callback_data="lang_en")]
        ]
    )

@router.message(Command("start"))
async def start_command(message: Message):
    try:
        await add_user(message.from_user.id, message.from_user.username)
    except Exception as e:
        print(f"Bazaga qo'shishda xatolik: {e}")
        
    clear_msg = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await clear_msg.delete()

    await message.answer(
        text="🌐 Tilni tanlang / Выберите язык / Select language:",
        reply_markup=get_lang_inline_keyboard()
    )

@router.callback_query(F.data.startswith("lang_"))
async def set_language_callback(callback: CallbackQuery):
    selected_lang = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user_languages[user_id] = selected_lang
    
    await callback.answer()
    await callback.message.delete()
    
    start_text = TEXTS[selected_lang]['start'].format(name=callback.from_user.full_name)
    await callback.message.answer(text=start_text, parse_mode="HTML")

@router.message(Command("settings"))
async def settings_command(message: Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, 'uz')
    await message.answer(text=TEXTS[lang]['settings_menu'], parse_mode="HTML", reply_markup=get_lang_inline_keyboard())

@router.message(Command("help"))
async def help_command(message: Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id)
    if not lang:
        await message.answer(TEXTS['uz']['need_lang'], reply_markup=get_lang_inline_keyboard())
        return
    await message.answer(TEXTS[lang]['help'], parse_mode="HTML")

@router.message(Command("restart"))
async def restart_command(message: Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, 'uz')
    status_message = await message.answer("🔄 Restarting...", parse_mode="HTML")
    await asyncio.sleep(1.5)
    await status_message.edit_text("✅ Done!", parse_mode="HTML")

# Render uchun soxta veb-sahifa xandleri
async def handle(request):
    return web.Response(text="Bot is running smoothly!")

async def main():
    # Soxta serverni ishga tushirish (Render portni ko'rishi uchun)
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Fake server active on port {port}")

    # Routerni dispatcherga ulash va polling boshlash
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
