from flask import Flask, jsonify, request
from requests_html import HTMLSession

app = Flask(__name__)

def scrape_audio():
    try:
        # Create a session using requests-html
        session = HTMLSession()
        all_audio_files = []
        # Open the webpage
        scraping_urls = ["https://carlislechurch.org/sermons/"]
        for i in range(2, (1 + num_pages)):
            new_scraping_url = f"https://carlislechurch.org/sermons/page/{i}/"
            scraping_urls.append(new_scraping_url)
        for cur_scraping_url in scraping_urls:
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
            for cur_file in audio_files:
                all_audio_files.append(current_file)
        return {"audio_files": audio_files}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/scrape-audio', methods=['GET'])
def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    if request.method == "GET":
        num_pages_to_scrape = request.args.get("pages")
        result = scrape_audio(int(num_pages_to_scrape))
        return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
