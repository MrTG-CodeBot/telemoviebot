import pyrogram
from pyrogram import Client
import openai
import requests
from requests import Session
from info import API_ID, API_HASH, BOT_TOKEN, OPENAAI_API_KEY
import os
import openai
openai.organization = "org-63EsIa4XvrrUsETGhjsDzYIq"
openai.api_key = os.getenv("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")
openai.Model.list()

# Authorize the OpenAI API key
def authorize_openai(api_key):
    session = Session()
    session.headers["Authorization"] = f"Bearer {api_key}"
    return session

# Define a function to handle incoming messages
@Client.on_message(pyrogram.filters.command('ask', prefixes='/'))
async def ask_command(client, message):
    
# Extract the user's question from the command
  question = ' '.join(message.command[1:])

  if not question:
    await message.reply("Please ask a question using the /ask command.")
  else:
      
# Authorize the OpenAI API key
    session = authorize_openai(OPENAAI_API_KEY)

# Generate a response using ChatGPT
    response = session.post(
      "https://api.openai.com/v1/engines/davinci/completions",
      headers={"Authorization": f"Bearer {OPENAAI_API_KEY}"},
      json={"prompt": f"I have a question: {question}", "max_tokens": 150, "temperature": 0.7}
    )

# Send the response to the user
    await message.reply(response.json()["choices"][0]["text"])
