

import tracemalloc
import requests
import telegram
import os
from datetime import datetime

# Initialize tracing (fixes the warning)
tracemalloc.start()

# Config - ALWAYS validate these first
URL = "https://drmustafametin.com"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") 
CHAT_ID = os.getenv("CHAT_ID")

def validate_credentials():
    """Check if env vars exist before running"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        raise ValueError("Missing Telegram credentials!")

def send_telegram_message(text: str):
    """Properly managed Telegram session"""
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode='HTML',
            timeout=20  # Prevents hanging
        )
    finally:
        # Clean up resources
        if 'bot' in locals():
            del bot
