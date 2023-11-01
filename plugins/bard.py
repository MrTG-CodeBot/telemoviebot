import pyrogram
from pyrogram import Client, filters
from transformers import AutoModelForQuestionAnswering
from transformers import AutoTokenizer

# Define the API credentials
API_ID = 8914119
API_HASH = "652bae601b07c928b811bdb310fdb4b0"
BOT_TOKEN = "6629383271:AAE1ZdxlW0ZMwbhGNXMdZpCvQZaW4LPDgX8"

# Initialize the Pyrogram client
async with pyrogram.Client("bard-ai-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:

    model = AutoModelForQuestionAnswering.from_pretrained("google/bard")
    tokenizer = AutoTokenizer.from_pretrained("google/bard")

@Client.on_message(filters.command("ask"))
async def ask_command(client, message):
    question = message.text.split(" ")[1:]

    answer = await model.generate(
        input_ids=tokenizer(question, return_tensors="pt").input_ids,
        max_length=1024,
    )[0][0]

    await message.reply_text(answer)

