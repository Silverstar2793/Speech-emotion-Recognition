import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Gateway service URL
GATEWAY_URL = 'http://127.0.0.1:5005'


@app.route('/')
def index():
    """
    Render the main page.
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle audio prediction requests by forwarding them to the gateway service.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Forward the file to the gateway service
        files = {'file': file}
        response = requests.post(f"{GATEWAY_URL}/process_audio", files=files)

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': response.json()}), response.status_code

    except Exception as e:
        return jsonify({'error': f"Internal error: {e}"}), 500


@app.route('/audio_metadata', methods=['POST'])
def audio_metadata():
    """
    Handle audio metadata requests by forwarding them to the gateway service.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Forward the file to the gateway service for metadata processing
        files = {'file': file}
        response = requests.post(f"{GATEWAY_URL}/audio_metadata", files=files)

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': response.json()}), response.status_code

    except Exception as e:
        return jsonify({'error': f"Internal error: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
