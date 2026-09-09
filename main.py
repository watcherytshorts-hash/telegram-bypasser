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
    
    # Simple check if user sent a link
    if not url.startswith("http://") and not url.startswith("https://"):
        bot.reply_to(message, "❌ Please send a valid link (starting with http:// or https://).")
        return
        
    bot.reply_to(message, "⏳ Bypassing your link... please wait...")

    try:
        # Note: You need a working public bypasser API endpoint.
        # Below is a standard structural example using common community bypass query formats
        api_url = f"https://fluxteam.net{url}" # Alternative: Use active community APIs like loots, bypass.vip etc.
        
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        # Check if the API returned a successful bypass key/result
        if response.status_code == 200 and "key" in data:
            bypassed_key = data["key"]
            bot.reply_to(message, f"✅ **Bypass Successful!**\n\n🔑 **Key/Link:** `{bypassed_key}`", parse_mode="Markdown")
        elif response.status_code == 200 and "result" in data:
            bypassed_key = data["result"]
            bot.reply_to(message, f"✅ **Bypass Successful!**\n\n🔑 **Key/Link:** `{bypassed_key}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Failed to bypass. The link might be invalid, or the API is currently down.")
            
    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred while processing your request.")

# Start the bot
bot.infinity_polling()
