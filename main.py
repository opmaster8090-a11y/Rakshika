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
user_id = message.author.id

# user ka message save
chat_memory[user_id].append({
    "role": "user",
    "content": content
})

reply = ask_ai(chat_memory[user_id])

# bot ka reply bhi save
chat_memory[user_id].append({
    "role": "assistant",
    "content": reply
})

await message.reply(reply, mention_author=False)

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))

