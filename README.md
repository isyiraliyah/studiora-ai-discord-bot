# Studiora – AI Study Buddy for Discord

**Studiora** is a smart and helpful Discord bot I built to assist students with studying, organizing, and staying motivated. It uses the OpenAI API to answer questions, explain code, summarize notes, and run a custom flashcard system.

When added to a server, the bot sets up dedicated channels for chatting, flashcards, and saving important content. It's a lightweight, real-world tool I made to sharpen my coding skills and help others at the same time.

---

## What It Can Do

- `!ask <question>` — Ask anything, from schoolwork to life advice
- `!summarise <text>` — Get quick summaries of notes or paragraphs
- `!explaincode <code>` — Understand what a block of code does
- `!motivate` — Get a motivational quote
- `!quizme question / answer` — Create flashcards
- `!question` — Receive a random flashcard question
- `!answer` — Reveal the answer to the last flashcard
- `!viewcards` — View all saved flashcards
- `!deletecard <number>` — Delete a specific flashcard
- React to bot messages to automatically save them in the bookmark channel
- `!help` — Show all available commands

---

## Auto-Organized Channels

When the bot joins a server, it creates:

- `#studybot-chat` — General interaction with the bot
- `#quiz-me` — Use all flashcard-related commands here
- `#bookmark` — Messages you react to will be saved here
- `#flashcard-deck` — Feed of all flashcards added via `!quizme`

---

## Tech Stack

- Python
- discord.py (for bot interaction)
- OpenAI API (for intelligent responses)
- Replit (used for 24/7 hosting)
- GitHub (version control)

---

## How to Run It

1. Clone this repository
2. Add your `DISCORD_TOKEN` and `OPENAI_API_KEY`
   - Use a `.env` file or Replit Secrets
3. Run `main.py`

You’ll need a Discord bot token and OpenAI API key.

---

## Why I Made This

I wanted to build a project that combined AI, useful study tools, and clean coding practices. As a computer science student, this project helped me put what I’ve learned into something practical and fun to use.

---

## Built by isyiraliyah
