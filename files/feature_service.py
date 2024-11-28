import os
import numpy as np
import librosa
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/extract_features', methods=['POST'])
def extract_features():
    data = request.get_json()
    file_path = data.get('file_path')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400

    try:
        y, sr = librosa.load(file_path, sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features = np.mean(mfccs, axis=1).tolist()
        return jsonify({'features': features}), 200
    except Exception as e:
        return jsonify({'error': f'Feature extraction failed: {e}'}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)
