from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, template_folder='templates')  # Use the 'templates' folder for HTML files

# Service URLs
UPLOAD_SERVICE_URL = "http://localhost:5001/upload"
EXTRACTION_SERVICE_URL = "http://localhost:5002/extract"
PREDICTION_SERVICE_URL = "http://localhost:5003/predict"
DATABASE_SERVICE_URL = "http://localhost:5004/store"

# Routes to render the HTML pages
@app.route('/')
def home():
    return render_template('page2.html')  # Serve the original page2.html

@app.route('/demo')
def demo():
    return render_template('index.html')  # Serve the original index.html

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Step 1: Upload file
        upload_response = requests.post(UPLOAD_SERVICE_URL, files={'file': file})
        if upload_response.status_code != 200:
            return jsonify({"error": "Error in file upload"}), 500
        
        upload_data = upload_response.json()
        file_path = upload_data.get("file_path")
        file_name = file.filename

        # Step 2: Extract features
        extract_response = requests.post(EXTRACTION_SERVICE_URL, json={"file_path": file_path})
        if extract_response.status_code != 200:
            return jsonify({"error": "Error in feature extraction"}), 500

        features = extract_response.json().get("features")

        # Step 3: Predict emotion
        predict_response = requests.post(PREDICTION_SERVICE_URL, json={"features": features})
        if predict_response.status_code != 200:
            return jsonify({"error": "Error in prediction"}), 500

        emotion = predict_response.json().get("emotion")

        # Step 4: Store in database
        store_response = requests.post(DATABASE_SERVICE_URL, json={
            "file_name": file_name,
            "file_path": file_path,
            "predicted_emotion": emotion
        })
        if store_response.status_code != 200:
            return jsonify({"error": "Error storing prediction"}), 500

        # Final response
        return jsonify({
            "file_name": file_name,
            "file_path": file_path,
            "predicted_emotion": emotion
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
