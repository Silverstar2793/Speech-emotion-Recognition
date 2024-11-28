import unittest
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_file_upload_and_prediction(self):
        # Create a mock audio file for testing
        with open('test_audio.wav', 'wb') as f:
            f.write(b'Test audio content')  # Mocked file content

        # Upload the file and test response
        with open('test_audio.wav', 'rb') as f:
            response = self.app.post('/predict', data={'file': f})
            self.assertEqual(response.status_code, 200)
            self.assertIn('emotion', response.json)

    def test_no_file_uploaded(self):
        # Test case for missing file in the upload
        response = self.app.post('/predict', data={})  # No file uploaded
        self.assertEqual(response.status_code, 400)  # Expecting "Bad Request" status
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "No file part")  # Check error message


if __name__ == '__main__':
    unittest.main()
