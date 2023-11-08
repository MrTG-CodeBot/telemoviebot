import asyncio
import os
from os import environ
from pyrogram import Client, filters

os.environ["SECURE_1PSID"] = "cwhU4YcCopoMy_3kxUtz-RW9qhycZAPMGN6lOic3SNCmbA-DwVQ8HRfq307q7bxrhTGeVw."
os.environ["SECURE_1PSIDTS"] = "sidts-CjEBNiGH7iFBn8ExXuBa7bjk6LTA7R1P1DzgWh7Cto_BmkM7MyOLBdtWqm9PWMUGyG2uEAA"

@Client.on_message(filters.command("bard", prefixes="!"))
async def command(client, message):
    prompt = message.text.split(maxsplit=1)[1]
    response = await bard_ai(prompt)
    await message.reply_text(f"Bard: {response}")
      async def main():
    with app:
        while True:
            prompt = input("You: ")

            if prompt == "!reset":
                # Resetting a conversation in Pyrogram might be different based on your use case.
                continue
            elif prompt == "!exit":
                break

            response = app.send_message("Bard", prompt)
            print(f"Bard: {response.text}")
