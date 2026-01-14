import discord
from discord.ext import commands
import os
from ai import ask_ai
from dotenv import load_dotenv
from memory import chat_memory

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

    # sirf mention ya private channel pe reply
    if bot.user not in message.mentions:
        return

    content = message.content.strip()

    # mention remove
    content = content.replace(f"<@{bot.user.id}>", "").strip()

    if not content:
        return

    user_id = message.author.id

    # user ka message save
    chat_memory[user_id].append({
        "role": "user",
        "content": content
    })

    async with message.channel.typing():
        reply = ask_ai(chat_memory[user_id])

    # bot ka reply bhi save
    chat_memory[user_id].append({
        "role": "assistant",
        "content": reply
    })

    await message.reply(reply, mention_author=False)

    await bot.process_commands(message)

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))
