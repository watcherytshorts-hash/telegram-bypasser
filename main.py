import telebot
import requests
import time

# --- 1. YOUR KEYS ---
# Get this from @BotFather
BOT_TOKEN = "8813724096:AAFdHvuoERJ-L8d8OZldxLiCu6PV1DuKOEs" 

# --- 2. THE SECRET ENGINES (The "Pro" Part) ---
# We use a list of APIs. If one fails, we swap to the next.
# These are the actual backends used by bypass websites.
APIS = [
    "https://bypass.vip",
    "https://bypass.city", 
    "https://adlinkbypass.com" 
]

bot = telebot.TeleBot(BOT_TOKEN)

def bypass_logic(url):
    """Try all engines until one works"""
    for api in APIS:
        try:
            # The magic request
            response = requests.get(api + url, timeout=10)
            data = response.json()
            
            # Check different success keys (APIs use different names)
            if data.get('status') == 'success' or 'destination' in data or 'bypassed' in data:
                return data.get('destination') or data.get('result') or data.get('bypassed')
        except:
            continue # If one fails, try the next one immediately
    return None

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    user_url = message.text.strip()
    
    # Simple check to see if it's a link
    if "http" in user_url:
        status_msg = bot.reply_to(message, "⚡ **Bypassing...**")
        
        # Run the secret engine
        result = bypass_logic(user_url)
        
        if result:
            bot.edit_message_text(
                f"✅ **Bypass Successful!**\n\n**Link:** {result}", 
                chat_id=message.chat.id, 
                message_id=status_msg.message_id
            )
        else:
            bot.edit_message_text(
                "❌ **Failed:** Could not bypass this link. It might be patched.", 
                chat_id=message.chat.id, 
                message_id=status_msg.message_id
            )

print("🚀 Bot is running...")
bot.infinity_polling()

