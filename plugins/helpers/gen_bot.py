from pyrogram import Client

bots_list = {}

async def get_bot(api_id, api_hash, bot_token):
    if bot_token not in bots_list:
        app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
        await app.start()
        bots_list[bot_token] = app
    return bots_list[bot_token]
