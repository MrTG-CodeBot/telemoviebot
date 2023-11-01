import pyrogram
from pyrogram import Client
import openai
from info import API_ID, API_HASH, BOT_TOKEN, OPENAAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Define a function to handle incoming messages
@Client.on_message(pyrogram.filters.command('ask', prefixes='/'))
async def ask_command(client, message):
    # Extract the user's question from the command
    question = ' '.join(message.command[1:])

    if not question:
        await message.reply("Please ask a question using the /ask command.")
    else:
        # Generate a response using ChatGPT
        response = openai.Completion.create(
            engine='text-davinci-002',
            prompt=f"I have a question: {question}",
            max_tokens=150,
            temperature=0.7
        )

        # Send the response to the user
        await message.reply(response.choices[0].text)

