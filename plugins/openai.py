import os
from pyrogram import Client, filters
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPEN_API_KEY, OPENAI_ORGANIZATION

openai.api_key = OPEN_API_KEY
openai.organization = OPENAI_ORGANIZATION

openai_api_key= "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"  
openai.organization = "org-1KWuVrdSyt25Vfvs8rvS3ofB"

openai.api_key = OPEN_API_KEY
openai.organization = OPENAI_ORGANIZATION


@app.on_message(filters.command("opeanai"))
async def openai(client, message):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=message.text,
      temperature=0.7,
      max_tokens=100
    )
          
    await client.send_message(chat_id=message.chat.id, text=response.choices[0].text.strip())

app.run()
