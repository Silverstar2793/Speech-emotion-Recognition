# **Speech Emotion Recognition **

## **Overview**
This project focuses on building a Speech Emotion Recognition (SER) system that identifies the emotional state of a speaker from audio input. 
By leveraging machine learning and audio processing techniques, the system classifies emotions such as:

'01': 'neutral', 
'02': 'calm', 
'03': 'happy',
'04': 'sad',
'05': 'angry',
'06': 'fearful',
'07': 'disgust',
'08': 'surprised'

## **Features**
- Extract features from speech using `librosa`.
- Train machine learning models using `scikit-learn`.
- Perform real-time speech emotion recognition with `SpeechRecognition` and `PyAudio`.
- Use a lightweight Python web framework that helps developers build web applications 'Flask'
---

## **Technologies Used**
- **Programming Language**: Python
- **Libraries**:
  - [Flask](https://flask.palletsprojects.com/) – For building the web interface (if applicable).
  - [Librosa](https://librosa.org/) – For audio processing and feature extraction.
  - [Scikit-learn](https://scikit-learn.org/) – For machine learning and model training.
  - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) – For speech-to-text and microphone input.
  - [PyAudio](https://pypi.org/project/PyAudio/) – For audio input/output.

---

## **Project Setup**

### 1. **Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
