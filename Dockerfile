# 1. Python-ning barqaror va yengil versiyasini tanlaymiz
FROM python:3.11-slim

# 2. Serverda videolarni birlashtirish (merge) uchun FFmpeg dasturi shart!
# yt-dlp FFmpeg-siz video va audioni qo'sha olmaydi.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 3. Konteyner ichidagi ishchi papkani belgilaymiz
WORKDIR /app

# 4. Kutubxonalar ro'yxatini konteynerga nusxalaymiz
COPY requirements.txt .

# 5. Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# 6. Loyihaning barcha qolgan kodlarini konteyner ichiga nusxalaymiz
COPY . .

# 7. Botni ishga tushirish buyrug'i
CMD ["python", "src/main.py"]
