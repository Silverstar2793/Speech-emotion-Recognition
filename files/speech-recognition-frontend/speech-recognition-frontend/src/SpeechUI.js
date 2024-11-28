import React, { useState } from 'react';
import axios from 'axios';

const SpeechUI = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState('');

  // Handle file input change
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle file upload
  const handleFileUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Replace with your backend API URL
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setPrediction(response.data.emotion); // Update the predicted emotion
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container d-flex flex-column align-items-center mt-5">
      <h1 className="text-center mb-4">Emotion Prediction from Audio</h1>
      <input
        type="file"
        className="form-control mb-3"
        onChange={handleFileChange}
      />
      <button
        className="btn btn-primary"
        onClick={handleFileUpload}
        disabled={loading}
      >
        {loading ? 'Uploading...' : 'Upload File'}
      </button>
      {prediction && <h3 className="mt-4">Predicted Emotion: {prediction}</h3>}
    </div>
  );
};

export default SpeechUI;
