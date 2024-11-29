from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

MODEL_PATH = 'emotion_model.pkl'
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'features' not in data:
        return jsonify({"error": "features not provided"}), 400

    try:
        features = np.array(data['features']).reshape(1, -1)
        emotion = model.predict(features)[0]
        return jsonify({"emotion": emotion}), 200
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
