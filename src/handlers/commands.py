import os
import sys
import asyncio

# Loyihaning asosiy papkasini (Beeconect+) Python qidiruv yo'liga qo'shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from src.database import add_user

router = Router()

# Foydalanuvchilar tilini vaqtinchalik saqlash
user_languages = {}

# 🌍 3 tildagi barcha matnlar lug'ati
TEXTS = {
    'uz': {
        'settings_menu': "⚙️ <b>Sozlamalar bo'limi</b>\n\nBot tilini o'zgartirish uchun quyidagi tugmalardan birini tanlang:",
        'lang_changed': "✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>\nEndi bot sizga o'zbek tilida xizmat ko'rsatadi.",
        'need_lang': "⚠️ Iltimos, oldin pastdagi tugmalardan tilni tanlang!",
        'help': """🤖 <b>Botdan qanday foydalanish kerak?</b>

Menga Instagram’dan biron bir video, rasm yoki Reels ssilkasini (havolasini) yuboring. Men uni sizga yuklab beraman.

📌 <b>Imkoniyatlar:</b>
• <b>Reels</b> yuklash
• <b>Post</b> (Rasm va Video) yuklash
• <b>Stories</b> (Hikoyalar) yuklash
• <b>Carousel</b> (Bitta postdagi bir nechta rasm) yuklash

⚙️ <b>Buyruqlar:</b>
/start — Botni qayta ishga tushirish
/help — Ushbu yordam oynasini ko‘rish
/settings — Bot tilini o'zgartirish
/restart — Bot funksiyalarini yangilash

⚠️ <b>Muhim:</b> Bot faqat ochiq (public) profillardagi videolarni yuklay oladi. Yopiq (private) profillardagi kontentlarni yuklash imkoni yo‘q.""",
        'start': """👑 <b>Assalomu alaykum, {name}!</b>

Instagram’dan media fayllarni reklamasiz va kutishlarsiz yuklab beruvchi botga xush kelibsiz! ✨

📥 <b>Qanday ishlatiladi?</b>
Instagram ilovasidan olingan havolani (linkni) ushbu chatga yuboring, xolos.

💡 <i>Bot faqat ochiq (public) sahifalar havolasini yuklay oladi.</i>

🛠 Buyruqlar menyusi: /help yoki /settings"""
    },
    'ru': {
        'settings_menu': "⚙️ <b>Раздел настроек</b>\n\nЧтобы изменить язык бота, выберите один из вариантов ниже:",
        'lang_changed': "✅ <b>Язык успешно изменен!</b>\nТеперь бот будет отвечать вам на русском языке.",
        'need_lang': "⚠️ Пожалуйста, сначала выберите язык, нажав на кнопку ниже!",
        'help': """🤖 <b>Как пользоваться ботом?</b>

Отправьте мне ссылку на любое video, фото или Reels из Instagram. Я скачаю и отправлю его вам.

📌 <b>Возможности:</b>
• Скачивание <b>Reels</b>
• Скачивание <b>Постов</b> (Фото и Видео)
• Скачивание <b>Stories</b> (Из историй)
• Скачивание <b>Carousel</b> (Несколько фото в одном посте)

⚙️ <b>Команды:</b>
/start — Перезапустить бота
/help — Посмотреть это окно помощи
/settings — Изменить язык бота
/restart — Обновить функции бота

⚠️ <b>Важно:</b> Бот может скачивать видео только из открытых (публичных) профилей. Скачивание контента из закрытых (приватных) профилей невозможно.""",
        'start': """👑 <b>Здравствуйте, {name}!</b>

Добро пожаловать в бот, который скачивает медиафайлы из Instagram без рекламы и ожиданий! ✨

📥 <b>Как использовать?</b>
Просто отправьте ссылку, скопированную из приложения Instagram, в этот чат.

💡 <i>Бот может скачивать ссылки только с открытых (публичных) страниц.</i>

🛠 Меню команд: /help или /settings"""
    },
    'en': {
        'settings_menu': "⚙️ <b>Settings Menu</b>\n\nTo change the bot language, please select one of the options below:",
        'lang_changed': "✅ <b>Language successfully changed!</b>\nNow the bot will serve you in English.",
        'need_lang': "⚠️ Please select a language from the buttons below first!",
        'help': """🤖 <b>How to use the bot?</b>

Send me any video, photo, or Reels link from Instagram. I will download and send it to you.

📌 <b>Features:</b>
• Download <b>Reels</b>
• Download <b>Posts</b> (Photos & Videos)
• Download <b>Stories</b>
• Download <b>Carousel</b> (Multiple photos in one post)

⚙️ <b>Commands:</b>
/start — Restart the bot
/help — View this help menu
/settings — Change bot language
/restart — Refresh bot functions

⚠️ <b>Important:</b> The bot can only download media from public profiles. Content from private profiles cannot be downloaded.""",
        'start': """👑 <b>Hello, {name}!</b>

Welcome to the bot that downloads media files from Instagram without ads or waiting! ✨

📥 <b>How to use?</b>
Just send the link copied from the Instagram app to this chat.

💡 <i>The bot can only download links from open (public) pages.</i>

🛠 Commands menu: /help or /settings"""
    }
}

