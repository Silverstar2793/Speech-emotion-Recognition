from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Database initialization
def create_db():
    conn = sqlite3.connect('uploads.db')
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


# Call this to ensure the database is created
create_db()


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if file is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Simplified emotion prediction logic (replace with your model later)
        emotion = "happy"  # Placeholder for prediction

        # Save to database
        conn = sqlite3.connect('uploads.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO predictions (file_name, file_path, predicted_emotion) VALUES (?, ?, ?)',
                       (file.filename, file_path, emotion))
        conn.commit()
        conn.close()

        return jsonify({"emotion": emotion}), 200

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
