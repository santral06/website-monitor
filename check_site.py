import requests
import hashlib
import os
import telegram
from datetime import datetime

URL = "https://drmustafametin.com"
HASH_FILE = "site_hash.txt"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def get_site_hash():
    response = requests.get(URL)
    content = response.text.encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def read_last_hash():
    if not os.path.exists(HASH_FILE):
        return None
    with open(HASH_FILE, "r") as f:
        return f.read().strip()

def save_current_hash(current_hash):
    with open(HASH_FILE, "w") as f:
        f.write(current_hash)

def send_telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(chat_id=CHAT_ID, text=f"[{now}] {message}")

def main():
    current_hash = get_site_hash()
    last_hash = read_last_hash()

    if last_hash is None:
        send_telegram_message("İlk kontrol yapıldı, takip başladı.")
    elif current_hash != last_hash:
        send_telegram_message("🔔 drmustafametin.com sitesinde DEĞİŞİKLİK var!")
    else:
        send_telegram_message("✅ drmustafametin.com sitesinde değişiklik YOK.")

    if current_hash != last_hash:
        save_current_hash(current_hash)
        os.system("git config user.name github-actions")
        os.system("git config user.email github-actions@github.com")
        os.system("git add site_hash.txt")
        os.system('git commit -m "Update hash (site changed)" || echo "No changes to commit"')
        os.system("git push origin HEAD:state")

if __name__ == "__main__":
    main()
