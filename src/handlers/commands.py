import os
import sys

# Loyihaning asosiy papkasini (Beeconect+) Python qidiruv yo'liga qo'shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# SIZNING ESKI IMPORTLARINGIZ ENDI SHUNDAN KEYIN KELADI:
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from src.database import add_user  # Endi bu xato bermaydi!



from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command
from src.database import add_user

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message):
    # Foydalanuvchini bazaga qo'shish
    await add_user(message.from_user.id, message.from_user.username)
    
    await message.answer(
        f"👋 **Assalomu alaykum, {message.from_user.full_name}!**\n\n"
        "Men Instagram, YouTube va TikTok videolarini yuklovchi professional botman.\n\n"
        "🚀 Menga shunchaki videoning **havolasini (linkini)** yuboring!"
    )

@router.message(Command("help"))
async def help_cmd(message: Message):
    # Foydalanuvchini bazaga qo'shish
    await add_user(message.from_user.id, message.from_user.username)
    
    await message.answer(
       help_text = """👋 Salom! Men Instagram'dan media fayllarni yuklovchi botman.

Bot ishlamay qolsa yoki tushunmayotgan bo'lsangiz, quyidagi ko'rsatmalarga amal qiling:
1. Instagram ilovasiga kiring.
2. O'zingizga yoqqan video yoki rasmning "Link" (Havola) nusxasini oling.
3. Olingan havolani ushbu chatga yuboring.
4. Bir necha soniya kuting, men uni sizga jo'nataman!

⚙️ Buyruqlar:
/start — Botni qayta ishga tushirish
/help — Yordam oynasini ko'rish

📬 Muammo yuzaga kelsa: @admin_username"""

    )
