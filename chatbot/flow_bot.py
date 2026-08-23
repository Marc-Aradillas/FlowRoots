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
    print(f'⚡ FlowBot active as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Help Command
    if message.content.strip() in ['!help', '!flowbot']:
        help_text = (
            "**🌊 FlowBot Commands:**\n"
            "`!ask <prompt>` or `!gemini <prompt>` - Fast operational queries (Gemini 2.5 Flash)\n"
            "`!draft <prompt>` or `!pro <prompt>` - Detailed proposals & copy (Gemini 2.5 Pro)\n"
            "`!ping` - Check bot connection"
        )
        await message.channel.send(help_text)
        return

    if message.content.startswith('!ping'):
        await message.channel.send('FlowBot is live and connected! 🌊')
        return

    # Determine Provider Route
    provider = None
    prompt = ""

    content = message.content
    if content.startswith('!ask '):
        provider = 'gemini-fast'
        prompt = content[5:]
    elif content.startswith('!gemini '):
        provider = 'gemini-fast'
        prompt = content[8:]
    elif content.startswith('!draft '):
        provider = 'gemini-pro'
        prompt = content[7:]
    elif content.startswith('!pro '):
        provider = 'gemini-pro'
        prompt = content[5:]

    if provider and prompt.strip():
        async with message.channel.typing():
            loop = asyncio.get_event_loop()
            reply = await loop.run_in_executor(None, query_llm, provider, prompt)

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