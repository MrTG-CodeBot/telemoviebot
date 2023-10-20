from pyrogram import Client, filters
import openai
from info.openai_api_key import openai_api_key

# Define a filter to handle the /ai command
@Client.on_message(filters.command("ai", prefixes="/"))
async def ai_command(_, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a question or input with the /ai command.")
        return

    user_input = " ".join(message.command[1:])
    response = generate_response_with_gpt3(user_input)
    await message.reply_text(response)

# Function to generate a response using GPT-3
def generate_response_with_gpt3(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=150,  # Adjust the response length as needed
    )
    return response.choices[0].text

