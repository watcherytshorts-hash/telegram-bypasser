import subprocess
import sys

# --- FORCE INSTALL DEPENDENCIES AT RUNTIME ---
def install_packages():
    try:
        import telebot
        import requests
    except ImportError:
        print("📦 Dependencies missing. Forcing installation now...")
        # Automatically run pip install for pyTelegramBotAPI and requests
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", "requests"])
        print("✅ Installation complete! Launching bot...")

# Execute the auto-install before running anything else
install_packages()

# --- YOUR ACTUAL BOT CODE STARTS HERE ---
import os
import requests
import telebot

# Replace with your token from @BotFather
API_TOKEN = '8813724096:AAFdHvuoERJ-L8d8OZldxLiCu6PV1DuKOEs'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the Key System Bypasser Bot!\n\n"
                          "Send me your Delta or Linkvertise link, and I will attempt to bypass it.")

@bot.message_handler(func=lambda message: True)
def bypass_link(message):
    url = message.text.strip()
    
    if not url.startswith("http://") and not url.startswith("https://"):
        bot.reply_to(message, "❌ Please send a valid link.")
        return
        
    bot.reply_to(message, "⏳ Bypassing your link... please wait...")

    try:
        # Request to a community bypass API
        api_url = f"https://fluxteam.net{url}"
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        if response.status_code == 200 and "key" in data:
            bot.reply_to(message, f"✅ **Bypass Successful!**\n\n🔑 **Key:** `{data['key']}`", parse_mode="Markdown")
        elif response.status_code == 200 and "result" in data:
            bot.reply_to(message, f"✅ **Bypass Successful!**\n\n🔑 **Key:** `{data['result']}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Failed to bypass. The link might be invalid, or the API is currently down.")
            
    except Exception as e:
        bot.reply_to(message, "⚠️ An error occurred while processing your request.")

# Start the bot
bot.infinity_polling()
