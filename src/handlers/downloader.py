import os
import asyncio
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from src.services.ytdlp_service import download_video_sync, download_audio_sync

router = Router()

# 1. Havolani tutib olish va to'g'ridan-to'g'ri videoni yuborish
@router.message(
    F.text.contains("instagram.com") | 
    F.text.contains("youtube.com") | 
    F.text.contains("youtu.be") | 
    F.text.contains("tiktok.com")
)
async def handle_video_download(message: Message):
    url = message.text.strip()
    status = await message.answer(" Iltimos, kuting ⏳ \nVideo yuklab olinmoqda...")

    try:
        # Videoni fonda yuklab olish
        loop = asyncio.get_event_loop()
        video_path = await loop.run_in_executor(None, download_video_sync, url)

        await status.edit_text("🚀 yana ozgina kuting...")
        
        # Musiqa tugmasi
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🎵 Musiqasini yuklash", callback_data="getaudio")
            ]
        ])
        
        # VIDEONI FOYDALANUVCHI XABARIGA REPLY QILIB YUBORISH (Bu juda muhim!)
        video_file = FSInputFile(video_path)
        await message.answer_video(
            video=video_file, 
            caption="✨  @Beeconect_bot orqali yuklab olindi! ",
            reply_markup=keyboard,
            reply_to_message_id=message.message_id  # <-- Mana shu qator zanjirni bog'laydi
        )
        await status.delete()

        # Server xotirasini tozalash
        if os.path.exists(video_path):
            os.remove(video_path)

    except Exception as e:
        await status.edit_text("❌ Xatolik yuz berdi \n\nHavola noto'g'ri yoki fayl hajmi juda katta.")
        print(f"Yuklashda xato: {e}")


# 2. Videoning pastidagi "Musiqasini yuklash" tugmasi bosilganda
@router.callback_query(F.data == "getaudio")
async def process_audio_download(call: CallbackQuery):
    # Video qaysi xabarga reply bo'lgan bo'lsa, o'sha asl xabarni (linkni) olamiz
    original_message = call.message.reply_to_message
    
    if not original_message or not original_message.text:
        await call.answer("❌ Asl havola topilmadi. Linkni qayta yuboring.", show_alert=True)
        return
        
    url = original_message.text.strip()
    await call.answer("🎵 Musiqa tayyorlanmoqda...")
    
    status = await call.message.answer("📥 Videodan musiqa ajratib olinmoqda...")
    
    try:
        loop = asyncio.get_event_loop()
        audio_path = await loop.run_in_executor(None, download_audio_sync, url)

        await status.edit_text("🚀 Musiqa  yuborilmoqda...")
        
        # Musiqani ham asl linkka reply qilib yuboramiz
        audio_file = FSInputFile(audio_path)
        await call.message.answer_audio(
            audio=audio_file, 
            caption="🎵 Videoning musiqasi ajratib berildi!\n✨ @Beeconect_bot",
            reply_to_message_id=original_message.message_id
        )
        await status.delete()

        # Server xotirasini tozalash
        if os.path.exists(audio_path):
            os.remove(audio_path)

    except Exception as e:
        await status.edit_text("❌ Musiqani yuklab olishda xatolik yuz berdi")
        print(f"Audio yuklashda xato: {e}")
