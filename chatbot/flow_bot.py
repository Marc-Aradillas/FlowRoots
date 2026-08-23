import os
import asyncio
import discord
from dotenv import load_dotenv
from router import query_llm

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def chunk_message(text: str, max_length: int = 1900):
    """Splits long responses into chunks under Discord's 2000 char limit."""
    chunks = []
    while len(text) > max_length:
        # Find the last newline or space before the limit to break cleanly
        split_idx = text.rfind('\n', 0, max_length)
        if split_idx == -1:
            split_idx = text.rfind(' ', 0, max_length)
        if split_idx == -1:
            split_idx = max_length

        chunks.append(text[:split_idx])
        text = text[split_idx:].lstrip()
    if text:
        chunks.append(text)
    return chunks

@client.event
async def on_ready():
    print(f'⚡ FlowBot active with non-blocking LLM routing as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Help Command
    if message.content.strip() == '!help' or message.content.strip() == '!flowbot':
        help_text = (
            "**🌊 FlowBot Multi-LLM Commands:**\n"
            "`!gemini <prompt>` - Query Gemini 2.5 Flash (Docs, context, fast tasks)\n"
            "`!claude <prompt>` - Query Claude 3.5 Sonnet (Proposals, pitches, copy)\n"
            "`!gpt <prompt>` - Query GPT-4o (Structured data, code, logic)\n"
            "`!ping` - Check bot status"
        )
        await message.channel.send(help_text)
        return

    if message.content.startswith('!ping'):
        await message.channel.send('FlowBot is live and connected! 🌊')
        return

    # Process Model Requests
    provider = None
    prompt = ""

    if message.content.startswith('!gemini '):
        provider = 'gemini'
        prompt = message.content[8:]
    elif message.content.startswith('!claude '):
        provider = 'claude'
        prompt = message.content[8:]
    elif message.content.startswith('!gpt '):
        provider = 'openai'
        prompt = message.content[5:]

    if provider and prompt.strip():
        async with message.channel.typing():
            # Run blocking API call in an executor so the bot loop stays responsive
            loop = asyncio.get_event_loop()
            reply = await loop.run_in_executor(None, query_llm, provider, prompt)

            # Send response in safe chunks
            for chunk in chunk_message(reply):
                await message.channel.send(chunk)

if __name__ == '__main__':
    client.run(TOKEN)




#_____________________________________________________________________________________________________
# INITIAL ITERATION OF FLOWBOT CODE
#_____________________________________________________________________________________________________

'''import os
import discord
from dotenv import load_dotenv
from router import query_llm

# Load secret environment variables from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure Discord Intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read channel text

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'⚡ FlowBot successfully authenticated as {client.user}!')

@client.event
async def on_message(message):
    # Ignore messages sent by FlowBot itself
    if message.author == client.user:
        return

    # Basic connection test command
    if message.content.startswith('!ping'):
        await message.channel.send('FlowBot is live and connected! 🌊')

if __name__ == '__main__':
    client.run(TOKEN)'''