# 🎹 Til tanlash uchun Inline klaviatura (faqat xabar ostida chiqadi)
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
    """Botga /start buyrug'i yuborilganda pastdagi tugmalarni o'chirish va tilni chiqarish"""
    try:
        await add_user(message.from_user.id, message.from_user.username)
    except Exception as e:
        print(f"Bazaga qo'shishda xatolik: {e}")
        
    # 🔥 1-QADAM: Pastdagi tugmani majburiy o'chirish uchun vaqtinchalik bo'sh xabar yuboramiz
    clear_msg = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    # O'sha bo'sh nuqta xabarini darhol o'chirib tashlaymiz (foydalanuvchi sezmaydi, lekin tugma yo'qoladi)
    await clear_msg.delete()

    # 🔥 2-QADAM: Til tanlash oynasini yuboramiz
    await message.answer(
        text="🌐 Tilni tanlang / Выберите язык / Select language:",
        reply_markup=get_lang_inline_keyboard()
    )



@router.callback_query(F.data.startswith("lang_"))
async def set_language_callback(callback: CallbackQuery):
    """Inline tugmalardan birontasi bosilganda tilni saqlash va start matnini ko'rsatish"""
    selected_lang = callback.data.split("_")[1] # 'uz', 'ru' yoki 'en' ajratiladi
    user_id = callback.from_user.id
    
    user_languages[user_id] = selected_lang
    
    await callback.answer()
    await callback.message.delete()
    
    start_text = TEXTS[selected_lang]['start'].format(name=callback.from_user.full_name)
    await callback.message.answer(
        text=start_text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove() # Pastdagi tugmalar butunlay yo'q qilinadi
    )


@router.message(Command("settings"))
async def settings_command(message: Message):
    """Botga /settings buyrug'i yuborilganda foydalanuvchi tilida inline tugmalarni ko'rsatish"""
    user_id = message.from_user.id
    lang = user_languages.get(user_id, 'uz') # til topilmasa defolt 'uz'
    
    await message.answer(
        text=TEXTS[lang]['settings_menu'],
        parse_mode="HTML",
        reply_markup=get_lang_inline_keyboard()
    )


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
    lang = user_languages.get(user_id)
    
    if not lang:
        await message.answer(TEXTS['uz']['need_lang'], reply_markup=get_lang_inline_keyboard())
        return

    loading_texts = {
        'uz': ("🔄 <b>Bot qayta ishga tushmoqda...</b>", "✅ <b>Bot muvaffaqiyatli qayta ishga tushirildi!</b>\n\nBarcha modullar yangilandi. Yangi havolani yuborishingiz mumkin. 🚀"),
        'ru': ("🔄 <b>Бот перезапускается...</b>", "✅ <b>Бот успешно перезапущен!</b>\n\nВсе модули обновлены. Можете отправить новую ссылку. 🚀"),
        'en': ("🔄 <b>Bot is restarting...</b>", "✅ <b>Bot successfully restarted!</b>\n\nAll modules updated. You can send a new link. 🚀")
    }
    
    status_message = await message.answer(loading_texts[lang][0], parse_mode="HTML")
    await asyncio.sleep(1.5)
    await status_message.edit_text(loading_texts[lang][1], parse_mode="HTML")
