import unittest
from app import app
from unittest.mock import patch
import numpy as np
import os


class TestApp(unittest.TestCase):
    def setUp(self):
        # Setup the test client for Flask
        self.app = app.test_client()
        self.app.testing = True

    @patch('librosa.load')
    def test_file_upload_and_prediction(self, mock_load):
        # Mock the return value of librosa.load to avoid actual audio file processing
        mock_load.return_value = (np.zeros(16000), 16000)  # Mocking a 1-second audio clip at 16kHz

        # Create a mock audio file for testing
        with open('test_audio.wav', 'wb') as f:
            f.write(b'Valid audio content')  # This is mocked content

        # Upload the mock audio file and test the response
        with open('test_audio.wav', 'rb') as f:
            response = self.app.post('/predict', data={'file': f})
            self.assertEqual(response.status_code, 200)
            self.assertIn('predicted_emotion', response.json)  # Ensure the response contains 'predicted_emotion'

    def test_no_file_uploaded(self):
        # Test case for missing file in the upload
        response = self.app.post('/predict', data={})  # No file uploaded
        self.assertEqual(response.status_code, 400)  # Expecting "Bad Request" status
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "No file part")  # Check the error message

    def tearDown(self):
        # Cleanup: Remove the mock audio file if it exists
        if os.path.exists('test_audio.wav'):
            os.remove('test_audio.wav')


if __name__ == '__main__':
    unittest.main()
