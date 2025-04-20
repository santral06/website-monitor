import requests
import telegram
import os

# Ayarlar
URL = "https://drmustafametin.com"  # Kontrol edilecek site
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # GitHub'dan alınacak
CHAT_ID = os.getenv("CHAT_ID")  # GitHub'dan alınacak

# Sayfayı çek ve değişikliği kontrol et
response = requests.get(URL)
current_content = response.text

# Eski içerikle karşılaştır (basit bir örnek)
try:
    with open("last_content.txt", "r") as f:
        last_content = f.read()
except FileNotFoundError:
    last_content = ""

if current_content != last_content:
    # Değişiklik varsa Telegram'a bildir
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=f"🔄 Değişiklik algılandı: {URL}")

    # Yeni içeriği kaydet
    with open("last_content.txt", "w") as f:
        f.write(current_content)
