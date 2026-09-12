import os
import sys
import asyncio

# Loyihaning asosiy papkasini (Beeconect+) Python qidiruv yo'liga qo'shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.database import add_user

router = Router()

# HTML formatida yozilgan xatosiz yordam matni
HELP_TEXT = """🤖 <b>Botdan qanday foydalanish kerak?</b>

Menga Instagram’dan biron bir video, rasm yoki Reels ssilkasini (havolasini) yuboring. Men uni sizga yuklab beraman.

📌 <b>Imkoniyatlar:</b>
• <b>Reels</b> yuklash
• <b>Post</b> (Rasm va Video) yuklash
• <b>Stories</b> (Hikoyalar) yuklash
• <b>Carousel</b> (Bitta postdagi bir nechta rasm) yuklash

⚙️ <b>Buyruqlar:</b>
/start — Botni qayta ishga tushirish
/help — Ushbu yordam oynasini ko‘rish
/restart — Bot funksiyalarini yangilash

⚠️ <b>Muhim:</b> Bot faqat ochiq (public) profillardagi videolarni yuklay oladi. Yopiq (private) profillardagi kontentlarni yuklash imkoni yo‘q."""


@router.message(Command("start"))
async def start_command(message: Message):
    """Botga /start buyrug'i yuborilganda ishlovchi funksiya"""
    try:
        await add_user(message.from_user.id, message.from_user.username)
    except Exception as e:
        print(f"Bazaga qo'shishda xatolik: {e}")
        
    start_text = (
        f"👑 <b>Assalomu alaykum, {message.from_user.full_name}!</b>\n\n"
        f"Instagram’dan media fayllarni reklamasiz va kutishlarsiz yuklab beruvchi botga xush kelibsiz! ✨\n\n"
        f"📥 <b>Qanday ishlatiladi?</b>\n"
        f"Instagram ilovasidan olingan havolani (linkni) ushbu chatga yuboring, xolos.\n\n"
        f"💡 <i>Bot faqat ochiq (public) sahifalar havolasini yuklay oladi.</i>\n\n"
        f"🛠 Buyruqlar menyusi: /help"
    )
    await message.answer(start_text, parse_mode="HTML")


@router.message(Command("help"))
async def help_command(message: Message):
    """Botga /help buyrug'i yuborilganda ishlovchi funksiya"""
    await message.answer(HELP_TEXT, parse_mode="HTML")


@router.message(Command("restart"))
async def restart_command(message: Message):
    """Botni qayta ishga tushirish buyrug'i"""
    status_message = await message.answer("🔄 <b>Bot qayta ishga tushmoqda...</b>\n<i>Keshlar tozalanmoqda...</i>", parse_mode="HTML")
    await asyncio.sleep(1.5)
    await status_message.edit_text(
        "✅ <b>Bot muvaffaqiyatli qayta ishga tushirildi!</b>\n\n"
        "Barcha yuklash modullari yangilandi. Menga yangi Instagram havolasini yuborishingiz mumkin. 🚀",
        parse_mode="HTML"
    )
