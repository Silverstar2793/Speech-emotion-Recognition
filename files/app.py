import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import speech_recognition as sr
import numpy as np
import librosa
import joblib
import sqlite3

# Set up paths and Flask configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load emotion detection model
model = joblib.load('emotion_model.pkl')

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


# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract features from the audio file
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs, axis=1)

# Function to save the file information and prediction to the database
def save_to_db(file_name, file_path, predicted_emotion):
    conn = sqlite3.connect('uploads.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (file_name, file_path, predicted_emotion)
        VALUES (?, ?, ?)
    ''', (file_name, file_path, predicted_emotion))
    conn.commit()
    conn.close()

@app.route('/demo')
def index():
    return render_template('index.html')

@app.route('/')
def about():
    """
    Render the About Us page.
    """
    return render_template('page2.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the emotion from an audio file.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            # Save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract features and predict emotion
            features = extract_features(file_path)
            prediction = model.predict([features])
            predicted_emotion = prediction[0]

            # Save prediction to database
            save_to_db(filename, file_path, predicted_emotion)

            return jsonify({'emotion': predicted_emotion}), 200
        except Exception as e:
            return jsonify({'error': f'Internal error: {e}'}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400


@app.route('/predictions', methods=['GET'])
def get_predictions():
    """
    Retrieve all predictions.
    """
    try:
        conn = sqlite3.connect('uploads.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, file_name, file_path, predicted_emotion FROM predictions")
        rows = cursor.fetchall()
        conn.close()

        predictions = [
            {'id': row[0], 'file_name': row[1], 'file_path': row[2], 'predicted_emotion': row[3]}
            for row in rows
        ]

        return jsonify(predictions), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch predictions: {e}'}), 500


@app.route('/predictions/<int:prediction_id>', methods=['DELETE'])
def delete_prediction(prediction_id):
    """
    Delete a specific prediction by its ID.
    """
    try:
        conn = sqlite3.connect('uploads.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Prediction {prediction_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to delete prediction: {e}'}), 500


@app.route('/audio_metadata', methods=['POST'])
def audio_metadata():
    """
    Retrieve metadata of an uploaded audio file.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            y, sr = librosa.load(file_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)

            return jsonify({'file_name': filename, 'duration': duration, 'sample_rate': sr}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to process metadata: {e}'}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400
if __name__ == '__main__':
    app.run(debug=True)