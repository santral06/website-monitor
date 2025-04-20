import requests
import telegram
import os
from difflib import unified_diff
from datetime import datetime

# Config
URL = "https://drmustafametin.com"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_notification(message, is_change=False):
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        if is_change:
            message = f"🚨 **DEĞİŞİKLİK VAR!**\n{message}"
        else:
            message = f"✅ **Değişiklik Yok**\n{datetime.now().strftime('%d.%m.%Y %H:%M')}\n{message}"
        
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Telegram bildirim hatası: {e}")

try:
    # Web sayfasını çek
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    current_content = response.text

    # Eski içerikle karşılaştır
    last_content = ""
    if os.path.exists("last_content.txt"):
        with open("last_content.txt", "r", encoding='utf-8') as f:
            last_content = f.read()

    if current_content != last_content:
        # Değişiklik varsa detayları hazırla
        diff = list(unified_diff(
            last_content.splitlines(keepends=True),
            current_content.splitlines(keepends=True),
            fromfile='Önceki',
            tofile='Şimdi',
            n=3
        ))
        
        diff_text = ''.join(diff)[:4000]  # Telegram mesaj sınırı
        
        message = (
            f"🔗 [{URL}]({URL})\n"
            f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            f"```\n{diff_text}\n```"
        )
        
        send_telegram_notification(message, is_change=True)
        
        # Yeni içeriği kaydet
        with open("last_content.txt", "w", encoding='utf-8') as f:
            f.write(current_content)
    else:
        # Değişiklik yoksa
        message = f"🔗 [{URL}]({URL})"
        send_telegram_notification(message, is_change=False)

except requests.exceptions.RequestException as e:
    error_msg = f"⚠️ **Siteye erişilemedi!**\nHata: {str(e)}"
    send_telegram_notification(error_msg, is_change=True)
except Exception as e:
    error_msg = f"❌ **Beklenmeyen Hata!**\n{str(e)}"
    send_telegram_notification(error_msg, is_change=True)
