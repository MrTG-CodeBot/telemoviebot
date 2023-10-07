from pyrogram import Client
from pyrogram import filters

from config import config  # Assuming you have a config file with your settings
from helpers import gen_bot

app = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.text & filters.forwarded & filters.create(lambda _, msg: msg.forward_from.username.lower() == "botfather"))
async def clone_bot(client, message):
    entities = message.entities
    msg_text = message.text or ""
    reply = await message.reply("Generating a clone.. Please wait..")
    
    # Extract bot token
    bot_token = extract_bot_token(msg_text, entities)
    
    if bot_token:
        # Create an instance of the `Bot` class and pass your authentication token to it.
        bot = await gen_bot(bot_token)
        
        if bot:
            try:
                # Get the current bot's webhook and extract domain
                webhook_info = await client.get_webhook_info()
                domain = webhook_info.url.split(config.WEBHOOK_PATH)[0]
                await bot.set_webhook(f"{domain}{config.WEBHOOK_PATH}?token={bot_token}")
            except Exception as e:
                print(e)
        
        await client.edit_message_text(chat_id=message.chat.id, message_id=reply.message_id, text=f"Successfully created a clone on @{bot.get_me().username}!")

# Define the function to extract bot token
def extract_bot_token(msg_text, entities):
    for entity in entities:
        if entity.type == "code":
            return msg_text[entity.offset:entity.offset + entity.length]

if __name__ == "__main__":
    app.run()
