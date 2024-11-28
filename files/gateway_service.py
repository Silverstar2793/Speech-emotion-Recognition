from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Microservices URLs (replace with the correct URLs of your services)
FILE_SERVICE_URL = 'http://127.0.0.1:5001'  # File service URL
FEATURE_SERVICE_URL = 'http://127.0.0.1:5002'  # Feature extraction service URL
PREDICTION_SERVICE_URL = 'http://127.0.0.1:5003'  # Prediction service URL
DB_SERVICE = 'http://127.0.0.1:5005'

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the gateway service!'})

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    file = request.files['file']

    try:
        # Step 1: Forward file to file service
        files = {'file': file}
        file_response = requests.post(f"{FILE_SERVICE_URL}/upload", files=files)
        file_response.raise_for_status()  # Will raise an exception if the status is not 2xx
        file_path = file_response.json()['file_path']  # Adjust this if file service sends a different response

        # Step 2: Feature extraction
        feature_response = requests.post(f"{FEATURE_SERVICE_URL}/extract", json={'file_path': file_path})
        feature_response.raise_for_status()
        features = feature_response.json()['features']

        # Step 3: Prediction
        prediction_response = requests.post(f"{PREDICTION_SERVICE_URL}/predict", json={'features': features})
        prediction_response.raise_for_status()
        emotion = prediction_response.json()['emotion']

        return jsonify({'emotion': emotion}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Error in processing request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)  # Gateway service runs on port 5000
