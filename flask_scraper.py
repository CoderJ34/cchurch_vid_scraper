from flask import Flask, jsonify
import os
import requests
from playwright.sync_api import sync_playwright

# Initialize Flask app
app = Flask(__name__)

@app.route('/scrape-audio', methods=['GET'])
def scrape_audio():
    try:
        # Start Playwright in headless mode
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # You can also use p.firefox or p.webkit
            page = browser.new_page()

            # Open the webpage
            url = 'https://carlislechurch.org/sermons/'
            page.goto(url)

            # Get all audio elements with the class 'wp-audio-shortcode'
            audio_elements = page.query_selector_all('audio.wp-audio-shortcode')

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

            # Close the browser
            browser.close()

        # Return the list of downloaded files as JSON
        return jsonify({"status": "success", "downloaded_files": downloaded_files})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
