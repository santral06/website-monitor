
import requests
import hashlib
import os
from telegram import Bot

# Telegram Bot Token'ınızı ve Chat ID'nizi ortam değişkenlerinden alın
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBSITE_URL = "https://www.drmustafametin.com" # Kontrol etmek istediğiniz web sitesi adresini buraya yazın

# Önceki içeriğin hash'ini saklamak için bir dosya adı belirleyin
HASH_FILE = "website_hash.txt"

def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Hatalı HTTP durum kodları için istisna oluşturur
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Web sitesine erişirken hata oluştu: {e}")
        return None

def calculate_hash(content):
    if content:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    return None

def load_previous_hash():
    try:
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_current_hash(current_hash):
    if current_hash:
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)

async def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        try:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        except Exception as e:
            print(f"Telegram mesajı gönderilirken hata oluştu: {e}")
    else:
        print("Telegram Bot Token veya Chat ID ortam değişkenleri tanımlanmamış.")

async def main():
    current_content = get_website_content(WEBSITE_URL)
    if current_content:
        current_hash = calculate_hash(current_content)
        previous_hash = load_previous_hash()

        if previous_hash is None:
            print("İlk çalıştırma. Hash kaydediliyor.")
            save_current_hash(current_hash)
        elif current_hash != previous_hash:
            print("Web sitesinde bir değişiklik tespit edildi!")
            await send_telegram_message(f"Dikkat! {WEBSITE_URL} adresinde bir güncelleme tespit edildi.")
            save_current_hash(current_hash)
        else:
            print("Web sitesinde herhangi bir değişiklik yok.")
    else:
        print("Web sitesi içeriği alınamadı.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
