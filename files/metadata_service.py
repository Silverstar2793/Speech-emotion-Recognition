import os
import librosa
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/audio_metadata', methods=['POST'])
def audio_metadata():
    data = request.get_json()
    file_path = data.get('file_path')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400

    try:
        y, sr = librosa.load(file_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        return jsonify({'file_path': file_path, 'duration': duration, 'sample_rate': sr}), 200
    except Exception as e:
        return jsonify({'error': f'Metadata extraction failed: {e}'}), 500

if __name__ == '__main__':
    app.run(port=5004, debug=True)
