import pyrogram
from pyrogram import Client, filters
from transformers import AutoModelForQuestionAnswering
from transformers import AutoTokenizer
from info import API_ID,API_HASH,BOT_TOKEN

# Initialize the Pyrogram client
async with pyrogram.Client("bard-ai-bot") as app:

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

    
