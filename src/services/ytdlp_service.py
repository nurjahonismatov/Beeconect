import os
# To'g'ri ko'rinishi:
import imageio_ffmpeg
# Windows-da ffmpeg muammosini hal qiluvchi kutubxona

from yt_dlp import YoutubeDL
from src.config import DOWNLOAD_DIR, COOKIES_DIR

def download_video_sync(url: str) -> str:
    """Videoni eng mos formatda (musiqasi bilan) yuklash"""
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        # 🌟 MANA BU QATOR WINDOWS-DAGI XATOLIKNI BUTUNLAY YO'Q QILADI:
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(), 
    }

    # Cookies tekshiruvi (Blokirovkalardan qochish uchun)
    yt_cookie = COOKIES_DIR / "youtube.txt"
    ig_cookie = COOKIES_DIR / "instagram.txt"
    
    if ("youtube.com" in url or "youtu.be" in url) and yt_cookie.exists() and os.path.getsize(yt_cookie) > 0:
        ydl_opts['cookiefile'] = str(yt_cookie)
    elif "instagram.com" in url and ig_cookie.exists() and os.path.getsize(ig_cookie) > 0:
        ydl_opts['cookiefile'] = str(ig_cookie)

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        return f"{base}.mp4"

def download_audio_sync(url: str) -> str:
    """Faqat musiqani (audioni) yuklab olish"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # Audio ajratishda ham FFmpeg kerak bo'ladi:
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        
        # ⬇️ TIMEOUT VA BLOKDAN QOCHISH SOZLAMALARI ⬇️
        'socket_timeout': 30,           # Aloqa kutish vaqtini 30 soniya qilib belgilaymiz
        'retries': 5,                   # Xato bersa avtomatik 5 martagacha qayta urinadi
        'fragment_retries': 5,          # Video bo'laklarini yuklashda 5 marta qayta urinish
        'ignoreerrors': False,
    }
