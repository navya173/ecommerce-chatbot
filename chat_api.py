from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime
import openai

app = Flask(__name__)

# Set your Groq API key here
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"

DB_PATH = "ecommerce.db"

# Create conversation table if not exists
def create_conversations_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

create_conversations_table()

# Store message
def store_message(conversation_id, role, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (conversation_id, role, message)
        VALUES (?, ?, ?)
    ''', (conversation_id, role, message))
    conn.commit()
    conn.close()

# Generate a response from LLM (Groq)
def get_llm_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="mixtral-8x7b-32768",  # or use 'llama3-70b-8192'
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error contacting LLM: {str(e)}"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    conversation_id = data.get("conversation_id", f"conv_{datetime.utcnow().timestamp()}")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Store user's message
    store_message(conversation_id, "user", user_message)

    # Get response from LLM
    response = get_llm_response(user_message)

    # Store bot response
    store_message(conversation_id, "assistant", response)

    return jsonify({
        "conversation_id": conversation_id,
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=True)
