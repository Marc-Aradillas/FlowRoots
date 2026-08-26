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

async def get_channel_context(channel, limit=15):
    """Fetches the last N messages from the active channel/thread."""
    messages = []
    async for msg in channel.history(limit=limit, oldest_first=False):
        if not msg.author.bot:
            messages.append(f"{msg.author.display_name}: {msg.content}")
    messages.reverse()
    return "\n".join(messages)

async def process_llm_prompt(channel_id, prompt: str, send_func, channel_obj=None, provider: str = "gemini-fast"):
    """Core logic to process prompts and maintain thread memory without response timeouts."""
    if channel_id not in conversation_memory:
        conversation_memory[channel_id] = []

    # Append user prompt to channel history
    conversation_memory[channel_id].append({"role": "user", "parts": [{"text": prompt}]})

    if len(conversation_memory[channel_id]) > 10:
        conversation_memory[channel_id] = conversation_memory[channel_id][-10:]

    loop = asyncio.get_event_loop()
    reply = await loop.run_in_executor(
        None, query_llm, provider, conversation_memory[channel_id]
    )

    # Check if an error occurred; if so, pop user message to keep memory clean
    if reply.startswith("⚠️"):
        conversation_memory[channel_id].pop()
    else:
        conversation_memory[channel_id].append({"role": "model", "parts": [{"text": reply}]})

    chunks = chunk_message(reply)
    if chunks:
        # Send first chunk via interaction followup or channel send
        await send_func(chunks[0])
        
        # Send additional chunks to channel directly if response exceeds 1900 chars
        if len(chunks) > 1 and channel_obj:
            for chunk in chunks[1:]:
                await channel_obj.send(chunk)

@bot.event
async def on_ready():
    print(f'⚡ FlowBot active as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the bot was tagged directly
    if bot.user.mentioned_in(message):
        clean_prompt = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
        
        if clean_prompt:
            async with message.channel.typing():
                await process_llm_prompt(
                    channel_id=message.channel.id,
                    prompt=clean_prompt,
                    send_func=message.channel.send,
                    channel_obj=message.channel,
                    provider="gemini-fast"
                )
            return

    # Process standard prefix commands (like !sync)
    await bot.process_commands(message)

# --- Slash Commands ---

@bot.tree.command(name="ask", description="Fast operational queries via Gemini Flash")
@app_commands.describe(prompt="What would you like to ask FlowBot?")
async def ask_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    await process_llm_prompt(
        channel_id=interaction.channel_id,
        prompt=prompt,
        send_func=interaction.followup.send,
        channel_obj=interaction.channel,
        provider="gemini-fast"
    )

@bot.tree.command(name="draft", description="Detailed proposals, copy, and grant writing via Gemini Pro")
@app_commands.describe(prompt="What content or proposal do you want FlowBot to draft?")
async def draft_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    await process_llm_prompt(
        channel_id=interaction.channel_id,
        prompt=prompt,
        send_func=interaction.followup.send,
        channel_obj=interaction.channel,
        provider="gemini-pro"
    )

@bot.tree.command(name="summarize", description="Summarize or revise recent messages in this channel")
@app_commands.describe(instructions="Optional specific instructions for the summary or revision")
async def summarize_command(interaction: discord.Interaction, instructions: str = "Summarize the recent discussions."):
    await interaction.response.defer(thinking=True)
    
    # Fetch recent channel context (last 15 messages)
    history_text = await get_channel_context(interaction.channel, limit=15)
    
    if not history_text:
        await interaction.followup.send("No recent user messages found in this channel to analyze.")
        return

    full_prompt = (
        f"Instructions: {instructions}\n\n"
        f"Here is the recent message history from this channel:\n\n{history_text}"
    )

    await process_llm_prompt(
        channel_id=interaction.channel_id,
        prompt=full_prompt,
        send_func=interaction.followup.send,
        channel_obj=interaction.channel,
        provider="gemini-fast"
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
        "`/ask <prompt>` - Fast operational queries (Gemini Flash)\n"
        "`/draft <prompt>` - Detailed proposals & copy (Gemini Pro)\n"
        "`/summarize [instructions]` - Read and summarize recent channel history\n"
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