import hashlib
import requests
import os
import subprocess
import telegram

URL = "https://drmustafametin.com"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_site_hash():
    response = requests.get(URL)
    content = response.text.encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def get_previous_hash_from_git():
    try:
        result = subprocess.run(
            ["git", "show", "origin/state:site_hash.txt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def write_current_hash_to_file(hash_value):
    with open("site_hash.txt", "w") as f:
        f.write(hash_value)

def send_telegram_message(message):
    if BOT_TOKEN and CHAT_ID:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    current_hash = get_site_hash()
    previous_hash = get_previous_hash_from_git()

    if not previous_hash:
        send_telegram_message("✅ İzleme başlatıldı.")
    elif current_hash != previous_hash:
        send_telegram_message("🔄 Web sitesinde değişiklik tespit edildi!")
    else:
        send_telegram_message("⏳ Kontrol yapıldı, değişiklik yok.")

    write_current_hash_to_file(current_hash)

if __name__ == "__main__":
    main()
