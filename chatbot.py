import sqlite3
import datetime

# DATABASE SETUP
conn = sqlite3.connect("chatbot.db")   # creates a file "chatbot.db"
cursor = conn.cursor()

# Create table for storing chat logs
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    bot_response TEXT,
    timestamp TEXT
)
''')
conn.commit()


# CHATBOT LOGIC
def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! Thanks for asking."
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a nice day 😊"
    elif "help" in user_input:
        return "Sure! I can answer FAQs like working hours, services, etc."
    else:
        return "Sorry, I didn’t understand that. Can you rephrase?"

# CHAT LOOP + STORE HISTORY
print("🤖 Chatbot: Hi, I'm your assistant. Type 'bye' to exit.")
while True:
    user_text = input("You: ")
    bot_reply = chatbot_response(user_text)
    print("🤖 Chatbot:", bot_reply)

    # Store in database
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO chat_history (user_input, bot_response, timestamp) VALUES (?, ?, ?)",
                   (user_text, bot_reply, timestamp))
    conn.commit()
    
    if "bye" in user_text.lower() or "exit" in user_text.lower():
        break

# Close DB connection
conn.close()