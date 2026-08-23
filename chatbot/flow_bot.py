import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from router import query_llm

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Track memory per channel/thread ID
conversation_memory = {}

def chunk_message(text: str, max_length: int = 1900):
    """Splits long responses into chunks under Discord's character limit."""
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

async def process_llm_prompt(channel_id, prompt: str, send_func, typing_func, provider: str = "gemini-fast"):
    """Core logic to process prompts and maintain thread memory."""
    if channel_id not in conversation_memory:
        conversation_memory[channel_id] = []

    # Append user prompt to channel history
    conversation_memory[channel_id].append({"role": "user", "parts": [{"text": prompt}]})

    if len(conversation_memory[channel_id]) > 10:
        conversation_memory[channel_id] = conversation_memory[channel_id][-10:]

    async with typing_func():
        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(
            None, query_llm, provider, conversation_memory[channel_id]
        )

        conversation_memory[channel_id].append({"role": "model", "parts": [{"text": reply}]})

        for chunk in chunk_message(reply):
            await send_func(chunk)

@bot.event
async def on_ready():
    print(f'⚡ FlowBot active as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the bot was tagged directly
    if bot.user.mentioned_in(message):
        # Strip out the mention tag (e.g. <@123456789>)
        clean_prompt = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
        
        if clean_prompt:
            await process_llm_prompt(
                channel_id=message.channel.id,
                prompt=clean_prompt,
                send_func=message.channel.send,
                typing_func=message.channel.typing,
                provider="gemini-fast"
            )
            return

    # Process standard prefix commands (like !sync)
    await bot.process_commands(message)

# --- Slash Commands ---

@bot.tree.command(name="ask", description="Fast operational queries via Gemini 3.6 Flash")
@app_commands.describe(prompt="What would you like to ask FlowBot?")
async def ask_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    await process_llm_prompt(
        channel_id=interaction.channel_id,
        prompt=prompt,
        send_func=interaction.followup.send,
        typing_func=interaction.channel.typing,
        provider="gemini-fast"
    )

@bot.tree.command(name="draft", description="Detailed proposals, copy, and grant writing via Gemini 3.6 Pro")
@app_commands.describe(prompt="What content or proposal do you want FlowBot to draft?")
async def draft_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    await process_llm_prompt(
        channel_id=interaction.channel_id,
        prompt=prompt,
        send_func=interaction.followup.send,
        typing_func=interaction.channel.typing,
        provider="gemini-pro"
    )

@bot.tree.command(name="clear", description="Reset conversation memory for this thread or channel")
async def clear_command(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    conversation_memory[channel_id] = []
    await interaction.response.send_message("🧹 Memory cleared for this thread!")

@bot.tree.command(name="flowhelp", description="Display available FlowBot commands and guidance")
async def flowhelp_command(interaction: discord.Interaction):
    help_text = (
        "**🌊 FlowBot Slash Commands:**\n"
        "`/ask <prompt>` - Fast operational queries (Gemini 3.6 Flash)\n"
        "`/draft <prompt>` - Detailed proposals & copy (Gemini 3.6 Pro)\n"
        "`/clear` - Reset conversation memory for this thread\n"
        "`/flowhelp` - View available commands\n"
        "💡 *You can also @FlowBot directly in any channel or thread!*"
    )
    await interaction.response.send_message(help_text)

@bot.command()
async def sync(ctx):
    try:
        bot.tree.clear_commands(guild=ctx.guild)
        await bot.tree.sync(guild=ctx.guild)
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Synced {len(synced)} global slash commands successfully!")
    except Exception as e:
        await ctx.send(f"❌ Sync failed: {str(e)}")

if __name__ == '__main__':
    bot.run(TOKEN)




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