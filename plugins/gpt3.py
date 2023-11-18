import openai
from pyrogram import Client, filters
import asyncio
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, PORT


@Client.on_message(filters.command("gpt3") & filters.private)
async def gpt3_handler(client, message):
    try:
        # Extract prompt from message
        prompt = message.text.split("gpt3 ")[1]

        # Send a typing indicator while processing
        await message.chat.send_action(action="typing")

        # Send prompt to OpenAI API and get response
        response = openai.Completion.create(
            prompt=prompt,
            model="text-davinci-003", 
            temperature=0.7,
            max_tokens=1024,
        )

        # Truncate response to a reasonable length
        response_text = response["choices"][0]["text"][:2048]

        # Send OpenAI response to Telegram chat
        await message.reply(response_text)

    except IndexError:
        await message.reply("Please provide a prompt after the command, e.g., /gpt3 Tell me a joke.")
    except Exception as e:
        print(f"Error occurred: {e}")
        await message.reply("An error occurred while processing your request. Please try again later.")
