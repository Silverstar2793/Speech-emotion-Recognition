import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('uploads.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            predicted_emotion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/save_prediction', methods=['POST'])
def save_prediction():
    data = request.get_json()
    file_name = data.get('file_name')
    file_path = data.get('file_path')
    predicted_emotion = data.get('predicted_emotion')

    if not (file_name and file_path and predicted_emotion):
        return jsonify({'error': 'Missing data'}), 400

    try:
        conn = sqlite3.connect('uploads.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (file_name, file_path, predicted_emotion)
            VALUES (?, ?, ?)
        ''', (file_name, file_path, predicted_emotion))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Prediction saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to save prediction: {e}'}), 500

if __name__ == '__main__':
    app.run(port=5005, debug=True)
