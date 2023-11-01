import pyrogram
from pyrogram import Client, filters
import asyncio
import re
from transformers import AutoModelForQuestionAnswering
from transformers import AutoTokenizer

# Define the API credentials
API_ID = "8914119"
API_HASH = "652bae601b07c928b811bdb310fdb4b0"
BOT_TOKEN = "6629383271:AAE1ZdxlW0ZMwbhGNXMdZpCvQZaW4LPDgX8"

async def main():
    model = AutoModelForQuestionAnswering.from_pretrained("google/bard")
    tokenizer = AutoTokenizer.from_pretrained("google/bard")

    client = Client(BOT_TOKEN)

    @client.on_message(filters.command("ask"))
    async def ask_command(client, message):
        question = message.text.split(" ")[1:]

        answer = await model.generate(
            input_ids=tokenizer(question, return_tensors="pt").input_ids,
            max_length=1024,
        )[0][0]

        await message.reply_text(answer)
