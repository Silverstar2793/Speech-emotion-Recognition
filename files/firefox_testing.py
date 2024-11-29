from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Setup WebDriver (assuming Firefox for this example)
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

try:
    print("Opening demo page...")
    driver.get("http://127.0.0.1:5000/demo")  # Replace with your actual URL

    # Wait for page to load and ensure that the file input is available
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fileInput")))

    # Upload file
    print("Uploading file...")
    file_input = driver.find_element(By.ID, "fileInput")
    file_input.send_keys(r'C:\Users\Megha\Downloads\Real-Time-Speech-Emotion-Recognition-master (1)\Real-Time-Speech-Emotion-Recognition-master\Dataset\speech-emotion-recognition-ravdess-data\Actor_24\03-01-07-02-01-02-24.wav') # Replace with the path to your file

    # Wait for audio preview section to show up
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "audioPreview")))

    # Wait for the file to be uploaded and ready for submission
    print("Waiting before submitting...")
    time.sleep(2)  # Add a sleep here to simulate waiting

    # Scroll to the submit button and wait for it to be clickable
    print("Clicking submit button...")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    # Scroll to the submit button if it's out of view
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)

    # Wait until the submit button is clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )

    # Click the submit button
    submit_button.click()

    # Wait for the result
    print("Waiting for result...")
    WebDriverWait(driver, 50).until(
        EC.visibility_of_element_located((By.ID, "emotionResult"))
    )

    # Retrieve and print the emotion result
    emotion_result = driver.find_element(By.ID, "emotionResult")
    print("Emotion prediction result:", emotion_result.text)

    # Allow time to see the result
    time.sleep(20)

except Exception as e:
    print(f"An error occurred during testing: {e}")
    # You can capture the page source for debugging if needed
    with open("debug_page_source.html", "w") as file:
        file.write(driver.page_source)
    print("Page Source for Debugging saved.")

finally:
    print("Closing the driver..")
    driver.quit()
