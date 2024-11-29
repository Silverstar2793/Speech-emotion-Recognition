from flask import Flask, request, jsonify, render_template
import os
import sqlite3
import librosa
import numpy as np
import pickle

# Initialize Flask app and configurations
app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load pre-trained model
MODEL_PATH = 'emotion_model.pkl'
if not os.path.exists(MODEL_PATH):
    print(f"Error: Model file not found at {MODEL_PATH}")
else:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully.")

# SQLite database setup
def create_db():
    """Create SQLite database and table if they do not exist."""
    conn = sqlite3.connect('uploads.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_path TEXT,
            predicted_emotion TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_db()

# Feature extraction function
def extract_features(audio_path):
    """Extract MFCC features from an audio file."""
    try:
        y, sr = librosa.load(audio_path, sr=16000)  # Load audio with 16 kHz sample rate
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Compute MFCC features
        return np.mean(mfcc.T, axis=0)  # Take mean of MFCC coefficients
    except Exception as e:
        print(f"Error extracting features from {audio_path}: {e}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('page2.html')  # Serve the HTML file

@app.route('/demo')
def demo():
    """Serve the HTML file for uploading files."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle audio file upload, feature extraction, prediction, and database storage."""
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract features and predict emotion
        features = extract_features(file_path)
        if features is None:
            return jsonify({"error": "Feature extraction failed"}), 400

        features = features.reshape(1, -1)  # Reshape for model input
        emotion = model.predict(features)[0]  # Predict emotion

        # Store prediction in SQLite database
        try:
            conn = sqlite3.connect('uploads.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO predictions (file_name, file_path, predicted_emotion) VALUES (?, ?, ?)',
                (file.filename, file_path, emotion)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error inserting into the database: {e}")
            return jsonify({"error": "Database insertion failed"}), 500

        # Respond with prediction results
        return jsonify({
            "file_name": file.filename,
            "file_path": file_path,
            "predicted_emotion": emotion
        }), 200

    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Main block to run the app
if __name__ == '__main__':
    app.run(debug=True)
