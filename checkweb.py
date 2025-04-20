import requests
import telegram
import os
from difflib import unified_diff  # Değişiklik detayı için

# Config
URL = "https://drmustafametin.com"  # İzlenecek site
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # GitHub Secrets'tan alınacak
CHAT_ID = os.getenv("CHAT_ID")  # GitHub Secrets'tan alınacak

def send_telegram_notification(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

# Web sayfasını çek
response = requests.get(URL)
current_content = response.text

# Eski içerikle karşılaştır
try:
    with open("last_content.txt", "r") as f:
        last_content = f.read()
except FileNotFoundError:
    last_content = ""

if current_content != last_content:
    # Değişiklik varsa detayları hazırla
    diff = list(unified_diff(
        last_content.splitlines(keepends=True),
        current_content.splitlines(keepends=True),
        fromfile='Önceki',
        tofile='Şimdi',
        n=3  # Bağlam satırı sayısı
    ))

    # Telegram mesajı
    message = (
        f"🚨 <b>Web Sayfası Değişikliği</b>\n"
        f"🔗 <a href='{URL}'>Siteyi Görüntüle</a>\n\n"
        f"<pre>Değişiklik Detayı:\n{''.join(diff)[:4000]}</pre>"
    )
    
    send_telegram_notification(message)
    
    # Yeni içeriği kaydet
    with open("last_content.txt", "w") as f:
        f.write(current_content)
