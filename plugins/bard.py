import asyncio
from pyrogram import Client, filters

@Client.on_message(filters.command("bard", prefixes="!"))
async def command(client, message):
    prompt = message.text.split(maxsplit=1)[1]
    response = await bard_ai(prompt)
    await message.reply_text(f"Bard: {response}")
      async def main() -> None:
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

app.run()
