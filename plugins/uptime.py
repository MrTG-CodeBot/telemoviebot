import psutil
from pyrogram import Client, filters

# Define the /stats command handler
@Client.on_message(filters.command("uptime") & filters.incoming)
def bot_status(client, message):

    # Get bot uptime
    uptime = psutil.boot_time()

    # Get bot CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Get bot RAM usage
    ram_usage = psutil.virtual_memory().percent

    # Get disk usage
    disk_usage = psutil.disk_usage("/").percent

    # Get network usage
    net_io = psutil.net_io_counters()
    net_in_rate = net_io.bytes_recv / 1024 / 1024
    net_out_rate = net_io.bytes_sent / 1024 / 1024

    # Format bot status message
    bot_status = f"**Bot Uptime:** {uptime}\n"
    bot_status += f"**CPU Usage:** {cpu_usage:.1f}%\n"
    bot_status += f"**RAM Usage:** {ram_usage:.1f}%\n"
    bot_status += f"**Disk Usage:** {disk_usage:.1f}%\n"
    bot_status += f"**Network In:** {net_in_rate:.1f} MB/s\n"
    bot_status += f"**Network Out:** {net_out_rate:.1f} MB/s\n"

    # Send bot status message
    message.reply_text(bot_status)
