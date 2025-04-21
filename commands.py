from openai import OpenAI
from features.motivate import handle_motivate
from features.quiz import handle_quizme, handle_question, handle_answer

openai_client = None  # Will be passed in from main.py

def set_openai_client(client):
    global openai_client
    openai_client = client

# !ask
async def handle_ask(message, user_input):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response.choices[0].message.content
        await message.channel.send(f"📚 Answer:\n{answer}")
    except Exception as e:
        await message.channel.send(f"⚠️ Error: {e}")

# !summarise
async def handle_summarise(message, text):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarise this:\n{text}"}]
        )
        summary = response.choices[0].message.content
        await message.channel.send(f"✅ Summary:\n{summary}")
    except Exception as e:
        await message.channel.send(f"⚠️ Error: {e}")

# !explaincode
async def handle_explaincode(message, code):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Explain what this code does:\n{code}"}]
        )
        explanation = response.choices[0].message.content
        await message.channel.send(f"📖 Explanation:\n{explanation}")
    except Exception as e:
        await message.channel.send(f"⚠️ Error: {e}")
