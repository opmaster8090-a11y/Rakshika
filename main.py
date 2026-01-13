import discord
from discord.ext import commands
import os
from ai import ask_ai
from dotenv import load_dotenv

load_dotenv()

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ---------- BOT ----------
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ---------- READY ----------
@bot.event
async def on_ready():
    print(f"RakshakX online as {bot.user}")

# ---------- MESSAGE HANDLER ----------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    is_mentioned = bot.user in message.mentions

    if is_mentioned:
        content = content.replace(f"<@{bot.user.id}>", "").strip()

    if content:
        async with message.channel.typing():  # typing indicator
            reply = ask_ai(content)
            await message.reply(reply, mention_author=False)

    await bot.process_commands(message)

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))
