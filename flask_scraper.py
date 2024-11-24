from flask import Flask, jsonify
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Initialize Flask app
app = Flask(__name__)

@app.route('/scrape-audio', methods=['GET'])
def scrape_audio():
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode for server environments
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Initialize the WebDriver using WebDriver Manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the webpage
        url = 'https://carlislechurch.org/sermons/'
        driver.get(url)

        # Get all audio elements with the class 'wp-audio-shortcode'
        audio_elements = driver.find_elements(By.CSS_SELECTOR, 'audio.wp-audio-shortcode')

        # Create a directory to store the downloaded audio files
        if not os.path.exists('sermon_audio'):
            os.makedirs('sermon_audio')

        downloaded_files = []

        # Loop through all found audio elements and download the mp3 files
        for i, audio in enumerate(audio_elements):
            audio_src = audio.get_attribute('src')
            # Check if the src attribute contains an .mp3 file
            if audio_src and ".mp3" in audio_src:
                # Download the mp3 file
                response = requests.get(audio_src)
                if response.status_code == 200:
                    file_name = f"sermon_audio/sermon_{i+1}.mp3"
                    with open(file_name, 'wb') as file:
                        file.write(response.content)
                    downloaded_files.append(file_name)
                else:
                    print(f"Failed to download {audio_src}")

        # Quit the WebDriver
        driver.quit()

        # Return the list of downloaded files as JSON
        return jsonify({"status": "success", "downloaded_files": downloaded_files})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
