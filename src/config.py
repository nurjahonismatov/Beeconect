import os
from pathlib import Path
from dotenv import load_dotenv

# .env faylini loyiha ildizidan qidirib yuklash
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Asosiy papkalar yo'li (Bular ytdlp_service uchun juda muhim!)
DOWNLOAD_DIR = BASE_DIR / "downloads"
COOKIES_DIR = BASE_DIR / "cookies"

# Kerakli papkalarni avtomatik yaratish
DOWNLOAD_DIR.mkdir(exist_ok=True)
COOKIES_DIR.mkdir(exist_ok=True)

# Maxfiy o'zgaruvchilarni olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Xavfsizlik tekshiruvi
if not BOT_TOKEN:
    print("\n❌ DIQQAT: .env faylida BOT_TOKEN topilmadi yoki .env fayli yaratilmagan!")
