from pyrogram import Client, filters
import openai  
from info import API_ID, API_HASH, BOT_TOKEN

# Initialize OpenAI GPT-3 with your API key
openai.api_key = OPENAI_API_KEY

# Define a function to handle /generate command
Client.on_message(filters.command("generate", "/generate") & filters.private).on(handle_generate_command)
 async def generate_test(client, message):
    user_request = message.text[9:]  # Extract user's request

    # Use OpenAI GPT-3 to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",  # Choose an appropriate engine
        prompt=user_request,
        max_tokens=50  # Adjust the response length
    )

    generated_response = response.choices[0].text

    # Send the generated response back to the user
    await message.reply(generated_response)

# Register the /generate command handler
