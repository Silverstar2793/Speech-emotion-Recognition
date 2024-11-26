import sqlite3

def create_db():
    conn = sqlite3.connect('uploads.db')
    cursor = conn.cursor()

    # Create a table for storing file information and predictions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            predicted_emotion TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Call this function when the app starts to ensure the database is created
create_db()
