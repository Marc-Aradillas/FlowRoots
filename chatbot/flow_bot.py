import os
import discord
from dotenv import load_dotenv

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
    client.run(TOKEN)