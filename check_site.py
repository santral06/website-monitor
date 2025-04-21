import hashlib
import requests
import os
import telegram

URL = "https://drmustafametin.com"
HASH_FILE = "site_hash.txt"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_site_hash():
    response = requests.get(URL)
    content = response.text.encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def read_previous_hash():
    if not os.path.exists(HASH_FILE):
        return ""
    with open(HASH_FILE, "r") as f:
        return f.read().strip()

def write_current_hash(hash_value):
    with open(HASH_FILE, "w") as f:
        f.write(hash_value)

def send_telegram_message(message):
    if BOT_TOKEN and CHAT_ID:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    current_hash = get_site_hash()
    previous_hash = read_previous_hash()

    if not previous_hash:
        send_telegram_message("✅ İzleme başlatıldı.")
        write_current_hash(current_hash)
        return

    if current_hash != previous_hash:
        send_telegram_message("🔄 Web sitesinde değişiklik tespit edildi!")
        write_current_hash(current_hash)
    else:
        send_telegram_message("⏳ Kontrol yapıldı, değişiklik yok.")

if __name__ == "__main__":
    main()
