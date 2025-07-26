import sqlite3

def create_conversation_tables():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    # Table to track conversations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table to track messages in each conversation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            sender TEXT,
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Conversation schema created.")

# Run this function
if __name__ == "__main__":
    create_conversation_tables()
