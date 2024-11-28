import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('emotion_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # This route should receive the feature data and predict the emotion
    try:
        data = request.json
        features = data.get('features')  # Make sure the features are being passed correctly
        if not features:
            return jsonify({'error': 'No features provided'}), 400

        prediction = model.predict([features])  # Assuming `model` is loaded and ready
        return jsonify({'emotion': prediction[0]}), 200
    except Exception as e:
        return jsonify({'error': f'Error in prediction: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True)

