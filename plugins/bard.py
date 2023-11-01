import pyrogram
import openai
import asyncio
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY

OPENAI_API_KEY = openai.api_key
openai.api_key = "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"

async def send_request(payload):
    async with asyncio.to_thread(curl.post, "https://api.openai.com/v1/chat/completions",
                                 json=payload, headers={"Authorization": f"Bearer {openai.api_key}"},                         content_type="application/json"):
        response = await resp.json()
        return response

async def ask(client, message):
    text = message.text

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": text},
        ],
        "temperature": 0.7,
    }

    response = await send_request(payload)

    await client.send_message(message.chat.id, response["choices"][0]["text"])
