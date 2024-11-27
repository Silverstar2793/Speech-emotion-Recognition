from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Paths
driver_path = r'F:/Speech-emotion-Recognition/files/geckodriver.exe'
file_path = r'C:\Users\Megha\Downloads\Real-Time-Speech-Emotion-Recognition-master (1)\Real-Time-Speech-Emotion-Recognition-master\Dataset\speech-emotion-recognition-ravdess-data\Actor_24\03-01-02-02-01-02-24.wav'

# Setup WebDriver
service = Service(driver_path)
driver = webdriver.Firefox(service=service)

try:
    driver.get("http://127.0.0.1:5000/")

    # Upload file
    print("Uploading file")
    file_input = driver.find_element(By.NAME, 'file')
    file_input.send_keys(file_path)

    # Submit form
    print("Clicking submit button")
    submit_button = driver.find_element(By.TAG_NAME, 'button')
    submit_button.click()

    # Wait for the page to process and render result
    print("Waiting for prediction result")
    time.sleep(45)  # Adding more time to wait for the result

    # Try to retrieve emotion result
    emotion_result = driver.find_element(By.ID, 'emotionResult')

    # Print the result if found
    if emotion_result:
        print(f"Emotion Prediction: {emotion_result.text}")
    else:
        print("Error: Emotion prediction result was not found.")
        print("Page Source for Debugging:")
        print(driver.page_source)  # Print the entire page source for debugging

except Exception as e:
    print(f"An error occurred during testing: {e}")

finally:
    print("Closing the driver")
    driver.quit()
