from flask import Flask, jsonify, request
from requests_html import HTMLSession

app = Flask(__name__)

def scrape_audio():
    try:
        # Create a session using requests-html
        session = HTMLSession()

        # Open the webpage
        url = 'https://carlislechurch.org/sermons/'
        response = session.get(url)

        # Render JavaScript (if necessary)
        response.html.render()

        # Find all audio elements with the class 'wp-audio-shortcode'
        audio_elements = response.html.find('audio.wp-audio-shortcode')

        audio_files = []

        # Loop through all found audio elements and download the mp3 files
        for audio in audio_elements:
            audio_src = audio.attrs.get('src')
            if audio_src and ".mp3" in audio_src:
                # Normalize the audio URL
                audio_url = audio_src if audio_src.startswith('http') else f'https://carlislechurch.org{audio_src}'
                audio_files.append(audio_url)

        return {"status": "success", "audio_files": audio_files}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/scrape-audio', methods=['GET'])
def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    result = scrape_audio()
    return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
