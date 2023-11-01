import pyrogram
from pyrogram import Client, filters
import openai
import re
import os
from os import environ


OPENAI_API_KEY = os.environ.get('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')
openai.api_key = OPENAI_API_KEY

async def openai_command(client, message):
    text = message.text.split(" ")[1:]
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    await client.send_message(message.chat.id, response.choices[0].text)

client.add_handler(openai_command, filters.command("openai"))
client.start()
