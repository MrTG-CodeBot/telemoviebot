from pyrogram import Client, filters
import openai
from info import OPENAI_API_KEY

# Define your OpenAI API key
OPENAI_API_KEY = "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"

# Function to generate a response using GPT-3
def generate_response_with_gpt3(user_input):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=user_input,
            max_tokens=2000,  # Adjust the response length as needed
        )
        return response.choices[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Define a filter to handle the /ai command
@Client.on_message(filters.command("ai", prefixes="/"))
async def ai_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a question or input with the /ai command.")
        return

    user_input = " ".join(message.command[1:])
    response = generate_response_with_gpt3(user_input)
    await message.reply_text(response)

