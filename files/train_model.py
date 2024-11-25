import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle


def load_data(path_to_dataset):
    """
    Load the dataset and extract features for emotion detection.
    """
    data = []
    labels = []
    emotions = {
        '01': 'neutral', '02': 'calm', '03': 'happy', '04': 'sad',
        '05': 'angry', '06': 'fearful', '07': 'disgust', '08': 'surprised'
    }

    # Traverse dataset directory
    for subdir, _, files in os.walk(path_to_dataset):
        for file in files:
            if file.endswith(".wav"):
                try:
                    # File path
                    audio_path = os.path.join(subdir, file)
                    print(f"Processing file: {audio_path}")

                    # Extract emotion from filename
                    parts = file.split("-")
                    emotion_code = parts[2]  # Adjust this based on your filename format
                    emotion = emotions.get(emotion_code)

                    if emotion:
                        labels.append(emotion)

                        # Load audio file
                        y, sr = librosa.load(audio_path, sr=16000)
                        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                        features = np.mean(mfcc.T, axis=0)
                        data.append(features)
                    else:
                        print(f"No valid emotion code for file: {file}")
                except Exception as e:
                    print(f"Error processing file {file}: {e}")

    return np.array(data), np.array(labels)


def train_and_save_model(data, labels, model_path):
    """
    Train a Random Forest Classifier and save the model.
    """
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    # Path to the dataset
    dataset_path = r'C:\Users\Megha\Downloads\Real-Time-Speech-Emotion-Recognition-master (1)\Real-Time-Speech-Emotion-Recognition-master\Dataset\speech-emotion-recognition-ravdess-data'

    # Load data
    data, labels = load_data(dataset_path)
    print(f"Data shape: {data.shape}, Labels count: {len(labels)}")

    if data.size > 0 and len(labels) > 0:
        # Train and save model
        model_path = r'C:\Users\Megha\PycharmProjects\pythonProject6\emotion_model.pkl'
        train_and_save_model(data, labels, model_path)
    else:
        print("No data or labels found. Check the dataset.")
