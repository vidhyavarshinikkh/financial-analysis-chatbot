from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

print("DEBUG:", api_key)

client = Groq(api_key="YOUR-GROK-API-KEY")


# Load financial data
df = pd.read_csv("financial.csv")

# Store conversation history
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    try:
        user_message = request.json["message"]

        # Save user message
        chat_history.append(f"User: {user_message}")

        # Last 10 messages for memory
        history_text = "\n".join(chat_history[-10:])

        context = f"""
You are FinBot, an intelligent financial analysis assistant.

Available Financial Data:
{df.to_string(index=False)}

Instructions:
- Respond naturally like ChatGPT.
- Answer greetings naturally.
- If the user asks financial questions, use the provided data.
- If the question is outside the data, answer politely.
- Compare companies when requested.
- Provide insights instead of only raw numbers.
- Maintain conversational context.
- Be professional but friendly.

Conversation History:
{history_text}
"""

        prompt = f"""
{context}

User Question:
{user_message}
"""

        chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
        model="llama-3.3-70b-versatile",
)

        bot_response = chat_completion.choices[0].message.content

        # Save bot response
        chat_history.append(f"Bot: {bot_response}")

        return jsonify({
            "response": bot_response
        })

    except Exception as e:

        return jsonify({
            "response": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)

