import random

motivational_quotes = [
    "Push yourself, because no one else is going to do it for you.",
    "You don’t have to be great to start, but you have to start to be great.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Dream it. Believe it. Build it.",
    "You are capable of amazing things.",
    "A little progress each day adds up to big results."
]

async def handle_motivate(message):
    quote = random.choice(motivational_quotes)
    await message.channel.send(f"💬 {quote}")
