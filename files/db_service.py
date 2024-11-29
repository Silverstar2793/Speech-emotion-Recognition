from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = 'uploads.db'

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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

create_db()

@app.route('/store', methods=['POST'])
def store():
    data = request.json
    if not all(k in data for k in ('file_name', 'file_path', 'predicted_emotion')):
        return jsonify({"error": "Missing fields"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO predictions (file_name, file_path, predicted_emotion) VALUES (?, ?, ?)',
                       (data['file_name'], data['file_path'], data['predicted_emotion']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": f"Error storing data: {str(e)}"}), 500

@app.route('/history', methods=['GET'])
def history():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM predictions')
        rows = cursor.fetchall()
        conn.close()
        return jsonify({"data": rows}), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching history: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5004)
