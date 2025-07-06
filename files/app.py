from flask import Flask, request, jsonify, render_template
import os
import sqlite3
import librosa
import numpy as np
import pickle
import boto3  # For AWS S3 interaction
from dotenv import load_dotenv  # To manage environment variables

# Initialize Flask app and configurations
app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load environment variables
load_dotenv()  # This loads variables from a .env file

# AWS S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("AWS_REGION")
S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=S3_REGION
)

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
            predicted_emotion TEXT,
            s3_url TEXT  -- Add a column to store the S3 file URL
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

        # Save the uploaded file locally
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Upload file to AWS S3
        try:
            s3_key = file.filename  # Use the filename as the key in S3
            S3_CLIENT.upload_file(
                Filename=file_path,
                Bucket=S3_BUCKET,
                Key=s3_key
            )
            # Generate the S3 file URL
            s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return jsonify({"error": "Failed to upload file to cloud storage"}), 500

        # Extract features and predict emotion
        features = extract_features(file_path)
        if features is None:
            return jsonify({"error": "Feature extraction failed"}), 400

        features = features.reshape(1, -1)  # Reshape for model input
        emotion = model.predict(features)[0]  # Predict emotion

        # Store prediction in SQLite database, including S3 URL
        try:
            conn = sqlite3.connect('uploads.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO predictions (file_name, file_path, predicted_emotion) VALUES (?, ?, ?, ?)',
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
            "predicted_emotion": emotion,
             # Include the S3 URL in the response
        }), 200

    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Main block to run the app
if __name__ == '__main__':
    app.run(debug=True)
