import pyrogram
from pyrogram import Client, filters
import asyncio
import re
from transformers import AutoModelForQuestionAnswering
from transformers import AutoTokenizer
from info import API_ID, API_HASH, BOT_TOKEN

# Define the API credentials
API_ID = "8914119"
API_HASH = "652bae601b07c928b811bdb310fdb4b0"
BOT_TOKEN = "6629383271:AAE1ZdxlW0ZMwbhGNXMdZpCvQZaW4LPDgX8"

async def main():
  # Load the model and tokenizer
  try:
    model = AutoModelForQuestionAnswering.from_pretrained("google/bard")
    tokenizer = AutoTokenizer.from_pretrained("google/bard")
  except Exception as e:
    print(e)
    return

  # Create a Pyrogram client
  try:
    client = Client(BOT_TOKEN)
  except Exception as e:
    print(e)
    return

  # Define a message handler for the /ask command
  @client.on_message(filters.command("ask"))
  async def ask_command(client, message):
    # Get the question from the message text
    question = message.text.split(" ")[1:]

    # Generate an answer using the model
    try:
      answer = await model.generate(
          input_ids=tokenizer(question, return_tensors="pt").input_ids,
          max_length=1024,
      )[0][0]
    except Exception as e:
      print(e)
      await message.reply_text("An error occurred while generating the answer.")
      return

    # Send the answer to the user
    await message.reply_text(answer)

  # Start the Pyrogram client
  try:
    await client.start()
  except Exception as e:
    print(e)
    return

  # Wait for the user to press Enter to quit
  await asyncio.get_event_loop().run_forever()

