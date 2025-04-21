import discord
import os
from openai import OpenAI
from commands import set_openai_client, handle_ask, handle_summarise, handle_explaincode
from keep_alive import keep_alive
from dotenv import load_dotenv

# Load environment variables (for VS Code)
load_dotenv()

# Replit keep-alive
keep_alive()

# Get keys
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Set up OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)
set_openai_client(openai_client)

# Setup bot intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ==== EVENTS ====

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content

    if content.startswith('!ask'):
        user_input = content[5:].strip()
        if not user_input:
            await message.channel.send("❗ Please provide a question after `!ask`.")
            return
        await message.channel.send("🧠 Thinking...")
        await handle_ask(message, user_input)

    elif content.startswith('!summarise'):
        text = content[10:].strip()
        if not text:
            await message.channel.send("📝 Please provide text to summarise.")
            return
        await message.channel.send("📚 Summarising...")
        await handle_summarise(message, text)

    elif content.startswith('!explaincode'):
        code = content[13:].strip()
        if not code:
            await message.channel.send("💻 Please paste some code.")
            return
        await message.channel.send("🔍 Explaining code...")
        await handle_explaincode(message, code)

    elif content.startswith('!help'):
        help_msg = (
            "**Studiora Commands:**\n"
            "`!ask <question>` — Ask anything \n"
            "`!summarise <text>` — Paste notes or text to summarise\n"
            "`!explaincode <code>` — Get an explanation of any code snippet\n"
            "`!help` — Show this help message again\n"
        )
        await message.channel.send(help_msg)

@client.event
async def on_guild_join(guild):
    print(f"📥 Bot joined {guild.name} ({guild.id})")

    category_name = "📚 Studiora"
    channel_name = "studybot-chat"

    try:
        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            print("🔧 Creating category...")
            category = await guild.create_category(name=category_name)

        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel is None:
            print("📁 Creating channel inside category...")
            new_channel = await guild.create_text_channel(name=channel_name, category=category)
            await new_channel.send(
                "**👋 Hello! I’m Studiora, your AI Study Buddy.**\n"
                "You can use commands like:\n"
                "`!ask` — Ask me anything\n"
                "`!summarise` — Summarise your notes\n"
                "`!explaincode` — Understand what code does\n"
                "✨ Type `!help` at any time to see what I can do!"
            )
        else:
            print("⚠️ Channel already exists.")
    except discord.Forbidden:
        print(f"❌ Missing permissions to create category/channel in {guild.name}")
    except Exception as e:
        print(f"⚠️ Unexpected error in {guild.name}: {e}")

# ==== RUN ====
client.run(DISCORD_TOKEN)
