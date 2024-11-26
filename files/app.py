import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import speech_recognition as sr
import numpy as np
import librosa
import joblib
import sqlite3

# Set up paths
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load emotion detection model
model = joblib.load('emotion_model.pkl')


# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to extract features from the audio file
def extract_features(file_path):
    # Load audio file and extract features (e.g., MFCCs)
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs, axis=1)


# Function to save the file information and prediction to the database
def save_to_db(file_name, file_path, predicted_emotion):
    conn = sqlite3.connect('uploads.db')
    cursor = conn.cursor()

    # Insert file and prediction into the database
    cursor.execute('''
        INSERT INTO predictions (file_name, file_path, predicted_emotion)
        VALUES (?, ?, ?)
    ''', (file_name, file_path, predicted_emotion))

    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract features from the audio file
        features = extract_features(file_path)
        prediction = model.predict([features])
        predicted_emotion = prediction[0]  # Use the predicted label directly

        # Save the file and prediction result to the database
        save_to_db(filename, file_path, predicted_emotion)

        return jsonify({'emotion': predicted_emotion})
    else:
        return jsonify({'error': 'Invalid file format'})


if __name__ == '__main__':
    app.run(debug=True)
