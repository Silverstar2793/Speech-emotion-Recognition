from flask import Flask, request, jsonify, render_template
import os
import sqlite3
import librosa
import numpy as np
import pickle

app = Flask(__name__, template_folder='templates')  # Specify the folder containing index.html
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MODEL_PATH = 'emotion_model.pkl'
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

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

create_db()

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        features = extract_features(file_path).reshape(1, -1)
        emotion = model.predict(features)[0]

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
