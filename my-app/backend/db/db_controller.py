import sqlite3
import json

# 🔹 Database file
DB_FILE = "db/ekankik_data.db"

# 🔹 Class to temporarily hold extracted data before database insertion
class TableEntry:
    """Structure for holding extracted data before inserting into SQLite."""
    def __init__(self, question_text, video_url, timestamp, video_date, video_index, video_question_index):
        self.question_text = question_text  # Extracted question
        self.video_url = video_url  # Full YouTube link
        self.timestamp = timestamp  # Timestamp in HH:MM format
        self.video_date = video_date  # Upload date
        self.video_index = video_index  # Unique index of the video
        self.video_question_index = video_question_index  # Index of the question in the video

def setup_database():
    """Drops and recreates the questions table to ensure no duplicate data."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ⚠️ Drop the existing table (reset the database)
    cursor.execute("DROP TABLE IF EXISTS questions")
    
    # Recreate the table
    cursor.execute('''
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT,
            video_url TEXT,
            timestamp TEXT,
            video_date TEXT,
            video_index INTEGER,
            video_question_index INTEGER
        )
    ''')    
    conn.commit()
    conn.close()


# 🔹 Function to insert a single entry into the database
def insert_into_db(entry):
    """Inserts a single TableEntry object into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO questions (question_text, video_url, timestamp, video_date, video_index, video_question_index)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (entry.question_text, entry.video_url, entry.timestamp, entry.video_date, entry.video_index, entry.video_question_index))

    conn.commit()
    conn.close()

# 🔹 Function to search for questions containing a keyword
def search_questions(query):
    """Searches the database for questions containing a given keyword."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT question_text, video_url, timestamp, video_date
        FROM questions
        WHERE question_text LIKE ?
        ORDER BY video_index DESC
    ''', ('%' + query + '%',))

    results = [{"question": row[0], "video_url": row[1], "timestamp": row[2], "video_date": row[3]} for row in cursor.fetchall()]
    conn.close()
    return results

# 🔹 Debug Function: Print all stored data in a readable format
def debug_print():
    """Prints all database entries in a readable format for debugging."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM questions ORDER BY video_index DESC")
    rows = cursor.fetchall()

    print("\n✅ Current Questions in Ekantik_DB:\n")
    
    if not rows:
        print("⚠️ No entries found in the database.")
    else:
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Question: {row[1]}")
            print(f"Video URL: {row[2]}")
            print(f"Timestamp: {row[3]}")
            print(f"Video Date: {row[4]}")
            print(f"Video Index: {row[5]}")
            print(f"Question Index: {row[6]}")
            print("-" * 50)  # Separator for readability
    
    conn.close()
