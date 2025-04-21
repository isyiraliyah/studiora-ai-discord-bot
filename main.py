import discord
import os
from openai import OpenAI
from commands import set_openai_client, handle_ask, handle_summarise, handle_explaincode
from keep_alive import keep_alive
from dotenv import load_dotenv
from features.motivate import handle_motivate
from features.quiz import handle_quizme, handle_question, handle_answer, handle_viewcards, handle_deletecard

# Load environment variables (for VS Code or Replit)
load_dotenv()

# Keep Replit app alive
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
            "**📚 Studiora Help Menu**\n"
            "I'm your AI-powered study buddy — here’s everything I can help you with:\n\n"

            "**General AI Commands:**\n"
            "`!ask <question>` — Ask anything: school, tech, essays, life advice\n"
            "`!summarise <text>` — Send me notes or paragraphs and I’ll summarize them\n"
            "`!explaincode <code>` — Paste code and I’ll tell you what it does\n"
            "`!motivate` — Get a motivational quote when you're feeling unproductive\n\n"

            "**🧠 Flashcard System (in #quiz-me):**\n"
            "`!quizme question / answer` — Add a flashcard\n"
            "`!question` — I’ll quiz you with a random card\n"
            "`!answer` — Reveal the answer to the last question\n"
            "`!viewcards` — View all flashcards you've added\n"
            "`!deletecard <number>` — Delete a specific flashcard by number\n\n"

            "**📁 Flashcard Deck (in #flashcard-deck):**\n"
            "Every flashcard added is automatically posted here so you and others can study together!\n\n"

            "**🔖 Bookmarking System (in #bookmark):**\n"
            "React with ⭐ to any of my answers in `#studybot-chat`, `#quiz-me`, and I’ll save them here.\n\n"

            "**💡 Pro Tips:**\n"
            "• All commands work in `#studybot-chat`\n"
            "• Use `!help` anytime to rediscover what I can do\n"
            "• Invite your friends to study with you and share flashcards!"
        )
        await message.channel.send(help_msg)

    elif content.startswith('!motivate'):
        await handle_motivate(message)

    elif content.startswith('!quizme'):
        quiz_input = message.content[len('!quizme'):].strip()
        await handle_quizme(message, quiz_input)

    elif content.startswith('!question'):
        await handle_question(message)

    elif content.startswith('!answer'):
        await handle_answer(message)

    elif content.startswith('!viewcards'):
        await handle_viewcards(message)

    elif content.startswith('!deletecard'):
        number = message.content[len('!deletecard'):].strip()
        await handle_deletecard(message, number)


@client.event
async def on_guild_join(guild):
    print(f"📥 Bot joined {guild.name} ({guild.id})")

    category_name = "📚 Studiora"
    channel_names = ["studybot-chat", "quiz-me", "bookmark", "flashcard-deck"]

    try:
        # Check if the category exists
        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            print("🔧 Creating category...")
            category = await guild.create_category(name=category_name)

        for name in channel_names:
            existing_channel = discord.utils.get(guild.text_channels, name=name)
            if existing_channel is None:
                print(f"📁 Creating channel '{name}'...")
                new_channel = await guild.create_text_channel(name=name, category=category)

                # ✨ Custom welcome messages for each channel
                if name == "studybot-chat":
                    await new_channel.send(
                        "**👋 Welcome to Studiora! I'm your AI-powered study buddy.**\n\n"
                        "Here’s how I can help you succeed:\n"
                        "• Ask me anything with `!ask`\n"
                        "• Summarise your notes with `!summarise`\n"
                        "• Understand confusing code with `!explaincode`\n"
                        "• Get inspired with `!motivate`\n"
                        "• ⭐ React to any of my replies to save them in `#bookmark`\n\n"
                        "You can also explore:\n"
                        "• `#quiz-me` — Make flashcards and quiz yourself with `!quizme`, `!question`, `!answer`\n"
                        "• `#flashcard-deck` — Browse shared flashcards, delete with `!deletecard`\n\n"
                        "Type `!help` anytime to see what I can do!"
                    )

                elif name == "quiz-me":
                    await new_channel.send(
                        "**🧠 Welcome to Quiz Mode!**\n\n"
                        "Use this space to create and quiz yourself using flashcards:\n"
                        "• `!quizme question / answer` → Add a flashcard\n"
                        "• `!question` → I’ll quiz you with a random card\n"
                        "• `!answer` → Reveal the answer to the last question\n"
                    )

                elif name == "bookmark":
                    await new_channel.send(
                        "**🔖 This is your Bookmark Vault**\n\n"
                        "React with ⭐ to any of my messages in other channels and I’ll save them here for you to review later!"
                    )

                elif name == "flashcard-deck":
                    await new_channel.send(
                        "**📂 Flashcard Deck**\n\n"
                        "This channel shows every flashcard added with `!quizme` so you can study as a group.\n"
                        "• Cards are auto-posted here\n"
                        "• Use `!deletecard <number>` to remove one\n"
                        "• Answers are hidden behind spoiler tags (click to reveal)"
                    )

            else:
                print(f"⚠️ Channel '{name}' already exists.")

    except discord.Forbidden:
        print(f"❌ Missing permissions to create category/channel in {guild.name}")
    except Exception as e:
        print(f"⚠️ Unexpected error in {guild.name}: {e}")


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    message = reaction.message
    channel = message.channel

    # Only react to bot messages in specific channels
    if channel.name in ["studybot-chat", "quiz-me"]:
        # Find the #bookmark channel
        bookmark_channel = discord.utils.get(message.guild.text_channels, name="bookmark")
        if bookmark_channel:
            # Copy message content and author
            content = message.content
            author = message.author.display_name
            await bookmark_channel.send(f" **Bookmarked by {user.display_name}:**\n{content}")

# ==== RUN ====
client.run(DISCORD_TOKEN)
