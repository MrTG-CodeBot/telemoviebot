import psutil
from pyrogram import Client, filters

# Define the /sakura command handler
@Client.on_message(filters.command("sakura"))
def bot_status(client, message):
    uptime = psutil.boot_time()
    bot_info = f"**Bot Uptime: {uptime}\n**"
    bot_info += f"**CPU Usage: {psutil.cpu_percent(interval=1)}%\n**"
    bot_info += f"**RAM Usage: {psutil.virtual_memory().percent}%**"
    message.reply_text(bot_info)

