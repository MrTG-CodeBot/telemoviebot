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
    # Load the model and tokenizer
    model = AutoModelForQuestionAnswering.from_pretrained("google/bard")
    tokenizer = AutoTokenizer.from_pretrained("google/bard")

    # Create a Pyrogram client
    client = Client(BOT_TOKEN)

    # Define a message handler for the /ask command
    @client.on_message(filters.command("ask"))
    async def ask_command(client, message):
        # Get the question from the message text
        question = message.text.split(" ")[1:]

        # Generate an answer using the model
        answer = await model.generate(
            input_ids=tokenizer(question, return_tensors="pt").input_ids,
            max_length=1024,
        )[0][0]

        # Send the answer to the user
        await message.reply_text(answer)

    # Start the Pyrogram client
    await client.start()

    # Wait for the user to press Enter to quit
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
