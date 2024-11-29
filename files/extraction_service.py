from flask import Flask, request, jsonify
import librosa
import numpy as np

app = Flask(__name__)

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0).tolist()

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    if 'file_path' not in data:
        return jsonify({"error": "file_path not provided"}), 400

    try:
        features = extract_features(data['file_path'])
        return jsonify({"features": features}), 200
    except Exception as e:
        return jsonify({"error": f"Error extracting features: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
