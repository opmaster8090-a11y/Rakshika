import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from ai import ask_ai
from memory import chat_memory

load_dotenv()

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

AI_CHANNEL_NAME = "rakshika-ai"

# ---------- READY ----------
@bot.event
async def on_ready():
    print(f"RakshikaX online as {bot.user}")

# ---------- ADMIN COMMAND ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def create_ai_channel(ctx):
    guild = ctx.guild

    # already exists?
    for channel in guild.text_channels:
        if channel.name == AI_CHANNEL_NAME:
            await ctx.send("AI channel already exists 😌")
            return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    channel = await guild.create_text_channel(
        AI_CHANNEL_NAME,
        overwrites=overwrites
    )

    await ctx.send(f"✅ AI channel created: {channel.mention}")

# ---------- MESSAGE HANDLER ----------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ❌ sirf AI channel me reply kare
    if message.channel.name != AI_CHANNEL_NAME:
        return

    content = message.content.strip()
    if not content:
        return

    user_id = message.author.id

    # user msg save
    chat_memory[user_id].append({
        "role": "user",
        "content": content
    })

    async with message.channel.typing():
        reply = ask_ai(chat_memory[user_id])

    # bot reply save
    chat_memory[user_id].append({
        "role": "assistant",
        "content": reply
    })

    await message.reply(reply, mention_author=False)

    await bot.process_commands(message)

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))
