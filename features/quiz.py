import random
import discord

# Stores all flashcards
flashcards = []

# Stores the last question asked per user
last_question_by_user = {}

async def handle_quizme(message, content):
    parts = content.split("/")
    if len(parts) != 2:
        await message.channel.send("⚠️ Use the format: `!quizme question / answer`")
        return

    question = parts[0].strip()
    answer = parts[1].strip()
    flashcards.append({"question": question, "answer": answer})

    await message.channel.send(f"✅ Flashcard added:\n**Q:** {question}\n**A:** {answer}")

    # Also post to the flashcard-deck channel if it exists
    deck_channel = discord.utils.get(message.guild.text_channels, name="flashcard-deck")
    if deck_channel:
        await deck_channel.send(
            f"🆕 **Flashcard Added** by {message.author.display_name}:\n"
            f"**Q:** {question}\n"
            f"**A:** ||{answer}||"
        )

async def handle_question(message):
    if not flashcards:
        await message.channel.send("❌ No flashcards yet! Use `!quizme question | answer` to add one.")
        return

    flashcard = random.choice(flashcards)
    last_question_by_user[message.author.id] = flashcard  # Save which question was sent to this user
    await message.channel.send(f"❓ {flashcard['question']}")

async def handle_answer(message):
    flashcard = last_question_by_user.get(message.author.id)
    if not flashcard:
        await message.channel.send("❌ No question asked yet! Use `!question` first.")
        return

    await message.channel.send(f"✅ Answer: {flashcard['answer']}")

async def handle_viewcards(message):
    if not flashcards:
        await message.channel.send("📭 You haven't added any flashcards yet.")
        return

    msg = "**🗂️ Your Flashcards:**\n"
    for i, card in enumerate(flashcards, 1):
        msg += f"`{i}.` {card['question']} → ||{card['answer']}||\n"

    await message.channel.send(msg)


async def handle_deletecard(message, index_text):
    if not flashcards:
        await message.channel.send("📭 No flashcards to delete.")
        return

    try:
        index = int(index_text.strip()) - 1
        if index < 0 or index >= len(flashcards):
            raise IndexError

        removed = flashcards.pop(index)
        await message.channel.send(f"🗑️ Removed card:\n**Q:** {removed['question']}")
    except (ValueError, IndexError):
        await message.channel.send("⚠️ Please use: `!deletecard <number>`\nCheck `!viewcards` to see the list.")

