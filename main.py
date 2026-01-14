import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

from ai import ask_ai
from memory import chat_memory

load_dotenv()

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ---------- BOT ----------
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

AI_CHANNEL_NAME = "rakshika-ai"

# ---------- FALLBACK MESSAGES ----------
FALLBACKS = [
    "Hmm… lagta hai main thoda soch me atak gayi 😅 Ek baar phir bolna.",
    "Oho, ye miss ho gaya 🙈 Dubara bolo na.",
    "Wait… ye interesting lag raha tha 👀 Ek baar aur bolo.",
    "Arre, brain thoda buffer ho gaya 😌 Phir se try karo.",
    "Hehe, mujhe lagta hai signal weak tha 😅 Ek baar repeat?"
]

WEAK_REPLY_GUARD = [
    "Hmm 😏 thoda detail me batao na.",
    "Aise chhota hint mat do 😌 pura scene batao.",
    "Interesting… par thoda aur bolo 👀",
    "Ruko ruko 😄 ye incomplete lag raha hai."
]

# ---------- READY ----------
@bot.event
async def on_ready():
    print(f"✅ RakshikaX online as {bot.user}")

# ---------- ADMIN COMMAND ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def create_ai_channel(ctx):
    guild = ctx.guild

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

    # ✅ FIX 1: AI sirf specific channel me bole
    if message.channel.name != AI_CHANNEL_NAME:
        await bot.process_commands(message)
        return

    content = message.content.strip()
    if not content:
        return

    user_id = message.author.id

    # ✅ FIX 2: SAME MESSAGE REPEAT DETECT
    if len(chat_memory[user_id]) >= 1:
        last_user_msg = chat_memory[user_id][-1]["content"]
        if last_user_msg.lower() == content.lower():
            await message.reply(
                "Same cheez repeat kar rahe ho 😌 thoda alag tareeke se bolo.",
                mention_author=False
            )
            return

    chat_memory[user_id].append({
        "role": "user",
        "content": content
    })

    try:
        async with message.channel.typing():
            reply = ask_ai(chat_memory[user_id])

        # ✅ FIX 3: AI reply NONE / EMPTY handle
        if not reply or not isinstance(reply, str):
            reply = random.choice(FALLBACKS)

        reply = reply.strip()

        # ✅ FIX 4: WEAK REPLY MEANING CHECK (length pe nahi)
        if reply.lower() in ["ok", "hmm", "idk", "yes", "no"]:
            reply = random.choice(WEAK_REPLY_GUARD)

        chat_memory[user_id].append({
            "role": "assistant",
            "content": reply
        })

        await message.reply(reply, mention_author=False)

    except Exception as e:
        print("AI ERROR:", e)

        # ❗ REAL crash pe hi glitch bole
        await message.reply(
            "Network thoda mood me nahi tha 😮‍💨 ab bolo.",
            mention_author=False
        )

    await bot.process_commands(message)

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))
